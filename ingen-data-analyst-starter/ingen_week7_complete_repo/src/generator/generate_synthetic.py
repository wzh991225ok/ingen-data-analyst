"""Week 7 — synthetic data generator for the InGen analytics warehouse.

Generates a reproducible star-schema dataset (fixed seed) at modest scale:
  - dim_date (2 years), dim_product (5), dim_geography, dim_customer (1,000)
  - fact_fleet_telemetry (~100k rows: robots x days)
  - fact_support_tickets (~5k rows)
  - fact_sales_pipeline (~1k rows)

Synthetic ONLY — no real InGen data. Reproducible from SEED below; all randomness flows
through the seeded Faker + random.Random instances, so re-running yields identical CSVs.

Run:  python -m src.generator.generate_synthetic
Outputs CSVs to data/week07/synthetic/ and writes a manifest with row counts + seed.
"""
from __future__ import annotations
import csv, json, random, datetime
from pathlib import Path
from faker import Faker

SEED = 20260607
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "week07" / "synthetic"
OUT.mkdir(parents=True, exist_ok=True)

N_CUSTOMERS = 1000
N_ROBOTS = 330            # fleet size; each robot emits ~daily telemetry over its active window
N_TICKETS = 5000
N_PIPELINE = 1000
START = datetime.date(2024, 6, 1)
END = datetime.date(2026, 5, 31)

PRODUCTS = [
    # code, name, vertical, form_factor, launch_year, list_price
    ("FARI", "Fari", "eldercare", "companion", 2023, 6000),
    ("SENPAI", "Senpai", "education", "tabletop", 2022, 3500),
    ("SENTINEL", "Sentinel Prime AI", "indoor_security", "wheeled", 2021, 45000),
    ("AIDOROVER", "Aido Rover", "outdoor_patrol", "rugged-wheeled", 2023, 70000),
    ("AIDOHUM", "Aido Humanoid", "humanoid", "humanoid", 2025, 120000),
]
REGIONS = [
    ("United States", "North America", ["California", "Texas", "New York", "Illinois"]),
    ("Canada", "North America", ["Ontario", "British Columbia"]),
    ("United Kingdom", "Europe", ["England", "Scotland"]),
    ("Germany", "Europe", ["Bavaria", "Berlin"]),
    ("Japan", "APAC", ["Tokyo", "Osaka"]),
    ("Australia", "APAC", ["New South Wales", "Victoria"]),
]
SEGMENTS = ["Enterprise", "Mid-Market", "SMB", "Public Sector"]
INDUSTRIES = ["Healthcare", "Education", "Logistics", "Retail", "Manufacturing", "Government", "Hospitality"]
SEVERITIES = [("Critical", 0.08), ("High", 0.22), ("Medium", 0.45), ("Low", 0.25)]
CATEGORIES = ["battery", "navigation", "connectivity", "software", "mechanical"]
STAGES_OPEN = ["Lead", "Qualified", "Proposal", "Negotiation"]


def _date_key(d: datetime.date) -> int:
    return d.year * 10000 + d.month * 100 + d.day


def _weighted(rng, pairs):
    r = rng.random(); acc = 0
    for val, w in pairs:
        acc += w
        if r <= acc:
            return val
    return pairs[-1][0]


