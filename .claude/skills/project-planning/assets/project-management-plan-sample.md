# Project Management Plan — Helios (sample)

Sample: the integrated plan for the sample Helios project (a fictional customer self-service
portal used throughout this catalog) as approved by the sponsor at M1, the end of Discovery.
Each section summarises the output of the skill named in it. Copy
`project-management-plan.md` for your own project.

| Field | Value |
|---|---|
| **Project** | Helios customer self-service portal |
| **Sponsor (baseline approver)** | Dana Okoro, VP Customer Operations |
| **Project manager** | Sam Lee |
| **Delivery approach** | Hybrid — fixed budget, milestones and integration work; UI and knowledge-base scope flexes in two-week sprints |
| **Version / date** | v1.0 / M1 |
| **Status** | Approved baseline |
| **Target approval** | M1 (Discovery complete) |

## 1. Purpose and objectives
- **Business need:** 40% of support tickets are password resets and order-status questions,
  about $600k a year in handling cost.
- **Objective (OBJ-1):** cut those two ticket types by 50% within 6 months of launch, measured
  against the 3-month pre-launch monthly volume; benefit owner Priya Nair (Head of Support
  Operations).

## 2. Assumptions and constraints
Log: `assumptions-log-sample.csv` — 5 assumptions (4 open, 1 validated), 4 constraints (all
honoured by this plan).

| Id | Assumption | If false | Owner | Validate by | Risk id |
|---|---|---|---|---|---|
| A1 | The existing identity provider supports customer logins without a license upgrade | SSO slips or costs more | Ben Adeyemi | W6, vendor sandbox | R001 |

A3 (20 agents released for UAT), A4 (articles accurate) and A5 (200 pilot customers by M4) are
tracked by their validate-by dates: the PM judged each recoverable within float and
contingency, so none is a separate risk.

| Id | Constraint | Honoured by | Status |
|---|---|---|---|
| CON-1 | Budget: BAC $500,000 incl. $40,000 contingency; $25,000 management reserve above it | Section 10 | validated |
| CON-2 | 6 months: MVP to the pilot cohort of 200 at M4, general availability at M6 | Section 7 | validated |
| CON-3 | Data-residency policy | Data-flow review in 1.4.2 Hardening & launch, signed by Hana Sato | validated |
| CON-4 | Accessibility policy, WCAG 2.1 AA | Accessibility audit before the M4 gate | validated |

## 3. Scope baseline
- Scope statement v1.0 approved by Dana Okoro at M1 — 11 deliverables (D1–D11), each with
  acceptance criteria and one acceptor — see `scope-and-requirements`.
- Exclusions: native mobile apps, back-office CRM changes, replacing the ticketing system.
- WBS: 5 level-1 elements, 10 work packages, validator PASS — see `work-breakdown-structure`.

## 4. Procurement and external dependencies
| Work package | Make or buy | Supplier / route | Need-by | Risk id |
|---|---|---|---|---|
| 1.3.1 Identity / SSO integration | Buy customer sign-in; build the integration in-house | Identity-provider vendor, fixed price | Sandbox when 1.3.1 starts in W6 | R001 |
| Hosting for all build work packages | Buy | Call-off under the enterprise agreement | Environments before W6 | R004 |

See `procurement-management`. The vendor's sandbox is an external dependency of task C.

## 5. Estimates
- Three-point (PERT) per work package; wideband Delphi for Identity / SSO integration;
  project management parametric — see `estimation`.
- Total effort 451.83 person-days expected, 468.63 at P80. Identity / SSO integration carries
  39% of the variance, then System & UAT testing (15%) and Self-service UI (14%).

## 6. Responsibilities and resources
- RACI: one Accountable per WBS element; the tech lead Ben Adeyemi is Accountable for the
  integration and UI work — see `raci-matrix`.
- Team: Ava Chen (product owner), Ben Adeyemi (tech lead), Carla Diaz (backend), Devin Patel
  (frontend), Elena Rossi (UX), Frank Müller (QA).
- Capacity gate over the build peak W6–W9: Carla Diaz peaked at 125% in W7 and Devin Patel at
  105%. Leveling moved 34 hours (Carla to Ben, Devin to Elena) and smoothed Carla's remaining
  knowledge-base hours into W9–W10 within that task's 3 weeks of float; the gate now passes —
  see `resource-management`.
- Key-person risk: Ben is the only backend cover and the lead engineer in R003; response is
  cross-training, not more hours on Ben.

## 7. Schedule baseline
| Milestone | Charter date | Baseline | Float or reserve |
|---|---|---|---|
| Discovery complete | M1 | M1 — baseline approved at this milestone | — |
| MVP live to pilot | M4 | Week 17 (end of H, Hardening & launch) | 0 weeks: critical |
| General availability | M6 | After the pilot, at M6 | 2.4-week schedule reserve held before GA |

