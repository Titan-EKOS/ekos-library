---
id: EKOS-LOCAL-006
title: PC-Hydro 7.4 browser automation - import, native validation and rainfall check
type: skill
function: hydrology
trigger: Driving the PC-Hydro web application unattended to build pk6 inputs and export
  hydrographs
steps:
- Terms approval is standing for PC-Hydro; record it, do not ask again
- Open File then Open .pk5/.pk6 before setting the file input; wait until the concentration-point
  field populates before reading inputs
- Read back every native input field and compare with the scenario values before Calculate;
  stop on any mismatch
- Quantize flow-length segments to whole ft so the segments sum exactly to the native
  total length; log each precision change
- Allocate soil percentages to whole numbers by largest remainder so they total 100;
  log source vs native share
- Enter coordinates at 4 decimals; use the native Fetch Rainfall and compare to saved
  NOAA Atlas 14 arrays at 2-decimal rounding (matched upper 90 percent confidence
  rows)
- Export the 1-minute hydrograph CSV, keep native files and hashes, run export checks
  before routing
gotchas:
- File-chooser events timed out on the first adapter; proper File-Open dialog initialization
  fixed it
- Import of 52.263/41.418/6.318 percent soils rounded to 52/41/6 (total 99) and failed
  validation; largest remainder 52/42/6 passed
- Full-precision GIS lengths failed the native length-sum check
- Never set fake valid flags or force Calculate enabled
- Direct HTTP rainfall request returned 403; use the native in-app fetch
- The guide cites an older Atlas edition than the data now served; record the edition
  actually fetched
- 'Recurrence note: 9 failed PC-Hydro tasks (NOAA mapping x3, Basin B import x4, road
  scenario x1, benchmark)'
jurisdiction: Pima County RFCD
tools_versions: PC-Hydro 7.4 (web), Edge isolated browser, pchydro_adapter.cjs
evidence:
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydrology\KB-008.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydrology\KB-016.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydrology\KB-017.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydrology\KB043.md
- D:\LocalAI_Test\EKOS_Runtime\pchydro_adapter.cjs
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\00_Admin\Local_Queue\pc-basin-b-sensitivity-001.log
hours_lost: 4.0
recurrence: 9
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:12+00:00'
schema_version: 1
---
