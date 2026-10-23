---
name: cad-base-update
description: Use when a consultant (architect, site-plan or civil) CAD base is reissued, when an automated run must pull or push geometry through Civil 3D (NETLOAD helpers, accoreconsole, COM), when a Civil 3D base must be rebuilt from a PDF DCR and GIS linework, or when model/site geometry must be handed to Civil 3D users as LandXML/DXF/DWG.
version: 1.0.0
status: active
function: project-setup
jurisdiction: all
tools_versions: "AutoCAD / Civil 3D 2026 (accoreconsole, COM, .NET helpers); InfraWorks 2026; LandXML 1.2; DXF AutoCAD 2018 format"
owner: JCO
replaces: "none (new; merges clusters DSO-C17 consultant base reissue, DSO-C21 Civil 3D automation, DSO-C22 base reconstruction from PDF, EXH-C14 LandXML handoff)"
---
# CAD Base Update and Civil 3D Automation

## When to use
- A consultant base (architect building/site plan, survey, civil) is reissued and xrefs must be swapped.
- A script or agent needs alignments, profiles, corridors or surfaces out of Civil 3D, or must load .NET helpers into a running session.
- Only a PDF DCR and GIS linework exist and a native Civil 3D base, corridor and plan set is needed.
- Site or model geometry produced outside CAD (Python, QGIS, model grids) must go to Civil 3D users.

Part A (reissue) is the most frequent use. Parts B-D are run as needed. Every part follows the source-file rule in Step 0.

