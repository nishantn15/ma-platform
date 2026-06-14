# M&A Leadership Platform — Tasks & Backlog

Live working tracker. Update as items move through pending → in_progress → done.
**Last refreshed: 2026-06-14.**

Repo: github.com/nishantn15/ma-platform (Pages). Account: nishantn15.
Live: `/` = v6 site · `/integration-room.html` · `/leads.html` ·
prior versions under `Platform Prototypes/`.

---

## ✅ Shipped (Apr–Jun 2026)

| Area | What | Status |
|------|------|--------|
| Brand | BRAND_SYSTEM.md v2 — Institution Builder, Asiatic Lion, voice rules, message stack | ✅ |
| Brand | DESIGN.md (Council palette, named rules), PRODUCT.md (5 principles, anti-refs) | ✅ |
| Lions | 9 image files (3 lions × 3 sizes, "at rest, watching — never roaring") | ✅ |
| Site v6 | Full Navy & Gold rebuild; impeccable score 28/40 (v5 was 22); detector clean | ✅ |
| Site v6 | Swapped to root `index.html` (old index → Platform Prototypes/platform_v5_index.html) | ✅ |
| Track C | Integration Leadership Room — 7-phase Anchor×Polaris deal walkthrough | ✅ |
| Track C | AlphaSense accuracy pass — deal realism critiqued + 4 fixes (ops vs value window, retention breadth, change-of-control, margin dilution) | ✅ |
| Track D | Leads dashboard restructure — 4 collapsible column groups + ARS column | ✅ |
| Leads v0.6 | ARS compound flag (3 strong + 22 aligned), industry rank/size-tier, mcap-5y + cash/rev backfills, contacts capture (phone + preferred channel) | ✅ |
| Leads v0.7 | **Full T1 AlphaSense M&A research — 31 companies, 475 broker citations.** research table in leads.db + 33 briefs in Leads/research/ + merged into leads.json + "M&A Intel" dashboard group/drawer | ✅ |

## TK feedback (Jun 2 + Jun 6) — all addressed

| # | Ask | Status |
|---|-----|--------|
| 1/6/7 | Strike "100 days" → bold "4–5 years" everywhere | ✅ index, v6, Room |
| 3 | Reorder brand line → "One account. Three layers. Holistic capability." | ✅ |
| 4 | "+practitioner alignment" (not just faculty) | ✅ |
| 5 | "Commit to two" → **commit to three** (Room Phase 02) | ✅ |
| 8 | Expand capability-building (programmatic, smaller deals → bold deal) | ✅ |
| 9 | ARS compound flag | ✅ |
| 10 | Surface 19-name slow-growth hot list | ✅ |
| Jun-6 #1 | Industry benchmarks (rank, size-tier) | ✅ computed |
| Jun-6 #2 | Recent M&A activity (deals/sizes/dates) | ✅ AS, all 31 T1 |
| Jun-6 #3 | Company profile (parent/subs/minority) | ✅ AS, all 31 T1 |
| Jun-6 #4 | ARS more robust (qualitative signals) | ✅ intent/review/activist flags |
| Jun-6 #5 | Contacts + preferred channel | ✅ drawer capture UI |

---

## ⏳ Pending / Next

| # | Task | Status | Notes |
|---|------|--------|-------|
| E | **Promotional video brief** — "The Company You Leave Behind" | pending | TK's #1 priority. Lion-metaphor imagery instead of people, emoted per flow |
| — | **Brochure** | pending | TK priority #2 |
| — | **Pitch content** | pending | TK priority #3 |
| — | Send TK update (since Jun 8): 100-day reframe, commit-to-3, full T1 M&A intel live | pending | He's available; a lot has landed |
| — | T2/T3 AlphaSense research (38 T2 + 342 T3) | backlog | Only if TK wants depth beyond T1; ~credits scale |
| — | Pricing model for 3-layer account offering | backlog | Bundle vs per-cohort |
| — | Confirm IIT/IIM + practitioner partnerships | backlog | "proposed" → confirmed |

---

## Company Identification Criteria (from TK, Apr 28)

For inclusion in target lead list:

1. **Cash rich** — strong balance sheet, low leverage
2. **Known names in their industry** — market leaders in their domain
3. **Profitable last 5 years** — sustained earnings
4. **Traditional businesses are fine** — operating in own industry, blue or whitespace

**Bonus signal:** Slow growth despite strong fundamentals → board urge to acquire as growth lever (the 19-name hot list).

**ARS (Acquisition Ready Score, TK May 23):** 40% disposable cash + 25% revenue-growth-slowing + 20% margin-shrinking + 15% profit-growth-slowing. Compound flag fires when cash firepower + ≥2 fatigue signals align.

**Universe:** BSE/NSE listed. 752 scanned → T1 31 / T2 38 / T3 342.

---

## Course Architecture (3 Layers — companies as accounts)

| Layer | Cohort | Duration | Audience | Status |
|-------|--------|----------|----------|--------|
| L1 | Enterprise M&A Leaders | 2.5 days + capstone | CXOs, board, promoters, corp dev heads, PE op partners | live in v6 |
| L2 | M&A Execution Leaders | 5 days (Day 5 half) | VPs, BU heads, integration leaders, functional heads | live in v6 |
| L3 | Implementation Champions | 5 days (Day 5 half) | Senior mgrs, analysts, integrators (sales/marketing), workstream leads | live in v6 |

**Sales model:** Onboard companies (not individuals). Company is the account. All 3 layers unlock holistically when onboarded.

**Commercial launch:** Execution Leaders flagship → Enterprise premium invite-only anchor → Champions for scale → bundle = "M&A Capability Building Stack".

---

## Data pipeline (Leads/scripts/)

`01_build_universe` → `02_enrich_yfinance` → `03_fetch_indices` → `04_auto_tier` →
`05_export_json` → `06_enrich_v05` (ARS) → `07_enrich_v06` (compound flag, industry) →
`08_backfill_mcap5y` → `09_research_schema` → `10_ingest_research` →
`11_parse_as_output` → `12_batch_ingest` (AlphaSense M&A briefs).
DB: `Leads/data/leads.db` (tracked). Briefs: `Leads/research/<TICKER>.md`.
AS raw outputs auto-saved to `~/as-outputs/`.
