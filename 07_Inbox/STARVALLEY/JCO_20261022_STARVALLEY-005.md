---
id: STARVALLEY-005
title: Independent submittal auditor agent (package vs comments vs letter)
type: agent
function: qc
trigger: Before every FEMA resubmittal, and after any FEMA closure or additional-data
  letter, run a separate-context audit of the archived upload package
steps:
- Work only from the archived upload package (zips as uploaded), not the working folders
- List zip members with timestamps; flag outputs older than inputs, missing outputs,
  TMP files, header/build mismatches
- 'For each agency comment classify: addressed with file evidence, done-but-not-run,
  not done, stale (agency text repeated from a prior letter that the files disprove),
  or new'
- Compare every response-letter claim to the model outputs and GIS actually in the
  package; flag any claim not backed by a file + page
- Separate defensible items (for fee or reopen requests) from legitimate findings
- Write decisions needed from the EOR and build rules for the next package
gotchas:
- Working letter carried 10 TO BE CONFIRMED placeholders while the uploaded PDF stated
  those items complete; the reviewer cited discrepancies between letter and model
- About a third of the closure text was stale AD02 wording; an audit with file evidence
  lets the cover letter point this out without arguing
- The audit should be done by an agent that did not build the package, so it does
  not trust the builder notes
jurisdiction: FEMA Region IX / Pima County RFCD
tools_versions: Python 3.12 (zipfile, python-docx), FLO-2D output readers
evidence:
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\00 Audit of 3rd Submittal\AUDIT
  - 3rd Submittal vs FEMA Closure (2026-09-20).md
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\07 Response Matrix and
  Cover Letter\Comment_Response_Plan_and_Closure_Assessment (DRAFT 2026-09-27).docx
hours_lost: 40.0
recurrence: 1
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:09+00:00'
schema_version: 1
---
