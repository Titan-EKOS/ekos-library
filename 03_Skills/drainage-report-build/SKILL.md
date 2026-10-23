---
name: "drainage-report-build"
description: "Entry point for building or revising any drainage report, technical memo or DCR (Pima County, City of Tucson, Marana, Sahuarita, other AZ jurisdictions, FEMA cases, Placer County CA, Caltrans) to JCO's standards - jurisdiction and method selection, design basis, content rules, formatting, native model runs, build chain, appendices, compiled PDF, deliverables and the submittable gate; use at the start of every report build or JCO-markup revision, then load the jurisdiction add-on and the specialist skills it names."
version: "2.0.0"
status: "active"
function: "report-assembly"
jurisdiction: "all (add-ons: pima-county-rfcd, city-of-tucson, town-of-marana, town-of-sahuarita, fema, placer-county-ca, caltrans-california)"
tools_versions: "PC-Hydro 7.4 (web); HEC-HMS 4.13; HEC-RAS 6.6; FLO-2D Pro 26.02.25; HY-8 8.00; FHWA Hydraulic Toolbox; EPA SWMM 5.2 / Autodesk SSA 2024.1 (Placer); Word / Excel COM; Drainage Report Standard v0.3"
owner: "JCO"
replaces: "drainage-report-build v1 (account skill)"
---
# Drainage Report Build

## When to use
Any drainage report, TM, DCR or memo build, and any revision from a JCO markup or agency comments. This skill is the entry
point: it sets the order of work and the rules every report must meet, then hands each task to the skill or agent that owns
it. Jurisdiction rules (from the add-on) override anything here; decisions D01-D57 override older rules.

Who does what:
| Task | Owner |
|---|---|
| Assembly chain (workbook -> assemble_report.py -> post-process -> Word export -> compiled PDF) | `drainage-report-standard` |
| Exhibit sheet standards (sizes, ramps, base content, FIRM marking, text size) | `drainage-report-exhibit-standards` |
| Scripted exhibit series | `scripted-exhibit-sheets` |
| Writing narrative and tables | agent `report-writer`, always paired with agent `qc-reviewer` |
| Independent review, submittal audit, blind rebuild | agent `qc-reviewer` |
| Exhibit review | agent `exhibit-reviewer` |
| Prior studies, criteria research, jurisdiction confirmation | agent `due-diligence-researcher` |
| Long model runs, queues, rerun-all gate | agent `model-run-supervisor` |
| PC-Hydro | `pchydro-hydrographs` |
| HEC-HMS | `hechms-headless` |
| HEC-RAS 2D | `hecras-2d-models`; result rasters `hecras-result-rasters` |
| FLO-2D | `flo2d-model-runs` |
| HY-8 culverts | `hy8-native-runs`; legacy calc reruns agent `legacy-calc-reproduction` |
| Storm drain SWMM / SSA | `swmm-ssa-storm-drain` |
| Existing vs proposed comparison, rise maps | `impact-comparison` |
| FEMA CLOMR / LOMR packages and AD responses | `fema-clomr-lomr` |
| Groundwater reinfiltration | `groundwater-reinfiltration-sizing` |
| Letter or technical memo format | `drainage-technical-memo` |
| Agency comment-response log | `agency-comment-response` |
| Project intake, terrain, CRS log | `project-intake` |
| CAD base reissue | `cad-base-update` |
| Delivery package | `delivery-package-build` |
| Closeout lessons | `project-harvest` |

## Inputs
- Job folder in the Standard v0.3 layout (D56): 00_Admin, 01_Reference, 02_Data, 10_Record, 20_Working, 30_Report, 40_QC,
  50_Correspondence (issued sets in 30_Report/Issued); dates YYYYMMDD. If the job is not in this layout, run `project-intake` first.
- Scope / contract, parcel record and plat case, current plan set, survey, geotech report.
- The Standard workbook for the report (00_Admin) when the job uses the Standard.
- Prior studies and effective FEMA data (from `due-diligence-researcher`).
- For revisions: the marked-up PDF (JCO or agency) and the current editable source.

## Steps

### 0. Start: jurisdiction, governing manuals, method selection
1. Confirm the jurisdiction and the reviewing agency from the parcel record, plat case, GIS jurisdiction layer and the
   contract before choosing any manual. Where City vs County or Town vs County is unclear, record both readings and ask
   JCO. Flag any conflict with the project description.
2. Load the add-on(s) for that jurisdiction (table under Jurisdiction add-ons). More than one can apply (for example
   town-of-marana + fema).
3. Cite the current edition of each governing manual from the add-on; never cite a superseded document; cite the current
   version of any redone prior study. Keep the governing policies and program guides in `01_Reference\Agency` for citation.
4. Use the agency report outline as the section list when the agency publishes one. Keep every section; where nothing
   applies write "Intentionally left blank" with the reason.
5. Method selection (write it into the design-basis section and the workbook Setup):
   - hydrology method by watershed size and jurisdiction (add-on method table);
   - rainfall source, statistic, return period and duration;
   - design events for each system type (only the jurisdiction design set; anything else is labelled a sensitivity);
   - hydraulic tools from the licensed set (D16): FHWA Hydraulic Toolbox, HY-8, Civil 3D hydraulic tools, HEC-RAS 6.6,
     HEC-HMS 4.13, FLO-2D, PC-Hydro. FlowMaster and CulvertMaster are legacy (default, to confirm).
   - tabulate concentration points with method, area and design Q.
