# Terrain / DEM build (DSO-C04; D53, D54, D55)

Environment: EKOS GIS venv (GDAL, rasterio) by full path (D11). Keep raw tiles in `02_Data\Topo_Survey\Elevation_3DEP\`
and never re-download inside a rerun.

1. Extent: project plus all upstream/offsite contributing watersheds plus a margin. Check the extent covers every
   contributing watershed before PC-Hydro or HMS inputs are built.
2. Query the TNM API for 1 m DEM and 1/3 arc-second tiles; save the item list:
   `https://tnmaccess.nationalmap.gov/api/v1/products?datasets=Digital%20Elevation%20Model%20(DEM)%201%20meter&bbox=<xmin>,<ymin>,<xmax>,<ymax>&prodFormats=GeoTIFF&max=500`
   -> `_tnm_items.json` (repeat with `National Elevation Dataset (NED) 1/3 arc-second`).
3. Select tiles by named collection / acquisition year, not publication date (D53); drop duplicate NED entries and
   overlapping vintages; log the collection chosen.
4. Clip the tile list to the model area plus buffer before import or mosaic.
5. Mosaic and reproject:
   ```
   gdalbuildvrt -input_file_list tiles.txt mosaic_m.vrt
   gdalwarp -t_srs EPSG:2868 -tr 3.28084 3.28084 -r bilinear -co COMPRESS=DEFLATE -co TILED=YES mosaic_m.vrt dem_3p28_m.tif
   gdal_calc.py -A dem_3p28_m.tif --calc="A*3.280839895" --NoDataValue=-9999 --outfile=dem_3p28ft.tif --co COMPRESS=DEFLATE
   gdalwarp -tr 10 10 -r average dem_3p28ft.tif dem_10ft.tif          (hydrology; 30 ft for large basins)
   gdalinfo -stats dem_3p28ft.tif                                       (grid size, min/max elevation)
   ```
   Target CRS per jurisdiction (Pima County: EPSG:2868, NAD83(HARN) Arizona Central intl ft, D55). USGS 1 m tiles
   are NAD83 UTM 12N in meters: convert to ft and compare to survey before use.
6. Cell sizes (D54): hydraulics/grading 3 ft (3.28 ft keeps native 1 m); hydrology 10 ft; large basins 30 ft. Write
   both DEMs; log grid size and min/max elevation; nodata fraction inside the contributing area must be 0.
7. Composites: merge in priority order and print the cell count taken from each source; any source with 0 cells
   stops the run.
8. Two vintages: difference newer minus older; list change areas over 20 ac with mean change; use the newer lidar only
   where it is bare earth and the ground changed (e.g. mine tailings growth changes depression volumes and flow
   paths); log the choice in the assumption log.
9. RAS Mapper: set the projection first from a known .prj (the Terrain projection, not a feature shapefile .prj); let
   RAS Mapper reproject on import; add shapefiles as map layers, not under Terrains; keep tiles under
   `Terrain\USGS` and record the tile list (a merged .vrt is a convenient index).
10. Pull the road centerline profile (crests/sags) and stream profiles at crossings from the site DEM.
11. Culvert inverts read from lidar are estimates; carry them as open items until survey.
