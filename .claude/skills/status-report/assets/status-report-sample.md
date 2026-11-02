# Sample status report — Helios — weekly, 2026-07-10

> **Sample, not a template.** The weekly status report of the sample Helios project (a fictional
> customer self-service portal used throughout this catalog), sent by Sam Lee on Friday
> 2026-07-10 as the pre-read for the bi-weekly steering committee of Tuesday 2026-07-14. Every
> name and figure is fictional and follows the catalog's Helios canon: earned value is the
> month-3 close in `cost-management` (CPI 0.93, SPI 0.92, AMBER). The fill-in version is
> `status-report-template.md`; the ratings history behind the trend arrows is
> `rag-history-sample.csv`.

| | |
| --- | --- |
| **Project** | Helios customer self-service portal |
| **Status date / data cut-off** | 2026-07-10 / 2026-07-09 (weekly control review); EVM as at the month-3 close, 2026-07-03 |
| **Reporting period** | 2026-07-06 to 2026-07-10 (decisions since the 2026-06-30 steering included) |
| **Prepared by / sent** | Sam Lee (project manager) / 2026-07-10 |
| **Audience and distribution** | Steering committee pre-read: Dana Okoro (sponsor, chair), Priya Nair, Finance, Marcus Webb, Hana Sato; key stakeholders per communication plan row C03 |
| **Overall RAG** | **AMBER** — previous (2026-07-03): AMBER — trend: **↓ worsening** (this week scope pressure rose and quality turned AMBER; cost and schedule hold at the month-3 close, after CPI 1.00 → 0.93 and SPI 0.94 → 0.92 since the month-2 close) |
| **Red triggers** | SSO not working in test by 2026-07-24 (M4 would then be more than 2 weeks late) · EAC above $550,000 (the composite forecast, $558,468, is already there if the schedule slip keeps adding cost) |
| **Tolerances** | Schedule: 2 weeks on M4 or M6 · Cost: EAC up to $550,000, the charter ceiling and stop trigger (BAC $500,000 + management reserve $25,000 = $525,000 sits below it) |

## Summary
Helios is AMBER and worsening: IdentityCo's sandbox outage (issue I001) has made the Identity /
SSO work package RED, moving the M4 pilot forecast one week late to 2026-08-14 and the cost
forecast to about $535,000 against the $500,000 budget — above budget plus management reserve,
still inside the $550,000 tolerance. The vendor's recovery plan met its first date (sandbox back
on 2026-07-06); its real test is SSO working in test by 2026-07-17. On 2026-07-14 we need Dana
Okoro to decide DEC002 (approve the recovery plan and how to fund the overrun) and whether
protecting M4 comes before partner logins (CR002).

## Decisions needed
| Id | Decision | Options (effect on cost / dates / scope) | Recommendation | Decider | Decide by | If no decision |
| --- | --- | --- | --- | --- | --- | --- |
| DEC002 | Approve IdentityCo's dated recovery plan, and draw management reserve now or later? | 1 Approve the plan; release reserve through change control (EAC about $535,000; M4 +1 week). 2 Also crash SSO with IdentityCo premium support, a $20,000 change request (ACT004): M4 back to 2026-08-07, but the CPI forecast rises to about $555,000, past the $550,000 stop line. 3 Trade scope through change control to stay inside BAC (M4 +1 week). | Option 1 now; size the reserve draw once SSO works in test on 2026-07-17 | Dana Okoro | 2026-07-14 (steering) | The M4 pilot slips further and the overrun grows unfunded |
| To log after steering | Protect M4 first, or add partner logins (CR002) now? The CCB decides CR002 at 14:00 the same day | 1 Defer CR002 until SSO works in test. 2 Approve CR002 now: $18,000 and 10 days on the RED SSO package. | Option 1: $28,000 of contingency is undrawn and the crash option plus CR002 would need $38,000 | Dana Okoro (priority); CCB (CR002) | 2026-07-14 | The CCB decides CR002 without a priority and the contingency is over-committed |

