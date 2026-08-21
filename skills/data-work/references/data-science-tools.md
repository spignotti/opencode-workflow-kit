# Data Science Tools

Curated catalog for analysis, statistics, visualization, classical ML, deep learning, notebooks, and experiment tracking. Verify API behavior via Context7 or official docs before implementation.

Use the most boring stack that fits the task: pandas/DuckDB for routine analysis, scikit-learn/XGBoost for classical ML, and deeper tooling only when the problem clearly requires it.

## numpy

**Capabilities:** Foundation for numerical arrays, linear algebra, and vectorized computation.

**Use when:** Almost any numerical Python work needs an array or low-level numeric foundation.

**Avoid when:** The task is purely SQL, configuration, or high-level visualization without array computation.

**Constraints:** Core dependency for scientific Python; verify dtype and broadcasting behavior for performance-sensitive work.

**Docs:** https://numpy.org

---

## NumExpr

**Capabilities:** Fast evaluation of string-based arithmetic expressions over NumPy arrays with reduced intermediate memory and multi-core parallel execution.

**Use when:** Profiling shows CPU or memory pressure in large-array numeric expressions (typically arrays too big for L1 cache, complex expressions); benchmark against plain NumPy first.

**Avoid when:** Arrays are small or expressions are simple — NumExpr can be slower than NumPy, and the expression-string API adds indirection. Keep it as an optimization, not a default dependency.

**Constraints:** Install only after a measured win; results can depend on expression complexity, array size, and core count. Verify supported functions via docs before use.

**Docs:** https://numexpr.readthedocs.io

---

## pandas

**Capabilities:** Label-aware tabular DataFrames with broad ecosystem support.

**Use when:** Most general-purpose tabular analysis, cleaning, joins, or exploratory work.

**Avoid when:** Performance or larger-than-memory scaling points toward Polars or DuckDB.

**Constraints:** The default DataFrame library; switch away only for concrete scale or API-fit reasons.

**Docs:** https://pandas.pydata.org/docs

---

## Polars

**Capabilities:** High-performance DataFrame engine with lazy evaluation and strong columnar execution.

**Use when:** Chained DataFrame transformations need higher performance or lower memory footprint than pandas.

**Avoid when:** The ecosystem fit or analytical workload is better served by pandas or DuckDB.

**Constraints:** Cross-reference to the engineering catalog for pipelines where SQL/Parquet behavior may matter more than DataFrame ergonomics.

**Docs:** https://docs.pola.rs

---

## DuckDB

**Capabilities:** Local analytical SQL engine for fast queries over CSV, Parquet, JSON, and DataFrame-like workloads.

**Use when:** Multi-table analytics, SQL-first thinking, or local Parquet exploration is the natural fit.

**Avoid when:** DataFrame-first transforms or broader ML/DL tooling are the primary workflow.

**Constraints:** Cross-reference to the engineering catalog for pipeline-scale storage and warehouse decisions.

**Docs:** https://duckdb.org

---

## pyarrow

**Capabilities:** Columnar Arrow memory format and efficient Parquet/IPC I/O.

**Use when:** Interoperability across pandas, Polars, DuckDB, and file-based formats is important.

**Avoid when:** You only need a DataFrame API and the backend already manages the format.

**Constraints:** Usually a supporting layer rather than a standalone analysis tool.

**Docs:** https://arrow.apache.org/docs/python/index.html

---

## SciPy

**Capabilities:** Scientific algorithms, optimization, linear algebra, signal processing, and numerical utilities.

**Use when:** You need numerical methods beyond numpy, statsmodels, or scikit-learn.

**Avoid when:** The task is simpler DataFrame work or standard ML pipeline construction.

**Constraints:** Broad library; load only the submodules relevant to the task.

**Docs:** https://docs.scipy.org

---

## ftfy

**Capabilities:** Fixes garbled Unicode text and encoding problems.

**Use when:** Text columns arrive with mojibake, inconsistent encoding, or broken characters.

**Avoid when:** The issue is text normalization, not corrupted text data.

**Constraints:** A narrow cleaning utility; useful but not a general NLP tool.

**Docs:** https://ftfy.readthedocs.io

---

## statsmodels

**Capabilities:** Classical statistical models, regression summaries, time-series analysis, and inference with coefficient tables and confidence intervals.

**Use when:** You need inference-heavy results, statistical tests, or model summaries rather than predictive-only pipelines.

**Avoid when:** You want a modern predictive ML pipeline instead of statistical interpretation.

