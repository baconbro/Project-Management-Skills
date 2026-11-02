# Planning checklist — before you baseline

Load this to confirm an integrated plan is complete and internally consistent before the
sponsor approves it as the baseline and it is handed to `project-delivery`. Walk it top to
bottom; mark each item done, or waived with a reason and the name of whoever accepted the
waiver. Sections follow the Workflow steps in `SKILL.md`. Examples use the sample Helios project
(a fictional customer self-service portal used throughout this catalog).

## Assumptions and constraints (step 1)
The log (`assumptions-log.csv`, Helios example `assumptions-log-sample.csv`) has six columns:
`id` (A1… for assumptions, CON-1… for constraints); `type` (`assumption` or `constraint`);
`statement` (one testable sentence); `owner` (the person who confirms it); `validated_by` (the
date or milestone by which it must be confirmed; for a constraint, by which the plan is checked
against it, normally the baseline approval); `status` — `open`, then `validated` (confirmed
true, or the plan honours the constraint) or `invalidated` (false, or the plan cannot honour
it: record the consequence in `risk-register` or the `project-delivery` issue log, and raise a
`change-request` if a baseline must move). Keep invalidated rows; never delete them.

- [ ] Every charter assumption and constraint is a row in the assumptions log
      (`assumptions-log.csv`) with an id, owner, `validated_by` and status.
- [ ] Assumptions added by the scope statement and the estimates are in the log too.
- [ ] Every assumption whose failure would breach a baseline is also logged in `risk-register`
      (Helios A1 → R001).
- [ ] Every constraint names the schedule date, budget line or activity that honours it; any
      constraint the plan cannot honour is escalated to the sponsor before approval.

## Scope (steps 2–3)
- [ ] The scope statement is agreed with the sponsor. See `scope-and-requirements`.
- [ ] Every charter in-scope item maps to a deliverable with acceptance criteria and one acceptor.
- [ ] Every charter out-of-scope item is in the exclusions.
- [ ] The WBS validator passes; every deliverable maps to work packages, each with one owner.
      See `work-breakdown-structure`.

## Procurement and external dependencies (step 4)
- [ ] Every work package that could be bought has a recorded make-or-buy decision. See
      `procurement-management`.
- [ ] Every supplier, contract and third-party dependency (Helios: the identity-provider
      vendor's sandbox) has a need-by date, and its lead time is in the schedule.
- [ ] Every vendor price is in the cost baseline and every vendor failure mode is in the risk
      register.

## Estimates (step 5)
- [ ] Every work package has an effort and cost estimate. See `estimation`.
- [ ] Each estimate names its technique, a range and its assumptions — no single-point figures
      presented as certain.

## Responsibilities, resources and schedule (step 6)
- [ ] Every work package has exactly one Accountable and at least one Responsible. See
      `raci-matrix`.
- [ ] Every Responsible person has capacity in the weeks the schedule puts their work, net of
      leave and other commitments. See `resource-management`.
- [ ] The capacity gate passes on the schedule as baselined: no one OVER in any period, or
      each residual is a recorded sponsor decision.
- [ ] Activities are sequenced, the critical path is computed (not guessed) and the
      near-critical tasks are named. See `project-schedule`.
- [ ] Every charter milestone has a baseline date on or before its charter date (Helios: M4
      MVP live to pilot, M6 general availability).
- [ ] Key-person dependencies have a named cover and a risk in the register.

## Risk and reserves (step 7)
- [ ] Risks were identified with more than one technique, including an assumptions analysis.
      See `risk-management`.
- [ ] Every risk is in `risk-register`, scored in the agreed scales; every HIGH or MEDIUM
      threat has an owner, a response and a trigger.
- [ ] Response actions that cost time or money are in the WBS, estimates and schedule.
- [ ] The contingency reserve is sized from the register at a stated confidence; the
      management reserve is set by policy; one schedule reserve is held, not spread into tasks.

## Quality (step 8)
- [ ] The definition of done, acceptance criteria and quality gates with entry and exit
      criteria are defined. See `quality-management`.
- [ ] Every gate is a dated milestone and every review and test activity is estimated and
      scheduled.

## Cost baseline (step 9)
- [ ] Work-package costs are aggregated bottom-up before any reserve is added. See
      `cost-management`.
- [ ] Cost baseline (BAC) = work-package costs + contingency; the S-curve ends at BAC.
- [ ] The management reserve is held above the baseline: outside BAC, controlled by the
      sponsor, released only through change control.
- [ ] BAC + management reserve fits the charter budget range, or the gap is escalated
      (Helios: $500,000 + $25,000 = $525,000 inside $450k–$550k).
- [ ] An earning rule is recorded per work package.

## Stakeholders and communications (step 10)
- [ ] The engagement strategy is current for every key stakeholder. See
      `stakeholder-management`.
- [ ] The communication plan gives every high-power or high-interest stakeholder a message,
      channel, cadence and owner, and names the escalation path. See `project-communication`.
- [ ] The governance cadence is set (Helios: daily stand-up, weekly status report, bi-weekly
      steering committee).

## Change control (step 11)
- [ ] The change-control procedure and the PM, board and sponsor tolerances are written down.
      See `change-management`.
- [ ] The rules for drawing down contingency and releasing management reserve are agreed.
- [ ] Agile or hybrid: the backlog changes the product owner may make without a change
      request are written down.

## Integration and approval (step 12)
Reconciliation cross-checks — each compares two components:
- [ ] Same ids everywhere: every work package appears in the estimates, the schedule, the RACI
      and the cost baseline, and nothing else does.
- [ ] Cost against schedule: the S-curve is time-phased on the leveled schedule, not on an
      earlier draft.
- [ ] Schedule against people: the capacity gate was re-run after the last schedule change.
- [ ] Schedule against vendors: every vendor delivery lands before the task that needs it.
- [ ] Risk against plan: every response with a cost is in the baseline; the contingency covers
      the residual exposure at the stated confidence.
- [ ] Assumptions against plan: no open assumption is past its `validated_by` date.

Approval:
- [ ] The integrated plan (`project-management-plan.md`) has no `<placeholder>` left.
- [ ] The sponsor approves the scope, schedule and cost baselines together in one dated
      decision. See `baseline-guide.md`.
- [ ] The approved version is snapshotted and the freeze is announced.

## Common gaps caught here
- A schedule that assumes a date the budget cannot fund, or vice versa.
- A schedule that was never leveled: the team average looks fine while one person is at 125%.
- A cost baseline whose contingency was set before the risks were analysed.
- Management reserve counted inside BAC.
- A vendor dependency with no lead time in the schedule.
- Estimates with no assumptions, so a slip cannot be traced to a cause.
- Charter assumptions that nobody owns or validates.
- A baseline approved without a change-control process to protect it.
