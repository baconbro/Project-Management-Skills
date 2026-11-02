# Helios walkthrough — one project from idea to closure

This is the catalog's worked example. It follows the sample Helios project (a fictional
customer self-service portal used throughout this catalog) through initiation, planning,
delivery and closure, and at each step names the user's ask, the skill that answers it, the
artifact it leaves behind and the helper command that produced the numbers. Every person,
vendor and figure is fictional. Run the commands from the repository root: they read the
bundled Helios samples and print the results quoted here. Files named `*-sample.*` hold the
filled Helios data; `*-template.*` files and the other blanks named below are what you copy.
For a real project, copy the matching template and point the same command at your own file.

How to use it: read it once end to end to see how the 27 skills fit together, or jump to the
stage the user is in. Hand the user one or two skills at a time, not this whole page.

## The project at a glance

| Item | Helios |
|---|---|
| Problem | 40% of support tickets are password resets and order-status questions (about $600k a year to handle) |
| Objective | Cut those two ticket types by 50% within 6 months of launch, against the 3-month pre-launch monthly volume |
| Sponsor / PM | Dana Okoro, VP Customer Operations / Sam Lee |
| Team | Ava Chen (product owner), Ben Adeyemi (tech lead), Carla Diaz (backend), Devin Patel (frontend), Elena Rossi (UX), Frank Müller (QA) |
| Key stakeholders | Priya Nair (Head of Support Operations, benefit owner), Marcus Webb (Security lead), Hana Sato (Legal & Compliance), Finance (budget holder), 200 pilot customers |
| Money | Charter range $450k-$550k; BAC $500,000 including $40,000 contingency; $25,000 management reserve above BAC |
| Time | 6 months: Discovery complete M1, MVP live to pilot M4, general availability M6 |
| Cadence | Daily stand-up, weekly status report, bi-weekly steering committee, two-week sprints |
| Approach | Hybrid |

## Stage 0 — Triage (`senior-pm`)

**Ask:** "I've been asked to launch a customer self-service portal. Where do I start?"

- **Canvas** (`.claude/skills/senior-pm/assets/project-state-template.md`): stage *idea*;
  baseline none / none / none; RAG *unknown — no baseline*; top risk *integration with the
  identity provider*; next decision *is this worth funding? — Dana Okoro*.
- **Methodology:** the checklist in `methodology-selection.md` scores 4 Yes (requirements will
  change as pilot customers react, early delivery is valuable, increments are cheap, there is
  a product owner) and 1 No (the identity contract makes some change costly). The fixed
  six-month date and budget override that to **hybrid**.
- **Route:** `project-initiation`, starting with `business-case`.

## Stage 1 — Initiation

**1.1 Is it worth it?** — `business-case`
- Artifacts: the Helios figures are in `.claude/skills/business-case/assets/cashflows.csv`
  (the recommended option), `.claude/skills/business-case/assets/cashflows-options-sample.csv`
  (all four options) and `.claude/skills/business-case/assets/benefits-register-sample.csv`;
  the document is written in the blank
  `.claude/skills/business-case/assets/business-case-template.md`.
- Commands:
  ```bash
  python .claude/skills/business-case/scripts/roi_npv.py .claude/skills/business-case/assets/cashflows-options-sample.csv
  python .claude/skills/business-case/scripts/roi_npv.py .claude/skills/business-case/assets/cashflows.csv --all
  ```
- Result: the recommended option ranks first on NPV ($196,173.88 at 10%) against the
  alternative ($79,709.22), do minimum ($35,815.74) and do nothing; IRR 23.61%, payback 2.85
  periods (3.47 discounted); benefits can fall 28.18% before NPV reaches zero. Dana Okoro
  approves funding in the $450k-$550k range.

**1.2 Authorize the project** — `project-charter`
- Artifact: `.claude/skills/project-charter/assets/charter-sample.md` (charter v1.0, signed
  by Dana Okoro on 2026-04-02; the blank is `charter-template.md`). No helper.
- Result: sponsor Dana Okoro and PM Sam Lee named; the SMART objective above; in scope
  password reset, order status, knowledge base and single sign-on through the existing
  identity provider; live chat out of scope (phase 2 candidate), as are partner-login SSO and
  non-English knowledge base; milestones M1, M4, M6; budget $450k-$550k.

