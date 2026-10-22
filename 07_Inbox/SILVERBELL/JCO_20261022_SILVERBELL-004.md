---
id: SILVERBELL-004
title: Culvert concept geometry standards for crossings
type: qc_rule
function: qc
trigger: Any proposed culvert or bridge crossing concept for this corridor.
steps:
- Extend barrels slightly beyond actual roadway fill toes; use ADOT headwalls and
  wingwalls.
- Drop inlets at 6:1 or flatter; outlet grading with positive downstream flowline;
  outlet riprap where ROW allows.
- RCBC top slab 1.0 ft for cover checks.
- Bridge alternatives span the floodplain with low chord at least 2 ft above computed
  Q100.
- Carry one common geometry through CAD, 1D/2D RAS and renderings.
gotchas:
- Old DCR culverts stopped inside the fill; lengths increased once toes were checked.
- One barrel axis extracted at 844.6 ft from a bad source trace; corrected to 138.6
  ft from the sheet barrel edges. Flag any length far outside its neighbors.
- Short-span bridge trial failed in 1D because flow bypassed over adjacent lower ground;
  size from the full existing flood envelope.
jurisdiction: Pima County / ADOT standards
tools_versions: Civil 3D 2026, HEC-RAS
evidence:
- C:\Ekos\projects\silverbell\ACTIVE_SCOPE.md (Active revision 4)
- C:\Ekos\projects\silverbell\prepare_culvert_revision4.py
- C:\Ekos\projects\silverbell\v4\README_REVISION4_PROGRESS.md
- C:\Ekos\projects\silverbell\v4\CHECKPOINT_1348.md
hours_lost: 2.0
recurrence: 3
confidence: high
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:23+00:00'
schema_version: 1
---
