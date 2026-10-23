# Add-on: FEMA floodplain content on exhibits (drainage-report-exhibit-standards)

Load whenever an SFHA is present, a FIRM panel or FIRMette is included, NFHL layers are plotted, or a CLOMR/LOMR
work map is made. Package and submittal rules: fema-clomr-lomr; zone delineation from FLO-2D results:
scripted-exhibit-sheets `addons/fema.md`.

## Layers and fields
1. NFHL layer set: S_FLD_HAZ_AR (zones), S_BFE, S_XS, S_LOMR; clip each to the exhibit extent. (TANGERINE-008)
2. 0.2% chance area: filter on the actual ZONE_SUBTY text "0.2 PCT ANNUAL CHANCE FLOOD HAZARD"; test the subset is
   non-empty before rendering; if empty, state "none mapped" and drop the legend entry. (CALFIRE-017)
3. Credit source and pull date; state the effective date of the mapping on the exhibit and in the text.
   (SAHPARK-010, SILVERBELL-017)

## Status handling
4. Effective mapping only on project exhibits. A pending revision (preliminary FIRM or work map) goes in a separate
   labelled appendix item with its status; never shown as effective. (SAHPARK-010)
5. Flood context sheets built from supplied rasters stay labelled a source review draft (internal) until return
   period, condition and vertical datum are confirmed; record any CRS assumed from file names or world files on the
   sheet. (TANGERINE-008)

## FIRM panel / FIRMette
6. Tight box or sketched alignment labelled "this project", covering the whole project; a full panel only with the
   project marked tightly (D39). Include the current panel and any panels the project touches. (SAHPARK-010,
   VALENCIA-023)

## Work maps (CLOMR/LOMR)
7. Show vector zone delineations (AE, AO depths, X) and BFE contours on the work map, not depth rasters; channel cells
   and basins deeper than 3 ft are Zone AE. Delineation procedure: scripted-exhibit-sheets `addons/fema.md`.
   (STARVALLEY-009)
8. Zone shapefiles included in the submittal GIS package and matching the work map. (STARVALLEY-009)

## Gotchas
- GeoPandas warned the 0.2% subset was empty and the figure was issued anyway. (CALFIRE-017)
- Draft exhibits omitted the floodplain entirely; the FIRM appendix held only the current panel. (SAHPARK-010)
- The project box covered most of the panel. (SAHPARK-010)
- Reviewer rejected depth rasters presented as the work map and flagged channel and >3 ft basins still shown as
  Zone A/AO. (STARVALLEY-009)
- Zone shapefiles built months earlier were left out of the upload. (STARVALLEY-009)

## QC
`get_qc_rules('fema')` plus `get_qc_rules('exhibits')`.
