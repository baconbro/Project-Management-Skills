# Change Control Process

Change control protects the project's baselines from uncontrolled change. The point is not to
prevent change (change is inevitable and often good) but to make every change *visible,
assessed, decided, communicated and reflected in every affected baseline*. Without it, scope
creep quietly consumes the budget and the schedule until the project is late and over budget
and nobody can say why.

Examples use the sample Helios project (a fictional customer self-service portal used
throughout this catalog): sponsor Dana Okoro (VP Customer Operations), project manager Sam Lee,
BAC $500,000 including a $40,000 contingency reserve, a $25,000 management reserve above it,
pilot at M4 (2026-08-07) and general availability at M6 (2026-10-03).

**Who owns what.** `change-request` owns the change request (CR) form and the **change log
artifact** (`.claude/skills/change-request/assets/change-log.csv`) and its scorer,
`change_impact.py`. This process owns the governance around them: what needs a CR, the change
control board (CCB), the approval tolerances, the emergency route and change freezes, the
decision and its communication, and verification that the baselines were updated. Write the
procedure down with `assets/change-control-plan-template.md`.

## What needs a change request
| Change | Route |
|---|---|
| Adds, removes or alters a deliverable, a Must requirement, an acceptance criterion or an exclusion | CR |
| Moves a baselined milestone, or a critical-path task beyond its estimate range | CR |
| Draws contingency, releases management reserve, or needs new budget | CR (funding is part of the decision) |
| Changes the definition of done, a quality gate's exit criteria or a vendor's statement of work | CR |
| Re-orders backlog items inside the release goal, sprint length and budget | No CR: the product owner decides |
| Re-sequences tasks inside their float with no milestone, budget or scope effect | No CR: the PM records it in the schedule |
| Corrects a clerical error in a plan (a typo, a wrong cross-reference) | No CR: note it in the version history |
| A problem that has already happened | Log it as an issue in `project-delivery`; raise a CR only if the fix changes a baseline |

## The end-to-end flow

```
Raise -> Log -> Assess -> Decide -> Communicate -> Implement -> Verify & close
  |       |       |         |            |              |              |
anyone  change  5 impact  PM / CCB /  requester +    baseline      PM checks every
        log id  ratings,  sponsor     affected       owners        baseline cites the
                options               owners         update        CR id; log closed
```

1. **Raise.** Anyone may request a change. Capture it on the CR form from `change-request`:
   what, why, who, and the date a decision is needed by. Nothing is "informal".
2. **Log.** Give it the next free id in the change log, status `Raised`. The log artifact is
   owned by `change-request` (`.claude/skills/change-request/assets/change-log.csv`); the PM
   keeps the project's copy current.
3. **Assess.** Rate scope, cost, schedule, quality and risk 1-5 with real units, lay out at
   least two options (one is "do nothing") and a recommendation, then score and route it with
   `change_impact.py`. Do not skip this for "small" changes; a small change still gets a LOW
   score and goes to the PM in minutes.
4. **Decide.** The authority the tolerances name (PM, CCB or sponsor) chooses one of the four
   outcomes below and records the decision, rationale, decider, date, conditions and funding
   source on the CR form and in the log.
5. **Communicate.** Tell the requester and every affected owner the decision, the rationale
   and the conditions, in writing, within one business day (see below).
6. **Implement.** For an approved change, the implementation owner does the work and each
   baseline owner issues a new version of their baseline (see "After approval"). Status
   `Implemented` once the work is done.
7. **Verify and close.** The PM confirms the work is done *and* that every affected baseline
   carries a new version citing the CR id; then status `Closed`. A rejected or deferred change
   is closed at the decision, with its reason (see the lifecycle).

### Decision outcomes
| Outcome | Use when | Record on the form and in the log | Log `status` |
|---|---|---|---|
| **Approve** (with or without conditions) | The benefit justifies the impact and funding exists | Conditions, funding source, baselines to update, implementation owner and due date | `Approved` |
| **Reject** | The impact outweighs the benefit, or it conflicts with an objective or constraint | The reason, in terms the requester can act on, and what new evidence would justify re-raising it | `Rejected` |
| **Defer** | Worth doing, but not now (a later phase, after a milestone, when funded) | The reason, a revisit date or trigger, and where it is parked (for example the phase-2 backlog) | `Deferred` |
| **Request more information** | The assessment cannot support a decision yet | The specific questions, who answers each, and the return date (normally the next CCB slot) | back to `Under assessment` |

Helios: CR003 (WCAG 2.2 AA uplift) approved with conditions by the CCB on 2026-06-30, $12,000
from contingency; CR005 (swap analytics vendor) rejected by the CCB on 2026-07-07 because it
moved the critical Reporting & analytics task 5 days for no gain against the objective; CR001
(live-chat widget, $60,000, more than the whole contingency) deferred to phase 2 by Dana Okoro on
2026-06-16; CR002 (extend SSO to partner logins) sent back on 2026-07-14 for IdentityCo's quote
and Marcus Webb's security view, so it stays `Under assessment`.

