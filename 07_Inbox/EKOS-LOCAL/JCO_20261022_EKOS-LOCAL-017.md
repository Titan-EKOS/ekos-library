---
id: EKOS-LOCAL-017
title: Morning review package - evidence dashboard built through failures
type: skill
function: report-assembly
trigger: Producing a reviewable interim package (HTML index, maps, tables, workbook
  copy) after an unattended run
steps:
- Schedule the package with after_settled dependencies so it builds even when some
  evidence tasks fail
- Show candidate geography, sourced evidence, assumptions, failed and missing calculations
  with links to native files
- Browser-check every local link, image and table row headlessly; render a preview
  image for visual check
- Refresh only when meaningful evidence changes; batch refreshes
- State clearly that the package is not the drainage report
gotchas:
- Package was refreshed 24 times overnight, each followed by a cloud visual check,
  adding cloud cost
- Package existence was close to being reported as report completion
- 'Recurrence note: 24 package refreshes'
jurisdiction: General
tools_versions: morning_package.py, headless browser QA (morning_package_qa.cjs)
evidence:
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\50_Deliverables\Morning_Review\index.html
- D:\LocalAI_Test\EKOS_Runtime\morning_package.py
- D:\LocalAI_Test\EKOS_Knowledge\topics\orchestration\KB-015.md
hours_lost: 2.0
recurrence: 24
confidence: medium
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:20+00:00'
schema_version: 1
---
