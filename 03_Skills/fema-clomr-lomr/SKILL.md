---
name: fema-clomr-lomr
description: Detailed FEMA CLOMR/LOMR procedure - case setup, effective-model basis, scripted model and post-processing chain, community items (flooding-source names, O&M, owner notification), additional-data (AD) letter response within 90 days, package build (README, ZIP64, review PDF) and the pre-upload package QC gate. Use when a CLOMR or LOMR is being prepared, an AD letter or closure letter arrives, a resubmittal or new case is being built, or any package is about to be zipped and uploaded to FEMA. This is the procedure that drainage-report-build/addons/fema.md points to.
version: 1.0.0
status: active
function: report-assembly
jurisdiction: FEMA (Region IX notes); community Pima County RFCD, Town of Marana co-signs in Marana
tools_versions: "FEMA MT-2 forms, Online LOMC; FLO-2D Pro 26.02.25; HEC-RAS 6.6; HY-8 8.0; QGIS 3.44; Python 3.12 (python-docx, openpyxl)"
owner: JCO
replaces: "none (new; detail for drainage-report-build addons/fema.md)"
---
# FEMA CLOMR / LOMR: submittal management, AD response, package build and QC gate

A case closes for insufficient data when the package, the models and the response letter do not
agree. Two closures on one project cost about 80 h and a new case fee (STARVALLEY-004,
STARVALLEY-006). This skill exists so that never happens again: every model is rerun after its last
edit, every response row points at a file in the package, community items are in hand, and a gate
script plus an independent auditor pass the archived upload package before it goes to FEMA.

## When to use
- Starting a CLOMR or LOMR (FLO-2D or HEC-RAS based), or reviving a closed case as a new case.
- An AD (additional data) letter or a closure letter arrives.
- Any rebuild of the duplicate effective, existing or proposed models for a FEMA package.
- Before any package is zipped and uploaded, and before any letter says an item is complete.
Report content rules (TDN outline, FEMA section text) stay in drainage-report-build with
`addons/fema.md`; this skill is the procedure.

## Inputs
- Effective study: FIS, FIRM panels, TDN, effective model package (all storm cases), NFHL.
- Survey, approved grading and drainage plans, structure data (as-builts or approved plans), HY-8
  projects for every structure.
- Community contacts (Pima County RFCD floodplain; Town of Marana where applicable).
- For a response: the AD or closure letter, the archived previous upload package (zips as uploaded),
  the prior response matrix.
- Project open-items document (D44) and run log.

## Related masters
- flo2d-model-runs: FLO-2D build, 1D channels, structures, development effects, run harness.
- hecras-2d-models: HEC-RAS based cases.
- impact-comparison: matched existing/proposed models, dWSE and 44 CFR 65.12 rise analysis.
- hy8-native-runs: native HY-8 ratings that HYSTRUC tables must equal.
- model-run-supervisor (agent): rerun-all gate and run status.
- qc-reviewer (agent): independent submittal audit and optional blind rebuild.
- agency-comment-response: comment log mechanics and D45 status vocabulary.
- drainage-report-exhibit-standards / scripted-exhibit-sheets: work maps and exhibits.
- delivery-package-build: zip, manifest, checksums.

## Steps

### 1. Case setup (day one)
1. Open a case folder under the D56 job layout: `10_Record/FEMA_Effective/` (unchanged effective
   package, hashed), `20_Working/Models/{DupEff,Existing,Proposed[_Phase]}/`, `30_Report/TDN/`,
   `40_QC/Package_QC/`, `50_Correspondence/FEMA/`, `30_Report/Issued/FEMA_Upload_<YYYYMMDD>/`.
2. Record the case type (CLOMR, LOMR, CLOMR-F, LOMR-F), case number, community (Pima County RFCD;
   in Marana also the Town, BARNETT-004) and the FEMA reviewer in the open-items document.
3. Read the effective TDN storm list (duration, depth) and controlling-storm statement. Confirm the
   effective package holds the upstream rainfall-runoff model and detailed model inputs for **every**
   storm case. Request missing cases from the community or the FEMA library before modeling; do not
   claim a flood envelope from one storm (STARVALLEY-022).
4. Use effective inflows, not county design flows, for the FEMA comparison; flag as an open item
   whether FEMA and agency design flows share an engineering basis.
5. Start community items the same day (Step 3): draft the flooding-source name, O&M and owner
   notification emails.
