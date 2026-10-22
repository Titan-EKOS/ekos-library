# QC group - reconciled clusters

Group file: group_qc.json (64 cards: 52 qc_rule, 8 agent, 4 skill; all source_ai = claude). 24 clusters.
Score = sum of hours_lost x recurrence. For qc_rule cards, recurrence usually counts individual redline or agency comments (one comment = 1), so redline-heavy clusters (C11, C09, C12) score high on modest hours; agent cards are mostly recurrence 1 with large hours.
Source tags give card id, harvesting AI and the evidence type (JCO redline, agency redline/comments, reviewer comments on a reference report, Codex session, run logs, session record).

---

### QC-C01 Independent QC reviewer and submittal auditor
agent | agent qc-reviewer | score 62.0 | hours 62.0 | cards 3 | projects 2 (HOMEWOOD, STARVALLEY) | confidence high/medium
Trigger: Before a drainage memo, county worksheets, storm drain model or SWQP goes to the agency; before every FEMA resubmittal and after any FEMA closure or additional-data letter; on a high-stakes CLOMR after several model rebuilds; or when the designer cannot reconcile methods.
Steps (merged):
1. Run in a separate context from the builder/designer. Do not read builder notes as truth; work only from the archived upload package (zips as uploaded) or the transmitted files, never the working folders.
2. Confirm governing standards in a table: method, design storm, HGL criterion, WQ, hydromodification, BMP siting (Placer case) or FEMA guidance and effective model (FEMA case).
3. Inventory the package: list zip members with timestamps; flag outputs older than inputs, missing outputs, TMP files, header/build mismatches.
4. List deficiencies by document: formulas, method mismatch, model settings, outlets vs plans, boundary conditions, memo/letter consistency.
5. For each agency comment classify: addressed with file evidence / done but not run / not done / stale (agency text repeated from a prior letter that the files disprove) / new.
6. Compare every response-letter or memo claim to the model outputs and GIS actually in the package; flag any claim not backed by a file and page.
7. Where an independent recalculation is warranted, re-run separately and report each basis separately (e.g. corrected county method, calibrated SWMM, same files in SSA); run every hydrology case for each plausible rainfall basis so the agency can choose without reruns.
8. Blind-rebuild mode (high-stakes CLOMR only): give the agent only a source list (effective model and TDN, survey, approved plans, O&M, ESA), forbid prior CLOMR products, scope to the checks that matter (duplicate effective reproduction, terrain and coordinate checks, native HY-8 structure ratings, basin storage, rise analysis), time-box to one session, require a continuation state file, judgment register and decision records.
9. Separate defensible items (fee or reopen requests) from legitimate findings.
10. Ask the EOR only for real decisions; explain in the question what a missing item is (model type, role).
11. Deliver: review report, corrected workbook, models, results summary, figures, scripts, a README stating which files are new, the EOR decisions needed, and build rules for the next package. Log differences from the main package for EOR decision.
Gotchas:
- Mark the review package as a review draft, not stamped; the EOR must accept it (HOMEWOOD-005, claude, independent review).
- Never overwrite designer originals; keep them in a reference folder and say so in the README (HOMEWOOD-005, claude, independent review).
- Whole review plus 36 SWMM and 17 SSA runs took about 1.5 h scripted vs weeks of manual pipe-sizing iterations; scripted re-runs are the main payoff (HOMEWOOD-005, claude, independent review).
- Working response letter carried 10 TO BE CONFIRMED placeholders while the uploaded PDF stated those items complete; the agency reviewer cited letter-vs-model discrepancies (STARVALLEY-005, claude, audit record).
- About a third of the agency closure text was stale wording from the prior letter; an audit with file evidence lets the cover letter say so without arguing (STARVALLEY-005, claude, audit record).
- The audit must be done by an agent that did not build the package so it does not trust builder notes (STARVALLEY-005, claude, audit record; same principle HOMEWOOD-005).
- A full blind rebuild is too large for one pass: one session ran about 9.5 h and used 47 pct of the weekly allowance without producing the notebook or rise analysis (STARVALLEY-021, claude via Codex session).
- The blind rebuild found items the main package had not flagged: effective 24-hr storm model files absent (only 3-hr supplied), basin grading storage 15.71 vs 18.10 ac-ft approved, a culvert headwater 0.02 ft over allowable, storm-drain outlet loss omitted (STARVALLEY-021, claude via Codex session).
- Three runs were left running unmonitored at session end; the reviewer must stop or hand off its own runs (STARVALLEY-021, claude via Codex session).
QC checks:
- Every response-letter claim has a file + page citation in the package.
- No placeholder (TBC, TO BE CONFIRMED, [ ]) in any transmitted letter.
- Package outputs newer than inputs; no TMP files; headers match build.
Source cards: HOMEWOOD-005, STARVALLEY-005, STARVALLEY-021

### QC-C02 Pre-QC self-check and mock agency review
agent | agent qc-reviewer (pre-review mode, called by report-writer before principal QC) | score 10.0 | hours 9.0 | cards 2 | projects 2 (SAHPARK, TANGERINE) | confidence high/medium
Trigger: A staff or agent draft memo/report is ready to go to principal (JCO) QC; or a concept/rezoning report will face agency review and a skeptical public before formal submittal.
Steps (merged):
1. Run the draft PDF and its source folder through the 05_QC_Rules checklist (headings, traceability, tables, exhibits, appendices, software versions, existing infrastructure).
2. Check every discharge against the source study table and every result against the calc output (see C07).
3. Check exhibits for border, scale, labels, storm title, transparency and legend ranges.
4. Mock review mode: give the agent the draft PDF, the governing manuals list and the review roles (town reviewer, county flood control reviewer, landowner-agency reviewer, public/opposition reader).
5. Run the same review prompt on two AI platforms independently (set A, set B).
6. Require each comment to carry a unique source-prefixed ID, a report location (section, page, table or figure), what is missing and the expected revision.
7. Merge the sets: collapse duplicates, keep the stricter wording, log which set raised each item; use overlap as the priority signal.
8. Return a findings list with page references; the author fixes before QC. Hand the merged list to the comment-response log (C03) and sort into fix now vs carry to the next report (e.g. master drainage report).
Gotchas:
- Reviewer asked staff to catch basic errors (a 200-yr flow label) before sending for review; 48 comments on a 5-page body cost a full rewrite cycle (SAHPARK-018, claude, JCO redline).
- Both mock-review sets independently flagged the same core items (uniform Manning n, non-common mesh comparison, unsized detention, crossing language, preserve area not on maps); overlap confirmed priority (TANGERINE-001, claude, mock review sets).
- ID collision: set A used A-1..A-3 for agency comments while set B used A-1..A-4 for the landowner-agency reviewer; prefix IDs by source set before merging (TANGERINE-001, claude, mock review sets).
- Prompts written from a public or opposition view produce politically framed text; keep it internal and never paste it into a deliverable (TANGERINE-001, claude, mock review sets).
QC checks:
- Self-check findings list attached to the QC transmittal; zero open basic items (flow labels, return periods, numbering).
Source cards: SAHPARK-018, TANGERINE-001

