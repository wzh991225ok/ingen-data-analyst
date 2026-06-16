"""Week 6 — financial peer-benchmark inputs (REAL public data, sourced; retrieved 2026-06-15).

Public-company financials are from SEC filings / earnings releases (FY2024). Private-company
funding rounds are from company press releases and reputable tech press, with a source per row.
Every figure carries provenance so a reviewer can reconcile to the original.

Where exact 12-quarter histories are needed, src/financials/edgar_fetch.py pulls them live from
the SEC EDGAR companyfacts API (no key). In a network-restricted environment the workbook is
populated from the FY2024 anchors below (clearly labelled), and the manifest records the mode.

All $ in millions USD unless noted. Margins as decimals.
"""

RETRIEVED = "2026-06-15"

# ---- Public peers: FY2024 actuals (sourced). data_quality flags any annualised estimate. ----
# fields: ticker, name, fy, revenue, revenue_prior, gross_margin, rnd, op_margin, net_margin, data_quality, source
PUBLIC = [
 dict(ticker="IRBT", name="iRobot", fy="FY2024", revenue=681.8, revenue_prior=890.2,
      gross_margin=0.209, rnd=93.3, op_margin=-0.151, net_margin=-0.213,
      data_quality="actual", source="iRobot FY2024 10-K / earnings (rev 681.8M, GM 20.9%, R&D 93.3M, op -15.1%)"),
 dict(ticker="TER", name="Teradyne", fy="FY2024", revenue=2820.0, revenue_prior=2680.0,
      gross_margin=0.585, rnd=460.9, op_margin=0.205, net_margin=0.192,
      data_quality="actual (op margin approx)", source="Teradyne FY2024 8-K/10-K (rev 2.82B, GM 58.5%, R&D 460.9M, NI 542.4M)"),
 dict(ticker="CGNX", name="Cognex", fy="FY2024", revenue=915.0, revenue_prior=866.0,
      gross_margin=0.68, rnd=148.0, op_margin=0.07, net_margin=0.09,
      data_quality="FY revenue/margins partly annualised from 10-Q quarters", source="Cognex 2024 10-Q Q1/Q2 (Q1 rev 210.8M, GM 67%, R&D 37.1M)"),
 dict(ticker="SYM", name="Symbotic", fy="FY2024", revenue=1790.0, revenue_prior=1178.0,
      gross_margin=0.18, rnd=120.0, op_margin=-0.05, net_margin=-0.04,
      data_quality="GM/R&D approx; rev actual (FY ended 28-Sep-2024)", source="Symbotic FY2024 results press (Q4 rev 577M; FY rev ~1.79B)"),
]

# ---- Private peers: funding rounds (sourced). One row per disclosed round. ----
# fields: name, round, date, amount_musd, post_money_busd, lead_investors, employees, source
PRIVATE = [
 dict(name="Figure AI", round="Series B", date="2024-02", amount_musd=675, post_money_busd=2.6,
      lead_investors="Microsoft, OpenAI Startup Fund, NVIDIA, Bezos Expeditions, Intel Capital",
      employees=80, source="TechCrunch 2024-02-29; valuation $2.6B post-money"),
 dict(name="Figure AI", round="Series C", date="2025-09", amount_musd=1000, post_money_busd=39.0,
      lead_investors="Parkway Venture Capital (Brookfield, LG, Salesforce, Qualcomm Ventures)",
      employees=300, source="Thomasnet/Contrary 2025; >$1B at $39B post-money"),
 dict(name="Apptronik", round="Series A", date="2025-02", amount_musd=403, post_money_busd=1.5,
      lead_investors="B Capital, Capital Factory, Google (Mercedes-Benz, ARK, Japan Post Capital)",
      employees=180, source="GlobeNewswire 2025-02-13 & 2025-03-18 (total round $403M); ~$1.5B val"),
 dict(name="Agility Robotics", round="Series C", date="2025-06", amount_musd=400, post_money_busd=2.12,
      lead_investors="Playground Global, TDK Ventures, Sony, Amazon",
      employees=400, source="Forge/Contrary 2025-06; $2.12B post-money ($66.15/share)"),
 dict(name="1X Technologies", round="Series B", date="2024-01", amount_musd=100, post_money_busd=None,
      lead_investors="EQT Ventures, Samsung NEXT (OpenAI Startup Fund)",
      employees=120, source="The Robot Report 2025 (Series B $100M; $136.5M total raised)"),
 dict(name="Neura Robotics", round="Series B", date="2025-01", amount_musd=123, post_money_busd=None,
      lead_investors="BlueCrest Capital, Volvo Cars Tech Fund, Delta Electronics, Lingotto",
      employees=250, source="Forge 2025 (Series B $123M; >$280M total over 5 rounds)"),
 dict(name="Gecko Robotics", round="(latest, implied)", date="2025-11", amount_musd=None, post_money_busd=1.15,
      lead_investors="(Forge Price implied valuation)",
      employees=600, source="Forge 2025-11-05 (implied valuation $1.15B)"),
]

PUBLIC_TICKERS_CIK = {  # for the live EDGAR fetcher
    "IRBT": "0001159167", "TER": "0000097210", "CGNX": "0000851205", "SYM": "0001837240",
}
