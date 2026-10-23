# Add-on: Caltrans / California (project-intake)

1. Locate crossings and entrances by Caltrans tenth-postmile points; harvest state highway lines, tenth postmiles,
   bridges, AADT and intersections, and state dam inundation boundaries (CALFIRE-003).
2. California received model sets (CA zone 6): check the NAD83 realization of every layer - EPSG:2230 (NAD83) vs
   EPSG:6426 (NAD83(2011)) - before sampling or overlaying; a silent mismatch can reach a few ft (DLR-002).
3. No local county manual: rainfall from NOAA PFDS, soils from SSURGO, land cover from NLCD 2021, gages from NWIS
   (CALFIRE-005).

Change log
- 1.0.0 2026-10-22: from DSO-C03 add-on public-gis-data-harvest/Caltrans-California (CALFIRE-003, CALFIRE-005) and
  HYD-C13 California add-on (DLR-002).
