"""
15_batch_ingest_contacts.py
---------------------------
Scan ~/as-outputs for EXHAUSTIVE-contact gensearch results, match each to
its NSE symbol via the "(NSE: XXX)" tag in the prompt, extract the fenced
JSON contact block, and ingest via 14_ingest_contacts.py. Newest file per
symbol wins. Idempotent.

Usage: python3 15_batch_ingest_contacts.py
"""
import json
import re
import subprocess
import sys
import sqlite3
from pathlib import Path

HOME = Path.home()
OUT = HOME / "as-outputs"
SCRIPTS = Path(__file__).resolve().parent
DB = SCRIPTS.parent / "data" / "leads.db"

# brace-matching extractor for the first balanced {...} that has a contact-ish key
def extract_json(md):
    # prefer fenced ```json blocks
    for m in re.finditer(r"```json\s*(\{.*?\})\s*```", md, re.S):
        try:
            return json.loads(m.group(1))
        except Exception:
            pass
    # fallback: scan for balanced braces containing "general_ir"
    i = 0
    while True:
        i = md.find("{", i)
        if i < 0:
            return None
        depth = 0
        for j in range(i, len(md)):
            if md[j] == "{":
                depth += 1
            elif md[j] == "}":
                depth -= 1
                if depth == 0:
                    blob = md[i:j + 1]
                    if "general_ir" in blob or "named_ir_contacts" in blob:
                        try:
                            return json.loads(blob)
                        except Exception:
                            break
                    break
        i += 1


def symbol_in_prompt(prompt):
    m = re.search(r"\(NSE:\s*([A-Z0-9&_-]+)\)", prompt or "")
    return m.group(1) if m else None


def main():
    files = sorted(OUT.glob("*EXHAUSTIVE_contact*.json"),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    # symbol -> AS id (for stamping)
    conn = sqlite3.connect(DB)
    asid = {r[0]: r[1] for r in conn.execute(
        "SELECT nse_symbol, as_company_id FROM research WHERE query_type='ma_readiness'")}
    conn.close()

    seen = set()
    ok = bad = 0
    for f in files:
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        sym = symbol_in_prompt((d.get("input") or {}).get("prompt", ""))
        if not sym or sym in seen:
            continue
        data = extract_json(d.get("markdown", ""))
        if not data:
            print(f"{sym}: no JSON block parsed"); bad += 1; seen.add(sym); continue
        data["nse_symbol"] = sym
        data.setdefault("as_company_id", asid.get(sym))
        payload = HOME / "tmp" / "contacts" / f"{sym}.json"
        payload.parent.mkdir(parents=True, exist_ok=True)
        payload.write_text(json.dumps(data))
        r = subprocess.run([sys.executable, str(SCRIPTS / "14_ingest_contacts.py"),
                            str(payload)], capture_output=True, text=True)
        out = (r.stdout or r.stderr).strip()
        print(out or f"{sym}: ingest produced no output")
        seen.add(sym); ok += 1
    print(f"\n[batch] ingested {ok} contact rows ({bad} unparsed)")


if __name__ == "__main__":
    main()
