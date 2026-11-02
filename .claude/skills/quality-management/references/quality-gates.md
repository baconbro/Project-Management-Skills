# Quality Gates and the Cost of Quality

A quality gate is a checkpoint where work must meet defined criteria before it may proceed.
Gates make quality a *decision* with an owner, not something that quietly erodes under
schedule pressure. Each gate has **entry criteria** (what must be true to start the review)
and **exit criteria** (what must be true to pass). This reference also covers how strict to
make the gates (the cost of quality) and how to keep quality apart from grade. Examples come
from the sample Helios project (a fictional customer self-service portal used throughout this
catalog).

## Entry and exit criteria

```
        entry criteria met            exit criteria met
  Work ───────────────────►  GATE  ───────────────────►  Next stage / release
                              │
                              └── not met ──► rework and re-review, or an explicit waiver
```

- **Entry criteria:** preconditions for the review to happen at all, e.g. "pilot-scope stories
  done; system and regression tests executed; UAT testers booked". Failing entry means the
  gate is not ready: do not convene it.
- **Exit criteria:** the pass conditions, e.g. "zero open severity-1/2 defects; every UAT
  script passed; accessibility audit shows no failures". Failing exit means rework or an
  explicit waiver decision.

Write exit criteria as *threshold + evidence source*: "zero open severity-1/2 defects in the
defect log at 12:00 on the gate day", not "testing complete" or "quality acceptable".

## Gate levels
| Level | When | Typical exit criteria | Who decides |
|---|---|---|---|
| Item | Every story or task, continuously | The Definition of Done | The team; QC verifies, the product owner accepts the story |
| Stage | Between test stages (ready for system test, ready for UAT, UAT exit) | Stage tests passed; open defects within the severity rule | QC lead; the UAT acceptor for UAT exit |
| Milestone / phase | End of a phase or before a milestone (requirements baseline, pilot, general availability) | All stage gates passed; non-functional floors met; evidence complete | Named approver per gate (PM or sponsor) |
| Release readiness | Days before go-live | The go/no-go criteria across every workstream | The go/no-go approver, run by `release-and-cutover` |

Quality management owns the first three levels. The release-readiness decision belongs to
`release-and-cutover`, which reuses the last quality gate's evidence (open defects by
severity, UAT sign-off, performance, security, accessibility) as its test-readiness criteria
instead of inventing new thresholds.

## By methodology
- **Waterfall:** phase-end gates with formal entry and exit criteria, a review meeting and a
  signed decision; stage gates between test levels.
- **Agile:** the recurring gate is the **Definition of Done**, applied to every item before it
  joins the Increment, plus a release-readiness gate before production. The Sprint Review
  inspects the Increment with stakeholders and adapts the backlog; it does not decide whether
  work is done. An item that fails the DoD is not part of the Increment, is not presented at
  the Sprint Review and returns to the Product Backlog.
- **Hybrid:** the DoD inside the sprints, plus milestone gates where the baseline needs a
  formal decision (Helios: M1, before the M4 pilot, before M6 general availability).

## Example: the Helios gate set
Helios runs one item gate and four stage or milestone gates. The full criteria are in
`assets/quality-plan-sample.md`, section 6.

| Gate | Level | Approver | Feeds |
|---|---|---|---|
| G0 Definition of Done | Item, every story | Frank Müller verifies; Ava Chen accepts the story | Sprint review, velocity, earned value |
| G1 Criteria ready | Milestone, M1 | Dana Okoro | Scope baseline |
| G2 Ready for UAT | Stage, before the M4 pilot | Frank Müller | G3 |
| G3 UAT exit (pilot) | Stage, before the M4 pilot go/no-go | Priya Nair | M4 pilot go/no-go |
| G4 GA quality gate | Milestone, before the M6 go/no-go | Sam Lee | Go/no-go criteria TE1–TE3, SE1–SE2 in `release-and-cutover` |

### Detail: Helios "ready for UAT" gate (G2)
| | Criteria | Evidence |
|---|---|---|
| **Entry** | Every pilot-scope story meets DoD v1.2; system and regression tests executed; 20 Support Operations agents booked for UAT (assumption A3) | Sprint review records; test summary; UAT schedule |
| **Exit** | Zero open severity-1/2 defects; every pilot Must's system test passed against the real identity provider, not a stub; independent accessibility audit (ACC-01) reports no failures against the baseline WCAG 2.1 AA criteria (the 2.2 AA criteria added by CR003 land in sprint S7 and are audited before G4); data-flow review (SEC-02) signed by Hana Sato | Defect log; test summary; audit report; signed review |

