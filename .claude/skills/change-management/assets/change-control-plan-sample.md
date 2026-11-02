# Change Control Plan — Helios (sample)

Sample: the completed plan for the sample Helios project (a fictional customer self-service
portal used throughout this catalog), approved with the baseline at M1 and annotated with the
first decisions made under it. For your own project, copy `assets/change-control-plan-template.md`.

| Field | Value |
|---|---|
| Version / date | 1.0 / 2026-05-08 |
| Prepared by | Sam Lee, project manager |
| Approved by | Dana Okoro, VP Customer Operations (sponsor), on 2026-05-08 with the M1 baseline |
| Change log | `.claude/skills/change-request/assets/change-log.csv` (CR001-CR006) |

## 1. Baselines under control
| Baseline | Version and date | Contents | Baseline owner |
|---|---|---|---|
| Scope | v1.0, 2026-05-08 | Scope statement (11 deliverables, exclusions), traceability matrix, WBS and WBS dictionary | Ava Chen (requirements), Sam Lee (WBS) |
| Schedule | v1.0, 2026-05-08 | M1 Discovery complete, M4 MVP live to pilot (2026-08-07), M6 general availability (2026-10-03); 25-week critical path A→B→D→G→H→J, 2026-04-06 to 2026-09-25, then the cutover week; no schedule reserve before GA (accepted by the sponsor: 27% chance of GA readiness by week 26, 2-week M6 tolerance to 2026-10-17) | Sam Lee |
| Cost | v1.0, 2026-05-08 | BAC $500,000 = $460,000 of work packages + $40,000 contingency reserve; $25,000 management reserve held by the sponsor above BAC | Sam Lee with Finance |
| Quality | v1.0, 2026-05-08 | Definition of done, quality-gate and UAT exit criteria | Frank Müller |

## 2. What needs a change request
- **Needs a CR:** any change to a deliverable, a Must requirement, an acceptance criterion or an
  exclusion; a move of M4 or M6 or of a critical-path task beyond its estimate range; any draw on
  contingency or management reserve; a change to the definition of done or a gate's exit
  criteria; any change to IdentityCo's statement of work.
- **Does not need a CR:** Ava Chen re-ordering Should and Could stories for the self-service UI
  and knowledge base inside the release goal; Sam Lee re-sequencing tasks inside their float
  with no milestone effect; clerical corrections, noted in the version history.

## 3. Roles
| Role | Who | Responsibility |
|---|---|---|
| Requester | Anyone on or around the project | Raises the CR with a reason and a needed-by date |
| Change log keeper | Sam Lee | Logs, scores with `change_impact.py`, routes, tracks status, verifies and closes |
| CCB chair | Dana Okoro (delegate: Priya Nair, named in writing for leave) | Decides CCB-level changes |
| CCB members | Sam Lee, Ava Chen (product owner), Ben Adeyemi (tech lead), Priya Nair (benefit owner) | Assess and advise; never decide their own request |
| Consulted per change | Finance (any reserve draw), Marcus Webb (authentication), Hana Sato (compliance, accessibility, data), Frank Müller (quality and test) | Advise when the change touches their area |
| Quorum | Chair or delegate + Sam Lee + at least 2 members | Without quorum, defer to the next slot |

