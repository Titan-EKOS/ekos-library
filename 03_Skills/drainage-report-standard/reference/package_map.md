# Standard v0.3 package map (EKOS)

Package root: `D:\LocalAI_Test\Drainage_Report_Standard_v0.3_TRANSFER\Drainage_Report_Standard_v0.3_TRANSFER`
`<STANDARD>` = `<root>\standard\30_Standard_v0.3` (one published copy; nothing from it is copied into a job except
the workbook template).

## Release folder
| Path | Use |
|---|---|
| `CURRENT.json` | release pointer: standard_version 0.3.0, published true, release_folder (set to the EKOS path) |
| `Psomas_Drainage_Report_TEMPLATE.docx` | official Report_Template_7 build, core property version 0.3.0; `--template`; never copied into a job |
| `Psomas_Drainage_Report_Workbook_TEMPLATE.xlsx` | copied to `00_Admin\<Job>_<ReportID>_Workbook.xlsx`, the only job-owned file |
| `standard\assemble_report.py` | generator: version gate, Manifest, library text, tables, figures, narrative modes, drift + leak checks, CalcRegister checks, `_ASSEMBLY_REPORT.md`, `_REWRITES.json` |
| `standard\apply_rewrites.py` | applies Accept / Revert / Edit from `_REWRITES.json`; keeps `_pre_rewrites.docx` |
| `standard\make_report_folder.py` (+ .bat) | builds the report folder from `folder_tree.txt`, MANIFEST.json, stubs |
| `standard\promote_calc.py` | 20_Working -> 10_Record with register update, checker rule, supersede, close-others, PROMOTION_LOG |
| `standard\reconcile_records.py` | audit E1-E12, markdown/JSON, exit 1 on exceptions |
| `standard\COORDINATION_PLAN_SPEC.md` | kickoff plan format |
| `standard\CLAUDE_ASSEMBLY_PROCEDURE.md` | v0.3 assembly procedure (content folded into this skill) |
| `standard\*.json` | master_outline (72 sections), text_library (173 entries), tables (51 blocks), requirements_matrix (152 rows), workbook_schema, setup_keys, inputs, qc_checklists (T1 29 / T2 18 / T3 19 / 14 recurring defects), workflow (W01-W13) |
| `build\patch_workbook_v03.py` | v0.2 -> v0.3 workbook migration (never by hand) |
| `regression\` | Campbell Avenue 60% re-assembly (internal only; reference output) |
| `pilot\` | Sahuarita pre-filled workbook + governance smoke test |
| `jobs.json` | active report folders for the weekly reconciliation |
Package root also has `requirements.txt` (openpyxl, python-docx, lxml, pypdf), `docs\`, `skills\` (superseded by
this skill), `example_job\` and `reference\` (v0.1 Procedures Guide, Standard Language Library, official templates).

## assemble_report.py options
`--workbook --template --out` (required); `--include-examples` (template dry runs only); `--mode build` (ignore the
template body, build from the outline; memo plain layout); `--trust-manifest`; `--keep-guidance` (working draft);
`--lib-tags` (gray `[LIB:ID]` after each entry for tracing); `--allow-version-mismatch` (template dry runs only, never
a job deliverable; say so when used).

## _ASSEMBLY_REPORT.md sections used here
s1 pre-flight (version gate, verbatim drift, leak check, CalcRegister lines) | s3 citation status (VERIFY entries) |
s5 unresolved placeholders | s6 tables with zero data rows | s9 human decisions | s10a rewrite queue | s10b
CONTEXT_ONLY rows (not printed) | s11 calculation-of-record list for the transmittal.

## Workbook sheets
Kickoff (W00) | Setup (P-01..P-27, S-01..S-41; every value cell is a named range = its key, so `{key}` resolves) |
Lists | Manifest (formulas; governance counters I3:J7) | 16 table sheets with 51 blocks `T-XXX-nn` (Include? (auto),
source-field row, header with units, EXAMPLE row skipped, 25 input rows; first column = element ID) | CalcRegister
(auto flags Y/Z, counters row 3) | Narrative (VERBATIM / REWRITE / CONTEXT_ONLY / OMIT) | ExhibitRegister (F-nn,
status Planned / Draft / Checked / Final / Superseded, Source CalcIDs) | AppendixRegister (A-L, Used?) | QC_Log (T1
29, T2, T3, 14 recurring defects) | RevisionLog | Checklist (jurisdiction matrix rows) | AI_Prompts (11 prompts).
Cell colours: yellow = enter; green = formula default you may overwrite; grey = fixed by release; white = formula.
Key Setup items: S-01 jurisdiction, S-02 secondary agencies (FEMA switches on TDN behaviour), S-03 report type (DR,
DR_PAVE, DR_MASTER, ADD, TM, HH, TDN, DCR), S-04 phase, S-06.01-.12 facility flags, S-23.1 detention method (volume
estimate withholds routing text and T-DET-01/02/06), S-36 numbering style, S-41 standard_version (do not edit),
P-09..P-21 cover/transmittal keys, P-22..P-27 people.
Filling order: Kickoff -> Setup S-01, S-03, S-04, S-06 flags, rest -> save -> plan and seed -> CalcRegister rows as
work starts, promote as work finishes -> table blocks from RECORD printouts -> Narrative -> Exhibit/Appendix
registers -> QC_Log T1 -> RevisionLog row -> recalc and save -> assemble.

## Job report folder (v0.3 tree + D56)
Mount: `<Job>\ENGR\DOCS\Drainage Report\<ReportID>_<ShortName>\` (no ENGR root: `<Job>\WATRES\GLOBAL\DOCS\Drainage Report\`).
ReportID = DR-01, DR-02, ADD-01, TM-01, HH-01, TDN-01, DCR-01.
```
00_Admin\        <Job>_<ReportID>_Workbook.xlsx, MANIFEST.json, COORDINATION_PLAN.md, REVISION_LOG.md, PROMOTION_LOG.md,
                 QC_LOG.md, DECISION_REGISTER.md (v0.3 stand-in for CS-06)
