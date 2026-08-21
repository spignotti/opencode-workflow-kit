---
name: analytics-engineering
description: Analytics engineering decision gates — dbt workflow, data modeling patterns, SQL patterns, database selection. Load when building dbt models, designing data marts, or transforming raw data into analytical datasets.
---

## dbt Project Structure

```
analytics/
├── models/
│   ├── staging/           # 1:1 with source tables, light cleaning
│   ├── intermediate/      # Business logic, joins, aggregations
│   └── marts/             # Final datasets for consumption
├── tests/                 # Custom singular tests
├── macros/                # Reusable Jinja
├── seeds/                 # CSVs for small reference data
├── dbt_project.yml
└── profiles.yml           # Connection credentials (gitignored)
```

## Model Layer Decision

| Layer | Materialization | Purpose | Example |
|-------|----------------|---------|---------|
| **Staging** | `view` or `ephemeral` | Rename, recast, light cleaning | `stg_sensors.sql` |
| **Intermediate** | `table` or `incremental` | Business logic, joins, aggregations | `int_daily_metrics.sql` |
| **Marts** | `table` or `incremental` | Final datasets: dimensions, facts | `dim_locations.sql`, `fct_readings.sql` |

## Data Modeling Decision

| Pattern | Structure | Use Case |
|---------|-----------|----------|
| **Star Schema** | Single fact + multiple dims | Reporting, dashboards |
| **Snowflake** | Normalized dims | Complex hierarchies |
| **Data Vault** | Hubs, Links, Satellites | Enterprise auditability |
| **One Big Table** | Denormalized flat table | ML feature sets, exports |

Rule of thumb: start with star schema. Move to data vault only when you need strict auditability. Use OBT for ML feature sets.

## Incremental Model Pattern

```sql
{{ config(materialized='incremental', unique_key='reading_id') }}

SELECT
    reading_id,
    sensor_id,
    timestamp,
    value
FROM {{ source('raw', 'readings') }}

{% if is_incremental() %}
    WHERE timestamp > (SELECT max(timestamp) FROM {{ this }})
{% endif %}
```

## Testing

```yaml
# schema.yml
version: 2
models:
  - name: stg_sensors
    columns:
      - name: sensor_id
        tests: [unique, not_null]
```

Test types: schema tests (unique, not_null, accepted_values, relationships), singular tests (custom SQL returning 0 rows), dbt_utils package.

## SQL Patterns

**CTEs over subqueries** — cleaner, sequential, debuggable.

| Function | Purpose |
|----------|---------|
| `ROW_NUMBER()` | Dedup, top-N per group |
| `LAG() / LEAD()` | Previous/next row value |
| `SUM() OVER (...)` | Running total |
| `MERGE INTO` | Upsert / incremental merge |

## Database Selection

| Database | Best For | Cost (Solo Dev) |
|----------|----------|-----------------|
| **DuckDB** | Local dev, single-node analytics, geo | Free (in-process) |
| **PostgreSQL** | Full-featured transactional + analytic | Free / $20–50/mo |
| **BigQuery** | Serverless, auto-scaling, geo | $0–5/mo (free tier) |
| **ClickHouse** | Real-time analytics, columnar | $0–30/mo |
| **MotherDuck** | DuckDB in the cloud | $0 (free tier) |

## QA Checklist

- [ ] Model layer structure: staging → intermediate → marts
- [ ] Incremental logic: unique key, filter for new rows, no duplicates on re-run
- [ ] Sources tested: freshness checks, not_null + unique on keys
- [ ] dbt tests pass on every model change
- [ ] Grain defined: every model has a documented row grain
- [ ] Database choice matches workload
- [ ] SQL readable: CTEs, consistent formatting, explicit JOINs
- [ ] SCD strategy chosen: Type 1 (overwrite), Type 2 (history), or Type 3 (previous)

## Common Pitfalls

- **Model name collisions:** Two models with the same name create ref ambiguity. Namespace: `stg__source`, `int__domain`, `dim__entity`, `fct__measure`.
- **Missing `is_incremental()` guard:** Incremental models without the guard rebuild from scratch.
- **Subqueries over CTEs:** Nested subqueries are harder to read and debug.
- **No freshness checks:** Stale source data produces stale models.
- **Over-normalization:** Star is simpler than snowflake for most solo-dev analytics.
