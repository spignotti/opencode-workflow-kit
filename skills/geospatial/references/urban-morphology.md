---
name: urban-morphology
description: Urban geometry analysis — building footprints, morphometric features (FAR, SVF, compactness), street network centrality, LCZ classification, UHI/SUHI features. Load when analyzing urban form or preparing urban features for thermal/energy/mobility models.
---

## Building Footprints

| Source | Coverage | Attributes | Best For |
|--------|----------|------------|----------|
| OSM via OSMnx | Global, best in cities | Varies, limited height | Street networks, outlines |
| Microsoft Building Footprints | US, Canada, parts of Europe | No height | Large-area coverage |
| Google Open Buildings | Global (ML-derived) | No height, confidence | Areas without OSM |
| Amtliche Daten (ALKIS) | Germany (local) | Height, usage, full | Precision urban analysis |

```python
import osmnx as ox

gdf = ox.features_from_place("Berlin, Germany", tags={"building": True})
gdf = gdf[gdf.geometry.type.isin(["Polygon", "MultiPolygon"])].copy()
gdf = gdf.to_crs("EPSG:25833")  # project to meters
```

**Quality**: OSM completeness varies by neighborhood. ML-derived footprints may have rough edges. Height data is the main bottleneck for FAR/volume/SVF.

## Morphometric Features (momepy)

| Feature | What It Measures | momepy Function |
|---------|-----------------|-----------------|
| Area | Building footprint size | `gdf.geometry.area` |
| Perimeter | Boundary complexity | `gdf.geometry.length` |
| Compactness | Circle-likeness (1.0 = circle) | 4π × area / perimeter² |
| Elongation | Shape stretch | length / width ratio |
| Orientation | Facing direction | `momepy.Orientation` |
| Convexity | Concavity | area / convex_hull area |
| Equivalent area | Circle with same area | `momepy.EquivalentArea` |
| Rectangularity | Fill ratio of bounding rect | area / bounding_rect area |

**Height-dependent features** (need DSM/LiDAR or CityGML):

| Feature | Formula | Use Case |
|---------|---------|----------|
| FAR (Floor Area Ratio) | total_floor_area / plot_area | Density |
| SVF (Sky View Factor) | from DSM analysis | Urban canyon effect |
| Volume | footprint_area × height | 3D density |

## Street Network Centrality

```python
import osmnx as ox

G = ox.graph_from_place("Berlin, Germany", network_type="drive")

# Betweenness centrality
bc = ox.betweenness_centrality(G, weight="length")
nx.set_node_attributes(G, bc, "betweenness")

# Closeness centrality
cc = ox.closeness_centrality(G, distance="length")
nx.set_node_attributes(G, cc, "closeness")
```

| Centrality | Question | Use Case |
|------------|----------|----------|
| Betweenness | "Which streets are through-routes?" | Traffic, noise |
| Closeness | "Which locations are most accessible?" | Accessibility, real estate |
| Degree | "Which intersections have most connections?" | Network connectivity |

## Local Climate Zone (LCZ) Classification

| LCZ | Name | Description |
|-----|------|-------------|
| 1-3 | Built-up (dense to open) | Tall buildings, high to low coverage |
| 4-6 | Built-up (open) | Low-rise, open spacing |
| 7-9 | Built-up (sparsely built) | Very low density |
| A-F | Land cover | Trees, low vegetation, bare rock, water, snow, impervious |

**Derivation**: combine building height/density + vegetation fraction + impervious fraction. Use OSM + remote sensing (NDVI for vegetation, NDWI for water).

## UHI/SUHI Feature Engineering

| Feature | Source | Use Case |
|---------|--------|----------|
| Sky View Factor | DSM / 3D model | Nocturnal UHI intensity |
| Building height variance | LiDAR / CityGML | Canyon geometry |
| Vegetation fraction | NDVI from RS | Evapotranspiration cooling |
| Impervious fraction | Land cover classification | Surface heat storage |
| Street connectivity | OSM network | Airflow, ventilation |
| Distance to water | Hydrology layer | Cooling effect |

## QA Checklist

- [ ] Building footprints validated against known count for the area
- [ ] CRS projected to meters for morphometric calculations
- [ ] Height data source documented (OSM, LiDAR, CityGML)
- [ ] Morphometric features computed at consistent spatial unit (building, block, grid)
- [ ] Street network covers the full study area
