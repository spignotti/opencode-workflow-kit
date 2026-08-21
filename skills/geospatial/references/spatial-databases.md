---
name: spatial-databases
description: Spatial database patterns — PostGIS (SQLAlchemy, GiST indexes, spatial predicates) and DuckDB Spatial (direct file queries, GeoParquet). Load when writing spatial SQL or choosing a spatial DB.
---

## Engine Decision

| Factor | PostGIS | DuckDB Spatial |
|--------|---------|----------------|
| Setup | PostgreSQL server | Embedded, no server |
| Data | Imported to DB | Direct file queries |
| Workload | Transactional, concurrent writes | Analytical, large batch queries |
| Persistence | Yes (ACID) | Ephemeral (file stays in Parquet/GPKG) |
| Index | GiST (R-tree) | Spatial extension auto-indexes |
| Best for | Geo-backends, APIs, multi-user | Local analysis, ML pipelines |

## PostGIS

### Connection & Setup

```python
from sqlalchemy import create_engine
from geoalchemy2 import Geometry
import geopandas as gpd

engine = create_engine("postgresql://user:pass@host:5432/dbname")
gdf.to_postgis("table_name", engine, if_exists="replace",
               dtype={"geom": Geometry(geometry_type="GEOMETRY", srid=25833)})
```

### Spatial Index (Required)

```sql
CREATE INDEX idx_table_geom ON table_name USING GIST (geom);
ANALYZE table_name;
```

### Key Spatial Predicates

| Predicate | SQL | Use Case |
|-----------|-----|----------|
| Intersects | `ST_Intersects(a, b)` | General overlap (fastest) |
| Contains | `ST_Contains(a, b)` | A fully encloses B |
| Within | `ST_Within(a, b)` | A is inside B |
| DWithin | `ST_DWithin(a, b, 1000)` | Within 1000 units (meters if projected) |
| Crosses | `ST_Crosses(a, b)` | Lines crossing polygons |

### ST_DWithin Pattern (Distance Queries)

```sql
-- Find all buildings within 500m of a point (projected CRS)
SELECT id, geom, ST_Distance(geom, point_geom) as dist
FROM buildings
WHERE ST_DWithin(geom, point_geom, 500)
ORDER BY dist;
```

**Always use ST_DWithin with a GiST index** — it's the only spatial predicate that uses the index for distance queries.

## DuckDB Spatial

### Direct File Queries

```sql
-- Query GeoParquet without import
INSTALL spatial; LOAD spatial;

SELECT id, ST_Area(geom) as area
FROM st_read('buildings.parquet')
WHERE ST_Within(geom, ST_GeomFromText('POLYGON(...)'));
```

### Key Functions

| Function | Purpose |
|----------|---------|
| `st_read()` | Read any GDAL-supported format |
| `st_area()` | Area of polygon |
| `st_length()` | Length of line |
| `st_distance()` | Distance between geometries |
| `st_intersects()` | Spatial predicate |
| `st_transform()` | CRS transformation |

### Performance

- DuckDB Spatial auto-creates spatial indexes on read
- For large files: use `WHERE` clauses that exploit spatial index (bounding box first)
- Export to Arrow for Python integration: `SELECT * FROM st_read('file.gpkg')`

## QA Checklist

- [ ] GiST index created (PostGIS) or spatial extension loaded (DuckDB)
- [ ] CRS is consistent between stored data and queries
- [ ] Spatial predicates use indexed functions (ST_DWithin, not ST_Distance in WHERE)
- [ ] Large queries use bounding box pre-filter