### QC-C03 Comment reconciliation and response log
skill + qc_rule + agent | new skill comment-response-log + QC rule (05_QC_Rules); run by agent qc-reviewer before resubmittal | score 20.0 | hours 20.0 | cards 3 | projects 2 (BARNETT, SAHPARK) | confidence high
Trigger: Any agency review comments or internal QC redlines received on a DCR, drainage report, memo or plan set; before any resubmittal (15/30/60/90 pct); when an owner says prior comments look unaddressed or a sub-consultant says its work was left out.
Steps (merged):
1. The day comments arrive, log every comment in one matrix: all agency divisions (each tab of the agency xlsx), reviewer summary lists and PDF markups.
2. Extract every PDF annotation with pypdf (page, author, subject, contents); drop links, popups, text-box labels and plain shapes.
3. Give every row a stable ID (C-01..., or source-prefixed) and tag copyedit vs substantive; summarize counts by category (missing content, technical errors, engineering content, exhibits, formatting, methodology, editorial).
4. Columns: document/page, comment, response/resolution, revised location (new section), Action, Completed by, Check by, disposition (incorporated / superseded / no change - comment noted). Blank is not an acceptable disposition.
5. Before the next submittal, search the issued text for the wording/topic of each comment and classify Addressed / Partially Addressed / Not Addressed / Cannot Determine with page or section evidence.
6. Compare sub-consultant batches by date and file size (draft vs final) with what the report contains; flag empty exhibit placeholders and claims such as "complete results incorporated in Section X".
7. Output a draft response matrix plus a prioritized remediation list (concept-affecting first, copyedit last) for engineer review.
8. Log extra variances found during a rewrite separately (unrealized assumptions, criteria not applied, undersized easement, sediment, scour).
9. If the report says a response matrix is in an appendix, confirm the appendix is in the package before issue. Review the log at the internal QA/QC checkpoint before each submittal.
10. Internal redline logs are internal quality records; do not transmit.
Gotchas:
- A text-only export strips images, so figure legibility, legends and graphic vintage cannot be verified; mark those Cannot Determine and check the native file (BARNETT-001, claude, agency markups).
- Reviewer markups were about 50 pct punctuation edits; sort them out before counting or the log is unreadable (BARNETT-001, claude, agency markups).
- Fixes made in one section were not carried to related sections written by other authors; search the whole report for the same term or claim (BARNETT-001, claude, agency markups).
- 15 pct DCR log had about 104 comment rows across four divisions with Action/Completed/Check blank; the 30 pct DCR still claimed an appendix matrix that was not in the files, and the owner reported comments as undocumented (BARNETT-002, claude, agency comment log).
- 48 JCO comments on a 24-page draft were structural; Rev A was rebuilt from sources rather than edited (SAHPARK-017, claude, JCO redline log).
- Rev A rewrite grew to about 90k characters and 20 tables while the 30 pct issue was a 4-page Rev B; size the rewrite to the deliverable before expanding (SAHPARK-017, claude, JCO redline log).
QC checks:
- Every comment row has a disposition and Completed by / Check by before issue.
- Responses to agency are written as what was done (see C06), with revised location.
- Appendix matrix referenced in text exists in the package.
Source cards: BARNETT-001, BARNETT-002, SAHPARK-017

### QC-C04 Open items, checklist status and assembly gate
qc_rule + skill | Standard v0.3 change + QC rule (05_QC_Rules) | score 1.4 | hours 1.4 | cards 3 | projects 3 (CALFIRE, RKN, SAH) | confidence high
Trigger: Any preliminary H&H package or draft from assemble_report.py before it goes to the EOR, owner or agency; issuing a requirements checklist with a prelim report.
Steps (merged):
1. Build the QC open-items / EOR checklist document (python-docx) with: table of submittal prerequisites (jurisdiction, plans match analysis, T2 check, seal, waivers, open items); numbered open items typed geotechnical / final design / waiver / approval / EOR decision / submittal; native-vs-report calc cross-check table (C07); EOR standards checklist with status and location, deviations called out; empty markup response log (document/page, comment, response, revised location).
2. Cross-check each agency/requirements checklist row against the open items; rows resting on lidar culvert data, assumed bridge geometry, unknown layout or unconfirmed calibration are Partial or Assumed, not Addressed.
3. For Standard v0.3 drafts read _ASSEMBLY_REPORT.md sections 1, 5 and 9; close or list in the transmittal every WARN, unresolved placeholder and human decision.
4. QC_Log Tier 1 must not be 0 answered; CalcRegister must not be empty for a design report.
5. Library entries marked VERIFY (prior study citation, current ADEQ CGP edition) need a checked citation.
6. Every [FIGURE:F-nn] in the template matches an ExhibitRegister ID; a table referenced in two sections has one owner.
Gotchas:
- Deviations from the standard (HEC-HMS 4.13 vs 4.12, Python exhibits vs QGIS, missing brand template) must be listed as EOR decisions, not buried (RKN-018, claude, session record).
- All 21 checklist rows were marked Addressed while the open-items memo listed 13 items, including culvert size/inverts, bridge low chord and new impervious area that drive the culvert, bridge and SWDR rows (CALFIRE-016, claude, session record).
- 30 pct draft went out with QC_Log 0/27, CalcRegister empty, 6 unresolved placeholders (EOR PE number, prior study fields) and F-06/F-08 unregistered (SAH-013, claude, assembly report).
- Assembler flagged library id PROJECT-TEXT not found and treats PROJECT-TEXT as one entry per report (later sections duplicate); text came through the Narrative sheet instead. Fix in the standard (SAH-013, claude, assembly report).
- s60 post-process deleted leftover placeholder paragraphs, which hides open items in the docx; keep them listed in the assembly report (SAH-013, claude, assembly report).
QC checks:
- Checklist status vocabulary limited to Addressed / Partial / Assumed (see conflict 5) and consistent with the open-items list.
- Assembly gate: QC_Log Tier 1 > 0, CalcRegister populated, zero unregistered figures, VERIFY items cited.
Source cards: CALFIRE-016, RKN-018, SAH-013

### QC-C05 EOR decision loop and design-basis changes
agent + qc_rule | QC rule (05_QC_Rules) + Standard v0.3 change (decision register); used by report-writer and model-run-supervisor | score 29.0 | hours 7.0 | cards 2 | projects 2 (VALENCIA, CAMPBELL) | confidence high
Trigger: Calc updates hit plan conflicts or design choices that change downstream flows; two design flows (or other basis values) exist for one feature across report tables, workbook and plans.
Steps (merged):
1. List each competing value with source, method and where it is used.
2. Classify each conflict: isolated (no receiving system or shared control affected) vs propagating.
3. Resolve isolated, evidence-supported conflicts; log feature, values, sources, choice, reason and dependency check.
4. Ask the EOR propagating questions one at a time with a short problem statement, options and consequences, and a plan/profile image. Do not edit tables until decided.
5. Once decided, update narrative, tables, exhibit labels, HY-8 and protection sizing together; keep each native run and the final decision.
6. Keep an open-item register with source pages, effort and owner; do not compile while items are open unless the EOR authorizes it, then list them in a separate unresolved-items document.
7. Write a continuation handoff with resolved decisions so the next session does not re-ask.
Gotchas:
- Agent team changed a design flow from 886.6 to 823.1 cfs; EOR reversed it: 886.6 cfs is the larger area routed to the crossing (CAMPBELL-014, claude, EOR direction via Codex session).
- One structure (D1) changed three times (3 arches, 2-18 in pipes, 2-24 in pipes); keep each native run and the final decision (VALENCIA-011, claude via Codex session).
- EOR wanted downstream flows to match the updated pavement drainage maps, not recomputed totals (VALENCIA-011, claude via Codex session).
- Do not call an odd size a typo without evidence; 18x11 in is a standard concrete arch (VALENCIA-011, claude via Codex session).
- Do not put EOR working assumptions (e.g. utility conflicts mitigated) in report text unless told (VALENCIA-011, claude via Codex session).
QC checks:
- No change to a design flow or structure size in tables without a decision-register entry.
- Decided values identical across narrative, tables, exhibits, HY-8 and protection sizing.
Source cards: VALENCIA-011, CAMPBELL-014

