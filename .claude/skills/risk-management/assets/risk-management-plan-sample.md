# Risk Management Plan — Helios (sample)

Sample: the risk management plan for the sample Helios project (a fictional customer
self-service portal used throughout this catalog), approved by the sponsor at M1 with the
baseline. Copy `risk-management-plan-template.md` for your own project.

| Field | Value |
|---|---|
| **Project** | Helios customer self-service portal |
| **Sponsor (approver)** | Dana Okoro, VP Customer Operations |
| **Project manager (process owner)** | Sam Lee |
| **Delivery approach** | Hybrid — fixed budget, milestones and integration work; UI and knowledge-base scope flexes in two-week sprints |
| **Version / date** | v1.0 / M1 |
| **Register** | `.claude/skills/risk-register/assets/risk-register-template.csv` (rows R001-R006) |
| **Response action log** | `risk-response-plan-sample.csv` |

## 1. Roles
| Role | Who | Responsibilities |
|---|---|---|
| Sponsor | Dana Okoro | Approves this plan, the appetite and the reserves; owns escalated risks; releases management reserve |
| Project manager | Sam Lee | Runs the process and reviews; controls contingency; owns R001 and R003 |
| Risk owners | Sam Lee (R001, R003), Dana Okoro (R002), Finance (R004), Elena Rossi (R005), Priya Nair (R006) | Watch the risk from the day it is logged; own its response and trigger |
| Action owners | Ben Adeyemi, Sam Lee, Dana Okoro, Finance, Elena Rossi, Priya Nair | Deliver the actions in the response log |
| Specialist reviewers | Marcus Webb (Security lead), Hana Sato (Legal & Compliance) | Rate every security and compliance risk; any MEDIUM or above goes to the sponsor |
| Steering committee | Dana Okoro (chair), Priya Nair, Finance, Marcus Webb, Hana Sato, Sam Lee | Decides escalations beyond the sponsor's authority; meets bi-weekly |
| Team | All | Raise new risks at the daily stand-up or at any time |

## 2. Scales (for ranking)
Impact takes the highest column that applies.

| Rating | Probability | Cost impact | Schedule impact | Quality / compliance |
|---|---|---|---|---|
| 1 | <= 10% | < $5,000 (< 1% of BAC) | < 1 week | Cosmetic |
| 2 | > 10% to 30% | $5,000 to < $15,000 | 1 to < 2 weeks, absorbed by float | Minor defect, workaround exists |
| 3 | > 30% to 50% | $15,000 to < $50,000 | 2 to < 4 weeks, recoverable only by fast-tracking or crashing (no schedule reserve) | A requirement only partly met |
| 4 | > 50% to 70% | $50,000 to < $100,000 | 4 to 6 weeks, threatens the M4 pilot | A Must-have requirement missed at pilot |
| 5 | > 70% | >= $100,000 (>= 20% of BAC) | > 6 weeks or misses general availability at M6 | Any security or compliance breach |

- Quantification unit for material risks: US dollars; probability as a fraction (0-1).
- Impacts are recorded as positive magnitudes; the register's `type` column says threat or opportunity.

**Helios on the matrix** (score = P x I):

```
            Impact →   1         2         3            4             5
Probability 5
            4          R005 (4)            R002 (12)
            3                              R004 (9)                   R001 (15)
            2                                           R003 (8)
                                                        R006 (8, opportunity)
            1
```

HIGH: R001. MEDIUM: R002, R004, R003, R006. LOW: R005. The money bands give the same split.

## 3. Thresholds
| Band | On the 1-5 grid (P x I) | In money (EMV) |
|---|---|---|
| HIGH | >= 15 | >= $25,000 (5% of BAC) |
| MEDIUM | >= 8 | >= $5,000 (1% of BAC) |
| LOW | Below 8 | Below $5,000 |

Scoring command used on every run:
`python .claude/skills/risk-register/scripts/risk_score.py .claude/skills/risk-register/assets/risk-register-template.csv --bac 500000`

