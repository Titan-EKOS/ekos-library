# RPT clusters - report assembly (30 cards) + compile PDF (10 cards)

Groups: group_report-assembly.json, group_compile-pdf.json. 40 cards, 15 clusters.
Score = sum(hours_lost x recurrence). Source tags: "claude" = harvested from a Claude session; "claude via Codex session" = Codex transcript cited as evidence; "EOR redline" = card built from EOR QC markup comments (recurrence on these cards usually counts individual redline comments).
Backbone for this group: Standard v0.3 chain = workbook (Excel recalc) -> assemble_report.py -> post-process -> Word export (fields/TOC) -> compiled bookmarked PDF -> delivery package.

---

### RPT-C01 Scripted report build on the Psomas template and Standard v0.3 chain
skill | target: drainage-report-build (update sec. 3 "Native model runs and tooling" with a "Build chain" subsection) + Standard v0.3 change (assemble.cmd recalc step, post-process step, named-range map) | score 24.5 | hours 8.8 | cards 5 | projects 5 | confidence high

Trigger: Model results must become the standard workbook, a draft DOCX on the firm template and a check PDF; rerun after every new selected alternative, EOR change or calc change.

Steps (merged):
1. Work on an isolated copy of the standard workbook; write only explicit input cells; keep the original admin workbook unchanged. (EKOS-LOCAL-018)
2. Recalculate natively before anything reads formula cells: private Excel instance (DispatchEx, Visible False, events/macros/link updates off), CalculateFullRebuild, save, close only that instance. In the Standard chain this is xl_recalc.ps1 inside assemble.cmd, before assemble_report.py. (EKOS-LOCAL-018, SAH-012, CALFIRE-013)
3. Reopen and compare semantically (unchanged cells, formulas, names, merged ranges, validation, panes, visible styles); require zero new formula errors and correct register counters. (EKOS-LOCAL-018)
4. Keep a map of workbook named ranges per Standard version so the layout does not have to be rediscovered. (SAH-012)
5. Generate the body into the current firm template (Report_Template_7.dotx copied to .docx with the main content type swapped in [Content_Types].xml; keep sectPr; strip sample body) so every paragraph carries a named style (headings, body, captions). Keep a pre-template content snapshot when re-applying a template from a reference DOCX (cover, theme, headings, footer, table style). (CALFIRE-013, TANGERINE-011, VALENCIA-009)
6. Fix the figure/table numbering scheme (e.g. by section, Figure 4-1) before any figure is rendered. (CALFIRE-013)
7. Run the Standard build sequence: structure table, proposed tables, exhibits, narrative (numbers read from result CSVs), workbook curation, assemble.cmd, DOCX post-process, Word export, contact sheets, compile. About 3 min per rebuild. (SAH-012)
8. DOCX post-process: remove template paragraphs that do not apply and leftover [FIGURE:]/[TABLE:] slots; set document properties (firm/preparer, no AI properties); remove DATE fields from footers and template custom properties; set cover office address and project number. (SAH-012, CALFIRE-013, VALENCIA-009)
9. Downsample figures before insertion (200-300 dpi at print size). (TANGERINE-011)
10. Word export in a separate Word instance via COM: update fields, TOC and table of figures twice; check for unstyled paragraphs; export PDF with heading bookmarks; make a reduced copy for email. (SAH-012, CALFIRE-013, VALENCIA-009, TANGERINE-011)
11. Render pages (JPG/PNG or 5x2 contact sheets at 45 dpi) and look at every page before issue. (SAH-012, CALFIRE-013, VALENCIA-009)
12. Make every edit script idempotent: back up first, check whether an insert already exists, assert counts before writing. After an EOR change, edit builder inputs first; do not run stale downstream builders. (VALENCIA-009)

Gotchas:
- openpyxl reads stale values for formula cells unless the workbook was recalculated and saved by Excel. (SAH-012, claude)
- Library-written workbook showed a COUNTIF wildcard counter of -14 status issues; native recalc gave 0 with no formula change. (EKOS-LOCAL-018, claude)
- Native Excel merges adjacent validation ranges and drops default styles; compare semantics, not raw XML. (EKOS-LOCAL-018, claude)
- Learning the workbook layout took four inspection passes plus manifest and library dumps. (SAH-012, claude)
- Compiled PDF was 23.8 MB; a 3.4 MB compressed copy was needed for transfer. (SAH-012, claude)
- Figures first numbered 1-7, then renumbered by section, so every exhibit was rendered twice. (CALFIRE-013, claude)
- Memo template ships its own core.xml and duplicated parts. (CALFIRE-013, claude)
- TOC level-2 tab leader missing in the template on short entries. (CALFIRE-013, claude)
- Cover office address and project number were placeholders. (CALFIRE-013, claude)
- Generated DOCX was 49-56 MB with 12 full-resolution images; some paragraphs had no style and python-docx failed on them; Word cleanup took 46 saves over about 1.6 h on submittal day. (TANGERINE-011, claude)
- Issued 96-page PDF and all three exhibit PDFs had no bookmarks. (TANGERINE-011, claude; also TANGERINE-016 in RPT-C10)
- First template pass pushed the cover to 2 pages and ran the footer across the 11x17 figure page. (VALENCIA-009, claude via Codex session)
- An integration script wrote the body then failed an assertion; rerunning would duplicate a paragraph - fix and resume. (VALENCIA-009, claude via Codex session)
- Compact output used pageBreakBefore, not w:br; grouping logic must handle both. (VALENCIA-009, claude via Codex session)

