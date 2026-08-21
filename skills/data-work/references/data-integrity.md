---
name: data-integrity
description: Data quality validation, anomaly detection, freshness checks, and drift monitoring. Load when setting up validation gates, investigating data quality issues, or designing monitoring for data pipelines.
---

## Validation Gates

Validate at every boundary where data crosses a trust level:

| Boundary | What to check | How |
|----------|--------------|-----|
| **Ingest** | Schema matches expected, row count > 0, no all-null columns | Soda Core checks, Great Expectations |
| **After transform** | Row count within expected range, key columns unique, no NULLs in required fields | Same tools, post-transform |
| **Before load** | No duplicates introduced, aggregations match pre-load totals | Cross-check with independent query |
| **Periodic** | Freshness < SLA, anomaly detection on row counts, null rates | Monitoring dashboard + alerts |

## Quality Rules

### Schema Invariants
- Column names, types, and nullability match the contract
- Timestamps are monotonically increasing after dedup
- Join keys are unique on the build side before joining
- Enum columns contain only expected values

### Statistical Invariants
- Row count within ±20% of historical average (or explicit threshold)
- Null rate per column within baseline ± 5%
- Numeric columns within expected min/max bounds
- No sudden distribution shifts (KS test or visual inspection)

### Business Invariants
- Revenue totals match across independent queries
- Foreign keys reference existing rows (referential integrity)
- Aggregations at different granularities are consistent
- No negative values in columns that should be non-negative

## Anomaly Detection Patterns

### Row Count Monitoring
```python
# Compare today's count to 7-day rolling average
import pandas as pd

df["ma_7"] = df["row_count"].rolling(7).mean()
df["anomaly"] = df["row_count"] > 2 * df["ma_7"]
```

### Null Rate Monitoring
```python
# Flag columns where null rate jumps
null_rates = df.isnull().mean()
drifted = null_rates[null_rates > baseline_null_rates * 1.5]
```

### Freshness Checks
```yaml
# Soda freshness check
checks for raw_orders:
  - freshness(timestamp) < 1d
```

## Investigation Workflow

When a quality issue is detected:

1. **Quantify** — how many rows affected? What percentage of total?
2. **Scope** — is it systemic (all data) or localized (specific source, time range, partition)?
3. **Root cause** — upstream schema change? API change? Pipeline failure? Data provider change?
4. **Impact** — which downstream models/reports are affected?
5. **Fix** — can it be fixed at the source? Or must we add a transform to clean it?
6. **Prevent** — add a validation gate to catch it next time

## Monitoring Setup

For solo dev, minimal monitoring:

- **Daily:** row count + freshness check via Soda or cron script
- **Weekly:** null rate drift check across key columns
- **On deploy:** full schema validation against expected contract

Alert via email/Slack when checks fail. Do not build complex dashboards for data you can check in a SQL query.

## Common Pitfalls

- **Validating too late.** Catch issues at ingest, not after transform.
- **Ignoring upstream changes.** Data providers change schemas without notice. Monitor freshness and schema.
- **Over-validating.** Too many checks create noise. Focus on invariants that affect downstream trust.
- **No baseline.** You cannot detect drift without a baseline. Record expected ranges on first load.
