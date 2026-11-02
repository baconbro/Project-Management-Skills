# Quality Management Plan — sample (Helios v1.3)

Sample: a completed quality management plan for the sample Helios project (a fictional customer
self-service portal used throughout this catalog), built from `quality-plan-template.md` and
shown as at the GA quality gate G4 on 2026-09-29. Do not copy the Helios values; copy the
template and set your own.

| Field | Value |
|---|---|
| Project | Helios customer self-service portal |
| Version / date | v1.3 / 2026-09-29 (gate record updated at G4) |
| Plan owner | Sam Lee, project manager |
| QC lead | Frank Müller, QA engineer |
| Approved by | Dana Okoro, Sponsor, VP Customer Operations, on 2026-05-08 (v1.0, at M1) |

## 1. Quality objectives and mandatory floors
Objective: the password-reset and order-status journeys work first time for customers, because
every failed journey sends a customer back to the phone and erodes the objective of cutting those
two ticket types by 50% within 6 months of launch (OBJ-1).

| Floor (standard) | Source | Applies to | Evidence | Owner |
|---|---|---|---|---|
| WCAG 2.2 level AA | Hana Sato's accessibility policy; raised from 2.1 AA by CR003 | Every journey and knowledge-base page (REQ-006) | ACC-01 independent audit: the baseline WCAG 2.1 AA criteria before G2 (pilot); the full 2.2 AA audit after the CR003 uplift (sprint S7), before G4; DoD scan | Elena Rossi |
| Data residency | Hana Sato's data-residency policy (constraint CON-3) | All customer personal data (REQ-007) | SEC-02 data-flow review signed by Hana Sato | Hana Sato |
| No open high or critical security finding | Marcus Webb's security standard | Every release candidate | Penetration test and retest (HEL-151) | Marcus Webb |

## 2. Quality metrics
| Metric | Formula | Target | Data source | Frequency | Owner | Latest actual |
|---|---|---|---|---|---|---|
| Open defects by severity | Count of open defects per severity | 0 severity-1/2 at any gate | Defect log | Weekly and at each gate | Frank Müller | 2026-09-29: 0 / 0 / 3 / 0 open, 1 severity-4 deferred |
| Defect removal efficiency | Found before release ÷ (found before + first 30 days after) × 100 | ≥ 90% | Defect log | Pilot + 30 days; GA + 30 days | Frank Müller | Pilot 75%, confirmed at pilot + 30 days on 2026-09-07 (audit QA-05); GA due 2026-11-02 |
| Escaped severity-1/2 defects | Severity-1/2 defects found after a release | 0 | Defect log | Weekly in the pilot and hypercare | Frank Müller | Pilot: 1 (DEF-008) |
| First-pass acceptance | Stories accepted at their first review ÷ stories reviewed | ≥ 90% | Sprint review records | Every sprint | Ava Chen | S7–S10: 94% |
| DoD compliance | Sampled done items meeting every DoD line ÷ sampled | 100% | Process audit | Monthly | Sam Lee | 7 of 9 at QA-03 (2026-07-10); scan now blocking in the pipeline |
| Page performance | Share of pages loading within 2 s, and error rate, at the forecast launch peak | ≥ 95% within 2 s; errors under 0.1% | Load test (HEL-150) | Before G4 | Ben Adeyemi | Met on release candidate 2.0 |
| Accessibility | Failures in the independent WCAG 2.2 AA audit | 0 | ACC-01 audit report | 2.1 AA criteria before G2; first full 2.2 AA audit before G4 | Elena Rossi | 0 on release candidate 2.0 |
| Security | Open high or critical penetration-test findings | 0 | Retest report (HEL-151) | Before G4 | Marcus Webb | 0 |

## 3. Roles
| Role | Who | Responsibility |
|---|---|---|
| Plan owner and QA (process audits) | Sam Lee | Maintains this plan; runs the monthly audit with a QA lead from another team; owns QA actions |
| QC lead | Frank Müller | Test strategy and stages, defect log, DoD verification, gate evidence |
| Peer reviewers | Ben Adeyemi, Carla Diaz, Devin Patel | Review every merge; branch protection enforces it |
| Specialist checks | Elena Rossi (accessibility), Marcus Webb (security), Ben Adeyemi (performance) | Commission and sign the specialist evidence |
| Item acceptance | Ava Chen, product owner | Accepts stories that meet the DoD and their criteria |
| Deliverable acceptance (scope validation) | Acceptors named in the scope statement, mostly Priya Nair | Accept deliverables that QC has verified, recorded with `scope-and-requirements` |

