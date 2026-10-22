---
id: EKOS-LOCAL-016
title: Report narrative only from structured results; report presence is not calculation
  acceptance
type: qc_rule
function: report-assembly
trigger: Any local-model drafted report text, review package or phone notification
steps:
- Build tables from structured calculation outputs; model writes prose only around
  checked rows
- Run a numeric guard rejecting model-authored numbers; allow only bounded software
  tokens (HY-8)
- Label every section with its evidence path and status (working, unresolved, record)
- Keep failed and missing analyses visible as explicit gaps
- Regenerate the Word draft when calculation evidence changes; date-stamp drafts
- Verify DOCX hyperlinks by anchor count, resolving each r:id to an existing target
gotchas:
- Autonomous draft copied stale checkpoint statements and wrong rainfall-resolution
  wording (1-minute hydrograph is not 1-minute rainfall)
- Earlier Word draft predated later road-crossing results and was still linked as
  current
- Numeric guard rejected the software name HY8 until a bounded exception was added
- Hyperlink check failed because 6 anchors share 5 relationship targets
- 'Recurrence note: 4'
jurisdiction: General
tools_versions: python-docx, report_working_brief.py, verify_working_report.py
evidence:
- D:\LocalAI_Test\EKOS_Knowledge\topics\local-models\KB038.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\orchestration\KB039.md
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\50_Deliverables\Autonomous_Review\report.md
- D:\LocalAI_Test\EKOS_ORCHESTRATION_REVIEW.md
hours_lost: 2.0
recurrence: 4
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:20+00:00'
schema_version: 1
---