6. If the scope adopts published regional or effective hydrology instead of new hydrology:
   - read the agency supersession memo first and confirm which study governs at the site (study limits);
   - take Q10 / Q100 from the governing tables and state which engine's results are used where several are tabulated;
   - for an effective FEMA study read the TDN storm list and controlling-storm statement and confirm the package holds the
     rainfall-runoff model and inputs for every storm case; request missing cases before modelling;
   - an event outside the published set (for example 500-yr) needs written client agreement to a ratio method or is scoped
     as added service;
   - apply the study's technical guidance (mesh size etc.) to any new model; represent existing flow splits (berm
     breakouts) rather than assuming containment.
7. Plan deficiencies: where the design differs from or falls short of the current plan set, list each item and ask JCO how
   to handle it (revise plans, note in report, alternative design). Never assume plan revisions.
8. Open the one internal QC open-items document for the report in 40_QC (D44). Every assumption, decision item and
   missing input goes there, not into the deliverable text.
9. For a markup revision:
   - read the markup page by page (Bluebeam annotations) and build a response-log row for every comment
     (`agency-comment-response`; status per D45: Addressed / Partial / Assumed / Not Addressed / Cannot Determine / Stale;
     disposition in a separate field: incorporated / superseded / no change);
   - copy the marked-up PDF to the 40_QC T3 review folder as `<Job>_<ReportID>_<Milestone>_<YYYYMMDD>_JCO-Markup.pdf`;
   - edit builder inputs first, then rebuild; never run stale downstream builders.

### 1. Design basis and discharge traceability
1. Define each storm used (regional and local, design and FEMA) once, in existing conditions. Use the qualifier with every
   reference ("10-yr regional", "100-yr local"); no synonyms.
2. Build a design discharge table: source (cross section, culvert record or CP id), location, Q10, Q100, governing
   duration, use (crossing vs parallel flow), method. Every Q in text, tables and captions matches it: one value, one
   qualifier, one source per flow.
3. Restate the design basis in the design section with the same wording and numbers. Keep the summary flow equal to the flow
   that sized the structure (approach flow is not crossing flow).
4. Check every map caption and table title against the storm of the values shown.
5. Allowable velocity is the velocity permitted over a lining or soil, not "the velocity of the soil".
6. Critical facilities (substation, BESS, utility, emergency facility) and any site needing a 500-yr WSE (D22):
   - confirm the critical-facility designation and requirement with the jurisdiction (improvements above the 500-yr WSE
     plus any freeboard from the add-on);
   - 500-yr WSE source, in this order: FIS 0.2% profile only where its cross sections bracket the site (annotate the profile
     with project extents and values used); else agency 500-yr hydrology; else a documented provisional value with agency
     agreement. A 1.75 x Q100 ordinate scaling is a labelled sensitivity only. Zone AO depth is not an elevation;
   - state the 500-yr source once; tabulate floor, pad and equipment elevations with datum and the controlling 100-yr and
     500-yr WSE;
   - add a FEMA floodplain section: effective zones, floodway, BFEs, how they constrain the design, and the consequence if
     existing ground is below the 500-yr WSE.
7. Rise and impact thresholds are cited from the governing agency or stakeholder per project (D29); no hard-coded 0.1 ft.
   Comparisons use `impact-comparison`.

### 2. Content rules
Watersheds and hydrology
1. Onsite watersheds end at the property line; omit offsite areas draining away; existing and proposed totals match to
   two decimals. Set the onsite boundary at the project boundary so pre vs post is shown there.
2. Areas not regraded are modelled on existing contours.
3. Nested areas: list each catchment with its parent; run a total-area unattenuated case once; never add upstream basin
   outflows or pipe catchment flows to it. Where detention is modelled, route the upstream outflow and add only the
   incremental downstream area. Load soils and attributes by the same catchment key as geometry; stop on mismatched keys.
4. Offsite areas near a storm drain: bring in the storm drain, manholes and inlets; include roadway and upstream
   subdivision areas tributary to it; state the inlet capture assumption; label upstream offsite infrastructure.
5. Watershed exhibits: boundaries follow visible ridge lines on shown topo; flow arrows agree with contours; Tc path shown;
   "flowline" where no stream exists (contour intervals per `drainage-report-exhibit-standards`, D42).
6. Tc = hydrology program value (PC-Hydro 5-min minimum); never call time to peak Tc; table values match native output.
7. Percent impervious and cover need a stated source (plans, independently labelled imagery meeting a set acceptance, or a
   named cover scenario S1/S2/S3). Classifier output is not field truth.
8. Basin outlets not surveyed: search as-builts and GIS pipe layers first; else ask the owner once and store the answer as
   a versioned scenario (source = owner); supersede explicitly, never overwrite; flag implausible derived slopes. Fallback
   with no invert data: pipe from lidar with 1 ft minimum cover tied to outfall ground.
9. Rainfall tables state source, statistic, return period and duration; runoff-coefficient columns headed with the symbol
   (for example Cw) and plain numbers.

Detention, first flush, infiltration
10. Give preliminary pre vs post peak Q and storage estimates even at concept level. Preliminary detention where PR > EX
    (2, 10, 100-yr): Vs = Vin,PR x (1 - Qex / Qpr), max of the three events; replace with a routed design at final.
11. Keep flood detention, first flush / water quality, sediment storage and harvesting separate, each with its own
    criteria and maintenance. Distributed (pod-level) detention gets a ledger per pod: allowable Q, required volume,
    phasing trigger, responsible entity. Name maintenance access and the responsible entity.
