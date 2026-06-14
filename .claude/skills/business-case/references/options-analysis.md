# Options Analysis

A credible business case compares **at least three** options so the recommendation is
a choice, not a foregone conclusion. Always include the baseline.

## The mandatory options
- **Do nothing (baseline / "do-minimum").** What happens if the organization invests
  nothing? This is the reference point every other option is measured against. It is
  rarely free — costs and risks usually grow over time.
- **Do the minimum.** The smallest credible change that keeps the lights on (e.g. patch
  the legacy system). Cheap up front, often expensive later.
- **The recommended option.** The investment the case argues for.
- **One or more alternatives.** A bigger or different approach (build vs. buy, phased vs.
  big-bang) so the recommendation is shown to be the best, not the only, choice.

## How to evaluate each option
Score every option on a consistent set of criteria, for example:

| Criterion        | What it captures                                         |
|------------------|----------------------------------------------------------|
| Strategic fit    | Alignment with organizational goals and the problem      |
| Benefits         | Size and confidence of the expected benefits             |
| Cost             | Whole-life cost (build + run), not just the project price|
| Financials       | NPV, ROI, payback (use `scripts/roi_npv.py`)             |
| Risk             | Delivery risk and risk of the option failing             |
| Feasibility      | Capacity, skills, dependencies, time-to-value            |

Keep the units and the appraisal period identical across options, or the comparison is
meaningless.

## Worked example (Helios)
For the Helios customer self-service portal:
- **Do nothing:** call volumes keep rising; cost-to-serve grows ~8%/year.
- **Do minimum:** add an FAQ page to the existing site — cheap, deflects few calls.
- **Recommended:** build a self-service portal (login, account view, ticketing).
- **Alternative:** buy an off-the-shelf SaaS portal — faster, less tailored, higher run cost.

Each option's net cashflows feed `scripts/roi_npv.py` to produce comparable NPV/ROI/payback,
which then populate the options table in `assets/business-case-template.md`.

## Common mistakes
- Omitting "do nothing", so there is no baseline to compare against.
- Loading the alternatives so the recommendation wins by construction.
- Comparing project cost only, ignoring multi-year run costs.
- Using different appraisal periods or benefit units across options.
