# HEC-HMS 4.13 text-file patterns

Status: working notes. Each block below must be checked against a file saved by HEC-HMS 4.13 on EKOS before a script
relies on it. When a block is confirmed, replace it with the native text and mark it "confirmed YYYYMMDD". Never infer a
keyword that is not in a native save; save the component once in the GUI and copy it (same rule as HY-8 templates, D10).

## Project layout (one folder per model)
```
<model>_413\
  <model>.hms          project file: lists basin, met, control, gage, run components
  <basin>.basin        subbasins, reaches, junctions, reservoirs, sources, sinks
  <met>.met            meteorology component
  <control>.control    start / end / time interval
  <model>.gage         gage list (precipitation, flow) with DSS paths
  <model>.run          run list: basin + met + control per run
  <model>.pdata        paired data (storage-outflow, elevation-storage, ratings) -> DSS
  <model>.dss          project DSS (paired data and results)
  results\RUN_<run>.results   results XML written by compute
  <run>.log            run log (ERROR / WARNING / NOTE lines)
```
Every component block starts with `<Type>: <Name>` and ends with `End:`; attribute lines are indented five spaces in
native saves. Keep CRLF line endings.

## Zero meteorology for gage-flow routing (D01 default)
Component name must be `No Precipitation`; evapotranspiration `No Evapotranspiration`. A component named `None` gave
Undefined controller errors (EKOS-LOCAL-009). Expected shape (to confirm against native save):
```
Meteorology: No Precipitation
     Unit System: English
     Precipitation Method: None
     Evapotranspiration Method: No Evapotranspiration
     Use Basin Model: <basin name>
End:
```

## External inflow source (GAGE_FLOW)
Source element in the .basin with the flow method set to the gage, and a Flow gage in the .gage file whose DSS pathname
matches the external record exactly (A/B/C/D/E/F parts). After any repoint, re-select the pathname (pchydro-hydrographs
reference/dss_formats.md). DSS record: INST-VAL, CFS, E part `1Minute` for PC-Hydro series.

## Reservoir (relative datum)
- Subtract one documented basin-bottom elevation from every elevation (initial pool, outlet inverts, overflow top,
  elevation-storage x values). Record the offset in the parameter table header and in the run log.
- Circular outlet keys seen in native files: Diameter, Chart, Scale, End Conduit (copy the full block from a native save).
- Overflow (weir) keys: coefficient, top length, top elevation.
- Initial condition below the first storage table elevation causes an initial-pool error; check after rounding.

## Specified Average met model (alternate, document when used)
Subbasin lines reference the precipitation gage with Use Basin Model lines. Used by the v1 skill; keep only where an
inherited model already uses it.

## Results XML
`check_hms_results.py` reads any element with a `name` attribute holding Statistic* children that carry a type (or name)
and a value. Statistic names used in reports: Outflow Maximum, Outflow Volume, Excess (precipitation excess volume).
Confirm the names on the first run of each new HMS build.
