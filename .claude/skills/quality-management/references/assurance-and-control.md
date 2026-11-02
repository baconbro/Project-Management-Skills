# Quality Assurance, Quality Control and Quality Metrics

Quality assurance and quality control answer different questions, need different owners and
run on different cadences. Collapsing them into "testing" leaves a project with detection and
no prevention: defects are found late, and the process that produced them never changes.
Examples come from the sample Helios project (a fictional customer self-service portal used
throughout this catalog).

## Three activities, three questions
| | Quality assurance (QA) | Quality control (QC) | Scope validation |
|---|---|---|---|
| Question | Are we following the process that should produce quality, and is it working? | Does this deliverable meet its criteria and the DoD? | Does the named acceptor accept it? |
| Focus | Process; prevention | Product; detection | Acceptance |
| Activities | Process audits, criteria and DoD reviews, root-cause analysis, process changes, training | Peer review, inspection, test stages, defect logging, gate checks | Formal acceptance against the criteria |
| Timing | Periodic (monthly or per phase) and after an escaped severity-1/2 | Continuous, at every stage and gate | When QC has verified a deliverable |
| Helios owner | Sam Lee (monthly process audit) | Frank Müller, QA engineer and QC lead | The named acceptor, e.g. Priya Nair |
| Output | Audit log, process changes | Test results, defect log, gate decisions | Acceptance log entry |
| Skill | `quality-management` | `quality-management` | `scope-and-requirements` |

Sequence: QC verifies, then scope validation accepts; QA watches both processes and changes them
when the data shows a gap.

## Running a process audit (QA)
- **Auditor:** someone independent of the work audited: the project manager, a QA lead from
  another team or the PMO. Developers do not audit their own merges.
- **Cadence:** a fixed rhythm (monthly, or at each phase end) plus a triggered audit after any
  escaped severity-1/2 defect or a missed defect-removal-efficiency target.
- **Sample:** look at evidence, not statements; take at least 5 items or 10–20% of the work since
  the last audit, chosen by the auditor.
- **Standard checks** (pick those the quality plan relies on):
  1. Acceptance criteria were written and passed the SMART-style checks before build started.
  2. Every merge was peer-reviewed by someone other than its author.
  3. Every item called done met every DoD line, with evidence (pipeline run, checklist).
  4. Planned test stages ran in order, in the planned environment, on current data.
  5. Acceptance evidence comes from the real environment, not stubs or mocks.
  6. Every defect carries severity, stage found, WBS id, requirement id and an owner; closed
     defects were retested by someone other than the fixer.
  7. Gate decisions are recorded with evidence, approver, conditions and waivers.
  8. Last audit's actions were done by their due date.
- **Rating:** *conforms*; *minor* (an isolated lapse, no defect escaped because of it); *major*
  (the rule is systematically not followed, or a defect reached a later stage because of it).
- **Actions:** change the process (tooling, a rule, training), not the person. Each finding gets
  an action, one owner and a due date in the audit log (`assets/quality-audit-log-template.csv`).
  A repeat finding, or a major one not closed by its due date, is escalated as an issue through
  `project-delivery`.

## Running quality control (QC)
- **Inspection and review:** peer code review, document walkthroughs, static analysis,
  design reviews. The cheapest appraisal: it finds defects before they are executed.
- **Test stages:** unit → integration → system and regression → non-functional (performance,
  security, accessibility) → user acceptance testing (UAT). Each stage has entry and exit
  criteria; see `references/quality-gates.md`.
- **Evidence:** every pass is backed by an artifact (pipeline run, test report, audit report,
  signed UAT script) that a gate reviewer can open. "Tested" without evidence is not tested.
- **Verify, do not accept:** QC tells the acceptor that the criteria are met; acceptance stays
  with the acceptor through `scope-and-requirements`.

## Defect management

### Severity scale
Severity is the impact, set by QC. Priority is the order of fixing, set by the product owner.
Keep the two apart: a cosmetic typo on the home page can be severity 4 and high priority.

