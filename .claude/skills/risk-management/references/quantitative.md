# Quantitative Risk Analysis

Qualitative analysis (in `risk-register`) ranks risks; quantitative analysis puts numbers on
the ones that justify the effort and on the project as a whole. Use it to size reserves and
to choose between options, not on every risk.

## Expected Monetary Value (EMV)
The probability-weighted value of an uncertain outcome.

```
EMV = probability x impact
```

By convention threats are negative and opportunities positive. Helios:
- Vendor slip: 40% x -$120,000 = **-$48,000**
- Early-deflection upside: 30% x +$60,000 = **+$18,000**

Summing EMV across independent risks estimates the contingency you should hold. (`risk-register`
computes per-risk and portfolio EMV via `risk_score.py`.)

## Decision Trees
When a decision branches into uncertain outcomes, draw a tree and fold back EMV to compare
paths. Example — build the integration in-house vs buy the vendor widget:

```
                       ┌ success (70%): -$50k   → EMV branch = .7(-50) + .3(-140) = -$77k
        ┌ Build ───────┤
Decision┤              └ rework  (30%): -$140k
        └ Buy widget ── certain: -$90k                         → -$90k
```

Choose **Build** here: -$77k expected beats -$90k certain, even though Build has a worse
worst case. Decision trees make the risk appetite explicit.

## Sensitivity Analysis and the Tornado Diagram
Vary one input at a time across its plausible range to see which inputs move the outcome most.
Plotting each input's swing as a horizontal bar, sorted longest-on-top, gives a **tornado
diagram**. The widest bars are where to focus management attention and where to buy more
certainty (e.g., the integration estimate dominates Helios's cost variance, so de-risk it first).

## Monte Carlo (concept)
Instead of single-point estimates, assign a probability distribution to each uncertain input
(cost, duration) and simulate thousands of runs. The output is a distribution of total
cost/finish-date and a confidence curve, so you can state, e.g., "**80% confident** of finishing
by 30 Nov" rather than a false single date. You do not need the tool to apply the idea: estimate
optimistic / most-likely / pessimistic and reason in ranges and confidence levels.

## Contingency vs Management Reserve
- **Contingency reserve** — for *identified* risks ("known-unknowns"). Size it from summed EMV
  or simulation; it is part of the cost baseline and the PM controls it.
- **Management reserve** — for *unidentified* risks ("unknown-unknowns"). A percentage held
  above the baseline, released by the sponsor, not the PM.

See `cost-management` for how reserves sit inside the cost baseline, and feed the reserve
figure back so the budget reflects analyzed risk rather than padding.
