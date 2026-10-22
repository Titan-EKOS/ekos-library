# Phase 3 conflicts - decisions for JCO

Source: 306 unique cards from 16 projects, merged in six groups (HYD hydraulics, QC, RPT report/compile, EXH exhibits,
HJR hydrology + jurisdiction, DSO data/setup/other). The group files in this folder hold the full evidence for each
side (card ids per claim). 69 raw conflicts collapse to the 57 decisions below.

Each item has a **proposed resolution**. Items marked **[JCO]** need a fact or a judgment call only you can make;
the rest can be accepted as proposed. Reply with "accept all except ..." plus answers to the [JCO] items.

Not conflicts (handled as jurisdiction add-ons): Pima County RFCD vs Placer County vs Caltrans criteria, Marana vs
Sahuarita manuals, FEMA-only requirements.

---

## A. Tool versions and run control

**D01 HEC-HMS version and met-model pattern.** Skill: 4.12, Specified Average met model (drainage-report-build s3).
Cards: every recent run used 4.13 (SAH, CALFIRE, CAMPBELL, EKOS-LOCAL, RKN); opening 4.12 in 4.13 upgrades one way;
EKOS-LOCAL-009 used a zero-met component named "No Precipitation" for gage-flow routing ("None" failed).
Sources: HYD-CF-01, HJR-6, QC-1, RPT-X06, DSO-4.
Proposed: standard = 4.13; work on upgraded copies; version stated in report and on native printouts; both met
patterns documented, the zero-met pattern as default for external-inflow routing.

**D02 HEC-RAS version.** No skill states one; projects mixed 6.6 and 7.0 plans (ELTORO-005); rerun kits pin 6.6.
Proposed: pin 6.6; 7.x only by logged decision on a pre-upgrade copy. (DSO-5)

**D03 FLO-2D build.** Marana manual names 17.08.17, which fails at startup on EKOS; 26.02.25 runs; 23.10.25 stalled.
Proposed: record agency-named build and working build in a tool-version table; use 26.02.25 with written agency
acceptance logged per project; Marana add-on states this. (HYD-CF-16, HJR-9) **[JCO]** confirm you will seek Town acceptance.

**D04 FLO-2D run-complete test.** STARVALLEY-019: exit code 0 required. NORTHLOOP-007 / SAH-004: build 26.02.25 keeps
running and must be terminated (non-zero code). Proposed: complete = termination line in SUMMARY.OUT + all outputs +
no TMP files; exit code logged, not required. (HYD-CF-05)

**D05 HEC-RAS headless launch order.** Five cards, four different primary methods. Proposed: Ras.exe -c <prj> <plan>
-hideCompute with dialog watcher first; RasUnsteady.exe direct on p##.tmp.hdf second; COM controller last; success
judged by result HDF, never by return code. (HYD-CF-10)

**D06 FLO-2D concurrency on EKOS.** 2 x 8 threads (NORTHLOOP) vs 3 streams + RAS (SAH, AppHang closures).
Proposed: max 2 solvers x 8 threads until a benchmark sets the limit. (HYD-CF-11)

**D07 FLO-2D warning dialogs.** Auto-Enter (SAH-004) vs stop and notify (NORTHLOOP-007). Proposed: known-benign list
auto-answered and logged; any other warning stops the run and notifies. (HYD-CF-12)

**D08 Status and notification cadence.** 30-min heartbeats still produced 15 status requests (CAMPBELL-005); 15-min
heartbeat (SILVERBELL-018). Proposed: one status file updated every poll; notify only on finish, failure or a decision. (HYD-CF-13)

**D09 Volume-error acceptance.** 0.1% FLO-2D (NORTHLOOP), 0.5% RAS gate (SILVERBELL-018), 0.25% rejected for WSEL
residual (SILVERBELL-005), 0.07% accepted with residual checks (CAMPBELL-001). Proposed: final runs <= 0.1% for both
engines plus max WSEL residual and iteration-warning checks; <= 0.5% allowed only for screening runs. (HYD-CF-09)

**D10 HY-8 automation and file authoring.** UI export worked after 9 probes (CALFIRE-012); never achieved unattended
(EKOS-LOCAL-012); seed-file text editing faster (SILVERBELL-015); from-scratch writer gave wrong catalog codes and
units (VALENCIA-003). Proposed: HY-8 is a supervised step by default; .hy8 files written only from a template saved by
HY-8 itself; unattended runs only after the writer is validated on that machine. (HYD-CF-02, -03)

