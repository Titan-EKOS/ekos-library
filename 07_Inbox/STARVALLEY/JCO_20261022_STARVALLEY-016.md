---
id: STARVALLEY-016
title: Preserve surveyed grade-control drops in channel inverts
type: qc_rule
function: hydraulics-model-run
trigger: Cutting channel cross sections from survey where the thalweg profile shows
  abrupt invert steps
steps:
- Treat abrupt invert drops in constructed channels as grade-control structures unless
  the EOR says otherwise
- Do not apply thalweg smoothing or conditioning to remove them
- List each drop with location and height for EOR review; decide if any needs an explicit
  structure rating
gotchas:
- 'EOR correction: steps up to 5.9 ft in the constructed channels are real rip-rap
  grade controls and must be kept in the section geometry'
jurisdiction: FEMA CLOMR (any FLO-2D model)
tools_versions: FLO-2D Pro Build 23.10.25
evidence:
- D:\Star Valley CLOMR\Comment 3 - Channel Rebuild\CHANNEL-REBUILD-MEMO.txt
- D:\Star Valley CLOMR\SV-CLOMR-AD02-CONTINUATION.md
hours_lost: 1.0
recurrence: 1
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:12+00:00'
schema_version: 1
---
