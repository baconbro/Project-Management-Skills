# Quality Management Plan — fill-in template

Fill-in template: copy it, replace every `<placeholder>`, and delete rows that do not apply.
Keep it to two or three pages; detail lives in the linked artifacts. `quality-plan-sample.md`
shows a completed version for the sample Helios project. Guidance for each section is in the
`quality-management` skill's references: `acceptance-criteria.md`, `quality-gates.md` and
`assurance-and-control.md`.

| Field | Value |
|---|---|
| Project | `<project name>` |
| Version / date | `<v1.0>` / `<YYYY-MM-DD>` |
| Plan owner | `<project manager>` |
| QC lead | `<name - owns test strategy and the defect log>` |
| Approved by | `<sponsor>` on `<YYYY-MM-DD>` |

## 1. Quality objectives and mandatory floors
Objective: `<what quality must achieve for the benefit - one or two sentences linked to the objective id>`.

Floors are met whatever the cost-of-quality arithmetic says; they are never waived.

| Floor (standard) | Source | Applies to | Evidence | Owner |
|---|---|---|---|---|
| `<legal / regulatory / contractual / safety standard and level>` | `<policy, law, contract clause>` | `<deliverables or requirement ids>` | `<audit / test / signed review>` | `<name>` |

## 2. Quality metrics
| Metric | Formula | Target | Data source | Frequency | Owner | Latest actual |
|---|---|---|---|---|---|---|
| `<open defects by severity>` | `<count of open defects per severity>` | `<0 severity-1/2 at any gate>` | `<defect log>` | `<each gate>` | `<name>` | `<value and date>` |
| `<defect removal efficiency>` | `<found before release ÷ (before + first 30 days after) × 100>` | `<≥ 90%>` | `<defect log>` | `<release + 30 days>` | `<name>` | `<value and date>` |
| `<metric>` | `<formula>` | `<target>` | `<source>` | `<frequency>` | `<name>` | `<value and date>` |

## 3. Roles
| Role | Who | Responsibility |
|---|---|---|
| Plan owner and QA (process audits) | `<name>` | `<maintains this plan; runs the audits; owns QA actions>` |
| QC lead | `<name>` | `<test strategy, test stages, defect log, gate evidence>` |
| Peer reviewers | `<names>` | `<review every merge or document before it is done>` |
| Specialist checks | `<names>` | `<accessibility / security / performance evidence>` |
| Item acceptance | `<product owner>` | `<accepts stories that meet the DoD>` |
| Deliverable acceptance (scope validation) | `<named acceptors in the scope statement>` | `<accept deliverables QC has verified - recorded with scope-and-requirements>` |

## 4. Cost of quality
| Category | Planned activities or expected failures | Cost or exposure | Where it sits (WBS id, reserve) |
|---|---|---|---|
| Prevention | `<criteria reviews, DoD, peer review, prototypes, training, audits>` | `<amount or "inside work packages">` | `<WBS ids>` |
| Appraisal | `<test stages, UAT, audits, specialist tests, gate reviews>` | `<amount>` | `<WBS ids>` |
| Internal failure | `<expected rework before release - risk ids>` | `<expected value>` | `<contingency reserve>` |
| External failure | `<what a defect after release costs - lost benefit per week, fixes, penalties>` | `<expected value or rate>` | `<not budgeted - avoided>` |

"Good enough" decision: `<which checks are kept, added or dropped, and why - the expected failure cost avoided against the cost of the check; floors excluded from the trade>`.

## 5. Acceptance-criteria standard
- Format: `<Given/When/Then for behaviour; checklist for documents, reports and data>`.
- Every Must's criterion passes the SMART-style checks and has a test id (`<test id prefixes>`).
- Captured in: `<RTM and scope statement (scope-and-requirements); backlog (agile-delivery); WBS dictionary>`.
- Reviewed by `<QC lead>` at `<refinement / before baseline>`; failures go back to `<owner>`.

## 6. Definition of Done and quality gates
Definition of Done: `<link to the DoD and its version>`.

| Gate | Level and when | Entry criteria | Exit criteria | Evidence | Approver |
|---|---|---|---|---|---|
| `<G0 Definition of Done>` | `<item - every story>` | `<item meets the definition of ready and is built>` | `<every DoD line checked>` | `<pipeline run; DoD checklist>` | `<verifier; product owner accepts>` |
| `<G1 name>` | `<stage or milestone - date or milestone id>` | `<preconditions>` | `<threshold + evidence source per line>` | `<artifacts>` | `<one named person>` |

Waiver rule: `<who may waive; written decision with compensating control, expiry and risk id; never a severity-1 defect, a floor or missing evidence; severity-2 only by the sponsor>`.
Release readiness: the last gate's evidence goes to the go/no-go run with `release-and-cutover` on `<date>`.

## 7. QA and QC activities and cadence
| Activity | Type (QA / QC) | When | Who | WBS id |
|---|---|---|---|---|
| `<criteria review at refinement>` | `<QA - prevention>` | `<weekly>` | `<name>` | `<WBS id>` |
| `<peer review>` | `<QC - inspection>` | `<every merge>` | `<names>` | `<WBS id>` |
| `<process audit>` | `<QA>` | `<monthly; and after any escaped severity-1/2>` | `<independent auditor>` | `<WBS id>` |
| `<test stage>` | `<QC - test>` | `<dates or before gate>` | `<name>` | `<WBS id>` |
| `<gate review>` | `<QC - decision>` | `<milestone>` | `<approver>` | `<WBS id>` |

All activities above are in the schedule and the cost baseline: `<link to the project management plan>`.

## 8. Defect management
| Severity | Definition | Gate rule | Fix target |
|---|---|---|---|
| 1 | `<service or critical journey down; data loss or exposure; legal breach; no workaround>` | Blocks every gate; never waived | `<time>` |
| 2 | `<core function broken for a segment; costly workaround only>` | Blocks every gate; waiver by the sponsor only | `<time>` |
| 3 | `<defect with a workaround published as a known error>` | May pass with workaround, owner and fix date | `<time>` |
| 4 | `<cosmetic>` | Product backlog | `<backlog>` |

Defect log: `<tool, exported to defect-log-template.csv format>`. A defect is closed only after a
retest by someone other than the fixer. Severity is changed only by the QC lead, with the reason
logged. No defect is closed as rejected or out of scope unless an approved change request changed
the criterion it breaks.

## 9. Gate decision record
| Gate | Date | Evidence reviewed | Decision (pass / conditional pass / fail / waiver) | Conditions or waivers (owner, due date, risk id) | Approver |
|---|---|---|---|---|---|
| `<gate>` | `<YYYY-MM-DD>` | `<artifacts and their key figures>` | `<decision>` | `<details>` | `<name>` |

## 10. Reporting, review and change
- Metrics against target reported in `<status report / sprint review / steering pack>` every `<cycle>`.
- This plan and the DoD are reviewed at `<each retrospective / phase end>`; changes are versioned below.
- A change to a floor, a gate's exit criteria or a requirement's acceptance criterion goes through
  change control (`change-request`).

| Version | Date | Change | Approved by |
|---|---|---|---|
| `<v1.0>` | `<YYYY-MM-DD>` | `<first approved version>` | `<sponsor>` |
