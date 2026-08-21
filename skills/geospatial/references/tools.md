# Geospatial Tools

Curated catalog of known-good libraries and tools. Use this to check whether a proven tool exists for a task before external search. Always verify API compatibility via Context7 or official docs before implementation.

Format per entry:

```
## <Tool / Package>

**Capabilities:** …
**Use when:** …
**Avoid when:** …
**Constraints:** …
**Docs:** <official URL>
```

---

## geopandas

**Capabilities:** Vector data model on top of pandas, geometry-aware I/O, spatial joins, overlays, and projections.

**Use when:** Working with GeoJSON, Shapefile, GeoPackage, or Parquet-backed vector datasets in Python.

**Avoid when:** You only need pure table analytics without geometry operations, or extremely large files where pyogrio-backed reading is enough.

**Constraints:** Depends on shapely and pyproj for geometry and CRS handling; I/O usually routes through pyogrio today.

**Docs:** https://geopandas.org

---

## shapely

**Capabilities:** Geometry construction and predicate logic: buffers, intersections, unions, contains, validity fixes, and constructive operations.

**Use when:** You need reliable, repeatable geometry math that sits below higher-level tools like GeoPandas.

**Avoid when:** You actually need I/O, attribute tables, or dataset-level joins rather than pure geometry operations.

**Constraints:** Planar geometry only; CRS correctness is your responsibility.

**Docs:** https://shapely.readthedocs.io

---

## pyproj

**Capabilities:** CRS handling, datum transforms, and coordinate conversions between geographic and projected systems.

**Use when:** Transforming coordinates, reprojecting layers, or translating between CRS definitions.

**Avoid when:** You only need a CRS label and the workflow already manages reprojection implicitly.

**Constraints:** Always confirm you are transforming the right axis order and that all inputs share a common CRS before multi-dataset operations.

**Docs:** https://pyproj4.github.io/pyproj

---

## pyogrio

**Capabilities:** Fast vector I/O backend for GeoPandas backed by GDAL/OGR; reads and writes GeoPackage, Shapefile, GeoJSON, and other OGR-supported formats.

**Use when:** You need fast, minimal vector I/O and do not need GeoPandas-level joins or analysis in the read step.

**Avoid when:** You need geopandas convenience features on top of I/O, or the target format is unsupported by GDAL.

**Constraints:** Often the default backend for modern geopandas I/O; verify format-specific options via Context7 or official docs.

**Docs:** https://geopandas.org/en/stable/docs/reference/api/geopandas.read_file.html

---

## rasterio

**Capabilities:** Raster I/O and windowed access for GeoTIFF and other GDAL-supported raster formats.

**Use when:** Reading, clipping, reprojecting, mosaicking, or writing gridded raster datasets.

**Avoid when:** You need higher-level analysis patterns better served by xarray or domain-specific raster workflows.

**Constraints:** Wraps GDAL; pin versions carefully in reproducible stacks and verify format/driver support before building pipelines.

**Docs:** https://rasterio.readthedocs.io

---

## xarray

**Capabilities:** N-dimensional labeled arrays with coordinates, dimensions, and lazy computation; strong fit for climate, weather, and EO time-series data.

**Use when:** You need to reason over labeled dimensions, combine multiple arrays, or analyze multi-temporal raster data.

**Avoid when:** You only need 2D raster I/O or a simple rasterio window read without label semantics.

**Constraints:** Raster extension behavior usually comes through rioxarray; check projection handling explicitly when mixing libraries.

**Docs:** https://docs.xarray.dev

---

## rioxarray

**Capabilities:** Brings rasterio-style CRS, reprojection, clipping, and geospatial metadata into xarray workflows.

**Use when:** Combining xarray with geospatial raster operations in a consistent CRS-aware workflow.

**Avoid when:** You are working outside xarray or need raw rasterio windowed access without labeled arrays.

**Constraints:** Verify CRS metadata on NetCDF/HDF sources; not all datasets arrive geospatially clean.

**Docs:** https://corteva.github.io/rioxarray

---

## dask

**Capabilities:** Parallel and out-of-core computation for larger-than-memory arrays and dataframes.

**Use when:** Scaling spatial pipelines beyond a single machine or single-core pandas/rasterio step.

**Avoid when:** The dataset fits comfortably in memory and parallelization overhead is not worth it.

**Constraints:** Task-graph overhead and chunk sizing dominate performance; validate that downstream spatial operations remain chunk-aware.

**Docs:** https://dask.org

---

## sentinelhub-py

**Capabilities:** Access Sentinel Hub Process, Catalog, and OGC APIs for satellite imagery retrieval and processing workflows.

**Use when:** You need curated Sentinel/Landsat-style access through Sentinel Hub rather than raw archive downloads.

**Avoid when:** A free, open STAC catalog or direct GEE workflow is simpler and sufficient.

