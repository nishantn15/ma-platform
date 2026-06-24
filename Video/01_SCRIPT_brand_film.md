# Video 01 — "The Company You Leave Behind"

**Founder-facing brand film.** TK's #1 priority. Emotive, not informational.
~75 seconds, 1920×1080, silent-render first (VO/music layered after lock).

## Direction (from TK, May 20 + May 23 + Jun 4)
- **Emotion first.** "Capture leaders' emotions on successfully closing a deal,
  successful integration to closure. Show the triumph as a hook."
- **Metaphor, not people.** Use the Asiatic lion (at rest, watching — never
  roaring) to *emote* the founder/board-member through the arc. No stock humans.
- **Composed, not frantic.** Boardroom-grade. Governance over conquest.
- **Sync with the site** — reuse the exact lions, Council Navy + Lion Gold,
  Playfair / DM Sans / JetBrains Mono, and the approved message-stack lines.
- **Brand voice is locked** — every on-screen line below is approved-as-written
  in BRAND_SYSTEM §5. No paraphrasing.

## Emotional arc (the founder's journey)
Pride built → the lonely question → conviction → disciplined integration →
institution → legacy. The triumph is not the deal closing; it's the company
that outlives the founder.

## Palette / type (from DESIGN.md)
- Council Navy `#0a1628` · Lion Gold `#c9a84c` · Cream `#f8f6f0`
- Playfair Display (serif, emotive headlines) · DM Sans (sub) · JetBrains Mono (eyebrows)
- Lion assets: `lion_hero` (seated, constellation), `lion_council` (pride elders),
  `lion_cub` (on plinths). Apply the same radial edge-fade as the site.

## Shot list (8 scenes · ~75s · 30fps)

| # | Dur | Visual (lion-metaphor) | On-screen text (approved lines) | Emotional intent |
|---|-----|------------------------|---------------------------------|------------------|
| 1 | 0–9s | Black → Council Navy fades up. `lion_hero` resolves slowly from dark, constellation lattice igniting behind. Hold, breathing. | *(eyebrow, mono gold)* A CAPABILITY INSTITUTION FOR INDIA'S NEXT GENERATION OF ACQUIRERS | Stillness. Gravity. Arrival. |
| 2 | 9–20s | Slow push-in on the lion's gaze. | *(serif, white)* You built a company. | Pride, recognition. The founder sees their life's work. |
| 3 | 20–30s | The lion turns to watch (cut to `lion_council` — the pride, elders seated). Cream wash. | *(serif)* The numbers are settled. The deal can be approved. | The lonely boardroom question. |
| 4 | 30–42s | Hold on the council. Gold hairline draws across. | *(serif, building)* But value is not created in the boardroom. **It is created through integration leadership.** | The turn — conviction over euphoria. |
| 5 | 42–52s | `lion_cub` on stacked plinths — the next generation, capability compounding. Navy. | *(mono eyebrow)* ACQUIRE WITH CONVICTION. INTEGRATE WITH DISCIPLINE. SCALE INTO AN INSTITUTION. | Discipline. The 4-5 year nurtured window, not a 100-day sprint. |
| 6 | 52–60s | Pull back: all three lions implied in one composed frame (hero returns, centered). | *(serif, the manifesto line)* India's next acquirers will not be louder. | Quiet defiance. The brand's thesis. |
| 7 | 60–68s | Hold. The lion, at rest, watching. Gold intensifies subtly. | *(serif, completes)* They will be more composed. | Resolution. Earned calm. |
| 8 | 68–75s | Settle to the master stanza on navy, lion small + centered beneath. Gold underline. | *(serif italic)* You built a company. **Now build an institution.** — *(mono, beneath)* M&A LEADERSHIP PLATFORM | Legacy. The company you leave behind. |

## Closer / CTA frame (static last 0.5s hold)
Master brand line, mono gold, centered:
**Boardroom judgment. Integration leadership. Enterprise-wide M&A capability.**

## Audio (layered after visual lock — Phase 2)
- VO: measured, low, unhurried (a single male/female voice, boardroom register).
  Script = the on-screen lines, read slower than they appear.
- Music: sparse, a single sustained cello/drone + one resolving piano motif at
  scene 8. Nothing triumphant-loud — composed, per brand.
- Render silent first; add `data-track-index` audio tracks once visuals lock.

## Build plan
- Composition dir: `Video/brand-film/` → `index.html` (8 scene clips, GSAP timeline).
- Reuse lion JPGs from `assets/lions/` (copy into `brand-film/assets/`).
- Draft-render at 24fps to iterate; final at 30fps `--quality high`.
- Render via `Video/render.sh brand-film`.