12. First flush retained below the outlet invert (raise the outlet inlet rather than regrade the basin); shallow first-flush
    areas up to 9 in deep where needed. Model outlets exactly as drawn.
13. Drawdown = retained depth / design infiltration rate with the standard factor of safety. Untested rate (D23): state the
    basis used and that field testing is required; the add-on sets the method (Pima: required-rate method; Placer: half
    NRCS rate with 0 in/hr sensitivity).
14. Flag basins in mapped riparian habitat and outfalls direct to a major wash (detention waiver candidates).
15. Maintenance / inspection plan only if the jurisdiction requires it; otherwise ask JCO.

Channels, culverts, streets
16. Constructed unlined earthen channels n = 0.025; natural channels from land cover with the source cited (D27). Tables
    show required depth (normal depth + required freeboard) vs provided, and the lining (earthen / unlined, concrete,
    shotcrete, riprap).
17. 2D Manning n: land-cover n for new, concept and master studies; uniform n only when extending an accepted model, stated
    in the report (D28).
18. Collector / diversion channels: size for the combined flow of all intercepted paths; check superelevation at each bend
    from radius; screen bank height with a conservative case (2 x normal depth or summed peaks); check transitions, lateral
    inflow and basin backwater. Where sediment load is high do not default to riprap; evaluate concrete or shotcrete;
    include sediment cleanout access. Where a collector returns flow to natural ground, provide a level spreader and compare
    existing vs proposed outlet split by domain exit.
19. Culverts: structure sizes from survey or as-builts (state the verified size, no discrepancy narrative); outlet velocity
    and protection per HEC-14 (at 9-13 fps a dumped riprap apron alone is not enough); inlet / outlet channel inverts at or
    below the box invert; cutoff walls for 100-yr scour plus long-term degradation; state the overtopping criterion with the
    margin achieved and check sensitivity to weir length; note sediment risk of perpendicular alignments.
20. Every quoted hydraulic result maps to a line of program output (Q, HW elevation, inlet vs outlet control, barrel length,
    slope, outlet velocity). A soffit or crown elevation is not computed headwater. Assumptions cite the same cross section
    that sized the structure.
21. Streets and inlets: state the design spread criterion, clogging factors used and design frequency in every inlet /
    scupper table; scuppers analysed in sump unless stated; ROW velocity check; apply clogging once (a two-grate sump with
    one grate assumed blocked already covers clogging); do not claim no bypass unless the calcs show it. Values per add-on.
22. Storm drain HGL: routing must be dynamic wave whenever HGL freeboard is reported; run fixed tailwater and free outfall
    cases and state the same boundary in model and text; compare peaks with receiving-system capacity and HGL before
    choosing retention vs discharge.

Narrative content (required in the first draft)
23. Project description: scope / RFP wording where the agency or client requires it (verbatim where the add-on says so);
    describe the improvement accurately (which part is developed, direction of expansion).
24. Existing conditions under one main heading with subheadings: area description (land use in every direction, slopes as
    range / average % and direction, soils); adjacent landowners and development (name the major adjacent owner); existing
    infrastructure (roads, berms, culverts, storm drains with sizes); existing hydrology, drainage easements, mapped local
    floodplains, existing basins. Split existing hydrology (offsite and onsite watersheds with calcs) from existing
    stormwater infrastructure.
25. Describe how the site drains today, including ponding locations, spill elevation and path, and ponding behind
    embankments; verify against topo.
26. Include the roadway typical section from the latest plan set; if uncurbed, say so and state that spread and inlet
    analyses do not apply. Delete statements about analyses not done (say why not needed) and template text for features
    the project does not have.
27. Floodplain status: FIRM summary (map number, panel, effective date, zones) for the project limits; effective and pending
    panels and which governs at submittal; read the zone at the actual alignment.
28. CP flows are stated as sums of sub-basins; one table compares calculated Q with prior-study Q for every CP, with
    differences discussed.
29. Describe the 2D model setup (culverts, cell size, refinement, inflows) before results; state which return periods and
    scenarios were run in each model (run matrix from completion files, not from the plan).
30. State whether increases reach habitable structures and give the cause.
31. Every exhibit citation gives figure number and appendix.
32. Terms: natural washes are "washes", engineered ones "channels"; no relative words ("near") - say "on the site" or
    "within the improvement limits". Short sentences and short paragraphs. No heading without body text.
33. Text started from another report: search for remnant road, wash, project names and old footers (target zero hits);
    update criteria to this project; verify claims about ditches, profile changes and ponding with the roadway team.
34. Concept reports: label concept level on the title page and executive summary; state what the report does not do (no
    entitlement, no new hydrology, no permitting) in the executive summary, the public-concern section and the conclusions;
    replace unearned compliance words with "is structured to meet, to be confirmed in the master drainage report"; keep
    objective findings separate from land-plan recommendations; state path continuity under major crossings and
    whether each existing structure stays, is adequate or is replaced; get written client decisions on level of protection
    and any designed overflow onto the site.
35. Criteria in minutes or text carry a citation or are marked OPEN in the QC open-items document; County criteria stay
    "County" until the Town confirms in writing.
36. Cite only real sources. Never mention superseded drafts, the calc workbook, Excel, scripts or independent checks.
    References numbered 1), 2), ... with online links where available.
37. Deliverables are written in completed tense; nothing reads as interim, draft or pending (D44).

### 3. Formatting
1. Build to this standard from the first draft (numbered sections and subsections, template styles for headings and
   spacing, no manual returns); do not build a generic layout and patch it later.
