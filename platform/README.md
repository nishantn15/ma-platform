# Platform MVP - the five-year capability workspace

Clickable static prototype of TK's platform vision (07-03), restructured to
Programme Blueprint v3.0. Lives in the same repo so GitHub Pages links work:
`nishantn15.github.io/ma-platform/platform/`.

## What it is
Each member company's **five-year capability-building workspace** - the classroom is
the front door; this is the building. Every screen is real (not a placeholder tile),
driven by one canonical data spine, threaded by one causal case.

## Vocabulary (read this before renaming anything)
Customer-facing names come from TK's customers deck (09 Aug 2026 v2) and are
**canonical**. They live in `data/spine.json` under `vocabulary`, and nowhere else -
`shell.js` holds nav layout only, and pages read labels back out of `Shell.MODULES`.
M1-M5 survive as the internal index (they appear as a nav sigil), never as the name
of a thing in front of a client.

| Index | Canonical name | Role |
|---|---|---|
| EGC | Enterprise Growth Charter | diagnostic + account spine document |
| M1 | Leadership Learning | capability journey |
| M2 | Ideas Development Funnel | intake engine |
| M3 | Patent-to-Enterprise Exchange | intake engine |
| ◈  | Strategic Growth Pathway Matrix | the decision |
| M4 | Target Sourcing & Strategic Fit | execution route |
| M5 | Deals Integration Room | execution route |

Two naming systems coexist deliberately for the five pathways. The deck names them by
**source** (Ideas, Patents, Partners, Invest, Acquire); the blueprint names the same five
by **transaction form** (Build, License, Partner, Invest, Acquire). Every route in the
spine carries both (`deckName` and `form`), so neither document has to change.

## The information architecture (this is the part that changed)
The funnel and the Exchange are **not peer modules alongside the matrix**. They are the
two front doors into it, per Blueprint v3.0. An idea leaves the funnel by being *routed*,
not approved; a patent leaves the Exchange qualified, not licensed. Both arrive at the
Pathway Matrix and are scored against the same five routes on the same seven dimensions.
Only then does an execution route open.

```
EGC charter opens (diagnostic)
      |
M1 names the gap
      |
   +--+--+ ------ M2 Ideas Development Funnel ---+
   |                                             +--> ◈ Pathway Matrix --> M4 Acquire route
   +--------- M3 Patent-to-Enterprise Exchange --+         |                    |
                                                           |                    v
                                        Build / License / Partner / Invest   M5 Deals
                                                                          Integration Room
```

## Pages
- `index.html` - Account Home: 5-year arc + live rollups, read left to right as a pipeline
- `charter.html` - **EGC Enterprise Growth Charter**: the diagnostic capture sheet. The four
  slide-4 questions in verbatim wording, plus the fifth route-lean prompt section 4 actually
  needs; captures the raw material for sections 1-4 live, shows 5-8 open, and prints as the
  room sheet (two pages by design: the ask, then what is handed back)
- `learning.html` - M1 Leadership Learning (3 layers + personas, experiential loop)
- `ideas.html` - M2 intake engine (kanban whose third column is the exit into the matrix)
- `exchange.html` - M3 intake engine (gallery + what it qualified, and what decided it)
- `pathway.html` - **◈ Strategic Growth Pathway Matrix**: the join, the 7x5 scoring grid,
  the portfolio verdict, route-by-route reasoning, the intake queue, and the honest gaps
- `targets.html` - M4 execution route, opens only because the matrix returned *acquire*
  (capability-gap filter -> longlist -> **Target Attractiveness Score**, 4 dims)
- `integration.html` - M5 execution route (7-gate spine + 4-5yr value arc)

## Architecture
- `data/spine.json` - **single source of truth** (v1.1). Every page reads from it. Edit here.
- `data/targets.json` - M4 comparables (AlphaSense-sourced)
- `assets/theme.css` - shared navy/gold brand theme (DESIGN.md tokens)
- `assets/shell.js` - nav layout, vocabulary resolution, the causal-thread crumb, `mount()`

The crumb is generated once in `shell.js` and injected by `mount()`, so the pipeline order
cannot drift page to page. Do not hand-write a `.crumb` div in a page.

## The causal thread (state continuity, not seven colored pages)
M1 surfaces Anchor's capability gap. It seeds an idea (M2) and a patent match (M3). Both
exit into the Pathway Matrix, which scores all five routes and returns a **portfolio**
answer, not one winner: *acquire now, build in parallel, license in Year 2*. Acquire opens
M4, where TAS scores real targets and Polaris wins; Polaris flows into the 7-gate deal (M5);
outcomes and matured ideas report onto the five-year account home.

## New this build
**◈ Strategic Growth Pathway Matrix** (`pathway.html`) - the screen named in both TK
documents and missing from the prototype. Seven weighted dimensions (capability depth .20,
speed .18, long-term value .16, control .14, risk .12, cost .10, integration burden .10;
the last three scored as *favourability*, so a high risk score means low risk). Weighted
totals: Acquire 76, Build 70, License 63, Partner 55, Invest 54. Weights are stated on the
screen as a per-account board decision, not a product constant.

