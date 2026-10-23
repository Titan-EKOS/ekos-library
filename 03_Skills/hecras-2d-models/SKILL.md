---
name: hecras-2d-models
description: Build, run and accept HEC-RAS 6.6 2D models (rain-on-grid and inflow, existing and alternatives, extensions of accepted models, screening models) by script and native tools - project hygiene, terrain, mesh, land-cover n, SA/2D connections, boundary inflow register, headless launch order, acceptance gates, SWE stability triage and GPU-beta limits; use for any HEC-RAS 2D work and when model-run-supervisor needs the HEC-RAS engine steps.
version: 1.0.0
status: active
function: hydraulics-model-run
jurisdiction: all (add-ons - Pima County RFCD, Town of Marana, FEMA)
tools_versions: "HEC-RAS 6.6 (pinned, D02); RasProcess.exe and RAS66 COM; ras-commander 0.103.0 (pinned); Python 3.12 gis env (h5py, numpy, rasterio, geopandas, psutil, pywinauto, pywin32)"
owner: JCO
replaces: "none (new); absorbs proposed skills hecras-2d-model-build, hecras-native-automation, hecras-2d-stability-triage, hecras-project-hygiene"
---
# HEC-RAS 2D Models

## When to use
- Building existing and proposed 2D models from GIS / lidar (rain-on-grid, offsite inflows, culverts as
  SA/2D connections), extending an accepted model, or a screening / review 2D model.
- Any HEC-RAS compute run headless, in parallel or overnight.
- A diffusion-wave model must be rerun with SWE (embankments, abrupt flow interruption) and crashes or
  shows large residuals, or velocity spikes appear after mesh refinement.
- A request to run a 6.x model on the GPU with the HEC-RAS 2025 beta.
- model-run-supervisor calls the HEC-RAS engine steps here: preflight (Step 9), launch (Step 10),
  completion and acceptance (Step 11), post-run extraction (Step 13).

Not here: result rasters (hecras-result-rasters); existing vs proposed differences (impact-comparison);
HMS hydrographs (hechms-headless); PC-Hydro inflows (pchydro-hydrographs); queue and notification policy
(model-run-supervisor).

## Inputs
- Accepted model (if extending) as a record copy; project CRS and vertical datum.
- DEM (e.g. USGS 1 m or 3 ft lidar, decision D53/D54) plus survey at crossings; proposed grading surfaces.
- Perimeter / basin boundaries, breaklines (road crown, wash banks, curbs, paths), land cover and soils.
- Hydrology: rain-on-grid hyetographs (e.g. NOAA Atlas 14 upper bound, 5-min) and / or inflow hydrographs
  with the source report page for each CP.
- Culvert / crossing data from survey or lidar (inverts, barrel length), not GIS line length.
- Job table row from model-run-supervisor (plan, cores, timeout).

Scripts (interpreter by full path, D11; no .ps1, D12). `<PY>` below = `"%HYDRAULICS_PY%"` for
ras_headless.py and ras_plan_register.py, `"%GIS_PY%"` for ras_result_check.py (h5py) - see 08_Platform_Builds/ENVIRONMENTS.md:
- `scripts/ras_plan_register.py` - plan / geometry / flow register and hygiene flags (read-only).
- `scripts/ras_headless.py` - D05 launch order with dialog log and result check.
- `scripts/ras_result_check.py` - acceptance numbers from a closed plan HDF.
- `reference/native_automation.md` - RasProcess / RasMapperLib / HDF / COM details (load before scripting).

## Steps

### 1. Working copy and project hygiene
1. Copy any accepted or received model to a new working copy; never edit it in place. Keep the delivered zip
   as the record copy. Budget disk at 2-3x the zip size; read .vrt and .rasmap text instead of opening
   multi-GB tif / HDF in a viewer.
2. Run `<PY> ras_plan_register.py <project.prj>` before any edit. It records the as-received Current Plan
   and flags unregistered plans, missing files, shared flow files, placeholder names, mixed versions,
   auto-duplicates and stray result copies (renamed HDF, tmp.hdf, snapshot, backup, sync conflict copies).
   Never treat a stray copy as a result.
3. HEC-RAS 6.6 is pinned (decision D02). Open a project in 6.6 only on a copy (opening rewrites plan and
   geometry files). 7.x only by a logged decision on a pre-upgrade copy. Record the version per plan.
