---
name: estimation
description: >-
  Estimates effort, duration, or cost using analogous, parametric, three-point
  (PERT), story-point, planning-poker, and wideband-Delphi techniques, and turns
  three-point inputs into expected values, standard deviations, and confidence
  ranges with the bundled pert_estimate.py helper. Use when the user wants to
  estimate or size work, produce effort/duration/cost figures, build a PERT or
  three-point estimate, run planning poker, or attach a confidence range to a
  number. Triggers: "estimate", "estimation", "sizing", "three-point", "PERT",
  "story points", "planning poker", "wideband Delphi", "confidence range",
  "how long", "how much effort". Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: artifact
  phase: planning
  related: [project-planning, work-breakdown-structure, project-schedule, cost-management]
license: MIT
---

# Estimation

## Overview
Estimation produces the effort, duration, and cost figures every plan depends on. Because
estimates are uncertain, the goal is not a single confident number but a defensible
**range** with a stated technique and assumptions. This skill covers the main techniques
and uses three-point/PERT math to convert optimistic / most-likely / pessimistic inputs
into expected values and confidence ranges.

## When to use this skill
- The user wants to estimate or size work (effort, duration, or cost).
- The user wants a three-point/PERT estimate or a confidence range.
- The user wants to run planning poker, story-point sizing, or wideband Delphi.
- Do NOT use this to define *what* to estimate — decompose scope with `work-breakdown-structure` first.
- Do NOT use this to sequence the estimated tasks into a timeline — use `project-schedule`.

## Methodology fit
- **Waterfall:** estimate work packages bottom-up (often three-point/PERT), roll up, baseline.
- **Agile:** relative sizing in story points via planning poker; velocity forecasts duration.
- **Hybrid:** PERT for fixed-scope, contracted work; story points for the evolving backlog.

## Inputs you need
The items to estimate — ideally the work packages from `work-breakdown-structure` — and,
per item, either a comparable past item (analogous), a quantity and per-unit rate
(parametric), or optimistic/most-likely/pessimistic values (three-point). See
`references/techniques.md` to pick a technique.

## Workflow
1. Take the items to estimate from `work-breakdown-structure` so the estimate covers 100%
   of the scope and nothing extra. *Done: every work package is on the list.*
2. **Choose a technique** per item using `references/techniques.md`: analogous for rough
   early numbers, parametric where per-unit data exists, three-point/PERT where uncertainty
   matters, story points/planning poker for an agile backlog, Delphi for novel work.
3. For three-point items, record optimistic (O), most-likely (M), pessimistic (P) for each
   in `assets/estimation-worksheet.csv`. Gather O/M/P from the team (planning poker reduces
   anchoring). *Done: O, M, P captured per item.*
4. Compute expected values and ranges:
   ```bash
   python scripts/pert_estimate.py assets/estimation-worksheet.csv
   ```
   The tool prints per-item E and std (E=(O+4M+P)/6, std=(P−O)/6) and the totals — sum E,
   total std, and ~68% / 90% / 95% confidence ranges. *Done: a range, not just a point.*
5. **Reconcile** bottom-up totals against an analogous top-down estimate; investigate big
   gaps. Hold one visible **contingency reserve** rather than padding each item.
6. Pass durations to `project-schedule` and costs to `cost-management`, and record
   estimate-vs-actual later to calibrate.

## Quality checklist
- [ ] Estimates cover 100% of the WBS scope and nothing extra.
- [ ] The technique is chosen deliberately per item and noted with its assumptions.
- [ ] Uncertain work is given a range (three-point/PERT), not a single number.
- [ ] Estimates are made by more than one person where it matters (poker / Delphi).
- [ ] Contingency is held once and visibly, not hidden inside each estimate.
- [ ] A plan exists to compare estimates to actuals and recalibrate.

## Anti-patterns
- Quoting a single number as if certain, ignoring the cone of uncertainty.
- Padding every line item instead of one transparent reserve.
- Estimating in isolation, letting one optimist or pessimist skew the figure.
- Never comparing estimates to actuals, so the estimates never improve.

## Resources
- `references/techniques.md` — when to use each technique, accuracy ranges, and the cone of uncertainty.
- `assets/estimation-worksheet.csv` — fill-in three-point worksheet; also the sample input for the script.
- `scripts/pert_estimate.py` — computes PERT E, std, and confidence ranges. Run
  `python scripts/pert_estimate.py --help`.

## Related skills
- `project-planning` — the broader planning phase these estimates support.
- `work-breakdown-structure` — supplies the work packages that get estimated.
- `project-schedule` — consumes the duration estimates to build the timeline.
- `cost-management` — consumes the cost estimates to build and track the budget.
