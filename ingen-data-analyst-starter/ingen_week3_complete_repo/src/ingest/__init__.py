"""Reusable public-data ingestion package (Week 3).

Each module downloads one public dataset (real API documented), hashes the raw file
for versioning, applies cleaning standards, saves clean CSV/parquet, and records a
manifest row. See datasets.py for the 12 sources and base.py for shared utilities.

Run all:  python -m src.ingest.run_all
"""
from .datasets import ALL_LOADERS  # noqa: F401
