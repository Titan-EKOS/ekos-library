# hechms-headless add-on: Pima County RFCD (TECH-018)

Load when: an HMS model is built for Pima County RFCD review, or for City of Tucson, Town of Marana or Town of Sahuarita
work where the County hydrology method governs watersheds over 1 sq mi. Report criteria: drainage-report-build
`addons/pima-county-rfcd.md`.

## Method (TECH-018)
- Applies to watershed systems over 1 sq mi; under 1 sq mi use PC-Hydro (pchydro-hydrographs) (RKN-006, RKN-017).
- Loss: SCS CN from the PC-Hydro ADOT tables (HSG A desert brush treated as B, 20% density = CN 83, per the PC-Hydro User
  Guide table where 2D rain-on-grid shares the parameters) (RKN-006, HYD-C11 ELTORO-004).
- Transform: SCS unit hydrograph, lag = 0.6 Tc with TR-55 segmented Tc (RKN-006).
- Routing: Modified Puls from normal-depth storage-outflow (RKN-006).
- Rainfall: NOAA Atlas 14 upper 90% at the system centroid, areal reduction over 1 sq mi (RKN-006, TECH-010).
- Critical storm = max of 3-hr and 24-hr results at each CP (RKN-006).
- PC-Hydro hydrographs for subbasins under 1 sq mi may enter HMS as Source elements on the same junction / reach network
  (SAH-007).
- Inflows from PC-Hydro DSS through GAGE_FLOW sources (HYD-C19).

## Review expectations
- Closed depressions (mine pits, stock ponds, tailings) treated as non-contributing only with agency agreement at the
  methodology meeting; bracket both ways (SAH-016).
- Older studies on NOAA Atlas 2 / 1979 county manual are cross-check only (ELTORO-007).

## Open questions to confirm
- Current TECH-018 edition and whether RFCD accepts 4.13 projects without comment (D01 states 4.13 in the report).
- Areal reduction method and table edition expected by RFCD for the specific basin size.
