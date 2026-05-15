# Indian Listed Company Leads Directory — Data Sources & Approach
**Date:** May 15, 2026
**Source:** Codex research, evaluating ~20 data sources

---

## TL;DR — Recommended Stack

**Combined approach (under Rs 2,000/year total):**
- **Free open-source layer**: NSE EQUITY_L.csv + BSE Equity list + `jugaad-data` (NSE bhavcopy) + `yfinance` (Yahoo Finance India) → universe + price-derived signals
- **Paid screening layer**: **Screener.in** (~Rs 1,400/yr) → custom-query filter on cash-rich + 5-yr profitable + market leader criteria, with CSV export
- **Dossier layer**: Annual reports PDF scraping from IR pages + SEBI XBRL filings for cash-position truth

**Skip:**
- Bloomberg / Refinitiv / Capital IQ — overkill ($12k+/yr each)
- Tracxn / VCCEdge — better for private M&A, not listed prospecting
- Tijori / Tickertape — solid for individual research but no exports/API
- FMP / EODHD / Alpha Vantage — thin India fundamentals coverage
- Kite / Breeze — pure trading APIs, no fundamentals

---

## Top 3 Sources (Ranked)

### Pick #1 — Screener.in (best-fit screener)
- ~Rs 1,400/year
- ~5,000+ NSE/BSE listed companies, 10-year financial history
- Ratios pre-computed: ROCE, ROE, OPM, debt/equity, cash, 5-yr CAGRs
- **Custom Query syntax** = exactly what TK's 5 criteria need:
  ```
  Market Capitalization > 5000 AND
  Debt to equity < 0.3 AND
  Cash from operations 5years > 0 AND
  Average return on capital employed 5Years > 18 AND
  Profit growth 5Years > 5 AND Profit growth 5Years < 25 AND
  Promoter holding > 40
  ```
- Excel/CSV export
- **TOS caveat:** Personal use only — use to *identify* leads, capture facts from primary sources

### Pick #2 — Trendlyne StratQ (for scale beyond 2,000 companies)
- Custom enterprise pricing
- 3,000+ parameters, 300 screener strategies
- Better on technicals, FII/DII flows, broker target prices
- Worth it if M&A signals like promoter holding deltas, recent block deals matter

