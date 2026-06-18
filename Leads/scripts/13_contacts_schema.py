"""
13_contacts_schema.py
---------------------
Creates the `contacts` table in leads.db — full outreach contact object
per company, sourced from AlphaSense (TK feedback #2). One row per
nse_symbol. Every field is publicly-disclosed corporate data; named-exec
direct emails only when literally published (never name+domain guessed).
Provenance (source doc + date + confidence) travels with each record so
the sheet stays defensible.

Idempotent: CREATE TABLE IF NOT EXISTS.
Run: python3 13_contacts_schema.py
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "leads.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS contacts (
    nse_symbol           TEXT PRIMARY KEY,
    as_company_id        TEXT,
    -- General investor-relations desk (always literally published)
    ir_inbox_email       TEXT,      -- e.g. investors@company.com / secretarial@
    ir_phone             TEXT,
    -- Named people (role always published; direct email only if literal)
    ir_head_name         TEXT,
    ir_head_title        TEXT,
    ir_head_email        TEXT,      -- direct, only when literally disclosed
    ir_head_phone        TEXT,
    cs_name              TEXT,      -- company secretary / compliance officer
    cs_email             TEXT,
    cfo_name             TEXT,
    cfo_email            TEXT,
    ceo_md_name          TEXT,
    ceo_md_title         TEXT,
    chairman_name        TEXT,
    -- External / alternate channels
    ir_advisor_firm      TEXT,      -- IR/PR agency (often most responsive to B2B)
    ir_advisor_contact   TEXT,      -- "Name (email; phone)"
    rta_firm             TEXT,      -- registrar & transfer agent
    rta_email            TEXT,
    rta_phone            TEXT,
    -- Locations
    registered_office    TEXT,
    corporate_office     TEXT,
    website              TEXT,
    -- The single best actionable channel surfaced to the dashboard
    primary_name         TEXT,      -- who to address ("Attn: …")
    primary_email        TEXT,      -- named-exec direct where literal, else IR inbox
    primary_email_kind   TEXT,      -- 'named_direct' | 'ir_inbox' | 'advisor' | 'rta'
    best_channel_note    TEXT,      -- one-line AS rationale for B2B-pitch routing
    -- Provenance
    contact_source       TEXT,      -- primary source doc(s)
    contact_date         TEXT,      -- YYYY-MM of source
    contact_confidence   TEXT,      -- 'high' | 'medium' | 'verify'
    sources_json         TEXT,      -- [{field, source, date}]
    generated_at         TEXT
);
"""


def main():
    if not DB_PATH.exists():
        raise SystemExit(f"DB not found: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.commit()
    cols = [r[1] for r in conn.execute("PRAGMA table_info(contacts)").fetchall()]
    print(f"[schema] contacts table ready — {len(cols)} columns")
    print("  " + ", ".join(cols))
    conn.close()


if __name__ == "__main__":
    main()