**Constraints:** Complements scikit-learn: statsmodels explains, scikit-learn predicts.

**Docs:** https://www.statsmodels.org/stable/index.html

---

## matplotlib

**Capabilities:** Foundational static plotting library for Python.

**Use when:** You need full control over plot composition or a base for seaborn/matplotlib-based workflows.

**Avoid when:** A higher-level or interactive tool is clearly sufficient and faster to use.

**Constraints:** Still the base layer for many Python visualization workflows.

**Docs:** https://matplotlib.org

---

## seaborn

**Capabilities:** High-level statistical plotting built on matplotlib.

**Use when:** Quick exploratory plots such as distributions, categories, relationships, and heatmaps.

**Avoid when:** You need deep interactivity or purely web-native visualization.

**Constraints:** Strong for analysis-time visualization; plotly serves interactive delivery better.

**Docs:** https://seaborn.pydata.org

---

## Plotly

**Capabilities:** Interactive charts and dashboards for analysis results and presentation.

**Use when:** Interactive exploration, sharing, or dashboarding is more valuable than static plots.

**Avoid when:** A static exploratory chart is faster and sufficient.

**Constraints:** Often used after the analysis stage for result delivery.

**Docs:** https://plotly.com/python/

---

## great-tables

**Capabilities:** Publication-quality table formatting from pandas or Polars DataFrames.

**Use when:** You need a polished, readable table rather than a chart.

**Avoid when:** You actually need a plot, dashboard, or raw dataframe output.

**Constraints:** Table presentation tool, not a visualization library for charts.

**Docs:** https://posit-dev.github.io/great-tables

---

## scikit-learn

**Capabilities:** Classical ML pipelines, preprocessing, model selection, evaluation, and tabular modeling.

**Use when:** Standard classification, regression, clustering, or preprocessing workflows are needed.

**Avoid when:** You need deep learning, heavy AutoML, or specialized experiment tracking.

**Constraints:** The classical baseline; XGBoost, PyCaret, and AutoGluon are escalation paths.

**Docs:** https://scikit-learn.org/stable/documentation.html

---

## XGBoost

**Capabilities:** Gradient boosting for high-performance tabular modeling.

**Use when:** Tabular predictive performance is the priority and tree-based boosting is appropriate.

**Avoid when:** Simpler interpretable models or deep learning better match the task.

**Constraints:** Often a stronger tabular baseline than generic ensemble defaults.

**Docs:** https://xgboost.readthedocs.io

---

## PyCaret

**Capabilities:** Low-code AutoML for rapid baselines and comparative model runs.

**Use when:** You want fast model comparison, shallow automation, or a quick baseline.

**Avoid when:** You need transparent manual control over the full ML pipeline.

**Constraints:** Faster for prototyping; heavier in runtime behavior than plain scikit-learn usage.

**Docs:** https://pycaret.gitbook.io/docs

---

## AutoGluon

**Capabilities:** AutoML across tabular, text, and vision tasks with strong defaults and model stacking.

**Use when:** Automated performance matters and the problem may be multimodal or harder to tune manually.

**Avoid when:** You want minimal abstractions and full control.

**Constraints:** Heavier than PyCaret; useful when accuracy or automation outweigh simplicity.

**Docs:** https://auto.gluon.ai

---

## PyTorch

**Capabilities:** Flexible deep learning framework for GPU-accelerated models, research, and custom training loops.

**Use when:** Deep learning is the explicit task or you need PyTorch-native model ecosystems.

**Avoid when:** Classical ML already fits the problem.

**Constraints:** Default new-project choice for deep learning; TensorFlow remains relevant only for existing ecosystems.

**Docs:** https://pytorch.org/docs/stable/index.html

---

## TensorFlow

**Capabilities:** Deep learning framework with Keras-focused APIs and production-oriented tooling.

**Use when:** An existing codebase, deployment target, or requirement already depends on TensorFlow/Keras.

**Avoid when:** You are starting fresh with no legacy constraint.

**Constraints:** Still relevant, but not the default solo-dev starting point for new DL work.

**Docs:** https://www.tensorflow.org/docs

---

## Transformers

**Capabilities:** Pre-trained models for NLP, vision, audio, and generative workflows from Hugging Face.

**Use when:** You need pretrained model access, fine-tuning scaffolds, or high-level inference APIs.

**Avoid when:** Classical ML or a simpler model-free heuristic already solves the task.

**Constraints:** Strong for model reuse; verify task fit, licensing, and model size before committing.

