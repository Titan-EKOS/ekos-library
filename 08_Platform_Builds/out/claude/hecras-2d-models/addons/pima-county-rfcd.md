# hecras-2d-models add-on: Pima County RFCD (TECH-018, TECH-033)

Load for HEC-RAS 2D models reviewed by Pima County Regional Flood Control District.

## Rules
1. TECH-033 2D rain-on-grid: run existing and each alternative; plans for the 2-, 10-, 100- and 500-yr events
   (100/2/10/500-yr set in the source case). One plan and flow file per event and condition (RKN-007, SAH-010).
2. TECH-018 critical storm: compare the 1-hr IDF storm with the SCS Type II 3-hr (and 24-hr where the basin
   size calls for it) and use the critical storm. Where an adjacent accepted study used a different storm
   (e.g. FLO-2D, SCS Type II 3-hr, 10 ft grid), align with that precedent and state it (ELTORO-004).
3. CN from the PC-Hydro User Guide table: HSG A desert brush treated as B; 20 pct cover density = CN 83
   (RKN-007). Burn roads / paths CN 99 (ELTORO-004).
4. Rainfall: NOAA Atlas 14 upper 90 pct (TECH-010), 5-min hyetograph to DSS; areal reduction over 1 sq mi per
   TECH-018.
5. Approval item: RFCD acceptance of a 2D approach is not automatic. Raise it at the methodology meeting and
   log it as an open item until accepted (RKN-007).
6. Regulatory washes with Q100 >= 100 cfs still need floodplain delineation; confirm with RFCD whether the 2D
   result serves or a 1D model is required.
7. Composite terrain from overlapping lidar collections allowed with a log (TECH-033 cited; decision D53);
   default CRS NAD83(HARN) AZ Central intl ft, EPSG:2868 (decision D55, default, to confirm).
8. Uniform n only when extending an accepted model (decision D28); RFCD reviewers expect land-cover n on new
   studies.

## QC
- run `get_qc_rules('pima-rfcd')`.
- Critical-storm comparison table in the model basis; acceptance item logged.
