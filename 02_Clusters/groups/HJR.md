# HJR - Hydrology + Jurisdiction Rules: reconciled clusters

Inputs: group_hydrology.json (27 cards), group_jurisdiction-rules.json (18 cards). 45 cards, 23 clusters, every card assigned once.
Score = sum(hours_lost x recurrence). Recurrence on QC-rule cards often counts individual redline comments (BARNETT-006 = 8 comments, TANGERINE-023 = 6, SAHPARK-003 = 3, TANGERINE-017/-021 = 4 each), so QC-rule scores overstate distinct events relative to skill cards.

Source tags used on gotchas: "claude session" (work log or KB written during a Claude run), "claude via Codex session" (owner correction captured in a Codex transcript), "JCO redline" (internal QC markup), "EOR markup", "agency redline" (reviewing-agency comment), "FEMA review" (AD letter / case closure record), "reviewer comment" (other external reviewer).

## Library structure proposed by this group (core + jurisdiction add-ons)

Core skills (jurisdiction-neutral procedure; each add-on overrides only what differs):

| Core | Role | Add-ons fed by HJR clusters |
|---|---|---|
| drainage-report-build | report build, method selection step (Sec. 0), content rules (Sec. 1) | /pima-rfcd (C09, C12, C14, C20), /city-of-tucson (C07, C12, C19), /town-of-marana (C12, C14), /town-of-sahuarita (C11, C22, C23), /fema (C11, C12, C21), /placer-county (C15, C16, C17), /caltrans-california (C14, C22) |
| pchydro-hydrographs | PC-Hydro engine (Pima County RFCD method; also accepted by City of Tucson, Marana, Sahuarita for onsite/non-regional work) | C01-C04; jurisdiction notes: Marana uses it for non-regional flows only (C12/C14) |
| hechms-headless (new) | scripted HMS build/compute/rerun, any jurisdiction | /pima-rfcd (TECH-018 parameters, C05), /caltrans-california (CN calibration, C18); C06 depression bracketing in core |
| groundwater-reinfiltration-sizing (new) | Darcy seepage, storage, gallery depth check | /placer-county (5 ft SHGW, TRPA volume) (C16/C17) |
| fema-clomr-lomr-submittal (new, = drainage-report-build/fema detail) | MT-2 package, AD response, community items | none (FEMA is the jurisdiction); Region IX notes |

Add-on file content template (one per jurisdiction): governing manuals and current editions; hydrology method by watershed size; rainfall source and statistic; design storms (design vs FEMA/regional); report outline; critical facility rule; detention/first flush rule; inlet/street criteria; submittal and coordination quirks; acceptance items to confirm in writing.

Seed content per add-on from this group:
- Pima County RFCD: PC-Hydro 7.4 under 1 sq mi, HEC-HMS TR-55 parameters over 1 sq mi (TECH-015, TECH-018); NOAA Atlas 14 upper 90% (TECH-010); Tc program value, 5 min min; regulatory washes Q100 >= 100 cfs get 1D floodplains; 2D rain-on-grid needs RFCD acceptance (TECH-033); first flush Table 2.1 rates; drawdown 12/24 h; RDM Table 2-9 clogging; RDM 2.10 roadway crossing (10-yr contained, 100-yr overtopping 1 ft max). Cards RKN-017, RKN-016, RKN-006, VALENCIA-012, PHXZOO-004.
- City of Tucson: agency report outline with all sections kept; offsite area includes roadway and upstream subdivision draining to city storm drain, inlets assumed to capture 100-yr; critical facility improvements above 500-yr WSE; confirm City vs County review from parcel record and contract. Cards TANGERINE-017, -021, -023, -024, -015.
- Town of Marana: Town of Marana Drainage Manual (2024) governs (Northern Marana requirements folded in); Town Code 17-15-10 H.5 finished floor 1 ft above 500-yr WSE plus 500-yr delineation and erosion protection; MDM 4.1 non-regional flows for design and onsite PC-Hydro, regional for FEMA; MDM 4.5 FLO-2D build named; Town co-signs CLOMR/LOMR community acknowledgement with RFCD; regional vs local qualifier discipline. Cards BARNETT-004, BARNETT-006, NORTHLOOP-003, NORTHLOOP-010, NORTHLOOP-013.
- Town of Sahuarita: Lee Moore Wash basin study hierarchy (PCRFCD 2018 supersession memo, LMW-East TDN vs 2008-2009 Basin Management Study); 10-yr and 100-yr are the design events; Q500 not published; LMW mesh 30 ft or finer; LMW Development Criteria discourage levee-like features; Town code text not readable online, confirm with staff; County criteria (RDM 2.10) apply only once the Town confirms in writing. Cards PHXZOO-002, PHXZOO-004, SAHPARK-003, SAHPARK-019.
- FEMA: effective inflows (not county design flows) for FEMA comparisons; all effective storm cases present in package; FIS 0.2% profile only where cross sections bracket the site; Zone AO depth is not an elevation; 90-day AD response, no extensions; community items (flooding-source names, O&M with community as responsible party, owner notification template). Cards STARVALLEY-006, -017, -018, -022, NORTHLOOP-010, TANGERINE-021.
- Placer County CA (East Placer / Lake Tahoe Basin / TRPA): Stormwater Management Manual Ch. V Small Watershed (peak-only, under 1 sq mi); nested county storm at 1-min steps; West vs East of crest basis confirmed in writing; East Placer SWMP Manual 2024 (not West Placer) for WQ; 85th percentile WQV; hydromod post <= pre 2-yr over 1 ac new impervious; TRPA 20-yr 1-hr volume; 5 ft BMP separation to SHGW; storm drain 10-yr with HGL 0.5 ft below rim. Cards HOMEWOOD-001, -002, -008, -009, -011, -012, -013, -016.
- Caltrans / California: HDM Ch. 800-890; HDM 819.2 Rational to about 320 ac, HEC-HMS NRCS CN with 24-hr Atlas 14 above that, USGS SIR 2012-5113 regression check (Table 819.2C); FIS Q100 governs at FEMA crossings; HDM Table 808.1 programs only (WSPG/CivilD need District approval); culvert 10-yr HW/D <= 1.0 with 100-yr check; 25-yr spread to shoulder (rural > 45 mph); bridge 50-yr with 2 ft freeboard; treatment BMPs at 10,000 sf new impervious; Location Hydraulic Study for base floodplain encroachment; CN calibration on HSG C/D foothills. Cards CALFIRE-002, -006, -007.

---

