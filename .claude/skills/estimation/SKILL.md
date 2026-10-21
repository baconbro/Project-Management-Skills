---
name: estimation
description: >-
  Estimates effort, duration, or cost using analogous, parametric, three-point
  (PERT), story-point, planning-poker, and wideband-Delphi techniques, and turns
  three-point inputs into expected values, variance shares, P50/P80/P90 commit
  levels, a contingency reserve, and a PERT-Beta simulation of the total with the
  bundled pert_estimate.py helper. Use when the user wants to estimate or size
  work, produce effort/duration/cost figures with a confidence range, build a
  PERT or three-point estimate, run planning poker, or size a reserve from a
  confidence level. Triggers: "estimate", "estimation", "sizing", "three-point",
  "PERT", "story points", "planning poker", "wideband Delphi", "confidence
  range", "how much effort", "P80", "basis of estimate". For sequencing
  durations into a timeline and critical path, use project-schedule. Works for
  waterfall, agile, and hybrid projects.
metadata:
  version: 1.1.0
  category: artifact
  phase: planning
  related: [project-planning, cost-management, work-breakdown-structure, project-schedule, agile-delivery, resource-management]
license: MIT
---

# Estimation

## Overview
Estimation produces the effort, duration, and cost figures every plan depends on. Because
estimates are uncertain, the goal is not one confident number but a defensible **range**
with a stated unit, technique, and assumptions — the basis of estimate. This skill covers
the main techniques and uses three-point/PERT math to turn optimistic / most-likely /
pessimistic inputs into expected values, the items that drive the uncertainty, one-sided
commit levels (P50/P80/P90), the contingency reserve a commitment needs, and a simulated
distribution of the total. The worked numbers come from the sample Helios project (a
fictional customer self-service portal used throughout this catalog).

## When to use this skill
- The user wants to estimate or size work — effort, duration, or cost — for tasks, work
  packages, or a backlog.
- The user wants a three-point/PERT estimate, a confidence range, or an answer to "what can
  we commit to at P80?".
- The user wants to run planning poker, story-point sizing, or wideband Delphi.
- The user needs to size a contingency reserve from a confidence level instead of a flat
  percentage.
- Do NOT use this to define *what* to estimate — decompose scope with
  `work-breakdown-structure` first.
- Do NOT use this to work out how long the whole project takes — tasks run in parallel, so
  project duration comes from the critical path in `project-schedule`; this skill sizes the
  individual tasks it consumes.
- Do NOT use this to build the budget or track spend — hand the figures to `cost-management`.

## Methodology fit
- **Waterfall:** bottom-up three-point estimates per WBS work package in person-days or
  currency, rolled up with `scripts/pert_estimate.py`, reconciled against a top-down
  analogous figure, then baselined with one reserve sized at the committed confidence level
  (typically P80).
- **Agile:** relative sizing in story points via planning poker; velocity ranges, not
  percentages, forecast when the backlog lands (see `agile-delivery`); three-point only for
  spikes, fixed-date commitments, and contracted work.
- **Hybrid:** PERT for the contracted, fixed-scope work (in Helios, the identity/SSO
  integration); story points for the evolving self-service UI and knowledge-base backlog;
  one project-level reserve.

## Inputs you need
The items to estimate — ideally the work packages from `work-breakdown-structure` with their
WBS ids — and, per item, either a comparable past item (analogous), a quantity and per-unit
rate (parametric), or optimistic / most-likely / pessimistic values (three-point), plus the
unit (person-days, weeks, or currency — one unit per worksheet), who estimated, and the
assumptions behind the numbers. For an agile backlog: the stories and the team's velocity
history. See `references/techniques.md` to pick a technique.

## Workflow
1. **List the items** as rows of a copy of `assets/estimation-worksheet-template.csv`, one
   per work package from `work-breakdown-structure`, using the WBS id as `id` so coverage
   can be diffed against the WBS. A level-of-effort element such as Helios 1.1 Project
   management is estimated parametrically (a percentage of the delivery effort), not
   three-point. *Done: every work package is on the list and nothing extra.*
2. **Choose a technique per item** with `references/techniques.md` and its estimate-class
   table: analogous for early order-of-magnitude figures, parametric where per-unit data
   exists, three-point/PERT where uncertainty matters, story points/planning poker for an
   agile backlog, wideband Delphi for novel work. *Done: a technique and estimate class are
   named per item.*
3. **Capture the basis of estimate** in the worksheet: unit, technique, O/M/P, assumptions
   and exclusions, and the estimators (planning poker or Delphi reduces anchoring).
   `assets/estimation-worksheet-sample.csv` shows the ten Helios work packages filled in,
   in person-days, with the SSO integration estimated by Delphi because of the vendor risk.
   *Done: every row has unit, technique, O ≤ M ≤ P, assumptions, and estimators.*
