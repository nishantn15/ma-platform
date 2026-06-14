"""
11_parse_as_output.py
---------------------
Parse a saved AlphaSense gensearch output JSON (~/as-outputs/*.json) into
an ingest payload for 10_ingest_research.py. Extracts:
  - the fenced ```json structured block (or first {...} block)
  - the prose brief markdown (everything, citations kept)
  - citations parsed from the [[n • Source • date • "title"]](url) footer

Usage:
  python3 11_parse_as_output.py <as_output.json> <nse_symbol> <as_company_id> \
      [--mode auto] [--credits 10] [--out payload.json]
"""
import json
import re
import sys
import time
from pathlib import Path


def extract_json_block(md):
    # Prefer a fenced ```json ... ``` block
    m = re.search(r"```json\s*(\{.*?\})\s*```", md, re.DOTALL)
    if not m:
        m = re.search(r"```\s*(\{.*?\})\s*```", md, re.DOTALL)
    if not m:
        # fall back: first balanced-looking {...} with our key
        m = re.search(r"(\{[^{}]*\"ma_deal_count_5y\".*?\})", md, re.DOTALL)
    if not m:
        return {}
    raw = m.group(1)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # tolerate trailing commas
        cleaned = re.sub(r",(\s*[}\]])", r"\1", raw)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {}


def extract_citations(md):
    """Parse the citation footer lines like:
    [[7] ARS • Company • 14 Jul 25 • "title"](url)
    and inline [[1 • Source]](url). Returns deduped list."""
    cites = {}
    # full form with title
    for m in re.finditer(
        r"\[\[(\d+)\]([^\]]*?)\]\((https?://[^)]+)\)", md
    ):
        n = int(m.group(1))
        meta = m.group(2).strip(" •")
        url = m.group(3)
        if n not in cites:
            cites[n] = {"n": n, "meta": meta, "url": url}
    # inline form [[1 • Source]](url)
    for m in re.finditer(r"\[\[(\d+)\s*•\s*([^\]]+?)\]\((https?://[^)]+)\)", md):
        n = int(m.group(1))
        if n not in cites or not cites[n].get("meta"):
            cites[n] = {"n": n, "meta": m.group(2).strip(), "url": m.group(3)}
    return [cites[k] for k in sorted(cites)]


def strip_json_block(md):
    """Remove the leading fenced json block so brief_md is prose-only-ish."""
    return re.sub(r"```json\s*\{.*?\}\s*```\s*", "", md, count=1, flags=re.DOTALL)


def main():
    args = sys.argv[1:]
    if len(args) < 3:
        raise SystemExit("usage: 11_parse_as_output.py <as_output.json> <nse_symbol> <as_company_id> [--mode m] [--credits n] [--out f]")
    src, symbol, company_id = args[0], args[1], args[2]
    mode = "auto"; credits = 10; out = None
    for i, a in enumerate(args):
        if a == "--mode": mode = args[i + 1]
        elif a == "--credits": credits = int(args[i + 1])
        elif a == "--out": out = args[i + 1]

    data = json.loads(Path(src).read_text())
    md = data.get("markdown", "")
    structured = extract_json_block(md)
    citations = extract_citations(md)

    payload = {
        "nse_symbol": symbol,
        "query_type": "ma_readiness",
        "as_company_id": company_id,
        "as_conversation_id": data.get("conversation_id"),
        "structured": structured,
        "brief_md": strip_json_block(md).strip(),
        "citations": citations,
        "mode": mode,
        "credits_spent": credits,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    out = out or f"/tmp/payload_{symbol}.json"
    Path(out).write_text(json.dumps(payload, indent=2))
    print(f"[parse] {symbol}: structured_keys={len(structured)} citations={len(citations)} -> {out}")
    # quick sanity echo
    print(f"  deals={structured.get('ma_deal_count_5y')} parent={structured.get('parent_company')} "
          f"warchest={structured.get('cash_warchest_cr')} "
          f"flags={structured.get('inorganic_intent_flag')}/{structured.get('strategic_review_flag')}/{structured.get('activist_flag')}")


if __name__ == "__main__":
    main()
