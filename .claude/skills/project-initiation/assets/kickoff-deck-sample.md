# Kickoff deck — Helios (sample)

> **Sample, not a template.** The slide content Sam Lee presented at the kickoff of the sample
> Helios project (a fictional customer self-service portal used throughout this catalog) on
> 2026-04-07, built from charter v1.0, business case v1.0 and the G0 gate record. Slide 11 shows
> what was captured in the meeting. Do not copy its values; copy `kickoff-deck-outline.md`.

---

## Slide 1 — Title and purpose of today
- Helios customer self-service portal — project kickoff — 2026-04-07 — deck v1.0
- Sponsor: Dana Okoro, VP Customer Operations | Project manager: Sam Lee
- Today we will: understand why Helios exists and how we will prove it worked, hear the
  boundaries, agree how we work, and leave with owned first planning actions.
- How decisions are made today: team ways of working by consent of the team (Ava Chen decides if
  consent fails); governance meetings by Dana Okoro after input. Scope questions go to the
  parking lot for Dana Okoro.

## Slide 2 — Why we are here (Dana Okoro)
- 40% of our support tickets are password resets and order-status questions: about 5,000 a
  month, about $600,000 a year to handle, and a 26-hour mean time to resolve.
- Doing nothing costs more every year: ticket volume and cost to serve grow about 8% a year.

## Slide 3 — Objective and benefits: how we will prove success
| Objective | Measure | Baseline | Target and date | Benefit owner |
|---|---|---|---|---|
| OBJ-1: cut password-reset and order-status tickets by 50% within 6 months of launch | Monthly volume of the two ticket types in the ticketing system | About 5,000 a month today (December 2025 – February 2026); formal baseline = average of the 3 months before launch | 50% below the baseline (about 2,500 a month), 6 months after general availability | Priya Nair, Head of Support Operations |

- Also tracked: faster resolution, 26 h → instant self-service or 2 h assisted (Priya Nair);
  customer satisfaction, CSAT 72% → 80% (Dana Okoro).
- Dis-benefits we will manage: 6 FTE of support agents redeployed to the complex-case queue
  (redeployment plan agreed before cutover); a temporary CSAT dip at cutover (pilot of 200
  customers, then a staged rollout).

## Slide 4 — Why this option
- Compared over five years at 10%: do nothing (NPV 0); do minimum, an FAQ page and macros
  (NPV $35,816); buy a SaaS portal (NPV $79,709); **build the Helios portal** (NPV $196,174,
  IRR 23.6%, payback 2.85 years).
- The portal creates the most value, and stays ahead unless benefits fall 28% or costs rise 39%.

## Slide 5 — Scope boundaries
- **In scope:** self-service password reset; order-status lookup from the order system; a
  searchable knowledge base with the existing articles migrated; customer sign-in through SSO
  with the existing identity provider; ticket-deflection reporting that evidences OBJ-1; a pilot
  with 200 customers, general availability, Support Operations training and the handover.
- **Out of scope (read aloud):** native mobile apps (not planned); live chat with agents
  (phase 2 candidate); back-office CRM changes (CRM programme); SSO for partner logins (not in
  this release); a knowledge base in other languages (not in this release); replacing the
  ticketing system (not planned).

## Slide 6 — Milestones, budget range and stop triggers
- **M1 Discovery complete** (end of month 1): requirements and UX prototype agreed; scope,
  schedule and cost baselines approved. **M4 MVP live to pilot** (end of month 4): password
  reset, order status and knowledge base live for the 200 pilot customers; SSO built and
  tested, switched on at GA. **M6 General availability** (end of month 6): live to all
  customers with SSO sign-in; Support Operations trained.
- **Budget range:** $450,000 – $550,000 including all reserves, from the Customer Operations
  investment budget. Until the baseline: Discovery and project management only; no new vendor
  or hosting commitment.
- **We stop or re-scope if:** the cost forecast passes $550,000 with no recovery plan; a
  switching value is crossed at M1, M4 or M6; the identity provider needs a license upgrade that
  breaks the budget or the schedule (sandbox test, week 6); fewer than 40 of the 200 pilot
  customers complete a self-service journey within 4 weeks of M4; or Support Operations
  withdraws as benefit owner.

