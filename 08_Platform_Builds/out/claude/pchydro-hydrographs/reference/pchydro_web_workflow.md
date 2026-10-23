# PC-Hydro Web Workflow: interactive mode

The Pima County PC-Hydro 7.4 app at **https://pchydro.rfcd.pima.gov/** is the engine. There is no
offline engine; peaks, printouts and hydrographs come from the website. Interactive mode drives the
site through a browser automation tool attached to a visible browser (for example a browser
extension with page read and form input). Use it for a few concentration points (CPs). For more than
a few CPs use batch mode (`reference/pchydro_batch_automation.md`, D18).

## Prerequisites
- Browser automation tool connected; PC-Hydro site open in a tab the tool can see.
- Phase 1 `*_basin_inputs.csv` (or GIS-built `.pk6` set) reviewed and confirmed by the user.
- Terms approval recorded for this project in the run log (D17, see step 2).

## Steps
1. **Open / focus** the PC-Hydro tab (open the URL if needed). Keep the window still for the
   whole sequence.
2. **Terms of use ("I Agree").** D17: JCO approval is recorded once per project in the run log
   (`00_Admin/run_log`, line "PC-Hydro terms approved by JCO, <YYYYMMDD>"). If the line exists, click
   I Agree. If it does not, ask JCO once, write the line, then click. Do not ask again on later
   sessions of the same project.
3. **Open or create the CP.** Preferred: File > Open the `.pk6` (initialize the File-Open dialog
   before setting the file input) and wait until the concentration-point field populates. New CP:
   set the Project / Concentration Point field to the basin id from the report so exports
   self-identify.
4. **Preparer.** Set userName to `Psomas (<initials>)` before Calculate.
5. **Enter or confirm parameters** from the extract CSV: drainage area, flow length and segment
   slopes, cover type and density, soil group shares, % impervious, watershed type. Use the form
   input tool; read every field back with a page read before Calculate and compare to the source
   values. Stop on any mismatch.
   - Flow-length segments: whole ft, summing exactly to the native total length.
   - Soil shares: whole percent by largest remainder so they total 100.
   - Log every precision change (source value vs native value).
   - Vegetation on graded ground: program default (D20). Do not type a density.
6. **Rainfall (D21).** Enter coordinates at 4 decimals and press the in-app **Fetch Rainfall**. Wait
   until the page shows Matches and the 100-yr 1-hr field is filled. Compare the served depths to the
   saved NOAA Atlas 14 upper 90% array at 2-decimal rounding. Record the Atlas edition served. The
   in-app values govern; any depth written by script is the comparison array only.
7. **Calculate.** Wait until calcDate changes and qp100 is filled. Read q100 and tc100 (Tc is the
   program value, 5 min minimum).
8. **Return periods.** Select the events needed (2, 5, 10, 25, 50, 100, 500 as scoped).
9. **Save outputs:** program printout PDF (check it is a PDF, not an HTML page), the 1-minute
   **Generate Hydrograph** CSV, and the recomputed `.pk6`. Each exported CSV holds all selected
   return periods with `Concentration Point`, `Return Period:` and `Peak Discharge:` header lines;
   `hydrographs_to_xlsx.py` reads the reported peak from these lines.
10. Repeat 3-9 for each CP. Write file hashes and a peaks table to the run folder.

## Gotchas
- **Page re-render when the browser window is moved or resized** can reset state. Keep the window
  still during a sequence; if it blanks, reload and resume from the last saved CP
  (pchydro-hydrographs v1 reference).
- **Match the export's Concentration Point field to the basin id**, not the filename; the assembly
  script keys series names off the in-file value (pchydro-hydrographs v1 reference).
- The exported CSV's per-event block is delimited by `Return Period:` lines with a following
  `Peak Discharge:` line; the 1-minute series is the time,flow rows beneath
  (pchydro-hydrographs v1 reference).
- Confirm units are **cfs** and the export step is really **60 s** (check the file, not only the UI
  setting) (EKOS-LOCAL-007).
- Never set fake valid flags or force Calculate enabled to get past a validation error; fix the
  input (EKOS-LOCAL-006).

## Hand-off to scripts
- Save all exported CSVs into one run folder (`20_Working/Hydrology/PC-Hydro/<YYYYMMDD>_<scenario>`).
- Phase 4: `hydrographs_to_xlsx.py` for the QC workbook, both peaks, and the routing CSV.
- Phase 5: `build_dss.py` on the routing CSV, then the round-trip check.
