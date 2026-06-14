"""
10_ingest_research.py
---------------------
Upsert one AlphaSense research result into the `research` table.
Called after each as_search_auto MCP call. Reads a payload JSON
(written by the caller) containing the structured fields + brief md
+ citations, and upserts keyed on (nse_symbol, query_type).

Usage: python3 10_ingest_research.py <payload.json>

payload.json shape:
{
  "nse_symbol": "PTC",
  "query_type": "ma_readiness",
  "as_company_id": "TK226817",
  "as_conversation_id": "...",
  "structured": { ma_deal_count_5y, ma_deals, parent_company,
                  promoter_holding_pct, subsidiaries, minority,
                  cash_warchest_cr, inorganic_intent_flag,
                  strategic_review_flag, activist_flag, signals_summary },
  "brief_md": "...",
  "citations": [{n, source, date, title, url}],
  "mode": "auto", "credits_spent": 10, "generated_at": "2026-06-14 ..."
}
"""
import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "leads.db"


def to_int(v):
    if isinstance(v, bool):
        return 1 if v else 0
    try:
        return int(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: python3 10_ingest_research.py <payload.json>")
    payload = json.loads(Path(sys.argv[1]).read_text())
    s = payload.get("structured", {})

    subs = s.get("subsidiaries") or []
    minority = s.get("minority") or []
    deals = s.get("ma_deals") or []
    cites = payload.get("citations") or []

    row = {
        "nse_symbol": payload["nse_symbol"],
        "query_type": payload.get("query_type", "ma_readiness"),
        "as_company_id": payload.get("as_company_id"),
        "as_conversation_id": payload.get("as_conversation_id"),
        "ma_deal_count_5y": to_int(s.get("ma_deal_count_5y")) if s.get("ma_deal_count_5y") is not None else (len(deals) or None),
        "ma_deals_json": json.dumps(deals) if deals else None,
        "parent_company": s.get("parent_company"),
        "promoter_holding_pct": s.get("promoter_holding_pct"),
        "subsidiary_count": to_int(s.get("subsidiary_count")) if s.get("subsidiary_count") is not None else (len(subs) or None),
        "subsidiaries_json": json.dumps(subs) if subs else None,
        "minority_count": to_int(s.get("minority_count")) if s.get("minority_count") is not None else (len(minority) or None),
        "minority_json": json.dumps(minority) if minority else None,
        "cash_warchest_cr": s.get("cash_warchest_cr"),
        "inorganic_intent_flag": to_int(s.get("inorganic_intent_flag")),
        "strategic_review_flag": to_int(s.get("strategic_review_flag")),
        "activist_flag": to_int(s.get("activist_flag")),
        "signals_summary": s.get("signals_summary"),
        "brief_md": payload.get("brief_md"),
        "citations_json": json.dumps(cites) if cites else None,
        "citation_count": len(cites) or None,
        "mode": payload.get("mode"),
        "credits_spent": to_int(payload.get("credits_spent")),
        "generated_at": payload.get("generated_at"),
    }

    conn = sqlite3.connect(DB_PATH)
    cols = ",".join(row.keys())
    ph = ",".join("?" for _ in row)
    conn.execute(f"INSERT OR REPLACE INTO research ({cols}) VALUES ({ph})", list(row.values()))
    conn.commit()
    conn.close()
    print(f"[ingest] {row['nse_symbol']} — deals={row['ma_deal_count_5y']} "
          f"subs={row['subsidiary_count']} warchest={row['cash_warchest_cr']} "
          f"flags(intent/review/activist)={row['inorganic_intent_flag']}/"
          f"{row['strategic_review_flag']}/{row['activist_flag']} "
          f"cites={row['citation_count']}")


if __name__ == "__main__":
    main()
