-- ============================================================================
-- InGen Analytics Warehouse — Reference Query Library (Week 7)
-- 15 documented queries answering real product-analytics questions.
-- DuckDB dialect. Each query is self-contained and delimited by ';'.
-- Techniques are noted per query: [JOIN] [AGG] [CTE] [WINDOW] [SETOP].
-- Run all:  python -m src.queries.run_queries
-- ============================================================================

-- Q01 [JOIN][AGG] Daily active fleet — distinct active robots per day (last 30 days).
SELECT d.full_date,
       COUNT(DISTINCT f.robot_id) AS active_robots
FROM fact_fleet_telemetry f
JOIN dim_date d ON f.date_key = d.date_key
WHERE f.is_active
GROUP BY d.full_date
ORDER BY d.full_date DESC
LIMIT 30;

-- Q02 [JOIN][AGG] Mean Time Between Failures (MTBF) proxy by product line:
-- total active uptime hours divided by total error events.
SELECT p.product_name, p.vertical,
       ROUND(SUM(f.uptime_hours), 0)                                  AS total_uptime_hours,
       SUM(f.error_count)                                             AS total_errors,
       ROUND(SUM(f.uptime_hours) / NULLIF(SUM(f.error_count), 0), 1)  AS mtbf_hours
FROM fact_fleet_telemetry f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product_name, p.vertical
ORDER BY mtbf_hours DESC;

-- Q03 [JOIN][AGG] Ticket-resolution time by severity (avg / median / p90), resolved only.
SELECT t.severity,
       COUNT(*)                                            AS resolved_tickets,
       ROUND(AVG(t.resolution_hours), 1)                   AS avg_hours,
       ROUND(MEDIAN(t.resolution_hours), 1)                AS median_hours,
       ROUND(QUANTILE_CONT(t.resolution_hours, 0.9), 1)    AS p90_hours
FROM fact_support_tickets t
WHERE t.is_resolved
GROUP BY t.severity
ORDER BY avg_hours;

-- Q04 [JOIN][AGG] Sales-pipeline velocity — win rate, avg cycle days, won value by product.
SELECT p.product_name,
       COUNT(*)                                                       AS opportunities,
       SUM(CASE WHEN s.is_won THEN 1 ELSE 0 END)                      AS won,
       ROUND(100.0 * SUM(CASE WHEN s.is_won THEN 1 ELSE 0 END) / COUNT(*), 1) AS win_rate_pct,
       ROUND(AVG(CASE WHEN s.is_won THEN s.sales_cycle_days END), 0)  AS avg_won_cycle_days,
       ROUND(SUM(CASE WHEN s.is_won THEN s.amount_usd ELSE 0 END), 0) AS won_value_usd
FROM fact_sales_pipeline s
JOIN dim_product p ON s.product_key = p.product_key
GROUP BY p.product_name
ORDER BY won_value_usd DESC;

-- Q05 [CTE][WINDOW] Month-over-month change in won bookings (running + MoM delta).
WITH monthly AS (
    SELECT d.year, d.month,
           SUM(CASE WHEN s.is_won THEN s.amount_usd ELSE 0 END) AS won_value
    FROM fact_sales_pipeline s
    JOIN dim_date d ON s.created_date_key = d.date_key
    GROUP BY d.year, d.month
)
SELECT year, month, ROUND(won_value, 0) AS won_value,
       ROUND(won_value - LAG(won_value) OVER (ORDER BY year, month), 0) AS mom_delta,
       ROUND(SUM(won_value) OVER (ORDER BY year, month), 0)             AS running_total
FROM monthly
ORDER BY year, month;

-- Q06 [JOIN][WINDOW] Rank customers by lifetime won value (top 10) with dense rank.
WITH cust_value AS (
    SELECT c.customer_id, c.customer_name, c.segment,
           SUM(CASE WHEN s.is_won THEN s.amount_usd ELSE 0 END) AS won_value
    FROM fact_sales_pipeline s
    JOIN dim_customer c ON s.customer_key = c.customer_key
    GROUP BY c.customer_id, c.customer_name, c.segment
)
SELECT customer_name, segment, ROUND(won_value, 0) AS won_value,
       DENSE_RANK() OVER (ORDER BY won_value DESC) AS value_rank
FROM cust_value
WHERE won_value > 0
ORDER BY won_value DESC
LIMIT 10;

-- Q07 [JOIN][AGG] Fleet utilization by region — avg uptime hours/robot-day.
SELECT g.region,
       COUNT(*)                          AS robot_days,
       ROUND(AVG(f.uptime_hours), 2)     AS avg_uptime_hours,
       ROUND(AVG(f.distance_km), 2)      AS avg_distance_km
FROM fact_fleet_telemetry f
JOIN dim_geography g ON f.geography_key = g.geography_key
GROUP BY g.region
ORDER BY avg_uptime_hours DESC;

