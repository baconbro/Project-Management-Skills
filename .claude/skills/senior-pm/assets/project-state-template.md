# Project-state canvas — `<project name>`

Fill-in template used by `senior-pm` at intake (Workflow steps 1-3). Replace every
`<angle-bracket placeholder>`; write "unknown" plus the question that would answer it rather
than guessing. Keep it to one page and bring it back to the next conversation so triage
starts from what changed. A filled example is `project-state-sample.md` (the sample Helios
project, a fictional customer self-service portal used throughout this catalog).

As of: `<YYYY-MM-DD>` · Filled by: `<name>`

## 1. Canvas (the one table)

| Stage | Baseline exists? (scope / schedule / cost) | RAG (overall + worst dimension) | Top risk or issue | Next decision (who, by when) |
|---|---|---|---|---|
| `<idea / initiation / planning / delivery / closure>` | `<approved / draft / none>` / `<approved / draft / none>` / `<approved / draft / none>` | `<GREEN / AMBER / RED / unknown>`, worst: `<dimension>`, direction `<improving / flat / worsening>` | `<id: one line>` — owner `<name>` | `<decision>` — decider `<name>` — by `<YYYY-MM-DD>` |

Context (one line each):
- Outcome and measure: `<what changes, by how much, by when, measured how>`
- Sponsor / project manager: `<name, title>` / `<name>`
- Approach: `<waterfall / agile / hybrid / not chosen>` — signal: `<the one or two facts that drove it>`
- Hard constraints: `<deadline, budget ceiling, compliance obligation>`

## 2. Health against the baseline

Thresholds (from `status-report`): GREEN when CPI and SPI are both >= 0.95, RED when either
is < 0.85, else AMBER. Rate scope, quality and risk with the per-dimension table in
`.claude/skills/status-report/references/rag-criteria.md` §3. The overall RAG is no greener
than the worst material dimension. With no baseline, every dimension is "unknown — no
baseline" and that is the top gap.

| Dimension | Baseline (approved) | Position now / forecast | Measure | RAG | Source |
|---|---|---|---|---|---|
| Scope | `<deliverables or backlog points baselined>` | `<approved changes; pending change requests>` | `<pending CR count and value vs contingency left>` | `<RAG>` | `<change log>` |
| Schedule | `<key milestone dates>` | `<forecast dates; slip in weeks>` | `<SPI, or velocity forecast vs sprints left, or % milestones on date>` | `<RAG>` | `<EVM check / velocity forecast / plan>` |
| Cost | `<BAC>` | `<AC to date; EAC>` | `<CPI; VAC; TCPI>` | `<RAG>` | `<EVM check / finance report>` |
| Risk | `<contingency reserve>` | `<top exposures; HIGH risks without a response>` | `<threat EMV vs reserve left>` | `<RAG>` | `<risk register>` |
| Quality (optional) | `<acceptance criteria / DoD>` | `<open severe defects; failed gates>` | `<defect trend>` | `<RAG>` | `<test report>` |

Helper commands (run from the repository root on your own files):
- Earned value: `python .claude/skills/cost-management/scripts/health_check.py <your-evm.csv>`
- Velocity and release outlook: `python .claude/skills/agile-delivery/scripts/velocity_forecast.py <your-sprint-history.csv> --sprints-left <N>`
- Risk exposure: `python .claude/skills/risk-register/scripts/risk_score.py <your-risk-register.csv> --bac <BAC>`
- Open, overdue and escalated items: `python .claude/skills/project-delivery/scripts/issue_log_check.py <your-issue-log.csv> --as-of <YYYY-MM-DD>`
- Change burden against the contingency: `python .claude/skills/change-request/scripts/change_impact.py <your-change-log.csv> --reserve-cost <contingency> --pm-limit-cost <PM cost limit> --pm-limit-days <PM day limit>`

## 3. Artifact checklist by stage

Tick what exists for the current stage and every earlier one. A missing artifact is a gap;
the owning skill is where to route it.

| Stage | Artifact | Owning skill | Exists? | Approved (date) |
|---|---|---|---|---|
| Initiation | Business case and benefits register | `business-case` | `<yes / no>` | `<date>` |
| Initiation | Signed charter (sponsor, PM, objectives, scope boundaries) | `project-charter` | `<yes / no>` | `<date>` |
| Initiation | Stakeholder register and engagement strategy | `stakeholder-management` | `<yes / no>` | `<date>` |
| Initiation | Kickoff held, decisions and actions recorded | `project-initiation`, `meeting-management` | `<yes / no>` | `<date>` |
| Planning | Scope statement and requirements traceability matrix | `scope-and-requirements` | `<yes / no>` | `<date>` |
| Planning | WBS and WBS dictionary | `work-breakdown-structure` | `<yes / no>` | `<date>` |
| Planning | Estimates with basis of estimate | `estimation` | `<yes / no>` | `<date>` |
| Planning | Schedule baseline and critical path | `project-schedule` | `<yes / no>` | `<date>` |
| Planning | Resource plan and capacity check | `resource-management` | `<yes / no>` | `<date>` |
| Planning | RACI for deliverables and decisions | `raci-matrix` | `<yes / no>` | `<date>` |
| Planning | Cost baseline (BAC) with contingency and management reserve | `cost-management` | `<yes / no>` | `<date>` |
| Planning | Risk register with owners and responses | `risk-register`, `risk-management` | `<yes / no>` | `<date>` |
| Planning | Definition of done, acceptance criteria, quality gates | `quality-management` | `<yes / no>` | `<date>` |
| Planning | Communication plan | `project-communication` | `<yes / no>` | `<date>` |
| Planning | Change control process and thresholds | `change-management` | `<yes / no>` | `<date>` |
| Planning | Procurement plan and contracts (if buying) | `procurement-management` | `<yes / no / n.a.>` | `<date>` |
| Planning | Ordered backlog and definition of ready (if agile or hybrid) | `agile-delivery` | `<yes / no / n.a.>` | `<date>` |
| Planning | Assumptions and constraints log | `project-planning` | `<yes / no>` | `<date>` |
| Planning | Project management plan; baseline approved | `project-planning` | `<yes / no>` | `<date>` |
| Delivery | Issue log: issues, actions, decisions and dependencies | `project-delivery` | `<yes / no>` | `<date>` |
| Delivery | Status report on the agreed cadence | `status-report` | `<yes / no>` | `<date>` |
| Delivery | Change log with decisions | `change-request` | `<yes / no>` | `<date>` |
| Delivery | Go/no-go checklist, cutover runbook, hypercare plan | `release-and-cutover` | `<yes / no / n.a.>` | `<date>` |
| Closure | Acceptance sign-off of deliverables | `scope-and-requirements`, `project-closure` | `<yes / no>` | `<date>` |
| Closure | Handover to operations and benefits owner | `project-closure` | `<yes / no>` | `<date>` |
| Closure | Lessons learned with owners | `lessons-learned` | `<yes / no>` | `<date>` |
| Closure | Contracts closed | `procurement-management` | `<yes / no / n.a.>` | `<date>` |
| Closure | Closure report; benefits tracking handed over | `project-closure`, `business-case` | `<yes / no>` | `<date>` |

## 4. Gaps and routing (at most two routes)

| # | Gap | Route to | First action | Artifact expected | Owner | By |
|---|---|---|---|---|---|---|
| 1 | `<gap>` | `<skill>` | `<first action>` | `<artifact>` | `<name>` | `<YYYY-MM-DD>` |
| 2 | `<gap>` | `<skill>` | `<first action>` | `<artifact>` | `<name>` | `<YYYY-MM-DD>` |
