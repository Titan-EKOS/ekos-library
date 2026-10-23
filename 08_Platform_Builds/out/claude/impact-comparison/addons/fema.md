# impact-comparison add-on: FEMA (44 CFR 65.12, Region IX)

Load for CLOMR / LOMR existing vs proposed comparisons and any BFE-rise statement. Package build:
fema-clomr-lomr. Source case: FLO-2D, FEMA Region IX with Pima County RFCD (STARVALLEY-008).

## Rules
1. Both models share the same grid cell by cell (CADPTS identical) so differences are exact; run
   `shared_input_hashes.py` and keep its JSON in the package QC.
2. dWSE = proposed MAXWSELEV - existing MAXWSELEV, from MAXWSELEV.OUT and DEPTH.OUT.
3. Evaluate rises where the cell is in the SFHA (max depth >= 1.0 ft) in both conditions; report any-depth
   counts separately:
   `<PY> flo2d_cell_compare.py --base EX=<ex> --scenario PR=<pr> --threshold <ft> --threshold-source "44 CFR 65.12 / <FEMA or community letter>" --fema --list-above 1.00 --outdir <folder>`.
   The threshold is the value stated by FEMA / the community for the project (decision D29).
4. Map new SFHA cells (>= 1 ft proposed, < 1 ft existing) and removed SFHA cells.
5. List every cell over 1.00 ft with ground change, depth change and location class: applicant land, inside
   approved grading, or channel prism (fill the `ownership_or_grading` column from the property and grading
   linework).
6. Write rasters, over-1-ft polygons, the summary JSON and an exhibit; quote report values only from these
   files.
7. For cells on other ownership: prepare alternatives, property-owner notices on the CLOMR template and the PE
   certification; JCO decides which path applies.
8. Duplicate-effective / corrected-effective / existing / proposed on one engine build (flo2d-model-runs
   `addons/fema.md`).

## Gotchas
- Extreme dWSE values at fill slopes and excavated basins come from ground change, not flood change; review before quoting min / max (STARVALLEY-008)
- A 34.6 ac over-1-ft cluster came from a placeholder flat surface in the proposed TOPO, not real grading (STARVALLEY-008)
- Property-boundary linework is needed to classify edge cells; request it early (STARVALLEY-008)

## QC
- run `get_qc_rules('fema')`.
- Every over-1-ft cell classified; notices / certification status recorded for other-ownership cells.