01_Reference\    Prior_Studies, Agency, FEMA, Record_Drawings, By_Others
02_Data\         Rainfall, Soils_LandUse, Topo_Survey, Field_Visit, Plans_Current
10_Record\       D_Hydrology .. J_Erosion_Sediment, X_Exhibits (_FIGURE_INDEX.md), _Superseded\<Letter>\
20_Working\      <Initials>_<YYYYMMDD>_<Topic>\   (only place new files are created)
30_Report\       Drafts\ (dated DRAFT .docx + _ASSEMBLY_REPORT.md + _REWRITES.json, never overwritten),
                 Appendices\A_..L_, Z_Digital_Appendix\, Issued\<YYYYMMDD>_<Milestone>\ (RECORD_SET.md)
40_QC\           T1_Self_Check, T2_Calc_Check (marked check prints), T3 review folder, reconcile_<YYYYMMDD>.md,
                 QC open-items document (D44), compile QA JSON
50_Correspondence\ <YYYYMMDD>_<Agency>_<Milestone>\
30_Report\Issued\   <Initials>_<YYYYMMDD>_<CODE>_<description>\   (D56; built by delivery-package-build)
```
Appendix letters: A Regulatory/Site Data, B Exhibits, C Previous Studies/As-builts, D Hydrology, E Floodplain/Channel
Models, F Culverts/Bridges/Scour, G Channels/Swales, H Pavement/Inlets/Storm Drain, I Detention/Retention/WQ,
J Erosion/Sediment, K Plan Sheets, L Correspondence/Checklists/Comments, Z Digital Appendix. Unused letters are
omitted from the report; the folder stays empty.
Older trees: 03_Calcs -> 10_Record; 04_Exhibits -> 10_Record\X_Exhibits; 05_Text -> 30_Report\Drafts;
06_Appendices -> 30_Report\Appendices; 07_QC -> 40_QC; 08_Submittals -> 30_Report\Issued; 09_Comments ->
50_Correspondence; 99_Superseded -> 10_Record\_Superseded; 99_Working -> 20_Working.

## File naming
Workbook `<Job>_<ReportID>_Workbook.xlsx`; drafts `<Job>_<ReportID>_<Milestone>_<YYYYMMDD>_DRAFT.docx`; record calcs
`<ElementID>[_Opt<X>]_<Software>_<YYYYMMDD>.<ext>` (e.g. `C-3_OptB_HY8_20261022.pdf`); figures
`Fig<sec>-<n>_<Title>_<YYYYMMDD>.pdf` (D52 numbering by section); working folders `<Initials>_<YYYYMMDD>_<Topic>`.
The job number appears in the workbook name, the folder, the cover and every calc header.
