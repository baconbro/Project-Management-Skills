# Project Scope Statement — Helios (sample)

Sample: the completed scope statement for the sample Helios project (a fictional customer
self-service portal used throughout this catalog), shown as at the M4 pilot go/no-go
review. Copy `scope-statement-template.md` for your own project.

| Field | Value |
|---|---|
| **Project** | Helios customer self-service portal |
| **Sponsor** | Dana Okoro, VP Customer Operations |
| **Project manager** | Sam Lee |
| **Product owner / requirements lead** | Ava Chen |
| **Version / date** | v1.1 / 2026-06-30 (v1.0 baselined at M1, 2026-05-08) |
| **Status** | Baselined |
| **Charter** | Helios charter v1.0, approved by Dana Okoro |
| **Requirements (RTM)** | `requirements-traceability-sample.csv` (extract of 12 requirements) |
| **WBS** | `.claude/skills/work-breakdown-structure/assets/wbs-sample.csv` |

Version history: v1.0 baselined at M1 at the end of Discovery. v1.1 adds the WBS ids and
raises the accessibility standard from WCAG 2.1 AA to 2.2 AA (CR003, approved by the CCB on
2026-06-30).

## 1. Product scope description
A customer self-service portal where registered customers reset a forgotten password,
check the status of their orders, and find answers in a searchable knowledge base,
instead of raising a support ticket. Customers sign in through the existing identity
provider (single sign-on). The portal reads order data from the order system and ticket
data from the ticketing system for deflection reporting; it does not change either system
or the back-office CRM.

## 2. Objectives and constraints this scope serves
| Id | Objective or constraint | Measure or limit | Owner |
|---|---|---|---|
| OBJ-1 | Cut password-reset and order-status tickets by 50% within 6 months of launch | Monthly ticket volume of the two types vs the 3-month pre-launch baseline (they are 40% of tickets, about $600k a year) | Priya Nair |
| CON-1 | Budget | BAC $500,000 including $40,000 contingency; $25,000 management reserve held by the sponsor above the baseline | Dana Okoro (Finance holds the budget) |
| CON-2 | Schedule | 6 months: MVP live to the pilot cohort of 200 at M4, general availability at M6 | Dana Okoro |
| CON-3 | Data-residency policy | Customer personal data stored and processed only in the approved region | Hana Sato |
| CON-4 | Accessibility policy | Customer-facing services conform to WCAG 2.2 AA (raised from 2.1 AA by CR003) | Hana Sato |

## 3. Deliverables and acceptance criteria
| # | Deliverable | WBS id | Description | Acceptance criteria | Acceptor | Requirements |
|---|---|---|---|---|---|---|
| D1 | Project management outputs | 1.1 | Plans, baselines, bi-weekly steering packs, weekly status reports, closure report | Baselines approved and the closure report accepted | Dana Okoro | — |
| D2 | Requirements & user research | 1.2.1 | This scope statement and the RTM from 12 customer interviews and 3 Support Operations workshops | Scope statement and RTM signed off | Priya Nair | all |
| D3 | UX design & prototype | 1.2.2 | Clickable prototype of the password-reset and order-status journeys | Prototype passes two usability rounds with pilot customers | Ava Chen | REQ-001, REQ-002 |
| D4 | Identity / SSO integration | 1.3.1 | Single sign-on with the existing identity provider | Pilot users authenticate through SSO in staging and the security review is passed | Marcus Webb | REQ-003 |
| D5 | Self-service UI | 1.3.2 | Password-reset and order-status journeys on desktop and mobile | Both journeys complete end to end and pass the WCAG 2.2 AA audit | Priya Nair | REQ-001, REQ-002, REQ-006, REQ-011 |
| D6 | Knowledge base | 1.3.3 | Searchable knowledge base with 150 migrated articles | The top-50 support questions are answered and searchable | Priya Nair | REQ-004, REQ-006, REQ-010 |
| D7 | Reporting & analytics | 1.3.4 | Ticket-deflection report evidencing OBJ-1 | Report reconciles with the ticketing system for a closed month | Priya Nair | REQ-005 |
| D8 | System & UAT testing | 1.4.1 | System, regression and UAT with 20 Support Operations agents | Zero open severity-1 or severity-2 defects and UAT signed off | Priya Nair | product Musts |
| D9 | Hardening & launch | 1.4.2 | Performance and security hardening and the production cutover | Security review passed, data-residency review signed by Hana Sato, GA readiness reviews passed and the portal live to all customers at the cutover | Marcus Webb | REQ-007 |
| D10 | Training & communications | 1.5.1 | Train-the-trainer for Support Operations and customer launch communications | All agents trained and launch communications sent | Priya Nair | REQ-008 |
| D11 | Operational handover | 1.5.2 | Runbooks, alerting and on-call rota handed to Support Operations | Runbooks accepted and the on-call rota live for the 4-week warranty period | Priya Nair | REQ-009 |

## 4. Acceptance process (scope validation)
- **Verification first:** Frank Müller (QA) confirms each deliverable passed its tests
  and attaches the results; the RTM rows move to `verified`.
- **Acceptance:** Ava Chen accepts sprint increments at each sprint review; the named
  acceptor signs each deliverable at the M4 pilot go/no-go or the M6 general-availability
  gate, within 5 working days of the request.
