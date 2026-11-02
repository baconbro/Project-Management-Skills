---
name: quality-management
description: >-
  Plans, assures and controls project quality: objectives and metrics, the
  cost-of-quality balance that decides what is good enough, the
  acceptance-criteria standard, a definition of done, quality gates with entry
  and exit criteria, and process audits (quality assurance) kept apart from
  testing and the defect log (quality control). Use when the user wants a
  quality management plan, a definition of done, gate exit criteria, a review
  and test cadence, quality metrics, a process audit or defect severities, or
  the team disputes whether work is done. Triggers: "quality management plan",
  "definition of done", "DoD", "quality gate", "entry and exit criteria",
  "acceptance criteria", "Given/When/Then", "cost of quality", "quality
  assurance vs quality control", "process audit", "defect log", "escaped
  defects", "quality vs grade". For each requirement's acceptance test and
  sign-off, use scope-and-requirements; for go-live readiness, use
  release-and-cutover. Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.1.0
  category: discipline
  phase: cross-cutting
  related: [project-planning, work-breakdown-structure, agile-delivery, scope-and-requirements, release-and-cutover]
license: MIT
---

# Quality Management

## Overview
Quality management decides what "good" means before the work starts, then proves as the work
proceeds that it is being met. It has three parts, kept deliberately apart:
- **Quality planning:** mandatory standards (floors), metrics with targets, the cost-of-quality
  balance, the acceptance-criteria standard, the Definition of Done (DoD) and the quality gates.
- **Quality assurance (QA), process-focused prevention:** audits that the agreed way of working is
  followed (criteria first, peer review, DoD applied, test stages run), and process fixes.
- **Quality control (QC), product-focused detection:** inspecting and testing deliverables against
  their criteria, logging defects by severity to closure, and enforcing gate exit criteria.

QC verifies; it does not accept. Formal acceptance by the named acceptor (scope validation)
belongs to `scope-and-requirements`, and the go-live decision to `release-and-cutover`. The
examples use the sample Helios project (a fictional customer self-service portal used throughout
this catalog): Frank Müller (QA engineer) leads quality control, Sam Lee (project manager) runs
the monthly process audit, and an item gate plus four stage and milestone gates lead to the M4
pilot and M6 general availability (GA).

## When to use this skill
- The user needs a quality management plan, quality metrics with targets, or a decision on how
  much review and testing is "good enough".
- The user needs a Definition of Done, a standard for acceptance criteria, or a testability review
  of existing criteria.
- The user needs quality gates (entry and exit criteria, approvers, waiver rules) or a review and
  test cadence.
- The user wants a process audit or a defect log and severity scheme, defects keep escaping to UAT
  or production, or the team is arguing over whether something is "done".
- Do NOT use this to capture each requirement's acceptance test or to get a deliverable formally
  accepted — use `scope-and-requirements` instead; this skill sets the standard those criteria
  follow and verifies work against them.
- Do NOT use this to decide whether a release goes live (go/no-go, cutover, hypercare) — use
  `release-and-cutover` instead; this skill supplies the quality evidence it decides on.
- Do NOT use this to write or split user stories or set the definition of ready — use
  `agile-delivery` instead.
- Do NOT use this to decompose scope into deliverables — use `work-breakdown-structure` instead.

## Methodology fit
- **Waterfall:** a quality management plan baselined with the project plan; formal stage gates
  (requirements baseline, ready for system test, ready for UAT, UAT exit) with documented entry and
  exit criteria and one named approver each; a process audit per phase; defects tracked by the
  stage that found them, with defect removal efficiency measured per release.
- **Agile:** the gate for every backlog item is the Definition of Done, applied before the item
  joins the Increment. The Sprint Review inspects the Increment with stakeholders and adapts the
  backlog; it does not decide whether work is done, and an item that misses the DoD is not
  presented but returns to the Product Backlog. QC lives in the pipeline (automated tests and
  scans); QA is the DoD review at each retrospective plus a periodic practice audit. A
  release-readiness gate still applies before production.
- **Hybrid (Helios):** one light quality plan with milestone gates — criteria ready at M1, ready
  for UAT and UAT exit before the M4 pilot, the GA quality gate before M6 — and the DoD inside
  two-week sprints. The GA gate's evidence becomes the test and security criteria of the go/no-go
  run with `release-and-cutover`.

## Inputs you need
- The scope statement and requirements traceability matrix (RTM) with an acceptance test per
  requirement (from `scope-and-requirements`), and the WBS with its dictionary (from
  `work-breakdown-structure`).
- Mandatory standards: legal, regulatory, contractual and organizational (Helios: WCAG 2.2 AA after
  change request CR003, the data-residency policy, the security standard).
- Stakeholder expectations and the sponsor's tolerance for defects reaching customers.
- The delivery approach, and the schedule and budget that quality activities must fit (from
  `project-planning`).

