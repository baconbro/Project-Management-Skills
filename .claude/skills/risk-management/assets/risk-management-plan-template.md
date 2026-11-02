# Risk Management Plan — <project name>

Fill-in template: replace every `<placeholder>`; delete guidance in *italics* once filled.
A completed example is in `risk-management-plan-sample.md`.

| Field | Value |
|---|---|
| **Project** | `<project name>` |
| **Sponsor (approver)** | `<name, title>` |
| **Project manager (process owner)** | `<name>` |
| **Delivery approach** | `<waterfall / agile / hybrid — one line on what is fixed and what flexes>` |
| **Version / date** | `<v0.1 / yyyy-mm-dd>` |
| **Register** | `<path to your copy of .claude/skills/risk-register/assets/risk-register-template.csv>` |
| **Response action log** | `<path to your copy of risk-response-plan-template.csv>` |

## 1. Roles
| Role | Who | Responsibilities |
|---|---|---|
| Sponsor | `<name>` | Approves this plan, the appetite and the reserves; owns escalated risks; releases management reserve |
| Project manager | `<name>` | Runs the process and reviews; controls contingency; first escalation point |
| Risk owners | Named per risk in the register | Watch the risk from the day it is logged; own its response and trigger |
| Action owners | Named per action in the response log | Deliver each response action by its due date |
| Steering committee | `<members>` | Decides escalations beyond the sponsor's authority; meets `<cadence>` |
| Team | All | Raise new risks at `<stand-up / sprint planning / any time>` |

## 2. Scales (for ranking)
*Probability bands must not overlap; impact takes the highest row that applies.*

| Rating | Probability | Cost impact | Schedule impact | Other (quality, compliance, reputation) |
|---|---|---|---|---|
| 1 | `<e.g. <= 10%>` | `<e.g. < 1% of BAC>` | `<e.g. < 1 week>` | `<description>` |
| 2 | `<range>` | `<range>` | `<range>` | `<description>` |
| 3 | `<range>` | `<range>` | `<range>` | `<description>` |
| 4 | `<range>` | `<range>` | `<range>` | `<description>` |
| 5 | `<e.g. > 70%>` | `<e.g. >= 20% of BAC>` | `<e.g. misses a committed milestone>` | `<description>` |

- Quantification unit for material risks: `<currency>`; probability as a fraction (0-1).
- Impacts are recorded as positive magnitudes; the register's `type` column says threat or opportunity.

## 3. Thresholds
| Band | On the 1-5 grid (P x I) | In money (EMV) |
|---|---|---|
| HIGH | `<default >= 15>` | `<default >= 5% of BAC = amount>` |
| MEDIUM | `<default >= 8>` | `<default >= 1% of BAC = amount>` |
| LOW | Below MEDIUM | Below MEDIUM |

Scoring command used on every run:
`python .claude/skills/risk-register/scripts/risk_score.py <register.csv> <--bac BAC | --high X --medium Y | --prob-scale 1-5 --impact-scale 1-5>`

## 4. Risk appetite
| Objective | Appetite | Meaning in practice |
|---|---|---|
| Schedule | `<low / moderate / high>` | `<e.g. no threat to milestone X above N weeks without sponsor sign-off>` |
| Cost | `<appetite>` | `<e.g. stay inside the charter range>` |
| Scope and quality | `<appetite>` | `<what may flex, what may not>` |
| Compliance and security | `<appetite>` | `<e.g. zero tolerance; any MEDIUM risk goes to the sponsor>` |
| Benefits (opportunities) | `<appetite>` | `<when an opportunity is worth pursuing>` |

## 5. Reserves
| Item | Value |
|---|---|
| Target confidence for contingency | `<e.g. P80>` |
| Method | `<residual simulation with risk_score.py --basis residual --simulate / summed residual EMV x uplift>` |
| Summed residual threat EMV (mean) | `<amount>` |
| Reserve at target confidence | `<amount>` |
| Contingency funded (inside BAC) | `<amount>` — covers `<x>`% of simulated outcomes |
| Accepted gap and decision path | `<none / what is not covered, who decides, and the options if it is needed>` |
| Management reserve (above BAC) | `<amount and policy, e.g. 5% of BAC>`, held by `<sponsor>` |
| Schedule reserve | `<duration at confidence>`, held before `<milestone>` |
| Drawdown rule | `<who may draw contingency, for what, and how it is recorded>` |

## 6. Cadence
| Event | When | What happens |
|---|---|---|
| New risks raised | `<e.g. stand-up / any time>` | Logged with owner and type the same day |
| Team risk review | `<e.g. sprint planning>` | Team risks re-scored; HIGH threats become spikes or backlog items |
| Register review | `<e.g. steering committee>` | `--check` passes; top risks, triggers, reserve drawdown reviewed |
| Status report | `<e.g. weekly>` | Top 5 risks from `--top 5 --format md` |
| Fresh identification | `<milestones / stage gates>` | Workshop with `risk-workshop-template.md` |
| Pre-mortem | `<before go-live>` | Pre-mortem with `risk-workshop-template.md` |
| Process audit | `<e.g. each stage>` | Are risks owned, responses done, triggers watched? |

## 7. Escalation
| Level | Owner | Handles | Escalate up when | Time-box |
|---|---|---|---|---|
| 1 | Risk owner | Their risk and its response | `<trigger>` | `<time>` |
| 2 | Project manager | Responses and contingency within tolerance | `<trigger, e.g. a new HIGH risk>` | `<time>` |
| 3 | Sponsor | Tolerance breaches, reserve gaps, escalated risks | `<trigger, e.g. drawdown above x% before milestone>` | `<time>` |
| 4 | Steering committee / portfolio | Cross-project or enterprise risks, re-baselining | — | `<next meeting>` |

## 8. Approval
| Name | Role | Decision | Date |
|---|---|---|---|
| `<name>` | Sponsor | `<approved / approved with conditions>` | `<yyyy-mm-dd>` |