4. Keep one working project; archive frozen copies as a dated zip, not parallel live folders.
5. Name plans `<condition>-<freq>-<variant>` with geometries to match; give every plan a condition-specific
   title and short ID before results are reported. Delete auto-named duplicates and placeholder plans; purge
   failed Retry geometries and their results once the cause is logged.
6. Run and store models on local D:\ (non-synced); copy only final plan results to the synced share. Delete
   .tmp.hdf and unused plan results before archiving. Keep fine-grid post-processing HDF (near 1 GB) out of
   synced folders.
7. Confirm contracted scope: if the contract assumed 1D and the job needs 2D, flag the mismatch to the PM
   early and carry a scope note into the report.

### 2. Terrain
1. Merge DEM + survey at crossings into one GeoTIFF in the model CRS and vertical datum; check the seam.
2. Proposed grading as a stacked raster / terrain modification, not re-copied tiles.
3. Create terrain natively (RasProcess CreateTerrain on the source grid, no resample, explicit projection and
   units); judge by the terrain HDF (exists, extent, dataset count), not by stderr warnings. Details:
   `reference/native_automation.md`.
4. CRS: read RASProjectionFilename in .rasmap and the SRS in each .vrt; same horizontal realization and units
   in every layer (decision D55 for Pima County); record before any reprojection.
5. Record which terrain each plan uses; terrain modifications stored only in a terrain HDF are invisible to
   scripted rasters (hecras-result-rasters, decision D57).

### 3. Domain and mesh
1. Cover the full contributing basin edge (check for slivers) or the project buffer. Extend the outflow BC at
   least 5 cells past the area of interest. Trim BC line ends so no two BC lines share a face.
2. Cell size by zone (e.g. 10 ft tributary / near roads, 20-30 ft corridor, 60-100 ft upper piedmont);
   overbank cells <= 100 ft where depths are 0.5-2 ft, or run a grid-independence check.
3. Breaklines on road crown, wash banks, curbs, paths. Along embankments use wash-aligned cells and broader
   transitions; avoid very short faces.
4. Fix grid-transition cells that fail the max-side-count check before running.

### 4. Land cover and loss parameters (decision D28)
1. New, concept and master studies: spatially varied n from land cover (active wash about 0.030-0.040,
   desert scrub 0.035-0.050, roads, pads, basins), source cited. Constructed unlined earthen channels
   n = 0.025 (decision D27).
2. Uniform n only when extending an accepted model, to keep comparability; state it in the report.
3. CN raster: burn pavement / path CN 99 and include roads (from plans or county land use).
4. Associate roughness through the native geometry association; HDF-only patches do not persist.

### 5. Structures
1. SA/2D connections along road crests with weir profile stations from terrain over the full line; profile
   length within 1 ft of the centerline length.
2. Culvert inverts and barrel length set explicitly from survey / lidar, never from GIS line length.
   Culvert names <= 12 ASCII bytes.
3. Bridges: type 32 (rating curves) under DWE; type 33 needs SWE.
4. Save face flow output in every plan (transect and structure flows cannot be recovered later without it).

### 6. Boundary conditions and the inflow register (hybrid rain-on-grid plus inflows)
1. Register every candidate inflow from the source reports: CP id, area (ac), Q2 / Q10 / Q100 (cfs), report
   page, condition (existing / developed).
2. Overlay each CP watershed on the 2D perimeter; keep an inflow BC only where the contributing area lies
   outside the mesh.
3. Build a map-based CP concordance across studies; one value for the same watershed under two names; remove
   the upstream CP whenever its downstream CP is entered.
4. Export the BC list from each .u## (name, peak) and reconcile line by line against the register; record the
   condition basis of each.
5. Place each inflow BC where the culvert or wash discharges into the mesh; tag with coordinates.
6. Rain-on-grid hyetographs to DSS; synthetic hydrographs labelled not calibrated.
7. Volume check after the run: precipitation volume + inflow volume = outflow + storage + infiltration.
8. Interval units of RAS hydrographs match the source workbook (1MIN vs 1HOUR); times strictly increasing.

### 7. Plans and run windows
1. One plan and one unsteady flow file per event and condition; the flow file matches the plan title / storm
   (the register flags shared flow files).
2. Run window covers the recession: find when the last inflow ends and cell peaks occur; pick the shortest end
   time with < 0.01 ft later rise in a 24 hr reference run.
3. Confirm ambiguous inputs (e.g. a duration given as "3 6 hours") with the requester early and log the answer.