The design surfaced a real gap, logged honestly in `pathwayMatrix.gaps` and printed on the
screen: **Partner and Invest are scoreable routes with no module behind them.** If a company
picks either, the platform currently hands them nothing. Cheapest fix is an alliance/stake
tracker sharing the M5 gate spine.

**EGC Enterprise Growth Charter** (`charter.html`) - the diagnostic capture sheet, structured
from Blueprint Part D section 18 (8 sections) and the customers deck slide 4 (4 questions).
The CEO leaves the room holding a named document, not an impression.

What the sheet promises is deliberately narrower than the first cut of it claimed. It does
**not** say the client walks out of a 15-minute opening with Charter sections 1 to 4 drafted.
The Blueprint makes sections 1-4 an output of the 2.5-day M1, and slide 12's own stated
diagnostic output is "a clear view on gaps, fit, priority capability development agenda and
growth pathways". Promising the drafted sections in the free 15 minutes would both over-promise
and cannibalise the paid M1 deliverable. So the sheet is positioned as the *input* to M1:
answers captured in the CEO's own words, which M1 then drafts and signs off. The reasoning is
recorded in `charter.diagnostic.promiseNote` so it cannot be quietly reverted.

One further honesty note, in `charter.diagnostic.questions[q4].sectionNote`: read literally,
"is your top management team equipped to build, buy, acquire and integrate them?" is a
capability-readiness question about the team, which is section 3 material. It is mapped to
section 2 (Leadership Commitment) because commitment is unanswerable without that read, so
the sheet now captures it twice - readiness into section 3, the commitment that follows into
section 2 - and asks an explicit follow-up ("what are you personally committing to, and what
has the board already approved in writing?") rather than inferring commitment from silence.

Building it surfaced a second real finding, recorded in `charter.diagnostic.routeLean._note`:
**the four deck questions produce Charter sections 1, 2 and 3, and nothing on slide 4 produces
section 4.** So the sheet closes with a fifth prompt ("if you had to lean today, which route
closes this gap - and what would change your mind?") plus a 1-10 route-confidence baseline that
the M1 exit poll can be compared against. Its five options are asserted equal to the matrix's
five route forms, so the diagnostic and the matrix cannot drift apart.

Stated narrowly, because the broad version is wrong: the only deck change this sheet asks for
is **a fifth opening prompt on slide 4, and only if the diagnostic is expected to seed section
4.** The route question is not missing from the deck - slide 12 already brainstorms growth
pathways later in the same workshop. It is missing from the first fifteen minutes, which is
the one place an unrehearsed lean can be recorded before the programme has framed the answer.

Sections 5-8 render as visibly open, with the module that closes each. That is the pull-through
into M2 and M3 the blueprint asks for, made literal on screen rather than asserted in a note.
The page also carries the eight M1-to-M2 handoff questions (Blueprint section 19), with the four
this sheet already seeds marked as such.

Print behaviour: `charter.html` **is** the room sheet, and it prints on two pages on purpose -
`.pagebreak` splits the four questions you put on the table from the captured draft you hand
back. "Print the capture sheet" renders the captured version; "Blank sheet for a new client"
prints the same instrument with the write-in lines empty, for use in the room. Edits persist in
`localStorage` only (keyed `egc:<accountId>`), which is honest for a static prototype - "Restore
Anchor Tech Services" drops back to the spine. Two smaller fixes worth knowing: everything typed
into the sheet is HTML-escaped before it is rendered back (a CEO who says "margins < 8% & falling"
sees that sentence, not a broken layout), and if the browser blocks the clipboard - which it does
on `http://` origins and inside some in-app browsers - "Copy sections 1-4" now drops the text into
a selected read-only box instead of saying "copy manually" with nothing to copy.

## Verification
`node ~/hydrate_check.mjs` runs every page against a minimal DOM shim and reports whether it
hydrates. Use it after spine edits - it catches renamed or removed spine paths that a browser
would only reveal by rendering an empty section.

## Status
MVP = static, no backend, sample-but-real data (Anchor x Polaris; AlphaSense-style targets;
anonymised institute patents). Phase 2 = auth/multi-tenant/persistence, live AlphaSense target
discovery, full patent EOI workflow, editable matrix weights, 5-year entitlement model. See
`../Platform_Architecture/PLATFORM_PLAN_v2.md`.

## Earlier build: Target Attractiveness Score (TAS)
Closes the long-known gap (ARS scores acquirers, not targets). 4 orthogonal dimensions:
Transactability (30%), Strategic fit (35%), Integration risk inverse (25%), Data confidence (10%).
Scarcity is a tie-breaker, not a scored factor. Each target flags what is AlphaSense-supplied
vs manually enriched.
