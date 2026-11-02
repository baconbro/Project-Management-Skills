# Engagement Assessment Matrix — Helios (sample)

Sample: the filled matrix for the sample Helios project (a fictional customer self-service
portal used throughout this catalog), built from `stakeholder-register-sample.csv` in week 2.
For your own project, copy the blank `engagement-matrix.md`.

**Confidential.** This matrix records candid judgements about named people. Share it with the
sponsor and the row owners only; the communication plan is the document you circulate.

| Version | As of | Prepared by | Reviewed with the sponsor |
|---|---|---|---|
| 1.0 | 2026-04-15 | Sam Lee | Dana Okoro, 2026-04-15 |

## 1. Current (C) versus desired (D) engagement

| Id | Stakeholder (role) | Quadrant | Unaware | Resistant | Neutral | Supportive | Leading | Gap | Owner |
|---|---|---|---|---|---|---|---|---|---|
| S01 | Dana Okoro (VP Customer Operations, sponsor) | Manage Closely | | | | C | D | +1 | Sam Lee |
| S02 | Priya Nair (Head of Support Operations, benefit owner) | Manage Closely | | | C | | D | +2 | Sam Lee |
| S03 | Marcus Webb (Security lead) | Keep Satisfied | | | C | D | | +1 | Ben Adeyemi |
| S04 | Hana Sato (Legal & Compliance) | Keep Satisfied | C | | D | | | +2 | Sam Lee |
| S05 | IdentityCo (identity-provider vendor) | Manage Closely | | | C | D | | +1 | Sam Lee |
| S06 | Finance (budget holder) | Keep Satisfied | C | | D | | | +2 | Sam Lee |
| S07 | Pilot customers (cohort of 200) | Keep Informed | C | | | D | | +3 | Ava Chen |
| S08 | Support agents (60) | Keep Informed | | C | | D | | +2 | Priya Nair |
| S09 | Order management team (order API) | Keep Satisfied | | | C | D | | +1 | Ben Adeyemi |
| S10 | Marketing (GA launch campaign) | Monitor | | | C D | | | 0 | Ava Chen |

## 2. Closing the gaps (priority order)

| Priority | Id | Stakeholder | From → to | Concern to address | Action | Owner | Due |
|---|---|---|---|---|---|---|---|
| 1 | S02 | Priya Nair | Neutral → Leading | Redeployment of 6 FTE of agents (dis-benefit D001); a 50% target her team did not set; being bypassed in design | Co-lead the 3 Support Operations requirements workshops; sign off the benefit baseline; agree the redeployment plan with HR; run the M4 pilot with her teams first | Sam Lee | Baseline signed by M1; redeployment plan before cutover |
| 2 | S01 | Dana Okoro | Supportive → Leading | The 50% ticket cut within the $500,000 BAC; no surprises | Hold a weekly 1:1; chair the bi-weekly steering committee; decide escalations within 2 business days; co-present the M4 pilot launch | Sam Lee | Weekly from week 2 |
| 3 | S05 | IdentityCo | Neutral → Supportive | Fixed-price margin; requests outside the SOW such as partner logins | Run a weekly working session (Ben Adeyemi), a monthly performance review and an executive review at M4 and M6; write down the escalation path | Sam Lee | Contract signature in week 5 |
| 4 | S06 | Finance | Unaware → Neutral | Spend against the $500,000 BAC; hosting overrun (R004) | Give an onboarding brief; send a monthly cost summary (CPI, SPI, EAC); flag any forecast above BAC before steering | Sam Lee | Brief before the M1 baseline approval |
| 5 | S04 | Hana Sato | Unaware → Neutral | Data residency of identity and knowledge-base data; accessibility policy (WCAG 2.1 AA, CON-4) | Give a 30-minute data-flow briefing; set the data-residency sign-off as a gate before the M4 pilot | Sam Lee | Briefing in week 3; sign-off by 2026-07-24 |
| 6 | S03 | Marcus Webb | Neutral → Supportive | Credential handling, MFA, session timeout | Run the threat-model review in Discovery; hold a security sign-off gate before the M4 pilot; consult him on every authentication change | Ben Adeyemi | Threat model by M1 |
| 7 | S09 | Order management team | Neutral → Supportive | Load on the order API; change freezes | Agree API access and a load-test window; track the dependency in the issue log | Ben Adeyemi | Week 6 |
| 8 | S07 | Pilot customers | Unaware → Supportive | Ease of use; privacy; keeping the phone channel | Send invitations and onboarding; recruit volunteers for the usability rounds; add a feedback button; survey in week 4 of the pilot | Ava Chen | Invitations 2 weeks before M4 |
| 9 | S08 | Support agents | Resistant → Supportive | Job security; a new triage route; pilot workload | Brief every team (Priya Nair) once the redeployment plan is agreed; put 20 agents in UAT; run train-the-trainer (WBS 1.5.1); plan adoption with `change-management` | Priya Nair | Briefings after priority 1; training before cutover |
| — | S10 | Marketing | Neutral (no gap) | Launch timing and messaging | Maintain: add to the GA launch distribution list; re-rate at M4 | Ava Chen | M4 |

Priorities 1 and 9 are one campaign: the agents will not move until their own head of
department visibly leads and the redeployment plan is agreed, so Priya Nair's row comes first
even though the agents' gap is the same size.

## 3. How to read it
- **C and D in one cell (no gap):** maintain; do not over-invest (Marketing).
- **C left of D:** raise engagement with the action in section 2 (every other row).
- **C right of D:** over-engaged; none in Helios at this review.
- **Unaware:** brief first, then re-rate (Hana Sato, Finance, pilot customers).

## 4. What the sponsor agreed
- 2026-04-15: Dana Okoro will agree the 50% target with Priya Nair in person before the M1
  baseline approval, rather than by email.
- 2026-04-15: the security and data-residency sign-offs become entry criteria for the M4 pilot
  go/no-go.
- 2026-04-15: the register stays confidential to Sam Lee, Dana Okoro and the row owners.

## 5. Review history

| Date | Reviewed by | Moves (id: from → to) | Evidence | Next review |
|---|---|---|---|---|
| 2026-04-15 | Sam Lee, Dana Okoro | First assessment | Initiation interviews; kickoff attendance; Priya Nair's questions about headcount | Manage Closely rows at the next steering committee; whole register at M1 |

## 6. Handoffs
- [x] Actions with a cadence passed to `project-communication` as communication-plan rows with
      the same owners.
- [x] Register ids S01–S10 passed to `raci-matrix` with the people who hold each role.
- [x] Every high-power or high-interest stakeholder (all rows except Marketing, including both
      approvers) passed to `scope-and-requirements` for the elicitation plan.
- [ ] IdentityCo's contacts confirmed against the contract in `procurement-management` at
      signature (week 5).