**1.3 Who is affected?** — `stakeholder-management`
- Artifacts: `.claude/skills/stakeholder-management/assets/stakeholder-register-sample.csv`
  (S01-S10), `.claude/skills/stakeholder-management/assets/engagement-matrix-sample.md`
  (current versus desired engagement, 2026-04-15); the blanks are `stakeholder-register.csv`
  and `engagement-matrix.md`. No helper.
- Result: Dana Okoro, Priya Nair (benefit owner) and IdentityCo managed closely; Marcus Webb,
  Hana Sato and Finance kept satisfied with sign-off gates and budget; the 200 pilot
  customers and the support agents (currently resistant) kept informed.

**1.4 Kick off** — `project-initiation` with `meeting-management`
- Artifacts: `.claude/skills/project-initiation/assets/initiation-gate-record-sample.md` (the
  G0 record), `.claude/skills/project-initiation/assets/kickoff-deck-sample.md` (the kickoff
  of 2026-04-07; slide 11 holds the decisions and actions captured in the room); the blanks
  are `initiation-gate-record.md` and `kickoff-deck-outline.md`. The meeting itself is run
  with the blank `.claude/skills/meeting-management/assets/agenda-template.md` and
  `.claude/skills/meeting-management/assets/action-items.csv`. No helper.
- Gate: G0 verdict *Go with conditions* from Dana Okoro on 2026-04-06 (e.g. C1: Priya Nair
  signs off the benefit baseline method), conditions due by the baseline approval → planning.
  Canvas: stage *planning*; baseline none; next decision *approve the baseline at M1*.

## Stage 2 — Planning (`project-planning` orchestrates)

**2.1 What exactly is in scope?** — `scope-and-requirements`
- Artifacts: `.claude/skills/scope-and-requirements/assets/scope-statement-sample.md`,
  `.claude/skills/scope-and-requirements/assets/requirements-traceability-sample.csv`. No helper.
- Result: requirements prioritized with MoSCoW and traced to objectives, WBS ids and tests;
  SSO is in the baseline; live chat is a Won't with its destination (phase 2). Dana Okoro
  signs the scope statement at M1.

**2.2 Break the scope down** — `work-breakdown-structure`
- Artifact: `.claude/skills/work-breakdown-structure/assets/wbs-sample.csv`.
- Command:
  ```bash
  python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py .claude/skills/work-breakdown-structure/assets/wbs-sample.csv --budget 500000
  ```
- Result: PASS, the 100% rule holds at all 5 parents; the $500,000 is allocated by weight to
  the control accounts (1.3.1 Identity / SSO integration $78,750, 1.4.1 System & UAT testing
  $70,000, 1.3.2 Self-service UI $67,500, ...).

**2.3 Build or buy?** — `procurement-management`
- Artifacts: `.claude/skills/procurement-management/assets/vendor-scorecard-sample.csv`,
  `.claude/skills/procurement-management/assets/statement-of-work-template.md`,
  `.claude/skills/procurement-management/assets/vendor-register-sample.csv`. No helper.
- Result: buy customer sign-in on the existing identity provider and build the integration
  in-house; IdentityCo scores 80.1 against 73.5 and 66.0 and is contracted on a firm fixed
  price with retention.

**2.4 How much effort, and how sure are we?** — `estimation`
- Artifacts: `.claude/skills/estimation/assets/estimation-worksheet-sample.csv` (effort),
  `.claude/skills/estimation/assets/duration-worksheet-sample.csv` (durations for the schedule).
- Command:
  ```bash
  python .claude/skills/estimation/scripts/pert_estimate.py .claude/skills/estimation/assets/estimation-worksheet-sample.csv --confidence 0.8
  ```
- Result: expected effort 451.83 person-days, P80 468.63 (a 16.80-day reserve); 1.3.1
  Identity / SSO integration drives 39.2% of the variance, so it is de-risked first.

**2.5 How long will it take?** — `project-schedule`
- Artifact: `.claude/skills/project-schedule/assets/schedule-sample.csv`.
- Command:
  ```bash
  python .claude/skills/project-schedule/scripts/critical_path.py .claude/skills/project-schedule/assets/schedule-sample.csv --unit weeks --near-critical 1
  ```
- Result: critical path A → B → D → F → G → H → J = 18 weeks to operational handover, with
  the M4 pilot after hardening and launch; C (SSO integration) has 1 week of float, E 3, I 1.

