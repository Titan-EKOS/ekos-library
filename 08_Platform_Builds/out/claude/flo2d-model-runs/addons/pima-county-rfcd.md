# flo2d-model-runs add-on: Pima County RFCD

Load for FLO-2D work reviewed by Pima County Regional Flood Control District (unincorporated Pima County,
and as floodplain administrator for other jurisdictions).

## Rules
1. Nested grids follow TECH-033 Amendment A: upstream (UPPER) outflow = downstream (LOWER) inflow. Use the
   skill's Step 6 handoff and inflow fix; report the volume check (UPPER outflow volume = LOWER inflow volume)
   in the model basis (SAH-002).
2. Acceptance of a 2D approach (FLO-2D or HEC-RAS 2D) where the manual expects 1D is an approval item; raise
   it at the methodology meeting and log it (RKN-007).
3. Development effects for FLO-2D (ARF, IRAINBUILDING, n, CN) per the skill's Step 5; RFCD reviews these with
   FEMA on CLOMR work (STARVALLEY-013).
4. Hydrographs from PC-Hydro enter INFLOW.DAT at the calc interval; follow pchydro-hydrographs for the native
   vs peak-adjusted series (decision D19) and state which series the model uses.
5. Default CRS NAD83(HARN) Arizona Central, intl ft, EPSG:2868 (decision D55, default, to confirm); record the
   realization in the data log.

## QC
- run `get_qc_rules('pima-rfcd')`.
