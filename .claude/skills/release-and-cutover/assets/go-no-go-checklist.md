# Go/no-go checklist — <release name>

> Fill-in template. Replace every `<angle-bracket placeholder>`, delete rows that do not apply and
> add your own. Fill sections 1-3 at T-6 to T-4 weeks, update section 2 at each readiness review,
> and complete sections 4-5 in the decision meeting and section 6 on the day. Verdict rules,
> waiver limits and the meeting agenda are in `references/go-no-go-and-rollback.md`. A filled-in
> sample from the Helios project (a fictional customer self-service portal used throughout this
> catalog) follows the template; delete it from your copy.

## 1. Decision frame
| Field | Value |
|---|---|
| Release / milestone | <release name, version and milestone> |
| Release strategy and stage | <big-bang / phased wave n / pilot / parallel run / flag ramp to n%> |
| Cutover window | <date, start-end time, time zone>; go-live (T0) <hh:mm> |
| Freezes | Code <from date>; change <from-to>; business <from-to or not needed> |
| Readiness reviews | T-4w <date> · T-2w <date> · T-1w <date> |
| Decision meeting | <date hh:mm> (T-<n> days) |
| Approver (decides) | <name, role> |
| Driver (recommends) | <name, role> |
| Consulted (each states go or no-go aloud) | <names and areas> |
| Informed | <names or groups> |
| Operations owner (accepts the service after hypercare) | <name, role> |

## 2. Readiness criteria
Status: Met / Not met / Waived. Blocking Y: an unmet, unwaived item forces NO-GO.

| # | Area | Criterion (measurable) | Owner | Evidence | Blocking | Status |
|---|---|---|---|---|---|---|
| BU1 | Scope and build | <release scope accepted by the product owner; release candidate id frozen> | <name> | <record or link> | Y | <status> |
| TE1 | Test and quality | <zero open severity-1/2 defects at decision time> | <name> | <defect report> | Y | <status> |
| TE2 | Test and quality | <UAT signed off by the business owner> | <name> | <sign-off> | Y | <status> |
| TE3 | Test and quality | <performance at forecast peak: threshold> | <name> | <load-test report> | Y | <status> |
| SE1 | Security and compliance | <no open high or critical security findings> | <name> | <retest report> | Y | <status> |
| SE2 | Security and compliance | <privacy, legal and accessibility sign-offs> | <name> | <signed memo or audit> | Y | <status> |
| DA1 | Data | <migration rehearsed; reconciliation within tolerance; backup restore tested> | <name> | <rehearsal log> | <Y/N> | <status> |
| OP1 | Operations | <runbooks accepted; on-call rota published for the hypercare period> | <name> | <signed review> | Y | <status> |
| OP2 | Operations | <monitoring, alerting and dashboards live in production> | <name> | <paging test> | Y | <status> |
| SU1 | Support and training | <service desk and end users trained: target %> | <name> | <attendance record> | <Y/N> | <status> |
| CM1 | Communications | <notices sent; go-live and rollback templates approved> | <name> | <sent log, templates> | N | <status> |
| VE1 | Vendors | <critical vendors confirmed for the window and for hypercare> | <name> | <written confirmation> | Y | <status> |
| CU1 | Cutover and rollback | <runbook rehearsed inside the window with at least 30 minutes margin> | <name> | <rehearsal log> | Y, never waivable | <status> |
| CU2 | Cutover and rollback | <rollback rehearsed and timed; triggers agreed> | <name> | <rehearsal log> | Y, never waivable | <status> |
| RI1 | Risk | <no open HIGH risk without an active response; cutover risks logged; register check passes> | <name> | <register check output> | Y | <status> |
| BZ1 | Business | <business calendar clear; benefits baseline captured> | <name> | <calendar, baseline report> | N | <status> |

## 3. Rollback readiness
| Item | Value |
|---|---|
| Rollback triggers (quantified, time-boxed) | <trigger 1>; <trigger 2>; <trigger 3> |
| Who may call a rollback without escalation | <name, role> |
| Full rollback duration (rehearsed / budget) | <minutes> / <minutes> |
| Point of no return | <runbook step and time, or none and why> |
| Last safe rollback start | <window end> − <rollback minutes> = <hh:mm> |
| Rollback-window checkpoint | <hh:mm>, at least 30 minutes before the last safe rollback start |

## 4. Open items at decision
**Conditions** (non-blocking items still open)

| # | Condition | Owner | Due | Must be met before |
|---|---|---|---|---|
| <C1> | <what must be done> | <name> | <date> | <go-live / ramp step / hypercare exit> |

**Waivers** (blocking items accepted by the approver)

