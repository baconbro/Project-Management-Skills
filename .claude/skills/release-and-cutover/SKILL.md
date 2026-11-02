---
name: release-and-cutover
description: >-
  Plans and runs the move from built and tested to live and supported: chooses the
  release strategy (big-bang, phased, pilot, parallel run, feature-flag ramp), sets
  go-live readiness criteria per workstream, runs the go/no-go decision to a GO,
  CONDITIONAL GO or NO-GO verdict by a named approver, writes and rehearses a timed
  cutover runbook with verifications and rollback triggers, then runs hypercare to
  measured exit criteria and hands the service to operations. Use when the user is
  preparing a launch, go-live, migration weekend or rollout, needs a go/no-go
  checklist, cutover runbook, rollback plan or hypercare plan, or must decide
  whether a release is ready. Triggers: "cutover plan", "cutover runbook", "go/no-go
  decision", "go-live readiness", "we go live next week", "rollback plan", "release
  strategy", "phased rollout", "pilot launch", "parallel run", "dress rehearsal",
  "hypercare". For closing the project after hypercare, use project-closure. Works
  for waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: artifact
  phase: delivery
  related: [project-delivery, project-closure, quality-management, project-communication, change-management, risk-register]
license: MIT
---

# Release and Cutover

## Overview
Release and cutover is the controlled move from "built and tested" to "live and supported". It
covers four decisions a senior project manager owns: **how** to release (the strategy:
big-bang, phased, pilot, parallel run or feature flags), **whether** to go (a go/no-go decision
on evidence, made by one named approver), **how to get there and back** (a timed cutover runbook
with a verification and a rollback action on every step), and **when the project can let go**
(hypercare, a time-boxed period of elevated support after go-live, ending on measured exit
criteria and the operations owner's signature). It is the bridge between `project-delivery`,
which builds and controls the work, and `project-closure`, which closes the project once the
service is handed over. The examples use the sample Helios project (a fictional customer
self-service portal used throughout this catalog): its general availability (GA) release at
milestone M6 moves customers from the 200-customer pilot to the full portal with SSO sign-in,
through a Saturday cutover on 2026-10-03 and four weeks of hypercare.

## When to use this skill
- A launch, go-live, migration weekend or rollout is weeks away and there is no agreed strategy,
  readiness criteria, runbook or rollback plan.
- The user must decide, or prepare the decision on, whether a release is ready ("we go live next
  week — are we ready?").
- The user needs a cutover runbook, a go/no-go checklist, rollback triggers, a dress rehearsal or
  a hypercare plan, or must decide when hypercare can end.
- A pilot or phased rollout needs gates between its stages.
- Do NOT use this to set acceptance criteria, test exit criteria or the definition of done — use
  `quality-management` instead; this skill reuses them as readiness evidence.
- Do NOT use this to close the project after hypercare (formal acceptance, financial close,
  releasing the team) — use `project-closure` instead.
- Do NOT use this to plan user adoption, training content or resistance — use
  `change-management` instead; this skill checks on the day that adoption readiness is in place.

## Methodology fit
- **Waterfall:** one or a few large cutovers at the end of build; readiness reviews at T-4, T-2
  and T-1 weeks; a go/no-go at the stage gate signed by the sponsor; at least two rehearsals; the
  runbook frozen at the decision and changed only through change control.
- **Agile:** continuous delivery makes deployment routine: small releases behind feature flags,
  "releasable" in the definition of done and a light readiness check per release goal. The
  business cutover (switching a channel, retiring the old process, readying the service desk)
  still gets a runbook, a go/no-go and hypercare.
- **Hybrid:** a formal go/no-go per milestone release, with sprint-built increments staged behind
  flags inside it. Helios: pilot at M4, then GA at M6 ramped 25% → 50% → 100% from 2026-10-03 to
  2026-10-12, each ramp step gated on hypercare metrics; Dana Okoro (Sponsor, VP Customer
  Operations) approves each go/no-go and Sam Lee (project manager) drives it.

## Inputs you need
- The release scope and its acceptance status: accepted stories or deliverables, UAT sign-off
  and the test exit criteria from `quality-management`.
- The milestones and fixed dates from `project-schedule`, the business calendar and blackout
  periods, and the contract end of anything being replaced.
- The open risks, especially HIGH ones, from `risk-register`; the approved changes in the
  release and the change freeze from `change-management`.
- Transition requirements (training, data conversion, support model, decommissioning) from
  `scope-and-requirements`, and the adoption plan from `change-management`.
- The go/no-go decision rights as a DACI from `raci-matrix`, the named operations owner who will
  accept the service, and the vendors needed in the window.
- The communication plan and escalation path from `project-communication`.

If nobody can name the operations owner who will accept the service, stop and get one named:
without one there is nobody to hand over to, and hypercare never ends.

## Workflow
1. **Choose the release strategy and the window.** Work through the eight questions in
   `references/release-strategies.md` (coexistence, reversibility, blast radius, data
   ownership, absorbable change, dual-running cost, fixed dates, what is still to learn), choose
   the strategy and its stages, set the code, change and business freezes, and size the window
   as rehearsed critical path + 20-30% contingency + full rollback time. Helios: a pilot at M4,
   then a GA flag ramp; window Saturday 2026-10-03 06:00-12:00 with go-live (T0) at 09:00; code
   freeze from 2026-09-28. *Done: strategy, stages, freezes and window are recorded with their
   reasons and agreed by the sponsor.*
2. **Set readiness criteria and decision rights.** At T-6 to T-4 weeks copy the template in
   `assets/go-no-go-checklist.md` and fill sections 1-2: one measurable criterion per line across
   the workstreams in `references/go-no-go-and-rollback.md`, each with an owner, an evidence
   source and a blocking flag, with test thresholds taken from `quality-management`. Name one
   approver and one driver and record them as a DACI with `raci-matrix`; book readiness reviews
   at T-4, T-2 and T-1 weeks and the decision at T-3 to T-1 days. *Done: every criterion has an
   owner, evidence and a blocking flag, and the approver, driver and review dates are published.*
3. **Write the cutover runbook.** Copy `assets/cutover-runbook-template.csv` and follow
   `references/cutover-runbook-and-hypercare.md`: anchor on T0, use the standard phases, give
   each 5-60 minute step one owner, an observable verification and a rollback action (or "None"
   with the reason), set predecessors so independent steps run in parallel, and add a go-live
   checkpoint, a rollback-window checkpoint and comms steps. `assets/cutover-runbook-sample.csv`
   is the Helios GA runbook v1.3: 20 steps from Friday's pre-cutover checks to the bridge
   closing at 11:00 on Saturday, plus rollback steps R1-R7 on standby. *Done: every row has an
   owner, planned start, offset, duration, verification and rollback action, and the critical
   path fits the window with its contingency.*
4. **Design the rollback and log the cutover risks.** In section 3 of
   `assets/go-no-go-checklist.md` record quantified, time-boxed rollback triggers; who may call a
   rollback without escalation; the point of no return; and the last safe rollback start (window
   end − rehearsed rollback duration), with the rollback-window checkpoint at least 30 minutes
   before it. Log the cutover risks and any waiver's risk in the register and check it:
   ```bash
   python .claude/skills/risk-register/scripts/risk_score.py .claude/skills/risk-register/assets/risk-register-template.csv --bac 500000 --check
   ```
   Helios: full rollback R1 → R5 → R6 takes 75 minutes, so the last safe rollback start is 10:45
   and the checkpoint is at 10:00; one trigger is SSO sign-in success below 95% over 15 minutes.
   *Done: triggers, authority, point of no return and last safe rollback start are written down,
   and the register check passes with the cutover risks in it.*
5. **Rehearse, then re-time.** Run a technical dry run and a dress rehearsal with the real
   people, bridge and comms, including the rollback restored from a real backup
   (`references/cutover-runbook-and-hypercare.md`). Put the rehearsed durations into the runbook
   and re-sequence until the window keeps at least 30 minutes of margin. Helios: the 2026-09-26
   rehearsal ran 25 minutes late on the search re-index, so v1.3 runs it alongside the SSO
   configuration; the rollback took 70 of its 75 minutes. *Done: runbook durations are rehearsed
   values, the rollback has been executed once, and the margin is at least 30 minutes.*
6. **Plan communications and hypercare.** Agree the release communications with
   `project-communication` (notices before, bridge updates and the go-live announcement during,
   a prepared rollback message), then fill `assets/hypercare-plan-template.md`: period and
   extension rule, ramp and decommission steps, L1/L2/L3 triage path, severity service levels,
   staffing by week, daily stand-down, metrics with thresholds, patch cadence and measurable
   exit criteria. Helios: 4 weeks from 2026-10-03 to 2026-10-30 (the warranty period in WBS
   1.5.2 Operational handover), accepted by Priya Nair (Head of Support Operations). *Done:
   comms have owners and approved templates, and the hypercare plan names the operations owner
   and measurable exit criteria.*
7. **Hold the go/no-go.** Run the meeting in `references/go-no-go-and-rollback.md`: walk the
   criteria by exception, review open HIGH risks and the rollback design, poll each consulted
   lead aloud, and let the approver decide. Record the verdict, conditions (owner, due date, the
   stage they gate) and waivers (compensating control, expiry, risk id) in sections 4-5 of
   `assets/go-no-go-checklist.md` and send them out within the hour. Helios on 2026-09-30:
   CONDITIONAL GO with conditions C1 (six agents still to train before the 50% ramp) and C2
   (three severity-3 fixes in patch 1) and waiver W1 (order-status probe replaced by manual
   checks until 2026-10-09). *Done: a verdict from the named approver, with every condition and
   waiver owned and dated, has reached everyone in the communication plan.*
8. **Execute from a command center.** At the bridge opening run the day-of checkpoint in section
   6 of `assets/go-no-go-checklist.md`, then the runbook: owners announce start and finish, the
   scribe logs actual times and decisions, the cutover lead reports every 30 minutes and at each
   checkpoint, calls go-live at the go-live checkpoint, and calls a rollback the moment a trigger
   fires, with no debate on the bridge. *Done: every step is done, skipped with a logged reason
   or rolled back, and go-live or rollback was declared at a checkpoint and announced.*
9. **Run hypercare and exit on criteria.** Hold the daily stand-down, triage through the agreed
   path, gate each ramp or decommission step on the metrics, ship fixes on the patch cadence and
   close the go/no-go conditions and waivers. At the exit review test every exit criterion in
   `assets/hypercare-plan-template.md` against evidence and extend week by week while any fails.
   On exit, transfer open defects, get the operations owner's signed acceptance, send the exit
   record to `project-closure` for its handover step, and take the post-release review findings
   to `lessons-learned`. *Done: exit criteria met with evidence, acceptance signed, and closure
   and lessons have their inputs.*

## Quality checklist
- [ ] Strategy, stages, freezes and window are recorded with their reasons and agreed by the sponsor.
- [ ] Every readiness criterion is measurable, with an owner, an evidence source and a blocking flag.
- [ ] The named approver's verdict, the poll, each condition (owner, due date) and each waiver
      (control, expiry, risk id) are recorded; no waiver covers a severity-1 defect, an untested
      rollback, a legal obligation or a missing operations owner.
- [ ] Every runbook row has one named owner, a planned start, a duration, an observable
      verification and a rollback action or a reasoned "None".
- [ ] Rollback triggers are quantified and time-boxed; the rollback-window checkpoint is at least
      30 minutes before the computed last safe rollback start.
- [ ] The cutover and the rollback were rehearsed, and the runbook durations are rehearsed values.
- [ ] Cutover risks are in the risk register and its `--check` passed before the decision.
- [ ] Release communications have owners and approved go-live and rollback templates.
- [ ] The hypercare plan has dates, an extension rule, a triage path, severity service levels,
      metric thresholds and measurable exit criteria.
- [ ] Hypercare ended on evidence against the exit criteria, and the operations owner's signed
      acceptance went to `project-closure`.

## Anti-patterns
- A go/no-go that always says go: criteria invented on the day, "green" by assertion, or the
  date deciding the verdict (more than two waivers is the tell).
- No rollback plan because "we will fix forward", or a rollback plan nobody has rehearsed.
- Debating a rollback on the bridge at 03:00 because the triggers were never quantified.
- Runbook steps such as "deploy the app — IT" with no named owner, duration or verification.
- Big-bang by default on a change with a large blast radius when a reversible option existed.
- Leaving training and service-desk readiness to the last week (lesson LL007 in `lessons-learned`).
- A Friday-evening go-live with nobody on hand on Monday morning.
- Hypercare that ends on a date regardless of incidents, or never ends because nobody owns exit.
- Switching off the old process before hypercare exit, so a rollback has nowhere to go.

## Resources
- `references/release-strategies.md` — deployment versus release versus cutover; big-bang,
  phased, pilot, parallel run, feature flags and blue-green compared; the eight questions that
  decide the strategy; freezes and window sizing; transition requirements; the Helios choice.
- `references/go-no-go-and-rollback.md` — readiness criteria per workstream, review cadence,
  decision rights, GO / CONDITIONAL GO / NO-GO rules, waiver limits, the meeting agenda, and
  rollback design: triggers, authority, point of no return, last safe rollback start, fix-forward.
- `references/cutover-runbook-and-hypercare.md` — building and rehearsing the runbook,
  command-center roles and cadence, hypercare duration, staffing, triage, metrics, exit criteria,
  handover and the post-release review.
- `assets/go-no-go-checklist.md` — fill-in go/no-go checklist (decision frame, criteria, rollback
  readiness, conditions and waivers, poll and verdict, day-of checkpoint) plus the Helios GA sample.
- `assets/cutover-runbook-template.csv` — fill-in runbook skeleton with the standard phases and a
  rollback block; columns `step, phase, action, owner, planned_start, t_offset, duration_min,
  predecessors, verification, rollback_action, status` (status `planned`, `in-progress`, `done`,
  `failed`, `skipped`, or `standby` for rollback rows).
- `assets/cutover-runbook-sample.csv` — sample: Helios GA runbook v1.3, steps 1-20 and R1-R7.
- `assets/hypercare-plan-template.md` — fill-in hypercare plan plus the Helios GA sample.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-delivery` — the phase this sits inside: release issues and decisions run through its
  issue log and steering, and this skill returns a live, supported service before it ends.
- `project-closure` — receives the hypercare exit record and the operations owner's signed
  acceptance, which complete its handover-to-operations step and feed the closure report.
- `quality-management` — supplies the acceptance criteria and the quality-gate and UAT exit
  criteria that this skill's test-readiness criteria reuse as go/no-go evidence.
- `project-communication` — schedules the release notices, bridge updates, go-live announcement
  and prepared rollback message, and provides the escalation path the command center uses.
- `change-management` — controls late changes through the freeze and emergency change route, and
  runs adoption and reinforcement alongside hypercare, including retiring the old way.
- `risk-register` — holds the cutover and waiver risks; its open HIGH risks and `--check` result
  are reviewed at every go/no-go.
