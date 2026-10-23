# drainage-report-build add-on: Placer County CA (East Placer / Lake Tahoe Basin / TRPA)

Load when: the site is in Placer County CA, especially East Placer within the Lake Tahoe Basin (TRPA) or above 5,000 ft
near the Sierra crest. Related skills: `swmm-ssa-storm-drain` (hydrograph models), `groundwater-reinfiltration-sizing`.
QC tag: `placer`.

## Governing manuals (confirm current edition)
- Placer County Stormwater Management Manual: Ch. V hydrology (Sec. V.E.2 Small Watershed, V.E.3 hydrograph methods,
  Table 5-A / 5-A-1, Fig. 5-3, Table 5-3, App. V-B), Ch. VI storm drain (HOMEWOOD-001, -002, -011).
- East Placer Storm Water Quality / Stormwater Management Manual (2024) and the East Placer SWQP template, not the West
  Placer manual (HOMEWOOD-013).
- TRPA BMP Handbook (4.1-d infiltration sizing) (HOMEWOOD-008).
- Project master plan criteria where adopted (50-yr 1-hr post <= pre) (HOMEWOOD-008).

## Methods
- Method scope: Small Watershed (Qp = q x A - Ap x Fi) for peaks used in inlet and upper-system pipe sizing only; any
  storage, peak control or HGL uses a hydrograph method (kinematic wave basis). Never mix a peak-only worksheet with a model
  generating unrelated runoff (HOMEWOOD-001, HOMEWOOD-012).
- Crest side: run every case with both West and East of crest Table 5-A and Fig. 5-3 values; compare with NOAA Atlas 14 at
  the site; get County confirmation of the basis in writing; state it (HOMEWOOD-011).
- Small Watershed inputs per area: area, % impervious (as a fraction in formulas), overland segments (L, S, n), collector
  segments (L, S, n, Z, contributing area). Overland time by Eq. 5-3; gutter, pipe, swale and pavement by Eq. 5-4; Fi by
  Eq. 5-5 at site elevation with Table 5-3 rates, same framework pre and post; unit peak from Fig. 5-3 for tr and elevation;
  50-yr by log-frequency interpolation between 25 and 100-yr; Ap = A x (1 - imp) (HOMEWOOD-001).
- Report the unrouted sum of area peaks vs existing; state that the method cannot credit storage (HOMEWOOD-001).
- Digitize Fig. 5-3 once (curves linear 5,000 ft to crest and crest to 5,000E), check against a known hand pick, reuse
  (HOMEWOOD-001).
- Nested design storm for hydrograph models: Table 5-A-1 depth at 5,000 ft plus change per 1,000 ft for the crest side;
  depths at site elevation 5 min to 24 hr; log-log interpolation of cumulative depth at 1-min steps (required when
  tr < 10 min); nest incremental depths with the maximum at mid-storm alternating after / before (App. V-B); 24-hr 2 / 10 /
  100-yr and a 1-hr storm for a 50-yr 1-hr criterion; write as VOLUME series (HOMEWOOD-002).
- The runoff method must also match the County method, not only the storm (HOMEWOOD-002).
- SWMM / SSA as the primary hydrograph model is allowed here (D26): calibrate subcatchment width to Small Watershed target
  peaks per storm (Horton f0 = fc = Table 5-3 rate, no depression storage), pre-condition catchments calibrated separately;
  dynamic wave routing whenever HGL is reported (HOMEWOOD-003, HOMEWOOD-004, HOMEWOOD-006).
- WQ event: scale the 2-yr shape to the 85th percentile depth; route it with and without infiltration and report volume
  leaving untreated (HOMEWOOD-002, HOMEWOOD-007).
- Keep a live-formula workbook (Basis, Fig 5-3 digitized, Post, Pre, Pre vs Post) in 20_Working; independent checks stay
  in 40_QC (D30) (HOMEWOOD-001).
- Storm drain tailwater: get receiving rim, invert and HGL; run fixed tailwater and free outfall; state the same boundary in
  model and memo (HOMEWOOD-010).

## Criteria
- Storm drain: 10-yr design (Ch. VI); HGL at least 0.5 ft below rim / grate (project criterion also applied to the 50-yr
  1-hr) (HOMEWOOD-006, HOMEWOOD-010).
- Design events used: 2-yr 24-hr and 50-yr 1-hr for peak control; 10 / 25 / 100-yr Small Watershed targets (HOMEWOOD-003,
  HOMEWOOD-007).
