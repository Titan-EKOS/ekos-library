---
id: EKOS-LOCAL-015
title: Confirm basin outlet topology from as-builts and log owner assumptions as scenarios
type: qc_rule
function: hydrology
trigger: Detention basin routing where outlet pipe, overflow weir or spill path is
  not surveyed
steps:
- Search as-built plans and GIS pipe layers for outlet pipe, overflow weir and spill
  route before modeling
- Ask the owner once for a preliminary assumption if records are missing; store it
  as a versioned scenario with source = owner
- Preliminary default used here - 24 in RCP inlet 1 ft above basin bottom, straight-line
  length, outlet above downstream channel bottom
- Fallback when no invert data - set pipe from lidar with min 1 ft cover, tie to outfall
  ground
- Supersede earlier clarifications explicitly (keep SUPERSEDED file), never silently
  overwrite
gotchas:
- Outlet description changed twice in one session (spill to right of way swale, then
  bottom pipe plus overflow weir); routing built on the first version had to be redone
- Assumed pipe produced 0.017 percent slope; flag implausible slopes rather than adopting
  them
- 'Recurrence note: 3 clarifications'
jurisdiction: Pima County RFCD
tools_versions: HEC-HMS 4.13, GIS
evidence:
- D:\EKOS\Library\00_Inventory\_local\codex_text\D_LocalAI_Test\2026-09-21_d92e6073ab48.txt
  (from Codex session 2026-09-21, owner prompts U12, U21-U23)
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\00_Admin\BASIN_OUTLET_OWNER_CLARIFICATION_SUPERSEDED.json
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\00_Admin\BASIN_FIRST_TEST_ASSUMPTIONS.json
hours_lost: 2.0
recurrence: 3
confidence: medium
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:19+00:00'
schema_version: 1
---
