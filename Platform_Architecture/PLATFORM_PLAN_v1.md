# M&A Leadership Platform - Architecture & MVP Plan (v1)

**Author:** Nishant (working draft for discussion with TK)
**Date:** 2026-07-08
**Inputs:** TK platform vision 07-03 (`TK_Platform_Vision/`), course blueprint v2 (`Curriculum/TK_Course_Blueprint/`), existing live build.
**Purpose:** TK's requested weekend first pass - platform architecture + what is MVP vs later. Two tracks run in parallel (course content, platform). This doc is the **platform** track.

---

## 1. The core idea (one line)

The platform is not a course website. It is each member company's **five-year capability-building workspace** - the place where classroom learning is converted into tracked ideas, patents, acquisition targets and integration outcomes. The classroom is the front door; the workspace is the building.

## 2. The five modules and what already exists

| # | TK module | What it does | Status today | MVP call |
|---|-----------|--------------|--------------|----------|
| 1 | **Learning Journey** | Course delivery, submissions, reflections, participant + company dashboards; visible, trackable, cumulative | Net-new (no app shell/login yet) | MVP-lite: the account home + journey view |
| 2 | **Ideas Funnel** | Capture course ideas, nurture idea -> funded -> piloted -> scaled over 5 yrs | Net-new | MVP prototype (sample pipeline) |
| 3 | **Patent-to-Enterprise Exchange** | Patent repository, business briefs, EOI, collaboration pathways (IIT Roorkee first) | Net-new | Phase 2 (thin catalogue stub in MVP) |
| 4 | **Target Sourcing** | Capability-led acquisition sourcing: gap -> filters -> longlist/shortlist -> fit -> outreach | **Partial** - `leads.html`+ARS exists but scores ACQUIRERS, not targets (see acquisition-targets-gap) | MVP: reframe leads into target sourcing |
| 5 | **Deal Integration** | Deal + integration thesis, Day-1, 30/60/90, workstreams, synergy, 5-yr value | **Exists** - `integration-room.html` (7-gate spine, milestones, India reg lane) | MVP: productize Room into the shell |

**Key insight:** modules 4 and 5 are ~70% built already. The MVP's job is to (a) wrap everything in one **company-account workspace shell**, (b) reframe leads as target sourcing, and (c) stand up credible prototypes of the three net-new surfaces - all brand-consistent, all sample-data driven (static, GitHub Pages), so TK can click through the whole five-year journey.

## 3. Architecture (MVP = static prototype, same repo)

Same repo `nishantn15/ma-platform`, new subfolder `platform/` so Pages links keep working:

```
platform/
  index.html            # Workspace home = company account dashboard (5-year overview across 5 modules)
  learning.html         # Module 1 - participant + cohort journey
  ideas.html            # Module 2 - ideas funnel (kanban pipeline)
  exchange.html         # Module 3 - patent-to-enterprise (catalogue stub)
  targets.html          # Module 4 - target sourcing (reframed from leads)
  integration.html      # Module 5 - deal integration (from integration-room)
  assets/               # shared navy/gold theme, lion, fonts (reuse DESIGN.md tokens)
  data/*.json           # sample data (thread ONE case - Anchor x Polaris - through all 5)
```

- **Brand:** reuse the locked system - Council Navy `#0a1628`, Lion Gold `#c9a84c`, cream, Playfair/DM Sans/JetBrains, Asiatic-lion, gold-ink for text-on-light (DESIGN.md). The workspace should feel like the same institution as the marketing site.
- **Shell:** persistent left nav (the 5 modules) + top account bar (company name, "Year 1 of 5", cohort). One consistent chrome across all six pages.
- **Connective tissue - the 5-year spine:** the account home shows a horizontal 5-year timeline; every module reports its state onto it (ideas maturing, patents in pipeline, targets in diligence, integration gate). This is what makes it a *workspace*, not five separate tools.
- **Sample-data thread:** reuse the **Anchor x Polaris** case already in the Integration Room so the whole platform tells one coherent story end to end.
- **No backend in MVP** - static HTML + JSON sample data. Real auth / multi-tenant / persistence is Phase 2. This is the right altitude for a "first pass to brainstorm."

## 4. MVP vs later (phasing)

**MVP (this pass - demonstrable prototype):**
- Workspace shell + account-home dashboard with the 5-year spine
- Module 5 Deal Integration: fold the existing Integration Room in
- Module 4 Target Sourcing: reframe leads/ARS into capability-gap -> target longlist/shortlist -> fit (adds the TARGET lens that closes the known gap)
- Module 2 Ideas Funnel: clickable kanban with sample ideas across the pipeline stages
- Module 1 Learning Journey: participant + company dashboard (progress, submissions, reflections) - lite
- Module 3 Patent Exchange: thin catalogue stub (a few IIT-Roorkee-style sample patents with business briefs)

**Phase 2 (after TK reacts):**
- Real accounts/auth, multi-tenant company data, persistence (backend)
- Live submissions, polls, cohort management for Learning Journey
- Full Patent Exchange with EOI + collaboration-pathway workflow
- Target Sourcing wired to the AlphaSense pipeline for live target discovery
- 5-year access controls / entitlement model

**Phase 3:**
- Ecosystem features: peer learning, cross-company idea/patent marketplace, analytics.

## 5. Commercial model (TK's 5-year access) - reflect in MVP framing

The MVP's account-home should visibly express the **five-year workspace** proposition (Year 1 of 5 badge, modules 2/3/5 usable across 5 years even without annual renewal). This is TK's differentiator vs "a course" - the MVP should *show* it, not just state it.

## 6. How this connects to the course track

The two tracks meet at Module 1 (Learning Journey) and the Ideas Funnel: what participants produce in M1/M2/M3 of the course flows into the workspace (ideas -> funnel, capability gaps -> target sourcing, the Integration Leadership Room capstone -> integration module). Build the platform shell so those handoffs are obvious even in the prototype.

## 7. Open questions for TK

- MVP scope: is a clickable, sample-data prototype the right first artifact to react to (recommended), or does he want a narrower deep-build of one module?
- Which module is the "wow" to lead the demo - Deal Integration (most built) or the 5-year account home (best expresses the vision)?
- Target Sourcing: confirm we build the missing TARGET-attractiveness lens now (vs continuing acquirer-only ARS).
- Does the 5-year-access entitlement need to be visible in the MVP or just narrated?

## 8. Immediate next step

Build the **workspace shell + account-home dashboard** first (it frames everything and expresses the vision), then fold in the Integration Room (module 5) and reframed Target Sourcing (module 4) since those have real substance, then the three sample-data prototypes. All in `platform/`, brand-consistent, one Anchor x Polaris story throughout.