| Severity | Definition | Gate rule | Helios example |
|---|---|---|---|
| 1 Critical | Service or a critical journey unavailable; data lost, corrupted or shown to the wrong person; a legal or security breach. No workaround | Blocks every gate; never waived | Portal down; SSO sign-in failing for more than 5% of attempts |
| 2 High | A core function broken for a segment of users; the only workaround is costly (e.g. phone the service desk) | Blocks every gate; a waiver needs the sponsor and a dated fix | DEF-005: a failed identity-provider response showed a blank page instead of the retry message |
| 3 Medium | A defect with a workaround that can be published as a known error | May pass a gate with the workaround published, an owner and a fix date | DEF-010: the carrier tracking link opens in the same tab and ends the portal session |
| 4 Low | Cosmetic issue or minor inconvenience | Goes to the product backlog | DEF-013: the "Track shipment" button label is truncated on 320-pixel screens |

The Helios hypercare plan in `release-and-cutover` uses the same four levels, so a defect keeps
its severity from test into operation.

### Lifecycle
`new` → `open` (triaged: severity, owner, WBS and requirement ids) → `fixed` → `verified`
(retested by someone other than the fixer) → `closed`. Side exits: `deferred` (severity 3–4
moved to the backlog by the product owner, with a reason) and `rejected` (works as specified).
A "works as designed" that contradicts an acceptance criterion is still a defect; if the
criterion is wrong, change it through a change request first.

Log every defect from system test onward, and every defect that escapes a stage, in the defect
log (`assets/defect-log-template.csv`). Defects caught and fixed inside a developer's own work
before merge need not be logged.

## Quality metrics catalog
Choose five to eight metrics, each with a formula, a target, a data source, a frequency and an
owner (section 2 of `assets/quality-plan-template.md`).

| Metric | Formula | Tells you | Typical target |
|---|---|---|---|
| Open defects by severity | Count of open defects per severity at a point in time | Whether a gate can pass | 0 severity-1/2 at any gate |
| Defect removal efficiency (DRE) | Defects found before release ÷ (found before release + found in the first 30 days after release) × 100 | How much of the defect load QC catches before customers do | ≥ 90%; higher for safety-critical work |
| Escaped defects | Defects found after release (pilot or production), by severity | Customer-visible failure; triggers a QA audit | 0 severity-1/2 |
| Defect density | Defects found ÷ size (per 100 story points accepted, per KLOC, per 10 document pages) | Where defects cluster | A downward trend; compare packages within one project only |
| First-pass acceptance | Items accepted at their first review ÷ items reviewed | Whether the DoD and criteria work before the review | ≥ 90% |
| DoD compliance | Sampled done items meeting every DoD line ÷ sampled done items | Whether the DoD is real or a wiki page | 100% |
| Defect ageing | Days open per severity, against the fix target | Whether known issues are being worked | Within the fix target per severity |
| Audit action closure | QA actions closed by their due date ÷ actions due | Whether QA findings change anything | 100% |
| Non-functional measures | As defined in the requirement (p95 page load, error rate, WCAG failures, open penetration-test findings) | Conformance to the floors and NFRs | The requirement's threshold |

Rules: a metric without a target is decoration; report trends, not single points; never use
defect counts to rate individuals, or people stop logging defects and every metric goes blind.

### Worked example: Helios pilot DRE
The Helios defect-log extract (`assets/defect-log-sample.csv`) shows the arithmetic. DEF-001
to DEF-006 were found before the pilot opened; DEF-007 was rejected (works as specified), so it
is not a defect and does not count; DEF-008 and DEF-009 were found by pilot customers. DRE for
the pilot release = 6 ÷ (6 + 2) × 100 = **75%**, the figure audit QA-05 reported for the full
log, below the 90% target. Both escapes trace to requirements nobody stated (session time-out
and order-status freshness), so the fix is in the process, not only in the code: QA-05 added
time-outs and data freshness to the non-functional probe list used with
`scope-and-requirements` and to the criteria review checklist in
`references/acceptance-criteria.md`.

## From QC data to QA action
- **Pareto by root cause:** sort defects by `root_cause` (requirements, design, code,
  configuration, data, environment, process); the top one or two categories usually hold most
  of the defects and point to the process to fix. Do the same for escaped defects separately:
  they show what the QC process misses.
- **Five whys:** for each escaped severity-1/2, ask why it was made and why it was not caught;
  record the lesson with `lessons-learned`.
- **Run and control charts:** for a repeating process (defects found per sprint, build failures
  per week), plot the values with their mean. A point outside the control limits (mean ± 3
  standard deviations) or seven consecutive points on one side of the mean signals a special
  cause worth investigating; normal variation inside the limits does not justify a process
  change.
- **Close the loop:** every QA action names the process artifact it changes (DoD version,
  criteria checklist, pipeline step, quality plan section), so the next audit can check it.