### 8. Scripted build order
1. geometry -> mesh -> BC lines (rewrite after any mesh change) -> land cover -> mesh layers -> unsteady flow
   and plans. One rebuild script runs all steps in order.
2. Alternatives: copy base, stack the grading raster, add culverts, regenerate the mesh, rewrite BC lines.
3. Native details (HDF attributes, CreateGeometry / CompleteGeometry keys, 1D fixed-width blocks, COM output
   discovery): `reference/native_automation.md`. Diff new geometry tables against the source to prove only
   intended changes.
4. Set PYTHONIOENCODING=utf-8 for library logs. Script the input prep; run long computes as supervised jobs.

### 9. Preflight (engine-specific part of the supervisor gate)
1. All project text files CRLF; register clean (no placeholder titles, no shared flow files across storms).
2. Terrain HDF exists and covers the 2D area; BC lines do not share faces; weir and culvert lengths checked.
3. Inflow chronology, interval units and volume match the source; no double-counted CPs (Step 6).
4. Face flow output on; core count set in the plan (benchmark cores once per model).
5. A 1 hr diagnostic run first; full events only after it finishes cleanly.
6. Run `get_qc_rules('model-runs')` and `get_qc_rules('hydraulics-2d')`.

### 10. Launch (decision D05)
1. `<PY> ras_headless.py <project.prj> p03 --timeout-hours 12`. Order:
   1) `Ras.exe -c <prj> <plan file> -hideCompute` with a dialog logger;
   2) if no plan HDF but p##.tmp.hdf remains: wait until no RasUnsteady.exe is open in the folder, run
      RasUnsteady.exe directly on the temp HDF, rename it to p##.hdf (confirm the argument pattern on the
      EKOS 6.6 install first);
   3) COM controller RAS66.HECRASController (open, set plan, compute, always QuitRas; COM may reset the core
      count to automatic).
2. One project copy per plan for parallel runs; copy the plan HDF and compute messages back.
3. Before launch check no other Ras / RasUnsteady compute uses the cores (ignore Ras -Embedding).
4. Never open a live p##.tmp.hdf or an HDF being written. Retry a plan up to 3 times, then log not complete.

### 11. Completion and acceptance (decision D09)
1. Success = closed plan HDF + compute messages, never the launcher return code. A run that returns in
   0.1 min with no HDF is a geometry error; read the messages (e.g. BC lines share the same face).
2. `<PY> ras_result_check.py <project.p##.hdf> [--screening]` reports finish message, volume error,
   iteration warnings, max WSEL error and max face velocity.
3. Final runs: volume error <= 0.1 pct AND max WSEL residual and iteration warnings reviewed AND full end time
   reached AND max face velocity physical. Screening runs: <= 0.5 pct, labelled screening.
4. A low volume error does not accept a run with thousands of iteration warnings or a large WSEL error.
5. Velocities far above physical (hundreds of fps) are numerical spikes: label the run diagnostic and check the
   saved velocity series before quoting any peak.

### 12. Stability triage (SWE wetting fronts, velocity spikes)
1. Keep the accepted DWE pair untouched; build trials in a new dated folder with new plan numbers.
2. Read the native compute log for the first residual cells and map them (steep terrain in small partly wet
   cells; roadway wetting fronts).
3. Try SWE-ELM before SWE-EM; for SWE-EM keep the Courant target below 1 per the HEC troubleshooting
   documents (not web posts).
4. Enlarge or realign cells at the failing front rather than refining; wash-aligned cells, breaklines along
   banks, broader transitions; avoid very short faces along embankments.
5. Retest the first 1-6 hr window before a full event.
6. After every run extract max face velocity and its location (not only volume error).
7. Timestep check: fixed step (adaptive off), e.g. 1 s base with 20 slices = 0.05 s local, on an
   identical-geometry existing / proposed pair. Do not claim timestep convergence from one pair.
8. Accept only with Step 11 checks; report peak WSEL change vs DWE by location. Numerical tests are not
   mitigation.

### 13. Post-run extraction
1. Check the plan HDF exists before StoreAllMaps / extraction (StoreAllMaps returns 0 files without it).
2. Store WSE, depth and velocity maps per plan; result rasters by hecras-result-rasters (naming D43, RAS
   Mapper spot check D57).
3. Extract culvert flow, HW / TW, flow out of each boundary and road overtopping to a results CSV. Flag BC
   lines with no results instead of reporting NaN peaks.
4. If an optional dataset (e.g. Max Courant, absent under fixed stepping) breaks a worker script, recover
   results from the closed HDF; do not rerun.
