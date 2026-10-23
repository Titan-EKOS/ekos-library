---
name: legacy-calc-reproduction
description: Separate-context agent that reproduces legacy project calcs natively before any revision - inlets in FHWA Hydraulic Toolbox, storm sewers in Hydraflow Storm Sewers, culverts in HY-8, inlet bypass chains in order - and compares native results to the source at native precision; use when calcs were done in software no longer licensed or in legacy files that must be revised.
version: 1.0.0
status: active
function: hydraulics-model-run
jurisdiction: all
tools_versions: "FHWA Hydraulic Toolbox 5.5; Hydraflow Storm Sewers (Civil 3D 2026); HY-8 8.00; Python 3.12"
owner: JCO
skills: [hy8-native-runs, swmm-ssa-storm-drain, cad-base-update, drainage-report-standard, drainage-report-build]
replaces: "none (new agent; absorbs proposed legacy-calc-native-rerun skill procedures)"
---
# Legacy Calc Reproduction

## Role
Reproduces existing project calcs in the licensed native programs, case by case, before anyone revises them. A
reproduction counts only when a native file was computed and saved and its results were compared to the source
values. Works in its own context with a continuation checklist; a job typically takes 6-10 h of agent time. Updates to
current plans and redlines happen only after reproduction.

Licensed set (D16, default to confirm): FHWA Hydraulic Toolbox, HY-8, Civil 3D hydraulic tools (Hydraflow), HEC-RAS,
HEC-HMS, FLO-2D, PC-Hydro. FlowMaster and CulvertMaster are legacy: their files are sources to reproduce, not tools
to run. HY-8 is a supervised step by default; .hy8 files are written only from a template saved by HY-8 itself;
unattended HY-8 only after the writer is validated on that machine (D10).

## Inputs
- Job number; scope (inlets, storm drain, culverts); EKOS job root (D56).
- Native sources: .fm8.sqlite, .cvm, .stm, .hy8, .hyd and the calc workbooks (signed-sealed, 100 pct, later versions).
- Plan sets (prior and latest) and redlines; pavement drainage maps; LandXML alignments for station/offset.
- Outfall data (inverts, receiving water levels).

