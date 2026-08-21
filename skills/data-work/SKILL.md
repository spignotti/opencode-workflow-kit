---
name: data-work
description: Process contract for all data tasks — ETL, dbt, analysis, ML. Defines source/purpose/grain documentation, schema invariants, reproducible transforms, independent validation, and uncertainty disclosure. Routes to specialized references for engineering, analytics-engineering, or data integrity work.
---

# Data Work

Process contract for every data task. It does not teach statistics or pipeline tools — it standardizes how you work with data so results are reproducible, validated, and honest about limitations.

## Source / Purpose / Grain

Before touching data, document three things in your working script or notebook header:

1. **Source** — where the data came from, how it was accessed, and when. Include dataset name, query or API call, and timestamp of access.
2. **Purpose** — what question this data answers. One sentence. If the purpose drifts during analysis, update the header.
3. **Grain** — what one row represents. "One row per sensor per hour." "One row per customer lifetime." If the grain is unclear, you cannot trust joins or aggregations.

## Schema Invariants

When you first load a dataset, lock down the schema and surface drift immediately:

- Document column names, types, and expected ranges
- Flag columns with >50% missing values
- Flag duplicate rows and explain whether they are expected
- For time-series: confirm timestamp column is monotonically increasing after dedup
- For joins: confirm join key uniqueness on the build side before joining

Any schema violation must be surfaced as a finding, not silently coerced. Coercion (type casting, fillna, dedup) is a deliberate transformation — document why it is safe.

## Reproducible Transforms

- Every transformation is a function or script that takes input and produces output. No inline one-offs that cannot be re-run.
- Use deterministic seeds for any random operation (train/test split, sampling, augmentation).
- Pin library versions in `pyproject.toml` or `requirements.txt`. Do not rely on system-installed versions.
- For notebooks: work on paired `.py` files with `jupytext --sync`. Never edit `.ipynb` directly.
- Save intermediate results to disk if the pipeline exceeds 5 minutes of compute. Do not re-run expensive steps on every iteration.

## Synthetic Data

When generated data stands in for real records:

- Preserve the schema, grain, and required relationships of the data it replaces (foreign keys, date ranges, value constraints).
- Use deterministic seeds where reproducibility matters (see Reproducible Transforms).
- Synthetic data is not anonymisation: a Faker-style replacement of a production export is still sensitive and must not go into prompts, logs, or shared artifacts.

## Independent Validation

Never validate your own work with the same method you used to produce it.

- **Critical numbers:** validate twice, on two independent paths (script + manual computation, Pandas + SQL, two independent queries). Document agreement.
- **Model results:** hold out a test set you never touch during development. Report metrics on the holdout, not the training set.
- **Aggregations:** cross-check totals with a different query or a manual back-of-envelope estimate.
- **Claims:** every claim must be backed by a computation shown to the user. "Looks about right" is not a finding.

## Uncertainty Disclosure

Report what the data cannot support, not just what it shows:

- Flag when sample size is too small for the claim (n < 30 for means, n < 5 for correlations)
- Flag when confounders are uncontrolled
- Flag when data is missing not-at-random and the analysis assumes it is
- State confidence intervals or ranges, not just point estimates, when the audience makes decisions from the numbers
- If the analysis is exploratory, say so. Do not dress EDA up as causal inference.

## Tool Selection

When the task asks which library, warehouse, engine, notebook, visualization, or experiment tool to use, check `references/tools.md` first. Use Context7 or official docs for runtime API evidence afterward.

## Reference Routing

Load exactly one reference based on the task signal. Use Context7 or official docs for any library API at use time — not this skill.

| Signal | Reference | When |
|--------|-----------|------|
| Tool/library selection, warehouse, notebook, experiment tool choice | `references/tools.md` | Selecting or comparing data tools before procedural work |
| Pipeline design, ingestion, orchestration, quality gates | `references/data-engineering.md` | Choosing stacks, building ETL/ELT, setting up monitoring |
| dbt models, data marts, star schemas, SQL transformation | `references/analytics-engineering.md` | Building transformation layer, designing marts |
| Data quality validation, anomaly detection, freshness checks | `references/data-integrity.md` | Setting up validation, investigating data drift |
| Test selection, model selection, evaluation metrics | `references/statistics.md` | Statistical analysis, ML model evaluation |
| Static/interactive plotting, dashboard layout | `references/visualization.md` | Producing charts, dashboards, reports |
| External geographic, climate, environmental, demographic, or public-statistical source selection | `geospatial/references/data-sources.md` | Choosing an external data source — the geo catalog owns source selection; `data-work` still owns provenance, schema, and validation |

Each reference is loaded on demand. Do not load references proactively.

## When the Contract Is Violated

If you discover that source/purpose/grain was not documented, schema invariants were skipped, or validation was self-referential — surface it as a Major finding. Do not proceed with analysis on unvalidated data without explicitly noting the gap and its impact on trustworthiness.
