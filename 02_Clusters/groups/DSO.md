# DSO clusters: data gathering, project setup, other

Group DSO = group_data-gathering (22 cards) + group_project-setup (14) + group_other (13) = 49 cards, 33 clusters.
Source tags: "claude session" = card harvested from a Claude session; "claude via Codex session" = card evidence is a Codex session transcript; "EOR redline" = card evidence is EOR redline comments on a draft.
Score = sum of hours_lost x recurrence over the cluster's cards. Header line: type | target | score | hours | cards | projects | confidence.

### DSO-C01 Due-diligence research pass: jurisdiction, standards harvest, data requests
agent | agent due-diligence-researcher | 1.5 | 1.5 | 2 | 2 (CALFIRE, NORTHLOOP) | high/medium
Trigger: New proposal, preliminary drainage job or study update where only the site location is known, the site is in an unfamiliar jurisdiction (including out of state), or the jurisdiction has released new standards since the last study.
Steps (merged):
1. Confirm jurisdiction at the parcel/site point from city/town limits and jurisdiction GIS layers; save the REST responses as evidence (CALFIRE-001, NORTHLOOP-002).
2. Probe the site point by REST: FEMA NFHL zones/panels/XS/BFE, Census place (city limits), NHD flowlines, state DOT postmiles and bridges (CALFIRE-001). Data harvest procedure in DSO-C03.
3. Build the jurisdiction table: state DOT governs inside R/W, city floodplain ordinance inside the SFHA, FEMA FIS/LOMRs, state water board permits (CALFIRE-001).
4. Crawl the agency drainage, engineering and development-plan pages; download every linked manual, checklist, standard detail set and code chapter (NORTHLOOP-002).
5. Write Standards_Register.txt: document, edition, URL, local path, current or historical, key sections used (NORTHLOOP-002; same register as DSO-C13 step 4).
6. Extract text of each PDF for search; flag requirements that change the prior study (software build, design event, freeboard, critical-facility criteria) (NORTHLOOP-002).
7. Write the Due Diligence Summary with tables: site summary, governing standards, methods/software, design rainfall, downloaded data, data by request, data with no known source, known vs unknown criteria (CALFIRE-001).
8. List every agency request (as-builts, effective HEC-RAS models, campus/master plan data, city improvement standards, dam operator data) with holder and route (public records request; FEMA data request about 4 wk) (CALFIRE-001).
9. List what could not be archived and how it was reviewed instead (NORTHLOOP-002).
10. Hand the open-criteria table to the PM for the scoping meeting (CALFIRE-001).
Gotchas:
- Run as a separate context: about 1.5 h of tool work before any hydrology, mostly waiting on web services (CALFIRE-001, claude session); long web crawl independent of model work, about 1-2 h (NORTHLOOP-002, claude via Codex session). Collapsed repeat: CALFIRE-001, NORTHLOOP-002.
- Several standards were not online (1988 city improvement standards; no published owner-agency drainage standard); list them as requests, do not guess (CALFIRE-001, claude session).
- About 155 town PDFs downloaded, but bulk download of the online code was blocked; save current code chapters as web extracts and mark older code PDFs historical (NORTHLOOP-002, claude via Codex session).
- Whether a state-agency project needs city floodplain review or state-coordinated review is a real open question; flag it (CALFIRE-001, claude session).
- Central Valley sites: DWR Best Available Maps and CVFPB regulated-stream status were not checked; add to the checklist (CALFIRE-001, claude session).
Jurisdiction add-ons:
- due-diligence-researcher/Caltrans-California: Caltrans governs in state highway R/W (postmile lookup), city floodplain ordinance in SFHA, SWRCB permits, DWR Best Available Maps, CVFPB regulated streams, state dam inundation boundaries (CALFIRE-001, CALFIRE-003).
- due-diligence-researcher/Town of Marana: online code cannot be bulk-downloaded; save chapters as web extracts (NORTHLOOP-002).
QC checks:
- Jurisdiction confirmed from a GIS layer with saved response before any criteria are adopted.
- Every governing standard in the register has edition, URL and current/historical status.
Source cards: CALFIRE-001, NORTHLOOP-002

### DSO-C02 Prior and adjacent study screen with CP concordance
agent | agent due-diligence-researcher (module: prior-study-screen) | 28 | 10 | 2 | 2 (ELTORO, PHXZOO) | high/medium
Trigger: New corridor project, proposal or Phase 1 start with a stack of prior master drainage plans, basin studies, drainage reports, or several adjacent developments/roads/plants sharing the same wash or floodplain.
Steps (merged):
1. Make one subfolder per adjacent project under an Adjacent Studies and Plans folder (state land master plans, school drainage report and as-builts, road extension, treatment plant, recorded plats) (PHXZOO-001).
2. Dedupe by SHA-256 before reading (PHXZOO-001 gotcha).
3. Inventory every report: firm-neutral title, date, author agency, pages, text layer yes/no, type (drainage report, CMDP, floodplain memo, as-builts, shapefiles, ERR, OHWM memo) (ELTORO-007, PHXZOO-001).
4. Rate each item High/Medium/Low for the site and mark keep, context only, duplicate or superseded; write the supersession chain; check for supersession memos before using any older study (ELTORO-007, PHXZOO-001).
5. Extract CP flows (Q2/Q10/Q100, area, method, rainfall basis) with page numbers, per source, without merging sources (ELTORO-007).
6. Compile existing and proposed structures with capacity vs Q100; note which conceptual structures were built (ELTORO-007).
7. Pull GIS layers (100-yr floodplain, PAD boundaries) into the project CRS and note their date (PHXZOO-001).
8. One-page summary table: which adjacent item fixes a boundary condition at the site (inflow Q, tailwater, berm crest, culvert invert, floodplain limit) (PHXZOO-001).
9. List method precedents (HEC-HMS vs PC-Hydro, storm distribution, CN tables), FEMA panels and usable exhibits with pages (ELTORO-007).
10. Note planned facilities that may change drainage later (future WWTP outfall to the wash, wetlands, road used as berm) (PHXZOO-001).
11. End with an open reconciliation list: CP concordance, double counts, disparities, data still needed (ELTORO-007).
Gotchas:
- Each study uses its own CP numbering; same-numbered CPs are not the same point (ELTORO-007, claude session).
- One 2005 plan was a verbatim subset of the 2006 plan; one 2007 report was superseded by its Stage 2 report (ELTORO-007, claude session).
- Example supersession: a 2018 TDN supersedes 2009 Basin Management Study delineations inside its study limit (PHXZOO-001, claude session).
- Calc-only appendices had no vicinity map or road names, so CPs could not be placed without the companion map volume (ELTORO-007, claude session).
- Scanned reports had no text layer; the cloud step limit (45 s) blocked full OCR, so only key pages were OCR'd; run ocrmypdf locally for full volumes (ELTORO-007, claude session).
- 1999 study uses NOAA Atlas 2 and the 1979 county manual; use only as a cross-check (ELTORO-007, claude session).
- The same as-built set was filed three times (two folders plus a Copy file); dedupe by hash before reading (PHXZOO-001, claude session).
- Large consultant shapefile sets (120-280 MB) were copied into two places; keep one copy and link to it (PHXZOO-001, claude session).
- Render scratch (_tmp_render PNGs, a .write_test file in Submitted) was left in the synced project folder; keep scratch outside the project share (PHXZOO-001, claude session).
- Non-drainage items (pavement, traffic, cultural, roundabout) sit in the same Reference folder; tag them so the drainage review skips them (PHXZOO-001, claude session).
Jurisdiction add-ons:
- Pima County RFCD: older studies on NOAA Atlas 2 / 1979 county manual are cross-check only (ELTORO-007).
QC checks:
- No CP flow is carried forward without source document and page.
- No two sources' CPs are merged without a written concordance entry.
Source cards: ELTORO-007, PHXZOO-001

