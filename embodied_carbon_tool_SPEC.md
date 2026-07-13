# Athanor Embodied Carbon tool — design spec (v1)

**Date:** 13 July 2026 · **Status:** for your review before build
**Anchor data:** NABERS Embodied Carbon calculator v2026.1 (Materials database sheet)

## 1. Purpose
A fifth tile in the Athanor teaching toolkit: a **rough, fast, whole-building upfront-embodied-carbon** tool. A student picks a building archetype, sizes it, swaps a few key material choices, and instantly sees the carbon, waste and material-mass consequences. It exists to make the *impact of a structural/material choice* legible in seconds — the studio-speed companion to the real NABERS spreadsheet, not a replacement for it.

**Audience:** ARCH 5004/6004 students, at sketch-design stage.

## 2. Placement & tech
- **New file:** `dossier/project web/Athanor_Embodied_Carbon.html` (lives beside the other four tiles so relative cross-links work).
- Add it to the nav of all four existing pages, and give it a nav linking back to them.
- **House style, exactly:** system font, `:root` tokens, black hero, rounded cards, `.seg` / `.stat` / `.checks` / `.why` / `.tip`, the auto-glossary block, nav with `overflow-x:auto`.
- **Charts:** Chart.js **4.4.1** from cdnjs (the version confirmed working; the toolkit's Footprint page uses the same). Includes the `prefers-reduced-motion` guard.

## 3. Scope (locked from our conversation)
**In:** upfront embodied carbon **A1–A3**, construction-waste carbon **A5**, and **material mass (tonnes)**.
**Out:** $ cost; operational energy; transport (A4) and end-of-life (B–C) stages beyond the A5 waste line. Deliberately kept to "upfront" so it stays a one-screen studio tool.

## 4. Data — baked-in NABERS 2026.1 subset (~24 materials)
All A1–A3 emission factors, densities and waste rates below are **read directly from the NABERS 2026.1 Materials database** and hard-coded into the HTML (fully self-contained except the Chart.js CDN). Each is cited on-hover as "NABERS 2026.1". Representative values:

| Material (declared unit) | A1–A3 kg CO₂e/unit | density / area-density | waste % |
|---|---|---|---|
| Concrete in-situ 32 MPa (m³) | 305 | 2400 kg/m³ | 0 |
| Concrete in-situ 40 MPa (m³) | 354 | 2400 | 0 |
| Precast concrete panel (t) | 233 | — | 0 |
| Hollowcore plank (m³) | 339 | 1480 | 0 |
| Reinforcing steel (t) | 1600 | — | 10% |
| Structural steel — sections (t) | 2270 | — | 0 |
| Structural steel — framing (t) | 3010 | — | 0 |
| GLT + CLT, softwood (m³) | 242 | 518 | 10% |
| LVL (m³) | 298 | 507 | 10% |
| Softwood timber (m³) | 188 | 514 | 10% |
| Clay brick (t) | 184 | — | 10% |
| Aluminium curtain wall — unitised (m²) | 264–680 | 35–68 kg/m² | 0 |
| Aluminium window (m²) | 159 | 23 kg/m² | 0 |
| Timber window (m²) | 61 | 37 kg/m² | 0 |
| Timber cladding/weatherboard (m³) | 195 | 512 | 10% |
| Fibre cement sheet (m²) | 12.6 | 14.2 kg/m² | 10% |
| Plasterboard (m²) | 3.4 | 11.1 kg/m² | 10% |
| Glass, treated (kg) | 1.7 | — | 0 |
| Steel sheet roof/cladding (m²) | 19.1 | 6.0 kg/m² | 0 |
| Clay roof tile (t) | 310 | — | 10% |
| Carpet (m²) | 13.3 | 3.2 kg/m² | 10% |
| Timber flooring (m³) | 347 | 744 | 10% |
| MEP — office (m²) | 55.3 | — | 0 |

(Exact final list confirmed at build; all pulled from the same sheet.)

## 5. Interaction
**a) Archetype** — a `.seg` control, one of four. Selecting one loads default element→material→quantity assumptions:
1. **Concrete frame** — RC frame + RC flat slab + precast/curtain-wall façade (the heavy baseline).
2. **Steel frame / shed** — structural-steel frame + composite floor + metal cladding (long-span).
3. **Mass timber** — GLT/CLT frame + CLT floors + timber cladding (low-carbon civic).
4. **Hybrid — "this project"** — concrete data-hall podium + timber civic wings + steel/glass greenhouse (Athanor's real mix).

**b) GFA slider** — scales all quantities. Element quantities are computed as **per-m² material intensities × GFA**; the intensity figures (e.g. RC frame ≈ 0.14 m³ concrete + 90 kg rebar per m²; CLT floor ≈ 0.16 m³/m²) are **rules of thumb**, labelled as such and sourced from typical published intensities — the *EFs* are NABERS-exact, the *quantities* are the rough part.

**c) Choice levers** — three `.seg`/`select` overrides that swap one element's material and recompute live:
- **Structural frame:** Reinforced concrete · Structural steel · Mass timber (GLT+CLT)
- **Floor system:** RC flat slab · Composite steel–concrete · CLT panel · Precast hollowcore
- **Façade:** Precast concrete · Brick veneer · Aluminium curtain wall · Timber cladding + windows

## 6. Calculation (rough, transparent)
- **A1–A3** = Σ over elements: quantity × material EF. Reported total (t CO₂e) and **kg CO₂e/m² GFA**.
- **Mass** = Σ quantity × density (t), and t/m².
- **A5 (waste)** ≈ Σ (element A1–A3 × material waste-rate %) — i.e. the embodied carbon of the over-ordered/wasted fraction. A simplification of NABERS' fuller A5 (which adds waste transport + EoL); stated plainly as an approximation. Also report waste tonnage and the recycle/landfill split from the NABERS waste class.

## 7. Outputs
- **Stat cards:** total A1–A3 (t CO₂e) · **kg CO₂e/m²** with benchmark band · A5 waste (t CO₂e) · total mass (t) · t/m².
- **Chart 1 — stacked bar: A1–A3 by element** (substructure / frame / floors / façade / roof / internal + services) — shows what dominates.
- **Chart 2 — comparison bar: your build vs the other three archetypes** — the "choices matter" moment.
- **Chart 3 — doughnut:** material-mass share (or waste recycle/landfill split — pick one at build).
- **`.checks` traffic-lights:** benchmark band read (e.g. LETI/NABERS kg CO₂e/m² context), a "mass timber cut frame carbon ~N%" style delta when a lever changes, and the standard **"RULE OF THUMB — a real LCA tool (eTool/One Click) + a QS replace this"** disclaimer.

## 8. Content integrity / disclaimers
- Every EF cited to NABERS 2026.1; every material-intensity figure flagged as a named rule of thumb.
- Benchmark bands cited (LETI / NABERS / RIBA 2030). No number presented as compliance.
- Mirrors the toolkit's existing "two kinds of number" ethos (verified clause vs named convention).

## 9. Glossary
Reuse the ACRO_GLOSSARY block; add embodied-carbon terms (A1–A3, A5, GWP, EPD, LCA, CLT, GLT, LVL, EoL, NABERS, GFA — several already defined).

## 10. Out of scope for v1 (YAGNI)
Custom material entry, transport/EoL detail, $ cost, operational energy, saving/exporting. Can follow later if the tool proves useful.
