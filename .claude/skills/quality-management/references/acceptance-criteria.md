# Writing Acceptance Criteria

Acceptance criteria are the testable conditions a deliverable must satisfy to be accepted.
Good criteria are written *before* the work, are objective enough that two reviewers reach the
same verdict, and trace to a real stakeholder need. They turn "is it done?" from an opinion
into a check.

## Two common styles

### 1. Given / When / Then (scenario style)
Best for behaviour — a user does something and expects a result. One scenario per rule.

```
Scenario: Customer resets a forgotten password
  Given a registered Helios customer on the login page
  When they request a password reset for a valid email
  Then a reset link is sent within 60 seconds
  And the link expires after 30 minutes
```

Strengths: unambiguous, maps directly to a test, captures edge cases as extra scenarios
(invalid email, expired link). Use it for user-facing behaviour and APIs.

### 2. Checklist / rule style
Best for deliverables that are not a single behaviour — a document, a config, a report.

```
The Helios analytics dashboard is accepted when:
  [ ] Shows ticket-deflection rate, refreshed at least hourly
  [ ] Loads in under 2 seconds on the standard test dataset
  [ ] Passes WCAG 2.1 AA contrast checks
  [ ] Figures reconcile with the source data warehouse to the cent
```

## Making criteria measurable
Replace adjectives with thresholds. Every criterion should answer "how would I test this?"

| Weak (un-testable)        | Strong (testable)                                   |
|---------------------------|-----------------------------------------------------|
| "fast"                    | "responds in < 500 ms at the 95th percentile"       |
| "user-friendly"           | "a new user completes signup in < 3 minutes unaided"|
| "secure"                  | "passes the OWASP top-10 scan with no high findings"|
| "handles load"            | "serves 500 concurrent users with < 1% error rate"  |

## INVEST-style quality checks for a criterion
- **Specific:** names the exact condition, not a category.
- **Measurable:** has a number, a state, or a clear yes/no.
- **Independent of solution:** says *what*, not *how to build it*.
- **Verifiable:** someone other than the author can confirm it.

## Acceptance criteria vs Definition of Done
- **Acceptance criteria** are *per deliverable* — specific to this feature/document.
- **Definition of Done** is *cross-cutting* — the bar *every* item clears regardless of feature
  (tested, reviewed, documented). See `assets/definition-of-done.md`.
A deliverable is releasable only when it meets *both* its acceptance criteria and the DoD.
