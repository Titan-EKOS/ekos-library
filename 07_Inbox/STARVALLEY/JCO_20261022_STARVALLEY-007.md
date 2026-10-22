---
id: STARVALLEY-007
title: One consistent model set for existing vs proposed comparison
type: qc_rule
function: hydraulics-model-run
trigger: Building duplicate-effective, existing and proposed FLO-2D models for a CLOMR
  and the 44 CFR 65.12 comparison
steps:
- Use the effective grid elevations as the base terrain in every model; replace only
  inside approved proposed grading surfaces
- Check effective grid vs new survey (mean and std dev) before deciding to resample
  terrain
- Carry the same 1D channel network, FPXSEC.DAT, INFLOW, OUTFLOW, TOLER, RAIN and
  engine build in every condition; only development and grading differ
- Run the existing-conditions model at the same vintage and include its outputs
- Hash-check the shared files across models in package QC
gotchas:
- 'June models: existing and Interim carried only an 18-cell eastern trapezoid while
  Ultimate carried a 567-cell western channel; offsite dWSE over 1 ft (157 cells)
  was an artifact of that mismatch'
- Interim and Ultimate used re-sampled terrain differing from the effective grid by
  up to 11 ft across the 3,060 ac domain; effective grid matched the 2025 survey to
  0.15 ft mean
jurisdiction: FEMA Region IX / Pima County RFCD
tools_versions: FLO-2D Pro Build 26.02.25
evidence:
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\06 Report\SV-CLOMR_TDN_Narrative_4th-Submittal_DRAFT.docx
- D:\Star Valley CLOMR\FEMA Case Closure Rview and Support\Star-Valley-CLOMR_Work-Completed-To-Date.md
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\build_models.log
hours_lost: 16.0
recurrence: 2
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:09+00:00'
schema_version: 1
---