2. Page breaks only before main sections (1.0, 2.0 ...) and appendices; no half-empty pages, no orphaned headings, no blank
   areas in the body. Placeholder pages only for named future items, labelled (D50).
3. Tables (D47): native Word tables, never screenshots; thin borders on all cells, no thick lines; header row in the
   template header style; no alternating shading and no highlight fills; text centred; full text width; portrait (drop
   constant columns and state them in a note, or transpose single-row tables); repeat the header row if a table breaks;
   fit short tables to one page.
4. One caption per table, above it, numbered by section; delete any second title inside the table. Figures and tables
   numbered by section (Figure 4-1, Table 4-1), fixed before any figure is rendered (D52).
5. Precision: elevations 2 decimals with no thousands separator; discharges whole cfs; stated precision kept (n = 0.025,
   slopes 4 decimals); same precision down a column.
6. "The ... is presented in Table n." at the end of the preceding paragraph; every table and section cross-reference
   resolves to the displayed number.
7. Full-size figures on 11x17 pages grouped at the end of their main section (D36); exhibit content per
   `drainage-report-exhibit-standards`.
8. Drainage maps: watershed lines thick dark / bright pink; flowlines cyan dashed with arrows; short squiggly sheet-flow
   arrows; labels aligned along rivers and roads; basin labels with required / provided first flush, 100-yr volume, depth
   and WSEL; node letters plus Q100 with full attributes in the report table (D41).
9. Memos (D46): letter memo up to 10 pages on one topic - inline figures, no lists; multi-section technical memo -
   contents and figures grouped at section end (`drainage-technical-memo`).
10. No footer dates. Fix TOC tab alignment and stray characters; pull a fresh template if the firm heading bar is missing.
11. Abbreviate directions with a period (S.) or write road names out; be consistent.
12. Cover: project-specific site photo, preferably from the field visit; office address and project number filled.
13. No AI or tool-assistant indication anywhere in a deliverable (calc sheets, printouts, document properties, folder names
    - use `<Initials>_<YYYYMMDD>_<topic>`); preparer "Psomas (<initials>)". Brand colours and fonts per the firm template.

### 4. Native model runs and tooling
Every value in the report comes from a native run whose printout is in the appendix (D38). Run the engines through their
skills; this section sets the report-facing rules only.
1. PC-Hydro 7.4 (`pchydro-hydrographs`): run every .pk6 natively (interactive or batch, D18); userName "Psomas
   (<initials>)"; terms approval recorded once per project in the run log (D17, default, to confirm).
   - Vegetation: leave the program default cover for all conditions including graded ground (20% per NORTHLOOP-013),
     verified against the 7.4 auto-fill before each batch; no 5% Desert Brush rule, no typed density, no fixed CN (D20,
     default, to confirm). Valid watershed types include Mixed / Undeveloped-Valley.
   - Rainfall: in-app Fetch Rainfall governs; script-written depths are the comparison array; record the Atlas 14 edition
     served (D21).
   - Hydrographs: the native export is the record; a peak-adjusted copy is used for routing with the added volume logged;
     both peaks reported (D19). Report tables use the PC-Hydro reported peak. New reports: report Q = native output
     (0.0 cfs tolerance). Rebuilds of an old report: the old report is the target and differences are listed.
   - State the PC-Hydro version; the version in text equals the version on the printouts.
2. HEC-HMS 4.13 (`hechms-headless`, D01): work on upgraded copies; version stated in the report and on printouts;
   zero-met "No Precipitation" component for gage-flow routing (Specified Average documented as alternate).
3. HEC-RAS 6.6 pinned (D02); 2D builds `hecras-2d-models`; runs through `model-run-supervisor`; final runs volume error
   <= 0.1% plus WSEL residual and iteration-warning checks, <= 0.5% for screening only (D09).
4. FLO-2D (`flo2d-model-runs`): record the agency-named build and the working build; 26.02.25 with written agency acceptance
   logged per project (D03).
5. HY-8 8.00 (`hy8-native-runs`): supervised by default; .hy8 written only from an HY-8-saved template (D10); native report
   exported to Word then PDF.
6. Storm drain: EPA SWMM as an independent check only in Arizona; SWMM / SSA primary allowed under the Placer add-on (D26)
   (`swmm-ssa-storm-drain`).
7. Independent checks (spreadsheet or Python, for example HDS-5 culvert checks or a native-vs-report comparison) live in
   40_QC only, never in a deliverable (D30). They do not replace the T2 independent calc check.
8. Native-vs-report comparison before issue: every CP and return period, report Q vs native output, max abs diff 0.0 cfs;
   recorded in the QC document. Run matrix (model x storm x RP x scenario) built from completion files (SUMMARY.OUT,
   result HDF, HMS results), and every narrative statement about storms, RPs or scenarios checked against it.
9. Reusing a calc workbook: list cached errors per sheet and which sheets feed the report; flag values pasted from legacy
   programs that do not recalc; relink external links to local copies; confirm which copy is current before use.
10. QGIS layouts export headless with the system Python that matches the PyQt build; scripted sheets per D37.

### 5. Build chain (Standard v0.3)
Follow `drainage-report-standard` for the full chain; the report-facing rules are:
1. Work on an isolated copy of the Standard workbook; write only explicit input cells.
2. Excel recalc before anything reads formula cells (D51): private DispatchEx instance, events and link updates off,
   CalculateFullRebuild, save, close only that instance; then reopen and compare values semantically; zero new formula
   errors and correct register counters.
