# Estimation Techniques

No single technique fits every situation. Choose by how much you know, how much precision
you need, and how much time you can spend. Estimates get more accurate as the work becomes
better understood — the **cone of uncertainty**. Examples refer to the sample Helios project
(a fictional customer self-service portal used throughout this catalog).

## The cone of uncertainty
Early in a project, estimates can be off by a factor of several in either direction; as
scope, design, and unknowns are resolved, the cone narrows toward the actuals. The
practical consequence: commit ranges, not single numbers, early on, and re-estimate as you
learn. Track estimate-vs-actual to calibrate.

## Estimate classes
Name the class of every estimate so the sponsor knows how much to trust it. Ranges are the
customary expectation for each class (PMBOK-style; AACE uses classes 5 to 1 for the same idea).

| Class | When | Typical range | Techniques |
|---|---|---|---|
| Rough order of magnitude (ROM) | Initiation, business case | −25% / +75% | Analogous |
| Budgetary / preliminary | Early planning, charter budget range | −10% / +25% | Parametric, analogous |
| Definitive | Baselined plan, commitments | −5% / +10% | Bottom-up three-point / PERT |

Helios: the charter's $450k–$550k range is budgetary; the $500,000 BAC set from the
bottom-up worksheet is definitive. Story points carry no percentage accuracy at all — an
agile forecast is a velocity range ("8 to 11 sprints at 25–32 points per sprint"), never a %.

## Effort vs duration
A three-point worksheet sums to **total effort** (person-days, currency), or to the
duration of **one strictly sequential chain**. It is not the project duration whenever
tasks run in parallel: the expected durations of the ten Helios work packages sum to
28.92 weeks, but the critical path is 18 weeks (19.17 expected with PERT skew). Estimate durations per
task, feed them to `project-schedule`, and total only a single path with
`pert_estimate.py --ids`. Variances add only for independent items; where one cause (a
vendor, a key engineer) sits behind several items the real range is wider than the sum.

## Techniques

### Analogous (top-down)
Estimate by comparison to a similar past project or item ("the last portal took ~6 months").
Fast and cheap, needs historical data, lowest accuracy. Use for early, order-of-magnitude
estimates and for sanity-checking bottom-up totals.
- Typical accuracy: ROM, often −25% / +75% (worse with a poor analogue).

### Parametric
Use a statistical relationship between a measurable driver and effort/cost
(e.g. cost per screen, hours per use case, $ per square metre). More accurate than
analogous when you have reliable per-unit data and a good quantity count. Also the right
tool for level-of-effort elements such as Helios 1.1 Project management (a percentage of
the delivery effort).
- Typical accuracy: budgetary, −10% / +25% when the parameters are calibrated to your context.

### Three-point / PERT
Capture three estimates per item — optimistic (O), most likely (M), pessimistic (P) —
and combine them: E = (O + 4M + P) / 6, std = (P − O) / 6. This dampens optimism bias and
yields a confidence range, not a point. `scripts/pert_estimate.py` does the math,
aggregates variance across items (variances add; the total std is their root-sum-square),
shows each item's share of the total variance (the uncertainty drivers), prints one-sided
P50/P80/P90 levels, and with `--simulate` samples each item's PERT-Beta distribution
(alpha = 1 + 4(M−O)/(P−O), beta = 1 + 4(P−M)/(P−O)) to give the real P10–P95 of the total
when it is skewed.
- Typical accuracy: definitive, −5% / +10% at work-package level with a known team.
- Use when uncertainty matters and you want a defensible range.

### Story points (relative sizing)
Size backlog items relative to each other on an abstract scale (often Fibonacci:
1, 2, 3, 5, 8, 13). Decouples size from a person's speed; velocity (points completed per
iteration) then forecasts duration. Good for agile delivery where work is discovered
incrementally; sprint planning and velocity tracking live in `agile-delivery`.

### Planning poker
A consensus technique for assigning story points (or hours): each estimator privately
picks a card, all reveal at once, and outliers explain their reasoning before re-voting.
Surfaces hidden assumptions and prevents anchoring on the first number spoken.

### Wideband Delphi
A structured, multi-round expert technique: experts estimate independently and anonymously,
a facilitator shares the spread (not the names), the group discusses divergences, and they
re-estimate until they converge. Good for novel work with no historical data and high stakes
— in Helios, the identity/SSO integration, which depends on an external vendor.

## Sizing the reserve from a confidence level
Decide the confidence at which you commit (P80 is common for contracted work, P50 for an
internal target), then **reserve = commit level − sum E**:

| Level | Normal approximation | Helios effort worksheet |
|---|---|---|
| P50 | sum E | 451.83 person-days |
| P80 | sum E + 0.842 × std | 468.63 → reserve 16.80 (3.7%) |
| P90 | sum E + 1.282 × std | 477.41 → reserve 25.58 (5.7%) |

`pert_estimate.py --confidence P80` prints the level and the reserve; add `--simulate` to
take them from the simulated distribution instead of the normal approximation. Hold the
reserve once, visibly, at project level, and hand it to `cost-management` as the
contingency reserve inside the baseline. Items whose range is wider than twice their
most-likely value (`wide`) and the top variance drivers are where another Delphi round or a
spike buys the most certainty.

## Choosing a technique
- Very early / no detail -> **analogous** (then refine).
- Reliable per-unit data or level-of-effort work -> **parametric**.
- Uncertainty you must quantify -> **three-point / PERT**.
- Agile backlog -> **story points** assigned via **planning poker**.
- Novel, high-stakes, expert-driven -> **wideband Delphi**.
Combine techniques and reconcile: a bottom-up total checked against an analogous top-down
estimate catches both missing work and optimism.

## Common mistakes
- Quoting a single number as if it were certain (ignoring the cone).
- Summing task durations and presenting the sum as the project duration.
- Padding individual estimates instead of holding one visible contingency reserve.
- Estimating in isolation, so one optimist or pessimist skews the number (use poker/Delphi).
- Never comparing estimates to actuals, so the estimates never get better.