### QC-C06 Transmittal control: freeze, hold-until-final, final cleanup
qc_rule | QC rule (05_QC_Rules) | score 10.5 | hours 2.5 | cards 3 | projects 3 (SILVERBELL, BARNETT, VALENCIA) | confidence high/medium
Trigger: Reviewer says "freeze" design and results; a draft with owner-unreviewed content (alternative cost/evaluation matrices) is going to the owner; a QC draft is being converted to the agency submittal.
Steps (merged):
1. Freeze: stop all geometry edits and solver reruns immediately; package current CAD, plans, results and exhibits with checksums; list unresolved items in the package README; pause any automatic follow-up after delivery.
2. Hold-until-final: keep a list of sections/tables marked hold until final; search the compiled draft for each before transmittal and remove or move it; release after the owner has reviewed the underlying data.
3. Final cleanup: remove DRAFT from the cover; set current date and current office address.
4. Turn off markups on included comment forms; rewrite responses as what was done, not "will comply".
5. Remove highlights and leftover review notes from exhibits and text.
6. Check spelling of road names and a single report font.
Gotchas:
- At freeze, proposed 2D convergence and bridge alternatives were unresolved; they were documented, not hidden or fixed silently (SILVERBELL-011, claude, JCO direction).
- The alternative evaluation matrix (cost and timeline) was meant to be held until the final report but went out in the 15 pct draft (BARNETT-010, claude, JCO redline).
- Exhibit notes still carried internal check markup in the draft (VALENCIA-020, claude, JCO redline).
- Road name misspelled in the report body (VALENCIA-020, claude, JCO redline).
QC checks:
- Hold-list search returns zero hits in the transmitted PDF.
- No DRAFT, highlight, markup layer or internal note in the submittal; one font.
Source cards: SILVERBELL-011, BARNETT-010, VALENCIA-020

