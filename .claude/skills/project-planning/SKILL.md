---
name: project-planning
description: >-
  Builds the integrated project plan and sets the performance baseline by
  sequencing scope/WBS, estimation, schedule, cost/budget, resource capacity,
  risk, quality, and communications into one coherent plan. Use when the user has
  an authorized project and needs to plan it, build a project management plan, set
  a baseline, or work out scope, schedule, budget, or resourcing before delivery.
  Triggers: "build a plan", "project plan", "planning phase", "set a baseline",
  "scope and schedule", "how do I resource this", "project management plan".
  Includes a capacity_check.py helper to flag over- and under-allocated people.
  Orchestrates the specialist skills rather than duplicating them. Works for
  waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: phase
  phase: planning
  related: [senior-pm, project-initiation, project-charter, work-breakdown-structure, project-schedule, estimation, cost-management, risk-management, quality-management, raci-matrix, project-delivery]
license: MIT
---

# Project Planning

## Overview
Planning turns an authorized charter into an executable, baselined plan. This skill
sequences the planning components so they build on each other — scope before schedule,
estimates before budget, risk and quality woven through — and sets a baseline that
delivery can be measured against. The detailed techniques live in the specialist skills
it calls; this skill keeps them in the right order and consistent with one another.

## When to use this skill
- The user has an authorized project (a charter) and needs to plan it.
- The user wants a project management plan, a baseline, or an integrated view of scope,
  schedule, budget, and resources.
- Do NOT use this to authorize the project — that is `project-initiation` /
  `project-charter`.
- Do NOT use this to execute or report on the plan — that is `project-delivery`.
- For a single component (just a WBS, just a schedule, just estimates), go straight to the
  specialist skill instead of running the whole sequence.

## Methodology fit
- **Waterfall:** plan the whole scope up front; baseline scope, schedule, and cost; change
  goes through change control.
- **Agile:** plan rolling-wave — a product backlog and release goals now, detailed sprint
  plans just-in-time; the "baseline" is a roadmap and a definition of done.
- **Hybrid:** baseline outcomes, budget, and key milestones; plan delivery iteratively
  inside that frame (the right call for the Helios customer self-service portal).

## Inputs you need
An agreed charter (objectives, scope boundaries, budget range, milestones), the
stakeholder list, the chosen delivery approach, and access to the team and their
availability. If there is no charter, run `project-initiation` first.

## Workflow
1. **Decompose scope.** Build the work breakdown so every deliverable maps to verifiable
   work packages. *Done: scope is fully decomposed with no orphan deliverables.* Uses
   `work-breakdown-structure`.
2. **Estimate the work.** Estimate effort, duration, and cost per work package (analogous,
   parametric, three-point/PERT, or story points). *Done: every package has an estimate
   with stated assumptions.* Uses `estimation`.
3. **Build the schedule.** Sequence the work, apply dependencies, and find the critical
   path. *Done: a schedule with a critical path and key milestones.* Uses
   `project-schedule`.
4. **Set the cost baseline.** Roll estimates into a time-phased budget and reserves.
   *Done: an approved cost baseline.* Uses `cost-management`.
5. **Plan resources and check capacity.** Assign people to work and confirm no one is
   over- or under-allocated using the helper on `assets/resource-allocation.csv`:
   ```bash
   python scripts/capacity_check.py assets/resource-allocation.csv
   ```
   Re-level until utilization is workable. *Done: no unresolved over-allocation.* Uses
   `scripts/capacity_check.py`, `assets/resource-allocation.csv`, and
   `references/resource-capacity.md`.
6. **Plan risk and quality.** Stand up the risk approach and define quality gates and
   acceptance criteria so they are planned in, not bolted on. *Done: risk and quality
   approaches are agreed.* Uses `risk-management` and `quality-management`.
7. **Plan responsibilities and communications.** Confirm who is responsible/accountable per
   activity and how the project communicates. *Done: a RACI and a comms approach exist.*
   Uses `raci-matrix`.
8. **Integrate and baseline.** Assemble the components into `assets/project-management-plan.md`,
   reconcile them against each other, and set the baseline using
   `references/baseline-guide.md`. Walk `references/planning-checklist.md` before sign-off.
   *Done: an integrated, baselined plan is approved.* Hands off to `project-delivery`.

## Quality checklist
- [ ] Scope is decomposed into verifiable work packages.
- [ ] Every package has an estimate with stated assumptions.
- [ ] The schedule has a critical path and dated milestones.
- [ ] A cost baseline and reserves are set.
- [ ] Capacity is checked; no one is left over-allocated (`capacity_check.py`).
- [ ] Risk, quality, responsibilities, and communications are planned, not deferred.
- [ ] The plan is integrated, internally consistent, and baselined for sign-off.

## Anti-patterns
- Scheduling before scope is decomposed, so the schedule rests on guesses.
- Planning components in silos that contradict each other (the budget assumes a date the
  schedule does not support).
- Over-allocating key people because capacity was never checked.
- Treating the plan as a one-time document instead of a baseline that delivery measures
  against and change control protects.

## Resources
- `references/planning-checklist.md` — items to complete before baselining.
- `references/baseline-guide.md` — how to set and protect the scope/schedule/cost baseline.
- `references/resource-capacity.md` — capacity, utilization, and leveling guidance.
- `assets/project-management-plan.md` — fill-in integrated plan template.
- `assets/resource-allocation.csv` — sample resource allocation; input for the script.
- `scripts/capacity_check.py` — flags over/under-allocated people. Run with `--help`.

## Related skills
- `senior-pm` — routes here once a project is authorized and needs an integrated plan.
- `project-initiation` — the prior phase that hands an authorized project to planning.
- `project-charter` — the mandate this plan delivers against.
- `work-breakdown-structure` — decomposes scope (step 1).
- `estimation` — estimates the work packages (step 2).
- `project-schedule` — builds the schedule and critical path (step 3).
- `cost-management` — sets and controls the budget baseline (step 4).
- `risk-management` — plans the risk approach (step 6).
- `quality-management` — plans quality gates and acceptance (step 6).
- `raci-matrix` — assigns responsibility per activity (step 7).
- `project-delivery` — the next phase this baselined plan hands off to.