## 4. Risk appetite
| Objective | Appetite | Meaning in practice |
|---|---|---|
| Schedule | Low | The M4 pilot and M6 general availability are committed (CON-2); any threat of more than 2 weeks to either goes to the sponsor |
| Cost | Moderate | Stay inside BAC $500,000 — the investment the business case appraised — and the charter range $450k-$550k |
| Scope and quality | Moderate for UI polish and knowledge-base breadth; low for the password-reset and order-status journeys | UI and article scope may flex in sprints; the two core journeys may not |
| Compliance and security | Zero tolerance | Data residency (CON-3) and accessibility (CON-4) are never traded; any MEDIUM or higher risk goes to the sponsor |
| Benefits (opportunities) | Moderate | Pursue an opportunity when the action costs less than the EMV it adds; never count its benefit in the budget until realised |

## 5. Reserves
| Item | Value |
|---|---|
| Target confidence for contingency | P80 |
| Method | `risk_score.py --basis residual --simulate 10000 --seed 42` on the register after responses were planned |
| Summed residual threat EMV (mean) | $52,300 (inherent $94,300 before responses) |
| Reserve at target confidence | P80 $99,000 (P50 $40,000; P90 $139,000) |
| Contingency funded (inside BAC) | **$40,000** — covers about 52% of simulated outcomes |
| Accepted gap and decision path | Funding P80 would lift BAC from $500,000 to $559,000, above the business case and the charter ceiling. The sponsor chose to hold BAC and accept the gap. R001's residual impact ($120,000) alone exceeds the reserve: if its trigger fires, Sam Lee escalates to the steering committee within 2 working days with three options — release management reserve, a scope trade-off through change control, or a re-baseline. |
| Management reserve (above BAC) | $25,000 (5% of BAC), held by Dana Okoro; released only through change control |
| Schedule reserve | None before general availability: the 25-week critical path ends 2026-09-25, leaving only the cutover week before GA on 2026-10-03. P80 is 28.25 weeks and the chance of GA readiness by week 26 is 27%; the sponsor accepted this gap at baseline, with the 2-week M6 tolerance (to 2026-10-17, about P75) and a pre-identified crash of H, Hardening & launch |
| Drawdown rule | Sam Lee draws contingency only to fund a contingent plan whose trigger has fired or an approved change, through change control: up to $5,000 within his tolerance, larger draws by the CCB from the undrawn contingency; each draw is logged with the risk or change id and reported at the next steering committee |

## 6. Cadence
| Event | When | What happens |
|---|---|---|
| New risks raised | Daily stand-up or any time | Logged with owner and type the same day |
| Team risk review | Sprint planning (every two weeks) | Team risks re-scored; HIGH threats become spikes or backlog items |
| Register review | Bi-weekly steering committee | `--check` passes; top risks, triggers and contingency drawdown against remaining exposure |
| Status report | Weekly | Top 5 risks from `--top 5 --format md` |
| Fresh identification | M1, M4 | Workshop with `risk-workshop-template.md` |
| Pre-mortem | Before the M4 pilot go/no-go and again before M6 | Pre-mortem with `risk-workshop-template.md` |
| Process audit | At M4 | Sam Lee and Dana Okoro check owners, response status and trigger watching |

## 7. Escalation
| Level | Owner | Handles | Escalate up when | Time-box |
|---|---|---|---|---|
| 1 | Risk owner | Their risk and its response | A trigger fires, or the response is late | 1 working day |
| 2 | Sam Lee | Responses and contingency within tolerance | A new HIGH risk; a contingent plan costs more than the remaining contingency; any compliance or security risk rated MEDIUM or above | 2 working days |
| 3 | Dana Okoro | Tolerance breaches, reserve gaps, escalated risks | Contingency drawdown above 50% before M4; R001's trigger fires; a decision needs management reserve, a re-baseline or another project | 2 working days |
| 4 | Steering committee / portfolio | Cross-project or enterprise risks, re-baselining | — | Next bi-weekly meeting |

## 8. Approval
| Name | Role | Decision | Date |
|---|---|---|---|
| Dana Okoro | Sponsor | Approved, with contingency held at $40,000 and the R001 decision path above | M1 |