3. Keep a named-range map per Standard version.
4. Generate the body into the current firm template so every paragraph carries a named style.
5. DOCX post-process: remove template paragraphs that do not apply and leftover [FIGURE:] / [TABLE:] slots; document
   properties set to the firm preparer; no DATE fields in footers; cover office address and project number set.
6. Downsample figures to 200-300 dpi at print size before insertion.
7. Word export in a separate Word instance: update fields, TOC and table of figures twice; check for unstyled paragraphs;
   export PDF with heading bookmarks; make a reduced copy for email.
8. Render every page (contact sheets) and look at each one before issue.
9. Edit scripts are idempotent: back up first, check whether an insert already exists, assert counts before writing.
10. Standard s60 placeholders stay flagged until the assembly report shows them closed (D44).

### 6. Appendices
1. Native output always in the appendix: PC-Hydro printouts and hydrographs per CP, HEC-HMS summary, Atlas 14 PFDS printout,
   HY-8 report, RAS computation summaries, FIS / LOMR / dam-safety pages (D38). Extracted or compact sheets may be added,
   titled "extracted summary", with values traced to the native file.
2. Hydrology appendix holds the actual hydrologic basis: source-study discharge tables for the cited sections and a
   location map annotated to the sections used. General floodplain mapping only if annotated to show why it matters.
3. Every reference excerpt states source document, section and why it is included; cite only the governing manual for the
   jurisdiction. Highlight the Q values used in reference studies.
4. Order appendices A, B, C, D with subparts (D-1, D-2) after the parent; channel calcs in their own subpart. Appendix
   titles match contents and software used. Storm events ordered 2, 10, 100-yr with matching headings; offsite hydrology
   grouped by event.
5. Every watershed and CP on the maps appears in the tables; study limits shown on each map; split flows and their routing
   stated.
6. Analyses the agency asked not to show are removed with a short statement why; appendix names updated after removal.
7. Package model files (HEC-RAS and others) and reference excerpts with the report.
8. Provide an existing-conditions summary wherever a proposed one is shown.

### 7. Compiled PDF
Compile per `drainage-report-standard` (assembly manifest), with these rules:
1. Start from the newest editable source and its fresh Word export; corrections in the DOCX must reach its PDF.
2. Manifest-driven: file, page range, final location; bookmarks, named destinations and links generated from it; no
   hard-coded page numbers in prose.
3. 11x17 figures at the end of each main section; a divider per appendix and per plan set or study; landscape pages
   rotated.
4. Annotations (D48): author highlights flattened; inherited plan revision clouds removed from the compiled copy (originals
   kept); third-party annotations (for example FreeText from LOMR pages) flattened or noted.
5. Remove review-draft wording, unneeded pages and unrequested appendices.
6. Bookmarks (D52): cover, TOC, each main section, each appendix, each exhibit; sorted by page within each level. Every
   bookmark and link checked by script, then in a native PDF reader.
7. Page-by-page comparison of assembled pages to sources (text, size, low-dpi render) with a QA JSON in 40_QC.
8. Size (D52): <= 50 MB per file or the agency limit if lower; split otherwise; keep a reduced copy for transfer.
9. If a model rerun is pending, wait for the new result file, regenerate results and figures, recompile, then copy to
   10_Record.

### 8. Deliverables
1. Report DOCX / PDF, compiled bookmarked PDF, stand-alone agency checklist (section numbers as displayed), appendix
   dividers, record copies in 10_Record, updated workbook.
2. Comment-response log (D49): editable separate deliverable, plus a bound copy behind the cover where the agency asks.
3. Package with `delivery-package-build`: standard folder set, `<Initials>_<YYYYMMDD>_<CODE>_<description>` naming, no run
   copies / temp HDF / scratch files, creator and last-modified-by set to the firm preparer, README with contents, CRS and
   software versions, hashes verified, saved to the dated OneDrive project folder.

### 9. Submittable gate
Do not call a report submittable until all are true:
1. Jurisdiction and reviewing agency confirmed; governing manual editions cited match the add-on.
2. Plans match the report, or JCO's decision on each deficiency is recorded.
3. T2 independent calc check done (checker evidence in 40_QC); native-vs-report table at 0.0 cfs; run matrix matches text.
4. `qc-reviewer` pass on the full package (report-writer never self-approves); exhibits through `exhibit-reviewer`.
5. QC open-items document closed, or JCO has authorized compile with named items open (D44). Assembly report shows no open
   placeholders.
6. Seal, waivers and approvals identified; agency acceptance items from the add-on logged (written where required).
7. Compiled PDF passes Section 7 checks.

## Jurisdiction add-ons
| Add-on | Load when |
|---|---|
| `addons/pima-county-rfcd.md` | Unincorporated Pima County, RFCD review, Pima County DOT roads; also base criteria for Tucson, Marana, Sahuarita where they adopt County rules |
| `addons/city-of-tucson.md` | City of Tucson review (confirm City vs County from parcel record and contract) |
| `addons/town-of-marana.md` | Town of Marana review |
| `addons/town-of-sahuarita.md` | Town of Sahuarita review; Lee Moore Wash basin |
| `addons/fema.md` | Any FEMA SFHA, CLOMR / LOMR, no-rise, duplicate effective or FIRM statement |
| `addons/placer-county-ca.md` | Placer County CA, East Placer / Lake Tahoe Basin, TRPA |
| `addons/caltrans-california.md` | Caltrans R/W or other California agency work |
Load with `get_skill("drainage-report-build", resource="addons/<file>.md")`. Each add-on lists governing manuals,
criteria, methods, review expectations and open questions to confirm. Where an add-on value is marked "to confirm", carry
it into the QC open-items document until written confirmation is filed.

