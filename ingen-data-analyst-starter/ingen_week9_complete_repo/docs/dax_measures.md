# DAX Measures Reference — InGen Analytics (Week 9)

Ten reusable DAX measures for the Power BI executive scorecard, written against the Week 7 star
schema imported into Power BI (`fact_fleet_telemetry`, `fact_support_tickets`, `fact_sales_pipeline`,
`dim_date`, `dim_product`, `dim_customer`, `dim_geography`). `dim_date` is marked as the date table.

Each measure is generic — it respects whatever slicer/filter context the report applies (product,
date range, geography), so the same measure works on every page and drill-through.

---

## 1. Won Value
Total closed-won bookings in the current filter context.
```DAX
Won Value =
CALCULATE ( SUM ( fact_sales_pipeline[amount_usd] ), fact_sales_pipeline[is_won] = TRUE () )
```

## 2. Win Rate %
Won opportunities as a share of all opportunities.
```DAX
Win Rate % =
DIVIDE (
    CALCULATE ( COUNTROWS ( fact_sales_pipeline ), fact_sales_pipeline[is_won] = TRUE () ),
    COUNTROWS ( fact_sales_pipeline )
)
```

## 3. Won Value YoY %
Year-over-year growth of won value, using the date table.
```DAX
Won Value YoY % =
VAR Curr = [Won Value]
VAR Prior =
    CALCULATE ( [Won Value], DATEADD ( dim_date[full_date], -1, YEAR ) )
RETURN
    DIVIDE ( Curr - Prior, Prior )
```

## 4. Won Value (Rolling 3M)
Trailing 3-month bookings — smooths monthly noise on the trend tile.
```DAX
Won Value Rolling 3M =
CALCULATE (
    [Won Value],
    DATESINRANGE ( dim_date[full_date], MAX ( dim_date[full_date] ) - 90, MAX ( dim_date[full_date] ) )
)
```

## 5. Won Value WoW Delta
Week-over-week change in bookings (absolute).
```DAX
Won Value WoW Delta =
VAR ThisWeek = [Won Value]
VAR LastWeek =
    CALCULATE ( [Won Value], DATEADD ( dim_date[full_date], -7, DAY ) )
RETURN
    ThisWeek - LastWeek
```

## 6. % of Total Won (by Product)
Each product's share of total won value, ignoring the product filter for the denominator.
```DAX
% of Total Won =
DIVIDE (
    [Won Value],
    CALCULATE ( [Won Value], REMOVEFILTERS ( dim_product ) )
)
```

## 7. Avg Resolution Hours
Average ticket resolution time (resolved tickets only).
```DAX
Avg Resolution Hours =
CALCULATE (
    AVERAGE ( fact_support_tickets[resolution_hours] ),
    fact_support_tickets[is_resolved] = TRUE ()
)
```

## 8. Avg CSAT
Average customer-satisfaction score where surveyed.
```DAX
Avg CSAT =
AVERAGEX (
    FILTER ( fact_support_tickets, NOT ISBLANK ( fact_support_tickets[csat_score] ) ),
    fact_support_tickets[csat_score]
)
```

## 9. Fleet Active Rate %
Share of telemetry rows where the robot reported active — fleet-health headline.
```DAX
Fleet Active Rate % =
DIVIDE (
    CALCULATE ( COUNTROWS ( fact_fleet_telemetry ), fact_fleet_telemetry[is_active] = TRUE () ),
    COUNTROWS ( fact_fleet_telemetry )
)
```

## 10. CSAT Status (traffic light)
RAG status string driving the scorecard tile color (target ≥ 4.0; watch ≥ 3.5).
```DAX
CSAT Status =
VAR V = [Avg CSAT]
RETURN
    SWITCH ( TRUE (),
        V >= 4.0, "On target",
        V >= 3.5, "Watch",
        "Off target"
    )
```

---

## Usage notes
- **Reusable across dashboards:** measures 1–9 are pure aggregations with no hard-coded product/date,
  so they drop straight into the Looker-equivalent pages or any new report page.
- **Traffic lights:** pair each KPI with a `… Status` measure (pattern of #10) and bind the tile's
  conditional formatting to that string. Define the matching `Win Rate Status`, `Active Rate Status`,
  etc., by copying #10 and swapping the value + thresholds.
- **Targets** live in the thresholds; to make them slicer-driven, replace the literals with a
  one-row `dim_targets` table and reference its columns.
- **Date intelligence** (measures 3–5) requires `dim_date` marked as the date table and a contiguous
  date range — both true for the Week 7 warehouse (730 contiguous days).
