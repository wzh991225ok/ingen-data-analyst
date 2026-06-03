"""Shared utilities for the public-data ingestion pipeline (Week 3).

Every source module uses these helpers to: resolve paths, download a raw file,
hash it (SHA-256) for versioning, record a manifest row, and apply the cleaning
standards in docs/data_standards.md.

Design choices:
- Network access in this environment is restricted, so each module supports an
  OFFLINE FALLBACK: a small, clearly-labelled synthetic sample with the SAME schema,
  so the pipeline, warehouse build, and tests all run end-to-end without network.
  When run in an environment with network access, set INGEST_ALLOW_NETWORK=1 and
  the modules will fetch the real public APIs documented in each module's SOURCE.
- Real API endpoints are documented in each module (Census, BLS, World Bank, etc.)
  so the code is immediately usable for a real pull.
"""
from __future__ import annotations
import os, json, hashlib, datetime, io
from pathlib import Path

# ---- paths ----
ROOT = Path(__file__).resolve().parents[2]          # ingen-data-analyst/
DATA = ROOT / "data" / "week03"
RAW = DATA / "raw"
CLEAN = DATA / "clean"
WAREHOUSE = DATA / "analytics.duckdb"
MANIFEST = DATA / "ingest_manifest.jsonl"
for d in (RAW, CLEAN):
    d.mkdir(parents=True, exist_ok=True)

TODAY = datetime.date.today().isoformat()
ALLOW_NETWORK = os.environ.get("INGEST_ALLOW_NETWORK", "0") == "1"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def write_raw(name: str, content: bytes, ext: str = "csv") -> Path:
    """Write raw bytes to data/week03/raw/<name>.<ext> and return the path."""
    p = RAW / f"{name}.{ext}"
    p.write_bytes(content)
    return p


def record_manifest(row: dict) -> None:
    """Append one JSON line recording a dataset version (source, date, hash, rows...)."""
    row = {"recorded_at": datetime.datetime.now().isoformat(timespec="seconds"), **row}
    with open(MANIFEST, "a") as f:
        f.write(json.dumps(row) + "\n")


def fetch_or_fallback(name: str, url: str, fallback_csv: str, ext: str = "csv"):
    """Fetch (or fall back) AND persist the raw bytes to data/week03/raw/<name>.<ext>.

    Returns (raw_path, mode). mode is 'network' or 'offline-fallback'.
    If INGEST_ALLOW_NETWORK=1, attempt the real fetch; otherwise (or on failure)
    use the provided synthetic fallback CSV string with the same schema.
    """
    raw_bytes = None
    mode = "offline-fallback"
    if ALLOW_NETWORK:
        try:
            import urllib.request
            req = urllib.request.Request(url, headers={"User-Agent": "ingen-intern-ingest/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                raw_bytes = r.read()
                mode = "network"
        except Exception as e:  # noqa: BLE001
            print(f"  [{name}] network fetch failed ({e}); using offline fallback")
    if raw_bytes is None:
        raw_bytes = fallback_csv.encode("utf-8")
    path = write_raw(name, raw_bytes, ext)
    return path, mode


def standard_clean(df, *, rename: dict | None = None, year_col: str | None = None):
    """Apply docs/data_standards.md conventions to a DataFrame.

    - snake_case all column names
    - strip whitespace on object columns
    - coerce a year column to nullable Int
    - leave NULLs as NULL (no sentinel strings)
    """
    import pandas as pd
    df = df.copy()
    if rename:
        df = df.rename(columns=rename)
    df.columns = [str(c).strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].astype("string").str.strip()
        df[c] = df[c].replace({"": pd.NA, "N/A": pd.NA, "n/a": pd.NA, "-": pd.NA})
    if year_col:
        yc = year_col.strip().lower().replace(" ", "_")
        if yc in df.columns:
            df[yc] = pd.to_numeric(df[yc], errors="coerce").astype("Int64")
    return df


def finalize(name: str, df, *, source: str, url: str, vertical: str, mode: str,
             raw_path: Path, license_: str = "Public domain (US govt) / see source") -> Path:
    """Save cleaned parquet+csv, record manifest, return clean csv path."""
    raw_bytes = raw_path.read_bytes()
    clean_csv = CLEAN / f"{name}.csv"
    df.to_csv(clean_csv, index=False)
    try:
        df.to_parquet(CLEAN / f"{name}.parquet", index=False)
    except Exception:
        pass  # parquet optional if pyarrow missing
    record_manifest({
        "dataset": name, "vertical": vertical, "source": source, "url": url,
        "license": license_, "retrieved": TODAY, "mode": mode,
        "raw_path": str(raw_path.relative_to(ROOT)),
        "raw_sha256": sha256_bytes(raw_bytes),
        "rows": int(len(df)), "cols": int(df.shape[1]),
        "columns": list(df.columns),
    })
    return clean_csv
