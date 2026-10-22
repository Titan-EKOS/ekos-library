---
id: STARVALLEY-004
title: FEMA FLO-2D package QC script before upload
type: skill
function: compile-pdf
trigger: Before any CLOMR/LOMR model package is zipped and uploaded to FEMA, and before
  any response letter states an item is complete
steps:
- 'For each model folder: FLOPRO.exe build string = CONT.DAT line 1 build = SUMMARY.OUT
  build; all DLLs present'
- All required input and output files present (CHAN/CHANBANK/XSEC when ICHANNEL=1;
  CHANMAX, CROSSMAX, HYDROSTRUCT, MAXWSELEV, DEPTH, ERROR.CHK)
- Zero *.TMP files; oldest output file newer than newest input file; SUMMARY.OUT shows
  completed run and volume conservation rating
- 'Cross-model hash check: CADPTS, INFLOW, OUTFLOW, FPXSEC, TOLER, RAIN identical
  across duplicate effective, existing and proposed'
- HYSTRUC rating tables equal the HY-8 export (names, discharge pairs, headwater reference
  offset)
- Flood zone and BFE contour shapefiles present for every condition
- Scan report, matrix and letter docx/xlsx for placeholders ([DATE], [TO BE CONFIRMED],
  bracketed notes) and fail the package if any remain
- Write package_QC_report.txt and include it as a report appendix
gotchas:
- The June package shipped Ultimate outputs older than 16 edited inputs, a CONT.DAT
  header of Build 16.06.16 against a 23.10.25 SUMMARY.OUT, existing-condition folders
  with zero outputs, 8 TMP files in Interim and no zone shapefiles; FEMA closed the
  case and a new case and fee were required
- FEMA runs the exe / CONT.DAT / SUMMARY.OUT build comparison itself; a stale header
  string alone draws a comment
jurisdiction: FEMA Region IX / Pima County RFCD
tools_versions: FLO-2D Pro Build 26.02.25, Python 3.12, python-docx, openpyxl
evidence:
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\package_qc.py
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\package_QC_report.txt
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\00 Audit of 3rd Submittal\AUDIT
  - 3rd Submittal vs FEMA Closure (2026-09-20).md
hours_lost: 40.0
recurrence: 1
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:08+00:00'
schema_version: 1
---
