---
target: platform_v6.html (post-patch Hybrid)
total_score: 28
p0_count: 0
p1_count: 0
timestamp: 2026-05-31T20-15-15Z
slug: platform-prototypes-platform-v6-html
---
# Critique — platform_v6.html (post-patch)

**Target:** `/storage/emulated/0/Download/MidMarket_MA_Platform_TK/Platform Prototypes/platform_v6.html`
**Date:** 2026-06-01
**Anchored against:** `PRODUCT.md` (5 design principles, 5 anti-references), `DESIGN.md` (Council Palette, named rules), `BRAND_SYSTEM.md` (verbatim message stack, voice rules, lion-at-rest spec)
**Predecessor:** v5 critique scored 22/40, 5 detector findings. Compare trend.

## Design Health Score (Nielsen)

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 4 | Sticky nav with active-section underline. Solid backdrop on scroll (post-patch). Tab/accordion state visible. |
| 2 | Match System / Real World | 4 | Vocabulary lands. "Acquire with conviction. Integrate with discipline. Scale into an institution." reads as committed not generic. |
| 3 | User Control and Freedom | 3 | Skip-link, keyboard reachable, mailto resolves. No back-to-top button (minor). |
| 4 | Consistency and Standards | 4 | All BRAND_SYSTEM verbatim lines preserved. Voice rules respected. Em-dashes ≤4 (down from 23). 0 side-tabs. 0 numbered scaffold. |
| 5 | Error Prevention | n/a | Informational page. |
| 6 | Recognition Rather Than Recall | 3 | Persistent nav, mono caps eyebrows above each section, scroll-spy works. Module rows now title-led without numeric scaffold. |
| 7 | Flexibility and Efficiency | 3 | No keyboard shortcuts. Hamburger handles mobile. 7 nav items + CTA — appropriate. |
| 8 | Aesthetic and Minimalist Design | 4 | Editorial register held throughout. Negative space is the brand's calm. The Manifesto section earns its silence. The promise block now uses the master line, eliminating v5's duplicate platform promise within 800px. |
| 9 | Error Recovery | n/a | No error states. |
| 10 | Help and Documentation | 3 | Founder paragraph + L1/L2/L3 deep-dives onboard naturally. Still no FAQ or glossary. |
| **Total** | | **28/40** | **Acceptable with strong moments. v5 → v6: +6 points.** |

## Anti-Patterns Verdict

**Does this look AI-generated?** No, not in the way v5 did. Specifically:

**LLM assessment (Assessment A):**

1. **Side-tab borders eliminated.** The 3 instances flagged in v5 (`.cohort-tier`, `.persona`, `.bundle-block`) are gone. Cohort architecture is now hairline-separated rows; cards use top-edge gold accents only. **This was the biggest AI-tell. Resolved.**

2. **Numbered display eyebrows eliminated.** The architecture row's `01-05` and the modules' `M.01-M.05` mono designators are both removed. Modules now read as title-led editorial rows. **Resolved.**

3. **Em-dashes reduced from 23 to 4.** Each remaining em-dash is in a canonical message-stack line (capstone titles, "Day 3 — Half" type indicator). No aphoristic-cadence default voice. **Resolved.**

4. **Card-on-card nesting eliminated.** Cohort architecture is rows, not cards-with-image-card-inside-them. **Resolved.**

5. **CTA decoration eliminated.** No pulse rings, no halos, no decorative gold dots. Single white button on navy. Hairline gold dashes prefix benefits. **Resolved.**

**Deterministic scan (Assessment B):** **0 findings.** Detector clean. (v5: 5 findings.)

**Visual overlay:** Browser automation succeeded; 8 scroll-position screenshots verified the page renders the brief. The hero, modules, cohorts, L1/L2/L3, capability stack, manifesto, and CTA sections were each visually inspected against the locked palette and DESIGN.md rules.

## Overall Impression

**v6 delivers brand v2 made real.** The single biggest gain over v5 is the page now reads as composed-by-default rather than composed-with-decoration-overlaid. The Manifesto section is the moment the brand's claim earns its register — pure stillness, the platform promise in italic serif on navy, "A FOUNDING MANIFESTO" in mono gold beneath, no other ornament. The hero's lion-at-rest signature, the cohort architecture as hairline rows, and the capability stack with the cub on stacked plinths are each on-brief and execute the BRAND_SYSTEM contract.

The biggest opportunity now is L2/L3 deep-dive density. They earn their seriousness but feel similar in pattern (audience pills + sim names + day grid). One signature treatment per layer would distinguish them.

## What's Working

1. **The Manifesto section is the page's strongest moment.** It is not decoration. It is the brand making its claim and walking away. A founder reading this will pause.

