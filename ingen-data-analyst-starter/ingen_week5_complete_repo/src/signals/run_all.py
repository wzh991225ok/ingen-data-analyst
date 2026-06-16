"""Run the full Week 5 demand-signal pipeline end-to-end.

Usage:
    python -m src.signals.run_all                      # offline fallbacks (default)
    INGEST_ALLOW_NETWORK=1 python -m src.signals.run_all   # live Google Trends + GDELT

Order: search interest -> news (volume+tone) -> voice-of-customer -> demand index.
Then run build_reports.py for the taxonomy markdown, charts, and methodology PDF.
"""
from . import base
from . import google_trends, gdelt_news, voc_reviews, demand_index


def main():
    base.reset_manifest()
    print(f"Week 5 demand signals @ {base.TODAY} (network={'ON' if base.ALLOW_NETWORK else 'OFF — offline fallbacks'})")
    print("[1/4] Search interest (Google Trends)")
    google_trends.collect()
    print("[2/4] News cadence & sentiment (GDELT)")
    gdelt_news.collect()
    print("[3/4] Voice-of-customer (review topic modelling)")
    voc_reviews.mine()
    print("[4/4] Demand-signal index")
    demand_index.build()
    print(f"\nDone. Manifest: {base.MANIFEST.relative_to(base.ROOT)}")


if __name__ == "__main__":
    main()