## Gotchas
Design basis and hydrology
- Candidate areas 40.0, 27.8, 27.0 and 12.9 ac were nested; summing would roughly triple the flow (EKOS-LOCAL-008, claude session).
- Local draft narrative started summing basin and road flows until guarded (EKOS-LOCAL-008, claude session).
- Flow arrows contradicted contours and one boundary had no supporting ridge (TANGERINE-023, JCO redline).
- Offsite watershed omitted roadway and subdivision areas tributary to the storm drain (TANGERINE-024, JCO redline).
- Outlet description changed twice in one session; routing built on the first had to be redone (EKOS-LOCAL-015, claude via Codex session).
- Assumed outlet pipe produced a 0.017% slope (EKOS-LOCAL-015, claude session).
- A preliminary outlet default (24-in RCP 1 ft above basin bottom) was project-specific, not a library default (EKOS-LOCAL-015).
- First first-flush version used 0.5 in over impervious only; corrected to Table 2.1 rates with disturbed pervious and drawdown checks (RKN-016, claude session).
- Concept report left block-level detention unsized and unassigned; reviewers asked for a per-pod ledger (TANGERINE-015, reviewer comment).
- Internal QC asked for preliminary pre-post detention and first-flush estimates in the hydraulics appendix (TANGERINE-015, JCO redline).
- Design-basis summary in a 30% DCR reintroduced regional / local ambiguity although definitions existed (BARNETT-006, agency redline).
- One flow quoted as 4,324 cfs and 4,325 cfs in different places (BARNETT-006, agency redline).
- A 100-yr value was labelled 200-yr; the source study has no 200-yr flows (SAHPARK-003, JCO redline; PHXZOO-007, JCO redline).
- Inflow map captioned 10-yr showed 100-yr rates (SAHPARK-003, JCO redline).
- Missing table referenced in hydrology text (SAHPARK-003, JCO redline).
- Approach flow (2,673 cfs) quoted as the crossing flow when the culvert was sized for 534 cfs (SAHPARK-003, JCO redline).
- Prior report stated the 500-yr basis two ways (1.75 x Q100 and a 10-yr reference) (NORTHLOOP-010, JCO markup).
- Nearest mapped cross section was about 1,848 ft from the development; the FIS profile could not be used (NORTHLOOP-010, claude session).
- Prior report placed equipment above the 500-yr and 1 ft above the 100-yr, which no longer meets current code (NORTHLOOP-003, claude session).
- Draft omitted critical facility and 500-yr discussion; legend listed Zone A not on the map and missed the floodway hatch (TANGERINE-021, JCO redline).
- Scope asked for refuge to the 500-yr while the design basis covered 10 / 100-yr only; carried as a client decision (PHXZOO-002, claude session).
- Existing berm breaks out near the 10-yr event; the split had to be represented (PHXZOO-002, claude session).
- Effective TDN listed 3-hr and 24-hr storms; only the 3-hr case was in the package; do not claim an envelope from one storm (STARVALLEY-022, claude session).
- Classifier on 128 model-labelled points reached 68.75% agreement with 60% of the catchment unknown; not used (EKOS-LOCAL-019, claude session).
- Model labelled a shadow as vegetation; labels are not field truth (EKOS-LOCAL-019, claude session).
- First imagery set did not cover the north reach; check coverage of the full hydraulic extent (EKOS-LOCAL-019, claude session).
- Saved standards still carried the old 5% Desert Brush graded-ground rule; JCO correction overrides it (NORTHLOOP-013, claude via Codex session).
- Confirm jurisdiction from the plat case and parcel data before choosing manuals (RKN-017, claude session).
- Development Engineering flagged a superseded Town document cited in four places (BARNETT-004, agency redline).
- Draft did not follow the agency outline; all agency sections required even when empty (TANGERINE-017, JCO redline).
- Jurisdiction unclear (City vs County); contracts and parcel map pointed to County (TANGERINE-017, reviewer comment).
- Highlighter terms must match manual wording; check regression region names by hand (CALFIRE-002, claude session).
- Town code text was not readable online; confirm with Town staff instead of assuming County criteria (PHXZOO-004, claude session).
- No published animal-facility drainage standard exists; state such topology as engineering judgment (PHXZOO-004, claude session).
- Keep research separate from minutes so unverified findings stay OPEN (PHXZOO-004, claude session).
Hydraulics content
- Riprap may not suit a high sediment load; later plans used 6 in shotcrete (NORTHLOOP-014, JCO redline).
- Candidate 8-ft bank was below the 8.71-ft depth from the conservative summed 500-yr flow (NORTHLOOP-015, JCO redline).
- Collector carried about 1,945 cfs at 49 in depth + 2 ft freeboard; superelevation had to be verified by radius (NORTHLOOP-015, JCO redline).
- A level spreader basin requested by markup stayed open in the response log pending disposition (NORTHLOOP-016, JCO redline).
- Draft had no outlet protection or scour content; 100-yr overtopping criterion met with no margin (SAHPARK-020, JCO redline).
- Shortest culvert alignment was perpendicular to flow; sediment maintenance may cancel the saving (SAHPARK-020, JCO redline).
- Rev B text gave HW 2,707.75 ft (the soffit) under outlet control; program output showed 2,707.50 ft and entrance control (SAHPARK-015, claude).
- Barrel length 65.99 ft in text vs 65.00 ft in the run; a summary sentence was truncated (SAHPARK-015, claude).
- An assumption cited one cross section while the culvert was sized from another; a section number was skipped (SAHPARK-015, claude).
- Two-grate sump with one grate blocked already covers clogging; applying 50% again double counts (VALENCIA-012, agency redline).
- Inlet depression in calcs must follow the agency standard apron detail (VALENCIA-012, agency redline).
- Do not claim no bypass at all inlets unless the calcs show it (VALENCIA-012, agency redline).
- Scupper tables omitted design frequency and clogging; a Q100 appeared where Q10 was expected (ELTORO-011, reviewer comment).
- SSA model on kinematic wave reported HGLs that cannot show backwater; the HGL table could not support the criterion (HOMEWOOD-006, claude).
- Model weir did not match the drawn outlets and overstated WQ retention; 32-68% of the WQ event left untreated as drawn (HOMEWOOD-007, claude).
- Tailwater 6 in below the receiving grate failed the HGL criterion before site runoff; the model used a free outfall while the memo claimed tailwater (HOMEWOOD-010, claude session).
- Draft asserted retention without checking the storm drain and claimed impervious removal the plan did not show (TANGERINE-025, claude session).
Native output and traceability
- Results scraped from web pages can drift from native output; the native cross-check is the only proof (RKN-005, claude).
- HMS results XML and RAS messages re-typeset in Courier were listed as native output and marked Addressed (CALFIRE-015, claude).
- Narrative said 2- to 100-yr storms ran in all models; FLO-2D finished only 100-yr runs because the queue stalled (SAH-017, claude).
- RAS 2- to 50-yr plans finished after the 30% draft date (SAH-017, claude).
- A reviewed report cited one PC-Hydro version in text and an earlier one on a later page (ELTORO-010, claude).
- A reviewer questioned the PC-Hydro version used in a source report; confirm the version the agency accepts (ELTORO-009, reviewer comment).
- 215 cached errors across 5 workbook versions; only some fed report sheets (VALENCIA-014, claude).
- Revert, overwrite, 100% and signed-sealed workbook copies differed; confirm which is current (VALENCIA-014, claude).
Narrative
- Template text kept boilerplate on curb inlets and storm drains the project did not have (CAMPBELL-017, JCO redline).
- Three empty headings flagged twice (SAHPARK-002, JCO redline).
- Typical section missing although 30% plans had been issued two weeks earlier (SAHPARK-002, JCO redline).
- County and Caltrans projects often require their own description text verbatim (TANGERINE-019, JCO redline).
- Draft stated the expansion direction opposite to the existing improvements (TANGERINE-019, JCO redline).
- Most existing-site content was added by markup; it belongs in the first draft (TANGERINE-020, JCO redline).
- Draft named the wrong project and another road, and claimed ditches and profile changes not in the design (VALENCIA-024, JCO redline).
- Reviewers flagged advocacy tone and overstated conclusions in five comments (TANGERINE-012, mock review).
- Text said Zone D while the road sat in Zone X and mapped floodplain (PHXZOO-007, JCO redline).
- JCO redlines caught all four floodplain / status items in a staff draft; check them before review (PHXZOO-007, JCO redline).
- Reviewer read 41 of 48 pages before learning a path was claimed continuous under the freeway and railroad (BARNETT-011, agency review).
- A designed overflow onto the site creates a second floodplain path and conflicts with matching existing peak Q at the boundary (PHXZOO-005, claude session).
Formatting
- All four reports on one job were built in a generic layout and restructured with one-time patches (RKN-014, claude).
- Table with green highlights, mixed elevation decimals and a name not matching the caption (SAHPARK-004, JCO redline).
- Screenshot of an Excel table plotted poorly (SAHPARK-004, JCO redline).
- Short appendix table ran onto a second page (SAHPARK-004, JCO redline).
- Excessive and inconsistent spacing; large blank area on one page (SAHPARK-005, JCO redline; TANGERINE-018).
- Table mismatch twice, extra space three times, a stray bracket and footer dates in one draft (TANGERINE-018, JCO redline).
- Border, colour and highlight fixes marked on 6 table pages (VALENCIA-021, JCO redline).
Build chain and compile
- openpyxl reads stale formula values unless Excel recalculated and saved the workbook (SAH-012, claude).
- A library-written workbook showed a counter of -14 status issues; native recalc gave 0 (EKOS-LOCAL-018, claude).
- Native Excel merges adjacent validation ranges and drops default styles; compare semantics, not raw XML (EKOS-LOCAL-018, claude).
- Learning the workbook layout took four inspection passes (SAH-012, claude).
- Figures numbered 1-7 then renumbered by section, so every exhibit was rendered twice (CALFIRE-013, claude).
- Memo template ships its own core.xml and duplicated parts (CALFIRE-013, claude).
- TOC level-2 tab leader missing on short entries (CALFIRE-013, claude).
- Cover office address and project number were placeholders (CALFIRE-013, claude).
- DOCX of 49-56 MB with full-resolution images; unstyled paragraphs broke python-docx; Word cleanup took 46 saves on submittal day (TANGERINE-011, claude).
- First template pass pushed the cover to 2 pages and ran the footer across the 11x17 page (VALENCIA-009, claude via Codex session).
- An integration script failed after writing the body; a rerun would have duplicated a paragraph (VALENCIA-009, claude via Codex session).
- Output used pageBreakBefore, not w:br; grouping logic must handle both (VALENCIA-009, claude via Codex session).
- Issued 96-page PDF and three exhibit PDFs had no bookmarks (TANGERINE-016, JCO redline; TANGERINE-011).
- Appendix bookmarks out of page order (CALFIRE-014, claude).
- Source LOMR pages brought FreeText annotations into the compiled PDF (CALFIRE-014, claude).
- A report link did not work in the reviewed draft (CAMPBELL-020, JCO redline).
- pypdf "Multiple definitions for key /PageMode" warnings from source PDFs are harmless (RKN-015, claude).
- Compiled PDFs reached 55-86 MB and 700 MB-1 GB; a 23.8 MB file needed a 3.4 MB copy (RKN-015, VALENCIA-008, SAH-012).
- Revision clouds vanished in merged plan pages; 39 sheets re-rendered (VALENCIA-008, claude via Codex session).
- Final report must not carry plan revision clouds (VALENCIA-008, claude via Codex session).
- The editable Word body held corrections that never reached its PDF (VALENCIA-008, claude via Codex session).
- Browser-based reader checks failed under URL policy; use a native PDF reader (VALENCIA-008, claude via Codex session).
Appendices and package
- Hydrology appendix contained only regional floodplain mapping (SAHPARK-011, JCO redline).
- Uncited manual page from another jurisdiction with no stated purpose (SAHPARK-011, JCO redline).
- Appendix D-1 came before Appendix D; a channel calc sat in the culvert appendix (SAHPARK-011, JCO redline).
- Offsite wash and FEMA comparison sections removed at agency request were later re-added and flagged (VALENCIA-022, JCO redline).
- Missing model files and excerpts made later reuse of the report flows hard; reconciliation years later (ELTORO-013, reviewer comment).
- A watershed on the map was missing from a table (ELTORO-013, reviewer comment).
- First delivery package used a non-standard folder name and missed printouts and QC; rebuilt two hours later (RKN-019, claude session).
- Download links failed on the phone; OneDrive worked (CAMPBELL-023, claude via Codex session).

