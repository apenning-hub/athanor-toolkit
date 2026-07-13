# The Athanor Toolkit

Six interactive teaching tools for the **ARCH 5004 / ARCH 6004** Master of Architecture studio (University of Adelaide), built around the **Southwark Thermal Commons** — a net-zero data centre, bathhouse and greenhouse for Southwark Grounds, Thebarton, South Australia.

**▶ Live site:** https://apenning-hub.github.io/athanor-toolkit/

Each tool is a single self-contained HTML file that works offline (open it in any modern browser). The only external dependency is Chart.js, loaded from a CDN by the Data Footprint and Embodied Carbon pages.

## The tools

| Tool | What it does |
|------|--------------|
| **[Project Web](Athanor_Project_Web.html)** | Force-directed map of the five domains of obligation (contractual, compliance, planning, design, governance), the people around the architect, three contract-delivery models, and a responsibility matrix. |
| **[Design Calculators](Athanor_Design_Calculators.html)** | Live NCC / AS sizing: stairs, occupancy + egress with a draggable exit planner, sanitary facilities, parking, HVAC plant, pool plant, a structural grid planner, and a component-by-component ceiling-services stack — plus a "verify register". |
| **[Net-Zero Data Centre](Athanor_DataCentre_NetZero.html)** | A six-step wizard from digital footprint → sizing → hot/cold aisles → cooling + heat cascade → power (solar + battery) → water → embodied carbon → a 30-year carbon ledger, with a 20-card systems library. |
| **[Embodied Carbon](Athanor_Embodied_Carbon.html)** | Pick a structural archetype, size it, swap frame / floor / façade materials, and see upfront embodied carbon (A1–A3 + A5 waste) and material mass move live. Emission factors from the NABERS Embodied Carbon calculator 2026.1. |
| **[Data Footprint](Data_Footprint_Calculator.html)** | What would it take to run a suburb's own data storage and streaming locally? Population → racks, energy, water and carbon. |
| **[Glossary & Sources](Athanor_Glossary.html)** | Every code, standard, regulation, reference and acronym the tools cite — searchable and categorised, traceable to the NCC clause or Australian Standard. |

## Using the numbers

The toolkit runs on **two kinds of number**, and treats them differently:

- **Code-derived values** come from the NCC or an Australian Standard — cite the clause and **verify the current text** yourself. All NCC references are **NCC 2022 Volume One, as adopted in South Australia** (NCC 2025 is deferred in SA until 1 May 2027). Verify at [ncc.abcb.gov.au](https://ncc.abcb.gov.au).
- **Named conventions** are industry rules of thumb (Madigan, Ching, BUIL 3004, AIRAH DA-series, TIA-942 / ASHRAE / NEXTDC precedent data, aquatic-centre practice) — they carry no legal status. Attribute them, and let the relevant consultant verify.

Every figure is a **first-pass planning number** for design-studio use, not an engineering or compliance deliverable. Embodied-carbon emission factors are from the NABERS Embodied Carbon calculator v2026.1; a recognised LCA tool (eTool, One Click LCA) and a quantity surveyor own the real numbers.

See **[Glossary & Sources](Athanor_Glossary.html)** for the full citation list.

## Repository contents

- `index.html` — landing page / hub
- the six tool pages listed above
- `USABILITY_REVIEW.md` — usability, functionality and design-consistency review notes
- `embodied_carbon_tool_SPEC.md` — design spec for the Embodied Carbon tool

## Credits

Prepared July 2026 as a studio teaching resource. Simplified for teaching — roles, instruments and approval pathways are indicative. Verify statutory processes with Plan SA, the City of West Torrens and current legislation.
