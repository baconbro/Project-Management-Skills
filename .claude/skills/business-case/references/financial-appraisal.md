# Financial Appraisal, Sensitivity and Switching Values

How to turn an option's cashflows into the figures an approver acts on, and how to show how
wrong they can be before the answer flips. The examples use the sample Helios project (a
fictional customer self-service portal used throughout this catalog): -$500,000 at period 0,
then net benefits of $150k, $180k, $200k, $200k and $200k, at a 10% discount rate.

## Set up the cashflows
- **Period 0 = today.** The up-front outlay sits in period 0 and is not discounted. A sheet that
  starts at period 1 discounts the outlay by one period and flatters nothing — the helper warns.
- **One net figure per period and option** (benefits minus build and run costs), or gross
  `benefit` and `cost` columns as positive magnitudes. Several rows for one period are netted.
- **Calendar years** (2026, 2027, ...) are only accepted with `--start-year 2026`, which rebases
  them and reports payback in years. Without it the helper refuses, because discounting by the
  2026th power silently returns an NPV of about zero.
- **Rate as a fraction or a percent:** `--rate 0.10` or `--rate 10%`. A bare `10` is refused as
  "looks like a percentage" because 1000% would flip any case.
- **Discount rate:** use the organization's hurdle rate or cost of capital, not a number that
  makes the case work. Write its source in the template.
- **Appraisal period:** the useful life of the asset or a policy horizon (3-5 years for
  software), identical for every option.

## The headline figures
| Figure | Formula (r = rate, t = period) | Read it as |
|--------|--------------------------------|------------|
| Discounted value | CF(t) / (1 + r)^t | today's worth of that period's cashflow |
| **NPV** | sum of discounted values | value created after paying for the money; rank options on it |
| **IRR** | the r at which NPV = 0 | the hurdle rate the case can bear; "n/a" when the cashflows never change sign |
| **ROI (undiscounted)** | (sum of benefits - sum of costs) / sum of costs | return per unit spent, ignoring timing |
| **Payback (undiscounted)** | point at which the running cumulative reaches 0 after its last dip below 0 | how long the money is at risk |
| **Discounted payback** | the same on the discounted cumulative | the stricter version approvers increasingly ask for |
| Whole-life cost | sum of costs over the period, undiscounted | the affordability figure |

ROI's denominator is the gross cost column when you give one, otherwise the *net outlay* (the
sum of the negative net periods). Netting run costs into benefit years therefore changes ROI;
do it the same way for every option, and prefer separate benefit/cost columns when options
differ in run cost. Payback is "not reached" when the cumulative ends negative (a case that
breaks even in year 2 and then sinks is not a 2-year payback) and "n/a (no outlay)" when nothing
was spent.

Helios: NPV $196,174 · IRR 23.6% · ROI 86% · payback 2.85 years · discounted payback 3.47 years.

## Sensitivity: how wrong can the inputs be?
A single-point NPV hides how fragile it is. Three tests, all available from the helper:

1. **Rate sweep** — `--sensitivity 0.05:0.25:0.025` recomputes NPV at each rate and reports the
   rate at which NPV turns negative. Helios stays positive up to 23.6% (its IRR) and is -$14,944
   at 25%.
2. **Stress case** — `--stress` (benefits x0.8, costs x1.2) or your own `--benefit-factor 0.7
   --cost-factor 1.3` shows base and stressed figures side by side. Helios survives either stress
   alone (NPV +$56,939 with benefits -20%; +$96,174 with costs +20%) but not both together
   (-$43,061), so the recommendation carries a condition tied to the leading benefit measure.
3. **Switching values** — `--break-even` solves for the benefit shortfall and the cost overrun at
   which NPV = 0, and names the rate switching value (the IRR). Helios: benefits can fall 28.2%
   or costs rise 39.2% before NPV reaches 0. A switching value inside the range of past
   estimating error is a red flag; one well outside it is the strongest sentence in the case.

Also test a **benefit delay** by hand (shift the benefit rows one period later and re-run): most
cases are more sensitive to timing than to size.

## Optimism bias
Appraisers systematically overstate benefits and understate costs and durations. Counter it
explicitly rather than by hoping: apply an uplift to costs and a haircut to benefits based on
reference-class data (your own past projects, or published ranges such as the HM Treasury Green
Book's uplifts by project type), state the adjustment in the template, and reduce it only when
you can show the estimate is better evidenced than usual. The stress factors are the quickest
way to see whether the adjusted case still clears the hurdle.

## Comparing options
Put every option in one sheet with an `option` column (see `assets/cashflows-options-sample.csv`)
and run once: the helper ranks the options by NPV, prints whole-life cost, total benefit, NPV,
IRR, ROI and payback per option, flags an option whose ROI beats the NPV winner (a smaller outlay
with a higher return is not the better investment), and shows which options turn negative under
stress. `--format md` emits the rows for the template; `--detail` adds each option's per-period
table.

```bash
python .claude/skills/business-case/scripts/roi_npv.py .claude/skills/business-case/assets/cashflows-options-sample.csv --all --stress --sensitivity 0.05:0.25:0.05
```

## Common mistakes
- Treating ROI or payback as discounted figures, or ranking on them instead of NPV.
- A rate chosen to make the case work; calendar years used as exponents; a rate typed as 10.
- Reporting the first break-even as the payback when the cumulative later ends negative.
- Sensitivity as a paragraph ("we are confident") instead of switching values and a stressed NPV.
- An optimism-bias adjustment of zero because "our estimates are good".