6. Decide phase scope now: if any phase has only concept-level grading, expect FEMA to require its
   removal or design-level grading and drainage plans. Make the decision with JCO before modeling
   and record it (Step 4.5).

### 2. Model basis and scripted build
1. Preserve the effective package unchanged; work on hashed copies. Convert a legacy effective model
   to the current build per flo2d-model-runs and get JCO acceptance of the current-build baseline in
   writing (D03: record agency-named build and working build; 26.02.25 with written acceptance).
2. One model set for all conditions: effective grid as base terrain, replaced only inside approved
   grading; same 1D channel network, FPXSEC, INFLOW, OUTFLOW, TOLER, RAIN and engine build in every
   condition; only development and grading differ (impact-comparison).
3. `build_models.py` regenerates every derived input from source surfaces, centerline and design data;
   it logs cell counts and surface sources. No hand edits to derived inputs.
4. Keep a shared helper module (grid, TOPO, LandXML, coordinate transform readers). Drive package
   variants (with/without phase, alternatives) by environment variables so all variants come from the
   same sources.
5. Back up each script version (`v3bak`, `v4bak` or a commit) before changing it so a regression can
   be traced.
6. Write all FLO-2D text inputs with CRLF line endings (STARVALLEY-001; checked by the gate).

### 3. Community items (start on day one; long lead)
Use `reference/community_items_and_matrix.md` section 1.
1. Signed letter or email from the community accepting the flooding-source name of each new
   AO/AH/AE source.
2. O&M plan: names each FEMA-required basin, community (not an HOA) as ultimate responsible party,
   who maintains and how often, community official signature or concurrence; scope does not exclude
   public basins or channels.
3. Owner notification on the FEMA **CLOMR** template (not LOMR) with the approved names; submit the
   draft before mailing.
4. Community acknowledgement signed by every community with jurisdiction (RFCD; Town of Marana too
   in Marana).
5. Track each item in the open-items document; none may be open at upload.

### 4. Run, post-process and assemble (the post-chain)
1. Run every model through model-run-supervisor (D04 completion for FLO-2D, D05 for HEC-RAS; D09
   final-run volume error <= 0.1%).
2. **Rerun-all gate:** every model, including existing conditions and the duplicate effective used for
   comparison, has outputs newer than its last input edit. Re-run any model edited after its run.
3. Post-chain, in order, from one script: post-process results; structure flows (stop if any wet-inlet
   structure shows zero flow); dWSE location tables and 44 CFR 65.12 rise analysis
   (impact-comparison); flood zones and BFE contours for every condition (vector zones, not depth
   rasters, on the work map); model shapefiles; Appendix D warnings; QGIS exhibits; report writer;
   package QC.
4. **Appendix D:** tabulate every ERROR.CHK and runtime-warning message per model; mark those that
   also appear in the duplicate-effective run as inherited; give a disposition for each.
5. **Concept-level phase:** if JCO keeps it, produce a conceptual grading and drainage exhibit
   (contours, flow arrows, spot elevations) and build both with-phase and without-phase packages from
   the same sources by environment variable. If FEMA has rejected the concept argument once, call the
   reviewer before resubmitting.
6. Report text generated by code is scanned for code fragments and placeholders (the gate does this;
   also read the generated sections once).

### 5. Package build
1. Folder structure per FEMA upload: Forms (MT-2), Report/TDN, Models (one folder per condition with
   FLOPRO.exe, DLLs, inputs, outputs), GIS (zones, BFE contours, model shapefiles, work map data),
   Exhibits, Correspondence (community items, response matrix and letter).
2. Write a package README (contents, model-to-condition map, engine build, how to run, file counts).
3. Run the gate (Step 6). Include `package_QC_report.txt` as a report appendix (package checklist
   result only); the script, its working files and any independent recalculation stay in
   `40_QC/Package_QC/` (D30).
4. Build ZIP64 zips at the end, after the gate passes; split per the FEMA upload limit.
5. Compile one review PDF of all exhibits and documents for the auditor and JCO (D48 flattening; D52
   bookmarks and size limit).
6. Archive the exact zips uploaded to `30_Report/Issued/FEMA_Upload_<YYYYMMDD>/`; never rebuild them
   after upload.

