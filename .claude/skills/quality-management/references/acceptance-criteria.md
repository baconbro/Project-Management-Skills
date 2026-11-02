# Writing Acceptance Criteria

Acceptance criteria are the testable conditions a deliverable or story must satisfy to be
accepted. Good criteria are written *before* the work starts, are objective enough that two
reviewers reach the same verdict, and trace to a real stakeholder need. They turn "is it
done?" from an opinion into a check. Examples come from the sample Helios project (a fictional
customer self-service portal used throughout this catalog); requirement ids (REQ-nnn) and test
ids (UAT-nn) match its RTM in `scope-and-requirements`.

## Who writes them, who sets the standard
| Level | Where the criteria are captured | Skill that captures them | What this skill does |
|---|---|---|---|
| Requirement | RTM `acceptance_test` column (test id + pass condition) | `scope-and-requirements` | Sets the format and reviews each Must for testability |
| Deliverable | Scope statement, "Deliverables and acceptance criteria" | `scope-and-requirements` | Same, and turns them into gate exit criteria |
| Work package | WBS dictionary, `acceptance criterion` column | `work-breakdown-structure` | Checks it is verifiable and matches the deliverable |
| User story | Product backlog, Given/When/Then | `agile-delivery` | Sets the standard; the DoD sits on top of every story |

This skill owns the *standard* and the *review*; it does not invent requirements. When a
criterion fails the checks below, send it back to its owner with the reason rather than
rewriting it alone; the acceptor must recognise the criterion they will sign against.

## Two styles

### 1. Given / When / Then (scenario style)
Best for behaviour: a user or system does something and expects a result. One scenario per
rule; add the unhappy paths as extra scenarios.

```
Scenario: Customer resets a forgotten password            (Helios REQ-001, test UAT-01)
  Given a registered customer on the sign-in page
  When they request a password reset for their registered e-mail address
  Then a reset link is e-mailed within 60 seconds
  And the link expires 30 minutes after it was sent

Scenario: Reset requested for an unknown e-mail address   (unhappy path)
  Given a visitor on the sign-in page
  When they request a reset for an address that is not registered
  Then the page shows the same confirmation message as for a registered address
  And no e-mail is sent
```

For one rule tested over many data values, use a scenario outline with an examples table
(for Helios REQ-002, one row per order state: placed, picked, shipped, delivered, cancelled)
instead of copying the scenario five times.

Strengths: unambiguous, maps directly to an automated or manual test, and makes edge cases
visible. Use it for user-facing behaviour and APIs. Three to seven scenarios per story is
typical; more usually means the story should be split (`agile-delivery`).

### 2. Checklist / rule style
Best for deliverables that are not a single behaviour: a document, a configuration, a report,
a dataset, a runbook.

```
The Helios weekly deflection report (REQ-005, test UAT-05) is accepted when:
  [ ] It shows password-reset and order-status ticket volumes per week against the
      3-month pre-launch baseline
  [ ] The figures for a closed month reconcile exactly with the ticketing system's own counts
      per ticket type
  [ ] It is available to Support Operations by 09:00 every Monday
  [ ] It passes the WCAG 2.2 AA automated scan (REQ-006, raised from 2.1 AA by CR003)
```

## Making criteria measurable
Replace adjectives with thresholds. Every criterion should answer "how would I test this, and
what result fails it?"

| Weak (untestable) | Strong (testable) |
|---|---|
| "fast" | "95% of pages load within 2 seconds at the forecast launch peak" |
| "user-friendly" | "9 of 10 pilot users finish a password reset unaided in under 3 minutes" |
| "secure" | "a penetration retest shows no open high or critical finding" |
| "accessible" | "an independent WCAG 2.2 AA audit reports no failures" |
| "handles load" | "serves 500 concurrent users for 30 minutes with an error rate under 0.1%" |
| "accurate" | "for 20 test orders covering every state, the portal shows the same status as the order system" |

## SMART-style checks for a criterion
Run every Must's criterion through these five checks before the work is planned:
- **Specific:** names one exact condition, not a category ("reset link e-mailed", not "reset works").
- **Measurable:** has a number, a state or a clear yes/no, with the unit and the conditions
  of measurement (load, device, data set).
- **Achievable:** can be tested with the environments, data and tools the project actually
  has; "zero defects ever" or a test that needs production data you cannot get fails here.
- **Relevant:** traces to a requirement id or stakeholder need in the RTM; a criterion with no
  source is gold-plating.
- **Time-bound:** says when it is verified (DoD check, system test, UAT, a named gate) and, for
  anything time-based, the time limit itself (60 seconds, 30 minutes).

Two further checks catch most remaining problems:
- **Solution-free:** says *what* must be true, not *how* to build it ("the error is announced to
  screen readers", not "use an ARIA live region").
- **Independently verifiable:** someone other than the author can run the check and reach the
  same verdict.

INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable) is a different checklist:
it applies to the *user story* the criteria hang off, not to the criteria. Story writing and
splitting live in `agile-delivery`.

## Non-functional criteria: in the story or in the DoD?
- **In the acceptance criteria** when the threshold is specific to that item (Helios HEL-150:
  95% of pages within 2 seconds at the forecast peak, tested once in the load test).
- **In the Definition of Done** when it applies to every item (Helios: every page passes the
  WCAG 2.2 AA automated scan).
- **In a gate's exit criteria** when it can only be shown for the whole release (full load
  test, penetration retest, independent accessibility audit).

## Acceptance criteria, Definition of Done, acceptance
- **Acceptance criteria** are *per item*: specific to this feature, document or deliverable.
- **Definition of Done** is *cross-cutting*: the bar every item clears regardless of feature
  (reviewed, tested, accessible, documented). See `assets/definition-of-done.md`.
- **Verification** (quality control) shows that both are met; **acceptance** (scope
  validation) is the named acceptor's decision to take the deliverable, recorded in
  `scope-and-requirements`. A passed test is not acceptance, and silence is not acceptance.

An item is ready for acceptance only when it meets *both* its acceptance criteria and the DoD.

## Reviewing a set of criteria (quick checklist)
- [ ] Every Must requirement and every committed story has at least one criterion.
- [ ] Each criterion passes the five SMART-style checks and the two further checks.
- [ ] Each behaviour has at least one unhappy-path scenario (invalid input, timeout, provider failure).
- [ ] Each criterion has a test id (UAT-nn, SIT-nn, ACC-nn, SEC-nn) recorded in the RTM or backlog.
- [ ] Time-outs and data freshness are stated wherever a session or a feed is involved
      (Helios learned this from two pilot escapes; see the audit log sample QA-05).
