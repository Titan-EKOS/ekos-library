---
id: NORTHLOOP-004
title: FLO-2D inflow hydrograph chronology preflight (no repeated or backward times)
type: qc_rule
function: hydraulics-model-run
trigger: Before launching any FLO-2D run that reuses or scales an inherited INFLOW.DAT
steps:
- Parse every inflow node series; assert times are strictly increasing and match the
  source calc interval (here 0.5 hr, 0 to 50 hr)
- Integrate volume and peak per node and in total; compare with the source workbook
  before and after any scaling
- If a series fails, repair timestamps from the source calcs only, keep every discharge
  value, log each change to CSV
- Hash shared input files (CADPTS, CONT, TOLER, INFLOW, OUTFLOW) and require equal
  hashes across scenarios being compared
- Block launch unless preflight_pass is true
gotchas:
- 41 of 185 inherited hydrographs had repeated integer-hour times and a jump back
  from hr 9 to hr 1; two 8-hr native runs used them and were rejected after completion
- Volume error 0.0% in SUMMARY.OUT does not validate boundary chronology
- An input-volume comparison computed with the bad times (2.3% discrepancy) was invalid
  and had to be withdrawn
jurisdiction: any
tools_versions: FLO-2D Pro 17.08.17; Python 3
evidence:
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\hydrograph_repair_candidate\JCO_2026-09-30_Hydrograph_Repair_Review.txt
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\hydrograph_time_audit.json
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\model_preflight_checks.json
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\scripts\preflight_checks.py
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\rejected_nonmonotonic_inflow_attempts\README.txt
hours_lost: 6.0
recurrence: 2
confidence: high
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:27+00:00'
schema_version: 1
---
