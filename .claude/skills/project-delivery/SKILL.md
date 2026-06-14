---
name: project-delivery
description: >-
  Executes the project plan and runs monitoring and control: tracks progress
  against the baseline, manages issues, actions, and decisions, controls change,
  monitors risk, reports status, and steers the project. Use when the user has a
  baselined plan and is running the project, managing day-to-day execution,
  tracking progress, handling issues or changes, or preparing to report and steer.
  Triggers: "we are in delivery", "execute the plan", "monitor and control",
  "track progress", "manage issues", "the project is running", "keep the project
  on track", "steering". Links out to status-report, change-management,
  cost-management, and risk-register rather than duplicating them. Works for
  waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: phase
  phase: delivery
  related: [senior-pm, project-planning, status-report, change-management, cost-management, risk-register, project-closure]
license: MIT
---

# Project Delivery

## Overview
Delivery is where the plan meets reality: the team does the work and the PM runs the
loop of measure, compare to baseline, decide, and act. This skill establishes that
monitoring-and-control rhythm and routes the specifics — reporting, change, earned value,
risk — to the specialist skills, keeping the loop tight and the baseline protected.

## When to use this skill
- The user has a baselined plan and the project is now running.
- The user is tracking progress, managing issues/actions/decisions, or steering.
- Do NOT use this to build the plan or set the baseline — that is `project-planning`.
- Do NOT use this to close the project — that is `project-closure`.
- For a single deliverable of delivery (just a status report, just one change, just the
  risk register), go straight to `status-report`, `change-request`/`change-management`,
  `cost-management`, or `risk-register`.

## Methodology fit
- **Waterfall:** execute to the plan; monitor against the baseline; control change through
  formal change requests and stage gates.
- **Agile:** deliver in iterations; the control loop is the daily standup, sprint review,
  and retrospective; the backlog absorbs change.
- **Hybrid:** iterate inside a baselined frame; report milestones up and run sprints down
  (the right call for the Helios customer self-service portal).

## Inputs you need
A baselined plan (scope, schedule, cost), the risk register, the stakeholder and comms
approach, and a place to track issues, actions, and decisions. If there is no baseline to
measure against, return to `project-planning` first.

## Workflow
1. **Set the cadence.** Establish the governance rhythm (daily, weekly, monthly) for the
   chosen approach using `references/delivery-cadence.md`. *Done: a recurring cadence with
   owners is agreed.* Uses `references/delivery-cadence.md`.
2. **Track progress against the baseline.** Capture actual progress and compare to the
   scope/schedule/cost baseline; for cost and schedule performance (CPI/SPI, forecasts),
   use `cost-management`. *Done: current vs. baseline is known.* Uses `cost-management`.
3. **Run the issue log.** Record issues, actions, and decisions in `assets/issue-log.csv`,
   each with an owner, priority, status, and due date; distinguish them and escalate using
   `references/issue-management.md`. *Done: every open item has an owner and a next step.*
   Uses `assets/issue-log.csv` and `references/issue-management.md`.
4. **Monitor risk.** Re-review and re-score the risk register on the agreed cadence; act on
   HIGH risks before they become issues. *Done: the register is current.* Uses
   `risk-register`.
5. **Control change.** Route any proposed change to the baseline through a change request
   and the change-control process; do not let scope drift in silently. *Done: changes are
   logged, assessed, and decided.* Uses `change-management`.
6. **Report status.** Produce a concise RAG status report for stakeholders on the cadence,
   surfacing variance, top risks, and decisions needed. *Done: stakeholders have a current
   status.* Uses `status-report`.
7. **Steer.** Take the report and the issue/risk picture to the steering forum, get
   decisions on escalations, and adjust the plan within change control. *Done: the project
   is corrected toward the baseline.*
8. **Recognize the end.** When deliverables are accepted and work is winding down, hand off
   to `project-closure`. *Done: closure owns the next step.* Hands off to `project-closure`.

## Quality checklist
- [ ] A governance cadence (daily/weekly/monthly) is running with owners.
- [ ] Progress is tracked against the baseline, not just "feels on track".
- [ ] Every open issue/action/decision in `assets/issue-log.csv` has an owner and a due date.
- [ ] The risk register is reviewed on cadence; HIGH risks are acted on.
- [ ] Changes go through change control; the baseline is protected.
- [ ] Stakeholders get a concise RAG status report on cadence.
- [ ] Escalations reach a steering decision rather than stalling.

## Anti-patterns
- Reporting "green" by gut feel instead of measuring against the baseline.
- Letting issues, actions, and decisions live in people's heads or chat — not a log.
- Allowing scope to creep in without a change request, then missing the baseline.
- Maintaining a risk register that is never re-reviewed during delivery.
- Confusing activity with progress: hours burned is not the same as value delivered.

## Resources
- `references/delivery-cadence.md` — daily/weekly/monthly governance rhythm by methodology.
- `references/issue-management.md` — issue vs. risk vs. action vs. decision, and escalation.
- `assets/issue-log.csv` — fill-in log for issues, actions, and decisions.

## Related skills
- `senior-pm` — routes here when a baselined project needs to be executed and controlled.
- `project-planning` — the prior phase that hands a baselined plan to delivery.
- `status-report` — produces the RAG status reports delivery sends (step 6).
- `change-management` — governs change to the baseline during delivery (step 5).
- `cost-management` — provides earned-value tracking against the baseline (step 2).
- `risk-register` — the live risk artifact delivery monitors and acts on (step 4).
- `project-closure` — the next phase this delivery hands off to.
