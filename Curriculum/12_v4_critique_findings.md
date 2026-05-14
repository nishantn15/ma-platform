# v4 Prototypes — Rubber-Duck Critique Findings
**Source:** Codex (GPT-5.4) independent review
**Date:** May 14, 2026
**Files reviewed:** `platform_v4_navy_gold.html` (2097 lines), `platform_v4_minimalist.html` (1589 lines)

---

## Verdict

> Both prototypes are a substantial step forward from text-heavy v3 drafts and implement the 3-layer cohort architecture credibly — the curriculum content, sim names, 9 artifacts, and persona tracks are largely present and correctly labeled. However, v4 has three categories of genuine risk:
>
> 1. **Content contradictions** (Platform Partner "all 5 modules" vs account model "all 3 layers", Growth Member implying partial access while account model promises full unlock, roadmap launching L1 before L2 against TK's explicit commercial logic) — a skeptical CFO or co-founder will catch these on first read.
>
> 2. **Accessibility failures** — complete absence of `focus-visible` styles, navy hamburger is a non-interactive `<div>`, making keyboard nav broken on the premium theme.
>
> 3. **Visual depth** — style guide's pattern requirements for SVG diagrams (pyramid, capability stack brace, failure spiral) remain unimplemented; the most important architecture visuals are CSS-only approximations that don't match the "McKinsey × Monocle" standard.

---

## TOP 5 FIXES BY IMPACT

**1. Fix account model / membership contradiction (A2, A9)** — Platform Partner says "all 5 modules" not "all 3 layers." Growth Member implies partial cohort access. Two contradictions on a single scroll make the commercial model unreadable to a CFO.

**2. Navy accessibility overhaul (E1, E2, E5, E6)** — Replace `<div class="hamburger">` with `<button>`, add `aria-expanded`, `prefers-reduced-motion`, `<main>`, `aria-label` on all sections. Port minimalist's a11y wholesale to navy.

**3. Add `focus-visible` styles to both files (E3)** — Zero focus states across 3686 combined lines. One CSS rule fixes both. Highest effort-to-impact ratio.

**4. Replace duplicate pyramid_hero in cohorts section with CSS/SVG pyramid (C1, C2)** — Pyramid appears twice in the same scroll. Cohorts section is the most important diagram. Replace photo with a stacked-bar pyramid per STYLE_GUIDE Pattern A.

**5. Content corrections aligning to TK's Apr 28 framing (A1, A11, A7, A4)** — Add "Group Heads" to L1 audience. Flip roadmap to launch L2 first. Add Escalation Game sim to L3 Day 3. Use "Announcement Day Tabletop" in minimalist.

---

## CRITICAL (4 findings)

### A2 — Platform Partner "all 5 modules" contradicts account model
**Files:** Both, navy line 1871
Account model says "all 3 layers unlock"; Platform Partner tier says "Full access — all 5 modules". Conflates the 5 platform modules with the 3 cohort layers.
**Fix:** Change to "Full access — all 3 cohort layers + all 5 platform modules" or split into two bullets.

### A9 — Growth Member tier contradicts account model "all 3 layers unlock"
**Files:** Both, navy lines 1892–1904, minimalist lines 1363–1375
Growth Member only mentions "observer access to forums" and "1 integration feature engagement". If account model is "all 3 layers unlock", what does Growth get?
**Fix:** Either explicitly exclude Growth from account model OR clarify cohort access (e.g., L3 only, or observation-only).

### E1 — Navy hamburger is `<div>` not `<button>`
**Files:** Navy line 1409
Not keyboard-focusable. Lacks `aria-expanded`. Minimalist correctly uses `<button>` (line 871).
**Fix:** Change to `<button type="button" class="hamburger" aria-label="Open navigation menu" aria-expanded="false" id="hamburger">` and toggle `aria-expanded` on open/close.

### E2 — Navy: No `prefers-reduced-motion` media query
**Files:** Navy
All fade-up animations trigger unconditionally. Minimalist correctly implements (line 772).
**Fix:** Add `@media (prefers-reduced-motion: reduce) { .fade-up { opacity: 1; transform: none; transition: none; } }`

### E3 — No `focus-visible` styles anywhere
**Files:** Both
Zero focus state CSS. Every button/link invisible to keyboard users on tab.
**Fix:** `:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }`

---

## SHOULD-FIX (22 findings)

### A. Content accuracy
- **A1** — L1 audience omits "Group Heads" (both files)
- **A3** — L1 Day 3 outputs truncated; missing "integration governance" + "stakeholder narrative"
- **A4** — L2 sim name: minimalist uses "Announcement Tabletop", should be "Announcement Day Tabletop"
- **A5** — "CXO Panel Presentation" should be "CXO Panel Capstone" (both)
- **A6** — Navy missing "9-Artifact Integration Blueprint Binder" label
- **A7** — L3 Day 3 "Escalation Game" sim absent (both)
- **A8** — Account Model section missing renewals/expansions/roadmap reviews
- **A11** — Roadmap order: L1 launches Q2 in minimalist, but TK said L2 should be flagship-first

### B. Style guide compliance
- **B1** — Minimalist: 8 heading violations exceeding 4-word card limit
- **B2** — Prose paragraphs >3 lines in 4 places across both files

### C. Visual design
- **C1** — Zero inline SVGs; all diagrams are CSS-only approximations (no capability-stack brace, no failure spiral)
- **C2** — `pyramid_hero.jpg` used twice in same scroll (hero + cohorts section) — looks like asset shortage
- **C3** — Minimalist module section missing flow connector (navy has gold gradient line)
- **C4** — Navy: L1/L2/L3 deep-dive sections have no `id` attributes
- **C5** — Navy: Anchors/Roadmap sections have no `id` attributes

### D. UX flow
- **D1** — Anchors/Roadmap not in nav (both)
- **D2** — `Request Access` buttons point to `#cta` self-loop (both) — buttons go nowhere
- **D3** — Account Model section redundant with Cohort Architecture overview (both introduce "all 3 layers unlock")

### E. Technical
- **E4** — Navy noscript fallback insufficient
- **E5** — Navy: No `<main>` landmark element
- **E6** — Navy: Only 1 `aria-label`; minimalist has 30
- **E7** — Container max-width 1240px deviates from STYLE_GUIDE spec (1120px)
- **E8** — Section padding 120px+ deviates from spec (100px)

### F. Missing elements
- **F1** — Day 3 missing "Dependency Map" + "Governance Cadence" artifacts
- **F2** — L3 "Integration Champion Field Kit" not mentioned (parallel to L2 binder)
- **F3** — "Cascade Communication Map" (Day 2 output) missing or merged into Stakeholder Comms Map without note

### G. Theme parity
- **G1** — 12 structural differences between navy and minimalist that should be identical content/structure but aren't (see critique for full table)

---

## NICE-TO-HAVE (10 findings)

- **A10** — Year-Long Coaching Engagement (optional 3-touchpoint post-L2 support) not surfaced
- **B3** — Navy uses `◈` and `◉` outside approved unicode set
- **B4** — Membership section lacks visual hierarchy element (suggest 3×3 tier-vs-modules matrix)
- **B5** — STYLE_GUIDE Pattern G (Failure Spiral / Pattern Map) not implemented for L1 Billion-Dollar Lessons
- **C6** — Minimalist image-panel-caption contrast risk on dark overlay
- **D4** — Day 4 label "Synergy, Risk, Stakeholder" loses "Management"; reads abstract
- **E9** — No skip-to-main-content link in either file (WCAG 2.4.1)
- **E10** — Google Fonts loaded without `&display=swap` causing FOUT/FOIT risk
- **F4** — Faculty model (Practitioner + Academic pair) not described anywhere
- **F5** — TK's "to know acquisition and integration" quote unattributed; consider "— Founding mandate"

---

## Theme parity table (G1 — key inconsistencies)

| Element | Navy/Gold | Minimalist |
|---|---|---|
| L1/L2/L3 section `id` attributes | Missing | Present |
| Anchors/Roadmap section `id` | Missing | Present |
| "9 Artifacts" label on toolkit | Missing | Present |
| Hamburger element type | `<div>` (broken) | `<button>` (correct) |
| `aria-label` on sections | 1 instance | 30 instances |
| `prefers-reduced-motion` | Absent | Present |
| `<main>` landmark | Absent | Present |
| Module connector line | Gold gradient | None |
| L2 Announcement sim name | "Announcement Day Tabletop" | "Announcement Tabletop" (wrong) |
| CTA section `id` | `#cta` | `#access` |
| Roadmap launch order | Vague | L1 first (wrong — should be L2) |

**Bottom line on parity:** Navy is the content baseline. Minimalist is the accessibility baseline. Fix needs both directions of porting.
