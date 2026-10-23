# Phase 3 decisions (resolved 2026-10-22)

JCO answer: "Use your defaults" for all [JCO] items; build list approved.
Every decision below is the proposed resolution in conflicts.md. Items that were [JCO] are marked
(default, unconfirmed): skills apply them and note "default, to confirm" in their change log.

D01 HEC-HMS 4.13 standard; work on upgraded copies; version stated in report and printouts; zero-met component
    ("No Precipitation") is the default pattern for gage-flow routing; Specified Average pattern documented as alternate.
D02 HEC-RAS 6.6 pinned; 7.x only by logged decision on a pre-upgrade copy.
D03 FLO-2D: record agency-named build and working build; use 26.02.25 with written agency acceptance logged
    per project (default, unconfirmed: JCO seeks Town of Marana acceptance).
D04 FLO-2D run complete = termination line in SUMMARY.OUT + all outputs + no TMP files; exit code logged, not required.
D05 HEC-RAS launch order: Ras.exe -c <prj> <plan> -hideCompute with dialog watcher; then RasUnsteady.exe direct;
    then COM controller. Success judged by result HDF.
D06 Max 2 FLO-2D solvers x 8 threads on EKOS until benchmarked.
D07 FLO-2D warnings: known-benign list auto-answered and logged; anything else stops and notifies.
D08 One status file updated every poll; notify only on finish, failure or decision needed.
D09 Final runs: volume error <= 0.1% (RAS and FLO-2D) plus max WSEL residual and iteration-warning checks;
    <= 0.5% for screening runs only.
D10 HY-8 supervised by default; .hy8 written only from an HY-8-saved template; unattended only after validation.
D11 Long jobs call the environment interpreter by full path; skill dependency lines name the environment; pip only
    for container-only skills.
D12 No .ps1 dependence in skills; launchers in Python or inline commands (setup scripts may use -ExecutionPolicy Bypass).
D13 Agent runs model computes natively by default; per-job override recorded in the continuation file (default, unconfirmed).
D14 EKOS-LOCAL jobs: local worker fetches data via replayable scripts; other jobs: due-diligence agent may fetch.
D15 Local model roles: Laguna S 2.1 reasoning/planning; Mistral Small 3.2 cited narrative and criteria answers;
    Qwen3.5-9B extraction and recovery only (default, unconfirmed).
D16 FlowMaster and CulvertMaster treated as legacy; licensed set = FHWA Hydraulic Toolbox, HY-8, Civil 3D hydraulic
    tools, HEC-RAS, HEC-HMS, FLO-2D, PC-Hydro (default, unconfirmed).
D17 PC-Hydro "I Agree": JCO approval recorded once per project in the run log (default, unconfirmed).
D18 PC-Hydro: interactive and batch (Playwright) modes both supported; batch for more than a few CPs.
D19 PC-Hydro: native export kept as record; peak-adjusted copy for routing with logged added volume; script reports
    both peaks. Native output is the reference for new reports (0.0 cfs tolerance); the old report is the target for rebuilds.
D20 PC-Hydro vegetation on graded ground: use the program default (20% per NORTHLOOP-013) and verify against the
    7.4 auto-fill before each batch; 5% Desert Brush rule removed (default, unconfirmed).
D21 Rainfall: in-app Fetch Rainfall governs; script-written depths are the comparison array; record the edition served.
D22 500-yr WSE: FIS 0.2% profile only if sections bracket the site; else agency 500-yr hydrology; else documented
    provisional value with agency agreement.
D23 Untested infiltration: core = state basis and testing requirement; Pima add-on = required-rate method
    (depth x FS / drawdown); Placer add-on = half NRCS rate with 0 in/hr sensitivity (to confirm with County).
D24 Marana: design on non-regional discharges (MDM 4.1); regional flows only where the facility is a regional
    channel / linear park (default, unconfirmed).
D25 East Placer: add-on carries 5 ft groundwater separation; WQ depth flagged for confirmation from the East Placer
    manual (1.2 in rainfall vs 0.9 in unit WQV).
