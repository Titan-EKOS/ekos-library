---
name: drainage-report-standard
description: Run the Psomas Drainage Report Standard package on EKOS end to end - kickoff and folder, workbook and register governance, native Excel recalc, assemble_report.py, DOCX post-process, Word export and the compiled bookmarked PDF - and hold the v0.4 change spec for the package.
version: 0.4.0
status: active
function: report-assembly
jurisdiction: all
tools_versions: "Standard package v0.3.0 (code); Python 3.10+ with openpyxl, python-docx, lxml, pypdf, pywin32; Word/Excel 365; HEC-HMS 4.13; HEC-RAS 6.6; HY-8 8.00"
owner: JCO
replaces: "Standard v0.3 package skills drainage-kickoff.md, drainage-governance.md, psomas-drainage-report-assembly.md, plus START_HERE and CLAUDE_ASSEMBLY_PROCEDURE operating content"
---
# Drainage Report Standard (workbook -> assemble -> post-process -> Word export -> compiled PDF)

Skill version 0.4.0. The package code on EKOS is still v0.3.0: the v0.4 changes in `reference/v0.4_change_spec.md`
are a spec, implemented and regression-tested in Phase 5. Until then this skill runs the v0.3 package and uses the
library helpers in `scripts/` (recalc, post-process, Word export, compile) where v0.4 will add package steps.
Do not edit the package code from this skill.

## When to use
- A drainage report, TM, addendum, H&H study, TDN or DCR is built on the Standard workbook (any jurisdiction).
- Kickoff or re-scope of a report: folder, Kickoff sheet, coordination plan, register seeding.
- Promoting, superseding, reconciling or auditing calcs; a design flow or basis value changed.
- Regenerating a draft after a calc, plan or comment change; compiling the submittal PDF.
- Content and formatting rules come from `drainage-report-build` and `drainage-report-exhibit-standards`; this skill
  is the mechanics of the Standard package. Memos: `drainage-technical-memo`. Comment cycles:
  `agency-comment-response`. Handover zips: `delivery-package-build`. New project folder and data:
  `project-intake`.

## Inputs
- Package root (EKOS): `D:\LocalAI_Test\Drainage_Report_Standard_v0.3_TRANSFER\Drainage_Report_Standard_v0.3_TRANSFER`.
  `<STANDARD>` = `<root>\standard\30_Standard_v0.3`. Map of files: `reference/package_map.md`.
- `%DOCS_PY%` = full path of the EKOS documents venv interpreter (openpyxl, python-docx, lxml, pypdf, pywin32)
  (D11). Example: `set DOCS_PY=D:\EKOS\venvs\docs\Scripts\python.exe` (path to confirm in the library config).
  Never bare `python` or a global pip in a long job.