## Gate reviews and outcomes
A gate review is the meeting or asynchronous check where the evidence is compared with the exit
criteria and a decision is recorded (section 9 of `assets/quality-plan-template.md`). Outcomes:
- **Pass:** proceed.
- **Conditional pass:** proceed with named, dated follow-ups, each with an owner, logged as
  actions; a condition that is not met by its date reopens the gate.
- **Fail:** rework and re-review; the next gate does not start.
- **Waiver:** proceed despite a missed criterion, by the authorized approver only, in writing,
  with a compensating control, an expiry date and the risk logged in `risk-register`.

Waiver limits: never waive a severity-1 defect, a mandatory floor (legal, regulatory,
contractual, safety) or missing evidence; a severity-2 waiver needs the sponsor. Waivers must be
rare and visible: routine waivers mean the gate is theatre. Name the approver per gate in
advance, not on the day.

## Setting the bar: cost of quality
The cost of quality (COQ) is the total cost of achieving quality plus the cost of failing to.
It is the tool for deciding what "good enough" means.

| Category | What it is | Examples |
|---|---|---|
| **Prevention** (cost of conformance) | Stopping defects from being made | Acceptance-criteria reviews, DoD, peer review, coding standards, prototypes and usability rounds, training, process audits |
| **Appraisal** (cost of conformance) | Finding defects before the customer does | Inspections, test stages, UAT, audits, load and penetration tests, gate reviews |
| **Internal failure** (cost of non-conformance) | Defects found before release | Rework, retest, re-review, schedule slip, scrap |
| **External failure** (cost of non-conformance) | Defects found by customers or in operation | Hotfixes, rollback, extra support load, lost benefits, penalties, reputation |

Rules of thumb:
- A defect costs more the later it is found: a missing criterion fixed at refinement costs a
  conversation; the same gap found in production costs a hotfix, support calls and lost benefit.
  Spend on prevention first.
- Add an appraisal or prevention activity while the expected failure cost it avoids
  (probability the defect escapes × cost if it does) is greater than what the activity costs.
  Stop there: beyond that point more checking is gold-plating.
- **Floors are not traded.** Legal, regulatory, contractual and safety standards (Helios: WCAG
  2.2 AA, data residency, the security standard) are met whatever the COQ arithmetic says.
- Count external failure in the currency the sponsor cares about: lost benefit, not just fix
  effort.

### Helios cost-of-quality balance
| Category | On Helios | Size |
|---|---|---|
| Prevention | DoD, peer review of every merge, criteria reviews at refinement, two usability rounds in UX design & prototype (1.2.2), monthly process audit | Inside the design and build package budgets |
| Appraisal | System & UAT testing (1.4.1) with 20 Support Operations agents; accessibility audit, penetration test and load test in Hardening & launch (1.4.2) | $70,000 for 1.4.1 (BAC), plus part of 1.4.2 |
| Internal failure | Rework found before release, e.g. risk R005 minor UI rework after usability testing | R005 exposure 0.7 × $4,000 = $2,800, held in contingency |
| External failure | A broken reset or order-status journey after launch sends customers back to the phone | Up to about $2,900 of the $150,000 year-1 benefit ($150,000 ÷ 52) lost for each week the journeys are unusable, plus hotfix and hypercare effort; a severity-1 at cutover triggers the 75-minute rollback |

Decision recorded in the Helios quality plan: keep the full 4-week System & UAT testing and the
independent accessibility audit (a floor); do **not** add a second full manual regression cycle
before the pilot, because the 200-customer pilot is itself a low-blast-radius appraisal and the
automated regression suite (HEL-153) re-runs both journeys on every release candidate.

## Quality vs grade — keep them separate
- **Quality** = the degree to which the product meets its requirements; *low quality is always a
  problem* (defects, items that fail their acceptance criteria).
- **Grade** = the category or level of features and capability; *low grade can be perfectly
  acceptable* (a basic but defect-free tool).

A basic car can be high quality (no defects, does what it promises) and low grade (few
features). The Helios MVP for the pilot is deliberately low grade (password reset, order status
and the knowledge base only; live chat deferred to phase 2 by CR001) but must be high quality.

Gates enforce quality; grade is a scope decision made through change control. The verifiable
rule:
- Every reduction in grade (a dropped feature, a lowered target, a relaxed criterion) is recorded
  as a scope decision with a change request id via `change-request`.
- No defect is closed as "rejected", "out of scope" or "enhancement" to get through a gate unless
  the criterion it breaks was changed by an approved change request; the defect log's
  `fix_ref` column carries that CR id.
- Severity is changed only by the QC lead, with the reason written in the defect log, never by
  the person who wants the gate to pass.