QC checks:
- Zero new formula errors after recalc; register counters match. (EKOS-LOCAL-018)
- No unstyled paragraphs; no [FIGURE:]/[TABLE:] slots; no DATE fields in footers; doc properties set to firm. (SAH-012, TANGERINE-011, CALFIRE-013)
- Every page rendered and viewed. (SAH-012, CALFIRE-013, VALENCIA-009)

Source cards: SAH-012, CALFIRE-013, VALENCIA-009, EKOS-LOCAL-018, TANGERINE-011

---

### RPT-C02 Report-writer agent: end-to-end report/memo build and update
agent | target: agent report-writer (paired with qc-reviewer); procedure body comes from drainage-report-build + RPT-C01 | score 26.5 | hours 8.5 | cards 2 | projects 2 | confidence high

Trigger: A drainage report, memo or TM must be built from scratch from public data and model output, or updated after new model results or agency comments.

Steps (merged):
1. Read drainage-report-build, drainage-report-exhibit-standards and the project AGENTS.md before writing; load the full report standard (EOR format, scenario switches EX/PR/PR2) into the base scripts from the start. (CAMPBELL-021, RKN-001)
2. Work in a new <Initials>_<date>_<topic> folder in a clean build folder; preserve originals and record hashes. (CAMPBELL-021)
3. Number scripts in run order (01 data, 10-18 hydrology, 19-23 hydraulics, 30-69 site plan, 70-78 reports/QC); log each run to logs\<step>.out/.err; one shared helper module per concern (geometry, maps, docx); a chain runner (.cmd) rebuilds the selected alternative end to end. (RKN-001)
4. Read every report number from model output files; never type numbers into report scripts. (RKN-001; see RPT-C03)
5. Launch long 2D runs (20-32 min each) early; build exhibits and report in parallel. (RKN-001)
6. Use the official report template (headings, TOC, lists, Arial, brand colors, centered tables); update text, tables and exhibit references together; keep a change and assumption register. (CAMPBELL-021)
7. Ask before replacing any existing exhibit. For urgent resubmittals offer replacement pages instead of a full rebuild. (CAMPBELL-021)
8. Export from Word on the host, compile the bookmarked PDF, render every page and look at it. (CAMPBELL-021)
9. Finish with automated QC (native PC-HYDRO vs report cross-check, layout QA, banned-word and metadata checks, no interim wording, no AI marks) and an open-items document before packaging; hand to qc-reviewer. (RKN-001, CAMPBELL-021)
10. Copy to OneDrive with hash check; report the folder path. (CAMPBELL-021)

Gotchas:
- Report rebuilt about 4 times (2026-09-20, 10-01, 10-02, 10-07) because standards were added late. (CAMPBELL-021, claude)
- Appendix G exhibits had to be swapped back to prior watershed maps. (CAMPBELL-021, claude)
- Urgent resubmittal needed only a replacement page 25. (CAMPBELL-021, claude)
- Deletes were not allowed so stale renders stayed in the folder; use a clean build folder. (CAMPBELL-021, claude)
- About 30 one-time _patch_*.py edits late in the run (EOR format, Alt2 switches, exhibits). (RKN-001, claude)
- Long 2D runs dominate wall time. (RKN-001, claude)

QC checks:
- Banned-word, AI-mark and document-metadata scan on every output. (CAMPBELL-021)
- Native program output vs report table cross-check. (RKN-001)

Source cards: CAMPBELL-021, RKN-001

---

### RPT-C03 Report numbers come only from structured results; report presence is not calculation acceptance
QC rule | target: 05_QC_Rules + guard inside agent report-writer (checked by qc-reviewer) | score 8 | hours 2 | cards 1 | projects 1 | confidence high

Trigger: Any model- or script-drafted report text, review package or notification.

Steps (merged):
1. Build tables from structured calculation outputs; the writer drafts prose only around checked rows. (EKOS-LOCAL-016; same principle RKN-001, SAH-012)
2. Run a numeric guard that rejects writer-authored numbers; allow only bounded software tokens (e.g. HY-8). (EKOS-LOCAL-016)
3. Label every section with its evidence path and status (working, unresolved, record); keep failed and missing analyses visible as explicit gaps. (EKOS-LOCAL-016)
4. Regenerate the Word draft when calculation evidence changes; date-stamp drafts; retire superseded drafts from "current" links. (EKOS-LOCAL-016)
5. Verify DOCX hyperlinks by anchor count, resolving each r:id to an existing target. (EKOS-LOCAL-016)
6. Scan generated DOCX for code fragments before release. (STARVALLEY-020, cross-ref RPT-C13)

Gotchas:
- Autonomous draft copied stale checkpoint statements and wrong rainfall-resolution wording (1-min hydrograph is not 1-min rainfall). (EKOS-LOCAL-016, claude)
- Earlier Word draft predated later road-crossing results and was still linked as current. (EKOS-LOCAL-016, claude)
- Numeric guard rejected the software name HY8 until a bounded exception was added. (EKOS-LOCAL-016, claude)
- Hyperlink check failed because 6 anchors share 5 relationship targets. (EKOS-LOCAL-016, claude)

QC checks:
- Every number in the narrative traces to a structured output row. (EKOS-LOCAL-016)
- No section without an evidence path/status label in working drafts; labels removed in deliverables. (EKOS-LOCAL-016)

Source cards: EKOS-LOCAL-016

---

### RPT-C04 Interim evidence/review package after unattended runs
agent | target: agent model-run-supervisor (package output step); cross-ref drainage-agent-system | score 48 | hours 2 | cards 1 | projects 1 | confidence medium

