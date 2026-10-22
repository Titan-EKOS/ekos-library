---
id: STARVALLEY-017
title: Concept-level phases in a CLOMR - decide early, package both variants
type: qc_rule
function: jurisdiction-rules
trigger: A CLOMR includes a phase with only concept-level grading (no grading and
  drainage plan of the same standard as the approved phases)
steps:
- Expect FEMA to require removal of the phase or design-level grading and drainage
  plans
- If the agency has rejected the concept argument once, call the reviewer before resubmitting
- Make the build and post-processing scripts switchable (environment variable) so
  a with-phase and without-phase package can both be produced from the same sources
- Produce a conceptual grading and drainage exhibit (contours, flow arrows, spot elevations)
  if the phase is kept
gotchas:
- FEMA rejected the concept mass-grading narrative in AD01, AD02 and the closure;
  two packages (with and without the phase) were built for the new case
jurisdiction: FEMA Region IX / Pima County RFCD
tools_versions: FLO-2D Pro Build 26.02.25, QGIS 3.44.12
evidence:
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\00 Audit of 3rd Submittal\AUDIT
  - 3rd Submittal vs FEMA Closure (2026-09-20).md
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\svlib.py
- D:\Star Valley CLOMR\_zip_log.txt
hours_lost: 8.0
recurrence: 3
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:13+00:00'
schema_version: 1
---