**2.6 Do we have the people?** — `resource-management`
- Artifacts: `.claude/skills/resource-management/assets/resource-allocation-sample.csv`,
  `.claude/skills/resource-management/assets/team-charter-template.md`.
- Command:
  ```bash
  python .claude/skills/resource-management/scripts/capacity_check.py .claude/skills/resource-management/assets/resource-allocation-sample.csv --level
  ```
- Result: Carla Diaz is OVER in W6-W8 (peak 125% in W7) and Devin Patel in W7-W8; leveling
  moves 34 hours to Ben Adeyemi and Elena Rossi, leaving 6 hours above Carla's capacity to
  re-sequence within float. Carla is a key-person risk (only backend engineer).

**2.7 Who is accountable?** — `raci-matrix`
- Artifacts: `.claude/skills/raci-matrix/assets/raci-sample.csv`,
  `.claude/skills/raci-matrix/assets/daci-decisions-sample.csv`.
- Command:
  ```bash
  python .claude/skills/raci-matrix/scripts/raci_validate.py .claude/skills/raci-matrix/assets/raci-sample.csv
  ```
- Result: PASS — every activity has exactly one Accountable and at least one Responsible.

**2.8 What could go wrong?** — `risk-management` for the process, `risk-register` for the register
- Artifacts: `.claude/skills/risk-register/assets/risk-register-template.csv` (holds the
  Helios register); `.claude/skills/risk-management/assets/risk-management-plan-sample.md`
  (scales, appetite, thresholds, approved at M1) and
  `.claude/skills/risk-management/assets/risk-response-plan-sample.csv` (response actions
  such as A01, the week-1 integration spike for R001); identification uses the blank
  `.claude/skills/risk-management/assets/risk-workshop-template.md`.
- Command:
  ```bash
  python .claude/skills/risk-register/scripts/risk_score.py .claude/skills/risk-register/assets/risk-register-template.csv --check
  ```
- Result: R001 identity-provider integration slips is HIGH (0.4 x $120,000 = EMV $48,000);
  total threat EMV $94,300, reduced to $52,300 by the planned responses; R006 is an
  opportunity (EMV $18,000); the check PASSes (every HIGH and MEDIUM risk has an owner,
  response and trigger).

**2.9 What will it cost?** — `cost-management`
- Artifact: `.claude/skills/cost-management/assets/cost-baseline-template.csv` (time-phased
  by month). The allocation comes from the `--budget` run in 2.2.
- Result: cost baseline (BAC) $500,000 = $460,000 of work + $40,000 contingency inside BAC.
  The contingency is about P50 of a simulation of the residual register (P80 $99,000; the
  $52,300 summed residual EMV is the mean, not the reserve); the sponsor accepted the gap to
  P80. The sponsor holds $25,000 management reserve above BAC; total budget $525,000, inside
  the charter range.

**2.10 Quality, communication and change control** — `quality-management`,
`project-communication`, `change-management`
- Quality artifacts: `.claude/skills/quality-management/assets/quality-plan-sample.md` (v1.0
  approved at M1, shown as at the GA gate),
  `.claude/skills/quality-management/assets/definition-of-done-sample.md`,
  `.claude/skills/quality-management/assets/defect-log-sample.csv` and
  `.claude/skills/quality-management/assets/quality-audit-log-sample.csv` (filled through
  delivery); the blanks are `quality-plan-template.md`, `definition-of-done.md`,
  `defect-log-template.csv` and `quality-audit-log-template.csv`.
- Communication artifacts:
  `.claude/skills/project-communication/assets/communication-plan-sample.csv` (C01-C19),
  `.claude/skills/project-communication/assets/communication-review-log-sample.csv`, and the
  blank `.claude/skills/project-communication/assets/escalation-ladder-template.md`; the
  blank plan and review log are `communication-plan.csv` and `communication-review-log.csv`.
- Change-control artifacts:
  `.claude/skills/change-management/assets/change-control-plan-sample.md` (approved with the
  baseline at M1) and, for adoption,
  `.claude/skills/change-management/assets/adoption-plan-sample.md`; the blanks are
  `change-control-plan-template.md` and `adoption-plan-template.md`. No helper.
