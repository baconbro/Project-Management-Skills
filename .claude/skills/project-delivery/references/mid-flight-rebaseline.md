# Mid-flight interim baseline: control a running project that never had one

Load this when a project is already under way, has no approved baseline (or only a charter
and a slide of dates), and someone needs a credible status soon: "we are halfway through and
the sponsor wants a status tomorrow." Sending that project back through full
`project-planning` would take weeks it does not have. Instead, capture an **interim
baseline** in about a day from what already exists, get the sponsor to approve it, and start
controlling against it at once. Fill `assets/rebaseline-template.md` as you go. Examples
follow the sample Helios project (a fictional customer self-service portal used throughout
this catalog).

## Which situation is this?

| Situation | Path |
|---|---|
| Running, and there was never an approved baseline | This guide: interim baseline in a day |
| A baseline exists but is out of date or unachievable (variance beyond tolerance, TCPI far above CPI) | A formal re-baseline: a change request through `change-request` and `change-management`, re-planned with `project-planning` for the remaining work |
| Authorized but not started | Full `project-planning`; nothing to retro-fit yet |

The interim baseline is honest about what it is: dated, labelled "interim", built from
current knowledge, not a reconstruction of what the plan "should have been".

## The four parts (one to two hours each)
1. **Scope list.** Every deliverable, with status (accepted, done awaiting acceptance, in
   progress, not started), one acceptance criterion and a named acceptor; plus an explicit
   out-of-scope list. Sources: the charter, the backlog, contracts and statements of work, the
   team. A deliverable with no criterion or acceptor gets one now, agreed with the sponsor;
   this list is also the acceptance tracker until a full scope statement exists.
2. **Milestone dates.** The three to seven remaining milestones, each with a forecast date, a
   confidence (committed, likely, at risk) and the dependency that drives it. Ask the people
   doing the work for a range, not a single date; use `estimation` later if the range is wide.
   Milestones already passed are recorded with their actual dates.
3. **Budget to date.** Approved budget or funding envelope; actual cost to date (from
   finance, not from memory); committed but not yet spent (purchase orders, contracts);
   the team's estimate to complete the work not already committed; then estimate at
   completion = actual + committed + estimate to complete, against the approved budget.
   Note any reserve. If there is no approved budget, say so; it is the first decision to ask
   for.
4. **Open risks and issues.** The top five to ten risks with owner, response and trigger,
   entered in the register (`risk-register`); every live problem entered in
   `assets/issue-log.csv` with one owner and a due date. Two hours with the team and the
   vendor contacts usually surfaces most of them.

Then write the gaps (what is unknown, and by when you will know it) and take the snapshot to
the sponsor. **Approval** is a dated decision: "The interim baseline of <date> is what we
control and report against until <date of full re-plan or the end of the project>."

## Reporting tomorrow
- Rate schedule on milestones: forecast against the interim baseline dates (and, for passed
  milestones, actual against whatever date was promised). Rate cost on the estimate at
  completion against the approved budget. Say which proxy you used; `status-report` gives the
  rule for proxies where earned value is not available.
- Rate scope on the scope list: deliverables with no agreed acceptor or criterion, and
  pending scope requests, are AMBER until settled.
- Do not report earned value until the interim baseline is approved; from then on, earn value
  per deliverable against the scope list, with `cost-management`.
- Lead the report with the decisions needed, starting with approving the interim baseline.

## After the interim baseline
- Run the normal delivery cadence (`delivery-cadence.md`) against it from the next week.
- If more than about two months of work remain, schedule a rolling-wave pass with
  `project-planning` for the next phase or the remaining work, and replace the interim
  baseline when the sponsor approves the result.
- From approval onwards, changes to the interim baseline go through change control like any
  other baseline.

## Hypothetical Helios example
Helios was baselined at M1, so it did not need this path. If it had reached the end of month 3
without one, the snapshot would read:
- **Scope:** 1.2.1 Requirements and 1.2.2 UX design accepted at M1; 1.3.1 Identity / SSO
  integration, 1.3.2 Self-service UI, 1.3.3 Knowledge base and 1.3.4 Reporting & analytics in
  progress; 1.4 Test & launch and 1.5 Adoption & handover not started. Out of scope: live chat
  (CR001, phase 2). Partner logins (CR002) pending a decision.
- **Milestones:** M1 Discovery complete, met; M4 MVP live to pilot, at risk (SSO is two weeks
  late after the IdentityCo sandbox outage, one week beyond its float); M6 general
  availability, at risk by the same week (no schedule reserve before GA).
- **Budget to date:** approved $500,000; actual $252,000; estimate at completion about
  $535,000, so about $35,000 over, against $40,000 of contingency already largely committed.
- **Risks and issues:** R001 identity-provider slip has occurred as issue I001; R002 scope
  growth, R003 lead-engineer departure and R004 hosting cost remain open.
- **Decisions for the sponsor:** approve the interim baseline; approve IdentityCo's recovery
  plan; decide whether to draw management reserve.

## Anti-patterns
- Restarting full planning while the project keeps running unmeasured.
- Back-filling a "baseline" from the current forecast, so variance is zero by construction.
- Reporting a precise earned value against a baseline nobody approved.
- Treating the interim baseline as permanent and never re-planning a long tail of work.
