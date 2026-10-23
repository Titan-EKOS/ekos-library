# Add-on: FEMA work-map zones from FLO-2D results (scripted-exhibit-sheets)

Load when Zone AE/AO delineations and BFE contours are needed for a CLOMR/LOMR work map from a FLO-2D model.
Exhibit content rules: drainage-report-exhibit-standards `addons/fema.md`. Package and submittal: fema-clomr-lomr.

## Steps
1. Get the depth-to-zone table of the **effective study for the reach**. The source case used: < 1 ft X;
   1.0-1.5 AO(1); 1.5-2.5 AO(2); 2.5-3.0 AO(3); > 3 ft AE (`exhibit_kit.ZONE_TABLE_SOURCE_CASE`). Never reuse a table
   across studies without checking it against the effective FIS. (STARVALLEY-009)
2. Map max depth (DEPTH.OUT, gridded on the model cell size, section C of the skill) through the table with
   `exhibit_kit.depth_to_zone(depth, table, ae_mask)`. Continuous bounds, upper bound exclusive (D32).
3. Build `ae_mask` and assign Zone AE to: channel cells, the connected inundated corridor along each 1D channel
   segment, and detention basins. (STARVALLEY-009)
4. Generate 1-ft BFE contours inside AE from MAXWSELEV (WSE taken directly from MAXWSELEV.OUT, never depth plus a
   different terrain). (STARVALLEY-009, TANGERINE-008)
5. Polygonize zones (dissolve by zone label) and write effective, existing and proposed zone shapefiles with an
   acreage table per zone. (STARVALLEY-009)
6. Map the vector delineations (and BFE lines) on the work map, not depth rasters. (STARVALLEY-009)
7. Include the zone shapefiles in the submittal GIS package and confirm they match the work map (same zone labels,
   same acreage). (STARVALLEY-009)
8. State the vertical datum, the effective study used for the table and the model plan on the sheet.

## Gotchas
- The reviewer rejected depth rasters presented as the work map and flagged the channel and over-3-ft basins still
  shown as Zone A/AO. (STARVALLEY-009)
- Zone shapefiles built months earlier were left out of the upload; package QC must check they exist.
  (STARVALLEY-009)
- FEMA Region IX / Pima County RFCD: the depth-to-zone table comes from the effective study for the reach.
  (STARVALLEY-009)

## QC checks
- `get_qc_rules('fema')`, `get_qc_rules('flo2d')`.
- Work map shows vector zones; channels, connected corridors and basins > 3 ft are AE; BFE contours at 1 ft.
- Zone table source cited; zone shapefiles present in the GIS package and matching the work map acreage table.