## 4. Cost of quality
| Category | Planned activities or expected failures | Cost or exposure | Where it sits |
|---|---|---|---|
| Prevention | Criteria reviews at refinement, DoD, peer review, two usability rounds, monthly process audit | Inside work-package budgets | 1.2.2, 1.3.1–1.3.4, 1.1 |
| Appraisal | System, regression and UAT testing with 20 Support Operations agents; accessibility audit, penetration test, load test | $70,000 for 1.4.1, plus part of 1.4.2 | 1.4.1, 1.4.2 |
| Internal failure | Rework found before release, e.g. R005 minor UI rework after usability testing | R005: 0.7 × $4,000 = $2,800 | Contingency reserve |
| External failure | Journeys unusable after launch send customers back to the phone; hotfixes; rollback | Up to about $2,900 of the $150,000 year-1 benefit per week; a severity-1 at cutover means the 75-minute rollback | Not budgeted — avoided |

"Good enough" decision (v1.0, confirmed at G4): keep the full System & UAT testing and the
independent accessibility audit (a floor). Do not add a second full manual regression cycle before
the pilot: the 200-customer pilot is a low-blast-radius appraisal, and the automated regression
suite (HEL-153) re-runs both journeys on every release candidate in under 30 minutes.

## 5. Acceptance-criteria standard
- Format: Given/When/Then for journeys and APIs; checklist for reports, content, runbooks and data.
- Every Must's criterion passes the SMART-style checks and has a test id: UAT-nn, SIT-nn, ACC-nn,
  SEC-nn, TRN-nn or OPS-nn, as in the RTM.
- Since v1.3 (audit QA-05) every journey also has a session time-out and a data-freshness scenario.
- Captured in the RTM and scope statement (`scope-and-requirements`) and the product backlog
  (`agile-delivery`); reviewed by Frank Müller at weekly refinement; failures go back to Ava Chen
  or the requirement's source.

## 6. Definition of Done and quality gates
Definition of Done: `definition-of-done-sample.md`, v1.2 of 2026-07-16.

| Gate | Level and when | Entry criteria | Exit criteria | Evidence | Approver |
|---|---|---|---|---|---|
| G0 Definition of Done | Item; every story, every sprint | Story met the definition of ready and is built | Every DoD v1.2 line checked | Pipeline run; DoD checklist on the story | Frank Müller verifies; Ava Chen accepts the story |
| G1 Criteria ready | Milestone; M1 | Scope statement and RTM drafted | Every Must has a criterion that passes the SMART-style checks and a test id; DoD v1.0 agreed; this plan approved | RTM review record | Dana Okoro |
| G2 Ready for UAT | Stage; before the M4 pilot | Pilot-scope stories meet the DoD; system and regression tests executed; 20 UAT agents booked (A3) | 0 open severity-1/2; every pilot Must's system test passed against the real identity provider; ACC-01 shows no failures against the baseline WCAG 2.1 AA criteria (the 2.2 AA criteria added by CR003 land in sprint S7 and are audited before G4); SEC-02 signed | Test summary; defect log; audit and review reports | Frank Müller |
| G3 UAT exit (pilot) | Stage; before the M4 pilot go/no-go | G2 passed; UAT scripts for UAT-01 to UAT-05 ready | Every UAT script passed; 0 open severity-1/2; each open severity-3 has a published workaround and a fix date; UAT signed | UAT sign-off; defect log | Priya Nair |
| G4 GA quality gate | Milestone; before the M6 go/no-go | Release candidate 2.0 frozen; GA stories meet the DoD; regression suite green | 0 open severity-1/2; ≥ 95% of pages within 2 s and errors under 0.1% at forecast peak; penetration retest with no open high or critical finding; ACC-01 with no failures at WCAG 2.2 AA; GA UAT signed; pilot DRE reported with its QA actions closed | Defect report; load-test, retest and audit reports; UAT sign-off; audit log | Sam Lee, on Frank Müller's recommendation |

Waiver rule: only the gate approver may waive, in writing, with a compensating control, an expiry
date and the risk logged in the risk register; never a severity-1 defect, a floor in section 1 or
missing evidence; a severity-2 waiver needs Dana Okoro.
Release readiness: G4's evidence becomes go/no-go criteria TE1–TE3 and SE1–SE2 in the decision of
2026-09-30, run with `release-and-cutover`; Dana Okoro decides there.

