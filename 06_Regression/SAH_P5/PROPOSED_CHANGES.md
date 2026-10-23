# Phase 5 - proposed library changes (pending JCO approval)

Found while running the library tools on the SAH regression. Nothing here is applied to the masters yet; the
regression uses patched copies in `D:\EKOS\Regression\JCO_20261022_SAH_P5\...\tools\` where a fix was needed to proceed.

| ID | Skill / script | Problem found | Proposed fix | Evidence |
|---|---|---|---|---|
| P5-01 | hecras-2d-models `ras_headless.py` | Ras.exe 6.6 needs project and plan paths in double quotes; the script passed an argument list, so unquoted paths opened the command-line help box and the run sat until the 12 h timeout. | Pass one quoted command string; kill Ras.exe at once if the help box appears; dialog logger on win32 backend (VB6 text boxes not read by uia); result check uses GIS_PY (needs h5py). | 40_QC\proposed\P5-01_ras_headless_quoted_paths.patch; trial p01 ran after the fix. |
| P5-02 | hechms-headless `make_hms_run_script.py` (and `check_hms_results.py`) | Runs file read as plain utf-8; a BOM from Windows PowerShell attaches to the first run name, so HMS would not find that run; print also crashed under cp1252. | Read with utf-8-sig; strip names; set stdout utf-8. | logs, 2026-10-22 18:27 |
| P5-03 | hechms-headless `check_hms_results.py` | Unit hydrograph volume parser takes the number in the subbasin name ("S24" -> 24) instead of the 1.0000 value; flagged 66 of 66 subbasins falsely. | Parse `is ([0-9.]+) in` after the quoted name. | 40_QC\hms_check_check.json vs Run_*.log NOTE 42413 lines |
| P5-04 | hechms-headless `check_hms_results.py` | Stale test fails every run because HMS re-saves .basin/.hms/.met at project close (content unchanged) in the same second as the results. | Compare content hash taken before compute, or ignore files HMS rewrites at close when content is unchanged; allow 5 s. | Existing.basin byte-identical to source (fc), same timestamp as results |
| P5-05 | hechms-headless `check_hms_results.py` | Reads the results XML only; reservoir outlet sub-elements (RES_xx-OUTLET-1, culvert flows) are DSS-only and are not checked. | Read outlet flows from DSS for reservoirs. | 500 of 2450 original peak rows not covered |
| P5-06 | flo2d-model-runs `flo2d_channel_check.py` | Writes channel_check.json into the model folder it checks (a read-only check wrote into 20 original run folders; removed). | Write to --out only; default to stdout. | detection pass 2026-10-22 18:34 |
| P5-07 | model-run-supervisor `run_checks.py` / flo2d harness | Volume conservation not parsed from FLO-2D Pro 26.02.25 SUMMARY.OUT (table format), so every completion check says "read it by hand". | Parse the VOLUME CONSERVATION table (inflow, rain, outflow, storage) and compute pct. | 40_QC\detect_flo2d\*_complete.json |
| P5-08 | flo2d-model-runs SKILL.md | Nested-pair steps reference an inflow fix and pair script that are not in the library (they live in the SAH job folder). | Import s41_nested_inflow_fix.py and a parameterized pair driver into the skill scripts. | SAH_flo2d_driver.py, tools\s41_nested_inflow_fix.py |
| P5-09 | hecras-2d-models / QC rules | D09 0.1 pct volume error limit: 6 of 10 original SAH plans exceeded it (0.12-0.39 pct) and the original queue only checked the finish message. | No rule change; ras_result_check in every queue (already in skill); record the 1SEC trial outcome here when done. | 40_QC\orig_check_p01..p10.json |
| P5-10 | drainage-technical-memo / exhibit standards (held-out gaps) | Held-out library missed the engineering-scale scale bar, Psomas border and pending-FIRM items that only SAHPARK cards teach. | None needed (full library covers them); keep as evidence those rules generalize only once learned. | RESULTS.md section 1 |
| P5-11 | v1 account skills | Previous drainage-report-build still names HEC-HMS 4.12. | Replaced by v2 proposals (Phase 4). | RESULTS.md section 1b |

## Model findings (project, not library)
| ID | Finding | Status |
|---|---|---|
| M-01 | I-19 culverts NBI-06343 / 05788 / 06342 are in series on one crossing but were modeled as three parallel structures on the same nodes in every original FLO-2D UPPER run (HYSTRUC error never dispositioned). | Rebuilt as a series chain in the regression (JCO decision). |
| M-02 | 167 levee-crest-below-grid warnings in each UPPER run. | Logged; to review. |