**Constraints:** Requires Sentinel Hub credentials and often a commercial/service agreement; verify rate limits and billing before scripting large jobs.

**Docs:** https://sentinelhub-py.readthedocs.io

---

## owslib

**Capabilities:** Client for OGC services such as WMS, WFS, WCS, and WMTS.

**Use when:** Connecting to institutional or legacy spatial data portals that expose OGC endpoints.

**Avoid when:** You have a modern STAC or cloud-native alternative that avoids WMS/WFS tile extraction.

**Constraints:** Behavior depends heavily on server implementation; validate supported versions and advertised operations before relying on them.

**Docs:** https://geopython.github.io/OWSLib

---

## planetary-computer

**Capabilities:** Python client for Microsoft Planetary Computer STAC search and signed asset access.

**Use when:** You want to search curated, open EO/climate collections and access protected assets through token signing without manual download plumbing.

**Avoid when:** You need general-purpose cloud compute or a substitute for any arbitrary public STAC endpoint.

**Constraints:** Search and asset access run through the Planetary Computer STAC API; always verify collection availability, licensing, and token behavior via official docs.

**Docs:** https://planetarycomputer.microsoft.com/docs/concepts/data-access

---

## pystac-client

**Capabilities:** Programmatic STAC search and pagination across STAC APIs.

**Use when:** Discovering and filtering STAC items before loading them into Python workflows.

**Avoid when:** You only need a browser-based catalog exploration or a non-STAC data source.

**Constraints:** Pair with a signing library such as planetary-computer when asset URLs require tokens; verify API filtering options via Context7.

**Docs:** https://pystac-client.readthedocs.io

---

## folium

**Capabilities:** Quick interactive Leaflet maps from Python, ideal for notebooks and lightweight previews.

**Use when:** Visualizing vector layers, markers, and web tiles interactively in Python.

**Avoid when:** You need static publication maps, production basemap rendering, or large-scale vector tile apps.

**Constraints:** Great for exploration, but not a full product mapping stack.

**Docs:** https://python-visualization.github.io/folium

---

## leafmap

**Capabilities:** Broader geospatial visualization toolkit with many data-source integrations, built on ipyleaflet/Leaflet patterns.

**Use when:** You need richer notebook map workflows than folium provides.

**Avoid when:** You need a production web-app mapping stack or purely static maps.

**Constraints:** Notebook-first workflow; verify widget/backend behavior outside Jupyter when embedding.

**Docs:** https://leafmap.org

---

## geemap

**Capabilities:** Interactive Google Earth Engine notebook workflows, including JS-to-Python conversion, layer inspection, drawing tools, timelapse creation, and export utilities.

**Use when:** You need to prototype or analyze GEE datasets from Jupyter and keep the workflow reproducible.

**Avoid when:** You do not use GEE or you only need static publication maps instead of interactive notebook mapping.

**Constraints:** Depends on Earth Engine authentication and quotas; pair with `geospatial` guardrails for reproducible derived products.

**Docs:** https://geemap.org

---

## contextily

**Capabilities:** Adds basemap tiles to matplotlib plots.

**Use when:** Publishing static maps that need a basemap background.

**Avoid when:** You need interactive web maps or tile-vector rendering at runtime.

**Constraints:** Web tile access depends on external tile providers; respect attribution and rate limits.

**Docs:** https://contextily.readthedocs.io

---

## geopy

**Capabilities:** Geocoding and reverse geocoding across multiple providers.

**Use when:** Converting addresses to coordinates or coordinates to places.

**Avoid when:** You need spatial indexing, geometry math, or vector analysis rather than place lookup.

**Constraints:** Provider selection controls accuracy, speed, usage limits, and licensing.

**Docs:** https://geopy.readthedocs.io

---

## GeoParquet

**Capabilities:** Columnar, cloud-friendly storage format for vector datasets.

**Use when:** You want fast analytical access to vector data in DuckDB, cloud workflows, or modern data stacks.

**Avoid when:** You need a universal interchange format for desktop GIS or legacy toolchains that expect GeoPackage/Shapefile.

**Constraints:** Tool support is strong and growing, but verify round-trip fidelity for complex geometries or exotic attributes.

**Docs:** https://geoparquet.org

---

## PostGIS

**Capabilities:** Spatial SQL, geometry/geography types, spatial indexes, and server-side geospatial analytics on PostgreSQL.

**Use when:** Managing transactional geospatial data, running spatial SQL at scale, or exposing spatial services from a database.

**Avoid when:** You only need local file analytics and the overhead of a database is not justified.

**Constraints:** Requires database operations discipline: schema design, indexing, and access control matter.

**Docs:** https://postgis.net

---

## DuckDB Spatial

