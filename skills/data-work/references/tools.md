# Data Tool Catalog

Curated catalog router for data libraries, platforms, and tools. Use this **before** loading procedural references. Verify API behavior via Context7 or official docs before implementation.

## Contract

- Catalogs are planner-first selection guides, not API evidence.
- Separate concerns:
  - `references/data-engineering-tools.md` — compute, storage, orchestration, warehouse, table-format decisions.
  - `references/data-science-tools.md` — analysis, statistics, visualization, ML/DL, notebooks, experiment tracking.
  - this file — synthetic test-data generation (Faker ecosystem), a cross-cutting concern shared by engineering and science work.
- Keep each catalog entry compact: capabilities, selection rule, avoidance rule, constraint, and official docs link.
- New libraries enter a catalog only when they are proven for repeated planner use.

## Routing

- Pipeline/engine/storage/warehouse/orchestration/table-format selection → `references/data-engineering-tools.md`.
- Analysis/visualization/statistics/ML/notebook/experiment selection → `references/data-science-tools.md`.
- Spatial tool selection → `geospatial/references/tools.md`.
- Synthetic/test-data generation selection → the `## Synthetic Test Data` section in this file.
- Methodology, evaluation, validation workflow, or plotting recipes → existing procedural references, not this catalog.

## Cross-domain routes

- Sedona / GeoParquet / torchgeo / geo-focused visualization → `geospatial/references/tools.md`.

## Synthetic Test Data

<!-- decision: entries live in this router file, because synthetic fixtures are a cross-cutting concern shared by engineering and science work; a third sub-catalog for three tools would be over-engineering. Alternative: new test-data-tools.md sub-file (rejected). -->

Boundary: LLM training and evaluation dataset generation is outside this pack; keep it separate from application test fixtures.

### Faker

**Capabilities:** Localized fake data generation (names, addresses, emails, dates, ...) for test fixtures, demos, and seed data.

**Use when:** You need realistic but non-sensitive records for tests or demos instead of copying real production data.

**Avoid when:** The data is used in production, or you need strongly typed schema-derived mock objects (see factory_boy).

**Constraints:** Deterministic via `seed` / `seed_instance`; synthetic output is not anonymisation of real data. TypeScript equivalent: `@faker-js/faker`.

**Docs:** https://faker.readthedocs.io/en/stable

---

### @faker-js/faker

**Capabilities:** Localized fake data generation for JavaScript/TypeScript (Node and browser), including seeded reproducible sequences.

**Use when:** Astro, Node, or browser projects need test fixtures or demo content without real personal data.

**Avoid when:** The project is Python-only (use Faker) or the fixtures must mirror an ORM schema (prefer factory-based helpers).

**Constraints:** Install as a dev dependency; use `faker.seed(n)` for deterministic tests. Synthetic output is not anonymisation of real data.

**Docs:** https://fakerjs.dev

---

### factory_boy

**Capabilities:** Declarative Python factories for complex test objects across Django and SQLAlchemy models, with built-in Faker integration.

**Use when:** Python ORM tests need many realistic, related model instances.

**Avoid when:** Flat, standalone fake records suffice — plain Faker is lighter.

**Constraints:** Adds an ORM integration layer; pin alongside the ORM version.

**Docs:** https://factoryboy.readthedocs.io
