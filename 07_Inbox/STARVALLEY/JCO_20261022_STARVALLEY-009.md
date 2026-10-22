---
id: STARVALLEY-009
title: Flood zone delineation from FLO-2D depth grid
type: skill
function: exhibits
trigger: Producing effective and proposed Zone AE/AO delineations and BFE contours
  from FLO-2D results for a CLOMR work map
steps:
- 'Use the depth-to-zone table of the effective study: under 1 ft X; 1.0-1.5 AO(1);
  1.5-2.5 AO(2); 2.5-3.0 AO(3); over 3 ft AE'
- Assign AE to channel cells, the connected inundated corridor along each 1D channel
  segment, and detention basins
- Generate 1-ft BFE contours inside AE from MAXWSELEV
- Write EFF/EXI/proposed zone shapefiles with acreage table; map vector delineations,
  not depth rasters
- Include zone shapefiles in the GIS package and match the work map
gotchas:
- Reviewer rejected depth rasters presented as the work map and flagged the channel
  and over-3-ft basins still shown as Zone A/AO
- Zone shapefiles built in June were left out of the upload; package QC must check
  they exist
jurisdiction: FEMA Region IX / Pima County RFCD
tools_versions: Python 3.12, rasterio, geopandas, scipy, QGIS 3.44.12
evidence:
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\zones.py
- D:\Star Valley CLOMR\SV-CLOMR-AD02-Comment-Tracking-Matrix.xlsx
hours_lost: 6.0
recurrence: 2
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:10+00:00'
schema_version: 1
---
