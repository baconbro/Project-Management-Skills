# Hypercare plan — <release name>

> Fill-in template. Replace every `<angle-bracket placeholder>` and agree the plan before the
> go/no-go: the decision checks that it exists. Guidance on duration, staffing, metrics and exit
> criteria is in `references/cutover-runbook-and-hypercare.md`. A filled-in sample from the Helios
> project (a fictional customer self-service portal used throughout this catalog) follows the
> template; delete it from your copy.

## 1. Scope and dates
| Field | Value |
|---|---|
| Release and go-live | <release, version, go-live date and time> |
| Hypercare period | <start date> to <planned end date> (<n> weeks) |
| Extension rule | <extend week by week while any exit criterion fails; who decides at the weekly exit check> |
| Hypercare lead | <name, role> |
| Operations owner (accepts the service) | <name, role> |
| Go/no-go conditions and waivers to close | <ids, owners and due dates from the go/no-go checklist> |

## 2. Ramp and decommission steps inside the period
| Date | Step | Gate (all must hold) | Decided by |
|---|---|---|---|
| <date> | <ramp to n% / next wave / retire old process step> | <metrics inside thresholds; conditions closed> | <name> |

## 3. Support model and triage path
| Level | Who | Hours | How to reach |
|---|---|---|---|
| L1 service desk | <team> | <hours> | <channel or queue> |
| L2 hypercare squad | <names> | <hours plus on-call rota> | <channel or pager> |
| L3 vendors and platform teams | <names> | <contracted response> | <channel> |

Route: <user or monitoring alert> → L1 logs, classifies and applies known errors → L2 within the
service level → L3 when <condition>. Severity-1: page <hypercare lead> at once and inform
<sponsor> within <time>. A ramp step is withdrawn by <name> against the rollback triggers.

## 4. Severity and service levels
| Severity | Definition | Respond within | Restore or work around within | Fix route |
|---|---|---|---|---|
| 1 | <service down, or a key journey failing for many users, or a data or security breach> | <minutes> | <hours> | <hotfix through the emergency change route> |
| 2 | <a key journey broken for a segment, workaround exists> | <time> | <time> | <next patch or hotfix> |
| 3 | <defect with a workaround> | <time> | <time> | <weekly patch> |
| 4 | <cosmetic or enhancement> | <time> | <not applicable> | <product backlog> |

## 5. Staffing by week
| Week | Dates | Coverage hours | Squad on hand | Service desk role |
|---|---|---|---|---|
| 1 | <dates> | <extended hours plus nights on call> | <names> | <shadows the squad> |
| <n> | <dates> | <business hours plus on call> | <names> | <runs alone; squad on call only> |

## 6. Daily stand-down
<hh:mm>, 15 minutes, chaired by <hypercare lead>; attendees <squad, service-desk lead, product
owner, vendor when needed>. Frequency: <daily in weeks n-n, then n times a week>. Agenda:
incidents since the last stand-down by severity · metrics against thresholds · next ramp or
decommission step · next patch content · known errors to publish · risks and issues to log.

## 7. Metrics and thresholds
| Metric | Source | Target | Threshold and action if breached |
|---|---|---|---|
| <stability: incidents by severity, availability> | <tool> | <target> | <action> |
| <performance: page load, error rate> | <tool> | <target> | <action> |
| <adoption: active users, journey completion> | <tool> | <target> | <action> |
| <business: deflection, satisfaction> | <report> | <target> | <action> |
| <support load: contacts about the new service> | <queue> | <target> | <action> |

## 8. Fixes and releases during hypercare
Patch cadence <day and time>; each patch passes <regression pack> and a short go/no-go by
<name>; emergency fixes go through <emergency change route> with <name>'s approval; the change
freeze on shared systems lifts on <date or condition>.

## 9. Communications
| Audience | What | When | Owner |
|---|---|---|---|
| <sponsor and steering committee> | <daily note, then the weekly status report> | <cadence> | <name> |
| <support agents> | <known errors and changes> | <cadence> | <name> |
| <customers or end users> | <known issues, ramp news, incident notices> | <trigger> | <name> |

## 10. Exit criteria
| # | Criterion (measurable) | Evidence | Status |
|---|---|---|---|
| E1 | <zero open severity-1/2 defects for n consecutive business days> | <defect tracker> | <met / not met> |
| E2 | <contacts about the new service below n per day for the last week> | <queue report> | <met / not met> |
| E3 | <service desk met every service level without the squad for the last n business days> | <service-level report> | <met / not met> |
| E4 | <all go/no-go conditions and waivers closed> | <go/no-go checklist> | <met / not met> |
| E5 | <runbooks, alerts and known-error articles updated for every fix> | <runbook review> | <met / not met> |
| E6 | <open defects moved to the operations backlog with priority and owner> | <backlog> | <met / not met> |
| E7 | <operations owner signs acceptance> | <signature below> | <met / not met> |