## RAG by dimension
| Dimension | RAG (prev → now, trend) | Evidence: measure vs threshold | Forecast | Owner | Action / decision (due) |
| --- | --- | --- | --- | --- | --- |
| Schedule | AMBER → AMBER, → steady | SPI 0.92 (0.85–0.95 band); SPI(t) 0.93, SV(t) −0.9 weeks; M4 slip inside the 2-week tolerance | M4 2026-08-14 (+1 week); M6 2026-10-03 on the likely release forecast, +1 week on the pessimistic one | Sam Lee | DEC002 at steering (2026-07-14); SSO working in test (2026-07-17) |
| Cost | AMBER → AMBER, → steady | CPI 0.93 (0.85–0.95 band); EAC above BAC ($500,000) and above BAC + management reserve ($525,000), inside the $550,000 tolerance; TCPI(BAC) 1.07 vs CPI 0.93: landing on BAC is not credible | EAC $535,032 (BAC / CPI); range $516,500 (one-off) to $558,468 (composite) | Sam Lee | Funding of the overrun decided in DEC002 (2026-07-14); Finance flagged on 2026-06-30 |
| Scope | AMBER → AMBER, ↓ worsening | Pending CRs: 1 (CR002), $18,000, 10 days, MEDIUM, decided by the CCB on 2026-07-14; plus the $20,000 crash option for steering; $38,000 asked against $28,000 contingency undrawn | Release cut line holds on the likely forecast; 17 points fall below it on the pessimistic one | Ava Chen | Priority set at steering, then CR002 at the CCB (2026-07-14) |
| Quality | GREEN → AMBER, ↓ worsening | Something the M4 gate depends on is overdue: stale QA data (I003, due 2026-07-08) makes test results unreliable; real-provider journey tests (ACT003) still blocked until SSO works in test. I002 (order-status page 3 s vs 2 s criterion) and ACT005 (two colour-contrast conditions of the S4 acceptance) due 2026-07-17. No gate failed | M4 go/no-go evidence complete only if SSO works in test by 2026-07-17 | Frank Müller | QA data refreshed (new date 2026-07-14); ACT003 run within 2 working days of SSO working in test (2026-07-21) |

**RED work packages** (the dimensions above are AMBER; these are not):
- 1.3.1 Identity / SSO integration — CPI 0.69, SPI 0.75 (EV $45,000, PV $60,000, AC $65,000) —
  owner Ben Adeyemi — IdentityCo recovery plan: sandbox restored 2026-07-06 (met), SSO working in
  test 2026-07-17; $880 delay credit claimed; milestone payment held until acceptance.
- 1.3.4 Reporting & analytics — CPI 0.71, SPI 0.67, waiting on self-service UI data — owner
  Carla Diaz — the deflection dashboard v1 is the sprint S5 goal (review 2026-07-17).

**Budget:** BAC $500,000 · AC to date $252,000 (50.4% of BAC) · EV $235,500 (47.1% complete) ·
EAC $535,032 (BAC / CPI) · VAC −$35,032 (−7.0%) · TCPI(BAC) 1.07 vs CPI 0.93 · contingency
$12,000 drawn (CR003) / $28,000 undrawn of $40,000, and the forecast overrun already needs all of
it · management reserve $25,000 undrawn (held by Dana Okoro) · cost tolerance $550,000 · EVM as
at 2026-07-03.

*Agile (sprints underneath the milestones):* velocity S1–S4 22, 27, 31, 29 points (average
27.25, minimum 22, trailing-3 29.0); 149 points left including CR003's 12; 6 sprints left (S5–S10,
the last ending 2026-09-25); likely 6 sprints (fits), pessimistic 7 (ends 2026-10-09, 17 points
short): release outlook AMBER.

