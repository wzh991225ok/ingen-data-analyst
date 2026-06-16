"""Live SEC EDGAR fetcher — exact quarterly financials for public peers (no API key).

Uses the SEC companyfacts API:
  https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
and pulls the last 12 quarters of Revenues, Gross Profit, R&D, and Operating Income, returning
a tidy DataFrame. Run with INGEST_ALLOW_NETWORK=1 (SEC requires a descriptive User-Agent).

This is the path to filing-exact numbers; peer_data.PUBLIC holds FY2024 anchors used when
network is unavailable. Imported by build_workbook only when ALLOW_NETWORK is set.
"""
from __future__ import annotations
import os, json, urllib.request
import pandas as pd
from .peer_data import PUBLIC_TICKERS_CIK

UA = {"User-Agent": "ingen-intern-research ziheng.wang@example.com"}
TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"],
    "gross_profit": ["GrossProfit"],
    "rnd": ["ResearchAndDevelopmentExpense"],
    "operating_income": ["OperatingIncomeLoss"],
}


def _facts(cik):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))


def _series(facts, tags):
    usgaap = facts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        if tag in usgaap:
            units = usgaap[tag].get("units", {}).get("USD", [])
            rows = [u for u in units if u.get("form") in ("10-Q", "10-K") and u.get("fp")]
            if rows:
                return tag, rows
    return None, []


def fetch_quarters(n_quarters: int = 12) -> pd.DataFrame:
    if os.environ.get("INGEST_ALLOW_NETWORK", "0") != "1":
        raise RuntimeError("Set INGEST_ALLOW_NETWORK=1 to fetch from SEC EDGAR.")
    out = []
    for tk, cik in PUBLIC_TICKERS_CIK.items():
        facts = _facts(cik)
        rev_tag, rev = _series(facts, TAGS["revenue"])
        by_end = {}
        for metric, tags in TAGS.items():
            _, rows = _series(facts, tags)
            for u in rows:
                key = (u.get("end"), u.get("fy"), u.get("fp"))
                by_end.setdefault(key, {})[metric] = u.get("val")
        recs = [dict(ticker=tk, end=k[0], fy=k[1], fp=k[2], **v) for k, v in by_end.items()]
        recs = sorted(recs, key=lambda r: r["end"], reverse=True)[:n_quarters]
        out.extend(recs)
    return pd.DataFrame(out)


if __name__ == "__main__":
    print(fetch_quarters().to_string(index=False))