## 7. QA and QC activities and cadence
| Activity | Type (QA / QC) | When | Who | WBS id |
|---|---|---|---|---|
| Criteria review at backlog refinement | QA — prevention | Weekly | Frank Müller with Ava Chen | 1.3.1–1.3.4 |
| Peer review of every merge | QC — inspection | Every merge | Ben Adeyemi, Carla Diaz, Devin Patel | 1.3.1–1.3.4 |
| Pipeline: unit and API tests, regression suite (HEL-153), WCAG 2.2 AA scan, security scans | QC — test | Every merge and nightly | Ben Adeyemi | 1.3.1–1.3.4 |
| DoD check (G0) | QC — item gate | Before a story goes to the sprint review | Frank Müller | 1.3.1–1.3.4 |
| Sprint review | Inspection of the done increment with stakeholders, not a gate | Every second Friday | Ava Chen | 1.1 |
| DoD and plan review at the retrospective | QA | Every sprint | Sam Lee | 1.1 |
| Process audit | QA | Last Friday of each month; a triggered audit after a major lapse or an escaped severity-1/2 replaces that month's audit | Sam Lee with a QA lead from another team | 1.1 |
| System and regression testing | QC — test | Before G2 and G4 | Frank Müller | 1.4.1 |
| UAT with 20 Support Operations agents | QC — test | 2026-07-28 to 2026-07-31 (pilot); 2026-09-21 to 2026-09-25 (GA) | Frank Müller; Priya Nair signs | 1.4.1 |
| Independent WCAG 2.2 AA audit | QC — specialist | 2.1 AA criteria before G2; full 2.2 AA audit after the CR003 uplift (sprint S7), before G4 | V04 accessibility audit firm (contract owner Frank Müller); Elena Rossi reviews the findings | 1.4.2 |
| Penetration test and retest; load test at forecast peak | QC — specialist | Before G4 | Marcus Webb; Ben Adeyemi | 1.4.2 |
| Gate reviews G1–G4 | QC — decision | 2026-05-08, 2026-07-28, 2026-07-31, 2026-09-29 | Approvers in section 6 | 1.1 |

All activities above are in the schedule and the cost baseline (project management plan,
sections 7 and 10).

## 8. Defect management
| Severity | Definition | Gate rule | Fix target |
|---|---|---|---|
| 1 | Portal down; SSO sign-in failing for more than 5% of attempts; data shown to the wrong customer | Blocks every gate; never waived | Restore within 2 hours; fix the same day |
| 2 | Reset, order status or search broken for a segment; the phone is the only workaround | Blocks every gate; waiver by Dana Okoro only | 1 business day |
| 3 | Defect with a workaround published as a known error | May pass with workaround, owner and fix date | Next sprint or weekly patch |
| 4 | Cosmetic issue or enhancement idea | Product backlog (Ava Chen) | Backlog order |

Defect log: the team's tracker, exported weekly in the format of `defect-log-template.csv`
(`defect-log-sample.csv` is an extract). Closed only after a retest by someone other than the
fixer. Severity is changed only by Frank Müller, with the reason logged. No defect is closed as
rejected or out of scope unless an approved change request changed the criterion it breaks.

## 9. Gate decision record
| Gate | Date | Evidence reviewed | Decision | Conditions or waivers | Approver |
|---|---|---|---|---|---|
| G1 | 2026-05-08 | RTM review: every Must has a criterion passing the checks and a test id; DoD v1.0 | Pass | — | Dana Okoro |
| G2 | 2026-07-28 | Test summary: 0 open severity-1/2 after DEF-005 was fixed and retested; real-provider runs (ACT003); ACC-01 no failures against the baseline WCAG 2.1 AA criteria (the CR003 2.2 AA stories HEL-142 and HEL-143 come in sprint S7); SEC-02 signed | Pass | — | Frank Müller |
| G3 | 2026-07-31 | UAT-01 to UAT-05 passed; 0 open severity-1/2; DEF-006 (four outdated articles) open with a workaround | Conditional pass | DEF-006 articles rewritten by M5 (Carla Diaz) | Priya Nair |
| G4 | 2026-09-29 | 0 open severity-1/2; DEF-010 to DEF-012 open severity-3 with known-error workarounds; DEF-013 deferred; load test met; retest 0 high or critical; ACC-01 0 failures at WCAG 2.2 AA (its first 2.2 AA pass); GA UAT signed; pilot DRE 75% with QA-05 actions closed | Conditional pass | DEF-010 to DEF-012 fixed in hypercare patch 1 by 2026-10-08 (Ben Adeyemi), carried into the go/no-go as condition C2 | Sam Lee |

## 10. Reporting, review and change
- Metrics against target in the weekly status report and at every gate; first-pass acceptance at
  every sprint review.
- This plan and the DoD are reviewed at every retrospective; changes are versioned below.
- A change to a floor, a gate's exit criteria or a requirement's acceptance criterion goes through
  change control (`change-request`).

| Version | Date | Change | Approved by |
|---|---|---|---|
| v1.0 | 2026-05-08 | First approved version with DoD v1.0 and gates G0–G4 | Dana Okoro |
| v1.1 | 2026-07-01 | Accessibility floor raised to WCAG 2.2 AA (CR003); DoD v1.1 | CCB, approving CR003 on 2026-06-30 |
| v1.2 | 2026-07-16 | DoD v1.2: blocking accessibility scan, "not done" rule, real-provider evidence (audits QA-03, QA-04) | Sam Lee |
| v1.3 | 2026-08-28 | Time-out and data-freshness scenarios added to the criteria standard (audit QA-05) | Sam Lee |