- **Outcomes:** accept, accept with conditions, or reject with reasons tied to a criterion.
- **Rejections:** a failed criterion returns to the team as a defect; a new need is
  raised as a change request.
- **Final acceptance:** Dana Okoro accepts the product at general availability (M6),
  conditional on Priya Nair accepting the operational handover (D11) at hypercare exit.

## 5. Exclusions (out of scope)
| Excluded item | Reason | Where it goes |
|---|---|---|
| Native mobile apps | Responsive web covers the pilot; apps add cost with no extra deflection | Not planned |
| Live chat with agents | Moves contacts to another channel rather than deflecting them | Phase 2 (CR001 deferred; REQ-012 kept as Won't) |
| Back-office CRM changes | Owned by the CRM programme | Other project |
| SSO for partner logins | Customers only in this release | Pending CR002 (under assessment) |
| Knowledge base in languages other than English | Pilot cohort is English-speaking | Pending CR004 (Spanish; raised) |
| Replacing the ticketing system | Portal only reads ticket data for reporting | Not planned |

## 6. Assumptions
| # | Assumption | Owner | Validate by | Impact if false |
|---|---|---|---|---|
| A1 | The existing identity provider supports customer logins without a license upgrade | Ben Adeyemi | Vendor sandbox, week 6 | SSO slips or costs more (risk R001) |
| A2 | The order system API returns current order status on request | Carla Diaz | M1 | REQ-002 needs a batch feed and a staleness message |
| A3 | Support Operations releases 20 agents for UAT | Priya Nair | M3 | UAT runs longer; M4 at risk |
| A4 | The 150 articles to migrate are accurate and current | Priya Nair | M2 | Rewrite effort lands in 1.3.3 |
| A5 | 200 pilot customers can be recruited before M4 | Ava Chen | M3 | Pilot evidence weaker (see CR006) |

## 7. Requirements summary
Counts for the 12-requirement extract in the sample RTM (the remaining Should and Could
stories live in the product backlog):

| Type | Must | Should | Could | Won't | Total |
|---|---|---|---|---|---|
| Functional | 5 | 1 | 0 | 1 | 7 |
| Non-functional | 2 | 0 | 1 | 0 | 3 |
| Transition | 2 | 0 | 0 | 0 | 2 |
| **Total** | 9 | 1 | 1 | 1 | 12 |

Must share of estimated build effort: about 60%. Coverage checks: all seven pass; every
product and transition work package (1.3.1-1.3.4, 1.4.2, 1.5.1, 1.5.2) traces to a
requirement.

## 8. Scope change control
- **Scope baseline:** this statement, the RTM and the WBS, approved by Dana Okoro at M1
  and re-issued as v1.1 after CR003.
- **Needs a change request:** adding or removing a deliverable or exclusion, changing a
  Must or an acceptance criterion, or anything that moves CON-1 to CON-4. Raised through
  `change-request`, decided under the `change-management` tolerances (PM, CCB or sponsor).
- **Within the product owner's authority:** Ava Chen may reorder the backlog and swap
  Should or Could stories of equal size within a release without a change request.

## 9. Acceptance log
Entries are added as deliverables are accepted; they record scope validation and do not
change the baseline or the version.

| When | Deliverable / REQ ids | Evidence | Acceptor | Decision | Conditions and follow-ups |
|---|---|---|---|---|---|
| M1 | D2 / all | Scope statement v1.0, RTM, playback notes | Priya Nair | Accepted | — |
| M1 | D3 / REQ-001, REQ-002 | Usability round 1 and 2 reports | Ava Chen | Accepted | — |
| M4 | D5 / REQ-001, REQ-002 | UAT-01, UAT-02 | Priya Nair | Accepted with conditions | REQ-006 at WCAG 2.2 AA (CR003) is built in sprint S7 and accepted after the ACC-01 audit, before GA; REQ-011 (Could) accepted separately if built |
| M4 | D6 / REQ-004 | UAT-04 | Priya Nair | Accepted with conditions | 4 migrated articles rewritten by M5 (Carla Diaz); REQ-006 as for D5; REQ-010 (Should) accepted separately when built |
| M4 | D8 / product Musts | Test summary: 0 open severity-1 or severity-2 defects; UAT sign-off | Priya Nair | Accepted | — |
| M4 | D4 / REQ-003 | SIT-03 passed in staging; security review | Marcus Webb | Pending | Accept after the first production SSO logins at GA (M6) |
| M4 | D9 / REQ-007 | SEC-02 data-flow review signed by Hana Sato; security review | Marcus Webb | Pending | Hardening runs 2026-08-17 to 09-18; accept after the GA readiness reviews and the cutover (M6) |
| M4 | D10 / REQ-008 | Training plan | Priya Nair | Pending | Training runs 2026-08-17 to 09-11; accept at the M6 go/no-go on TRN-01 |
| M4 | D7 / REQ-005 | UAT-05 on test data | Priya Nair | Pending | Needs one closed month of pilot data (M5) |

## 10. Approval
| Role | Name | Decision | Date |
|---|---|---|---|
| Sponsor | Dana Okoro | Approved v1.0; approved v1.1 | 2026-05-08; 2026-06-30 (with CR003) |
| Project manager | Sam Lee | Agreed | M1 |
| Product owner | Ava Chen | Agreed | M1 |
| Benefit owner | Priya Nair | Agreed | M1 |
