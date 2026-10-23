# Add-on: Pima County RFCD exhibits (drainage-report-exhibit-standards)

Load for any Pima County Regional Flood Control District submittal. Report-level Pima rules live in
drainage-report-build `addons/pima-county-rfcd.md`.

## Rules
1. DS-305 workmap/exhibit standards govern content and symbology; sheet size stays 11x17 (scalable to 22x34) per D36.
2. Roadway reports: label curb and scupper outfalls with arrows and Q values; draw berms as thick colored lines with
   basic dimensions and raised-berm limits. (CAMPBELL-018)
3. Culverts: label both the design-plan Q and the calculated Q, with cells, size and type. (TANGERINE-022)
4. Difference maps: the increases-only display and class set in the core (Result maps, 4.7) came from Pima County
   RFCD review (CAMPBELL-016); use it unless the District reviewer asks for a different threshold, and cite that
   threshold (D29, D33).
5. Depth maps for Pima County and Town of Sahuarita local sites use the core "local" ramp (SAHPARK-006, D31).
6. CRS default: NAD83(HARN) Arizona Central, intl ft, EPSG:2868; state the realization in the datum callout and the
   data log; flag mixed realizations (D55, default, to confirm).

## Gotchas
- Outfall Q labels and berm dimensions were missing on roadway drainage maps and came back as redlines. (CAMPBELL-018)
- Difference classes were re-cut three times before the District-facing set was fixed. (CAMPBELL-016)

## QC
`get_qc_rules('pima-rfcd')` plus `get_qc_rules('exhibits')`.
