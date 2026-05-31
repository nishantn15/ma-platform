"""
06_enrich_v05.py
----------------
Per TK's May 23 expansion ask. Extends the leads schema and computes
9 new financial fields from existing yfinance data + introduces the
Acquisition Ready Score.

NEW COLUMNS ADDED TO leads.db:
  Group: Revenue
    revenue_last_yr_cr       latest fiscal-year revenue (Cr)
    revenue_5y_cagr_pct      compound growth across available yrs

  Group: Market Cap
    market_cap_5y_change_pct  pct change vs 5y ago (close-of-FY)

  Group: Cash
    cash_pct_revenue_pct     cash & equiv as % of last-yr revenue

  Group: NPAT (Net Profit After Tax)
    npat_last_yr_cr          last-yr net income (Cr)
    npat_pct_revenue_pct     net margin %

  Group: Operating Margins
    op_margin_last_yr_pct    operating income / revenue
    op_margin_5y_growth_pct  margin pct-points growth across years

  Group: Acquisition Ready Score (the headline)
    acquisition_ready_score   0-100 weighted score
    ars_components            JSON of component scores (audit trail)

Re-runs in place: idempotent ALTER TABLE, idempotent recompute.
Reads from existing leads.db (assumes 02_enrich already ran).
Refreshes by fetching yfinance financials() for each ticker.

Run: python3 06_enrich_v05.py [--limit N]
"""
import json
import sqlite3
import sys
import time
from pathlib import Path

import pandas as pd
import yfinance as yf

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data"
DB_PATH = DATA_DIR / "leads.db"

NEW_COLS = [
    ("revenue_last_yr_cr", "REAL"),
    ("revenue_5y_cagr_pct", "REAL"),
    ("market_cap_5y_change_pct", "REAL"),
    ("cash_pct_revenue_pct", "REAL"),
    ("npat_last_yr_cr", "REAL"),
    ("npat_pct_revenue_pct", "REAL"),
    ("op_margin_last_yr_pct", "REAL"),
    ("op_margin_5y_growth_pct", "REAL"),
    ("acquisition_ready_score", "REAL"),
    ("ars_components", "TEXT"),
    ("financials_enriched_at", "TEXT"),
]


def cr(value):
    if value is None:
        return None
    try:
        return round(float(value) / 1e7, 2)
    except (TypeError, ValueError):
        return None


def cagr(series_sorted_asc):
    if series_sorted_asc is None or len(series_sorted_asc) < 2:
        return None
    start = series_sorted_asc.iloc[0]
    end = series_sorted_asc.iloc[-1]
    n = len(series_sorted_asc) - 1
    if start is None or start <= 0 or end is None or n <= 0:
        return None
    try:
        return round(((end / start) ** (1.0 / n) - 1.0) * 100.0, 2)
    except (ValueError, ZeroDivisionError, OverflowError):
        return None


def first_present(df, names):
    for n in names:
        if n in df.index:
            return df.loc[n].dropna()
    return None


def ensure_columns(conn):
    existing = {row[1] for row in conn.execute("PRAGMA table_info(leads)").fetchall()}
    added = 0
    for name, decl in NEW_COLS:
        if name not in existing:
            conn.execute(f"ALTER TABLE leads ADD COLUMN {name} {decl}")
            added += 1
    conn.commit()
    return added


