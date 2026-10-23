# swmm-ssa-storm-drain add-on: Placer County CA (East Placer / Lake Tahoe Basin / TRPA)

Load for Placer County projects. Hydrology rules (Small Watershed method, crest side, nested storm) live in
drainage-report-build `addons/placer-county-ca.md`; this add-on covers the SWMM / SSA model.

## Rules
1. Primary model allowed (decision D26): SWMM, handed to SSA, is the hydrograph / HGL model for storage, peak
   control, water quality volume and freeboard. The Small Watershed method (Stormwater Management Manual Ch. V)
   gives peaks for inlet and upper-system sizing only and cannot credit storage; any storage, peak control or
   HGL uses the hydrograph model (HOMEWOOD-003, HJR-C15).
2. Calibration targets: Small Watershed peaks for the 10-, 25- and 100-yr events per area, on the crest side
   confirmed in writing by the County. Infiltration: Table 5-3 rates at site elevation as constant-rate Horton
   (f0 = fc), the same framework pre and post. Calibrate pre-condition separately. Achieved fits on the source
   job: +/-4 pct and +/-8 pct (HOMEWOOD-003, HOMEWOOD-004).
3. Rainfall: nested county design storm at 1-min steps (required when tr < 10 min), written as a VOLUME series;
   24-hr 2/10/100-yr and a 1-hr storm where a 50-yr 1-hr criterion applies (HOMEWOOD-002).
4. Storm drain: 10-yr design; HGL at least 0.5 ft below rim / grate (also applied to the 50-yr 1-hr where the
   project criterion calls for it). Run fixed-tailwater and free-outfall cases (HOMEWOOD-010).
5. Infiltration BMPs in the model: field rate at BMP depth; until tested use half the NRCS rate with a 0 in/hr
   sensitivity run (decision D23, to confirm with the County). Re-enter exfiltration in SSA by hand.
6. BMP bottoms at least 5 ft above seasonal high groundwater (East Placer Sec. 3.1.1, decision D25); flag any
   gallery that does not meet it.
7. Water quality depth: flag for confirmation from the East Placer manual (1.2 in rainfall vs 0.9 in unit WQV;
   decision D25). Do not equate the 85th percentile depth with a 50-yr 1-hr depth.
8. TRPA: subsurface infiltration sized to retain at least the 20-yr 1-hr volume from tributary impervious area
   (TRPA BMP Handbook 4.1-d); chamber voids 80-90 pct vs gravel 40 pct.
9. Cite the East Placer manual and SWQP template, never West Placer (HOMEWOOD-013).

## Gotchas
- TR-55 CN runoff on a 1-hr storm does not reproduce county peaks; the runoff method must match, not only the storm (HOMEWOOD-002)
- Two incompatible methods were mixed for weeks; model peaks were 4-7 times lower than worksheet peaks (HOMEWOOD-012)
- Tailwater 6 in below the receiving grate failed the 0.5 ft criterion before site runoff; free outfall passed; report both (HOMEWOOD-010)

## QC
- run `get_qc_rules('placer')` and `get_qc_rules('storm-drain')`.
