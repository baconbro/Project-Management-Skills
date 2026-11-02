# Definition of Done — fill-in template

The Definition of Done (DoD) is the shared, cross-cutting bar that *every* work item must clear
before it counts as complete, whichever feature it belongs to. It complements per-item
acceptance criteria: an item is done only when it meets both its acceptance criteria **and**
this DoD. Copy this file, replace every `<placeholder>`, delete lines that do not apply, then
have the whole team and the product owner agree it and post it where the work happens.
`definition-of-done-sample.md` shows a completed version for the sample Helios project.

| Field | Value |
|---|---|
| Project | `<project name>` |
| Version / date | `<v1.0>` / `<YYYY-MM-DD>` |
| Agreed by | `<team members>`; `<product owner>` |
| Applies to | `<stories / tasks / documents / every item that can be called done>` |
| Verified by | `<role who checks the DoD - not the person who built the item>` |

An item is **Done** when every line below is true. An item that fails any line is **not done**:
it is not presented at the sprint review or gate, it returns to the backlog, and it counts toward
neither velocity nor earned value.

## Build and review
- [ ] Merged to `<main branch>` and builds cleanly in `<pipeline name>`.
- [ ] Peer-reviewed and approved by at least `<n>` person(s) who did not write it.
- [ ] `<coding standard / linter / style guide>` passes with no new warnings.
- [ ] No debug output, commented-out code or unresolved to-do notes left for this item.

## Test
- [ ] Unit tests written and passing; coverage of changed code at least `<n>`%.
- [ ] `<integration / API / regression suite>` passing for every affected path.
- [ ] Every acceptance criterion verified by `<role who did not build it>`, with its test id
      recorded against the item.
- [ ] No open severity-1 or severity-2 defect against the item; any open severity-3 has a
      logged workaround and a fix date.

## Non-functional
- [ ] `<performance budget - e.g. 95% of pages in the journey load within n seconds in the test environment>`.
- [ ] `<accessibility standard>` automated scan passes as a blocking pipeline step; manual
      `<keyboard / screen-reader>` check done for any new or changed UI.
- [ ] `<security scan>` shows no new high or critical finding.
- [ ] Privacy review done where personal data is touched (`<policy name>`).

## Documentation and release
- [ ] User-facing help or release notes updated.
- [ ] Runbook, alerts and operational notes updated if behaviour or configuration changed.
- [ ] Deployed to `<environment>`, and the product owner has seen it working before the
      `<sprint review / gate>`.

## Version history
| Version | Date | Change | Reason (audit finding, change request, retrospective) |
|---|---|---|---|
| `<v1.0>` | `<YYYY-MM-DD>` | First agreed version | `<planning / kickoff>` |

## Rules for using it
- Every line must be checkable by someone other than the author from evidence (a pipeline run,
  a checklist, a report). "Code is clean" is not a DoD line; "linter passes with no new
  warnings" is.
- The DoD is the gate for every item. In Scrum it is applied *before* the Sprint Review: the
  review inspects done work with stakeholders, it does not decide whether work is done.
- The DoD is not negotiable per item under deadline pressure. If an item cannot meet it, the
  item is not done: return it to the backlog or escalate the gate failure; never "accept it
  with conditions" as done.
- Review it at every retrospective or phase end. Add a line when an escaped defect or an audit
  finding shows a gap; remove a line that no longer earns its keep. Record each change in the
  version history.
- Universal non-functional rules (accessibility, security scans) belong here; item-specific
  thresholds belong in that item's acceptance criteria; whole-release checks (full load test,
  penetration retest) belong in a gate's exit criteria.
- For stage, milestone and release completeness, pair the DoD with the exit criteria of the
  relevant quality gate (`references/quality-gates.md` in the `quality-management` skill).