Trigger: An unattended run finishes (fully or partly) and a reviewable interim package (HTML index, maps, tables, workbook copy) is needed.

Steps (merged):
1. Schedule the package with after-settled dependencies so it builds even when some evidence tasks fail. (EKOS-LOCAL-017)
2. Show candidate geography, sourced evidence, assumptions, and failed/missing calculations, with links to native files. (EKOS-LOCAL-017)
3. Browser-check every local link, image and table row headlessly; render one preview image for visual check. (EKOS-LOCAL-017)
4. Refresh only when meaningful evidence changes; batch refreshes. (EKOS-LOCAL-017)
5. State on the package that it is not the drainage report and not calculation acceptance. (EKOS-LOCAL-017, EKOS-LOCAL-016)

Gotchas:
- Package refreshed 24 times overnight, each followed by a cloud visual check, adding cloud cost (recurrence 24 = refresh count). (EKOS-LOCAL-017, claude)
- Package existence was close to being reported as report completion. (EKOS-LOCAL-017, claude)

Source cards: EKOS-LOCAL-017

---

### RPT-C05 Agency comment register and response matrix
skill | target: new skill agency-comment-response (core) + jurisdiction add-on agency-comment-response/pima-county-rfcd; link from drainage-report-build sec. 0 | score 15 | hours 6 | cards 3 | projects 3 | confidence high

Trigger: A revised report or resubmittal must answer review comments (agency, internal or mock review).

Steps (merged):
1. List every comment ID from every source file first; count them and record the count. Keep original comment text, number, sheet and prior response unchanged. (TANGERINE-002, VALENCIA-007)
2. Keep only drainage-related comments; drop other disciplines (landscape etc.). (VALENCIA-007)
3. One response per comment, tied to that comment only; cross-reference other responses by number. (CAMPBELL-015)
4. Each response states what was done and where: section, table, figure and appendix numbers as displayed. (CAMPBELL-015, VALENCIA-007, TANGERINE-002)
5. Write responses in completed tense ("has been revised"), never "will". (CAMPBELL-015, VALENCIA-007)
6. Track status and remaining action per comment (Incorporated / Partial / Deferred, or status + remaining action) and keep a summary-of-revisions list keyed to comment IDs; remaining items grouped by workstream. See conflict RPT-X01 on whether status/open items go in the deliverable. (TANGERINE-002, VALENCIA-007, CAMPBELL-015)
7. Record agency directions and contradictory comments as EOR decisions so later passes do not undo them. (VALENCIA-007)
8. Rebuild responses after every calc change. (VALENCIA-007)
9. If responses are missing, ask the EOR before final compilation. (VALENCIA-007)
10. Before issue: diff matrix IDs against source IDs; search for ?, TBD, XX and placeholders; set the memo date at issue. (TANGERINE-002)

Gotchas:
- Commingled-flow text for one comment was merged into the railroad response; EOR had it split back. (CAMPBELL-015, claude via Codex session)
- Draft responses said "will"; EOR required all to read as done. Prior responses said "will comply". (CAMPBELL-015, VALENCIA-007; claude via Codex session)
- Stale response text (grate count, flows, D1 size) found twice after calc changes. (VALENCIA-007, claude via Codex session)
- Agency asked to omit an extra FEMA floodplain comparison; record the direction. (VALENCIA-007, claude via Codex session)
- Initial vs later RFCD comments conflicted (remove exhibit vs keep and label). (VALENCIA-007, claude via Codex session)
- Matrix omitted whole comment sets from the second review (Town, landowner agency, county flood control, public). (TANGERINE-002, claude)
- Placeholder reference (T1-?) left in the remaining-items table. (TANGERINE-002, claude)
- Memo date read June 2026 while later files were October. (TANGERINE-002, claude)

Jurisdiction add-ons:
- Pima County RFCD / Pima County DOT: write responses back into the agency's original comment-form layout; place forms (response table) directly behind the cover page. (VALENCIA-007, CAMPBELL-015)

QC checks:
- Comment ID count in matrix = count in source files. (TANGERINE-002)
- No "will" in responses. (CAMPBELL-015, VALENCIA-007)
- Every cited section/table/figure number resolves to the displayed number in the current build. (CAMPBELL-015)

Source cards: CAMPBELL-015, VALENCIA-007, TANGERINE-002

---

### RPT-C06 Report formatting: tables, spacing, footers, references, cover
QC rule | target: drainage-report-build sec. 2 + drainage-report-exhibit-standards sec. 2 (update) + Standard v0.3 change (Word template table style, TOC tab leader) + 05_QC_Rules | score 21 | hours 4.25 | cards 4 | projects 3 | confidence high

Trigger: Building any report or memo by script, and the final formatting pass before QC.

Steps (merged):
1. Build to the EOR standard from the first draft, not in a generic layout patched later: numbered main sections and subsections; Contents and List of Figures (see conflict RPT-X02 for memos). (RKN-014)
2. Apply template styles for headings and paragraph spacing; no manual returns. (SAHPARK-005)
3. Tables: native Word tables, never screenshots; one table style throughout (header row color with white text, alternating row shading, no highlight fills - see RPT-X03); thin borders; all cells centered; portrait; full width; drop constant columns and note them. (SAHPARK-004, RKN-014, TANGERINE-018)
4. One caption per table, above the table, numbered by section; delete any second title inside the table; consistent spacing between caption and table. (SAHPARK-004, TANGERINE-018)
5. Precision: elevations 2 decimals, no thousands separator; discharges whole cfs; same precision down a column. (SAHPARK-004, RKN-014)
6. Fit tables to one page where possible; if a table must break, repeat the header row. (SAHPARK-004)
7. Each table introduced by a "presented in Table n" sentence. (RKN-014)
8. Page breaks only before main sections and appendices; scroll the PDF and remove large white areas and orphaned headings. (RKN-014, SAHPARK-005)
9. 11x17 figures grouped at end of their main section. (RKN-014)
10. No dates in footers (single pages can then be replaced without replotting). Preparer and file properties set to the firm. (RKN-014, TANGERINE-018)
11. Fix TOC tab alignment, stray characters and missing firm heading bar (pull a fresh template if unsure). (TANGERINE-018)
12. Number references 1), 2), ...; real sources only. (TANGERINE-018, RKN-014)
13. Abbreviate directions with a period (S.) or write road names out; be consistent. (SAHPARK-005)
14. Cover: project-specific site photo, preferably from the field visit. (TANGERINE-018)

