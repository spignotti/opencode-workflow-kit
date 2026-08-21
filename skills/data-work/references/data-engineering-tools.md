# Data Engineering Tools

Curated catalog for data pipeline, storage, orchestration, warehouse, and table-format decisions. Verify API behavior via Context7 or official docs before implementation.

Use the default escalation path unless a constraint forces another choice: `dlt → DuckDB → Soda → Prefect` for local processing, then expand only when the workload or platform requires it.

## dbt

**Capabilities:** Version-controlled SQL transformation framework with testing, documentation, and layered modeling.

**Use when:** Building reusable staging → intermediate → marts layers where lineage, tests, and documentation matter.

**Avoid when:** The transform logic is a one-off script or lives mostly outside SQL.

**Constraints:** Pair with a warehouse or DuckDB backend; keep the transformation contract in analytics-engineering, not in this catalog.

**Docs:** https://docs.getdbt.com

---

## dlt

**Capabilities:** Declarative data loading with schema evolution, incremental extraction, and repeatable ingestion workflows.

**Use when:** You want a lightweight, Pythonic ingestion layer that can start local and scale toward warehouses or lakes without rewriting the load logic.

**Avoid when:** The ingestion logic is tiny, one-off, or better handled by ad-hoc scripts and direct file copies.

**Constraints:** The recommended ingestion start for local pipelines; pair with DuckDB/Soda/Prefect only when the workflow actually grows beyond a script.

**Docs:** https://dlthub.com/docs

---

## DuckDB

**Capabilities:** In-process analytical SQL engine for local Parquet/CSV/JSON work and sub-100 GB analytics without infrastructure.

**Use when:** Prototyping or running local SQL-first analytics, especially on columnar file sets.

**Avoid when:** You need distributed compute, multi-writer concurrency, or long-lived server-backed services.

**Constraints:** The local default for solo-dev pipelines; escalate beyond it only when scale, latency, or concurrency demands it.

**Docs:** https://duckdb.org

---

## Polars

**Capabilities:** Fast, memory-efficient DataFrame engine with lazy evaluation and Arrow-native columnar execution.

**Use when:** DataFrame-first transformations are clearer than SQL, or when single-node performance matters.

**Avoid when:** The problem is dominated by multi-table SQL analytics better handled by DuckDB.

**Constraints:** Strong single-node alternative; verify streaming and expression behavior via Context7 before complex operations.

**Docs:** https://docs.pola.rs

---

## Dask

**Capabilities:** Parallel and out-of-core compute for Python arrays, DataFrames, and task graphs.

**Use when:** Scaling beyond pandas/DuckDB on one machine before moving to a managed distributed platform.

**Avoid when:** Single-node DuckDB/Polars is sufficient or when you actually need a managed warehouse or Spark ecosystem.

**Constraints:** Scheduling and chunk-size decisions dominate performance; expect more operational overhead than single-node tools.

**Docs:** https://dask.org

---

## PySpark

**Capabilities:** Distributed SQL and DataFrame processing built on Apache Spark.

**Use when:** You need cluster-scale processing, structured streaming, or broad ecosystem compatibility with enterprise data platforms.

**Avoid when:** Solo-dev local processing is still sufficient or when DuckDB/Polars covers the workload.

**Constraints:** Infrastructure-heavy compared to local tools; treat Spark as a scale-up path rather than a default.

**Docs:** https://spark.apache.org/docs/latest/api/python/index.html

---

## Ibis

**Capabilities:** Portable DataFrame API that compiles to SQL across multiple backends.

**Use when:** You want a consistent development surface across DuckDB locally and BigQuery/Snowflake/Spark in production.

**Avoid when:** You only use one backend and want direct backend-native performance and behavior.

**Constraints:** An abstraction layer, not an engine; backend-specific behaviors can still matter.

**Docs:** https://ibis-project.org

---

## Apache Sedona