### HJR-C01 PC-Hydro 7.4 web app execution (interactive and batch)
skill | update pchydro-hydrographs (Phase 2 + new reference/pchydro_batch_automation.md) | score 43 | hours 7 | cards 3 | projects 3 (EKOS-LOCAL, RKN, SAH) | confidence medium-high
Trigger: PC-Hydro peaks, program printouts and 1-min hydrographs are needed for one or many concentration points (watersheds under 1 sq mi) on pchydro.rfcd.pima.gov.
Steps (merged):
1. Record the terms-of-use approval once per project/run log; for unattended runs the approval is standing (see conflict 1). Click I Agree.
2. Choose mode: interactive (Claude in Chrome, few CPs) or batch (Playwright, Edge channel, headless or isolated browser; many CPs).
3. Load each .pk6 through File > Open (initialize the File-Open dialog before setting the file input); wait until the concentration-point field populates.
4. Set userName to "Psomas (<initials>)" before Calculate.
5. Read back every native input field and compare to the scenario/extract values; stop on any mismatch. Quantize flow-length segments to whole ft so they sum exactly to the native total length; allocate soil shares to whole percent by largest remainder so they total 100; log every precision change (source vs native).
6. Enter coordinates at 4 decimals; use the native Fetch Rainfall; wait for completion (Matches shown and 100-yr 1-hr field filled); compare to saved NOAA Atlas 14 upper 90% arrays at 2-decimal rounding; record the Atlas edition actually served.
7. Calculate; wait until calcDate changes and qp100 is filled; read q100 and tc100.
8. Save the program PDF (pdf.php), the 1-min hydrograph CSV (hydrograph.php / Generate Hydrograph), the recomputed .pk6, file hashes and a peaks table.
9. Log failed CPs and rerun only those. Keep the .pk6 inputs so any run can be repeated by hand if the web app changes.
10. Hand off to C03 export checks before any routing or DSS build.
Gotchas:
- App JS is obfuscated; button/field names and page functions (openProject, fillSCS, hydroCalc, hydroGraph, printFile) had to be found with probe scripts before automation worked (RKN-004, SAH-007; claude session).
- Vegetation density auto-fill behaviour had to be probed from the live page; confirm default cover densities match the PC-Hydro guide before a batch (SAH-007, claude session).
- File-chooser events timed out until the File-Open dialog was initialized properly (EKOS-LOCAL-006, claude session).
- Soils 52.263/41.418/6.318% rounded to 52/41/6 (total 99) failed validation; largest remainder 52/42/6 passed (EKOS-LOCAL-006, claude session).
- Full-precision GIS lengths failed the native length-sum check (EKOS-LOCAL-006, claude session).
- Never set fake valid flags or force Calculate enabled (EKOS-LOCAL-006, claude session).
- Direct HTTP rainfall request returned 403; use the in-app fetch (EKOS-LOCAL-006, claude session).
- The PC-Hydro guide cites an older Atlas 14 edition than the data now served; record the edition fetched (EKOS-LOCAL-006, claude session).
- pdf.php sometimes returns text/html instead of a PDF (seen at CP-103); check content-type and retry the CP (RKN-004, claude session).
- A local CORS helper server (127.0.0.1 with private-network headers) was used first to feed records to a tab; the Playwright file-input route is simpler (RKN-004, SAH-007; claude session).
- 67 subbasins ran in about 25 min once working (SAH-007, claude session).
- Web app changes can break the batch (SAH-007, claude session).
- Recurrence: 9 failed PC-Hydro tasks on one project (NOAA mapping x3, basin import x4, road scenario x1, benchmark) (EKOS-LOCAL-006, claude session).
- Existing skill gotchas retained: window move/resize re-renders and resets state; match the in-file Concentration Point field to the basin id (pchydro-hydrographs reference).
Jurisdiction add-ons:
- Pima County RFCD: PC-Hydro 7.4 is the accepted method under 1 sq mi (TECH-015); confirm the version the reviewing agency accepts when reusing an older study (see C02, ELTORO-009).
QC checks:
- Native input read-back matches scenario values field by field before Calculate.
- Fetched rainfall matches saved Atlas 14 upper 90% arrays at 2 decimals; edition recorded.
- Printout PDF content-type is application/pdf; userName shows the firm preparer string.
Source cards: EKOS-LOCAL-006, RKN-004, SAH-007

### HJR-C02 GIS concentration points, watersheds, .pk6 inputs and offsite inflow points
skill | update pchydro-hydrographs (new Phase 1b: GIS build of .pk6) | score 2 | hours 1.5 | cards 2 | projects 2 (ELTORO, RKN) | confidence medium
Trigger: Existing-conditions hydrology for many small watersheds (100+ CPs) on a large site, or offsite washes entering a model domain (e.g., through freeway cross-culverts) beyond the limits of prior studies.
Steps (merged):
1. Gather structure inventory: master plan inventory and DOT as-builts (size, station, invert) for each cross-culvert or entry point.
2. Condition the DEM (10-ft or finer; WhiteboxTools least-cost breach, D8 pointer and accumulation, streams >= 5 ac, slope).
3. Place CPs by rule: IN (offsite inflow >= 5 ac), OUTR/OUTX (exits across exclusion or other boundary), junctions, and one CP per cross-culvert.
4. Build incremental and total watersheds, longest watercourses, segment slopes, land-use and soil overlays.
5. Write one PC-Hydro 7.4 .pk6 (JSON) per CP under 1 sq mi with Atlas 14 upper 90% depths at the watershed centroid; route CPs over 1 sq mi to HEC-HMS (C05).
6. Run PC-Hydro (C01) for Q2/Q10/Q100 with the version the reviewing agency accepts.
7. Where the watershed to a culvert cannot be defined, use culvert capacity as the upper bound of inflow.
8. Enter each flow as an inflow BC at the culvert outlet (or domain edge) and add it to the model inflow register.
9. Keep a tracked rerun list for CPs whose inputs change after a DEM extension.
Gotchas:
- rasterio prints "NoneType has no attribute exc_info" tracebacks at interpreter exit; harmless; close datasets explicitly to keep logs clean (RKN-003, claude session).
- CPs whose inputs changed after the DEM extension need a tracked rerun list so carried results stay consistent (RKN-003, claude session).
- Source report covered only the central reach; north and south reaches had no inventory and had to be scoped as new work (ELTORO-009, claude session).
- A reviewer had already questioned the PC-Hydro version used in the source report; confirm version with the agency first (ELTORO-009, reviewer comment).
Jurisdiction add-ons:
- Pima County RFCD + ADOT: culvert data from ADOT as-builts; PC-Hydro for each watershed under 1 sq mi.
QC checks:
- Every inflow BC appears in the inflow register with source (study, new PC-Hydro run, or capacity bound).
- Nested-area check from C07 before any flows are summed.
Source cards: RKN-003, ELTORO-009

### HJR-C03 PC-Hydro hydrograph export QC: 1-min step, audited peak adjustment, volume, DSS transfer
qc_rule | update pchydro-hydrographs (Phase 3/4) + QC rule 05_QC_Rules | score 8 | hours 2 | cards 1 | projects 1 (EKOS-LOCAL) | confidence high
Trigger: Any PC-Hydro hydrograph passed to HEC-HMS, HEC-RAS, FLO-2D or a report table.
Steps (merged):
1. Confirm the actual sample spacing in the export is 60 s (not only the UI setting); units cfs.
2. Compare the sampled hydrograph maximum to the PC-Hydro reported peak; expect a difference.
3. Make a separate peak-adjusted copy that replaces the maximum ordinate with the reported peak; keep the native export unchanged; log the added volume.
4. Report equation-based runoff volume, integrated hydrograph volume and adjustment volume separately; do not reject an export because they differ.
5. Close a nonzero tail with one extra minute to zero; log the added volume.
6. Write to DSS (INST-VAL, CFS, 1Minute) and reopen; verify every ordinate, interval, units and volume.
Gotchas:
- Owner correction during the run: at steps other than 1 min the peak never matches and has to be adjusted manually (EKOS-LOCAL-007, claude via Codex session).
- An invented 1% volume-equality gate wrongly flagged the export as corrupt; the county manual defines the hydrograph integral as an approximation (EKOS-LOCAL-007, claude session).
- Recurrence: 4 catchment scenario sets (benchmark, basin, road crossing, HMS inflows) (EKOS-LOCAL-007, claude session).
- Existing skill: data_type not INST-VAL makes HMS read all zeros (pchydro-hydrographs reference/dss_formats.md); retained.
QC checks:
- Peaks table reports both reported peak and sampled max; report tables use the reported peak (see conflict 3 on hydrographs_to_xlsx.py).
- DSS round-trip verified ordinate by ordinate.
Source cards: EKOS-LOCAL-007

