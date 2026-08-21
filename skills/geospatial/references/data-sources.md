# Geospatial Data Sources

Curated catalog of public, reproducible geospatial datasets and the portals that serve them. Dataset-first: choose the dataset you need, then go through the access source listed under `via`. This is selection guidance — verify API signatures and current terms via Context7 or the official page at use time.

## Conventions

- **`via <source>`** names the access source(s) from the [Access Source Directory](#access-source-directory). One dataset can be served by several sources; one source can serve several datasets.
- **`verified: YYYY-MM-DD`** marks the last reconciliation against first-party documentation (this file: 2026-08-14).
- Free-tier quotas, feature counts, and prices are deliberately omitted — they drift. Check the official page.
- "Free" means free to download/use under the stated license; registration may still be required.
- License labels are exact where verified: public domain, CC BY, CC BY-NC, CDLA Permissive, ODbL. They are not interchangeable — check before publishing derived work.
- `"open (registration)"` — free and open access under the provider's data policy, with account creation required (e.g., Copernicus Sentinel data via CDSE).
- Paid/aggregated sources (e.g. Planet TFO, Sentinel Hub, Mapbox, UP42, Statista) are out of scope; this catalog is for public, reproducible data.

## Dataset catalog

### Satellite imagery & Earth observation

Selection notes: optical → Sentinel-2 / Landsat; radar (all-weather) → Sentinel-1 or Umbra; atmosphere → Sentinel-5P; nightlights → VIIRS/DMSP; crisis VHR → Vantor / Planet / Umbra.

- **Landsat** (USGS/NASA) — Global; 30 m; 1972–today; public domain. via USGS (EarthExplorer / National Map), NASA Earthdata. https://www.usgs.gov/landsat-mission · verified 2026-08-14
- **MODIS** (NASA) — Global; 250 m–1 km; 2000–today (daily); open. via NASA Earthdata. https://modis.gsfc.nasa.gov/ · verified 2026-08-14
- **Sentinel-1 SAR** (ESA/Copernicus) — Global; 5–20 m C-band SAR; 2014–today; open (registration). via CDSE. https://dataspace.copernicus.eu/ · verified 2026-08-14
- **Sentinel-2 MSI** (ESA/Copernicus) — Global; 10/20/60 m, 13 bands; 2015–today; open (registration). via CDSE. https://dataspace.copernicus.eu/ · verified 2026-08-14
- **Sentinel-3 OLCI/SLSTR** (ESA/EUMETSAT) — Global ocean/land surface; 300 m; 2016–today; open (registration). via CDSE. https://dataspace.copernicus.eu/ · verified 2026-08-14
- **Sentinel-5P TROPOMI** (ESA/KNMI) — Global air-quality trace gases; ~5.5 × 3.5 km; 2017–today; open (registration). via CDSE. https://dataspace.copernicus.eu/ · verified 2026-08-14
- **DMSP-OLS Archive** (NOAA/EOG) — Global nightlights; ~5 km (30 arc-sec); 1992–2013; public domain. via EOG. https://eogdata.mines.edu/products/vnl/ · verified 2026-08-14
- **VIIRS DNB Composites** (Colorado School of Mines/EOG) — Global nightlights; ~742 m; 2012–today; CC BY. via EOG. https://eogdata.mines.edu/products/vnl/ · verified 2026-08-14
- **Umbra Open Data** (Umbra Space) — VHR SAR up to 16 cm; 1000+ global sites; 2021–today; CC BY. https://umbra.space/open-data/ · verified 2026-08-14
- **Wyvern Open Data** (Wyvern) — Hyperspectral, 23 bands, 5.3 m; selected scenes; 2024–today; CC BY. https://opendata.wyvern.space/ · verified 2026-08-14
- **Vantor Open Data Program** (Vantor, formerly Maxar Open Data) — VHR optical for disaster response; 30 cm–1.2 m; event-based; **CC BY-NC 4.0** (non-commercial). https://vantor.com/company/open-data-program/ · verified 2026-08-14
- **Planet Crisis Response** (Planet Labs) — Daily PlanetScope, 3–5 m, disaster zones; free for qualified organizations, annual renewal. https://www.planet.com/disasterdata/ · verified 2026-08-14

### Elevation & terrain

Selection notes: global DSM → Copernicus DEM / SRTM; terrain with vegetation removed → FABDEM; LiDAR point clouds → OpenTopography / USGS 3DEP; bathymetry → GEBCO.

- **SRTM GL1** (NASA/USGS) — Global 60°N–56°S; 30 m DSM; Feb 2000 acquisition; public domain. via OpenTopography, NASA Earthdata. https://portal.opentopography.org/datasetMetadata?otCollectionID=OT.112020.4326.1 · verified 2026-08-14
- **Copernicus DEM GLO-30** (ESA/DLR/Airbus) — Global; 30 m (GLO-30) / 90 m (GLO-90) DSM; TanDEM-X based; open. via OpenTopography. https://portal.opentopography.org/datasetMetadata?otCollectionID=OT.032021.4326.1 · verified 2026-08-14
- **ALOS AW3D30** (JAXA) — Global; 30 m DSM; photogrammetric, 2006–2011 imagery; open. via OpenTopography. https://www.eorc.jaxa.jp/ALOS/en/aw3d30/index.htm · verified 2026-08-14
- **FABDEM** (University of Bristol / Fathom) — Global; 30 m DTM with vegetation/building artefacts removed; free download; CC BY 4.0. https://data.bris.ac.uk/data/dataset/s5hqmjcdj8yo2ibzi9b4ew3sn · verified 2026-08-14
- **GEBCO Grid** (Nippon Foundation/GEBCO) — Global ocean bathymetry + land; ~450 m (15 arc-sec); annual releases (GEBCO_2026 at time of writing); public domain. https://www.gebco.net/ · verified 2026-08-14
- **USGS 3DEP** (USGS) — USA (growing coverage); LiDAR point clouds, 1 m DEMs (S1M product), derivatives; free, no use restrictions. via USGS (EarthExplorer / National Map). https://www.usgs.gov/3d-elevation-program · verified 2026-08-14

### Hydrology & water

- **JRC Global Surface Water** (JRC/Google) — Global 56°S–82.8°N; 30 m; 1984–2021, pixel-level statistics; open. https://global-surface-water.appspot.com/ · verified 2026-08-14
- **HydroSHEDS** (WWF/USGS) — Global south of 60°N; hydrographic vectors + rasters, 3–30 arc-sec; static reference model; free (CC BY). https://www.hydrosheds.org/ · verified 2026-08-14

### Soil

- **SoilGrids** (ISRIC) — Global; 250 m; soil properties (pH, SOC, bulk density, texture, CEC, nitrogen, ...) for six depth intervals, with per-pixel uncertainty; CC BY 4.0. Download via soilgrids.org; the REST API is a beta service without uptime guarantee (temporarily paused at time of writing) — prefer direct downloads. https://soilgrids.org/ · verified 2026-08-14

### Land cover & settlement

Selection notes: global land cover → WorldCover (10 m) or ESRI LULC (10 m, annual); Europe → CORINE/CLCplus, Urban Atlas for cities; buildings → OSM, Microsoft or Google footprints; settlement time series → GHSL / WSF.

- **CORINE Land Cover** (EEA/Copernicus) — Europe; 100 m / 25 ha MMU; 1990–2018 (6-year cycles); 44 classes; open. Superseded by CLCplus on CLMS. via CLMS. https://land.copernicus.eu/pan-european/corine-land-cover · verified 2026-08-14
- **NLCD** (USGS/MRLC) — USA; 30 m; National Land Cover Database — legacy 2001–2021, **Annual NLCD Collection 1.2 covers 1985–2025**; public domain. https://www.mrlc.gov/ · verified 2026-08-14
- **ESRI/Microsoft Global Land Cover** (ESRI/Microsoft) — Global; 10 m; 2017–today, annual; CC BY; AI-classified from Sentinel-2. https://livingatlas.arcgis.com/landcover/ · verified 2026-08-14
- **ESA WorldCover** (ESA/VITO) — Global; 10 m, 11 classes; 2020 v100 + 2021 v200 + annual composites; CC BY 4.0. via Terrascope, GEE (also AWS S3 / Zenodo per data-access page). https://esa-worldcover.org/en/data-access · verified 2026-08-14
- **Microsoft Global Building Footprints** (Microsoft AI for Good) — Large multi-country coverage; building polygons; snapshot; CDLA Permissive 2.0. Project README: ~1.4B footprints (2014–2024 release). https://github.com/microsoft/GlobalMLBuildingFootprints · verified 2026-08-14
- **Google Open Buildings** (Google Research) — Global South (Africa, South Asia, LatAm); building polygons from 50 cm imagery, confidence score per polygon; CC BY. https://sites.research.google/open-buildings/ · verified 2026-08-14
- **Overture Maps** (Linux Foundation: Meta, Microsoft, Amazon, TomTom + Esri) — Global buildings/places/transportation layers, stable GERS IDs, snapshot releases; CDLA Permissive 2.0. Collaborative aggregation of multiple sources — not an OSM successor. https://overturemaps.org/ · verified 2026-08-14
- **WSF Evolution** (DLR) — Global; 30 m; annual settlement maps 1985–2015 from Landsat archive; open. https://geoservice.dlr.de/web/maps/eoc:wsfevolution · verified 2026-08-14
- **GHSL — Global Human Settlement Layer** (EU JRC) — Global; 10 m–1 km depending on product; 1975–2030 multitemporal; built-up surface, population; open. https://ghsl.jrc.ec.europa.eu/ · verified 2026-08-14
- **Copernicus Urban Atlas + Building Height** (CLMS) — European functional urban areas; land use/cover (2021 edition) + Building Height 2021 at 10 m; open. via CLMS. https://land.copernicus.eu/en/products/urban-atlas · verified 2026-08-14

### Boundaries & reference layers

- **GADM** (GADM) — Global administrative boundaries, multi-level; free download; license per site terms. https://gadm.org/ · verified 2026-08-14
- **GeoBoundaries** (William & Mary geoLab) — Global administrative boundaries, consolidated per country; CC BY. https://www.geoboundaries.org/ · verified 2026-08-14
- **Natural Earth** (community) — Global vector + raster at 1:10m / 1:50m / 1:110m; admin, hydro, physical layers; public domain. https://www.naturalearthdata.com/ · verified 2026-08-14
- **US Census TIGER/Line** (US Census Bureau) — USA; roads, water, administrative areas; annual; public domain. https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html · verified 2026-08-14
- **OpenAddresses** — Global focus NA/EU; address points from public sources; public domain; continuously updated. https://openaddresses.io/ · verified 2026-08-14
- **OpenStreetMap** (OSM community) — Global; roads, buildings, POIs, land use; ODbL (attribution + share-alike). via Geofabrik, Overpass API. https://www.openstreetmap.org/ · verified 2026-08-14

### Climate & weather

Selection notes: global reanalysis → ERA5 / ERA5-Land; rainfall for data-sparse regions → CHIRPS; monthly water balance → TerraClimate; projections → CMIP6 / CORDEX; quick point weather → Open-Meteo API.

- **ERA5** (ECMWF/C3S) — Global; 25 km; hourly, 1940–today; CC BY. via CDS. https://cds.climate.copernicus.eu/ · verified 2026-08-14
- **ERA5-Land** (ECMWF/C3S) — Global; 0.1° (~9 km native); hourly land variables, 1950–today; CC-BY. via CDS. https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land · verified 2026-08-14
- **CMIP6 Projections** (WCRP) — Global; ~100 km per GCM; 1850–2100, SSP scenarios; open. via CDS. https://cds.climate.copernicus.eu/datasets/projections-cmip6 · verified 2026-08-14
- **CORDEX Projections** (WCRP CORDEX) — 14 global domains; regional downscaling, EUR-11 at 12.5 km; to 2100; open. via CDS. https://cordex.org/ · verified 2026-08-14
- **CHIRPS** (UC Santa Barbara Climate Hazards Center) — 50°S–50°N; 0.05° daily precipitation; 1981–near-present; public domain (CC0). v3 now available — v2 production ends December 2026. https://www.chc.ucsb.edu/data/chirps · verified 2026-08-14
- **TerraClimate** (Climatology Lab) — Global land; ~4 km (1/24°); monthly climate + water balance, 1958–present (v1.1); free netCDF via THREDDS. https://www.climatologylab.org/terraclimate.html · verified 2026-08-14
- **Open-Meteo** (Open-Meteo) — Global; forecast (to 16 days) + historical weather API over national model output; free for non-commercial use, CC BY 4.0 (commercial tier requires key). https://open-meteo.com/en/docs · verified 2026-08-14

### Demographics & socioeconomic

- **WorldPop** (University of Southampton) — Global; 100 m–1 km population rasters, yearly, by age group; 2000–today; CC BY. Sibling product: WorldPop Poverty Maps (development indicators, ~100 m–1 km). https://www.worldpop.org/ · verified 2026-08-14
- **GRID3 Population** (CIESIN/UNFPA/Flowminder) — Sub-Saharan Africa focus; ~100 m cells; satellite + ML-based micro-census estimates; CC BY. https://data.grid3.org/ · verified 2026-08-14
- **LandScan Global** (Oak Ridge National Laboratory) — Global; ~1 km (30 arc-sec); annual population distribution (2024 release); free download with registration. https://landscan.ornl.gov/ · verified 2026-08-14
- **Gridded Global GDP** (Kummu et al., Aalto) — Global; 30 arc-sec (~1 km); 1990–2022 (2025 release); CC BY; dasymetric downscaling with OECD validation. via GEE. https://gee-community-catalog.org/projects/gridded_gdp_hdi/ · verified 2026-08-14
- **HREA Dataset** (University of Michigan) — Global development focus; ~500 m; electricity access/reliability 2012–today from VIIRS nightlights; open. https://public.websites.umich.edu/~brianmin/HREA/ · verified 2026-08-14
- **EEA Strategic Noise Maps** (European Environment Agency) — Europe; noise contours per EU directive, 5 dB bands; 5-year cycles (round 4, 2021); CC BY. https://www.eea.europa.eu/en/data-and-maps/ · verified 2026-08-14
- **NASA SEDAC** (CIESIN/NASA) — Global population/environment (GPWv4 etc.); free; now served via Earthdata Cloud / AppEEARS. https://sedac.ciesin.columbia.edu/ · verified 2026-08-14
- **Eurostat** (EU) — Europe; population, economy, environment, mobility statistics; free, API available. https://ec.europa.eu/eurostat · verified 2026-08-14

### Energy & infrastructure

- **Global Power Plant Database** (WRI) — Global; point locations of power plants with fuel, capacity, generation; open, v1.3.0 (updated Oct 2025). via WRI Data Explorer. https://datasets.wri.org/dataset/globalpowerplantdatabase · verified 2026-08-14

### Transport & mobility

- **GTFS Feeds** (MobilityData / agencies) — 2000+ transit agencies globally; stops + schedules in the GTFS standard; open. https://mobilitydatabase.org/ · verified 2026-08-14
- **OpenCelliD** (Unwired Labs) — Global; crowdsourced cell tower locations + parameters; CC BY. https://opencellid.org/ · verified 2026-08-14
- **OpenFlights** — Global; airport coordinates, routes, aircraft; open; historically maintained. https://openflights.org/data · verified 2026-08-14

### ML benchmarks & research data

Selection notes: EO classification benchmarks → EuroSAT / BigEarthNet; object detection → fMoW; pretraining corpus → MajorTOM; tree species → TreeSatAI / GlobalGeoTree. Research repositories below serve supplementary raw data.

- **EuroSAT** (DFKI) — Europe (34 countries); 27k Sentinel-2 patches, 10 land-use/land-cover classes; open. https://github.com/phelber/EuroSAT · verified 2026-08-14
- **BigEarthNet v2.0** (TU Berlin/BIFOLD) — Europe (10 countries); multi-label Sentinel-1+2, CORINE classes; CDLA Permissive. https://huggingface.co/datasets/BIFOLD-BigEarthNetv2-0/BigEarthNet.txt · verified 2026-08-14
- **fMoW — Functional Map of the World** (IARPA) — Global; VHR satellite object detection, 62 categories, temporal context; open. https://github.com/fMoW/dataset · verified 2026-08-14
- **MajorTOM** (ESA Φ-lab) — Global; 23 TB Sentinel-2 L2A pretraining patches; open. https://huggingface.co/Major-TOM · verified 2026-08-14
- **TreeSatAI** (Uni Göttingen / Niedersächsische Landesforsten) — Lower Saxony; tree species benchmark, 20 species/15 genera, Sentinel-1/2 + aerial; CC BY. https://zenodo.org/records/6780578 · verified 2026-08-14
- **GlobalGeoTree** (research community) — Global; 6.3M geolocated occurrences, 21k+ tree species; zero-/few-shot species recognition benchmark; open. https://github.com/MUYang99/GlobalGeoTree · verified 2026-08-14
- **Research repositories** — supplementary raw data: PANGAEA (https://www.pangaea.de/), GFZ Data Services (https://dataservices.gfz-potsdam.de/), Zenodo (https://zenodo.org/), Harvard Dataverse (https://dataverse.harvard.edu) · verified 2026-08-14

## Access source directory

Portals and platforms that grant access to the datasets above. Aggregators are access layers, not data producers — confirm the underlying dataset license before use.

| Source | Role | Principal datasets | Access |
|--------|------|--------------------|--------|
| Copernicus Data Space Ecosystem (CDSE) | Sentinel data + CLMS distribution, successor of the retired SciHub | Sentinel-1/2/3/5P, CLMS products | Free registration; STAC/OData/S3/openEO. https://dataspace.copernicus.eu/ |
| Copernicus Climate Data Store (CDS) | C3S reanalysis/projection distribution | ERA5, ERA5-Land, CMIP6, CORDEX | Free registration; cdsapi; CC BY. https://cds.climate.copernicus.eu/ |
| Copernicus Atmosphere Data Store (ADS) | CAMS atmosphere monitoring | Global/regional air-quality analyses, forecasts | Free registration; cdsapi. https://ads.atmosphere.copernicus.eu/ |
| Copernicus Land Monitoring Service (CLMS) | Copernicus land products | CORINE/CLCplus, Urban Atlas + Building Height, GHSL-family | Free; land.copernicus.eu. https://land.copernicus.eu/ |
| NASA Earthdata | NASA EO/earth-science distribution | MODIS, SRTM, Landsat (joint), SEDAC, GPM | Free registration; Earthdata Login. https://earthdata.nasa.gov/ |
| USGS (EarthExplorer / National Map) | US federal elevation/imagery | Landsat, 3DEP LiDAR, TIGER-family | Free; public domain. https://earthexplorer.usgs.gov/ |
| OpenTopography | LiDAR/DEM portal | SRTM, Copernicus DEM, AW3D30, point clouds | Free registration. https://opentopography.org/ |
| Google Earth Engine (GEE) | Multi-petabyte cloud catalog + compute | WorldCover, CHIRPS, GDP grids, many others | Free registration; quota-limited. https://earthengine.google.com/ |
| Microsoft Planetary Computer | STAC + hosted analytics | Open EO/climate collections, SAS-signed assets | Free; STAC API. https://planetarycomputer.microsoft.com/ |
| AWS Earth Search (Element 84) | Open STAC catalog on AWS RODA | Sentinel-2 COGs, no egress cost | Open STAC. https://earth-search.aws.element84.com/ |
| Terrascope (VITO) | Belgian EO platform | ESA WorldCover, composites | Free registration. https://terrascope.be/ |
| EOG (Colorado School of Mines) | Nightlights distribution | DMSP-OLS, VIIRS DNB | Free download. https://eogdata.mines.edu/products/vnl/ |
| Geofabrik | OSM regional extracts | OpenStreetMap PBF downloads | Free download. https://download.geofabrik.de/ |
| Overpass API | OSM query API | OpenStreetMap subsets (e.g. all benches in a city) | Free, rate-limited. https://wiki.openstreetmap.org/wiki/Overpass_API |
| NOAA Data Access | US ocean/atmosphere | Weather, climate, coastal, oceanographic | Free. https://www.noaa.gov/products/data |
| OpenAQ | Global air-quality aggregator | Real-time + historical air quality | Free API. https://openaq.org/ |
| Global Forest Watch | Forest monitoring portal | Deforestation, fires, CO2 emissions layers | Free; API with geostore. https://data.globalforestwatch.org/ |
| Humanitarian Data Exchange (HDX) | UN OCHA humanitarian data | Crisis indicators, subnational admin stats | Free; CKAN/HAPI API. https://data.humdata.org/ |
| EMODnet | European marine in-situ data | Bathymetry, biology, physical time series | Free. https://emodnet.ec.europa.eu/ |
| INSPIRE Geoportal | EU INSPIRE metadata + services | INSPIRE-conformant datasets, WFS/WMS | Free. https://inspire-geoportal.ec.europa.eu/ |
| data.europa.eu | EU open-data meta-portal | Aggregated metadata from European public portals | Free; DCAT-AP. https://data.europa.eu/ |
| WRI Data Explorer | WRI open data | Global Power Plant Database | Free download. https://datasets.wri.org/ |

All directory entries verified against their official sites 2026-08-14.

## Germany / DACH public data

Public, reproducible sources for Germany, Austria, and Switzerland. Regional German portals that the old catalog listed individually are consolidated under **Länder portals** below — all are also discoverable via GovData.

### Germany

- **GovData** — Federal, state, and municipal open data; license mix (DL-DE-BY-2.0 / CC BY 4.0 common). https://www.govdata.de/ · verified 2026-08-14
- **DWD Open Data** — Weather and climate data, free of charge by statute; station observations, radar, model output (ICON), Climate Data Center (CDC) archive; WMS/WFS geoservices; no service-level guarantee. https://opendata.dwd.de/ · verified 2026-08-14
- **Destatis GENESIS-Online** — Federal statistics with API access; free; data licence DE / CC BY 4.0 for most tables. https://www.destatis.de/ · verified 2026-08-14
- **BKG Geodatenzentrum** — Federal geobasis data: ATKIS, administrative boundaries, topographic products; free download, attribution required (DL-DE-BY-2.0). https://gdz.bkg.bund.de/ · verified 2026-08-14
- **UBA Umweltbundesamt** — Environmental data: air quality, noise, soil, water, emissions; free. https://www.umweltbundesamt.de/ · verified 2026-08-14
- **BGR Geoportal** — Geological, soil, geophysical, mineral-resource data for Germany and global projects; free. https://geoportal.bgr.de/ · verified 2026-08-14
- **Mobilithek (BMDV)** — National mobility data platform: schedules, real-time traffic, roadworks, charging infrastructure; DATEX II, NeTEx, SIRI, OCPI. https://mobilithek.info/ · verified 2026-08-14
- **Statistik Berlin-Brandenburg** — Regional statistics for Berlin/Brandenburg (demography, economy, urban development). https://www.statistik-berlin-brandenburg.de/ · verified 2026-08-14

**Länder portals** (state geobasis/ALKIS/3D data; also reachable via GovData):

| Portal | Unique data | URL |
|--------|-------------|-----|
| Geoportal Berlin | LOR planning areas, environmental atlas, ALKIS | https://gdi.berlin.de/viewer/ |
| Geoportal Brandenburg | State geodata from 100+ providers, WFS/WMS | https://geoportal.brandenburg.de/ |
| BayernAtlas | Orthophotos, cadastre, 3D DOM mesh, LiDAR | https://geoportal.bayern.de/ |
| GEOportal.NRW | ALKIS, environmental data, LoD2 3D city models | https://www.geoportal.nrw/ |

All four Länder portals verified against their official sites 2026-08-14.

### Austria

- **data.gv.at** — Austrian open-data portal (federal + regional); per-dataset licenses, most federal datasets under the OGD Austria licence (CC BY 4.0). https://www.data.gv.at/ · verified 2026-08-14

### Switzerland

- **data.geo.admin.ch** — Swiss federal geoinformation platform; thousands of `ch.*` collections with download, STAC API, preview, and metadata per dataset; per-dataset licenses (CC BY 4.0 common). https://data.geo.admin.ch/ · verified 2026-08-14

## Catalog maintenance notes

Maintained as a curated catalog (reviewed 2026-08-14):

- **Replaced:** Copernicus SciHub (retired Oct 2023) → CDSE as the primary Sentinel access point.
- **Removed — defunct:** Descartes Labs (domain parked), Radiant MLHub (offline).
- **Removed — paid/aggregated out of scope:** Planet Tropical Forest Observatory (formerly free NICFI basemaps, now paid), Sentinel Hub, Mapbox, UP42, Woosmap, OpenCage (geocoding covered by `geocoding.md`), N2YO (satellite-tracking API), Google Dataset Search (search engine, not a source), OpenML/Kaggle (general ML platforms, not geo), FID GEO (bibliographic service), Bulwiengesa/empirica-regio (paid real-estate).
- **Removed — narrow scope:** OpenTrees.org (aggregator of municipal street-tree registers, no canonical dataset) and GUTI (Global Urban Tree Inventory, static release) — tree data covered by per-city inventories plus GlobalGeoTree / TreeSatAI for tree-species benchmarks.
- **Merged:** DWD CDC ↔ DWD Open Data (one entry); ERA5/CMIP6/CORDEX rows now point at the CDS source; Sentinel rows now point at CDSE; WorldPop Poverty Maps merged into the WorldPop entry as a sibling product.
- **Corrected:** NICFI → renamed and moved to paid (removed); Maxar Open Data → Vantor Open Data Program (CC BY-NC 4.0); NLCD temporal range → Annual Collection 1.2 (1985–2025); GEBCO → annual releases (GEBCO_2026 at time of writing); Microsoft Global Buildings count → ~1.4B per project README; Overture description → collaborative aggregation, not "OSM successor"; FABDEM → free download (was "Freemium"); HydroSHEDS → free (was "Free for Research"); GlobalGeoTree URL → corrected to GitHub repo; CHIRPS → v3 noted as current with v2 sunset Dec 2026.
- **Kept as siblings, documented tradeoff:** GADM vs GeoBoundaries (licensing differs — check per use).
- **Volatile numbers dropped:** free-tier quotas, credits, feature counts, and prices are not catalogued.
