---
id: STARVALLEY-001
title: Convert script-written FLO-2D inputs to CRLF before running
type: qc_rule
function: hydraulics-model-run
trigger: Any FLO-2D .DAT/.RGH input written or edited by a script (Linux, WSL, cloud
  container, Python with default newline) before a Windows FLO-2D or GDS run
steps:
- Write FLO-2D text inputs with explicit CRLF line endings and a trailing CRLF
- Before every run, scan all .DAT/.RGH files for bare LF and convert to CRLF; leave
  binary NEIGHBORS.DAT untouched
- Preserve the original line-ending style when patching an existing file (detect CRLF
  vs LF first, write via temp file and rename)
- Add the line-ending check to the package QC script so it fails the build
gotchas:
- LF-only CHAN/CHANBANK/CHAN.RGH/XSEC files gave error while creating channel segments
  and subscript out of range; content fixes (banks, dup cells, point counts) did not
  clear it until CRLF conversion
- The same LF problem was present in the Build 23 converted existing-conditions model
  (TOPO, MANNINGS_N, FPLAIN, CONT, RAIN, HYSTRUC, INFLOW)
jurisdiction: FEMA CLOMR (any FLO-2D model)
tools_versions: FLO-2D Pro Build 23.10.25 and 26.02.25, Python 3.12
evidence:
- D:\Star Valley CLOMR\SV-CLOMR-AD02-CONTINUATION.md
- D:\Star Valley CLOMR\Comment 3 - Channel Rebuild\CHANNEL-REBUILD-MEMO.txt
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\fix_hystruc_names.py
hours_lost: 4.0
recurrence: 2
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:07+00:00'
schema_version: 1
---
