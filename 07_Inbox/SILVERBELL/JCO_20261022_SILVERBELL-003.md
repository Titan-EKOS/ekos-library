---
id: SILVERBELL-003
title: Restricted-frontage crossings stay inside existing ROW
type: qc_rule
function: qc
trigger: Culvert or roadway concept along a frontage where new ROW or downstream easement
  is not available.
steps:
- Ask which frontage is restricted before extending outlets, grading or easements
  on that side.
- Shift the road alignment away from the restricted side and use retaining walls in
  place of fill slopes.
- Fit a minimum section inside the stated usable envelope; check footprint overlap
  against current county parcel geometry (target zero sq ft).
- Allow an upstream drainage easement only; raise outlets to tie to EG inside ROW
  and dissipate inside the box.
gotchas:
- Agent extended downstream grading (378 ft to reach EG at C01) before the restriction
  was known; JCO direction reversed it.
- Restricted parcel data may be split; check the current record, not the plan label.
- Do not interpret a county restriction attribute field as a development restriction.
jurisdiction: Pima County
tools_versions: Civil 3D 2026, county parcel GIS
evidence:
- C:\Ekos\projects\silverbell\ACTIVE_SCOPE.md (LATEST USER DIRECTION, CONFIRMED RESTRICTED
  PARCEL)
- C:\Ekos\projects\silverbell\v4\README_REVISION4_PROGRESS.md
- C:\Ekos\projects\silverbell\build_restricted_geometry.py
- C:\Ekos\projects\silverbell\resolve_restricted_outlets.py
hours_lost: 3.0
recurrence: 3
confidence: high
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:22+00:00'
schema_version: 1
---
