---
name: swmm-ssa-storm-drain
description: Build EPA SWMM 5.x hydrograph / storm drain models by script, calibrate subcatchment width to an agency peak method, hand them to Autodesk SSA, and report HGL, storage, peak control and tailwater cases; SWMM/SSA is the primary model only where the Placer County CA add-on allows it (decision D26) and an independent check elsewhere.
version: 1.0.0
status: active
function: hydraulics-model-run
jurisdiction: all (primary-model use - Placer County CA add-on; Arizona - independent check only)
tools_versions: "EPA SWMM 5.2.4 via swmm-toolkit; Autodesk SSA 2024.1 (SWMM 5.1 engine); Python 3.12 hydro env"
owner: JCO
replaces: "drainage-report-build v1 section 3 line 'EPA SWMM as an independent check only' (now scoped by D26)"
---
# SWMM / SSA Storm Drain

## When to use
- Storage, peak control or HGL must be shown with a hydrograph model while the agency peak method is
  rational-type (e.g. Placer County Small Watershed) - Placer County CA add-on.
- Scripted SWMM models must be handed to an engineer in Autodesk SSA.
- An independent check of a storm drain HGL or a detention routing in an Arizona jurisdiction, where
  PC-Hydro / HEC-HMS and the agency-accepted tools stay primary (decision D26).
- A storm drain ties into a public main or street structure and HGL freeboard is checked.

Role by jurisdiction (decision D26):
| Jurisdiction | SWMM / SSA role |
|---|---|
| Arizona (Pima County RFCD, City of Tucson, Marana, Sahuarita, others) | independent check only; file in 40_QC (decision D30) unless JCO decides otherwise |
| Placer County CA (and other jurisdictions whose add-on allows it) | primary hydrograph / HGL model, calibrated to the county peak method |