## 11. Handover and acceptance
| Item | Value |
|---|---|
| Exit review | <date>; attendees <names> |
| Open defects transferred | <count and ids>; owner <name> |
| Squad on-call rota stood down | <date> |
| Accepted by (operations owner) | <name, role, date> |
| Hypercare lead sign-off | <name, date> |
| Exit record sent to project closure | <date> |
| Post-release review | <date>; lessons sent to lessons-learned <date> |

---

## Sample: Helios general availability hypercare plan (filled in)
Sample from the sample Helios project (a fictional customer self-service portal used throughout
this catalog), as agreed before the go/no-go of 2026-09-30. Exit status is shown as planned.

### 1. Scope and dates
| Field | Value |
|---|---|
| Release and go-live | Release 2.0, general availability (M6), go-live Saturday 2026-10-03 09:00 |
| Hypercare period | 2026-10-03 to Friday 2026-10-30 (4 weeks, the warranty period in the acceptance criterion of WBS 1.5.2; Priya Nair accepts D11 Operational handover at exit) |
| Extension rule | Extend week by week while any exit criterion fails; Sam Lee and Priya Nair decide at the Friday exit check |
| Hypercare lead | Sam Lee, project manager |
| Operations owner | Priya Nair, Head of Support Operations |
| Go/no-go items to close | C1 training (Priya Nair, 2026-10-06) · C2 three severity-3 fixes (Ben Adeyemi, 2026-10-08) · W1 order-status probe (Ben Adeyemi, 2026-10-09) |

### 2. Ramp and decommission steps
| Date | Step | Gate | Decided by |
|---|---|---|---|
| Sat 2026-10-03 | Pilot cohort (200) → 25% of customers | Cutover runbook checkpoints passed | Sam Lee |
| Wed 2026-10-07 | 25% → 50% | Zero open sev-1/2; SSO success at least 98% on days 1-3; C1 closed | Sam Lee, Dana Okoro informed |
| Mon 2026-10-12 | 50% → 100% (GA complete) | Patch 1 live; C2 and W1 closed; metrics inside thresholds | Dana Okoro on Sam Lee's recommendation |
| Mon 2026-10-19 | Retire the password-reset and order-status ticket-form categories | A full week at 100% inside thresholds | Priya Nair |

### 3. Support model and triage path
| Level | Who | Hours | How to reach |
|---|---|---|---|
| L1 service desk | Support Operations agents (trained) | 07:00-22:00 in week 1, then 08:00-18:00 | Support queue tagged "portal" |
| L2 hypercare squad | Ben Adeyemi, Carla Diaz, Devin Patel, Frank Müller | Same hours plus a night on-call rota in weeks 1-2 | Hypercare channel; pager for severity-1 |
| L3 vendors | Identity-provider vendor; hosting platform team | 4-hour response during hypercare | Vendor priority line via Ben Adeyemi |

Route: customer or synthetic probe → L1 logs, classifies and applies known errors → L2 → L3 for
identity-provider or hosting faults. Severity-1: page Sam Lee at once; Dana Okoro informed
within one hour; a suspected data or security breach also goes to Marcus Webb. Sam Lee may
withdraw the latest ramp step against the rollback triggers in the go/no-go checklist.

### 4. Severity and service levels
| Severity | Definition | Respond | Restore or work around | Fix route |
|---|---|---|---|---|
| 1 | Portal down; SSO sign-in failing for more than 5% of attempts; data shown to the wrong customer | 15 min | 2 h (flag back one ramp step) | Same-day hotfix, emergency change |
| 2 | Reset, order status or search broken for a segment; phone is the only workaround | 1 h | 1 business day | Hotfix or next patch |
| 3 | Defect with a workaround published as a known error | 1 business day | Not applicable | Weekly patch |
| 4 | Cosmetic issue or enhancement idea | 3 business days | Not applicable | Product backlog (Ava Chen) |

