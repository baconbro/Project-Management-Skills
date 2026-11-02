---
name: project-closure
description: >-
  Closes a project or phase, including a cancelled one: formal acceptance, handover to
  operations, open items and contracts, final cost, post-project review, team release and
  closure report. Use when the work is done and needs sign-off and handover, or when a
  project is being stopped early.
metadata:
  version: 1.1.0
  category: phase
  phase: closure
  related: [senior-pm, project-delivery, lessons-learned, business-case, release-and-cutover, procurement-management]
license: MIT
---

# Project Closure

## Overview
Closure is the disciplined end of a project or phase: a real "yes" from the people who asked
for the work, a named person signed for the product and for each benefit, an explicit
disposition for every open issue, risk, defect, contract and access right, reconciled money
and closed cost codes, lessons captured while the team is still reachable, and a signed
closure report. An unclosed project keeps consuming budget and attention, and nobody owns the
benefits the business case promised. Closure is also how a project that should stop *does*
stop: a well-run premature closure is governance working, not failure. The examples use the
sample Helios project (a fictional customer self-service portal used throughout this catalog),
which went live on 2026-10-03, left hypercare on 2026-10-30 and was closed by its sponsor,
Dana Okoro (VP Customer Operations), on 2026-11-20.

## When to use this skill
- The work is built (or the last release is live) and the project or phase must be formally
  accepted, handed over and closed.
- The user needs final sign-off, a closure report, a post-project review or a benefits
  handover, or must release the team.
- The project is being cancelled or stopped early and must be wound down properly.
- A project "finished" months ago but still has open cost codes, unsigned acceptance, live
  vendor access or no benefits owner.
- Do NOT use this while deliverables are still being built — stay in `project-delivery`.
- Do NOT use this to plan the go-live, run the go/no-go or decide when hypercare ends — use
  `release-and-cutover` instead; this skill takes its exit record as handover evidence.
- Do NOT use this to close a single vendor contract — use `procurement-management` instead.
- Do NOT use this to run only a retrospective — use `lessons-learned` instead.
- Do NOT use this to decide whether a troubled project is still worth doing — use
  `business-case` to re-appraise it, then come back here if the sponsor decides to stop.

## Methodology fit
- **Waterfall:** final acceptance against the scope statement at the last stage gate, a
  phase-end report at every earlier gate (the phase path below), contracts closed against
  their statements of work, and a closure report signed by the sponsor.
- **Agile:** increments were accepted at sprint reviews, so closure confirms the final
  release, widens the last retrospective into a post-project review, and hands the remaining
  backlog to a continuing product owner instead of deleting it. A stable product team may
  stay together: "release the team" then means moving its funding and reporting line.
- **Hybrid:** formal acceptance and financial closure at the top, sprint acceptance
  underneath. Helios: Ava Chen accepted increments at sprint reviews, named acceptors signed
  deliverables in the scope statement's acceptance log, Dana Okoro gave final acceptance
  after the 100% ramp, and the phase-2 backlog passed to Ava Chen as product owner.

## Inputs you need
- Deliverables with acceptance criteria and acceptors: ideally the scope statement and
  acceptance log from `scope-and-requirements`, or the definition of done and gate criteria
  from `quality-management`. If none were ever written, step 1 agrees them now.
- If there was a go-live: hypercare exited and operations acceptance signed, that is the
  hypercare exit record and the operations owner's signed acceptance from
  `release-and-cutover`.
- The acceptance log, issue log, risk register, change log and open defects from
  `project-delivery`; the
  cost baseline, actuals and reserve drawdown from `cost-management`; the contract register
  from `procurement-management`.
- The benefits register from `business-case`. With no business case, step 5 derives benefits
  from the charter objectives and records unquantified ones qualitatively.
- The lessons log so far, the team list, and the archive location and retention rules.

If work is still being built, stay in `project-delivery`; obtaining formal acceptance is
step 1 of this skill. If the product is live but hypercare is still running, finish it in
`release-and-cutover` (steps 3-4 can be prepared meanwhile). Missing acceptance criteria or a
missing business case are not blockers: steps 1 and 5 have fallbacks.

## Workflow
Pick the closure path first and record it in the closure report header:
- **Completed project:** run steps 1-8.
- **Phase or stage:** run steps 1, 3, 4, 6 and 8 at phase scope and attach the phase-end
  report to the gate decision; steps 2, 5 and 7 cover only what the phase handed over.
- **Cancelled or stopped early:** follow `references/premature-closure.md`. Step 1 becomes
  the sponsor's signed termination decision plus acceptance of the salvaged work; steps 2-8
  run on what remains, with the result `stopped early`.

