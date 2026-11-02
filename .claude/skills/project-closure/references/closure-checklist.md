# Closure checklist — leave nothing open

Load this to walk a closure from start to finish, and once more before the sponsor signs the
closure report. Mark every item done, or not applicable with a one-line reason. File paths are
relative to this skill's folder. Examples use the sample Helios project (a fictional customer
self-service portal used throughout this catalog).

## Closure path
- [ ] The path is chosen and recorded in the closure report header: completed project, phase
  or stage closure, or stopped early.
- [ ] Phase closure: the phase-end report is attached to the gate decision, and only the
  items the phase handed over, started realising or released are closed here.
- [ ] Stopped early: work through `references/premature-closure.md` alongside this list.

## Acceptance and sign-off (step 1)
- [ ] The source of the acceptance criteria is recorded (scope statement, definition of done
  or gate criteria, contract statement of work, charter, or agreed at closure).
- [ ] If no criteria existed, checklist-style criteria were agreed with the sponsor in
  writing before the evidence was judged (`references/acceptance-at-closure.md`).
- [ ] Every in-scope deliverable is accepted, accepted with conditions, or rejected with
  the failed criterion named; requirements not built are formally deferred, not forgotten.
- [ ] Each deliverable's evidence (tests, UAT, audits, the hypercare exit record) is attached.
- [ ] Every condition and known exception is in the closeout log with an owner and a date.
- [ ] The sponsor has signed final acceptance (scope statement acceptance log, or Part D of
  `assets/acceptance-record-template.md`).
- [ ] For a cancelled project: the termination reason, decider and date, the salvage
  decisions and the outstanding obligations are recorded and signed off (Part T).

## Handover to operations and the benefits owner (step 2)
- [ ] If there was a go-live: hypercare has exited on its criteria and the operations owner
  has signed the exit record (run in `release-and-cutover`; closure only checks it).
- [ ] The product, environments, access and support arrangements are transferred to a named
  run owner who signed.
- [ ] Runbooks, operational documentation and known-error articles are current.
- [ ] The remaining product backlog and roadmap have a named product owner.
- [ ] Licences, subscriptions and warranties have an operational owner.
- [ ] Knowledge transfer or training for the receiving team is complete.

## Open items (step 3)
- [ ] Every open issue, action, defect, risk, undecided change request, contract, access
  right and record is a row in a copy of `assets/closeout-log-template.csv`.
- [ ] Each row has one disposition: closed, transferred, accepted as residual, or cancelled.
- [ ] Every transferred row names a receiving owner who agreed, with a date.
- [ ] Residual risks and known exceptions are accepted by the sponsor in writing.
- [ ] Undecided change requests are passed to a named decider (for example the next phase's
  backlog), not left "under assessment".

## Contracts (step 3, run through `procurement-management`)
- [ ] Every deliverable from each vendor is accepted, or open items are settled in writing.
- [ ] Final invoices match accepted deliverables; credits applied; retention released when
  the warranty ends.
- [ ] Vendor access is revoked and data returned or its deletion certified.
- [ ] Contracts that continue (subscriptions, hosting) are transferred to an operational owner.
- [ ] A vendor performance review is written and the closed contract is a closeout-log row.

## Financial closure (step 4)
- [ ] Final actual cost is reconciled to the cost baseline from `cost-management`; the
  variance is explained.
- [ ] Contingency and management-reserve drawdowns are listed with their approvals.
- [ ] Late invoices are accrued; purchase orders and commitments are closed.
- [ ] Unused budget and reserve are returned to the budget holder.
- [ ] Finance has closed the cost codes to new charges.

## Benefits (step 5)
- [ ] Every benefit and dis-benefit is listed with measure, baseline, target, owner, review
  dates and the forum that will receive the reviews (`references/benefits-realization.md`).
- [ ] Each benefit owner has accepted ownership in writing.
- [ ] Where there was no business case, benefits were derived from the charter objectives,
  and unquantified ones are recorded qualitatively with a first review date.

## Lessons, team and records (steps 6-7)
- [ ] The post-project review was held while the team could still attend (anyone released
  earlier was invited back); lessons are in the log in `lessons-learned` with owners, and
  the top ones have a destination.
- [ ] Each team member has a release date, and their line manager has received feedback.
- [ ] Project access (repositories, consoles, shared drives) is revoked or transferred.
- [ ] Records, decisions, logs and the acceptance record are archived in a findable place
  with the retention period stated.
- [ ] Stakeholders are told the project is closing and who to contact from now on
  (`project-communication`).

## Closure report (step 8)
- [ ] `assets/closure-report.md` is complete, with no `<placeholder>` left.
- [ ] The sponsor has signed it, and the closure is announced.

## Common gaps caught here
- A go-live celebrated while invoices, retention and vendor access stay open for months.
- A handover with documentation but no named person who signed to run the product.
- Change requests left "under assessment" forever because nobody owns them after closure.
- Cost codes left open, so other work is quietly charged to the closed project.
- Lessons "discussed" but never recorded or routed for reuse.
- The project closed with no forum and no dates for checking whether the benefits arrive.