### 5. Staffing by week
| Week | Dates | Coverage | Squad on hand | Service desk role |
|---|---|---|---|---|
| 1 | 10-03 to 10-09 | 07:00-22:00 plus nights on call | All four, seated with the service desk | Shadows the squad |
| 2 | 10-12 to 10-16 | 08:00-20:00 plus nights on call | All four | Leads, squad backs up |
| 3 | 10-19 to 10-23 | Business hours plus on call | Ben Adeyemi, Frank Müller | Leads |
| 4 | 10-26 to 10-30 | Business hours | On call only | Runs alone (tests exit criterion E3) |

### 6. Daily stand-down
09:30, 15 minutes, chaired by Sam Lee; squad, the service-desk lead, Ava Chen and Priya Nair,
the vendor when needed. Daily in weeks 1-2, Monday-Wednesday-Friday in weeks 3-4.

### 7. Metrics and thresholds
| Metric | Source | Target | Threshold and action |
|---|---|---|---|
| SSO sign-in success | Identity-provider log and portal telemetry | At least 98% a day | Below 95% over 15 min: severity-1, flag back one ramp step |
| Availability | Synthetic probes every 5 min | At least 99.5% a week | Any outage over 5 min: severity-1 or 2 |
| p95 page load and error rate | Monitoring dashboard | Under 2 s; under 0.1% | Over 4 s or over 1% for 10 min: severity-1 |
| Journey completion (reset, order status) | Portal analytics | At least 80% of started journeys | Below 70% for a day: review drop-off at the stand-down |
| Portal-related contacts at L1 | Support queue | Falling week on week | Above 50 a day: known-error review and comms |
| Deflection of the two ticket types | Weekly deflection report (HEL-145) against the 3-month pre-launch baseline | Reported weekly; the 50% target is the 6-month benefit | Flat for two weeks: Priya Nair raises it at steering |
| CSAT on support interactions | Monthly CSAT | No more than 3 points below the 72% baseline (D002) | Breach: steering decides on extra comms or a slower ramp |

### 8. Fixes and releases during hypercare
Weekly patch on Thursdays at 18:00 (patch 1 on 2026-10-08), each passing the automated
regression pack (HEL-153) and a 10-minute go/no-go by Sam Lee with Frank Müller and Ben
Adeyemi. Emergency fixes need Sam Lee's approval through the emergency change route. After the
cutover-weekend change freeze ends on Monday 2026-10-05, changes to the identity-provider
configuration or the order-system interface still need Sam Lee's approval until 2026-10-16,
when the 100% ramp has run for a stable working week.

### 9. Communications
| Audience | What | When | Owner |
|---|---|---|---|
| Dana Okoro and the steering committee | One-paragraph daily note, then the weekly status report | Daily in week 1, then weekly | Sam Lee |
| Support agents | Known errors, ramp dates and changes | Daily huddle | Priya Nair |
| Customers | Known-issue banner, welcome email at each ramp step, incident notices | On each event | Priya Nair |

### 10. Exit criteria
| # | Criterion | Evidence | Status |
|---|---|---|---|
| E1 | Zero open severity-1/2 defects for 10 consecutive business days | Defect tracker | Planned |
| E2 | Portal-related contacts below 20 a day for the last week | Support queue report | Planned |
| E3 | Service desk met every service level without the squad in week 4 | Service-level report | Planned |
| E4 | C1, C2 and W1 closed | Go/no-go checklist | Planned |
| E5 | Runbook, alerts and known-error articles updated for every hypercare fix; no unactioned alerts in week 4 | Runbook review | Planned |
| E6 | Open severity-3/4 defects in the Support Operations backlog or Ava Chen's product backlog, each with priority and owner | Backlogs | Planned |
| E7 | Identity-provider support moved from the 4-hour hypercare terms to the standard contract | Vendor confirmation | Planned |
| E8 | Retired ticket-form categories not reinstated for 7 days | Support-site configuration log | Planned |
| E9 | Priya Nair signs acceptance of the service | Section 11 | Planned |

### 11. Handover and acceptance
| Item | Value |
|---|---|
| Exit review | Friday 2026-10-30; Sam Lee, Priya Nair, Ben Adeyemi, Ava Chen, Dana Okoro |
| Open defects transferred | Listed at the exit review; owners in the receiving backlogs |
| Squad on-call rota stood down | At acceptance |
| Accepted by | Priya Nair, Head of Support Operations, at the exit review |
| Hypercare lead sign-off | Sam Lee, at the exit review |
| Exit record sent to project closure | Within two business days of acceptance, for the handover step in `project-closure` |
| Post-release review | Within two weeks of exit; lessons to `lessons-learned`; benefits tracking continues monthly with Priya Nair against the business-case baseline |