- Result: quality objectives, a definition of done and gate exit criteria; weekly status,
  bi-weekly steering and daily stand-up; approval tolerances: the PM decides LOW-band changes
  up to $5,000 and 2 working days, the CCB (chaired by Dana Okoro) decides the rest within the
  remaining contingency, and the sponsor decides HIGH-band changes, any use of management
  reserve and any move of M6.

**2.11 Backlog for the iterative part** — `agile-delivery`
- Artifacts: `.claude/skills/agile-delivery/assets/product-backlog-sample.csv` (the blank is
  `product-backlog-template.csv`), `.claude/skills/agile-delivery/assets/sprint-plan-template.md`.
- Helper: `velocity_forecast.py` needs completed sprints, so it first runs in delivery (step
  3.1) on `.claude/skills/agile-delivery/assets/sprint-history-sample.csv`:
  ```bash
  python .claude/skills/agile-delivery/scripts/velocity_forecast.py .claude/skills/agile-delivery/assets/sprint-history-sample.csv --backlog .claude/skills/agile-delivery/assets/product-backlog-sample.csv --sprints-left 4
  ```
- Result: an ordered backlog with MoSCoW priorities and a definition of ready; two-week
  sprints under the milestones, starting with S1 on 2026-05-11.

**2.12 Approve the baseline** — `project-planning`
- Artifacts: `.claude/skills/project-planning/assets/project-management-plan-sample.md` (the
  filled Helios plan; the blank is `project-management-plan.md`),
  `.claude/skills/project-planning/assets/assumptions-log-sample.csv` (e.g. A1: the existing
  identity provider supports customer logins without a licence upgrade, owner Ben Adeyemi).
  No helper; it reconciles the outputs of 2.1-2.11.
- Gate: Dana Okoro approves scope, schedule and cost baselines at M1. Canvas: stage
  *delivery*; baseline approved / approved / approved; RAG GREEN at the start.

## Stage 3 — Delivery (`project-delivery` runs the control loop)

**3.1 Are the sprints on course?** — `agile-delivery`
- Artifact: `.claude/skills/agile-delivery/assets/sprint-history-sample.csv` (sprints S1-S6,
  the last ending 2026-07-31, so this reading is a month later than the month-3 snapshot in
  3.2; at the 2026-07-10 status report, after S4, it was 149 points and 6 sprints left, likely
  6, pessimistic 7, also AMBER).
- Command:
  ```bash
  python .claude/skills/agile-delivery/scripts/velocity_forecast.py .claude/skills/agile-delivery/assets/sprint-history-sample.csv --backlog .claude/skills/agile-delivery/assets/product-backlog-sample.csv --sprints-left 4
  ```
- Result: velocity 22-31 (mean 27.33, trailing-3 28.00); 100 points left; 4 sprints likely,
  5 pessimistic against 4 available → release outlook AMBER; at the pessimistic velocity the
  cut line falls after HEL-170, so GA commits to the Must and Should items.

**3.2 Is it on budget and on time? (end of month 3)** — `cost-management`
- Artifacts: `.claude/skills/cost-management/assets/evm-snapshot.csv`,
  `.claude/skills/cost-management/assets/evm-history-sample.csv`.
- Command:
  ```bash
  python .claude/skills/cost-management/scripts/health_check.py .claude/skills/cost-management/assets/evm-snapshot.csv
  ```
- Result: PV $255,000, EV $235,500, AC $252,000 → CPI 0.93, SPI 0.92 → **AMBER**; EAC
  ≈ $535,000, VAC ≈ -$35,000; TCPI 1.07 is more than 0.10 above the CPI, so the tool says
  re-plan or re-baseline. 1.3.1 Identity / SSO integration is the RED work package (CPI 0.69,
  SPI 0.75, the vendor slip); Reporting & analytics is also below the band on a small budget.
  Run the same command on `evm-history-sample.csv` for the trend: CPI 1.05 → 1.00 → 0.93.

**3.3 Log the problem** — `project-delivery`
- Artifact: `.claude/skills/project-delivery/assets/issue-log-sample.csv` (14 issues,
  actions, decisions and dependencies; the blank is `issue-log.csv`).
- Command:
  ```bash
  python .claude/skills/project-delivery/scripts/issue_log_check.py .claude/skills/project-delivery/assets/issue-log-sample.csv --as-of 2026-07-10
  ```
