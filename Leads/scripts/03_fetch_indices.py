"""
03_fetch_indices.py
-------------------
Downloads Nifty 500 and BSE 500 constituent lists, merges them by ISIN,
and writes the combined screening universe to ../data/index_universe.csv.

This is the canonical input for enrichment (full mid-cap + large-cap + top small-cap
coverage — ~700 companies, ~95% of Indian listed market cap).

Run: python3 03_fetch_indices.py
"""
import io
import sys
import time
import pandas as pd
import requests
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/csv,application/csv,text/plain,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.niftyindices.com/",
}

NIFTY500_URL = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
NIFTY_MIDCAP150_URL = "https://archives.nseindia.com/content/indices/ind_niftymidcap150list.csv"
NIFTY_SMALLCAP250_URL = "https://archives.nseindia.com/content/indices/ind_niftysmallcap250list.csv"
NIFTY_MICROCAP250_URL = "https://archives.nseindia.com/content/indices/ind_niftymicrocap250_list.csv"
NIFTY_TOTAL_MARKET_URL = "https://archives.nseindia.com/content/indices/ind_niftytotalmarket_list.csv"


def fetch_csv(url, label):
    print(f"[{label}] downloading ...")
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.columns = [c.strip() for c in df.columns]
    print(f"[{label}] {len(df)} rows · cols: {list(df.columns)[:5]}...")
    return df


def normalise_nse(df, index_tag):
    """Standardise NSE-index CSV columns."""
    rename = {}
    for src in df.columns:
        s = src.strip().lower().replace(" ", "_")
        if s in ("symbol",):
            rename[src] = "nse_symbol"
        elif s in ("company_name",):
            rename[src] = "name"
        elif "isin" in s:
            rename[src] = "isin"
        elif "industry" in s:
            rename[src] = "industry"
        elif "series" in s:
            rename[src] = "series"
    df = df.rename(columns=rename)
    keep = [c for c in ["isin", "nse_symbol", "name", "industry", "series"] if c in df.columns]
    df = df[keep].copy()
    df[index_tag] = True
    return df


def main():
    frames = []
    for url, tag in [
        (NIFTY_TOTAL_MARKET_URL, "in_total_market"),
        (NIFTY500_URL, "in_nifty500"),
        (NIFTY_MIDCAP150_URL, "in_midcap150"),
        (NIFTY_SMALLCAP250_URL, "in_smallcap250"),
        (NIFTY_MICROCAP250_URL, "in_microcap250"),
    ]:
        try:
            df = fetch_csv(url, tag)
            df = normalise_nse(df, tag)
            frames.append(df)
            time.sleep(1.0)
        except Exception as e:
            print(f"[{tag}] FAILED: {e}", file=sys.stderr)

    if not frames:
        print("All NSE index fetches failed.", file=sys.stderr)
        sys.exit(2)

    # Merge: outer join on ISIN
    base = frames[0]
    for f in frames[1:]:
        flags = [c for c in f.columns if c.startswith("in_")]
        base = base.merge(
            f[["isin"] + flags + (["nse_symbol", "name", "industry"] if "nse_symbol" not in base.columns else [])],
            on="isin", how="outer", suffixes=("", "_y"),
        )
        # collapse fallback columns
        for col in ["nse_symbol", "name", "industry"]:
            y = col + "_y"
            if y in base.columns:
                base[col] = base[col].fillna(base[y]) if col in base.columns else base[y]
                base = base.drop(columns=[y])

    # Fill index flags as False where NaN
    flag_cols = [c for c in base.columns if c.startswith("in_")]
    for c in flag_cols:
        base[c] = base[c].fillna(False).astype(bool)

    # Tag bucket
    def bucket(row):
        if row.get("in_microcap250"):
            return "micro_cap"
        if row.get("in_smallcap250"):
            return "small_cap"
        if row.get("in_midcap150"):
            return "mid_cap"
        if row.get("in_nifty500"):
            return "large_cap"
        if row.get("in_total_market"):
            return "other_total_market"
        return "other"
    base["bucket"] = base.apply(bucket, axis=1)

    # Deduplicate by ISIN
    base = base.drop_duplicates(subset=["isin"]).reset_index(drop=True)

    out = DATA_DIR / "index_universe.csv"
    base.to_csv(out, index=False)

    print(f"\n[OK] wrote {out} — {len(base)} unique companies")
    for b in ["large_cap", "mid_cap", "small_cap", "micro_cap", "other_total_market", "other"]:
        n = (base['bucket']==b).sum()
        if n > 0:
            print(f"     {b:20s}  {n}")


if __name__ == "__main__":
    main()
