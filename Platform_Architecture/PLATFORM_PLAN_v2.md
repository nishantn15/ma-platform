# M&A Leadership Platform - Architecture & MVP Plan (v2)

**Author:** Nishant (working draft for TK)
**Date:** 2026-07-08
**Supersedes:** PLATFORM_PLAN_v1.md (+ CODEX_CRITIQUE_v1.md)
**Decision:** Build the **full 5-module MVP**, but every module carries **real depth** (not a hollow stub). This directly answers Codex's v1 warning ("all-5 static demo = hollow modules") by refusing the hollow part: each module ships with genuine content, real data, or a real model. We have AlphaSense + the course blueprint + the existing build to make that possible.

---

## 1. Positioning (unchanged, now provable)

The platform is each member company's **five-year capability-building workspace**. The classroom is the front door; the workspace is where learning becomes tracked ideas, patents, targets and integration outcomes. v2's job: make all five modules feel *real*, so the 5-year promise is demonstrated, not merely claimed.

## 2. Depth commitment per module (the anti-hollow rule)

Each module must clear a "depth bar" before it ships in the MVP. No lorem-ipsum tiles.

| # | Module | Depth source (what makes it real) | Depth bar for MVP |
|---|--------|-----------------------------------|-------------------|
| 1 | **Learning Journey** | Course blueprint v2 (real M1/M2/M3 arc, personas per level, experiential loop) | Real course structure: L1/L2/L3 tracks, the 3-module year, a participant view with actual M1 "engine" case content + a company cohort dashboard. Content is genuine (from the blueprint), not placeholder. |
| 2 | **Ideas Funnel** | Course exercises produce real idea types; blueprint's Patent-to-Enterprise Canvas | Working kanban (submitted -> ... -> scaled) with 6-8 realistic seeded ideas that map to actual course outputs, each with the canvas fields filled. 5-year maturation shown on cards. |
| 3 | **Patent-to-Enterprise Exchange** | AlphaSense + real IIT-Roorkee-style patent domains; blueprint's Exchange spec (Gallery/Walkthrough/Canvas) | A real catalogue of 8-12 patents with business-language briefs, inventor/institute, industry use case, and the collaboration-pathway funnel. Sourced/plausible, not "coming soon." |
| 4 | **Target Sourcing** | AlphaSense research pipeline + **NEW target-attractiveness model** (see 4) | Capability-gap -> filters -> longlist/shortlist -> **target-attractiveness score** -> fit -> outreach. Real companies from AlphaSense, scored on the new model. |
| 5 | **Deal Integration** | Existing Integration Room (7-gate spine, milestones, India reg lane) | Fold the built Room in; per-deal instance, 30/60/90 + 5-year value track. Already substantial. |

**The rule:** if a module cannot clear its depth bar, it does NOT ship as a fake - it ships as an explicit, dated "in build" state with the real spec visible. Honesty over hollow.

## 3. The connective tissue - one company, five years, one case

Thread the **Anchor x Polaris** case (already in the Integration Room) across all five, but make the linkage causal, not cosmetic:
- Learning (M1) surfaces a **capability gap** ->
- that gap seeds an **Idea** in the funnel AND a **capability-gap** in Target Sourcing ->
- Target Sourcing scores real targets (incl. Polaris) on attractiveness ->
- the chosen target flows into **Deal Integration** (the existing 7-gate Room) ->
- integration outcomes + matured ideas report back onto the **5-year account home**.

This is a real workflow, not a curated slideshow - each module consumes the previous module's output.

## 4. NEW: Target-Attractiveness model (module 4's real substance)

Today's ARS scores **acquirer readiness**. Module 4 needs the inverse - how attractive a company is **as a target**. Build it as a distinct lens (separate column set, never overload ARS):

**Target Attractiveness Score (TAS)** - candidate factors (to refine with data):
- **Valuation headroom** - multiple vs sector median (cheaper = more attractive)
- **Succession / promoter exit signal** - promoter age, family-run, stake dynamics, stated exit intent
- **Distress / turnaround** - leverage, margin trend, covenant stress (fixable underperformance)
- **Fragmentation / roll-up fit** - sector concentration (fragmented = roll-up target)
- **Capability match** - does the target hold the exact capability the acquirer's gap names? (ties to the "Where Does Power Sit?" map)
- **Integration burden (inverse)** - size ratio, culture/geography proximity, founder-dependency
- **Scarcity** - is this capability rare / hard to build?