## QC checks
Pull these rule sets and the add-on tag before issue:
`get_qc_rules('report-text')`, `get_qc_rules('tables')`, `get_qc_rules('exhibits')`, `get_qc_rules('hydrology')`,
`get_qc_rules('appendix')`, `get_qc_rules('package')`, `get_qc_rules('existing-conditions')`, plus as applicable
`hydraulics-2d`, `flo2d`, `culverts`, `storm-drain`, `model-runs`, `comment-response`, `crs`, and the jurisdiction tag
(`pima-rfcd`, `tucson`, `marana`, `sahuarita`, `fema`, `placer`, `caltrans`).

Checks this skill must pass itself:
- Jurisdiction, reviewing agency and manual editions recorded; section list matches the agency outline one to one.
- Design discharge table present; every Q in text, tables and captions matches it; no RP outside the design set unless
  labelled a sensitivity.
- Parent-child area table; incremental areas sum to total; no flows summed across nested areas.
- Native-vs-report table: max abs diff 0.0 cfs; quoted hydraulic results map to output lines; versions in text equal versions
  on printouts; run matrix attached and matching the narrative.
- 500-yr source stated once; legend zones match the map.
- No empty headings, no boilerplate for absent features, no remnant names from other projects, no footer dates, no image
  tables, one table style, one caption per table, consistent column precision.
