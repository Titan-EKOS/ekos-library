# hechms-headless add-on: Caltrans / California (HDM 819.2, CN calibration)

Load when: an HMS model is built for a California site or work in Caltrans R/W. Report criteria: drainage-report-build
`addons/caltrans-california.md`.

## Method
- HDM 819.2: Rational to about 320 ac; above that HEC-HMS with NRCS CN loss, NRCS unit hydrograph and the 24-hr NOAA Atlas 14
  storm; Tc floor 5 min (CALFIRE-006).
- Independent check: USGS SIR 2012-5113 regional regression (HDM Table 819.2C). Check the regression region name by hand;
  keyword search returned only 4 hits on region terms (CALFIRE-002, CALFIRE-006).
- FIS Q100 governs at FEMA-mapped crossings (CALFIRE-006).

## CN calibration on HSG C/D foothill basins
1. Reconcile the DEM watershed area with the FIS area before calibrating (CALFIRE-007).
2. Compare uncalibrated Q100 with FIS and regression (CALFIRE-007).
3. Sweep a uniform CN reduction (6 to 14 points); pick the reduction that matches FIS Q100 (CALFIRE-007).
4. Check the full frequency curve after calibration (CALFIRE-007).
5. Keep the uncalibrated 100-yr as a sensitivity run through the hydraulics (culvert and 2D) (CALFIRE-007).
6. Put the calibration and its limits in the QC open-items document for District Hydraulics confirmation (CALFIRE-007).

## Gotchas
- Uncalibrated Q100 was about 1.9x FIS on the 9 sq mi creek and 2.5x regression on the 0.79 sq mi tributary (CALFIRE-007).
- Calibrated 2-yr fell below regression (18 vs 27 cfs) (CALFIRE-007).
- A 14-point CN cut is large; report it plainly (CALFIRE-007).
- DEM watershed for the creek differed from the FIS area (CALFIRE-007).

## Open questions to confirm
- Which method District Hydraulics accepts for mid-size watersheds (HMS vs regression); not written (CALFIRE-006).
- District acceptance of the CN calibration magnitude (CALFIRE-007).
