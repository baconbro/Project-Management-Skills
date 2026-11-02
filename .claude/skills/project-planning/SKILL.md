---
name: project-planning
description: >-
  Builds the integrated project plan and baseline in one ordered pass (scope, WBS,
  estimates, resources, schedule, risk, quality, cost, communications, change control) and
  reconciles it for sponsor approval. Use when planning a project end to end or setting or
  re-setting a baseline.
metadata:
  version: 1.1.0
  category: phase
  phase: planning
  related: [senior-pm, project-initiation, project-charter, work-breakdown-structure, project-schedule, estimation, cost-management, risk-management, quality-management, raci-matrix, project-delivery, project-communication, stakeholder-management, change-management, risk-register, agile-delivery, scope-and-requirements, procurement-management, resource-management, release-and-cutover]
license: MIT
---

# Project Planning

## Overview
Planning turns an authorized charter into an integrated plan and a performance baseline: the
approved scope, schedule and cost that delivery is measured against. This skill conducts the
planning phase. It runs the specialist skills in the order in which each one's output becomes
the next one's input (scope before the WBS, people before dates, risks before reserves,
reserves before the cost baseline), keeps the assumptions and constraints log, reconciles the
parts and takes the whole baseline to the sponsor for one approval. The techniques live in the
specialist skills; this skill owns the sequence, the consistency checks and the integrated
plan. The examples use the sample Helios project (a fictional customer self-service portal used
throughout this catalog): eleven work packages, a 25-week critical path, a cost baseline (BAC) of
$500,000 ($460,000 of work-package costs plus $40,000 contingency) with a $25,000 management
reserve held above it, all approved by the sponsor Dana Okoro in one decision at M1
(Discovery complete).

## When to use this skill
- The user has an authorized project (an approved charter) and needs to plan it end to end.
- The user wants a project management plan, or must set the baseline and first check that
  scope, schedule, cost and resources agree.
- An approved change is too large to measure against the old baseline, so the remaining work
  must be re-planned and re-baselined (`references/baseline-guide.md`).
- Charter assumptions and constraints need to be carried into the plan, owned and validated.
- Do NOT use this to authorize the project — use `project-initiation` and `project-charter`.
- Do NOT use this to execute, track or report against the baseline — use `project-delivery`.
- Do NOT use this for a single component — go straight to its specialist skill, e.g.
  `scope-and-requirements` for the scope statement, `project-schedule` for the critical path,
  `resource-management` for staffing and capacity, `cost-management` for the budget.

## Methodology fit
- **Waterfall:** run all twelve steps for the whole scope up front; the sponsor approves the
  scope baseline (scope statement, WBS and dictionary), the schedule baseline and the cost
  baseline together; every later change goes through change control.
- **Agile:** plan rolling-wave with `agile-delivery`. The baseline is a prioritised product
  backlog (the scope, ordered by value), a release plan (fixed sprint length and team cost per
  sprint, and a velocity-based forecast of the scope that fits the release date) and a
  definition of done (the quality bar an increment must meet to count as progress, set with
  `quality-management`). Progress is a burn-up against the release plan; scope flexes by
  re-ordering the backlog while the date and the team cost hold. Steps 2, 3, 5 and 6 run at
  epic and release level, and sprint plans are made just in time.
- **Hybrid (Helios):** baseline the outcomes, the budget, the M1/M4/M6 milestones and the fixed
  elements in full: the Identity / SSO integration with its vendor dependency, the compliance
  requirements and the Must requirements. The Should and Could scope is a backlog that flexes
  inside that frame as scope contingency.

## Inputs you need
The approved charter (objectives, in- and out-of-scope lists, milestones, budget range,
assumptions, constraints, top risks), the business case envelope if there is one, the
stakeholder register from `stakeholder-management`, the delivery approach (ask `senior-pm` if
it is undecided), the organisation's policies (estimating, reserve percentages, procurement
thresholds, change tolerances, who signs a baseline) and who is available to work on the
project. With no approved charter, run `project-initiation` first.