- Every exhibit citation names figure and appendix; CP vs prior-study table present when a prior study exists.
- Appendix contents match titles and order; native output pages are printouts or titled "extracted summary".
- Compiled PDF: minimum bookmark set, all links and bookmarks resolve, sorted by page; QA JSON present; no revision clouds,
  no draft wording; size within limit.
- QC open-items document closed or JCO authorization recorded.

## Change log
- 2.0.0 2026-10-22: rebuilt as library entry point. Clusters: HJR-C04, C07, C08, C09, C10, C11, C12, C13, C14 (method
  selection step), C19, C20; RPT-C01, C06, C07, C10, C11; QC-C07, C09, C12, C15; HYD-C19, C20, C25 (report-facing parts);
  DSO-C31. Decisions applied: D01, D16, D19, D20, D21, D22, D23, D24, D25, D26, D27, D28, D29, D30, D38, D44, D45, D46,
  D47, D48, D49, D50, D51, D52, D56; D02, D03, D09, D10, D17, D18, D36, D37, D41, D42 referenced where they touch the report.
  Changes from v1: HMS 4.12 -> 4.13 with zero-met default (D01); earthen n limited to constructed unlined channels (D27);
  500-yr fallback order (D22); untested infiltration split core / add-on (D23); table style without alternating shading
  (D47); PC-Hydro native vs peak-adjusted series (D19); in-app rainfall governs (D21); FlowMaster / CulvertMaster legacy
  (D16); compile, bookmark, size and annotation rules (D48, D52); one QC open-items document and completed tense (D44);
  response status vocabulary (D45); comment-response log as separate deliverable (D49); markup copy renamed
  `_JCO-Markup.pdf`; method-selection step, design discharge table, narrative content list, build chain, appendices and
  submittable gate added; seven jurisdiction add-ons added under addons/. All v1 content, formatting, tooling and
  deliverable rules kept unless listed here.
  Items marked "default, to confirm": D16 licensed set, D17 PC-Hydro terms approval, D20 20% vegetation default, D24 Marana
  regional flows, D46 memo layouts, D47 table style, D52 numbering / size / bookmarks, D41 drainage map labels.