**Docs:** https://huggingface.co/docs/transformers

---

## OpenCV

**Capabilities:** Computer vision primitives, image/video processing, and classic CV algorithms.

**Use when:** Low-level image manipulation or classical CV operations are required.

**Avoid when:** You only need lightweight image I/O or a high-level ML pipeline.

**Constraints:** Powerful but low-level; Pillow is usually lighter for simple image prep.

**Docs:** https://docs.opencv.org/4.x/

---

## Pillow

**Capabilities:** Simple image I/O and manipulation in Python.

**Use when:** Reading, resizing, converting, or validating images in data/ML workflows.

**Avoid when:** You need full computer vision processing rather than basic image handling.

**Constraints:** Lightweight utility; pair with deeper libraries when needed.

**Docs:** https://pillow.readthedocs.io

---

## JupyterLab

**Capabilities:** Interactive notebook environment for exploration and iteration.

**Use when:** Interactive exploration, visualization, or ecosystem plug-in compatibility is important.

**Avoid when:** A more reproducible, version-control-friendly notebook format is a better fit.

**Constraints:** Still the broadest notebook ecosystem; marimo is the modern reproducible alternative.

**Docs:** https://jupyterlab.readthedocs.io

---

## marimo

**Capabilities:** Reactive Python notebooks stored as `.py` files with strong reproducibility and deployment ergonomics.

**Use when:** Reproducibility, Git-friendly workflows, or notebook-as-app workflows matter.

**Avoid when:** You need legacy Jupyter extensions or notebook habits that marimo does not replicate.

**Constraints:** Preferred choice for new reproducible notebook projects.

**Docs:** https://docs.marimo.io

---

## MLflow

**Capabilities:** Open-source experiment tracking and model registry.

**Use when:** You want minimal, self-hostable tracking for parameters, metrics, artifacts, and models.

**Avoid when:** You prefer a managed visualization-heavy experiment platform.

**Constraints:** Default open-source tracking choice; W&B is stronger on hosted visualization.

**Docs:** https://mlflow.org/docs/latest/index.html

---

## Weights & Biases

**Capabilities:** Hosted experiment tracking, visualization, and collaboration tooling.

**Use when:** Experiment visibility and rich tracking dashboards are worth a cloud-based workflow.

**Avoid when:** You want a fully local, self-hosted, lightweight tracker.

**Constraints:** Strong visualization and UX; verify account/licensing terms for the project.

**Docs:** https://docs.wandb.ai

---

## ClearML

**Capabilities:** End-to-end MLOps platform spanning tracking, orchestration, data management, and automation.

**Use when:** You want a broader platform rather than only experiment tracking.

**Avoid when:** A lighter tracker is enough.

**Constraints:** More platform than MLflow; use it when the wider feature set is actually needed.

**Docs:** https://docs.clear.ml

---

## DVC

**Capabilities:** Git-friendly data and pipeline versioning.

**Use when:** Large datasets, model artifacts, or pipeline stages need reproducible versioning.

**Avoid when:** Dataset and model versioning is not yet a real problem.

**Constraints:** Useful beyond ML when data versioning is genuinely required.

**Docs:** https://dvc.org/doc

---

## Google Colab

**Capabilities:** Hosted Jupyter environment with convenient cloud compute and GPU access.

**Use when:** You need quick experimentation or a hosted environment without local setup.

**Avoid when:** Long-term reproducibility, governance, or project integration require local control.

**Constraints:** Convenience-first environment; not a replacement for local or CI-managed reproducibility.

**Docs:** https://colab.research.google.com

---

## Datawrapper

**Capabilities:** External no-code charting and publishing platform.

**Use when:** The goal is a published chart for the web rather than a programmatic Python plot.

**Avoid when:** The task needs a Python-native plotting or dashboard workflow.

**Constraints:** Publishing tool, not a Python plotting library.

**Docs:** https://www.datawrapper.de

---

## RAWGraphs

**Capabilities:** Exploratory browser-based charting tool for non-standard visual layouts.

**Use when:** You want exploratory, designer-oriented visuals for review or communication.

**Avoid when:** The task needs programmatic analysis or repeatable Python visualization.

**Constraints:** Design/exploration tool, not part of the Python analysis stack.

**Docs:** https://www.rawgraphs.io

---

## Cross-domain routes

- Geo-focused visualization and geospatial ML pipelines → `geospatial/references/tools.md`.
- Methodology, evaluation, validation workflow, and plotting recipes → `data-work` procedural references, not this catalog.
