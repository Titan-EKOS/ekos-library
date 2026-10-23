# EKOS Python environments (D11)

Skills and agents call Python by full interpreter path, never `python` from PATH. On EKOS the paths are set as
user environment variables, so `.cmd` launchers use `"%GIS_PY%"` and PowerShell uses `& $env:GIS_PY`.
The environments are the locked uv projects under `C:\EKOS\<env>` (pyproject.toml + uv.lock). Add packages with
`uv add --project C:\EKOS\<env> <package>`; never bare pip.

| Variable | Interpreter | Key packages | Used by |
|---|---|---|---|
| `GIS_PY` | `C:\EKOS\gis\.venv\Scripts\python.exe` | rasterio, geopandas, h5py, numpy, scipy, matplotlib, whitebox | hecras_result_rasters, ras_result_check, rise_exceedance, run_checks, exhibit_kit, flo2d_cell_compare, shared_input_hashes, rest_harvest, terrain builds |
| `DOCS_PY` | `C:\EKOS\documents\.venv\Scripts\python.exe` | python-docx, openpyxl, pypdf, pymupdf, pdfplumber, lxml, pywin32, psutil, PyYAML | drainage-report-standard scripts, crl_tools, build_package, package_qc, hash_manifest, extract_redlines, intake_inventory, pchydro extract/xlsx |
| `HYDRO_PY` | `C:\EKOS\hydrology\.venv\Scripts\python.exe` | numpy 1.26 (pinned by pydsstools), scipy, pandas, xarray, pydsstools 3.1 | build_dss, make_hms_run_script, check_hms_results, swmm_width_calibrate, gw_reinfiltration_calc |
| `HYDRAULICS_PY` | `C:\EKOS\hydraulics\.venv\Scripts\python.exe` | numpy, pandas, matplotlib, pywinauto, pywin32, psutil | ras_headless, ras_plan_register, flo2d_harness, flo2d_dialog_watch, flo2d_channel_check, hy8_template, hds5_check |
| `ACQ_PY` | `C:\EKOS\acquisition\.venv\Scripts\python.exe` | playwright | PC-Hydro batch automation |
| `LIBRARY_PY` | `D:\EKOS\Library\09_Server\.venv\Scripts\python.exe` | mcp, PyYAML | library server, library_cli, build.py, hooks |

Changes 2026-10-22 (JCO): pydsstools added to hydrology (moved numpy 2.5.1 to 1.26.4 and scipy 1.18.0 to 1.17.1 in
that env); pywinauto, pywin32 and psutil added to hydraulics. Backups of the previous pyproject.toml and uv.lock sit
beside each file as `*.JCO_20261022.bak`.
