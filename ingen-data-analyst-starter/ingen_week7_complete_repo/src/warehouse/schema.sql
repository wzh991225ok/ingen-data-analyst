-- ============================================================================
-- InGen Analytics Warehouse — Star Schema DDL (Week 7)
-- DuckDB dialect. Synthetic data only; no real InGen data.
--
-- Design: classic star schema.
--   Dimensions (dim_*): one surrogate key each (*_key, INTEGER), plus a natural/
--     business key and descriptive attributes.
--   Facts (fact_*): surrogate PK + foreign keys to dimensions (surrogate keys) +
--     additive/semi-additive measures. Facts hold no descriptive text.
--   Grain is documented on each fact table.
-- ============================================================================

-- ---------- DIMENSIONS ----------

-- Date dimension (role-played by event_date, ticket dates, pipeline dates)
CREATE TABLE dim_date (
    date_key        INTEGER PRIMARY KEY,   -- surrogate (YYYYMMDD)
    full_date       DATE NOT NULL,
    year            SMALLINT NOT NULL,
    quarter         TINYINT NOT NULL,
    month           TINYINT NOT NULL,
    month_name      VARCHAR NOT NULL,
    day             TINYINT NOT NULL,
    day_of_week     TINYINT NOT NULL,      -- 1=Mon .. 7=Sun
    day_name        VARCHAR NOT NULL,
    is_weekend      BOOLEAN NOT NULL
);

-- Product dimension — the five InGen verticals / anchor products
CREATE TABLE dim_product (
    product_key     INTEGER PRIMARY KEY,   -- surrogate
    product_code    VARCHAR NOT NULL,      -- natural key, e.g. 'FARI'
    product_name    VARCHAR NOT NULL,      -- e.g. 'Fari'
    vertical        VARCHAR NOT NULL,      -- eldercare / education / indoor_security / outdoor_patrol / humanoid
    form_factor     VARCHAR NOT NULL,
    launch_year     SMALLINT,
    list_price_usd  INTEGER
);

-- Customer dimension
CREATE TABLE dim_customer (
    customer_key    INTEGER PRIMARY KEY,   -- surrogate
    customer_id     VARCHAR NOT NULL,      -- natural key, e.g. 'CUST-000123'
    customer_name   VARCHAR NOT NULL,
    segment         VARCHAR NOT NULL,      -- Enterprise / Mid-Market / SMB / Public Sector
    industry        VARCHAR NOT NULL,
    geography_key   INTEGER NOT NULL,      -- FK -> dim_geography
    signup_date_key INTEGER NOT NULL       -- FK -> dim_date
);

-- Geography dimension
CREATE TABLE dim_geography (
    geography_key   INTEGER PRIMARY KEY,   -- surrogate
    country         VARCHAR NOT NULL,
    region          VARCHAR NOT NULL,      -- e.g. 'North America'
    state_province  VARCHAR,
    city            VARCHAR
);

-- ---------- FACTS ----------

-- Fleet telemetry — grain: one row per robot per day (daily heartbeat/health)
CREATE TABLE fact_fleet_telemetry (
    telemetry_key       BIGINT PRIMARY KEY,    -- surrogate
    date_key            INTEGER NOT NULL,      -- FK -> dim_date
    product_key         INTEGER NOT NULL,      -- FK -> dim_product
    customer_key        INTEGER NOT NULL,      -- FK -> dim_customer
    geography_key       INTEGER NOT NULL,      -- FK -> dim_geography
    robot_id            VARCHAR NOT NULL,      -- degenerate dimension (device identifier)
    uptime_hours        DECIMAL(5,2) NOT NULL, -- measure (0..24)
    distance_km         DECIMAL(7,2) NOT NULL, -- measure
    battery_cycles      SMALLINT NOT NULL,     -- measure
    error_count         SMALLINT NOT NULL,     -- measure
    is_active           BOOLEAN NOT NULL       -- measure (reported in that day)
);

-- Support tickets — grain: one row per ticket
CREATE TABLE fact_support_tickets (
    ticket_key          INTEGER PRIMARY KEY,   -- surrogate
    opened_date_key     INTEGER NOT NULL,      -- FK -> dim_date
    closed_date_key     INTEGER,               -- FK -> dim_date (NULL if open)
    product_key         INTEGER NOT NULL,      -- FK -> dim_product
    customer_key        INTEGER NOT NULL,      -- FK -> dim_customer
    geography_key       INTEGER NOT NULL,      -- FK -> dim_geography
    ticket_id           VARCHAR NOT NULL,      -- degenerate dimension
    severity            VARCHAR NOT NULL,      -- Critical / High / Medium / Low
    category            VARCHAR NOT NULL,      -- battery / navigation / connectivity / software / mechanical
    resolution_hours    DECIMAL(8,2),          -- measure (NULL if open)
    is_resolved         BOOLEAN NOT NULL,      -- measure
    csat_score          TINYINT                -- measure (1..5, NULL if not surveyed)
);

-- Sales pipeline — grain: one row per opportunity
CREATE TABLE fact_sales_pipeline (
    pipeline_key        INTEGER PRIMARY KEY,   -- surrogate
    created_date_key    INTEGER NOT NULL,      -- FK -> dim_date
    closed_date_key     INTEGER,               -- FK -> dim_date (NULL if still open)
    product_key         INTEGER NOT NULL,      -- FK -> dim_product
    customer_key        INTEGER NOT NULL,      -- FK -> dim_customer
    geography_key       INTEGER NOT NULL,      -- FK -> dim_geography
    opportunity_id      VARCHAR NOT NULL,      -- degenerate dimension
    stage               VARCHAR NOT NULL,      -- Lead / Qualified / Proposal / Negotiation / Won / Lost
    units               INTEGER NOT NULL,      -- measure
    amount_usd          DECIMAL(12,2) NOT NULL,-- measure
    is_won              BOOLEAN NOT NULL,      -- measure
    sales_cycle_days    INTEGER                -- measure (NULL if open)
);
