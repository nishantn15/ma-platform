"""
08_backfill_mcap5y.py
---------------------
Backfill market_cap_5y_change_pct (0/752 after v0.5 — the original fetch
never populated it). Uses 5y monthly close price change as the proxy
(share count ~constant for these large caps; price change ~ mcap change).

Targets only T1-T3 rows missing the value. Resilient to Yahoo 429s:
retries with backoff, skips on persistent failure, commits each row so
partial progress survives interruption.

Run: python3 08_backfill_mcap5y.py [--limit N]
"""
import sqlite3
import sys
import time
from pathlib import Path

import yfinance as yf

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "leads.db"


def fetch_5y_change(symbol, retries=3):
    for attempt in range(retries):
        try:
            t = yf.Ticker(symbol + ".NS")
            h = t.history(period="5y", interval="1mo")
            if h is not None and not h.empty:
                p = h["Close"].dropna()
                if len(p) >= 2 and p.iloc[0] > 0:
                    return round(float((p.iloc[-1] / p.iloc[0] - 1) * 100.0), 2)
            return None
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
            else:
                print(f"  [warn] {symbol}: {repr(e)[:80]}")
    return None


def main():
    limit = None
    if len(sys.argv) > 1 and sys.argv[1].startswith("--limit"):
        limit = int(sys.argv[2]) if "=" not in sys.argv[1] else int(sys.argv[1].split("=")[1])

    conn = sqlite3.connect(DB_PATH)
    sql = ("SELECT nse_symbol FROM leads WHERE tier IN ('T1','T2','T3') "
           "AND market_cap_5y_change_pct IS NULL ORDER BY tier, market_cap_cr DESC")
    if limit:
        sql += f" LIMIT {limit}"
    syms = [r[0] for r in conn.execute(sql).fetchall()]
    print(f"[input] {len(syms)} tickers to backfill")

    ok = 0
    for i, sym in enumerate(syms, 1):
        val = fetch_5y_change(sym)
        if val is not None:
            conn.execute("UPDATE leads SET market_cap_5y_change_pct=? WHERE nse_symbol=?", (val, sym))
            conn.commit()
            ok += 1
        if i % 25 == 0:
            print(f"  ...{i}/{len(syms)} done, {ok} populated")
        time.sleep(0.6)

    print(f"[done] {ok}/{len(syms)} populated")
    conn.close()


if __name__ == "__main__":
    main()
