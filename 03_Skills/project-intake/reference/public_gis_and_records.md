# Public GIS harvest, record plans and reference documents

## A. Public GIS and hydrology data (DSO-C03)
For sites with no client CAD/GIS or no local county manual, and for effective FEMA linework.
Run `scripts/rest_harvest.py` with a layer config (one entry per layer; page 500; outFields *). On EKOS-LOCAL jobs the
local worker runs it from the saved config so the pull is replayable (D14).

Layer set (pick what applies):
- FEMA NFHL: flood hazard zones, flood hazard boundaries, FIRM panels, LOMRs, cross sections, BFE lines, profile
  baselines.
- USGS NHD flowlines, waterbodies, areas; WBD HUC12; NWI wetlands.
- Census places and counties; TIGER roads; USA Structures footprints.
- State DOT highway lines, tenth postmiles, bridges, AADT, intersections (California: Caltrans add-on).
- County parcels and zoning; state dam inundation boundaries.

Hydrology inputs for sites with no local manual (Arizona jurisdictions with a county manual, e.g. Pima County RFCD
PC-Hydro, use the manual's rainfall and soils sources instead):
- Rainfall: NOAA PFDS point query, depth and intensity (PDS, mean); save the raw text and a DDF CSV; build 24-hr nested
  hyetographs at 5-min. PFDS returns JavaScript text (`result = values; quantiles = [...]`), not JSON: parse the arrays.
- Soils: SSURGO via Soil Data Access, map units with HSG; percent HSG per watershed; state the rule for dual groups
  (B/D, C/D) and Not rated units in the assumption log before CN assignment.
- Land cover: NLCD 2021 clip by WCS/GeoTIFF. Gages: NWIS site list within the HUC.
- FEMA: save a native CAD reference drawing, RAS Mapper layers and render overlays from the same NFHL download; list
  LOMRs and compare to the hydraulic baseline before any regulatory statement.
Keep the GeoPackage as the master per theme (shapefiles truncate field names over 10 characters). Display-clipped
polygons never feed hydraulic encroachment logic. An updated local model plus mapped lines is a screening, not a
duplicate-effective model.

## B. Record plans and field books (DSO-C06)
1. Search the public catalog with description queries (words) and plan queries (plan ID); act only on observed
   action links on the page.
2. Field books: cookie session and CSRF token; follow next-page links with a page budget; shortlist matching file
   names before choosing.
3. Save every download with SHA-256; check PDF/TIFF magic bytes; keep receipts (query, URL, time).
4. OCR with Tesseract per page with orientation detection; make a rotated derivative and keep the original.
5. Read OCR text with explicit strict utf-8 on Windows.
6. Quote text deterministically from the original by source-offset excerpt IDs; verify the page image before using
   any number.
7. Accept a crossing detail only after it is spatially anchored (plan titles naming roads do not geolocate a structure).

## C. Reference documents and standards (DSO-C09, DSO-C13 step 8)
1. Download current jurisdiction standards into `01_Reference\Agency\Standards_<YYYYMMDD>\` with a register: title,
   edition date, adoption, URL, current or historical, project applicability (unknown stays unknown).
2. Copy reference folders without altering the source; compare SHA-256 before marking verified; keep original names
   and paths. Inventory executables but never run them.
3. Extract PDFs to page-aware JSON with page provenance; record PDF and artifact SHA-256. OCR only zero-text or
   low-text PDFs, into separate derived files. Leave encrypted PDFs pending; do not bypass protection. Diagnose
   timeouts individually before longer retries. Judge success by exit code and output artifact, not stdout text.
4. Human decisions go in a separate sheet; never approve numbers from OCR alone.
5. Retrieval index (local RAG) for these documents is built by `local-model-gateway`: chunk by tokenizer length,
   fingerprint the embedding profile, versioned collections, retrieval metrics (hit@1, hit@5, MRR) before any
   generated answer, citations mapped to chunk IDs, abstention when unanswerable.
