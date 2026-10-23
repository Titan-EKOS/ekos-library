# Review record - <job no> - <deliverable name> - <mode>

Internal QC record - not for transmittal. Review package is not stamped; JCO accepts or rejects each finding.

| Field | Value |
|---|---|
| Job no | |
| Deliverable(s) reviewed | file name, revision, hash (SHA-256, first 12 chars) |
| Mode | full / submittal-audit / blind-rebuild / mock-agency |
| Scope tags pulled | e.g. report-text, tables, exhibits, hydrology, flo2d, fema, pima-rfcd |
| Rules pulled | count and date of get_qc_rules call |
| Evidence set | list or link to evidence_index.csv |
| Excluded inputs | producer notes / working folders refused (list) |
| Reviewer | platform and instance (separate context from producer) |
| Date | YYYYMMDD |

## Governing standards
| Item | Governing value | Source (document, edition, section) |
|---|---|---|
| Hydrology method | | |
| Design storms | | |
| HGL / freeboard criterion | | |
| WQ / hydromodification | | |
| FEMA guidance / effective model | | |

## Items
Status (D45): Addressed / Partial / Assumed / Not Addressed / Cannot Determine / Stale.
Disposition (separate field, filled after producer response): incorporated / superseded / no change.

| ID | Document / page / section | Finding | Evidence (file + page) | Rule tag | Status | Disposition | Required action | Owner |
|---|---|---|---|---|---|---|---|---|
| QC-01 | | | | | | | | |

## Native-vs-report table (hydrology / hydraulics)
| CP / structure | RP | Report value | Native value | Native file + page | Diff | Pass |
|---|---|---|---|---|---|---|

## Run matrix (from completion files, not plans)
| Model | Storm | RP | Scenario | Completion evidence | In narrative? |
|---|---|---|---|---|---|

## Decisions for JCO
See decisions_for_JCO.md (one entry per decision: problem, options, consequences, image).

## Independent checks (40_QC only, D30)
| File | Basis | New / reference | Result summary |
|---|---|---|---|