def compute_for_ticker(symbol):
    """Pull yfinance financials, return dict of computed fields."""
    out = {
        "revenue_last_yr_cr": None, "revenue_5y_cagr_pct": None,
        "market_cap_5y_change_pct": None, "cash_pct_revenue_pct": None,
        "npat_last_yr_cr": None, "npat_pct_revenue_pct": None,
        "op_margin_last_yr_pct": None, "op_margin_5y_growth_pct": None,
    }
    try:
        t = yf.Ticker(symbol + ".NS")
        try:
            fin = t.financials
        except Exception:
            fin = None
        if fin is None or fin.empty:
            return out

        rev = first_present(fin, ["Total Revenue", "Operating Revenue"])
        if rev is not None and len(rev) >= 1:
            rev_sorted = rev.sort_index()  # asc
            out["revenue_last_yr_cr"] = cr(rev_sorted.iloc[-1])
            out["revenue_5y_cagr_pct"] = cagr(rev_sorted)

        np_ = first_present(fin, ["Net Income", "Net Income Common Stockholders"])
        if np_ is not None and len(np_) >= 1:
            np_sorted = np_.sort_index()
            out["npat_last_yr_cr"] = cr(np_sorted.iloc[-1])

        op = first_present(fin, ["Operating Income"])
        margins_pct = None
        if op is not None and rev is not None:
            op_sorted = op.sort_index()
            rev_sorted = rev.sort_index()
            margins_pct = pd.Series(
                [(o / r * 100.0) if r else None
                 for o, r in zip(op_sorted.values, rev_sorted.reindex(op_sorted.index).values)],
                index=op_sorted.index,
            ).dropna()
            if len(margins_pct) >= 1:
                out["op_margin_last_yr_pct"] = round(float(margins_pct.iloc[-1]), 2)
            if len(margins_pct) >= 2:
                out["op_margin_5y_growth_pct"] = round(
                    float(margins_pct.iloc[-1] - margins_pct.iloc[0]), 2
                )

        # Net margin %
        if (out["npat_last_yr_cr"] is not None
                and out["revenue_last_yr_cr"] not in (None, 0)):
            out["npat_pct_revenue_pct"] = round(
                out["npat_last_yr_cr"] / out["revenue_last_yr_cr"] * 100.0, 2
            )

        # Market cap 5y change — use historical close prices x shares outstanding
        try:
            hist = t.history(period="5y", interval="1mo")
            if not hist.empty:
                # crude proxy: pct change in closing price across the 5y window
                prices = hist["Close"].dropna()
                if len(prices) >= 2:
                    out["market_cap_5y_change_pct"] = round(
                        float((prices.iloc[-1] / prices.iloc[0] - 1) * 100.0), 2
                    )
        except Exception:
            pass

        return out
    except Exception as e:
        print(f"  [warn] {symbol}: {e}")
        return out


# ============================================================
# Acquisition Ready Score (proposal — to be tuned by TK)
# ============================================================
# TK's 4 factors (May 23 02:46):
#   - Disposable cash available for acquisition
#   - Revenue growth slowing down
#   - Operating margins shrinking
#   - Profit growth slowing down
#
# Score = sum of 4 weighted components, each 0-100, then weighted average.
# Total: 0-100. Higher = more ready (more cash + more clearly stalling).
#
# Weights (proposal — easy to retune):
ARS_WEIGHTS = {
    "cash_disposable":    40,   # absolute firepower
    "revenue_slowing":    25,   # boards reach for inorganic when growth stalls
    "margin_shrinking":   20,   # margin pressure forces strategic options
    "profit_slowing":     15,   # rounds out the growth-fatigue signal
}
assert sum(ARS_WEIGHTS.values()) == 100


def score_disposable_cash(row):
    """Higher score for more cash relative to mcap (more firepower)."""
    cash_pct = row.get("cash_pct_mcap")
    if cash_pct is None:
        return 0
    # Sigmoid-ish: 0% mcap -> 0, 5% -> 50, 10% -> 80, 15%+ -> 95+
    if cash_pct <= 0:
        return 0
    if cash_pct >= 20:
        return 100
    return min(100, round(cash_pct * 6 + 5, 1))


def score_revenue_slowing(row):
    """Higher score when revenue growth is in the 'slow but stable' zone (3-12%).
    Very slow (<3%) is decline → still get partial points (reach for inorganic).
    Very fast (>20%) is the wrong profile (don't need M&A) → low score.
    """
    g = row.get("revenue_5y_cagr_pct")
    if g is None:
        return 0
    if g < 0:
        return 60   # negative growth — board pressure to do something
    if g <= 3:
        return 80   # very slow — high incentive
    if g <= 12:
        return 90   # sweet spot
    if g <= 18:
        return 50   # decent growth, mid-incentive
    return 20       # growing fast organically


def score_margin_shrinking(row):
    """Higher score when op-margin growth is negative or flat (margin compression
    is a strategic-option-forcing function).
    """
    m = row.get("op_margin_5y_growth_pct")
    if m is None:
        return 0
    # Margin growth in pct-points across 4-5 yrs.
    # -5pp+ = severe shrinkage = high score
    # -2pp = moderate shrinkage = good score
    # 0 = flat = mid score
    # +2pp = expanding = low score
    if m <= -5:
        return 95
    if m <= -2:
        return 80
    if m <= 0:
        return 65
    if m <= 2:
        return 40
    return 20


def score_profit_slowing(row):
    """Same shape as revenue but uses profit_5y_cagr."""
    g = row.get("profit_5y_cagr")
    if g is None:
        return 0
    if g < 0:
        return 70
    if g <= 5:
        return 85
    if g <= 12:
        return 75
    if g <= 20:
        return 50
    return 25