## Milestones
| Milestone | Baseline | Forecast | Variance | RAG | Owner | Recovery action (due) |
| --- | --- | --- | --- | --- | --- | --- |
| M1 Discovery complete | 2026-05-08 | met 2026-05-08 | 0 | GREEN (complete) | Sam Lee | — |
| SSO working in test (IdentityCo, WBS 1.3.1) | 2026-07-03 | 2026-07-17 | +2 weeks (1 week beyond task C's float) | RED | Ben Adeyemi | Vendor recovery plan ACT001: sandbox restored 2026-07-06 (met); next date 2026-07-17 |
| M4 MVP live to the 200-customer pilot | 2026-08-07 | 2026-08-14 | +1 week | AMBER | Sam Lee | DEC002 at steering (2026-07-14) |
| M6 General availability | 2026-10-03 | 2026-10-03 (likely); 2026-10-09 (pessimistic) | 0 / +1 week | AMBER | Ava Chen | Keep 17 points of low-priority scope below the cut line at S6 planning (2026-07-20) |

## Progress this period (outcomes, not activity)
- IdentityCo's sandbox restored on 2026-07-06, the first date in the recovery plan (ACT001).
- Sprint S4 increment accepted by Ava Chen on 2026-07-03 (29 of 32 points): pilot-ready reset
  and order journeys against the identity-provider stub, with two colour-contrast conditions
  (ACT005).
- CR003 accessibility uplift approved by the CCB on 2026-06-30 and planned into sprint S5; CR005
  rejected by the CCB on 2026-07-07.
- Costed $20,000 crash change request (ACT004) delivered in this pre-read, as the 2026-06-30
  steering asked.

## Changes this period
| CR | Title | Status | Cost / days | Decided or to be decided by (date) |
| --- | --- | --- | --- | --- |
| CR002 | Extend SSO to partner logins | Pending (raised 2026-07-08, under assessment) | $18,000 / 10 | CCB (2026-07-14, 14:00) |
| ACT004 | Crash SSO with IdentityCo premium support | To be raised as a change request with DEC002 | $20,000 / protects M4 | Dana Okoro (2026-07-14) |
| CR005 | Swap analytics vendor | Rejected | $4,000 / 5 | CCB (2026-07-07) |
| CR003 | Accessibility (WCAG 2.2 AA) uplift | Approved, in sprint S5 | $12,000 from contingency / 2 | CCB (2026-06-30) |

## Top risks and issues
| Id | Type | Description | Severity, trend | Owner | Next action (due) |
| --- | --- | --- | --- | --- | --- |
| I001 | issue | IdentityCo sandbox down 2026-06-12 to 2026-07-06 blocked SSO testing; risk R001 has occurred | High, ↑ improving | Carla Diaz | SSO working in test (2026-07-17) |
| R002 | risk | Undocumented requirements expand portal scope: three new requirements since the baseline (CR001, CR003, CR002); the trigger fires at more than three | MEDIUM, ↓ worsening | Dana Okoro | Priority at steering; every addition through change control (2026-07-14) |
| ACT003 / I003 | issue | Real-provider journey tests blocked; QA environment data stale (2 days overdue) | High / Low, ↓ worsening | Frank Müller | QA data refreshed (2026-07-14); ACT003 (2026-07-21) |
| DEP002 | dependency | Legal's data-residency sign-off is needed before the M4 pilot | Medium, → steady | Sam Lee (Hana Sato signs) | Sign-off (2026-07-24); steering item 5 |
| R006 | opportunity | Knowledge base deflects tickets earlier than planned | MEDIUM, → steady | Priya Nair | Top-20 articles published before the pilot (2026-08-07) |

## Next period
- SSO working in test against the real identity provider — Ben Adeyemi with IdentityCo — 2026-07-17
- DEC002 and the CR002 priority decided — Dana Okoro — 2026-07-14; CR002 at the CCB the same day
- Sprint S5 review: CR003 uplift and the deflection dashboard v1 accepted — Ava Chen — 2026-07-17
- I002 and ACT005 fixed — Devin Patel — 2026-07-17
- Real-provider journey tests (ACT003) passed — Frank Müller — 2026-07-21
- Data-residency sign-off (DEP002) — Hana Sato with Sam Lee — 2026-07-24

## Links
Risk register `.claude/skills/risk-register/assets/risk-register-template.csv` · issue log
`.claude/skills/project-delivery/assets/issue-log-sample.csv` · change log
`.claude/skills/change-request/assets/change-log.csv` · EVM
`.claude/skills/cost-management/assets/evm-history-sample.csv` · RAG history
`rag-history-sample.csv`