### DSO-C03 Public GIS and hydrology data harvest by REST/API
skill | new skill public-gis-data-harvest (+ add-on FEMA) | 3.7 | 1.5 | 3 | 2 (CALFIRE, SILVERBELL) | high
Trigger: Assembling base GIS and hydrology inputs for a site with no client CAD/GIS or no local county manual; exhibits or models need effective FEMA linework.
Steps (merged):
1. Query each ArcGIS REST layer by envelope with paging (500 records), outFields *; save a shapefile plus one master GeoPackage per theme (CALFIRE-003).
2. Layers: NFHL (zones, boundaries, panels, LOMRs, XS, BFE, profile baselines), NHD flowlines/waterbodies/areas, WBD HUC12, NWI, Census places/counties, state DOT highway lines, tenth postmiles, bridges, AADT, intersections, TIGER roads, USA Structures footprints, county parcels/zoning, state dam inundation boundaries (CALFIRE-003, SILVERBELL-013).
3. Write _download_log.csv: theme, layer, feature count or ERR text, source URL; log failures and continue (CALFIRE-003).
4. Locate crossings and entrances by state DOT tenth-postmile points (CALFIRE-003).
5. Rainfall: NOAA PFDS point query, depth and intensity (PDS, mean); save raw text and a DDF CSV; build 24-hr nested hyetographs at 5-min (CALFIRE-005).
6. Soils: SSURGO via Soil Data Access, map units with HSG; percent HSG per watershed (CALFIRE-005).
7. Land cover: NLCD 2021 clip by WCS/GeoTIFF. Gages: NWIS site list within the HUC (CALFIRE-005).
8. FEMA: save a native CAD reference drawing, RAS Mapper layers and render overlays from the same NFHL download; list LOMRs and compare to the hydraulic baseline before any regulatory statement (SILVERBELL-013).
Gotchas:
- NHD MapServer timed out at 180 s, then returned empty JSON on retry (4 download passes); fall back to the staged HU8 shapefile zip from the TNM S3 bucket (CALFIRE-003, claude session).
- Shapefile truncates field names over 10 characters; keep the GeoPackage as master (CALFIRE-003, claude session).
- Log failures instead of stopping the loop so one dead service does not cost the whole pass (CALFIRE-003, claude session).
- PFDS returns JavaScript text (result = values; quantiles = [...]), not JSON; parse the arrays (CALFIRE-005, claude session).
- Dual groups (B/D, C/D) and Not rated units (3-6 pct) need a stated rule before CN assignment (CALFIRE-005, claude session).
- Display-clipped polygons must not feed hydraulic encroachment logic (SILVERBELL-013, claude session; cross-ref SILVERBELL-002 in another group).
- An updated local model plus mapped lines is a screening, not a duplicate-effective model (SILVERBELL-013, claude session).
Jurisdiction add-ons:
- public-gis-data-harvest/FEMA: NFHL layer set, LOMR check before regulatory statements, screening vs duplicate-effective wording (SILVERBELL-013).
- public-gis-data-harvest/Caltrans-California: tenth-postmile points, AADT, state dam inundation boundaries (CALFIRE-003).
- Arizona jurisdictions with a county manual (e.g. Pima County RFCD PC-Hydro) use the manual's rainfall and soils sources instead of steps 5-7; steps 5-7 are for sites with no local manual (CALFIRE-005 trigger).
QC checks:
- _download_log.csv has no ERR rows unresolved before hydrology starts.
- HSG rule for dual/not-rated units stated in the assumption log.
Source cards: CALFIRE-003, CALFIRE-005, SILVERBELL-013

### DSO-C04 Terrain build from USGS 3DEP and composite DEM sources
skill | new skill terrain-dem-build (+ add-on Pima County RFCD) | 4.2 | 3.2 | 4 | 4 (CALFIRE, DLR, RKN, SAH) | high/low/medium
Trigger: Terrain needed for watershed delineation, road profile, 2D model or RAS Mapper; tiles from USGS TNM 3DEP with overlapping collections, or a composite of several lidar/DEM sources.
Steps (merged):
1. Size the extent from the full contributing area first: project plus all upstream/offsite watersheds plus margin (RKN-002).
2. Query the TNM API for 1 m DEM and 1/3 arc-sec tiles over the extent; save the item list (_tnm_items.json) (CALFIRE-004, RKN-002).
3. Select tiles by named collection/acquisition year, not by publication date; filter duplicates and overlapping vintages (RKN-002, CALFIRE-004; see conflict 1).
4. Clip the tile list to the model area plus buffer before import/mosaic (DLR-007).
5. Mosaic, reproject to the project State Plane (ft), convert NAVD88 m to ft (CALFIRE-004, RKN-002, DLR-007).
6. Write the hydraulics/grading DEM (3 ft; or 3.28 ft to keep native 1 m) and a hydrology DEM (10 ft or 30 ft by basin size); log grid size, min/max elevation; check nodata fraction is 0 (CALFIRE-004, RKN-002, DLR-007; see conflict 2).
7. Composites: merge in priority order and print the cell count taken from each source (SAH-020).
8. Difference newer and older lidar; list change areas over 20 ac with mean change; use newer lidar only where it is bare earth and the ground changed; log the vintage choice in the assumption log (SAH-020).
9. RAS Mapper: set the projection first from a known .prj; let RAS Mapper reproject on import; add shapefiles as map layers, not under Terrains; keep tiles under Terrain\USGS and record the tile list (a merged .vrt is a convenient index) (DLR-007).
10. Pull centerline profile (crests/sags) and stream profile at crossings from the site DEM (CALFIRE-004).
11. Keep raw tiles in Elevation_3DEP; never re-download inside a rerun (CALFIRE-004).
Gotchas:
- Tiles carry 2-3 overlapping vintages (2017, 2019, 2025) and duplicate NED entries; filter by project date or the mosaic mixes surfaces (CALFIRE-004, claude session).
- Newest-published logic picked the older 2018 collection (published 2025) on several tiles; fixed with a collection-preference step and a DEM rebuild (RKN-002, claude session).
- Initial DEM extent did not cover the full offsite watersheds; extending it changed several CP inputs and forced PC-Hydro reruns (RKN-002, claude session).
- A 107-tile merged input built a 20 GB terrain tif; clip first (DLR-007, claude session).
- Street and wash network shapefiles ended up listed under Terrains in the .rasmap (DLR-007, claude session).
- The USGS 2021 10-ft DEM contributed 0 cells to the composite and the run continued without noticing (SAH-020, claude session).
- Large changes (30 to 80 ft mean over hundreds of ac) were mine tailings growth, which affects depression volumes and flow paths (SAH-020, claude session).
- 1.8 GB of raw tiles per site (CALFIRE-004, claude session).
- Culvert inverts read from lidar are estimates only; carry as open items until survey (CALFIRE-004, claude session).
- USGS 1 m tiles are NAD83 UTM 12N, m (DLR-007); 1 m DEM is UTM m, convert to ft and compare to survey before use (STARVALLEY-014). Collapsed repeat: DLR-007, STARVALLEY-014.
- DLR-007 lessons come from a test project, not the DLR received set (DLR-007, claude session).
Jurisdiction add-ons:
- terrain-dem-build/Pima County RFCD: collections AZ_PimaCounty_2021_B21 (preferred), 2018, 2015 overlap; PAG 2015 10 ft lidar with NED 1/3 arc-sec outside coverage used on SAH; target CRS NAD83 HARN AZ Central intl ft (RKN-002, DLR-007, SAH-018, SAH-020; see conflict 3). TECH-033 cited for composite (SAH-020).
QC checks:
- Per-source cell count in a composite; any source with 0 cells stops the run.
- Nodata fraction 0 inside the contributing area.
- DEM extent covers every contributing watershed before PC-Hydro inputs are built.
Source cards: CALFIRE-004, RKN-002, SAH-020, DLR-007

### DSO-C05 Verify CRS, units and vertical datum of incoming survey/CAD/GIS against the model grid
qc_rule | QC rule (05_QC_Rules) | 11 | 4 | 2 | 2 (NORTHLOOP, STARVALLEY) | high/medium
Trigger: Using LandXML surfaces, CAD/DXF, shapefiles or new survey from the civil team with a model grid in State Plane; setting a pad or floor elevation against a modeled WSE.
Steps (merged):
1. Do not trust declared EPSG/.prj metadata; compare a few known points to the model grid (STARVALLEY-014).
2. If the file is in local site coordinates, apply the documented local-to-State Plane transform (translate, rotate, scale about base point) (STARVALLEY-014).
3. Find the vertical datum and benchmark note in the survey; if absent, request it and mark dependent elevations provisional (NORTHLOOP-019).
4. Reconcile units (metric survey vs ft plans) before any grid update (NORTHLOOP-019).
5. LandXML P order is northing, easting, elevation; interpolate on original triangles, exclude invisible faces, no extrapolation across voids; update the grid from the original survey triangles, not a new triangulation (STARVALLEY-014, NORTHLOOP-019).
6. Compare the new survey surface with the model grid/DEM (mean, std dev); list differences over 2 ft (NORTHLOOP-019, STARVALLEY-014).
7. Preserve CAD arcs with a chord tolerance before transforming (STARVALLEY-014).
Gotchas:
- LandXML declared EPSG:2223 but was in local coordinates; watershed and parcel shapefiles likewise had State Plane .prj with local coordinates (STARVALLEY-014, claude session).
- Old channel files sat about 50 ft off the true centerline (STARVALLEY-014, claude session).
- One CAD vertex differed by 100 ft and was excluded (STARVALLEY-014, claude session).
- Survey CAD had no datum or benchmark statement; pad elevation and WSE remain provisional (NORTHLOOP-019, claude session).
- An early Delaunay terrain was replaced by exact LandXML triangles (26,507 cells updated) (NORTHLOOP-019, claude session).
- DCR vertical datum unknown; EG vs FG differences are not earthwork depths (SILVERBELL-007, claude session; cross-ref DSO-C22).
QC checks:
- Known-point check (at least 3 points) logged for every incoming CAD/GIS/LandXML file.
- Vertical datum and benchmark stated for every survey used to set an elevation; otherwise the elevation is labeled provisional.
- Survey vs model grid difference table; differences over 2 ft explained.
Source cards: STARVALLEY-014, NORTHLOOP-019

