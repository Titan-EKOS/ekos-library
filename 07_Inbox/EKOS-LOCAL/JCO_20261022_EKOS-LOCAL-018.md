---
id: EKOS-LOCAL-018
title: Native Excel recalculation of the drainage workbook after scripted edits
type: skill
function: report-assembly
trigger: Writing input cells into the standard drainage workbook with a non-Excel
  library
steps:
- Edit only explicit input cells on an isolated copy; keep the original admin workbook
  unchanged
- Recalculate in a private DispatchEx Excel instance (Visible False, events, macros
  and link updates off, CalculateFullRebuild), save, close only that instance
- Reopen and compare unchanged cells, formulas, names, merged ranges, validation,
  panes and visible styles semantically
- Require zero new formula errors and correct register counters
gotchas:
- Library-written file showed COUNTIF wildcard counter of -14 status issues; native
  recalc gave 0 without changing formulas
- Native Excel merges adjacent validation ranges and drops default styles; compare
  semantics, not raw XML
- 'Recurrence note: 2'
jurisdiction: General
tools_versions: Excel 16.0, pywin32, openpyxl
evidence:
- D:\LocalAI_Test\EKOS_Knowledge\topics\orchestration\KB-027.md
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\00_Admin\Local_Queue\workbook-native-recalc-002.log
hours_lost: 1.0
recurrence: 2
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:20+00:00'
schema_version: 1
---
