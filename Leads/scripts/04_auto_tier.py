"""
04_auto_tier.py
---------------
Reads enriched leads from ../data/leads.db, applies TK's criteria as a scoring
function, and writes tier assignments (T1/T2/T3/skip) back to the DB.

TK CRITERIA (Apr 28 brief):
  1. Cash rich          → cash_and_equivalents_cr / market_cap_cr ratio
  2. Market leader      → debt_to_equity low + market_cap large
  3. Profitable 5 yrs   → profit_5y_cagr present and > 0
  4. Traditional/blue+whitespace OK → use sector for context only
  5. Known name         → market_cap_cr (proxy)

BONUS SIGNAL (highest-intent profile):
  - Slow growth (5-15% CAGR) + strong fundamentals (cash + low debt) → board urge to acquire

OUTPUT TIERS:
  - T1 : market_cap >= Rs 50,000 Cr AND cash/mcap >= 2% AND d/e <= 0.5
  - T2 : market_cap Rs 5,000 - 50,000 Cr AND cash/mcap >= 5% AND d/e <= 0.5
  - T3 : market_cap < Rs 5,000 Cr OR fundamentals weaker but profitable
  - skip : negative 5y CAGR OR d/e > 1.5 (highly leveraged)

PRIORITY FLAG (TK's "slow-growth-strong-fundamentals" hot list):
  - profit_5y_cagr between 5% and 15%
  - cash/mcap >= 5%
  - debt_to_equity <= 0.3

Output: tier + tier_score + slow_growth_signal written back to DB
        plus a CSV summary at ../output/leads_tiered.csv

Run: python3 04_auto_tier.py
"""
import sqlite3
import sys
import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data"
OUT_DIR = SCRIPT_DIR.parent / "output"
OUT_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "leads.db"
OUT_CSV = OUT_DIR / "leads_tiered.csv"


def ensure_columns(conn):
    """Add tier_score and slow_growth_signal columns if missing."""
    cols = {row[1] for row in conn.execute("PRAGMA table_info(leads)").fetchall()}
    if "tier_score" not in cols:
        conn.execute("ALTER TABLE leads ADD COLUMN tier_score REAL")
    if "slow_growth_signal" not in cols:
        conn.execute("ALTER TABLE leads ADD COLUMN slow_growth_signal INTEGER DEFAULT 0")
    if "cash_pct_mcap" not in cols:
        conn.execute("ALTER TABLE leads ADD COLUMN cash_pct_mcap REAL")
    conn.commit()


FINANCIAL_SECTORS = {
    "Financial Services", "Banks", "Financials", "Banking",
    "Diversified Financial Services", "Capital Markets", "Insurance",
}


def score_row(row):
    """Return (tier, score, slow_growth_flag, cash_pct)."""
    mcap = row.get("market_cap_cr") or 0
    cash = row.get("cash_and_equivalents_cr") or 0
    d2e  = row.get("debt_to_equity")
    cagr = row.get("profit_5y_cagr")
    sector = (row.get("sector") or "").strip()
    industry = (row.get("industry") or "").strip()
    cash_pct = (cash / mcap * 100) if mcap > 0 else 0

    # Skip financial sector — cash isn't acquisition firepower, it's inventory
    if any(f.lower() in sector.lower() or f.lower() in industry.lower()
           for f in FINANCIAL_SECTORS):
        return ("skip_financial", 0, 0, cash_pct)

    # Skip rules
    if cagr is not None and cagr < 0:
        return ("skip", 0, 0, cash_pct)
    if d2e is not None and d2e > 1.5:
        return ("skip", 0, 0, cash_pct)
    if mcap <= 0:
        return ("skip", 0, 0, cash_pct)

    # Slow-growth + strong-fundamentals signal (TK hot list)
    # Loosened from original: 5y CAGR 3-18, cash_pct >= 3, d/e <= 0.5
    slow_growth_flag = 0
    if (cagr is not None and 3 <= cagr <= 18
            and cash_pct >= 3
            and d2e is not None and d2e <= 0.5):
        slow_growth_flag = 1

    # Score: weighted on cash %, leverage, profit, scale
    score = 0
    score += min(cash_pct, 30)               # cash up to 30 pts
    score += max(0, 20 - (d2e or 0) * 20)    # less debt is better, max 20 pts
    if cagr is not None and cagr > 0:
        score += min(cagr, 30)               # up to 30 pts for growth
    score += min(mcap / 10000, 20)           # scale, 20 pts at Rs 2L Cr+

    if slow_growth_flag:
        score += 15  # priority bonus

    # Tier buckets (TK rules of thumb)
    if mcap >= 50000 and cash_pct >= 2 and (d2e is None or d2e <= 0.5):
        tier = "T1"
    elif mcap >= 5000 and cash_pct >= 5 and (d2e is None or d2e <= 0.5):
        tier = "T2"
    elif cagr is not None and cagr > 0:
        tier = "T3"
    else:
        tier = "skip"

    return (tier, round(score, 1), slow_growth_flag, round(cash_pct, 2))