Gotchas:
- All four RKN reports first built in a generic layout and restructured with one-time patches, about 1.25 h rework. (RKN-014, claude/EOR format)
- Table with green highlights, mixed elevation decimals and a table name not matching the caption. (SAHPARK-004, EOR redline)
- Screenshot of an Excel table plotted poorly. (SAHPARK-004, EOR redline)
- Short appendix table ran onto a second page. (SAHPARK-004, EOR redline)
- Excessive and inconsistent spacing between sections; large blank area on one page. (SAHPARK-005, EOR redline; also TANGERINE-018 x3)
- Table mismatch flagged twice, extra space three times, a stray bracket and footer dates in one draft. (TANGERINE-018, EOR redline)

QC checks (05_QC_Rules):
- No image tables; one table style; one caption per table. (SAHPARK-004, TANGERINE-018)
- Column precision consistent; elevations 2 decimals no separator. (SAHPARK-004, RKN-014)
- No footer dates; no blank half pages; no orphaned headings. (TANGERINE-018, SAHPARK-005, RKN-014)
- Redline recurrence on these cards counts individual comments (TANGERINE-018 = 10, RKN-014 = 4 patch passes).

Source cards: RKN-014, SAHPARK-004, SAHPARK-005, TANGERINE-018

---

### RPT-C07 Narrative content rules: project description, existing conditions, analysis description
QC rule | target: drainage-report-build sec. 1 (update, add "Required narrative content" list) + 05_QC_Rules; enforced by report-writer, checked by qc-reviewer | score 38.5 | hours 5.25 | cards 4 | projects 3 | confidence high

Trigger: Drafting or QC of project description, existing conditions and analysis narrative in any drainage report or memo.

Steps (merged):
1. Project description: use the scope-of-work/RFP description wording when one is required; describe the improvement accurately (which part is developed, direction of expansion). (TANGERINE-019)
2. Existing conditions: one main heading with subheadings - area description (land use in every direction, slopes as range/average % and direction, soils); adjacent landowners and development (name the major adjacent owner - needed for easements); existing infrastructure (roads, berms, culverts and storm drains with sizes); existing hydrology, drainage easements, mapped local floodplains, existing basins/detention. (SAHPARK-002, TANGERINE-020)
3. Describe how the site drains today, including ponding locations and the spill elevation and path; verify against topo. Describe ponding behind embankments (e.g. railroad). (TANGERINE-020, CAMPBELL-017)
4. Include the roadway typical section from the latest plan set; if uncurbed, say so and state spread and inlet analyses do not apply. Delete statements about analyses not done and say why not needed; remove template boilerplate for features the project does not have. (SAHPARK-002, CAMPBELL-017)
5. State figure number and appendix for every exhibit cited. (CAMPBELL-017)
6. State that concentration point flows are sums of sub-basins; show calculated Q vs prior-study Q for all CPs in one table and discuss differences. (CAMPBELL-017)
7. Describe the 2D model setup (culverts, cell size, refinement, inflows) before results. (CAMPBELL-017)
8. State whether increases reach habitable structures and give the cause. (CAMPBELL-017)
9. Terms: natural washes are "washes", engineered ones "channels"; avoid relative words ("near") - say "on the site" or "within the improvement limits". (CAMPBELL-017, TANGERINE-020)
10. Short sentences and short paragraphs. (CAMPBELL-017)
11. No heading without body text before QC. (SAHPARK-002; also SAHPARK-001)

Gotchas:
- Template text kept boilerplate on curb inlets and storm drains the project did not have. (CAMPBELL-017, EOR redline)
- Three empty headings (Hydrology, Methodology, Methodology and Design Criteria), flagged twice. (SAHPARK-002, EOR redline)
- Typical section missing although 30% plans had been issued two weeks earlier. (SAHPARK-002, EOR redline)
- County and Caltrans projects often require their own description text verbatim. (TANGERINE-019, EOR redline)
- Draft stated the expansion direction opposite to the existing improvements. (TANGERINE-019, EOR redline)
- EOR added most existing-site content by markup; it is standard and belongs in the first draft. (TANGERINE-020, EOR redline)

Jurisdiction add-ons:
- Caltrans / Pima County: required project-description text verbatim from scope/RFP (drainage-report-build/caltrans-california, drainage-report-build/pima-county-rfcd). (TANGERINE-019)

QC checks:
- Every exhibit citation names figure number and appendix. (CAMPBELL-017)
- CP Q vs prior-study Q comparison table present when a prior study exists. (CAMPBELL-017)
- No empty headings; no boilerplate for absent features. (SAHPARK-002, CAMPBELL-017)
- Recurrence counts individual redline comments (CAMPBELL-017 = 12, TANGERINE-020 = 6).

