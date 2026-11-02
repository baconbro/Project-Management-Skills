# Project Closure Report — Helios (sample)

Sample: the completed closure report for the sample Helios project (a fictional customer
self-service portal used throughout this catalog), signed on 2026-11-20. For your own
project, copy the fill-in template `assets/closure-report.md`, not this file. The open items
summarised in section 5 are the rows of `assets/closeout-log-sample.csv`.

| Field | Value |
|---|---|
| Project | Helios customer self-service portal |
| Closure path | Completed project |
| Overall result | Delivered with approved changes |
| Sponsor | Dana Okoro, VP Customer Operations |
| Project manager | Sam Lee |
| Closure date | 2026-11-20 |
| Report version | v1.0 |
| Key records | Scope statement v1.1 acceptance log; closeout log (22 rows); lessons log LL001-LL007; PMO repository, Helios/closed |

## 1. Summary
Helios set out to cut password-reset and order-status tickets, 40% of all support tickets
and about $600,000 a year to handle, by 50% within 6 months of launch, by giving customers a
self-service portal (password reset, order status, knowledge base) with single sign-on. It
delivered all eleven baselined deliverables plus the WCAG 2.2 AA accessibility uplift
(CR003), went live to the 200-customer pilot at M4 and to all customers at M6 (go-live
2026-10-03, 100% of customers on 2026-10-12), and left hypercare on plan on 2026-10-30. It
finished $18,600 (3.7%) over the $500,000 BAC, covered from the management reserve, after an
identity-provider sandbox outage put the SSO work package two weeks behind at month 3. The
two ticket types were already 22% down in October; Priya Nair reviews the 50% target in
April 2027.

## 2. Acceptance
Criteria source: scope statement v1.1 (deliverables, criteria and one acceptor each), with
test thresholds from the definition of done.

| Deliverable | Acceptor | Decision | Date | Conditions or exceptions (owner, due) |
|---|---|---|---|---|
| D2 Requirements & user research; D3 UX design & prototype | Priya Nair; Ava Chen | Accepted | M1 | None |
| D5 Self-service UI; D8 System & UAT testing; D10 Training & communications | Priya Nair | Accepted | M4 | None |
| D6 Knowledge base | Priya Nair | Accepted with conditions | M4 | 4 migrated articles rewritten (Carla Diaz, M5); closed at M5 |
| D4 Identity / SSO integration; D9 Hardening & launch | Marcus Webb | Accepted | M4, after the first production sign-ins in the pilot | None |
| D7 Reporting & analytics | Priya Nair | Accepted | M5, after a closed month of pilot data reconciled | None |
| Product at general availability | Dana Okoro | Accepted with conditions | 2026-10-14 | D11 to be accepted at hypercare exit (Priya Nair); closed 2026-10-30 |
| D11 Operational handover | Priya Nair | Accepted | 2026-10-30 | None |
| D1 Project management outputs | Dana Okoro | Accepted by signing this report | 2026-11-20 | None |

Final acceptance by Dana Okoro on 2026-10-14. Not built and formally deferred: REQ-011 (a
Could) to Ava Chen's product backlog.

## 3. Performance against baseline
| Dimension | Baseline | Actual or final | Variance and reason |
|---|---|---|---|
| Scope | D1-D11 | D1-D11 accepted; CR003 approved and delivered; CR001 deferred to phase 2; CR005 rejected; CR006 withdrawn; CR002 and CR004 undecided, passed to the phase-2 backlog | Scope held; one approved change |
| Schedule | M1, M4, M6 | All three met; hypercare exited without extension | SSO was 2 weeks late at month 3 (issue I001); the recovery plan held the M4 pilot date |
| Cost | BAC $500,000 | Final actual cost $518,600 (final CPI 0.96) | −$18,600 (−3.7%); SSO recovery and hosting above forecast exhausted the contingency. The month-3 forecast of about $535,000 improved after the recovery plan |
| Quality | Zero open severity-1/2 defects at hypercare exit; WCAG 2.2 AA | Zero severity-1/2 for 10 consecutive business days; WCAG 2.2 AA passed on retest | 4 severity-3/4 defects transferred (section 5) |

| Milestone | Planned | Actual |
|---|---|---|
| Discovery complete | M1 | M1 |
| MVP live to pilot (200 customers) | M4 | M4 |
| General availability | M6, go-live 2026-10-03 | Go-live 2026-10-03; 100% of customers 2026-10-12 |
| Hypercare exit | 2026-10-30 | 2026-10-30 |
| Project closed | Not in the baseline | 2026-11-20 |

| Reserve | Held | Used | Approved by | Returned |
|---|---|---|---|---|
| Contingency (inside BAC) | $40,000 | $40,000: CR003 $12,000; SSO recovery (R001) $21,000; UI rework (R005) $4,000; hosting above forecast (R004) $3,000 | CCB and Sam Lee within tolerance | $0 |
| Management reserve (above BAC) | $25,000 | $18,600 for the overrun | Dana Okoro, through change control at the 2026-09-09 steering committee | $6,400 to Finance |

