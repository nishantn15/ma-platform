"""
02_enrich_yfinance.py
---------------------
Reads ../data/starter_list.csv (or another CSV with `nse_symbol` column),
enriches each ticker via yfinance, and writes results into a SQLite DB.

MVP fields per TK schema decision:
  - name, nse_symbol, sector
  - market_cap_cr
  - cash_and_equivalents_cr
  - total_debt_cr
  - debt_to_equity
  - profit_5y_cagr
  - tier (from input)
  - pipeline fields (outreach_status, last_contacted, notes)

Output: ../data/leads.db (SQLite) + ../output/leads_enriched.csv

Run: python3 02_enrich_yfinance.py [INPUT_CSV]
     defaults INPUT_CSV=../data/starter_list.csv
"""
import csv
import os
import sqlite3
import sys
import time
from pathlib import Path

import pandas as pd
import yfinance as yf

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data"
OUT_DIR = SCRIPT_DIR.parent / "output"
OUT_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "leads.db"
DEFAULT_INPUT = DATA_DIR / "starter_list.csv"

SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
    nse_symbol TEXT PRIMARY KEY,
    name TEXT,
    sector TEXT,
    industry TEXT,
    tier TEXT,
    tier_reason TEXT,
    market_cap_cr REAL,
    cash_and_equivalents_cr REAL,
    total_debt_cr REAL,
    debt_to_equity REAL,
    revenue_ttm_cr REAL,
    net_profit_ttm_cr REAL,
    profit_5y_cagr REAL,
    enriched_at TEXT,
    outreach_status TEXT DEFAULT 'pending',
    last_contacted TEXT,
    notes TEXT
);
"""


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def cr(value):
    """Convert raw INR to Crores (Rs 1 Cr = 10,000,000)."""
    if value is None:
        return None
    try:
        return round(float(value) / 1e7, 2)
    except (TypeError, ValueError):
        return None


def safe_get(d, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and k in d and d[k] is not None:
            return d[k]
    return default


def compute_5y_cagr(financials_df):
    """5-yr profit CAGR from yfinance income-statement DataFrame.
    yfinance returns a DataFrame indexed by metric, columns are years (descending).
    """
    if financials_df is None or financials_df.empty:
        return None
    rows = ["Net Income", "Net Income Common Stockholders", "Net Income Continuous Operations"]
    series = None
    for r in rows:
        if r in financials_df.index:
            series = financials_df.loc[r].dropna()
            break
    if series is None or len(series) < 2:
        return None
    sorted_series = series.sort_index()
    start, end = sorted_series.iloc[0], sorted_series.iloc[-1]
    n = len(sorted_series) - 1
    if start is None or start <= 0 or end is None or n <= 0:
        return None
    try:
        cagr = ((end / start) ** (1.0 / n) - 1.0) * 100.0
        return round(cagr, 2)
    except (ZeroDivisionError, ValueError, OverflowError):
        return None


def enrich_one(row):
    """Take a row from starter list, return enriched dict (or None)."""
    sym = row["nse_symbol"].strip()
    ticker = sym + ".NS"
    print(f"  fetching {ticker} ...", end=" ", flush=True)
    try:
        t = yf.Ticker(ticker)
        info = t.info or {}
        bal = None
        try:
            bal = t.balance_sheet
        except Exception:
            bal = None
        fin = None
        try:
            fin = t.financials
        except Exception:
            fin = None

        market_cap = safe_get(info, "marketCap")
        cash = None
        debt = None
        if bal is not None and not bal.empty:
            for k in ["Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments",
                      "Cash And Short Term Investments", "Cash"]:
                if k in bal.index:
                    cash = bal.loc[k].iloc[0]
                    break
            for k in ["Total Debt", "Long Term Debt", "Net Debt"]:
                if k in bal.index:
                    debt = bal.loc[k].iloc[0]
                    break
        d2e = safe_get(info, "debtToEquity")
        if d2e is not None:
            try:
                d2e = round(float(d2e) / 100.0, 3)  # yfinance returns it as %; normalise
            except Exception:
                pass

        rev_ttm = safe_get(info, "totalRevenue")
        np_ttm = safe_get(info, "netIncomeToCommon", "netIncome")
        profit_5y = compute_5y_cagr(fin)
        sector = safe_get(info, "sector") or row.get("sector", "")
        industry = safe_get(info, "industry") or ""

        result = {
            "nse_symbol": sym,
            "name": row.get("name", info.get("longName")),
            "sector": sector,
            "industry": industry,
            "tier": row.get("tier", ""),
            "tier_reason": row.get("tier_reason", ""),
            "market_cap_cr": cr(market_cap),
            "cash_and_equivalents_cr": cr(cash),
            "total_debt_cr": cr(debt),
            "debt_to_equity": d2e,
            "revenue_ttm_cr": cr(rev_ttm),
            "net_profit_ttm_cr": cr(np_ttm),
            "profit_5y_cagr": profit_5y,
            "enriched_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "outreach_status": row.get("outreach_status", "pending"),
            "last_contacted": "",
            "notes": row.get("notes", ""),
        }
        print(f"OK (mcap={result['market_cap_cr']}, cash={result['cash_and_equivalents_cr']})")
        return result
    except Exception as e:
        print(f"FAIL: {e}")
        return None


def upsert(conn, row):
    cols = list(row.keys())
    placeholders = ",".join(["?"] * len(cols))
    col_list = ",".join(cols)
    update = ",".join([f"{c}=excluded.{c}" for c in cols if c != "nse_symbol"])
    sql = (f"INSERT INTO leads ({col_list}) VALUES ({placeholders}) "
           f"ON CONFLICT(nse_symbol) DO UPDATE SET {update}")
    conn.execute(sql, [row[c] for c in cols])


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    if not input_path.exists():
        print(f"Input not found: {input_path}", file=sys.stderr)
        sys.exit(2)

    df_in = pd.read_csv(input_path)
    print(f"[input] {input_path.name} — {len(df_in)} rows")

    conn = init_db()
    enriched = []
    for _, row in df_in.iterrows():
        result = enrich_one(row)
        if result:
            upsert(conn, result)
            enriched.append(result)
        time.sleep(1.0)  # polite rate limit

    conn.commit()
    conn.close()

    out_csv = OUT_DIR / "leads_enriched.csv"
    pd.DataFrame(enriched).to_csv(out_csv, index=False)
    print(f"\n[done] enriched {len(enriched)}/{len(df_in)} rows")
    print(f"       db:  {DB_PATH}")
    print(f"       csv: {out_csv}")


if __name__ == "__main__":
    main()