With no requirements or acceptance tests, run `scope-and-requirements` first: this skill sets the
bar and checks against it; it does not invent the requirements.

## Workflow
1. **Set objectives, floors and metrics.** Copy `assets/quality-plan-template.md` and fill
   sections 1–3: list each mandatory standard as a floor with its source, then choose 5–8 metrics
   from the catalog in `references/assurance-and-control.md`, each with a formula, target, data
   source, frequency and owner, and name the QC lead and the QA auditor. Helios: zero open
   severity-1/2 defects at every gate, defect removal efficiency (DRE) ≥ 90%, 95% of pages within
   2 seconds at peak, zero WCAG 2.2 AA failures. *Done: every floor names its source and every
   metric has a formula, a target and an owner.*
2. **Decide the cost-of-quality balance.** In section 4 of the plan, estimate prevention and
   appraisal spend against the expected internal and external failure cost, using "Setting the
   bar: cost of quality" in `references/quality-gates.md`. Keep a check while the failure cost it
   is expected to avoid exceeds its cost; never trade below a floor. Helios keeps the full System
   & UAT testing ($70,000, WBS 1.4.1) and the independent accessibility audit, and treats the
   200-customer pilot as extra appraisal instead of a second manual regression cycle. *Done: all
   four cost categories are estimated and the "good enough" decision is written with its reason.*
3. **Set the acceptance-criteria standard and review the criteria.** Requirement and deliverable
   criteria are captured in `scope-and-requirements` (the RTM `acceptance_test` column and the
   scope statement); story criteria in `agile-delivery`. Fix the format (Given/When/Then or
   checklist) in section 5 of the plan, then review every Must's criterion against the
   SMART-style checks in `references/acceptance-criteria.md` and return failures to their owner.
   *Done: every Must has a criterion that passes all the checks and carries a test id.*
4. **Agree the Definition of Done.** Fill `assets/definition-of-done.md`: the cross-cutting bar for
   build and review, test, non-functional checks and documentation, each line checkable by someone
   other than its author. `assets/definition-of-done-sample.md` is the Helios DoD v1.2. *Done: a
   versioned DoD agreed by the team and the product owner and posted where the work happens.*
5. **Design the quality gates.** In section 6 of the plan define each gate's level (item, stage,
   milestone), entry criteria, exit criteria as threshold plus evidence source, and one named
   approver, plus the waiver rule, following `references/quality-gates.md`. In agile the item gate
   is the DoD. Route release readiness to `release-and-cutover`: the last gate hands it its evidence
   (Helios: gate G4 on 2026-09-29 feeds go/no-go criteria TE1–TE3 and SE1–SE2). *Done: every gate
   has entry and exit criteria, an evidence source and one named approver.*
6. **Schedule and cost the QA and QC activities.** In section 7 list each activity with its type
   (QA or QC), timing, owner and WBS id — criteria reviews, peer review, pipeline tests, DoD checks,
   test stages, specialist tests, process audits, gate reviews — and hand the list to
   `project-planning` for the schedule and cost baseline. *Done: every activity has an owner, a date
   or cadence and a home in the schedule and budget.*
7. **Assure the process (QA).** At the agreed cadence, and after any escaped severity-1/2 defect,
   audit a sample of recent work with the standard checks in `references/assurance-and-control.md`.
   Log each audit in a copy of `assets/quality-audit-log-template.csv`
   (`assets/quality-audit-log-sample.csv` shows Helios audits QA-01 to QA-06). When escapes or a low
   DRE show a gap, change the process (DoD, checklist, pipeline step), not just the defect. *Done:
   each audit has a result; each finding has an action, one owner and a due date; repeat findings
   are escalated.*
8. **Control the product (QC) and enforce the gates.** Inspect and test each deliverable against
   its criteria and the DoD. Log every defect in a copy of `assets/defect-log-template.csv` with
   severity (scale in `references/assurance-and-control.md`), stage found, WBS and requirement ids
   and an owner, and close it only after a retest by someone other than the fixer
   (`assets/defect-log-sample.csv` is a Helios extract). At each gate compare the evidence with the
   exit criteria and record pass, conditional pass, fail or waiver in section 9 of the plan
   (`assets/quality-plan-sample.md` shows G1–G4). *Done: every defect has severity, stage, owner
   and status; every gate decision is recorded with its evidence and approver.*
9. **Hand on, report and improve.** Send verified deliverables to their acceptor through
   `scope-and-requirements` and the last gate's record to `release-and-cutover`. Report metrics
   against target every status cycle. Raise any dropped feature or lowered target as a change
   request (`change-request`), never as a reclassified defect. Review the DoD and the plan at each
   retrospective or phase end. *Done: metrics are reported against target, every grade reduction
   has a change request id, and the DoD and plan versions are current.*

## Quality checklist
- [ ] Every floor (legal, regulatory, contractual, safety standard) is listed with its source and
      evidence, and none appears in a waiver.