Source cards: SAHPARK-002, TANGERINE-019, TANGERINE-020, CAMPBELL-017

---

### RPT-C08 Technical memo structure and memo types (TM, drainage evaluation memo, alternatives memo)
skill | target: new skill drainage-technical-memo (core outline + three memo types); link from drainage-report-build | score 42 | hours 12 | cards 3 | projects 2 | confidence high/medium

Trigger: Any preliminary or final drainage TM, short drainage evaluation from an existing 2D model, or alternatives/justification memo requested by an agency.

Steps (merged):
1. Purpose states what the memo documents/decides (approach and analyses supporting the design; or the decision being made, including what is already designed or under construction) - not the project description. (SAHPARK-001, ELTORO-021)
2. Core TM subsections: data sources; design criteria (table with the authority for each criterion); assumptions; constraints; decisions (date and who made them); methods; results; Summary and Conclusions with next steps. Never leave Conclusions empty. (SAHPARK-001)
3. Attribute agency direction to the meeting date it was given. (SAHPARK-001)
4. Drainage evaluation memo (existing 2D model): Purpose, Analysis Approach (software, grid, n, flow source), Results, Conclusions; state no new hydrology was done and flows come from the approved regional study; say regional flows on local areas give conservative depths; compare existing vs ultimate WSE and report increases above the jurisdiction threshold inside/outside ROW and at structures; attach depth and difference figures. (ELTORO-018)
5. For qualitative concepts add a limitations section (not a full hydraulic design; does not pass Q100 without overtopping, where true). (ELTORO-018)
6. Alternatives memo: inputs are meeting transcript, meeting notes and one or two prior agency memos as format examples; define each alternative once with a figure and use the same definition throughout; cite specific parameters from each reference (speed, buffer width, volumes), not just titles; sections purpose, background, alternatives, constraints (ROW, drainage), circulation/user benefits, constructability, recommendation. (ELTORO-021)
7. Check facts in machine meeting notes against the transcript. (ELTORO-021)
8. Set running header text and "Page x of y" after figures are appended. (ELTORO-018)

Gotchas:
- Draft 3 purpose described the road project only; no criteria, assumptions or decisions anywhere. (SAHPARK-001, EOR redline)
- Summary and Conclusions heading empty in the draft sent for QC. (SAHPARK-001, EOR redline)
- Memo title "Drainage Evaluation" vs running header "Drainage Statement" and "Page x of 3" in a 20-page PDF. (ELTORO-018, claude)
- Regional flows applied to local areas give conservative depths; say so. (ELTORO-018, claude)
- Five drafts over about three months; reviewers repeatedly flagged unclear alternative definitions, purpose not stating the decision, references without parameters, missing traffic data. (ELTORO-021, claude)
- Machine meeting notes carry an accuracy warning. (ELTORO-021, claude)

Jurisdiction add-ons:
- Town of Sahuarita: record Town criteria with meeting date (e.g. 1.0 ft max overtopping depth). (SAHPARK-001)
- Sahuarita / Pima County RFCD: 0.10 ft WSE increase reporting threshold used in evaluation memo (see conflict RPT-X05). (ELTORO-018)

QC checks:
- Criteria table present with authority column; decisions dated. (SAHPARK-001)
- Header text and page count match final PDF. (ELTORO-018)

Source cards: SAHPARK-001, ELTORO-018, ELTORO-021

---

### RPT-C09 Pre-issue self-consistency check (claims vs content, final inputs, datum)
QC rule | target: 05_QC_Rules + agent qc-reviewer checklist | score 32 | hours 8 | cards 2 | projects 2 | confidence high

Trigger: Final check of any report or memo before submittal; any time a sub-consultant sends more than one batch of sections or graphics.

Steps (merged):
1. Log each sub-consultant batch with date received; mark the final one; diff report sections against the final batch, not the coordination draft; replace preliminary graphics with final-vintage files. (BARNETT-003)
2. Search for statements that results are incorporated in another section and confirm the content is there; populate or remove exhibit placeholders. (BARNETT-003)
3. If content is condensed or replaced on purpose, tell the sub-consultant and say so in the report or an appendix. (BARNETT-003)
4. Tables use the same vertical datum as the current model and plans. (HOMEWOOD-015)
5. Summary tables actually pass the stated criteria. (HOMEWOOD-015)
6. Conclusion names only BMPs/facilities and storms actually analyzed. (HOMEWOOD-015)
7. Appendix titles match contents and software used. (HOMEWOOD-015; see RPT-C11)
8. Facility sizes match current plans and vendor calculators; management-area areas match the SWQP. (HOMEWOOD-015)
9. Remove files from other projects from the project folder. (HOMEWOOD-015)

Gotchas:
- Final outreach survey analysis arrived five weeks before the 30% DCR, yet only two numbers made it in, the exhibit placeholder was empty, and the text claimed full incorporation. Final plan/section images were 4-10x larger and sharper than preliminary. (BARNETT-003, claude)
- HGL table at about 1,580 ft vs plan datum near 6,240 ft; HGL above rim at one node. (HOMEWOOD-015, claude)
- Conclusion cited bioretention planters (none proposed) and the 10-yr storm while analysis was 50-yr 1-hr. (HOMEWOOD-015, claude)
- Appendix titled Hydraflow contained an SSA report; unrelated RETDET.xls in the storm folder. (HOMEWOOD-015, claude)
- Gallery sizes in vendor calculators (60-in / 18-in) differed from plans (72-in / 30-in). (HOMEWOOD-015, claude)

