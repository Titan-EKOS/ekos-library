#!/usr/bin/env python3
"""
extract_basin_inputs.py  -- Phase 1 of the PC-Hydro skill.

Pull watershed/basin parameters and any reported peak flows out of a drainage
report (PDF / .xlsx / .docx) so they can (a) drive PC-Hydro runs and (b) be used
to QC the resulting hydrographs against the approved report.

Emits two files next to --out-stem:
  <stem>_basin_inputs.csv   one row per basin, best-effort parsed parameters
  <stem>_report_text.txt    raw extracted text (for manual review / regex tuning)

Recognised fields (label-matched, units noted): basin/watershed ID, drainage
area (ac or sq mi), curve number CN, runoff coefficient C, time of
concentration Tc (min), lag (min), % impervious, and peak Q by return period
(Q2..Q500). Parsing is heuristic -- always eyeball the CSV before running PC-Hydro.

Usage:
  python3 extract_basin_inputs.py --in report.pdf --out-stem ./PROJ_CP
  python3 extract_basin_inputs.py --in calcs.xlsx --out-stem ./PROJ_CP
"""
import argparse, csv, os, re, sys, subprocess

def read_pdf(p):
    try:
        import pdfplumber
        with pdfplumber.open(p) as pdf:
            return "\n".join((pg.extract_text() or "") for pg in pdf.pages)
    except Exception:
        try:
            return subprocess.run(["pdftotext","-layout",p,"-"],
                                  capture_output=True,text=True).stdout
        except Exception as e:
            sys.exit(f"PDF read failed (install pdfplumber or poppler): {e}")

def read_docx(p):
    try:
        import docx
    except Exception:
        sys.exit("python-docx not installed: pip install python-docx")
    d=docx.Document(p); out=[]
    for para in d.paragraphs: out.append(para.text)
    for t in d.tables:
        for row in t.rows:
            out.append("\t".join(c.text for c in row.cells))
    return "\n".join(out)

def read_xlsx(p):
    try:
        import openpyxl
    except Exception:
        sys.exit("openpyxl not installed: pip install openpyxl")
    wb=openpyxl.load_workbook(p,data_only=True); out=[]
    for ws in wb.worksheets:
        out.append(f"### SHEET {ws.title}")
        for row in ws.iter_rows(values_only=True):
            out.append("\t".join("" if v is None else str(v) for v in row))
    return "\n".join(out)

def get_text(p):
    e=os.path.splitext(p)[1].lower()
    if e==".pdf":  return read_pdf(p)
    if e==".docx": return read_docx(p)
    if e in (".xlsx",".xlsm"): return read_xlsx(p)
    if e in (".txt",".csv"):   return open(p,errors="ignore").read()
    sys.exit(f"Unsupported input type: {e}")

NUM=r"([\d,]+\.?\d*)"
def f(m): return float(m.group(1).replace(",","")) if m else None

PATTERNS={
 "drainage_area": re.compile(r"(?:drainage\s*area|area)\D{0,20}"+NUM+r"\s*(ac|acre|sq\.?\s*mi|mi2|mi²)?",re.I),
 "CN":            re.compile(r"\bCN\b\D{0,10}"+NUM,re.I),
 "C_coeff":       re.compile(r"runoff\s*coeff\w*\D{0,15}"+NUM,re.I),
 "Tc_min":        re.compile(r"(?:time\s*of\s*conc\w*|\bTc\b)\D{0,15}"+NUM,re.I),
 "lag_min":       re.compile(r"\blag\b\D{0,15}"+NUM,re.I),
 "pct_imperv":    re.compile(r"impervious\D{0,15}"+NUM,re.I),
}
RP=re.compile(r"Q\s*[-_]?\s*(500|200|100|50|25|10|5|2)(?!\d)\D{0,8}"+NUM,re.I)

def parse(text):
    row={k:f(p.search(text)) for k,p in PATTERNS.items()}
    bid=re.search(r"(?:watershed|basin|sub-?basin|WS)\s*#?\s*([A-Za-z0-9\-]+)",text,re.I)
    row["basin_id"]=bid.group(1) if bid else ""
    for rp,val in RP.findall(text):
        row[f"Q{rp}"]=float(val.replace(",",""))
    return row

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--in",dest="inp",required=True)
    ap.add_argument("--out-stem",required=True)
    a=ap.parse_args()
    text=get_text(a.inp)
    open(a.out_stem+"_report_text.txt","w").write(text)
    row=parse(text)
    cols=["basin_id","drainage_area","CN","C_coeff","Tc_min","lag_min","pct_imperv",
          "Q2","Q5","Q10","Q25","Q50","Q100","Q200","Q500"]
    w=csv.DictWriter(open(a.out_stem+"_basin_inputs.csv","w",newline=""),fieldnames=cols)
    w.writeheader(); w.writerow({c:row.get(c,"") for c in cols})
    print("WROTE",a.out_stem+"_basin_inputs.csv")
    print("WROTE",a.out_stem+"_report_text.txt  (review & refine regex if fields are blank)")
    print("Parsed:",{k:v for k,v in row.items() if v not in ("",None)})

if __name__=="__main__": main()