## Open creative choices for Nishant / TK
1. VO or text-only (silent + music)? (affects scene timing)
2. Length: 75s (this) vs a tighter 45s cut for social?
3. End on the founder line or the master brand line?

---

## Render status
- **Draft v1 rendered** 2026-06-15: `Video/renders/brand-film-draft.mp4`
  — 1920×1080, 24fps, 75.0s, 7.9 MB, H.264. ~12.5 min render (screenshot mode).
- All 8 scenes verified in the final MP4 (frame extract + contact sheet).
- Known polish items for v2:
  - Scenes 6/7: manifesto text overlaps the centred lion slightly — add scrim
    or offset text to lower third (as done for scenes 3/8).
  - Scene 8 small lion shows faint rectangular edge at 300px — tighten mask.
  - Add music bed (sparse cello/piano), then VO if approved.
  - Final render: 30fps, --quality high.

---

## v2 render status (2026-06-16)
- **Draft v2 rendered**: `Video/renders/brand-film-v2-draft.mp4` — 1920×1080, 24fps,
  62.0s, 8.6 MB, H.264. Faster cut, full-bleed lions, platform-in-action typing scene,
  big wordmark closer.
- All 9 sampled beats verified in the final MP4, incl. the Readiness-Gates panel
  typing/checking in sequence (frames 35s empty → 38s filled).
- Still pending (v3 / final): music bed (sparse cello/piano), optional VO,
  final 30fps --quality high render. WhatsApp sent to TK 2026-06-16 promising an
  early draft "in a day".

---

## v3 render status (2026-06-22)
Rebuilt to 9 scenes (~72s) on a consistent navy chamber. Changes vs v2:
- **No blinding white**: the old full-screen cream "turn" scene (s4) redesigned on
  navy with an "Integration" ghost-word.
- **4-5 year discipline beat** (TK pt 1, his most emphatic note): new scene on a
  bespoke cadence lion (concentric floor rings = the multi-year horizon), line
  "Integration is not a hundred-day sprint. It is a 4-5 year discipline, nurtured
  each year."
- **Capability-compounds beat** (TK pt 8): pride-pyramid lion, "Capability is
  earned, not announced. Several disciplined acquisitions earn the right to one
  bold one."
- **Closer fixed** to the locked master line: "Boardroom judgment · Integration
  leadership · Enterprise-wide M&A capability."
- **Manifesto** moved onto the profile lion's negative space (fixes v2 text/lion
  overlap).
- **Gold readability** (TK pt 4): bright gold only on navy; the cream cockpit card
  uses the deeper gold-ink.
- Built with the installed **HyperFrames skill** (lint 0 errors; layout inspect
  0 issues). New cadence lion generated via Codex imagegen, then **regenerated with
  the original lions attached as visual reference** after a first attempt drifted
  too bright/yellow — final asset matches the antique bronze-gold sculpt family.

## v4 render status (2026-06-24) — CURRENT
Three targeted changes on top of v3 (TK review):
- **Hero no longer double-pops**: old scenes 1+2 merged into ONE continuous 15s
  hero shot (#s1, 0-15s). The hero lion fades in once and holds; the eyebrow yields
  to "You built a company." over the same shot — no fade-out/re-pop.
- **Richer interactive showcase** (replaces the simplistic 4-row Readiness card):
  scene 5 is now the **Anchor × Polaris Integration Cockpit** — the real 7-gate
  spine (Pre-LOI · Diligence · Signing · Day 1 Readiness [active] · Day 100 · Value
  Capture · Capability Build) with gold progress bars and statuses (3 passed /
  1 active / 3 pending), an active-gate detail panel (Owner / Evidence / Decision)
  and live metrics (Workstreams green 9/11 meter, Founder retention Locked).
  Consistent with the current integration-room.html.
- **Hyphens, not em/en dashes**, throughout the script and on-screen copy.
- Draft: `Video/renders/brand-film-v4-draft.mp4` (24fps). Final:
  `Video/renders/brand-film-v4.mp4` (30fps, --quality high).
- Still pending: audio (sparse cello/piano music bed + optional VO) — film is silent
  for now, to be layered after visual lock. Lion-age-by-stage (TK pt: older lion in
  boardroom, adults in integration, cubs for legacy) is partially expressed (cub on
  plinths, pride pyramid) but not yet a full age-graded pass.
