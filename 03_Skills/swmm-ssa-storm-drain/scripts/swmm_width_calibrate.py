"""Calibrate SWMM subcatchment width to agency target peaks (HYD-C22). Environment: hydro env with
swmm-toolkit (EPA SWMM 5.2.x engine).

For each storm case, bisects the width of one subcatchment in log space on a runoff-only model until the
modeled peak runoff matches the target, then reports the geometric mean of the storm widths and the fit of
that single width against every target (pass within --tol, default 10 pct).

  D:\\EKOS\\envs\\hydro\\.venv\\Scripts\\python.exe swmm_width_calibrate.py --sub S1
      --case runoff_10yr.inp 0.42 --case runoff_25yr.inp 0.61 --case runoff_100yr.inp 0.90
      [--lo 1 --hi 100000 --iters 26 --tol 0.10 --out width_calibration.json]

Model set-up expected (done before calling): constant-rate infiltration (Horton f0 = fc = agency table rate,
decay 0), no depression storage, the subcatchment outlet to an outfall, one inp per storm.
Calibrate pre-condition and post-condition catchments separately, each against its own targets.
"""
import argparse
import json
import math
import os
import re
import shutil
import sys
import tempfile


def set_width(inp_text, sub, width):
    out, in_sec, done = [], False, False
    for line in inp_text.splitlines():
        s = line.strip()
        if s.startswith("["):
            in_sec = s.upper() == "[SUBCATCHMENTS]"
        elif in_sec and s and not s.startswith(";"):
            t = line.split()
            if t[0] == sub and len(t) >= 7:
                t[5] = f"{width:.6g}"  # Name RainGage Outlet Area %Imperv Width %Slope CurbLen [SnowPack]
                line = "  ".join(t)
                done = True
        out.append(line)
    if not done:
        raise ValueError(f"subcatchment {sub} not found in [SUBCATCHMENTS]")
    # Calibration copy only: save this subcatchment in the binary output (SWMM saves none by default).
    out += ["", "[REPORT]", f"SUBCATCHMENTS {sub}"]
    return "\r\n".join(out) + "\r\n"


def peak_from_rpt(rpt, sub):
    text = open(rpt, errors="replace").read()
    m = re.search(r"Subcatchment Runoff Summary(.*?)(\n\s*\n\s*\*{5,}|\Z)", text, re.S)
    if not m:
        raise RuntimeError("Subcatchment Runoff Summary not found in report; check the run for errors:\n" + text[-2000:])
    for line in m.group(1).splitlines():
        t = line.split()
        if t and t[0] == sub:
            return float(t[-2])  # columns end with Peak Runoff, Runoff Coeff
    raise RuntimeError(f"{sub} not in Subcatchment Runoff Summary")


def peak_from_out(outfile, sub):
    """Max runoff rate at the report step from the binary output (full precision; the .rpt table rounds
    small peaks to 0.01 cfs). Set REPORT_STEP to 1 min or less in the calibration models."""
    from swmm.toolkit import output, shared_enum as se
    h = output.init()
    output.open(h, outfile)
    try:
        n_sub = output.get_proj_size(h)[0]
        idx = next(i for i in range(n_sub) if output.get_elem_name(h, se.ElementType.SUBCATCH, i) == sub)
        n = output.get_times(h, se.Time.NUM_PERIODS)
        return max(output.get_subcatch_series(h, idx, se.SubcatchAttribute.RUNOFF_RATE, 0, n - 1))
    finally:
        output.close(h)


def quiet_run(inp, rpt, out):
    """Run the engine with its console progress lines sent to the null device."""
    from swmm.toolkit import solver
    sys.stdout.flush()
    saved = os.dup(1)
    null = os.open(os.devnull, os.O_WRONLY)
    try:
        os.dup2(null, 1)
        solver.swmm_run(inp, rpt, out)
    finally:
        os.dup2(saved, 1)
        os.close(null)
        os.close(saved)


def run_peak(inp_text, sub, width, work):
    inp = os.path.join(work, "cal.inp")
    rpt, out = inp[:-4] + ".rpt", inp[:-4] + ".out"
    with open(inp, "w", newline="") as f:
        f.write(set_width(inp_text, sub, width))
    quiet_run(inp, rpt, out)
    try:
        return peak_from_out(out, sub)
    except Exception:
        return peak_from_rpt(rpt, sub)


def bisect(inp_text, sub, target, lo, hi, iters, work):
    a, b = math.log(lo), math.log(hi)
    pa, pb = run_peak(inp_text, sub, lo, work), run_peak(inp_text, sub, hi, work)
    if not (pa <= target <= pb):
        return None, {"error": "target outside peak range at width bounds", "peak_lo": pa, "peak_hi": pb}
    for _ in range(iters):
        m = (a + b) / 2
        if run_peak(inp_text, sub, math.exp(m), work) < target:
            a = m
        else:
            b = m
    w = math.exp((a + b) / 2)
    return w, {"width_ft": round(w, 3), "peak_cfs": round(run_peak(inp_text, sub, w, work), 4)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sub", required=True)
    ap.add_argument("--case", nargs=2, action="append", metavar=("INP", "TARGET_CFS"), required=True)
    ap.add_argument("--lo", type=float, default=1.0)
    ap.add_argument("--hi", type=float, default=1e5)
    ap.add_argument("--iters", type=int, default=26)
    ap.add_argument("--tol", type=float, default=0.10)
    ap.add_argument("--out", default="width_calibration.json")
    a = ap.parse_args(argv)
    work = tempfile.mkdtemp(prefix="swmmcal_")
    rep = {"subcatchment": a.sub, "storms": []}
    widths = []
    try:
        for inp, tgt in a.case:
            text = open(inp, errors="replace").read()
            w, info = bisect(text, a.sub, float(tgt), a.lo, a.hi, a.iters, work)
            info.update({"inp": inp, "target_cfs": float(tgt)})
            rep["storms"].append(info)
            if w:
                widths.append(w)
        if widths and len(widths) == len(a.case):
            gm = math.exp(sum(math.log(w) for w in widths) / len(widths))
            rep["geomean_width_ft"] = round(gm, 3)
            fits = []
            for inp, tgt in a.case:
                pk = run_peak(open(inp, errors="replace").read(), a.sub, gm, work)
                err = (pk - float(tgt)) / float(tgt)
                fits.append({"inp": inp, "target_cfs": float(tgt), "peak_cfs": round(pk, 4), "error_pct": round(100 * err, 1)})
            rep["fit"] = fits
            rep["pass"] = all(abs(f["error_pct"]) <= 100 * a.tol for f in fits)
        else:
            rep["pass"] = False
    finally:
        shutil.rmtree(work, ignore_errors=True)
    with open(a.out, "w") as f:
        json.dump(rep, f, indent=2)
    print(json.dumps(rep, indent=2))
    return 0 if rep.get("pass") else 1


if __name__ == "__main__":
    sys.exit(main())
