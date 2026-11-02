# Project-state canvas — SAMPLE: Helios at the end of month 3

Sample only: a filled copy of `project-state-template.md` for the sample Helios project (a
fictional customer self-service portal used throughout this catalog). Every name and number
is fictional and follows the catalog's Helios canon; do not copy it into a real project. The
numbers come from the bundled samples (commands in section 2).

As of: end of month 3 of 6 · Filled by: Sam Lee (project manager)

## 1. Canvas (the one table)

| Stage | Baseline exists? (scope / schedule / cost) | RAG (overall + worst dimension) | Top risk or issue | Next decision (who, by when) |
|---|---|---|---|---|
| Delivery (M1 "Discovery complete" met; M4 "MVP live to pilot" next) | approved / approved / approved | AMBER, worst: schedule (SPI 0.92), direction worsening | R001 identity-provider integration slip has materialised as issue I001 (vendor sandbox outage); work package 1.3.1 Identity / SSO integration is RED — owner Sam Lee | Approve the SSO recovery plan and decide whether to draw management reserve — decider Dana Okoro — at the next bi-weekly steering committee |

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
| Scope | Scope statement signed by Dana Okoro at M1; SSO is in the baseline | CR003 accessibility uplift approved ($12,000 from contingency); CR002, CR004, CR006 pending ($30,000) | Committed + pending $42,000 against $40,000 contingency | AMBER | `change_impact.py` on the change log |
| Schedule | Critical path A → B → D → F → G → H → J = 18 weeks; milestones M1, M4, M6 | SSO integration two weeks late (task C has only 1 week of float); release outlook 4 sprints likely, 5 pessimistic, 4 left | SPI 0.92 (1.3.1 at 0.75) | AMBER | `health_check.py`, `velocity_forecast.py` |
| Cost | BAC $500,000 incl. $40,000 contingency | AC $252,000; EAC ≈ $535,000 | CPI 0.93 (1.05 → 1.00 → 0.93), VAC ≈ -$35,000, TCPI 1.07 | AMBER | `health_check.py` |
| Risk | $40,000 contingency; threat EMV $94,300 → $52,300 after responses | R001 (HIGH, EMV $48,000) occurring; every HIGH/MEDIUM risk has an owner and a response | Contingency nearly consumed by the forecast overrun and changes | AMBER | `risk_score.py --check` |
| Quality | Definition of done; quality gates per sprint | No failed gate reported | — | GREEN | sprint reviews |

Overall AMBER: no dimension is RED, but schedule and cost are both below 0.95 and worsening.

Commands that produced these numbers (run from the repository root):
- `python .claude/skills/cost-management/scripts/health_check.py .claude/skills/cost-management/assets/evm-snapshot.csv`
- `python .claude/skills/cost-management/scripts/health_check.py .claude/skills/cost-management/assets/evm-history-sample.csv` (the CPI trend)
- `python .claude/skills/agile-delivery/scripts/velocity_forecast.py .claude/skills/agile-delivery/assets/sprint-history-sample.csv --backlog .claude/skills/agile-delivery/assets/product-backlog-sample.csv --sprints-left 4`
- `python .claude/skills/risk-register/scripts/risk_score.py .claude/skills/risk-register/assets/risk-register-template.csv --check`
- `python .claude/skills/change-request/scripts/change_impact.py .claude/skills/change-request/assets/change-log.csv`

## 3. Artifact checklist by stage

| Stage | Artifact | Owning skill | Exists? | Approved (date) |
|---|---|---|---|---|
| Initiation | Business case and benefits register | `business-case` | yes | before M1 |
| Initiation | Signed charter | `project-charter` | yes | before M1 |
| Initiation | Stakeholder register and engagement strategy | `stakeholder-management` | yes | M1 |
| Initiation | Kickoff held, decisions and actions recorded | `project-initiation`, `meeting-management` | yes | M1 |
| Planning | Scope statement and requirements traceability matrix | `scope-and-requirements` | yes | M1 |
| Planning | WBS and WBS dictionary | `work-breakdown-structure` | yes | M1 |
| Planning | Estimates with basis of estimate | `estimation` | yes | M1 |
| Planning | Schedule baseline and critical path | `project-schedule` | yes | M1 |
| Planning | Resource plan and capacity check | `resource-management` | yes (Carla Diaz OVER W6-W8 not yet levelled) | M1 |
| Planning | RACI | `raci-matrix` | yes | M1 |
| Planning | Cost baseline with contingency and management reserve | `cost-management` | yes | M1 |
| Planning | Risk register with owners and responses | `risk-register`, `risk-management` | yes | M1 |
| Planning | Definition of done, acceptance criteria, quality gates | `quality-management` | yes | M1 |
| Planning | Communication plan | `project-communication` | yes | M1 |
| Planning | Change control process and thresholds | `change-management` | yes | M1 |
| Planning | Procurement plan and contracts | `procurement-management` | yes (IdentityCo, firm fixed price) | M1 |
| Planning | Ordered backlog and definition of ready | `agile-delivery` | yes | M1 |
| Planning | Assumptions and constraints log | `project-planning` | yes (A1 identity licence still open) | M1 |
| Planning | Project management plan; baseline approved | `project-planning` | yes | M1 |
| Delivery | Issue, action and decision log | `project-delivery` | yes | ongoing |
| Delivery | Weekly status report | `status-report` | yes | weekly |
| Delivery | Change log with decisions | `change-request` | yes | ongoing |
| Delivery | Go/no-go checklist, cutover runbook, hypercare plan | `release-and-cutover` | no — due before the M4 pilot | — |
| Closure | (not yet due) | `project-closure` | n.a. | — |

## 4. Gaps and routing (at most two routes)

| # | Gap | Route to | First action | Artifact expected | Owner | By |
|---|---|---|---|---|---|---|
| 1 | SSO vendor slip threatens the M4 pilot | `procurement-management` | Hold IdentityCo to a dated recovery plan under the contract remedies | Updated vendor register and recovery milestone | Sam Lee | next steering |
| 2 | TCPI 1.07 exceeds CPI 0.93 by more than 0.10 and contingency is nearly gone | `cost-management` | Re-forecast EAC and prepare the reserve or re-plan decision for the sponsor | Revised forecast and reserve request | Sam Lee | next steering |
