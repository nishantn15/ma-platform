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
