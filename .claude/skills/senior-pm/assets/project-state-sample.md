# Project-state canvas — SAMPLE: Helios at the end of month 3

Sample only: a filled copy of `project-state-template.md` for the sample Helios project (a
fictional customer self-service portal used throughout this catalog). Every name and number
is fictional and follows the catalog's Helios canon; do not copy it into a real project. The
numbers come from the bundled samples (commands in section 2) and match the weekly status
report of the same date (`status-report-sample.md` in `status-report`).

As of: 2026-07-10, the week after the month-3 close (earned value as at 2026-07-03; change,
issue and sprint data to 2026-07-10) · Filled by: Sam Lee (project manager)

## 1. Canvas (the one table)

| Stage | Baseline exists? (scope / schedule / cost) | RAG (overall + worst dimension) | Top risk or issue | Next decision (who, by when) |
|---|---|---|---|---|
| Delivery (M1 "Discovery complete" met on 2026-05-08; M4 "MVP live to pilot" next: forecast 2026-08-14, and M6 general availability 2026-10-10, each one week late) | approved / approved / approved | AMBER, worst: schedule (SPI 0.92), direction worsening | R001 identity-provider integration slip (risk owner Sam Lee) has materialised as issue I001: IdentityCo's sandbox was down from 2026-06-12 to 2026-07-06 and SSO is not yet working in test (issue owner Carla Diaz, due 2026-07-17); work package 1.3.1 Identity / SSO integration is RED | DEC002: approve IdentityCo's recovery plan and decide how to fund the forecast overrun, which is about $10,000 beyond the management reserve — decider Dana Okoro — steering committee 2026-07-14 |

Context:
- Outcome and measure: cut password-reset and order-status tickets by 50% within 6 months of
  launch, against the 3-month pre-launch monthly volume; benefit owner Priya Nair.
- Sponsor / project manager: Dana Okoro, VP Customer Operations / Sam Lee.
- Approach: hybrid — signal: the 6-month date and the $500,000 BAC are fixed, while the UX
  and knowledge-base content are learned in two-week sprints.
- Hard constraints: GA at M6; total budget $525,000 (BAC $500,000 + $25,000 management
  reserve held by the sponsor); customer data stays in the approved region.

## 2. Health against the baseline

| Dimension | Baseline (approved) | Position now / forecast | Measure | RAG | Source |
|---|---|---|---|---|---|
| Scope | Scope statement signed by Dana Okoro at M1; SSO is in the baseline | CR003 accessibility uplift approved ($12,000 from contingency); CR002 partner-login SSO pending ($18,000, 10 days; CCB 2026-07-14); the $20,000 SSO crash option (ACT004) goes to steering with DEC002 | Committed + pending $30,000 against the $40,000 contingency ($28,000 undrawn); with the crash option, $38,000 asked | AMBER | `change_impact.py` on the change log |
| Schedule | Critical path A → B → D → G → H → J = 25 weeks (2026-04-06 to 2026-09-25, then the cutover week); milestones M1 2026-05-08, M4 2026-08-07, M6 2026-10-03; no schedule reserve before GA, accepted by the sponsor (27% chance of GA readiness by week 26; the 2-week M6 tolerance covers about P75) | SSO working in test two weeks late (baseline 2026-07-03, forecast 2026-07-17), so task C finishes 2026-07-24, 1 week past its late finish of 2026-07-17; M4 forecast 2026-08-14 and M6 2026-10-10 (+1 week each), inside the 2-week tolerance; after sprint S4, 149 points left and 6 sprints left: likely 6, pessimistic 7 | SPI 0.92 (1.3.1 at 0.75); release outlook AMBER | AMBER | `critical_path.py`, `health_check.py`, `velocity_forecast.py` |
| Cost | BAC $500,000, including the $40,000 contingency; $25,000 management reserve above BAC | AC $252,000; EAC ≈ $535,000. BAC already contains the contingency, so the forecast has used all of it and overruns BAC by about $35,000, about $10,000 more than the management reserve: a sponsor decision | CPI 0.93 (1.07 → 1.00 → 0.93), VAC ≈ -$35,000, TCPI 1.07 | AMBER | `health_check.py` |
| Risk | Contingency $40,000, about P50 of a simulation of the residual register (P80 $99,000; the $52,300 summed residual EMV is the mean, not the reserve); the sponsor accepted the gap to P80 | R001 (HIGH, EMV $48,000) has occurred; every HIGH/MEDIUM risk has an owner and a response | $12,000 of contingency drawn (CR003) and $28,000 undrawn, but the cost forecast already needs all of it | AMBER | `risk_score.py --check` |
| Quality | Definition of done; quality gates per sprint | No gate failed; I003 (stale QA data, 2 days overdue) makes test results unreliable; ACT003 (real-provider journey tests) blocked until SSO works in test | 1 overdue and 1 blocked item the M4 gate depends on | AMBER | `issue_log_check.py` |

Overall AMBER: no dimension is RED, but every dimension is AMBER, schedule and cost are below
0.95 and worsening, and work packages 1.3.1 Identity / SSO integration and 1.3.4 Reporting &
analytics (a small budget) are RED.

