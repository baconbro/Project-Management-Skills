# Baseline guide — set it once, protect it, change it deliberately

Load this to set the performance baseline at the end of planning and keep it meaningful through
delivery. A baseline is the approved version of scope, schedule and cost that actual progress is
measured against. Examples use the sample Helios project (a fictional customer self-service
portal used throughout this catalog).

## What a baseline is (and is not)
- It IS the approved, frozen reference for scope, schedule and cost, with a version and a date.
- It is NOT the latest working forecast. The forecast moves every week; the baseline moves only
  through change control.
- Without a baseline you cannot say whether you are ahead or behind, over or under: there is
  nothing to compare actuals with.

## The three baselines and the reserves
| Baseline | Contents | Produced by |
|---|---|---|
| Scope | Scope statement, WBS and WBS dictionary | `scope-and-requirements` (scope statement and requirements traceability matrix); `work-breakdown-structure` (WBS and WBS dictionary) |
| Schedule | The resource-leveled schedule: dates, critical path, milestones | `project-schedule`, `resource-management` |
| Cost | Time-phased work-package costs + contingency reserve = BAC | `cost-management` |

Together these form the **performance measurement baseline** that earned value is computed
against. Where the reserves sit:
- **Contingency reserve** (identified risks, sized in `risk-management`) is **inside** the cost
  baseline and inside BAC; the project manager draws it down.
- **Management reserve** (unidentified risks, set by policy) sits **above** the baseline: part of
  the total budget, not of BAC, never planned as PV or earned as EV. The sponsor releases it,
  only through change control: a release for unplanned in-scope work raises BAC; a release
  that funds an overrun on baselined work raises the funded budget but not BAC, so the cost
  variance and CPI stay measured against the original BAC.
- **Schedule reserve** is held once, visibly, before the milestone it protects — not spread
  into task durations.

Helios: $460,000 work packages + $40,000 contingency = BAC $500,000; the $25,000 management
reserve brings the total budget to $525,000. Helios holds no schedule reserve: the 25-week
schedule ends on 2026-09-25, leaving only the cutover week before general availability on
2026-10-03. Dana Okoro accepted that gap at baseline (a 27% chance of GA readiness by week 26;
the 2-week M6 tolerance covers about P75) with a crash of H, Hardening & launch, ready. An
accepted gap is recorded in the baseline decision like any reserve.

## Baselines by approach
- **Waterfall:** firm scope, schedule and cost baselines for the whole project, approved together.
- **Agile:** the baseline is a **prioritised product backlog** (the scope, ordered by value), a
  **release plan** (fixed sprint length and team cost per sprint, and a velocity-based forecast
  of the scope that fits the release date) and a **definition of done** (the quality bar an
  increment must meet to count as progress). Progress is measured as a burn-up against the
  release plan; the backlog re-orders within the fixed sprints and budget without a change
  request. Build it with `agile-delivery`; the definition of done comes from
  `quality-management` and is the standard for counting done work, not the yardstick of
  progress itself.
- **Hybrid:** full baselines for the outcomes, budget, milestones and fixed elements; a
  release-level backlog for the flexible scope inside that frame (Helios: the SSO integration
  and launch work are baselined in full; the UI and knowledge-base Should and Could stories flex).

## How to set the baseline — one approval
1. Reconcile the components with `planning-checklist.md`: scope, schedule, cost and resources
   agree, and every constraint in the assumptions log is honoured.
2. Confirm the schedule meets the fixed dates and BAC + management reserve fits the charter
   budget range; escalate any gap before asking for approval.
3. Get the sponsor's explicit approval of scope, schedule and cost **together**, in one dated
   decision. A baseline is an agreement, not a calculation; component baselines approved one
   by one drift apart. (Helios: Dana Okoro approved v1.0 at M1.)
4. Snapshot the approved version — the plan, the WBS, the schedule export, the time-phased
   budget, the register — so later reports can compare against it.
5. Announce that the baseline is frozen and that changes now go through change control.

## Protecting the baseline
- Route every proposed change to scope, schedule or cost through a `change-request` and the
  `change-management` tolerances before the baseline moves. Helios: the PM approves up to
  $5,000 and 2 days within contingency, the change control board decides above that, the
  sponsor decides HIGH-impact changes.
- In delivery, measure actuals against the baseline (CPI and SPI in `cost-management`) and
  report variance in the `status-report`.

## Approved change, rolling-wave refinement, or re-baseline?
| Situation | What changes | Is it a re-baseline? |
|---|---|---|
| An approved change request | The affected baseline component gets a new version; variance history is kept | No |
| Contingency drawn down for a risk that occurred | Moves budget between work packages inside BAC | No |
| Management reserve released for unplanned in-scope work | BAC rises by the released amount, through change control | No, but it is a baseline change |
| Management reserve released to fund an overrun | Funding rises; BAC and the variance history stay | No |
| Rolling-wave: a planning package is detailed into work packages | Detail added inside the same control-account budget and dates | No |
| The remaining plan is so different that variances against it mean nothing (a major scope or funding change, an approved recovery plan) | The whole remaining baseline is replaced | **Yes** |

Re-baseline only in the last case, and only with the sponsor's approval: record why, keep the
old snapshot, and report against both for one period so the history stays visible. Helios:
CR003 (accessibility uplift to WCAG 2.2 AA) was approved by the change control board and the
scope statement re-issued as v1.1 — an approved change, not a re-baseline.

## Anti-patterns
- Never setting a baseline, so "are we on track?" has no answer.
- Approving the scope, schedule and cost baselines at different times so they contradict each other.
- Counting the management reserve inside BAC.
- Calling the definition of done the agile baseline, so nobody can say whether the release is
  ahead or behind.
- Quietly editing the baseline to match reality, hiding the variance instead of explaining it.
- Re-baselining so often the baseline means nothing.
