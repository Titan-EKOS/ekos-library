---
id: NORTHLOOP-003
title: Marana critical-facility and FLO-2D criteria to check before modeling
type: qc_rule
function: jurisdiction-rules
trigger: Substation, BESS or other vital utility in a Town of Marana floodplain
steps:
- 'Town Code 17-15-10 H.5: finished floor 1 ft above the 500-yr WSE; H also requires
  500-yr delineation and erosion protection; tabulate floor, pad and equipment elevations
  with datum and the controlling 100-yr and 500-yr WSE'
- Marana Drainage Manual (Sep 2024) 4.5 names FLO-2D Pro build 17.08.17 for the regional
  (TAFS) model; record the build in every SUMMARY.OUT used
- Use non-regional design discharges for design and onsite PC-Hydro; regional results
  serve FEMA purposes (MDM 4.1)
- 'Confirm with the Town early: facility classification, accepted 500-yr hydrology,
  engine build, collector channel criteria, outlet criteria'
gotchas:
- Prior report used equipment above the 500-yr level and 1 ft above the 100-yr level,
  which no longer meets the current code
- Archived model outputs showed builds 19.07.21 and 21.08.23, not the build named
  in the manual; treat as historical until accepted
- Runs were moved to build 26.02.25 to avoid a startup failure; this departs from
  MDM 4.5 and needs Town acceptance (see NORTHLOOP-008)
jurisdiction: Town of Marana
tools_versions: FLO-2D Pro 17.08.17 / 26.02.25; PC-Hydro 7.4
evidence:
- C:\Users\Titan\OneDrive\Northloop\Review_2026-09-30\Drainage_Review.txt (F02, F03,
  F04)
- C:\Users\Titan\OneDrive\Northloop\Review_2026-09-30\Standards\town-of-marana-drainage-manual-september-2024.pdf
hours_lost: 1.0
recurrence: 2
confidence: high
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:26+00:00'
schema_version: 1
---
