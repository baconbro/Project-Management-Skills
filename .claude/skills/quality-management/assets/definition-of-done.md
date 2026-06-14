# Definition of Done (template)

The Definition of Done (DoD) is the shared, cross-cutting bar that *every* work item must clear
before it counts as complete — independent of which feature it belongs to. It complements
per-deliverable acceptance criteria: an item ships only when it meets both its acceptance
criteria **and** this DoD. Adapt the lists below, then have the whole team agree and post it
where work happens.

## Project: Helios customer self-service portal

A work item (story, task, or deliverable) is **Done** when:

### Build & code
- [ ] Code complete and merged to the main branch (no long-lived feature branches).
- [ ] Peer-reviewed and approved by at least one other engineer.
- [ ] Coding standards and linters pass with no new warnings.
- [ ] No commented-out code, debug logs, or TODOs left for this item.

### Test
- [ ] Unit tests written and passing; coverage does not drop below the agreed target.
- [ ] Integration / API tests passing for affected paths.
- [ ] All acceptance criteria for the item demonstrably pass.
- [ ] No open critical or high-severity defects against the item.

### Non-functional
- [ ] Meets the performance budget (e.g. p95 response < 500 ms).
- [ ] Meets accessibility standard (WCAG 2.1 AA) for any UI.
- [ ] Security checks pass (no new high findings in the scan).
- [ ] Privacy reviewed where personal data is touched.

### Documentation & release
- [ ] User-facing changes documented (release notes / help content updated).
- [ ] Runbook / operational notes updated if behaviour or config changed.
- [ ] Demonstrated to and accepted by the product owner.

## How to use it
- Keep it short enough to remember and strict enough to mean something.
- Review it each iteration / phase — add items when escaped defects reveal a gap; remove items
  that no longer earn their keep.
- The DoD is *not* negotiable per item under deadline pressure; if an item cannot meet it, that
  is a gate failure to escalate, not a corner to cut silently.
- For phase-level or release-level completeness, pair this with the exit criteria of the relevant
  quality gate (`references/quality-gates.md`).