### DSO-C06 Record plan and field-book retrieval with OCR provenance
skill | new skill record-plan-retrieval (+ add-on City of Tucson) | 15 | 3 | 1 | 1 (EKOS-LOCAL) | high
Trigger: Locating as-built plans, crossing details and benchmark/datum records for a drainage study from a public records catalog.
Steps (merged):
1. Search the public catalog with description queries by words and plan queries by plan ID; offer the model only observed action links (EKOS-LOCAL-013).
2. Field books: cookie session and CSRF token; follow next-page links with a page budget; shortlist matching filenames before model selection (EKOS-LOCAL-013).
3. Save every download with SHA-256; check PDF/TIFF magic bytes; keep receipts (EKOS-LOCAL-013).
4. Tesseract per page with orientation detection; make a rotated derivative and keep the original (EKOS-LOCAL-013).
5. Read OCR files with explicit strict utf-8 on Windows (EKOS-LOCAL-013).
6. Model picks source-offset excerpt IDs; quote text deterministically from the original; verify the page image before using any number (EKOS-LOCAL-013).
7. Accept a crossing detail only after it is spatially anchored (EKOS-LOCAL-013).
Gotchas:
- First field-book search stopped at page 1 and called the target missing (EKOS-LOCAL-013, claude session).
- Sideways scans gave zero OCR hits on all 26 pages until orientation was corrected (EKOS-LOCAL-013, claude session).
- Default cp1252 decoding failed on utf-8 OCR text (EKOS-LOCAL-013, claude session; same rule in EKOS-LOCAL-021).
- Free-form model quotes: only 40 of 137 matched the source exactly (EKOS-LOCAL-013, claude session).
- OCR misread 2698.20 as 2696.20 on one record; two monuments with the same elevation were different points (EKOS-LOCAL-013, claude session).
- Plan titles naming roads do not geolocate a structure; candidate crossing details stayed unaccepted until spatially anchored (EKOS-LOCAL-013, claude session).
- Recurrence: 8 datum/crossing retrieval tasks, 5 failed or empty (EKOS-LOCAL-013, claude session).
Jurisdiction add-ons:
- record-plan-retrieval/City of Tucson: Maps and Records public catalog (plan ID and description queries), field-book pages with cookie + CSRF session (EKOS-LOCAL-013).
QC checks:
- Every number taken from a record is checked against the page image, not OCR text.
- Every quoted excerpt matches the source byte-for-byte.
Source cards: EKOS-LOCAL-013

### DSO-C07 Verify existing conditions against governing as-builts, current imagery and regional flow paths
qc_rule | QC rule (05_QC_Rules) | 10.5 | 2.5 | 2 | 2 (ELTORO, SAHPARK) | high/medium
Trigger: Writing existing conditions or an existing-infrastructure inventory from as-built plans, especially for a corridor next to recent development.
Steps (merged):
1. Check revision blocks on every as-built set received; if two sets differ, note it on the cover and confirm the governing set with the owner before modeling (ELTORO-023).
2. Read every as-built and grading revision for adjacent projects; tabulate pipes and ditches with size, inverts, slope, outlet protection (SAHPARK-014).
3. Use current aerial imagery; note subdivisions built since the base imagery (SAHPARK-014).
4. Mark the main regional flow corridors and their 100-yr Q and state whether the project intercepts them (SAHPARK-014).
5. Where adjacent future development appears to redirect runoff, record it as an assumption and a risk (SAHPARK-014).
Gotchas:
- Two as-built versions of the sewer plans (ending Rev 7 and Rev 5) did not match (ELTORO-023, claude session).
- Draft missed 2 - 36 in. pipes at a school access and a ditch added by a grading revision (SAHPARK-014, EOR redline).
- Draft imagery predated a built subdivision (SAHPARK-014, EOR redline).
- Direction of runoff from an adjacent future facility was not addressed (SAHPARK-014, EOR redline).
- Regional corridor example: about 6,000 cfs 100-yr west of the alignment (SAHPARK-014, EOR redline).
QC checks:
- Governing as-built revision recorded for each set; conflicting sets noted and owner decision logged.
- Imagery date stated and later than the newest adjacent construction, or the gap noted.
- Regional flow corridors crossing or bordering the site have Q100 and an intercept statement.
- Recurrence counts individual redline comments (5 comments, SAHPARK-014).
Source cards: ELTORO-023, SAHPARK-014

### DSO-C08 Plan-to-report-to-calc crosswalk for inlets, pipes and culverts
skill | new skill plan-calc-crosswalk (used by qc-reviewer) | 9 | 3 | 1 | 1 (VALENCIA) | high
Trigger: Report and calcs must be checked against a newer or earlier plan set.
Steps (merged):
1. Extract all PDF markups and text from report, redlines and plan sets to CSV registers (VALENCIA-006).
2. Build crosswalks: inlet/scupper (ID, station, offset, type, opening), storm pipe (size, material, length, slope, inverts, rims), culvert (barrels, size, length, inverts, HW) (VALENCIA-006).
3. Keep watershed IDs; map plan IDs, report IDs and model IDs in separate columns without assuming they are equal (VALENCIA-006).
4. Three-way compare prior plan vs prior report vs latest plan; list design changes and actions (VALENCIA-006).
5. Locate features by station/offset from Civil 3D LandXML alignments where coordinates are needed (VALENCIA-006).
Gotchas:
- Old and new IDs shift (old SC11 = current SC15); keep both columns (VALENCIA-006, claude session).
- Plan sheets conflict internally (schedule vs profile labels; note says 3 arches while the sheet draws 2 barrels); record, do not pick silently (VALENCIA-006, claude session).
- A 387 ft profile length included a 50 ft segment past a junction; check dimensions before correcting lengths (VALENCIA-006, claude session).
QC checks:
- Every inlet, pipe and culvert in the latest plan set has a row in the crosswalk with report and model values or a "not in report" flag.
- Internal plan conflicts are listed as questions to the designer.
Source cards: VALENCIA-006

### DSO-C09 Reference library intake and local RAG with page citations
skill | new skill reference-library-intake | 8 | 4 | 2 | 1 (EKOS-LOCAL) | medium
Trigger: Bringing a folder of legacy reference documents into the shared library, or answering method/criteria questions from local reference PDFs with a local model.
Steps (merged):
1. Copy without altering source; compare SHA-256 before marking verified; keep original names and paths (EKOS-LOCAL-023).
2. Inventory executables but never run them (EKOS-LOCAL-023).
3. Extract PDFs to page-aware JSON with page provenance; record PDF and artifact SHA-256 (EKOS-LOCAL-022, EKOS-LOCAL-023).
4. OCR only zero-text or low-text PDFs, into separate derived files (EKOS-LOCAL-023).
5. Leave encrypted PDFs pending; do not bypass protection (EKOS-LOCAL-023).
6. Diagnose timeouts individually before longer retries (EKOS-LOCAL-023).
7. Chunk by actual tokenizer length; freeze and fingerprint the embedding profile (EKOS-LOCAL-022).
8. Version the Qdrant collection by artifact hash plus chunking and embedding profile; write only to pilot_ or versioned collections (EKOS-LOCAL-022).
9. Evaluate retrieval (hit@1, hit@5, MRR) before generation (EKOS-LOCAL-022).
10. Generator cites short evidence labels mapped by code to chunk IDs; reject unknown labels; require abstention when unanswerable (EKOS-LOCAL-022).
11. Keep edition, adoption and project applicability as separate registry fields; unknown stays unknown (EKOS-LOCAL-022).
12. Put human decisions in a separate sheet; never approve numbers from OCR alone (EKOS-LOCAL-023).
Gotchas:
- 715-file intake ran 5.3 h; 220 of 264 PDFs verified, 16 timeouts, 18 page-label failures, 8 zero-text (EKOS-LOCAL-023, claude session).
- A stdout warning on a successful extraction made the orchestrator mark failure; judge by exit code and output artifact (EKOS-LOCAL-023, claude session).
- OCR of map pages misread labels (EKOS-LOCAL-023, claude session).
- Qdrant 1.15.3 accepted but did not return collection metadata; verify the fingerprint in point payloads instead (EKOS-LOCAL-022, claude session).
- LM Studio rejected json_object response format (HTTP 400) (EKOS-LOCAL-022, EKOS-LOCAL-005, claude session). Collapsed repeat.
- Only a synthetic 5-page test passed; real manuals not yet qualified (EKOS-LOCAL-022, claude session).
QC checks:
- Retrieval metrics recorded before any generated answer is used.
- Every answer carries page citations that resolve to chunk IDs.
Source cards: EKOS-LOCAL-022, EKOS-LOCAL-023

