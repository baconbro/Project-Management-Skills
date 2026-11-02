# Project Charter — Helios (sample)

Sample: the approved charter of the sample Helios project (a fictional customer self-service
portal used throughout this catalog), as signed by the sponsor at the end of initiation. Do not
copy its values; copy `charter-template.md` for your own project.

| Field | Value |
|---|---|
| **Project name** | Helios customer self-service portal |
| **Sponsor** | Dana Okoro, VP Customer Operations |
| **Project manager** | Sam Lee |
| **Business case** | Helios business case v1.0, approved by Dana Okoro: recommended option NPV $196,174 at 10%, IRR 23.6%, payback 2.85 years; funding $450k–$550k |
| **Delivery approach** | Hybrid — the outcome, budget range, M1/M4/M6 and single sign-on through the existing identity provider are fixed; portal and knowledge-base features flex in two-week sprints ordered by the product owner |
| **Version / date** | v1.0 / 2026-04-02 |
| **Status** | Approved |

## 1. Business need
40% of support tickets are password resets and order-status questions that customers could
answer themselves; handling them costs about $600k a year. A self-service portal lets customers
resolve both without an agent.

## 2. Objectives and success criteria
| Id | Objective (SMART) | Metric and baseline | Target and date | Benefit owner |
|---|---|---|---|---|
| OBJ-1 | Cut password-reset and order-status tickets by 50% within 6 months of launch | Monthly ticket volume of the two types in the ticketing system; baseline = average of the 3 months before launch | 50% below baseline, 6 months after general availability | Priya Nair, Head of Support Operations |

## 3. Scope boundaries (high level)
**In scope**
- Customer self-service password reset.
- Order-status lookup that reads the order system.
- A searchable knowledge base, with existing support articles migrated.
- Customer sign-in through single sign-on (SSO) with the existing identity provider.
- Ticket-deflection reporting that evidences OBJ-1.
- A pilot with 200 customers, general availability, Support Operations training and the
  handover to operations.

**Out of scope**
| Excluded item | Reason | Where it goes |
|---|---|---|
| Native mobile apps | A responsive web portal covers the need; apps add cost without extra deflection | Not planned |
| Live chat with agents | Moves contacts to another channel instead of deflecting them | Phase 2 candidate |
| Back-office CRM changes | Owned by the CRM programme | Other project |
| SSO for partner logins | Customers only in this release | Not in this release |
| Knowledge base in languages other than English | The pilot cohort is English-speaking | Not in this release |
| Replacing the ticketing system | The portal only reads ticket data for reporting | Not planned |

## 4. High-level milestones
| Id | Milestone | Target | What must be true |
|---|---|---|---|
| M1 | Discovery complete | End of month 1 | Requirements and UX prototype agreed; scope, schedule and cost baselines approved |
| M4 | MVP live to pilot | End of month 4 | Password reset, order status and knowledge base live for the 200 pilot customers; SSO built and tested, switched on at GA (M6) |
| M6 | General availability | End of month 6 | Portal live to all customers; Support Operations trained |

## 5. Budget range and funding
| Item | Value |
|---|---|
| **Budget range** (total, including all reserves) | $450,000 – $550,000 |
| **Funding source** | Customer Operations investment budget; Finance holds the budget |
| **Basis of the range** | Business case investment of $500,000, ±10% until the cost baseline is set at M1 |
| **Spend allowed before the baseline** | Discovery (requirements, user research, UX prototype) and project management to M1; no new vendor or hosting commitment until the baseline is approved |

## 6. Assumptions and constraints
| Id | Assumption (taken as true, to validate) | Owner | Validate by | If false |
|---|---|---|---|---|
| A1 | The existing identity provider supports customer logins without a license upgrade | Ben Adeyemi | Week 6 (vendor sandbox) | SSO slips or costs more; possible stop trigger |
| A2 | The order system API returns current order status on request | Carla Diaz | M1 | Order status needs a batch feed and a staleness message |
| A3 | Support Operations releases 20 agents for UAT | Priya Nair | M3 | UAT runs longer; M4 at risk |
| A4 | The 150 articles to migrate are accurate and current | Priya Nair | M2 | Knowledge-base content must be rewritten first |
| A5 | 200 pilot customers can be recruited before M4 | Ava Chen | M3 | Smaller pilot; weaker evidence at the M4 review |

| Id | Constraint (fixed limit) | Limit | Owner |
|---|---|---|---|
| CON-1 | Budget | Total cost, all reserves included, within $450,000 – $550,000 | Dana Okoro |
| CON-2 | Schedule | 6 months: MVP to the pilot cohort of 200 at M4, general availability at M6 | Dana Okoro |
| CON-3 | Data-residency policy | Customer personal data stored and processed only in the approved region | Hana Sato |
| CON-4 | Accessibility policy | Customer-facing services conform to WCAG 2.1 AA | Hana Sato |

## 7. Top risks (qualitative)
Logged as R001–R003 in the risk register during planning.

