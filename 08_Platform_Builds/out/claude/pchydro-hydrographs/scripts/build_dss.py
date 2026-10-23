#!/usr/bin/env python3
"""
build_dss.py -- Phase 4. Build DSS-7 flow time series from a hydrograph CSV for
HEC-RAS and/or HEC-HMS. Mirrors the pydsstools call proven on prior projects.

Feed it the PEAK-ADJUSTED routing CSV from hydrographs_to_xlsx.py --adjusted-csv (D19);
the native export stays as the record copy. After writing, reopen the file (HEC-DSSVue or
pydsstools read_ts) and verify every ordinate, interval, units and volume.

Input CSV: first column = time in minutes (regular step); remaining columns =
named flow series in cfs. Lines beginning with '#' are ignored (comment header).

Writes (DSS-7 only -- pydsstools cannot write v6):
  <stem>_RAS.dss   pathnames  //<SERIES>/FLOW//<Epart>/<Fpart>/          (A-part blank)
  <stem>_HMS.dss   pathnames  /<Apart>/<SERIES>/FLOW//<Epart>/<Fpart>/

Correctness notes (learned the hard way):
  * data_type = 'INST-VAL'  (HMS reads ZEROS if this is left INVALID/lowercase).
  * units = 'CFS'.
  * E-part default '1Minute' for a 1-min step; DSS-7 stores it canonically.
  * In HEC-HMS: repoint each gage to the DSS and RE-SELECT the pathname.
  * In HEC-RAS: a DSS BC needs Use DSS=True + the pathname; if the model uses
    INLINE hydrographs (Use DSS=False) use the inline-replacement playbook instead.

Usage:
  python3 build_dss.py --csv CP_routing_series.csv --out-stem ./PROJ_CP \
      --variant both --epart 1Minute --fpart DESIGN --apart PROJCODE
"""
import argparse, csv, os, sys

def load(csvpath):
    lines=[l for l in open(csvpath).read().splitlines() if not l.lstrip().startswith("#")]
    rdr=csv.reader(lines); rows=list(rdr)
    hdr=rows[0]; data=rows[1:]
    series={}
    for j in range(1,len(hdr)):
        series[hdr[j]]=[float(r[j]) for r in data if r and r[0] not in ("",None)]
    return series

def write_dss(path, series, epart, fpart, start_time, apart):
    from pydsstools.heclib.dss.HecDss import Open
    from pydsstools.core import TimeSeriesContainer
    if os.path.exists(path): os.remove(path)
    fid=Open(path, mode="rw")
    for name,vals in series.items():
        pathname=f"/{apart}/{name}/FLOW//{epart}/{fpart}/"
        tsc=TimeSeriesContainer(pathname, len(vals), 1,
              values=list(map(float,vals)),
              start_time=start_time, data_units="CFS", data_type="INST-VAL")
        fid.put_ts(tsc)
    fid.close()
    print(f"WROTE {path}  ({len(series)} records, peak example {max(next(iter(series.values()))):.2f})")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--csv",required=True)
    ap.add_argument("--out-stem",required=True)
    ap.add_argument("--variant",choices=["ras","hms","both"],default="both")
    ap.add_argument("--epart",default="1Minute")
    ap.add_argument("--fpart",default="DESIGN")
    ap.add_argument("--apart",default="PROJECT",help="HMS A-part (basin/run label)")
    ap.add_argument("--start",default="01JAN2000 0000")
    a=ap.parse_args()
    series=load(a.csv)
    if not series: sys.exit("No data series found in CSV.")
    if a.variant in ("ras","both"):
        write_dss(a.out_stem+"_RAS.dss", series, a.epart, a.fpart, a.start, apart="")
    if a.variant in ("hms","both"):
        write_dss(a.out_stem+"_HMS.dss", series, a.epart, a.fpart, a.start, apart=a.apart)

if __name__=="__main__": main()
