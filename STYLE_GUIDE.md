# M&A Leadership Platform — Style Guide

**Version:** 2.0 (post Apr 28 feedback)
**Status:** Active for v4 prototypes and beyond

> **TK feedback driving this version:** *"Text heavy, lack of visuals currently. Add visuals to convey the same meaning."*

---

## 1. Visual-First Principle

**Default to diagram. Prose only where a diagram cannot carry the meaning.**

| If you're tempted to write… | Use this instead |
|------------------------------|------------------|
| A list of 3 layers / tiers / stages | Pyramid, ladder, or stepped bar diagram |
| Comparison of 2-4 options | Side-by-side cards or comparison table with iconography |
| A process (more than 3 steps) | Horizontal flow with numbered nodes + connector arrows |
| Audience definition with attributes | Persona card with role / signal / outcome |
| Timeline (days, months, quarters) | Horizontal axis with milestone markers |
| Stats / proof points | Big-number panels — one stat per panel, large numeral, one-line context |
| Architecture / system structure | Layered block diagram with labeled regions |
| Trade-offs / quadrants | 2×2 matrix |
| Long bullet list (>5 items) | Group into 2-3 columns of cards |

**Diagram density rule:** Every section should have **at least one diagram or visual element above the fold**. Prose paragraphs of more than 3 lines are a smell — break into shorter beats, callouts, or a diagram.

---

## 2. Themes — Two Approved Treatments

### Theme A — Modern Minimalist (Editorial)
- **Charcoal** `#36454f` — primary text, dark sections, accents
- **Slate Gray** `#708090` — secondary text, subtle UI
- **Light Gray** `#d3d3d3` — dividers, target bars in charts, soft fills
- **Off-white background** `#f4f4f2` — alternating section bg
- **White** `#ffffff` — clean cards, light sections
- **Fonts:** Inter (body), Newsreader serif (headings), JetBrains Mono (labels)
- **Use when:** Modern, editorial, McKinsey-light, broadest audience

### Theme B — Navy & Gold (Luxury Finance)
- **Dark Navy** `#0a1628` — primary dark background
- **Navy Light** `#0f1f3a` — secondary dark surface
- **Gold** `#c9a84c` — primary accent, key numerals
- **Gold Light** `#ddc06a` — hover state, secondary accent
- **Cream** `#f8f6f0` — alternating light section bg
- **Fonts:** Playfair Display (headings), DM Sans (body), JetBrains Mono (labels)
- **Use when:** Premium, boardroom, CXO-facing, "anchor" feel

**Both themes share:** identical layout structure, identical diagrams (theme-recoloured), identical content. Themes are interchangeable.

---

## 3. Diagram Patterns (Required for v4+)

### Pattern A — Layer Pyramid (used for 3-layer architecture)
```
        ┌─────────────────────────┐
        │   L1  Enterprise         │  2.5 days
        │   (CXO / Board)          │  Boardroom-quality forum
        ├─────────────────────────┤
        │   L2  Execution          │  5 days
        │   (VP / BU Heads)        │  Applied + simulation
        ├─────────────────────────┤
        │   L3  Champions          │  5 days
        │   (Managers / Analysts)  │  Practical fluency
        └─────────────────────────┘
       Companies as accounts — all 3 unlock together
```
Build as stacked horizontal bars with: layer name, audience tag, duration chip, one-line promise.

### Pattern B — Cohort Comparison Matrix
3-column card grid. Each card: badge ("Premium" / "Flagship" / "Scale"), title, audience pill list, duration, signature feature line, "Outputs:" tag row.

### Pattern C — Capability Stack
Vertical building-block diagram showing L1 + L2 + L3 stacked → labeled bracket on the right reading **"M&A Capability Building Stack"**.

### Pattern D — Day-by-Day Mini Flow
Horizontal day cards (1→2→3→4→5) with: day number chip, theme, "Output:" pill. Used inside each cohort detail block.

### Pattern E — Big-Number Panels
For stats: `70–90%`, `INR 1L Cr+`, `3–5x`, `115,000+`. One numeral per panel, large, single context line below. Never a paragraph.

### Pattern F — Persona Cards
For audience definitions: 4-column grid. Each card: role title, comma-separated role tags (e.g. "CXO · Board · Promoter · PE Op Partner"), one-line "why they're here".

### Pattern G — Failure Spiral / Pattern Map
For L1 signature content (Billion-Dollar-Lessons-style). Concentric arcs or radial diagram listing acquisition failure modes: value leakage · cultural mismatch · synergy overclaiming · integration governance breakdown · stakeholder misalignment.

---

## 4. Content Density Rules

| Block type | Max length |
|------------|-----------|
| Section heading | 6 words |
| Section sub-line | 14 words |
| Card title | 4 words |
| Card description | 18 words / 2 lines |
| Stat panel context | 8 words |
| Day-card focus line | 20 words |
| Output / takeaway pill | 6 words |

**Prose paragraph rule:** If a paragraph exceeds 3 lines on desktop, split it or convert to a diagram.

---

## 5. Iconography

- No emoji. Use unicode geometric symbols or inline SVG.
- Approved unicode set: `◆ ■ ◎ ★ ⚙ ▲ ▼ ● ◇ □ ◻`
- All icons should sit inside a circular or square chip with consistent size (32–40px).

---

## 6. Layout Grids

- Container: max-width 1120px desktop
- Section padding: 100px vertical (desktop) / 60px (mobile)
- Card gutter: 20–24px
- Alternating section backgrounds (white ↔ off-white / dark) to visually segment

## 7. Interactions

- Nav: sticky, with active section highlight (IntersectionObserver)
- Tabs: tab bar with underline indicator on active
- Day cards: click-to-expand accordion with smooth max-height transition
- Hover: subtle lift (translateY -3px) + soft shadow on cards
- Scroll reveal: fade-up on entry (opacity + translateY)
- All buttons: subtle scale or color shift on hover, never bouncy

## 8. Accessibility

- Color contrast: WCAG AA minimum (4.5:1 for body, 3:1 for large text)
- Focus-visible outlines on all interactive elements
- `<noscript>` fallback so content is readable without JS
- Mobile hamburger nav (no horizontal scrolling)

## 9. Voice & Tone

- Direct, declarative. Past the buzzwords.
- Numbers and concrete nouns over adjectives.
- TK / personal contact info — **never on public surfaces** (web, GitHub, share links).
- Institutional / partner names — always footnote as **proposed / to-be-confirmed** until signed.

## 10. Privacy & PII Rules

- Public surfaces (GitHub repo, Pages site, shared HTML) must never contain: personal names, phone numbers, work emails, or unredacted reference deck binaries.
- The `Reference Decks/` folder is gitignored — originals stay local only.
- Use `[contact redacted]` or generic placeholders in any quoted email/call content that's pushed.