## Slide 7 — Team and roles (draft)
**Draft of roles from the charter.** The full RACI matrix is built in planning with
`raci-matrix` once the work is broken down.

| Role | Name | Decides or accepts |
|---|---|---|
| Sponsor | Dana Okoro | The baseline, go/no-go for the pilot and GA, any release of management reserve, any move of M4 or M6, final acceptance |
| Project manager | Sam Lee | Team assignments, the order of work, changes up to $5,000 and 2 working days; above that, the change control board (set up in planning) or the sponsor |
| Product owner | Ava Chen | Backlog order; accepts increments at sprint reviews |
| Benefit owner | Priya Nair | OBJ-1 after handover; accepts the self-service journeys and the operational handover; releases agents for UAT |
| Tech lead | Ben Adeyemi | Technical design; validates assumption A1 (identity provider) |
| Security lead | Marcus Webb | Accepts SSO and the security review |
| Legal & Compliance | Hana Sato | Signs off data residency and accessibility |
| Budget holder | Finance | Confirms funding; receives monthly cost reports |
| Core team | Carla Diaz (backend), Devin Patel (frontend), Elena Rossi (UX), Frank Müller (QA) | Their build, design and test areas |

## Slide 8 — Delivery approach and cadence
- **Hybrid**, because 4 of 5 checklist answers point to agile, but the six-month date and the
  budget are fixed.
- **Fixed:** OBJ-1, the budget range, M1/M4/M6, SSO through the existing identity provider,
  data residency and accessibility. **Flexes:** portal and knowledge-base features, in two-week
  sprints ordered by Ava Chen.
- **Cadence (proposed, decided today):** daily stand-up; two-week sprints with the review and
  retrospective every second Friday; weekly status report on Fridays; bi-weekly steering
  committee on Tuesdays, chaired by Dana Okoro.

## Slide 9 — Top risks and assumptions
- **Risks:** the identity-provider integration is unproven and vendor lead times are long →
  SSO slips → the M4 pilot moves (Sam Lee); support processes are partly undocumented →
  requirements surface late → scope and cost grow (Dana Okoro); integration knowledge sits
  with one engineer → the lead engineer leaves → the build stalls (Sam Lee).
- **Assumptions to validate:** A1 the identity provider supports customer logins without a
  license upgrade (Ben Adeyemi, week 6); A2 the order system API returns current status
  (Carla Diaz, M1); A3 Support Operations releases 20 agents for UAT (Priya Nair, M3); A4 the
  150 articles to migrate are accurate (Priya Nair, M2); A5 200 pilot customers are recruited
  before M4 (Ava Chen, M3).

## Slide 10 — How we will plan
- Planning produces the scope statement and traceability matrix, the WBS, the make-or-buy
  decisions (identity provider, hosting), estimates, the schedule and critical path, the risk
  register with contingency, the cost baseline with the management reserve above it, the RACI
  matrix, the communication plan and change control.
- **Baseline approval:** M1 (Discovery complete), 2026-05-08, by Dana Okoro in one decision.
- **Open gate conditions:** C1 — Priya Nair agrees the 50% target and the baseline method with
  Dana Okoro (by 2026-05-08); C2 — Sam Lee reviews the engagement matrix with Dana Okoro (by
  2026-04-15).

## Slide 11 — Next steps (captured in the meeting)
- **Decisions:** KD1 daily stand-up at 09:30 and two-week sprints, review and retrospective
  every second Friday; KD2 steering committee bi-weekly on Tuesdays from 2026-04-21.
- **Actions:** K1 open the plan and the assumptions log — Sam Lee — 2026-04-10; K2 schedule
  the three Support Operations requirements workshops, co-led with Priya Nair — Ava Chen —
  2026-04-10; K3 meet Priya Nair to agree the 50% target, the baseline method and the
  redeployment approach — Dana Okoro — 2026-05-08; K4 book the threat-model review with Marcus
  Webb — Ben Adeyemi — 2026-04-17; K5 brief Hana Sato on the data flows — Sam Lee — 2026-04-24.
- **Parking lot:** agent headcount (Priya Nair) → K3; live chat (Devin Patel) → out of scope,
  phase 2 candidate; dropped by agreement.
- **Next meeting:** steering committee, Tuesday 2026-04-21.
