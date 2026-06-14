# Estimation Techniques

No single technique fits every situation. Choose by how much you know, how much precision
you need, and how much time you can spend. Estimates get more accurate as the work becomes
better understood — the **cone of uncertainty**.

## The cone of uncertainty
Early in a project, estimates can be off by a factor of several in either direction; as
scope, design, and unknowns are resolved, the cone narrows toward the actuals. The
practical consequence: commit ranges, not single numbers, early on, and re-estimate as you
learn. Track estimate-vs-actual to calibrate.

## Techniques

### Analogous (top-down)
Estimate by comparison to a similar past project or item ("the last portal took ~6 months").
Fast and cheap, needs historical data, lowest accuracy. Use for early, order-of-magnitude
estimates and for sanity-checking bottom-up totals.
- Typical accuracy: rough order of magnitude, often -50% / +100% early.

### Parametric
Use a statistical relationship between a measurable driver and effort/cost
(e.g. cost per screen, hours per use case, $ per square metre). More accurate than
analogous when you have reliable per-unit data and a good quantity count.
- Typical accuracy: good when the parameters are calibrated to your context.

### Three-point / PERT
Capture three estimates per item — optimistic (O), most likely (M), pessimistic (P) —
and combine them: E = (O + 4M + P) / 6, std = (P − O) / 6. This dampens optimism bias and
yields a confidence range, not a point. `scripts/pert_estimate.py` does the math and
aggregates variance across items (variances add; the total std is their root-sum-square).
- Use when uncertainty matters and you want a defensible range.

### Story points (relative sizing)
Size backlog items relative to each other on an abstract scale (often Fibonacci:
1, 2, 3, 5, 8, 13). Decouples size from a person's speed; velocity (points completed per
iteration) then forecasts duration. Good for agile delivery where work is discovered
incrementally.

### Planning poker
A consensus technique for assigning story points (or hours): each estimator privately
picks a card, all reveal at once, and outliers explain their reasoning before re-voting.
Surfaces hidden assumptions and prevents anchoring on the first number spoken.

### Wideband Delphi
A structured, multi-round expert technique: experts estimate independently and anonymously,
a facilitator shares the spread (not the names), the group discusses divergences, and they
re-estimate until they converge. Good for novel work with no historical data and high stakes.

## Choosing a technique
- Very early / no detail -> **analogous** (then refine).
- Reliable per-unit data -> **parametric**.
- Uncertainty you must quantify -> **three-point / PERT**.
- Agile backlog -> **story points** assigned via **planning poker**.
- Novel, high-stakes, expert-driven -> **wideband Delphi**.
Combine techniques and reconcile: a bottom-up total checked against an analogous top-down
estimate catches both missing work and optimism.

## Common mistakes
- Quoting a single number as if it were certain (ignoring the cone).
- Padding individual estimates instead of holding one visible contingency reserve.
- Estimating in isolation, so one optimist or pessimist skews the number (use poker/Delphi).
- Never comparing estimates to actuals, so the estimates never get better.
