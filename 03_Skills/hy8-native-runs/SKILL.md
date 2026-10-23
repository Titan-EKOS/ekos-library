---
name: hy8-native-runs
description: Produce native HY-8 8.00 culvert output (headwater, control, outlet velocity, overtopping) for reports, legacy CulvertMaster/HY-8 reproductions, contractor substitution checks and FLO-2D rating tables - .hy8 written only from an HY-8-saved template, supervised GUI session with clean-project hygiene, report export, and an independent HDS-5 check kept in 40_QC.
version: 1.0.0
status: active
function: hydraulics-model-run
jurisdiction: all (add-ons - Caltrans / California, City of Tucson)
tools_versions: "HY-8 8.00.2; Word (report export); Python 3.12 gis env (pywinauto for supervised automation only)"
owner: JCO
replaces: "drainage-report-build v1 section 3 HY-8 line (UI automation as the default path)"
---
# HY-8 Native Runs

## When to use
- A report, memo or appendix needs HY-8 native culvert output.
- Reproducing a CulvertMaster (legacy, decision D16) or archived HY-8 case natively.
- Contractor substitution check (e.g. boxes to arches) against the approved report headwater.
- User-defined arch or irregular shapes.
- HY-8 rating tables for FLO-2D structures (flo2d-model-runs Step 4) or HEC-RAS crossing checks.

Licensed set (decision D16, default, to confirm): HY-8 and the FHWA Hydraulic Toolbox are the culvert tools;
CulvertMaster and FlowMaster are legacy and used only to read archived files.

## Inputs
- Plan profile stations / elevations or survey for barrel count, size, length, inverts (not callout text).
- Design discharges (and the sensitivity flows the jurisdiction requires), tailwater basis, roadway profile.
- The approved analysis for the crossing, if one exists, and the current plan shape.
- Seed / template .hy8 saved by HY-8 itself for each culvert type and material in use (library resource or
  a project seed; never a file written from scratch).

Scripts (gis env by full path; `<PY>` = `D:\EKOS\envs\gis\.venv\Scripts\python.exe` or the path in the
library environment table):
- `scripts/hy8_template.py` - `fill` (values into a template by exact key), `check` (CRLF, ENDPROJECTFILE,
  keys, inch/ft warning), `diff` (INPUT vs NATIVE).
- `scripts/hds5_check.py` - independent HDS-5 inlet / outlet control check (internal QC only).

Run mode (decision D10): HY-8 is a supervised step by default - a person (or the supervisor with a visible
desktop) watches the GUI session. Unattended runs only after the template writer and the export sequence are
validated on that machine and the validation is logged.

## Steps

### 1. Confirm the crossing data
1. Take barrel count, size, length and inverts from plan profile stations / elevations or survey. Confirm the
   approved analysis matches the current plan shape (e.g. boxes vs arches). On any conflict ask JCO.
2. If no baseline exists, rebuild one with stated assumptions.
3. Read request wording carefully (e.g. "drainage area reduction" may mean opening area per cell).
4. HY-8 cannot model a skewed box inlet (e.g. 25 deg); note the limitation in the report.

### 2. Independent check first (internal)
1. `<PY> hds5_check.py --shape box --span 10 --rise 4 --barrels 3 --length 120 --slope 0.010 --n 0.012
   --ke 0.5 --inlet box_90_15_wingwall --tw 3.2 --q 250 450`. Save the JSON in 40_QC (decision D30); never
   put it in a deliverable.
2. This check is the reconciliation target for Step 6.

### 3. Write the INPUT .hy8 from a template
1. Start from a template saved by HY-8 itself. Take catalog codes (e.g. IRREGSIZE) and material enums from the
   native example; never infer them (e.g. from a RAS HDF).