QC checks:
- Datum check on every elevation table. (HOMEWOOD-015)
- Every "incorporated in/see section" claim resolves to real content. (BARNETT-003)
- Conclusions vs analyzed scenarios/storms. (HOMEWOOD-015)
- Sizes in report = plans = vendor calcs. (HOMEWOOD-015)

Source cards: BARNETT-003, HOMEWOOD-015

---

### RPT-C10 Compiled bookmarked PDF (body + figures + dividers + native output)
skill | target: Standard v0.3 change (formalize compile step, e.g. compile_report.py with manifest) + drainage-report-build sec. 3 (update "compiled PDF" bullet) + 05_QC_Rules for bookmarks/links | score 24.3 | hours 5.4 | cards 5 | projects 5 | confidence high

Trigger: Final assembly of the report body, 11x17 figures, appendix dividers, native model output, reference studies and plan sheets into one submittal PDF; recompile after any model rerun.

Steps (merged):
1. Start from the newest editable source and its fresh Word export. (VALENCIA-008)
2. Keep an assembly manifest (file, page range, final location) and a destination map; generate bookmarks, named destinations and links from it; never hardcode page numbers in prose. (VALENCIA-008)
3. Insert 11x17 figures at the end of each main section; add a divider per appendix and per plan set or study; rotate landscape pages. (RKN-015, CALFIRE-014, CAMPBELL-020)
4. Append native output: PC-HYDRO printouts and hydrographs per CP, HEC-HMS output, Atlas 14 PFDS printout, HY-8 report, RAS computation summaries, FIS/LOMR/dam-safety pages. (RKN-015, CALFIRE-014)
5. Highlight the relevant Q values in reference studies; replace table numbers on images with markup over them matching size, font and color. (CAMPBELL-020)
6. Insert intentionally blank pages only where items are to follow; remove unneeded pages and unrequested appendices; remove review-draft wording. (CAMPBELL-020, VALENCIA-008)
7. Annotations: flatten markups that must print (flattened but recoverable); flatten or note FreeText annotations brought in from source pages; remove plan revision clouds from the compiled copy, keep original marked PDFs (see conflict RPT-X04). (CAMPBELL-020, CALFIRE-014, VALENCIA-008)
8. Bookmarks at minimum: cover, TOC, each main section, each figure, each main appendix; generated by script from headings and captions; sorted by page within each level. (TANGERINE-016, CALFIRE-014)
9. Check every link and bookmark target programmatically; log page and bookmark counts; then check interactively in a native PDF reader (Bluebeam). (CAMPBELL-020, CALFIRE-014, VALENCIA-008, TANGERINE-016)
10. Compare every assembled page to its source (text, size, low-dpi render); keep a QA JSON; render pages to PNG for a visual check. (VALENCIA-008, RKN-015)
11. Reduce duplicated resources at the end; check agency upload limits and compress rasters; keep a reduced copy for transfer. (VALENCIA-008, RKN-015)
12. If a model rerun is pending, run a watcher that waits for the new HDF, regenerates results and figures, recompiles, then copies to 10_Record. (CALFIRE-014)

Gotchas:
- Appendix bookmark order wrong (Table A-2 on p. 26 listed after Table A-1 on p. 27). (CALFIRE-014, claude)
- Source LOMR pages bring FreeText annotations into the compiled PDF. (CALFIRE-014, claude)
- A report link did not work in the reviewed draft. (CAMPBELL-020, EOR redline)
- Source PDFs raise pypdf "Multiple definitions for key /PageMode" warnings; harmless. (RKN-015, claude)
- Compiled PDFs reached 55-86 MB (RKN-015), 700 MB-1 GB (VALENCIA-008); 23.8 MB needed a 3.4 MB copy (SAH-012). (RKN-015, VALENCIA-008, SAH-012; claude, claude via Codex session)
- Revision cloud annotations vanished in merged plan pages; 39 sheets had to be re-rendered. (VALENCIA-008, claude via Codex session)
- Final report must not carry plan revision clouds. (VALENCIA-008, claude via Codex session)
- Editable Word body held corrections that never reached its PDF. (VALENCIA-008, claude via Codex session)
- Browser-based reader checks failed under computer-use URL policy; use a native PDF reader. (VALENCIA-008, claude via Codex session)
- Issued 96-page PDF and three exhibit PDFs had no bookmarks (EOR general comment on a substation report draft). (TANGERINE-016, EOR redline; TANGERINE-011)

QC checks (05_QC_Rules):
- Every report and exhibit PDF has the minimum bookmark set; every bookmark and link resolves; bookmarks sorted by page. (TANGERINE-016, CAMPBELL-020, CALFIRE-014)
- Page-by-page source comparison QA JSON exists. (VALENCIA-008)
- No revision clouds, no review-draft wording, no unflattened stray annotations. (VALENCIA-008, CALFIRE-014, CAMPBELL-020)
- File size checked against the receiving agency limit. (RKN-015)

Source cards: CALFIRE-014, CAMPBELL-020, RKN-015, VALENCIA-008, TANGERINE-016

---

### RPT-C11 Appendix contents match titles; appendix order
QC rule | target: 05_QC_Rules + drainage-report-build sec. 1 (appendix rules) | score 6 | hours 1.5 | cards 1 | projects 1 | confidence high

Trigger: Assembling appendices for a drainage report or memo.

Steps (merged):
1. Hydrology appendix holds the actual hydrologic basis: source-study discharge tables for the cited sections and a location map annotated to the sections used. (SAHPARK-011)
2. Keep general floodplain mapping only if annotated to show why it matters. (SAHPARK-011)
3. Every reference excerpt states source document, section and why it is included; cite only the governing manual for the jurisdiction. (SAHPARK-011)
4. Order appendices A, B, C, D with subparts D-1, D-2 after the parent; channel calcs in their own subpart, not under culverts. (SAHPARK-011)
5. Appendix title matches contents and software used. (HOMEWOOD-015, cross-ref RPT-C09)