### HJR-C04 PC-Hydro input rules: default cover on graded ground, native runoff parameters, Tc
qc_rule | update drainage-report-build Sec. 3 + pchydro-hydrographs operating rules | score 1 | hours 0.5 | cards 1 | projects 1 (NORTHLOOP) | confidence high
Trigger: Onsite PC-Hydro runs that include graded (developed pad) ground.
Steps (merged):
1. Keep the PC-Hydro default vegetation cover for graded ground (stated as the program 20% default); no blanket 5% Desert Brush override.
2. Use the native runoff parameters for the selected cover and soil group; do not carry a fixed CN 86.
3. Tc is the program value, 5 min minimum.
Gotchas:
- Saved standards still carried the old 5% rule; the EOR correction overrides it; shared skill must be updated (NORTHLOOP-013, claude via Codex session / EOR correction).
Jurisdiction add-ons:
- Pima County and Town of Marana: rule observed on Marana onsite work using PC-Hydro.
QC checks:
- No PC-Hydro run shows a manually typed vegetation density or fixed CN on graded ground unless the EOR approved it.
Source cards: NORTHLOOP-013

### HJR-C05 HEC-HMS headless build, batch compute, rerun and DSS extraction
skill | new skill hechms-headless (core) + add-on hechms-headless/pima-rfcd (TECH-018); drainage-report-build Sec. 3 points to it | score 10.5 | hours 2.5 | cards 3 | projects 3 (CAMPBELL, RKN, SAH) | confidence medium-high
Trigger: HMS model built from GIS parameters (watershed systems over 1 sq mi in Pima County, many storms or areal-reduction variants), or verification of archived HMS results before reuse.
Steps (merged):
1. Work on copies in a native folder; archive old results and logs first; close HMS before copying (file locks).
2. Build: delineate subbasins with outlets just above junctions where both branches exceed a threshold area; write .hms/.basin/.met/.control/.gage text files from the parameter table; write paired data (storage-outflow, rating) with hecdss.
3. Check every input path exists before starting the chain.
4. Write a Jython script: OpenProject, ComputeRun for each run, Exit(1); run with HEC-HMS.cmd -s <script> from the HMS install folder.
5. Delete old results CSV before the run; read peaks, volumes and hydrographs from the project DSS (HecDss in the same Jython session or hecdss Python) for needed paths only.
6. Chain build, compute and read in one .cmd; write a .done file at the end for the next step.
7. For reproduction of archived work: compare each element peak and volume with archived values; list items not recomputed; check RAS inflow hydrographs match the HMS DSS series.
8. Critical storm = max of 3-hr and 24-hr (Pima).
Gotchas:
- Opening upgrades 4.12 projects to 4.13; work on copies (CAMPBELL-012, claude session).
- A Source element with ZERO_FLOW and no downstream link caused ClassCastException at every step; remove it in a documented copy (CAMPBELL-012, claude session).
- A 24-hr run never executed in the original (missing basin depths, ERROR 23430); report as missing, do not fill (CAMPBELL-012, claude session).
- Every -s run prints an XML/JAXB "Premature end of file" exception; harmless; confirm results exist rather than trusting the console (RKN-006, SAH-008; claude session).
- HEC-HMS 4.12 (the standard) was not installed; 4.13 used and logged as an EOR decision item (RKN-006, claude session).
- hecdss prints every zread to stdout (log reached 1.7 MB); redirect or lower the DSS message level (SAH-008, claude session).
- 50 runs (5 RP x 2 durations x 5 areal-reduction variants) gave a 492 MB DSS with 152,759 records; read only needed paths (SAH-008, claude session).
- First chain failed on a hard-coded input path that did not exist (hand-drawn berm file) (SAH-008, claude session).
- Copying an HMS project while HMS had it open failed with WinError 32 (SAH-008, claude session).
Jurisdiction add-ons:
- Pima County RFCD (TECH-018): SCS CN from PC-Hydro ADOT tables; SCS UH with lag 0.6 Tc (TR-55 segmented Tc); Modified Puls routing from normal-depth storage-outflow; Atlas 14 upper 90% at system centroid with areal reduction over 1 sq mi; PC-Hydro hydrographs for subbasins under 1 sq mi may enter HMS as Source elements on the same junction/reach network (SAH-007).
- Caltrans/California: see C18 (calibrate CN to FIS/regression).
QC checks:
- HMS version recorded in report and log; any departure from the governing version is an EOR decision item.
- Results existence and element count checked after compute, independent of console text.
Source cards: CAMPBELL-012, RKN-006, SAH-008

### HJR-C06 Closed depressions bracketed as contributing and non-contributing
skill | new skill hechms-headless (section: depression bracketing) + agent model-run-supervisor (paired runs) | score 3 | hours 1.5 | cards 1 | projects 1 (SAH) | confidence medium
Trigger: Closed depressions (mine pits, tailings toes, stock ponds) inside the watershed of a 2D or HMS model.
Steps (merged):
1. Fill depressions on the DEM (WhiteboxTools); keep those over a volume threshold (20 af used); compute volume, area and catchment (8 found, 7,727 af total on SAH).
2. Run HMS twice: depressions filled (contributing) and catchments removed (non-contributing); compare peaks at key CPs.
3. Run the same non-contributing variant in the PC-Hydro routing model.
4. For FLO-2D, run a filled-terrain variant only after checking cells at the fill edges.
Gotchas:
- Mine areas changed 30 to 80 ft between 2015 and 2021 terrain; terrain vintage controls depression volumes (SAH-016, claude session).
- Non-contributing treatment of pits and impoundments was based on public disclosures and permits; needs agency agreement at the methodology meeting (SAH-016, claude session).
Jurisdiction add-ons:
- Pima County RFCD TECH-018: depression treatment is a methodology-meeting item.
QC checks:
- Both bracketing runs reported; terrain vintage stated.
Source cards: SAH-016

