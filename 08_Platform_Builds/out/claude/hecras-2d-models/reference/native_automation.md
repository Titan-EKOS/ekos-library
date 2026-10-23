# HEC-RAS 6.6 native automation reference (HYD-C10)

Use when creating terrain, geometry, 2D mesh, 1D sections, culverts, roughness associations or plans without
the GUI. Every item below came from a failed or slow attempt; tags give the source card.

## Ground rules
1. Copy the project to a new work folder; never edit source plans. Run COM / CLI only on isolated copies and
   always quit the controller (`QuitRas`).
2. Write .prj, .g##, .p##, .u##, .rasmap with CRLF line endings. LF files are read as empty: RAS created a
   default g01/p01 and started a steady run (CAMPBELL-004).
3. Keep project units explicit and record every conversion.
4. Check the RasMapperLib command inventory before scripting; several commands (GenerateMesh,
   SetGeometryAssociation XMLSave) are not implemented (SILVERBELL-006).
5. PowerShell script execution is disabled on EKOS. Exact CLI arguments came from passive .NET metadata
   (dnfile, dncil), with no policy bypass (EKOS-LOCAL-010; decision D12).

## HDF edits (h5py)
- String attributes: delete and recreate. `attrs.modify` keeps the old fixed length and truncates paths and
  names. A truncated raster path gave "terrain does not cover the 2D Flow Area"; a truncated flow-area name
  ("Perimete") made table generation build an empty mesh (CAMPBELL-004).
- New datasets: chunked and gzip compressed like native ones. Contiguous datasets gave
  "H5Pget_chunk not a chunked storage layout" (CAMPBELL-004).
- Never read an HDF RAS is writing (*.tmp.hdf); a read during a write caused a write failure and the mesh was
  discarded and rebuilt (SILVERBELL-005).
- HDF-only roughness patches do not persist; use the native association (SILVERBELL-005).

## Terrain
- RasProcess CreateTerrain on the source grid (no resample), explicit ESRI projection and units; read back
  every pixel. It writes stderr warnings but completes; judge by the terrain HDF (exists, extent, dataset
  count), not the warning stream (RKN-007, SAH-010).
- RasMapperLib route: initialize native GDAL, use a console progress display, pass NaN for the unused
  tile-write parameter, compute raster statistics and then overviews before import. Eight helper builds over
  about 30 min returned "No target dataset specified" until the NaN and stats/overview order were fixed
  (SILVERBELL-006).
- Place rasters in the project Terrain folder (hard link if needed); absolute raster paths in the terrain HDF
  are not resolved.

## Geometry and mesh
- `CreateGeometry GeometryFilename=... UnitSystem=...`, then GenerateMesh with the perimeter shapefile and
  cell size, then `CompleteGeometry GeomFilename=... RasMapFilename=...`. Note the key names differ:
  CreateGeometry uses GeometryFilename, CompleteGeometry uses GeomFilename (EKOS-LOCAL-010).
- Count only the first `Cell Count` polygons as real cells; the rest are ghost centers. Check no gaps or overlaps.
- CompleteGeometry may warn "Geometry/Structures not found"; do not add fake structures to silence it
  (EKOS-LOCAL-010).

## 1D blocks and culverts
- Station-elevation in strict 8-character fixed width with Decimal values; read the native HDF back for every
  ordinate, bank, length and roughness.
- Culvert names longer than 12 ASCII bytes are silently truncated in the HDF; reject before running
  (EKOS-LOCAL-010).

## Roughness
- Associate through the native RasProcess geometry association (default NoData n; channel polygons first;
  first polygon wins).

## Run through COM / RasUnsteady
- COM preprocess, confirm property tables recomputed, set the core count in the tmp.hdf (COM may reset it to
  automatic; verify the native setting), launch RasUnsteady and check stdout (CAMPBELL-004).
- Command-line runs gave no output within 90 s on one attempt; the COM fallback worked for 1D (EKOS-LOCAL-010).
  Launch order for production: decision D05 (see SKILL.md Step 10 and `scripts/ras_headless.py`).
- Discover outputs with Output_Variables / Output_GetNodes; treat 3.4e38 as unavailable.
- pywin32 GetTypeAttr function count is index 6; index 8 gave a false empty output inventory (EKOS-LOCAL-010).

## Prove the change
- Diff new geometry tables against the source (cell centers, faces, structures, n) to prove only intended
  changes.
- Synthetic reach and culvert tests passing is not a project result; about 25 RAS tasks with 4 failures never
  reached the project 1D/2D model (EKOS-LOCAL-010).
