"""
09_research_schema.py
---------------------
Creates the `research` table in leads.db to hold AlphaSense-sourced
M&A intelligence per company (TK June-6 #2/#3/#4). One row per
(nse_symbol, query_type). Structured fields for the dashboard +
full markdown + citations for humans + audit trail.

Idempotent: CREATE TABLE IF NOT EXISTS.
Run: python3 09_research_schema.py
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "leads.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS research (
    nse_symbol            TEXT NOT NULL,
    query_type            TEXT NOT NULL DEFAULT 'ma_readiness',
    as_company_id         TEXT,
    as_conversation_id    TEXT,
    -- TK #2 Recent M&A activity (last 5y)
    ma_deal_count_5y      INTEGER,
    ma_deals_json         TEXT,      -- [{type, counterparty, value_cr, date, direction}]
    -- TK #3 Company profile
    parent_company        TEXT,
    promoter_holding_pct  REAL,
    subsidiary_count      INTEGER,
    subsidiaries_json     TEXT,      -- [{name, stake_pct, note}]
    minority_count        INTEGER,
    minority_json         TEXT,      -- [{name, stake_pct}]
    -- TK #4 Capital-allocation / inorganic signals (ARS robustness)
    cash_warchest_cr      REAL,
    inorganic_intent_flag INTEGER,   -- 0/1 management stated inorganic appetite
    strategic_review_flag INTEGER,   -- 0/1 active strategic review / divestiture
    activist_flag         INTEGER,   -- 0/1 activist / governance pressure
    signals_summary       TEXT,      -- one-line human summary
    -- Raw payload
    brief_md              TEXT,
    citations_json        TEXT,      -- [{n, source, date, title, url}]
    citation_count        INTEGER,
    -- Meta
    mode                  TEXT,      -- fast|auto|thinkLonger|deep
    credits_spent         INTEGER,
    generated_at          TEXT,
    PRIMARY KEY (nse_symbol, query_type)
);
"""


def main():
    if not DB_PATH.exists():
        raise SystemExit(f"DB not found: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.commit()
    cols = [r[1] for r in conn.execute("PRAGMA table_info(research)").fetchall()]
    print(f"[schema] research table ready — {len(cols)} columns")
    print("  " + ", ".join(cols))
    conn.close()


if __name__ == "__main__":
    main()
