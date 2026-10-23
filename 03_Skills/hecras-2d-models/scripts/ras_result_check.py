"""HEC-RAS 2D plan result acceptance check (decisions D05, D09; HYD-C09, HYD-C11). Read-only.

Environment: gis env (h5py, numpy).
  D:\\EKOS\\envs\\gis\\.venv\\Scripts\\python.exe ras_result_check.py <project.p##.hdf>
      [--final | --screening] [--vmax-fps 30] [--out result_check.json]

Refuses a *.tmp.hdf or a plan whose .tmp.hdf still exists beside it (RAS may be writing).
Reads compute messages (any string dataset whose name contains 'Compute Messages'), the volume
accounting attributes, and every 'Maximum Face Velocity' summary dataset. Reports:
  finished            'Finished Unsteady Flow Simulation' (or 'Finished Successfully') present
  volume_error_pct    from attributes or messages (abs value)
  iteration_warnings  count of message lines mentioning iteration / iterations warnings
  max_wsel_error_ft   largest number on message lines about max WSEL / water surface error
  max_face_velocity   per 2D area, value and face index
  accept              final: volume <= 0.1 pct; screening: <= 0.5 pct; plus finished, no velocity
                      above --vmax-fps (label diagnostic), and the residual/iteration items listed for JCO.
Message wording differs between RAS versions; anything not found is reported as null, never as a pass.
"""
import argparse
import json
import os
import re
import sys

import numpy as np

FIN_RE = re.compile(r"Finished Unsteady Flow Simulation|Finished Successfully", re.I)
VOL_RE = re.compile(r"volume.*?(?:error|accounting).*?(?:percent|percentage|%)\D{0,20}(-?\d+\.?\d*(?:E[-+]?\d+)?)", re.I)
ITER_RE = re.compile(r"iteration", re.I)
WSEL_RE = re.compile(r"(max(imum)?\s*(wsel|w\.?s\.?|water\s*surface).*error|error.*max(imum)?\s*(wsel|water\s*surface))", re.I)
NUM_RE = re.compile(r"-?\d+\.\d+(?:E[-+]?\d+)?", re.I)


def collect(h5):
    msgs, vel, vol_attrs = [], {}, {}

    def visit(name, obj):
        import h5py
        if isinstance(obj, h5py.Dataset):
            if "compute messages" in name.lower():
                data = obj[()]
                if isinstance(data, bytes):
                    msgs.append(data.decode("utf-8", "replace"))
                elif isinstance(data, np.ndarray):
                    for x in data.ravel():
                        msgs.append(x.decode("utf-8", "replace") if isinstance(x, bytes) else str(x))
            if name.lower().endswith("maximum face velocity"):
                arr = np.asarray(obj[()], dtype=float)
                vals = arr[0] if arr.ndim == 2 else arr
                vals = np.where(np.abs(vals) > 1e30, np.nan, vals)
                if vals.size and np.isfinite(vals).any():
                    i = int(np.nanargmax(np.abs(vals)))
                    area = name.split("/")[-2]
                    vel[area] = {"max_fps": round(float(abs(vals[i])), 3), "face_index": i, "dataset": name}
        if "volume accounting" in name.lower():
            for k, v in obj.attrs.items():
                vol_attrs[f"{name}:{k}"] = v.item() if hasattr(v, "item") else v

    h5.visititems(visit)
    return "\n".join(msgs), vel, vol_attrs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("hdf")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--final", action="store_true", default=True)
    g.add_argument("--screening", action="store_true")
    ap.add_argument("--vmax-fps", type=float, default=30.0)
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    import h5py

    if a.hdf.lower().endswith(".tmp.hdf") or os.path.exists(a.hdf[:-4] + ".tmp.hdf"):
        print(json.dumps({"refused": "temp HDF present; RAS may be writing. Never open an active .tmp.hdf."}))
        return 2
    if not os.path.exists(a.hdf):
        print(json.dumps({"refused": "plan HDF missing - run did not produce results (check geometry errors)"}))
        return 2
    with h5py.File(a.hdf, "r") as h5:
        text, vel, vol_attrs = collect(h5)

    rep = {"hdf": a.hdf, "mode": "screening" if a.screening else "final"}
    rep["finished"] = bool(FIN_RE.search(text))
    vol = None
    for k, v in vol_attrs.items():
        if re.search(r"error.*(percent|%)", k, re.I):
            try:
                vol = abs(float(v))
            except (TypeError, ValueError):
                pass
    if vol is None:
        m = VOL_RE.findall(text)
        if m:
            vol = max(abs(float(x)) for x in m)
    rep["volume_error_pct"] = vol
    lines = text.splitlines()
    rep["iteration_warnings"] = sum(1 for ln in lines if ITER_RE.search(ln) and re.search(r"warn|exceed|max", ln, re.I))
    wsel = [abs(float(n)) for ln in lines if WSEL_RE.search(ln) for n in NUM_RE.findall(ln)]
    rep["max_wsel_error_ft"] = max(wsel) if wsel else None
    rep["max_face_velocity"] = vel
    limit = 0.5 if a.screening else 0.1
    reasons = []
    if not rep["finished"]:
        reasons.append("finish message not found")
    if vol is None:
        reasons.append("volume error not found - read compute messages by hand")
    elif vol > limit:
        reasons.append(f"volume error {vol} pct > {limit} pct")
    spikes = {k: v for k, v in vel.items() if v["max_fps"] > a.vmax_fps}
    if spikes:
        reasons.append(f"max face velocity above {a.vmax_fps} fps - numerical spike? label diagnostic until checked")
    rep["for_jco"] = ["max WSEL residual and iteration warnings reviewed against the run",
                      "full end time reached (hydrograph tails, wet boundary)",
                      "saved velocity series checked before quoting a peak"]
    rep["accept"] = not reasons
    rep["reasons"] = reasons
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.hdf)),
                                os.path.basename(a.hdf).replace(".hdf", "_result_check.json"))
    with open(out, "w") as f:
        json.dump(rep, f, indent=2, default=str)
    print(json.dumps({k: rep[k] for k in ("finished", "volume_error_pct", "iteration_warnings",
                                          "max_wsel_error_ft", "accept", "reasons")}, default=str))
    return 0 if rep["accept"] else 1


if __name__ == "__main__":
    sys.exit(main())
