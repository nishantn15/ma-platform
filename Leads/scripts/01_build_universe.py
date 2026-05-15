"""
01_build_universe.py
--------------------
Downloads the official NSE and BSE listed-company lists, dedupes by ISIN,
and writes a unified universe CSV to ../data/.

Output: ../data/listed_universe.csv (~5,500 unique listed entities)

Run: python3 01_build_universe.py
"""
import csv
import io
import os
import sys
import pandas as pd
import requests
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Browser-ish headers — NSE/BSE block bare requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/csv,application/csv,text/plain,*/*",
    "Accept-Language": "en-US,en;q=0.9",
}

NSE_URL = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
BSE_URL = "https://api.bseindia.com/BseIndiaAPI/api/ListOfScripCodeWith_New/w?Group=&Status=Active&industry=&segment=Equity"


def fetch_nse() -> pd.DataFrame:
    """NSE equity master list — direct CSV from archives."""
    print("[NSE] downloading EQUITY_L.csv ...")
    r = requests.get(NSE_URL, headers=HEADERS, timeout=30)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.columns = [c.strip().upper().replace(" ", "_") for c in df.columns]
    # Expected columns: SYMBOL NAME_OF_COMPANY SERIES DATE_OF_LISTING PAID_UP_VALUE
    # MARKET_LOT ISIN_NUMBER FACE_VALUE
    df = df.rename(columns={
        "SYMBOL": "nse_symbol",
        "NAME_OF_COMPANY": "name",
        "ISIN_NUMBER": "isin",
        "DATE_OF_LISTING": "date_of_listing",
        "FACE_VALUE": "face_value",
        "SERIES": "series",
    })
    df["exchange"] = "NSE"
    df = df[["isin", "nse_symbol", "name", "series", "date_of_listing", "face_value", "exchange"]]
    print(f"[NSE] {len(df)} rows")
    return df


def fetch_bse() -> pd.DataFrame:
    """BSE equity list — JSON API."""
    print("[BSE] downloading active equity list ...")
    headers = {**HEADERS, "Accept": "application/json", "Referer": "https://www.bseindia.com/"}
    r = requests.get(BSE_URL, headers=headers, timeout=45)
    r.raise_for_status()
    data = r.json()
    if not isinstance(data, list) or not data:
        raise RuntimeError("BSE response unexpected: %r" % str(data)[:300])
    df = pd.DataFrame(data)
    # Common BSE fields seen in this endpoint:
    # SCRIP_CD, scrip_id, Scrip_Name, Status, Group, Industry, ISIN_NUMBER, Segment
    df.columns = [c.strip() for c in df.columns]
    rename = {}
    for src, dst in [("SCRIP_CD", "bse_code"), ("scrip_id", "bse_symbol"),
                     ("Scrip_Name", "name_bse"), ("ISIN_NUMBER", "isin"),
                     ("Industry", "industry"), ("Group", "bse_group")]:
        if src in df.columns:
            rename[src] = dst
    df = df.rename(columns=rename)
    keep = [c for c in ["isin", "bse_code", "bse_symbol", "name_bse", "industry", "bse_group"] if c in df.columns]
    df = df[keep]
    df["exchange_bse"] = "BSE"
    print(f"[BSE] {len(df)} rows")
    return df


def merge(nse: pd.DataFrame, bse: pd.DataFrame) -> pd.DataFrame:
    """Outer-merge on ISIN."""
    nse = nse[nse["isin"].notna() & (nse["isin"].str.len() == 12)]
    bse = bse[bse["isin"].notna() & (bse["isin"].str.len() == 12)]
    merged = nse.merge(bse, on="isin", how="outer", indicator=True)
    merged["listed_on"] = merged["_merge"].map({
        "both": "NSE+BSE", "left_only": "NSE", "right_only": "BSE"
    })
    merged["name"] = merged["name"].fillna(merged.get("name_bse"))
    merged = merged.drop(columns=["_merge", "name_bse", "exchange", "exchange_bse"], errors="ignore")
    return merged


def main():
    try:
        nse = fetch_nse()
    except Exception as e:
        print(f"[NSE] FAILED: {e}", file=sys.stderr)
        nse = pd.DataFrame(columns=["isin", "nse_symbol", "name", "series", "date_of_listing", "face_value"])

    try:
        bse = fetch_bse()
    except Exception as e:
        print(f"[BSE] FAILED: {e}", file=sys.stderr)
        bse = pd.DataFrame(columns=["isin", "bse_code", "bse_symbol", "name_bse", "industry", "bse_group"])

    if nse.empty and bse.empty:
        print("Both sources failed; aborting.", file=sys.stderr)
        sys.exit(2)

    merged = merge(nse, bse)
    out = DATA_DIR / "listed_universe.csv"
    merged.to_csv(out, index=False)
    print(f"\n[OK] wrote {out} — {len(merged)} rows")
    print(f"     NSE-only: {(merged['listed_on']=='NSE').sum()}")
    print(f"     BSE-only: {(merged['listed_on']=='BSE').sum()}")
    print(f"     Both:     {(merged['listed_on']=='NSE+BSE').sum()}")


if __name__ == "__main__":
    main()