**Capabilities:** Distributed spatial SQL and geometry/raster operations across Spark/Flink/Snowflake-compatible stacks.

**Use when:** Spatial joins or transformations must run at distributed scale.

**Avoid when:** Local file analytics or simpler SQL workflows are sufficient.

**Constraints:** Spatial compute choice for large-scale geospatial pipelines; for tool selection, follow `geospatial/references/tools.md`.

**Docs:** https://sedona.apache.org

---

## Soda Core

**Capabilities:** Lightweight data quality checks in SQL/YAML for freshness, completeness, duplicates, and bounds.

**Use when:** Adding validation gates at ingest boundaries or after transforms.

**Avoid when:** You need heavier contract-first validation or shared data-quality dashboards across teams.

**Constraints:** The local/dev quality default; Great Expectations and pointblank serve heavier or more reporting-oriented needs.

**Docs:** https://docs.soda.io/soda-core/soda-core-overview.html

---

## Pandera

**Capabilities:** DataFrame-level schema validation for pandas, Polars, and related backends.

**Use when:** You want typed, inline validation attached to DataFrames or transforms.

**Avoid when:** SQL-level pipeline checks or YAML-based freshness monitors are a better fit.

**Constraints:** Strong for Python-side schema contracts; complement rather than replace ingest-side validation.

**Docs:** https://pandera.readthedocs.io

---

## Great Expectations

**Capabilities:** Data contract and validation platform with expectations, checkpoints, and documentation artifacts.

**Use when:** Building reusable, shareable validation rules or integrating validation into team data contracts.

**Avoid when:** Soda Core already provides enough lightweight quality gating for the project.

**Constraints:** More powerful but heavier than Soda Core; use it when validation needs outgrow minimal checks.

**Docs:** https://docs.greatexpectations.io

---

## pointblank

**Capabilities:** DataFrame and table validation with rich reporting and presentation-friendly outputs.

**Use when:** You want validation plus an immediately readable output for review or publication.

**Avoid when:** You need a minimal local quality gate without extra reporting behavior.

**Constraints:** More presentation-oriented than Soda Core or Pandera; pair with a simpler validation layer where needed.

**Docs:** https://posit-dev.github.io/pointblank

---

## BigQuery

**Capabilities:** Managed serverless analytics warehouse with strong SQL, geospatial capabilities, and GCP-native integration.

**Use when:** On GCP, or when serverless, scalable analytics and cost-effective free-tier exploration are useful.

**Avoid when:** The workload stays local or requires a different cloud provider’s warehouse.

**Constraints:** Service, credential, and cost decisions follow the provider's own guidance.

**Docs:** https://cloud.google.com/bigquery/docs

---

## Snowflake

**Capabilities:** Managed cloud data warehouse with strong multi-cloud separation of storage and compute.

**Use when:** You need a managed warehouse outside GCP or cross-cloud interoperability is an explicit requirement.

**Avoid when:** BigQuery or local DuckDB already covers the project’s needs at lower cost.

**Constraints:** Operational choice for managed SQL, not a local prototyping tool.

**Docs:** https://docs.snowflake.com

---

## Databricks

**Capabilities:** Lakehouse platform combining Spark processing, Unity Catalog, and warehouse-style analytics.

**Use when:** The project explicitly requires Databricks-native processing or lakehouse platform integration.

**Avoid when:** You are choosing a stack from scratch for solo-dev work.

**Constraints:** Platform, not just engine; treat it as a constrained enterprise or employer-driven choice.

**Docs:** https://docs.databricks.com

---

## GCS

**Capabilities:** Managed object storage and central data lake layer for GCP workflows.

**Use when:** Building a GCP-native lake or staging layer with lifecycle policies and integrations.

**Avoid when:** The project is not on GCS or you need a non-GCP object store.

**Constraints:** Region, credential, and lifecycle decisions follow the provider's own guidance.

**Docs:** https://cloud.google.com/storage/docs

---

## S3