def write_csv(name, header, rows):
    p = OUT / name
    with open(p, "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
    return len(rows)


def generate():
    fake = Faker(); Faker.seed(SEED)
    rng = random.Random(SEED)
    counts = {}

    # ---- dim_date ----
    dim_date = []
    d = START
    while d <= END:
        dim_date.append([_date_key(d), d.isoformat(), d.year, (d.month - 1) // 3 + 1, d.month,
                         d.strftime("%B"), d.day, d.isoweekday(), d.strftime("%A"),
                         d.isoweekday() >= 6])
        d += datetime.timedelta(days=1)
    counts["dim_date"] = write_csv("dim_date.csv",
        ["date_key","full_date","year","quarter","month","month_name","day","day_of_week","day_name","is_weekend"], dim_date)
    all_date_keys = [r[0] for r in dim_date]

    # ---- dim_geography ----
    dim_geo = []; gkey = 1; geo_keys = []
    for country, region, states in REGIONS:
        for st in states:
            dim_geo.append([gkey, country, region, st, fake.city()]); geo_keys.append(gkey); gkey += 1
    counts["dim_geography"] = write_csv("dim_geography.csv",
        ["geography_key","country","region","state_province","city"], dim_geo)

    # ---- dim_product ----
    dim_prod = []
    for i, (code, nm, vert, ff, yr, price) in enumerate(PRODUCTS, 1):
        dim_prod.append([i, code, nm, vert, ff, yr, price])
    counts["dim_product"] = write_csv("dim_product.csv",
        ["product_key","product_code","product_name","vertical","form_factor","launch_year","list_price_usd"], dim_prod)
    product_keys = [r[0] for r in dim_prod]

    # ---- dim_customer ----
    dim_cust = []
    for i in range(1, N_CUSTOMERS + 1):
        dim_cust.append([i, f"CUST-{i:06d}", fake.company(), _weighted(rng, [(s, w) for s, w in zip(SEGMENTS, [0.2,0.3,0.35,0.15])]),
                         rng.choice(INDUSTRIES), rng.choice(geo_keys),
                         rng.choice(all_date_keys[:max(1, len(all_date_keys)//2)])])
    counts["dim_customer"] = write_csv("dim_customer.csv",
        ["customer_key","customer_id","customer_name","segment","industry","geography_key","signup_date_key"], dim_cust)
    customer_keys = [r[0] for r in dim_cust]
    cust_geo = {r[0]: r[5] for r in dim_cust}

    # ---- fact_fleet_telemetry (~100k) ----
    # each robot belongs to a customer+product, active over a random window; emits ~daily rows
    rows = []; tkey = 1
    target = 100000
    robots = []
    for rid in range(1, N_ROBOTS + 1):
        ck = rng.choice(customer_keys); pk = rng.choice(product_keys)
        start_i = rng.randint(0, len(all_date_keys) - 200)
        span = rng.randint(200, len(all_date_keys) - start_i)
        robots.append((f"RBT-{rid:05d}", ck, pk, cust_geo[ck], start_i, span))
    # emit until ~target rows, cycling robots/days
    ri = 0
    while len(rows) < target:
        robot_id, ck, pk, gk, start_i, span = robots[ri % len(robots)]
        day_offset = (ri // len(robots))
        if day_offset >= span:
            ri += 1
            if ri > len(robots) * 400:
                break
            continue
        dk = all_date_keys[start_i + day_offset]
        active = rng.random() > 0.04           # ~96% days active
        uptime = round(rng.uniform(6, 23.5) if active else 0, 2)
        dist = round(rng.uniform(0.5, 25) if active else 0, 2)
        cycles = rng.randint(1, 4) if active else 0
        errors = rng.choices([0,1,2,3,5,8], weights=[60,20,10,5,3,2])[0] if active else 0
        rows.append([tkey, dk, pk, ck, gk, robot_id, uptime, dist, cycles, errors, active])
        tkey += 1; ri += 1
    counts["fact_fleet_telemetry"] = write_csv("fact_fleet_telemetry.csv",
        ["telemetry_key","date_key","product_key","customer_key","geography_key","robot_id",
         "uptime_hours","distance_km","battery_cycles","error_count","is_active"], rows)

    # ---- fact_support_tickets (~5k) ----
    rows = []
    for i in range(1, N_TICKETS + 1):
        ck = rng.choice(customer_keys); pk = rng.choice(product_keys); gk = cust_geo[ck]
        opened_i = rng.randint(0, len(all_date_keys) - 1)
        opened_dk = all_date_keys[opened_i]
        sev = _weighted(rng, SEVERITIES)
        resolved = rng.random() > 0.12
        if resolved:
            base = {"Critical": 6, "High": 18, "Medium": 48, "Low": 96}[sev]
            res_hours = round(abs(rng.gauss(base, base * 0.5)) + 1, 2)
            closed_i = min(len(all_date_keys) - 1, opened_i + max(0, int(res_hours // 24)))
            closed_dk = all_date_keys[closed_i]
            csat = rng.choices([1,2,3,4,5], weights=[5,8,17,40,30])[0]
        else:
            res_hours = ""; closed_dk = ""; csat = ""
        rows.append([i, opened_dk, closed_dk, pk, ck, gk, f"TKT-{i:06d}", sev,
                     rng.choice(CATEGORIES), res_hours, resolved, csat])
    counts["fact_support_tickets"] = write_csv("fact_support_tickets.csv",
        ["ticket_key","opened_date_key","closed_date_key","product_key","customer_key","geography_key",
         "ticket_id","severity","category","resolution_hours","is_resolved","csat_score"], rows)

    # ---- fact_sales_pipeline (~1k) ----
    rows = []
    for i in range(1, N_PIPELINE + 1):
        ck = rng.choice(customer_keys); pk = rng.choice(product_keys); gk = cust_geo[ck]
        created_i = rng.randint(0, len(all_date_keys) - 1)
        created_dk = all_date_keys[created_i]
        price = dict((r[0], r[6]) for r in dim_prod)[pk]
        units = rng.randint(1, 25)
        amount = round(units * price * rng.uniform(0.85, 1.0), 2)
        outcome = rng.random()
        if outcome < 0.35:      # won
            stage = "Won"; is_won = True
            cycle = rng.randint(20, 180)
            closed_i = min(len(all_date_keys) - 1, created_i + cycle // 1)
            closed_dk = all_date_keys[min(closed_i, len(all_date_keys)-1)]
        elif outcome < 0.6:     # lost
            stage = "Lost"; is_won = False
            cycle = rng.randint(15, 150)
            closed_i = min(len(all_date_keys) - 1, created_i + cycle)
            closed_dk = all_date_keys[closed_i]
        else:                   # open
            stage = rng.choice(STAGES_OPEN); is_won = False; cycle = ""; closed_dk = ""
        rows.append([i, created_dk, closed_dk, pk, ck, gk, f"OPP-{i:06d}", stage, units, amount, is_won, cycle])
    counts["fact_sales_pipeline"] = write_csv("fact_sales_pipeline.csv",
        ["pipeline_key","created_date_key","closed_date_key","product_key","customer_key","geography_key",
         "opportunity_id","stage","units","amount_usd","is_won","sales_cycle_days"], rows)

    manifest = {"seed": SEED, "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
                "date_range": [START.isoformat(), END.isoformat()], "row_counts": counts,
                "note": "Synthetic data only — no real InGen data. Reproducible from fixed seed."}
    (OUT / "_manifest.json").write_text(json.dumps(manifest, indent=2))
    print("Synthetic warehouse generated (seed", SEED, "):")
    for k, v in counts.items():
        print(f"  {k:26s} {v:>7,} rows")
    return counts


if __name__ == "__main__":
    generate()
