# Synthesis: May 20-24 TK Feedback vs Current State

**Sources:**
- TK WhatsApp May 20 (16:55, 16:58) — 6-point checklist
- TK WhatsApp May 23 02:46 — leads directory column requests
- TK shared May 22 docx — Brand Persona Blueprint v1
- TK shared May 23 docx — same + Overall Assessment + Asiatic Lion section
- Self-notes May 20 (16:42–16:51) — emotive video direction
- Date now: May 31, 2026 (~1 week after TK's last message; Nishant: "going through these" May 24)

---

## 1. TK's 6-point checklist (May 20 16:55-16:58)

| # | TK ask | Current state | Gap / next |
|---|--------|---------------|------------|
| 1 | **Lead — refine criteria** | v0.3 has 5 base criteria + slow-growth flag (19 names). | TK's May 23 expansion: add 6 column groups (see §3 below). Tier_score formula needs rebuild around "Acquisition Ready Score". |
| 2 | **Leads — contact and channel** | Schema has `cfo_name`, `ir_email`, `lead_owner`, `next_action` columns; dashboard exposes them. **No discovery script run yet.** | Build script 06: scrape NSE corporate filings (KMP) for top 50 names → populate CFO/CS/IR contacts + IR phone. Then "channel" framing: LinkedIn/email/warm intro. |
| 3 | **Demo of platform — end to end cycle, integration blown up** | Dashboard tab in v5 site shows Pipeline + Synergy chart — too thin. | Build a richer "Integration Leadership Room" demo: Day 1 readiness → 100-day plan → workstream tracker → synergy realization → governance cadence. Per-deal view, not aggregate. **TK's May 20 self-note echoes this: "platform kicks in" demo end-to-end.** |
| 4 | **Video — emotive feelings** | Not started. | TK's May 23 doc gives a full direction: "The Company You Leave Behind" — founder/promoter emotional arc. Self-note May 20 said: "focus on feelings to acquire someone and successfully integrate them. Show the triumph as a hook." Both align. |
| 5 | **Website content to be in sync with video content** | v5 site is informational/brochure; not emotive. Self-note: "current content is like a brochure. Next version is an emotive platform and video." | After video direction is locked, rewrite hero + key sections to mirror video's emotional beats. Brand voice rules (May23 §9) constrain language. |
| 6 | **Brand persona** | Not in v5. Asset images (low-poly lion) instinctively right per TK. | Apply full brand system from May23 doc: see §2. |

**Two of these (3 = integration demo, 4 = video) are TK's biggest jumps since v5. They're not visible in current site.**

---

## 2. Brand Persona Blueprint — what's now decided

### Master persona
**Institution Builder** — calm, unhurried, certain authority. Audience-specific expressions:
- **Boardroom Architect** (Founder/CXO)
- **Integration Leadership Partner** (L2/L3 execution)

### Core lines (TK-approved, use verbatim)
- **Master brand line:** "Boardroom judgment. Integration leadership. Enterprise-wide M&A capability."
- **Platform promise:** "Acquire with conviction. Integrate with discipline. Scale into an institution."
- **Founder line:** "You built a company. Now build an institution."
- **CXO line:** Same as platform promise.
- **Execution line:** "The deal is approved in the boardroom. Value is created through integration leadership."
- **Category idea:** "A capability institution for India's next generation of acquirers."

### Market thesis (sharpened)
> The mid-market **arena**, not merely mid-market companies, is the theatre. Buyer archetypes: large companies, mid-market consolidators, small firms scaling, PE platforms, founder-led / family businesses.

### Persona attributes
Composed · Boardroom-grade · Institution-building · Execution-obsessed · Discreet · Practical · India-rooted, globally credible.

### Brand voice rules (already a usable table)
- **Use more:** Conviction, integration leadership, institutional scale, boardroom judgment, capability, value capture, milestone discipline, founder legacy.
- **Use less:** Training program, course, modules, templates, features, networking opportunity, certificate, marketplace.
- **Avoid:** War room, play room, deal frenzy, salesy jargon, overclaiming, SaaS hype, generic consulting brochure tone.

### Terminology decisions
- **Integration Leadership Room** replaces "war room" everywhere.
- "Integration leadership" = the capability; the room is the operating format.

### Brand animal: Asiatic Lion (locked in)
Not just mascot. Five reasons:
1. Only big cat with a social structure (pride) — mirrors L1/L2/L3 exactly
2. Composed, not frantic — "boardroom-grade"
3. Rare and India-specific (Gir Forest only) — mirrors "India's first/only"
4. Ashoka Lion Capital connection — institutional intent, governance over conquest
5. Recur the lion **at rest, watching** — never roaring (avoid generic-strong cliché)

### TK's own assessment of his doc (May 23 — strengths / where to sharpen)
**Working well:** 3-layer persona architecture, 3-beat platform promise, founder line, "Integration Leadership Room" naming, voice rules table.

**Sharpen:**
- "Institution Builder" needs a behavioral one-liner (not just mission)
- §6 (Full-Cycle Platform Scope) reads like a feature matrix; move out of brand doc into product deck
- Video treatment column "Voiceover/message" too close to copy — should be emotional intent per scene
- "India's Next Acquirers" weaker as alternate; should be a manifesto line within primary

---

## 3. Leads directory expansion (TK May 23 02:46)

TK wants 6 column groups added + UX reorganized (collapse/expand groups via "+ button"):

| Group | Fields TK asks for |
|-------|--------------------|
| **Financials — Revenue** | Last year revenue, 5-yr CAGR |
| **Financials — Market Cap** | Absolute, change over last 5 years |
| **Financials — Cash** | Absolute amount, % of revenue |
| **Financials — Net Profit After Tax** | Absolute, % of revenue |
| **Financials — Operating Margins** | Last year %, 5-yr growth |
| **Acquisition Ready Score** | **Mathematical formula** based on: disposable cash, revenue growth slowing, op-margin shrinking, profit growth slowing |
| **Industry Benchmarks** | Industry tier (Large/Mid/Small or 4 quartiles) + change in rank over 5 years |
| **Recent M&A Activity** | Names of cos acquired last 5y, count, deal size (revenue), acquisition price |
| **Company Profile** | Parent co, # subsidiaries, # minority investments |

**Current schema covers ~30%.** Already have: market_cap, cash_and_equivalents, total_debt, debt_to_equity, profit_5y_cagr, slow_growth_signal.

**Missing (need build):**
- Revenue 5-yr CAGR + Operating Margin trend → can compute from yfinance financials (have the raw data, not extracted)
- 5-yr Market Cap change → need historical market cap (yfinance has it)
- NPAT % of revenue, Cash % of revenue → derivable from existing fields
- **Acquisition Ready Score** → TK's explicit formula needed; current `tier_score` is close but doesn't weight "slowing growth + shrinking margins" the way TK wants
- Industry tier ranking + change → need sector classification + market-cap rank within sector
- Recent M&A activity → external (news scrape, MCA filings, or paid Tracxn/VCCEdge)
- Company profile (subs, minority investments) → MCA21 filings or annual report scraping

**Dashboard UX:** TK wants column groups with collapse/expand. Current dashboard is flat — needs grouped sections.

---

## 4. Self-notes May 20 (Nishant) — distinct ideas not in TK's checklist

- **Peer-based learning + Institute-based learning** as twin pillars (already in v5 architecture)
- **"Xeal advisors"** to help with platform AND with integration (suggests external advisor network — different from faculty model)
- "Demo platform capture end to end cycle" — same as TK #3
- **"Integration ka blown up version"** — full-screen integration view, not a tab
- Video should focus on **emotion**: "capture leaders' emotions on successfully closing a deal, successful integration to closure"
- "Show the triumph as a hook" — visual climax
- "The current content is like a brochure. The next version is an emotive platform and video." — explicit acknowledgment v5 needs replacing

---

## 5. Where current site stands vs the new ask

| Piece | v5 (live) | Required by TK May 20-24 |
|-------|-----------|--------------------------|
| Information architecture | 3-layer cohorts + account model + bundle | Keep + add brand voice overlay |
| Brand voice/persona | Implicit | **Apply Institution Builder system everywhere — promise, founder line, voice rules** |
| Integration demo | Thin (1 dashboard tab) | **Full Integration Leadership Room demo, end-to-end deal cycle** |
| Emotive video | Absent | **"The Company You Leave Behind" — founder arc** |
| Hero copy | Functional | **Master line + platform promise + founder hook** |
| Asiatic Lion | Asset images use it | **Make the brand animal explicit; recur at-rest watching motif** |
| Leads dashboard | 8 financial columns + outreach | **Group columns, add 9 new fields + Acquisition Ready Score** |

---

## 6. Impeccable design system — what it gives us

TK's quality push (brochure → emotive) needs a design language to execute. Impeccable provides exactly this.

### 7 pillars
Typography · Color (OKLCH, tinted neutrals) · Spatial design · Motion · Interaction · Responsive · UX writing.

### Workflow we'd use
1. `impeccable craft` — interview-driven plan (creates `design.md` + `product.md`)
2. Generate **3 macro variants side-by-side** (transcript: editorial / drenched / brutalist) — pick one
3. `impeccable live` — browser-based micro-edits with `bolder` / `quieter` / `distill` / `delight` / `tune`
4. `impeccable critique` and `impeccable audit` — surface AI-slop anti-patterns
5. `impeccable polish` + `harden` — pre-ship pass

### Anti-patterns it flags (relevant to our v5)
- Pure black/gray without tinting — **v5 uses #0a1628 navy; check tint quality**
- Cramped padding & small touch targets
- Side-tab borders ("AI slop")
- Skipped heading hierarchy — **v5 had this in v4 critique**
- Bounce/elastic easing — **v5 uses these in some accordions**
- Overused fonts (system fonts without justification) — **v5 uses Playfair + DM Sans, OK**
- Excessive card nesting
- Purple-to-blue gradients — N/A for navy/gold
- Dark glows (low contrast) — **v5 hover states may trip this**

### What this means for v6
v5 is decent but has detectable v4-era patterns. Impeccable + the brand persona system + integration demo + emotive video = v6 should be a substantial rebuild, not a tweak. Worth running `impeccable critique` against current `index.html` first to get the verdict in writing.

---

## 7. Proposed next-steps stack (for review with Nishant)

### Track A — Brand & content (must precede any redesign)
1. Codify a `BRAND_SYSTEM.md` from May23 doc (one-pager, in repo root): personas, lines, voice rules, terminology, animal cues
2. Apply Asiatic Lion treatment guide ("at rest, watching") to existing brand assets — note which to keep, which to regenerate
3. Lock the founder-facing "The Company You Leave Behind" narrative in repo before video brief

### Track B — Site v6 redesign
4. Install Impeccable skill in repo (single-line install per video)
5. Run `impeccable document` against current `index.html` → reverse-engineer current `design.md`
6. Run `impeccable critique` → verdict in writing
7. `impeccable craft` with brand system + content pillars as input
8. Generate 3 macro variants side-by-side; share with Nishant + TK
9. Pick variant; run `impeccable live` for micro-tuning
10. `harden` + `polish` pre-ship pass

### Track C — Integration Leadership Room demo
11. Sketch the per-deal UX: Day 1 readiness → 100-day plan → workstream tracker → synergy → governance cadence
12. Static HTML mockup first; behind-the-tab demo on the site

### Track D — Leads v0.5
13. Compute the 9 new financial fields from existing yfinance data (revenue 5y CAGR, op margin trend, % of revenue ratios)
14. Implement TK's "Acquisition Ready Score" formula (he gave the inputs; we propose weights)
15. Add column-grouping with collapse/expand to `leads.html`
16. Build script 06: contact discovery (CFO/CS/IR) for top 50 leads from NSE filings

### Track E — Video brief (low-priority, blocked on v6 content lock)
17. Draft a video brief based on TK's storyboard but tightened per his own feedback (mood per scene, not voiceover)
18. Identify production options later

---

## 8. Open questions for Nishant

Before any execution:
1. Which track to sequence first — A (brand) or B (impeccable redesign)? They're tightly coupled.
2. Should v5 stay live as-is during v6 build, or take the Pages site offline for the rebuild?
3. Acquisition Ready Score formula weights — propose first or wait for TK's view?
4. Does "Integration Leadership Room demo" need to be a separate page (`/integration-room.html`) or stay as a tab?
5. The Asiatic Lion is locked. Do we keep current low-poly stylized assets or shift toward "lion at rest, watching" — meaning re-generate via codex?
6. Track E (video) — does Nishant want a written brief now or wait until B/C are done?
