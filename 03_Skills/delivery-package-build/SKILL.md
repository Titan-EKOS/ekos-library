---
name: delivery-package-build
description: Build a delivery or review package (report update, alternative, multi-GB review folder with CAD, models and PDFs) that someone else can review or rebuild - standard folder set, exclusions, firm document properties, README / inventory / rebuild guide / SHA256SUMS, one verified zip per deliverable in the dated OneDrive folder.
version: 1.0.0
status: active
function: compile-pdf
jurisdiction: all
tools_versions: "Python 3.10+ (stdlib zipfile ZIP64, pypdf); OneDrive client on EKOS"
owner: JCO
replaces: "none (new; carries the deliverable-packaging part of Standard v0.3 change DSO-C31 and drainage-report-build sec. 4)"
---
# Delivery Package Build

## When to use
- Handing over a report update, an alternative, or a multi-GB review folder (CAD, models, PDFs, renderings) so
  someone else can review or rebuild it.
- Transferring finished H&H or site-plan deliverables, or JCO needs results to review on another computer or a phone.
- A reviewer says "freeze": package current CAD, plans, results and exhibits with checksums.

## Inputs
- Finished content only: final report PDFs (compiled and checked with `drainage-report-standard` compile step),
  exhibits, GIS, CAD, model folders with final plan results, native printouts, scripts, QC records.
- Package name `<Initials>_<YYYYMMDD>_<CODE>_<description>` (dates YYYYMMDD, D56), e.g. `JCO_20261022_HOML5_Review`.
- Delivery folder: `30_Report\Issued\<package name>\` in the job tree (D56) and the dated synced OneDrive project
  folder on EKOS.
- `%DOCS_PY%` = documents env interpreter, `C:\EKOS\documents\.venv\Scripts\python.exe` (D11; ENVIRONMENTS.md); `%SK%` = this skill's `scripts\` folder.

## Steps
1. Finish all content before the final copy. Copy finished model results only, never while a run is writing (check
   that no solver is running on those folders; the builder stops on files modified in the last 10 min).
2. Stage the source in the work folder (local, non-synced drive) with the standard folder set (default, to confirm):
   01_Reports, 02_Exhibits, 03_GIS, 04_CAD, 05_Models, 06_Calculations (native printouts), 07_Scripts, 08_QC.
   One package per deliverable: an original-report update and a separate alternative are two zips. Keep reference
   model exports separate from the deliverable models.
3. Write `PACKAGE_README.md` from `reference/PACKAGE_README_template.md` (contents, which files are new and where the
   originals stay, coordinate system, software versions matching the models) and `REBUILD_GUIDE.md` (rebuild order).
   For a freeze package, list unresolved items in the README and pause any automatic follow-up after delivery.
4. Check compiled PDFs before copying: `"%DOCS_PY%" "<drainage-report-standard>\scripts\compile_pdf.py" check --pdf <file> --limit-mb <agency limit>`.
5. Build:
   ```
   "%DOCS_PY%" "%SK%\build_package.py" build --src <staged source> --stage D:\<work>\pkg_stage ^
      --out-dir "<OneDrive job folder>\<YYYYMMDD>" --name <package name> --creator "Psomas (JCO)" ^
      --pointer-in "<old work folder>"
   ```
   The stage folder is a dedicated folder, deleted and recreated each run (the script refuses one that overlaps the
   source). It excludes run copies, runtime junctions, temp/checkpoint HDF and scratch (`_run0x`, `.tmp.hdf`, `_body_`,
   `compute_stdout`, names starting with `_`, `.bck`, `.sol`, node_modules, __pycache__, .git, lock and temp files);
   sets docx/xlsx creator and last-modified-by to the firm preparer string; writes EXCLUSIONS.txt, FILE_INVENTORY.csv
   (fill the purpose column for the reviewer), SHA256SUMS and verify_package.py; zips once (ZIP64); re-reads every
   zip member and matches hashes; fails if another zip or temp file sits in the delivery folder.
6. Read the build log: file count, zipped and unzipped size, excluded items, warnings. Fix and rebuild on any failure;
   keep exactly one final zip per deliverable and delete zip temp files.
7. Copy the same package folder (unzipped) into `30_Report\Issued\` of the job tree when the job uses the Standard
   layout.
8. Save to the synced OneDrive project folder (dated). Leave the `Delivery_Location.txt` pointer in the old work
   folder; do not redistribute older D: copies after delivery moves to OneDrive.
9. Phone review: include portable HTML and MP4 for exhibits and animations; point JCO to the OneDrive folder, not a
   download link or email.
10. Handoff message: package path, file count, sizes, SHA-256 of the zip, and that cloud sync was not checked (allow
    time for multi-GB uploads).

## Jurisdiction add-ons
- None. Agency upload limits and file naming come from the reviewing agency add-on of `drainage-report-build`.

## Gotchas
- Two zips of different size (5.9 MB and 8.8 MB) and a leftover zip temp file remained in the package folder
  (HOMEWOOD-022).
- Late additions (source model, re-rendered views) forced re-copies; finish content first (SILVERBELL-012).
- Copying while a RAS run is writing risks partial HDFs (SILVERBELL-012).
- Zips were 4.4 GB and 7.4 GB (ZIP64); allow time for OneDrive sync (VALENCIA-010).
- The agent cannot open OneDrive share links in its browser; use the locally synced folder (VALENCIA-010).
- Older D: copies must not be redistributed after delivery moves to OneDrive (VALENCIA-010).
- The first package used a non-standard folder name and missed printouts/QC; it was rebuilt two hours later (3.4 GB
  then 3.7 GB zip) (RKN-019).
- Download links failed on the phone and email was not set up; OneDrive on the phone worked (CAMPBELL-023).

## QC checks
- Pull rules: `get_qc_rules('package')`.
- SHA-256 match for every member; exactly one final zip per deliverable; no temp files (VALENCIA-010, SILVERBELL-012,
  HOMEWOOD-022).
- Package contains native printouts and the QC folder; no excluded patterns present; README versions match the models
  (RKN-019, CAMPBELL-023).
- Office files carry the firm creator string; no tool or assistant names in file properties or folder names.
- Package name matches `<Initials>_<YYYYMMDD>_<CODE>_<description>` (D56).

## Change log
- 1.0.0 2026-10-22: built from clusters RPT-C12 and DSO-C31; decisions D48 (compiled PDFs inside a package follow the
  annotation rules, checked before packaging), D52 (PDF size limit check before packaging), D56 (YYYYMMDD names,
  30_Report/Issued). Default, to confirm: package folder set 01_Reports..08_QC. Added scripts/build_package.py
  (tested on a sample folder: exclusions, creator fix, inventory, ZIP64, verification) and the README template.