- Water quality: retain / infiltrate the 85th percentile WQV (East Placer Sec. 4.3.4). WQ depth flagged for confirmation
  (D25): 1.2 in rainfall at 6,000-6,500 ft vs 0.9 in unit WQV at about 6,300 ft. In SWQP Form 3-1 enter the actual site
  elevation; back-check WQV = impervious area x runoff coefficient x unit depth; never equate the 85th percentile 24-hr
  depth with a 50-yr 1-hr depth (HOMEWOOD-002, HOMEWOOD-008).
- Hydromodification: projects over 1 ac new impervious, post <= pre 2-yr (Sec. 4.4) (HOMEWOOD-008).
- SWQP Forms 4-2 / 4-3: full site area checked against survey acreage; 2-yr rainfall at Tt, not a 1-hr WQ depth; YES / NO
  answer agrees with computed post vs pre; provided volume >= required, or routed results per Sec. 4.4 (HOMEWOOD-014).
- TRPA 4.1-d: subsurface infiltration retains at least the 20-yr 1-hr volume from tributary impervious area; prefabricated
  chambers 80-90% voids vs 40% gravel (HOMEWOOD-008).
- Groundwater separation (D25): BMP bottom at least 5 ft above SHGW (East Placer Sec. 3.1.1) or move, redesign or seek a
  variance; document SHGW at each BMP footprint; check geotech limits on infiltrating above lowest foundations
  (HOMEWOOD-009).
- CMP / chamber depth check under pavement: FG to SHGW >= pipe diameter + 2 in bedding + 12 in cover to the bottom of the
  structural section + structural section + required separation (cover is measured to the bottom of the structural
  section) (HOMEWOOD-017).
- Untested infiltration (D23): field rate at BMP depth; until tested use half the NRCS rate with a 0 in/hr sensitivity
  (HOMEWOOD-009).
- WQV <= storage below the lowest outlet invert as drawn; fix by raising the outlet invert or adding a weir plate / riser,
  then rerun WQ and design events (HOMEWOOD-007).
- Storage must be shown with a hydrograph method (TANGERINE-015 cross-ref, HOMEWOOD-012).
- Groundwater displacement from cuts: reinfiltration with overflow path (geotech requires overflow) (HOMEWOOD-016)
  (`groundwater-reinfiltration-sizing`).
- One source for DMA impervious areas across memo, exhibit and SWQP template (HOMEWOOD-008).

## Review expectations
- Manual names: East Placer throughout (HOMEWOOD-013).
- Gallery sizing vs WQV and outlet invert check shown on the exhibit (HOMEWOOD-018).
- Exhibit headers and sheet labels match the event and elevation used (HOMEWOOD-001).

## Gotchas specific to this add-on
- % impervious typed as 7 not 0.07 made the infiltration term add flow; existing 10-yr went 7.87 to 4.32 cfs and the pre /
  post conclusion reversed (HOMEWOOD-001).
- Eq. 5-3 on every collector overstated tr (pipe 2.99 vs 0.58 min; swale 21.1 vs 8.7 min) (HOMEWOOD-001).
- Post pervious set to 0 in/hr while existing used 0.09 in/hr (HOMEWOOD-001).
- Site drains east of crest but Atlas 14 matched West values; East results about 35% lower (HOMEWOOD-011).
- WQ findings are volume-based and do not depend on crest side (HOMEWOOD-011).
- Two incompatible methods mixed for weeks gave model peaks 4-7 times lower than worksheet peaks (HOMEWOOD-012).
- SWQP template at 6,600 ft gave 1.0 in unit WQV; site at about 6,300 ft gives 0.9 in; memo claimed 1.3 in (HOMEWOOD-008).
- Memo assumed 2 ft separation with SHGW at galleries undocumented (HOMEWOOD-009).
- Form 4-2 used 111,270 sf for a 139,392 sf site and answered YES with post 68.8 vs pre 31.3 cfs (HOMEWOOD-014).

## Open questions to confirm
- County written confirmation of the West vs East of crest basis (HOMEWOOD-011).
- WQ depth from the East Placer manual: 1.2 in rainfall vs 0.9 in unit WQV (D25) (HOMEWOOD-008).
- 5 ft vs 2 ft separation for galleries and the groundwater reinfiltration CMP (D25) (HOMEWOOD-009).
- Half-NRCS untested infiltration rate acceptance with the County (D23).
- Small Watershed and nested-storm tools (sw.py, storms.py from HJR-C15) are not yet in the library; add as add-on scripts
  when recovered from the project record.
