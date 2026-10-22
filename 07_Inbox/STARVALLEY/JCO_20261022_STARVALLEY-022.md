---
id: STARVALLEY-022
title: Confirm every effective storm case is in the effective model package
type: qc_rule
function: hydrology
trigger: Duplicating an effective FLO-2D study for a CLOMR/LOMR
steps:
- Read the effective TDN storm list (duration, depth) and controlling-storm statement
- Check the supplied model package has the upstream rainfall-runoff model and detailed
  model inputs for every storm case
- Request missing cases from the community or FEMA library before modeling; do not
  claim a flood envelope from one storm
- Use effective inflows, not county design flows, for the FEMA comparison
gotchas:
- Effective TDN listed 3 hr 3.34 in and 24 hr 4.55 in storms; only the 3 hr case was
  in the package; the main package and blind rebuild both ran 3 hr only
jurisdiction: FEMA Region IX / Pima County RFCD
tools_versions: FLO-2D Pro Build 26.02.25
evidence:
- D:\SV-BLIND-CLOMR\_WORK\00_Admin\JCO_20261011_Closeout_and_Resume.txt
- D:\SV-BLIND-CLOMR\_WORK\00_Admin\judgment_register.json
hours_lost: 2.0
recurrence: 1
confidence: medium
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:15+00:00'
schema_version: 1
---
