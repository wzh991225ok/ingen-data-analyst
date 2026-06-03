"""Week 4 market-sizing inputs — REAL public market anchors with sources (retrieved 2026-06-01).

Design principle (honesty): published market estimates DISAGREE a lot. We therefore record a
LOW and HIGH anchor per vertical (from different reputable firms), size top-down AND bottom-up,
and present RANGES with explicit assumptions — never a single spuriously-precise number.

All $ are USD. CAGR as decimal. Each anchor carries its source so a mentor can verify.
"""

RETRIEVED = "2026-06-01"

# --------------------------------------------------------------------------- #
# Top-down market anchors per vertical (LOW / HIGH from different sources)     #
# --------------------------------------------------------------------------- #
# Each: market_2024_low/high (USD bn), cagr_low/high, plus the source strings.
ANCHORS = {
"Eldercare (Fari)": dict(
    market_label="Eldercare / companion assistive robots (global)",
    low_bn=2.7, high_bn=3.4, cagr_low=0.119, cagr_high=0.176,
    us_share=0.30,  # US ~30% of global (NA-led; US ~83% of NA per Vision Research)
    sources=[
        "Grand View Research: elder-care assistive robots ~$3.4B (2025), CAGR 14.2%",
        "InsightAce / Global Industry Analysts: ~$2.7-3.1B (2024), CAGR 11.9-16.1%",
        "Vision Research: global $2.55B (2023), US 83.7% of North America",
        "Grand View: healthcare companion robots $2.09B (2024), CAGR 17.6%",
    ]),
"Education (Senpai)": dict(
    market_label="Educational robots (K-12 / consumer learning, global)",
    low_bn=1.4, high_bn=2.2, cagr_low=0.14, cagr_high=0.21,
    us_share=0.25,
    sources=[
        "Educational-robot market commonly cited ~$1.4-2.2B (2024) across firms",
        "Humanoid 'education & entertainment' segment >30% of humanoid market (multiple)",
        "NCES K-12 enrollment ~49.5M public (Week 3 warehouse) as bottom-up base",
    ]),
"Indoor Security (Sentinel Prime AI)": dict(
    market_label="Security robots (commercial subset of broader market, global)",
    low_bn=4.69, high_bn=19.07, cagr_low=0.135, cagr_high=0.176,
    us_share=0.38,  # NA ~37-40% of global
    sources=[
        "Mordor: security robots $15.72B (2024), CAGR 13.6% (broad, incl. defense UAV)",
        "Precedence: $19.07B (2024), CAGR 14.9%",
        "MRFR: $4.69B (2023), CAGR 17.65% (narrower scope)",
        "Mordor: commercial & industrial facilities highest CAGR 17.6%; patrol 45% of apps",
        "NOTE: wide spread driven by defense/UAV inclusion. Sentinel = COMMERCIAL INDOOR only.",
    ]),
"Outdoor Patrol (Aido Rover)": dict(
    market_label="Security patrol robots (ground, outdoor perimeter subset)",
    low_bn=0.153, high_bn=2.0, cagr_low=0.036, cagr_high=0.18,
    us_share=0.40,
    sources=[
        "Valuates: narrow 'security patrol robot' $153M (2024), CAGR 3.6% (tight definition)",
        "Mordor security-robots: patrol & surveillance 45% of apps; RaaS ~18.9% CAGR",
        "Precedence: patrolling = biggest application segment in 2024",
        "NOTE: huge definitional spread; ground-only outdoor perimeter is a small real slice.",
    ]),
"Humanoid (Aido Humanoid)": dict(
    market_label="General-purpose humanoid robots (global, emerging)",
    low_bn=0.29, high_bn=4.89, cagr_low=0.175, cagr_high=0.506,
    us_share=0.48,  # NA ~47-52%
    sources=[
        "Grand View: humanoid $1.55B (2024), CAGR 17.5%",
        "Precedence: $1.84B (2025), CAGR 16.9%",
        "Fortune Business Insights: $4.89B (2025), CAGR 50.6% (very aggressive)",
        "IntelMarket: $290M (2024), CAGR 23.7% (conservative)",
        "NOTE: among the widest spreads in all of tech forecasting; treat as scenario range.",
    ]),
}

