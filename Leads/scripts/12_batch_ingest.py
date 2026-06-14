"""
12_batch_ingest.py
-------------------
Scan ~/as-outputs for M&A-readiness gensearch results, match each to a
T1 ticker by the company name in the prompt, parse + ingest into the
research table. Idempotent (INSERT OR REPLACE). No grep, no shell globs.

Usage: python3 12_batch_ingest.py
Reads the ticker->(as_id, name-substring) map below.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
OUT = HOME / "as-outputs"
SCRIPTS = Path(__file__).resolve().parent

# ticker: (as_company_id, name substring to match in the prompt)
T1 = {
    "GLENMARK": ("TK61665", "Glenmark"),
    "BIOCON": ("TK226997", "Biocon"),
    "DRREDDY": ("TK112871", "Dr Reddy"),
    "INFY": ("TK179981", "Infosys"),
    "MARICO": ("TK448632", "Marico"),
    "ASIANPAINT": ("TK523533", "Asian Paints"),
    "TCS": ("TK242393", "Tata Consultancy"),
    "BRITANNIA": ("TK523774", "Britannia"),
    "HYUNDAI": ("TK971018", "Hyundai"),
    "TATACONSUM": ("TK536231", "Tata Consumer"),
    "HINDUNILVR": ("TK532742", "Hindustan Unilever"),
    "CRISIL": ("TK219296", "CRISIL"),
    "LT": ("TK758735", "Larsen"),
    "SUNPHARMA": ("TK290076", "Sun Pharm"),
    "ITC": ("TK716833", "ITC Ltd"),
    "PAYTM": ("TK534185", "One97"),
    "MOTHERSON": ("TK240411", "Motherson"),
    "PIDILITIND": ("TK207274", "Pidilite"),
    "NESTLEIND": ("TK758734", "Nestle India"),
    "M&M": ("TK527972", "Mahindra"),
    "HEROMOTOCO": ("TK758669", "Hero MotoCorp"),
    "CUMMINSIND": ("TK719426", "Cummins"),
    "LODHA": ("TK522435", "Lodha"),
    "MAZDOCK": ("TK860487", "Mazagon"),
    "POWERINDIA": ("TK814499", "Hitachi"),
    "BAJAJ-AUTO": ("TK380146", "Bajaj Auto"),
    "PTC": ("TK226817", "PTC India"),
}


def company_in_prompt(path):
    try:
        d = json.loads(path.read_text())
    except Exception:
        return None
    prompt = (d.get("input") or {}).get("prompt", "")
    m = re.search(r"profile for ([^(]+)\(", prompt)
    return m.group(1).strip() if m else None


def main():
    # newest first so re-runs pick the latest result per company
    files = sorted(OUT.glob("*M_A-readiness*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    done = set()
    for tkr, (cid, sub) in T1.items():
        if tkr in done:
            continue
        match = None
        for f in files:
            co = company_in_prompt(f) or ""
            if sub.lower() in co.lower():
                match = f
                break
        if not match:
            print(f"{tkr}: no file yet")
            continue
        payload = HOME / "tmp" / "payloads" / f"{tkr}.json"
        payload.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, str(SCRIPTS / "11_parse_as_output.py"),
                        str(match), tkr, cid, "--out", str(payload)],
                       capture_output=True)
        r = subprocess.run([sys.executable, str(SCRIPTS / "10_ingest_research.py"),
                            str(payload)], capture_output=True, text=True)
        print(r.stdout.strip() or f"{tkr}: ingest produced no output")
        done.add(tkr)


if __name__ == "__main__":
    main()
