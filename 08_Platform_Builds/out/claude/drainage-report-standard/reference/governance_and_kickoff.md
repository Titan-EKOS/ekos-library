# Governance actions and kickoff plan (from Standard v0.3 package skills)

Carried from the v0.3 package skills `drainage-kickoff.md` and `drainage-governance.md`; every rule still valid is
kept. Changes: the reviewing-engineer role reads JCO; decision register (QC-C05) and open-items list (D44) added;
dates YYYYMMDD (D56). `<STANDARD>` = the release folder; `%DOCS_PY%` = documents venv interpreter (full path).

## The register is the lock
- CalcRegister: one row per Element x Option (ElementID such as C-3, CH-2, DB-1, CP-14, 2D-PROP; OptionID A/B/C).
- Status WORKING -> OPTION -> RECORD -> SUPERSEDED / NOT_SELECTED / VOID. One RECORD per element; RECORD needs checker
  initials; only RECORD is citable.
- Files: WORKING in `20_Working\<Initials>_<YYYYMMDD>_<Topic>\` (the only place new files are created; nothing there
  is citable); OPTION/RECORD in `10_Record\<Letter>\`; SUPERSEDED / NOT_SELECTED / VOID in
  `10_Record\_Superseded\<Letter>\` (never deleted).
- The ask creates the row: when someone is about to run a calc, add the WORKING row first (ElementID, description,
  letter, planned software and version).
- Calc letters D-J in 10_Record equal the appendix letters in 30_Report\Appendices.
- Native models may stay in the job CALCS tree; the CalcRegister `Native model path` points at them; the printout the
  report relies on lives in 10_Record.

## Actions (AI_Prompts ids)
**PROMOTE-01**
`"%DOCS_PY%" "<STANDARD>\standard\promote_calc.py" --workbook <..>\00_Admin\<wb>.xlsx --calc CR-nnn --status OPTION|RECORD [--checker ABC] [--close-others NOT_SELECTED] [--reason "..."]`
or, for a file with no row yet: `--file <20_Working path> --element C-3 --option B --letter F_Culverts_Bridges_Scour
--software HY-8 --version 8.00 --desc "..." --status OPTION`. It refuses RECORD without a checker, supersedes the
previous RECORD (file -> _Superseded), closes other options, logs to 00_Admin\PROMOTION_LOG.md, recalculates.
Use `--dry-run` first when unsure; report what moved. v0.3: write the DecisionRegister entry (below) yourself
before superseding a RECORD; v0.4 adds `--decision DEC-nn` (CS-06).

**CASCADE-01 (after a hydrology or basis change)**
Read CalcRegister (ElementID links, Feeds table blocks), every hydraulic/detention/erosion/floodplain table block,
ExhibitRegister Source CalcIDs, Narrative and ReportText. Write the DecisionRegister row first, then the impact
list grouped re-run / re-transcribe / re-word; create WORKING rows for each re-run; STOP for JCO approval before
any RECORD changes.

**DECIDE (decision loop, QC-C05)**
1. List each competing value with source, method and where it is used.
2. Classify: isolated (no receiving system or shared control affected) vs propagating.
3. Resolve isolated, evidence-supported conflicts; log feature, values, sources, choice, reason, dependency check.
4. Ask JCO propagating questions one at a time: short problem statement, options and consequences, a plan/profile
   image. Do not edit tables until decided.
5. Once decided, update narrative, tables, exhibit labels, HY-8 and protection sizing together; keep each native run
   and the final decision.
6. Write resolved decisions to the continuation handoff so the next session does not re-ask.
v0.3 home for the register: `00_Admin\DECISION_REGISTER.md` (columns as CS-06); v0.4: workbook sheet.

**QC-TABLE-01** Compare every value and unit in a block to the RECORD calc file for its ElementIDs; flag rows whose
element has no RECORD; test results against Criteria (T-GEN-01) limits. Pass/Fail per row with the exact
discrepancy. Read-only.

**RECONCILE-01** `"%DOCS_PY%" "<STANDARD>\standard\reconcile_records.py" --report-folder <..> --md <..>\40_QC\reconcile_<YYYYMMDD>.md`
(or `--jobs <STANDARD>\jobs.json`). Codes E1-E12: files in 10_Record without rows (E1), rows without files (E2),
wrong tier (E3), RECORD without checker (E4), duplicate RECORD (E5), open options (E6), stale WORKING (E7), idle
20_Working folders (E8), RECORD file modified after its check date (E9), exhibits without a source calc (E10/E11),
version drift (E12). Read-only; exit 1 when anything must be fixed. Send exceptions to preparer and PM only when
asked or when running as the weekly task; if the folder is not reachable, say so instead of guessing.

**PRECHECK-01** Zero duplicate RECORD flags, zero RECORD without checker, zero open OPTION rows, zero WORKING rows
feeding an included table, zero Narrative rows on excluded sections, zero exhibits still Planned/Draft, QC_Log T1
complete with no Fail, RevisionLog row for the milestone, zero open items in the open-items list (or JCO
authorization recorded, D44). Pass/fail with offending rows.

**FILL-01** Fill a table block from a printout: block rows plus a "could not read" list; never estimate.
**QC-NARR-01** Narrative vs tables: list every disagreement (a wrong number in VERBATIM text passes the drift check;
governance is about traceability, so this check is the one that catches it).
**COMPARE-01** Compare to prior study: T-HYD-06 filled, variance narrative as REWRITE.

## Kickoff (W00) -> COORDINATION_PLAN.md
Format: `<STANDARD>\standard\COORDINATION_PLAN_SPEC.md` - follow it exactly.
1. If the report folder does not exist:
   `"%DOCS_PY%" "<STANDARD>\standard\make_report_folder.py" <job_root> <ReportID> <ShortName> --job <Job> --title "..." --jurisdiction <code> --workbook-template "<STANDARD>\Psomas_Drainage_Report_Workbook_TEMPLATE.xlsx"`
   (the seal-name argument of the v0.3 script takes JCO's name and PE number as on the cover).
2. Read the workbook: Kickoff (narrative, client ask, deadline, location block, ko_site_image, data inventory,
   expected analyses linked to Setup, constraints), Setup, Lists, Manifest, CalcRegister, Narrative,
   ExhibitRegister, AppendixRegister. Read the package JSON: master_outline.json, tables.json,
   requirements_matrix.json, text_library.json. If ko_site_image is given, read streets, coordinates, washes, parcel
   lines from it and state how confident the geolocation is.
3. Write 00_Admin\COORDINATION_PLAN.md: Understanding (12 lines max); Open questions (every blank Kickoff cell, every
   "Need", every Setup-vs-narrative conflict, each with what it blocks); task graph in dependency order (hydrology ->
   hydraulics -> detention/erosion -> floodplain comparison -> exhibits -> assembly), one block per task with
   executor = local model | reasoning model | engineer, inputs, tool + version from Setup, method reference from the
   requirements matrix with the criterion value, outputs as 10_Record\<Letter>\<file> -> CalcRegister element ->
   table block(s), acceptance checks with numbers, escalate-when triggers, hours; escalation protocol; register
   seeding list; schedule back from the deadline.
4. Seed the workbook (never overwrite an existing row; recalc with xl_recalc.py afterwards): CalcRegister one WORKING
   row per element x option; Narrative CONTEXT_ONLY rows for every assumption, constraint and open question plus one
   REWRITE topic sentence per included section the narrative supports; ExhibitRegister rows at Planned for every
   figure the Manifest expects, with Source CalcID(s) or n/a.
5. Set Kickoff ko_plan_status = "Plan drafted", ko_planner = model + date. Stop. JCO approves before execution.

Kickoff rules
- Never compute engineering results, invent data or change Setup; blanks become open questions, not guesses.
- Use the jurisdiction's method names as they appear in Setup (S-07, S-08, S-23.1, S-28).
- Executor rule: local model = deterministic transcription, formatting, file handling, running a documented tool with
  fixed inputs; reasoning model = judgment, method choice, interpreting disagreement, drafting narrative;
  engineer = licensed decision, site visit, phone call, anything that changes a RECORD.
- Every task produces a file that gets a register row; otherwise it is a step inside a task.
- The plan must read the same whichever executor runs it. Escalation answers go back into Narrative as CONTEXT_ONLY
  so context lives in the workbook, not in chat history.
- Return: plan path, open-questions table, counts of rows seeded per register, first three tasks that can start now.

## Never
- Delete a file or row (supersede/void instead); edit Setup/Manifest/table structure during governance actions;
  promote to RECORD without checker initials; change a RECORD without JCO's explicit approval.
- Guess a value: anything not in a file or the workbook is a question for the engineer.
- Print EngineerNotes or CONTEXT_ONLY text; edit VERBATIM text in Word (workbook cell only); copy the template into
  a job (the workbook is the only job-owned file).
