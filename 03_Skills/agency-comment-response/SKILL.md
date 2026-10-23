---
name: agency-comment-response
description: Log, reconcile and answer review comments (agency, JCO redlines, internal or mock review) on a drainage report, DCR, memo or plan set - one matrix, stable IDs, D45 status and disposition, completed-tense responses tied to displayed section/table/figure numbers, and pre-issue checks.
version: 1.0.0
status: active
function: qc
jurisdiction: all
tools_versions: "Python 3.10+ with pypdf, openpyxl; Bluebeam or Acrobat for markups"
owner: JCO
replaces: "none (new; covers W11 comment cycle of the Standard and the response-log bullets of drainage-report-build)"
---
# Agency Comment Response

## When to use
- Agency review comments or internal QC redlines arrive on a DCR, drainage report, memo or plan set.
- Before any resubmittal (15/30/60/90%) and at the internal QA/QC checkpoint before each submittal.
- An owner says prior comments look unaddressed, or a sub-consultant says its work was left out.
- A mock review (from qc-reviewer) needs a merged findings log.

## Inputs
- Every comment source: agency letter, agency xlsx (every tab and division), reviewer summary lists, marked PDFs
  (Bluebeam/Acrobat), portal exports, prior response matrix.
- The current build (docx and its Word-exported PDF) and the Standard workbook if the job uses it.
- Folder: `50_Correspondence\<YYYYMMDD>_<Agency>_<Milestone>\` holds the originals unrenamed; the log is
  `<Job>_<ReportID>_CommentResponse_<YYYYMMDD>.xlsx` in the same folder.
- `%DOCS_PY%` = documents venv interpreter by full path (D11); `%SK%` = this skill's `scripts\` folder.

## Status vocabulary (D45)
- Status: Addressed / Partial / Assumed / Not Addressed / Cannot Determine / Stale.
  Stale = agency text repeated from a prior letter that the current files disprove.
- Disposition (separate field): incorporated / superseded / no change. Blank is not an acceptable disposition.
- Status and remaining actions are internal tracking (D44). The transmitted response reads as done.

## Steps
1. The day comments arrive, file the originals unrenamed in 50_Correspondence and log every comment in one matrix:
   all agency divisions (each tab of the agency xlsx), reviewer summary lists and PDF markups.
2. Extract PDF annotations:
   `"%DOCS_PY%" "%SK%\crl_tools.py" extract --pdf <marked.pdf> --csv <..>\J_markups.csv --prefix J`
   (page, author, subject, subtype, contents; links, popups, text-box labels and plain shapes without text are
   dropped). Check the native PDF for figure legibility, legends and graphic vintage; a text-only export cannot show
   them (mark those Cannot Determine until checked).
3. Build the log:
   `"%DOCS_PY%" "%SK%\crl_tools.py" new-log --out <..>\<Job>_<ReportID>_CommentResponse_<YYYYMMDD>.xlsx --source R=<agency.xlsx> --source J=<..>\J_markups.csv`
   List every comment ID from every source first; record the count per source (Sources sheet). Keep original comment
   text, number, sheet and prior response unchanged. IDs are stable and source-prefixed (R-DRA-1, J-01, M-1); a
   merged mock review keeps the set prefix so IDs cannot collide.
4. Triage: mark Discipline (keep drainage; other disciplines such as landscape are marked "other discipline" and not
   answered here); tag substantive vs copyedit and sort punctuation edits out before counting; Category (missing
   content, technical error, engineering content, exhibits, formatting, methodology, editorial); summarize counts by
   category.
5. Columns to fill per comment: Response, Revised location (new section/table/figure/appendix as displayed), Action,
   Completed by, Check by, Status, Disposition, Evidence (file + page). One response per comment, tied to that comment
   only; cross-reference other responses by ID. Do not merge two topics into one response.
6. Write responses in completed tense ("has been revised", "has been added"), never "will" and never "will comply".
   Each response states what was done and where: section, table, figure and appendix numbers as displayed in the
   current build.
7. Agency directions and contradictory comments (e.g. initial vs later comments: remove an exhibit vs keep and label
   it) go to the Decisions sheet as JCO decisions so later passes do not undo them. Ask JCO for missing responses
   before final compilation.
8. Before the next submittal, search the issued text for the wording and topic of each comment and set Status with
   page or section evidence. Search the whole report for the same term or claim: a fix in one section must reach
   related sections written by other authors.
9. Sub-consultant input: compare batches by date and file size (draft vs final) with what the report contains; flag
   empty exhibit placeholders and claims such as "complete results incorporated in Section X".
10. Output for JCO: the draft response matrix plus a prioritized remediation list (concept-affecting first, copyedit
    last). Log variances found during a rewrite separately (unrealized assumptions, criteria not applied, undersized
    easement, sediment, scour) as open items in the internal QC open-items document (D44), not in the response.
11. Size the rewrite to the deliverable before expanding it (a 4-page issue does not need a 90k-character rebuild).
    When redlines are structural (dozens of comments on a short draft), rebuild the section from sources rather than
    patching sentences.
12. Rebuild responses after every calc change (grate counts, flows, structure sizes go stale).
13. Pre-issue check:
    `"%DOCS_PY%" "%SK%\crl_tools.py" check --log <log.xlsx> --pdf <current build.pdf> --issue --json <..>\40_QC\crl_check_<YYYYMMDD>.json`
    Fix every finding: ID count = source count, no duplicates, no blank Status/Disposition/Completed by/Check by,
    no "will", no placeholders (?, TBD, XX, TBC, [ ]), vocabulary per D45, every cited section/table/figure number
    present in the current build. Set the memo or letter date at issue.
14. Placement (D49): the log is an editable separate deliverable; a bound copy goes behind the cover of the
    resubmitted report where the agency asks for it (Pima County RFCD add-on). If the report says a response matrix is
    in an appendix, confirm the appendix is in the package before issue.
15. Transmitted copy: turn off markups on included comment forms; Status, remaining actions and internal notes are not
    in the transmitted matrix (D44). Internal redline logs (JCO markups, mock reviews) are internal quality records
    and are never transmitted.
16. Copy JCO's marked-up PDF to `40_QC\` (T3 review folder) as `<Job>_<ReportID>_<Milestone>_<YYYYMMDD>_DRAFT_Markup.pdf`
    and log a row for every comment the same way.

## Jurisdiction add-ons
- `addons/pima-county-rfcd.md` (this skill): RFCD / Pima County DOT comment forms, bound copy behind the cover.
- Placement, outline and criteria rules of the reviewing agency: `get_skill("drainage-report-build",
  resource="addons/<agency>.md")`.

## Gotchas
- A text-only export strips images, so figure legibility, legends and graphic vintage cannot be verified; mark those
  Cannot Determine and check the native file (BARNETT-001).
- Reviewer markups were about 50% punctuation edits; sort them out before counting or the log is unreadable
  (BARNETT-001).
- Fixes made in one section were not carried to related sections written by other authors; search the whole report
  for the same term or claim (BARNETT-001).
- A 15% DCR log had about 104 comment rows across four divisions with Action/Completed/Check blank; the 30% DCR still
  claimed an appendix matrix that was not in the files, and the owner reported comments as undocumented (BARNETT-002).
- 48 JCO comments on a 24-page draft were structural; Rev A was rebuilt from sources rather than edited (SAHPARK-017).
- The Rev A rewrite grew to about 90k characters and 20 tables while the 30% issue was a 4-page Rev B; size the rewrite
  to the deliverable before expanding (SAHPARK-017).
- Commingled-flow text for one comment was merged into the railroad response; JCO had it split back (CAMPBELL-015).
- Draft responses said "will"; JCO required all to read as done. Prior responses said "will comply" (CAMPBELL-015,
  VALENCIA-007).
- Stale response text (grate count, flows, D1 size) found twice after calc changes (VALENCIA-007).
- The agency asked to omit an extra FEMA floodplain comparison; record the direction (VALENCIA-007).
- Initial vs later RFCD comments conflicted (remove exhibit vs keep and label) (VALENCIA-007).
- The matrix omitted whole comment sets from the second review (Town, landowner agency, county flood control, public)
  (TANGERINE-002).
- Placeholder reference (T1-?) left in the remaining-items table (TANGERINE-002).
- Memo date read June 2026 while later files were October (TANGERINE-002).
- ID collision in a merged mock review: set A used A-1..A-3 for agency comments while set B used A-1..A-4 for the
  landowner-agency reviewer; prefix IDs by source set before merging (TANGERINE-001).

## QC checks
- Pull rules: `get_qc_rules('comment-response')`, `get_qc_rules('report-text')`, plus the agency tag (`pima-rfcd`,
  `tucson`, `marana`, `sahuarita`, `fema`, `placer`, `caltrans`).
- Comment ID count in the matrix = count in the source files (TANGERINE-002).
- Every comment row has Status, Disposition, Completed by and Check by before issue (BARNETT-002).
- No "will" in responses; responses state what was done with revised location (CAMPBELL-015, VALENCIA-007).
- Every cited section/table/figure number resolves to the displayed number in the current build (CAMPBELL-015).
- Appendix matrix referenced in the text exists in the package (BARNETT-002).
- No placeholder (TBC, TO BE CONFIRMED, ?, [ ]) in any transmitted response (TANGERINE-002).
- Transmitted matrix carries no internal status columns or open items (D44).

## Change log
- 1.0.0 2026-10-22: built from clusters QC-C03 and RPT-C05 (plus the TANGERINE-001 ID-prefix gotcha from QC-C02);
  decisions D44 (completed tense, open items internal), D45 (status vs disposition), D49 (separate editable log plus
  bound copy where the agency asks). RPT-C05 status list Incorporated / Partial / Deferred replaced by D45. Added
  scripts/crl_tools.py (extract, new-log, check; tested on sample PDF/xlsx). No items marked default, to confirm.
