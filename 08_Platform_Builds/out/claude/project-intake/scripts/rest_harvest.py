r"""Public GIS harvest from ArcGIS REST layers by envelope, with paging and a download log (skill project-intake,
DSO-C03). Replayable: the same config and envelope give the same request set (D14 for EKOS-LOCAL jobs).

Config (JSON): {"envelope": [xmin, ymin, xmax, ymax], "in_sr": 4326, "out_sr": 2868,
                "layers": [{"theme": "FEMA", "name": "NFHL_Flood_Hazard_Zones",
                            "url": "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28"}, ...]}
Usage:
  python rest_harvest.py --config harvest.json --out <job>\02_Data\GIS_Public\<YYYYMMDD> [--page 500] [--timeout 180]
  python rest_harvest.py --config harvest.json --out <dir> --dry-run      (prints the requests only)
Writes one GeoJSON per layer (and a GeoPackage per theme when geopandas is installed) plus _download_log.csv
(theme, layer, feature count or ERR text, source URL, query time). Failures are logged and the loop continues.
Exit codes: 0 all layers ok, 1 one or more ERR rows, 2 usage error.
"""
import argparse
import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path


def query(url, params, timeout):
    q = url.rstrip("/") + "/query?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(q, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def harvest_layer(layer, env, in_sr, out_sr, page, timeout, retries=2):
    feats, offset = [], 0
    base = {"where": "1=1", "outFields": "*", "f": "geojson", "returnGeometry": "true",
            "geometry": ",".join(str(v) for v in env), "geometryType": "esriGeometryEnvelope",
            "inSR": in_sr, "outSR": out_sr, "spatialRel": "esriSpatialRelIntersects",
            "resultRecordCount": page}
    while True:
        params = dict(base, resultOffset=offset)
        for attempt in range(retries + 1):
            try:
                data = query(layer["url"], params, timeout)
                break
            except Exception:  # noqa: BLE001 - logged by caller after the last retry
                if attempt == retries:
                    raise
                time.sleep(3 * (attempt + 1))
        if "error" in data:
            raise RuntimeError(json.dumps(data["error"])[:300])
        batch = data.get("features", [])
        feats += batch
        exceeded = data.get("exceededTransferLimit") or (data.get("properties") or {}).get("exceededTransferLimit")
        if not batch or (len(batch) < page and not exceeded):
            break
        offset += len(batch)
    return feats


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--page", type=int, default=500)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    env, in_sr, out_sr = cfg["envelope"], cfg.get("in_sr", 4326), cfg.get("out_sr", 4326)
    out = Path(a.out)
    if a.dry_run:
        for L in cfg["layers"]:
            print(f"{L['theme']}/{L['name']}: {L['url']}/query envelope={env} inSR={in_sr} outSR={out_sr} page={a.page}")
        return 0
    out.mkdir(parents=True, exist_ok=True)
    log_rows, by_theme = [], {}
    for L in cfg["layers"]:
        t0 = datetime.now().strftime("%Y%m%d %H:%M:%S")
        try:
            feats = harvest_layer(L, env, in_sr, out_sr, a.page, a.timeout)
            fc = {"type": "FeatureCollection", "features": feats}
            (out / f"{L['theme']}_{L['name']}.geojson").write_text(json.dumps(fc), encoding="utf-8")
            by_theme.setdefault(L["theme"], []).append((L["name"], fc))
            log_rows.append([L["theme"], L["name"], len(feats), L["url"], t0])
            print(f"{L['theme']}/{L['name']}: {len(feats)} features")
        except Exception as e:  # noqa: BLE001 - one dead service must not stop the pass
            log_rows.append([L["theme"], L["name"], f"ERR {type(e).__name__}: {str(e)[:200]}", L["url"], t0])
            print(f"{L['theme']}/{L['name']}: ERR {e}")
    with open(out / "_download_log.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["theme", "layer", "features_or_error", "source_url", "queried"])
        w.writerows(log_rows)
    try:
        import geopandas as gpd  # optional: GeoPackage master per theme keeps full field names
        for theme, items in by_theme.items():
            for name, fc in items:
                if fc["features"]:
                    gdf = gpd.GeoDataFrame.from_features(fc["features"], crs=f"EPSG:{out_sr}")
                    gdf.to_file(out / f"{theme}.gpkg", layer=name, driver="GPKG")
    except ImportError:
        print("geopandas not installed: GeoJSON written; build the GeoPackage in the GIS environment")
    errs = sum(1 for r in log_rows if str(r[2]).startswith("ERR"))
    print(f"log: {out / '_download_log.csv'} ({errs} ERR rows)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
