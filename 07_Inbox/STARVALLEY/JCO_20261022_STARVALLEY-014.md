---
id: STARVALLEY-014
title: Check coordinate system of LandXML, shapefiles and DEM against the model grid
type: qc_rule
function: data-gathering
trigger: Using LandXML surfaces, CAD/DXF or shapefiles from the civil design team
  with a FLO-2D grid in State Plane
steps:
- Do not trust declared EPSG metadata; compare a few known points to the model grid
- Apply the documented local-to-State Plane transform (translate, rotate, scale about
  base point) when the file is in local site coordinates
- LandXML P order is northing, easting, elevation; interpolate on original triangles,
  exclude invisible faces, no extrapolation across voids
- USGS 1 m DEM is UTM meters; convert to ft and compare to survey (mean and std dev)
  before use
- Preserve CAD arcs with a chord tolerance before transforming
gotchas:
- LandXML declared EPSG:2223 but was in local coordinates; watershed and parcel shapefiles
  likewise had State Plane .prj with local coordinates
- Old channel files sat about 50 ft off the true centerline
- One CAD vertex differed by 100 ft and was excluded
jurisdiction: FEMA Region IX / Pima County RFCD
tools_versions: Python 3.12, QGIS 3.44.12, NAD83 AZ Central Intl ft, NAVD88
evidence:
- D:\Star Valley CLOMR\SV-CLOMR-AD02-CONTINUATION.md
- D:\SV-BLIND-CLOMR\_WORK\00_Admin\judgment_register.json
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\svlib.py
hours_lost: 3.0
recurrence: 3
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:12+00:00'
schema_version: 1
---