**Capabilities:** Local, serverless spatial SQL over files such as GeoParquet, GeoJSON, Shapefile, and other supported formats.

**Use when:** Running fast, local analytical queries without provisioning a database server.

**Avoid when:** You need transactional services, concurrent writers, or mature server-backed geospatial APIs.

**Constraints:** Strong for analytics; weaker than PostGIS for persistent geospatial application backends.

**Docs:** https://duckdb.org/docs/extensions/spatial

---

## h3

**Capabilities:** Uber’s discrete global grid for hexagonal binning, indexing, and neighborhood aggregation.

**Use when:** Aggregating points or areas into hex cells, building consistent spatial indexes, or computing multi-resolution neighborhoods.

**Avoid when:** You need graph-based network analysis or pure topological topology rather than grid indexing.

**Constraints:** Useful for aggregation and search, but not a replacement for exact geometry operations.

**Docs:** https://h3geo.org

---

## osmnx

**Capabilities:** Fetch street networks and building footprints from OpenStreetMap and model them as network graphs.

**Use when:** Analyzing street networks, blocks, or OSM-sourced urban geometry.

**Avoid when:** You need proprietary or curated authoritative street data rather than OpenStreetMap coverage.

**Constraints:** Results depend on OSM completeness and tagging quality for the study area.

**Docs:** https://osmnx.readthedocs.io

---

## momepy

**Capabilities:** Urban morphometrics: quantifying form, size, shape, orientation, and spatial arrangement.

**Use when:** Computing morphological features for urban analysis or spatial ML on building/street datasets.

**Avoid when:** You only need basic area or length statistics rather than repeatable urban form metrics.

**Constraints:** Depends on clean, topologically consistent urban geometry input.

**Docs:** https://momepy.readthedocs.io

---

## pysal

**Capabilities:** Spatial statistics suite: autocorrelation, spatial regression, point pattern analysis, and related methods.

**Use when:** Performing rigorous spatial statistical analysis beyond descriptive mapping.

**Avoid when:** You only need quick exploratory plots or simple geometry summaries.

**Constraints:** Large metapackage; load only the submodules relevant to the current task.

**Docs:** https://pysal.org

---

## whitebox-python

**Capabilities:** Python frontend for WhiteboxTools with 518 terrain, hydrology, LiDAR, image-processing, and GIS tools.

**Use when:** You need proven analytical routines for terrain analysis, hydrological modeling, raster preprocessing, or LiDAR workflows.

**Avoid when:** You need visualization, geospatial notebooks, or higher-level modeling abstractions better supplied by other Python libraries.

**Constraints:** Strong analytical backend, not a full GIS; the package downloads a standalone engine on first run, so verify availability in offline or locked environments.

**Docs:** https://whitebox.readthedocs.io

---

## torchgeo

**Capabilities:** PyTorch datasets, samplers, transforms, and pretrained models for geospatial imagery.

**Use when:** Training or fine-tuning EO models with geospatially aware data pipelines.

**Avoid when:** You need a full end-to-end experiment framework rather than reusable dataset and model building blocks.

**Constraints:** Often paired with STAC/cloud-native data loaders; verify data contract and model assumptions before training.

**Docs:** https://torchgeo.readthedocs.io

---

## segment-geospatial

**Capabilities:** SAM and SAM-derived models for geospatial segmentation using text prompts, box prompts, or interactive markers.

**Use when:** You need pretrained segmentation without building a custom training loop.

**Avoid when:** You need full model training, custom architectures, or experiment orchestration better supplied by TorchGeo or Raster Vision.

**Constraints:** GPU and model weights can be large; verify prompts, tiling, and output format for the specific imagery scale.

**Docs:** https://samgeo.gishub.org

---

## geoai

**Capabilities:** Higher-level geo-ML toolkit for classification, segmentation, change detection, and foundation-model workflows on satellite and aerial imagery.

**Use when:** You want a broader, notebook-friendly AI workflow above the component libraries.

**Avoid when:** You need minimal, composable model-building blocks or a lower-level training stack.

**Constraints:** Treat it as a workflow accelerator, not a substitute for model validation and guardrails.

**Docs:** https://opengeoai.org

---

## rastervision

**Capabilities:** End-to-end ML pipeline for geospatial imagery: chip classification, object detection, and semantic segmentation.

**Use when:** You want a reproducible, config-driven pipeline from chipping through prediction.

**Avoid when:** You only need model components or dataset utilities rather than opinionated pipeline orchestration.

**Constraints:** Strong opinions help reproducibility; verify current backend support before planning a stack.

**Docs:** https://docs.rastervision.io

---

## Domain cross-routes

- Street-network graph analysis and urban morphology → `urban-morphology.md`.
- Spatial statistics methodology → `spatial-statistics.md`.
- Deep-learning methodology and training patterns → `geospatial-dl.md`.