- `%SK%` = this skill's `scripts\` folder in the library.
- Job report folder `<Job>\ENGR\DOCS\Drainage Report\<ReportID>_<ShortName>\` and its workbook
  `00_Admin\<Job>_<ReportID>_Workbook.xlsx`.
- Stop and ask if missing: workbook path; milestone / revision / office address / contact in Setup (P-09..P-21);
  confirmed reviewing agency; JCO seal name and PE number (P-07/P-08).

## Steps

### A. Release check (every run)
1. Read `<STANDARD>\CURRENT.json`: `published: true`, note `standard_version`. On EKOS set `release_folder` to the
   EKOS path once (the shipped value points at an office OneDrive folder).
2. Workbook Setup S-41 and the template core-property version must equal CURRENT.json or the generator stops
   (`FAIL version gate`). A pre-v0.3 workbook is migrated with
   `"%DOCS_PY%" "<STANDARD>\build\patch_workbook_v03.py" <old.xlsx> <new.xlsx>`, never by hand; then register every
   existing calc (RECORD only if it was actually checked).
3. Never use `--allow-version-mismatch` for a job deliverable.

### B. Kickoff and folder (W00-W02)
4. Confirm the reviewing agency (City vs County) from the parcel record and the contract before drafting (HJR-C19);
   record the basis in Kickoff. Jurisdiction rules override this skill; load the `drainage-report-build` add-on.
5. Build the report folder with `make_report_folder.py` (command in `reference/governance_and_kickoff.md`), then add
   `30_Report\Issued\` beside `50_Correspondence\` and `00_Admin\DECISION_REGISTER.md` (D56, QC-C05; v0.3 does not
   create them). Dates in every folder and file name are YYYYMMDD (D56).
6. Fill Kickoff and Setup (S-01, S-03, S-04, S-06 flags, then the rest). Where the agency has a standard report
   outline (City of Tucson), its section list governs: keep every section and write "Intentionally left blank"
   with the reason where nothing applies; split existing conditions into hydrology and existing stormwater
   infrastructure (HJR-C19). In v0.3 do this with Narrative VERBATIM rows per section.
7. Set Setup S-36 to chapter-based numbering before any figure is rendered; figures and tables are numbered by
   section (Figure 4-1) (D52). Exhibit files `Fig<sec>-<n>_<Title>_<YYYYMMDD>.pdf`.
8. Plan: write `00_Admin\COORDINATION_PLAN.md` per the spec and seed CalcRegister / Narrative / ExhibitRegister
   (procedure and rules in `reference/governance_and_kickoff.md`). Stop for JCO approval of the plan.
9. Concept reports (channels with multi-use paths crossing roads, freeways or railroads; sites crossed by a large
   offsite wash) - put in the introduction, not deep in the body (HYD-C27):
   - whether the path is continuous under major crossings (freeway, railroad) or ends at them, and the crossing type
     at each road (at grade, under, con-arch);
   - for each existing crossing structure: stays, adequate, or replaced;
   - offsite conveyance alternatives with the count of road crossings for each; prefer one consolidated crossing;
     compare culvert cells for 10-yr vs 100-yr capacity;
   - alternatives note bank-protection options (e.g. geosynthetics on 4:1 vegetated slopes), precast vs
     cast-in-place culvert extensions, basin or spreader options at overchutes, terraced channel option (10-yr
     low-flow channel, 100-yr terrace outside sensitive areas);
   - flow paths described in downstream order;
   - written client decisions on level of protection (100-yr vs 500-yr), onsite containment and acceptance of
     controlled flooding; a designed overflow onto the site needs agency agreement;
   - grates/bar racks at fence crossings checked for headloss and debris; next deliverables listed after decisions.

### C. Governance during the work (W03-W05)
10. The ask creates the row: add the WORKING row before opening software. Work only in
    `20_Working\<Initials>_<YYYYMMDD>_<Topic>\`. Promote with `promote_calc.py` (OPTION, or RECORD with checker
    initials). Actions PROMOTE / CASCADE / QC-TABLE / RECONCILE / PRECHECK: `reference/governance_and_kickoff.md`.
11. Decision register (QC-C05): when two values exist for one feature (design flow, structure size, basis) across
    tables, workbook and plans, list each with source, method and where used; classify isolated vs propagating;
    resolve isolated, evidence-backed ones and log them; ask JCO propagating ones one at a time (problem, options,
    consequences, plan/profile image). No table edit until decided. Once decided, update narrative, tables, exhibit
    labels, HY-8 and protection sizing together; keep each native run. Log in `00_Admin\DECISION_REGISTER.md`.
12. Design discharge traceability (HJR-C10): define regional and local storms and their peaks once in existing
    conditions and use the qualifier with every reference (10-yr regional, 100-yr local), no synonyms; keep a design
    discharge table (source cross section or culvert record ID, location, Q10, Q100, governing duration, use:
    crossing vs parallel flow); use only the jurisdiction's design recurrence intervals; restate the basis in the
    design section with the same wording and numbers; check every caption and table title against the storm of the
    values shown; summary flow = flow used to size the structure; allowable velocity is the velocity permitted over a
    lining or soil. v0.3 has no T-HYD-10 block: keep the table as T-HYD-04 rows plus a Narrative VERBATIM table
    lead-in, or in 40_QC as the check list.
13. Appendix calc rules (HYD-C26, D16, D38, D30, EXH-C13):
    - once plans show a selected design, run that design (size, count, inverts, length from plans, project-datum
      inverts, not an arbitrary 100 ft datum) and insert native output; drop option-comparison tables. Options still
      open: native sheets for each option, not only a summary;
    - licensed set (D16, default, to confirm): FHWA Hydraulic Toolbox, HY-8, Civil 3D hydraulic tools, HEC-RAS,
      HEC-HMS, FLO-2D, PC-Hydro. FlowMaster and CulvertMaster are legacy: reproduce legacy calcs in Toolbox / HY-8;
    - no new spreadsheet a reviewer must check; independent checks stay in 40_QC (D30);
    - print areas set so every output sheet plots on one page;
    - native output always in the appendix; an extracted or compact sheet may be added, titled "extracted summary",
      every value traced to the native file (D38);
    - Hydraulic Toolbox inlets: do not tick Add Profile; keep the native Word export as evidence; compact one-inlet
      page filled only from saved .hyd values; where the export prints longitudinal slope 0.0000, show the saved slope
      with a note that the native export misprints it; check every compact page visually.
14. Fill table blocks from RECORD printouts only; units in headers; one software version per analysis per cycle.

### D. Recalculate (D51)
15. Every time a script wrote to the workbook (and before any assembly):
    `"%DOCS_PY%" "%SK%\xl_recalc.py" recalc --workbook "<wb>" --keep-copy "<wb>.pre_recalc.xlsx" --json "<..>\40_QC\recalc_<YYYYMMDD>.json"`
    Private Excel instance, events and link updates off, CalculateFullRebuild, then semantic compare. Require zero
    formula or input changes, zero new formula errors, and CalcRegister row-3 counters / Manifest J4 equal to what
    Excel shows. Work on an isolated workbook copy when testing; write only explicit input cells. Do not use the
    v0.3 `xl_recalc.ps1` (D12). LibreOffice recalc is a fallback only; flag it.

### E. Assemble (W06)
16. Run to a new dated file (issued drafts are never overwritten):
    ```
    "%DOCS_PY%" "<STANDARD>\standard\assemble_report.py" ^
      --workbook "<..>\00_Admin\<Job>_<ReportID>_Workbook.xlsx" ^
      --template "<STANDARD>\Psomas_Drainage_Report_TEMPLATE.docx" ^
      --out "<..>\30_Report\Drafts\<Job>_<ReportID>_<Milestone>_<YYYYMMDD>_DRAFT.docx"
    ```
    `VERSION GATE FAILED` -> stop and report.
17. Read `_ASSEMBLY_REPORT.md`:
    - s1 must show OK version gate, OK verbatim narrative present unchanged, OK no engineer notes / context-only text
      printed. FAIL on CalcRegister (duplicate RECORD, RECORD without checker) blocks issue.
    - Issue gate (QC-C04; v0.4 CS-04 automates it): QC_Log Tier 1 answered > 0; CalcRegister populated for a design
      report; zero unregistered figures (every `[FIGURE:F-nn]` has an ExhibitRegister row); s3 VERIFY citations
      checked (prior study citation, current ADEQ CGP edition); a table referenced in two sections has one owner.
    - s5 unresolved placeholders -> list for the engineer; they stay yellow in Word (D44).
    - s9 human decisions grouped: governance first (duplicate RECORD, RECORD without checker, table rows citing
      non-RECORD calcs, narrative on excluded sections, ReportText withheld), then Manifest, text, data, derivations.
    - s10a rewrites: fill `proposed` in `_REWRITES.json` for each item (same numbers, names, cited standards; section
      tone; no new facts); show original -> proposed; record Accept / Revert / Edit (`final`); then
      `"%DOCS_PY%" "<STANDARD>\standard\apply_rewrites.py" --docx <draft> --rewrites <..>\_REWRITES.json`.
      Accepted wording that should persist goes back into the Narrative cell as VERBATIM. Not reviewable until s10a
      is empty.
    - s11 = calculation-of-record list for the transmittal.
18. Open items (D44): one internal QC open-items document in 40_QC (prerequisites table: jurisdiction, plans match
    analysis, T2 check, seal, waivers, open items; numbered open items typed geotechnical / final design / waiver /
    approval / JCO decision / submittal; native-vs-report calc cross-check table; standards checklist with status and
    location, deviations called out; empty markup response log). Every assembly WARN, unresolved placeholder and
    human decision is closed or listed there. Checklist status uses Addressed / Partial / Assumed / Not Addressed /
    Cannot Determine / Stale (D45); rows resting on lidar culvert data, assumed bridge geometry, unknown layout or
    unconfirmed calibration are Partial or Assumed. Deviations from the Standard (tool version, exhibit method,
    missing template) are listed as JCO decisions. Deliverables read in completed tense; the open-items document is
    never transmitted.

### F. Post-process the DOCX
19. ```
    "%DOCS_PY%" "%SK%\postprocess_docx.py" --docx <draft.docx> --fix --out <draft>_PP.docx --preparer "Psomas (JCO)" --json <..>\40_QC\postprocess_<YYYYMMDD>.json
    ```
    Sets author / last-modified-by to the firm string, clears comments/keywords/subject, drops template custom
    properties, removes DATE fields from headers and footers. It lists, and never deletes, placeholders, leftover
    `[FIGURE:]` / `[TABLE:]` / `[LIB:]` slots and rewrite tags (D44: placeholders stay flagged until the assembly
    report shows them closed). Remove template paragraphs that do not apply and slots of excluded sections by hand
    or by regenerating; set cover office address and project number in Setup and regenerate.
20. Fix every finding at its source (workbook, Narrative, template), regenerate, and re-run. Tables: thin borders on
    all cells, header row in the template header style, no alternating shading (D47, default, to confirm); one
    caption per table above it, numbered by section, no second title inside the table; header row repeats; cells
    centered; portrait and full width (drop constant columns and note them); native Word tables, never screenshots;
    elevations 2 decimals without thousands separator, discharges whole cfs, one precision per column; each table
    introduced by a "presented in Table n" sentence; fit to one page where possible (RPT-C06).
    Page breaks only before main sections and appendices; template styles for headings and spacing, no manual
    returns; references numbered 1), 2) with real sources only; directions abbreviated with a period (S.) or road
    names written out, one convention; no dates in footers; fix TOC tab alignment and stray characters (pull a fresh
    template if unsure); cover carries a project site photo, preferably from the field visit (RPT-C06).
21. Figures embedded in the docx are downsampled to 200-300 dpi at print size before insertion.

### G. Word export
22. ```
    "%DOCS_PY%" "%SK%\word_export.py" --docx <draft>_PP.docx --pdf <..>\30_Report\Drafts\<name>.pdf --email-pdf <..>\<name>_email.pdf
    ```
    Separate Word instance; fields, TOC and tables of figures updated twice; PDF with heading bookmarks. Then
    confirm no paragraph lacks a named style and every Table/Figure number resolved (LibreOffice previews show
    "Table Introduction-1" where Word shows "Table 1-1": judge captions in Word).
23. Render every page and look at each one (`pdftoppm -r 45 -png <pdf> <prefix>`, contact sheets 5x2) before
    issue: cover on one page, footer not on 11x17 figure pages, no large white areas, no orphaned headings.

### H. Compile the bookmarked PDF (W09)
24. Write `30_Report\compile_manifest.json` (format in the script docstring) from the newest editable source and its
    fresh Word export: body split at the end of each main section with that section's 11x17 figures inserted, one
    divider per appendix and per plan set or study, native output (PC-Hydro printouts and hydrographs per CP, HEC-HMS
    output, Atlas 14 PFDS printout, HY-8 report, RAS computation summaries, FIS/LOMR/dam-safety pages), landscape
    pages rotated. Never hardcode page numbers in prose.
25. Prepare sources: highlight the relevant Q values in reference studies; replace table numbers on images with markup
    matching size, font and color; flatten author markups in the PDF reader (originals kept); third-party FreeText
    (e.g. LOMR pages) flattened or noted; inherited plan revision clouds removed from the compiled copy, original
    marked PDFs kept (D48).
26. ```
    "%DOCS_PY%" "%SK%\compile_pdf.py" build --manifest <..>\30_Report\compile_manifest.json --split
    ```
    Required bookmarks (D52, default, to confirm): cover, TOC, each main section, each appendix, each exhibit; children
    sorted by page. Checks: every bookmark and link target resolves, links dropped by the compile fail, page-by-page
    source comparison in the QA JSON (keep it in 40_QC), near-blank pages, size against S-35.1 / the agency limit
    (D52: 50 MB per file or the agency limit if lower; over -> compress, then split at top-level bookmarks; keep a
    reduced copy for transfer).
27. Placeholder pages only for named future items, labelled with the item; no blank areas in the body; remove
    unneeded pages, unrequested appendices and review-draft wording (D50).
28. Final interactive check of bookmarks and links in a native PDF reader (Bluebeam), not a browser viewer.
29. A pending model rerun: hand the watcher (wait for the new HDF, regenerate results and figures, recompile, copy to
    10_Record) to `model-run-supervisor`.

### I. Issue (W10) and after
30. Gate: open-items document empty, or JCO authorization recorded and the unresolved items listed in a separate
    internal document (D44); PRECHECK pass; RevisionLog row for the milestone; T1 complete, then T2 and T3.
31. Issued set in `30_Report\Issued\<YYYYMMDD>_<Milestone>\` with RECORD_SET.md (final PDF, frozen docx, transmittal).
    Handover package -> `delivery-package-build` (into 30_Report/Issued). Comments back -> `agency-comment-response`.
32. Design change after issue: log it in REVISION_LOG.md with affected letters, figures, tables and sections; CASCADE
    for hydrology changes; re-run in a new 20_Working folder; promote; regenerate to a new dated draft; compare old vs
    new drafts (Word Compare or `pandoc -t markdown` + diff) and the two assembly reports; T2 reopens for changed
    letters, T3 for changed sections; recompile.
33. Text that belongs in every future report goes into the library JSON (v0.4 release work), never into one .docx;
    project prose goes into Narrative or CalcRegister ReportText so regeneration reproduces it.

### J. End-to-end rerun of a job (DSO-C14)
34. Parameterize the project root and job work folder in every script (one parameter file); grep for absolute paths
    before a rerun - none outside the parameter file. Scripts write `.log` and `.err`; dated scripts folder
    `20_Working\<Initials>_<YYYYMMDD>_scripts\` (D56 replaces 99_Working).
35. Prerequisites: .hy8 writer module, minimal HMS template project, Report_Template_7 and memo template paths, pinned
    ras_commander, pywinauto, HY-8 8.00, HEC-HMS 4.13 (D01), HEC-RAS 6.6 (D02). Fix known blocking items from the
    prior run first.
36. Run order: due diligence; data/GIS (DEM, subbasins, culverts, terrain compare, crossings, inventory); hydrology
    (HMS build/runs, PC-Hydro, routing); 1D/2D runs in a separate agent; HY-8; alternatives; exhibits; report
    (recalc, assemble, post-process, Word export, contact sheets); compile; record copy. FLO-2D and HEC-RAS in
    parallel on separate core sets (D06 limits on EKOS).
37. Budget wall time: about 6.5 h for a one-session preliminary report; about 48 h minimum for a full 2D pilot,
    governed by HEC-RAS (10 plans about 43 h sequential on 12 cores); report build about 3 min per rebuild.
38. Every edit script is idempotent: back up first, check whether an insert already exists, assert counts before
    writing. After a JCO change edit the builder inputs first; do not run stale downstream builders.

## Jurisdiction add-ons
- Load `get_skill("drainage-report-build", resource="addons/<file>.md")` for the reviewing agency before step 6.
- `addons/city-of-tucson.md`: City manual outline is the section list (HJR-C19).
- `addons/town-of-marana.md`: concept reports explain trail termination or the crossing at I-10/UPRR (HYD-C27);
  regional vs local terminology per MDM 4.1 (HJR-C10, D24).
- `addons/town-of-sahuarita.md` / `addons/pima-county-rfcd.md`: a designed overflow onto the site conflicts with
  matching existing peak Q and floodplain at the property boundary (HYD-C27); 10-yr and 100-yr are the design events
  (HJR-C10).
- `addons/fema.md`: TDN behaviour via S-02.

## Gotchas
- openpyxl reads stale values for formula cells unless the workbook was recalculated and saved by Excel (SAH-012).
- A library-written workbook showed a COUNTIF wildcard counter of -14 status issues; native recalc gave 0 with no
  formula change (EKOS-LOCAL-018).
- Native Excel merges adjacent validation ranges and drops default styles; compare semantics, not raw XML
  (EKOS-LOCAL-018).
- Learning the workbook layout took four inspection passes plus manifest and library dumps; keep a named-range map per
  Standard version (SAH-012).
- Compiled PDF was 23.8 MB; a 3.4 MB compressed copy was needed for transfer (SAH-012).
- Figures first numbered 1-7, then renumbered by section, so every exhibit was rendered twice (CALFIRE-013).
- The memo template ships its own core.xml and duplicated parts (CALFIRE-013).
- TOC level-2 tab leader missing in the template on short entries (CALFIRE-013).
- Cover office address and project number were placeholders (CALFIRE-013).
- Generated DOCX was 49-56 MB with 12 full-resolution images; some paragraphs had no style and python-docx failed on
  them; Word cleanup took 46 saves over about 1.6 h on submittal day (TANGERINE-011).
- Issued 96-page PDF and all three exhibit PDFs had no bookmarks (TANGERINE-011, TANGERINE-016).
- First template pass pushed the cover to 2 pages and ran the footer across the 11x17 figure page (VALENCIA-009).
- An integration script wrote the body then failed an assertion; rerunning would duplicate a paragraph - fix and
  resume (VALENCIA-009).
- Compact output used pageBreakBefore, not w:br; grouping logic must handle both (VALENCIA-009).
- All four reports of one program were first built in a generic layout and restructured with one-time patches, about
  1.25 h rework; build to the standard from the first draft (RKN-014).
- Table with green highlights, mixed elevation decimals and a table name not matching the caption (SAHPARK-004).
- A screenshot of an Excel table plotted poorly; tables are native Word tables (SAHPARK-004).
- A short appendix table ran onto a second page (SAHPARK-004).
- Excessive and inconsistent spacing between sections; a large blank area on one page (SAHPARK-005, TANGERINE-018).
- Table mismatch flagged twice, extra space three times, a stray bracket and footer dates in one draft (TANGERINE-018).
- Appendix bookmark order wrong (Table A-2 on p. 26 listed after Table A-1 on p. 27) (CALFIRE-014).
- Source LOMR pages bring FreeText annotations into the compiled PDF (CALFIRE-014).
- A report link did not work in the reviewed draft (CAMPBELL-020).
- Source PDFs raise pypdf "Multiple definitions for key /PageMode" warnings; harmless (RKN-015).
- Compiled PDFs reached 55-86 MB and 700 MB-1 GB (RKN-015, VALENCIA-008).
- Revision cloud annotations vanished in merged plan pages; 39 sheets had to be re-rendered (VALENCIA-008).
- The final report must not carry plan revision clouds (VALENCIA-008).
- The editable Word body held corrections that never reached its PDF; compile from the newest source and its fresh
  export (VALENCIA-008).
- Browser-based reader checks failed under computer-use URL policy; use a native PDF reader (VALENCIA-008).
- Deviations from the Standard (HEC-HMS 4.13 vs 4.12, Python exhibits vs QGIS, missing brand template) must be listed
  as JCO decisions, not buried (RKN-018).
- All 21 checklist rows were marked Addressed while the open-items memo listed 13 items, including culvert
  size/inverts, bridge low chord and new impervious area that drive those rows (CALFIRE-016).
- A 30% draft went out with QC_Log 0/27, CalcRegister empty, 6 unresolved placeholders (seal PE number, prior study
  fields) and F-06/F-08 unregistered (SAH-013).
- The assembler flagged library id PROJECT-TEXT not found and treats PROJECT-TEXT as one entry per report (later
  sections duplicate); put project text through the Narrative sheet until CS-03 ships (SAH-013).
- The s60 post-process deleted leftover placeholder paragraphs, hiding open items in the docx; keep them listed in the
  assembly report (SAH-013).
- An agent team changed a design flow from 886.6 to 823.1 cfs; JCO reversed it: 886.6 cfs is the larger area routed to
  the crossing (CAMPBELL-014).
- One structure (D1) changed three times (3 arches, 2-18 in pipes, 2-24 in pipes); keep each native run and the final
  decision (VALENCIA-011).
- JCO wanted downstream flows to match the updated pavement drainage maps, not recomputed totals (VALENCIA-011).
- Do not call an odd size a typo without evidence; 18x11 in is a standard concrete arch (VALENCIA-011).
- Do not put JCO working assumptions (e.g. utility conflicts mitigated) in report text unless told (VALENCIA-011).
- A draft appendix had only an options summary table on an arbitrary datum while the plans already showed a
  3 - 10x4 ft RCBC (SAHPARK-012).
- Custom normal-depth spreadsheets with an undocumented geometry sketch added review time and were removed
  (SAHPARK-013).
- FHWA Hydraulic Toolbox 5.5 native Word export prints longitudinal slope 0.0000 although the saved input and dialog
  have a nonzero slope; reproducible across 110 cases (VALENCIA-002).
- Raw Toolbox output took 2 pages per inlet; reformatting in Word from native values was accepted by JCO
  (VALENCIA-002).
- The reviewer read 41 of 48 pages before learning the path was claimed continuous under I-10 and UPRR; Development
  Engineering asked for the trail to stop at I-10 or explain the crossing (BARNETT-011).
- A designed overflow onto the site creates a second floodplain path and conflicts with matching existing peak Q and
  floodplain at the property boundary; needs Town and PCRFCD buy-in (PHXZOO-005).
- Double chain-link fencing passes stormwater freely, which removed the pipe-escape concern only because no pipes leave
  the enclosures (PHXZOO-005).
- The design-basis summary sentence in a 30% DCR reintroduced the ambiguity flagged earlier even though definitions
  existed (BARNETT-006).
- One flow quoted as 4,324 cfs and 4,325 cfs in different places (BARNETT-006).
- A draft labeled a 100-yr value as 200-yr; the source study has no 200-yr flows (SAHPARK-003).
- An inflow map captioned 10-yr showed 100-yr rates (SAHPARK-003).
- Missing table referenced in hydrology text (SAHPARK-003).
- Approach flow (2,673 cfs) quoted as the crossing flow when the culvert was sized for 534 cfs (SAHPARK-003).
- A prior report stated the 500-yr basis two ways (NORTHLOOP-010).
- A draft did not follow the City outline; restructure requested and all City sections required even when empty
  (TANGERINE-017).
- Jurisdiction unclear (City vs County); a second reviewer noted contracts and the parcel map point to County
  (TANGERINE-017).
- Scripts held hard paths to another project folder and to Python 3.12 site-packages; all scripts hard-coded the
  OneDrive job folder and the D: work folder (CALFIRE-018, SAH-018).
- Model runs and web services are the waits (CALFIRE-018).
- The original pilot run used about 25 h of continuous agent time plus 43 h of RAS queue (SAH-018).
- Fix SAH-002, SAH-003, SAH-006 and SAH-015 items first or the same reruns repeat (SAH-018).
- Recorded run times (FLO-2D UPPER + LOWER, h): 3-hr 100-yr 0.63 + 0.82; 24-hr 100-yr 1.86 + 2.91; 3-hr NoBerm
  0.34 + 0.69; 24-hr NoBerm 1.09 + 3.54; 3-hr NoBerm MineFill 0.33 + 0.69; other frequencies est. 1.5 h per pair;
  HMS 50 runs about 40 min; PC-Hydro 67 subbasins 25 min; report build about 3 min (SAH-018).
- First delivery package used a non-standard folder name and missed printouts/QC; rebuilt two hours later
  (RKN-019) - see `delivery-package-build`.
- Download links failed on the phone and email was not set up; OneDrive on the phone worked (CAMPBELL-023).

## QC checks
- Pull rules: `get_qc_rules('report-text')`, `get_qc_rules('tables')`, `get_qc_rules('appendix')`,
  `get_qc_rules('package')`, `get_qc_rules('exhibits')`, plus the jurisdiction tag (`pima-rfcd`, `tucson`,
  `marana`, `sahuarita`, `fema`, `placer`, `caltrans`).
- Recalc: zero new formula errors; register counters match Excel (EKOS-LOCAL-018).
- Assembly: s1 OK lines; issue gate (T1 > 0, CalcRegister populated, zero unregistered figures, VERIFY cited); s10a
  empty; open-items document empty or JCO authorization recorded.
- DOCX: no unstyled paragraphs; no leftover slots in included sections; no DATE fields in footers; properties set to
  the firm; no tool or assistant names; tables thin-bordered without banding (SAH-012, TANGERINE-011, CALFIRE-013).
- Every page rendered and viewed (SAH-012, CALFIRE-013, VALENCIA-009).
- Compiled PDF: minimum bookmark set present and ordered by page; every bookmark and link resolves; QA JSON page
  comparison clean; no revision clouds, no review-draft wording, no unflattened stray annotations; size under the
  agency limit (TANGERINE-016, CAMPBELL-020, CALFIRE-014, VALENCIA-008, RKN-015).
- Every Q in text, tables and captions matches the design discharge table (value, event, duration, source); no
  recurrence interval outside the jurisdiction design set unless stated as a sensitivity (HJR-C10).
- No change to a design flow or structure size in tables without a decision-register entry; decided values identical
  across narrative, tables, exhibits, HY-8 and protection sizing (QC-C05).
- Section list matches the agency outline one to one where one exists (HJR-C19).
- Appendix: native output for the selected design; extracted summaries labelled and traced; Toolbox slope note where
  the export shows 0.0000; 100% compact-page visual check logged (HYD-C26, EXH-C13).
- Rerun: grep for absolute paths before a rerun; none outside the parameter file (DSO-C14).

## Change log
- 0.4.0 2026-10-22: new master built from clusters QC-C04, QC-C05, RPT-C01, RPT-C06, RPT-C10, HYD-C26, HYD-C27,
  HJR-C10, HJR-C19, DSO-C14, DSO-C31, EXH-C13 and the v0.3 package skills/procedure; decisions D16, D44, D45, D47,
  D48, D50, D51, D52, D56 (plus D01, D02, D06, D11, D12, D30, D38 where cited). Items marked "default, to confirm":
  D16 licensed tool list, D47 table shading, D52 size target and bookmark set. Added library helpers xl_recalc.py,
  postprocess_docx.py, word_export.py, compile_pdf.py (compile_pdf and postprocess tested on sample files; recalc
  and Word export need Windows + Office). Added reference/v0.4_change_spec.md (CS-00..CS-20). Package code remains
  v0.3.0 until Phase 5. Old package skills folded in: kickoff, governance actions, assembly checklist; the reviewing-engineer role reads JCO.
