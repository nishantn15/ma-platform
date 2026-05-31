---
name: M&A Leadership Platform
description: Boardroom judgment. Integration leadership. Enterprise-wide M&A capability.
colors:
  navy: "#0a1628"
  navy-light: "#0f1f3a"
  navy-mid: "#162a4a"
  gold: "#c9a84c"
  gold-light: "#ddc06a"
  gold-dim: "rgba(201,168,76,0.15)"
  gold-glow: "rgba(201,168,76,0.08)"
  cream: "#f8f6f0"
  cream-dark: "#eee9df"
  white: "#ffffff"
  text-dark: "#1a1a2e"
  text-muted: "#5a5a6e"
  text-light: "rgba(255,255,255,0.78)"
  text-light-dim: "rgba(255,255,255,0.6)"
typography:
  display:
    fontFamily: "Playfair Display, Georgia, serif"
    fontSize: "clamp(40px, 5.6vw, 64px)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Playfair Display, Georgia, serif"
    fontSize: "clamp(32px, 4.2vw, 48px)"
    fontWeight: 600
    lineHeight: 1.18
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Playfair Display, Georgia, serif"
    fontSize: "clamp(22px, 2.6vw, 28px)"
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "DM Sans, -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "JetBrains Mono, monospace"
    fontSize: "11px"
    fontWeight: 500
    letterSpacing: "0.18em"
rounded:
  xs: "2px"
  sm: "3px"
  md: "8px"
  lg: "16px"
  pill: "20px"
  full: "50%"
spacing:
  nav-height: "72px"
  section-pad: "100px"
  section-pad-tablet: "80px"
  section-pad-mobile: "70px"
  max-width: "1120px"
components:
  button-primary:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.navy}"
    rounded: "{rounded.md}"
    padding: "14px 28px"
  button-primary-hover:
    backgroundColor: "{colors.gold-light}"
    textColor: "{colors.navy}"
    rounded: "{rounded.md}"
    padding: "14px 28px"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.gold}"
    rounded: "{rounded.md}"
    padding: "14px 28px"
  card-light:
    backgroundColor: "{colors.cream}"
    textColor: "{colors.text-dark}"
    rounded: "{rounded.lg}"
    padding: "32px"
  card-dark:
    backgroundColor: "{colors.navy-light}"
    textColor: "{colors.text-light}"
    rounded: "{rounded.lg}"
    padding: "32px"
  pill-label:
    backgroundColor: "{colors.gold-dim}"
    textColor: "{colors.gold}"
    rounded: "{rounded.pill}"
    padding: "4px 12px"
---

# Design System: M&A Leadership Platform

## 1. Overview

**Creative North Star: "The Council Chamber"**

The system is a chamber, not a storefront. Composed, deliberate, dimly-lit by gold; everything in it has been placed with intent. The reader enters expecting a brochure and finds, instead, an institution speaking with composure and feeling. Density is editorial — generous gutters, restrained motion, large negative spaces where a less confident system would crowd in features. The Asiatic Lion at rest is the signature: power held in stillness, never advertised.

This system **explicitly rejects** four registers (per `PRODUCT.md`): the SaaS-clone aesthetic (tinted-neutral palette, Inter, Bento, dashboard glow); the Big-4 brochure (mega-nav, stock handshakes, button-as-pill); the Indian fintech glassy-gradient (translucent panels, gradient meshes, neon accents); and the generic strong-brand cliché (roaring lion, mountain peak, chess piece). The pages are quiet. They earn their gravity.

**Key Characteristics:**
- Navy + gold against cream — three colors carrying the entire system
- Editorial display serif, humanist body sans, monospace labels — three fonts, no more
- The accent is rare. Gold appears on ≤10% of any given screen
- Negative space is the brand's calm; we don't fill it to look full
- Motion is restrained. The page does not perform; the reader does

## 2. Colors: The Council Palette

