# v6 Site — Shape Brief (Compact)

**Per impeccable craft Step 1.** Brief is clear from `PRODUCT.md` + `BRAND_SYSTEM.md` + `DESIGN.md` + the v5 critique findings. Compact form.

---

## What we're building

A complete rebuild of the M&A Leadership Platform marketing landing page (`/index.html` on Pages), replacing v5 (currently live at https://nishantn15.github.io/ma-platform/). Single self-contained HTML file (no build pipeline; matches v5's deployment shape).

## Visual lane

**The Council Chamber** (DESIGN.md Creative North Star). Editorial / boardroom-grade / institutional. Three colours: navy + lion gold + cream. Three families: Playfair Display + DM Sans + JetBrains Mono. The Asiatic Lion at rest, watching — never roaring. Negative space carries the brand's calm. Decoration is forbidden in empty space.

## What changes vs v5

- Strip the 5 priority issues from the v5 critique (side-tab borders ×3, numbered section markers, em-dash overuse, card-on-card nesting, pulse-ring decoration in CTA)
- Lions v2 replace v5's pyramid_hero / boardroom_l1 / capability_stack — three locations
- Manifesto line earns its own quiet section (currently absent from v5)
- Founder paragraph (BRAND_SYSTEM §11) gets a dedicated section above L1 deep-dive
- Voice rules table (BRAND_SYSTEM §6) is the lint pass for every line of copy

## What stays

- 3-layer cohort architecture (L1 / L2 / L3) — content unchanged
- Hero canonical pattern (eyebrow → master line → platform promise)
- ROI panel, Anchors row, Roadmap timeline, Founding cohort CTA
- All accessibility wins from v4→v5 (skip-link, focus-visible, hamburger button, prefers-reduced-motion, alt text, lazy load, noscript)
- Mailto-resolved CTAs (no #cta self-loops)

## Three macro variants we'll generate

Per the impeccable craft protocol — show 3 macro lanes side-by-side before micro-tuning.

1. **Editorial** — long-form magazine register. Generous gutters, big serif headlines, single column where possible, sectioned by horizontal gold rules. The Monocle / Apolitical lane.
2. **Boardroom** — tight institutional. Smaller display sizes, denser hierarchy, more navy, the cream sections do less. The Bridgewater memo / law-firm lane.
3. **Manifesto** — strong opinion-piece register. The manifesto line ("India's next acquirers will not be louder. They will be more composed.") drives the page. Hero is the manifesto. The lion is large and singular. The Apple keynote / Nike "Sound Mind, Sound Body" lane.

All three respect DESIGN.md tokens, anti-references, and the lion-at-rest spec. They differ in **density, tone, and which message-stack line leads**.

## Confirm or override

Specifically:
1. Are the three macro lanes the right three? (Alt: Boardroom / Editorial / Boardroom-with-Manifesto-section.)
2. v6 ships single-file HTML (matches v5 deployment), correct?
3. Path: replace v5 `index.html` directly, or build at `Platform Prototypes/platform_v6.html` first and swap once approved?

Once locked, I'll generate the three variants and present side-by-side before any single-direction polish.
