---
name: data-engineering
description: Data engineering decision gates — stack selection, ingestion patterns, quality gates, orchestration for solo dev. Load when designing pipelines, choosing tools, or setting up monitoring.
---

## Stack Selection

| Layer | Primary tool | Why |
|-------|-------------|-----|
| Ingestion | `dlt` | Declarative, schema-evolving, no DB migrations |
| Processing | `DuckDB` | In-process, zero-infra, handles <100 GB comfortably |
| Quality | `Soda Core` | SQL-based checks, CI-friendly |
| Orchestration | `Prefect` | Python-native, simple setup, Cloud Run deployable |
| Storage (staging) | `GCS` / `S3` | Object storage for raw/landing data |

Rule of thumb: start with `dlt → DuckDB → Soda`. Add Prefect when you need scheduling, retries, or observability. Reach for Spark only when data exceeds single-node DuckDB capacity.

## Ingestion Pattern Decision

| Pattern | Volume | Latency | When |
|---------|--------|---------|------|
| Full refresh | <100 MB | Batch | One-time loads, reference tables |
| Incremental (append) | 100 MB–100 GB | Batch (daily/hourly) | Event data, logs, sensor readings |
| Incremental (merge) | 100 MB–10 GB | Batch | Slowly changing dimensions, upserts |
| CDC | 10 GB+ | Near-real-time | DB replication, streaming sources |
| Streaming | Continuous | Real-time | Dashboards, alerts, live feeds |

## Quality Gates

Validate at the ingest boundary; do not let dirty data propagate.

```yaml
# checks.yml
checks for raw_sensors:
  - row_count >= 0
  - missing(id) = 0
  - duplicate_count(id) = 0
  - max(value) < 1000
  - freshness(timestamp) < 1d
```

Pipeline shape:
```
Ingest → Validate (Soda) → [fail → alert, retry, dead-letter] → Transform → Validate → Load
```

## Orchestration

Minimal Prefect pattern for solo dev:

```python
from prefect import flow, task

@task(retries=2, retry_delay_seconds=60)
def extract():
    return download_data()

@task
def validate(data):
    return run_soda_checks(data)

@task
def load(data):
    return write_to_duckdb(data)

@flow(log_prints=True)
def daily_pipeline():
    data = extract()
    valid = validate(data)
    load(valid)
```

Deploy as Docker image to Cloud Run with `prefect deploy` or a cron trigger. For very simple daily loads, `cron` + `dlt` is acceptable.

## QA Checklist

- [ ] Ingestion pattern matches data volume and latency
- [ ] Schema evolution handled (dlt auto or explicit migration)
- [ ] Quality gates at ingest and after transform, with dead-letter handling
- [ ] Retries + backoff configured for transient failures
- [ ] Logs, failure alerts, freshness monitoring in place
- [ ] Idempotent — re-running produces the same result
- [ ] Stack matches scale (DuckDB solo-dev, Spark only when required)

## Common Pitfalls

- **Over-engineering the stack.** DuckDB + dlt + cron covers most solo-dev use cases.
- **No schema validation.** Dirty data propagates silently. Validate at the ingest boundary.
- **Idempotency not guaranteed.** Re-running duplicates data. Use merge/upsert from the start.
- **Monolithic scripts.** Break into pipeline stages so each is debuggable, retryable, testable.
- **Orchestrator for everything.** Not every script needs Prefect; `cron` + `dlt` is fine for daily loads.
- **Missing freshness SLAs.** A broken pipeline can go unnoticed without freshness checks.
- **Local paths in production.** Use object storage (GCS/S3) for intermediate data, not local FS.
