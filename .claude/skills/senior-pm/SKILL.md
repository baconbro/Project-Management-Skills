---
name: senior-pm
description: >-
  Acts as the front door to the project-management catalog: diagnoses where a
  project sits (idea, initiation, planning, delivery, or closing) and how healthy
  it is, recommends a methodology (waterfall, agile, or hybrid), and routes the
  user to the right specialist skill. Use when the user is unsure where to start,
  asks for general project-management help, describes a project without naming an
  artifact, wants a methodology recommendation, or needs a health check and next
  step. Triggers: "help me manage a project", "where do I start", "is my project
  on track", "which approach should I use", "what should I do next", "project
  health check", "waterfall or agile". Works for waterfall, agile, and hybrid
  projects.
metadata:
  version: 1.0.0
  category: orchestrator
  phase: cross-cutting
  related: [project-initiation, project-planning, project-delivery, project-closure, risk-management]
license: MIT
---

# Senior PM

## Overview
This skill is the triage desk for the whole catalog. It figures out what stage a
project is in, takes a quick read on its health, suggests how the work should be run
(waterfall vs. agile vs. hybrid), and then sends the user to the specialist skill that
actually does the work. It does little itself — its value is asking the right questions
and routing well.

## When to use this skill
- The user describes a project or a problem but does not name a specific artifact or phase.
- The user asks "where do I start", "what should I do next", or "is my project on track".
- The user wants a methodology recommendation or a quick health check.
- Do NOT use this once the stage and need are clear — go straight to the phase skill
  (`project-initiation`, `project-planning`, `project-delivery`, `project-closure`) or
  the relevant artifact skill instead.

## Methodology fit
- **Waterfall:** recommend when scope is well understood, change is costly, and stage
  gates and sign-offs matter (compliance, construction, fixed-price).
- **Agile:** recommend when requirements are uncertain, feedback loops are valuable, and
  the team can deliver in increments.
- **Hybrid:** recommend when outcomes and constraints are fixed but delivery can be
  iterative — the common case for the Helios customer self-service portal.
- See `references/methodology-selection.md` for the full decision guide.

## Inputs you need
A short description of the project, its current state (does it have a charter? a plan? is
it running? is it ending?), the biggest pain or question right now, and any hard
constraints (deadline, budget, compliance). If the user cannot describe the desired
outcome at all, start at `project-initiation`.

## Workflow
1. Run a quick **intake** — ask the user, in order:
   (a) What outcome are you trying to achieve? (b) What exists today — idea, charter,
   plan, work in progress, or a finished deliverable? (c) What is the single biggest
   problem or decision right now? (d) Any fixed deadline, budget, or compliance constraint?
   *Done: you can name the stage and the top concern.*
2. **Diagnose the stage** from the answers: no charter/justification → initiation; charter
   but no baseline → planning; baselined and executing → delivery; deliverable accepted or
   work stopping → closure. *Done: one stage is chosen.*
3. **Read health** quickly — is scope agreed, is there a plan/baseline, are risks tracked,
   is status known, are stakeholders engaged? Flag any "no" as a gap to close.
   *Done: a one-line RAG-style health read with the top gap named.*
4. **Recommend a methodology** using `references/methodology-selection.md`. State the
   recommendation and the one or two signals that drove it. *Done: waterfall/agile/hybrid
   recommended with reasons.*
5. **Route** to the right skill using `references/routing-map.md`, naming the skill in
   backticks and the first action to take there. Route to at most two skills so the user
   is not overwhelmed. *Done: the user has a named next skill and first step.*
6. If a term is unclear to the user, point them to `references/pm-glossary.md`.
   *Done: hand-off complete.*

## Quality checklist
- [ ] The four intake questions were asked (or already answered).
- [ ] Exactly one stage is named (initiation / planning / delivery / closure).
- [ ] A one-line health read names the single biggest gap.
- [ ] A methodology is recommended with the signal(s) behind it.
- [ ] The user is routed to a named skill and a concrete first step.

## Anti-patterns
- Routing before diagnosing the stage — the wrong skill wastes the user's time.
- Recommending a methodology by default (always "agile") instead of from the signals.
- Dumping the whole catalog on the user; route to one or two skills, not ten.
- Doing the downstream work here (writing the charter, building the plan) instead of
  handing off — this skill triages, the specialist skills deliver.

## Resources
- `references/methodology-selection.md` — when waterfall, agile, or hybrid each fits, with signals and a checklist.
- `references/routing-map.md` — situation-to-skill routing table covering all 22 catalog skills.
- `references/pm-glossary.md` — concise definitions of the key PM terms used across the catalog.

## Related skills
- `project-initiation` — route here to stand up a new project (need, charter, stakeholders, kickoff).
- `project-planning` — route here once a project is authorized and needs an integrated plan.
- `project-delivery` — route here to execute and monitor a baselined project.
- `project-closure` — route here to formally close a project or phase.
- `risk-management` — route here when the dominant concern is uncertainty and threats.