- [ ] Every metric has a formula, a target, a data source, a frequency and an owner.
- [ ] The four cost-of-quality categories are estimated and the "good enough" decision is written.
- [ ] Every Must requirement has an acceptance criterion that passes the SMART-style checks and a
      test id.
- [ ] The DoD is versioned, agreed by the team and product owner, and every line is checkable from
      evidence.
- [ ] Every gate has entry criteria, exit criteria with an evidence source, and one named approver.
- [ ] Every gate decision and waiver is recorded; each waiver has an approver, a compensating
      control, an expiry and a risk id, and none covers a severity-1 defect.
- [ ] Process audits ran at the planned cadence; every finding has an action, owner and due date.
- [ ] Every defect in the log has a severity, stage found, WBS id, requirement id and owner; every
      closed defect was retested by someone other than the fixer.
- [ ] Reductions in grade (dropped features, lowered targets) are recorded as scope decisions with
      a `change-request` id; no defect that breaks a current acceptance criterion was closed as
      rejected, out of scope or an enhancement.
- [ ] Every QA and QC activity appears in the schedule and the cost baseline.

## Anti-patterns
- Treating QA as "the testers": all detection, no prevention, so the process that made the
  defects never changes.
- "Looks good to me" sign-offs with no written, testable criteria.
- Using the sprint review as the quality gate: undone work is demonstrated and "accepted with
  conditions" instead of being returned as not done (Helios audit QA-03).
- A DoD that lives on a wiki and is skipped at crunch time, or whose lines nobody can check
  ("code is clean").
- Gates that always pass, or routine waivers with no risk id or expiry: that is theatre, not a gate.
- Reclassifying defects as enhancements or "out of scope" to pass a gate; confusing low grade (few
  features) with low quality (defects).
- Accepting evidence from stubs, mocks or stale test data as proof that a criterion is met.
- Gold-plating: quality nobody asked for, paid for in scope or schedule.
- Using defect counts to rate individuals: people stop logging defects and the metrics go blind.
- Testing quality in at the end: one big test phase and nothing before it.

## Resources
- `references/acceptance-criteria.md` — who captures criteria at each level, Given/When/Then and
  checklist styles with Helios examples, making criteria measurable, the SMART-style checks
  (INVEST is for stories), non-functional criteria, and the criteria review checklist.
- `references/quality-gates.md` — entry and exit criteria, gate levels, the agile gate (the DoD,
  not the sprint review), the Helios gates, outcomes and waiver limits, cost of quality with the
  Helios balance, and quality vs grade with its verifiable rule.
- `references/assurance-and-control.md` — QA vs QC vs scope validation, running a process audit,
  running QC, the severity scale and defect lifecycle, the metrics catalog with formulas, the
  Helios pilot DRE worked example, and root-cause tools.
- `assets/quality-plan-template.md` — fill-in quality management plan (`<placeholders>`): floors,
  metrics, roles, cost of quality, criteria, DoD and gates, cadence, defects, gate decision record.
- `assets/quality-plan-sample.md` — sample: the Helios quality plan v1.3 as at gate G4 on
  2026-09-29, with decisions for gates G1–G4.
- `assets/definition-of-done.md` — fill-in Definition of Done template with rules for using it.
- `assets/definition-of-done-sample.md` — sample: Helios DoD v1.2 with its version history.
- `assets/defect-log-template.csv` — fill-in defect log; columns `id, title, severity, status,
  stage_found, found_by, found_date, wbs_id, req_id, owner, root_cause, fix_ref, closed_date`.
- `assets/defect-log-sample.csv` — sample: a 13-defect Helios extract from system test to GA,
  including pilot escapes, a rejected report and the three severity-3 defects open at the go/no-go.
- `assets/quality-audit-log-template.csv` — fill-in process audit log; columns `audit_id, date,
  process_area, check, sample, result, finding, action, owner, due, status, closed`.
- `assets/quality-audit-log-sample.csv` — sample: Helios process audits QA-01 to QA-06.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-planning` — takes the quality plan into the integrated plan and puts every gate,
  review, test and audit specified here into the schedule and cost baseline.
- `work-breakdown-structure` — supplies the deliverables and work packages this skill attaches
  criteria to; its WBS dictionary records each package's acceptance criterion, and test work sits
  in packages such as Helios 1.4.1 System & UAT testing.
- `agile-delivery` — applies this skill's Definition of Done as the gate for every story and writes
  story-level Given/When/Then criteria to its standard; its sprint reviews inspect only done work.
- `scope-and-requirements` — captures each requirement's acceptance test in the RTM to the standard
  set here, and runs scope validation on the deliverables this skill's quality control has verified.
- `release-and-cutover` — runs the go/no-go, cutover and hypercare, taking the last quality gate's
  evidence (open defects by severity, UAT, performance, security, accessibility) as its
  test-readiness criteria, on the same severity scale.
