"""Generate the star-schema ER diagram as PNG + committed .dot source.

Run:  python -m src.warehouse.er_diagram
Outputs src/warehouse/er_diagram.dot and reports/week07/er_diagram.png
"""
from __future__ import annotations
from pathlib import Path
from graphviz import Digraph

ROOT = Path(__file__).resolve().parents[2]
DOT = ROOT / "src" / "warehouse" / "er_diagram.dot"
PNG = ROOT / "reports" / "week07" / "er_diagram"

NAVY = "#1F3864"; BLUE = "#2E5496"; FACT = "#DCE6F4"; DIM = "#FCE4D6"


def table_label(name, pk, cols, is_fact):
    head = FACT if is_fact else DIM
    rows = "".join(f'<tr><td align="left" port="{c}">{c}</td></tr>' for c in cols)
    return (f'<<table border="0" cellborder="1" cellspacing="0">'
            f'<tr><td bgcolor="{head}"><b>{name}</b></td></tr>'
            f'<tr><td align="left" port="{pk}" bgcolor="#F2F2F2"><i>{pk} (PK)</i></td></tr>'
            f'{rows}</table>>')


def build():
    g = Digraph("ingen_warehouse", format="png")
    g.attr(rankdir="LR", bgcolor="white", splines="spline", nodesep="0.5", ranksep="1.2")
    g.attr("node", shape="plaintext", fontname="Helvetica", fontsize="10")
    g.attr("edge", color=NAVY, arrowhead="crow", arrowtail="none", dir="both", penwidth="1.1")

    dims = {
        "dim_date": ("date_key", ["full_date","year","quarter","month","day_of_week","is_weekend"]),
        "dim_product": ("product_key", ["product_code","product_name","vertical","form_factor","list_price_usd"]),
        "dim_customer": ("customer_key", ["customer_id","customer_name","segment","industry","geography_key"]),
        "dim_geography": ("geography_key", ["country","region","state_province","city"]),
    }
    facts = {
        "fact_fleet_telemetry": ("telemetry_key",
            ["date_key","product_key","customer_key","geography_key","robot_id","uptime_hours","distance_km","error_count","is_active"]),
        "fact_support_tickets": ("ticket_key",
            ["opened_date_key","closed_date_key","product_key","customer_key","geography_key","severity","category","resolution_hours","csat_score"]),
        "fact_sales_pipeline": ("pipeline_key",
            ["created_date_key","closed_date_key","product_key","customer_key","geography_key","stage","units","amount_usd","is_won","sales_cycle_days"]),
    }
    for n, (pk, cols) in dims.items():
        g.node(n, table_label(n, pk, cols, False))
    for n, (pk, cols) in facts.items():
        g.node(n, table_label(n, pk, cols, True))

    edges = [
        ("fact_fleet_telemetry","date_key","dim_date","date_key"),
        ("fact_fleet_telemetry","product_key","dim_product","product_key"),
        ("fact_fleet_telemetry","customer_key","dim_customer","customer_key"),
        ("fact_fleet_telemetry","geography_key","dim_geography","geography_key"),
        ("fact_support_tickets","opened_date_key","dim_date","date_key"),
        ("fact_support_tickets","product_key","dim_product","product_key"),
        ("fact_support_tickets","customer_key","dim_customer","customer_key"),
        ("fact_support_tickets","geography_key","dim_geography","geography_key"),
        ("fact_sales_pipeline","created_date_key","dim_date","date_key"),
        ("fact_sales_pipeline","product_key","dim_product","product_key"),
        ("fact_sales_pipeline","customer_key","dim_customer","customer_key"),
        ("fact_sales_pipeline","geography_key","dim_geography","geography_key"),
        ("dim_customer","geography_key","dim_geography","geography_key"),
    ]
    for ft, fc, dt, dc in edges:
        g.edge(f"{ft}:{fc}", f"{dt}:{dc}")

    DOT.write_text(g.source)
    g.render(str(PNG), cleanup=True)
    print(f"ER diagram -> {DOT.relative_to(ROOT)} (source) + {PNG.relative_to(ROOT)}.png")


if __name__ == "__main__":
    build()
