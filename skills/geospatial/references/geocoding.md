---
name: geocoding
description: Address-to-coordinate and coordinate-to-address conversion using geopy, Nominatim, and OpenCage. Load when geocoding addresses, reverse-geocoding coordinates, or batch converting address lists.
---

## Forward Geocoding

```python
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my-app-name")  # required — change per project

# Structured input (recommended for German addresses)
location = geolocator.geocode({
    "street": "Musterstr. 1",
    "postalcode": "10115",
    "city": "Berlin",
    "country": "Germany"
})

# Free-text (more ambiguity)
location = geolocator.geocode("Musterstr. 1, 10115 Berlin")
```

Structured input reduces false matches by ~30-50% for German addresses.

**Always check match quality:**

```python
loc = geolocator.geocode(query, exactly_one=True)
if loc:
    print(f"({loc.latitude}, {loc.longitude})")
    print(f"Address: {loc.address}")
    print(f"Raw: {loc.raw}")  # contains importance, type, confidence hints
```

## Reverse Geocoding

```python
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my-app-name")
location = geolocator.reverse((52.5200, 13.4050), language="de")

if location:
    print(location.address)
    print(location.raw)
```

## Batch Strategies

| Strategy | When | Implementation |
|----------|------|----------------|
| Sequential + delay | <100 addresses | Simple loop with `time.sleep(1)` |
| Parallel + rate limit | 100-10000 | `concurrent.futures` + semaphore |
| Service API | >10000 | OpenCage or Google Geocoding API (paid) |

```python
import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="batch-geocoder")

results = []
for addr in addresses:
    loc = geolocator.geocode(addr)
    if loc:
        results.append({"address": addr, "lat": loc.latitude, "lon": loc.longitude})
    time.sleep(1)  # Nominatim rate limit: 1 req/sec
```

## Rate Limiting

- **Nominatim**: 1 request/second (strict, enforced). Use `user_agent` identifying your app.
- **OpenCage**: 2500 req/day free tier, 50 req/sec paid.
- **Google Geocoding**: 50 req/sec, billing enabled.

## Caching

For repeated queries (same addresses in different sessions):

```python
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent="my-app")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
```

## German Address Specifics

- **Street + house number**: `Musterstr. 1` (with abbreviation dot)
- **Postal code**: 5 digits, always included in structured queries
- **Ortsteil (district)**: useful for disambiguation in large cities
- **Ó (umlaut)**: Nominatim handles `oe` and `ö` equivalently
- **Cadastral parcels (Flurstück)**: not geocodable via standard services — use ALKIS/official cadastral data

## Common Pitfalls

- **No user_agent**: Nominatim returns 401. Always set a unique app name.
- **Rate limiting**: Nominatim bans IPs exceeding 1 req/sec. Respect the limit.
- **Ambiguous queries**: "Berlin" matches multiple locations. Use structured input or add context.
- **Coordinate precision**: geopy returns float64 — sufficient for sub-meter.
