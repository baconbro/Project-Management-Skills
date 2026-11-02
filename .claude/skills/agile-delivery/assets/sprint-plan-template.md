# Sprint plan: <team name> — <sprint name>

| Field | Value |
|---|---|
| **Sprint** | <sprint name or number> |
| **Dates** | <start YYYY-MM-DD> to <end YYYY-MM-DD> (<n> working days) |
| **Product owner** | <name: orders the backlog and accepts the work> |
| **Facilitator** | <Scrum Master, delivery lead, or project manager> |
| **Release this sprint serves** | <release goal and the milestone it must meet> |
| **Sprints left before that milestone** | <n, including this one> |

## 1. Sprint goal
<One sentence: the outcome this sprint delivers and why it matters now. A goal, not a list of
stories: the team can renegotiate individual stories with the product owner and still meet it.>

## 2. Capacity
| Team member | Role | Usual days per sprint | Days available this sprint | Notes (leave, training, other work) |
|---|---|---:|---:|---|
| <name> | <role> | <n> | <n> | <reason for any difference> |
| <name> | <role> | <n> | <n> | |
| **Total** | | **<usual>** | **<available>** | |

- **Capacity factor** = available ÷ usual = <x.xx>
- **Reference velocity** = trailing-3 average from `velocity_forecast.py` = <points>
- **Planning capacity** = reference velocity × capacity factor = <points>. Commit to about
  this figure, never to the best sprint on record.

## 3. Committed backlog items
Take items in backlog order; skip any that fail the definition of ready and say why below.

| Order | ID | Story (short title) | Points | Meets DoR | Owner / pair | Dependencies |
|---:|---|---|---:|---|---|---|
| 1 | <ID> | <title> | <pts> | <yes> | <name> | <none / what it waits for> |
| 2 | <ID> | <title> | <pts> | <yes> | <name> | |
| | | **Committed total** | **<sum>** | | | |

- **Stretch** (started only when every committed item is done): <ID — title — points>
- **Skipped and why:** <ID — the definition-of-ready item it fails and who is resolving it>

## 4. Definition of done (from `quality-management`)
- [ ] <acceptance criteria met and demonstrated to the product owner>
- [ ] <peer reviewed; automated tests written and passing in the pipeline>
- [ ] <non-functional checks, e.g. accessibility and security scans, passed>
- [ ] <deployed to the test environment; user-facing help updated>

## 5. Risks, dependencies, and assumptions
| Item | Type | Owner | Trigger or next action |
|---|---|---|---|
| <description> | <risk / dependency / assumption> | <name> | <what we watch and what we do> |

## 6. Ceremony calendar
| Event | When | Timebox (two-week sprint) |
|---|---|---|
| Sprint planning | <date, time> | <4 h> |
| Daily stand-up | <time, every day> | <15 min> |
| Backlog refinement | <day, time> | <at most 10% of capacity> |
| Sprint review | <date, time> | <2 h> |
| Retrospective | <date, time> | <1.5 h> |

## 7. Mid-sprint change rule
<The sprint goal does not change. Urgent work enters only by swapping out committed work of
the same size, agreed with the product owner. A change that moves a milestone, the budget, or
committed Must-have scope is raised as a change request.>

## 8. End-of-sprint record (complete at the sprint review)
| Committed points | Completed points | Delivered % | Release scope (points) | Carry-over items | Goal met? |
|---:|---:|---:|---:|---|---|
| <n> | <n> | <%> | <n> | <IDs, re-ordered in the backlog> | <yes / no and why> |

Add the row to the team's sprint-history CSV and re-run the forecast before the next planning.

---

## Sample: Helios sprint 7 (filled in)
Sample from the sample Helios project (a fictional customer self-service portal used throughout
this catalog), planned on 2026-08-03 after the sprint 6 review. S1–S5 built the portal, S6 ran
system test and the pilot UAT, and S7 launches the M4 pilot on Friday 2026-08-07 and stabilises
it (network task G); S8–S10 cover hardening, pilot feedback, approved changes and GA readiness.
Forecast inputs: `assets/sprint-history-sample.csv` and `assets/product-backlog-sample.csv`.

| Field | Value |
|---|---|
| **Sprint** | S7 |
| **Dates** | 2026-08-03 to 2026-08-14 (10 working days) |
| **Product owner** | Ava Chen |
| **Facilitator** | Sam Lee (project manager) |
| **Release this sprint serves** | General availability at M6: Must and Should stories (84 points); this sprint also launches the M4 pilot to the 200 customers |
| **Sprints left before that milestone** | 4 (S7 to S10, the last ending 2026-09-25) |

**Sprint goal:** launch the pilot on 2026-08-07 and keep it stable, with every hotfix
regression-tested in under 30 minutes, and make the reset and order-status journeys accessible
(CR003).

| Team member | Role | Usual days | Available | Notes |
|---|---|---:|---:|---|
| Ben Adeyemi | Tech lead | 10 | 8 | Two days on the pilot launch and pilot on-call; also coordinates the identity-provider vendor |
| Carla Diaz | Backend engineer | 10 | 10 | |
| Devin Patel | Frontend engineer | 10 | 7 | Three days of leave |
| Elena Rossi | UX designer | 5 | 5 | Half-time on the team throughout |
| Frank Müller | QA engineer | 10 | 8 | Two days triaging pilot support tickets with Support Operations |
| **Total** | | **45** | **38** | Capacity factor 0.84 (38 ÷ 45) |

Reference velocity 28.00 (trailing-3, S4 to S6) × 38 ÷ 45 = **23.6 points** of planning
capacity, below the forecast's 27.33 average because of the pilot launch; the S7 review re-runs
the forecast with the real figure.

| Order | ID | Story (short title) | Points | Meets DoR | Owner / pair | Dependencies |
|---:|---|---|---:|---|---|---|
| 1 | HEL-142 | Keyboard-only operation of every journey (CR003) | 5 | yes | Devin Patel, Elena Rossi | none |
| 2 | HEL-143 | Screen-reader announcement of form errors (CR003) | 5 | yes | Devin Patel | none |
| 3 | HEL-153 | Automated regression tests for the reset and order-status journeys | 8 | yes | Frank Müller, Carla Diaz | pipeline runner capacity |
| 4 | HEL-152 | Clear message when an order number is not found | 3 | yes | Devin Patel | none |
| | | **Committed total** | **21** | | | |

- **Stretch:** none — the next ready item, HEL-145 (weekly deflection report, 8 points), does not
  fit; the 2.6 points of spare capacity absorb pilot defects (severity 1 fixed the same day and
  severity 2 within one business day, per the quality plan).
- **Skipped and why:** HEL-141 (SSO sign-in, Must, 8 points) fails the definition of ready: the
  vendor's production identity-provider tenant is not live (risk R001; SSO works in test since
  2026-07-17, but the pilot runs on email sign-in and SSO goes live only at GA). Sam Lee takes it
  to the bi-weekly steering committee; if it is not ready by S8 planning, the Must scope for GA is
  at risk and a change request follows.
- **End-of-sprint record:** completed at the S7 review on 2026-08-14.
