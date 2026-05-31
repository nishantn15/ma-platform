# Product

## Register

**brand** (primary) — marketing landing page where design IS the product. Two product-register subsurfaces inherit the same brand: `/leads.html` and the forthcoming `/integration-room.html`.

## Users

**Primary audiences** (Boardroom Architects):
- CEOs, promoters, family-business heads, board members, group heads, corp dev heads, CFO/CHRO/CSO
- PE operating partners, family-office principals
- Reading on a laptop, at a desk, often alone, deciding whether to forward to their team

**Secondary audiences** (Integration Leadership Partners):
- VP / BU heads, integration leaders, functional heads (strategy, finance, HR, IT, ops, sales, transformation)
- Senior managers, analysts, sales/marketing integrators
- Reading the L2/L3 surfaces and the Integration Leadership Room demo

**Job to be done:**
- For the founder/CXO: convince me, in two minutes, that this institution can help me turn an acquisition into an enduring company. Convince me without selling.
- For the integration lead: show me the working machine — Day 1 readiness, 100-day plan, governance cadence — at a level my CEO would respect.

**Context when arriving:** A warm intro, a LinkedIn link from TK, or a forwarded email. Reader expectation: institutional, not transactional.

## Product Purpose

The M&A Leadership Platform is a capability institution for India's next generation of acquirers. It helps companies playing in India's mid-market arena build the boardroom judgment, integration leadership, and enterprise-wide M&A capability required to acquire with conviction, integrate with discipline, and scale into enduring institutions.

The site exists to:
1. Convey what the institution stands for, in the brand's own register
2. Make a Boardroom Architect want to spend 30 minutes with us
3. Show the Integration Leadership Partner that the execution is real
4. Surface the founding-cohort opportunity for partners worth onboarding

Success looks like: a CEO reads the site, forwards it to two people, and replies to TK.

## Brand Personality

Three words: **composed, institutional, certain.**

Voice and tone follow `BRAND_SYSTEM.md` — composure first, conviction second, evidence third. Calm authority that doesn't announce itself. Composure is not coldness; the brand has feeling, especially when speaking to founders.

Emotional goals by surface:
- Hero: certainty, gravity, restraint
- Founder section: weighted, unhurried, legacy
- L1 boardroom: discreet, peer-grade
- L2 execution: practical, milestone-driven, calm
- L3 champions: clear, confidence-building, role-aware
- Bundle / Integration Leadership Room: composed, instrument-grade
- CTA / Founding cohort: invited, not pitched

## Anti-references

**v6 must explicitly NOT look like any of these:**

1. **Generic SaaS landing aesthetic (Linear / Vercel / Stripe-clone).** Tinted-neutral palette, Inter everywhere, Bento grids, dashboard glow on hero, "modern" by-default. Overused in 2026 AI-built sites. The category default. v6 must avoid this default at every step.

2. **Big-4 / consulting brochure (Deloitte / PwC / EY).** Stiff corporate-brochure energy, heavy mega-nav, stock-photo handshakes, Georgia headlines, button-as-pill, stock skylines. v5 drifted here per Nishant's own self-note: "current content reads like a brochure."

3. **Indian fintech / startup gradient dashboard (Razorpay / Cred / glassy fintech).** Translucent glass panels, gradient meshes, neon accents, "fintech-bro" energy. Wrong register entirely for a boardroom audience.

4. **Generic strong-brand cliché.** Roaring lion, mid-charge tiger, mountain peak with arrow, chess piece, handshake-with-globe-overlay. The mascot section in `BRAND_SYSTEM.md §7` is explicit on this — *the lion is at rest, watching*.

5. **Aphoristic-cadence body copy.** "It is not X. It is Y." pattern repeated as default voice. The voice rules table in `BRAND_SYSTEM.md §6` lints this.

## Design Principles

1. **Composure over performance.** Negative space is the brand's calm. Generous gutters, restrained motion, the silence before the move. If a section feels rushed, salesy, or performative, it isn't on-brand. The reader's eye should rest, not race.

2. **Two rooms, one voice.** A founder reading the hero and an integration lead reading the L2 page must hear the same brand. The first names the *why*. The second names the *how*. Same DNA, different vocabulary. (BRAND_SYSTEM §2.)

3. **Show the machine, don't claim it.** The brand earns "institution-building" by showing real artefacts: the Day 1 checklist, the synergy tracker, the integration cadence. The Integration Leadership Room is the proof, not a screenshot. *The emotion is institution-building. The proof is execution capability.* (BRAND_SYSTEM §12.)

4. **The lion at rest, watching.** Visual identity recurs the Asiatic Lion — composed, social, India-rooted, Ashoka-connected. Never roaring, never charging. Stillness over aggression. (BRAND_SYSTEM §7-8.)

5. **Lines we don't paraphrase.** Six brand lines + one manifesto line are committed verbatim across surfaces (BRAND_SYSTEM §5). The hero pattern is canonical: eyebrow → master line → platform promise. Decoration is allowed; rewriting is not.

## Accessibility & Inclusion

- WCAG AA minimum (4.5:1 body, 3:1 large). Body text never sits at the muted-gray default that fails on tinted near-white.
- `prefers-reduced-motion` honoured on every animation. Reveal animations enhance an already-visible default; nothing is gated behind motion.
- Keyboard navigability: every interactive surface (tabs, accordions, dialogs, hamburger) reachable and visible-on-focus.
- Copy is screen-reader friendly: link text has standalone meaning ("View pricing plans" not "Click here"); button labels are verb + object.
- Mobile: full responsive, no horizontal scrolling, hamburger menu for nav <768px.
- The `.claude/skills/impeccable/reference/audit.md` checklist applies as the pre-ship lint pass.
