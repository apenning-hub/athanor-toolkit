# Athanor teaching toolkit — usability, functionality & design review

**Date:** 13 July 2026 · **Scope:** the four interactive tools in `dossier/project web/`
**Aesthetic:** preserved exactly (system font, `:root` tokens, black hero headers, rounded cards, gradient SVG charts). No fonts, libraries or frameworks added. Every page remains a single self-contained file that works offline from Box — *except* the Footprint page's one Chart.js CDN dependency (see F-1).

## Method
- Extracted every `<script>` block and ran `node --check` — **all pass**.
- Loaded each page in **jsdom** (`runScripts:'dangerously'`, `pretendToBeVisual`) — **zero window/runtime errors** on all four at load (Footprint's only error is the expected canvas/Chart-CDN absence under jsdom).
- Opened every page in **Chrome** at ~1440 px and ~390 px, poked the controls, and drove the interactive tools (drag, toggles, wizard steps).
- Cross-checked NetZero + Footprint with an independent code audit (class-usage vs CSS, links, anchors, glossary).

Content is layout/CSS only — **no numbers, formulas, wording, sources, or the "RULE OF THUMB" / "VERIFY the clause" disclaimers were changed.** Two genuine functional bugs were found and fixed (F-1, F-2); both are flagged as such.

---

## Athanor_Design_Calculators.html

**C-1 [High] — A whole cluster of controls had no CSS (a dropped `<style>` block).**
`.seg`, `.seg button`, `.seg button.on`, `.why`/`summary`/`.body`, `.cybtn`, `.cypill`, `#cy_card tr.head` were used in markup/JS but defined **nowhere**. So the overlay toggle, air-system selector, ceiling-finish toggle, the ← → cycler arrows, the 1–9 component pills and the "Fine-tune" disclosure all rendered as raw grey browser buttons — badly off-brand and with no visible active state.
**Fix:** restored the canonical `.seg` and `.why` rules (ported verbatim from `Athanor_DataCentre_NetZero.html`, where they still existed, so the two pages match), and added matching `.cybtn` / `.cypill` styles + `:focus-visible` states in the same Apple idiom.

**C-2 [High] — Ceiling-services module cramped (the known offender), now redesigned.**
The two diagrams were jammed side-by-side in a `1.15fr 1fr` grid; the depth-section bands were capped at 52–120 px with 16 px chips and 8.5 px labels, and **BAND 3's title collided with its five component chips** (they wrapped up over the heading).
**Fix, three parts:**
1. Stacked the two diagrams **full-width** (single-column grid; the spacing plan centred, max 620 px).
2. Rewrote `cyDepth()` — bands are now sized to their chip rows (**≥74 px**, proportional to mm), chips are **26 px tall with 11 px labels laid out in rows *below* each band title** (collision gone), and headers/mm dimensions are ≥10.5 px.
3. Rewrote `cyPlan()` at a larger scale (sc 44→58, pad 26→32) so **every label is ≥10 px** (was 7.5–9 px).
Verified: cycler pills, ← →, band-chip click-to-jump, the air-selector appearing only on component 3, and the `#svc_gotoair` jump-link all still work; the glossary re-annotates and never touches the SVG text.

**C-3 [Low] — Remaining sub-10 px labels left deliberately.** "SHARED" (8.5 px, accessible-bay overlay), "EXIT" (9 px) and the "2.8 m" bay-width tag (9 px) sit inside small graphical boxes where they are legible and enlarging would risk overflow. Not the "disease" the offender was — left as-is.

---

## Athanor_Project_Web.html

**P-1 [Med] — Nav wrapped chaotically at narrow widths.** Unlike the other three pages, this nav lacked `overflow-x:auto; white-space:nowrap`, so its many links wrapped into a ragged stack on mobile.
**Fix:** added `overflow-x:auto; white-space:nowrap` — the nav now scrolls horizontally, matching the toolkit.

**P-2 [Low / Accessibility] — Force simulation had no `prefers-reduced-motion` guard.** The force-directed diagram animated its settle on every load with no opt-out.
**Fix:** refactored the loop into `physics()` + `draw()`. When the user prefers reduced motion, the layout is **pre-settled instantly (600 steps, no animated intro)** and the rAF loop still runs only so dragging stays live (at equilibrium it is effectively static). Default behaviour is unchanged.
Verified working & untouched: node drag, hover highlighting, domain filter pills, people-card expand/collapse, the contract-type toggle redrawing the organigram **including the orange novation arrow**, and the responsibility matrix.

---

## Athanor_DataCentre_NetZero.html

**N-1 [Low] — Orphan `.note` class.** The aisle-plan caption (`<p class="note">`, line 221) used a class with **no CSS rule**, so it rendered as full-size body text instead of the small grey caption used elsewhere.
**Fix:** added a `.note` rule matching the calculators page (11.5 px, `--sec`, max 90ch).

**N-2 [Low] — One 9 px in-box label left deliberately.** The "{used} MWh used" label (line 573) sits inside a box whose height is data-driven; enlarging it risks crowding at low heat-utilisation. Left as-is.

All six wizard steps, Step 0's "Size Step 1 to this community" button, the cooling-strategy rewiring (PUE/recovery/WUE/kW-rack), solar + battery, the benchmark chart, the 30-year carbon-ledger verdict, the typology cards and the 20-card systems library were all verified working. Nav, `.grid`/`.cards` stacking and SVG scaling are already responsive. No continuous animation, so no reduced-motion guard is warranted.

---

## Data_Footprint_Calculator.html

**F-1 [High · FUNCTIONAL BUG] — Broken Chart.js CDN URL; all four charts silently dead.** The page loaded `…/Chart.js/4.4.4/chart.umd.min.js`, but **cdnjs never published 4.4.4** — that path returns **404** (confirmed; 4.4.0 and 4.4.1 return 200 on the same CDN). So `window.Chart` was `undefined` and every chart failed to render, on every visit, online or off.
**Fix:** changed the version to **4.4.1** on the same cloudflare CDN (`cdnjs.cloudflare.com`). Verified in-browser: Chart loads, all four charts render.

**F-2 [Med · FUNCTIONAL BUG] — Two-line axis labels rendered on one line.** `scenarioChart` used `'South Australia\n(0.22)'`-style strings; Chart.js v4 does not split on `\n`.
**Fix:** converted the labels to arrays (`['South Australia','(0.22)']`, …) — Chart.js renders each array element on its own line. Verified.

**F-3 [Med] — Nav clipped its wrapped links at ~390 px.** `.navrow` had a fixed `height:52px` while `.navlinks` used `flex-wrap:wrap`, so the second row was clipped.
**Fix:** `.navlinks` now scrolls horizontally (`flex-wrap:nowrap; overflow-x:auto; white-space:nowrap`) like the other pages; the brand is `white-space:nowrap` so it stays on one line.

**F-4 [Low] — Hero `h1` fixed at 48 px.** Made fluid: `clamp(32px,7vw,48px)`.

**F-5 [Low / Accessibility] — Chart.js animations had no reduced-motion guard.**
**Fix:** under `prefers-reduced-motion: reduce`, `Chart.defaults.animation = false`.

Sliders, presets, quality toggle and `recompute()` were verified updating outputs; the glossary is byte-for-byte identical to the other pages.

---

## Verified working across the suite (unchanged)
- **Auto-glossary** on all pages re-annotates after dynamic re-renders and **never wraps SVG text or `.tip` tooltips** (77 / 53 / 112 / 17 `<abbr>` respectively; 0 inside any `<svg>`).
- **State couplings:** `svcDepth()`+`svcCeil()` → grid-planner floor zone + `#stx_sel` summary; egress population → sanitary tool; cooling/sizing → aisle rack count; Step 0 watts → people-served stats.
- **All 8 cross-page links resolve** (relative hrefs, same folder).

## Deliberately left alone
- Every pedagogically load-bearing number, formula, source and disclaimer.
- The sub-10 px in-box labels noted in C-3 / N-2 (legible; enlarging risks overflow).

## Remaining recommendations (not actioned)
1. **Self-host Chart.js.** F-1 shows CDN drift is a real risk, and it's the only thing keeping the Footprint page from being fully offline like its siblings. Dropping `chart.umd.min.js` next to the HTML and pointing the `<script>` at it would make the whole toolkit self-contained. (Not done unilaterally — it changes the offline story and adds a binary to the Box folder; worth a yes/no.)
2. If any of the small in-box diagrams (parking accessible bay, ceiling detection tile) are ever reworked, bump the remaining 8.5–9.5 px labels to 10 px at the same time.