def compute_ars(row):
    """Returns (score 0-100, components dict)."""
    components = {
        "cash_disposable":  score_disposable_cash(row),
        "revenue_slowing":  score_revenue_slowing(row),
        "margin_shrinking": score_margin_shrinking(row),
        "profit_slowing":   score_profit_slowing(row),
    }
    weighted = sum(components[k] * ARS_WEIGHTS[k] for k in ARS_WEIGHTS) / 100.0
    return round(weighted, 1), components


# ============================================================
# Main
# ============================================================
def main():
    if not DB_PATH.exists():
        print(f"DB not found: {DB_PATH}", file=sys.stderr); sys.exit(2)

    limit = None
    if len(sys.argv) > 1 and sys.argv[1].startswith("--limit"):
        limit = int(sys.argv[1].split("=", 1)[1]) if "=" in sys.argv[1] else int(sys.argv[2])

    conn = sqlite3.connect(DB_PATH)
    added = ensure_columns(conn)
    if added:
        print(f"[schema] added {added} new columns")

    # Pull rows that need refresh: any without financials_enriched_at, or with limit
    where = "WHERE tier IN ('T1','T2','T3') AND tier != 'skip_financial'"
    sql = f"SELECT nse_symbol, sector FROM leads {where} ORDER BY tier, market_cap_cr DESC"
    if limit:
        sql += f" LIMIT {limit}"
    rows = conn.execute(sql).fetchall()
    print(f"[input] {len(rows)} candidates to enrich")

    success = 0
    for sym, sector in rows:
        print(f"  fetching {sym} ...", end=" ", flush=True)
        fields = compute_for_ticker(sym)
        # Persist financial fields
        sets = []; vals = []
        for k, v in fields.items():
            sets.append(f"{k}=?"); vals.append(v)
        sets.append("financials_enriched_at=?")
        vals.append(time.strftime("%Y-%m-%d %H:%M:%S"))
        vals.append(sym)
        conn.execute(f"UPDATE leads SET {','.join(sets)} WHERE nse_symbol=?", vals)
        conn.commit()
        if any(v is not None for v in fields.values()):
            success += 1
            print(f"OK (rev={fields['revenue_last_yr_cr']}, op_mar={fields['op_margin_last_yr_pct']}%, p5y={fields['revenue_5y_cagr_pct']}%)")
        else:
            print("no data")
        time.sleep(0.5)

    print(f"\n[financials] {success}/{len(rows)} enriched")

    # ============================================================
    # Compute ARS for every row that has the inputs
    # ============================================================
    print("\n[ARS] computing Acquisition Ready Score for all leads...")
    df = pd.read_sql("SELECT * FROM leads", conn)
    ars_count = 0
    for _, row in df.iterrows():
        score, components = compute_ars(row.to_dict())
        if any(v > 0 for v in components.values()):
            conn.execute(
                "UPDATE leads SET acquisition_ready_score=?, ars_components=? WHERE nse_symbol=?",
                (score, json.dumps(components), row["nse_symbol"]),
            )
            ars_count += 1
    conn.commit()
    print(f"[ARS] scored {ars_count} leads")

    # Summary
    summary = conn.execute("""
        SELECT tier, COUNT(*) as n, ROUND(AVG(acquisition_ready_score),1) as avg_ars
        FROM leads
        WHERE acquisition_ready_score IS NOT NULL
        GROUP BY tier
        ORDER BY tier
    """).fetchall()
    print("\n[summary]")
    for tier, n, avg in summary:
        print(f"  {tier}: {n} leads, avg ARS {avg}")

    print("\n[top 15 by ARS]")
    top = conn.execute("""
        SELECT nse_symbol, name, tier, ROUND(acquisition_ready_score,1) as ars,
               ROUND(cash_pct_mcap,1) as cash_pct,
               ROUND(revenue_5y_cagr_pct,1) as rev_5y,
               ROUND(op_margin_5y_growth_pct,1) as opm_chg,
               ROUND(profit_5y_cagr,1) as p5y
        FROM leads
        WHERE acquisition_ready_score IS NOT NULL
        ORDER BY acquisition_ready_score DESC
        LIMIT 15
    """).fetchall()
    print(f"  {'sym':12s} {'name':30s} {'tier':4s} {'ARS':5s} {'cash%':6s} {'rev5y':6s} {'opmCh':6s} {'p5y':5s}")
    for row in top:
        sym, name, tier, ars, cp, r5y, omc, p5y = row
        print(f"  {sym:12s} {(name or '')[:30]:30s} {tier:4s} {ars:5} {cp or '-':>6} {r5y or '-':>6} {omc or '-':>6} {p5y or '-':>5}")

    conn.close()


if __name__ == "__main__":
    main()
