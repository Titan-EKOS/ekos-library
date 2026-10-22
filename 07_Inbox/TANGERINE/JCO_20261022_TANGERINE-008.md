---
id: TANGERINE-008
title: FLO-2D output to GIS rasters for flood context exhibits
type: skill
function: exhibits
trigger: A supplied FLO-2D export must be mapped (max depth, max WSE) with FEMA zones
steps:
- Read TOPO.DAT, DEPTH.OUT and MAXWSELEV.OUT; assert their cell coordinates match
- Grid the values on the model cell size (100 ft here) using the bounds of a correctly
  tagged MapCrafter raster
- Take WSE directly from MAXWSELEV.OUT; do not derive it from depth plus a different
  terrain
- Mask dry cells (WSE coded 0) and depths below 0.1 ft; keep cell edges visible
- Clip FEMA S_FLD_HAZ_AR, S_BFE, S_XS, S_LOMR to the extent and label the sheet a
  source review draft until return period, condition and vertical datum are confirmed
gotchas:
- MapCrafter MAXIMUM_DEPTH.tif carried a California CRS tag (EPSG 3498) while its
  identical twin MAXIMUM_DEPTH (1).tif carried AZ Central EPSG 2223; compare arrays
  and CRS before use
- WSE minus terrain minus depth showed large residuals driven by dry zero cells; compute
  residuals on wet cells only
- Aerial EPSG came only from filenames and world files; record that assumption on
  the sheet
jurisdiction: Town of Marana; FEMA
tools_versions: FLO-2D export (MapCrafter), rasterio, geopandas, matplotlib
evidence:
- C:\Ekos\projects\tangerine\prepare_gis.py
- C:\Ekos\projects\tangerine\make_flood_maps.py
- C:\Ekos\projects\tangerine\README.md
- C:\Ekos\projects\tangerine\deliverables\flood_context_draft\READ_ME.txt
hours_lost: 1.0
recurrence: 1
confidence: high
project: TANGERINE
source_ai: claude
timestamp: '2026-10-22T23:35:08+00:00'
schema_version: 1
---