A three-color system: deep institutional navy, restrained editorial gold, and cream as the quiet contrast. Every other token is a shade of these three.

### Primary
- **Council Navy** (#0a1628): The chamber walls. Hero backgrounds, dark sections, the foundation of the brand's gravity. Every surface that wants to feel "boardroom-grade" sits on this navy.
- **Council Navy Light** (#0f1f3a): Card surfaces inside dark sections. Used to layer without breaking the navy continuity.
- **Council Navy Mid** (#162a4a): Subtle elevation — borders, dividers, hover lifts on dark backgrounds.

### Secondary
- **Lion Gold** (#c9a84c): The accent. Rare and considered. Logo lions, key numerals, primary CTAs, hover hints. Never decorative; always carrying meaning.
- **Lion Gold Light** (#ddc06a): The hover/active state for gold. Brightens by 12%; never flashes neon.

### Neutral
- **Parchment Cream** (#f8f6f0): The light section background. The "soft-light" half of the page rhythm. Body sections, ROI panels, persona cards.
- **Parchment Cream Dark** (#eee9df): Dividers, table-row alternation, restrained-emphasis tints on cream surfaces.
- **Pure White** (#ffffff): Card surfaces inside cream sections. The cleanest reading surface for body text.
- **Ink** (#1a1a2e): Body text on light backgrounds. Sits at 16:1 contrast on cream — passes AA/AAA without effort.
- **Ink Muted** (#5a5a6e): Secondary text, captions, eyebrows on light. Hits 7:1 on cream — never the muted-gray-on-tinted-white that AI-built sites default to.
- **Ink on Dark** (rgba(255,255,255,0.78)): Body text on navy. Slightly tempered white to avoid clinical contrast.
- **Ink on Dark Dim** (rgba(255,255,255,0.6)): Captions, eyebrows on dark surfaces.

### Named Rules

**The One-Voice Gold Rule.** Lion Gold appears on ≤10% of any given screen. Its rarity is the point. Gold stops being a brand cue the moment it becomes a divider color. If a screen reads as "lots of gold," it's wrong.

**The Three-Color Rule.** Navy. Gold. Cream. Every other value is a shade or transparency of these. No fourth accent. No "and a bit of green for success states." The system is built on restraint.

**The Tinted-Black Rule.** No `#000000`. No `#222`. Pure black is harsh and dated. Where we need "darker than navy," we use Council Navy at 100% — the system's deepest value.

## 3. Typography

**Display Font:** Playfair Display (with Georgia, serif fallback)
**Body Font:** DM Sans (with -apple-system, BlinkMacSystemFont, sans-serif fallback)
**Label / Mono Font:** JetBrains Mono (with Courier New, monospace fallback)

**Character:** A pairing on the contrast axis — high-contrast editorial serif against a humanist geometric sans. Playfair's modulated stroke and tall capitals carry the institutional gravity; DM Sans's open counters and clear x-height carry the body without competing. JetBrains Mono earns its place as labels only — eyebrows, day-chips, stat tags — never as body. Three families, no more.

### Hierarchy
- **Display** (700, clamp(40px → 64px), 1.1, -0.02em letter-spacing): Hero H1 only. The master brand line.
- **Headline** (600, clamp(32px → 48px), 1.18, -0.01em): Section titles. The "The Council Architecture" / "Three Layers. One Account." anchors.
- **Title** (600, clamp(22px → 28px), 1.3): L1 / L2 / L3 sub-headings, card titles, persona names.
- **Body** (400, 16px, 1.65): All running prose. Capped at 65–75ch line length on hero copy and reusable paragraphs.
- **Label** (500 mono, 11px, 0.18em letter-spacing, all-caps allowed): Eyebrows above section titles, day-chips, stat tags, table headers. Never sentences.

### Named Rules

**The No All-Caps Body Rule.** Uppercase is reserved for short labels (≤4 words), section eyebrows, and badges. Sentences in ALL CAPS are unreadable at body size and read as marketing-shouty. The brand doesn't shout.

**The Three-Family Cap.** Playfair + DM Sans + JetBrains Mono. Adding a fourth family to "richen" the system reads as indecision, not range.

**The Hero Pattern Rule.** The hero's three lines are committed verbatim from `BRAND_SYSTEM.md §1`:
```
Eyebrow (Label):   A capability institution for India's next generation of acquirers.
H1 (Display):      Boardroom judgment. Integration leadership. Enterprise-wide M&A capability.
Sub (Body, 18px):  Acquire with conviction. Integrate with discipline. Scale into an institution.
```
No paraphrasing.

## 4. Elevation

The system is mostly flat. Elevation is conveyed through **tonal layering** (Council Navy → Navy Light → Navy Mid) rather than ambient shadows. Cards on dark surfaces lift through brightening, not blurring.

Where shadows do appear, they are restrained and either ambient (a soft gold halo) or structural (a card lift on hover). No drop-shadows on flat sections.

### Shadow Vocabulary

- **Lift Shadow** (`box-shadow: 0 12px 32px rgba(10,22,40,0.10)`): Card hover-lift on cream sections. The card raises 4px and gains this soft navy-tinted shadow. Used only on hover/focus, never at rest.
- **Gold Halo** (`box-shadow: 0 0 24px 4px rgba(201,168,76,0.12)`): Ambient glow under gold pill labels and around the L1 lion image at hover. The halo signals interactivity through warmth, not brightness.
- **Pulse Ring** (`box-shadow: 0 0 0 6px rgba(201,168,76,0.28), 0 0 0 12px rgba(201,168,76,0.12)`): Reserved for the "Limited Founding Cohort" CTA. The single moment the system permits a heartbeat.

### Named Rules

**The Flat-By-Default Rule.** Surfaces are flat at rest. Shadow appears only as a response to state (hover, focus, active). A flat homepage with one shadow on the CTA reads as more confident than a homepage with shadows on every card.

**The No-Glassmorphism Rule.** No backdrop-filter blur, no translucent panels, no frosted glass. The aesthetic is solid stone, not blown glass.

## 5. Components

### Buttons
- **Shape:** Soft-corner rectangles (radius 8px / `{rounded.md}`). Never pills, never sharp-edged squares.
- **Primary:** Lion Gold (#c9a84c) background, Council Navy (#0a1628) text. Padding 14px 28px. JetBrains Mono is **not** used here — DM Sans 14px, weight 600, letter-spacing 0.04em. The button reads as type, not as ornament.
- **Hover / Focus:** Background → Lion Gold Light (#ddc06a). Translate Y by -1px over 0.35s using `cubic-bezier(0.25, 0.46, 0.45, 0.94)`. Focus-visible adds a 2px gold outline at 3px offset.
- **Ghost:** Transparent background, gold text, 1px gold border at 30% opacity. Used for "secondary" CTAs that aren't the primary "Request Access."

### Pills (Audience tags / Eyebrows)
- **Style:** Background `gold-dim` (rgba(201,168,76,0.15)), text Lion Gold, border 1px Lion Gold at 30% opacity. JetBrains Mono 11px / 0.18em letter-spacing / uppercase. Padding 4px 12px. Radius 20px.
- **State:** No interactive state. Pills are labels, not buttons.

### Cards / Containers
- **Corner Style:** 16px (`{rounded.lg}`).
- **Background on light sections:** Pure White (#ffffff) — for maximum readability of body text.
- **Background on dark sections:** Council Navy Light (#0f1f3a). Layered by tone, never by shadow.
- **Shadow Strategy:** No shadow at rest. Hover-lift uses Lift Shadow only on cream-section cards; dark-section cards brighten their border to Navy Mid instead.
- **Border:** 1px Council Navy Mid on dark surfaces; 1px Cream Dark on light surfaces.
- **Internal Padding:** 32px desktop, 24px tablet, 20px mobile.

### Day-cards (signature component)
- **Structure:** A small card per cohort day (Day 1 - Day 5). Eyebrow chip in JetBrains Mono ("DAY 1"), title in Playfair 22px, body in DM Sans 14px.
- **Top accent:** A 3px Lion Gold border on the **top edge** of each day-card. Signals continuity along the cohort's arc without flooding the surface with gold.
- **State:** On hover, the gold top-edge brightens to Gold Light and the card lifts 4px.

### Inputs / Fields
- *(Not currently used in v5; deferred to Track C dashboard.)*

### Navigation
- **Style:** Full-width transparent on hero, switches to navy 96% + 1px gold-dim bottom border on scroll.
- **Typography:** DM Sans 13px, weight 500, letter-spacing 0.02em. Active section underlined by a 2px gold mark via IntersectionObserver.
- **Mobile:** Hamburger triggers a full-screen navy overlay with gold-bordered links. Smooth 0.3s slide.

### Lion (signature visual, not a component)
- The Asiatic Lion is the recurring imagery (`assets/lions/`). Every lion appears at rest, watching, never roaring. Composition lives inside dark navy panels with subtle gold borders — see `BRAND_SYSTEM.md §7-8` for the full image asset spec.

## 6. Do's and Don'ts

### Do:
- **Do** use Lion Gold sparingly — ≤10% of any screen. Rarity is the point.
- **Do** layer dark surfaces tonally (Navy → Navy Light → Navy Mid). Tonal depth beats shadows on dark.
- **Do** keep Playfair on display + headline + title; DM Sans on body; JetBrains Mono on labels only.
- **Do** quote `BRAND_SYSTEM.md §5` lines verbatim on customer-facing surfaces. The brand has six committed lines plus one manifesto line; no paraphrasing.
- **Do** honour `prefers-reduced-motion` on every animation. Reveal effects must enhance an already-visible default.
- **Do** end a section in negative space, not a divider. The pause is the rhythm.
- **Do** pair the lion's "at rest, watching" image with calm copy. Image and tone should match.
- **Do** keep body text at #1a1a2e on cream / rgba(255,255,255,0.78) on navy. Never the muted-gray default.

### Don't:
- **Don't** introduce a fourth color. Navy + gold + cream is the system. No "subtle blue for trust." No "warm orange for energy."
- **Don't** use pure black (#000) or untinted greys. Council Navy is the deepest value.
- **Don't** ship a SaaS-clone aesthetic — Inter font, Bento grids, dashboard glow on hero, tinted-neutral pastels. (`PRODUCT.md` anti-reference #1.)
- **Don't** ship a Big-4 brochure — mega-nav, stock handshakes, button-as-pill, Georgia headlines. (`PRODUCT.md` anti-reference #2.)
- **Don't** use glassmorphism, gradient meshes, neon accents, or translucent panels. (`PRODUCT.md` anti-reference #3.)
- **Don't** use the lion mid-roar, mid-charge, or with bared teeth. Stillness over the roar. (`PRODUCT.md` anti-reference #4 + `BRAND_SYSTEM.md §7`.)
- **Don't** repeat the aphoristic-cadence body voice ("It is not X. It is Y.") more than twice on a page. (`PRODUCT.md` anti-reference #5.)
- **Don't** introduce bounce/elastic easing. The system uses one ease-out: `cubic-bezier(0.25, 0.46, 0.45, 0.94)`.
- **Don't** nest cards inside cards. A nested card is always wrong.
- **Don't** stretch body line length past 75ch. Long lines on cream make the page read clinical.
- **Don't** add a fourth font to "richen" the system. Three families is the cap.
- **Don't** put gold on gold. Gold lives against navy or cream — never against itself.
- **Don't** decorate negative space. The whitespace is intentional. Gold pinpricks in empty space read as anxiety.
