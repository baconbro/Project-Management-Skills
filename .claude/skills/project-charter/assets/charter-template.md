# Project Charter — <project name>

Fill-in template. Replace every `<placeholder>`, delete rows you do not need, and keep the
filled charter to one or two pages. Definitions and phrasing examples for each section are in
`../references/charter-elements.md`; a completed example is `charter-sample.md`. Until the
sponsor signs section 11, this document is a draft and authorizes nothing.

| Field | Value |
|---|---|
| **Project name** | <name> |
| **Sponsor** | <one named executive who funds the project and owns the outcome — name, title> |
| **Project manager** | <name> |
| **Business case** | <reference, version, approval date> — or: waived by <sponsor> on <date> because <reason> |
| **Delivery approach** | <waterfall / agile / hybrid> — <what is fixed and what may flex> |
| **Version / date** | <v0.1> / <YYYY-MM-DD> |
| **Status** | <Draft / Submitted / Approved / Superseded> — Draft until section 11 is signed |

## 1. Business need
<One or two plain-language sentences: the problem or opportunity, its measurable cost or value,
and why now.>

## 2. Objectives and success criteria
| Id | Objective (SMART) | Metric and baseline | Target and date | Benefit owner |
|---|---|---|---|---|
| OBJ-1 | <outcome, not activity> | <metric; baseline value and the period it was measured over> | <target; by when> | <name> |
| OBJ-2 | <outcome> | <metric; baseline> | <target; date> | <name> |

## 3. Scope boundaries (high level)
**In scope** (outcomes and major deliverables — the detailed scope statement comes in planning)
- <outcome or major deliverable>
- <outcome or major deliverable>

**Out of scope** (explicit exclusions)
| Excluded item | Reason | Where it goes |
|---|---|---|
| <excluded item> | <why it is excluded> | <later phase / another project / not planned> |
| <excluded item> | <why> | <destination> |

## 4. High-level milestones
| Id | Milestone | Target | What must be true |
|---|---|---|---|
| <M1> | <milestone> | <month or date> | <evidence that it is reached> |
| <M2> | <milestone> | <month or date> | <evidence> |

## 5. Budget range and funding
| Item | Value |
|---|---|
| **Budget range** (total, including all reserves) | <$low – $high> |
| **Funding source** | <budget line, cost centre or investment decision> |
| **Basis of the range** | <business case figure / analogous estimate / top-down allocation> |
| **Spend allowed before the baseline** | <what the PM may commit before the plan is approved, e.g. discovery staff only> |

## 6. Assumptions and constraints
| Id | Assumption (taken as true, to validate) | Owner | Validate by | If false |
|---|---|---|---|---|
| A1 | <assumption> | <name> | <date or milestone> | <consequence> |

| Id | Constraint (fixed limit) | Limit | Owner |
|---|---|---|---|
| CON-1 | <budget / deadline / regulation / technology> | <the limit> | <name> |

## 7. Top risks (qualitative)
| Risk (cause → event → effect) | Likelihood (H/M/L) | Impact (H/M/L) | Owner |
|---|---|---|---|
| <because of …, … may happen, causing …> | <H/M/L> | <H/M/L> | <name> |
| <risk> | <H/M/L> | <H/M/L> | <name> |

## 8. Key stakeholders
| Stakeholder | Role or interest | What they approve, accept or provide |
|---|---|---|
| <name or group> | <role / interest> | <decision, acceptance or input> |
| <name or group> | <role / interest> | <decision, acceptance or input> |

## 9. Project manager authority and governance
- **PM decides alone:** <decisions such as team assignments and work order>; changes up to
  <$ amount> and <n> working days
- **Escalate to** <steering committee / change control board>: <changes above the PM's limits
  that stay inside the budget range and fixed milestones>
- **Sponsor decides:** <objectives, budget range, fixed milestones, exit decisions>
- **Governance cadence:** <steering committee members and frequency; status report frequency>

## 10. Approval requirements and exit criteria
**Approval requirements**
| What | Approved or accepted by | When / evidence |
|---|---|---|
| This charter | <sponsor> | Signature in section 11 |
| Baseline (scope, schedule, cost) | <sponsor> | <milestone, dated approval> |
| Each deliverable | <acceptor named per deliverable in the scope statement> | <gate or review> |
| Go-live / release decisions | <named approver> | <go/no-go record> |
| Project completion | <sponsor> | <final acceptance and closure report> |
| Business success (objectives met) | <benefit owner> | <measurement date after launch> |

**Exit criteria — normal close:** <the conditions under which the project is finished and
handed over, e.g. live, accepted, handed to operations, closure report signed>

**Cancellation criteria (stop triggers)** — any one triggers a continue / re-scope / stop
decision by the sponsor; the PM recommends within <n> working days.
| Trigger | Threshold | Checked when, by whom |
|---|---|---|
| <cost forecast> | <e.g. forecast total cost above the top of the budget range with no recovery plan> | <each steering committee, PM> |
| <business case> | <e.g. re-appraisal crosses a switching value; NPV below zero> | <each gate, sponsor's analyst> |
| <adoption or outcome signal> | <e.g. pilot usage below n% n weeks after launch> | <date, benefit owner> |
| <critical assumption or dependency> | <e.g. assumption A1 proves false and no workaround fits the constraints> | <validate-by date, owner> |

## 11. Sign-off
The charter is approved only when the sponsor named above records a decision on the version
shown. "Approved with conditions" stays a draft for anything the conditions block.

| Role | Name | Decision (Approved / Approved with conditions / Rejected) | Version | Date | Conditions |
|---|---|---|---|---|---|
| Sponsor | <name> | <decision> | <vX.Y> | <YYYY-MM-DD> | <conditions, or none> |
| Project manager (accepts the appointment) | <name> | <accepted> | <vX.Y> | <YYYY-MM-DD> | — |
| <Budget holder> (funding confirmed) | <name or function> | <confirmed> | <vX.Y> | <YYYY-MM-DD> | — |

## Version history
| Version | Date | Change | Approved by |
|---|---|---|---|
| <v0.1> | <YYYY-MM-DD> | <first draft> | — |
