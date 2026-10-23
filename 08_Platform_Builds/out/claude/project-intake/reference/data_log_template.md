# Data log and CRS record (template)

File: `02_Data\<Job>_DataLog_<YYYYMMDD>.md` (or .xlsx with the same columns). One per job; every dataset that feeds a
model, map or calc has a row before it is used. Internal record; not a deliverable.

## Project coordinate reference
| Item | Value |
|---|---|
| Horizontal CRS | e.g. NAD83(HARN) / Arizona Central (ft), EPSG:2868 (D55 Pima County default; default, to confirm) |
| Realization | HARN / NAD83(1986) / NAD83(2011) - always stated (D55) |
| Units | international ft / US survey ft |
| Vertical datum | NAVD88 ft (state the geoid if a conversion was made) |
| Basis | survey basis statement, benchmark ID and elevation (from the survey); if absent: requested on <date>, dependent elevations provisional |
| Local site coordinates | none / transform: translate dx, dy; rotate deg about base point x, y; scale factor |

Rule: any layer whose realization differs from the project realization is flagged before use (CRS QC rule) and
transformed with a stated method; never let a GIS reproject on the fly silently.

## Dataset rows
| ID | Theme | Source / collection | Acquisition (vintage) | Retrieved (YYYYMMDD) | Native CRS (EPSG + realization) | Vertical datum / units | Processing (reprojection, unit conversion, clip, mosaic) | Cell size (D54) | Known-point check (3+ points, max diff ft) | Use | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-01 | Terrain | USGS 3DEP 1 m, collection <name> | 2021 | | EPSG:26912 UTM 12N m | NAVD88 m | mosaic, EPSG:2868, m->ft x 3.280839895 | 3.28 ft (native 1 m kept) | | hydraulics | lidar chosen by acquisition collection (D53) |
| D-02 | Terrain (hydrology) | same | | | | | resample | 10 ft | | hydrology | |
| D-03 | Survey | civil team LandXML | | | declared EPSG:2223; checked: local coords | NAVD88 ft, BM <id> | local -> State Plane transform | n/a | 3 pts, 0.04 ft | grid update | |

## Cell sizes (D54)
Hydraulics and grading 3 ft (keep 3.28 ft when that preserves native 1 m); hydrology 10 ft; large basins 30 ft.

## Lidar choice (D53)
Choose by acquisition collection, not publication date; log the choice; difference vintages where both exist (list
change areas over 20 ac with mean change); a composite is allowed with per-source cell counts logged.

## Assumption log (same file, second table)
| ID | Assumption | Basis | Affects | Owner | Status |
|---|---|---|---|---|---|
| A-01 | HSG for dual groups (B/D, C/D) and Not rated units | stated rule, e.g. drained condition / most restrictive | CN, losses | | |
