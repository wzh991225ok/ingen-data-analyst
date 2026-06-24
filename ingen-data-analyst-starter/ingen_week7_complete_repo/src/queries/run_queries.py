"""Run the 15 reference queries against the warehouse and confirm each runs without error.

Run:  python -m src.queries.run_queries          # summary (pass/fail + row counts)
      python -m src.queries.run_queries --show    # also print first rows of each
"""
from __future__ import annotations
import sys, re
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "data" / "week07" / "ingen_warehouse.duckdb"
SQL = ROOT / "src" / "queries" / "reference_queries.sql"


def split_queries(text):
    # split on ';' at end of line, keep comment header preceding each query as its label
    chunks, buf = [], []
    for line in text.splitlines():
        buf.append(line)
        if line.strip().endswith(";"):
            chunks.append("\n".join(buf)); buf = []
    out = []
    for c in chunks:
        if not c.strip() or all(l.strip().startswith("--") for l in c.splitlines()):
            continue
        m = re.search(r"--\s*(Q\d+.*)", c)
        label = m.group(1).strip() if m else c.strip()[:60]
        out.append((label, c))
    return out


def main(show=False):
    con = duckdb.connect(str(DB), read_only=True)
    qs = split_queries(SQL.read_text())
    print(f"Running {len(qs)} reference queries against {DB.name}\n")
    passed = 0
    for label, q in qs:
        try:
            df = con.execute(q).fetchdf()
            passed += 1
            print(f"  [OK]  {label}  -> {len(df)} rows")
            if show:
                print(df.head(5).to_string(index=False), "\n")
        except Exception as e:  # noqa: BLE001
            print(f"  [FAIL] {label}: {e}")
    con.close()
    print(f"\n{passed}/{len(qs)} queries ran without error.")
    return passed == len(qs)


if __name__ == "__main__":
    ok = main(show="--show" in sys.argv)
    sys.exit(0 if ok else 1)