### Communicate the decision
A decision nobody hears about is not a decision: rejected requests resurface next month and
requesters learn to go around the board.
- **Who:** the requester; the owner of every baseline to update; the implementation owner;
  Finance when a reserve is drawn; the risk owner when a risk changes; the vendor, through the
  contract owner, when a statement of work changes.
- **What:** the decision, the rationale, any conditions, the funding source, what happens next
  and by when; for a rejection, what would change the answer; for a deferral, the revisit date.
- **How and when:** in writing (an email or a message linking the CR form) within one business
  day, never verbally only; then in the next weekly status report and at stand-up for the team.

### Change log status lifecycle
The lifecycle stages map onto the `status` values that `change-request` writes in the log:

```
Open -> Assessed -> Decided --approve------------------> Implemented -> Closed (verified)
                       |--reject / defer------------------> closed at the decision, with reason
                       |--request more information--------> back to Assessed
```

| Stage | Log `status` | Enters when | Exits when |
|---|---|---|---|
| Open | `Raised` | The CR has an id, a description, a raiser and a needed-by date | An assessor is named |
| Assessed | `Under assessment` | Assessment starts (or the decider asked for more information) | Five ratings, options, a recommendation, a score and an authority exist |
| Decided | `Approved`, `Rejected` or `Deferred` | The decision is recorded | It is communicated; approved work starts, rejected and deferred CRs end here |
| Implemented | `Implemented` | The work is done and the baseline owners have issued new versions | The PM has verified every affected baseline |
| Closed | `Closed` | Verification is recorded | Never: terminal |

A rejected or deferred CR is closed at the decision: its status stays `Rejected` or `Deferred`
(the log reserves `Closed` for implemented-and-verified changes, so the change-burden totals stay
right), the reason sits in "Conditions / rationale" on the CR form, and a deferral carries a
revisit date. To see reasons in the log itself, add a `decision_note` column; `change_impact.py`
passes extra columns through. Never delete a row.

## The change control board (CCB)
- **Membership:** the sponsor or a named delegate as chair, the PM (who runs the log and the
  agenda), and the voices the changes touch: product owner, technical lead, benefit owner;
  Finance, security, compliance and quality are consulted per change.
- **Decision rule:** the chair decides after hearing the members; consensus is welcome, not
  required. A member does not decide their own request.
- **Quorum:** the chair (or delegate), the PM and at least two members; otherwise defer to the
  next slot or escalate to the sponsor.
- **Cadence:** a fixed slot (Helios: Tuesdays, 30 minutes, held only when a request is pending)
  plus the emergency route. Sponsor-level changes go to the steering committee (Helios:
  bi-weekly, or an extra session within 2 business days).
- **Agenda order:** by the needed-by date and value, not by impact band; the band says how deep
  the assessment goes and who decides, not what matters most.

A CCB that rubber-stamps everything adds no control; one that is too slow gets bypassed. Tune
the tolerances so routine changes flow and only material ones reach the board.

## Approval tolerances
| Authority | Decides | Helios |
|---|---|---|
| PM | LOW impact band and within the PM limits, funded from contingency or a saving | Up to $5,000 and 2 working days (inclusive); CR006 |
| CCB | Everything above the PM limits that the remaining contingency can fund, with no move of general availability | CR002-CR005 |
| Sponsor | HIGH band; management reserve or new budget; a move of the GA milestone (M6); a change to an objective or benefit | CR001 |

Helios in one line: the PM approves changes up to $5,000 and 2 days within contingency, larger
ones go to the CCB, and HIGH-impact ones, any management-reserve release and any move of M6 go
to the sponsor. Give the same numbers to the scorer so its routing matches the plan, setting
`--ccb-limit-cost` to the contingency still undrawn ($40,000 at baseline, $28,000 after CR003):

```bash
python .claude/skills/change-request/scripts/change_impact.py .claude/skills/change-request/assets/change-log.csv --pm-limit-cost 5000 --pm-limit-days 2 --ccb-limit-cost 28000 --reserve-cost 40000
```

The scorer routes on impact band, money and days only. The PM applies the other sponsor
triggers (management reserve, a move of M6, a change to an objective) when routing, and a
request may always be escalated a tier, never routed down one.

## Emergency route and change freezes
- **Emergency route:** for a severity-1 or severity-2 production fix, or a change needed now to
  protect security, safety or compliance. A named approver (Helios: Sam Lee, with Ben Adeyemi
  for technical sign-off and Marcus Webb for anything touching authentication) decides within
  hours; the CR is raised retrospectively within one business day and the CCB ratifies it at
  its next slot. An emergency route used for convenience is a bypass: report how often it is used.