## Inputs
- Agency target peaks per drainage area and design storm (county method calc; for Placer see
  drainage-report-build `addons/placer-county-ca.md` and this skill's add-on).
- Agency infiltration rate table, site plan areas (impervious, pervious, roof), pipe / structure data from
  survey or plans, storage / gallery / trench geometry.
- Receiving structure rim, invert and HGL from the agency or as-builts.

Scripts (hydro env interpreter by full path, D11; `<PY>` = `"%HYDRO_PY%"` = `C:\EKOS\hydrology\.venv\Scripts\python.exe`, per
the path in the 08_Platform_Builds/ENVIRONMENTS.md):
- `scripts/swmm_width_calibrate.py` - log-space bisection of subcatchment width to target peaks; geometric mean;
  fit report.

## Steps

### 1. Targets
1. Compute target peaks per area for each design storm with the county method; record the method and table
   values used.
2. Calibrate pre-condition (existing) catchments separately with their own targets.

### 2. Runoff-only calibration models
1. One runoff-only .inp per storm: each subcatchment to an outfall; constant-rate infiltration (Horton
   f0 = fc = agency table rate, decay 0); no depression storage; REPORT_STEP 1 min or less.
2. `<PY> swmm_width_calibrate.py --sub <S> --case <runoff_10yr.inp> <Q10> --case <runoff_25yr.inp> <Q25>
   --case <runoff_100yr.inp> <Q100>`. It bisects width in log space (26 iterations default) per storm, takes
   the geometric mean of the storm widths, and reports the fit of that one width against every target
   (pass within 10 pct).
3. Report the fit in the memo (target vs modeled per storm). Plot a calibration figure.
4. Carry the calibrated widths unchanged into every routed scenario.
5. Do not try to close the gap by switching SSA hydrology methods (TR-55 / TR-20); width calibration is what
   matches the county peaks.

### 3. Routed models
1. Write .inp in SWMM 5.1 syntax (SSA imports 5.1), one file per scenario named
   `<code>-<side>-<run>-<storm>-<condition>`.
2. Keep routing Hydrodynamic. Set surcharge elevation and sag-inlet ponded area deliberately (otherwise SSA
   raises Warning 108 surcharge elevation below max depth, and Warning 139 zero ponded area on sag inlets).
3. Storage nodes: exfiltration rates from the agency / geotech basis; record the source.

### 4. Tailwater and receiving system
1. Get rim, invert and HGL of the receiving structure from the agency or as-builts.
2. Run a fixed-tailwater case and a free-outfall case; report both. The model and the memo state the same
   boundary.
3. Compare the assumed tailwater with the lowest onsite rims and gallery crowns before any site runoff arrives.
4. Compare proposed peaks with receiving storm drain capacity and HGL; explain why each discharge alternative
   (alley, street, storm drain, retention) was or was not used; coordinate connection feasibility with the
   site designer.
5. Verify report claims (e.g. impervious area removed) against the site plan.

### 5. SSA handoff
1. Import in SSA: File > Import > EPA SWMM v5.x. Save each scenario as .spf with its text report.
2. SSA does not transfer storage exfiltration: set storage-node exfiltration in Project Options and re-enter
   gallery / trench infiltration rates by hand. Recheck surcharge elevations and sag-inlet ponded areas.
3. Keep Hydrodynamic routing in SSA.

### 6. Compare and report
1. Parse the SSA .rpt (Node Depth Summary, Outfall Loading, Storage Node Summary, continuity) and the SWMM .rpt
   on identical inputs; compare HGL and outfall peaks.
2. SSA routing continuity omits exfiltrated volume; report continuity with exfiltration added back.
3. SSA uses the older SWMM 5.1 surcharge algorithm; where surcharged node depths differ, use the more
   conservative result and say which engine it came from.
4. HGL freeboard against the governing criterion at every structure (Placer: 0.5 ft below rim).
5. Native program output in the appendix (decision D38): SSA / SWMM report pages for the selected design.

## Jurisdiction add-ons
- `addons/placer-county-ca.md` (load with `get_skill("swmm-ssa-storm-drain", resource="addons/placer-county-ca.md")`):
  SWMM / SSA as primary, Small Watershed targets, Table 5-3 infiltration, 0.5 ft HGL freeboard, East Placer
  items.
- City of Tucson: justify retention vs discharge with receiving storm drain capacity and HGL; rules in
  drainage-report-build `addons/city-of-tucson.md` (TANGERINE-025).

## Gotchas
- Switching SSA hydrology between TR-55 and TR-20 never matched county peaks (50-yr 0.13 vs 0.90 cfs); calibration of width closes the gap (HOMEWOOD-003)
- Calibrate the pre-condition catchment separately with its own target (HOMEWOOD-003)
- SSA does not transfer storage exfiltration on import; peak-control and WQ runs were wrong until set by hand (HOMEWOOD-004)
- SSA routing continuity omits exfiltrated volume, so a run shows 19-48 pct continuity error equal to exfiltration; report it with exfiltration added back (HOMEWOOD-004)
- SSA uses the older SWMM 5.1 surcharge algorithm; surcharged nodes ran 0.3-2.1 ft higher than SWMM 5.2; use the more conservative result (HOMEWOOD-004)
- The original SSA export raised Warning 108 (surcharge elevation below max) and 139 (zero ponded area on sag inlets); set these deliberately (HOMEWOOD-004)
- Tailwater set 6 in below the receiving grate was only 0.52-0.55 ft below the lowest onsite rims, so the lower system failed the 0.5 ft criterion before site runoff arrived; free outfall passed (HOMEWOOD-010)
- The original model used a free outfall while the memo claimed tailwater; model and memo must state the same boundary (HOMEWOOD-010)
- A draft asserted retention without checking the storm drain and claimed impervious removal the plan did not show (TANGERINE-025)
- The .rpt Subcatchment Runoff Summary rounds small peaks to 0.01 cfs; the calibration script reads the binary output instead (build note, 2026-10-22)

## QC checks
- Pull: `get_qc_rules('storm-drain')`; Placer: `get_qc_rules('placer')`.
- width_calibration.json pass (each storm within 10 pct with the single geometric-mean width); pre and post
  calibrated separately.
- Exfiltration re-entered in SSA; continuity reported with exfiltration added back.
- Fixed-tailwater and free-outfall cases both run; memo boundary matches the model.
- HGL freeboard checked at every structure; more conservative engine result used where they differ.
- Arizona jobs: SWMM files and results in 40_QC only, not in the deliverable (D26, D30).

## Change log
- 1.0.0 2026-10-22: built from clusters HYD-C22 and HYD-C23; decisions D26, D30, D38. Width calibration script
  tested against the SWMM 5.2.4 engine (swmm-toolkit) on a synthetic catchment.