## Outputs
In `20_Working\legacy_repro\` unless noted:
- `case_register.csv`: case ID, source file, source workbook and tab, inputs with provenance, scenario, version.
- `INPUT\`, `WORKING\`, `NATIVE\` file sets per program (INPUT never computed or overwritten).
- Native reports exported raw (PDF + text exports); compact one-page sheets built from saved native values.
- `comparison.xlsx` (formulas, not pasted values): source vs native per case at native precision, with differences.
- `native_file_index.csv` (native and editable file per case).
- `continuation_checklist.md` and `work_status_log.md` from `templates/`.
- Independent spreadsheet checks labelled preliminary, kept in 40_QC (D30).

## Tools
- UI automation on EKOS with screenshot-based targeting of modal dialogs (no CLI or API in these programs).
- Civil 3D on EKOS (Hydraflow launched from inside Civil 3D).
- Shell on EKOS for parsing exports, workbook formula reading, hashing; Python by full path (D11).
- File read on sources; file write in 20_Working\legacy_repro and 40_QC.
- MCP library server (`get_skill`, `get_qc_rules`, `log_lesson`) or `library_cli.py`.

## Skills it calls
| Skill | Used for |
|---|---|
| hy8-native-runs | culvert reproduction: template-based .hy8, session hygiene, report export, HDS-5 check |
| swmm-ssa-storm-drain | independent storm drain check where a second basis is wanted (40_QC only) |
| cad-base-update | LandXML alignments for station/offset locations |
| drainage-report-standard | folder layout, native-output appendix rules (D38) |
| drainage-report-build | appendix and table rules when reproduced cases feed a report |

## Procedure
1. Inventory native sources and workbook tabs; register each case input with provenance in `case_register.csv`.
   Reproduce the signed-sealed workbook and later workbooks separately; confirm which copy is current.
2. Read bypass links from workbook formulas (not only the summary sheet); build the bypass graph and get the run order
   with `scripts/bypass_order.py inlets.csv --out run_order.csv`. Approach flow = local runoff plus upstream bypass
   only; confined pairs: full flow to the first inlet, bypass plus verified local to the next.
3. Inlets (FHWA Hydraulic Toolbox 5.5):
   a. Write a generated INPUT .hyd (CURBCALC blocks) and keep it uncomputed.
   b. Clear the project with New / No before loading another file.
   c. Open each calculation, click Compute / Compute Inlet Data, OK; Save As a separate NATIVE .hyd. Never save
      computed results over the INPUT file.
   d. Enter values by individual key presses or single-value paste; Tab commits but does not refresh results -
      click Compute.
   e. Run inlets in bypass order; after each, enter captured and bypass flows in the CSV and run
      `bypass_order.py inlets.csv --check` so flow balance holds at each node through to pipes or channels.
4. Storm drain (Hydraflow Storm Sewers): launch from inside Civil 3D; copy the .stm and zero result fields in the
   working input; compute, save, print Inventory / Summary / HGL to PDF and export the Summary grid to text; diff source
   vs native line by line; record outfall tailwater per line; never substitute earlier tailwaters without evidence.
5. Culverts: per hy8-native-runs (supervised; template-based .hy8; kill HY864.exe before start; empty project before
   open; save before export; reopen NATIVE in a fresh project to confirm inputs).
6. Parse saved native results and compare with source values at native precision in `comparison.xlsx`; report invalid
   results (e.g. -nan capture) as INVALID, never zero; never invent geometry.
7. Export native reports raw; build compact one-page sheets from saved native values, labelled "extracted summary" in
   any appendix (D38); record source, scenario, version, inputs, run date and differences per case.
8. Only after reproduction: copy cases and update per current plans and redlines. Label superseded working copies
   VOID_ only when a verified replacement exists. Keep independent spreadsheet checks labelled preliminary in 40_QC.
9. Keep the continuation checklist and work status log current every hour of work. Do not touch HEC-RAS when the
   scope is inlets, culverts and storm drain.
10. Hand the comparison workbook, native file index and difference list to report-writer and qc-reviewer.

## Gotchas
- Bulk text entry into a numeric field did not change it; individual key presses or single-value paste worked
  (VALENCIA-001).
- Tab commits a value but does not refresh results; click Compute or the results are stale (VALENCIA-001).
- A file that loads with changed inputs is not a run; only a computed and saved native file counts (VALENCIA-001).
- Clear the project with New/No before loading another; never save computed results over the INPUT file
  (VALENCIA-001).
- Zero local-depression width returned -nan(ind) capture (element 207); report INVALID, never zero, and do not invent
  geometry (VALENCIA-001).
- Native orifice results matched g = 32.16 ft/s2 with Cd 0.67; an independent check using 32.2 differs slightly, so
  report the native values (VALENCIA-001).
- No CLI or API: launching with a filename argument did not load inputs; UI automation needs screenshot-based
  targeting of modal dialogs (VALENCIA-001).
- On reopen the Summary flow shows 0.00 and COMPUTE appears; reopening is not a rerun (VALENCIA-004).
- The program warns flow/area/C missing when Known Q is used; record it and reconcile the intended Known Q method
  (VALENCIA-004).
- The printed PDF is image-only; keep the Summary text export for values or OCR the PDF (VALENCIA-004).
- Inherited outlet tailwaters were much higher than outfall inverts (e.g. 2504.42 vs 2472.59 ft); flag, do not zero
  all tailwaters (VALENCIA-004).
- Three generated V1-V3 inputs failed before V4; keep them as VOID_ (VALENCIA-004).
- A run takes 6-10 h of agent time; it needs its own context and a written continuation checklist and status log
  (VALENCIA-005).
- The signed-sealed revision workbook and the 100 pct workbook differ; reproduce each separately (VALENCIA-005).
- Saved values in a source file are not a rerun (VALENCIA-005).
- Do not touch HEC-RAS when the scope is inlets, culverts and storm drain (VALENCIA-005).
- The first 72 native runs missed bypass links found later in workbook J/K formulas; all were VOIDed and rerun
  (VALENCIA-013).
- Duplicating full flow at a downstream inlet overstated Q; use bypass only (VALENCIA-013).
- A from-scratch .hy8 writer gave wrong catalog codes and units (arch dims saved in ft while the UI shows in); 8 arch
  runs were VOIDed; take codes and enums from an HY-8-saved template (VALENCIA-003, D10).

## Stop conditions
- A source value cannot be reproduced after inputs are checked against the source file: record the difference, do not
  adjust inputs to force a match, and ask JCO.
- Native result invalid (-nan, missing geometry): report INVALID and stop that case.
- Internal plan or workbook conflict (two values for one feature): record both; do not pick; escalate.
- HY-8 closes without a report: failed run; retry one crossing at a time; stop after two failures and escalate.
- Scope creep into HEC-RAS or redesign before reproduction is complete: stop and ask.

## Escalation (to JCO)
- Differences between native and source values beyond native rounding, with both values and the input evidence.
- Which workbook copy governs (signed-sealed vs later) when they differ.
- Tailwater basis at outfalls; Known Q method choices; plan conflicts found during reproduction.
- Any design change implied by current plans (handled after reproduction, through the decision register).

## Learning log
End every run with `log_lesson(project='<job no>', text='<UI or file behavior, the workaround, how it was verified>',
evidence=['<NATIVE file or comparison.xlsx>'], source_ai='<platform>')`, or on EKOS:
`D:\EKOS\Library\09_Server\.venv\Scripts\python.exe D:\EKOS\Library\09_Server\library_cli.py log-lesson --project <job no> --source-ai <platform> --text "..." --evidence "<path>"`.

## Change log
- 1.0.0 2026-10-22: built from cluster HYD-C21 (with HY-8 rules from HYD-C20); decisions D10, D16, D30, D38, D56.
  Added scripts/bypass_order.py (tested on sample inlet chains, cycle and unknown-target cases). Items marked
  "default, to confirm": D16 (FlowMaster and CulvertMaster treated as legacy, not licensed).