def main():
    if not DB_PATH.exists():
        print(f"DB not found: {DB_PATH}", file=sys.stderr)
        sys.exit(2)

    conn = sqlite3.connect(DB_PATH)
    ensure_columns(conn)

    df = pd.read_sql("SELECT * FROM leads", conn)
    print(f"[input] {len(df)} rows in leads.db")

    # PRESERVE manual T1/T2 tier from starter_list.csv (authoritative source)
    starter_csv = DATA_DIR / "starter_list.csv"
    manual_tiers = {}
    if starter_csv.exists():
        starter_df = pd.read_csv(starter_csv)
        for _, row in starter_df.iterrows():
            if row.get("tier") in ("T1", "T2"):
                manual_tiers[row["nse_symbol"]] = (row["tier"], row.get("tier_reason", ""))
    print(f"[preserve] {len(manual_tiers)} hand-curated tier assignments from starter_list.csv will be kept")

    # Score everything
    results = []
    for _, row in df.iterrows():
        tier, score, slow, cash_pct = score_row(row.to_dict())
        sym = row["nse_symbol"]
        # Override with manual tier from starter_list.csv if present
        if sym in manual_tiers:
            final_tier, manual_reason = manual_tiers[sym]
        else:
            final_tier, manual_reason = tier, row.get("tier_reason", "")
        results.append({
            "nse_symbol": sym,
            "tier": final_tier,
            "tier_score": score,
            "slow_growth_signal": slow,
            "cash_pct_mcap": cash_pct,
            "tier_reason": manual_reason,
        })

    # Write back to DB
    for r in results:
        conn.execute(
            "UPDATE leads SET tier=?, tier_score=?, slow_growth_signal=?, cash_pct_mcap=?, tier_reason=? "
            "WHERE nse_symbol=?",
            (r["tier"], r["tier_score"], r["slow_growth_signal"], r["cash_pct_mcap"],
             r["tier_reason"], r["nse_symbol"]),
        )
    conn.commit()

    # Summary CSV
    out_df = pd.read_sql(
        "SELECT nse_symbol, name, sector, tier, tier_score, slow_growth_signal, "
        "market_cap_cr, cash_and_equivalents_cr, cash_pct_mcap, debt_to_equity, "
        "profit_5y_cagr, outreach_status FROM leads ORDER BY tier_score DESC",
        conn,
    )
    out_df.to_csv(OUT_CSV, index=False)
    conn.close()

    # Print summary
    print("\n[summary]")
    print(out_df["tier"].value_counts().to_string())
    print(f"\nslow-growth signal flagged: {out_df['slow_growth_signal'].sum()} companies")
    print(f"\n[done] wrote {OUT_CSV}")
    print("\nTop 15 by tier score:")
    print(out_df.head(15)[["nse_symbol", "tier", "tier_score", "slow_growth_signal",
                            "market_cap_cr", "cash_pct_mcap", "profit_5y_cagr"]].to_string(index=False))


if __name__ == "__main__":
    main()
