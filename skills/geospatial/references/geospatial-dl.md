---
name: geospatial-dl
description: Deep learning on Earth Observation data — model loading, fine-tuning, STAC-to-GPU streaming, tiling/stitching inference, training best practices. Load when training or deploying DL on satellite or aerial imagery.
---

## Setup

```bash
uv add torch torchvision torchgeo  # geo datasets, samplers, transforms
uv add xarray rioxarray             # N-D array handling
uv add "stacchip[all]"              # STAC → ML training chips
uv add odc-stac stackstac           # lazy STAC → array
uv add xbatcher                     # batched streaming from xarray
```

## Data Pipeline: STAC → GPU

Stream from cloud storage without intermediate files:

```python
import pystac_client, odc.stac, xarray as xr, xbatcher

catalog = pystac_client.Client.open("https://earth-search.aws.element84.com/v1")
items = catalog.search(bbox=[13.3, 52.4, 13.5, 52.6], datetime="2024-06-01/2024-09-33")

ds = odc.stac.load(list(items.items()), bands=["B04", "B03", "B02", "B08"],
                    bbox=[13.3, 52.4, 13.5, 52.6], resolution=10)

# Batch into chips
batches = xbatcher.BatchGenerator(ds, input_dims={"x": 256, "y": 256}, batch_size=8)
```

**No TFRecords or `.npy` patches** — streaming means changing patch size or bands is one parameter, not a re-engineering effort.

## Model Access

| Model | Type | Access |
|-------|------|--------|
| Prithvi (NASA) | Foundation model | HuggingFace Hub |
| Clay | Foundation model | HuggingFace Hub |
| TorchGeo models | Classification/segmentation | `torchgeo.models` |
| Custom | Fine-tuned | Train from scratch or fine-tune foundation |

## Training Pattern

```python
from torchgeo.trainers import SemanticSegmentationTask

task = SemanticSegmentationTask(
    model="resnet50",
    weights="imagenet",
    num_classes=n_classes,
    learning_rate=1e-3,
)
trainer = pl.Trainer(max_epochs=50, accelerator="gpu")
trainer.fit(task, datamodule)
```

## Inference: Tiling and Stitching

For large rasters that don't fit in memory:

```python
from rasterio.windows import from_bounds

# Tile → predict → stitch
for window in windows:
    chip = raster.read(window=window)
    pred = model.predict(chip)
    out.write(pred, window=window)
```

## Common Pitfalls

- **Band order mismatch**: S2 is B4/B3/B2/B8, Landsat is SR_B4/SR_B3/SR_B2/SR_B5. Check `bandNames()` before training.
- **Resolution mismatch**: resample all inputs to the same resolution before batching.
- **Label leakage**: ensure train and test tiles don't overlap spatially.
- **Memory**: use mixed precision (`fp16`) and gradient accumulation for large chips.