4. **Compute expected values, ranges, and drivers:**
   ```bash
   python .claude/skills/estimation/scripts/pert_estimate.py .claude/skills/estimation/assets/estimation-worksheet-sample.csv
   ```
   Per item it prints E = (O + 4M + P)/6, std = (P − O)/6, the item's share of the total
   variance (`Var%`), and a `wide` flag where P − O exceeds 2M. For the total it prints sum E,
   the ~68/90/95% two-sided ranges (a clamped lower bound is marked — the sign of a skewed
   total), the one-sided P50/P80/P90 levels, and the top uncertainty drivers. Helios: sum E
   451.83 person-days, std 19.96; the SSO integration alone carries 39% of the variance — the
   place for another Delphi round or a spike. **Sum E is total effort (or the duration of one
   strictly sequential chain), never the project duration.** *Done: a range and the drivers,
   not just a point.*
5. **Decide the commit level and size the reserve** with `--confidence` (0.8, 80 or P80;
   repeatable) and, for a skewed or high-stakes total, `--simulate N --seed K`, which draws
   every item from its PERT-Beta distribution and reports P10/P50/P80/P90/P95 of the total:
   ```bash
   python .claude/skills/estimation/scripts/pert_estimate.py .claude/skills/estimation/assets/estimation-worksheet-sample.csv --confidence P80 --simulate 20000 --seed 42
   ```
   Reserve = commit level − sum E. Helios at P80 is 468.63 person-days, a reserve of 16.80
   (3.7%). Hold that reserve once and visibly rather than padding each item. Items are
   assumed independent, so correlated risks (one vendor behind several items) widen the real
   range — note them in `assumptions`. *Done: commit level, reserve, and the confidence
   behind them are written down.*
6. **Reconcile** the bottom-up total against a top-down analogous or parametric figure (a
   comparable past build, or the estimate class in `references/techniques.md`) and
   investigate gaps above roughly 15%: missing work, optimism, or a different scope. *Done:
   the gap is explained or the estimate revised.*
7. **Hand off and calibrate.** Durations go to `project-schedule`: keep a duration worksheet
   per task (`assets/duration-worksheet-sample.csv`, in weeks) and total only one chain with
   `--ids`, e.g. the Helios critical path:
   ```bash
   python .claude/skills/estimation/scripts/pert_estimate.py .claude/skills/estimation/assets/duration-worksheet-sample.csv --ids A,B,D,F,G,H,J
   ```
   That gives 19.17 weeks expected along the critical path (18 weeks on most-likely
   durations, the baseline in `project-schedule`) versus 28.92 weeks if the expected
   durations of all ten tasks were simply summed. Costs and the reserve go to `cost-management`, effort to `resource-management`,
   story points to `agile-delivery`; `--format csv|json|md` exports the per-item E for those
   hand-offs. Record `actual` in the worksheet when work completes and compare. *Done:
   figures handed off and actuals tracked.*

## Quality checklist
- [ ] Every WBS work package has exactly one row keyed by its WBS id; nothing extra.
- [ ] One unit per worksheet; technique, assumptions, and estimators recorded per row.
- [ ] Uncertain work carries a range (O ≤ M ≤ P), not a single number; `wide` items revisited.
- [ ] Estimates were made by more than one person where it matters (poker / Delphi).
- [ ] The commit level is explicit (e.g. P80) and the reserve equals that level minus sum E,
      held once and visibly.
- [ ] Sum E is reported as total effort; project duration was taken from `project-schedule`.
- [ ] The bottom-up total was reconciled against a top-down figure and the gap explained.
- [ ] A plan exists to record actuals and recalibrate.

## Anti-patterns
- Quoting a single number as if certain, ignoring the cone of uncertainty.
- Adding up task durations and calling it the project duration when tasks run in parallel.
- Padding every line item instead of one transparent, confidence-based reserve.
- Estimating in isolation, letting one optimist or pessimist skew the figure.
- Treating story points as hours, or attaching a percentage accuracy to them.
- Never comparing estimates to actuals, so the estimates never improve.

## Resources
- `references/techniques.md` — when to use each technique, estimate classes with accuracy
  ranges, the cone of uncertainty, effort vs duration, and sizing a reserve from a
  confidence level.
- `assets/estimation-worksheet-template.csv` — fill-in worksheet (`<placeholders>`): id,
  task, unit, technique, O/M/P, assumptions, estimators, actual.
- `assets/estimation-worksheet-sample.csv` — sample worksheet for the Helios project: the
  ten WBS work packages in person-days; the default script input.
- `assets/duration-worksheet-sample.csv` — sample duration worksheet for the Helios
  schedule network (ids A–J, weeks) for `--ids` chains.
- `scripts/pert_estimate.py` — per-item E, std, and variance share; totals, two-sided
  ranges, P50/P80/P90; `--confidence P` reserve; `--simulate N --seed K` PERT-Beta
  simulation; `--ids` chain filter; `--unit`; `--json`; `--format table|json|csv|md`. Run
  `python .claude/skills/estimation/scripts/pert_estimate.py --help`.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-planning` — the planning phase that commissions these estimates and folds them
  into the performance baseline.
- `cost-management` — turns the cost estimates and the reserve into the cost baseline and
  tracks them with earned value.
- `work-breakdown-structure` — supplies the work packages (WBS ids) the worksheet must cover
  100%.
- `project-schedule` — consumes the per-task duration estimates and derives the project
  duration of parallel work from the critical path.
- `agile-delivery` — consumes story-point sizes and velocity for sprint and release
  forecasting.
- `resource-management` — turns the effort estimates into staffing demand and checks it
  against capacity.
