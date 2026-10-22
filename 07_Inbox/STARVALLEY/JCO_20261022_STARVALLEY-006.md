---
id: STARVALLEY-006
title: AD letter response must be a complete re-run package within 90 days
type: qc_rule
function: jurisdiction-rules
trigger: FEMA additional-data (AD) letter received on a CLOMR/LOMR case
steps:
- Log the 90-day deadline (no extensions) and plan the last model run at least 10
  days before it
- Every response row states what changed, file name, folder and report page; status
  other than addressed does not ship
- Re-run every model after its last input edit, including existing conditions used
  for comparison
- Start community-dependent items (flooding-source names, O&M acceptance, signatures)
  on the day the letter arrives
- If an item needs a decision the agency has already rejected, settle it with a call
  before resubmitting
gotchas:
- Response was sent 37 days early but with unrun models and missing community letters;
  the case was closed for insufficient data and had to be resubmitted as a new case
jurisdiction: FEMA Region IX / Pima County RFCD
tools_versions: FEMA MT-2, Online LOMC
evidence:
- D:\Star Valley CLOMR\FEMA Case Closure Rview and Support\Star-Valley-CLOMR_Work-Completed-To-Date.md
- D:\Star Valley CLOMR\Star Valley CLOMR Timeline.xlsx
- D:\Star Valley CLOMR\SV-CLOMR-AD02-Comment-Tracking-Matrix.xlsx
hours_lost: 24.0
recurrence: 1
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:09+00:00'
schema_version: 1
---
