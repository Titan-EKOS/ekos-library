---
name: project-intake
description: Start work on a project folder or a received model set - confirm real local files, copy and inventory, set the standard job layout, find the prior report/models/plans/correspondence, harvest standards and public GIS, build terrain, retrieve record plans, register HEC-RAS/FLO-2D model sets, verify CRS and datum into a data log, and write numbered findings and a one-page scope.
version: 1.0.0
status: active
function: project-setup
jurisdiction: all
tools_versions: "Python 3.10+ (stdlib; pypdf); GDAL 3.x in the EKOS GIS venv; robocopy; HEC-RAS 6.6 (read-only register); Tesseract OCR"
owner: JCO
replaces: "none (new; collects DSO-C13 intake with DSO-C03, DSO-C04, DSO-C05, DSO-C06, DSO-C09 and the intake part of HYD-C13)"
---
# Project Intake

## When to use
- Starting AI or script work on a project folder (often OneDrive), a new job, or an update of an earlier study to
  current standards that needs a short scope.
- A HEC-RAS or FLO-2D model set is received, or reused from an archive.
- Base GIS, terrain, record plans or reference documents must be assembled before hydrology or hydraulics.
- Incoming survey, CAD, LandXML or GIS must be checked against the model grid.
- The prior/adjacent study screen and jurisdiction confirmation that follow are run by `due-diligence-researcher`.

## Inputs
- Source project folder (read-only) and a work area on a local non-synced drive (D:).
- Job number, jurisdiction (to be confirmed), client ask.
- `%DOCS_PY%` / `%GIS_PY%` = documents and GIS venv interpreters by full path (D11); `%SK%` = this skill's `scripts\`.
- On EKOS-LOCAL jobs, data retrieval runs on the local worker from replayable scripts and saved configs (D14).

## Steps

### A. Real files, copy, inventory (DSO-C13)
1. Check the folder holds real files, not only desktop.ini or cloud placeholders. Set "Always keep on this device" or
   download first. `intake_inventory.py` flags cloud-only files, desktop.ini-only folders and empty folders.
2. After any bulk upload, check for a nested copy of the folder inside itself and for size growth before work starts
   (the inventory lists nested-copy suspects).
3. Copy to the work area and log it:
   `robocopy "<source>" "D:\<work>\<Job>\Source_<YYYYMMDD>" /S /E /MT:8 /R:1 /W:1 /LOG:"D:\<work>\<Job>\Intake_<YYYYMMDD>\robocopy_<YYYYMMDD>.log"`
   then verify count, bytes and a SHA-256 sample:
   `"%DOCS_PY%" "%SK%\intake_inventory.py" verify --src "<source>" --dst "D:\<work>\<Job>\Source_<YYYYMMDD>"`
   Record in the project notes that the copy is complete. Source files stay read-only; work on copies.
4. Inventory the whole project folder (path, size, mtime, readable, cloud-only) to CSV; ZIP contents separately;
   keep the inventory and all generated work outside the source job folder:
   `"%DOCS_PY%" "%SK%\intake_inventory.py" inventory --root "<source>" --out "D:\<work>\<Job>\Intake_<YYYYMMDD>\inventory_<YYYYMMDD_HHMM>.csv"`
5. If an upload is still running, save dated snapshots and a delta (`--previous <earlier csv>`); rerun when complete;
   mark findings provisional until the inventory shows no growth (`"final": true`). File dates on OneDrive are sync
   times, not work history: keep a dated log.

