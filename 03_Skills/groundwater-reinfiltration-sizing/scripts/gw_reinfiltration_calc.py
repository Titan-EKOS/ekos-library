#!/usr/bin/env python3
"""
gw_reinfiltration_calc.py -- groundwater displacement and reinfiltration sizing
(groundwater-reinfiltration-sizing v1, HJR-C17; HOMEWOOD-016, HOMEWOOD-017, HOMEWOOD-009).

Reads one JSON case file and prints / writes a calc summary:
  1. Seepage per impeded face (Darcy): Q = k * i * A
  2. Storage required = total Q x storage_hours (default 24 hr)
  3. Infiltration area required so the facility infiltrates the continuous seepage
     at the design rate; drawdown time of the stored volume; 0 in/hr sensitivity
     (all seepage to overflow)
  4. Gallery gross volume from the void ratio
  5. Depth check, finished grade to SHGW:
       pipe/chamber height + bedding + min cover to bottom of structural section
       + structural section + required separation to SHGW

Units: k in ft/day; areas in sf; gradient i in ft/ft; rates in in/hr; lengths in in
unless named _ft. Every number in the output traces to the JSON input.

Example case file (keys shown with typical units):
{
  "case": "PROJ GW reinfiltration rev 3",
  "date": "20261022",
  "faces": [ {"name": "North wall", "k_ft_per_day": 2.0, "gradient": 0.5, "area_sf": 600} ],
  "storage_hours": 24,
  "design_infiltration_in_hr": 1.0,
  "infiltration_basis": "untested: half NRCS rate (Placer add-on, to confirm)",
  "provided_infiltration_area_sf": 1050,
  "void_ratio": 0.40,
  "provided_gross_volume_cf": null,
  "depth_check": {"unit_height_in": 36, "bedding_in": 2, "min_cover_in": 12,
                  "structural_section_in": 12, "separation_ft": 5.0,
                  "separation_basis": "East Placer 5 ft SHGW rule",
                  "available_fg_to_shgw_ft": 9.0}
}

Usage:
  "%HYDRO_PY%" gw_reinfiltration_calc.py case.json --out case_summary.csv
  python3 gw_reinfiltration_calc.py case.json
Exit code 0 = all checks met, 2 = a check not met (see the CHECK lines).
"""
import argparse
import csv
import json
import sys


def ft_per_day(in_hr):
    return in_hr / 12.0 * 24.0


def depth_required_ft(d):
    """Finished grade to SHGW required (ft). Cover is to bottom of structural section."""
    stack_in = d["unit_height_in"] + d.get("bedding_in", 0) + d.get("min_cover_in", 0) \
        + d.get("structural_section_in", 0)
    return stack_in / 12.0, stack_in / 12.0 + d["separation_ft"]


def run(case):
    rows, checks = [], []

    def put(item, value, unit, note=""):
        rows.append([item, value if not isinstance(value, float) else round(value, 4), unit, note])

    put("case", case.get("case", ""), "", case.get("date", ""))
    q_total = 0.0
    for f in case["faces"]:
        q = f["k_ft_per_day"] * f["gradient"] * f["area_sf"]
        q_total += q
        put(f"seepage {f['name']}", q, "cf/day",
            f"k={f['k_ft_per_day']} ft/day x i={f['gradient']} x A={f['area_sf']} sf")
    put("seepage total", q_total, "cf/day", f"{q_total / 86400.0:.5f} cfs; {q_total * 7.48052 / 1440:.3f} gpm")

    hrs = case.get("storage_hours", 24)
    storage = q_total * hrs / 24.0
    put("storage required", storage, "cf", f"total seepage x {hrs} hr")

    vr = case.get("void_ratio")
    if vr:
        gross = storage / vr
        put("gross gallery volume required", gross, "cf", f"storage / void ratio {vr}")
        prov = case.get("provided_gross_volume_cf")
        if prov:
            ok = prov >= gross - 1e-6
            checks.append(("gallery volume", ok, f"provided {prov} cf vs required {gross:.1f} cf"))

    rate = case.get("design_infiltration_in_hr")
    put("design infiltration rate", rate if rate is not None else "none", "in/hr",
        case.get("infiltration_basis", "basis not stated"))
    if not case.get("infiltration_basis"):
        checks.append(("infiltration basis stated", False, "state tested rate or untested basis and testing requirement"))
    if rate:
        a_req = q_total / ft_per_day(rate)
        put("infiltration area required (continuous seepage)", a_req, "sf",
            f"Q / ({rate} in/hr = {ft_per_day(rate):.3f} ft/day)")
        a_prov = case.get("provided_infiltration_area_sf")
        if a_prov:
            ok = a_prov >= a_req - 1e-6
            checks.append(("infiltration area", ok, f"provided {a_prov} sf vs required {a_req:.1f} sf"))
            net = a_prov * ft_per_day(rate) - q_total
            if net > 0:
                put("drawdown of full storage", storage / net * 24.0, "hr",
                    "storage / (infiltration capacity - continuous seepage)")
            else:
                put("drawdown of full storage", "does not drain", "",
                    "infiltration capacity <= seepage; overflow carries the difference")
    put("0 in/hr sensitivity: overflow flow", q_total / 86400.0, "cfs",
        "all seepage to overflow; overflow path required")

    d = case.get("depth_check")
    if d:
        stack_ft, req_ft = depth_required_ft(d)
        put("unit + bedding + cover + structural section", stack_ft, "ft",
            f"{d['unit_height_in']} + {d.get('bedding_in', 0)} + {d.get('min_cover_in', 0)} + "
            f"{d.get('structural_section_in', 0)} in")
        put("finished grade to SHGW required", req_ft, "ft",
            f"+ separation {d['separation_ft']} ft ({d.get('separation_basis', 'basis not stated')})")
        avail = d.get("available_fg_to_shgw_ft")
        if avail is not None:
            checks.append(("depth to SHGW", avail >= req_ft - 1e-6,
                           f"available {avail} ft vs required {req_ft:.2f} ft"))
        if not d.get("separation_basis"):
            checks.append(("separation basis cited", False, "cite the governing rule"))
    checks.append(("overflow path", bool(case.get("overflow_path")),
                   case.get("overflow_path", "not described; overflow is required")))
    return rows, checks


def main(argv=None):
    ap = argparse.ArgumentParser(description="Groundwater displacement and reinfiltration sizing")
    ap.add_argument("case_json")
    ap.add_argument("--out", help="CSV summary")
    a = ap.parse_args(argv)
    with open(a.case_json) as fh:
        case = json.load(fh)
    rows, checks = run(case)
    for r in rows:
        print(f"{r[0]:<50} {r[1]!s:>14} {r[2]:<7} {r[3]}")
    bad = 0
    for name, ok, msg in checks:
        print(f"CHECK {'MET    ' if ok else 'NOT MET'} {name}: {msg}")
        bad += 0 if ok else 1
    if a.out:
        with open(a.out, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["item", "value", "unit", "note"])
            w.writerows(rows)
            for name, ok, msg in checks:
                w.writerow([f"CHECK {name}", "MET" if ok else "NOT MET", "", msg])
        print("WROTE", a.out)
    return 0 if bad == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
