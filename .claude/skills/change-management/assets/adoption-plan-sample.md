# Adoption Plan — Helios (sample)

Sample: the completed adoption plan for the sample Helios project (a fictional customer
self-service portal used throughout this catalog), as agreed at the steering committee of
2026-07-28, ahead of the M4 pilot, with one later status note. For your own project, copy
`assets/adoption-plan-template.md`.

| Field | Value |
|---|---|
| Version / date | 1.1 / 2026-07-28 |
| Prepared by | Sam Lee, project manager |
| Sponsor | Dana Okoro, VP Customer Operations |
| Benefit owner | Priya Nair, Head of Support Operations |
| Releases covered | MVP to the pilot cohort of 200 (M4) on 2026-08-07; general availability (M6) from 2026-10-03, ramped 25% → 50% → 100% to 2026-10-12 |

## 1. The change
- **What changes:** customers reset passwords, check order status and search the knowledge base
  on the portal instead of raising tickets; support agents point those contacts to the portal,
  and 6 FTE of agents move to the complex-case queue.
- **Who must change:** 60 support agents; the 200 pilot customers; then all portal customers.
- **Benefit it serves:** B001, password-reset and order-status tickets down 50% within 6 months
  of launch.
- **Old path to retire:** the password-reset and order-status ticket-form categories on
  2026-10-19, decided by Priya Nair after a full week at 100% inside the hypercare thresholds.

## 2. Sponsor actions (active and visible)
| ADKAR step | Sponsor action | Audience | Date | Status |
|---|---|---|---|---|
| Awareness | Present the case for change: 40% of tickets, about $600k a year, the 50% target | Customer Operations all-hands | 2026-05-14 | Done |
| Desire | Agree the 50% target with Priya Nair in person before the baseline | Priya Nair | Before 2026-05-08 | Done |
| Desire | With Priya Nair, brief every agent team in person on the signed redeployment plan | 60 support agents | Week of 2026-08-03 | Planned |
| Knowledge / Ability | Co-present the M4 pilot launch; protect agents' training time from queue targets | Pilot teams, all agents | 2026-08-07; September | Planned |
| Reinforcement | Review the adoption dashboard at every bi-weekly steering committee | Steering committee | From 2026-08-11 | Planned |
| Reinforcement | Thank the pilot teams and the agents who rewrote knowledge-base articles at the GA launch | All agents | 2026-10-03 | Planned |
| Reinforcement | Announce the retirement of the old ticket-form categories | Agents and customers | 2026-10-12, effective 2026-10-19 | Planned |

Change leaders under the sponsor: Priya Nair co-leads the agent briefings, runs the M4 pilot
with her teams first and decides the old-path retirement; her team leads run a weekly floor
huddle on portal questions.

## 3. Readiness assessment
| Group | Size | Impact | Attitude | Capacity | History | Readiness | Weakest ADKAR step | Evidence |
|---|---|---|---|---|---|---|---|---|
| Support agents | 60 | High | Resistant | Low (20 released for UAT; pilot workload) | Mixed | Low | Desire (job security) | Initiation interviews; stakeholder register S08; slow UAT sign-up |
| Pilot customers | 200 | Medium | Unaware | High | None (first self-service channel) | Medium | Awareness | Usability rounds; pilot recruitment |
| All portal customers | All | Medium | Unaware | High | None | Medium | Awareness, then Knowledge | Pilot results and survey, to be confirmed in week 4 of the pilot |

## 4. Adoption targets (agreed before go-live)
| Id | Group | Measure | Baseline | Target | By | Source | Owner |
|---|---|---|---|---|---|---|---|
| T1 | Support agents | Agents trained on the portal and the new triage route | 0 of 60 | 60 of 60 | 2026-10-03 (go-live) | Training attendance | Priya Nair |
| T2 | Pilot customers | Pilot customers completing at least one reset or order-status journey on the portal | 0 of 200 | At least 120 (60%) | 2026-09-04 (4 weeks after M4) | Portal analytics | Ava Chen |
| T3 | All customers | Started reset and order-status journeys completed | New measure | At least 80% a day | Through hypercare, to 2026-10-30 | Portal analytics | Ava Chen |
| T4 | All customers | Weekly self-service deflection of the two ticket types | 0% | At least 30%; then at least 40% | 2026-10-30; 2027-01-31 | Weekly deflection report (HEL-145) | Priya Nair |
| T5 | Support agents | Agents redeployed to the complex-case queue (dis-benefit D001) | 0 FTE | 6 FTE, no attrition | 2027-04-03 | HR records | Priya Nair |
| T6 | All | Monthly password-reset and order-status tickets (benefit B001) | 5,000 a month (May-July 2026) | 2,500 a month (−50%) | 2027-04-03 | Ticketing system | Priya Nair |

