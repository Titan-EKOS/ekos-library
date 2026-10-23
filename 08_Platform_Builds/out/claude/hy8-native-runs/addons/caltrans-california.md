# hy8-native-runs add-on: Caltrans / California

Load for culverts on Caltrans facilities or California projects that follow the Caltrans Highway Design Manual.

## Rules
1. Alternatives and sensitivity flows per HDM Table 808.1: build one crossing per alternative (e.g. 1-48 in,
   2-48 in, 60 in, 72 in RCP) with a user discharge list that includes the sensitivity flow (CALFIRE-012).
2. Roadway profile from the terrain profile (every 10th point is enough), trapezoid tailwater channel unless
   a rating is available (CALFIRE-012).
3. Report: summary table, rating curve, performance plot, site / culvert / tailwater / roadway data and front
   view per crossing (CALFIRE-012).
4. Check cover for every alternative against the road profile; flag any under 1 ft (CALFIRE-012).
5. Bridge data for related HEC-RAS work come from DOT as-builts and the NBI record (CALFIRE-011).

## QC
- run `get_qc_rules('caltrans')`.