### HJR-C07 Watershed delineation and area accounting (nested areas, topo support, tributary roadway/storm drain)
qc_rule | QC rule 05_QC_Rules + update drainage-report-build Sec. 1 + drainage-report-exhibit-standards; add-on drainage-report-build/city-of-tucson | score 18 | hours 4.5 | cards 3 | projects 2 (EKOS-LOCAL, TANGERINE) | confidence high
Trigger: Any watershed delineation (terrain-derived or hand-drawn), especially small flat sites, nested outlet areas, or offsite areas discharging to an existing storm drain.
Steps (merged):
1. List each catchment with its parent; state which outlet areas include upstream basins or pipe catchments.
2. Run a total-area unattenuated scenario once; never add upstream basin outflows or pipe catchment flows to it. Where detention is modeled, route upstream outflow and add only the incremental downstream area.
3. Load soils and other attributes by the same catchment key as geometry; stop on mismatched keys.
4. Show topo on every watershed exhibit; boundaries follow visible ridge lines; 1-ft contours minimum, 0.5-ft on flat sites; highlight depressions and the flow line into them.
5. Draw flow arrows that agree with contours; show the Tc flow path; call it a flowline where no stream exists.
6. Set the onsite watershed boundary at the project boundary so pre vs post is shown there (consistent with drainage-report-build Sec. 1).
7. For offsite areas near a storm drain: bring in the storm drain, manholes and inlets; include roadway and upstream subdivision areas tributary to it; state the inlet capture assumption; label upstream offsite infrastructure.
Gotchas:
- Candidate areas 40.0, 27.8, 27.0 and 12.9 ac were nested; summing would roughly triple the flow (EKOS-LOCAL-008, claude session).
- Local draft narrative started summing basin and road flows until guarded (EKOS-LOCAL-008, claude session).
- Flow arrows contradicted contours and one boundary had no supporting ridge (TANGERINE-023, JCO redline).
- Offsite watershed omitted roadway and subdivision areas tributary to the storm drain (TANGERINE-024, JCO redline).
Jurisdiction add-ons:
- City of Tucson: assume inlets capture the 100-yr flow at each inlet unless shown otherwise; include city storm drain base (TANGERINE-024).
QC checks:
- Parent-child area table; sum of incremental areas equals total; no flows summed across nested areas.
- Every boundary segment supported by contours; arrows agree with contours.
Source cards: EKOS-LOCAL-008, TANGERINE-023, TANGERINE-024

### HJR-C08 Unsurveyed basin outlet topology: as-built search and versioned owner assumptions
qc_rule | QC rule 05_QC_Rules + agent due-diligence-researcher (records search) + model-run-supervisor (scenario versioning) | score 6 | hours 2 | cards 1 | projects 1 (EKOS-LOCAL) | confidence medium
Trigger: Detention basin routing where the outlet pipe, overflow weir or spill path is not surveyed.
Steps (merged):
1. Search as-built plans and GIS pipe layers for outlet pipe, overflow weir and spill route before modeling.
2. If records are missing, ask the owner once for a preliminary assumption; store it as a versioned scenario with source = owner.
3. Fallback with no invert data: set pipe from lidar with minimum 1 ft cover, tied to outfall ground.
4. Supersede earlier clarifications explicitly (keep the superseded file); never overwrite silently.
5. Flag implausible derived slopes rather than adopting them.
Gotchas:
- Outlet description changed twice in one session (spill to ROW swale, then bottom pipe plus overflow weir); routing built on the first had to be redone (EKOS-LOCAL-015, claude via Codex session).
- Assumed pipe produced 0.017% slope (EKOS-LOCAL-015, claude session).
- Preliminary default used on that project (24-in RCP inlet 1 ft above basin bottom) is project-specific, not a library default (EKOS-LOCAL-015).
QC checks:
- Every outlet element in the model cites as-built, survey or a versioned owner assumption.
Source cards: EKOS-LOCAL-015

### HJR-C09 Preliminary detention, first-flush and sediment storage with per-pod ledger
skill | update drainage-report-build Sec. 1 (core) + add-on drainage-report-build/pima-rfcd | score 4.6 | hours 1.3 | cards 2 | projects 2 (RKN, TANGERINE) | confidence high
Trigger: Proposed conditions increase peak flow at perimeter outfalls, new impervious area is created, or the site lies in a Pima County critical basin.
Steps (merged):
1. Give preliminary pre vs post peak Q and storage estimates even at concept level.
2. Preliminary detention where PR > EX (2, 10, 100-yr): Vs = Vin,PR x (1 - Qex/Qpr); take the max of the three events; replace with a routed design at final.
3. Separate flood detention, first-flush/water-quality retention, sediment storage and optional harvesting; each has its own criteria and maintenance.
4. For distributed (block-level) detention, tabulate allowable outflow and volume per development pod and the phasing trigger.
5. Name maintenance access and responsible entity.
6. Flag basins in mapped riparian habitat and outfalls direct to a major wash (detention waiver candidates).
Gotchas:
- First version used 0.5 in over impervious area only; corrected to Table 2.1 rates including disturbed pervious and drawdown checks (RKN-016, claude session).
- Concept report left block-level detention unsized and unassigned; reviewers and the landowner agency asked for a per-pod ledger (TANGERINE-015, reviewer comment).
- Internal QC asked for preliminary pre-post detention and first-flush estimates in the hydraulics appendix (TANGERINE-015, JCO redline).
Jurisdiction add-ons:
- Pima County RFCD: Detention/Retention Standards Table 2.1 lower-permeability rates, 1,440 cf/ac new impervious + 140 cf/ac disturbed pervious; retain below outlet invert, max 9 in deep; drawdown 12 h for basins <= 10 ac, 24 h > 10 ac; required field rate = 9 in x FS 2.0 / drawdown limit until testing; higher Table 2.1 values in riparian habitat (RKN-016).
- City of Tucson / Town of Marana: same separation of detention, first flush and sediment requested (TANGERINE-015).
- Placer County: storage must be shown with a hydrograph method (C15).
QC checks:
- Ledger table per pod: allowable Q, required volume, phasing trigger, responsible entity.
Source cards: RKN-016, TANGERINE-015

### HJR-C10 Design discharge traceability: one value, one qualifier, one source per flow
qc_rule | QC rule 05_QC_Rules + report-writer/qc-reviewer check; Standard v0.3 change (design discharge table) | score 25 | hours 5 | cards 2 | projects 2 (BARNETT, SAHPARK) | confidence high
Trigger: Any report or memo that carries regional and local flows, or adopts flows from a regional study instead of new hydrology.
Steps (merged):
1. Define regional and local storms and their peaks once in existing conditions; use the qualifier with every reference (10-yr regional, 100-yr local); no synonyms (non-regional, localized).
2. Build a design discharge table: source cross section or culvert record ID, location, Q10, Q100, governing duration, use (crossing vs parallel flow).
3. Use only recurrence intervals that are design standards for the jurisdiction; stop and check any other value.
4. Restate the design basis in the design section with the same wording and numbers; one value per flow.
5. Check every map caption and table title against the storm of the values shown.
6. Keep the summary flow consistent with the flow used to size the structure.
7. Write allowable velocity as the velocity permitted over a lining or soil, not the velocity of the soil.
Gotchas:
- Design-basis summary sentence in the 30% DCR reintroduced the ambiguity flagged earlier even though definitions existed (BARNETT-006, agency redline).
- One flow quoted as 4,324 cfs and 4,325 cfs in different places (BARNETT-006, agency redline).
- Draft labeled a 100-yr value as 200-yr; source study has no 200-yr flows (SAHPARK-003, JCO redline).
- Inflow map captioned 10-yr showed 100-yr rates (SAHPARK-003, JCO redline).
- Missing table referenced in hydrology text (SAHPARK-003, JCO redline).
- Approach flow (2,673 cfs) quoted as the crossing flow when the culvert was sized for 534 cfs (SAHPARK-003, JCO redline).
- Prior report stated the 500-yr basis two ways (NORTHLOOP-010; cross-ref C12).
Jurisdiction add-ons:
- Town of Marana: regional vs local (non-regional) terminology per MDM 4.1 (BARNETT-006, NORTHLOOP-003).
- Town of Sahuarita / LMW: 10-yr and 100-yr are the design events (SAHPARK-003).
QC checks:
- Every Q in text, tables, captions matches the design discharge table (value, event, duration, source).
- No recurrence interval outside the jurisdiction design set unless explicitly a sensitivity.
Source cards: BARNETT-006, SAHPARK-003