- **Change freezes:** before a release, stop all change except through the emergency route.
  State each freeze's start, end and systems. Helios GA: code freeze from Monday 2026-09-28;
  change freeze on the order system, ticketing system, identity provider and support site from
  Friday 2026-10-02 18:00 to Monday 2026-10-05 09:00; identity-provider configuration and the
  order-system interface still need Sam Lee's approval until 2026-10-16. `release-and-cutover`
  puts the freezes in the runbook and checks them at the go/no-go.

## Integrated change control
A change is reflected *across every affected baseline at once*: approve a scope addition and the
schedule, the cost baseline, the quality plan, the resource plan and the risk register move with
it, in one decision, not piecemeal. Helios CR002 (extend SSO to partner logins, $18,000, 10
days, scored 3.40 MEDIUM) is not just "more development": it adds partner-login requirements and
acceptance tests, extends the Identity / SSO work package that already slipped (issue I001),
draws contingency on top of the $12,000 CR003 took, changes IdentityCo's statement of work, adds
security test cases and raises the identity-provider risk (R001). Assessed alone it looks
affordable; with the other pending CRs it would take committed plus pending changes to $42,000,
105% of the contingency, which is why the board sees the cumulative burden every time.

## After approval: who updates which baseline
The implementation owner does the work; each baseline owner issues the new version of their
baseline citing the CR id; the PM verifies. Use the specialist skill for each update.

| Baseline | What changes | Updated with | Re-check | Helios CR003 |
|---|---|---|---|---|
| Scope | Scope statement, requirements and acceptance criteria, traceability matrix | `scope-and-requirements` | Every changed requirement traces to a work package and a test | Self-service UI acceptance criteria; scope statement v1.1 |
| Scope | WBS and WBS dictionary | `work-breakdown-structure` | Re-run `wbs_validate.py` | No new element; 1.3.2 dictionary entry updated |
| Schedule | Durations, dependencies, milestones | `project-schedule` | Re-run `critical_path.py`; do M4 and M6 still hold? | +2 days on Self-service UI, recovered in parallel with UAT preparation |
| Cost | Control-account budgets, contingency, BAC | `cost-management` | Re-run `health_check.py`; contingency left | $12,000 from contingency to 1.3.2; $28,000 left; BAC stays $500,000 |
| Quality | Definition of done, quality plan, gate exit criteria | `quality-management` | Gate criteria still testable | WCAG 2.2 AA added to the definition of done and the UAT exit criteria |
| Risk | New secondary risks, re-scored risks, risk cover | `risk-register` | Re-run `risk_score.py` | New LOW risk: a third-party widget fails the audit (Devin Patel) |
| Resources | Assignments and capacity | `resource-management` | Re-run `capacity_check.py` | Devin Patel 8 days, Elena Rossi 2 days |
| Contracts | A vendor's statement of work or price | `procurement-management` | Contract change signed before work starts | Not affected (CR002 would be) |

The scripts are `.claude/skills/work-breakdown-structure/scripts/wbs_validate.py`,
`.claude/skills/project-schedule/scripts/critical_path.py`,
`.claude/skills/cost-management/scripts/health_check.py`,
`.claude/skills/risk-register/scripts/risk_score.py` and
`.claude/skills/resource-management/scripts/capacity_check.py`; run each with `--help`. Report
approved changes and the change burden in the next `status-report`.

## Approved change or re-baseline?
An approved CR gives the affected baseline components a new version and keeps the variance
history; it is not a re-baseline. Drawing contingency moves budget inside BAC; releasing
management reserve raises BAC through change control. Re-baseline (replace the whole remaining
baseline, with the sponsor's approval, keeping the old snapshot) only when the remaining plan is
so different that variances against it mean nothing. The test and the procedure are in
`.claude/skills/project-planning/references/baseline-guide.md`. Helios: CR003 was an approved
change (scope statement v1.1), not a re-baseline; CR001 would have needed new budget and a
re-baseline, one reason it was deferred to phase 2.

## Verify and close
Before setting `Closed`, the PM checks, for each baseline named in the decision: the new version
exists, it cites the CR id, and the numbers agree across baselines (the schedule days, the cost
moved and the scope added are the same change). Record "verified by / date" on the CR form.
Verification of an approved change is due within five business days of `Implemented`; an
approved CR left open for weeks hides a baseline that no longer matches reality.

## Agile and hybrid
- The product owner re-orders the backlog inside the release goal, the sprint length and the
  budget without a CR; the sprint review is where those changes are made visible.
- A CR is needed only when a change breaks the fixed frame: the budget, the release date, a
  contracted or committed Must, the definition of done.
- Hybrid (Helios): M4, M6, the $500,000 BAC and the contracted SSO scope are under the CCB; the
  self-service UI and knowledge-base Should and Could stories flex in the backlog.

## Is the process working?
Track, and report at steering: time from raise to decision (Helios target: PM 2 business days,
CCB the next Tuesday slot, sponsor the next steering); changes found implemented without a CR
(target zero); emergency-route uses; rejected requests re-raised without new evidence; and the
committed-plus-pending burden against the contingency (Helios: 30% committed, 105% if every
pending CR were approved).
