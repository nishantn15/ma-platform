"""
05_export_json.py
-----------------
Extends the leads.db schema with outreach state columns (idempotent — safe to re-run),
then exports the full leads table as JSON suitable for the static dashboard.

New columns added (if missing):
  - contact_attempts INTEGER DEFAULT 0
  - lead_owner TEXT
  - next_action TEXT
  - next_action_date TEXT
  - cfo_name TEXT
  - cs_name TEXT
  - ir_email TEXT
  - ir_phone TEXT

Outputs:
  ../../assets/leads.json     (consumed by /leads.html dashboard on the Pages site)
  ../output/leads_export.json (mirror for reference)

Run: python3 05_export_json.py
"""
import json
import sqlite3
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data"
OUT_DIR = SCRIPT_DIR.parent / "output"
OUT_DIR.mkdir(exist_ok=True)
REPO_ROOT = SCRIPT_DIR.parent.parent
ASSETS_DIR = REPO_ROOT / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "leads.db"

NEW_COLUMNS = [
    ("contact_attempts", "INTEGER DEFAULT 0"),
    ("lead_owner", "TEXT"),
    ("next_action", "TEXT"),
    ("next_action_date", "TEXT"),
    ("cfo_name", "TEXT"),
    ("cs_name", "TEXT"),
    ("ir_email", "TEXT"),
    ("ir_phone", "TEXT"),
]


def ensure_columns(conn):
    existing = {row[1] for row in conn.execute("PRAGMA table_info(leads)").fetchall()}
    added = 0
    for name, decl in NEW_COLUMNS:
        if name not in existing:
            conn.execute(f"ALTER TABLE leads ADD COLUMN {name} {decl}")
            added += 1
    conn.commit()
    return added


def main():
    if not DB_PATH.exists():
        print(f"DB not found: {DB_PATH}", file=sys.stderr)
        sys.exit(2)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    added = ensure_columns(conn)
    if added:
        print(f"[schema] added {added} new columns")

    # Use SELECT * so new v0.5 columns flow through automatically
    rows = conn.execute("""
        SELECT * FROM leads
        ORDER BY
          CASE tier
            WHEN 'T1' THEN 1 WHEN 'T2' THEN 2 WHEN 'T3' THEN 3
            WHEN 'skip' THEN 4 WHEN 'skip_financial' THEN 5 ELSE 6 END,
          COALESCE(acquisition_ready_score, tier_score) DESC NULLS LAST
    """).fetchall()
    conn.close()

    leads = [dict(row) for row in rows]

    # Merge AS research (M&A intel) fields per company, if the research table exists.
    research_fields = [
        "ma_deal_count_5y", "ma_deals_json", "parent_company", "promoter_holding_pct",
        "subsidiary_count", "subsidiaries_json", "minority_count", "minority_json",
        "cash_warchest_cr", "inorganic_intent_flag", "strategic_review_flag",
        "activist_flag", "signals_summary", "citation_count",
    ]
    try:
        rconn = sqlite3.connect(DB_PATH)
        rconn.row_factory = sqlite3.Row
        research = {}
        for r in rconn.execute("SELECT * FROM research WHERE query_type='ma_readiness'"):
            d = dict(r)
            research[d["nse_symbol"]] = {f: d.get(f) for f in research_fields}
        rconn.close()
        merged = 0
        for l in leads:
            rec = research.get(l["nse_symbol"])
            if rec:
                # prefix research keys so they're unambiguous in the dashboard
                for k, v in rec.items():
                    l["research_" + k] = v
                l["has_research"] = 1
                merged += 1
            else:
                l["has_research"] = 0
        print(f"[research] merged M&A intel into {merged} leads")
    except sqlite3.OperationalError:
        print("[research] no research table — skipping merge")

    # Summary stats
    by_tier = {}
    slow_count = 0
    compound_strong = 0
    compound_aligned = 0
    for r in leads:
        by_tier[r["tier"] or "untiered"] = by_tier.get(r["tier"] or "untiered", 0) + 1
        if r.get("slow_growth_signal"):
            slow_count += 1
        cf = r.get("ars_compound_flag")
        if cf == "strong":
            compound_strong += 1
        elif cf == "aligned":
            compound_aligned += 1

    payload = {
        "generated_at": __import__("time").strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(leads),
        "by_tier": by_tier,
        "slow_growth_count": slow_count,
        "compound_strong_count": compound_strong,
        "compound_aligned_count": compound_aligned,
        "research_count": sum(1 for l in leads if l.get("has_research")),
        "leads": leads,
    }

    main_out = ASSETS_DIR / "leads.json"
    main_out.write_text(json.dumps(payload, indent=2, default=str))
    mirror = OUT_DIR / "leads_export.json"
    mirror.write_text(json.dumps(payload, indent=2, default=str))

    print(f"[done] {len(leads)} leads exported")
    print(f"  primary: {main_out}")
    print(f"  mirror:  {mirror}")
    print(f"  tiers: {by_tier}")
    print(f"  slow-growth signal: {slow_count}")
    print(f"  compound: strong={compound_strong} aligned={compound_aligned}")


if __name__ == "__main__":
    main()
