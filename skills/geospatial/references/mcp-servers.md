# Geospatial MCP Servers

Curated backup catalog of MCP servers for geospatial tasks. Use this when a task could be solved through an MCP server instead of a direct Python library or API call. Always verify current upstream documentation and tool permissions before use.

## Contract

- This catalog is a discovery and selection aid, not approval to install and not API evidence.
- Configure MCP servers only in the consuming project, with environment-backed credentials. Never add them to global configuration.
- Prefer read-only sources; every entry discloses local file writes, cost, authentication, and community-maintainer status.
- Direct Python libraries from `references/tools.md` and direct data sources from `references/data-sources.md` remain the default; MCP servers are an alternative for agent-driven workflows.

## NASA Earthdata MCP

**Capabilities:** Read-only discovery over the NASA Common Metadata Repository (CMR) — Earth science datasets, collections, granules, services, and citations.

**Use when:** An agent needs to discover and verify NASA Earth science data without hand-writing a CMR client.

**Avoid when:** The workflow is a deterministic pipeline — `earthaccess` or the direct CMR API is simpler and more testable.

**Constraints:** Official NASA server, hosted endpoint, read-only. Data access itself happens via the `earthaccess` library with a free Earthdata Login.

**Docs:** https://github.com/nasa/earthdata-mcp

---

## STAC MCP

**Capabilities:** Natural-language search of any STAC-compliant catalog (defaults to Planetary Computer) — collections, items, queryables, data-size estimates.

**Use when:** An agent needs catalog-agnostic STAC discovery across public catalogs.

**Avoid when:** `pystac-client` is already the workflow — direct code is more maintainable than an MCP hop.

**Constraints:** Community-maintained (Wayfinder-Foundry), read-only; works with public STAC APIs; signed assets depend on the catalog's own token handling.

**Docs:** https://github.com/BnJam/stac-mcp

---

## dynamical.org MCP

**Capabilities:** Read-only access to dynamical.org's open STAC catalog of cloud-optimized weather and climate archives (GFS, HRRR, ECMWF/AIFS) — dataset search, access patterns, recent-run freshness.

**Use when:** An agent needs to discover weather/climate archives with ready-to-run xarray/Zarr snippets.

**Avoid when:** You need validated, deterministic climate data access — direct xarray/STAC code against the same catalog gives more control.

**Constraints:** Official dynamical.org server, strictly read-only, no auth. Young project; verify the current tool surface before relying on it.

**Docs:** https://github.com/dynamical-org/mcp

---

## GDAL MCP

**Capabilities:** GDAL-style raster/vector workflows — info, convert, reproject, stats, query, clip, buffer, simplify — with writes restricted to declared workspaces.

**Use when:** An agent needs local geoprocessing with forced CRS/resampling justification and path scoping.

**Avoid when:** The workflow is a deterministic pipeline — rasterio/geopandas code from `references/tools.md` is more testable and versionable.

**Constraints:** Community-maintained (Wayfinder-Foundry); writes local files scoped to `GDAL_MCP_WORKSPACES` only when the variable is set (unset = all paths allowed); set it and review tool permissions before enabling.

**Docs:** https://github.com/JordanGunn/gdal-mcp

---

## GIS MCP

**Capabilities:** Broad toolkit over core GIS libraries (Shapely, PyProj, GeoPandas, Rasterio, PySAL, Folium) — geometry, CRS, raster, spatial statistics, visualization, and data gathering.

**Use when:** An agent needs exploratory GIS work across many tool families without switching to code.

**Avoid when:** You need GDAL-parity semantics (use GDAL MCP) or a deterministic pipeline (use the direct libraries).

**Constraints:** Community-maintained, beta; writes output files locally (GeoTIFF, GeoJSON, maps); some data gathering needs free CDS or Copernicus credentials.

**Docs:** https://github.com/mahdin75/gis-mcp