### HJR-C11 Adopting published regional or effective hydrology as the design basis
skill | update drainage-report-build Sec. 0 (core) + agent due-diligence-researcher; add-ons /town-of-sahuarita (LMW) and /fema | score 6.5 | hours 3.5 | cards 2 | projects 2 (PHXZOO, STARVALLEY) | confidence medium
Trigger: Scope relies on published regional flows (e.g., PCRFCD basin study TDN) or an effective FEMA study instead of new offsite hydrology.
Steps (merged):
1. Read the agency supersession memo first; confirm which study governs at the site (study limits).
2. Take Q10/Q100 at the site from the governing tables; state which engine's results are used where several are tabulated (PC-Hydro, HEC-HMS, FLO-2D).
3. For an effective FEMA study: read the TDN storm list (duration, depth) and controlling-storm statement; confirm the package has the upstream rainfall-runoff model and inputs for every storm case; request missing cases from the community or FEMA library before modeling.
4. Use effective inflows, not county design flows, for FEMA comparisons; flag as open whether FEMA and agency design flows share an engineering basis.
5. If an event beyond the published set (e.g., 500-yr) is in scope, note it is not published; get written client agreement to a ratio method or scope it as additional service.
6. Apply the study's technical guidance (mesh size etc.) to any new model.
7. Represent existing flow splits (e.g., berm breakout) rather than assuming containment.
Gotchas:
- Scope asked for refuge to the 500-yr while the design basis covered 10/100-yr only; carried as a client decision (PHXZOO-002, claude session).
- Existing berm breaks out near the 10-yr event; existing split must be represented (PHXZOO-002, claude session).
- Effective TDN listed 3-hr 3.34 in and 24-hr 4.55 in storms; only the 3-hr case was in the package; main package and blind rebuild both ran 3-hr only; do not claim a flood envelope from one storm (STARVALLEY-022, claude session).
Jurisdiction add-ons:
- Town of Sahuarita / Pima County RFCD: Lee Moore Wash study hierarchy (2018 supersession memo; LMW-East TDN vs 2008-2009 Basin Management Study); mesh 30 ft or finer; sheet-flooding zone context, pre-ordinance berms cannot be compelled to be enlarged (PHXZOO-002).
- FEMA: all effective storm cases; effective inflows for comparisons (STARVALLEY-022).
QC checks:
- Design basis section names the governing study, table, engine and storm cases used.
Source cards: PHXZOO-002, STARVALLEY-022

### HJR-C12 Critical facility 500-yr basis and FEMA floodplain discussion
qc_rule | update drainage-report-build Sec. 1 + drainage-report-exhibit-standards (critical facility line); add-ons /town-of-marana, /city-of-tucson, /pima-rfcd, /fema | score 11 | hours 4 | cards 3 | projects 2 (NORTHLOOP, TANGERINE) | confidence high
Trigger: Substation, BESS, utility or emergency facility in or near a FEMA or local floodplain; any site needing a 500-yr WSE.
Steps (merged):
1. Confirm critical facility designation with the jurisdiction and state the requirement (improvements above the 500-yr WSE, plus any freeboard).
2. Add a FEMA floodplain section: effective zones, floodway, BFEs, how they constrain design; state the consequence if existing ground is below the 500-yr WSE.
3. Check NFHL cross sections against the parcel; use the FIS 0.2% profile only where its sections bracket the site; Zone AO depth/velocity is not an absolute 500-yr elevation.
4. Where only 100-yr hydrographs exist, a 1.75 x Q100 ordinate scaling is a sensitivity only; label provisional; obtain the accepted 500-yr hydrology from the agency.
5. Tabulate floor, pad and equipment elevations with datum and the controlling 100-yr and 500-yr WSE.
6. Exhibit: 500-yr limit, 1-ft WSE contours, FEMA lettered cross sections; legend lists only zones present and includes floodway hatch.
7. Confirm early with the agency: facility classification, accepted 500-yr hydrology, engine build, collector channel and outlet criteria.
Gotchas:
- Nearest mapped cross section was about 1,848 ft from the development boundary; the river profile could not be used (NORTHLOOP-010, claude session).
- Prior report stated the 500-yr basis two ways (1.75 x Q100 and a 10-yr reference) (NORTHLOOP-010, EOR markup).
- Prior report used equipment above the 500-yr and 1 ft above the 100-yr, which no longer meets current code (NORTHLOOP-003, claude session).
- Archived model outputs showed FLO-2D builds 19.07.21 and 21.08.23, not the manual build; treat as historical until accepted (NORTHLOOP-003, claude session).
- Runs moved to build 26.02.25 to avoid a startup failure; departs from MDM 4.5, needs Town acceptance (NORTHLOOP-003, claude session).
- Draft omitted critical facility and 500-yr discussion; legend listed Zone A not on the map and missed floodway hatch (TANGERINE-021, JCO redline).
Jurisdiction add-ons:
- Town of Marana: Town Code 17-15-10 H.5 finished floor 1 ft above 500-yr WSE; H also requires 500-yr delineation and erosion protection; MDM 4.5 FLO-2D build; MDM 4.1 non-regional for design (NORTHLOOP-003).
- City of Tucson / Pima County RFCD: improvements above 500-yr WSE (TANGERINE-021).
- FEMA: FIS profile applicability and AO limitation (NORTHLOOP-010).
QC checks:
- 500-yr source stated once (FIS profile with bracketing XS, agency hydrology, or labeled provisional sensitivity).
- Legend zones match map.
Source cards: NORTHLOOP-010, NORTHLOOP-003, TANGERINE-021

### HJR-C13 Imperviousness and cover from classified imagery need independent labels
qc_rule | QC rule 05_QC_Rules | score 4 | hours 2 | cards 1 | projects 1 (EKOS-LOCAL) | confidence medium
Trigger: Estimating percent impervious or vegetative cover from NAIP or other imagery with a model-based classifier.
Steps (merged):
1. Use dated native-resolution imagery with locked raster IDs.
2. Build training and holdout labels independently of the model being tested; check shadow and tree occlusion.
3. Report agreement as diagnostic only; set a minimum acceptance before using percentages.
4. If the classifier fails, run explicitly labeled cover scenarios (S1/S2/S3).
5. Check imagery coverage of the full hydraulic extent separately from the watershed.
Gotchas:
- Classifier on 128 model-labeled points reached 68.75% agreement (67% balanced) with 60% of the main catchment unknown; failed and not used (EKOS-LOCAL-019, claude session).
- Model labeled a shadow as vegetation; labels are not field truth (EKOS-LOCAL-019, claude session).
- First imagery set did not cover the north reach (EKOS-LOCAL-019, claude session).
QC checks:
- No percent impervious in a model without a stated source (plans, independent labels meeting acceptance, or named scenario).
Source cards: EKOS-LOCAL-019

