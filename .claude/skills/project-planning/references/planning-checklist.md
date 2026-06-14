# Planning checklist — before you baseline

Load this to confirm an integrated plan is complete and internally consistent before it is
baselined and handed to `project-delivery`. Walk it top to bottom; mark each item done or
waived with a reason. Examples use the running sample project: **Helios**, a customer
self-service portal.

## Scope
- [ ] Scope is decomposed into verifiable work packages (a WBS). See
  `work-breakdown-structure`.
- [ ] Every charter deliverable maps to at least one work package (no orphans).
- [ ] The out-of-scope list from the charter is reflected and respected.

## Estimates
- [ ] Every work package has an effort/duration/cost estimate. See `estimation`.
- [ ] Each estimate names its method and its key assumptions.
- [ ] Estimates carry an appropriate range or contingency, not false precision.

## Schedule
- [ ] Activities are sequenced with dependencies. See `project-schedule`.
- [ ] A critical path is identified.
- [ ] Milestones and the next gate are dated.
- [ ] The schedule supports any fixed dates from the charter (e.g. the Helios Q4 launch).

## Cost
- [ ] A time-phased cost baseline is built from the estimates. See `cost-management`.
- [ ] Contingency and (if used) management reserve are explicit.
- [ ] The baseline fits within the charter budget range, or the gap is escalated.

## Resources
- [ ] People are assigned to work packages. See `resource-capacity.md`.
- [ ] Capacity is checked; no one is over-allocated (run `capacity_check.py`).
- [ ] Key-person dependencies and single points of failure are noted.

## Risk, quality, responsibilities, communications
- [ ] A risk approach exists and the top risks are logged. See `risk-management`.
- [ ] Quality gates, a definition of done, and acceptance criteria are defined. See
  `quality-management`.
- [ ] Responsibilities are assigned (a RACI). See `raci-matrix`.
- [ ] A communications approach exists (audiences, channels, cadence).

## Integration and baseline
- [ ] Components are reconciled: budget, schedule, and scope agree with each other.
- [ ] The integrated plan (`project-management-plan.md`) has no unfilled placeholders.
- [ ] The baseline is approved by the sponsor (see `baseline-guide.md`).
- [ ] A change-control approach is agreed so the baseline is protected in delivery.

## Common gaps caught here
- A schedule that assumes a date the budget cannot fund, or vice versa.
- Estimates with no assumptions, so a slip cannot be traced to a cause.
- A baseline approved without a change-control process to protect it.
