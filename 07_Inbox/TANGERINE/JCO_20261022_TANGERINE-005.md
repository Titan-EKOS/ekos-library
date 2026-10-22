---
id: TANGERINE-005
title: 2D alluvial-fan concept model inputs reviewers expect (Town of Marana / Pima
  County)
type: skill
function: hydraulics-model-run
trigger: Building or documenting a HEC-RAS 2D model of distributary sheet flow on
  an alluvial fan for a concept or master drainage report
steps:
- 'Use spatially varied Manning n from a land-cover layer: active sandy wash about
  0.030-0.040, dense overbank desert scrub or xeroriparian about 0.035-0.050, plus
  roads, pads and basins; a uniform 0.035 is accepted only for feasibility'
- Keep overbank cells at or below 100 ft where depths are 0.5-2 ft, or run a grid-independence
  check; cells of 150-270 ft were rejected as too coarse
- Run diffusion wave for broad fan flow, then list and test full momentum (SWE) at
  roadway crossings, pinch points, berms and high-velocity cells
- Document terrain source, breaklines, boundary hydrographs, timestep, Courant diagnostics,
  volume balance and instability locations in an appendix
- Add a 200-yr (or increased-rainfall) stress run and a node-to-node volume ledger
  from boundary inflows to downstream concentration points
- Report velocities in erodible soils with bank protection or erosion-hazard setbacks
  where corridor velocities approach 16-20 fps
gotchas:
- Every one of these items was raised by reviewers on the concept model and carried
  as deferred work (A-1, A-3, T1-4, T1-5, T1-7, T1-8); doing them in the first model
  build avoids a second model cycle
- Contracted scope assumed 1D HEC-RAS; the 2D approach needed a scope note in the
  report; flag scope mismatch to the PM early
jurisdiction: Town of Marana Drainage Manual 2024; Pima County RFCD; ADWR SS4-95 /
  SS5-96; FEMA alluvial fan guidance
tools_versions: HEC-RAS 6.6 / 7.0 2D unsteady
evidence:
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\Comments\Internal\Comments
  A.docx
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\Comments\Internal\Comments
  B.docx
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\ASLD_Tangerine_Comment_Response_Report.docx
hours_lost: 3.0
recurrence: 6
confidence: high
project: TANGERINE
source_ai: claude
timestamp: '2026-10-22T23:35:06+00:00'
schema_version: 1
---