- Result: PASS, 9 of 14 items open. Issue I001 (IdentityCo's sandbox down from 2026-06-12,
  blocking SSO integration testing; owner Carla Diaz, due 2026-07-17) means R001 has
  materialised; I001 and decision DEC002 go to the 2026-07-14 steering committee; I003 (stale
  QA data) is 2 days overdue and ACT003 (real-provider journey tests) is blocked.

**3.4 The vendor is late** — `procurement-management`
- Artifact: `.claude/skills/procurement-management/assets/vendor-register-sample.csv`. No helper.
- Result: "SSO working in test" is two weeks late; the contract's delay credit is claimed and
  IdentityCo commits to a dated recovery plan.

**3.5 Changes are piling up** — `change-request`, governed by `change-management`
- Artifacts: `.claude/skills/change-request/assets/change-log.csv`,
  `.claude/skills/change-request/assets/change-request-sample.md`.
- Command:
  ```bash
  python .claude/skills/change-request/scripts/change_impact.py .claude/skills/change-request/assets/change-log.csv --reserve-cost 40000
  ```
- Result (the log as at 2026-07-21; CR004 was raised on 2026-07-14 and CR006 on 2026-07-21):
  CR002 (extend SSO to partner logins) scores 3.40 MEDIUM and goes to the CCB, which asks for
  more information on 2026-07-14; CR003 (WCAG 2.2 AA uplift) is approved for $12,000 from
  contingency; CR006 (pilot cohort 200 → 50) is LOW and within the PM's tolerance; CR001
  (live chat) is deferred to phase 2. Committed + pending changes would use 105% of the
  $40,000 contingency — on top of a cost forecast that already needs all of it (step 3.2).

**3.6 Report and decide** — `status-report`, then `meeting-management`
- Artifacts: `.claude/skills/status-report/assets/status-report-sample.md` (the weekly
  report of 2026-07-10) and `.claude/skills/status-report/assets/rag-history-sample.csv` (the
  ratings behind its trend arrows); the blanks are `status-report-template.md` and
  `rag-history-template.csv`. For the steering committee of 2026-07-14:
  `.claude/skills/meeting-management/assets/agenda-sample.md`,
  `.claude/skills/meeting-management/assets/action-items-sample.csv` and
  `.claude/skills/meeting-management/assets/decision-log-sample.csv` (the blanks are
  `agenda-template.md`, `action-items.csv` and `decision-log.csv`). No helper.
- Result: the weekly report is AMBER overall (schedule, cost, scope and quality AMBER;
  1.3.1 Identity / SSO integration RED; direction worsening). BAC already includes the
  $40,000 contingency, so an EAC of about $535,000 means the forecast has used all of it;
  the roughly $35,000 overrun exceeds the $25,000 management reserve by about $10,000, which
  only the sponsor can decide. The report asks the steering committee for that decision
  (DEC002: approve the SSO recovery plan and how to fund the overrun) and for a priority
  between protecting M4 and adding partner logins (CR002).

**3.7 Re-triage** — `senior-pm`
- Artifact: `.claude/skills/senior-pm/assets/project-state-sample.md` (the canvas as at
  2026-07-10, the week after the month-3 close; the blank is `project-state-template.md`).
- Result: stage delivery, baselines approved, AMBER, top issue I001 / R001, next decision at
  the 2026-07-14 steering committee; routes to `procurement-management` and `cost-management`.

**3.8 Go live** — `release-and-cutover`
- Artifacts: `.claude/skills/release-and-cutover/assets/go-no-go-checklist.md`,
  `.claude/skills/release-and-cutover/assets/cutover-runbook-sample.csv`,
  `.claude/skills/release-and-cutover/assets/hypercare-plan-template.md`. No helper.
- Result: a pilot at M4, then GA at M6 by a feature-flag ramp (25% → 50% → 100%); the GA
  go/no-go returns CONDITIONAL GO with owned, dated conditions; the rehearsed runbook carries
  verifications and rollback triggers; hypercare runs to measured exit criteria before the
  service is handed to Support Operations.

## Stage 4 — Closure (`project-closure`)

**4.1 Accept and hand over** — `project-closure` (with `scope-and-requirements` for scope validation)
- Artifact: `.claude/skills/project-closure/assets/closure-report.md`. No helper.
- Result: deliverables accepted against the signed scope statement; the service handed to
  operations and the benefits to Priya Nair; final cost against BAC and the reserve drawdown
  explained in the closure report.