### DSO-C10 Source files are read-only: work on scratch copies, hash before and after
qc_rule | QC rule (05_QC_Rules) | 1 | 1 | 1 | 1 (NORTHLOOP) | high
Trigger: Extracting geometry from source DWG files with AutoCAD console or scripts; more generally any automated read of received source files.
Steps (merged):
1. Copy the DWG to a scratch folder and run the export there (NORTHLOOP-018).
2. Hash source files before and after; stop if any source changes (NORTHLOOP-018).
3. Same rule applies to archives and reference intake: keep originals unchanged and work on copies (CAMPBELL-011 step 1, EKOS-LOCAL-023 step 1, NORTHLOOP-001 step 1). Collapsed repeat.
Gotchas:
- AutoCAD console refreshed a historical DWG and its BAK; the DWG was restored from backup but the older BAK was lost (NORTHLOOP-018, claude session).
QC checks:
- Before/after hash manifest of the source folder for every automated CAD export.
Source cards: NORTHLOOP-018

### DSO-C11 Official boundary GIS before any acreage or overlap numbers
qc_rule | QC rule (05_QC_Rules) | 2 | 2 | 1 | 1 (TANGERINE) | medium
Trigger: A report quantifies acreage of development, preserve, riparian habitat or swap land.
Steps (merged):
1. Obtain the official property, preserve and parcel GIS from the client team before computing any acreage (TANGERINE-007).
2. Record source, date and CRS of each layer in a data log (TANGERINE-007).
3. Compute overlaps by script so numbers can be rerun when layers change (TANGERINE-007).
4. After any layer update, rerun and push numbers to text, tables and figures in one pass (TANGERINE-007).
Gotchas:
- After the official boundary and preserve GIS arrived, swap land dropped from about 1,197 ac to 673 ac and baseline riparian preservation changed from about 55% to 73%; text, two tables and two figures had to be redone (TANGERINE-007, claude session).
Jurisdiction add-ons:
- Pima County riparian classification layer is the habitat source on Pima County sites (TANGERINE-007).
QC checks:
- Every acreage in text matches the scripted table from the logged layer versions.
Source cards: TANGERINE-007

### DSO-C12 Damaged project archive recovery and lost-model rebuild
skill | new skill archive-recovery | 3 | 3 | 1 | 1 (CAMPBELL) | medium
Trigger: Project export (large zip) is damaged or missing files.
Steps (merged):
1. Keep the original archive unchanged; recover entries without the central directory and CRC-check each (CAMPBELL-011).
2. Unpack nested zips; read notices of failed exports (CAMPBELL-011).
3. Write a file inventory CSV with sizes, dates and status (CAMPBELL-011).
4. Rebuild the model from surviving geometry, terrain, hydrographs and plan PDFs; record each assumption (CAMPBELL-011).
5. Keep recovered, working and revised models in separate folders (CAMPBELL-011).
Gotchas:
- 14 GB zip with no central directory failed standard extraction (CAMPBELL-011, claude via Codex session).
- Culvert native export and an impervious-surface shapefile were never downloaded; list as missing, never zero (CAMPBELL-011, claude via Codex session).
Source cards: CAMPBELL-011

### DSO-C13 Project intake and folder setup: local-file check, inventory, standards, findings, one-page scope
skill | new skill project-intake (feeds due-diligence-researcher) | 12.5 | 5.5 | 2 | 2 (NORTHLOOP, TANGERINE) | high
Trigger: Starting AI or script work on a project folder (often OneDrive), or an earlier study must be updated to current standards and a short scope is needed.
Steps (merged):
1. Check the folder holds real files (not only desktop.ini or cloud placeholders); set Always keep on this device or download first (TANGERINE-009).
2. After any bulk upload, check for a nested copy of the folder inside itself and for size growth before work starts (TANGERINE-009).
3. Copy to the work area with robocopy /S /E /MT:8 /R:1 /W:1 and log it; verify count and bytes; spot-check SHA-256; record in project notes that the copy is complete (TANGERINE-009).
4. Inventory the whole project folder (path, size, mtime, readable yes/no) to CSV; inventory ZIP contents separately; keep the inventory and all generated work outside the source job folder (NORTHLOOP-001).
5. If an upload is still running, save dated snapshots and a delta file; rerun the inventory when complete; mark findings provisional until then (NORTHLOOP-001).
6. Identify the prior report, native model folders, current site plan/CAD, survey, geotech report and correspondence; record which layout the prior report actually adopted (NORTHLOOP-001).
7. Check correspondence early for prior agency approval of the old report (decides addendum vs full replacement report) (NORTHLOOP-001).
8. Download all current jurisdiction standards into Review_<date>\Standards with a register (title, edition date, URL, current or historical) (NORTHLOOP-001; procedure in DSO-C01).
9. Write numbered findings (F01...) with severity, evidence locator (report page, model file) and action (NORTHLOOP-001).
10. Write the scope as plain text, one page target, two pages max, no subtasks, with assumptions and exclusions; list conditional services (FEMA map revision, regional model rebuild, easement-driven redesign) separately (NORTHLOOP-001).
Gotchas:
- Folder showed only desktop.ini until a manual download; the run stalled about 1 h (TANGERINE-009, claude session).
- A bulk upload created a full nested duplicate of the project folder inside itself (about 2,258 files, 50 GB), about 3 h to sync (TANGERINE-009, claude session).
- OneDrive resets file timestamps to the sync time, so file dates cannot be used to estimate work history; keep a dated log (TANGERINE-009, claude session).
- Upload grew from 1,726 to 2,653 files during the review; findings from the first snapshot had to be revised (NORTHLOOP-001, claude via Codex session).
- Correspondence did not show prior agency approval of the old report (NORTHLOOP-001, claude via Codex session).
- Prior report carried conflicting dates and tables (Q500 basis stated two ways); do not reuse tables without tracing to calcs (NORTHLOOP-001, claude via Codex session).
QC checks:
- Inventory final (no growth since last snapshot) before findings are issued.
- Copy verification log (count, bytes, hash sample) present.
Source cards: NORTHLOOP-001, TANGERINE-009

### DSO-C14 End-to-end rerun kit: folders, library prerequisites, run order and wall-time budget
standard/agent | Standard v0.3 change (run order + rerun kit) / agent model-run-supervisor | 0.5 | 0.5 | 2 | 2 (CALFIRE, SAH) | medium
Trigger: Rerunning or repeating an end-to-end drainage job (one-session preliminary report, or a full pilot) on a new site or for an agent-system test.
Steps (merged):
1. Parameterize the project root and job work folder in every script before a rerun (CALFIRE-018, SAH-018).
2. Standard folders with a dated scripts folder in 99_Working; all scripts write .log and .err files (CALFIRE-018; folder scheme in conflict 8).
3. Library prerequisites: .hy8 writer module, minimal HMS template project, Report_Template_7 and memo template paths, pinned ras_commander, pywinauto, HY-8 8.00, HEC-HMS 4.13, HEC-RAS 6.6 (CALFIRE-018).
4. Fix known blocking items from the prior run before rerunning (SAH-018).
5. Run order: due diligence agent; data/GIS (DEM, subbasins, culverts, terrain compare, crossings, inventory); hydrology (HMS build/runs, PC-Hydro, routing); 1D/2D runs in a separate agent; HY-8; alternatives; exhibits; report; compile; record copy (CALFIRE-018, SAH-018).
6. Run FLO-2D and HEC-RAS in parallel on separate core sets (SAH-018).
7. Budget wall time: about 6.5 h for a one-session preliminary report; about 48 h minimum for a full 2D pilot, governed by HEC-RAS (10 plans about 43 h sequential on 12 cores) (CALFIRE-018, SAH-018).
Gotchas:
- Scripts held hard paths to another project folder and to Python 3.12 site-packages (CALFIRE-018); all scripts hard-code the OneDrive job folder and the D: work folder (SAH-018). Collapsed repeat: CALFIRE-018, SAH-018 (claude session).
- Model runs and web services are the waits (CALFIRE-018, claude session).
- Original SAH run used about 25 h of continuous agent time plus 43 h of RAS queue (SAH-018, claude session).
- Fix SAH-002, SAH-003, SAH-006 and SAH-015 items first or the same reruns repeat (SAH-018, claude session).
- Recorded run times (FLO-2D UPPER + LOWER, h): 3-hr 100-yr 0.63 + 0.82; 24-hr 100-yr 1.86 + 2.91; 3-hr NoBerm 0.34 + 0.69; 24-hr NoBerm 1.09 + 3.54; 3-hr NoBerm MineFill 0.33 + 0.69; other frequencies est. 1.5 h per pair; HMS 50 runs about 40 min; PC-Hydro 67 subbasins 25 min; report build about 3 min (SAH-018, claude session).
QC checks:
- Grep for absolute paths before a rerun; none outside the parameter file.
Source cards: CALFIRE-018, SAH-018