Gotchas:
- Hydrology Calculations appendix contained only regional floodplain mapping. (SAHPARK-011, EOR redline)
- Uncited City of Tucson manual page with no stated purpose on a Town/County project. (SAHPARK-011, EOR redline)
- Appendix D-1 came before Appendix D; a channel calc sat in the culvert appendix. (SAHPARK-011, EOR redline)

Jurisdiction add-ons:
- Town of Sahuarita / Pima County RFCD projects: do not cite City of Tucson standards. (SAHPARK-011)

Source cards: SAHPARK-011

---

### RPT-C12 Delivery and review package (zip, manifest, checksums, rebuild guide)
skill | target: new skill delivery-package-build | score 9 | hours 4 | cards 3 | projects 3 | confidence high

Trigger: Handing over a report update, alternative or multi-GB review folder (CAD, models, PDFs, renderings) so someone else can review or rebuild it.

Steps (merged):
1. Finish all content before the final copy; copy finished model results only (never while a run is writing). (SILVERBELL-012)
2. Stage in the work folder, then copy to the delivery folder; one zip per deliverable (original-report update, separate alternative). (SILVERBELL-012, VALENCIA-010)
3. Include START_HERE/PACKAGE_README stating which files are new and where originals stay, FILE_INVENTORY (csv/html, purpose of each file), sheet index, REBUILD_GUIDE, EXCLUSIONS, SHA256SUMS and a verify script. (SILVERBELL-012, VALENCIA-010, HOMEWOOD-022)
4. Exclude regenerated files (.bck/.sol), node_modules, __pycache__, .git and other packages; keep reference model exports separate. (HOMEWOOD-022, VALENCIA-010)
5. Run PDF verification on compiled PDFs before copying. (SILVERBELL-012)
6. Re-read every zip member and match hashes and sizes (source vs delivery); keep one final zip; delete zip temp files. (VALENCIA-010, SILVERBELL-012, HOMEWOOD-022)
7. Save deliverables to the synced OneDrive folder; leave a Delivery_Location pointer in the old work folder; do not redistribute older copies. (VALENCIA-010)

Gotchas:
- Two zips of different size (5.9 MB and 8.8 MB) and a leftover zip temp file remained in the package folder. (HOMEWOOD-022, claude)
- Late additions (source model, re-rendered views) forced re-copies. (SILVERBELL-012, claude)
- Copying while a RAS run is writing risks partial HDFs. (SILVERBELL-012, claude)
- Zips were 4.4 GB and 7.4 GB (ZIP64); allow time for OneDrive sync. (VALENCIA-010, claude via Codex session)
- Agent cannot open OneDrive share links in its browser; use the locally synced folder. (VALENCIA-010, claude via Codex session)
- Older D: copies must not be redistributed after delivery moves to OneDrive. (VALENCIA-010, claude via Codex session)

QC checks:
- SHA256 match for every member; exactly one final zip per deliverable; no temp files. (VALENCIA-010, SILVERBELL-012, HOMEWOOD-022)

Source cards: HOMEWOOD-022, SILVERBELL-012, VALENCIA-010

---

### RPT-C13 FEMA CLOMR/LOMR package: scripted model build, post-chain and pre-upload QC
skill | target: new skill flo2d-clomr-package (core) + jurisdiction add-on flo2d-clomr-package/fema + QC rule (package QC gate in 05_QC_Rules); qc-reviewer runs the gate independently | score 58 | hours 43 | cards 2 | projects 1 | confidence high

Trigger: Producing a FEMA CLOMR/LOMR package (duplicate effective, existing, proposed models, results, GIS, exhibits, report tables) that will be rebuilt several times; before any package is zipped and uploaded and before any response letter states an item is complete.

Steps (merged):
1. build_models.py regenerates every derived input from source surfaces, centerline and design data; log cell counts and surface sources. (STARVALLEY-020)
2. Shared helper module for grid, TOPO, LandXML and transform readers; drive package variants by environment variables; keep backups of each script version. (STARVALLEY-020)
3. Post-chain: post-process results, structure flows, dWSE location tables, flood zones, model shapefiles, Appendix D warnings, QGIS exhibits, report writer, package QC. (STARVALLEY-020)
4. Appendix D: tabulate every ERROR.CHK and runtime-warning message per model; mark those also in the duplicate-effective run as inherited; give a disposition. (STARVALLEY-020)
5. Package QC per model folder: FLOPRO.exe build = CONT.DAT line 1 build = SUMMARY.OUT build; all DLLs present. (STARVALLEY-004)
6. All required input/output files present (CHAN/CHANBANK/XSEC when ICHANNEL=1; CHANMAX, CROSSMAX, HYDROSTRUCT, MAXWSELEV, DEPTH, ERROR.CHK). (STARVALLEY-004)
7. Zero *.TMP files; oldest output newer than newest input; SUMMARY.OUT shows completed run and volume conservation rating. (STARVALLEY-004)
8. Cross-model hash check: CADPTS, INFLOW, OUTFLOW, FPXSEC, TOLER, RAIN identical across duplicate effective, existing and proposed. (STARVALLEY-004)
9. HYSTRUC rating tables equal the HY-8 export (names, discharge pairs, headwater reference offset). (STARVALLEY-004)
10. Flood zone and BFE contour shapefiles present for every condition. (STARVALLEY-004)
11. Scan report, matrix and letter DOCX/XLSX for placeholders ([DATE], [TO BE CONFIRMED], bracketed notes) and code fragments; fail the package if any remain. (STARVALLEY-004, STARVALLEY-020)
12. Write package_QC_report.txt and include it as a report appendix; write a package README; build ZIP64 zips; compile a review PDF of all exhibits and documents. (STARVALLEY-004, STARVALLEY-020)