**4.2 Close the contracts** — `procurement-management`
- Artifact: `.claude/skills/procurement-management/assets/vendor-register-sample.csv` (status
  closed). Retention is released once acceptance and the warranty period are complete.

**4.3 Learn** — `lessons-learned`
- Artifact: `.claude/skills/lessons-learned/assets/lessons-learned.csv`. No helper.
- Result: lessons with owners and dates, e.g. give vendor onboarding a named owner in the
  plan; report AMBER the moment a milestone is threatened.

**4.4 Track the benefits** — `business-case`
- Artifact: `.claude/skills/business-case/assets/benefits-register-sample.csv`.
- Result: Priya Nair measures the two ticket types monthly against the 3-month pre-launch
  baseline; the 50% target is reviewed 6 months after launch.

## Asset map — which step uses which file

| Skill | Files (under `.claude/skills/<skill>/assets/`) | Step |
|---|---|---|
| `senior-pm` | `project-state-template.md`, `project-state-sample.md` | 0, 3.7 |
| `business-case` | `business-case-template.md`, `cashflows.csv`, `cashflows-options-sample.csv`, `benefits-register-sample.csv` | 1.1, 4.4 |
| `project-charter` | `charter-template.md` | 1.2 |
| `stakeholder-management` | `stakeholder-register.csv`, `engagement-matrix.md` | 1.3 |
| `project-initiation` | `kickoff-deck-outline.md` | 1.4 |
| `meeting-management` | `agenda-template.md`, `action-items.csv` | 1.4, 3.6 |
| `scope-and-requirements` | `scope-statement-template.md`, `scope-statement-sample.md`, `requirements-traceability-template.csv`, `requirements-traceability-sample.csv` | 2.1, 4.1 |
| `work-breakdown-structure` | `wbs-template.md`, `wbs-template.csv`, `wbs-sample.csv` | 2.2 |
| `procurement-management` | `statement-of-work-template.md`, `vendor-scorecard-template.csv`, `vendor-scorecard-sample.csv`, `vendor-onboarding-checklist.md`, `vendor-register-template.csv`, `vendor-register-sample.csv` | 2.3, 3.4, 4.2 |
| `estimation` | `estimation-worksheet-template.csv`, `estimation-worksheet-sample.csv`, `duration-worksheet-sample.csv` | 2.4 |
| `project-schedule` | `schedule-template.csv`, `schedule-sample.csv` | 2.5 |
| `resource-management` | `resource-allocation-template.csv`, `resource-allocation-sample.csv`, `team-charter-template.md` | 2.6 |
| `raci-matrix` | `raci-template.md`, `raci-template.csv`, `raci-sample.csv`, `daci-decisions-sample.csv` | 2.7 |
| `risk-register` | `risk-register-template.csv` | 2.8 |
| `cost-management` | `cost-baseline-template.csv`, `evm-snapshot.csv`, `evm-history-sample.csv` | 2.9, 3.2 |
| `quality-management` | `definition-of-done.md` | 2.10 |
| `project-communication` | `communication-plan.csv` | 2.10 |
| `agile-delivery` | `product-backlog-template.csv`, `product-backlog-sample.csv`, `sprint-plan-template.md`, `sprint-history-sample.csv` | 2.11, 3.1 |
| `project-planning` | `project-management-plan.md`, `project-management-plan-sample.md`, `assumptions-log.csv`, `assumptions-log-sample.csv` | 2.12 |
| `project-delivery` | `issue-log.csv` | 3.3 |
| `change-request` | `change-request-template.md`, `change-request-sample.md`, `change-log.csv` | 3.5 |
| `status-report` | `status-report-template.md`, `status-report.csv` | 3.6 |
| `release-and-cutover` | `go-no-go-checklist.md`, `cutover-runbook-template.csv`, `cutover-runbook-sample.csv`, `hypercare-plan-template.md` | 3.8 |
| `project-closure` | `closure-report.md` | 4.1 |
| `lessons-learned` | `lessons-learned.csv` | 4.3 |

Skills with no asset of their own in this walk: `risk-management` (process, step 2.8),
`change-management` (thresholds and CCB, steps 2.10 and 3.5). File names can change between
catalog versions; `ls .claude/skills/<skill>/assets/` is authoritative.