### 6. Pre-upload QC gate (fail = do not upload)
1. Run the gate on the staged package model folders:
   `D:\EKOS\venvs\gis\Scripts\python.exe scripts\package_qc.py --model DUPEFF=<dir> --model EXIST=<dir> --model PROP=<dir> --gis <GIS dir> --docs <Report dir> --out package_QC_report.txt`
   (container: `python3 scripts/package_qc.py ...`). First model = duplicate effective (DLL reference).
   Checks, per model: build strings exe = CONT.DAT line 1 = SUMMARY.OUT; DLL set present; required
   inputs/outputs present (CHAN/CHANBANK/XSEC and CHANMAX/CROSSMAX when channels exist;
   HYDROSTRUCT with HYSTRUC; MAXWSELEV, DEPTH, ERROR.CHK); zero TMP files; oldest output newer than
   newest input; SUMMARY.OUT completed with a volume conservation line; CRLF in text inputs. Across
   models: CADPTS, INFLOW, OUTFLOW, FPXSEC, TOLER, RAIN identical by hash. Package: zone and BFE
   shapefiles per condition (file names carry the condition name); no placeholders ([DATE],
   [TO BE CONFIRMED], bracketed notes) or code fragments in DOCX/XLSX/TXT/MD.
2. Manual line in the report: HYSTRUC rating tables equal the HY-8 export (names, discharge pairs,
   headwater reference offset). Record pass/fail.
3. Exit code 1 = FAIL. Fix and rerun; do not override a failed check.
4. For HEC-RAS cases run the equivalent checks by hand or through model-run-supervisor: one RAS
   version (D02), plan result HDF newer than geometry/flow/plan files, volume accounting, no
   placeholders, shared boundary files identical.

### 7. Independent audit before upload
1. qc-reviewer (an agent or person that did not build the package) audits the **archived upload
   zips**, not the working folders: zip members and timestamps, output-older-than-input, missing
   outputs, TMP files, build mismatches.
2. For each FEMA comment it classifies: addressed with file evidence, done-but-not-run, not done,
   stale (agency text repeated from a prior letter that the files disprove), or new.
3. It compares every response-letter claim to the models and GIS in the package and flags any claim
   without a file and page.
4. Optional for high-stakes cases: a time-boxed blind rebuild scoped to duplicate-effective
   reproduction, terrain/coordinate checks, HY-8 ratings, basin storage and rise analysis (qc-reviewer).
5. Findings go to JCO as decisions; the upload waits for JCO sign-off.

### 8. AD letter response (90 days, no extensions)
1. On receipt: log the 90-day deadline in the open-items document; fill the deadline worksheet
   (`reference/community_items_and_matrix.md` section 3); the last model run finishes at least 10 days
   before the deadline.
2. Start community-dependent items the same day (Step 3).
3. Build the response matrix (reference section 2): every row states what changed, file name, folder
   and report page; status per D45. Any status other than Addressed (or Stale with evidence) does not
   ship.
4. If an item needs a decision the agency already rejected, settle it by call before resubmitting;
   record the call in `50_Correspondence/FEMA/`.
5. Re-run every model after its last input edit, including existing conditions used for comparison
   (rerun-all gate), then Steps 4-7.
6. Generate the response letter from the matrix; no separate typing.
7. Upload only after gate PASS, audit complete and JCO sign-off. Do not upload early just because
   the package looks done.

### 9. After upload or closure
1. Archive the uploaded zips, gate report, audit report and matrix together.
2. On a closure letter: run the independent audit on the archived package first, separate legitimate
   findings from items the files disprove (for fee or reopen requests), then plan the new case from
   Step 1.
3. Log lessons (`log_lesson`) with card-style evidence.

## Jurisdiction add-ons
- This skill is the FEMA procedure; report content rules are in
  `get_skill("drainage-report-build", resource="addons/fema.md")` (effective inflows for FEMA
  comparisons, all effective storm cases, FIS 0.2% profile only where sections bracket the site per
  D22, Zone AO depth is not an elevation, FIRM marking per D39).
- Community: `addons/pima-county-rfcd.md` (RFCD is the community for unincorporated Pima County);
  `addons/town-of-marana.md` (Town co-signs the community acknowledgement with RFCD, BARNETT-004).
- impact-comparison carries a FEMA add-on for the rise analysis; use the agency or FEMA threshold
  cited per project (D29), 1.00 ft for 44 CFR 65.12 where it applies.

## Gotchas
- Response sent 37 days early with unrun models and missing community letters; case closed for
  insufficient data and resubmitted as a new case (STARVALLEY-006).
- FEMA rejected the concept mass-grading narrative in AD01, AD02 and the closure; two packages (with
  and without the phase) were built for the new case (STARVALLEY-017).
- Revised O&M named the HOA, excluded public basins, lacked a community signature block and did not
  name basins; two community items open at closure and at new-case build (STARVALLEY-018).
