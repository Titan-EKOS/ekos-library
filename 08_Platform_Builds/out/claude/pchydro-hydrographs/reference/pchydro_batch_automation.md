# PC-Hydro Batch Mode (Playwright)

Batch mode runs PC-Hydro 7.4 for many concentration points (CPs) without a person at the browser.
D18: use it for more than a few CPs; interactive mode (`pchydro_web_workflow.md`) for a few.
Proven on three projects: 67 subbasins in about 25 min once working (SAH-007); many-CP printout runs
(RKN-004); unattended local-queue runs with native validation (EKOS-LOCAL-006).

## Environment (EKOS)
- Python venv with `playwright` installed and the Edge channel available
  (`<venv>\Scripts\python.exe -m playwright install msedge` once). Call the venv python by full
  path (D11), e.g. `D:\EKOS\venvs\gis\Scripts\python.exe run_pchydro_batch.py ...` (confirm the venv
  path in the EKOS environment table; no .ps1 launchers, D12).
- Browser: Microsoft Edge channel, headless or an isolated (separate profile) window.
- Inputs: one `.pk6` (JSON) per CP, built from GIS (Phase 1b) or saved from earlier runs, plus the
  saved NOAA Atlas 14 upper 90% arrays per CP for the rainfall comparison.
- Run folder: `20_Working/Hydrology/PC-Hydro/<YYYYMMDD>_<scenario>/` with `inputs/`, `outputs/`,
  `run_log.txt`, `peaks.csv`, `hashes.csv`, `failed_cps.txt`.

## Before the first batch on a project
1. **Terms approval (D17).** Confirm the project run log holds "PC-Hydro terms approved by JCO,
   <YYYYMMDD>". If not, ask JCO once and write it. The batch script then clicks I Agree on every
   session without asking.
2. **Probe the live page.** The app JS is obfuscated; field ids and page functions change without
   notice. Run a probe that dumps `querySelectorAll('input,select,button')` (id, name, type, value)
   and the global function names to `probe_<YYYYMMDD>.txt`. Confirm the names the batch relies on
   are still present. Names seen in 2026 runs (confirm each time):
   - fields: `userName`, `calcDate`, `qp100`, `q100`, `tc100`, the 100-yr 1-hr rainfall field,
     the concentration-point field, the File-Open file input
   - page functions: `openProject`, `fillSCS`, `hydroCalc`, `hydroGraph`, `printFile`
   - output endpoints: `pdf.php` (program printout), `hydrograph.php` (1-min hydrograph CSV)
3. **Vegetation auto-fill check (D20).** On one graded-ground CP and one natural CP, record what the
   auto-fill writes into vegetation density. Graded ground must show the program default (20% per
   NORTHLOOP-013). If the live value differs, stop and ask JCO before the batch. Never hard-code a
   density into `.pk6` builders to replace the program default.
4. **Version check.** Record the PC-Hydro version shown on the page and confirm it is the version the
   reviewing agency accepts (see ELTORO-009 in SKILL.md gotchas).

## Per-CP loop
For each `.pk6` in `inputs/`:
1. **Load.** Open File > Open first so the File-Open dialog initializes, then set the file input to
   the `.pk6` (`page.set_input_files`). Wait until the concentration-point field shows the CP id.
2. **Preparer.** Set `userName` to `Psomas (<initials>)`.
3. **Read back.** Read every native input field and compare to the `.pk6`/scenario values. Apply the
   precision rules (lengths whole ft summing to the native total; soil shares whole percent by
   largest remainder totalling 100) and log each change as `CP, field, source, native`. Any other
   mismatch: mark the CP failed, go to the next CP.
4. **Rainfall (D21).** Enter coordinates at 4 decimals; trigger the in-app Fetch Rainfall. Wait for
   the Matches text and a filled 100-yr 1-hr field (timeout 60 s; on timeout mark failed). Compare
   every served depth to the saved array at 2 decimals. Log the Atlas edition served. A difference is
   logged and the served value is used; the batch does not overwrite the served depths.
5. **Calculate.** Call the page's calculate path (button click or `hydroCalc`). Wait until `calcDate`
   changes and `qp100` is filled (timeout 60 s). Read `q100`, `tc100` and the peak for every return
   period into `peaks.csv`.
6. **Outputs.** Either click the print/hydrograph buttons or call `printFile` / `hydroGraph` and
   capture the form posts, then post them to `pdf.php` and `hydrograph.php` from the same browser
   context (SAH-007 route). Save:
   - `<CP>_printout.pdf`: check the response content-type is `application/pdf`; if it is
     `text/html`, retry the CP once, then mark failed (RKN-004, seen at CP-103).
   - `<CP>_hydrograph.csv`: 1-minute export with the `Return Period:` / `Peak Discharge:` lines.
   - `<CP>.pk6`: the recomputed project as the app saves it.
7. **Hash.** SHA-256 of each saved file into `hashes.csv`.

After the loop:
- Write `failed_cps.txt` and rerun only those CPs. Repeat until empty or the same CP fails twice; then
  stop and report the CP with its log lines.
- Run Phase 4 (`hydrographs_to_xlsx.py`) on `outputs/*_hydrograph.csv`.

## Outline (Python, Playwright sync API)
Names below are the 2026 probe results; confirm with the probe before use.
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(accept_downloads=True)
    pg = ctx.new_page()
    pg.goto("https://pchydro.rfcd.pima.gov/")
    pg.get_by_text("I Agree").click()            # D17 approval already in run log
    for pk6 in pk6_files:
        pg.get_by_text("File").click(); pg.get_by_text("Open").click()   # init File-Open first
        pg.set_input_files("input[type=file]", str(pk6))
        pg.wait_for_function("document.querySelector('#cpName') && document.querySelector('#cpName').value !== ''")
        pg.fill("#userName", "Psomas (JCO)")
        # read back all fields -> compare -> log precision changes
        # fetch rainfall -> wait for 'Matches' and 100-yr 1-hr value -> compare at 2 dp
        old = pg.input_value("#calcDate")
        # trigger calculate, then:
        pg.wait_for_function(f"document.querySelector('#calcDate').value !== '{old}' && document.querySelector('#qp100').value !== ''")
        # capture printFile / hydroGraph posts -> ctx.request.post('.../pdf.php', ...) ; check content-type
```
`#cpName` is a placeholder for the concentration-point field id found by the probe.

## Do not
- Do not set fake valid flags or force Calculate enabled (EKOS-LOCAL-006).
- Do not request rainfall by direct HTTP; it returns 403. Use the in-app fetch (EKOS-LOCAL-006).
- Do not feed records through a local CORS helper server (127.0.0.1 with private-network headers);
  it worked early but the file-input route is simpler (RKN-004, SAH-007).
- Do not hard-code a vegetation density or a fixed CN into `.pk6` builders (D20, NORTHLOOP-013).

## When the web app changes
The batch breaks when the county changes the page (SAH-007). Re-run the probe, update the names in
the script, and log the change. The `.pk6` inputs are kept so any CP can be rerun by hand in
interactive mode while the batch is repaired.

## Failure record seen (for expectations)
One project logged 9 failed PC-Hydro tasks before the adapter was stable: NOAA mapping x3, basin
import x4, road scenario x1, benchmark x1 (EKOS-LOCAL-006). Causes: file-chooser timeouts (dialog not
initialized), soil shares totalling 99, full-precision GIS lengths failing the length-sum check, and
the 403 on direct rainfall requests.