## Inputs
- Job number and the Standard v0.3 job folder (D56): received bases land in `01_Reference\By_Others\<consultant>\`; working copies and scratch exports in `20_Working\<Initials>_<YYYYMMDD>_<Topic>\`.
- The CAD project xref folder (where the live xrefs sit) and the current check-plot set.
- Exhibit and sheet register (which exhibits/sheets reference which xref).
- For Part D: model grid or surface, CRS and vertical datum from the project data log.
- Environment: EKOS Python environment interpreter by full path (D11); no .ps1 files (D12).

## Steps

### Step 0 - Source files are read-only (all parts)
1. Copy every source DWG/DXF/LandXML to a scratch folder under `20_Working\...` and run all automated reads there. (NORTHLOOP-018)
2. Write a SHA-256 manifest of the source folder before the run and compare after; stop and report if any source file changed:
   `D:\EKOS\envs\<env>\.venv\Scripts\python.exe <skill>\scripts\hash_manifest.py make <source_folder> <scratch>\before.json`
   then `... hash_manifest.py check <source_folder> <scratch>\before.json` (exit code 1 = a source file changed or vanished).
3. Never open a received DWG in place with accoreconsole or a script that saves; console runs can refresh the DWG and its .bak. (NORTHLOOP-018)

### Part A - Consultant base reissue
1. Log the reissue: consultant, issue date, file names, transmittal reference, in the reissue log beside the xref folder (`CAD_Reissue_Log.md`, one row per issue).
2. Before replacing any xref, copy the current xref set to `<xref folder>\<consultant>\Archive\<YYYYMMDD>_Before_CAD_Update\`. Do not overwrite an earlier archive folder. (HOMEWOOD-021)
3. Place the new files in `01_Reference\By_Others\<consultant>\<YYYYMMDD>\` as received (unchanged), then copy into the xref folder under the same xref names so host drawings repath without edits.
4. Check the new base before swapping: units, insertion base point, CRS/known points against the previous issue (at least 3 points); flag any shift. (STARVALLEY-014; see project-intake for the full CRS check)
5. Swap/reload the xrefs, then list what moved: buildings and footprints, pads and finished floors, site linework, walls, utilities and electrical areas, grading limits. Use an overlay of old vs new (old in a contrasting color) or a scripted DXF comparison of layer extents and entity counts. (HOMEWOOD-021)
6. Flag affected design items: storm drain alignments and inverts, inlets, grading and FG surfaces, galleries/underground storage, basin footprints, drainage-area boundaries, exhibits and report figures. (HOMEWOOD-021)
7. Write the change list `CAD_Change_List_<YYYYMMDD>.md` beside the archive folder: what moved, affected items, affected sheets/exhibits (register IDs), rework owner, status. (HOMEWOOD-021)
8. Reissue check plots for every affected sheet/exhibit; mark superseded figures per the exhibit register (move old record figures to `10_Record\_Superseded\X\`, never delete).
9. If the reissue changes impervious area, drainage areas or facility footprints, notify the hydrology/hydraulics owner and add an open item to the QC open-items document (D44).

### Part B - Civil 3D automation (helpers, accoreconsole, COM)
1. Before scheduling, confirm a Civil 3D seat is free on this machine (no "Device limit reached"); if not, stop and report rather than queue. (TANGERINE-010)
2. Build any NETLOAD plugin as a proper project targeting the installed AutoCAD .NET runtime (one runtime only); test it in accoreconsole on one scratch drawing before any batch. (TANGERINE-010)
3. Pre-trust one helper folder, or batch helpers into one DLL, so the user approves the Load Once / trust dialog once. (SILVERBELL-009)
4. Verify the exact target drawing FullName before each SendCommand; re-check after any ActiveDocument change. (SILVERBELL-009)
5. Write a completion marker file per helper (`<helper>.done` with time and drawing); never repeat NETLOAD for a helper already logged complete. On restart, read the markers and resume. (SILVERBELL-009)
6. Run native CAD COM from an elevated shell; launch through Python (subprocess / win32com) or inline commands, not .ps1 files (D12). (SILVERBELL-009)
7. Headless runs: `"C:\Program Files\Autodesk\AutoCAD 2026\accoreconsole.exe" /i <scratch.dwg> /s <script.scr> /l en-US`; judge success by the output file existing and the return code being 0, and read the console log for "Unknown command" or "Unable to load assembly". (RKN-011, TANGERINE-010)
8. Fallback when helpers or seats fail: export LandXML alignments and profiles from Civil 3D by hand and read them by script; record the fallback in the run log. (TANGERINE-010)
9. InfraWorks: build the base model (terrain, aerial) only after CRS and vertical units are verified; never present source-only aerial views as proposed-corridor renders; label each view with its geometry basis. (TANGERINE-010)

### Part C - Base reconstruction from PDF DCR and GIS linework
1. Extract the construction baseline from the PDF vector strokes; georeference to the supplied GIS linework; keep a CAD-to-plan station crosswalk table. (SILVERBELL-007)
2. Build the EG TIN from clipped lidar (lidar choice and DEM per D53/D54, logged); trace the proposed profile from the plotted line at about 5 ft spacing. (SILVERBELL-007)
3. Build corridor regions at the source transition stations; record every schematic assumption on a decisions sheet. (SILVERBELL-007)
4. Produce individual sheets plus a combined PDF; package each revision with checksums. (SILVERBELL-007)
5. Keep the .mms companion file beside each DWG and include it in every copy and package. (SILVERBELL-007)
6. State the vertical datum of the DCR; if unknown, label EG vs FG differences as indicative only, not earthwork depths. (SILVERBELL-007)

### Part D - LandXML / DXF / DWG handoff to Civil 3D users
1. Confirm CRS and units of the outgoing geometry match the receiving drawing (EPSG and realization from the data log, D55 for Pima County; intl ft vs US survey ft stated).
2. Write LandXML 1.2: EX and PR TIN surfaces (25-ft grid inside grading limits + 300 ft), road alignments with FG profiles, private streets, block and lot parcels. LandXML point order is northing, easting, elevation. (RKN-011, STARVALLEY-014)
3. Check EX and PR surface point counts equal the grid count before export. (RKN-011)
4. Write a layered DXF (AutoCAD 2018 format) with lot numbers and 2-ft/10-ft contours. (RKN-011)
5. Convert DXF to DWG with accoreconsole headless (Part B step 7); confirm the DWG exists and rc = 0. (RKN-011)
6. Open the DWG once in Civil 3D (or have the CAD user confirm) to see surfaces and alignments load; log the check.
7. Ship with a short transmittal note: CRS, vertical datum, units, surface extents, source model/plan and date.

## Gotchas
- Architect base was reissued about 7 times and the site plan 4 times in five months; each update forced storm drain and exhibit rework, so the archive and change list are not optional. (HOMEWOOD-021)
- AutoCAD console refreshed a historical DWG and its BAK; the DWG was restored from backup but the older BAK was lost. Work on scratch copies only. (NORTHLOOP-018)
- A csc-compiled Extract.dll mixing .NET 8 and .NET 10 references failed in accoreconsole with "Unable to load assembly", then "Unknown command". (TANGERINE-010)
- Civil 3D showed "Device limit reached" because another device held the seat; proposed corridor and six perspectives stayed pending. (TANGERINE-010)
- Choose Assembly and Load Once dialogs blocked COM; screen automation could not reach off-monitor dialogs and the user had to click for 4 helpers. (SILVERBELL-009)
- A generic assembly error left one helper unapplied; native grading finished only with a later helper. Check each helper's marker, not the batch exit. (SILVERBELL-009)
- Native CAD COM needs an elevated shell. (SILVERBELL-009)
- Recovered chainage drifted 32.7 ft over the corridor; keep the drift in the crosswalk, do not hide it with a coordinate shift. (SILVERBELL-007)
- Printed vertical-curve labels conflicted with the plotted line; the trace follows plotted geometry and the conflict is flagged on the decisions sheet. (SILVERBELL-007)
- DCR vertical datum unknown; EG vs FG differences are not earthwork depths. (SILVERBELL-007)
- Without the .mms companion file the large surface is lost. (SILVERBELL-007)
- LandXML declared EPSG:2223 but was in local site coordinates; check known points, not metadata. (STARVALLEY-014)
- Surface point counts that do not match the grid mean a clipped or duplicated export. (RKN-011)

## QC checks
- Pull rules: `get_qc_rules('crs')`, `get_qc_rules('exhibits')`, `get_qc_rules('existing-conditions')`.
- Before/after hash manifest filed for every automated CAD read; no source file changed.
- Each reissue has an archive folder, a reissue-log row and a change list naming affected sheets/exhibits; affected check plots reissued.
- Known-point check (3 points minimum) logged for each new base and each outgoing LandXML/DWG.
- Every helper has a completion marker; no helper applied twice; fallback use logged.
- Handoff: surface point counts = grid count; DWG exists and rc 0; opens with surfaces and alignments.
- Reconstruction: station crosswalk, decisions sheet, checksums per revision, .mms beside each DWG.

## Change log
- 1.0.0 2026-10-22: built from clusters DSO-C17, DSO-C21, DSO-C22, EXH-C14 (with DSO-C10 source-file rule and DSO-C05 known-point check); decisions D11, D12, D44, D53, D54, D55 (default, to confirm), D56. Archive folder name `<YYYYMMDD>_Before_CAD_Update` and reissue-log/change-list file names are defaults, to confirm.