2. **Hero composition is the brief delivered.** Manifesto-scale serif, mono caps eyebrow, italic platform-promise sub, single gold CTA, lion-at-rest with the radial fade-mask blending into page navy. The hero hits the registers PRODUCT.md asked for: certainty, gravity, restraint.

3. **3-Layer cohort architecture as hairline rows is the right answer.** No card chrome competing with the content. Group Heads correctly in L1 audience. Each row is one scan-line of useful information.

4. **CTA is invited, not pitched.** "Limited Founding Cohort" eyebrow, big serif "Join as a Founding Partner", quiet sub, 5 bullet benefits each prefixed by hairline gold dashes, single white button, italic footnote. Zero performance.

5. **Voice and visual rules held without exception.** No paraphrasing of BRAND_SYSTEM lines on customer-facing surfaces. No fourth color. No fourth font. No glassmorphism. No bounce easing. Three families: Playfair, DM Sans, JetBrains Mono.

## Priority Issues

1. **[P2] L2 and L3 day-grids share the same visual rhythm.** Both deep-dives use 5-card grids on the same axis. After scrolling through one, the second reads as repetition. **Fix:** keep L2 as the 5-card grid (flagship, full applied intensive). Render L3 as a 2-column day-list (Day | Theme) on cream — emphasising practicality over symmetry. **Suggested command:** `/impeccable distill` on the L3 section.

2. **[P3] Lion image edge fade is correct on hero but absent on `lion_council` and `lion_cub`.** The radial mask was applied only to `.hero-lion img`. The L1 council image and the capability-stack cub image still show their painted-frame boundaries faintly. **Fix:** add the same radial-gradient mask to `.l1-image img` and `.stack-image img` for consistency.

3. **[P3] Module rows could use one signature differentiator.** Currently they're 5 identical hairline-row patterns. Adding a single subtle visual cue per module (a small mono caps "TIME" or "RHYTHM" tag, or an icon glyph in the gutter) would differentiate without adding decoration. **Suggested command:** `/impeccable bolder` on `.module-row` selectively.

## Persona Red Flags

**Boardroom Architect (CEO, founder, family business head):** Lands on the manifesto-scale hero. Reads the master brand line. Sees the lion. Scrolls past the platform promise and the 70-90% problem. Hits the founder paragraph with drop-cap on cream — *this is the moment they decide to keep reading.* The cohort architecture row layout reads as a private memo. The L1 deep-dive shows them they're the audience without naming them generically. The Manifesto section is where they reach for forward. **Outcome: forwards to a peer, not just to corp dev.**

**Integration Leadership Partner (VP, BU head, integration lead):** Deep-links into the L2 section from a sales/marketing-integrator outreach. The 5-card day grid plus the 9-Artifact Integration Blueprint Binder gives them the artefact list they came for. Sims named (Deal Thesis Defense, IMO Sprint Room, Synergy Pressure Test, CXO Panel Capstone) read as practical. **Outcome: convinced this is a real working program; asks about pilot.**

## Minor Observations

- `prefers-reduced-motion` honoured (verified in CSS + JS).
- `<noscript>` block keeps `.reveal` content visible.
- 7 `focus-visible` rules across skip link, buttons, links, tier CTAs.
- Hamburger is a `<button>` with `aria-expanded` toggling correctly.
- All 9 lion image variants referenced; srcset at 800/1200/1600 widths.
- Em-dash count: 4 (canonical only).
- Container max-width: 1120px (matches DESIGN.md).
- Section padding: 100px desktop (matches DESIGN.md).
- 0 personal info (no Tribhuwan, no 9029 phone, no work emails).
- Page weight: 80KB HTML + ~440KB lions (3 sizes × 3 lions). Under 600KB total — light.
- Total weight after Pages assets cache: very fast first paint.

## Questions to Consider

- **Should the founder paragraph drop-cap be gold instead of navy?** Currently navy on cream. Gold would tie the editorial moment back to the brand accent. Worth a single A/B test.
- **The "FOUNDING MANIFESTO" mono caps after the centred italic line — should it sit above the line as an eyebrow instead of below?** Currently below. Above would frame it as "this is what follows is the manifesto" rather than "this was the manifesto."
- **Is the v6 promise block (using master line) earning its space?** It currently sits between the hero and the 70-90% Problem section. It might be redundant — the hero already carried the master line. Consider removing the promise block entirely, letting hero → Problem flow directly.

## Trend
- v5 (2026-05-31): 22/40, 5 detector findings, 2 P0 + 3 P1
- v6 (2026-06-01): **28/40**, **0 detector findings**, 0 P0 + 0 P1 + 1 P2 + 2 P3

**+6 points. Detector clean. P0/P1 cleared.** Eligible for swap to `index.html`.