- June package shipped Ultimate outputs older than 16 edited inputs, a CONT.DAT header of Build
  16.06.16 against a 23.10.25 SUMMARY.OUT, existing-condition folders with zero outputs, 8 TMP files
  in Interim and no zone shapefiles; FEMA closed the case and a new case and fee were required (40 h)
  (STARVALLEY-004).
- FEMA runs the exe / CONT.DAT / SUMMARY.OUT build comparison itself; a stale header string alone
  draws a comment (STARVALLEY-004).
- Report text generated from code leaked a Python conditional string into the TDN draft (sec. 4.8.3)
  (STARVALLEY-020).
- Keep backups of each script version so a regression can be traced (STARVALLEY-020).
- Effective TDN listed 3-hr 3.34 in and 24-hr 4.55 in storms; only the 3-hr case was in the package;
  the main package and the blind rebuild both ran 3-hr only (STARVALLEY-022).
- LF-only FLO-2D inputs written by script caused channel errors that content fixes did not clear;
  the line-ending check belongs in package QC (STARVALLEY-001).
- Working response letter carried 10 TO BE CONFIRMED placeholders while the uploaded PDF stated those
  items complete; the reviewer cited letter-vs-model discrepancies (STARVALLEY-005).
- About a third of a closure letter was stale wording from the prior letter; an audit with file
  evidence lets the cover letter say so without arguing (STARVALLEY-005).
- The audit must be done by an agent or person that did not build the package, so it does not trust
  builder notes (STARVALLEY-005).
- A full blind rebuild in one session ran about 9.5 h and used 47% of the weekly allowance without
  finishing; scope and time-box it (STARVALLEY-021).
- The blind rebuild found items the main package missed: absent 24-hr storm files, basin storage
  15.71 vs 18.10 ac-ft approved, a culvert headwater 0.02 ft over allowable, omitted storm-drain
  outlet loss (STARVALLEY-021, STARVALLEY-023).
- Zone shapefiles built months earlier were left out of the upload; depth rasters presented as the
  work map were rejected (STARVALLEY-009).
- Existing and proposed models carried different channel networks; offsite dWSE over 1 ft (157 cells)
  was an artifact of the mismatch (STARVALLEY-007).

## QC checks
Pull: `get_qc_rules('fema')`, `get_qc_rules('package')`, `get_qc_rules('flo2d')` (FLO-2D cases) or
`get_qc_rules('hydraulics-2d')` (HEC-RAS cases), `get_qc_rules('comment-response')`,
`get_qc_rules('model-runs')`, plus `('pima-rfcd')` / `('marana')` for the community.
This skill must pass before upload:
- `package_QC_report.txt` RESULT: PASS, included as a report appendix; HYSTRUC = HY-8 manual line
  recorded.
- Rerun-all gate: every model's outputs newer than its last input edit (model-run-supervisor).
- Every effective storm case present and run; effective inflows used for the comparison.
- Response matrix 100% Addressed (or Stale with evidence); every row cites a file, folder and page in
  the archived package; letter generated from the matrix.
- Community letters in hand: flooding-source names, signed O&M (community responsible), CLOMR owner
  notification draft accepted, community acknowledgement signed (RFCD; Town of Marana where
  applicable).
- Independent audit of the archived zips complete; JCO sign-off recorded.
- Deadline worksheet shows last run >= 10 days before the AD deadline.
- Zero placeholders or code fragments in any document (D44).

## Files
- `scripts/package_qc.py`: pre-upload gate for FLO-2D packages (writes package_QC_report.txt;
  exit 1 on FAIL).
- `reference/community_items_and_matrix.md`: community item checklist, O&M checklist, AD response
  matrix columns, deadline worksheet.

## Change log
- 1.0.0 2026-10-22: built from clusters HJR-C21 and RPT-C13 (with STARVALLEY-001, -005, -007, -009,
  -021, -022, -023 detail from cards and HJR-C11/C12 FEMA seed content); decisions D02, D03 (default,
  to confirm), D04, D05, D09, D22, D29, D39, D44, D45, D48, D49, D52 (default, to confirm), D56.
  package_qc.py written and tested on synthetic model folders (pass case and a failing case covering
  build mismatch, TMP, stale output, LF endings, hash mismatch, missing shapefiles, placeholders).
  Items marked default, to confirm: FLO-2D 26.02.25 acceptance per project (D03); deadline worksheet
  offsets other than the 10-day last-run rule.