Commands that produced these numbers (run from the repository root):
- `python .claude/skills/project-schedule/scripts/critical_path.py .claude/skills/project-schedule/assets/schedule-sample.csv --unit weeks --start-date 2026-04-06 --workdays --simulate 10000 --seed 42 --target 26` (the baseline dates, task C's float and the 27%)
- `python .claude/skills/cost-management/scripts/health_check.py .claude/skills/cost-management/assets/evm-snapshot.csv`
- `python .claude/skills/cost-management/scripts/health_check.py .claude/skills/cost-management/assets/evm-history-sample.csv` (the CPI and SPI trends)
- `head -5 .claude/skills/agile-delivery/assets/sprint-history-sample.csv | python .claude/skills/agile-delivery/scripts/velocity_forecast.py - --remaining 149 --sprints-left 6` (sprints S1-S4 only; the bundled history runs on to S6, ending 2026-07-31. 149 = 137 left after S4 + CR003's 12 points, which the history adds only in the S5 row, so the script's 'reconcile' note is expected)
- `python .claude/skills/risk-register/scripts/risk_score.py .claude/skills/risk-register/assets/risk-register-template.csv --check`
- `python .claude/skills/change-request/scripts/change_impact.py .claude/skills/change-request/assets/change-log.csv --reserve-cost 40000` (the bundled log runs to 2026-07-21: on 2026-07-10 only CR002 was pending, since CR004 was raised on 2026-07-14 and CR006 on 2026-07-21)
- `python .claude/skills/project-delivery/scripts/issue_log_check.py .claude/skills/project-delivery/assets/issue-log-sample.csv --as-of 2026-07-10`

## 3. Artifact checklist by stage

| Stage | Artifact | Owning skill | Exists? | Approved (date) |
|---|---|---|---|---|
| Initiation | Business case and benefits register | `business-case` | yes | 2026-03-20 |
| Initiation | Signed charter | `project-charter` | yes | 2026-04-02 |
| Initiation | Stakeholder register and engagement strategy | `stakeholder-management` | yes | 2026-04-15 |
| Initiation | Kickoff held, decisions and actions recorded | `project-initiation`, `meeting-management` | yes | 2026-04-07 |
| Planning | Scope statement and requirements traceability matrix | `scope-and-requirements` | yes | M1 |
| Planning | WBS and WBS dictionary | `work-breakdown-structure` | yes | M1 |
| Planning | Estimates with basis of estimate | `estimation` | yes | M1 |
| Planning | Schedule baseline and critical path | `project-schedule` | yes | M1 |
| Planning | Resource plan and capacity check | `resource-management` | yes (levelled before M1: 34 hours moved to Ben Adeyemi and Elena Rossi; Carla Diaz's remaining 6 knowledge-base hours smoothed into W9–W10 inside task E's window; gate passed) | M1 |
| Planning | RACI | `raci-matrix` | yes | M1 |
| Planning | Cost baseline with contingency and management reserve | `cost-management` | yes | M1 |
| Planning | Risk register with owners and responses | `risk-register`, `risk-management` | yes | M1 |
| Planning | Definition of done, acceptance criteria, quality gates | `quality-management` | yes | M1 |
| Planning | Communication plan | `project-communication` | yes | M1 |
| Planning | Change control process and thresholds | `change-management` | yes | M1 |
| Planning | Procurement plan and contracts | `procurement-management` | yes (IdentityCo, firm fixed price) | M1 |
| Planning | Ordered backlog and definition of ready | `agile-delivery` | yes | M1 |
| Planning | Assumptions and constraints log | `project-planning` | yes (A1 validated in W6: integration spike A01 passed on the IdentityCo sandbox, the charter's week-6 check) | M1 |
| Planning | Project management plan; baseline approved | `project-planning` | yes | M1 (2026-05-08) |
| Delivery | Issue log: issues, actions, decisions and dependencies | `project-delivery` | yes | ongoing |
| Delivery | Weekly status report | `status-report` | yes | weekly (latest 2026-07-10) |
| Delivery | Change log with decisions | `change-request` | yes | ongoing |
| Delivery | Go/no-go checklist, cutover runbook, hypercare plan | `release-and-cutover` | partly — release strategy set at M1 (pilot at M4, GA flag ramp); the M4 pilot go/no-go has its decision rights in the DACI and its evidence gate G3 in `quality-management`; the GA checklist, runbook and hypercare plan start no later than six weeks (T-6) before the 2026-10-03 cutover | M1 (strategy) |
| Closure | (not yet due) | `project-closure` | n.a. | — |

## 4. Gaps and routing (at most two routes)

| # | Gap | Route to | First action | Artifact expected | Owner | By |
|---|---|---|---|---|---|---|
| 1 | SSO vendor slip threatens the M4 pilot and, with no schedule reserve before GA, M6 | `procurement-management` | Hold IdentityCo to its dated recovery plan under the contract remedies (SSO working in test by 2026-07-17) | Updated vendor register and recovery milestone | Sam Lee | 2026-07-14 |
| 2 | TCPI 1.07 exceeds CPI 0.93 by more than 0.10; the EAC of about $535,000 has used the whole contingency and overruns BAC by about $35,000, about $10,000 beyond the $25,000 management reserve | `cost-management` | Re-forecast the EAC and prepare the sponsor's options: draw the management reserve, fund the remaining gap, or trade scope through change control | Revised forecast and a funding request through change control | Sam Lee | 2026-07-14 |
