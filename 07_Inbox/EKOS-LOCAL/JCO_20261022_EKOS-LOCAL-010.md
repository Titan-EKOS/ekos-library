---
id: EKOS-LOCAL-010
title: HEC-RAS 6.6 native automation and geometry handoff (RasProcess and COM)
type: skill
function: hydraulics-model-run
trigger: Creating terrain, geometry, 2D mesh, 1D sections or culverts and running
  RAS without the GUI
steps:
- Run plans through the RAS66.HECRASController COM object on isolated copies; always
  quit the controller
- Create terrain with RasProcess CreateTerrain on the source grid (no resample), explicit
  ESRI projection, units Meters; read back every pixel
- Create geometry with CreateGeometry GeometryFilename=... UnitSystem=si, then GenerateMesh
  with perimeter shapefile and cell size; then CompleteGeometry GeomFilename=... RasMapFilename=...
- Count only the first Cell Count polygons as real cells (rest are ghost centers);
  check no gaps or overlaps
- Write station-elevation blocks in strict 8-character fixed width with Decimal values;
  read the native HDF back for every ordinate, bank, length, roughness
- Discover outputs with Output_Variables and Output_GetNodes; treat 3.4e38 as unavailable,
  not zero
- Keep project units explicit - terrain in m NAVD88, English project geometry needs
  a recorded conversion
gotchas:
- Command-line runs gave no output within 90 s; COM fallback worked for 1D
- PowerShell script execution is disabled on this host; exact CLI arguments came from
  passive .NET metadata (dnfile, dncil), no policy bypass
- CreateGeometry uses GeometryFilename but CompleteGeometry uses GeomFilename
- Culvert names longer than 12 ASCII bytes are silently truncated in the HDF; reject
  before running
- pywin32 GetTypeAttr function count is index 6; index 8 gave a false empty output
  inventory
- CompleteGeometry warned Geometry/Structures not found; do not add fake structures
  to silence it
- Synthetic reach and culvert tests passed but the project 1D/2D model was never completed;
  synthetic success is not a project result
- 'Recurrence note: about 25 RAS tasks, 4 failures, project model not reached'
jurisdiction: General
tools_versions: HEC-RAS 6.6 (RasProcess.exe, RAS66 COM), pywin32, dnfile 0.18.0, h5py
evidence:
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydraulics\KB-002.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydraulics\KB-024.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydraulics\KB-025.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydraulics\KB-026.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydraulics\KB-032.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydraulics\KB-034.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydraulics\KB-035.md
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\00_Admin\Local_Queue\ras-native-geometry-handoff-001.log
hours_lost: 6.0
recurrence: 4
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:18+00:00'
schema_version: 1
---