## 4. Approval tolerances
| Authority | Decides when | Funding it may commit |
|---|---|---|
| PM (Sam Lee) | LOW band, cost up to $5,000 and up to 2 working days (inclusive) | Contingency up to $5,000, or a saving |
| CCB | Above the PM limits, within the remaining contingency, no move of M6 | Contingency still undrawn |
| Sponsor (Dana Okoro) | HIGH band, or management reserve or new budget, or a move of M6, or a change to the objective, or any change that crosses a charter boundary (an in-scope outcome such as the 200-customer pilot, a milestone's definition, a cancellation criterion); a charter re-issue follows | Management reserve ($25,000); requests new budget |

Scorer settings: `--pm-limit-cost 5000 --pm-limit-days 2 --ccb-limit-cost 40000 --reserve-cost
40000` at baseline; after CR003, `--ccb-limit-cost 28000`. No `--reserve-days`: Helios holds no
schedule reserve before GA, so any day a change adds to the critical path moves GA readiness.
The scorer cannot see charter boundaries: Sam Lee routes those to the sponsor himself.

## 5. Cadence, emergency route and freezes
- **CCB slot:** Tuesdays 14:00, 30 minutes, held only when a request is pending.
- **Sponsor-level decisions:** at the bi-weekly steering committee, or an extra session within 2
  business days when a dimension turns RED (decision DEC003).
- **Decision time targets:** PM 2 business days after a complete assessment; CCB the next
  Tuesday; sponsor the next steering committee.
- **Emergency route:** Sam Lee approves severity-1/2 fixes and urgent security or compliance
  changes within 4 hours, with Ben Adeyemi's technical sign-off and Marcus Webb's for anything
  touching authentication; a retrospective CR is raised within 1 business day and ratified at
  the next CCB.
- **Change freezes (GA):** code freeze from Monday 2026-09-28 (severity-1/2 fixes only, through
  the emergency route); change freeze on the order system, ticketing system, identity provider
  and support site from Friday 2026-10-02 18:00 to Monday 2026-10-05 09:00; identity-provider
  configuration and the order-system interface need Sam Lee's approval until 2026-10-16.

## 6. Flow, decisions and status
Raise → Log → Assess → Decide → Communicate → Implement → Verify & close, with the four outcomes
and the lifecycle in `references/change-control-process.md`. Decisions so far:

| CR | Outcome | Decider / date | Rationale or conditions | Log `status` |
|---|---|---|---|---|
| CR001 Live-chat widget | Defer to phase 2 | Dana Okoro / 2026-06-16 | $60,000 exceeds the whole contingency; live chat moves contacts rather than deflecting them; revisit at the phase-2 business case | Deferred |
| CR003 WCAG 2.2 AA uplift | Approve with conditions | CCB / 2026-06-30 | $12,000 from contingency; audit in parallel with UAT preparation so no milestone moves | Approved |
| CR005 Swap analytics vendor | Reject | CCB / 2026-07-07 | 5 days on Reporting & analytics would use all of its 1 week of float, for no gain against the objective; re-raise only with a cost or quality case | Rejected |
| CR002 Partner-login SSO | Request more information | CCB / 2026-07-14 | IdentityCo's quote and Marcus Webb's security view needed; back on 2026-07-28 | Under assessment |

## 7. Communicating decisions
- **Within:** 1 business day of the decision, by email linking the CR form.
- **To:** the requester; the owners of the affected baselines; the implementation owner; Finance
  when a reserve is drawn; the risk owner; Sam Lee as IdentityCo's contract owner for vendor changes.
- **Then:** listed in the weekly status report; approved changes announced at stand-up.

Sent for CR005 on 2026-07-08: "CR005 Swap analytics vendor was rejected by the CCB on
2026-07-07. Rationale: it adds 5 days to Reporting & analytics, using all of that task's float
before the pilot, and gives no gain against the 50% ticket objective. Conditions: none. Funding: none. Next: the current
analytics vendor stays; re-raise after GA if you have a cost or quality case. Questions to Sam Lee."

## 8. Updating baselines after approval
| Baseline | Updated by | Using skill | Re-check |
|---|---|---|---|
| Scope statement, requirements, traceability | Ava Chen | `scope-and-requirements` | Every changed requirement traces to a work package and a test |
| WBS and dictionary | Sam Lee | `work-breakdown-structure` | `wbs_validate.py` passes |
| Schedule | Sam Lee | `project-schedule` | `critical_path.py`; M4 and M6 still met |
| Cost and reserves | Sam Lee with Finance | `cost-management` | `health_check.py`; contingency left after CR003: $28,000 |
| Quality | Frank Müller | `quality-management` | Gate criteria still testable |
| Risk register | Sam Lee, with each risk owner | `risk-register` | `risk_score.py`; secondary risks logged |
| Resources | Sam Lee | `resource-management` | `capacity_check.py`; no one over-allocated |
| Contracts | Sam Lee | `procurement-management` | IdentityCo contract change signed before work starts |

CR003 updated five baselines: scope statement v1.1 (Self-service UI acceptance criteria), cost
($12,000 moved from contingency to 1.3.2; BAC stays $500,000), schedule (+2 days on Self-service
UI, recovered in parallel with UAT preparation), quality (WCAG 2.2 AA in the definition of done
and UAT exit criteria) and risk (a new LOW widget risk owned by Devin Patel). An approved change,
not a re-baseline.

## 9. Verification, closure and reporting
- **Verified by:** Sam Lee, within 5 business days of Implemented: each baseline named in the
  decision has a new version citing the CR id, and the numbers agree across baselines.
- **Reported:** decided and pending CRs in the weekly status report; the change burden at each
  steering committee (at 2026-07-28: committed $12,000, 30% of the $40,000 contingency;
  committed plus pending $42,000, 105%, so CR002 and CR004 cannot both be funded from it).
- **Process health:** time from raise to decision; changes found without a CR (target 0);
  emergency-route uses; re-raised rejections.

## 10. Approval
| Name | Role | Decision | Date |
|---|---|---|---|
| Dana Okoro | Sponsor, VP Customer Operations | Approved | 2026-05-08 |
| Sam Lee | Project manager | Prepared | 2026-05-06 |
