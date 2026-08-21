---
name: spatial-statistics
description: Spatial statistics methodology — autocorrelation (Moran's I, LISA, Gi*), regression (lag/error, GWR), point patterns (Ripley's K, KDE), interpolation (kriging, IDW). Load when analyzing spatial distributions, testing clustering, detecting hotspots.
---

## Library Setup

```bash
uv add pysal  # metapackage: libpysal, esda, spreg, mgwr, pointpats, tobler
```

## Spatial Weights

Everything in spatial statistics depends on weights. Wrong weights → wrong autocorrelation → wrong regression.

| Data Type | Question | Weight Type |
|-----------|----------|-------------|
| Polygons (admin boundaries) | "Do neighboring zones correlate?" | Queen contiguity (default) |
| Polygons (grid/chessboard) | "Do edges-only neighbors correlate?" | Rook contiguity |
| Points or mixed-resolution | "Are k-closest correlated?" | k-nearest neighbors (k=5-10) |
| Points with known range | "Correlation within radius r?" | Distance-band |
| Continuous spatial process | "Closer = more related" | Kernel weights |

```python
import libpysal
w = libpysal.weights.Queen.from_dataframe(gdf)
w.transform = 'R'  # row-standardize (default recommendation)
```

**Islands** (disconnected features): check before computing — `w.islands`. Remove or connect them.

## Spatial Autocorrelation

| Method | Scope | Question | Library |
|--------|-------|----------|---------|
| Moran's I | Global | "Is there overall spatial clustering?" | `esda.Moran` |
| Moran's I (local) | Local (LISA) | "Where are the clusters?" | `esda.Moran_Local` |
| Getis-Ord Gi* | Local | "Where are hot/cold spots?" | `esda.G_Local` |

**Interpretation**: Significant positive Moran's I = clustering. Significant negative = dispersion. LISA clusters: HH (hot spot), LL (cold spot), HL/LH (spatial outliers).

## Spatial Regression

| Model | Use When | Key Assumption |
|-------|----------|----------------|
| OLS (baseline) | First pass, no spatial structure | Independent errors (often violated) |
| Spatial lag | Spatial dependence in Y | Y in one zone affects Y in neighbors |
| Spatial error | Spatial dependence in errors | Unmeasured spatial factors in error term |
| GWR | Relationship varies across space | Non-stationary coefficients |

**Rule**: Never run OLS on spatially data without testing for spatial autocorrelation first. If Moran's I on OLS residuals is significant → switch to lag or error model.

```python
from spreg import ML_Lag, ML_Error

lag_model = ML_Lag(y, X, w, name_y='price', name_x=features)
error_model = ML_Error(y, X, w, name_y='price', name_x=features)
```

## Point Pattern Analysis

| Method | Question | Library |
|--------|----------|---------|
| Ripley's K | Clustered, random, or dispersed at distance r? | `pointpats.distance_statistics` |
| KDE | Where is the density surface? | `esda.gaussian_kde` |
| Quadrat analysis | Are points evenly distributed in cells? | `pointpats.quadrat_statistics` |

## Spatial Interpolation

| Method | Data Type | When |
|--------|-----------|------|
| IDW | Point values | Simple, fast, no assumptions |
| Ordinary kriging | Point values | Best linear unbiased predictor, provides uncertainty |
| Regression kriging | Point + covariates | When auxiliary data improves prediction |

## QA Checklist

- [ ] Spatial weights constructed and verified (no islands unless expected)
- [ ] Row-standardization applied unless binary weights are justified
- [ ] Global autocorrelation tested before regression
- [ ] Residual autocorrelation checked after model fitting
- [ ] GWR bandwidth selected (AICc or cross-validation)