Data via AlphaSense (financials, promoter/holding, deal history) as already used for leads. Output: a ranked, filterable target longlist with a TAS breakdown per target - closes the long-known acquisition-targets gap.

## 5. Architecture (static prototype, same repo, real data)

Same repo `nishantn15/ma-platform`, new subfolder `platform/` (Pages links keep working):

```
platform/
  index.html          # Account home: 5-year spine + module rollups (real events)
  learning.html       # M1 Learning Journey (blueprint content, personas, cohort dash)
  ideas.html          # M2 Ideas Funnel (seeded real ideas, canvas fields)
  exchange.html       # M3 Patent Exchange (real catalogue + funnel)
  targets.html        # M4 Target Sourcing (TAS model, AlphaSense-sourced)
  integration.html    # M5 Deal Integration (existing Room, per-deal)
  assets/             # shared navy/gold theme, lion, fonts (DESIGN.md tokens)
  data/*.json         # real/plausible data, Anchor x Polaris thread
```

- **Brand:** locked system - Council Navy `#0a1628`, Lion Gold `#c9a84c`, cream, Playfair/DM Sans/JetBrains, Asiatic-lion, gold-ink on light (DESIGN.md). Same institution as the marketing site + Integration Room.
- **Shell:** persistent left nav (5 modules) + top account bar ("Anchor Industries - Year 1 of 5", cohort). Consistent chrome across all six pages.
- **Static MVP, real content.** No backend yet; JSON sample data that is genuine (AlphaSense-sourced targets/patents, real course content). Auth/multi-tenant/persistence = Phase 2. The MVP proves the *product*, not the infra.

## 6. Build order (substance-first, per Codex)

1. **Workspace shell + account home** (frames the vision; but built thin until modules feed it).
2. **Deal Integration (M5)** - fold in the existing Room (most built).
3. **Target Sourcing (M4) + TAS model** - real AlphaSense targets, the new score (highest net-new value; closes the gap).
4. **Learning Journey (M1)** - blueprint content, personas, cohort dash.
5. **Ideas Funnel (M2)** - seeded real ideas from course outputs.
6. **Patent Exchange (M3)** - real catalogue + funnel.
7. Wire the **causal thread** (4.3) so the home rolls up real module events.

## 7. Phasing beyond MVP

- **Phase 2:** real auth/multi-tenant/persistence; live submissions/polls/cohort mgmt; Target Sourcing wired live to AlphaSense; full Patent Exchange EOI + pathway workflow; 5-year entitlement model.
- **Phase 3:** ecosystem - peer learning, cross-company idea/patent marketplace, analytics.

## 8. Risks carried from Codex (and how v2 answers them)

- *Hollow modules* -> the depth-bar rule (2): real content or explicit "in build," never fake.
- *Overpromising Phase-2 delivery* -> MVP is explicitly a static prototype for brainstorming; infra deferred and labelled.
- *Category confusion (capability-building vs transaction tooling)* -> the causal thread (3) unifies them into one story: capability gap -> build/buy -> integrate. Still worth a positioning note for TK.
- *5-year access heavy for first buyer* -> flagged as commercial open question, not baked into MVP mechanics.

## 9. Open questions for TK

- The causal thread makes 5 modules one workflow - does that resolve the "5 separate tools" risk for you?
- Target Sourcing: confirm the new TAS model factors (section 4) - which matter most for your buyers?
- Which module leads the demo: the 5-year account home (vision) or Deal Integration (most tangible)?
- 5-year access: visible in MVP framing, or narrated only?

## 10. Immediate next step

Build in the order in section 6, starting with the shell + folding in the Integration Room, then Target Sourcing + the TAS model (the highest-value net-new). All in `platform/`, brand-consistent, one Anchor x Polaris causal thread throughout.
