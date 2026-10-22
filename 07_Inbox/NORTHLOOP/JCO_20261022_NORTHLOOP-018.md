---
id: NORTHLOOP-018
title: Export CAD from scratch copies only
type: qc_rule
function: data-gathering
trigger: Extracting geometry from source DWG files with AutoCAD console or scripts
steps:
- Copy the DWG to a scratch folder and run the export there
- Hash source files before and after; stop if any source changes
gotchas:
- AutoCAD console refreshed a historical DWG and its BAK; the DWG was restored from
  backup but the older BAK was lost
jurisdiction: any
tools_versions: AutoCAD / Civil 3D accoreconsole
evidence:
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\source_recovery\recovery_record.json
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\scripts\restore_cad_source.py
hours_lost: 1.0
recurrence: 1
confidence: high
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:31+00:00'
schema_version: 1
---
