# DSS Formats and Gotchas (RAS / HMS)

## Which series goes into DSS (D19)
- The **peak-adjusted routing copy** (`hydrographs_to_xlsx.py --adjusted-csv`) is the series written
  to DSS for HEC-RAS, HEC-HMS or FLO-2D inflow. Column names carry the `_ADJ` suffix so the DSS
  B-part shows it is the adjusted copy.
- The **native export** stays unchanged as the record copy and goes in the report appendix.
- Added volume from the peak adjustment and from tail closure is logged on the workbook
  `Adjustment_Log` and `Peaks` sheets; quote it in the hydrology QC note.

## Version
- Only **DSS-7** can be written from the container (pydsstools on Linux cannot write v6).
  HEC-RAS 6.6 and HEC-HMS 4.13 read v7 natively.

## Record settings (non-negotiable)
- **data_type = `INST-VAL`.** If left INVALID or lowercase, **HEC-HMS reads the series as all
  zeros**; this was the root cause of a multi-hour gage-DSS debug on a prior project. Always INST-VAL.
- **units = `CFS`.**
- **E-part = interval string** matching the data step. Use `1Minute` for 1-min PC-Hydro output.
  (The older `1MIN` also works on write; DSS-7 stores it canonically. In HMS, after repointing a gage
  you must **re-select the pathname** so it picks up the correct E-part.)
- Start datetime is arbitrary for design storms (`01JAN2000 0000` default). DSS stores 1-minute regular
  series in **per-day blocks**, so a record may appear under two D-parts (e.g. `31Dec1999` and
  `01Jan2000`); RAS/HMS read across blocks by the simulation window. This is normal, not data loss.

## Pathname structure (built by `build_dss.py`)
- **RAS:** `//<SERIES>/FLOW//<Epart>/<Fpart>/` (A-part blank).
- **HMS:** `/<Apart>/<SERIES>/FLOW//<Epart>/<Fpart>/` (A-part = project code or run label).
- `<SERIES>` is the CSV column header (e.g. `CP-101_100yr_ADJ`). Name columns so the pathnames
  describe themselves.

## Round-trip check (required before any model uses the file)
1. Reopen the DSS file (HEC-DSSVue on EKOS, or pydsstools `read_ts` in the container).
2. For every record compare to the routing CSV: ordinate count, every ordinate (0.001 cfs),
   interval (1Minute), units (CFS), type (INST-VAL), integrated volume (ac-ft).
3. Record pass/fail per record in the hydrology QC note. A failed record is rewritten, never
   hand-patched in DSSVue.

## RAS: DSS BC vs INLINE hydrograph (check first)
HEC-RAS 2D boundary conditions can read flow hydrographs **inline** (stored in the `.u##` file,
`Use DSS=False`) **or from DSS** (`Use DSS=True` + pathname).
- Read the plan's BC table (project summary or the `.u##` text).
- If `Use DSS=True` with a real path: point it at the `*_RAS.dss` pathname.
- If `Use DSS=False` (inline): a DSS will not be read; overwrite the inline ordinate blocks instead
  (see hecras-2d-models, inline inflow replacement).

## HMS
- Repoint each Source/gage to the `*_HMS.dss` file and **re-select** the pathname.
- Confirm the gage shows nonzero values after import (the INST-VAL check above).

## After any change
- Inputs only: you must **recompute** the RAS plan(s) / HMS run(s) for results to reflect the new
  hydrographs (model-run-supervisor rerun gate: output newer than last input edit).
