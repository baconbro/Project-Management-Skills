# Escalation Paths

Load this in step 6 of the workflow, to fill `assets/escalation-ladder-template.md`. An escalation
path is the agreed route for raising an issue or a decision to someone with the authority or
information to resolve it, *before* it does damage. Defined in advance, escalation is fast and
unremarkable; left undefined, issues either fester at the wrong level or reach the sponsor as a
surprise. Examples use the sample Helios project (a fictional customer self-service portal used
throughout this catalog).

## The four ingredients
1. **Levels** — the ladder of who handles what, each with one named owner and a deputy.
2. **Authority** — what each level may decide alone: its tolerance. Take it from the change
   control tolerances in `change-management` so the two never disagree.
3. **Triggers** — objective conditions that move an item up a level, written on the *forecast*.
4. **Time-boxes** — how long an item may sit at a level before it must move.

This is management by exception: each level works inside its tolerance and raises an exception
as soon as a forecast shows the tolerance will be exceeded, not after it has been.

## The Helios ladder (sample)

| Level | Owner | May decide alone | Escalate up when | Time-box |
|---|---|---|---|---|
| 1 | Team: Ben Adeyemi (tech lead) for technical items; Ava Chen (product owner) for backlog and sprint scope | Technical choices, blockers and story trade-offs inside the sprint goal | Not resolved inside the team; a cross-team or vendor dependency; anything that touches cost, a milestone or an acceptance criterion | 1 working day |
| 2 | Sam Lee (project manager) | Changes up to $5,000 and 2 days, including contingency draws up to $5,000 for fired risk triggers and approved changes; re-sequencing within float | Any level-3 trigger in the table below | 2 working days |
| 3 | Dana Okoro (sponsor, VP Customer Operations) | The $25,000 management reserve, released through change control; milestone moves; scope trade-offs; escalated risks | A re-baseline; a conflict with another project; anything beyond her authority | 2 working days |
| 4 | Steering committee: Dana Okoro (chair), Priya Nair, Finance, Marcus Webb, Hana Sato, Sam Lee | Re-baselining; cross-project and enterprise issues | — | Next bi-weekly meeting, or an extra session within 2 business days when any dimension turns RED |

The ladder routes the *problem*. A fix that changes a baseline also needs a change request,
decided under the same tolerances (`change-management`: the PM up to $5,000 and 2 days, the change
control board above that, the sponsor for HIGH-impact changes and any release of management
reserve). The time-boxes match the Helios risk management plan, and the sponsor's 2 business days
match her engagement commitment in the stakeholder register.

## Triggers: escalate on the forecast

Escalate on defined conditions, not on mood. Good triggers are objective:
- A tolerance is **forecast** to be breached: a milestone's forecast finish slips beyond the
  agreed schedule tolerance, or the forecast cost (EAC) shows an overrun that the remaining
  contingency cannot absorb. Escalate then, while contingency is left — not when the forecast
  has also used up the management reserve.
- A decision is needed that is outside the current level's authority.
- A risk has occurred and its response exceeds the level's means.
- A time-box has expired with no resolution.
- A dependency on another team or a vendor is blocked.

**Helios trigger table**

| Dimension | Team → Sam Lee (level 2) | Sam Lee → Dana Okoro (level 3) | → Steering committee (level 4) |
|---|---|---|---|
| Schedule | A task's forecast slip exceeds its float (SSO integration, task C, has 1 week) | A forecast slip of more than 2 weeks to M4 or M6, the limit in the risk appetite; any change of more than 2 days | No option within the sponsor's authority keeps M4 or M6 |
| Cost | Any unplanned spend | A change above $5,000; more than half of the $40,000 contingency drawn before M4; a forecast overrun the remaining contingency cannot absorb (EAC above the $500,000 BAC, which already contains the contingency); any decision that needs management reserve | A forecast above BAC plus management reserve ($525,000); a re-baseline |
| Scope and quality | A request outside the sprint goal | A Must-have requirement, or the password-reset or order-status journey, at risk at the pilot | A change to the objective (the 50% cut in the two ticket types) |
| Risk and compliance | A risk trigger fires | A new HIGH risk; R001's trigger fires; any security or compliance risk rated MEDIUM or above | An enterprise-level risk or a regulatory breach |
| RAG | A work package turns AMBER | A work package turns RED (the sponsor is told the same day) | Any dimension turns RED: an extra session within 2 business days |