| # | Criterion waived | Compensating control | Owner | Expiry | Risk id |
|---|---|---|---|---|---|
| <W1> | <criterion id and gap> | <control in place until expiry> | <name> | <date> | <risk id> |

## 5. Poll and decision
| Consulted lead | Area | Go / no-go | Comment |
|---|---|---|---|
| <name> | <area> | <go or no-go> | <reason or condition> |

- **Verdict:** <GO / CONDITIONAL GO / NO-GO>
- **Decided by:** <approver> on <date hh:mm> · **Recorded by:** <scribe>
- **Delegation for the window:** <cutover lead> may call go-live and rollback against the triggers in section 3
- **If NO-GO:** reason <reason>; fix owner <name>; new decision date <date>; no-go message sent <time>
- **Decision sent to:** <audiences from the communication plan> at <time>

## 6. Day-of checkpoint (bridge opening, before the first production change)
- [ ] Every step owner and vendor contact is on the bridge.
- [ ] No new severity-1/2 defect or production incident since the decision.
- [ ] Every condition due before go-live is closed; every waiver's compensating control is in place.
- [ ] Backups are scheduled in the runbook and the rollback team is on standby.
- [ ] The cutover lead confirms the start: <name, time>.

---

## Sample: Helios general availability go/no-go (filled in)
Sample from the sample Helios project (a fictional customer self-service portal used throughout
this catalog). The runbook it approves is `assets/cutover-runbook-sample.csv`; the hypercare
plan is the sample in `assets/hypercare-plan-template.md`.

### 1. Decision frame
| Field | Value |
|---|---|
| Release / milestone | Release 2.0, general availability (GA), milestone M6 |
| Release strategy and stage | Flag ramp from the 200-customer pilot to 25% at go-live, 50% on 2026-10-07, 100% on 2026-10-12 |
| Cutover window | Saturday 2026-10-03, 06:00-12:00 local; go-live (T0) 09:00 |
| Freezes | Code from Monday 2026-09-28; change on shared systems Friday 18:00 to Monday 09:00; no business freeze (no master data moves) |
| Readiness reviews | T-4w 2026-09-02 · T-2w 2026-09-16 · T-1w 2026-09-23 |
| Decision meeting | Wednesday 2026-09-30 15:00 (T-3 days) |
| Approver (decides) | Dana Okoro, Sponsor, VP Customer Operations |
| Driver (recommends) | Sam Lee, project manager |
| Consulted | Ava Chen (scope), Ben Adeyemi (technical, operations, vendor), Marcus Webb (security), Priya Nair (support, training, business) |
| Informed | Steering committee, Hana Sato (Legal & Compliance), Finance, support agents |
| Operations owner | Priya Nair, Head of Support Operations |

### 2. Readiness criteria
| # | Area | Criterion | Owner | Evidence | Blocking | Status |
|---|---|---|---|---|---|---|
| BU1 | Scope and build | Must and Should stories (84 points) accepted; release candidate 2.0 frozen | Ava Chen | Sprint 10 review record, 2026-09-25 | Y | Met |
| BU2 | Scope and build | SSO sign-in (HEL-141) accepted against the identity provider's production tenant | Ben Adeyemi | Vendor confirmation of the live tenant; acceptance record | Y | Met |
| TE1 | Test and quality | Zero open severity-1/2 defects | Frank Müller | Defect report 2026-09-30 12:00: 0 sev-1, 0 sev-2, 3 sev-3 with workarounds | Y | Met (see C2) |
| TE2 | Test and quality | UAT signed off by Priya Nair after testing with 20 Support Operations agents | Frank Müller | UAT sign-off | Y | Met |
| TE3 | Test and quality | Load test at forecast launch peak: 95% of pages under 2 s, error rate under 0.1% (HEL-150) | Ben Adeyemi | Load-test report | Y | Met |
| SE1 | Security and compliance | Penetration retest shows no open high or critical finding (HEL-151) | Marcus Webb | Retest report | Y | Met |
| SE2 | Security and compliance | Privacy notice and terms updated for SSO; legal sign-off; WCAG 2.2 AA audit passed (CR003) | Hana Sato | Signed memo; accessibility audit by Elena Rossi | Y | Met |
| DA1 | Data | 150 knowledge-base articles migrated and reviewed; top 50 questions answered; snapshot restore tested | Carla Diaz | Content audit; restore test in rehearsal | N | Met |
| OP1 | Operations | Runbook and alerting accepted (HEL-155); on-call rota published for the 4-week hypercare | Ben Adeyemi | Service-desk sign-off of the runbook review | Y | Met |
| OP2 | Operations | Synthetic probes, dashboards and paging live for all three journeys | Ben Adeyemi | Paging test; probe list | Y | Waived (W1) |
| SU1 | Support and training | All 60 support agents trained on the portal and the new triage route | Priya Nair | Attendance: 54 of 60 trained | N | Not met (C1) |
| SU2 | Support and training | Redeployment plan for 6 FTE agreed (dis-benefit D001) | Priya Nair | Signed plan | N | Met |
| CM1 | Communications | Pilot and customer notices sent; go-live and rollback templates approved | Priya Nair | Sent log; templates approved by Sam Lee | N | Met |
| VE1 | Vendors | Identity-provider vendor on the bridge for the window and on 4-hour response for hypercare | Ben Adeyemi | Written confirmation | Y | Met |
| CU1 | Cutover and rollback | Runbook v1.3 rehearsed inside the window with at least 30 minutes margin | Sam Lee | Rehearsal 2026-09-26: 25 min late on re-index; re-sequenced in v1.3 | Y | Met |
| CU2 | Cutover and rollback | Full rollback rehearsed within its 75-minute budget; triggers agreed | Ben Adeyemi | Rehearsal log: 70 minutes | Y | Met |
| RI1 | Risk | No open HIGH risk without an active response; cutover risks logged; register check passes | Sam Lee | `risk_score.py --check` PASS; R001 response complete (production tenant live) | Y | Met |
| BZ1 | Business | No month-end or peak trading in the window; ticket-volume baseline (3 months pre-launch) captured | Priya Nair | Calendar; deflection report baseline (HEL-145) | N | Met |