D26 SWMM: independent check only in AZ; SWMM/SSA primary allowed in the Placer add-on.
D27 n = 0.025 applies to constructed unlined earthen channels; natural channels from land cover with source cited.
D28 Uniform 2D Manning n only when extending an accepted model (stated in report); new/concept/master studies use land-cover n.
D29 Rise thresholds cited from the governing agency or stakeholder per project; no hard-coded 0.1 ft.
D30 Independent spreadsheet/Python checks live in 40_QC only, never in a deliverable.
D31 Depth ramps: "local" default = <0.2 ft hidden, 0.2-0.5, 0.5-1.0, 1.0-2.0, 2.0-3.0, >3.0 ft
    (yellow, cyan, blue, orange, red); "deep-flow" = 0-3, 3-5, 5-10, >10 ft for regional washes and corridors;
    exhibit states which (default, unconfirmed).
D32 Continuous class bounds, upper bound exclusive.
D33 Raster data mask 0.01 ft; display cutoff = bottom of the chosen ramp; difference maps hide |d| < 0.10 ft unless
    the agency threshold differs.
D34 Text: 9 pt minimum for new text; 0.1 in absolute minimum for inherited CAD text (default, unconfirmed).
D35 Location/vicinity map: no aerial (explicit exception to full aerial coverage).
D36 Report exhibits 11x17 (scalable to 22x34); CAD coordination exhibits 30x42 allowed; appendix 8.5x11 with Psomas border.
D37 QGIS/CAD for report exhibits; scripted (Python) sheets for review, screening and result-map series that pass the
    same checks; editable source kept (default, unconfirmed).
D38 Native output always in the appendix; extracted/compact sheets may be added, labelled "extracted summary",
    values traced to the native file.
D39 FIRM marking: tight box or sketched alignment, labelled; full panel only with the project marked tightly.
D40 Aerial at full strength; result raster at 60% opacity (default, unconfirmed).
D41 Drainage maps: node letters plus Q100; full attributes in the report table (default, unconfirmed).
D42 Watershed exhibits: 1-ft contours minimum, 0.5-ft on flat sites; 2-ft only for large offsite areas.
D43 Raster names: <scenario>_<event>_<variable>_<units>_<cell>ft.tif + plan-number dictionary; differences in a
    Differences folder.
D44 One internal QC open-items document; deliverables in completed tense; compile blocked while items are open
    unless JCO authorizes; Standard s60 keeps placeholders flagged until the assembly report shows them closed;
    fix PROJECT-TEXT handling.
D45 Status = Addressed / Partial / Assumed / Not Addressed / Cannot Determine / Stale; disposition (separate field)
    = incorporated / superseded / no change.
D46 Letter memo (up to 10 pages, single topic): inline figures, no lists. Multi-section technical memo: contents,
    figures grouped at section end (default, unconfirmed).
D47 Table style: thin borders on all cells; header row in the template's header style; no alternating shading
    (default, unconfirmed).
D48 Compiled PDF: author highlights flattened; inherited plan revision clouds removed (originals kept);
    third-party annotations flattened or noted.
D49 Comment-response log: editable separate deliverable plus bound copy behind the cover where the agency asks.
D50 Placeholder pages only for named future items, labelled; no blank areas in the body.
D51 Excel recalc: private DispatchEx instance, events and link updates off, CalculateFullRebuild, then value compare.
D52 Figure/table numbering by section (Figure 4-1); PDF <= 50 MB per file or agency limit if lower, split otherwise;
    bookmarks = cover, TOC, each main section, each appendix, each exhibit (default, unconfirmed).
D53 Lidar chosen by acquisition collection, logged; vintages differenced where both exist; composite allowed with log.
D54 DEM: hydraulics/grading 3 ft (3.28 ft when preserving native 1 m), hydrology 10 ft, large basins 30 ft; in data log.
D55 Pima County default CRS: NAD83(HARN) Arizona Central, intl ft, EPSG:2868; realization recorded in every data
    log; mixing flagged (default, unconfirmed).
D56 Standard v0.3 job layout for every job (00_Admin, 01_Reference, 02_Data, 10_Record, 20_Working, 30_Report,
    40_QC, 50_Correspondence; issued sets in 30_Report/Issued); dates YYYYMMDD.
D57 hecras-result-rasters: warn on HDF-only terrain modifications; volume pre-check; mandatory RAS Mapper spot check.