# --------------------------------------------------------------------------- #
# Bottom-up build inputs per vertical (units x penetration x ASP)             #
# Each driver has low/base/high; tornado sensitivity varies one at a time.    #
# --------------------------------------------------------------------------- #
BOTTOM_UP = {
"Eldercare (Fari)": dict(
    unit_label="US adults 65+ aging in place (households)",
    base_units=58_000_000,      # ~58M Americans 65+ (Census/World Bank 65+ ~17.7%)
    units_low=55_000_000, units_high=62_000_000,
    serviceable_pct_base=0.06, serviceable_pct_low=0.03, serviceable_pct_high=0.10,  # share addressable now
    penetration_base=0.02, penetration_low=0.005, penetration_high=0.05,            # adoption of a robot
    asp_base=1500, asp_low=800, asp_high=2500,                                       # annual ASP (device+service)
    note="Base ~58M 65+; serviceable = independent-living + able-to-adopt; ASP blends device + subscription."),
"Education (Senpai)": dict(
    unit_label="US K-12 public schools",
    base_units=98_000,          # ~98k US public K-12 schools
    units_low=95_000, units_high=100_000,
    serviceable_pct_base=0.20, serviceable_pct_low=0.10, serviceable_pct_high=0.35,
    penetration_base=0.05, penetration_low=0.01, penetration_high=0.12,
    asp_base=4000, asp_low=2000, asp_high=8000,
    note="School-level base; serviceable = schools with STEM/special-needs budget; ASP per school/year."),
"Indoor Security (Sentinel Prime AI)": dict(
    unit_label="US large commercial buildings (>100k sqft)",
    base_units=300_000,
    units_low=250_000, units_high=350_000,
    serviceable_pct_base=0.15, serviceable_pct_low=0.07, serviceable_pct_high=0.25,
    penetration_base=0.04, penetration_low=0.01, penetration_high=0.08,
    asp_base=60000, asp_low=35000, asp_high=90000,   # MaaS annual (guard-replacement economics)
    note="Building base; ASP = annual MaaS (~1/3 of human-guard cost per Mordor)."),
"Outdoor Patrol (Aido Rover)": dict(
    unit_label="US large perimeter sites (campuses, logistics, infra)",
    base_units=120_000,
    units_low=90_000, units_high=150_000,
    serviceable_pct_base=0.12, serviceable_pct_low=0.05, serviceable_pct_high=0.20,
    penetration_base=0.03, penetration_low=0.005, penetration_high=0.07,
    asp_base=75000, asp_low=40000, asp_high=120000,
    note="Outdoor perimeter sites; ASP = annual patrol service; ground-only (excludes pure drone)."),
"Humanoid (Aido Humanoid)": dict(
    unit_label="US warehouse/logistics + manufacturing facilities (early target)",
    base_units=20_000,
    units_low=15_000, units_high=30_000,
    serviceable_pct_base=0.10, serviceable_pct_low=0.03, serviceable_pct_high=0.20,
    penetration_base=0.02, penetration_low=0.002, penetration_high=0.06,
    asp_base=100000, asp_low=50000, asp_high=200000,  # per-unit (or annual lease) — pre-commercial
    note="Pre-commercial; facility base x units-per-site folded into penetration; ASP highly uncertain."),
}

VERTICALS = list(ANCHORS.keys())
ANCHOR_PRODUCT = {
    "Eldercare (Fari)": "Fari",
    "Education (Senpai)": "Senpai",
    "Indoor Security (Sentinel Prime AI)": "Sentinel Prime AI",
    "Outdoor Patrol (Aido Rover)": "Aido Rover",
    "Humanoid (Aido Humanoid)": "Aido Humanoid",
}


def bottom_up_som(v, *, units=None, serviceable=None, penetration=None, asp=None):
    """Bottom-up serviceable-obtainable value = units x serviceable% x penetration% x ASP."""
    b = BOTTOM_UP[v]
    u = units if units is not None else b["base_units"]
    s = serviceable if serviceable is not None else b["serviceable_pct_base"]
    p = penetration if penetration is not None else b["penetration_base"]
    a = asp if asp is not None else b["asp_base"]
    return u * s * p * a


def top_down(v):
    """Return dict of TAM(low/high), SAM(US, low/high) from anchors."""
    a = ANCHORS[v]
    tam_low = a["low_bn"] * 1e9
    tam_high = a["high_bn"] * 1e9
    sam_low = tam_low * a["us_share"]
    sam_high = tam_high * a["us_share"]
    return dict(tam_low=tam_low, tam_high=tam_high, sam_low=sam_low, sam_high=sam_high,
                us_share=a["us_share"])