1. **Obtain formal acceptance.** Take the criteria from the first source that exists, in the
   order in `references/acceptance-at-closure.md`: scope statement, definition of done and
   gate criteria, a contract's statement of work, the charter. If none were ever agreed,
   agree acceptance with the sponsor now: two to five checklist-style, pass/fail criteria per
   deliverable from the charter's success criteria (or the original request), agreed in
   writing *before* anyone judges the evidence. Acceptances already logged during delivery
   count; get a decision on each remaining deliverable (accept, accept with conditions,
   reject), then the sponsor's final acceptance, in the scope statement's acceptance log or a
   copy of `assets/acceptance-record-template.md`; silence is not acceptance. Helios: D2-D10
   were signed by their acceptors during delivery, and Dana Okoro accepted the product on
   2026-10-14 on one condition, that Priya Nair accept D11 Operational handover at hypercare
   exit. *Done: a
   signed decision (or termination) covers every deliverable, and every condition has an
   owner and a date.*
2. **Confirm the handover to operations.** For a live service, check the hypercare exit
   record from `release-and-cutover`: every exit criterion met with evidence, operations
   owner's signature present; if hypercare has not exited, stop and finish it there. Then
   hand over what hypercare does not cover (product backlog, documentation, licences,
   knowledge, measurement tooling) to named owners, using the handover items in
   `references/closure-checklist.md`, and record them in section 4 of
   `assets/closure-report.md`. With no go-live, the receiving owner signs here. Helios:
   Priya Nair (Head of Support Operations) signed the service on 2026-10-30. *Done: a named
   receiving owner has signed for every product, service and support item.*
3. **Dispose of every open item.** Copy `assets/closeout-log-template.csv` and list every open
   condition, defect, issue, action, risk, undecided change request, contract, access right
   and record. Give each one a disposition: closed, transferred (receiving owner agreed),
   accepted as residual by the sponsor, or cancelled. Close each contract through
   `procurement-management` and log the result. `assets/closeout-log-sample.csv` is the
   Helios log: 22 rows, including the IdentityCo services contract closed with the $880 delay
   credit applied and the $2,200 retention released after the warranty. *Done: no row is
   open, and every transferred row names a receiving owner who agreed and a date.*
4. **Close the finances.** Reconcile final actual cost to the `cost-management` baseline,
   explain the variance and each contingency and management-reserve draw, accrue late
   invoices, close purchase orders, return unused budget and have Finance close the cost
   codes, following the financial items in `references/closure-checklist.md`. Helios:
   $518,600 against BAC $500,000 (−3.7%); contingency fully used; $18,600 of the $25,000
   management reserve drawn through change control, $6,400 returned. *Done: final cost is
   reconciled and explained, no commitment is open, and the cost codes are closed.*
5. **Hand over benefits tracking.** Copy each benefit and dis-benefit from the
   `business-case` register into section 7 of `assets/closure-report.md` with measure,
   baseline, target, owner, review dates and the forum that will receive the reviews, plus
   the first leading-measure readings (`references/benefits-realization.md`). Each owner was
   named in the business case and confirmed at the initiation gate (G0 in
   `project-initiation`): confirm here that they accept accountability in writing, and name
   an owner only for a benefit the case left without one. With no business case, derive
   benefits from the charter objectives; record any you cannot quantify qualitatively, with
   an observable sign and a first review date. Helios: Priya
   Nair owns the 50% cut in the two ticket types (October: −22% against 5,000 a month),
   reviewed in January and April 2027. *Done: every benefit has an owner who accepted it in
   writing, a measure, a baseline or a stated absence, a target and review dates.*
6. **Run the post-project review.** While the team can still attend, review delivery against
   the baseline and the benefits so far, then capture and route lessons with
   `lessons-learned`; summarise the top ones in section 8 of `assets/closure-report.md`.
   Helios: the review on 2026-11-04 confirmed LL001-LL007; LL001 (vendor onboarding owner)
   and LL007 (training a week before launch) went into the PMO's standard plan. *Done:
   lessons have owners and statuses, and each top lesson has a named destination.*
7. **Release the team and archive.** Release each person on a stated date with feedback to
   their line manager (plan releases with `resource-management`), revoke project access,
   archive records and logs under the retention rules, and tell stakeholders through
   `project-communication`, using the administrative items in
   `references/closure-checklist.md`. *Done: everyone has a release date, access is revoked,
   and the archive location is recorded.*
