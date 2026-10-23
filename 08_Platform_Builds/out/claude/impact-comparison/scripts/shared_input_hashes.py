"""Hash-check the inputs that must be identical across compared conditions (HYD-C08 step 1). Pure Python.

  "%GIS_PY%" shared_input_hashes.py --folders <EX> <PR> [<ALT> ...]
      [--files CADPTS.DAT CONT.DAT TOLER.DAT INFLOW.DAT OUTFLOW.DAT RAIN.DAT FPXSEC.DAT CHAN.DAT XSEC.DAT FLOPRO.exe]
      [--out shared_input_hashes.json]

Default file list is the FLO-2D shared set. For HEC-RAS pass the files that must match (e.g. the unsteady
flow file, the perimeter / breakline shapefiles, the terrain .tif) - only terrain inside approved grading
surfaces and roughness / development may differ. Exit 1 if any listed file differs or is missing.
"""
import argparse
import hashlib
import json
import os
import sys

DEFAULT = ["CADPTS.DAT", "CONT.DAT", "TOLER.DAT", "INFLOW.DAT", "OUTFLOW.DAT", "RAIN.DAT", "FPXSEC.DAT",
           "CHAN.DAT", "XSEC.DAT", "CHANBANK.DAT", "FLOPRO.exe"]


def find_ci(folder, name):
    for f in os.listdir(folder):
        if f.upper() == name.upper():
            return os.path.join(folder, f)
    return None


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--folders", nargs="+", required=True)
    ap.add_argument("--files", nargs="+", default=DEFAULT)
    ap.add_argument("--out", default="shared_input_hashes.json")
    a = ap.parse_args(argv)
    table, bad = {}, []
    for name in a.files:
        row = {}
        for fo in a.folders:
            p = find_ci(fo, name)
            row[fo] = sha(p) if p else None
        table[name] = row
        vals = set(row.values())
        if len(vals) > 1 or None in vals:
            present = [v for v in row.values() if v]
            if present or len(vals) > 1:
                bad.append(name)
    rep = {"folders": a.folders, "hashes": table, "differ_or_missing": bad, "pass": not bad}
    with open(a.out, "w") as f:
        json.dump(rep, f, indent=2)
    print(json.dumps({"pass": rep["pass"], "differ_or_missing": bad}))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
