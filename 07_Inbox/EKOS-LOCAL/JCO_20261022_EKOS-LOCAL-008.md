---
id: EKOS-LOCAL-008
title: Nested catchments - count the total area once
type: qc_rule
function: hydrology
trigger: Terrain-derived catchments where one outlet area contains upstream basins
  or pipe catchments
steps:
- List each catchment with its parent; record that the road-crossing area includes
  the upstream basin areas
- Run a total-area unattenuated scenario once; never add upstream basin outflows or
  pipe catchment flows to it
- Where detention is modeled, route upstream outflow and add only the incremental
  area downstream
- Load soils by the same catchment key as geometry; stop on mismatched keys
gotchas:
- Candidate areas 40.0, 27.8, 27.0 and 12.9 ac were nested; summing would roughly
  triple the flow
- Local draft narrative started summing basin and road flows until guarded
- 'Recurrence note: 3 scenario sets'
jurisdiction: Pima County RFCD
tools_versions: PC-Hydro 7.4, Whitebox flowpaths, GeoPandas 1.1
evidence:
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydrology\KB042.md
- D:\LocalAI_Test\EKOS_Runtime\EXECUTION_CHECKPOINT.md
hours_lost: 1.0
recurrence: 3
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:17+00:00'
schema_version: 1
---
