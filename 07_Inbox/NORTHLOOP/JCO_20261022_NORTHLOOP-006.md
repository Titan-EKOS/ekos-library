---
id: NORTHLOOP-006
title: Do not pick archived model terrain or alternative by folder name
type: qc_rule
function: hydraulics-model-run
trigger: Several archived model folders (existing/proposed, Alt1/Alt2, backups) exist
  for a prior study
steps:
- 'Register every native model folder: build, grid, run time, terrain changes vs base,
  levee/barrier records'
- Diff each alternative grid against the base to see actual grading, channels and
  barriers
- Match the folder to the report figures before adopting; do not select by newest
  timestamp alone
- Separate artificial levee barriers from real proposed grading so they do not carry
  into new runs
gotchas:
- Folder named Alt1 had an eastern channel and 2120-ft artificial barriers, while
  the report preferred alternative left the east natural
- Both named 500-yr folders were empty; the old 500-yr used a 1.75 x Q100 multiplier,
  not a saved run
jurisdiction: any
tools_versions: FLO-2D Pro; Python 3 numpy
evidence:
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\native_model_register.csv
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\old_alt1_changes.png
- C:\Users\Titan\OneDrive\Northloop\Review_2026-09-30\Drainage_Review.txt (F17)
hours_lost: 1.5
recurrence: 1
confidence: high
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:27+00:00'
schema_version: 1
---
