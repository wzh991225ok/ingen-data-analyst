# Data Dictionary — Week 7 (synthetic warehouse)

**Synthetic only — no real InGen data. Reproducible from SEED=20260607.**

## Dimensions
- dim_date(date_key PK, full_date, year, quarter, month, day_of_week, is_weekend, ...)
- dim_product(product_key PK, product_code, product_name, vertical, form_factor, list_price_usd, ...)
- dim_customer(customer_key PK, customer_id, customer_name, segment, industry, geography_key FK, signup_date_key FK)
- dim_geography(geography_key PK, country, region, state_province, city)

## Facts (grain noted)
- fact_fleet_telemetry — 1 row per robot per day. FKs: date/product/customer/geography. Measures: uptime_hours, distance_km, battery_cycles, error_count, is_active. ~100k rows.
- fact_support_tickets — 1 row per ticket. FKs: opened/closed date, product, customer, geography. Measures: resolution_hours, is_resolved, csat_score. 5k rows.
- fact_sales_pipeline — 1 row per opportunity. FKs: created/closed date, product, customer, geography. Measures: units, amount_usd, is_won, sales_cycle_days. 1k rows.

## Conventions
- Surrogate keys: *_key (integer). Natural/business keys kept as separate columns (customer_id, product_code, ...).
- date_key is YYYYMMDD. Degenerate dimensions (robot_id, ticket_id, opportunity_id) live on the fact.
- Empty CSV cells = SQL NULL (loaded with NULLSTR '').