**D11 Python environments.** uv locked envs (EKOS-LOCAL-021) vs full-path Python 3.12 (SAH-015) vs pip in skills.
Proposed: long jobs call the env interpreter by full path; skill dependency lines name the env; pip only for
container-only skills. (DSO-6)

**D12 PowerShell scripts on EKOS.** EKOS-LOCAL-021 says .ps1 execution is disabled; SAH-015 launched long jobs via a
.ps1. (The library's own setup ran with -ExecutionPolicy Bypass.) Proposed: no .ps1 dependence in skills; launchers
in Python or inline commands; setup scripts keep the Bypass call. (DSO-7)

**D13 Who runs model computes.** Engineer runs computes (ELTORO-022) vs agent runs them (CALFIRE, SAH) vs local AI
only (EKOS-LOCAL-003). Proposed: library default = agent runs computes natively; per-job override recorded in the
continuation file. (DSO-11) **[JCO]**

**D14 Cloud vs local data retrieval (EKOS jobs).** Owner correction: cloud must not fetch data on EKOS-LOCAL jobs
(EKOS-LOCAL-003) vs cloud ran due diligence directly (CALFIRE, NORTHLOOP). Proposed: on EKOS-LOCAL jobs the local
worker fetches via replayable scripts; elsewhere the due-diligence agent may fetch directly. (DSO-12)

**D15 Local model roles.** Qwen3.5-9B drafted narrative (EKOS-LOCAL-001) but invented a standard (EKOS-LOCAL-005);
Mistral Small 3.2 passed 10/10 cited answers. Proposed: one role table in the local-model gateway skill - cited
narrative and criteria answers on the model that passed the cited-answer test; 9B for extraction and recovery only.
(DSO-10) **[JCO]** where Laguna S 2.1 sits in that table.

**D16 Licensed tool list.** SAHPARK-013 redline: use FlowMaster / CulvertMaster or HY-8. VALENCIA-001/005: FlowMaster
and CulvertMaster no longer licensed; reproduced in Hydraulic Toolbox / HY-8. Proposed: Standard lists the licensed
set; FlowMaster/CulvertMaster legacy. (HYD-CF-06) **[JCO]** are FlowMaster and CulvertMaster licensed or not?

## B. Hydrology and jurisdiction method

**D17 PC-Hydro terms ("I Agree").** Skill: ask every time. Cards: standing approval; batch scripts click it.
Proposed: your approval recorded once per project in the run log. (HJR-1) **[JCO]**

**D18 PC-Hydro headless.** Skill: cannot run headless, Chrome only. Cards: Playwright batch runs worked (67 subbasins
in about 25 min, SAH-007; RKN-004). Proposed: skill carries both modes, batch for more than a few CPs. (HJR-2)

**D19 PC-Hydro peak and series.** Script takes sampled max, never equal to the reported peak at 1-min steps; which
series goes to DSS is unstated; "not replicas" conflicts with a peak-adjusted copy. Proposed: native export kept as
record; peak-adjusted copy used for routing with logged added volume; script reports both peaks. Native output is the
reference for new reports (0.0 cfs tolerance); the old report is the target for rebuilds. (HJR-3, QC-3)

**D20 PC-Hydro vegetation default on graded ground.** Skill: leave auto-fill default. NORTHLOOP-013: keep 20% (replaces
an older 5% Desert Brush rule). Proposed: confirm the 7.4 auto-fill value; purge the 5% rule. (HJR-4) **[JCO]** is 20%
the auto-fill value or a fixed rule?

**D21 Rainfall source in .pk6.** Script-written Atlas 14 depths (RKN-003, SAH-007) vs in-app Fetch Rainfall (EKOS-LOCAL-006,
RKN-004). Proposed: native fetch governs; script values only as the comparison array; record the edition served. (HJR-5)

**D22 500-yr WSE for critical facilities.** Skill: FIS profile at up/downstream sections. NORTHLOOP-010: only if the
sections bracket the site; AO zones give depth not elevation; 1.75 x Q100 provisional only. Proposed: add a bracketing
test and fallback order (FIS bracketed -> agency 500-yr hydrology -> documented provisional with agency agreement). (HJR-7)

**D23 Untested infiltration rate.** Skill: state required field rate. HOMEWOOD-009: half NRCS rate with 0 in/hr
sensitivity. Proposed: core = state basis and testing requirement; required-rate method in Pima add-on; half-NRCS in
Placer add-on (to confirm). (HJR-10)

**D24 Marana regional flows.** NORTHLOOP-003: non-regional flows for design (MDM 4.1). BARNETT-006: 10-yr regional and
100-yr local both carried. Proposed: Marana add-on states MDM 4.1 rule with the linear-park/channel exception.
(HJR-11) **[JCO]** confirm the reading.

**D25 East Placer values.** WQ depth 1.2 in vs 0.9 in at about 6,300 ft (HOMEWOOD-002/008); groundwater separation 2 ft
vs 5 ft (HOMEWOOD-017). Proposed: due-diligence agent confirms both from the East Placer manual before the Placer
add-on is written; until then the add-on carries 5 ft and flags the WQ number. (HJR-12, QC-8)

**D26 SWMM role.** Skill: SWMM as independent check only. HOMEWOOD: SWMM/SSA primary model, calibrated to county
peaks. Proposed: AZ rule unchanged; SWMM/SSA-primary practice in the Placer add-on. (HYD-CF-04)

**D27 Earthen channel n.** Skill: n = 0.025. Cards: natural washes 0.030-0.050. Proposed: reword to "constructed unlined
earthen channels n = 0.025"; natural channels from land cover with source cited. (HYD-CF-15)

**D28 Uniform Manning n in 2D.** Keep uniform 0.035 to match an accepted model (ELTORO-004) vs reviewers expect
spatially varied n (TANGERINE-005). Proposed: uniform allowed only when extending an accepted model, stated in the
report; new, concept and master studies use land-cover n. (HYD-CF-08)

**D29 0.1 ft rise threshold.** Used as a trigger (ELTORO-018, CAMPBELL-024) vs not universal (SILVERBELL-016, railroad
criteria). Proposed: threshold cited from the governing agency or stakeholder per project; no hard-coded value. (RPT-X05)

**D30 Independent checks vs "no new spreadsheet".** SAHPARK-013 redline vs HDS-5 checks (CALFIRE-012, CAMPBELL-013).
Proposed: independent checks are internal QC (40_QC), never in the deliverable. (HYD-CF-07)

## C. Exhibits

**D31 Depth class breaks.** SAHPARK-006 (your redline): <0.2 hidden, 0.21-0.5, 0.51-1, 1-2, 2-3, >3 ft. CAMPBELL-018 (your
redline): 0-3, 3-5, 5-10, >10 ft. Proposed: two ramps - "local" (SAHPARK) default, "deep-flow" (CAMPBELL) for regional
washes and corridors; the exhibit states which. (EXH-X01) **[JCO]**

**D32 Class-bound notation.** Continuous (CAMPBELL-016) vs discrete with gaps (SAHPARK-006). Proposed: continuous bounds
(0.2-0.5, 0.5-1.0 ...), upper bound exclusive. (EXH-X03)

**D33 Wet mask vs display cutoff.** Raster script masks > 0.01 ft; maps hide < 0.1 or < 0.2 ft; difference maps hide
|dWSE| < 0.10 ft. Proposed: data mask 0.01 ft in rasters (unchanged); display cutoff = bottom of the chosen ramp;
difference maps hide |d| < 0.10 ft unless the agency threshold differs. (EXH-X02)

**D34 Minimum text size.** 0.1 in (7.2 pt) in your exhibit standard vs 9 pt (NORTHLOOP-011, your instruction).
Proposed: 9 pt for new text; 0.1 in absolute minimum for inherited CAD text. (EXH-X04) **[JCO]**

**D35 Aerial on location maps.** Full aerial coverage rule vs location map with no aerial (TANGERINE-022, your redline).
Proposed: location/vicinity map is an explicit exception. (EXH-X05)

**D36 Sheet sizes.** Proposed: report exhibits 11x17 (scalable to 22x34); CAD coordination exhibits 30x42 allowed;
appendix exhibits 8.5x11 with the Psomas border. (EXH-X06)

**D37 Scripted (Python) vs editable (QGIS/CAD) figures.** Python framework used on 5 projects; logged as a deviation
(RKN-012); you asked for figures recreated in QGIS/CAD (TANGERINE-006). Proposed: QGIS/CAD for report exhibits;
scripted sheets allowed for review, screening and result-map series that pass the same checks; editable source kept.
(EXH-X07, QC-9) **[JCO]**

**D38 Native output vs reformatted appendix sheets.** Proposed: native output always in the appendix; a compact or
extracted sheet may be added, labelled "extracted summary", with values traced to the native file. (EXH-X08, QC-2)

**D39 FIRM panel marking.** Proposed: tight box or sketched alignment, labelled; full panel only with the project
marked tightly. (EXH-X10)

**D40 Result layer opacity.** Three values used, none standard. Proposed: aerial at full strength, result raster at
60% opacity. (EXH-X11) **[JCO]**

**D41 CP labels on drainage maps.** Exhibit standard: node letters only, attributes in the table. RKN-013: CP number and
Q100 on the map. Proposed: node letters plus Q100 on drainage maps; full attributes in the report table. (QC-4) **[JCO]**

**D42 Watershed contour interval.** Proposed: 1-ft minimum for watershed exhibits, 0.5-ft on flat sites; 2-ft only for
large offsite areas. (HJR-8)

**D43 Raster file naming.** Script uses plan number; DLR-005 uses condition_event_variable. Proposed:
<scenario>_<event>_<variable>_<units>_<cell>ft.tif with a plan-number dictionary; differences in a Differences folder. (EXH-X09)

## D. Report, compile and QC process

**D44 Open items, status and tense in deliverables.** Responses in completed tense with open items internal (CAMPBELL-015,
VALENCIA-007) vs Partial/Deferred dispositions and remaining-items tables in the issued memo (TANGERINE-002) vs open
items memo issued with the report (CALFIRE-013); three different homes for the list; Standard s60 deletes placeholders
and hides open items (SAH-013). Proposed (matches your global rule that deliverables never read as interim): one
internal QC open-items document; deliverables use completed tense; compile is blocked while items are open unless
you authorize it; s60 keeps placeholders flagged until the assembly report shows them closed; fix PROJECT-TEXT.
(QC-6, QC-7, RPT-X01)

**D45 Status vocabulary.** Four different lists. Proposed: status = Addressed / Partial / Assumed / Not Addressed /
Cannot Determine / Stale; disposition (separate field) = incorporated / superseded / no change. (QC-5)

**D46 Memo format.** Inline figures, no lists (exhibit standard) vs Contents and grouped 11x17 figures (RKN-014).
Proposed: letter memo (short, single topic) = inline figures, no lists; multi-section technical memo = contents,
figures grouped at section end. (RPT-X02) **[JCO]** page or section threshold.

**D47 Table style.** Header color with alternating shading (SAHPARK-004) vs thin borders only (your skills).
Proposed: read the style defined in the Word template and write it into the Standard; thin borders on all cells
either way. (RPT-X03) **[JCO]** shading yes/no.

**D48 Markups in the compiled PDF.** Proposed: author highlights flattened; inherited plan revision clouds removed from
the compiled copy (originals kept); third-party annotations flattened or noted. (RPT-X04)

**D49 Comment-response log placement.** Proposed: both - editable separate deliverable, and a bound copy behind the
cover where the agency asks for it (Pima County RFCD add-on). (RPT-X08)

**D50 Blank pages.** Proposed: placeholder pages only for named future items, labelled; no blank areas in the body. (RPT-X09)

**D51 Excel recalc.** Proposed: private DispatchEx instance, events and link updates off, CalculateFullRebuild, then a
value compare. (RPT-X07)

**D52 Standard gaps.** Proposed: figure/table numbering by section (Figure 4-1); PDF size target <= 50 MB per file or
the agency limit if lower, split otherwise; minimum bookmark set = cover, TOC, each main section, each appendix, each
exhibit. (RPT gaps) **[JCO]** size target.

## E. Data and project setup

**D53 Lidar selection.** Newest per tile (CALFIRE-004) vs named collection (RKN-002) vs composite (SAH-020). Proposed:
choose by acquisition collection, log the choice, difference vintages where both exist; composite allowed with log. (DSO-1)

**D54 DEM cell sizes.** Proposed: hydraulics/grading 3 ft (keep 3.28 ft when that preserves native 1 m), hydrology 10 ft,
large basins 30 ft; stated in the data log. (DSO-2)

**D55 Arizona Central State Plane realization.** NAD83(HARN) EPSG:2868 (RKN, DLR; Pima County GIS) vs NAD83 EPSG:2223
(STARVALLEY). Proposed: default per jurisdiction from the survey basis; realization recorded in every data log;
mixing flagged by the CRS QC rule. (DSO-3) **[JCO]** default for Pima County work.

**D56 Folder map and date format.** Five folder layouts in use; dates as YYYYMMDD and YYYY-MM-DD. Proposed: Standard
v0.3 job layout (00_Admin, 01_Reference, 02_Data, 10_Record, 20_Working, 30_Report, 40_QC, 50_Correspondence,
50_Deliverables) for every job; dates YYYYMMDD per your naming rule. (DSO-8, DSO-9)

**D57 hecras-result-rasters terrain fidelity.** Script resolves terrain by file name and misses HDF-only terrain
modifications; flat per-cell WSE (DLR-006). Proposed: skill warns, adds a volume pre-check and a mandatory RAS Mapper
spot check. (HYD-CF-14, QC-10)
