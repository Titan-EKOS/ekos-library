---
id: SILVERBELL-006
title: Scripted RAS terrain creation fails without proper GDAL init
type: skill
function: hydraulics-model-run
trigger: Creating RAS terrain HDF from a GeoTIFF by script instead of the RAS Mapper
  GUI.
steps:
- Initialize native GDAL and a console progress display before TerrainComputable.
- Pass NaN for the unused tile-write parameter.
- Create raster statistics, then overviews, in that order, before import.
- Verify the terrain HDF exists and its extent before associating it with a geometry.
gotchas:
- Eight helper builds over about 30 min returned No target dataset specified until
  NaN and stats/overview order were fixed.
- Several RasMapperLib scripting commands (GenerateMesh, SetGeometryAssociation XMLSave)
  are not implemented; check the inventory before scripting.
jurisdiction: n/a
tools_versions: HEC-RAS RasMapperLib .NET API
evidence:
- C:\Ekos\projects\silverbell\v4\CURRENT_STATUS_2026-09-13.md
- C:\Ekos\projects\silverbell\v4\CHECKPOINT_1348.md
- C:\Ekos\projects\silverbell\v4\terrain_run_il.txt
- C:\Ekos\projects\silverbell\hydraulics\ras_command_templates.txt
hours_lost: 1.5
recurrence: 8
confidence: medium
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:23+00:00'
schema_version: 1
---