### HJR-C14 Governing manual and hydrology method selection by jurisdiction
skill | update drainage-report-build Sec. 0 (core method-selection step) + add-ons /pima-rfcd, /town-of-marana, /caltrans-california | score 4.4 | hours 1.4 | cards 3 | projects 3 (BARNETT, CALFIRE, RKN) | confidence medium-high
Trigger: Start of any drainage study, report or memo.
Steps (merged; core step for drainage-report-build Sec. 0):
1. Confirm jurisdiction from the plat case, parcel data and contract before choosing manuals.
2. Cite the current governing manual edition; do not cite superseded documents; cite the current version of any redone prior study.
3. Select the hydrology method by watershed size and jurisdiction (add-on table); state rainfall source, statistic, return period and duration.
4. Tabulate concentration points with method, area and design Qs.
5. Keep a refs folder with the governing policies and program guides for citation.
Gotchas:
- Confirm jurisdiction from the County plat case and parcel data before choosing manuals (RKN-017, claude session).
- Development Engineering flagged the superseded Northern Marana document in four places (BARNETT-004, agency redline).
- Which method Caltrans District Hydraulics accepts for mid-size watersheds (HMS vs regression) is not written; confirm before final (CALFIRE-006, claude session).
Jurisdiction add-ons:
- Pima County RFCD: PC-Hydro 7.4 < 1 sq mi; HEC-HMS TR-55 > 1 sq mi (TECH-015, TECH-018); Atlas 14 upper 90% (TECH-010); Tc program value, 5 min min; Q100 >= 100 cfs regulatory washes 1D; 2D rain-on-grid needs RFCD acceptance (TECH-033) (RKN-017).
- Town of Marana: Town of Marana Drainage Manual (2024); CLOMR/LOMR coordination names RFCD and the Town; the Town signs the community acknowledgement (BARNETT-004).
- Caltrans/California: HDM 819.2 Rational to about 320 ac, Atlas 14, Tc floor 5 min; HEC-HMS NRCS CN + UH + 24-hr Atlas 14 above that; USGS SIR 2012-5113 regression check (Table 819.2C); FIS Q100 governs at FEMA crossings; roadside areas delineated from DEM flow paths and road crests/sags (CALFIRE-006).
- Placer County: see C15/C16.
QC checks:
- Governing manual edition cited matches the add-on list; no superseded document names.
Source cards: RKN-017, BARNETT-004, CALFIRE-006

### HJR-C15 Placer County hydrology: Small Watershed peaks, nested design storm, crest side, peak-only limit
skill | jurisdiction add-on drainage-report-build/placer-county (with scripts sw.py, storms.py as add-on tools) | score 55 | hours 17 | cards 4 | projects 1 (HOMEWOOD) | confidence high
Trigger: Placer County site needing peak flows, design storms or storage analysis (Stormwater Management Manual Ch. V), especially above 5,000 ft near the Sierra crest.
Steps (merged):
1. Decide method scope: Small Watershed (Sec. V.E.2, Qp = qA - ApFi) for peaks used in inlet and upper-system pipe sizing only; any storage, peak control or HGL uses a hydrograph method (Sec. V.E.2.a, V.E.3, kinematic wave basis). Do not mix a peak-only worksheet with a model generating unrelated runoff.
2. Crest side: run every case with both West and East of crest Table 5-A and Fig. 5-3 values; compare to NOAA Atlas 14 at the site; get County confirmation in writing; state the basis.
3. Small Watershed inputs per area: area, % impervious, overland segments (L, S, n), collector segments (L, S, n, Z, contributing area).
4. Overland travel time by Eq. 5-3; gutter, pipe, swale and pavement by Eq. 5-4 (collector).
5. Fi by Eq. 5-5 at site elevation using Table 5-3 rates, same framework pre and post.
6. Unit peak q from Fig. 5-3 for tr and elevation on the chosen side; 50-yr by log-frequency interpolation between 25 and 100-yr.
7. Qp = q x A - Ap x Fi with Ap = A x (1 - imp/100); imp as a fraction in formulas.
8. Report unrouted sum of area peaks vs existing; note the method cannot credit storage.
9. Nested design storm for hydrograph models: Table 5-A-1 depth at 5,000 ft plus change per 1,000 ft for the crest side; depths at site elevation 5 min to 24 hr; log-log interpolate cumulative depth at 1-min step (required when tr < 10 min); nest incremental depths with the maximum at mid-storm alternating after/before (App. V-B); build 24-hr 2/10/100-yr and 1-hr storm for a 50-yr 1-hr criterion; write as VOLUME series.
10. Water quality event: scale the 2-yr shape to the 85th percentile depth (1.2 in at 6,000-6,500 ft).
11. Keep a live-formula workbook (Basis, Fig 5-3 digitized, Post, Pre, Pre vs Post).
Gotchas:
- % impervious typed as a whole number (7 not 0.07) made the infiltration term add flow; existing 10-yr peak went 7.87 to 4.32 cfs after the fix and reversed the pre/post conclusion (HOMEWOOD-001, claude session).
- Eq. 5-3 used for every collector overstated tr (pipe 2.99 vs 0.58 min; swale 21.1 vs 8.7 min) and understated post peaks (HOMEWOOD-001, claude session).
- Post pervious set to 0 in/hr while existing used 0.09 in/hr; use consistent Table 5-3 rates (HOMEWOOD-001, claude session).
- 100-yr sheet headers labeled 10-yr, offsite sheet at wrong elevation, 100% impervious DMAs entered as 0%, broken summary references (HOMEWOOD-001, claude session).
- Digitize Fig. 5-3 once (curves linear 5,000 ft to crest and crest to 5,000E) and reuse; check against a known hand pick (HOMEWOOD-001, claude session).
- Model used 5-min rainfall steps; county requires 1-min for short tr (HOMEWOOD-002, claude session).
- TR-55 CN runoff on a 1-hr storm does not reproduce county peaks; runoff method must also match, not only the storm (HOMEWOOD-002, claude session).
- Site drains east of crest but Atlas 14 matched West values; East results about 35% lower and changed conveyance findings (HOMEWOOD-011, claude session).
- WQ findings are volume-based and do not depend on crest side (HOMEWOOD-011, claude session).
- Two incompatible methods mixed for weeks; model peaks 4-7 times lower than worksheet peaks, irreconcilable (HOMEWOOD-012, claude session; manual markup).
Jurisdiction add-ons:
- This cluster is the Placer County add-on content for hydrology; tools sw.py / storms.py become add-on scripts.
QC checks:
- Impervious entered as fraction; collector segments use Eq. 5-4; same infiltration framework pre/post; headers match event.
- Crest-side basis stated and County-confirmed.
- No storage credit claimed from Small Watershed results.
Source cards: HOMEWOOD-001, HOMEWOOD-002, HOMEWOOD-011, HOMEWOOD-012

