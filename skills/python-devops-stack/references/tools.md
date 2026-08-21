# Python Developer Tools

Curated catalog for Python dev-time utilities, CLI tooling, HTTP clients, and local tooling decisions. The standard stack (`uv`, `ruff`, `pyright`, `pytest`, `nox`) remains authoritative in `SKILL.md`. Verify API behavior via Context7 or official docs before implementation.

Use this catalog when adding a utility around the core toolchain, not when changing the toolchain itself.

## pydantic

**Capabilities:** Data validation, settings management, and structured schemas for runtime contract enforcement.

**Use when:** Validating API I/O, config, CLI options, or structured LLM outputs in typed Python code.

**Avoid when:** A plain dataclass or pyright-only typing already captures the required contract.

**Constraints:** Prefer small, explicit boundary models; avoid expanding Pydantic usage into unrelated internal logic.

**Docs:** https://docs.pydantic.dev

---

## pre-commit

**Capabilities:** Git hook framework for repetitive checks, formatting, and fast local validation.

**Use when:** You want lightweight, reproducible pre-commit checks that developers can also run manually.

**Avoid when:** The repository already enforces the same checks reliably through nox/CI.

**Constraints:** Useful as a convenience layer, not a replacement for CI validation.

**Docs:** https://pre-commit.com

---

## python-dotenv

**Capabilities:** Loads `.env` values into the process environment for local development.

**Use when:** Local scripts need simple env overrides without extra tooling.

**Avoid when:** Secrets should stay in a secrets manager, CI environment, or deployment platform.

**Constraints:** Development convenience only; never promote `.env` into production workflows.

**Docs:** https://github.com/theskumar/python-dotenv

---

## ty

**Capabilities:** Fast, newer Python type checker from Astral.

**Use when:** You are actively evaluating alternative type checkers for speed or workflow ergonomics.

**Avoid when:** The repository must stay on the agreed standard toolchain.

**Constraints:** Currently the emerging watch candidate only; `pyright` remains the standard type checker for this stack.

**Docs:** https://docs.astral.sh/ty

---

## pdoc

**Capabilities:** Generates API documentation from Python docstrings.

**Use when:** You need lightweight API docs for internal or published Python packages.

**Avoid when:** Documentation needs are narrative, report, or publishing focused rather than API reference focused.

**Constraints:** Useful for reference output, but not a substitute for clear code and tests.

**Docs:** https://pdoc.dev

---

## typer

**Capabilities:** Modern CLI framework built on Click, using type hints for interface definition.

**Use when:** Building new Python CLIs with minimal boilerplate and readable argument definitions.

**Avoid when:** The project already depends heavily on Click APIs or needs Click-only plugin patterns.

**Constraints:** The default choice for new Python CLIs unless legacy constraints already exist.

**Docs:** https://typer.tiangolo.com

---

## click

**Capabilities:** Established CLI framework with explicit command composition and plugin patterns.

**Use when:** You need Click-specific ecosystem compatibility or are working in an existing Click-based CLI.

**Avoid when:** You are starting a new CLI without a concrete Click dependency reason.

**Constraints:** Still valid, but not the default recommendation for new solo-dev Python CLIs.

**Docs:** https://click.palletsprojects.com

---

## rich

**Capabilities:** Formatted console output with tables, panels, colors, and progress display.

**Use when:** Making CLI output significantly more readable or adding inspectable progress feedback.

**Avoid when:** The output is already minimal and plain text is fine.

**Constraints:** Good complement to Typer for user-facing CLI polish.

**Docs:** https://rich.readthedocs.io

---

## loguru

**Capabilities:** Lightweight structured logging with simpler setup than stdlib logging.

**Use when:** You want faster developer ergonomics for logging in scripts, services, or tools.

**Avoid when:** The project already uses stdlib/structlog conventions consistently.

**Constraints:** Convenient, but keep logging consistent across the codebase.

**Docs:** https://loguru.readthedocs.io

---

## tqdm

**Capabilities:** Progress bars for loops and long-running operations.

**Use when:** A visible progress signal materially improves CLI or notebook feedback.

**Avoid when:** Progress is unnecessary or would add noise to short operations.

**Constraints:** Lightweight utility; use sparingly in automation logs.

**Docs:** https://tqdm.github.io

---

## watchdog

**Capabilities:** Filesystem event monitoring for local automation and reload workflows.

**Use when:** You need reactive behavior on file changes during development.

**Avoid when:** A simpler polling, manual rerun, or containerized workflow is sufficient.

**Constraints:** Useful for local dev loops; not a production-grade event backbone.

**Docs:** https://python-watchdog.readthedocs.io

---

## httpx

**Capabilities:** Modern Python HTTP client with sync/async support and HTTP/2 capabilities.

**Use when:** You need a cleaner, more contemporary HTTP client than requests, especially for async work.

**Avoid when:** A dependency or API client already locks you into requests or another HTTP library.

**Constraints:** Often preferred in new code; verify async behavior and timeout semantics before adoption.

**Docs:** https://www.python-httpx.org

---

## beautifulsoup4

**Capabilities:** HTML/XML parsing for scraping and document extraction.

**Use when:** You need lightweight, forgiving HTML parsing for scraping or legacy markup handling.

**Avoid when:** A structured API exists or a full scraping framework is a better fit.

**Constraints:** Pairs well with httpx/requests for simple fetching workflows.

**Docs:** https://www.crummy.com/software/BeautifulSoup/bs4/doc/

---

## scrapy

**Capabilities:** Full scraping framework with crawling, pipelines, and structured extraction.

**Use when:** The scraping job is more than a simple request-and-parse script.

**Avoid when:** A small script with httpx and BeautifulSoup is sufficient.

**Constraints:** Strong for larger scraping workloads; heavier than ad-hoc scraping.

**Docs:** https://docs.scrapy.org

---

## ngrok

**Capabilities:** Localhost tunneling for webhooks, external integrations, and testing inbound traffic.

**Use when:** You need safe, temporary external access to a local service.

**Avoid when:** The test environment should remain fully local or use a deployed preview instead.

**Constraints:** Handy for integration testing; keep credentials and access policies tight.

**Docs:** https://ngrok.com/docs

---

## Cross-domain routes

- Streamlit / Shiny / Mercury / other Python UI frameworks → frontend design guidance
- Quarto / document publishing → documentation conventions
- Playwright-based browser testing or screenshots → frontend testing guidance
- Sentry / Grafana / observability stacks → dedicated observability guidance
- Cloud and container deployment decisions → dedicated cloud and container guidance
- General data libraries and notebook tooling → data methodology guidance