### DSO-C15 Continuation file for multi-session work
skill | new skill session-continuation | 2 | 1 | 1 | 1 (ELTORO) | medium
Trigger: Model or proposal work that spans several AI chats or sessions.
Steps (merged):
1. Keep one continuation file in the project folder: scope, current model status, active task, open flags, data gaps, next actions, file map, key facts (ELTORO-022).
2. Record the execution split (who preps inputs, who runs compute, who post-processes) (ELTORO-022; see conflict 11).
3. Put unresolved reconciliation flags at the top so the next session checks them first (ELTORO-022).
4. Each open flag gets an explicit next action (e.g. re-export the model copy for checking) (ELTORO-022 gotcha).
5. Pair it with companion files (inflow register, relevance review) rather than one large file (ELTORO-022).
Gotchas:
- The top open flag (inflow values mismatch) was carried forward but the model copy was never re-exported for checking (ELTORO-022, claude session).
- Related: drafting from an append-only checkpoint log repeats superseded statements; the continuation file must be a curated current state, not a history (EKOS-LOCAL-001, claude session; cross-ref DSO-C26).
Source cards: ELTORO-022

### DSO-C16 HEC-RAS project hygiene: plans, geometries, versions, copies
skill | new skill hecras-project-hygiene (used by model-run-supervisor) | 18 | 6 | 1 | 1 (ELTORO) | high
Trigger: Any 2D model that goes through more than one design iteration or is reused for a second project.
Steps (merged):
1. Keep one working project; archive frozen copies as dated zip instead of parallel live folders (ELTORO-005).
2. Name plans <condition>-<freq>-<variant> and geometries to match; delete auto-named duplicates and placeholder plans (ELTORO-005).
3. Record the HEC-RAS version per plan; do not mix versions in one project without a pre-upgrade copy (ELTORO-005).
4. Purge failed Retry geometries and their results once the cause is logged (ELTORO-005).
5. Keep large post-processing HDF (fine-grid runs near 1 GB) out of synced folders (ELTORO-005).
Gotchas:
- Each project copy carried 36-40 plans; p01-p14 were duplicated by auto-named p16-p29 pointing to the same geometry/flow pairs (ELTORO-005, claude session).
- Placeholder names (plan "1", "Plan 37", geometry "New Geometry") and Retry/Retry2 geometries made it unclear which run fed the memo (ELTORO-005, claude session).
- The same model existed in three live folders plus a full duplicate tree under another OneDrive folder (ELTORO-005, claude session).
- Plans p01-p36 are 6.6 while p37-p40 are 7.0 in the same project (ELTORO-005, claude session).
- Geometry autosave produced 22 backups of one geometry in one day and about 75 backup geometries in total (ELTORO-005, claude session).
QC checks:
- Report/memo cites plan name, plan number and HEC-RAS version for every run used.
- No placeholder plan or geometry names in a delivered project.
Source cards: ELTORO-005

### DSO-C17 Consultant CAD base reissue: archive, swap, list changes, flag rework
skill | new skill cad-base-update | 88 | 8 | 1 | 1 (HOMEWOOD) | medium
Trigger: Architect or site-plan CAD base is reissued during design.
Steps (merged):
1. Before replacing xrefs, copy current files to References\DWG\<consultant>\Archive\<date> Before CAD Update (HOMEWOOD-021).
2. Swap the xref, then list what moved (buildings, electrical area, site linework) (HOMEWOOD-021).
3. Flag affected storm drain, grading, gallery and exhibit items and reissue check plots (HOMEWOOD-021).
Gotchas:
- Architect base reissued about 7 times and site plan 4 times in five months; each update forced storm drain and exhibit rework (HOMEWOOD-021, claude session).
Jurisdiction add-ons:
- None procedural; project in Placer County CA / TRPA, but the procedure is jurisdiction-neutral.
QC checks:
- Change list per reissue, with affected sheets/exhibits, filed beside the archive folder.
Source cards: HOMEWOOD-021

