# Definition of Done — sample (Helios v1.2)

Sample: a completed Definition of Done for the sample Helios project (a fictional customer
self-service portal used throughout this catalog), built from `definition-of-done.md`. It is
version 1.2, agreed after process audit QA-03 (see `quality-audit-log-sample.csv`). Do not copy
the Helios values; copy the template and set your own.

| Field | Value |
|---|---|
| Project | Helios customer self-service portal |
| Version / date | v1.2 / 2026-07-16 |
| Agreed by | Ben Adeyemi, Carla Diaz, Devin Patel, Elena Rossi, Frank Müller; Ava Chen (product owner) |
| Applies to | Every story and task in the product backlog, and every document deliverable in WBS 1.5 |
| Verified by | Frank Müller (QA engineer), or another engineer who did not build the item |

An item is **Done** when every line below is true. An item that fails any line is **not done**:
it is not presented at the sprint review, it fails gate G0 and returns to the product backlog,
and it counts toward neither velocity nor earned value.

## Build and review
- [ ] Merged to `main` and builds cleanly in the Helios CI pipeline.
- [ ] Peer-reviewed and approved by at least one engineer who did not write it (branch
      protection enforces this since audit QA-02).
- [ ] Linters and the front-end style guide pass with no new warnings.
- [ ] No debug output, commented-out code or unresolved to-do notes left for this item.

## Test
- [ ] Unit tests written and passing; coverage of changed code at least 80%.
- [ ] API tests and the automated regression suite for the reset and order-status journeys
      (HEL-153) pass for every affected path.
- [ ] Every acceptance criterion verified by Frank Müller or another engineer who did not build
      it, against the real identity provider wherever sign-in is involved (stub results are not
      acceptance evidence), with its test id recorded on the story.
- [ ] No open severity-1 or severity-2 defect against the item; any open severity-3 has a
      logged workaround and a fix date.

## Non-functional
- [ ] 95% of pages in the item's journey load within 2 seconds in the test environment (the full
      peak-load test, HEL-150, is a gate G4 criterion).
- [ ] WCAG 2.2 AA automated scan passes as a blocking pipeline step (added in v1.2); keyboard-only
      and screen-reader check done by Elena Rossi for any new or changed UI (CR003).
- [ ] Dependency and static security scans show no new high or critical finding.
- [ ] Any new store or flow of customer personal data stays in the approved data-residency region
      (Hana Sato's data-residency policy, REQ-007).

## Documentation and release
- [ ] Help-centre article or release note updated for any user-facing change.
- [ ] Runbook and alerts updated if behaviour or configuration changed (HEL-155).
- [ ] Deployed to staging, and Ava Chen has seen it working before the sprint review.

## Version history
| Version | Date | Change | Reason |
|---|---|---|---|
| v1.0 | 2026-05-08 | First agreed version, accessibility at WCAG 2.1 AA | Gate G1 at M1 |
| v1.1 | 2026-07-01 | Accessibility raised to WCAG 2.2 AA; keyboard and screen-reader check added | CR003 approved by the CCB on 2026-06-30 |
| v1.2 | 2026-07-16 | WCAG 2.2 AA scan made a blocking pipeline step; "an item failing any line is not done" made explicit; real identity provider required for sign-in evidence | Audit QA-03: two contrast defects (DEF-003, DEF-004) reached the sprint S4 review and were accepted with conditions (ACT005); audit QA-04 on stub evidence |