### B. Job layout (D56)
6. Set the Standard job layout at the job work root: 00_Admin, 01_Reference, 02_Data, 10_Record, 20_Working,
   30_Report, 40_QC, 50_Correspondence (issued sets in 30_Report/Issued); dates YYYYMMDD in every name. Drainage report deliverables
   get their report folder from `drainage-report-standard` (make_report_folder.py). Working sandboxes
   `20_Working\<Initials>_<YYYYMMDD>_<Topic>\`.

### C. What the project already has (DSO-C13)
7. Identify the prior report, native model folders, current site plan/CAD, survey, geotech report and correspondence;
   record which layout the prior report actually adopted.
8. Check correspondence early for prior agency approval of the old report (decides addendum vs full replacement
   report). Do not reuse prior-report tables without tracing them to calcs.
9. Download all current jurisdiction standards into `01_Reference\Agency\Standards_<YYYYMMDD>\` with a register
   (title, edition date, URL, current or historical) - `reference/public_gis_and_records.md` C.

### D. Received or archived model sets (HYD-C13)
10. Keep the delivered zip/archive untouched as the record copy; work on an extracted copy. Budget disk at 2-3x the
    zip size; never open multi-GB tif/HDF in a viewer - read .vrt and .rasmap as text.
11. Register the HEC-RAS set without opening RAS:
    `"%DOCS_PY%" "%SK%\ras_plan_register.py" --prj <model.prj> --out <model folder>\_plan_register.csv --json <..>\Intake_<YYYYMMDD>\ras_findings.json`
    It reads the .prj (registered Geom, Unsteady, Plan files; as-received Current Plan - record it before any edit),
    each .p## (Plan Title, Short Identifier, Geom File, Flow File, Program Version, Computation Interval), compares
    with the files on disk and flags unregistered plans, entries without files, stray copies (renamed .hdf, .tmp.hdf,
    snapshot HDFs, Backup.p##, sync conflict copies), plans sharing a flow file under different storm titles and
    generic plan titles. Never treat stray copies as results. Fill the condition, terrain and status (live /
    superseded) columns and keep the register in the model folder.
12. Confirm each plan's flow file matches its title/storm; separate titles or clearly named plans for existing vs
    proposed; rename generic plan titles to condition-specific names (on a copy) before results are reported.
13. FLO-2D archives: register every native folder (build, grid, run time, terrain changes vs base, levee/barrier
    records); diff each alternative grid against the base; match folders to report figures; never select by folder
    name or newest timestamp; separate artificial levee barriers from real proposed grading.
14. Terrain packages: list Terrain folder sizes and each scenario .vrt source and cell size; scenario modifications
    live in the terrain HDF or geometry, not the tif; identify duplicate source tiles; check stored maps' Terrain
    name and StoredFilename and regenerate missing maps.
15. Open in the same or newer RAS version on a copy only (opening rewrites plan and geometry files); record versions;
    a 7.x set is not upgraded or mixed into 6.6 work without a logged decision (D02).
16. Run and store models on a local non-synced drive; copy only final plan results to the synced share; delete
    .tmp.hdf and unused plan results before archiving (on the working copy).
17. Every caption and table that uses results cites plan file, short ID and geometry (report-writer applies this).

### E. Public data, terrain, records, reference documents
18. Public GIS and hydrology data: `"%DOCS_PY%" "%SK%\rest_harvest.py" --config <harvest.json> --out <job>\02_Data\GIS_Public\<YYYYMMDD>`
    (envelope query with paging, GeoJSON per layer, GeoPackage per theme in the GIS venv, `_download_log.csv`; one
    dead service is logged and the pass continues). Layer list and rainfall/soils/land-cover rules:
    `reference/public_gis_and_records.md` A. Resolve every ERR row before hydrology starts.
19. Terrain: `reference/terrain_dem_build.md` - extent over all contributing watersheds, TNM item list, tiles chosen
    by acquisition collection and logged (D53), clip before mosaic, project CRS, m->ft, DEMs at 3 ft (3.28 ft for
    native 1 m) for hydraulics/grading, 10 ft for hydrology, 30 ft for large basins (D54), per-source cell counts for
    composites, vintage differencing.
20. Record plans and field books: `reference/public_gis_and_records.md` B (catalog queries, page budget, SHA-256 and
    magic bytes, OCR with orientation, strict utf-8, deterministic quotes, numbers checked on the page image, crossing
    details accepted only when spatially anchored).
21. Reference documents: `reference/public_gis_and_records.md` C (copy unaltered, hash, page-aware extraction, OCR only
    low-text PDFs, encrypted PDFs left pending, human decisions in a separate sheet).

### F. CRS, units, vertical datum and the data log (DSO-C05; D55)
22. Start `02_Data\<Job>_DataLog_<YYYYMMDD>.md` from `reference/data_log_template.md`. Project CRS by jurisdiction from
    the survey basis; Pima County default NAD83(HARN) Arizona Central, intl ft, EPSG:2868 (D55, default, to confirm).
    Record the realization of every layer; mixing realizations is flagged.
23. Do not trust declared EPSG/.prj metadata: compare at least 3 known points to the model grid for every incoming
    CAD/GIS/LandXML file and log the result.
24. Local site coordinates: apply the documented local-to-State Plane transform (translate, rotate, scale about the
    base point); preserve CAD arcs with a chord tolerance before transforming.
25. Find the vertical datum and benchmark note in the survey; if absent, request it and mark dependent elevations
    (pads, floors vs modeled WSE) provisional.
26. Reconcile units (metric survey vs ft plans) before any grid update.
27. LandXML: P order is northing, easting, elevation; interpolate on the original triangles, exclude invisible faces,
    no extrapolation across voids; update the grid from the original survey triangles, not a new triangulation.
28. Compare the new survey surface with the model grid/DEM (mean, std dev); list differences over 2 ft and explain them.
29. Received model sets: read RASProjectionFilename in the .rasmap, the SRS of each .vrt and each delivered .prj;
    confirm the same horizontal realization and units (e.g. EPSG:2230 vs 6426 in California) and vertical datum;
    record the CRS of each layer before any reprojection.

### G. Findings and scope (DSO-C13)
30. Write numbered findings (F01, F02 ...) with severity, evidence locator (report page, model file) and action, in
    `00_Admin\<Job>_Intake_Findings_<YYYYMMDD>.md`. Issue only after the inventory is final.
31. Write the scope as plain text: one page target, two pages max, no subtasks, with assumptions and exclusions; list
    conditional services (FEMA map revision, regional model rebuild, easement-driven redesign) separately.
32. Hand off to `due-diligence-researcher` (prior and adjacent studies, existing conditions, jurisdiction
    confirmation) with the inventory, data log, model registers and findings.

## Jurisdiction add-ons
- `addons/pima-county-rfcd.md`: lidar collections and composite rule, target CRS (D55).
- `addons/fema.md`: NFHL layer set, LOMR check, screening vs duplicate-effective wording.
- `addons/caltrans-california.md`: tenth-postmile points, AADT, dam inundation; California CRS realization check.
- `addons/city-of-tucson.md`: Maps and Records catalog and field books.
- Arizona jurisdictions with a county manual use the manual's rainfall and soils sources (`drainage-report-build`
  add-on of that agency).

## Gotchas
- The folder showed only desktop.ini until a manual download; the run stalled about 1 h (TANGERINE-009).
- A bulk upload created a full nested duplicate of the project folder inside itself (about 2,258 files, 50 GB),
  about 3 h to sync (TANGERINE-009).
- OneDrive resets file timestamps to the sync time, so file dates cannot be used to estimate work history; keep a
  dated log (TANGERINE-009).
- The upload grew from 1,726 to 2,653 files during the review; findings from the first snapshot had to be revised
  (NORTHLOOP-001).
- Correspondence did not show prior agency approval of the old report (NORTHLOOP-001).
- The prior report carried conflicting dates and tables (Q500 basis stated two ways); do not reuse tables without
  tracing to calcs (NORTHLOOP-001).
- Plan p01 (floodwall, existing event) existed on disk with a 1.5 GB result HDF and was cited in the delivered data
  dictionary, but was not registered in the .prj, so it did not appear in the RAS plan list; add the plan back through
  the .prj or open the .p01 directly (DLR-001).
- A stray renamed copy of a plan result HDF (p02 with extra letters appended) was the same size as the real one; easy
  to map the wrong file (DLR-001).
- RAS Mapper listed a 91% snapshot HDF as a results layer next to the completed run; check the layer name for Snapshot
  before mapping (DLR-001).
- One geometry HDF appeared twice in RAS Mapper under two names, and a stub geometry HDF (0 MB) was referenced but not
  in the .prj (DLR-001).
- Plans mixed 30 s and 1 s computation intervals and RAS 6.70 / 7.00 / 7.01 files; a test plan created after receipt
  changed the project Current Plan; record the as-received Current Plan before editing (DLR-001).
- The .rasmap projection was set from a feature shapefile .prj under Features rather than the Terrain Projection.prj;
  it matched, but this is fragile when features are replaced (DLR-002).
- Delivered spot elevation points were in NAD83(2011) CA zone 6 ftUS (EPSG:6426) while all sampled rasters were NAD83
  CA zone 6 ftUS (EPSG:2230); a silent realization mismatch of up to a few ft if a GIS transforms on the fly (DLR-002).
- The base terrain was one 53 GB tif at 0.615 ft cells (about 430,000 px square) plus a 2.2 GB terrain HDF; the three
  scenario terrains were VRTs over that same tif (DLR-003).
- Stored depth maps referenced terrain clone names that were not delivered and output folders that did not exist, so
  they would not display until recomputed (DLR-003).
- The same USGS and county DEM tiles were delivered twice in two Terrain subfolders, including two 6.8 GB county DEM
  copies (DLR-003).
- Report and figure captions cited existing conditions as Plan 12 / EX_<init>_LG, but p12 was titled Plan 12 with no
  short ID (geometry g08), the project notes named p09 EX_<init> as existing, and no plan carried EX_<init>_LG
  (TANGERINE-004).
- 12 plans and 8 geometries in one project with superseded iterations p01-p08 make the wrong HDF easy to read; confirm
  the plan before exporting rasters (TANGERINE-004).
- Plans p05 (100-yr) and p06 (10-yr) both pointed to flow file u02 - the 10-yr run either used 100-yr flows or the file
  was overwritten between runs; it matched a mislabeled-storm comment on the draft (SAHPARK-016).
- OneDrive sync created a conflict copy of the g04 geometry .hdf (225 MB) (SAHPARK-016).
- The same 8 USGS tiles were copied into three terrain folders (SAHPARK-016).
- About 40 geometry saves (g02) and 19 saves (g04) in Backup show heavy iteration on berm and road terrain
  (SAHPARK-016).
- A folder named Alt1 had an eastern channel and 2,120 ft of artificial barriers, while the report's preferred
  alternative left the east natural (NORTHLOOP-006).
- Both named 500-yr folders were empty; the old 500-yr used a 1.75 x Q100 multiplier, not a saved run (NORTHLOOP-006).
- The NHD MapServer timed out at 180 s, then returned empty JSON on retry (4 passes); fall back to the staged HU8
  shapefile zip from the TNM S3 bucket (CALFIRE-003).
- Shapefiles truncate field names over 10 characters; keep the GeoPackage as master (CALFIRE-003).
- Log failures instead of stopping the loop so one dead service does not cost the whole pass (CALFIRE-003).
- PFDS returns JavaScript text (result = values; quantiles = [...]), not JSON; parse the arrays (CALFIRE-005).
- Dual groups (B/D, C/D) and Not rated units (3-6%) need a stated rule before CN assignment (CALFIRE-005).
- Display-clipped polygons must not feed hydraulic encroachment logic (SILVERBELL-013).
- An updated local model plus mapped lines is a screening, not a duplicate-effective model (SILVERBELL-013).
- Tiles carry 2-3 overlapping vintages (2017, 2019, 2025) and duplicate NED entries; filter or the mosaic mixes
  surfaces (CALFIRE-004).
- Newest-published logic picked the older 2018 collection (published 2025) on several tiles; fixed with a
  collection-preference step and a DEM rebuild (RKN-002).
- The initial DEM extent did not cover the full offsite watersheds; extending it changed several CP inputs and forced
  PC-Hydro reruns (RKN-002).
- A 107-tile merged input built a 20 GB terrain tif; clip first (DLR-007).
- Street and wash network shapefiles ended up listed under Terrains in the .rasmap (DLR-007).
- The USGS 2021 10-ft DEM contributed 0 cells to the composite and the run continued without noticing (SAH-020).
- Large changes (30 to 80 ft mean over hundreds of ac) were mine tailings growth, which affects depression volumes and
  flow paths (SAH-020).
- 1.8 GB of raw tiles per site (CALFIRE-004).
- Culvert inverts read from lidar are estimates only; carry as open items until survey (CALFIRE-004).
- USGS 1 m tiles are NAD83 UTM 12N in meters; convert to ft and compare to survey before use (DLR-007, STARVALLEY-014).
- The DLR-007 terrain lessons come from a test project, not the received set (DLR-007).
- LandXML declared EPSG:2223 but was in local coordinates; watershed and parcel shapefiles likewise had State Plane .prj
  files with local coordinates (STARVALLEY-014).
- Old channel files sat about 50 ft off the true centerline (STARVALLEY-014).
- One CAD vertex differed by 100 ft and was excluded (STARVALLEY-014).
- Survey CAD had no datum or benchmark statement; pad elevation and WSE remain provisional (NORTHLOOP-019).
- An early Delaunay terrain was replaced by exact LandXML triangles (26,507 cells updated) (NORTHLOOP-019).
- DCR vertical datum unknown; EG vs FG differences are not earthwork depths (SILVERBELL-007).
- The first field-book search stopped at page 1 and called the target missing (EKOS-LOCAL-013).
- Sideways scans gave zero OCR hits on all 26 pages until orientation was corrected (EKOS-LOCAL-013).
- Default cp1252 decoding failed on utf-8 OCR text (EKOS-LOCAL-013).
- Free-form model quotes: only 40 of 137 matched the source exactly (EKOS-LOCAL-013).
- OCR misread 2698.20 as 2696.20 on one record; two monuments with the same elevation were different points
  (EKOS-LOCAL-013).
- Plan titles naming roads do not geolocate a structure; candidate crossing details stayed unaccepted until spatially
  anchored (EKOS-LOCAL-013).
- 8 datum/crossing retrieval tasks, 5 failed or empty (EKOS-LOCAL-013).
- A 715-file reference intake ran 5.3 h; 220 of 264 PDFs verified, 16 timeouts, 18 page-label failures, 8 zero-text
  (EKOS-LOCAL-023).
- A stdout warning on a successful extraction made the orchestrator mark failure; judge by exit code and output
  artifact (EKOS-LOCAL-023).
- OCR of map pages misread labels (EKOS-LOCAL-023).
- Qdrant 1.15.3 accepted but did not return collection metadata; verify the fingerprint in point payloads instead
  (EKOS-LOCAL-022).
- LM Studio rejected the json_object response format (HTTP 400) (EKOS-LOCAL-022, EKOS-LOCAL-005).
- Only a synthetic 5-page test passed retrieval qualification; real manuals are not yet qualified (EKOS-LOCAL-022).

## QC checks
- Pull rules: `get_qc_rules('crs')`, `get_qc_rules('existing-conditions')`, `get_qc_rules('model-runs')`, plus the
  jurisdiction tag.
- Inventory final (no growth since last snapshot) before findings are issued; copy verification log (count, bytes,
  hash sample) present (NORTHLOOP-001, TANGERINE-009).
- Every cited plan exists, is registered, carries a condition-specific title and matches the caption; plan flow file
  matches plan title/storm (HYD-C13).
- `_download_log.csv` has no unresolved ERR rows before hydrology starts; HSG rule for dual/not-rated units stated in
  the assumption log (DSO-C03).
- Per-source cell count in a composite (any source with 0 cells stops the run); nodata fraction 0 inside the
  contributing area; DEM extent covers every contributing watershed (DSO-C04).
- Known-point check (at least 3 points) logged for every incoming CAD/GIS/LandXML file; vertical datum and benchmark
  stated for every survey used to set an elevation, otherwise labelled provisional; survey vs grid difference table
  with differences over 2 ft explained (DSO-C05).
- Every number taken from a record checked against the page image; every quoted excerpt matches the source
  byte-for-byte (DSO-C06).
- Data log names the realization of every layer (D55) and the cell size of every DEM (D54).

## Change log
- 1.0.0 2026-10-22: built from clusters DSO-C13, DSO-C04, DSO-C03, DSO-C06, DSO-C05, DSO-C09 and the intake part of
  HYD-C13 (steps 1-10; step 11 citation rule handed to report-writer); decisions D53, D54, D55 (default, to confirm:
  Pima County EPSG:2868), D56, plus D02, D11, D14. Added scripts intake_inventory.py, ras_plan_register.py,
  rest_harvest.py (tested on sample folders, a synthetic RAS project and a local mock REST service; live public
  services were not reachable from the build container) and reference files for data log, terrain build, public GIS,
  records and reference documents.