Agreed by Dana Okoro and Priya Nair on 2026-07-28. Guardrail: CSAT on support interactions no
more than 3 points below the 72% baseline in the cutover month (dis-benefit D002, Dana Okoro).

## 5. Actions by ADKAR gap
| Group | Gap | Action (lever) | Owner | Due | WBS / backlog ref |
|---|---|---|---|---|---|
| Support agents | Desire | Agree and sign the redeployment plan with HR (6 FTE, no attrition); sponsor briefings | Priya Nair | Plan 2026-07-31; briefings week of 2026-08-03 | D001 |
| Support agents | Desire | Put 20 agents in UAT; invite agents to review knowledge-base articles | Frank Müller; Ava Chen | From 2026-07-27 | WBS 1.4.1; DEP001 |
| Support agents | Knowledge | Train-the-trainer, then team sessions on the portal and the new triage route | Priya Nair | Before 2026-10-03 | WBS 1.5.1 |
| Support agents | Ability | Hypercare squad seated with the service desk; job aid for walking a customer through the portal | Sam Lee | 2026-10-03 to 2026-10-09 | WBS 1.5.2 |
| Pilot customers | Awareness | Invitations and onboarding | Ava Chen | 2026-07-24 | WBS 1.5.1 |
| Pilot customers | Knowledge | How-to video; feedback button; survey in week 4 of the pilot | Ava Chen | 2026-09-04 | Product backlog |
| All customers | Awareness | GA announcements per the communication plan; portal links on the old ticket form | Ava Chen with Marketing | From 2026-10-03 | WBS 1.5.1 |

## 6. Resistance log
| Id | Source | What we see or hear | Root cause | Type | Response | Owner | Status |
|---|---|---|---|---|---|---|---|
| RS1 | Support agents | "If customers self-serve, our jobs go"; slow UAT sign-up | Fear of job loss; the redeployment plan is not yet announced | Reluctance (Desire) | Signed redeployment plan; in-person briefings by Dana Okoro and Priya Nair; agents in UAT | Priya Nair | Responding |
| RS2 | Support agents in the pilot teams | "The knowledge-base articles are wrong for order-status edge cases" | Genuine content gap | Product flaw | Articles corrected through the product backlog; agents review new articles before GA | Ava Chen | Open |
| RS3 | Pilot customers | Some keep phoning for password resets | Habit; distrust of email reset links | Reluctance (Awareness, Knowledge) | Phone stays open in the pilot; agents send the portal link and walk the customer through once; reasons asked in the week-4 survey | Ava Chen | Open |

## 7. Go-live adoption readiness criteria
Handed to the GA go/no-go checklist in `release-and-cutover`:
- All 60 support agents trained on the portal and the new triage route (T1; checklist SU1).
- The redeployment plan for 6 FTE signed (D001; checklist SU2).
- Pilot adoption target T2 met, or the gap accepted by Dana Okoro with a condition.
- GA customer and agent communications ready (`project-communication`).

## 8. Reinforcement and handover
- **Review cadence:** T3 and T4 daily at the hypercare stand-down in weeks 1-2, then weekly;
  the adoption dashboard at each bi-weekly steering committee.
- **Recognition:** Dana Okoro thanks the pilot teams at the GA launch; Priya Nair names the
  month's top knowledge-base contributors at the floor huddle.
- **Old path retired:** the two ticket-form categories on 2026-10-19, announced by Dana Okoro on
  2026-10-12, decided by Priya Nair after a full week at 100% inside thresholds.
- **Feedback loop:** the portal feedback button and the agents' huddle notes, triaged weekly by
  Ava Chen; defects go to the defect log, ideas to the product backlog.
- **Owner after handover:** Priya Nair from hypercare exit (2026-10-30), reviewed monthly at the
  Customer Operations review chaired by Dana Okoro, with formal reviews in 2027-01 and 2027-04.

## 9. Approval
| Name | Role | Decision | Date |
|---|---|---|---|
| Dana Okoro | Sponsor | Agreed | 2026-07-28 |
| Priya Nair | Benefit owner | Agreed | 2026-07-28 |

**Status note, 2026-09-30 (GA go/no-go):** T1 stood at 54 of 60 trained, the other six agents
being on leave. The gap became condition C1: they complete training by 2026-10-06, and until
then only trained agents take portal-related contacts.
