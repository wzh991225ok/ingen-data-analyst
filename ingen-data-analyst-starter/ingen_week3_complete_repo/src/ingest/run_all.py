"""Run all 12 ingestion modules end-to-end.

Usage:
    python -m src.ingest.run_all              # offline fallbacks (default)
    INGEST_ALLOW_NETWORK=1 python -m src.ingest.run_all   # real public APIs

Clears the manifest first, then runs each loader and prints a one-line summary.
"""
from __future__ import annotations
from . import base
from .datasets import ALL_LOADERS


def main():
    # fresh manifest each run
    if base.MANIFEST.exists():
        base.MANIFEST.unlink()
    print(f"Ingest run @ {base.TODAY}  (network={'ON' if base.ALLOW_NETWORK else 'OFF — offline fallbacks'})")
    ok = 0
    for fn in ALL_LOADERS:
        try:
            p = fn()
            ok += 1
            print(f"  ✓ {fn.__name__:30s} -> {p.relative_to(base.ROOT)}")
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ {fn.__name__:30s} FAILED: {e}")
    print(f"Done: {ok}/{len(ALL_LOADERS)} datasets ingested. Manifest: {base.MANIFEST.relative_to(base.ROOT)}")


if __name__ == "__main__":
    main()
