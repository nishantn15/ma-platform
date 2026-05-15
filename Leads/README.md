# Leads Directory

Pipeline + data for the M&A Leadership Platform outreach pipeline.

## Status

**v0.1** — Bootstrap pipeline working. Starter list (37 companies) enriched with real data.

| Tier | Count | Examples |
|------|-------|----------|
| T1 | 20 | ITC, HUL, L&T, M&M, TCS, Infy, Wipro, Sun Pharma, Coal India |
| T2 | 17 | Persistent, Coforge, KPIT, Tata Elxsi, CAMS, CDSL, Page, Bata, Astral |

## Layout

```
Leads/
├── scripts/
│   ├── 01_build_universe.py    NSE+BSE listed-company master list
│   └── 02_enrich_yfinance.py   Enrich tickers via yfinance, write to SQLite
├── data/
│   ├── listed_universe.csv     NSE/BSE merged universe (~2,365 NSE + BSE TBD)
│   ├── starter_list.csv        Hand-curated T1+T2 starter (37 companies)
│   └── leads.db                SQLite database (final enriched data)
├── output/
│   └── leads_enriched.csv      Enriched CSV (mirror of leads.db.leads table)
└── README.md
```

## MVP Schema (`leads.db.leads` table)

| Field | Type | Source |
|-------|------|--------|
| `nse_symbol` | TEXT (PK) | starter_list |
| `name` | TEXT | starter_list / yfinance |
| `sector` | TEXT | yfinance / starter_list |
| `industry` | TEXT | yfinance |
| `tier` | TEXT | starter_list (T1/T2/T3) |
| `tier_reason` | TEXT | starter_list (hand) |
| `market_cap_cr` | REAL | yfinance (INR Crores) |
| `cash_and_equivalents_cr` | REAL | yfinance balance sheet |
| `total_debt_cr` | REAL | yfinance balance sheet |
| `debt_to_equity` | REAL | yfinance (normalized) |
| `revenue_ttm_cr` | REAL | yfinance |
| `net_profit_ttm_cr` | REAL | yfinance |
| `profit_5y_cagr` | REAL | computed from financials |
| `enriched_at` | TEXT | timestamp |
| `outreach_status` | TEXT | pending/contacted/meeting/won/lost |
| `last_contacted` | TEXT | date string |
| `notes` | TEXT | free-form |

## Usage

```bash
# 1. Build the universe (download NSE+BSE listed-company master)
python3 scripts/01_build_universe.py

# 2. Enrich the starter list (defaults to data/starter_list.csv)
python3 scripts/02_enrich_yfinance.py

# 3. Query the DB
sqlite3 data/leads.db "SELECT tier, COUNT(*) FROM leads GROUP BY tier"
sqlite3 data/leads.db "SELECT name, market_cap_cr, cash_and_equivalents_cr FROM leads WHERE tier='T1' ORDER BY market_cap_cr DESC"

# 4. Update outreach status manually or via SQL
sqlite3 data/leads.db "UPDATE leads SET outreach_status='contacted', last_contacted='2026-05-20' WHERE nse_symbol='LT'"
```

## Data Quality Notes

- **yfinance cash field is conservative.** ITC and similar companies hold huge sums in mutual funds / investments that don't show as "Cash And Cash Equivalents." For tier-1 dossiers, **always verify cash against the latest annual report**, not yfinance.
- **NSE alone enriched.** BSE API endpoint returned HTML rather than JSON — will retry with the BSE Equity CSV download approach later. NSE coverage of ~2,365 names is sufficient for T1/T2.
- **yfinance rate limit.** Script paces at 1 req/sec. Full Nifty 500 enrichment = ~10 min wall clock.

## Next Steps

1. Fix BSE endpoint (try the BSE Equity CSV download path)
2. Expand enrichment to full Nifty 500 + BSE 500 (~700 companies)
3. Add Screener.in custom-query layer (Rs 1,400/yr subscription) for the deeper criteria
4. Add acquisition-history field (manual or via news API)
5. Add IR contact fields (ir_email, cfo_name)
6. Build a simple HTML/Streamlit dashboard view of the directory

## Gitignore

`leads.db` and CSV outputs are tracked for now (small file, easy to review). If/when the directory grows beyond 1MB, move outputs to `.gitignore` and keep just the scripts + starter_list.csv tracked.
