---
name: stakeholder-management
description: >-
  Identifies, analyzes, and engages project stakeholders by mapping power and
  interest, assessing salience, comparing current versus desired engagement, and
  setting an engagement strategy per stakeholder. Use when the user wants to find
  out who the stakeholders are, analyze or prioritize them, build a stakeholder
  register or power/interest grid, decide how to engage or influence a group, or
  manage a difficult sponsor or blocker. Triggers: "stakeholder analysis",
  "stakeholder register", "stakeholder map", "power/interest grid", "salience
  model", "engagement plan", "who are the stakeholders", "manage stakeholders".
  Hands off responsibilities to raci-matrix and the comms plan to
  project-communication. Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: discipline
  phase: cross-cutting
  related: [project-initiation, raci-matrix, project-communication, project-charter]
license: MIT
---

# Stakeholder Management

## Overview
Stakeholder management is the discipline of working out who is affected by or can affect
the project, how much they matter, where they stand today, and what you will deliberately
do to move them to where you need them. Projects rarely fail on the technology; they fail
because a key stakeholder was ignored, surprised, or left unconvinced.

## When to use this skill
- The user is starting a project and needs to identify who is involved or affected.
- The user wants to analyze, prioritize, or map stakeholders (power/interest, salience).
- A stakeholder is blocking, disengaged, or over-engaged and needs a deliberate strategy.
- Do NOT use this to assign task-level responsibilities — use `raci-matrix` instead.
- Do NOT use this to design the communication cadence and channels — use
  `project-communication`, which consumes the engagement strategy produced here.

## Methodology fit
- **Waterfall:** a formal stakeholder register and analysis, reviewed at stage gates.
- **Agile:** a lightweight stakeholder map; the Product Owner carries engagement, reviewed
  each iteration as new stakeholders surface.
- **Hybrid:** register fixes the key players and strategy; engagement adapts per cadence.

## Inputs you need
The project charter or brief (for sponsor and named stakeholders), the org chart, the
list of teams and external parties affected, and any history of past projects with these
people. If no sponsor or stakeholder list exists yet, pull them from `project-charter` or
run `project-initiation` first.

## Workflow
1. **Identify** every stakeholder — internal and external, supportive and opposed. Brainstorm
   by category (sponsor, users, ops, vendors, regulators, neighbours). For Helios, that spans
   the VP of Support (sponsor), call-centre agents, customers, the identity vendor, and
   security/compliance. *Done: a draft list with no obvious group missing.*
2. **Analyze** each stakeholder. Rate **power** and **interest** (H/M/L) and place them on the
   grid; for contested cases apply the salience model (power/legitimacy/urgency). Use
   `references/analysis-techniques.md` for the grid, salience model, and stakeholder cube.
   *Done: every stakeholder has power and interest rated.*
3. **Assess engagement** — record each stakeholder's **current** stance (Unaware / Resistant /
   Neutral / Supportive / Leading) and the **desired** stance the project needs. The gap, not
   the absolute level, drives effort. *Done: current and desired captured for each.*
4. **Set a strategy** per stakeholder to close the gap (Manage Closely / Keep Satisfied / Keep
   Informed / Monitor, plus a concrete action). Capture it in
   `assets/stakeholder-register.csv`. *Done: every High-power stakeholder has a named strategy.*
5. **Visualize and align** using `assets/engagement-matrix.md` so the sponsor sees who is where
   and agrees the priorities. *Done: matrix filled and reviewed with the sponsor.*
6. **Hand off** responsibilities to `raci-matrix` and feed the strategy into
   `project-communication` to turn engagement intentions into a scheduled comms plan.
   *Done: both downstream skills have what they need.*
7. **Review on cadence.** Re-rate as the project changes; stakeholders move. *Done: a review
   rhythm is set.*

## Quality checklist
- [ ] Every stakeholder has power and interest rated and a grid position.
- [ ] Current and desired engagement levels are both recorded.
- [ ] Every High-power stakeholder has a named owner and a concrete strategy.
- [ ] The register and engagement matrix are reviewed with the sponsor.
- [ ] Responsibilities handed to `raci-matrix`; strategy fed to `project-communication`.
- [ ] A review cadence is set so the analysis stays current.

## Anti-patterns
- Treating the stakeholder list as a one-time artifact never revisited.
- Confusing interest with power — a loud, low-power voice is not a priority by volume.
- Listing only supporters and ignoring resistors and silent blockers.
- Writing strategies as adjectives ("engaged") rather than actions with an owner.
- Collapsing engagement into communication — engagement is the intent, comms is the vehicle.

## Resources
- `references/analysis-techniques.md` — power/interest grid, salience model, and stakeholder cube.
- `assets/stakeholder-register.csv` — fill-in register with power, interest, and engagement.
- `assets/engagement-matrix.md` — current-vs-desired engagement matrix template.

## Related skills
- `project-initiation` — the phase where stakeholders are first identified.
- `project-charter` — names the sponsor and key stakeholders this analysis builds on.
- `raci-matrix` — turns stakeholders into role-level responsibilities.
- `project-communication` — consumes the engagement strategy to build the comms plan.