- Critical path A→B→D→F→G→H→J = 18 weeks; near-critical C (Identity / SSO integration, 1 week
  of float, vendor-dependent) and I (1 week).
- Simulation P50 19.3, P80 20.4 weeks: a 2.4-week reserve held once, not spread into tasks —
  see `project-schedule`.

## 8. Risk plan
- Probability 0–1, impact in dollars; HIGH at 5% and MEDIUM at 1% of BAC; reviewed at every
  bi-weekly steering committee and team risks at sprint planning — see `risk-management`.
- Register R001–R006: five threats and one opportunity; threat EMV $94,300 inherent, $52,300
  after planned responses — see `risk-register`.
- Contingency $40,000: about P50 of a 10,000-trial simulation of the residual register (P80
  $99,000; the $52,300 residual EMV is the mean). Funding P80 would have lifted BAC above the
  charter ceiling, so Dana Okoro accepted the gap; if R001's trigger fires, Sam Lee escalates to
  the steering committee within 2 working days — see `risk-management`.
- Top risks: R001 identity-provider integration slips (0.4 × $120,000, Sam Lee); R002
  undocumented requirements expand scope (0.6 × $40,000, Dana Okoro); R006 opportunity:
  knowledge base deflects tickets earlier than planned (0.3 × $60,000, Priya Nair).

## 9. Quality plan
- Acceptance criteria per deliverable in the scope statement; definition of done for every
  sprint increment — see `quality-management`.
- Gates: M4 pilot go/no-go and M6 general availability; Frank Müller verifies, the named
  acceptor accepts.
- System & UAT testing (1.4.1) runs 4 weeks with 20 Support Operations agents (A3).

## 10. Cost baseline and reserves
```
Total project budget            $525,000   held by Dana Okoro
├─ Management reserve           $ 25,000   ABOVE the baseline; sponsor releases it only
│                                          through change control
└─ Cost baseline = BAC          $500,000   time-phased M1–M6; EVM measured against it
   ├─ Contingency reserve       $ 40,000   identified risks; Sam Lee draws it down
   └─ Work-package costs        $460,000   ten work packages, bottom-up
```

| Line | Amount | Inside BAC? | Controlled by |
|---|---|---|---|
| Work-package costs | $460,000 | Yes | Sam Lee |
| + Contingency reserve | $40,000 | Yes | Sam Lee |
| **= Cost baseline (BAC)** | **$500,000** | — | — |
| + Management reserve (above the baseline) | $25,000 | No | Dana Okoro |
| **= Total project budget** | **$525,000** | — | — |
| Charter budget range | $450,000 – $550,000 | | |

- Cumulative planned value: M1 $53,333 · M2 $161,666 · M3 $255,000 · M4 $368,333 · M5
  $436,666 · M6 $500,000; contingency distributed to work packages by WBS weight.
- Earned value monthly against this baseline; RAG GREEN when CPI and SPI are both at least
  0.95, RED when either is below 0.85 — see `cost-management`.

## 11. Stakeholder engagement and communications
- Manage closely: Dana Okoro (sponsor), Priya Nair (benefit owner). Keep satisfied: Marcus Webb
  (security acceptor for D4 and D9), Hana Sato (data residency and accessibility), Finance
  (budget holder). Keep informed: the pilot cohort of 200 customers — see
  `stakeholder-management`.
- Cadence: daily stand-up (team), weekly status report (sponsor and key stakeholders),
  bi-weekly steering committee (decisions and escalations) — see `project-communication`.
- Escalation: team → Sam Lee within a day → steering committee → Dana Okoro.

## 12. Change control
- Tolerances: the PM approves up to $5,000 and 2 days within contingency; the change control
  board decides above that; the sponsor decides HIGH-impact changes and any release of
  management reserve — see `change-management` and `change-request`.
- Ava Chen may reorder the backlog and swap Should or Could stories of equal size within a
  release without a change request.

## 13. Baseline approval
| Reconciliation check | Result |
|---|---|
| $460,000 + $40,000 = BAC $500,000; S-curve ends at $500,000 | Pass |
| BAC + $25,000 management reserve = $525,000, inside $450k–$550k | Pass |
| M1, M4 and M6 met by the leveled 18-week schedule plus 2.4-week reserve | Pass |
| Capacity gate passes on the baselined schedule (no one OVER) | Pass |
| CON-1 to CON-4 honoured (section 2) | Pass |

| Role | Name | Decision | Date |
|---|---|---|---|
| Sponsor | Dana Okoro | Approved scope, schedule and cost baselines v1.0 | M1 |
| Project manager | Sam Lee | Agreed | M1 |
| Benefit owner | Priya Nair | Agreed | M1 |

Baseline snapshot v1.0 stored with the plan; freeze announced in the first weekly status
report; handed to `project-delivery` at M1.
