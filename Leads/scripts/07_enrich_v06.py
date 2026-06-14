"""
07_enrich_v06.py
----------------
Per TK feedback June 2 (#9 ARS compound flag) and June 6 (#1 industry
benchmarks). Computes purely from data already in leads.db — no network.

NEW COLUMNS:
  ars_compound_flag     TEXT  'strong' | 'aligned' | None
  ars_compound_reason   TEXT  human-readable why it fired
  industry_rank         INTEGER  rank within industry by market cap (1 = largest)
  industry_size         INTEGER  count of peers in same industry (T1-T3)
  industry_size_tier    TEXT  'Large' | 'Mid' | 'Small' (mcap tercile within industry)

COMPOUND FLAG (TK #9): fires when cash firepower AND growth-fatigue signals
align — a genuinely multi-dimensional target, not a one-signal artefact.
  strong  : cash_disposable >= 60 AND >= 2 of {revenue_slowing, margin_shrinking,
            profit_slowing} score >= 70
  aligned : cash_disposable >= 40 AND >= 1 fatigue signal >= 70
Only evaluated for rows with real financials (revenue_5y_cagr_pct present),
so skip_financial rows don't get false compound flags from cash alone.

Run: python3 07_enrich_v06.py
Idempotent: ALTER TABLE IF NOT EXISTS-style guard + full recompute.
"""
import json
import sqlite3
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR.parent / "data" / "leads.db"

NEW_COLS = [
    ("ars_compound_flag", "TEXT"),
    ("ars_compound_reason", "TEXT"),
    ("industry_rank", "INTEGER"),
    ("industry_size", "INTEGER"),
    ("industry_size_tier", "TEXT"),
]

FATIGUE_KEYS = ("revenue_slowing", "margin_shrinking", "profit_slowing")
FATIGUE_LABEL = {
    "revenue_slowing": "revenue slowing",
    "margin_shrinking": "margin shrinking",
    "profit_slowing": "profit slowing",
}


def ensure_columns(conn):
    existing = {row[1] for row in conn.execute("PRAGMA table_info(leads)").fetchall()}
    added = 0
    for name, decl in NEW_COLS:
        if name not in existing:
            conn.execute(f"ALTER TABLE leads ADD COLUMN {name} {decl}")
            added += 1
    conn.commit()
    return added


def compound_flag(components, has_real_financials):
    """Return (flag, reason) per TK #9. None unless multi-signal alignment."""
    if not has_real_financials or not components:
        return None, None
    cash = components.get("cash_disposable", 0) or 0
    fired = [FATIGUE_LABEL[k] for k in FATIGUE_KEYS
             if (components.get(k, 0) or 0) >= 70]
    n = len(fired)
    if cash >= 60 and n >= 2:
        return "strong", f"High cash firepower + {n} fatigue signals ({', '.join(fired)})"
    if cash >= 40 and n >= 1:
        return "aligned", f"Cash available + {n} fatigue signal ({', '.join(fired)})"
    return None, None


def main():
    if not DB_PATH.exists():
        raise SystemExit(f"DB not found: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    added = ensure_columns(conn)
    if added:
        print(f"[schema] added {added} new columns")

    rows = conn.execute(
        "SELECT nse_symbol, industry, tier, market_cap_cr, ars_components, "
        "revenue_5y_cagr_pct FROM leads"
    ).fetchall()

    # ---- Compound flag ----
    flagged = {"strong": 0, "aligned": 0}
    for sym, industry, tier, mcap, comp, rev5y in rows:
        cc = json.loads(comp) if comp else {}
        flag, reason = compound_flag(cc, rev5y is not None)
        conn.execute(
            "UPDATE leads SET ars_compound_flag=?, ars_compound_reason=? WHERE nse_symbol=?",
            (flag, reason, sym),
        )
        if flag:
            flagged[flag] += 1
    conn.commit()
    print(f"[compound] strong={flagged['strong']}  aligned={flagged['aligned']}")

    # ---- Industry rank + size tier (T1-T3 universe only) ----
    by_ind = {}
    for sym, industry, tier, mcap, comp, rev5y in rows:
        if tier in ("T1", "T2", "T3") and industry and mcap is not None:
            by_ind.setdefault(industry, []).append((sym, mcap))

    ranked = 0
    for industry, members in by_ind.items():
        members.sort(key=lambda x: -x[1])  # largest mcap first
        size = len(members)
        for i, (sym, mcap) in enumerate(members):
            rank = i + 1
            # tercile by position: top third Large, middle Mid, bottom Small
            frac = i / size if size > 1 else 0.0
            if frac < 1 / 3:
                stier = "Large"
            elif frac < 2 / 3:
                stier = "Mid"
            else:
                stier = "Small"
            conn.execute(
                "UPDATE leads SET industry_rank=?, industry_size=?, industry_size_tier=? "
                "WHERE nse_symbol=?",
                (rank, size, stier, sym),
            )
            ranked += 1
    conn.commit()
    print(f"[industry] ranked {ranked} leads across {len(by_ind)} industries")

    # ---- Summary ----
    print("\n[compound strong names]")
    for sym, name, tier, ars in conn.execute(
        "SELECT nse_symbol, name, tier, acquisition_ready_score FROM leads "
        "WHERE ars_compound_flag='strong' ORDER BY acquisition_ready_score DESC"
    ):
        print(f"  {sym:12s} {tier} ARS={ars}  {name}")

    conn.close()


if __name__ == "__main__":
    main()
