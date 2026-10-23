# <fill: package name, e.g. JCO_20261022_CODE_description>

Project: <fill: project name>  |  Psomas job: <fill: job number>  |  Date: <fill: YYYYMMDD>
Prepared by: Psomas (<fill: initials>)

## Purpose
<fill: what this package is for (agency review, client review, report update, alternative) and which deliverable it
supports>

## What is new
<fill: list of files or folders that are new in this package. Original files are not changed; originals remain at
<location>.>

## Contents
| Folder | Contents |
|---|---|
| 01_Reports | <fill> |
| 02_Exhibits | <fill> |
| 03_GIS | <fill> |
| 04_CAD | <fill> |
| 05_Models | <fill: model, plans used, result files> |
| 06_Calculations | <fill: native printouts> |
| 07_Scripts | <fill> |
| 08_QC | <fill: QC records included for the reviewer> |
Full file list with purpose and SHA-256: FILE_INVENTORY.csv. Items left out: EXCLUSIONS.txt.

## Coordinate system and datum
Horizontal: <fill: e.g. NAD83(HARN) Arizona Central, international feet, EPSG:2868>
Vertical: <fill: e.g. NAVD88, feet>

## Software
| Software | Version | Used for |
|---|---|---|
| <fill> | <fill> | <fill> |

## Rebuild
See REBUILD_GUIDE.md for the order in which models and documents are regenerated.

## Verify
Run `python verify_package.py verify --dir .` in the extracted folder; every file is checked against SHA256SUMS.
