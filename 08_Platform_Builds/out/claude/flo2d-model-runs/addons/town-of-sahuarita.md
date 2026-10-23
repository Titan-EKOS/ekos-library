# flo2d-model-runs add-on: Town of Sahuarita

Load for FLO-2D road-drainage screening (skill Step 12) on Town of Sahuarita roads.

## Rules
1. Road criteria used in the screening tables (SAH-011):
   - Town of Sahuarita: 12 in all-weather access;
   - Pima County Roadway Design Manual: 1 ft maximum depth in the paved section.
   Confirm the governing criterion for each road with the Town before reporting.
2. Report per trial: max lane depth, 500-ft reaches over 1 ft and over 0.5 ft, buildings with depth > 0.5 ft
   and with increase > 0.1 ft (increase threshold from the governing agency per decision D29).
3. Test both the 3-hr and 24-hr design storms on the recommended layout before it is reported (SAH-011).

## QC
- run `get_qc_rules('sahuarita')`.
