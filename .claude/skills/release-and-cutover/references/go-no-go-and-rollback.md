# Go/no-go and rollback

The go/no-go decision answers one question on evidence: is it safer to go live now than to
wait? Rollback is what makes "go" a reversible decision. Design both together, weeks before the
date, and record them in `assets/go-no-go-checklist.md`.

## Readiness criteria by workstream
| Workstream | Typical criteria | Evidence | Blocking? |
|---|---|---|---|
| Scope and build | Release scope accepted by the product owner; release candidate frozen | Review record, build id | Yes |
| Test and quality | Zero open severity-1/2 defects; UAT signed off; performance at forecast peak | Defect report, UAT sign-off, load-test report | Yes |
| Security and compliance | No open high/critical findings; privacy, legal and accessibility sign-offs | Penetration retest, signed memos, audit report | Yes |
| Data | Migration rehearsed; reconciliation within tolerance; backup restore tested | Rehearsal log, reconciliation report | Yes when data moves |
| Operations | Capacity, monitoring and alerting live; runbooks accepted; on-call rota published | Dashboards, paging test, signed runbook review | Yes |
| Support and training | Service desk and end users trained; triage path and known-error articles ready | Attendance record, triage chart | Usually not |
| Communications | Notices sent; go-live and rollback message templates approved | Sent log, approved templates | Usually not |
| Vendors and dependencies | Critical vendors confirmed for the window; no colliding release | Written confirmation, change calendar | Yes for critical vendors |
| Cutover and rollback | Runbook rehearsed inside the window; rollback rehearsed; triggers agreed | Rehearsal log with timings | Always, never waivable |
| Risk | No open HIGH risk without an active response; cutover risks logged | Risk register check | Yes |
| Business | Calendar clear; benefits baseline captured; role changes agreed | Calendar, baseline report, signed plan | Usually not |

Write each criterion so a stranger could check it: a threshold, an owner, an evidence source and
a blocking flag. "Testing complete" is not a criterion; "zero open severity-1/2 defects in the
tracker at noon on decision day" is. Reuse the gate and UAT exit criteria from
`quality-management` instead of inventing new thresholds.

## Cadence
- **T-6 to T-4 weeks:** agree the criteria, owners and decision rights; publish the checklist.
- **T-4, T-2 and T-1 weeks:** readiness reviews. Each owner reports status and trend, and every
  amber item gets a recovery date. Trend matters more than the snapshot: an item still red at
  T-1 week rarely turns green by the decision.
- **T-3 to T-1 days:** the go/no-go decision. Late enough to see final test results, early
  enough to stand vendors down and send a no-go message calmly.
- **Day of cutover:** a 10-minute checkpoint at the bridge opening, before the first production
  change, confirming that owners are present and nothing has changed since the decision.

## Decision rights
One **Approver** decides, usually the sponsor. The **Driver**, usually the project manager,
runs the reviews and makes the recommendation. Workstream leads are **Consulted** and state
their own verdict aloud; operations and support are at least **Informed**. Record this as a
DACI with `raci-matrix` before the first readiness review. For the general availability (GA)
release of the sample Helios project (a fictional customer self-service portal used throughout
this catalog), Dana Okoro (Sponsor, VP Customer Operations) approves, Sam Lee (project manager)
drives, and Ava Chen (product owner), Ben Adeyemi (tech lead), Marcus Webb (Security lead) and
Priya Nair (Head of Support Operations) are consulted.

## Verdict rules
- **GO:** every blocking criterion met; every non-blocking criterion met.
- **CONDITIONAL GO:** every blocking criterion met or waived; each open non-blocking item becomes
  a condition with an owner, a due date and the stage it must be met before (for example
  "before the 50% ramp").
- **NO-GO:** any blocking criterion unmet and not waived, or a consulted lead's "no" that the
  approver cannot resolve with a condition. A no-go is the process working: record the reason,
  the fix owner and the new decision date, and send the prepared no-go message the same day.

## Waivers
Only the approver waives a blocking criterion, and only with a compensating control, an owner,
an expiry date and a risk logged in `risk-register`. Never waive an open severity-1 defect, an
untested rollback, a legal or regulatory obligation, or a missing operations owner. Count them:
more than two waivers on one release usually means the date, not readiness, is deciding.

## Running the meeting (30-45 minutes)
1. The driver states the release, the strategy, the window and the decision required.
2. Walk the checklist by exception: only criteria not met, with their owner speaking.
3. Review the open HIGH risks and the cutover risks from the register.
4. Confirm the rollback triggers, the last safe rollback start and who may call a rollback.
5. Poll each consulted lead for go or no-go on their area. Silence is not consent.
6. The approver decides; the scribe reads back the verdict, conditions and waivers.
7. Send the decision to every audience in the communication plan within the hour.

## Designing the rollback
- **Triggers** are observable, quantified and time-boxed ("SSO sign-in success below 95% over
  15 minutes"), never "if things look bad". Agree them at the go/no-go, not on the bridge.
- **Authority:** the cutover lead may call a rollback against an agreed trigger without
  escalation; the approver is informed, not asked. Anything outside the triggers is escalated.
- **Point of no return (PONR):** the step after which rollback loses data or breaks a commitment
  (users have transacted in a migrated system; the legacy contract is cancelled). Push it as
  late as possible and put a go-live checkpoint immediately before it.
- **Last safe rollback start** = window end − rehearsed full rollback duration. Hold a
  rollback-window checkpoint at least 30 minutes before it. A rollback that cannot finish
  inside the window is a second outage.
- **Fix forward instead** only when the cause is known, the fix is small and tested, and it
  lands before the last safe rollback start. Otherwise roll back and fix in daylight.
- **Partial rollback:** flags let you withdraw one capability. If that changes committed scope
  (Helios GA without SSO), the scope decision goes back to the approver.
- **Rehearse it.** An untested rollback is a hope: time it in the dress rehearsal and restore
  from the real backup at least once.
- **After a rollback:** reconcile any data created in the new system, communicate, log an issue
  in the `project-delivery` issue log, hold a blameless review and return to go/no-go with a
  new date.

## Helios GA numbers
Window Saturday 2026-10-03 06:00-12:00, go-live (T0) 09:00. The full rollback (R1 → R5 → R6 in
`assets/cutover-runbook-sample.csv`) is budgeted at 75 minutes and rehearsed at 70, so the last
safe rollback start is 10:45 and the rollback-window checkpoint is at 10:00. Triggers: any
severity-1 defect not fixed within 30 minutes; SSO sign-in success below 95% over 15 minutes
with at least 20 attempts; error rate above 1% or p95 page load above 4 seconds for 10 minutes;
a data-integrity mismatch after migration; the runbook more than 45 minutes late at the go-live
checkpoint.