5. Cite plan file, short ID, geometry and HEC-RAS version in every caption and table that uses results.

### 14. Screening mode (FEMA-studied stream, no effective model yet)
1. Inventory supplied studies, DCR pages and models; record FEMA effective vs later local updates.
2. Reproduce the supplied source model exactly (all profiles, all XS) before edits; save as model 00.
3. Expand terrain from public USGS 1 m lidar, reproject to project state plane ft, clip to a buffer.
4. Place XS at FEMA lettered / unlettered stations; tabulate model WSEL vs effective 1 pct WSEL.
5. Floodway screening: encroachment stations from effective mapped floodway lines (Method 1) on existing; hold
   the same stations in proposed; restrict to the project reach plus approaches; derive boundaries from full
   polygons and clip only display linework.
6. Flag bridge low chord (road crest less assumed slab) and pier width as assumptions; use the NBI record for
   span, length, deck width, channel rating; request DOT as-builts / bridge hydraulic file and the effective
   model before Zone A / AE work.
7. Run paired existing / proposed Q100, map depth and WSEL change, publish a short screening review.
8. Keep a running scope / checkpoint file (provisional items, failures, what must not be claimed) that
   supersedes older status. State in the result basis that it is screening, not certification; do not block
   modeling on the effective model. No no-rise or CLOMR finding from a non-effective model.

### 15. HEC-RAS 2025 beta GPU conversion
1. Before converting, list structures (culverts, bridges, SA/2D connections) and inflow types (internal vs
   perimeter).
2. After import audit cells, terrain tables, structures, BCs and CRS; an incomplete import is not an
   equivalent model.
3. Run native plan preparation first (it states unsupported features); verify support there before telling
   anyone a feature works.
4. Run a short test and confirm nonzero depths before any calibration.
5. Ask JCO before replacing structures with culverts or terrain openings; record dimensions and losses as
   approximations; apply terrain changes as raster cuts and check that cell minima changed.

## Jurisdiction add-ons
Load with `get_skill("hecras-2d-models", resource="addons/<file>.md")`:
- `addons/pima-county-rfcd.md` - TECH-033 rain-on-grid for existing and each alternative, TECH-018 critical
  storm, CN from the PC-Hydro table, 2D acceptance as an approval item.
- `addons/town-of-marana.md` - alluvial fan practice (DWE then SWE tests, appendix content, stress run,
  volume ledger, erodible-soil velocities).
- `addons/fema.md` - FEMA 2D guidance for rain-on-mesh, duplicate-effective rule for findings, Caltrans /
  California bridge data for screening.