2. Barrel data and geometry are serialized in ft even when the UI shows inches.
3. Match exact field keys with whitespace boundaries (INLETEDGETYPE is not INLETEDGETYPE71).
4. `<PY> hy8_template.py fill <seed.hy8> <values.json> INPUT_<crossing>.hy8`, then
   `<PY> hy8_template.py check <seed.hy8> INPUT_<crossing>.hy8` (CRLF, ENDPROJECTFILE, no invented keys,
   inch/ft warning). For repeats, edit a seed crossing rather than building from nothing.
5. User-defined arches: solve springline and tangent point from crown / haunch radius, span and rise;
   integrate the exact area; about 19 coordinate pairs within 0.3 pct of the area; save the coordinates JSON
   beside the model; note that inlet relationships for user shapes are generic (no manufacturer inlet data).
6. Keep the writer as an importable library module; never exec source text borrowed from another project.

### 4. Supervised HY-8 session
1. Kill any HY864.exe before each start.
2. File New (Ctrl+N, answer No) to an empty project before Open. Opening into a non-empty project appends the
   crossings to the current tree.
3. Open INPUT; confirm only the intended crossings are loaded. Never save a contaminated session.
4. Check every tab: tailwater type, roadway crest, inlet edge, n, material, barrel dimensions as displayed.
5. Run Analysis. Save the project as NATIVE_<crossing>.hy8 BEFORE exporting (HY-8 can close during export).
6. Create Report (Shift+End selects all crossings) to Word, then PDF. If export closes HY-8 without a DOCX,
   the run failed: retry one crossing at a time.
7. Reopen NATIVE in a fresh project and confirm inputs; `<PY> hy8_template.py diff INPUT_<x>.hy8 NATIVE_<x>.hy8`
   to see what HY-8 changed.
8. Keep INPUT, WORKING and NATIVE files. Word locks an open export DOCX; if a rename fails, write a VOID
   sidecar note instead.
9. Supervised automation notes: refresh the screenshot before every action (focus and cached modal indexes go
   stale); run button invokes on threads because dialogs block; on the welcome screen Return opens the
   chooser, Alt+N moves to the file name, verify the caret before typing.

### 5. Read the native report
1. Parse the exported report: total = barrel flow + roadway flow.
2. Record the solver mode actually used (e.g. Full Flow); do not call it a matched RAS profile comparison
   unless the mode matches.
3. Check cover for each alternative against the road profile.
4. For archived cases, compare printed inputs with the saved model before calling a mismatch.

### 6. Reconcile
1. Stop and reconcile if native and independent results differ by more than 0.2 ft HW or 0.5 fps.
2. Compare with archived output field by field and keep the differences; never adjust inputs to force a match.

### 7. Substitution checks (contractor alternatives)
1. Identical flow, slope, n, length and fixed tailwater from the report model.
2. Bracket the entrance loss (Ke 0.2 beveled, 0.5 square edge).
3. Stress cases: high tailwater, and full crossing flow through one structure where the original flow split
   between openings.
4. Compare HW with the report existing HW; report differences in computed area loss (e.g. recomputed vs
   contractor value).
5. One-page memo with native output attached (drainage-technical-memo).

### 8. Barrel-only checks
1. An artificial high road crest suppresses overtopping and does not prove zero overflow; state it.

### 9. Deliverable
1. Native report PDF of the selected design goes in the appendix (decision D38); option tables only while
   options are open, each with its calc sheet.
2. Project datum inverts, not an arbitrary datum; print areas so each sheet is one page.

## Jurisdiction add-ons
Load with `get_skill("hy8-native-runs", resource="addons/<file>.md")`:
- `addons/caltrans-california.md` - HDM Table 808.1 alternatives and sensitivity flow list.
- `addons/city-of-tucson.md` - contractor substitution memo against the approved report HW.

