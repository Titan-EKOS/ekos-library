---
id: EKOS-LOCAL-009
title: HEC-HMS 4.13 scripted detention routing with external PC-Hydro inflow
type: skill
function: hydraulics-model-run
trigger: Building and running an HMS reservoir model from terrain stage-storage and
  PC-Hydro DSS inflows without the GUI
steps:
- Use GAGE_FLOW source with a Flow gage on external DSS; keep a zero meteorology component
  named No Precipitation / No Evapotranspiration
- Write DSS with canonical interval names (1Minute, 1Hour) and INST-VAL; write, close,
  reopen and compare every ordinate before running
- Translate all elevations and stage-storage x values by one documented basin-bottom
  offset (relative datum); keep absolute source values
- Author circular outlets with Diameter, Chart, Scale and End Conduit, and overflow
  with coefficient, top length and top elevation from native examples
- Check stage-storage implied area (dS/dz) against the footprint; flag jumps from
  connected-component masks
- Compute continuity from DSS storage endpoints; run each case in an isolated project
  and keep per-case failures
gotchas:
- Absolute elevation 2687.90658 was saved as 2687.9, below the storage table minimum,
  causing an initial-pool error; relative datum fixed it
- Generic meteorology name None produced Undefined controller errors
- All 100-yr cases failed with native error 40253 (stage above storage curve); do
  not extrapolate the table, enlarge storage with street areas or tune weir width
  to force a pass
- Connected-component stage-storage jumped where a saddle flooded (implied 3181 m2
  vs 846 m2 footprint)
- Lowest DEM cell was an isolated 4-cell depression; use the dominant connected minimum
  as a floor candidate only
- Repeating inlet-location sensitivity did not change the 4 failures; stop re-running
  without new geometry
- 'Recurrence note: 3 native HMS runs, 4 of 6 cases failed each time; 3 failed setup
  tasks'
jurisdiction: Pima County RFCD
tools_versions: HEC-HMS 4.13 (bundled Java/Jython), hms_project_diagnostic.py
evidence:
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydrology\KB-013.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydrology\KB-018.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydrology\KB-019.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydrology\KB-037.md
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\00_Admin\Local_Queue\hms-project-isolated-004.log
hours_lost: 5.0
recurrence: 3
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:17+00:00'
schema_version: 1
---
