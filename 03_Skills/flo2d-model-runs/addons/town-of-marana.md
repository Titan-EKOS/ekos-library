# flo2d-model-runs add-on: Town of Marana

Load when the project is in the Town of Marana (confirm jurisdiction from the parcel record first).
Governing manual: Town of Marana Drainage Manual (2024), Section 4.5 for FLO-2D.

## Rules
1. Engine build (decision D03, default, to confirm): the manual names FLO-2D Pro build 17.08.17. On EKOS that
   build fails at startup (War30.bac access denied, admin prompt). Use the working build 26.02.25 and:
   - record both builds in the tool-version table of the model basis;
   - log an open item "agency acceptance of build 26.02.25" in the QC open-items document (decision D44);
   - JCO requests written Town acceptance; log the reply per project;
   - state the build and the departure from MDM 4.5 in the report issues section.
   (NORTHLOOP-008, NORTHLOOP-003)
2. Archived Town / regional models may show other builds (e.g. 19.07.21, 21.08.23); treat their results as
   historical until accepted and rerun every compared condition on the working build (NORTHLOOP-003).
3. Flows (decision D24, default, to confirm): design FLO-2D runs for site facilities on non-regional
   discharges (MDM 4.1); regional flows only where the facility is a regional channel / linear park, and for
   FEMA mapping. State which basis each run uses in the run register and captions.
4. Finished floor 1 ft above the 500-yr WSE (Town Code 17-15-10 H.5): a 500-yr run is needed where floors are
   set from the model. A 500-yr from a 1.75 x Q100 multiplier is provisional only; follow decision D22 and
   get Town agreement (NORTHLOOP-006, NORTHLOOP-003).
5. Collector channels in alluvial piedmont areas: 2 ft freeboard; lining and level-spreader items per the
   drainage-report-build Town of Marana add-on (NORTHLOOP-014, -015, -016).
6. Reviewers require common-mesh / common-grid existing and proposed runs before any no-adverse-impact text
   (TANGERINE-003); see impact-comparison.

## QC
- run `get_qc_rules('marana')`.
- Build acceptance item open or closed with the Town letter on file.
