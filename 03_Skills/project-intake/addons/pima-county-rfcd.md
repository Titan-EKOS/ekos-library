# Add-on: Pima County RFCD (project-intake)

1. Lidar collections over Pima County overlap: AZ_PimaCounty_2021_B21 (preferred), 2018, 2015. Choose by acquisition
   collection and log it (D53, RKN-002, DLR-007).
2. PAG 2015 10 ft lidar with NED 1/3 arc-second outside its coverage has served as the hydrology terrain (SAH-018,
   SAH-020); a composite follows the composite rule (per-source cell counts, newer lidar only where bare earth changed)
   with TECH-033 cited for the composite (SAH-020).
3. Target CRS: NAD83(HARN) Arizona Central, international ft, EPSG:2868 (D55, default, to confirm). Pima County GIS
   data is HARN (DLR-007). Survey or CAD declaring EPSG:2223 (NAD83, not HARN) is checked with known points and
   transformed with a stated method (STARVALLEY-014); the realization goes in the data log.
4. Hydrology inputs come from the RFCD method (PC-Hydro rainfall and soils sources), not the generic PFDS/SSURGO/NLCD
   path (DSO-C03).

Change log
- 1.0.0 2026-10-22: from DSO-C04 add-on (RKN-002, DLR-007, SAH-018, SAH-020), DSO-C03, DSO-C05; D53, D55.