## Gotchas
Runs and launch
- compute_plan reported FAILED / could not confirm solver quiescence on 3 of 4 plans while the temp HDF remained; fix was a watchdog that polls RasUnsteady.exe, then runs RasUnsteady.exe on p##.tmp.hdf and renames it (CALFIRE-009)
- StoreAllMaps returned 0 files when the plan HDF was missing; check the HDF exists before mapping (CALFIRE-009)
- One late rerun of plan 01 forced a second figure and PDF compile (about 35 min) (CALFIRE-009)
- Plan returned rc=0 after 0.1 min with no HDF: geometry error "BC lines share the same face"; trim 100 ft off the BC line end nearest the other line and recheck, for EX and PR (RKN-007)
- Each 2D plan ran 19-32 min; one Alt2 plan had to be rerun alone (RKN-007)
- First compute through ras-commander compute_plan produced no result; the base 100-yr plan did not finish until the next day (SAH-009)
- A retry script crashed because the plan HDF did not exist yet; check for the file before reading messages (SAH-009)
- A queue crashed on import (h5py missing) after a restart used a different Python; call the env interpreter by full path (SAH-009, SAH-015)
- Other projects ran HEC-RAS on the same machine; the wrapper polled process command lines and started only after those jobs ended (SAH-001)
- Low CPU (about 8 pct) during a headless RAS run is normal; explain core counts up front, benchmark later, do not restart live runs (CAMPBELL-005)
- Worker scripts failed on the optional Max Courant dataset, absent under fixed stepping; recover results from the closed HDF instead of rerunning (CAMPBELL-005)
- Old queue sessions and obsolete diagnostic runs had to be stopped to avoid duplicate computes (SILVERBELL-018)
- Generator scripts that rebuild all inputs must not run while cases compute; use targeted edits (SILVERBELL-018)
- Command-line runs gave no output within 90 s; the COM fallback worked for 1D (EKOS-LOCAL-010)
- COM may reset core count to automatic; verify the native setting (CAMPBELL-004)
Build
- RasProcess CreateTerrain reports stderr warnings but completes; check the terrain HDF dataset count instead (RKN-007, SAH-010)
- Data error: weir profile length 1 vs GIS centerline 900 ft (must match within 1 ft); set connection profile stations from terrain along the full line (CALFIRE-009)
- Culvert barrel length from the GIS line differed from the lidar-measured 110 ft; set length explicitly (CALFIRE-009)
- The rebuild script must run all four steps in order; BC lines were rewritten after mesh changes (SAH-010)
- Library banners use non-ASCII characters and broke logs; set PYTHONIOENCODING=utf-8 (SAH-010)
- Opening an HDF while RAS was writing caused a write failure; the mesh was discarded and rebuilt. Never read an active .tmp.hdf (SILVERBELL-005)
- Direct HDF-only roughness patches did not persist; use the native association (SILVERBELL-005)
- An ambiguous duration from the user (3 6 hours) was interpreted and logged; confirm such inputs early (SILVERBELL-005)
- A basin sliver extended about 1,000 ft west of the perimeter corner; the perimeter was widened to capture it (ELTORO-004)
- Roads omitted from the CN layer are slightly non-conservative locally; burn them from plans or county land use (ELTORO-004)
- The adjacent accepted study used FLO-2D with SCS Type II 3-hr on a 10 ft grid; moving from 1-hr to 3-hr aligned better with precedent (ELTORO-004)
- Manning n kept uniform 0.035 to match the accepted model; changing it breaks comparability with accepted results (ELTORO-004; decision D28)
- Every build item here was raised by reviewers on a concept model and carried as deferred work (A-1, A-3, T1-4, T1-5, T1-7, T1-8); doing them in the first build avoids a second model cycle (TANGERINE-005)
- Contracted scope assumed 1D HEC-RAS; the 2D approach needed a scope note in the report; flag scope mismatch to the PM early (TANGERINE-005)
- More native API traps (LF files read as empty, truncated attributes, contiguous datasets, CreateGeometry vs CompleteGeometry keys, 12-byte culvert names, GetTypeAttr index, unimplemented RasMapperLib commands, synthetic tests not a project result): reference/native_automation.md (CAMPBELL-004, EKOS-LOCAL-010, SILVERBELL-006)
Inflow register
- The accepted model carried CP-13 twice (BC lines CP-13 and CP13, both 43 cfs); a straight double count that survived into the extended model (ELTORO-001)
- Project notes listed 967/667/95/717 cfs where the report developed values are 2/40/3/43 cfs; treat note values as suspect until checked against the .u## (ELTORO-001)
- Rebuilding inflows replaced CP-W1 (2,254 cfs) with CP-10 (1,412 cfs) plus the South Outfall CPs; remove the upstream CP whenever its downstream CP is entered (ELTORO-001)
- CP numbering is not consistent across the 1999, 2005/2006, 2008 and 2021 studies; build a map-based concordance before transferring any value (ELTORO-001)
- A run window of 12 hr was too short (inflow lasted to 15.5 hr; 20 hr chosen); B-1/B-2 inflows were double counted (CAMPBELL-010)
Acceptance and stability
- Proposed run had 3,520 iteration warnings and 17.1 ft max WSEL error at 0.25 pct volume error; not accepted. The existing run (517,161 cells, 1 hr 39 min) had 0.000136 pct (SILVERBELL-005)
- Advice copied from web posts (Courant 3) conflicted with HEC guidance for SWE-EM; follow the HEC troubleshooting documents (CAMPBELL-001)
- Changing the momentum solver alone did not fix wetting-front errors; the mesh at the road front had to change (CAMPBELL-001)
- A fixed 0.05 s SWE-ELM pair finished near 0.07 pct volume error but localized peak WSEL shifted up to 1.5 ft vs adaptive runs; do not claim timestep convergence (CAMPBELL-001)
- A smaller timestep did not remove the railroad increase (1.33 ft vs 1.06 ft); numerical tests are not mitigation (CAMPBELL-001)
- Two refinement levels (54,036 and 68,273 points) gave 438-588 fps spikes on short railroad faces and did not converge (CAMPBELL-003)
- Wash-aligned refinement removed the spikes (max about 24 fps, volume error 0.006 pct) (CAMPBELL-003)
- A brief sub-minute native velocity peak (93 fps vs 3 fps saved 60 s max) stayed unresolved; do not accept a peak velocity without checking saved series (CAMPBELL-003)
- Mesh generation can fail the max-side-count check at a grid transition; fix the transition cell before running (CAMPBELL-003)
Hygiene and received models
- Each project copy carried 36-40 plans; p01-p14 were duplicated by auto-named p16-p29 on the same geometry / flow pairs (ELTORO-005)
- Placeholder names (plan "1", "Plan 37", geometry "New Geometry") and Retry / Retry2 geometries made it unclear which run fed the memo (ELTORO-005)
- The same model existed in three live folders plus a full duplicate tree under another synced folder (ELTORO-005)
- Plans p01-p36 were 6.6 while p37-p40 were 7.0 in the same project (ELTORO-005)
- Geometry autosave produced 22 backups of one geometry in one day and about 75 backup geometries in total (ELTORO-005)
- Plans p05 (100-yr) and p06 (10-yr) both pointed to flow file u02; the 10-yr run either used 100-yr flows or the file was overwritten (SAHPARK-016)
- Report captions cited a plan short ID that no plan file carried; confirm the plan before exporting rasters (TANGERINE-004)
- A plan with a 1.5 GB result was cited but not registered in the .prj; a stray renamed copy of a result HDF was the same size as the real one; a 91 pct snapshot HDF showed as a results layer (DLR-001)
- The 10 ft grid run produced a 934 MB post-processing HDF; keep fine-grid runs out of synced folders (ELTORO-017)
Screening
- Lidar under water and bridge decks gives no channel bottom or low chord; expect high bias in WSEL (CALFIRE-011)
- The agent first wanted a duplicate-effective baseline; JCO clarified the fixed-map intent (SILVERBELL-002)
- A first trial over all 100 intersecting XS reported a spurious 23.7 ft surcharge from disconnected polygon pieces; the project reach gave about 4 ft existing surcharge and 0.16 ft max project rise (SILVERBELL-002)
- Clipping FEMA floodway polygons for display before deriving boundaries broke the hydraulic areas (SILVERBELL-002)
- Local-peak tributary runs with iterated tailwaters are not a connected mass-conserving network; label results screening (SILVERBELL-001)
- The source local model differed from FEMA effective; no no-rise or CLOMR finding can be drawn from it (SILVERBELL-001)
- Long autonomous runs need a checkpoint file that supersedes older status text, or later sessions act on stale state (SILVERBELL-001)
GPU beta
- The importer dropped bridge, culverts and boundary conditions (CAMPBELL-006)
- The GPU solver rejected culvert hydraulics (5 barrels), so bridge-as-culvert also failed (CAMPBELL-006)
- Legacy terrain modifications were stored but not applied to hydraulic tables; use raster cuts and check cell minima changed (CAMPBELL-006)
- Raster sampling precedence was the reverse of the CLI help (later inputs override) (CAMPBELL-006)
- GPU initialization ignored internal inflow boundaries: a 20 hr run ended OK with all depths zero (CAMPBELL-006)
- An earlier general answer that the beta supports culverts was wrong for the GPU engine; verify with native preparation before telling the user (CAMPBELL-006)

## QC checks
- Pull: `get_qc_rules('hydraulics-2d')`, `get_qc_rules('model-runs')`; plus `get_qc_rules('fema')` for screening
  near FEMA streams.
- plan_register.csv clean: every cited plan registered, condition-specific title, flow file matches storm,
  one HEC-RAS version, no placeholder names.
- Inflow register reconciled to the .u## line by line; volume balance closes.
- result_check.json accept = true for every plan quoted (final: <= 0.1 pct; screening: <= 0.5 pct and labelled).
- Max face velocity physical or the run labelled diagnostic; saved series checked before quoting peak velocity.
- No GPU-beta result reported as equivalent without the Step 15 audit.
- Captions and tables cite plan, short ID, geometry and HEC-RAS version.

## Change log
- 1.0.0 2026-10-22: built from clusters HYD-C11, HYD-C09, HYD-C10, HYD-C12, HYD-C16, HYD-C18, DSO-C16, RAS parts of
  HYD-C01, HYD-C03, HYD-C13; decisions D02, D05, D09, D11, D12, D27, D28, D43, D57. RasUnsteady direct argument
  pattern and compute-message wording parsed by ras_result_check.py to confirm on the first EKOS 6.6 run
  (default, to confirm).