### Why "forecast over baseline plus reserve" is too late
Baseline plus reserve is the whole budget. For Helios that is $525,000: the $500,000 BAC, which
contains the $40,000 contingency, plus the $25,000 management reserve above it. A trigger set
there fires only once the forecast has consumed the contingency *and* the management reserve, so
the sponsor's first warning arrives when her only options are new funding, a cut in scope or
cancellation. As the SSO overrun grew during month 3, Helios's forecast crossed $500,000
(contingency forecast to run out) before it reached $525,000; a baseline-plus-reserve trigger
would have stayed silent through exactly the weeks in which a vendor recovery plan, a
premium-support crash or a small scope trade-off was still cheap. Use the whole-budget line only
as the level-4 trigger for a re-baseline or new funding.

## Time-boxes: stop issues rotting
Each level holds an item only for its time-box; if it is unresolved, it *must* move up.
Time-boxes prevent the two failure modes: hoarding an issue too long, and panic-escalating it
instantly. Count from when the item was logged, not from when someone noticed it was late.

## Parallel routes
- **Vendors.** The contract's own ladder runs alongside the project ladder. Helios with
  IdentityCo: Ben Adeyemi and the integration engineer (2 business days), Sam Lee and the account
  manager (5 business days), Dana Okoro and IdentityCo's executive sponsor (10 business days),
  then Legal under the dispute clause (`procurement-management`). Only the contract owner
  instructs the vendor.
- **Cutover and go-live.** On the day, the command center escalates by the route in the
  `release-and-cutover` runbook. Rollback triggers are pre-authorized: the cutover lead calls a
  rollback without climbing this ladder, and the sponsor is told at once.
- **Security or privacy incidents** start the incident process immediately; the project ladder
  is informed, not asked.

## The escalation note
Escalate the **decision needed**, not just the problem, with options and a recommendation. Use
section 4 of `assets/escalation-ladder-template.md`. Helios example, raised by Sam Lee on
2026-06-26 and updated on 2026-07-10 (month-3 figures, costed crash option) for the 2026-07-14
steering pre-read:

- **Item:** DEC002, from issue I001 (the IdentityCo sandbox outage; risk R001 has occurred).
- **What happened and the impact:** work package 1.3.1 Identity / SSO integration is RED; the
  project is AMBER at CPI 0.93 and SPI 0.92; EAC is about $535,000 against the $500,000 BAC; the
  M4 pilot date is at risk.
- **Decision needed:** approve IdentityCo's dated recovery plan and decide whether to draw
  management reserve for the 1.3.1 overrun. **Decider:** Dana Okoro at the steering committee.
  **Decide by:** 2026-07-14.
- **Options:** (1) approve the recovery plan and release management reserve through change
  control; (2) also crash the SSO work with IdentityCo premium support, a $20,000 change request
  (ACT004) that protects M4; (3) trade scope through change control to stay inside BAC.
- **Recommendation:** approve the recovery plan now and size the reserve draw once SSO works in
  test on 2026-07-17.
- **If no decision by the date:** the M4 pilot slips and the overrun grows unfunded.

## Good escalation hygiene
- Escalate early and small rather than late and large; a forecast breach is reason enough.
- Never skip a level without telling the level you skipped.
- Record the escalation in the issue log's `escalated_to` field and its outcome as a decision
  item (`project-delivery`), and list open escalations in the weekly status report.
- Publish the ladder with the communication plan in `assets/communication-plan.csv` so people
  know the route before they need it, and review it with the plan at each milestone.

## Anti-patterns
- Triggers written as feelings ("when it looks serious") instead of numbers and dates.
- Triggers set on actuals or on the whole budget, so escalation starts after the options are gone.
- A ladder where everything reaches the sponsor: the lower levels are not empowered.
- An escalation with no options and no decide-by date, which hands the analysis to the sponsor.
- A ladder that disagrees with the change-control tolerances, so the PM may approve a change
  but may not decide the issue behind it.
