---
name: geospatial
description: Base guardrail for all geospatial work — CRS, units, geometry/raster validity, Nodata, alignment, provenance, and a task-signal routing table to specialized references. Load when doing anything spatial, remote sensing, spatial statistics, geocoding, or DL on EO data.
---

# Geospatial

Base guardrail for all spatial work. Every spatial operation must pass these checks before methodology or tool-specific guidance applies.

## Non-Negotiable Guardrails

These prevent silent corruption of spatial results. Check before any spatial operation.

1. **CRS is mandatory** — every geometry needs an explicit CRS (SRID). Without it, all spatial operations are meaningless.
2. **No metric calculations on WGS84** — EPSG:4326 uses angular units (degrees). Always transform to an appropriate projected CRS before distance, area, or buffer calculations.
3. **Use spatial index for joins** — `sindex` (R-tree) on GeoDataFrames. Without it, spatial joins are O(n²).
4. **Coordinate precision** — 6–7 decimal places suffice for sub-meter accuracy. Beyond that is noise.
5. **Ring orientation** — exterior rings CCW, interior rings (holes) CW. Use `shapely.geometry.polygon.orient()` to normalize.
6. **Axis order** — GeoJSON is `(lon, lat)`; Shapely is `(x, y)`. Do not confuse them.
7. **Null ≠ empty** — `None` vs `Point()` have different semantics. `None` means unknown; empty means known but nothing there.
8. **Common CRS before any operation** — reproject all datasets to the same CRS before spatial joins, intersections, or any multi-dataset operation.
9. **Nodata handling** — raster Nodata values must be explicitly set and masked. Never treat Nodata as zero.
10. **Alignment before raster math** — rasters must share CRS, resolution, extent, and rotation before element-wise operations. Use `rasterio.warp.reproject` or `xr.reproject`.
11. **Provenance** — document data source, access date, processing steps, and CRS for every derived dataset.

## Pre-Operation Checklist

When opening a new spatial dataset, always verify:

- CRS present and correct?
- Null or empty geometries? (filter or flag)
- Invalid geometries? (self-intersections, ring orientation — use `geopandas.GeoSeries.is_valid`)
- CRS mismatches across datasets?
- For rasters: Nodata value, band count, dtype, resolution?

## Tool Selection

Use `references/tools.md` for curated library/tool selection, `references/data-sources.md` for dataset/source selection, and `references/mcp-servers.md` for MCP server selection. Load this skill for guardrails and routing; load the catalogs when choosing libraries, data sources, or MCP servers.

## Format Decision Tree

```
Data type?
├── Vector (points, lines, polygons)
│   ├── Production / exchange → GeoPackage
│   ├── Cloud-native analytics → GeoParquet
│   └── Web tiles / quick sharing → PMTiles
├── Raster (2D grids)
│   ├── Single scene, web-ready → Cloud Optimized GeoTIFF (COG)
│   ├── Deep time series / datacube → Zarr / GeoZarr
│   └── Stitched large mosaic → COG with overviews
├── Point cloud (LiDAR, photogrammetry)
│   └── Cloud access → COPC (LAZ + embedded octree)
└── Metadata layer over any format
    └── STAC (SpatioTemporal Asset Catalog)
```

## Task-Signal → Reference Routing

Load references on demand as the task requires. Use Context7 or official docs for any library API at use time — not this skill.

| Signal | Reference | When |
|--------|-----------|------|
| Tool/library selection, STAC, NAIP, Overture, GEE, geedim, xee, geemap | `references/tools.md` | Choosing or using a geo library or tool |
| Dataset/source selection, data acquisition, EO/land-cover/climate/public-statistics discovery | `references/data-sources.md` | Choosing a geo dataset or data source |
| MCP server selection, agent-driven geo workflows | `references/mcp-servers.md` | Choosing a geo MCP server for LLM/agent-driven access |
| Spectral indices, cloud masking, compositing, time series, change detection | `references/remote-sensing.md` | Working with Sentinel-2, Landsat, MODIS, NAIP |
| Spatial autocorrelation, regression, point patterns, interpolation, hotspot detection | `references/spatial-statistics.md` | Analyzing spatial distributions, testing clustering |
| Spatial joins, zonal stats, distance features, H3 binning, spatial CV, feature engineering | `references/spatial-features.md` | Preparing geodata for ML models |
| Spatial train/test split, cross-validation, leakage prevention | `references/spatial-validation.md` | Any ML with spatial data |
| DL model loading, fine-tuning, STAC-to-GPU streaming, inference patterns | `references/geospatial-dl.md` | Training or deploying DL on EO imagery |
| PostGIS, DuckDB Spatial, spatial SQL, schema design | `references/spatial-databases.md` | Writing spatial SQL or choosing a spatial DB |
| Address-to-coordinate conversion, batch geocoding, rate limiting | `references/geocoding.md` | Geocoding addresses or reverse-geocoding |
| Building footprints, morphometrics, street network centrality, LCZ classification | `references/urban-morphology.md` | Analyzing urban form |

Tool selection and method reference may both be needed — load both when appropriate.

## Cloud-Native Streaming Pattern

EO / ML pipelines should stream data instead of generating intermediate files:

```
STAC Catalog
  → pystac-client (discovery: bbox × time × cloud cover)
  → odc-stac / stackstac (lazy array: metadata only, no pixels loaded)
  → Dask (distributed: cloud masking, compositing, reprojection)
  → xbatcher (N‑dim batches → PyTorch/TF DataLoader)
  → GPU training
```

## When to Use GEE vs Local Processing

| Factor | GEE | Local (Python) |
|--------|-----|----------------|
| Data volume | Petabyte-scale, unlimited | RAM-limited |
| Compute | Server-side, quota-limited | Full local resources |
| Reproducibility | Black box, catalog changes | Full control |
| ML integration | Export required | Direct PyTorch/TF connection |
| Cost | Free (with quotas) | Compute + storage |
| **Best for** | Quick prototyping, global-scale composites | Production pipelines, custom algorithms |

## When the Guardrails Are Violated

If you discover CRS mismatch, missing projection, invalid geometry, or unhandled Nodata — surface it as a Major finding. Do not proceed with analysis on spatially invalid data without explicitly noting the gap and its impact on result trustworthiness.
