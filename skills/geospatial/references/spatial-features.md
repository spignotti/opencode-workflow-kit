---
name: spatial-features
description: Feature engineering for geospatial ML — spatial joins, zonal stats, distance features, spatial lag, H3 binning, shape descriptors, spatial CV. Load when preparing geodata for ML models.
---

## Spatial Joins

Always check join cardinality: if you expect 1:1, confirm it before trusting downstream features.

| Join Type | Method | Use Case | Cardinality Risk |
|-----------|--------|----------|------------------|
| Point-in-polygon | `predicate='within'` | "Which zone is this point in?" | None (1:1) |
| Polygon on polygon | `predicate='intersects'` | "Which polygons overlap?" | High |
| Nearest polygon | `sjoin_nearest(k=1)` | "What's the closest zone?" | None (1:1) |
| Distance search | `predicate='dwithin'` | "What's within 1 km?" | Medium |

**Performance**: `sjoin` uses R-tree automatically. For >1M rows, pre-filter to bbox first.

**CRS**: distance-based predicates (`dwithin`) on EPSG:4326 are in degrees. Project to local UTM first.

## Zonal Statistics (Raster → Vector)

Extract raster-derived features per polygon or grid cell.

```python
import rasterstats

stats = rasterstats.zonal_stats(
    polygons_gdf, raster_path,
    stats=['mean', 'std', 'min', 'max', 'count'],
    geojson_out=True
)
```

| Aggregation | When |
|-------------|------|
| Mean/median | Average value per zone (e.g., mean NDVI per district) |
| Std | Variability within zone |
| Count | Coverage (e.g., number of valid pixels) |
| Majority | Most common class per zone (land use) |

## Distance Features

| Feature | Method | Use Case |
|---------|--------|----------|
| Nearest distance | `scipy.spatial.cKDTree` | Distance to nearest point of category X |
| K-nearest distances | `cKDTree.query` | Distance to 1st, 2nd, 3rd nearest |
| Distance to line/polygon | `shapely.ops.nearest_points` | Distance to road, river, boundary |
| Buffer-based count | `gpd.sjoin` after buffer | Count of features within radius |

## Spatial Lag Features

| Feature | Method | Use Case |
|---------|--------|----------|
| Spatial lag of Y | `libpysal.weights.lag_spatial(w, y)` | Average value of neighbors |
| Spatial lag of X | Same with covariate | Neighborhood context |
| Moran's I (local) | `esda.Moran_Local` | Cluster/outlier indicator |

## H3 Hex Binning

```python
import h3

# Convert point to H3 index at resolution 8 (~460m edge)
h3_index = h3.latlng_to_cell(lat, lon, resolution=8)

# Aggregate points per hex
df['h3'] = df.apply(lambda r: h3.latlng_to_cell(r.lat, r.lon, 8), axis=1)
hex_counts = df.groupby('h3').size().reset_index(name='count')
```

| Resolution | Edge Length | Use Case |
|------------|-------------|----------|
| 5 | ~2.5 km | Regional analysis |
| 7 | ~1.2 km | City-level |
| 8 | ~460 m | Neighborhood |
| 9 | ~170 m | Block-level |
| 10 | ~65 m | Micro-analysis |

## Geometric Shape Descriptors

From building footprints or polygon layers:

| Feature | Formula | Use Case |
|---------|---------|----------|
| Area | `geometry.area` | Building size |
| Perimeter | `geometry.length` | Boundary complexity |
| Compactness | 4π × area / perimeter² | Circle-likeness (1.0 = circle) |
| Elongation | length / width ratio | Shape stretch |
| Orientation | `shapely.orient` + angle | Facing direction |

## Spatially-Aware Train/Test Split

**Never use random split on spatial data.** Spatial autocorrelation inflates test metrics.

| Method | When | Implementation |
|--------|------|----------------|
| Spatial block CV | Default for point data | `spopt.region_kmeans_kmeans` or manual grid blocks |
| Buffer exclusion | When locations cluster | Exclude buffer around each test point |
| Leave-one-cluster-out | Grouped data (e.g., by region) | `GroupShuffleSplit` with spatial groups |
| Chronological split | Time series | Sort by time, split by date threshold |

## QA Checklist

- [ ] Join cardinality verified (no unexpected many-to-many)
- [ ] CRS projected for distance-based features
- [ ] Spatial lag computed with appropriate weight type
- [ ] Train/test split respects spatial autocorrelation
- [ ] Feature ranges validated (no inf, no NaN from failed joins)
