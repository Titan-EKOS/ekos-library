---
id: NORTHLOOP-009
title: Existing vs proposed FLO-2D impact comparison (pad clearance, new wet areas,
  outlet split)
type: skill
function: hydraulics-model-run
trigger: Raised pad or new channel in a sheet-flow floodplain; need offsite impact
  and pad clearance from existing and proposed runs
steps:
- Use identical grid, boundary, control and inflow files; only grading and roughness
  differ (check hashes)
- Join cells by verified ID and XY; compare depth, WSE and velocity for cells wet
  above 0.1 ft; report new wet areas separately
- Pad clearance = max wet-cell WSE within 100 ft of the pad, with 30, 50, 100 and
  200 ft reference values; label it screening, not a certified floor elevation
- Build synchronized 0.5-hr outlet hydrographs and domain-exit group totals from the
  final OUTNQ.OUT
- Split changes beyond the parcel from changes near the boundary where CAD and GIS
  lines disagree
- Run the results script with all scenario folders in order so the register is complete
gotchas:
- Running the comparison with only two folders overwrote the three-case results register
- FLO-2D lowers outlet-cell elevations internally, so WSE minus ground there does
  not equal max depth; interior cells reconcile within 0.0002 ft
- Partial outlet review from an incomplete run window is not usable; wait for the
  final file
jurisdiction: any
tools_versions: FLO-2D Pro; Python 3 numpy
evidence:
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\scripts\analyze_results.py
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\scripts\outlet_distribution.py
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\CONTINUATION_NOTES.txt
hours_lost: 1.0
recurrence: 2
confidence: medium
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:28+00:00'
schema_version: 1
---