### DSO-C18 Phase coordination tracker and meeting agenda/minutes kit
skill | new skill project-coordination-tracker | 4 | 2 | 1 | 1 (PHXZOO) | high
Trigger: Conceptual drainage phase with recurring meetings with a client site planner and an adjacent internal project.
Steps (merged):
1. One workbook: Dashboard, Task Tracker, Open Questions (Q-###), Data Exchange (D-###), Meeting Log, Action Items (AI-###); Dashboard counts open items live from the log tabs (PHXZOO-003).
2. Load tasks from the executed scope only (task no, description, target date as NTP + n months); never from draft fee versions (PHXZOO-003).
3. Dashboard meeting-count flag: meetings held vs meetings budgeted in the admin task (PHXZOO-003).
4. Reusable agenda: progress, concept alternatives, open questions, data exchange, adjacent project interface, agency coordination, action items (PHXZOO-003).
5. After each meeting convert the agenda into minutes with an outcome callout per item; copy every new action item and data transfer into the workbook the same day (PHXZOO-003).
6. Move the used agenda to _superseded once minutes are issued (PHXZOO-003).
7. Ask for the current site plan iteration before each analysis step and log it as a D-### item (PHXZOO-003).
Gotchas:
- Six action items were written in Meeting 1 minutes but the Action Items and Data Exchange tabs stayed empty (PHXZOO-003, claude session).
- Dashboard kept placeholders (last updated, NTP, as-of date) and 0 percent complete while hours were already charged; fill dates at first update (PHXZOO-003, claude session).
- Budget covered about six monthly meetings but cadence was set weekly (about 26); flag the change-order need early (PHXZOO-003, claude session).
- Scope said up to a third option would be explored without defining it; confirm and document undefined scope items at the first meeting (PHXZOO-003, claude session).
- Site plan on file (March draft) lacked an item the planner referenced (PHXZOO-003, claude session).
Jurisdiction add-ons:
- Agenda agency line lists the governing agencies (e.g. Town of Sahuarita, PCRFCD, county plant boundary) (PHXZOO-003).
QC checks:
- Open action items in minutes = open rows in the Action Items tab.
- Meetings held <= meetings budgeted, or a change-order flag raised.
Source cards: PHXZOO-003

### DSO-C19 Constraint-matrix construction phasing for long channel projects (proposal stage)
skill | new skill construction-phasing-plan | 1 | 1 | 1 | 1 (BARNETT) | medium
Trigger: Owner wants a complete drainage plan set for grant applications and the option to build in phases as funds arrive.
Steps (merged):
1. Walk the roll plot from the outfall upstream; break segments where a governing constraint changes (BARNETT-012).
2. Score each segment: real property, utilities, irrigation district relocation (underground or not), access during and after construction, unresolved design items, need for community input (BARNETT-012).
3. Phase by work type as well as station: drainage channel, culverts and base path first; park amenities later (BARNETT-012).
4. Assume one comprehensive plan set (CMAR can build by station range); separate bid packages are additional services (BARNETT-012).
5. Stop design short of jurisdictional waters at the river tie-in unless a 404 delineation is in hand (BARNETT-012).
6. Allocate the overall cost estimate to each phase so the owner can match CIP funding (BARNETT-012).
7. Hold the phasing workshop early in final design with traffic, planning and the owner present (BARNETT-012).
Gotchas:
- An outfall-only phase spends money without function until the channel upstream is built; check each phase delivers benefit alone (BARNETT-012, claude session).
- Irrigation district asked for new easements matching existing ones wherever facilities are relocated, after plans were drawn; ask at scoping (BARNETT-012, claude session).
Source cards: BARNETT-012

### DSO-C20 Confirm the controlling submitted version before revising
qc_rule | QC rule (05_QC_Rules) | 6 | 3 | 1 | 1 (BARNETT) | medium
Trigger: Revising any previously submitted proposal or report from local working files.
Steps (merged):
1. Get the as-submitted PDF and treat it as controlling; compare totals and task text against the working Word and Excel files before editing (BARNETT-013).
2. Flag internal contradictions in the submitted text (a task described as included and also listed as excluded) (BARNETT-013).
3. If an emailed attachment is rights-protected, open it in Outlook on the workstation and save a readable copy; PDF libraries cannot read it (BARNETT-013).
4. Save outputs to the project OneDrive folder, not a local tool workspace (BARNETT-013; same rule in CAMPBELL-023).
Gotchas:
- The working spreadsheet did not match the submitted PDF, and the first copy of the submitted PDF was encrypted; recovered through Outlook and rebuilt (BARNETT-013, claude via Codex session).
QC checks:
- Fee totals and task list of the revision start from the as-submitted PDF; differences vs working files listed.
Source cards: BARNETT-013

### DSO-C21 Civil 3D automation: seat check, NETLOAD helpers, modal dialogs, completion markers
skill | new skill civil3d-automation | 12 | 4 | 2 | 2 (SILVERBELL, TANGERINE) | medium
Trigger: An automated run needs alignments, profiles or corridor geometry from Civil 3D, loads compiled .NET helpers into a running Civil 3D session, or needs InfraWorks renders.
Steps (merged):
1. Before scheduling, confirm a Civil 3D seat is free on this machine (no Device limit reached) (TANGERINE-010).
2. Build any NETLOAD plugin as a proper project targeting the installed AutoCAD .NET runtime; test it in accoreconsole on one drawing (TANGERINE-010).
3. Pre-trust a single helper folder or batch helpers into one DLL so the user approves once (SILVERBELL-009).
4. Verify the exact target drawing FullName before SendCommand; guard ActiveDocument changes (SILVERBELL-009).
5. Write a completion marker file per helper; never repeat NETLOAD for a helper already logged complete (SILVERBELL-009).
6. Run native CAD COM from an elevated shell (SILVERBELL-009).
7. Fallback: export LandXML alignments and profiles from Civil 3D by hand and read them by script (TANGERINE-010).
8. Build the InfraWorks base model (terrain, aerial) only after CRS and vertical units are verified; do not present source-only aerial views as proposed-corridor renders (TANGERINE-010).
9. Work on scratch copies of source DWGs (DSO-C10).
Gotchas:
- A csc-compiled Extract.dll mixing .NET 8 and .NET 10 references failed in accoreconsole with Unable to load assembly, then Unknown command (TANGERINE-010, claude session).
- Civil 3D showed Device limit reached because another device held the seat; proposed corridor and six perspectives stayed pending (TANGERINE-010, claude session).
- Choose Assembly and Load Once dialogs blocked COM; computer-use could not reach off-monitor dialogs; the user had to click for 4 helpers (SILVERBELL-009, claude session).
- A generic assembly error left one helper unapplied; native grading finished only with a later helper (SILVERBELL-009, claude session).
- Native CAD COM needs an elevated shell (SILVERBELL-009, claude session).
Source cards: TANGERINE-010, SILVERBELL-009

### DSO-C22 Civil 3D base reconstruction from PDF DCR and GIS linework
skill | new skill civil3d-reconstruction-from-pdf | 16 | 4 | 1 | 1 (SILVERBELL) | high
Trigger: Only a PDF DCR and GIS linework exist and a native Civil 3D base, corridor and plan set is needed.
Steps (merged):
1. Extract the construction baseline from PDF vector strokes; georeference to the supplied GIS; keep a CAD-to-plan station crosswalk (SILVERBELL-007).
2. Build EG TIN from clipped lidar; trace the proposed profile from the plotted line at about 5 ft spacing (SILVERBELL-007).
3. Build corridor regions at source transition stations; record every schematic assumption on a decisions sheet (SILVERBELL-007).
4. Produce individual sheets plus a combined PDF; package with checksums per revision (SILVERBELL-007).
5. Keep the .mms companion file beside each DWG (SILVERBELL-007).
Gotchas:
- Recovered chainage drifted 32.7 ft over the corridor; keep it in the crosswalk, do not hide it with a coordinate shift (SILVERBELL-007, claude session).
- Printed vertical-curve labels conflicted with the plotted line; trace follows plotted geometry and the conflict is flagged (SILVERBELL-007, claude session).
- DCR vertical datum unknown; EG vs FG differences are not earthwork depths (SILVERBELL-007, claude session).
- Without the .mms companion file the large surface is lost (SILVERBELL-007, claude session).
Source cards: SILVERBELL-007

### DSO-C23 EKOS workstation environment rules for scripts and agents
skill | new skill ekos-environment-rules (load in every EKOS agent) | 15 | 3 | 1 | 1 (EKOS-LOCAL) | high
Trigger: Any agent running Python, GIS or install commands on the EKOS workstation.
Steps (merged):
1. Use the locked uv environments (uv run --project <env>); never bare pip or global Python 3.14 (EKOS-LOCAL-021).
2. GIS venv for rasterio/geopandas; documents venv for model schema validation (EKOS-LOCAL-021; same rule in EKOS-LOCAL-002).
3. Keep QGIS GDAL/PROJ off PATH; use the QGIS shell wrapper or the conda PDAL env (EKOS-LOCAL-021).
4. PowerShell .ps1 execution is disabled; run Python or inline commands; do not change policy (EKOS-LOCAL-021; see conflict 7).
5. Open text with explicit encoding utf-8 (Windows default is cp1252) (EKOS-LOCAL-021, EKOS-LOCAL-013). Collapsed repeat.
6. Use a Docker named volume for Qdrant data, not a Windows bind mount (EKOS-LOCAL-021).
7. Write validation scratch to workspace paths, not user TEMP (EKOS-LOCAL-021).
Gotchas:
- install-wsl-admin.ps1 failed: running scripts is disabled (EKOS-LOCAL-021, claude via Codex session).
- Qdrant rejected the Windows bind mount for durability; moved to named volume (EKOS-LOCAL-021, claude via Codex session).
- Hugging Face cache cannot symlink without Developer Mode (extra disk only) (EKOS-LOCAL-021, claude via Codex session).
- Sandbox validations could not write to user TEMP (EKOS-LOCAL-021, claude via Codex session).
- GIS venv lacked jsonschema; keep GIS calculation and local-model schema validation in separate qualified environments (EKOS-LOCAL-002, claude via Codex session).
- After a session restart, python on PATH lacked numpy and h5py (SAH-015, claude session; cross-ref DSO-C25).
Source cards: EKOS-LOCAL-021

### DSO-C24 Engineering software install and validation (FLO-2D Pro + QGIS plugin, CFD engines)
skill | new skill software-install-validation | 5.5 | 3.5 | 2 | 2 (EKOS-LOCAL, SAH) | medium
Trigger: New workstation, FLO-2D upgrade, QGIS FLO-2D toolbar missing, or installing CFD/DEM engines or GIS plugins.
Steps (merged):
1. Check what is already installed first (engine folder Program Files (x86)\FLO-2D PRO vs QGIS plugin; installed QGIS LTR version); back up QGIS settings (EKOS-LOCAL-024, SAH-005).
2. If a compatible QGIS is present, skip the bundled QGIS; install the matching FLO-2D plugin (2.2.0 "Gila" for QGIS 3.44) into the existing QGIS profile plugins folder and enable it; set engine path (EKOS-LOCAL-024, SAH-005). Collapsed repeat.
3. Run the license activator from its own folder; confirm activation by running a model (SAH-005).
4. Validate every install by running a real example end to end; for FLO-2D check SUMMARY.OUT (full simulation, volume conservation) and ERROR.CHK (no fatal errors) (EKOS-LOCAL-024, SAH-005).
5. Close finished runs before rerunning the same folder (EKOS-LOCAL-024).
6. WSL: source the OpenFOAM bashrc from the profile; build LIGGGHTS STUBS before make serial (EKOS-LOCAL-024).
7. GPU: RTX 5090 (SM 12.0) needs CUDA 12.8 PyTorch builds (EKOS-LOCAL-024).
8. Save a short ready-to-run note and the plugin dependency check (h5py, netCDF4, engine path); record account-bound or interactive steps as unresolved instead of claiming done (SAH-005, EKOS-LOCAL-024).
Gotchas:
- FLO-2D installer complained QGIS was not part of the install; the real gap was the missing plugin (EKOS-LOCAL-024); plugin missing from the QGIS profile though the engine was installed, installer QGIS step failed because QGIS already existed (SAH-005). Collapsed repeat: EKOS-LOCAL-024, SAH-005 (claude via Codex session).
- Second FLO-2D run hit a file lock from an open test process (EKOS-LOCAL-024, claude via Codex session).
- CUDA 12.4 kernels failed on SM 12.0 (EKOS-LOCAL-024, claude via Codex session).
- The activator window closes by itself on success without a message; a user check was needed (SAH-005, claude via Codex session).
Source cards: EKOS-LOCAL-024, SAH-005

### DSO-C25 Long model jobs must survive session restarts
agent | agent model-run-supervisor | 10 | 2.5 | 1 | 1 (SAH) | high
Trigger: An AI session or remote shell starts model runs that last longer than the session.
Steps (merged):
1. Call the interpreter by full path in every .cmd; never rely on python from PATH (SAH-015; see conflict 6).
2. Start long jobs outside the calling process tree (Win32_Process Create through CIM; detached launcher) so a session end does not kill them (SAH-015; see conflict 7).
3. Write a .started and .done file per step; on restart, read them and resume instead of re-running finished steps (SAH-015).
4. Check every input path exists, and no input is locked by another program, before a chain starts (SAH-015).
Gotchas:
- All running FLO-2D and HEC-RAS jobs under the session were killed at once when the session ended; queues were relaunched about 1 h later and one run restarted (SAH-015, claude session).
- After restart python on PATH lacked numpy and h5py, so the inflow fix step and a RAS queue failed at import (SAH-015, claude session).
- Chain failed on a missing berm geojson; a later step failed on a file locked by HMS (SAH-015, claude session).
QC checks:
- Every step in a chain has .started/.done markers; resume log shows skipped completed steps.
Source cards: SAH-015

### DSO-C26 Unattended local supervisor: manifest, loop guards, completion gates, honest end-state alerts
agent | agent ekos-local-supervisor | 20 | 7 | 2 | 1 (EKOS-LOCAL) | high
Trigger: Any unattended local-model run that plans steps, calls tools and drafts a drainage report without cloud supervision, and alerts the owner when it ends.
Steps (merged):
1. Give the supervisor a compact current-state manifest (completed milestones, open blockers, accepted inputs) generated from structured outputs; never draft from the append-only checkpoint or history log (EKOS-LOCAL-001).
2. Read JSON evidence as parsed objects or targeted keys, not fixed 50-line text windows (EKOS-LOCAL-001).
3. Fingerprint repeated work on action plus target file (ignore offset/window arguments); after 2 repeats force a different action or end the branch (EKOS-LOCAL-001).
4. Cap native retries at 2 identical attempts and at most 2 materially different recoveries; then log and move to an independent branch (EKOS-LOCAL-001).
5. Gate completion on required native artifacts (fresh output files, numeric checks, provenance), not on filled report sections (EKOS-LOCAL-001).
6. On exit write a terminal heartbeat (finally block) and reconcile state, queue and actual process existence before notifying (EKOS-LOCAL-001).
7. Distinct end states: completed, partial, blocked, failed; a draft with unresolved modeling is partial and the alert says so (EKOS-LOCAL-001, EKOS-LOCAL-020). Collapsed repeat.
8. Honor an owner STOP_REQUESTED file and a single-instance lock (EKOS-LOCAL-001).
9. Notification: keep server and topic in a private config outside prompts and logs; test once; distinguish server-accepted from owner-confirmed receipt (EKOS-LOCAL-020).
10. Persist send intent before posting; investigate delivery_unknown before resending; clear intent/receipt per run ID (EKOS-LOCAL-020).
11. Message gives end state and file paths on the workstation (EKOS-LOCAL-020).
Gotchas:
- Continuation run ended after 8 steps (about 20 s) as draft-ready with unresolved modeling after re-reading the same summary.json 3 times in 50-line windows; no hydraulic work attempted (EKOS-LOCAL-001, claude session).
- Sections drafted from the checkpoint log repeated superseded statements and misread a task label as a project name (EKOS-LOCAL-001, claude session).
- One section failed on an unterminated JSON string from the local model after 2 bounded attempts and was left Unresolved; correct behavior, keep it (EKOS-LOCAL-001, claude session).
- Heartbeat stayed LOCAL_REASONING after the run terminated (EKOS-LOCAL-001, claude session).
- Exact-match loop detection is evaded by small argument changes (start or line offsets) (EKOS-LOCAL-001, claude session).
- Fourteen filled report headings looked complete while all RAS 1D/2D, HY-8 and 100-yr routing were missing (EKOS-LOCAL-001, claude session).
- Alert said draft ready while hydraulics were missing (EKOS-LOCAL-020, EKOS-LOCAL-001, claude session). Collapsed repeat.
- A leftover intent or receipt can suppress the next alert (EKOS-LOCAL-020, claude session).
- Paths sent to a phone do not give remote file access (EKOS-LOCAL-020, claude session); deliver review copies to OneDrive (DSO-C31).
- Recurrence: 3 autonomous pilots, all ended without hydraulic progress (EKOS-LOCAL-001, claude session).
QC checks:
- Completion gate list of required native artifacts per report type (PC-Hydro printouts, HMS/RAS/HY-8 outputs) checked before any "completed" state.
Source cards: EKOS-LOCAL-001, EKOS-LOCAL-020

### DSO-C27 Persistent local queue worker: dependencies, failure capture, idle detection
agent | agent ekos-local-supervisor (queue worker component) | 88 | 4 | 1 | 1 (EKOS-LOCAL) | high
Trigger: Running registered local scripts (GIS, PC-Hydro, HMS, RAS, report build) overnight from a task plan.
Steps (merged):
1. Keep tasks in a plan file that maps only to registered actions in an approved-actions catalog; adding a task ID needs no restart (EKOS-LOCAL-002).
2. Strict dependencies for calculations; after_settled dependencies for progress packaging so a failed evidence job does not block the review package (EKOS-LOCAL-002).
3. Retry only adapters marked resume_safe, with a finite attempt limit; preserve failed attempts; continue independent tasks (EKOS-LOCAL-002).
4. Hold one OS-level worker lock; confirm a fresh RUNNING heartbeat, child PID and an advancing task log before claiming work is delegated (EKOS-LOCAL-002).
5. When a task is replaced, explicitly cancel or re-point dependents of the failed ID; refresh dependencies of existing pending tasks (EKOS-LOCAL-002).
6. Store stderr tail and exit reason with every failed task in the supervisor inbox (EKOS-LOCAL-002).
7. Write a deduplicated supervisor inbox when ready work is exhausted (EKOS-LOCAL-002).
Gotchas:
- Queue policy only added new IDs and never refreshed dependencies of existing pending tasks; 3 obsolete tasks stayed pending forever on failed predecessors (EKOS-LOCAL-002, claude via Codex session).
- 22 of 140 tasks ended NEEDS_REVIEW and the inbox recorded every one as error null with exit_code 1, so each had to be re-investigated from logs (EKOS-LOCAL-002, claude via Codex session).
- Worker in WAITING_FOR_SUPERVISOR showed 0 GPU use while the owner expected work; waiting is not engineering progress (EKOS-LOCAL-002, claude via Codex session).
- Registering a new action in worker code requires a controlled restart (RESTART_REQUESTED marker); the approved-actions catalog avoids that (EKOS-LOCAL-002, claude via Codex session).
- GIS venv lacked jsonschema (EKOS-LOCAL-002; moved to DSO-C23).
Source cards: EKOS-LOCAL-002

### DSO-C28 Cloud supervisor budget: one plan, one exception packet, one final QA
agent | agent ekos-local-supervisor (cloud supervision policy) | 200 | 10 | 1 | 1 (EKOS-LOCAL) | high
Trigger: Using a paid cloud model (Codex, Claude, GPT) to supervise local models on an engineering job.
Steps (merged):
1. Cloud writes the plan and task list once, then stops; the local worker executes (EKOS-LOCAL-003).
2. Local agents make reversible choices and owner-authorized preliminary assumptions; log each with source, rationale and affected outputs (EKOS-LOCAL-003).
3. Batch unresolved questions into one review packet (completed milestones, decisions to review, failed attempts with evidence paths, grouped questions); omit routine status and unchanged files (EKOS-LOCAL-003).
4. Cloud answers return as structured decisions plus draft lessons; local replay required before a lesson is marked verified (EKOS-LOCAL-003; lifecycle in DSO-C29).
5. At most one daily cloud check; never a 15 or 30 min heartbeat (EKOS-LOCAL-003).
6. When the cloud solves a novel issue it records the procedure (knowledge.put) and has the local worker replay it, instead of computing results or fetching data itself (EKOS-LOCAL-003; see conflict 12).
Gotchas:
- 15-30 min heartbeats, incremental connector development, repeated image reviews and 24 review-package refreshes used about 50 percent of the weekly cloud quota in about 1.5 days; owner judged it more than doing the job directly (EKOS-LOCAL-003, claude via Codex session, owner correction).
- Cloud agent kept ending its turn with a final response, so nothing ran between owner prompts; progress updates must not end the work turn (EKOS-LOCAL-003, claude via Codex session).
- Cloud started doing calculations itself; owner correction: the local AI does the calcs, cloud only plans, teaches and reviews (EKOS-LOCAL-003, claude via Codex session, owner correction).
- Cloud fetched source data itself; owner correction: teach the local worker the retrieval procedure so it can repeat it (EKOS-LOCAL-003, claude via Codex session, owner correction).
- Recurrence: about 20 scheduled cloud heartbeats overnight plus 4 owner corrections (EKOS-LOCAL-003).
Source cards: EKOS-LOCAL-003

### DSO-C29 Shared knowledge base lesson lifecycle for local models
skill | new skill knowledge-lesson-lifecycle | 8 | 2 | 1 | 1 (EKOS-LOCAL) | high
Trigger: Before a local worker retries a known problem, and after any investigated failure.
Steps (merged):
1. Look up verified lessons through the knowledge module before each local model request (gateway injects up to 3 matching procedures) (EKOS-LOCAL-004).
2. For a novel issue the supervisor investigates, solves, then records topic, applicability, steps, validation evidence and limits (EKOS-LOCAL-004).
3. Mark a lesson verified only after the local worker replays it through its own tools; otherwise record it as open or blocked (EKOS-LOCAL-004, EKOS-LOCAL-003).
4. Keep draft, blocked, retired and verified states distinct; retire superseded lessons with a pointer to the replacement (EKOS-LOCAL-004).
5. Keep project facts, owner assumptions and approvals out of lessons; a lesson never grants approval (EKOS-LOCAL-004).
6. Group lessons by topic folders (local-models, gis-records, hydrology, hydraulics, orchestration); sqlite is authoritative, md/json are mirrors (EKOS-LOCAL-004).
7. Drop a lesson from automatic retrieval when its evidence files change or go missing (EKOS-LOCAL-004).
Gotchas:
- Retrieval is keyword matching; relevance can be poor; include error strings and software names in lesson titles (EKOS-LOCAL-004, claude session).
- Standalone LM Studio and Ollama chats do not see the knowledge base; direct integration was still not done after 4 weekly reminders (EKOS-LOCAL-004, claude session).
- A successfully proposed repair is not proof of local replay (EKOS-LOCAL-004, claude session).
- 45 lessons recorded in 1.5 days (EKOS-LOCAL-004, claude session).
Note: this lifecycle overlaps the shared skills library card format (verified/draft states, no project facts); align fields with the library card schema.
Source cards: EKOS-LOCAL-004

### DSO-C30 Local model gateway: context budget, structured output, model roles
skill | new skill local-model-gateway | 18 | 3 | 1 | 1 (EKOS-LOCAL) | high
Trigger: Sending evidence, OCR or catalog data to a local LM Studio model for selection, reading or narrative.
Steps (merged):
1. Budget prompt plus output inside the loaded context (8k for 4B/9B); pre-filter rows or shortlist links before inference (EKOS-LOCAL-005, EKOS-LOCAL-013).
2. Use the LM Studio native API with reasoning off for small models and a strict json_schema response format (EKOS-LOCAL-005, EKOS-LOCAL-022).
3. Model selects only observed IDs (records, OCR excerpt IDs, URLs, evidence labels); reject unknown IDs; resolve quotes deterministically from source (EKOS-LOCAL-005, EKOS-LOCAL-013, EKOS-LOCAL-022). Collapsed repeat.
4. Generate numeric wording from checked structured rows; never accept numbers written by the model (EKOS-LOCAL-005).
5. Model roles: 4B for first-pass crop reading, 9B for recovery and extraction, a 4B dispatcher for routing only (not numbers); inference concurrency 2 (EKOS-LOCAL-005; see conflict 10).
6. Route every local call through the gateway so knowledge lookup and attempt logging happen (EKOS-LOCAL-005).
Gotchas:
- Sending 131 scan links into an 8k context caused HTTP 500; shortlist first (EKOS-LOCAL-005, claude session).
- Long reviews through the OpenAI-compatible endpoint exhausted output budget on reasoning; native API with reasoning off fixed it (EKOS-LOCAL-005, claude session).
- LM Studio rejected response_format json_object with HTTP 400; use json_schema or text (EKOS-LOCAL-005, EKOS-LOCAL-022, claude session). Collapsed repeat.
- Gemma 4 12B passed only 5/10 cited answers (token budget spent in reasoning); Mistral Small 3.2 passed 10/10 on the same synthetic test (EKOS-LOCAL-005, claude session).
- Nemotron Nano 4B rounded 11/12 ft too coarsely; do not use it for numbers (EKOS-LOCAL-005, claude session).
- Local Qwen invented a hydraulic standard and misbound a stage value to the wrong area result; schema-valid output is not factual (EKOS-LOCAL-005, claude session).
Source cards: EKOS-LOCAL-005

### DSO-C31 Deliverable package assembly, naming and OneDrive delivery
standard | Standard v0.3 change (deliverable packaging) / drainage-report-build sec 4 | 4.8 | 1.4 | 2 | 2 (CAMPBELL, RKN) | high
Trigger: Transferring finished H&H/site plan deliverables, or the user needs results to review on another computer or phone.
Steps (merged):
1. Standard folder set inside the package (reports, exhibits, GIS, CAD, models, calculations, scripts, QC) (RKN-019; folder numbering in conflict 8).
2. Name the folder and zip <Initials>_<date>_<CODE>_<description> (RKN-019, CAMPBELL-023; date format in conflict 9).
3. Exclude run copies, runtime junctions, temp/checkpoint HDF and scratch (_run0x, .tmp.hdf, _body_, compute_stdout, files starting with _) (RKN-019, CAMPBELL-023). Collapsed repeat.
4. Set docx/xlsx creator and last-modified-by to the firm preparer string (RKN-019; matches drainage-report-build sec 2).
5. Write a README listing contents, coordinate system and software versions; report file count, zipped and unzipped size (RKN-019, CAMPBELL-023).
6. Save every deliverable to the dated OneDrive project folder; include portable HTML and MP4 for phone review (CAMPBELL-023, BARNETT-013).
7. Verify hashes; state that cloud sync was not checked (CAMPBELL-023).
Gotchas:
- First package used a non-standard folder name and missed printouts/QC; rebuilt two hours later (3.4 GB then 3.7 GB zip) (RKN-019, claude session).
- Download links failed on the phone and email was not set up; OneDrive on the phone worked (CAMPBELL-023, claude via Codex session).
QC checks:
- Package contains native printouts and QC folder; no excluded patterns present; README versions match the models.
Source cards: CAMPBELL-023, RKN-019

### DSO-C32 Concept site plan layout chain to drive proposed-conditions H&H
skill | new skill concept-site-layout | 2 | 1 | 1 | 1 (RKN) | medium
Trigger: A concept site plan alternative is needed to drive proposed-conditions H&H.
Steps (merged):
1. Build hard constraints: floodplains, slopes >= 25%, cultural, setbacks; optional alternative preserving every Q100 > 100 cfs wash floodplain plus 25 ft (RKN-010).
2. Developable pods from 200-ft-window average slope < 15%, opened 75 ft to remove slivers (RKN-010).
3. Public roads (spine 95-ft ROW, R >= 600 ft, 8% max; collectors 60-ft ROW) tied to fixed crossings such as a bridge in an effective CLOMR (RKN-010).
4. Gated blocks, loop and connector streets, lots fronting connected streets; run layout QA (overlaps, lots in ROW/washes, connectivity) and report counts (RKN-010).
5. Mass grading on a 5-ft grid with per-block cut/fill balance; proposed DEM; slope-concern markups (RKN-010).
Gotchas:
- Lot script crashed on MultiPolygon block cores ('no attribute exterior'); explode to parts before SVD orientation (RKN-010, claude session).
- QA still found lots inside local street ROW; keep the QA step in the chain and report counts (RKN-010, claude session).
Jurisdiction add-ons:
- Road geometry values (95-ft spine ROW, R >= 600 ft, 8% max, 60-ft collector ROW) are project/Pima County assumptions; confirm against the governing roadway standard per jurisdiction (RKN-010).
Source cards: RKN-010

### DSO-C33 Bluebeam Revu MCP and OCR setup for markup-driven review
skill | new skill bluebeam-mcp-setup | 1.5 | 1.5 | 1 | 1 (VALENCIA) | high
Trigger: Agent needs to read or add markups, OCR scanned output, or compare PDFs on EKOS.
Steps (merged):
1. Confirm the Revu account shows a plan (Max/trial); Plan Unassigned disables editing (VALENCIA-015).
2. Enable Preferences > Admin > MCP and restart the AI client (VALENCIA-015).
3. Test on copies: page count, markup list, add FreeText, named destination and link, save and reread with pypdf (VALENCIA-015).
4. Run native OCR on image-only program output to make values searchable (VALENCIA-015).
Gotchas:
- Installer needs admin approval at the PC; plan activation is a separate step (VALENCIA-015, claude session).
- Compare Documents did not flag an unflattened markup; treat compare as a smoke test only (VALENCIA-015, claude session).
Source cards: VALENCIA-015