**Capabilities:** Managed object storage widely used for data lakes, archives, and platform integrations.

**Use when:** The workload is AWS-native or vendor-neutral object storage is required.

**Avoid when:** GCS is the project’s primary lake and S3 adds unnecessary cloud coupling.

**Constraints:** Cost and lifecycle behavior depend on storage class and access patterns.

**Docs:** https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html

---

## Cloudflare R2

**Capabilities:** S3-compatible object storage without egress fees.

**Use when:** Hosting or serving assets/data where egress cost is material.

**Avoid when:** You need deep cloud-native analytics integrations or broad first-party lakehouse support.

**Constraints:** Good fit for asset/data hosting; less mature as a full data-lake platform than S3/GCS.

**Docs:** https://developers.cloudflare.com/r2/

---

## Prefect

**Capabilities:** Python-native workflow orchestration with retries, scheduling, and deployment-friendly execution.

**Use when:** Cron is no longer sufficient and pipelines need retries, observability, and explicit orchestration.

**Avoid when:** Simple shell-level scheduling or a single-script pipeline is still enough.

**Constraints:** The local/solo-dev orchestration default; Airflow or Dagster only for heavier organizational or asset-lineage needs.

**Docs:** https://docs.prefect.io

---

## Apache Airflow

**Capabilities:** Mature DAG scheduler/orchestrator for complex, dependency-driven pipelines.

**Use when:** An existing platform already requires Airflow or the team operates it as a standard.

**Avoid when:** Solo-dev pipelines would be over-served by heavier scheduler infrastructure.

**Constraints:** Often heavier than needed for solo projects; prefer Prefect unless Airflow is already mandated.

**Docs:** https://airflow.apache.org/docs

---

## Dagster

**Capabilities:** Asset-oriented orchestrator focused on software-defined assets, lineage, and incremental materialization.

**Use when:** Asset lineage, stronger dev ergonomics, or a more modern orchestration model matter.

**Avoid when:** A lighter orchestrator or cron-based workflow is still sufficient.

**Constraints:** Stronger than Prefect in some modeling areas but adds orchestration complexity.

**Docs:** https://docs.dagster.io

---

## Parquet

**Capabilities:** Columnar, analytics-optimized storage format with strong compression and tool support.

**Use when:** Storing analytical datasets for local or cloud analytics.

**Avoid when:** You need a universal GIS interchange format rather than analytical storage.

**Constraints:** Use GeoParquet when geometry must travel with the table.

**Docs:** https://parquet.apache.org/docs

---

## Iceberg

**Capabilities:** Open table format for ACID transactions, time travel, schema evolution, and multi-engine access.

**Use when:** Multiple engines must read the same governed tables reliably.

**Avoid when:** Plain Parquet already solves the current file/analytics problem.

**Constraints:** Adopt only when multi-engine consistency or governance is a real requirement.

**Docs:** https://iceberg.apache.org/docs

---

## Delta Lake

**Capabilities:** Open table format with strong merge/upsert behavior and lakehouse features.

**Use when:** You want robust change management and merge-heavy workflows on lakehouse data.

**Avoid when:** Cross-engine portability points more clearly toward Iceberg.

**Constraints:** Evaluate against Iceberg based on backend compatibility rather than defaulting to one format.

**Docs:** https://docs.delta.io

---

## DuckLake

**Capabilities:** Lakehouse-style features around DuckDB and Parquet for versioning, cataloging, and time travel.

**Use when:** You want lightweight lakehouse semantics while staying largely inside the DuckDB ecosystem.

**Avoid when:** The project needs a proven, broadly supported table-format stack now.

**Constraints:** Still emerging; prefer Iceberg/Delta for stronger ecosystem maturity until DuckLake is independently validated.

**Docs:** https://ducklake.select/docs/stable

---

## Cross-domain routes

- GeoParquet / Sedona / spatial file workflows → `geospatial/references/tools.md`.