| Risk (cause → event → effect) | Likelihood (H/M/L) | Impact (H/M/L) | Owner |
|---|---|---|---|
| The identity-provider integration is unproven and vendor lead times are long → SSO slips → the M4 pilot moves | M | H | Sam Lee |
| Support processes are partly undocumented → requirements surface late → scope and cost grow | H | M | Dana Okoro |
| Integration knowledge sits with one engineer → the lead engineer leaves → the build stalls | L | H | Sam Lee |

## 8. Key stakeholders
| Stakeholder | Role or interest | What they approve, accept or provide |
|---|---|---|
| Dana Okoro, VP Customer Operations | Sponsor | Approves this charter, the baseline, go/no-go decisions and final acceptance |
| Priya Nair, Head of Support Operations | Benefit owner (OBJ-1) | Accepts the self-service journeys and the operational handover; releases UAT agents |
| Ava Chen | Product owner | Orders the backlog; accepts increments at sprint reviews |
| Ben Adeyemi | Tech lead | Technical design; owns the identity-provider assumption (A1) |
| Marcus Webb | Security lead | Accepts SSO and the security review |
| Hana Sato | Legal & Compliance | Signs off data residency and accessibility |
| Finance | Budget holder | Confirms funding; receives monthly cost reports |
| Pilot customers (cohort of 200) | First users | Use the MVP from M4 and give feedback |

## 9. Project manager authority and governance
- **PM decides alone:** team assignments, the order of work, and changes up to $5,000 and
  2 working days (drawn from contingency once the baseline exists).
- **Escalate to** the change control board (chaired by Dana Okoro; constituted in planning):
  changes above the PM's limits that stay inside the contingency and the fixed milestones.
- **Sponsor decides:** HIGH-impact changes, any release of management reserve, any move of M4
  or M6, and any change to OBJ-1, the budget range or the cancellation criteria.
- **Governance cadence:** steering committee bi-weekly (Dana Okoro, Priya Nair, Finance,
  Sam Lee, Ava Chen); status report weekly; team stand-up daily.

## 10. Approval requirements and exit criteria
**Approval requirements**
| What | Approved or accepted by | When / evidence |
|---|---|---|
| This charter | Dana Okoro | Signature in section 11 |
| Baseline (scope, schedule, cost) | Dana Okoro | M1, one dated approval of all three |
| Each deliverable | The acceptor named per deliverable in the scope statement (e.g. Marcus Webb for SSO, Priya Nair for the self-service journeys) | At the M4 or M6 gate, after QA verification |
| M4 pilot and M6 general-availability releases | Dana Okoro, on the PM's recommendation | Go/no-go record |
| Project completion | Dana Okoro | Final acceptance of the product at general availability (M6), conditional on Priya Nair accepting the operational handover at hypercare exit; closure report after hypercare |
| Business success (OBJ-1) | Priya Nair, reported to Dana Okoro | 6 months after general availability |

**Exit criteria — normal close:** the portal is live to all customers, Dana Okoro signs final
acceptance, hypercare exit criteria are met, Priya Nair accepts the operational handover and the
closure report is issued; OBJ-1 tracking passes to Priya Nair.

**Cancellation criteria (stop triggers)** — any one triggers a continue / re-scope / stop
decision by Dana Okoro; Sam Lee recommends within 5 working days.
| Trigger | Threshold | Checked when, by whom |
|---|---|---|
| Cost forecast | Forecast total cost above $550,000 (top of the range) with no recovery plan agreed at the next steering committee | Each steering committee; Sam Lee |
| Business case | Re-appraisal crosses a switching value: benefits more than 28% below the case or costs more than 39% above it (NPV below zero) | M1, M4 and M6; Finance |
| Identity provider (A1) | Customer sign-in through the existing identity provider needs a license upgrade that breaks CON-1 or CON-2 | Vendor sandbox test, week 6; Ben Adeyemi |
| Pilot adoption | Fewer than 40 of the 200 pilot customers (20%) have completed a password-reset or order-status journey 4 weeks after M4 | 4 weeks after M4; Ava Chen reports, Priya Nair confirms |
| Benefit owner | Support Operations withdraws as benefit owner, or the need disappears | Each steering committee; Dana Okoro |

## 11. Sign-off
The charter is approved only when the sponsor named above records a decision on the version
shown.

| Role | Name | Decision (Approved / Approved with conditions / Rejected) | Version | Date | Conditions |
|---|---|---|---|---|---|
| Sponsor | Dana Okoro | Approved | v1.0 | 2026-04-02 | None |
| Project manager (accepts the appointment) | Sam Lee | Accepted | v1.0 | 2026-04-02 | — |
| Finance (funding confirmed) | Finance (budget holder) | Confirmed | v1.0 | 2026-04-02 | — |

## Version history
| Version | Date | Change | Approved by |
|---|---|---|---|
| v0.1 | 2026-03-24 | First draft from the approved business case | — |
| v0.2 | 2026-03-30 | Review: OBJ-1 given a baseline and benefit owner; partner SSO and non-English knowledge base added to the exclusions; PM limits and cancellation criteria added | — |
| v1.0 | 2026-04-02 | Approved by the sponsor | Dana Okoro |