## Workflow
Run the steps in order: each consumes what the earlier ones produced. When a later step changes
an earlier output (a risk response adds work, leveling moves a date), re-run the affected steps
before step 12. `references/planning-sequence.md` maps each step's inputs, outputs and loops.

1. **Open the plan and the assumptions log.** Copy `assets/project-management-plan.md` and
   record the approach, the baseline approver and the approval milestone (Helios: hybrid, Dana
   Okoro, M1). Copy `assets/assumptions-log.csv` and enter each charter assumption and
   constraint with an owner, a `validated_by` date or milestone and status `open` (Helios:
   `assets/assumptions-log-sample.csv`). An assumption whose failure would breach a baseline is
   also a risk: log it in `risk-register` (Helios A1, no identity-provider license upgrade
   needed, sits behind R001). *Done: every charter assumption and constraint has a row with an
   owner and a `validated_by`.*
2. **Agree the scope statement.** Run `scope-and-requirements`: elicit and prioritise the
   requirements, write the scope statement (deliverables with acceptance criteria and an
   acceptor, exclusions, assumptions, constraints) and start the traceability matrix; log new
   assumptions. Agile: a product vision, constraints and exclusions, with the requirements as an
   epic-level backlog in `agile-delivery`. *Done: every charter in-scope item maps to a
   deliverable, every charter exclusion is listed, and the sponsor agrees the statement for
   baselining in step 12.*
3. **Decompose the work.** Run `work-breakdown-structure` on those deliverables: a
   deliverable-oriented WBS and dictionary (owner, acceptance criterion, control account per
   work package), weights summing to 100, checked by its validator; trace the requirements to
   the WBS ids. Helios: five level-1 elements, eleven work packages (ten scheduled tasks plus
   level-of-effort project management). *Done: the validator passes
   and every deliverable maps to work packages.*
4. **Decide make-or-buy.** For each work package that could be bought (services, licences,
   hosting, contractors) run `procurement-management`: decision, sourcing route, contract type,
   need-by date and lead time. Helios buys customer sign-in from the existing identity-provider
   vendor, builds the integration in-house and calls off hosting under the enterprise
   agreement. *Done: every candidate has a recorded decision; every buy has an owner, a need-by
   date and a lead time.*
5. **Estimate the work.** Run `estimation` per work package: technique, range and basis of
   estimate, its assumptions logged; bought items are priced from step 4. Helios: 451.83
   person-days expected (P80 468.63); Identity / SSO integration carries 39% of the variance.
   Agile: size the backlog in story points. *Done: every work package has an estimate with its
   method, range and assumptions.*
6. **Staff the work and level the schedule.** Give each work package one Accountable and its
   Responsible roles with `raci-matrix`; set demand by role and week against real capacity with
   `resource-management`; sequence the work in `project-schedule` with durations for the people
   assigned and vendor lead times as external dependencies. Then level: run the capacity check,
   move work within free then total float, re-run the critical path, and repeat until nobody is
   over-allocated, or take the residual to the sponsor as a scope, capacity or date decision.
   Agile: sprint capacity and the release forecast from `agile-delivery` replace the network.
   Helios: A→B→D→G→H→J = 25 weeks, 2026-04-06 to 2026-09-25; the backend engineer's 125% W7
   peak and the frontend engineer's 105% are leveled by moving 34 hours (Carla to Ben, Devin
   to Elena) and smoothing 6 hours of the backend engineer's knowledge-base work into later
   weeks of that task's window (W9–W10). *Done: the capacity gate in `resource-management`
   passes (no one OVER in any period) and the leveled schedule meets the charter dates or
   carries an escalated decision.*