### Pick #3 — Open-source bootstrap stack (free)
- **NSE**: archives.nseindia.com/content/equities/EQUITY_L.csv
- **BSE**: bseindia.com Equity list
- **yfinance** (Python lib): `RELIANCE.NS` / `RELIANCE.BO` → balance sheet, cash, market cap
- **jugaad-data** (best NSE wrapper, nsepy is EOL'd)
- Free. Scriptable. Termux-compatible.
- TOS: Don't redistribute raw data. Internal lead list = de facto industry norm.

---

## Week 1 Quick-Start

| Day | Action |
|-----|--------|
| 1-2 | Download NSE + BSE equity lists, dedupe by ISIN → universe ~5,500 entities. Trim to Nifty 500 + BSE 500 constituents (~700 "real" companies) |
| 3-4 | yfinance enrichment pass: market cap, cash, debt, 5-yr revenue/profit. 1 req/sec, batch 50, SQLite cache. ~2 hr full pass |
| 5 | Subscribe to Screener.in. Run TK qualification query. Export CSV → ~150-250 hits |
| 6-7 | Tier assignment + dossier prep: T1 (cap >Rs 50K Cr + cash >Rs 5K Cr + debt-free) ~30-40 names · T2 (cap Rs 5-50K Cr + cash >Rs 500 Cr) ~80-120 names · T3 monitor |

---

## Data Schema (Leads Directory)

Recommended fields (SQLite or Postgres):

**Identity**
- company_name, legal_name
- nse_symbol, bse_code, isin (primary key)
- sector, industry, sub_industry (NIC + GICS mapping)

**Scale**
- market_cap_cr, market_cap_tier
- revenue_ttm_cr, revenue_5y_cagr (slow-growth signal if 5y CAGR 5-15%)
- net_profit_ttm_cr, net_margin_5y_avg, pat_5y_cagr

**Cash & Leverage (TK criterion #1)**
- cash_and_equivalents_cr, cash_pct_market_cap (>15% = significant)
- debt_total_cr, debt_to_equity (<0.3 preferred)

**Market Leadership (TK criterion #2)**
- roce_5y_avg, roe_5y_avg

**Promoter/Holding signals**
- promoter_holding_pct, promoter_pledge_pct
- fii_holding_pct, dii_holding_pct

**Acquisition appetite signals (most important — slow-growth + cash hoard)**
- dividend_payout_5y_avg (high payout = no reinvestment runway = M&A appetite)
- last_capex_cr, capex_to_revenue (low capex + high cash = acquisition signal)
- last_acquisition_date, last_acquisition_value, acquisition_count_5y

**Governance**
- board_size, independent_directors, avg_director_age (older boards more open to inorganic)
- auditor, auditor_tenure_years

**Contact**
- ir_contact_name, ir_email, ir_phone
- cfo_name, cs_name

**Filings**
- last_qresult_date, last_annual_report_url

**Pipeline (internal)**
- tier, tier_reason, tk_score
- outreach_status, last_contacted
- notes, tags

---

## Risks & Gotchas

1. **NSE/BSE TOS**: prohibit commercial scraping/redistribution. Mitigation: internal lead list only, no resale.
2. **NSE Akamai bot defense**: bootstrap cookies via real-browser headers. `jugaad-data` handles this; raw requests fail.
3. **Screener TOS personal-use only**: heavy automated scraping = IP block. Manual CSV exports of saved screens are fine.
4. **yfinance freshness**: lags 2-4 quarters, gaps for mid-caps. Verify cash position against latest filed result, not yfinance.
5. **MCA21 V3 launched Jul 2025**: APIs stabilizing. Rs 100/company/year fee — limit to dossier deep-dives only.
6. **Covid distortion**: FY21-22 skewed margins. Compute 7-yr trailing instead of 5-yr where possible.
7. **Acquisition history is hard to source for free**: VCCEdge/Tracxn paid solve. Free proxy = news search + SEBI Reg 30 filings.
8. **Slow-growth + strong-fundamentals paradox**: many such companies are "promoter-comfortable" and NOT open to M&A. Filter must include behavioural signals: payout >50%, capex/sales <5%, idle cash >2 years, recent buyback.

---

## Tier-1 Starter List (20 companies)

All fit TK brief: listed, profitable 5 yrs, cash-rich, market leader.

| # | Company | NSE Ticker | Sector | Why fits |
|---|---------|-----------|--------|----------|
| 1 | ITC Ltd | ITC | FMCG/Cigarettes/Hotels | Rs 30,000+ Cr net cash; cigarette monopoly; 80%+ payout; slow growth; demerging hotels |
| 2 | Hindustan Unilever | HINDUNILVR | FMCG | Cash-rich, debt-free, oligopoly leader; 7-9% growth; acquisitive |
| 3 | Nestle India | NESTLEIND | FMCG/Foods | Negative working capital; debt-free; category dominance |
| 4 | Asian Paints | ASIANPAINT | Paints | Decorative leader (~50% share); high ROCE; cash-rich |
| 5 | Pidilite Industries | PIDILITIND | Adhesives/Chem | Fevicol monopoly; debt-free; serial acquirer |
| 6 | Larsen & Toubro | LT | Infra/EPC | Diversified leader; defence+tech subs; sits on cash; active inorganic |
| 7 | Mahindra & Mahindra | M&M | Auto/Farm Eq | Tractor leader; debt-free standalone; group famously acquisitive |
| 8 | Tata Consultancy Services | TCS | IT Services | Rs 73,000+ Cr cash; 30%+ ROE; tuck-in acquirer |
| 9 | Infosys | INFY | IT Services | Rs 36,000+ Cr cash; debt-free; serial inorganic |
| 10 | HCL Technologies | HCLTECH | IT Services | Rs 6,500+ Cr cash; debt-free; acquisitive |
| 11 | Wipro | WIPRO | IT Services | Rs 37,000+ Cr cash; Premji cash hoard; serial acquirer |
| 12 | Coal India | COALINDIA | Mining | Near-debt-free PSU; massive cash; 6%+ div yield; diversification mandate |
| 13 | Bajaj Auto | BAJAJ-AUTO | Auto/2W | Net cash >Rs 20,000 Cr; #2 in 2W; buyback history |
| 14 | Hero MotoCorp | HEROMOTOCO | Auto/2W | Cash-rich; #1 entry-level 2W; under-leveraged |
| 15 | Dr Reddy's Labs | DRREDDY | Pharma | Net cash positive; serial inorganic (US generics) |
| 16 | Sun Pharmaceutical | SUNPHARMA | Pharma | India #1 pharma; cash-rich post-deleveraging; serial acquirer (Taro, Concert) |
| 17 | Marico | MARICO | FMCG | Parachute/Saffola monopoly; debt-free; D2C acquirer (Beardo, Just Herbs) |
| 18 | Britannia Industries | BRITANNIA | FMCG/Foods | Biscuit leader; high payout; Wadia cash discipline |
| 19 | Cummins India | CUMMINSIND | Industrials/Engines | Cash-rich MNC sub; market leader; under-leveraged |
| 20 | CRISIL | CRISIL | Ratings/Analytics | Debt-free; cash-generating; S&P parent backing |

## Tier-2 Starter (17 companies, Mindtree-class)

Persistent Systems (PERSISTENT), Coforge (COFORGE), KPIT Tech (KPITTECH), Tata Elxsi (TATAELXSI), CAMS (CAMS), CDSL (CDSL), MCX (MCX), Page Industries (PAGEIND), Bata India (BATAINDIA), 3M India (3MINDIA), Honeywell Automation (HONAUT), Schaeffler India (SCHAEFFLER), Castrol India (CASTROLIND), Care Ratings (CARERATING), Gujarat Gas (GUJGASLTD), Supreme Industries (SUPREMEIND), Astral (ASTRAL).

---

## Recommended Next Actions

1. **Decide on Screener.in subscription** (Rs 1,400/yr) — it's the screening layer linchpin.
2. **Approve the data schema** above so we can build the SQLite table.
3. **Approve the Tier-1 starter list** (or edit) — these become our first outreach batch.
4. **Build the bootstrap pipeline**: NSE/BSE list → yfinance enrich → Screener filter → tier assignment.
5. **Stand up `Leads/` folder** in the repo with directory CSV + outreach tracker.
