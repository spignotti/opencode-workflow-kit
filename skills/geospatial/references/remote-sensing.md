---
name: remote-sensing
description: Satellite and aerial imagery methodology — spectral indices, cloud masking, compositing, time series, atmospheric correction, change detection. Load when working with Sentinel-2, Landsat, MODIS, NAIP.
---

## Sensor Quick Reference

| Sensor | Bands | Resolution | Revisit | BOA Available | QA Available |
|--------|-------|------------|---------|---------------|--------------|
| Sentinel-2 MSI | 13 | 10/20/60 m | 5 d | L2A | SCL band |
| Landsat 8-9 OLI | 11 | 30/100 m | 8 d | Collection 2 L2 | QA_PIXEL |
| MODIS (Terra+Aqua) | 36 (7 for RS) | 250/500/1000 m | 1-2 d | MOD09 series | State_QA |
| NAIP | 4 (R,G,B,NIR) | 0.6-1.0 m | 2-3 yr | N/A | None |

## Cloud and Shadow Masking

Never calculate an index or composite without masking clouds first. Unmasked clouds are the #1 source of silent corruption.

| Sensor | Mask Source | Method |
|--------|-------------|--------|
| Sentinel-2 L2A | SCL band | Keep values 4-7 (veg, bare soil, water, low cloud). Mask 3 (shadow), 8-10 (clouds), 11 (snow), 1 (saturated) |
| Landsat 8-9 L2 | QA_PIXEL | Unpack bits: bit 3=cloud, bit 4=shadow, bit 5=snow. Mask cloud|shadow|high_confidence |
| MODIS MOD09 | State_QA | Bit 0-1: 00=clear, 01=cloudy, 10=mixed. Mask 01 and 10 |
| NAIP | None | No native mask. Use spectral screening or skip — typically flown in clear conditions |

**Shadow handling**: Dilate cloud mask by 2-3 pixels in dominant wind direction. Shadow pixels are dark in SWIR (B11/B12 < 0.05). SCL class 3 = shadow.

## Spectral Indices

| Index | Formula | Use Case |
|-------|---------|----------|
| NDVI | (NIR - Red) / (NIR + Red) | Vegetation health, cover fraction |
| NDWI | (Green - NIR) / (Green + NIR) | Water bodies |
| NBR | (NIR - SWIR2) / (NIR + SWIR2) | Burn severity, vegetation moisture |
| EVI | 2.5 × (NIR - Red) / (NIR + 6×Red - 7.5×Blue + 1) | Dense vegetation (saturation-resistant) |
| NDWI (McFeeters) | (Green - NIR) / (Green + NIR) | Open water |

**Always apply cloud mask before computing indices.** Composite before indexing only if the composite method handles clouds (median, quality mosaic).

## Compositing

| Method | When | Robustness |
|--------|------|------------|
| Median | General purpose, cloud-free | High — outliers (clouds) excluded |
| Quality mosaic | Best-pixel selection (e.g., max NDVI) | High — explicit quality criterion |
| Mean | Dense time series, no outliers | Low — cloud contamination persists |
| Min/Max | Specific use (e.g., min value for snow) | Depends on use case |

## Time Series Analysis

- **Temporal smoothing**: Savitzky-Golay or rolling median for noisy indices
- **Break detection**: BFAST or LandTrendr for disturbance/ recovery
- **Phenology**: Fit double logistic or harmonic model to NDVI curves

## Change Detection

| Method | Data Requirement | Output |
|--------|-----------------|--------|
| Image differencing | 2 dates, same sensor | Continuous change map |
| Image ratioing | 2 dates, same sensor | Relative change |
| Post-classification | 2 classified maps | Thematic change matrix |
| CVA (Change Vector Analysis) | 2 dates, multi-band | Direction + magnitude |

## QA Checklist

- [ ] Cloud mask applied before any index or composite computation
- [ ] CRS is correct and consistent across dates
- [ ] Resolution matches the analysis requirement
- [ ] Nodata values handled (not treated as zero)
- [ ] Scale factors applied (Landsat Collection 2: multiply by 0.0000275, offset -0.2)