### 3. Rollback readiness
| Item | Value |
|---|---|
| Rollback triggers | Any severity-1 not fixed within 30 minutes; SSO sign-in success below 95% over 15 minutes (at least 20 attempts); error rate above 1% or p95 page load above 4 s for 10 minutes; data-integrity mismatch after migration; runbook more than 45 minutes late at the go-live checkpoint |
| Who may call a rollback without escalation | Sam Lee (cutover lead); Dana Okoro informed |
| Full rollback duration (rehearsed / budget) | 70 / 75 minutes (R1 → R5 → R6) |
| Point of no return | None: the portal owns no master data; rollback redirects users to the ticket channel |
| Last safe rollback start | 12:00 − 75 minutes = 10:45 |
| Rollback-window checkpoint | 10:00 (runbook step 18) |

### 4. Open items at decision
| # | Condition | Owner | Due | Must be met before |
|---|---|---|---|---|
| C1 | The 6 agents on leave complete portal training; until then only trained agents take portal-related contacts | Priya Nair | 2026-10-06 | The 50% ramp on 2026-10-07 |
| C2 | Fix the 3 severity-3 defects; publish their workarounds as known errors before go-live | Ben Adeyemi | 2026-10-08 (hypercare patch 1) | The 100% ramp on 2026-10-12 |

| # | Criterion waived | Compensating control | Owner | Expiry | Risk id |
|---|---|---|---|---|---|
| W1 | OP2: no synthetic probe yet for the order-status journey (carrier test hook not available in production) | Service desk runs the order-status journey by hand every 2 hours, 07:00-22:00, until the probe ships | Ben Adeyemi | 2026-10-09 (probe in patch 1) | Logged as a cutover risk |

### 5. Poll and decision
| Consulted lead | Area | Go / no-go | Comment |
|---|---|---|---|
| Ava Chen | Scope | Go | Could stories cut at the forecast line; Must and Should complete |
| Ben Adeyemi | Technical, operations, vendor | Go | With W1; vendor confirmed for the window |
| Marcus Webb | Security | Go | Retest clean; joins step 11 on the day |
| Priya Nair | Support, training, business | Go | With C1; trained agents only until 2026-10-06 |

- **Verdict:** CONDITIONAL GO
- **Decided by:** Dana Okoro on 2026-09-30 15:40 · **Recorded by:** Elena Rossi
- **Delegation for the window:** Sam Lee may call go-live and rollback against the triggers in section 3
- **Decision sent to:** steering committee, all step owners, Support Operations and the identity-provider vendor at 16:15

### 6. Day-of checkpoint (Saturday 2026-10-03, 06:00, runbook step 4)
- [x] Every step owner and the identity-provider vendor contact is on the bridge.
- [x] No new severity-1/2 defect or production incident since the decision.
- [x] No condition is due before go-live; W1's manual order-status checks are rostered from 07:00.
- [x] Snapshot (step 5) and rollback team R1-R7 on standby.
- [x] The cutover lead confirms the start: Sam Lee, 06:12.