7. **Analyse risk and size the reserves.** Run `risk-management`: identify risks (including an
   assumptions analysis of the log and the vendor dependencies), analyse them, choose responses.
   Log a risk — every one — in `risk-register` with an owner, response, trigger and residual
   score. Responses that cost time or money are work: add them to the plan and re-run step 6
   for what they touch. Size the contingency from the residual exposure at a confidence the
   sponsor accepts, set the management reserve by policy, and hold one schedule reserve from
   the `project-schedule` simulation. Helios: R001 (identity-provider integration slips, EMV
   $48,000) is the top threat; contingency $40,000 (about P50 of the residual simulation; the
   sponsor accepted the gap to the $99,000 P80), management reserve $25,000, and no schedule
   reserve before GA: P80 is 28.25 weeks against a deterministic 25 and GA readiness by week
   26 has a 27% chance, which the sponsor accepted with the 2-week M6 tolerance and a
   pre-identified crash of H. *Done: every HIGH or MEDIUM threat has an owner, a response and
   a trigger, and each reserve (or accepted gap) is justified by a stated confidence.*
8. **Plan quality.** Run `quality-management`: acceptance criteria from the scope statement,
   the definition of done, quality gates with entry and exit criteria (Helios: the M4 pilot
   go/no-go and the M6 general-availability gate) and the review and test cadence. Gates,
   reviews and tests are work: put them in the estimates and schedule. Plan the transition
   with `release-and-cutover` step 1: release strategy and stages, freezes, rehearsals,
   hypercare length and staffing, decommissioning. Put the rehearsals, readiness reviews and
   hypercare into WBS 1.4.2/1.5.2, the schedule and the cost baseline (Helios: pilot at M4,
   GA flag ramp 25/50/100% from 2026-10-03, four weeks of hypercare). *Done: every gate has
   entry and exit criteria and every quality and transition activity is scheduled and
   costed.*
9. **Set the cost baseline.** Run `cost-management`: aggregate the work-package costs from
   steps 4–8 (Helios $460,000), add the contingency to reach the cost baseline (BAC $500,000),
   time-phase it on the leveled schedule into the S-curve, and agree an earning rule per work
   package. Hold the management reserve ($25,000) above the baseline: outside BAC, controlled by
   the sponsor, released only through change control; Helios' $525,000 total budget fits the
   charter's $450k–$550k. *Done: a time-phased BAC and a separate management reserve, proposed
   for approval in step 12.*
10. **Plan engagement and communications.** Refresh the engagement strategy with
    `stakeholder-management`, then turn it into the communication plan with
    `project-communication`: audiences, messages, channels, cadence, owners and the escalation
    path. Helios: daily stand-up, weekly status report, bi-weekly steering committee. *Done:
    every high-power or high-interest stakeholder has a scheduled message with an owner, and
    the escalation path is written down.*
11. **Agree change control.** With `change-management`, set the PM, change control board and
    sponsor tolerances on scope, cost and schedule, how requests are raised and logged
    (`change-request`), how contingency is drawn down and management reserve released, and
    which backlog changes the product owner may make alone. Helios: the PM approves up to $5,000
    and 2 days, the board decides above that, the sponsor decides HIGH-impact changes. *Done: a
    written procedure with tolerances, agreed before the freeze.*
12. **Integrate, reconcile and approve the baseline once.** Paste each component's summary into
    the plan, walk `references/planning-checklist.md` and resolve every conflict (a date the
    budget cannot fund, a person double-booked, an assumption with no owner, a broken
    constraint); after any late change re-run the capacity gate and re-confirm the critical
    path. Then follow `references/baseline-guide.md`: the sponsor approves the scope, schedule
    and cost baselines together in one decision, the version is snapshotted and the freeze
    announced (Helios: `assets/project-management-plan-sample.md`). Hand off to
    `project-delivery`. *Done: a dated sponsor approval, a stored baseline snapshot, and no
    `<placeholder>` left in the plan.*

## Quality checklist
- [ ] Every charter assumption and constraint is logged with an owner, `validated_by` and status.
- [ ] Every assumption that could breach a baseline is also a risk in the register.
- [ ] The agreed scope statement covers every charter in-scope item and lists every exclusion.
- [ ] The WBS validator passes; every deliverable maps to work packages with one owner.
- [ ] Every buy has a lead time in the schedule, a price in the baseline and its risks registered.
- [ ] Every work package has an estimate with its method, range and assumptions.
- [ ] Every work package has exactly one Accountable.
- [ ] The capacity gate passes on the schedule as baselined (no one OVER in any period).
- [ ] The leveled schedule has a critical path and meets the charter dates, or a sponsor decision
      is recorded.
