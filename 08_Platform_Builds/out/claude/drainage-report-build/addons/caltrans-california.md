# drainage-report-build add-on: Caltrans / California

Load when: work inside Caltrans R/W (postmile lookup) or for a California agency; California city / county floodplain
ordinances apply in SFHA. HMS calibration: `hechms-headless` add-on caltrans-california. QC tag: `caltrans`.

## Governing manuals (confirm current edition)
- Caltrans Highway Design Manual (HDM) Ch. 800-890: 808.1 (approved programs), 819.2 (hydrology method by area, Table
  819.2C regression), 831.3 (design storm by highway class and speed) (CALFIRE-002, CALFIRE-006, CALFIRE-012).
- USGS SIR 2012-5113 regional regression (CALFIRE-006).
- Effective FIS at FEMA-mapped crossings (CALFIRE-006).
- Due-diligence set: Caltrans governs in state highway R/W; city floodplain ordinance in SFHA; SWRCB permits; DWR Best
  Available Maps; CVFPB regulated streams; state dam inundation boundaries (CALFIRE-001, CALFIRE-003).

## Methods
- Hydrology (HDM 819.2): Rational to about 320 ac with Atlas 14 and a 5-min Tc floor; above that HEC-HMS NRCS CN + UH with
  the 24-hr Atlas 14 storm; USGS SIR 2012-5113 regression check (Table 819.2C); FIS Q100 governs at FEMA crossings
  (CALFIRE-006).
- Roadside areas delineated from DEM flow paths and road crests / sags (CALFIRE-006).
- CN models on HSG C/D foothills calibrated to FIS and regression; uncalibrated 100-yr kept as a hydraulics sensitivity
  (CALFIRE-007).
- Programs: HDM Table 808.1 programs only; WSPG / CivilD need District approval (CALFIRE-012).
- Culverts with HY-8: alternatives and sensitivity flow list per HDM (CALFIRE-012) (`hy8-native-runs`).
- Bridge data from DOT as-builts and the NBI record (CALFIRE-011).
- Received California model sets: check NAD83 realization (EPSG 2230 vs 6426) before use (DLR-002).
- Public data: tenth-postmile points, AADT, state dam inundation boundaries (CALFIRE-003).

## Criteria
- Culverts: 10-yr HW/D <= 1.0 with a 100-yr check (CALFIRE-002 seed).
- Pavement: 25-yr spread to the shoulder on rural highways > 45 mph; Table 831.3 storm set by highway class and posted
  speed (CALFIRE-002).
- Bridges: 50-yr design with 2 ft freeboard (CALFIRE-002 seed).
- Treatment BMPs where new impervious is 10,000 sf or more (CALFIRE-002 seed).
- Location Hydraulic Study for any base floodplain encroachment (CALFIRE-002 seed).

## Review expectations
- Project description text verbatim from the scope / RFP where Caltrans requires it (TANGERINE-019).
- District Hydraulics confirms methods and calibrations; carry each as an open item until confirmed (CALFIRE-006, CALFIRE-007).
- Agency data requests (as-builts, effective HEC-RAS models, master plan data, dam operator data) take weeks; a FEMA data
  request took about 4 weeks (CALFIRE-001).

## Open questions to confirm
- Method District Hydraulics accepts for mid-size watersheds (HMS vs regression) (CALFIRE-006).
- Highway class and posted speed for the Table 831.3 storm; record as an assumption until traffic confirms (CALFIRE-002).
- District acceptance of a large CN calibration (14 points on CALFIRE) (CALFIRE-007).
- Criteria marked "seed" above came from the HJR add-on seed list for CALFIRE-002 / -006 / -007; confirm each against the
  current HDM section before citing.