### HJR-C16 East Placer / TRPA water quality and BMP criteria checklist
qc_rule | jurisdiction add-on drainage-report-build/placer-county (WQ/BMP checklist) + QC rules | score 22 | hours 8 | cards 3 | projects 1 (HOMEWOOD) | confidence high
Trigger: Start of any drainage memo or SWQP in Placer County within the Lake Tahoe Basin; filling the East Placer SWQP template; siting infiltration BMPs.
Steps (merged):
1. Use East Placer (not West Placer) manual and SWQP template names.
2. Peak flow per C15; storm drain 10-yr design (Sec. VI); HGL at least 0.5 ft below rim/grate (project criterion also applied to 50-yr 1-hr).
3. Water quality: retain/infiltrate the 85th percentile WQV (East Placer Sec. 4.3.4). In SWQP Form 3-1 enter actual site elevation; back-check WQV = impervious area x runoff coeff x unit depth; confirm the memo depth matches; do not equate the 85th percentile 24-hr depth to the 50-yr 1-hr depth.
4. Hydromodification: projects over 1 ac new impervious, post <= pre 2-yr (Sec. 4.4); check project master plan for added 50-yr 1-hr post <= pre.
5. TRPA BMP Handbook 4.1-d: size subsurface infiltration to retain at least the 20-yr 1-hr volume from tributary impervious area; prefab chambers 80-90% voids vs 40% gravel.
6. BMP siting: document SHGW at each footprint; bottom at least 5 ft above SHGW (East Placer Sec. 3.1.1) or move, redesign or get a variance; check geotech limits on infiltrating above lowest foundations.
7. Infiltration rate: field rate at BMP depth; until tested use half the NRCS rate (1.0 in/hr on HOMEWOOD) with a 0 in/hr sensitivity.
8. Keep one source for DMA impervious areas across memo, exhibit and template.
Gotchas:
- Template set at 6,600 ft gave 1.0 in unit WQV; site at about 6,300 ft gives 0.9 in; memo claimed 1.3 in (a West-of-crest 50-yr 1-hr value) (HOMEWOOD-008, claude session).
- DMA impervious areas differed between memo/exhibit and SWQP template version (HOMEWOOD-008, claude session).
- Memo assumed 2 ft separation; SHGW at galleries not documented (HOMEWOOD-009, claude session).
- Team assumption of 2 ft for the groundwater reinfiltration CMP needs confirmation against the 5 ft rule (HOMEWOOD-009, claude session).
- Memo cited the West Placer manual throughout for an East Placer site (HOMEWOOD-013, claude session).
Jurisdiction add-ons:
- Placer County / East Placer / TRPA: entire cluster is add-on content.
QC checks:
- Manual names East Placer; WQV back-check matches; 5 ft SHGW separation documented per BMP; TRPA 20-yr 1-hr volume met.
Source cards: HOMEWOOD-008, HOMEWOOD-009, HOMEWOOD-013

### HJR-C17 Groundwater displacement and reinfiltration sizing
skill | new skill groundwater-reinfiltration-sizing (core) with add-on /placer-county (5 ft SHGW, TRPA) | score 50 | hours 10 | cards 1 | projects 1 (HOMEWOOD) | confidence medium
Trigger: Building cuts or foundations intercept perched/seasonal groundwater that must be captured and reinfiltrated.
Steps (merged):
1. Get perched water height and seepage area from geotech; map cut depth to foundations vs SHGW.
2. Q = k x A x i (Darcy) per impeded face; storage required = Q x 24 hr.
3. Size the gallery by infiltration area from geotech.
4. Depth check for CMP: diameter + 2 in bedding + 12 in cover to bottom of structural section + structural section + separation to SHGW.
5. Route foundation drains on the upslope side to the facility; provide overflow; slope paving 2% away from buildings.
6. Keep one dated workbook and a design-reasoning note; log each revision driver (architecture, cuts, geotech).
Gotchas:
- Calc reworked 5 times Apr-Aug as architecture, cuts and geotech changed (HOMEWOOD-016, claude session).
- Whether overflow is needed for GW reinfiltration was left open in markups; geotech says overflow must be incorporated (HOMEWOOD-016, reviewer comment / coordination markup).
Jurisdiction add-ons:
- Placer County / Tahoe: separation to SHGW per East Placer 5 ft rule (C16, HOMEWOOD-009).
QC checks:
- Overflow path shown; SHGW separation value cited to the governing rule.
Source cards: HOMEWOOD-016

### HJR-C18 NRCS CN calibration to FIS and regression on clay foothill basins
qc_rule | add-on hechms-headless/caltrans-california + QC rule 05_QC_Rules (calibrate-or-justify any uncalibrated CN model) | score 1 | hours 1 | cards 1 | projects 1 (CALFIRE) | confidence high
Trigger: HEC-HMS CN model with Atlas 14 24-hr storm on HSG C/D foothill watersheds.
Steps (merged):
1. Reconcile DEM watershed area with the FIS area before calibrating.
2. Compare uncalibrated Q100 with FIS and regression.
3. Sweep a uniform CN reduction (6 to 14 points); pick the one matching FIS Q100.
4. Check the full frequency curve after calibration.
5. Keep the uncalibrated 100-yr as a sensitivity run through the hydraulics (culvert and 2D).
6. Put the calibration and its limits in the open items for District Hydraulics confirmation.
Gotchas:
- Uncalibrated HMS Q100 was about 1.9x FIS on the 9 sq mi creek and 2.5x regression on the 0.79 sq mi tributary (CALFIRE-007, claude session).
- Calibrated 2-yr fell below regression (18 vs 27 cfs) (CALFIRE-007, claude session).
- A 14-point CN cut is large; report it plainly (CALFIRE-007, claude session).
- DEM watershed for the creek differed from the FIS area (CALFIRE-007, claude session).
Jurisdiction add-ons:
- Caltrans District 10 / California foothills (add-on hechms-headless/caltrans-california).
QC checks:
- Any CN model on HSG C/D compared to an independent estimate (FIS, regression) before use; calibration magnitude reported.
Source cards: CALFIRE-007

### HJR-C19 Confirm reviewing agency and follow its report outline
qc_rule | update drainage-report-build Sec. 0 + Standard v0.3 change (outline per agency, Intentionally left blank rule); add-on /city-of-tucson | score 12 | hours 3 | cards 1 | projects 1 (TANGERINE) | confidence high
Trigger: Starting or reviewing a drainage report for a specific reviewing agency.
Steps (merged):
1. Confirm the reviewing agency (City vs County) from property records and the contract before drafting.
2. Use the agency standard report outline as the section list; keep every section; where nothing applies write "Intentionally left blank" with the reason.
3. Split existing conditions into hydrology (offsite and onsite watersheds with calcs) and existing stormwater infrastructure.
4. Import styles from the current firm template when starting from an agency outline document.
Gotchas:
- Draft did not follow the City outline; restructure requested and all City sections required even when empty (TANGERINE-017, JCO redline).
- Jurisdiction unclear (City vs County); a second reviewer noted contracts and parcel map point to County (TANGERINE-017, reviewer comment).
Jurisdiction add-ons:
- City of Tucson: City manual outline is the section list.
QC checks:
- Section list matches agency outline one to one.
Source cards: TANGERINE-017

