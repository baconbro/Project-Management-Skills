# Baseline guide — set it and protect it

Load this to set a performance baseline at the end of planning and keep it meaningful
through delivery. A baseline is the approved version of scope, schedule, and cost that
actual progress is measured against. Examples use the running sample project: **Helios**,
a customer self-service portal.

## What a baseline is (and is not)
- It IS the approved, frozen reference for scope, schedule, and cost.
- It is NOT the latest working estimate. The working plan moves; the baseline does not,
  except through change control.
- Without a baseline you cannot say whether you are ahead or behind, over or under — there
  is nothing to compare actuals to.

## The three baselines
1. **Scope baseline** — the approved WBS and scope statement. See `work-breakdown-structure`.
2. **Schedule baseline** — the approved schedule with the critical path and milestones. See
   `project-schedule`.
3. **Cost baseline** — the approved time-phased budget plus contingency. See
   `cost-management`. Together these support earned-value tracking in delivery.

## How to set the baseline
1. Confirm scope, schedule, and cost are internally consistent (see `planning-checklist.md`).
2. Confirm the schedule supports any fixed dates and the cost fits the charter budget.
3. Get explicit sponsor approval — a baseline is an agreement, not a calculation.
4. Record the approved version and date, and snapshot it so it can be compared later.
5. Communicate that the baseline is now frozen and changes go through change control.

## Protecting the baseline
- Route every proposed change to scope, schedule, or cost through a `change-request` and
  the `change-management` process before the baseline moves.
- Re-baseline only when an approved change is large enough that measuring against the old
  baseline is misleading — and record why.
- In delivery, measure actuals against the baseline (see `cost-management` for CPI/SPI) and
  report variance in the `status-report`.

## Methodology notes
- **Waterfall:** a firm, signed baseline for scope, schedule, and cost.
- **Agile:** the "baseline" is a release roadmap, a sprint cadence, and a definition of
  done; the backlog re-prioritizes within fixed iterations.
- **Hybrid:** baseline outcomes, budget, and key milestones; leave feature detail to
  iterate inside the frame.

## Anti-patterns
- Never setting a baseline, so "are we on track?" has no answer.
- Quietly editing the baseline to match reality, hiding the variance instead of explaining it.
- Re-baselining so often the baseline is meaningless.
