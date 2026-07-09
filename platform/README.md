# Platform MVP - the five-year capability workspace

Clickable static prototype of TK's 5-module platform vision (07-03). Lives in the
same repo so GitHub Pages links work: `nishantn15.github.io/ma-platform/platform/`.

## What it is
Each member company's **five-year capability-building workspace** - the classroom is
the front door; this is the building. All five modules are real (not placeholder
tiles), driven by one canonical data spine, threaded by one causal case.

## Pages
- `index.html` - Account Home: 5-year arc + live module rollups
- `learning.html` - M1 Learning Journey (blueprint content, 3 layers + personas, experiential loop)
- `ideas.html` - M2 Ideas Funnel (kanban pipeline, Patent-to-Enterprise Canvas, 5-yr maturation)
- `exchange.html` - M3 Patent-to-Enterprise Exchange (gallery + one real decision vs the deal)
- `targets.html` - M4 Target Sourcing (capability-gap -> longlist -> **Target Attractiveness Score**, 4 dims)
- `integration.html` - M5 Deal Integration (7-gate spine + 4-5yr value arc; productises the Integration Room)

## Architecture
- `data/spine.json` - **single source of truth**. Every page reads from it. Edit here.
- `assets/theme.css` - shared navy/gold brand theme (DESIGN.md tokens)
- `assets/shell.js` - renders the sidebar nav + account bar; loads the spine

## The causal thread (state continuity, not six colored pages)
M1 surfaces Anchor's capability gap -> seeds an Idea (M2) AND the capability-gap filter (M4)
-> TAS scores real targets, Polaris wins (M4) -> Polaris flows into the 7-gate deal (M5)
-> outcomes + matured ideas report onto the 5-year account home. A patent (M3) is scored
against the acquisition and loses on the 12-month talent horizon (kept as a Year-2 option).

## Status
MVP = static, no backend, sample-but-real data (Anchor x Polaris; AlphaSense-style targets;
IIT-Roorkee-style patents). Phase 2 = auth/multi-tenant/persistence, live AlphaSense target
discovery, full patent EOI workflow, 5-year entitlement model. See
`../Platform_Architecture/PLATFORM_PLAN_v2.md`.

## New this build: Target Attractiveness Score (TAS)
Closes the long-known gap (ARS scores acquirers, not targets). 4 orthogonal dimensions:
Transactability (30%), Strategic fit (35%), Integration risk inverse (25%), Data confidence (10%).
Scarcity is a tie-breaker, not a scored factor. Each target flags what is AlphaSense-supplied
vs manually enriched.