-- Q08 [CTE][WINDOW] 7-day moving average of daily errors across the fleet.
WITH daily AS (
    SELECT d.full_date, SUM(f.error_count) AS errors
    FROM fact_fleet_telemetry f
    JOIN dim_date d ON f.date_key = d.date_key
    GROUP BY d.full_date
)
SELECT full_date, errors,
       ROUND(AVG(errors) OVER (ORDER BY full_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 1) AS errors_7d_ma
FROM daily
ORDER BY full_date DESC
LIMIT 30;

-- Q09 [JOIN][AGG] Ticket volume by product x category (pivot-style heat input).
SELECT p.product_name, t.category, COUNT(*) AS tickets
FROM fact_support_tickets t
JOIN dim_product p ON t.product_key = p.product_key
GROUP BY p.product_name, t.category
ORDER BY p.product_name, tickets DESC;

-- Q10 [JOIN][AGG] CSAT by product line (avg score + survey coverage).
SELECT p.product_name,
       COUNT(*)                                                 AS resolved_tickets,
       COUNT(t.csat_score)                                      AS surveyed,
       ROUND(100.0 * COUNT(t.csat_score) / COUNT(*), 1)         AS survey_coverage_pct,
       ROUND(AVG(t.csat_score), 2)                              AS avg_csat
FROM fact_support_tickets t
JOIN dim_product p ON t.product_key = p.product_key
WHERE t.is_resolved
GROUP BY p.product_name
ORDER BY avg_csat DESC;

-- Q11 [CTE][WINDOW] First-touch to first telemetry: each product's top error-day rank.
WITH prod_day AS (
    SELECT p.product_name, d.full_date, SUM(f.error_count) AS errors
    FROM fact_fleet_telemetry f
    JOIN dim_product p ON f.product_key = p.product_key
    JOIN dim_date d ON f.date_key = d.date_key
    GROUP BY p.product_name, d.full_date
)
SELECT product_name, full_date, errors
FROM (
    SELECT product_name, full_date, errors,
           ROW_NUMBER() OVER (PARTITION BY product_name ORDER BY errors DESC) AS rn
    FROM prod_day
) ranked
WHERE rn = 1
ORDER BY errors DESC;

-- Q12 [JOIN][AGG] Quarterly bookings by vertical (won amount).
SELECT p.vertical, d.year, d.quarter,
       ROUND(SUM(CASE WHEN s.is_won THEN s.amount_usd ELSE 0 END), 0) AS won_value
FROM fact_sales_pipeline s
JOIN dim_product p ON s.product_key = p.product_key
JOIN dim_date d ON s.created_date_key = d.date_key
GROUP BY p.vertical, d.year, d.quarter
ORDER BY d.year, d.quarter, won_value DESC;

-- Q13 [SETOP] Customers who have BOTH an open support ticket AND an open pipeline opportunity
-- (intersection), useful for account-health review.
SELECT DISTINCT c.customer_id, c.customer_name
FROM fact_support_tickets t
JOIN dim_customer c ON t.customer_key = c.customer_key
WHERE NOT t.is_resolved
INTERSECT
SELECT DISTINCT c.customer_id, c.customer_name
FROM fact_sales_pipeline s
JOIN dim_customer c ON s.customer_key = c.customer_key
WHERE s.stage IN ('Lead', 'Qualified', 'Proposal', 'Negotiation')
ORDER BY customer_id;

-- Q14 [SETOP] Active fleet customers with NO Critical/High-severity ticket (set difference) —
-- healthy-fleet accounts that are good candidates for case studies / upsell.
SELECT DISTINCT c.customer_id, c.customer_name
FROM fact_fleet_telemetry f
JOIN dim_customer c ON f.customer_key = c.customer_key
WHERE f.is_active
EXCEPT
SELECT DISTINCT c.customer_id, c.customer_name
FROM fact_support_tickets t
JOIN dim_customer c ON t.customer_key = c.customer_key
WHERE t.severity IN ('Critical', 'High')
ORDER BY customer_id
LIMIT 25;

-- Q15 [CTE][WINDOW][JOIN] Segment contribution: each segment's share of total won value,
-- with cumulative share (Pareto view).
WITH seg AS (
    SELECT c.segment,
           SUM(CASE WHEN s.is_won THEN s.amount_usd ELSE 0 END) AS won_value
    FROM fact_sales_pipeline s
    JOIN dim_customer c ON s.customer_key = c.customer_key
    GROUP BY c.segment
)
SELECT segment, ROUND(won_value, 0) AS won_value,
       ROUND(100.0 * won_value / SUM(won_value) OVER (), 1)                                   AS pct_of_total,
       ROUND(100.0 * SUM(won_value) OVER (ORDER BY won_value DESC)
                   / SUM(won_value) OVER (), 1)                                               AS cumulative_pct
FROM seg
ORDER BY won_value DESC;