- [ ] Every HIGH or MEDIUM threat has an owner, a response and a trigger; response work is in the plan.
- [ ] Contingency is sized from the register at a stated confidence.
- [ ] Gates, reviews and tests are scheduled and costed.
- [ ] Work-package costs + contingency = BAC, and the S-curve ends at BAC.
- [ ] The management reserve sits outside BAC, and BAC + management reserve fits the charter range.
- [ ] Every high-power or high-interest stakeholder has a scheduled message with an owner.
- [ ] Change-control tolerances are written down before the freeze.
- [ ] The sponsor approved the whole baseline in one dated decision; a snapshot is stored.

## Anti-patterns
- Scheduling before the scope is agreed and decomposed, so the dates rest on guesses.
- Fixing dates before checking who is available: fine on paper until one engineer hits 125%.
- Setting the cost baseline before the risks are analysed, so the contingency is a guess or padding.
- Counting the management reserve inside BAC, which hides it and distorts every index.
- Approving the component baselines one at a time, so they contradict each other.
- Treating charter assumptions as facts that nobody owns or validates.
- Calling the definition of done the agile baseline, or forcing a task network on an agile team.
- Treating the plan as a one-off document instead of a baseline that change control protects.

## Resources
- `references/planning-sequence.md` — why this order, the step input/output map, feedback loops,
  agile and hybrid variants.
- `references/planning-checklist.md` — pre-baseline checklist by step and the reconciliation
  cross-checks between components.
- `references/baseline-guide.md` — the three baselines, where each reserve sits, one approval,
  approved changes versus re-baselining.
- `assets/project-management-plan.md` — fill-in integrated plan (`<placeholders>`), one section
  per component, each naming its skill.
- `assets/project-management-plan-sample.md` — sample Helios plan as approved at M1.
- `assets/assumptions-log.csv` — fill-in log (`<placeholders>`): id, type (assumption or
  constraint), statement, owner, validated_by, status (open, validated, invalidated).
- `assets/assumptions-log-sample.csv` — sample Helios log at baseline: A1–A5 and CON-1–CON-4.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `senior-pm` — routes here when a project is authorized or has no baseline; uses the approved one.
- `project-initiation` — the prior phase; hands over the charter, stakeholder register and approach.
- `project-charter` — the objectives, boundaries, budget range, assumptions and constraints (step 1).
- `work-breakdown-structure` — decomposes the deliverables into the work packages later steps use (step 3).
- `project-schedule` — computes and levels the critical path and simulates the schedule reserve (steps 6–7).
- `estimation` — estimates each work package with a range and its assumptions (step 5).
- `cost-management` — turns costs plus contingency into the time-phased BAC; holds the management reserve above it (step 9).
- `risk-management` — identifies and analyses risks, chooses responses and sizes the contingency (step 7).
- `quality-management` — the acceptance criteria, definition of done and gates the plan must include (step 8).
- `raci-matrix` — one Accountable and the Responsible roles per work package (step 6).
- `project-delivery` — the next phase; receives the approved baseline and measures progress against it.
- `project-communication` — turns the engagement strategy into the communication plan (step 10).
- `stakeholder-management` — supplies the register and engagement strategy behind the communication plan (step 10).
- `change-management` — the procedure and tolerances that protect the baseline once frozen (step 11).
- `risk-register` — where every risk is logged and scored, including risky assumptions (steps 1 and 7).
- `agile-delivery` — the prioritised backlog and velocity-based release plan of the agile baseline (steps 2, 5, 6).
- `scope-and-requirements` — the scope statement and traceability matrix the WBS is built from (step 2).
- `procurement-management` — make-or-buy decisions, vendor prices, contract types and lead times (step 4).
- `resource-management` — capacity per person and week, leveling, and the capacity gate (step 6).
- `release-and-cutover` — the release strategy, rehearsals, cutover and hypercare that step 8 puts into the WBS, schedule and cost baseline.
