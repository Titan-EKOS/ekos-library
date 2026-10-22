---
id: NORTHLOOP-010
title: Provisional 500-yr by Q100 multiplier and FIS profile applicability
type: qc_rule
function: hydrology
trigger: Critical facility needs a 500-yr WSE and only 100-yr hydrographs exist
steps:
- A 1.75 x Q100 ordinate scaling is a sensitivity only; label it provisional and get
  the accepted 500-yr hydrology from the agency
- Check NFHL cross sections against the parcel; use an FIS 0.2% profile only if its
  sections bracket the site
- If the site is Zone AO, note that AO depth and velocity are not an absolute 500-yr
  elevation
gotchas:
- Nearest mapped cross section was about 1,848 ft from the development boundary; the
  river profile could not be used for the site
- Prior report stated the 500-yr basis two ways (1.75 x Q100 and a 10-yr reference)
jurisdiction: Town of Marana; FEMA
tools_versions: FEMA NFHL REST; FLO-2D Pro
evidence:
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\fis_cross_section_distances.json
- C:\Users\Titan\OneDrive\Northloop\Review_2026-09-30\Drainage_Review.txt (F02, F05)
- C:\Users\Titan\OneDrive\Northloop\40_QC\T3_EOR_Review\NorthLoop_Concept1_Historical_2026-09-30_DRAFT_EOR-Markup.pdf
  p.1 callouts 1-2 (EOR 2021)
hours_lost: 1.5
recurrence: 2
confidence: high
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:29+00:00'
schema_version: 1
---
