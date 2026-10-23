"""Template-driven .hy8 authoring and checks (decision D10; HYD-C20). Pure Python.

The only allowed source of keys, catalog codes (e.g. IRREGSIZE) and material enums is a .hy8 file saved by
HY-8 itself (the seed / template). This script never invents a key.

  fill   <template.hy8> <values.json> <out_INPUT.hy8>
         values.json = {"KEY": "value text", "KEY2": ["occ1 text", "occ2 text"], ...}
         Replaces the text after KEY on lines whose first token equals KEY exactly (whitespace boundary,
         so INLETEDGETYPE never matches INLETEDGETYPE71). A list sets successive occurrences; a string sets
         every occurrence. Unknown keys are an error. Output is CRLF.
  check  <template.hy8> <file.hy8> [--max-barrel-ft 30]
         CRLF everywhere, ENDPROJECTFILE present, every key in file exists in the template, key counts vs
         template, and a units warning when BARREL* numeric values look like inches (barrel data are
         stored in ft even when the UI shows in).
  diff   <a.hy8> <b.hy8>
         Line-by-line key/value differences (use to compare INPUT vs NATIVE after HY-8 saves it).

  "%HYDRAULICS_PY%" hy8_template.py check seed.hy8 INPUT_<crossing>.hy8
Exit 1 on any error.
"""
import argparse
import json
import re
import sys
from collections import Counter


def read_lines(path):
    raw = open(path, "rb").read()
    text = raw.decode("latin-1")
    return raw, text.replace("\r\n", "\n").split("\n")


def key_of(line):
    t = line.split(None, 1)
    return t[0] if t else ""


def cmd_fill(a):
    _, lines = read_lines(a.template)
    vals = json.load(open(a.values))
    tkeys = Counter(key_of(ln) for ln in lines)
    unknown = [k for k in vals if k not in tkeys]
    if unknown:
        print(json.dumps({"error": "keys not in template (never invent keys)", "keys": unknown}))
        return 1
    seen = Counter()
    out = []
    for ln in lines:
        k = key_of(ln)
        if k in vals:
            v = vals[k]
            idx = seen[k]
            seen[k] += 1
            if isinstance(v, list):
                if idx < len(v) and v[idx] is not None:
                    lead = re.match(r"^(\s*\S+)(\s+)", ln + " ")
                    ln = f"{lead.group(1)}{lead.group(2) if lead else ' '}{v[idx]}"
            else:
                lead = re.match(r"^(\s*\S+)(\s+)", ln + " ")
                ln = f"{lead.group(1)}{lead.group(2)}{v}"
        out.append(ln.rstrip())
    while out and out[-1] == "":
        out.pop()
    with open(a.out, "wb") as f:
        f.write(("\r\n".join(out) + "\r\n").encode("latin-1"))
    short = {k: (len(v), seen[k]) for k, v in vals.items() if isinstance(v, list) and len(v) != seen[k]}
    print(json.dumps({"written": a.out, "occurrence_count_mismatch": short}))
    return 0


def cmd_check(a):
    _, tl = read_lines(a.template)
    raw, fl = read_lines(a.file)
    errs, warns = [], []
    if re.search(rb"(?<!\r)\n", raw):
        errs.append("bare LF line endings (HY-8 files are CRLF)")
    if not any(key_of(ln) == "ENDPROJECTFILE" for ln in fl):
        errs.append("ENDPROJECTFILE missing")
    tk, fk = Counter(key_of(x) for x in tl if x.strip()), Counter(key_of(x) for x in fl if x.strip())
    extra = sorted(k for k in fk if k not in tk)
    if extra:
        errs.append({"keys not in template": extra[:50]})
    ratio = {k: (tk[k], fk[k]) for k in tk if fk.get(k, 0) and fk[k] % tk[k] != 0 and tk[k] > 1}
    if ratio:
        warns.append({"key counts not a multiple of template counts (check crossing blocks)": ratio})
    for ln in fl:
        k = key_of(ln)
        if k.startswith("BARREL"):
            nums = [float(x) for x in re.findall(r"-?\d+\.?\d*", ln[len(k):])]
            big = [x for x in nums if x > a.max_barrel_ft]
            if big:
                warns.append({"possible inches in ft field": ln.strip()[:120]})
    print(json.dumps({"pass": not errs, "errors": errs, "warnings": warns[:30]}, indent=2))
    return 0 if not errs else 1


def cmd_diff(a):
    _, al = read_lines(a.a)
    _, bl = read_lines(a.b)
    diffs = []
    for i in range(max(len(al), len(bl))):
        x = al[i].strip() if i < len(al) else "<none>"
        y = bl[i].strip() if i < len(bl) else "<none>"
        if x != y:
            diffs.append({"line": i + 1, "a": x[:160], "b": y[:160]})
    print(json.dumps({"n_diffs": len(diffs), "diffs": diffs[:200]}, indent=2))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("fill"); p.add_argument("template"); p.add_argument("values"); p.add_argument("out")
    p = sub.add_parser("check"); p.add_argument("template"); p.add_argument("file")
    p.add_argument("--max-barrel-ft", type=float, default=30.0)
    p = sub.add_parser("diff"); p.add_argument("a"); p.add_argument("b")
    a = ap.parse_args(argv)
    return {"fill": cmd_fill, "check": cmd_check, "diff": cmd_diff}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
