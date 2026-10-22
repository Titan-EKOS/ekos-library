---
id: STARVALLEY-003
title: Verify size and hash after copying model files to OneDrive
type: qc_rule
function: hydraulics-model-run
trigger: Copying FLO-2D model folders (binary NEIGHBORS.DAT, FLOPRO.exe, DLLs, large
  TOPO/FPLAIN) to or from a OneDrive-synced folder or through a time-limited shell
steps:
- After every copy compare byte size and hash of each file against the source
- Check NEIGHBORS.DAT size equals the expected value for the grid before running
- Check FLOPRO.exe size and build string and the DLL count in every model folder
gotchas:
- A copy cut off by a 45 s shell timeout left Interim NEIGHBORS.DAT at 733 KB instead
  of 5.9 MB; FLO-2D reported a misleading MANNINGS_N mismatched grid element / TOLER.DAT
  error
jurisdiction: FEMA CLOMR (any FLO-2D model)
tools_versions: FLO-2D Pro Build 23.10.25
evidence:
- D:\Star Valley CLOMR\SV-CLOMR-AD02-CONTINUATION.md
- D:\Star Valley CLOMR\FEMA Case Closure Rview and Support\Star-Valley-CLOMR_Work-Completed-To-Date.md
hours_lost: 2.0
recurrence: 1
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:08+00:00'
schema_version: 1
---
