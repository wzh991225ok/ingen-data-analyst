"""Shared utilities for the Week 5 demand-signal pipeline.

Pattern mirrors Week 3: every collector either fetches the real public source
(when INGEST_ALLOW_NETWORK=1 and the host is reachable) or falls back to a
clearly-labelled, schema-correct synthetic sample so the whole pipeline,
topic modelling, and index all run end-to-end without network. Each run records
a manifest line noting the mode (network vs offline-fallback) per source, so a
reviewer always knows what is real and what is a placeholder.

Verticals (InGen anchor products):
  eldercare -> Fari   education -> Senpai   indoor_security -> Sentinel Prime AI
  outdoor_patrol -> Aido Rover   humanoid -> Aido Humanoid
"""
from __future__ import annotations
import os, json, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "week05"
REPORTS = ROOT / "reports" / "week05"
MANIFEST = DATA / "signal_manifest.jsonl"
for d in (DATA, REPORTS):
    d.mkdir(parents=True, exist_ok=True)

TODAY = datetime.date.today().isoformat()
ALLOW_NETWORK = os.environ.get("INGEST_ALLOW_NETWORK", "0") == "1"

# Vertical -> (InGen product, curated keywords for search/news)
VERTICALS = {
    "eldercare":        ("Fari",              ["eldercare robot", "companion robot", "elderly care robot"]),
    "education":        ("Senpai",            ["educational robot", "classroom robot", "STEM education robot"]),
    "indoor_security":  ("Sentinel Prime AI", ["security robot", "indoor security robot"]),
    "outdoor_patrol":   ("Aido Rover",        ["patrol robot", "surveillance robot", "perimeter security robot"]),
    "humanoid":         ("Aido Humanoid",     ["humanoid robot", "general purpose robot"]),
}


def stable_seed(text: str) -> int:
    """Deterministic seed from a string (independent of PYTHONHASHSEED)."""
    import hashlib
    return int(hashlib.md5(text.encode()).hexdigest()[:8], 16)


def record_manifest(row: dict) -> None:
    row = {"recorded_at": datetime.datetime.now().isoformat(timespec="seconds"), **row}
    with open(MANIFEST, "a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def reset_manifest() -> None:
    if MANIFEST.exists():
        MANIFEST.unlink()


def http_get_json(url: str, timeout: int = 30):
    """GET JSON from a URL. Returns parsed JSON or raises."""
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "ingen-intern-signals/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def month_range(n_months: int = 24):
    """Return a list of YYYY-MM strings ending this month, length n_months."""
    today = datetime.date.today().replace(day=1)
    out = []
    y, m = today.year, today.month
    for _ in range(n_months):
        out.append(f"{y:04d}-{m:02d}")
        m -= 1
        if m == 0:
            m = 12; y -= 1
    return list(reversed(out))
