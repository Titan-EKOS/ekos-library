---
id: STARVALLEY-002
title: FLO-2D natural-section 1D channel validity checks
type: qc_rule
function: hydraulics-model-run
trigger: Building or rebuilding a FLO-2D 1D channel (CHAN.DAT, CHANBANK.DAT, XSEC.DAT)
  from a centerline and terrain surfaces
steps:
- Bank cell must be a floodplain cell, never another channel cell; derive it as the
  first non-channel cell perpendicular to flow
- Each grid cell belongs to exactly one segment; drop stub reaches of 2 cells or less
- 'XSEC.DAT: 20-25 station points per section (hard limit near 33); thalweg interior
  with ground rising on both sides; relief at least 0.5 ft; no duplicate stations'
- Number natural cross sections consecutively with no gaps; one XSEC per channel element
  (1:1 references)
- Do not model onsite drainage channels as dead-end 1D reaches without their outlet
  culverts; they fill and spill
- Write a QC table of every section that needed synthetic banks or relief adjustment
  (xsec_adjustments_*.csv) and flag them for engineer review
- Plot plan, profile and section QC exhibits before the first run
gotchas:
- 'Channel rebuild took 8 fix iterations in one day (v1-v8): bank-is-channel cells,
  duplicate cells, stub reach, 61-point sections, LF line endings, thalweg at section
  endpoint and flat sections giving Error 11 division by zero'
- Non-consecutive cross-section numbering let a 30 hr run finish integration then
  fail writing output (Intel Fortran EOF at CHMAX2.TMP); only consecutive renumbering
  fixed it
- CHANBANK written before sections were re-cut produced a fatal mismatch; build banks
  after the final section cut
- 65 flat-terrain sections needed synthetic banks (thalweg + 1.5 ft); consider leaving
  flat tails as 2D instead
jurisdiction: FEMA CLOMR (any FLO-2D model)
tools_versions: FLO-2D Pro Build 23.10.25 and 26.02.25
evidence:
- D:\Star Valley CLOMR\Comment 3 - Channel Rebuild\CHANNEL-REBUILD-MEMO.txt
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\01 Models\_run_log.txt
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\xsec_adjustments_interim.csv
- D:\SV-BLIND-CLOMR\_WORK\00_Admin\JCO_20261011_Closeout_and_Resume.txt
- D:\SV-BLIND-CLOMR\_WORK\00_Admin\proposed_output_failure.json
hours_lost: 10.0
recurrence: 10
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:08+00:00'
schema_version: 1
---