## Gotchas
- Opening a file into a non-empty HY-8 project appends its crossings to the current tree (e.g. into a prior benchmark session), producing a combined model; never save a contaminated session (CAMPBELL-013, EKOS-LOCAL-012, VALENCIA-003)
- HY-8 closing during report export without producing a DOCX is a failed run; retry one crossing at a time (CAMPBELL-013, EKOS-LOCAL-012)
- The .hy8 writer was borrowed from another project by exec of split source text with a hard path; keep it as an importable library module (CALFIRE-012)
- HY-8 has no command-line report; GUI automation took 9 probe scripts and about 25 min; kill HY864.exe before each start and invoke run buttons on threads because dialogs block (CALFIRE-012)
- Barrel dimensions are stored in ft even if the UI shows in (CAMPBELL-013)
- HY-8 cannot model 25 deg skew on a box inlet; note it (CAMPBELL-013)
- An agent team left HY-8 pending; native runs happened 11 days later; schedule HY-8 as an explicit supervised step (CAMPBELL-013)
- Accessibility focus and cached modal element indexes went stale; refresh the screenshot before every action (EKOS-LOCAL-012)
- Native summary showed Full Flow mode despite the profile toolbar; do not call it a matched RAS profile comparison (EKOS-LOCAL-012)
- An unattended local HY-8 run was never achieved; only supervised GUI runs worked (EKOS-LOCAL-012)
- Recurrence: 2 modal failures and 2 key-matching failures (INLETEDGETYPE vs INLETEDGETYPE71) in one job (EKOS-LOCAL-012)
- Arch dimensions show in inches in the UI but BARRELDATA / BARRELGEOMETRY are saved in feet; the first 8 concrete-arch runs were wrong and voided (VALENCIA-003)
- A corrugated steel arch 50x31 in needed IRREGSIZE 1 1 1, not the code derived from the HDF; the report run closed HY-8 with no output until fixed (VALENCIA-003)
- Material enum was set wrong in a generated file (4 instead of concrete 1); corrected in the UI before the run (VALENCIA-003)
- The HY-8 window disappeared during Word export before the post-analysis save; save the project before exporting (VALENCIA-003)
- An archive printed 4.0 ft rise while the saved model had 3.5 ft; check printed inputs vs the saved model before calling a mismatch (VALENCIA-003)
- Word locks an open export DOCX; rename fails until closed, so use a VOID sidecar note (VALENCIA-003)
- The report analyzed six 12x8 ft boxes while the later plan shows three 24x8 ft arches, and the plan HW note repeated the old box result (SILVERBELL-014)
- A request said drainage area reduction; it meant opening area per cell (about 10 sq ft each, 29-30 sq ft total) (SILVERBELL-014)
- The original flow split between two openings; also test full crossing flow through one structure (SILVERBELL-014)
- Recomputed arch area loss (10.00 sq ft) differed from the contractor value (9.58); report the difference (SILVERBELL-014)
- Result was HW rise 0.45-0.50 ft, still at least 2.6 ft below existing HW; state margin to the approved HW (SILVERBELL-014)
- GUI automation through dialogs was slow and fragile; text editing of a seed .hy8 file was faster (SILVERBELL-015)
- Inlet relationships for user-defined shapes are generic; note no manufacturer inlet data (SILVERBELL-015)
- LibreOffice was not available for DOCX rendering; Word export was used for page QA (SILVERBELL-015)
- 72 in RCP alternative had under 1 ft cover; check cover for every alternative (CALFIRE-012)

## QC checks
- Pull: `get_qc_rules('culverts')`, `get_qc_rules('appendix')`.
- `hy8_template.py check` pass on every INPUT file; NATIVE reopened in a fresh project.
- HY-8 closed without a report = failed run, logged.
- Native vs independent HDS-5 within 0.2 ft HW and 0.5 fps, or the difference reconciled and recorded in 40_QC.
- Total flow = barrel + roadway; solver mode recorded; cover checked.
- Appendix carries the native report for the selected design; independent check not in the deliverable.

## Change log
- 1.0.0 2026-10-22: built from cluster HYD-C20 (plus HYD-C26 appendix items); decisions D10, D16 (default, to
  confirm), D30, D38. HDS-5 coefficient rows in hds5_check.py to confirm against HDS-5 Appendix C before first
  use (default, to confirm).
