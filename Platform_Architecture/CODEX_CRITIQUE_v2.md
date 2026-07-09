# Codex build-support critique of PLATFORM_PLAN_v2 (2026-07-08)

Verdict: **ADJUST-FIRST** (three concrete pre-build adjustments; scope confirmed - full 5 modules).

Findings:
1. **Depth-bar necessary but not sufficient.** Module 3 (Patent Exchange) is the module most likely to feel thin - a catalogue risks being a browsable library, not a decision system. FIX before building: give M3 one explicit job in the thread - one patent directly addresses Anchor's capability gap, competes against the seeded idea AND the acquisition target, and produces a clear collaborate/license/build decision (with why it did/didn't beat Polaris).
2. **TAS factors overlap.** Valuation headroom + distress + promoter-exit all proxy transactability/price. Scarcity overlaps fragmentation. Missing: strategic value-realization risk (can Anchor extract the capability without breaking the target?) and regulatory/execution friction (the Integration Room already has an India reg lane). AlphaSense populatability is a HYPOTHESIS for private mid-market firms - promoter succession/distress/scarcity/integration burden likely need manual enrichment. Add a per-target data-confidence flag.
3. **Causal thread is right, but brittle.** If M1 doesn't produce a concrete gap, everything downstream feels retrofitted; if TAS doesn't explain why Polaris wins, M5 is a generic room with a pasted-in target. Stated build order (M5 before M4/M1/M2/M3) CREATES REWORK - M5 gets renamed/restructured once Polaris/TAS/timeline are known.
4. **Highest risk = state continuity.** In a static no-backend demo, it lives/dies on whether each module visibly CONSUMES prior outputs (shared IDs, dates, scores, labels, narrative consequences), not just links to another colored page. If those drift, it's "six static pages with matching colors."
5. **Best sequencing change:** start with the Anchor x Polaris DATA SPINE, not the shell or Room.

ADJUST-FIRST actions (folded into build):
- A. Write the **Anchor x Polaris canonical data spine** as ONE document/JSON before any page: Anchor profile, capability gap, L1/L2/L3 learning implication, one seeded idea, one patent alternative, target longlist, TAS scoring, selected Polaris deal, integration gates, 5-year outcome timeline. Every page reads from this spine only.
- B. First vertical slice = **account home + Target Sourcing (M4) + Deal Integration (M5)** (proves the hardest causal link first; makes M5 rework intentional). M1/M2/M3 follow once their spine role is fixed.
- C. Tighten **TAS from 7 overlapping factors -> 4 orthogonal dimensions**: (1) Transactability (valuation headroom + promoter signal + distress), (2) Strategic fit (capability match + fragmentation fit), (3) Integration risk (inverse integration burden + regulatory friction), (4) Data confidence (per-target flag: AlphaSense-supplied vs manual enrichment). Scarcity = tie-breaker, not standalone.
