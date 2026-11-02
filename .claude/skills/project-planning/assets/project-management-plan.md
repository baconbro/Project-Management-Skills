# Project Management Plan — <project name>

Fill-in template for the integrated plan that the sponsor approves as the baseline at the end of
planning. Each section names the skill that produces its detail: run that skill, then paste a
short summary and a link to its artifact here, not the full artifact. Replace every
`<placeholder>`. A filled example for the sample Helios project (a fictional customer
self-service portal used throughout this catalog) is in `project-management-plan-sample.md`.

| Field | Value |
|---|---|
| **Project** | <project name> |
| **Sponsor (baseline approver)** | <name, title> |
| **Project manager** | <name> |
| **Delivery approach** | <waterfall / agile / hybrid> — <one-line reason> |
| **Version / date** | <v0.1> / <yyyy-mm-dd> |
| **Status** | <Draft / Proposed for approval / Approved baseline> |
| **Target approval** | <milestone or date> |

## 1. Purpose and objectives
- **Business need:** <one or two sentences from the charter or business case>
- **Objectives and success criteria:** <measurable objective, baseline, target, date, benefit owner>

## 2. Assumptions and constraints
Log: <link to your copy of `assumptions-log.csv`> — <n> assumptions (<n> open, <n> validated,
<n> invalidated), <n> constraints.

Assumptions whose failure would breach a baseline (each also in the risk register):

| Id | Assumption | If false | Owner | Validate by | Risk id |
|---|---|---|---|---|---|
| <A1> | <statement> | <effect on scope, schedule or cost> | <owner> | <date or milestone> | <R00n> |

Constraints and where the plan honours them:

| Id | Constraint | Honoured by | Status |
|---|---|---|---|
| <CON-1> | <fixed limit> | <the schedule date, budget line or activity that respects it> | <open / validated> |

## 3. Scope baseline
- Scope statement: <version, approval date> — see `scope-and-requirements`.
- Deliverables: <count, with acceptors>; exclusions: <the explicit out-of-scope list>.
- WBS and dictionary: <version, number of work packages, validator result> — see
  `work-breakdown-structure`. Traceability matrix: <link>.
- Agile: product vision, release goal and the prioritised backlog <link> — see `agile-delivery`.

## 4. Procurement and external dependencies
| Work package | Make or buy | Supplier / route | Contract type | Need-by date | Lead time | Risk id |
|---|---|---|---|---|---|---|
| <WBS id and name> | <make / buy> | <supplier or RFI / RFQ / RFP> | <fixed price / T&M / ...> | <date> | <weeks> | <R00n> |

See `procurement-management`. Every lead time appears in section 7, every price in section 10.

## 5. Estimates
- Techniques used and why: <analogous / parametric / three-point / story points> — see `estimation`.
- Total effort: <expected> (<P80 or chosen commit level>); top uncertainty drivers: <work packages>.
- Key estimating assumptions: <logged in section 2 as ids>.

## 6. Responsibilities and resources
- RACI: <link>; one Accountable per work package — see `raci-matrix`.
- Team: <roles, named people, start and end dates, how acquired>.
- Capacity gate: <result of the capacity check at the baselined schedule, peak utilization,
  leveling done, residual decisions> — see `resource-management`.
- Key-person risks: <role, cover, risk id>.

## 7. Schedule baseline
| Milestone | Charter date | Baseline date | Float or reserve |
|---|---|---|---|
| <milestone> | <date> | <date> | <weeks> |

- Critical path: <task chain> = <duration>; near-critical: <tasks with little float>.
- Schedule reserve: <amount> at <P80 or chosen confidence>, held once before <milestone>, or
  <the probability of meeting the date that the sponsor accepted without one> — see
  `project-schedule`.
- Agile: sprint length <n weeks>, sprints to release <n>, forecast range <optimistic / likely /
  pessimistic> — see `agile-delivery`.

## 8. Risk plan
- Approach: scales, thresholds, review cadence, escalation threshold — see `risk-management`.
- Register: <link>; <n> threats, <n> opportunities; inherent threat EMV <$>; residual <$> —
  see `risk-register`.
- Top risks at baseline: <id, description, owner, response>.

## 9. Quality plan
- Acceptance criteria per deliverable: <link to the scope statement>.
- Definition of done: <link>; quality gates: <gate, entry and exit criteria, milestone>.
- Reviews and tests: <cadence, owner>; all scheduled in section 7 and costed in section 10 —
  see `quality-management`.

## 10. Cost baseline and reserves
The management reserve sits **above** the cost baseline: it is part of the total budget but not
of BAC, is never planned as PV or earned as EV, and is released only through change control.

```
Total project budget            <$>   held by <sponsor>
├─ Management reserve           <$>   ABOVE the baseline: unidentified risks; sponsor releases it
│                                     only through change control
└─ Cost baseline = BAC          <$>   time-phased; PV, EV and AC are measured against it
   ├─ Contingency reserve       <$>   identified risks from section 8; PM draws it down
   └─ Work-package costs        <$>   aggregated from the estimates and vendor prices
```

| Line | Amount | Inside BAC? | Controlled by |
|---|---|---|---|
| Work-package costs | <$> | Yes | <PM> |
| + Contingency reserve | <$> | Yes | <PM> |
| **= Cost baseline (BAC)** | **<$>** | — | — |
| + Management reserve (above the baseline) | <$> | No | <sponsor> |
| **= Total project budget** | **<$>** | — | — |
| Charter budget range | <$ – $> | | |

- Time-phasing (S-curve): <cumulative planned cost per period>.
- Earning rule per work package and the reporting period: <link> — see `cost-management`.

## 11. Stakeholder engagement and communications
- Engagement strategy: <key stakeholders, current versus desired engagement, actions> — see
  `stakeholder-management`.
- Communication plan: <link>; cadence: <stand-up, status report, steering committee>.
- Escalation path: <levels and time-boxes> — see `project-communication`.

## 12. Change control
- Tolerances: PM <$ and days>; change control board <$ and days>; sponsor <above that>.
- Process and log: raise → assess → decide → update baselines → verify — see
  `change-management` and `change-request`.
- Reserve rules: contingency drawn down by <PM / board>; management reserve released by <sponsor>.
- Agile: changes the product owner may make without a request: <rule>.

## 13. Baseline approval
| Reconciliation check (`planning-checklist.md`) | Result |
|---|---|
| Work-package costs + contingency = BAC; S-curve ends at BAC | <pass / note> |
| BAC + management reserve inside the charter budget range | <pass / note> |
| Every charter milestone met by the leveled schedule | <pass / note> |
| Capacity gate passes on the baselined schedule | <pass / note> |
| Every constraint in section 2 is honoured | <pass / note> |

| Role | Name | Decision | Date |
|---|---|---|---|
| Sponsor | <name> | <Approved / Approved with conditions / Rejected> | <date> |
| Project manager | <name> | <Agreed> | <date> |

Baseline snapshot stored at: <location>. Freeze announced to: <audiences>. Handed to
`project-delivery` on <date>.