### QC-C07 Report values trace to native output and completed runs
qc_rule | QC rule (05_QC_Rules) + update drainage-report-build sec. 3-4 (and pchydro-hydrographs QC direction) | score 4.5 | hours 3.5 | cards 6 | projects 6 (RKN, SAHPARK, CALFIRE, ELTORO, SAH, VALENCIA) | confidence high/medium
Trigger: Before issuing any memo/report whose text or tables quote program results (PC-Hydro peaks, CulvertMaster/HY-8 headwater, HMS/RAS/FLO-2D results); assembling a native-output appendix; narrative written while model queues are still running; reusing a calc workbook for report tables; reviewing a report that uses PC-Hydro.
Steps (merged):
1. Re-run every CP natively in PC-Hydro and keep the printout PDF; compare each report Q (2, 10, 100-yr) to native output; require max abs diff 0.0 cfs.
2. Tie every result in the text to a line of the program output: Q, HW elevation, inlet vs outlet control, barrel length, slope, outlet velocity. Do not report a soffit or crown elevation as computed headwater.
3. Check assumptions cite the same governing cross section/source used to size the structure.
4. Native output appendix: print or export from the program (HMS summary/results tables, RAS summary output). If results must be extracted from XML/HDF, title the PDF as an extracted summary and keep the program file in the record.
5. Build a run matrix (model x storm x RP x scenario) from SUMMARY.OUT / HDF completion, not from the plan; check every narrative sentence naming storms, return periods or scenarios against it; state plainly which return periods were run in each model.
6. PC-Hydro version: state the version; the version in text matches the version on output sheets throughout; when reviewing others' work, ask why the latest version was not used or require justification.
7. Calc workbook reuse: list cached errors per sheet (#REF!, #VALUE!) and which sheets feed the report; flag values pasted from FlowMaster that do not recalc; check numeric cells holding text; relink external links to office drives to local copies; confirm which copy (revert, overwrite, 100 pct, signed-sealed) is current.
8. Record the native-vs-report comparison table in the QC document; state that this automated check does not replace the T2 independent check.
9. Check section numbering runs without gaps and no sentence is truncated.
Gotchas:
- Results assembled from web-page scraping can drift from native output after input changes; the cross-check found nothing here (106 EX, 51 PR CPs matched) but is the only proof (RKN-005, claude, QC script record).
- Rev B text gave HW 2,707.75 ft (the soffit) under outlet control; CulvertMaster output shows HW 2,707.50 ft and Entrance Control (SAHPARK-015, claude, session record vs program output).
- Barrel length 65.99 ft in text vs 65.00 ft in the run; summary sentence truncated after "outlet control, 3." (SAHPARK-015, claude, session record vs program output).
- Assumption A-2 cites one source cross section while the culvert is sized from another; section 4.4 missing between 4.3 and 4.5 (SAHPARK-015, claude, session record vs program output).
- HMS results XML and RAS compute messages were re-typeset in Courier and listed as native output; the checklist marked it Addressed (CALFIRE-015, claude, session record).
- Narrative said 2- to 100-yr storms were run for both durations; HMS and RAS did, but FLO-2D finished only 100-yr runs because the queue stalled (SAH-017, claude, assembly report + run logs; see SAH-003).
- RAS 2- to 50-yr plans finished after the 30 pct draft date (SAH-017, claude, assembly report + run logs).
- Reviewed report cited one PC-Hydro version in text and an earlier one on a later page (ELTORO-010, claude, reviewer comments on reference report).
- 215 cached errors across 5 workbook versions; only some were in active report sheets (VALENCIA-014, claude, workbook audit).
- Revert, overwrite, 100 pct and signed-sealed workbook copies differ; confirm which is current before use (VALENCIA-014, claude, workbook audit).
QC checks:
- Native-vs-report table: every CP and RP, max abs diff 0.0 cfs.
- Every quoted hydraulic result maps to an output line; control type matches.
- Native-output appendix pages are program printouts or are titled "extracted summary".
- Run matrix attached; narrative RP/scenario statements match it.
- Software versions in text = versions on printouts.
Source cards: RKN-005, SAHPARK-015, CALFIRE-015, ELTORO-010, SAH-017, VALENCIA-014

### QC-C08 Internal consistency and numeric check
qc_rule | QC rule (05_QC_Rules) | score 24.0 | hours 4.0 | cards 2 | projects 2 (BARNETT, TANGERINE) | confidence high
Trigger: Before any multi-author report or draft goes to senior review or issue.
Steps (merged):
1. Recompute every percent or ratio cited in text from the table values; use one rounding rule.
2. Check funding/scope statements agree across sections (e.g. grant applications vs "no federal funding anticipated").
3. Check cost-category percentages sum to 100 pct.
4. Check structure counts match everywhere and cite the source (e.g. ADOT record drawings).
5. Check every crossing on the exhibits appears in the crossing table and vice versa.
6. Check volumes and flows quoted in different sections refer to the same basis.
7. Check statements on a figure or map do not contradict each other or the text.
8. Check heading hierarchy (parallel alternatives at the same level, no duplicate titles) and that the document states its milestone (15 or 30 pct) up front; if schedule is discussed include a milestone table or Gantt.
9. Search for doubled qualifiers and filler ("approximately about"), stray characters and placeholders.
Gotchas:
- Funding contradiction, cost percentages and section heading structure were flagged at 15 pct and still unchanged at 30 pct (BARNETT-009, claude, agency/reviewer redlines).
- A crossing shown on exhibits was missing from the crossing table (BARNETT-009, claude, agency/reviewer redlines).
- Text cited a 68-69 pct increase while the table gave +67.7 pct and +68.9 pct; reviewers asked for consistent rounding (TANGERINE-014, claude, mock review).
- Draft text read "approximately about 1,464 acres" (TANGERINE-014, claude, mock review).
- JCO on another project's report: two map statements could not both be true; check this before the document reaches review (TANGERINE-014, claude, JCO redline).
QC checks:
- Percent/ratio recompute table; exhibit-vs-table crossing list match; cost percentages sum to 100.
Source cards: BARNETT-009, TANGERINE-014

### QC-C09 Narrative text: carried-over text, framing, floodplain status
qc_rule | QC rule (05_QC_Rules); FEMA items to jurisdiction add-on drainage-report-build/fema; Town of Sahuarita annexation note to drainage-report-build/sahuarita | score 29.0 | hours 4.0 | cards 3 | projects 3 (VALENCIA, TANGERINE, PHXZOO) | confidence high
Trigger: Report narrative started from another project's report; planning-level or rezoning report on a contested site; any memo, proposal background or agenda describing FEMA zone, return periods or floodplain authority.
Steps (merged):
1. Search for remnant names of other roads, washes or projects; remove old-job footers.
2. Update design criteria to this project (lane count, storm event per system type); use only design return periods in the governing standard (2, 10, 100, 500-yr as scoped).
3. Verify statements on ditches, profile changes and ponding with the roadway team before keeping them.
4. Describe all major wash crossings including side streets; add a location map and typical section.
5. Floodplain: summarize FIRM panels (map number, panel, effective date, zones) for the project limits; include both the effective and the soon-to-be-effective panel and say which governs at submittal; read the zone at the actual alignment, no blanket zone statement.
6. State whether the site is within or will be annexed into town limits, since that sets the floodplain authority; when a later executed scope reverses an earlier floodplain statement, note the reversal in the coordination record.
7. Concept reports: label concept-level on the title page and executive summary; state what it does not do (no entitlement, no new hydrology, no permitting); repeat the not-an-entitlement statement in the executive summary, public-concern section and conclusions.
8. Replace unearned compliance words (conforms, adequate, decisively) with "is structured to meet, to be confirmed in the master drainage report"; use "community concern" and "technical response" instead of "opponents"; add a concern status table (addressed, partial, deferred).
9. Keep objective findings separate from yield or land-plan recommendations; say "maintains principal flow paths and boundary discharge locations to the extent practicable" rather than "preserves natural drainage".
10. Add a plain-language residual flood risk box and a water-supply box when those concerns exist.
Gotchas:
- Draft named the wrong project and another road, and claimed roadside ditches and profile changes not in the design (VALENCIA-024, claude, JCO redline).
- Reviewers flagged advocacy tone and overstated conclusions in five comments (TANGERINE-012, claude, mock review comments).
- Text said Zone D while the road sat in Zone X and mapped floodplain (PHXZOO-007, claude, JCO redline).
- A 200-yr flow label was an error tracing back to a 100-yr value (PHXZOO-007, claude, JCO redline).
- JCO redlines caught all four floodplain/status items in a staff draft; the author should check these before review (PHXZOO-007, claude, JCO redline).
Jurisdiction add-ons:
- FEMA: effective vs pending FIRM panel statement and which governs at submittal (PHXZOO-007).
- Town of Sahuarita: state town-limits/annexation status as it sets floodplain authority (PHXZOO-007).
QC checks:
- Search hits for prior project names = 0; return periods only from governing standard; FIRM summary table present.
Source cards: VALENCIA-024, TANGERINE-012, PHXZOO-007

### QC-C10 Existing-conditions and approved-plan verification
qc_rule | QC rule (05_QC_Rules); procedure input to agent due-diligence-researcher | score 53.5 | hours 9.0 | cards 5 | projects 4 (BARNETT, ELTORO, STARVALLEY, SAH) | confidence high/medium
Trigger: Existing-conditions, crossings and recommended-features sections where development is active; using master-plan or approved-plan structures in an existing-condition model; modeling an existing crossing with as-builts; any model with culvert sizes, berms or grading assumed from aerials, NBI or terrain.
Steps (merged):
1. Confirm with the agency which crossings are already constructed and remove them from proposed-structure lists, exhibits and phasing text; confirm road closures and drop structures tied to closed roads; check access items against current plans.
2. Check each master-plan structure against aerials, as-builts and site visit before modeling; flag structures proposed but never built and those built in a different form (pipe instead of bridge).
3. Confirm map CP labels match their tabulated location; note any figure missing from a scanned copy and request it.
4. As-built crossings: compare modeled max WSE to the as-built road centerline high point; match culvert Q100, n and entrance loss to as-built design values and note them on the plan sheet; compare with field-observed overtopping.
5. Approved plans without as-builts: recompute basin stage-storage from the supplied grading surface and compare with the approved report; rerun culvert and storm-drain checks in HY-8 or by hand at the county design flow and compare headwater to allowable; keep approved geometry and record each difference with numbers in the judgment memo after EOR decision.
6. Log every assumed structure, berm and grading edit with ID, basis, source, verify-by and X/Y (CSV + GIS layer); sort by influence (berms and culverts near the road first) and verify by survey, record drawings or field review; mark Verified Yes/No and report the unverified count in the assumptions appendix.
7. List every effective FEMA zone in the study area the first time zones are listed, and match later lists (see C09).
Gotchas:
- About 12 agency comments on a 15 pct DCR were facts that had changed since base data was gathered (crossings built by development, a road removed from service); the zone-list fix was made in one section but not the earlier one (BARNETT-005, claude, agency comments).
- Reviewer markups on a prior basin study: culvert never constructed; a pipe exists where a bridge is shown; a CP shown at a location tabulated under another label; a referenced plan sheet missing from the scan (ELTORO-008, claude, reviewer comments on prior study).
- Modeled WSE 63.70 vs centerline high point 63.62 showed overtopping by about 0.1 ft, consistent with reports; as-built culvert values Q100 99 cfs, n 0.012, Ke 0.5 (ELTORO-014, claude, as-built review comments).
- Supplied basin surface gave 15.71 ac-ft at 2548.69 ft vs 18.10 ac-ft reported; storm-drain inlet water level rose from 2544.09 to 2545.00 ft with full outlet loss, above inlet ground (STARVALLEY-023, claude, EOR decisions via Codex session).
- Assumption log held 226 items (153 berms/embankments, 20 assumed culverts, 12 culvert dimensions); none verified when the 30 pct draft was issued (SAH-014, claude, assumption log).
- Berm presence changed results enough that a NoBerm scenario was run for 3-hr and 24-hr storms; berm assumptions are high-influence (SAH-014, claude, assumption log).
QC checks:
- Assumption log unverified count stated in report; high-influence items verified before issue.
- Approved-vs-recalculated table (storage, HW vs allowable) with EOR decision reference.
Source cards: BARNETT-005, ELTORO-008, ELTORO-014, STARVALLEY-023, SAH-014

### QC-C11 Structure tables match latest signed-sealed plans
qc_rule | QC rule (05_QC_Rules) | score 366.0 | hours 10.0 | cards 5 | projects 2 (VALENCIA, TANGERINE) | confidence high/medium
Note: score driven by agency redline counts (VALENCIA-017 r60, VALENCIA-018 r70 count individual redlined values).
Trigger: Report culvert/driveway, inlet, storm drain or channel tables, outlet protection notes or pavement drainage maps are written or updated after plan revisions; report cites existing or planned roadway cross-drainage structures.
Steps (merged):
1. Pull values from the latest signed-sealed plan set (and latest roadway plans/drainage report for adjacent projects), not an older DCR; cite the plan sheet for each value.
2. Culverts: check barrel count, size, material, length, inverts, slope, Q100 and HW for every culvert; each alternative row uses its own HW and velocity.
3. Outlet protection notes agree with the plan outlet protection table and riprap at each outlet.
4. Inlets: renumber CB/SC to the latest plans; show removed CBs as removed, add missing ones; update station and side; no duplicate IDs; update appendix map labels to the same numbers.
5. Modified catch basins: record actual sump length and wings; scupper openings are not wing-length based; note non-PAG standards used (e.g. ADOT C-15.20 curb-opening CB). If opening length changes, rerun capture.
6. Storm drain: each line lists upstream structure, length, slope, size/material, Q, HGL and velocity; add missing upstream lines; match length, slope and size to plan profiles and model output pages; mark existing lines receiving added flow and check them.
7. Channels: narrative for each proposed channel (location, tributary watersheds, inflow structures, outlet); add to the channel table, numbered consistently with appendix calc labels; analyze an existing receiving channel that gets added flow; show freeboard and provided depth separately from normal depth.
8. Crossing table lists every existing, planned and proposed crossing with design Q, capacity and status; the adequacy statement in the table agrees with the text.
Gotchas:
- Redline found inverts off by 0.01-0.19 ft, a 0.64 pct slope rounding mismatch, and alt 1 HW/velocity used for alt 2 (VALENCIA-016, claude, agency redline).
- Pipe callouts changed to 2-18 in, 2-24 in, 2-19x30 and 2-29x45 HERCP per plans (VALENCIA-016, claude, agency redline).
- A note conflicted with the outlet protection table (VALENCIA-016, claude, agency redline).
- About 40 CB/SC numbers and stations to change; CB13, CB32, SC11 missing; duplicate CB24 (VALENCIA-017, claude, agency redline).
- Changing opening length changes capture values; rerun, do not just edit the label (VALENCIA-017, claude, agency redline).
- Two upstream lines missing from the table; material listed as RCP where plans show CPP or HERCP (VALENCIA-018, claude, agency redline).
- Redesigned runs (split into 2-24 in, 36 in at 0.70 pct) not reflected in appendix output (VALENCIA-018, claude, agency redline).
- Four channels without description and an existing receiving channel not analyzed (VALENCIA-019, claude, agency redline).
- Arch pipes removed from the project were still in the table; an existing 30 in CMP shown as proposed (VALENCIA-019, claude, agency redline).
- Table said no crossing was undersized while the next paragraph flagged upsizing (TANGERINE-013, claude, mock review).
- Later roadway plan markups replaced DCR structures (girder bridges and CBCs became hybrid boxes, RCPs eliminated, washes consolidated), so DCR sizes were out of date (TANGERINE-013, claude, mock review + roadway plans).
QC checks:
- Table-to-plan diff (sheet cited per value); zero duplicate inlet IDs; table IDs = map labels = appendix calc labels.
- Appendix output pages regenerated after any redesign.
Source cards: VALENCIA-016, VALENCIA-017, VALENCIA-018, VALENCIA-019, TANGERINE-013

### QC-C12 Table formatting, appendix structure and package completeness
qc_rule | QC rule (05_QC_Rules) + update drainage-report-build sec. 2 (tables) and sec. 4 (deliverables) | score 29.0 | hours 3.5 | cards 3 | projects 2 (VALENCIA, ELTORO) | confidence high
Trigger: Report tables and inlet calc summaries; organizing hydrology and hydraulic appendices; reviewing any report that will be reused as the hydrology basis for later projects.
Steps (merged):
1. One thin single border style on all tables; center content.
2. Print summaries from Excel (or the program), not screenshots (no green error arrows).
3. Stations for every scupper; footnote N/A spread entries; asterisk note for blank areas or untouched offsite areas.
4. Provide an existing-conditions summary when a proposed one is shown.
5. Appendices: bookmarks and sub-section dividers; storm events ordered 2, 10, 100-yr with matching headings; group offsite hydrology by event, not by watershed size.
6. Remove analyses the agency asked not to show and add a short statement why (e.g. offsite washes unchanged, FEMA mapped with larger flows); update appendix names when a section is removed; fill or remove sections lacking references.
7. Package completeness: include HEC-RAS (and other) model files with the report; include excerpts of referenced reports in the appendix.
8. Every watershed and CP on the maps appears in the tables; study limits shown on each map; state where any split flow occurs and how it is routed; road and landmark references point to the right feature.
Gotchas:
- Border, color and highlight fixes were marked on 6 table pages (VALENCIA-021, claude, JCO redline).
- Offsite wash and FEMA comparison sections had to be removed at agency request, and re-added text was flagged later (VALENCIA-022, claude, JCO redline).
- Missing model files and appendix excerpts made later reuse of the report flows harder; reused flows needed reconciliation years later (ELTORO-013, claude, reviewer comments on reference report).
- A watershed on the map was missing from a table (ELTORO-013, claude, reviewer comments on reference report).
QC checks:
- Map-vs-table watershed/CP list match; model files and reference excerpts in package; appendix bookmarks resolve.
Source cards: VALENCIA-021, VALENCIA-022, ELTORO-013

### QC-C13 Drainage map symbology
qc_rule | update drainage-report-exhibit-standards sec. 3 (checked by agent exhibit-reviewer) | score 0.8 | hours 0.4 | cards 1 | projects 1 (RKN) | confidence medium
Trigger: Any existing or proposed drainage map exhibit.
Steps (merged):
1. Pink watershed boundaries, cyan dashed flowlines with arrows, sheet-flow arrows, CP symbols by type, watershed labels with CP number and Q100.
2. Show HEC-HMS subbasins distinctly from PC-Hydro watersheds.
3. Full aerial background; text >= 0.1 in.
Gotchas:
- The first existing drainage map lacked the standard symbology and had to be rebuilt by patch (RKN-013, claude, session record).
QC checks:
- Symbology checklist per exhibit before compile; HMS vs PC-Hydro basins distinguishable in legend.
Source cards: RKN-013

### QC-C14 Channel, outlet and erosion protection review
qc_rule | QC rule (05_QC_Rules) | score 13.0 | hours 2.0 | cards 2 | projects 2 (ELTORO, CAMPBELL) | confidence high
Trigger: Reviewing or writing channels, culverts, basin outlets, riprap, apron or channel protection tables in a drainage report or memo.
Steps (merged):
1. Show max flow depth and required freeboard to demonstrate capacity; where a headwater elevation is reported, state whether freeboard is included.
2. Velocity and scour depth for each channel reach; state whether velocities come from the 2D model or normal depth and confirm they match RAS.
3. Outlet protection design for culverts and basin outlets; erosion protection at major wash crossings; check high outlet velocities with HY-8.
4. Aprons over 10 fps carry a wire-tied note; flag segments near the no-riprap threshold.
5. Edge protection: D50 6 in, at least 5 ft from pavement edge or to toe of fill.
6. Table of toe-down depths for each lot or bank protection reach; add a station-to-station column for plan use.
Gotchas:
- A final memo reported a headwater elevation without freeboard; the label implied it was the design top (ELTORO-012, claude, reviewer comments on reference report).
- Velocities in protection tables did not match the RAS model (CAMPBELL-019, claude, JCO redline).
- HEC-14 plunge basin sheet used a single barrel in error (CAMPBELL-019, claude, JCO redline).
QC checks:
- Protection-table velocity = RAS/HY-8 value at same station; barrel count in HEC-14 sheets = plans.
Source cards: ELTORO-012, CAMPBELL-019

### QC-C15 Street drainage, spread and scupper review
qc_rule | QC rule (05_QC_Rules); Town of Sahuarita-specific values to jurisdiction add-on drainage-report-build/sahuarita once confirmed | score 6.0 | hours 1.0 | cards 1 | projects 1 (ELTORO) | confidence high
Trigger: Reviewing street drainage and scupper or curb opening design in a subdivision or roadway drainage report.
Steps (merged):
1. Require the 10-yr max spread between curbs.
2. Require the clogging factors used to be stated.
3. Scuppers analyzed and designed in sump condition, not on grade with bypass, unless stated otherwise; require splashover length or a note that the opening is in sump.
4. Demonstrate ROW velocities below 3 fps.
5. Check tabulated Q at each scupper against the hydrology (design frequency matches).
Gotchas:
- Several scupper tables omitted the design frequency and clogging assumption; a Q100 value appeared where a Q10 was expected (ELTORO-011, claude, reviewer comments on reference report).
Jurisdiction add-ons:
- Card applies to Pima County RFCD and Town of Sahuarita; confirm which values (10-yr spread, 3 fps ROW velocity) come from which manual before splitting into add-ons (ELTORO-011).
Source cards: ELTORO-011

### QC-C16 Crossing concept geometry and restricted-ROW layout
qc_rule | new skill crossing-concept-layout + QC rule (05_QC_Rules); Pima County / ADOT details as add-on | score 15.0 | hours 5.0 | cards 2 | projects 1 (SILVERBELL) | confidence high
Trigger: Any proposed culvert or bridge crossing concept; culvert or roadway concept along a frontage where new ROW or downstream easement is not available.
Steps (merged):
1. Ask which frontage is restricted before extending outlets, grading or easements on that side.
2. Shift the road alignment away from the restricted side; use retaining walls in place of fill slopes; fit a minimum section inside the stated usable envelope; check footprint overlap against current county parcel geometry (target 0 sq ft).
3. Allow an upstream drainage easement only where restricted; raise outlets to tie to EG inside ROW and dissipate inside the box.
4. Extend barrels slightly beyond actual roadway fill toes; ADOT headwalls and wingwalls.
5. Drop inlets at 6:1 or flatter; outlet grading with positive downstream flowline; outlet riprap where ROW allows.
6. RCBC top slab 1.0 ft for cover checks.
7. Bridge alternatives span the floodplain with low chord at least 2 ft above computed Q100; size from the full existing flood envelope.
8. Carry one common geometry through CAD, 1D/2D RAS and renderings.
Gotchas:
- Agent extended downstream grading (378 ft to reach EG at one culvert) before the restriction was known; JCO direction reversed it (SILVERBELL-003, claude, JCO direction).
- Restricted parcel data may be split; check the current record, not the plan label (SILVERBELL-003, claude, JCO direction).
- Do not interpret a county restriction attribute field as a development restriction (SILVERBELL-003, claude, JCO direction).
- Old DCR culverts stopped inside the fill; lengths increased once toes were checked (SILVERBELL-004, claude, session record).
- One barrel axis extracted at 844.6 ft from a bad source trace; corrected to 138.6 ft from the sheet barrel edges; flag any length far outside its neighbors (SILVERBELL-004, claude, session record).
- Short-span bridge trial failed in 1D because flow bypassed over adjacent lower ground (SILVERBELL-004, claude, session record).
Jurisdiction add-ons:
- Pima County / ADOT: ADOT headwall/wingwall standards, 6:1 drop inlets, RCBC slab 1.0 ft (SILVERBELL-004); confirm source manual sections.
QC checks:
- Footprint overlap with restricted parcels = 0 sq ft; barrel lengths reach fill toes; outlier length check.
Source cards: SILVERBELL-003, SILVERBELL-004

### QC-C17 Footprint, ROW, easement and trial-grading screening
skill + qc_rule | new skill grading-footprint-screening | score 11.0 | hours 5.0 | cards 3 | projects 3 (CAMPBELL, SILVERBELL, NORTHLOOP) | confidence high/medium
Trigger: Screening impact areas inside a railroad/road corridor from parcel data; building corridor assemblies from scripted section data in Civil 3D; building trial proposed grading on a model grid (raised pad, new channel).
Steps (merged):
1. Build polygons from closed parcel line features before raster screening; state that parcels screen only and do not certify legal ROW; restate earlier numbers if a line burn was used.
2. Civil 3D: mirror assembly X when converting section offsets (positive Civil 3D offset is opposite the section data sign); add an explicit outer boundary to the corridor surface; do not trust the automatic dynamic boundary.
3. Export the surface and check footprint overlap against restricted parcels before using it for hydraulics; mark superseded exports explicitly.
4. Overlay recorded permanent and temporary easements; report cut/fill area and max depth inside each.
5. Screen adjacent cell pairs for new slopes steeper than 3:1 (about 35.3 pct), especially where an inherited channel is clipped.
6. Compare max fill depth with the geotech settlement basis; compare infiltration test locations with basin locations.
7. Report earthwork as screening quantities (no shrink, swell or stripping).
Gotchas:
- Earlier screening burned only one-pixel parcel boundary lines, understating corridor areas (CAMPBELL-022, claude, findings record).
- First TIN overlapped the restricted parcel by 36,430 sq ft from a side flip and invalid boundary; rebuilt as a fixed corridor (SILVERBELL-008, claude, CAD QA record).
- A stale exported FG CSV was nearly used for hydraulics (SILVERBELL-008, claude, CAD QA record).
- Wall solid extrusion along 3D paths threw eNonPlanarEntity; use planar profiles per segment (SILVERBELL-008, claude, CAD QA record).
- Carried-forward channel cut about 0.10 ac of permanent water easement (up to 2.7 ft) (NORTHLOOP-017, claude, screening record).
- Clipping the old channel left 7 cell pairs up to 0.87 ft/ft; one scenario mixed pad and bad tie-in effects (NORTHLOOP-017, claude, screening record).
- Pad needed about 12.7 ft fill while geotech covered about 12 in; infiltration tests were not at the basin (NORTHLOOP-017, claude, screening record).
QC checks:
- Overlap areas reported for restricted parcels and easements; slope screen result; fill depth vs geotech basis.
Source cards: CAMPBELL-022, SILVERBELL-008, NORTHLOOP-017

### QC-C18 Storm drain HGL routing and WQ retention below outlet
qc_rule | QC rule (05_QC_Rules) | score 5.0 | hours 5.0 | cards 2 | projects 1 (HOMEWOOD) | confidence high
Trigger: Any storm drain model used to show HGL freeboard, surcharge or tailwater effects; subsurface infiltration gallery or CMP retention system used for water quality volume.
Steps (merged):
1. Check link routing is Dynamic/Hydrodynamic, not Kinematic Wave; use a short routing step (1 s used) and entrance/exit losses (0.5 used).
2. Report minimum freeboard to rim per structure against the criterion (0.5 ft below rim/grate in the Placer case).
3. Compute storage below the lowest outlet invert from the stage-storage curve; compare to WQV.
4. Model outlets exactly as drawn on the plan/detail sheets, not idealized weirs.
5. Route the WQ event (85th percentile 24-hr in the Placer case) with and without infiltration and report the volume leaving untreated.
6. Fix by raising the outlet invert or adding a weir plate/riser, then rerun the WQ event and the design events (2-yr 24-hr and 50-yr 1-hr in the Placer case).
Gotchas:
- SSA model on kinematic wave reported HGLs that cannot show backwater or tailwater; the HGL table could not support the criterion (HOMEWOOD-006, claude, independent review).
- 72-in gallery with 12-in outlet 3.0 ft above bottom retained 1,893 of 3,763 cf; 30-in gallery with outlet at invert retained almost nothing (HOMEWOOD-007, claude, independent review).
- Model weir at 4.47 ft and at pipe crown did not match the drawn outlets, so the model overstated retention (HOMEWOOD-007, claude, independent review).
- As drawn, 32-68 pct of the WQ event inflow left the site untreated (HOMEWOOD-007, claude, independent review).
Jurisdiction add-ons:
- Placer County CA: 0.5 ft HGL freeboard below rim/grate; 85th pct 24-hr WQ event; 2-yr 24-hr and 50-yr 1-hr design events (HOMEWOOD-006, HOMEWOOD-007).
QC checks:
- Routing method = dynamic wave whenever HGL is reported; WQV <= storage below lowest outlet invert as drawn. Consistent with existing skill rule "first flush below the outlet invert (raise the outlet)".
Source cards: HOMEWOOD-006, HOMEWOOD-007

### QC-C19 East Placer SWQP hydromod forms and CMP gallery depth
qc_rule | jurisdiction add-on drainage-report-build/placer-county | score 3.0 | hours 2.0 | cards 2 | projects 1 (HOMEWOOD) | confidence high/medium
Trigger: Completing East Placer SWQP hydromodification Forms 4-2 / 4-3; placing a CMP or chamber gallery under pavement near groundwater.
Steps (merged):
1. Forms 4-2/4-3: use full site area (check against survey acreage); use 2-yr rainfall at Tt, not a 1-hr WQ depth; check the YES/NO answer agrees with computed post vs pre numbers; provided volume >= required, or substitute routed model results per SWQP Sec. 4.4.
2. Required depth FG to SHGW = pipe dia + bedding + min cover to bottom of structural section + structural section + required separation. Markup example: 36 in + 2 + 12 + 12 in = 5.17 ft + 2 ft = 7.17 ft; 24 in system 6.17 ft; 18 in system 5.67 ft.
3. Redo with 5 ft separation if the East Placer rule governs.
Gotchas:
- Form 4-2 used 111,270 sf for a 139,392 sf site, reported post 68.8 vs pre 31.3 cfs and still answered YES; Form 4-3 entered 850 cf vs 1,178 cf required (HOMEWOOD-014, claude, independent review).
- Under pavement, cover is measured to the bottom of the structural section, not to finished grade (HOMEWOOD-017, claude, agency/reviewer markup).
Jurisdiction add-ons:
- Placer County CA (East Placer / Lake Tahoe Basin / TRPA): all of the above; separation (2 ft vs 5 ft) unresolved, see conflict 8.
Source cards: HOMEWOOD-014, HOMEWOOD-017

### QC-C20 HEC-RAS unsteady input integrity (BC sets, names, precipitation)
qc_rule | QC rule (05_QC_Rules); enforced by agent model-run-supervisor | score 8.0 | hours 6.5 | cards 3 | projects 1 (ELTORO) | confidence high/medium
Trigger: Inflow BCs added, removed or renamed in one unsteady flow file of a multi-frequency 2D model; naming or scripting BC lines; before reporting results from a model described as rain-on-grid or hybrid.
Steps (merged):
1. Back up .g0x and .u0x with a timestamp before any scripted edit.
2. Name each BC line <source>-<CP>-<Q100> (e.g. R9-CP17-1422) so the name traces to one report row; check names are unique before saving (resolve duplicates and near duplicates such as CP-13 vs CP13).
3. After editing, list BC names and peaks for every .u0x (2-, 10-, 100-yr) and diff the name sets; each frequency has the same BC lines with frequency-specific hydrographs; none keeps a removed or duplicate line.
4. Re-check plans so each plan points to the intended .u0x.
5. Rain-on-grid: open each .u0x and confirm Precipitation Mode is not Disable and the gridded/point DSS path is filled; confirm the DSS named in build notes exists and pathnames match the plan frequency; check precip volume in the computation log volume accounting.
Gotchas:
- 100-yr flow file was rebuilt to 29 BCs while the 2-yr file kept the old 14 BCs including a removed CP and a duplicate; 2-yr results would not be comparable to 100-yr (ELTORO-002, claude, model file review).
- All saved flow files showed Precipitation Mode=Disable with empty DSS path while the notes said a 3-hr rain-on-grid was added (ELTORO-003, claude, model file review).
- Build checklist pointed to a _v2 precip DSS; only the unversioned DSS was in the build folder (ELTORO-003, claude, model file review).
- A later model version may sit in another project folder; check before concluding the runs were inflow-only (ELTORO-003, claude, model file review).
- Two BC lines were both labeled 23 (582 and 483 cfs); 483 cfs matches master plan CP-22, so one label is a typo (ELTORO-006, claude, model file review).
- Master plan inflows (767, 786, 1,658, 1,840 cfs) were added then replaced within one day; timestamped backups made it possible to trace which set was live (ELTORO-006, claude, model file review).
QC checks:
- BC name-set diff across all .u0x = empty; BC names unique; precip mode and DSS path verified; plan-to-flow-file map listed in run register.
Source cards: ELTORO-002, ELTORO-003, ELTORO-006

### QC-C21 2D results acceptance (volume, boundaries, artifacts) before reuse or reporting
qc_rule + skill | QC rule (05_QC_Rules); enforced by agent model-run-supervisor; pre-check added to hecras-result-rasters step 4 | score 80.5 | hours 14.5 | cards 3 | projects 3 (CALFIRE, CAMPBELL, PHXZOO) | confidence high/medium
Trigger: Any HEC-RAS 2D or coupled 1D/2D run reports "Finished Successfully"; reporting 2D results at a road crossing; reusing an adjacent project's 2D model, plans or memo as the existing-condition basis.
Steps (merged):
1. Read native global and per-area Volume Accounting before any mapping; stop processing above 0.1 pct global error; check regional errors for large opposing values that cancel in the global number.
2. Diagnose with short (6 hr) one-control runs from CLOSED source inputs: baseline, tolerance only, BC volume check only, coupling iterations only; confirm the baseline reproduces wetting of the full run before trusting copied-input diagnostics.
3. Do not publish rejected full events; keep the earlier accepted comparison as the reported basis.
4. Confirm an outflow BC exists (normal depth at the downstream mesh limit).
5. Check the flow split: when most flow exits a boundary rather than through the structure, the boundary is driving the answer; extend the domain to the receiving stream and refine the mesh at problem cells before drawing conclusions on overtopping.
6. A metric identical across all events, or identical 10- and 100-yr max WSE in any zone, is an extraction error or numerical artifact; sample the WSE result, not terrain or a fixed cell.
7. Reused models: check mesh cell size range against the 30 ft LMW guidance and breaklines on channel, road and berms; match modeled culverts (barrels, inverts, length, slope, station) to latest plans and as-builts; confirm existing geometry removes proposed crossings (otherwise the WSE change map is not a no-rise screening); check terrain VRT source order, spurious modification-raster elevations, BC labels and velocity spikes at wet-dry faces.
8. Log interface items with the adjacent design team (entry culvert location and size, berm raise or removal, grading tie-in, CAD sharing).
Gotchas:
- Full 20-hr existing/proposed pair finished with 8.6 pct volume error; the native success message is not acceptance (CAMPBELL-002, claude via Codex session).
- Changing coupling iterations and BC volume check together suppressed nearly all inflow (99.99 pct loss); change one control at a time (CAMPBELL-002, claude via Codex session).
- Tighter 0.001 ft tolerances alone did not improve balance (4.03 vs 4.02 pct) (CAMPBELL-002, claude via Codex session).
- Face-only regional residuals omit internal point and structure sources; they are not complete mass closure (CAMPBELL-002, claude via Codex session).
- Max HW along the road was 297.15 ft for every event 10- through 100-yr: an extraction error that the open-items memo did not flag (CALFIRE-010, claude, run log + open-items memo).
- Culvert passed only 42 of 261 cfs while 175 cfs left through the west normal-depth boundary (CALFIRE-010, claude, run log + open-items memo).
- A closed domain fills and shows false 15-28 ft depths (PHXZOO-006, claude, model review note).
- Five critical or major defects in an adjacent road model were found only while making exhibits: no outflow BC, artifact strip at the crossing, cells 1.4 sq ft to 143 ac, 2 vs 3 barrel mismatch, existing geometry kept proposed culverts (PHXZOO-006, claude, model review note).
- Road alignment interacts with site drainage: a raised road acting as a berm shifts failure responsibility; carry as an open cost comparison (PHXZOO-006, claude, model review note; project item, see open items).
QC checks:
- Volume accounting table (global and per area) with pass/fail at 0.1 pct; outflow BC present; boundary vs structure flow split; event-to-event result variation check; reused-model screening list complete.
Source cards: CALFIRE-010, CAMPBELL-002, PHXZOO-006

### QC-C22 FLO-2D run checks (ERROR.CHK, stall watchdog, placeholder TOPO)
qc_rule | QC rule (05_QC_Rules); enforced by agent model-run-supervisor; FEMA CLOMR note to add-on drainage-report-build/fema | score 21.0 | hours 13.0 | cards 3 | projects 2 (SAH, STARVALLEY) | confidence high/medium
Trigger: Every FLO-2D run built by script before tables or exhibits are made; any unattended FLO-2D run, especially after terrain edits; any proposed-conditions TOPO.DAT received from others or edited for grading.
Steps (merged):
1. Read ERROR.CHK after the first short test run; list each ERROR and WARNING by file; record the result in the run register; do not start the production queue with open errors.
2. HYSTRUC.DAT: no inflow node used by two structures; repeated outflow nodes need a D-line limit or separate nodes.
3. LEVEE.DAT: no grid element next to a levee higher than the levee crest; resample crest from the fine DEM along the berm line or drop the segment.
4. Record expected run time from the matching base run; every 15 min read SUMMARY.OUT simulation time and TIME.OUT; stop the run if simulated hours per wall hour drops below 25 pct of the base run or one grid element controls the time step for many intervals.
5. Fix the controlling cell (TIME.OUT element): check elevation, n value and levee/structure at that cell; rerun. Do not let queued jobs wait without a limit on a stalled one.
6. Proposed TOPO: search for large patches of cells at one constant elevation; compare to the design TIN and to existing ground inside grading limits (mean, median, std, pct within 0.5 ft); check max step between adjacent cells at the regrade boundary and smooth artificial steps.
Gotchas:
- A MineFill 100-yr run reported 89.8 h run time vs 0.63 h base; TIME.OUT showed one grid element limiting every interval; it ran four days unattended (SAH-003, claude, run logs).
- Its queue never reached the 2-, 10-, 25- and 50-yr 3-hr pairs and the LOWER run, so FLO-2D results exist only for the 100-yr storm (SAH-003, claude, run logs).
- Every UPPER run (base, NoBerm, MineFill) carried the same HYSTRUC inflow-node error and dozens of levee-crest-below-grid warnings; never fixed before report runs (SAH-006, claude, ERROR.CHK).
- Berm levees were built from DEM sampling at 40 ft, so crests fell below adjacent cells (SAH-006, claude, ERROR.CHK).
- 3,072 interim cells sat at one elevation (2555.77 ft), 6-30 ft above ground, driving a 34.6 ac cluster of dWSE over 1 ft (STARVALLEY-015, claude, change memo).
- Regrade-boundary steps up to 7 ft were reduced to 2.5 ft and 185 residual placeholder cells replaced (STARVALLEY-015, claude, change memo).
QC checks:
- ERROR.CHK clean (or each warning dispositioned) in run register; run-rate watchdog log; constant-elevation patch scan result for proposed TOPO.
Source cards: SAH-003, SAH-006, STARVALLEY-015

### QC-C23 Record-plan reading: keep WSEL, crest, invert, banktop separate
qc_rule | QC rule (05_QC_Rules); used by agent due-diligence-researcher and local plan-reading models | score 6.0 | hours 2.0 | cards 1 | projects 1 (EKOS-LOCAL) | confidence high
Trigger: Reading detention basin, channel or outlet sections from record plans for model inputs.
Steps (merged):
1. Identify dimension-arrow endpoints on the image before assigning meaning.
2. Subtract labeled WSEL and invert in the same datum and compare with any claimed depth.
3. Store WSEL, banktop, crest, apron size and utility inverts as separate fields.
4. Never take weir width from slab width or scale an NTS section.
5. Do not treat a historical 100-yr WSEL as an overflow crest, nor a DEM minimax path as a weir length.
6. Keep historical datum offsets unadopted until a common monument tie is verified.
Gotchas:
- Local model read a 10 ft arrow to banktop as 10 ft water depth; WSEL minus invert was 7.7 ft (EKOS-LOCAL-014, claude, EKOS supervisor corrections).
- Model conflated WSEL with a datum and with the crest (EKOS-LOCAL-014, claude, EKOS supervisor corrections).
- An 8-in adjacent utility was nearly taken as the basin outlet (EKOS-LOCAL-014, claude, EKOS supervisor corrections).
- Three misreadings were corrected by the supervisor; supervisor review of plan reads is required for local models (EKOS-LOCAL-014, claude, EKOS supervisor corrections).
Source cards: EKOS-LOCAL-014

### QC-C24 Connector development and recovery
agent | agent connector-developer (new; sub-role of model-run-supervisor) | score 24.0 | hours 4.0 | cards 1 | projects 1 (EKOS-LOCAL) | confidence medium
Trigger: A native-application connector (PC-Hydro, HMS, RAS, HY-8, Excel) fails or a new capability is needed.
Steps (merged):
1. Work only on isolated copies; hash originals and confirm unchanged at the end.
2. Qualify against retained benchmark evidence before any project use (HMS samples 28 statistics; RAS 1D 316 WSE and flow; RAS 2D 36,862 cells).
3. One patch at a time; rerun the regression set; keep failed patches and roll back on any regression.
4. Record what was qualified and what was not (e.g. solver replay does not qualify new geometry authoring).
5. Activate the connector in approved_actions only after tests pass; record a lesson and local replay.
Gotchas:
- Cloud built most connectors interactively at high quota; the local recovery loop was never implemented (EKOS-LOCAL-011, claude, EKOS runtime record).
- Repeating already-passed benchmarks was used as visible progress; do not rerun unchanged benchmarks (EKOS-LOCAL-011, claude, EKOS runtime record).
- Archive readback (HY-8) was briefly treated as fresh calculation; it is not (EKOS-LOCAL-011, claude, EKOS runtime record).
- Recurrence counted as 6 connectors (EKOS-LOCAL-011, claude, EKOS runtime record).
Source cards: EKOS-LOCAL-011
