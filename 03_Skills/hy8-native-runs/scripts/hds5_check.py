"""Independent HDS-5 culvert headwater check (internal QC only; decision D30 - file in 40_QC, never in a
deliverable). Concrete circular and box barrels, inlet and outlet control. Pure Python, US units.

  "%HYDRAULICS_PY%" hds5_check.py --shape box --span 10 --rise 4 --barrels 3
      --length 120 --slope 0.01 --n 0.012 --ke 0.5 --inlet box_90_15 --q 450 --tw 3.2 [--q-list 100 200]

Inlet control: HDS-5 (FHWA, 3rd ed., 2012) equations 1 (unsubmerged, form 1), 3 (submerged), linear
transition between Q/(A D^0.5) = 3.5 and 4.0; Ku = 1.0, slope term Ks = -0.5 (use +0.7 for mitered inlets).
Outlet control: HW = ho + H - S L, H = (1 + ke + 29 n^2 L / R^1.33) V^2 / 2g, ho = max(TW, (dc + D)/2).
Coefficients: check the row against HDS-5 Appendix C for the inlet in use before relying on a result.
Compare with HY-8: stop and reconcile if HW differs by more than 0.2 ft or outlet velocity by 0.5 fps.
"""
import argparse
import json
import math
import sys

G = 32.2
INLETS = {
    # key: (form, K, M, c, Y)  - HDS-5 Appendix C, form 1 coefficients
    "pipe_square_headwall": (1, 0.0098, 2.0, 0.0398, 0.67),
    "pipe_groove_headwall": (1, 0.0018, 2.0, 0.0292, 0.74),
    "pipe_groove_projecting": (1, 0.0045, 2.0, 0.0317, 0.69),
    "box_30_75_wingwall": (1, 0.026, 1.0, 0.0347, 0.81),
    "box_90_15_wingwall": (1, 0.061, 0.75, 0.0400, 0.80),
    "box_0_wingwall": (1, 0.061, 0.75, 0.0423, 0.82),
}


def circ_area(D, y):
    y = min(max(y, 0.0), D)
    th = 2 * math.acos(1 - 2 * y / D)
    A = D * D / 8 * (th - math.sin(th))
    T = D * math.sin(th / 2)
    P = D * th / 2
    return A, T, P


def critical_depth(shape, q, span, D):
    """q = flow per barrel (cfs)."""
    if shape == "box":
        return min((q / span) ** 2 / G, 1e9) ** (1 / 3)
    lo, hi = 1e-4, D * 0.9999
    for _ in range(100):
        y = (lo + hi) / 2
        A, T, _ = circ_area(D, y)
        if q * q * T / (G * A ** 3) > 1:
            lo = y
        else:
            hi = y
    return (lo + hi) / 2


def full_props(shape, span, D):
    if shape == "box":
        A = span * D
        P = 2 * (span + D)
    else:
        A = math.pi * D * D / 4
        P = math.pi * D
    return A, A / P


def inlet_hw(shape, inlet, q, span, D, S):
    form, K, M, c, Y = INLETS[inlet]
    A, _ = full_props(shape, span, D)
    x = q / (A * D ** 0.5)
    dc = min(critical_depth(shape, q, span, D), D)
    if shape == "box":
        Ac = span * dc
    else:
        Ac = circ_area(D, dc)[0]
    Hc = dc + (q / Ac) ** 2 / (2 * G)
    ks = -0.5
    unsub = D * (Hc / D + K * x ** M + ks * S)
    sub = D * (c * x * x + Y + ks * S)
    if x <= 3.5:
        return unsub, x, "unsubmerged"
    if x >= 4.0:
        return sub, x, "submerged"
    f = (x - 3.5) / 0.5
    return unsub + f * (sub - unsub), x, "transition"


def outlet_hw(shape, q, span, D, L, S, n, ke, tw):
    A, R = full_props(shape, span, D)
    V = q / A
    H = (1 + ke + 29 * n * n * L / R ** 1.33) * V * V / (2 * G)
    dc = min(critical_depth(shape, q, span, D), D)
    ho = max(tw, (dc + D) / 2)
    return ho + H - S * L, V


def run(a, Q):
    q = Q / a.barrels
    D = a.rise if a.shape == "box" else a.diameter
    span = a.span if a.shape == "box" else D
    hwi, x, regime = inlet_hw(a.shape, a.inlet, q, span, D, a.slope)
    hwo, vfull = outlet_hw(a.shape, q, span, D, a.length, a.slope, a.n, a.ke, a.tw)
    ctrl = "inlet" if hwi >= hwo else "outlet"
    return {"Q_cfs": Q, "q_per_barrel_cfs": round(q, 2), "Q_over_AD05": round(x, 3), "inlet_regime": regime,
            "HW_inlet_ft": round(hwi, 2), "HW_outlet_ft": round(hwo, 2), "HW_ft": round(max(hwi, hwo), 2),
            "control": ctrl, "V_full_fps": round(vfull, 2),
            "note": "outlet velocity in HY-8 uses outlet depth; compare V with HY-8 at the same depth basis"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--shape", choices=["box", "pipe"], required=True)
    ap.add_argument("--span", type=float, help="box span ft")
    ap.add_argument("--rise", type=float, help="box rise ft")
    ap.add_argument("--diameter", type=float, help="pipe diameter ft")
    ap.add_argument("--barrels", type=int, default=1)
    ap.add_argument("--length", type=float, required=True)
    ap.add_argument("--slope", type=float, required=True)
    ap.add_argument("--n", type=float, default=0.012)
    ap.add_argument("--ke", type=float, default=0.5)
    ap.add_argument("--inlet", choices=sorted(INLETS), required=True)
    ap.add_argument("--tw", type=float, default=0.0, help="tailwater depth above outlet invert, ft")
    ap.add_argument("--q", type=float, nargs="+", required=True)
    a = ap.parse_args(argv)
    if a.shape == "box" and not (a.span and a.rise):
        ap.error("box needs --span and --rise")
    if a.shape == "pipe" and not a.diameter:
        ap.error("pipe needs --diameter")
    if a.shape == "box" and a.inlet.startswith("pipe") or a.shape == "pipe" and a.inlet.startswith("box"):
        ap.error("inlet type does not match shape")
    print(json.dumps({"label": "INTERNAL QC - independent HDS-5 check, not for the deliverable",
                      "results": [run(a, Q) for Q in a.q]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