8. **Issue the closure report and get it signed.** Fill `assets/closure-report.md`, compare it
   with `assets/closure-report-sample.md` (the Helios report), walk
   `references/closure-checklist.md` once more and route it to the sponsor. The signature
   closes the project: no further charges, decisions or change requests. *Done: the sponsor
   has signed the closure report, and the closure is announced.*

## Quality checklist
- [ ] The closure path (completed, phase, stopped early) is in the report header.
- [ ] Every deliverable has a signed accept, accept-with-conditions or reject decision against
      criteria agreed before the evidence was judged; none was accepted by silence.
- [ ] For a live service, the hypercare exit record and the operations owner's signature are
      attached; every other handover item has a named receiving owner who signed.
- [ ] No closeout-log row is open; every condition and transferred item names an owner who
      agreed and a date.
- [ ] Every contract is closed or transferred through `procurement-management`, with
      retention, credits, access and data settled.
- [ ] Final cost is reconciled, variance and reserve draws are explained, and Finance has
      confirmed the cost codes are closed.
- [ ] Every benefit has an owner who accepted it, a measure, a baseline (or stated absence), a
      target, review dates and a forum that outlives the project.
- [ ] The post-project review was held while the team could attend (anyone released earlier
      was invited back), and each top lesson has an owner and a destination.
- [ ] For a stopped project: termination reason, decider and date, salvage decisions and
      outstanding obligations are recorded and signed.
- [ ] The closure report has no placeholder left and is signed by the sponsor.

## Anti-patterns
- "Closing" by stopping work: open cost codes, unpaid invoices, live vendor access, no sign-off.
- Bouncing between "not accepted, go back to delivery" and "delivery is finished": final
  acceptance, and any acceptance still missing, is obtained here in step 1.
- Writing or tightening acceptance criteria after seeing the result.
- Using benefits as acceptance criteria ("accept when tickets fall 50%"): benefits arrive
  months later and belong to the benefits owner.
- "Conditions" that are really unfinished scope with no owner or date.
- Handing over to "operations" or "the business" instead of a named person who signed.
- Closing before hypercare has exited on its criteria, so defects have nowhere to go.
- Keeping a doomed project alive for sunk cost, or stopping it with no termination record,
  salvage review or contract notice.
- Skipping the post-project review because the team has already moved on.

## Resources
- `references/acceptance-at-closure.md` — criteria sources in order, agreeing criteria with
  the sponsor when none exist, the decision, conditions, stalled acceptance, Helios example.
- `references/premature-closure.md` — stopping early: who decides, the termination record,
  salvage, contracts and obligations, how steps 2-8 change, a hypothetical Helios stop.
- `references/closure-checklist.md` — walk-through checklist by path and area: acceptance,
  handover, open items, contracts, finances, benefits, lessons, team, records.
- `references/benefits-realization.md` — output to benefit, the handover with or without a
  business case, reviews after closure, the Helios benefits table.
- `assets/acceptance-record-template.md` — fill-in acceptance record (`<placeholders>`):
  criteria and source, decisions, conditions, termination confirmation, signatures.
- `assets/closeout-log-template.csv` — fill-in closeout log (`<placeholders>`); columns `id,
  item_type, source_ref, description, current_owner, disposition, receiving_owner,
  receiver_agreed, due, status, evidence`.
- `assets/closeout-log-sample.csv` — sample: the Helios closeout log at closure, 22 rows.
- `assets/closure-report.md` — fill-in closure report (`<placeholders>`) for all three paths.
- `assets/closure-report-sample.md` — sample: the Helios closure report signed on 2026-11-20.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `senior-pm` — routes here when work is built, the release is live or work is stopping, and
  marks the project closed in its project-state canvas once the report is signed.
- `project-delivery` — keeps the project while work is still being built, accepts finished
  deliverables one by one, and hands over the acceptance log (step 1's evidence) and the
  issue log, risk register, change log and actuals that steps 3 and 4 dispose of; final
  acceptance, and any acceptance still missing, is obtained here.
- `lessons-learned` — runs the post-project review format and keeps the lessons log with
  owners (step 6); this skill makes sure the review happens before the team disperses.
- `business-case` — supplies the benefits register that step 5 hands over; a re-appraisal
  there that no longer justifies the project is the usual trigger for a stopped-early closure.
- `release-and-cutover` — owns go-live and hypercare; its exit record and the operations
  owner's signed acceptance are the evidence step 2 confirms.
- `procurement-management` — closes each contract (acceptance, payment, credits, retention,
  access, data, vendor review) or applies its termination terms, and reports the result into
  the closeout log in step 3.