### HJR-C20 Inlet clogging and sump grate factors
qc_rule | add-on drainage-report-build/pima-rfcd (RDM Table 2-9) + QC rule 05_QC_Rules | score 4.5 | hours 1.5 | cards 1 | projects 1 (VALENCIA) | confidence high
Trigger: Sizing or checking curb openings, scuppers or grates.
Steps (merged):
1. Apply the jurisdiction clogging factors (Pima: 0.80 curb openings, 0.50 grates, on grade and sump).
2. If the calculator has no clogging input, reduce opening length or grate area to the effective value (25 ft clear = 20 ft effective).
3. State that the 1.25 length multiplier is the reciprocal of 0.80, not a bypass allowance.
4. Recompute capture/bypass for 10-yr and 100-yr; route changed bypass downstream.
Gotchas:
- Two-grate sump with one grate assumed fully blocked already covers clogging; applying 50% again double counts (VALENCIA-012, agency redline).
- Inlet depression in calcs must follow PAG Std Detail 305 apron depression (VALENCIA-012, agency redline).
- Do not claim no bypass at all inlets unless the calcs show it (VALENCIA-012, agency redline).
Jurisdiction add-ons:
- Pima County RFCD / DOT: RDM Table 2-9 factors; PAG Std Detail 305.
QC checks:
- Effective length/area shown in calcs; no double clogging reduction.
Source cards: VALENCIA-012

### HJR-C21 FEMA CLOMR/LOMR submittal management: AD response, concept phases, community items
skill | new skill fema-clomr-lomr-submittal (= add-on drainage-report-build/fema) + agent model-run-supervisor (rerun-all gate) | score 66 | hours 38 | cards 3 | projects 1 (STARVALLEY) | confidence high
Trigger: CLOMR/LOMR case in preparation or an AD letter received.
Steps (merged):
1. On AD letter receipt: log the 90-day deadline (no extensions); plan the last model run at least 10 days before it; start community-dependent items the same day.
2. Every response row states what changed, file name, folder and report page; any status other than addressed does not ship.
3. Re-run every model after its last input edit, including existing conditions used for comparison.
4. If an item needs a decision the agency already rejected, settle it by call before resubmitting.
5. Concept-level phases: expect FEMA to require removal or design-level grading and drainage plans; decide early; make build and post-processing scripts switchable (environment variable) to produce with-phase and without-phase packages from the same sources; if kept, produce a conceptual grading and drainage exhibit (contours, flow arrows, spot elevations).
6. Community items: signed acceptance of flooding-source names for each new AO/AH/AE source; O&M plan naming each FEMA-required basin, community (not an HOA) as ultimate responsible party, who maintains and how often, community official signature or concurrence; O&M scope does not exclude public basins or channels; CLOMR (not LOMR) owner-notification template with approved names, draft submitted before mailing.
Gotchas:
- Response sent 37 days early with unrun models and missing community letters; case closed for insufficient data, resubmitted as a new case (STARVALLEY-006, FEMA review).
- FEMA rejected the concept mass-grading narrative in AD01, AD02 and the closure; two packages built for the new case (STARVALLEY-017, FEMA review).
- Revised O&M named the HOA, excluded public basins, lacked community signature block and did not name basins; two community items open at closure and at new-case build (STARVALLEY-018, FEMA review).
Jurisdiction add-ons:
- FEMA Region IX with Pima County RFCD as community; in Marana the Town also signs (C14, BARNETT-004).
QC checks:
- Rerun-all gate: model output timestamps later than last input edit for every model (model-run-supervisor).
- Response matrix 100% addressed; community letters in hand before upload.
Source cards: STARVALLEY-006, STARVALLEY-017, STARVALLEY-018

### HJR-C22 Criteria research before scoping or coordination meetings
agent | agent due-diligence-researcher (separate from minutes/report writer); add-ons /town-of-sahuarita, /caltrans-california | score 21.3 | hours 3.3 | cards 2 | projects 2 (CALFIRE, PHXZOO) | confidence medium-high
Trigger: Before a scoping or coordination meeting with open questions that depend on local, county, state or federal criteria; any work inside Caltrans R/W or a California city/county.
Steps (merged):
1. Assemble the governing document set (manuals, permits, FIS/LOMRs, local codes and plans).
2. Run a keyword highlighter on each PDF (section numbers, table numbers, thresholds) and write a highlight index (file, source, blocks, pages, terms).
3. For each numbered question record citation and status (confirmed, county-only, not found).
4. Write a known vs unknown criteria table for the meeting; mark County criteria as County until the Town confirms in writing.
5. After the meeting merge the recorded notes into the agenda as outcome callouts; list items still open as client decisions.
6. Keep the research agent separate from the minutes/report writer so unverified findings stay OPEN.
Gotchas:
- Highlighter terms must match manual wording; USGS SIR 2012-5113 returned only 4 hits on region terms; check regression region name manually (CALFIRE-002, claude session).
- Highway class and posted speed control the Table 831.3 storm; record as an assumption until traffic confirms (CALFIRE-002, claude session).
- Town code text (Title 14 floodplain, Title 16 grading) not readable online, only the table of contents; confirm with Town staff instead of assuming County criteria apply (PHXZOO-004, claude session).
- No published animal-facility (AZA) drainage design standard exists; state exhibit drainage topology as engineering judgment (PHXZOO-004, claude session).
- Keep research separate from minutes so unverified web findings are marked OPEN (PHXZOO-004, claude session).
Jurisdiction add-ons:
- Town of Sahuarita / Pima County: RDM 2.10 roadway crossing (10-yr contained, 100-yr overtopping 1 ft max) as County criterion; PC/COT Detention/Retention Manual favors distributed shallow basins, private-development provisions may not apply over 1 sq mi; ADEQ AZPDES CAFO permit applicability; 9 CFR 3.127 fencing (PHXZOO-004).
- Caltrans/California: document set and key criteria listed in the add-on seed above (CALFIRE-002).
QC checks:
- qc-reviewer confirms every criterion in minutes or report has a citation or is marked OPEN.
Source cards: PHXZOO-004, CALFIRE-002

### HJR-C23 Road alignment along a berm in a distributary flow area
skill | add-on drainage-report-build/town-of-sahuarita (Lee Moore Wash criteria) with core decision note in drainage-report-build Sec. 1 | score 6 | hours 3 | cards 1 | projects 1 (SAHPARK) | confidence medium
Trigger: Road extension that can run straight or follow an existing private flood berm in a sheet-flow area.
Steps (merged):
1. Compare straight vs berm-following alignment: fill savings vs ponding against the road, higher velocities, erosion protection, larger structures.
2. Prefer the alignment that keeps existing drainage patterns so no adverse impact is easy to show at downstream property and jurisdiction boundary.
3. If the road acts as a berm, build mitigation to return flows to existing conditions with the road; record berm owner and maintenance.
4. Get written Floodplain Administrator concurrence that a raised berm is a drainage training embankment in an easement, not a levee, before 60%.
5. Size the drainage easement from headwater and setback before landowner negotiation.
Gotchas:
- Berm-following option saved about 10,000 CY of fill but shifted flood-protection responsibility and armoring of a road carrying about 6,000 cfs to the Town (SAHPARK-019, claude session).
- Lee Moore Wash Development Criteria discourage levee-like features; berm status became schedule-critical (SAHPARK-019, redline variance log).
Jurisdiction add-ons:
- Town of Sahuarita / Pima County RFCD: LMW Development Criteria; Floodplain Administrator concurrence.
QC checks:
- Berm status decision recorded in writing before 60%.
Source cards: SAHPARK-019
