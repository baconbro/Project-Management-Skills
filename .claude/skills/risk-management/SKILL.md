---
name: risk-management
description: >-
  Runs the end-to-end project risk process — plan risk management, identify
  risks, analyze them qualitatively and quantitatively, plan threat and
  opportunity responses, and govern and monitor risk through delivery. Use when
  the user wants to set up risk management, run a risk identification workshop or
  pre-mortem, choose a response strategy, compute expected monetary value or a
  contingency reserve, or decide how to monitor and govern risk over time.
  Triggers: "risk management", "risk process", "identify risks", "pre-mortem",
  "risk response", "mitigate risk", "contingency reserve", "EMV", "decision
  tree", "Monte Carlo", "risk governance". For the register artifact and the
  scoring script, use risk-register. Works for waterfall, agile, and hybrid
  projects.
metadata:
  version: 1.0.0
  category: discipline
  phase: cross-cutting
  related: [project-planning, risk-register, senior-pm]
license: MIT
---

# Risk Management

## Overview
Risk management is the discipline of deciding, in advance, what could derail or boost the
project and what you will do about it. It owns the *judgment* — how to find risks, how to
weigh them, which response to pick, and how to keep watching — while the living list of
risks and its scoring live in `risk-register`. Good risk management turns surprises into
prepared decisions.

## When to use this skill
- The user wants to establish the risk process or run identification (workshop, pre-mortem).
- The user needs to analyze risk (qualitative ranking, EMV, decision trees, sensitivity).
- The user needs to choose responses or size a contingency / management reserve.
- Do NOT use this to build or score the register itself — use `risk-register`, which owns
  the `risk_score.py` helper and the register template. This skill links to it, never
  duplicates it.

## Methodology fit
- **Waterfall:** a formal risk management plan, scheduled identification, and stage-gate reviews.
- **Agile:** risk handled inside the cadence — risks surfaced in planning/retros, high-severity
  ones pulled into the backlog as spikes or stories; reserves expressed as buffer capacity.
- **Hybrid:** plan and reserves set up front; identification and response reviewed each cycle.

## Inputs you need
The charter and plan (scope, schedule, budget, assumptions, constraints), the team's
expertise, lessons from past projects, and any existing `risk-register`. If there is no
plan to assess against, run `project-planning` first — risks are deviations from a plan.

## Workflow
1. **Plan risk management.** Decide methodology, roles, cadence, probability/impact scales,
   and risk appetite/thresholds. Record who owns the process. *Done: a one-page approach the
   team agrees on, including the scales the register will use.*
2. **Identify risks** using several techniques so you do not miss whole categories —
   brainstorming, checklists, assumptions/constraints analysis, a pre-mortem, and SWOT.
   See `references/identification.md`. Capture both threats and opportunities. *Done: a
   first-pass risk list spanning multiple categories, logged into `risk-register`.*
3. **Analyze qualitatively.** Rate probability and impact, then prioritize. Hand the list to
   `risk-register` and run its `risk_score.py` to rank by exposure into HIGH/MEDIUM/LOW.
   *Done: risks ranked; the vital few separated from the trivial many.*
4. **Analyze quantitatively** for the risks that justify it — EMV, decision trees,
   sensitivity/tornado, and the Monte Carlo concept — and size contingency reserves. See
   `references/quantitative.md`. *Done: contingency reserve and any modeled outcomes computed.*
5. **Plan responses.** Pick a strategy per material risk — threats: avoid / transfer /
   mitigate / accept / escalate; opportunities: exploit / share / enhance / accept. Assign an
   owner and a concrete action. See `references/response-strategies.md`. *Done: every HIGH risk
   has an owner, a strategy, and an action, recorded back in `risk-register`.*
6. **Govern and monitor.** Set the review cadence, track residual and secondary risks, watch
   triggers, and report status (escalate per the agreed thresholds, often to `senior-pm`).
   *Done: a live monitoring rhythm with clear escalation paths.*

## Quality checklist
- [ ] A risk management plan exists (scales, roles, cadence, appetite/thresholds).
- [ ] Identification used more than one technique and covers threats AND opportunities.
- [ ] Risks are qualitatively ranked (via `risk-register`); the material few are clear.
- [ ] Quantitative analysis and a justified contingency reserve exist where warranted.
- [ ] Every HIGH risk has an owner, a chosen response strategy, and a concrete action.
- [ ] A monitoring cadence and escalation thresholds are defined.

## Anti-patterns
- Identifying risks once at kickoff and never revisiting them.
- Logging only threats and ignoring opportunities worth pursuing.
- Defaulting every risk to "accept and monitor" — that is avoidance dressed as a strategy.
- Setting a contingency reserve by gut feel instead of analysis.
- Confusing the process (this skill) with the artifact — duplicating the register or its script.

## Resources
- `references/identification.md` — brainstorming, checklists, assumptions analysis, pre-mortem, SWOT.
- `references/response-strategies.md` — threat and opportunity response strategies, defined.
- `references/quantitative.md` — EMV, decision trees, sensitivity/tornado, Monte Carlo, reserves.

## Related skills
- `risk-register` — the artifact and `risk_score.py` scoring this process feeds and consumes.
- `project-planning` — produces the plan whose deviations this skill assesses as risk.
- `senior-pm` — where major risks are escalated and governance decisions are taken.
