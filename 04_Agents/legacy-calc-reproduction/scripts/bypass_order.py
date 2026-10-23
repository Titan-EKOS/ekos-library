"""Order inlet runs for bypass chains and check flow balance (legacy-calc-reproduction, HYD-C21 step 3).

Input CSV columns (one row per inlet):
  inlet_id, bypass_to, local_q_cfs[, captured_q_cfs, bypass_q_cfs]
- bypass_to: inlet that receives this inlet's bypass ('' or 'NONE' = leaves the system, e.g. to a channel).
- local_q_cfs: verified local runoff to this inlet only (never the upstream total).
- captured_q_cfs / bypass_q_cfs: optional native results, filled after each native run.

  python bypass_order.py inlets.csv                 -> run order upstream to downstream (JSON)
  python bypass_order.py inlets.csv --check         -> also flow balance per inlet from native results
  python bypass_order.py inlets.csv --out order.csv -> writes run order with the approach flow formula per inlet

Approach flow at an inlet = local_q + sum(bypass_q of inlets that bypass to it). Full upstream flow is never
duplicated at a downstream inlet. Exit code 1 on a cycle, an unknown bypass target, or a balance error > --tol.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict, deque


def load(path: str) -> dict[str, dict]:
    rows = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            iid = (r.get("inlet_id") or "").strip()
            if not iid:
                continue
            if iid in rows:
                raise ValueError(f"duplicate inlet_id {iid}")
            tgt = (r.get("bypass_to") or "").strip()
            rows[iid] = {
                "bypass_to": "" if tgt.upper() in ("", "NONE") else tgt,
                "local_q": float(r.get("local_q_cfs") or 0),
                "captured": float(r["captured_q_cfs"]) if (r.get("captured_q_cfs") or "").strip() else None,
                "bypass": float(r["bypass_q_cfs"]) if (r.get("bypass_q_cfs") or "").strip() else None,
            }
    return rows


def order(rows: dict[str, dict]) -> tuple[list[str], list[str], dict]:
    errors = []
    upstream = defaultdict(list)
    indeg = {k: 0 for k in rows}
    for k, r in rows.items():
        t = r["bypass_to"]
        if t:
            if t not in rows:
                errors.append(f"{k} bypasses to unknown inlet {t}")
                continue
            upstream[t].append(k)
            indeg[t] += 1
    q = deque(sorted(k for k, d in indeg.items() if d == 0))
    seq = []
    while q:
        k = q.popleft()
        seq.append(k)
        t = rows[k]["bypass_to"]
        if t in indeg:
            indeg[t] -= 1
            if indeg[t] == 0:
                q.append(t)
    if len(seq) < len(rows):
        errors.append("bypass cycle among: " + ", ".join(sorted(set(rows) - set(seq))))
    return seq, errors, upstream


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--tol", type=float, default=0.01, help="balance tolerance, cfs")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    try:
        rows = load(a.csv)
    except (OSError, ValueError) as e:
        print(json.dumps({"error": str(e)}))
        return 2
    seq, errors, upstream = order(rows)
    res = {"run_order": seq, "errors": errors, "inlets": []}
    for k in seq:
        ups = sorted(upstream.get(k, []))
        rec = {"inlet_id": k, "receives_bypass_from": ups, "bypass_to": rows[k]["bypass_to"] or "NONE",
               "approach_formula": "local" + "".join(f" + bypass({u})" for u in ups)}
        if a.check:
            byp_in = [rows[u]["bypass"] for u in ups]
            if None in byp_in or rows[k]["captured"] is None or rows[k]["bypass"] is None:
                rec["balance"] = "native results missing - run upstream inlets first"
            else:
                approach = rows[k]["local_q"] + sum(byp_in)
                diff = approach - rows[k]["captured"] - rows[k]["bypass"]
                rec.update({"approach_q": round(approach, 3), "balance_diff": round(diff, 3)})
                if abs(diff) > a.tol:
                    errors.append(f"{k}: approach {approach:.2f} != captured + bypass "
                                  f"({rows[k]['captured']:.2f} + {rows[k]['bypass']:.2f})")
        res["inlets"].append(rec)
    if a.out:
        with open(a.out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["run_seq", "inlet_id", "receives_bypass_from", "bypass_to", "approach_formula"])
            for i, rec in enumerate(res["inlets"], 1):
                w.writerow([i, rec["inlet_id"], ";".join(rec["receives_bypass_from"]), rec["bypass_to"],
                            rec["approach_formula"]])
    print(json.dumps(res, indent=1))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