## 4. Handover
| Item | Receiving owner | Signed on | Evidence |
|---|---|---|---|
| Live service: runbooks, alerting, on-call rota (D11) | Priya Nair, Head of Support Operations | 2026-10-30 | Hypercare exit record from `release-and-cutover`; exit criteria E1-E9 met |
| Product backlog: CR001, CR002, CR004, REQ-011, 2 severity-3 defects | Ava Chen, product owner | 2026-11-13 | Backlog review minutes |
| Identity-provider subscription | Priya Nair | 2026-10-30 | IdentityCo standard support confirmed (exit criterion E7) |
| Hosting | Finance (operating budget holder) | 2026-11-13 | Operating budget line opened |
| Benefits measurement: ticket-deflection report and weekly dashboard | Priya Nair | 2026-11-13 | Report D7 and its query handed over |

## 5. Open items at closure
Summary of the closeout log: 22 rows; 10 closed, 11 transferred, 0 accepted as residual,
1 cancelled; none open.

| Residual risk or known exception accepted by the sponsor | Owner after closure |
|---|---|
| None. R004 (hosting cost) continues in the operations risk log | Finance |

## 6. Contracts
| Vendor and contract | Outcome | Final cost | Retention and credits | Performance rating |
|---|---|---|---|---|
| IdentityCo services (firm fixed price $22,000) | Closed 2026-11-13 through `procurement-management` | $21,120 | $2,200 retention released after the warranty ended on 2026-10-30; $880 delay credit applied | Amber: missed the sandbox milestone (I001), then recovered on a dated plan; buy again, with a named onboarding owner |
| IdentityCo subscription ($1,200 a month) | Transferred to Priya Nair as an operating contract | $6,000 for M2-M6 | None | Green |
| Cloud hosting (enterprise agreement) | Transferred to Finance as an operating cost | $15,000 for M2-M6 against a $12,000 forecast | None | Green |
| Accessibility audit firm (purchase order $4,000) | Closed 2026-09-18 | $4,000 | None | Green |

## 7. Benefits
Source: the business case benefits register. Reviews report to the monthly Customer
Operations review, chaired by Dana Okoro.

| Id | Benefit or dis-benefit | Measure | Baseline | Target and date | At closure | Owner | Review dates |
|---|---|---|---|---|---|---|---|
| B001 | Reduced ticket handling cost | Monthly tickets of the two types; weekly deflection % | 5,000 a month (May-July 2026) | 2,500 a month (−50%) by 2027-04-03 | October 3,900 (−22%); deflection 31% in the last week | Priya Nair | Monthly; formal 2027-01 and 2027-04 |
| B002 | Faster issue resolution | Mean time to resolve | 26 h | Instant self-service; 2 h assisted, by 2027-01 | Assisted 9 h | Priya Nair | 2027-01 |
| B003 | Higher customer satisfaction | Quarterly CSAT | 72% | 80% by 2027-10 | 73% | Dana Okoro | 2027-01, 2027-04, 2027-10 |
| D001 | Support agents redeployed (6 FTE) | FTE moved; attrition | 0 | 6 moved, no attrition, by 2027-04 | 2 moved; plan signed | Priya Nair | 2027-01, 2027-04 |
| D002 | CSAT dip in the cutover month | October CSAT | 72% | No more than 3 points down | No dip; closed | Dana Okoro | Closed |

## 8. Lessons learned
Post-project review held on 2026-11-04 with the whole team, combined with the post-release
review; full log: the lessons log in `lessons-learned` (LL001-LL007).

| Lesson id | Lesson (what to repeat or change) | Owner | Routed to |
|---|---|---|---|
| LL001 | Give vendor onboarding a named owner from the day of award; the late sandbox request delayed SSO | PMO Lead | PMO standard plan template: vendor onboarding workstream |
| LL002 | Report amber the moment a milestone is threatened, not two weeks later | Project Manager | PMO status-report standard |
| LL007 | Finish support-agent training one week before launch | Support Lead | PMO standard plan template |
| LL006 | Repeat: an explicit out-of-scope list prevented late scope disputes | Project Manager | Charter template (required element) |
| LL003 | Repeat: the reusable API design cut build time | Tech Lead | Engineering standards library |

## 9. Team and records
| Person | Role | Released on | Feedback to line manager |
|---|---|---|---|
| Elena Rossi | UX designer | 2026-10-16 (invited back to the review) | Yes, 2026-10-16 |
| Devin Patel | Frontend engineer | 2026-11-04 | Yes, 2026-11-04 |
| Carla Diaz | Backend engineer | 2026-11-04 | Yes, 2026-11-04 |
| Frank Müller | QA engineer | 2026-11-04 | Yes, 2026-11-04 |
| Ben Adeyemi | Tech lead | 2026-11-06 | Yes, 2026-11-06 |
| Ava Chen | Product owner | Continues as product owner for phase 2, funded by Customer Operations | Not applicable |
| Sam Lee | Project manager | 2026-11-20 | Yes, by Dana Okoro |

Records archived in the PMO repository under Helios/closed; contract records kept 7 years.
Stakeholders told on 2026-11-20 through the closure note in the communication plan;
contacts after closure: Priya Nair for the service, Ava Chen for the product.

## 10. Sign-off
| Role | Name | Decision | Date |
|---|---|---|---|
| Sponsor | Dana Okoro | Project closed | 2026-11-20 |
| Project manager | Sam Lee | Submitted | 2026-11-18 |
| Benefits owner | Priya Nair (B001, B002, D001); Dana Okoro (B003, D002) | Benefits ownership accepted | 2026-11-13 |
| Operations owner | Priya Nair | Handover accepted | 2026-10-30 |
| Finance | Finance | Cost codes closed | 2026-11-20 |

With the sponsor's signature the project is closed: no further charges, decisions or change
requests are made against it.