Gotchas:
- June package shipped Ultimate outputs older than 16 edited inputs, a CONT.DAT header of Build 16.06.16 against a 23.10.25 SUMMARY.OUT, existing-condition folders with zero outputs, 8 TMP files in Interim and no zone shapefiles; FEMA closed the case and a new case and fee were required (40 h). (STARVALLEY-004, claude)
- FEMA runs the exe / CONT.DAT / SUMMARY.OUT build comparison itself; a stale header string alone draws a comment. (STARVALLEY-004, claude)
- Report text generated from code leaked a Python conditional string into the TDN draft (sec. 4.8.3). (STARVALLEY-020, claude)
- Keep backups of each script version so a regression can be traced. (STARVALLEY-020, claude)

Jurisdiction add-ons:
- FEMA (Region IX): build-string consistency, duplicate-effective inheritance of warnings, zone/BFE shapefiles, ZIP64 upload packages. (STARVALLEY-004, STARVALLEY-020)

QC checks (gate, fail = do not upload):
- Build strings match; no TMP; output newer than input; required files present; boundary files identical across conditions; HYSTRUC = HY-8; shapefiles present; zero placeholders. (STARVALLEY-004)

Source cards: STARVALLEY-020, STARVALLEY-004

---

### RPT-C14 Proposal / SOQ / interview drainage content
skill | target: new skill proposal-drainage-approach (core) + QC rule for proposal language | score 20 | hours 5.5 | cards 3 | projects 2 | confidence medium/high

Trigger: Writing the drainage section of an SOQ or proposal, a drainage approach narrative, or interview slides on drainage, floodplain and schedule risk.

Steps (merged):
1. Start from scoping meeting notes and the RFP; list drainage components (offsite hydrology, cross-drainage, berms, FEMA, onsite, WQ, utility conflicts). (ELTORO-020)
2. Pull head-start facts from prior firm work on the corridor (master plan CPs and facilities, existing 2D model, prior DCR) and cite them. (ELTORO-020, ELTORO-019)
3. Put the client first in the opening sentence; state goals in the client's terms (e.g. all-weather access, no adverse impact to adjacent property, 100-yr under the road where preferred, cost efficiency). (ELTORO-019)
4. Describe existing conditions first (e.g. widespread shallow sheet flow, few/undersized crossings, berms worsening flooding). (ELTORO-019)
5. Propose an early methods-and-criteria memo coordinated with the agency and RFCD before design. (ELTORO-019)
6. Write the approach narrative plus a risk list (railroad, berm discharge, floodplain permitting, ultimate section sizing); produce full and one-page versions. (ELTORO-020)
7. Schedule language: critical-path; aim for a stable regulatory basis early, not a frozen 30% design; present CLOMR (12-24 mo), LOMR (9-12 mo) and historic review durations as planning allowances. (SILVERBELL-016)
8. Technical claims: do not assert unconfirmed utilities at crossings; separate precedent from confirmed site data; equal cut and fill does not prove no rise - test compensatory grading hydraulically; do not treat 0.1 ft rise as a universal trigger or assume Zone A becomes AO. (SILVERBELL-016)
9. No description of who does what between software tools and engineers; write for the client. (ELTORO-020)

Gotchas:
- Draft led with the firm and a generic approach; reviewer redline asked for all five changes. (ELTORO-019, EOR redline)
- Took Rev 1 to Rev 3 plus a one-page cut; the draft named the AI/engineer division of work and had to be rewritten. (ELTORO-020, claude)
- Opening slide and DCR disagreed on the direction of a POC. (SILVERBELL-016, claude)
- Mobile chat schedule dates conflicted with the deck; deck schedule governs. (SILVERBELL-016, claude)

QC checks:
- Client-first opening; goals in client terms; existing conditions before approach. (ELTORO-019)
- Durations labeled as planning allowances; no unconfirmed site facts. (SILVERBELL-016)

Source cards: ELTORO-019, ELTORO-020, SILVERBELL-016

---

### RPT-C15 Crossing rise memo: exceedance duration and hazard from 2D output
skill | target: new skill crossing-rise-impact-memo (2D post-processing + memo outline); cross-ref hecras-result-rasters and RPT-C08 | score 2 | hours 1 | cards 1 | projects 1 | confidence medium

Trigger: Agency or railroad owner needs a reach memo on WSEL rise at a crossing.

Steps (merged):
1. Focus on the last proposed iteration; list modeling effort, assumptions and data gaps. (CAMPBELL-024)
2. Compute time above 0.1, 0.5 and 1.0 ft rise at common-wet cells from saved output; plot exceedance durations; note maxima can occur at different cells. (CAMPBELL-024)
3. Compute depth x velocity^2 hazard for both conditions. (CAMPBELL-024)
4. Map WSEL and velocity differences; show bridge and barrel flows separately. (CAMPBELL-024)

Gotchas:
- Native cell counts are not raster areas. (CAMPBELL-024, claude via Codex session)

Jurisdiction add-ons:
- Railroad owner: guidance uses subgrade and structure elevations, not one pass/fail rise limit. (CAMPBELL-024)

Source cards: CAMPBELL-024
