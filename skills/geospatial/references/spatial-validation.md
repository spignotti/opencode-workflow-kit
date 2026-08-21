---
name: spatial-validation
description: Spatial train/test splitting, cross-validation, and leakage prevention for ML on geodata. Load whenever training models on spatial data.
---

## Why Spatial Validation Matters

Spatial data has autocorrelation — nearby locations are more similar than distant ones. Random train/test splits leak information: a model can "see" the answer through neighboring training points. This inflates test metrics by 10-50% in practice.

**Rule**: never use `train_test_split(random_state=...)` on spatial data without spatial awareness.

## Spatial Block Cross-Validation

The recommended default for spatial point data:

```python
from sklearn.model_selection import GroupKFold
import numpy as np

# Create spatial blocks (e.g., 5km grid)
df['block'] = h3.latlng_to_cell(df.lat, df.lon, resolution=7)

# GroupKFold ensures same block stays in same fold
gkf = GroupKFold(n_splits=5)
for train_idx, test_idx in gkf.split(X, y, groups=df['block']):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
```

| Method | Spatial Awareness | Implementation |
|--------|------------------|----------------|
| Random split | None | `train_test_split` — **do not use for spatial data** |
| Spatial block CV | Blocks keep neighbors together | `GroupKFold` with H3 or grid blocks |
| Buffer exclusion | Excludes buffer zone around test points | Manual buffer + mask |
| Leave-one-cluster-out | Groups by spatial cluster | `GroupKFold` with region labels |
| Chronological | Respects time, ignores space | Sort by timestamp, split by date |

## Buffer Exclusion

For high-autocorrelation data (e.g., soil samples, air quality sensors):

```python
# For each test point, exclude training points within buffer
from shapely.geometry import Point

buffer_m = 1000  # 1 km exclusion zone
test_geom = gdf.iloc[test_idx].geometry
train_geom = gdf.iloc[train_idx].geometry

# Keep only train points outside buffer
mask = train_geom.apply(lambda g: all(g.distance(t) > buffer_m for t in test_geom))
clean_train = gdf.iloc[train_idx][mask]
```

## Leakage Prevention

Common spatial leakage patterns:

| Pattern | How It Leaks | Fix |
|---------|-------------|-----|
| Random split on clustered data | Neighbors in train and test | Block CV or buffer exclusion |
| Feature engineering before split | Global stats (mean, std) computed on full data | Compute stats within train fold only |
| Temporal overlap | Same location, same time in train and test | Chronological split |
| Aggregation before split | Aggregated features leak spatial context | Split at raw level, aggregate after |

**Feature engineering rule**: any feature that uses global statistics (e.g., regional mean NDVI, distance to city center computed on full dataset) must be computed within the training fold only. Use `Pipeline` to prevent leakage.

```python
from sklearn.pipeline import Pipeline

# Correct: stats computed within each CV fold
pipe = Pipeline([
    ('features', SpatialFeatureEngineer()),  # computes stats on train only
    ('model', RandomForestRegressor())
])
```

## Metrics

Report spatial CV metrics, not random-split metrics:

| Metric | When | Notes |
|--------|------|-------|
| RMSE / MAE | Regression | Standard, interpretable |
| R² | Regression | Baseline-comparable |
| F1 / AUC-ROC | Classification | Standard |
| Spatial autocorrelation of residuals | Both | Moran's I on residuals — should be non-significant |

**Always report**: spatial CV score ± std, and Moran's I of residuals. If residuals show spatial autocorrelation, the model is missing spatial structure.

## QA Checklist

- [ ] Train/test split is spatially aware (no random split)
- [ ] Feature engineering happens inside the CV pipeline (no global stats leak)
- [ ] Buffer exclusion applied if data has strong spatial autocorrelation
- [ ] Spatial CV score reported (not random-split score)
- [ ] Residual spatial autocorrelation checked (Moran's I)
