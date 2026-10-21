# Options Analysis

A credible business case compares **at least three** options so the recommendation is a
choice, not a foregone conclusion. Do-nothing, do-minimum and the recommended option are three
*different* options — never merge the first two to make the count. The examples use the sample
Helios project (a fictional customer self-service portal used throughout this catalog).

## The mandatory options
- **Do nothing (the baseline).** The status quo: what happens if the organization invests
  nothing? Every other option is appraised as an increment over this one. It is rarely free —
  costs and risks usually grow over time, and that growth belongs in the baseline description.
- **Do the minimum.** The smallest credible change that keeps the lights on (e.g. patch the
  legacy system, add an FAQ page). Cheap up front, often expensive or ineffective later. It is
  a separate option with its own cashflows, not another name for the baseline.
- **The recommended option.** The investment the case argues for.
- **One or more alternatives.** A bigger or different approach (build vs. buy, phased vs.
  big-bang, outsource) so the recommendation is shown to be the best, not the only, choice.

## How to evaluate each option
Score every option on a consistent set of criteria, for example:

| Criterion        | What it captures                                                         |
|------------------|--------------------------------------------------------------------------|
| Strategic fit    | Alignment with organizational goals and the problem                      |
| Benefits         | Size and confidence of the expected benefits (`benefits.md`)             |
| Cost             | Whole-life cost (build + run), not just the project price                |
| Financials       | NPV, IRR, ROI, payback (`scripts/roi_npv.py`; see `financial-appraisal.md`) |
| Risk             | Delivery risk and the risk of the option failing to deliver the benefit  |
| Feasibility      | Capacity, skills, dependencies, time-to-value                            |

Keep the units, the appraisal period and the **cashflow basis** identical across options or
the comparison is meaningless. State the basis once, in the options table: either every
option's cashflows are *incremental to do-nothing* (so do-nothing has NPV 0 by definition and
its rising cost appears as avoided cost inside the other options' benefits), or every option is
appraised on *absolute* cashflows, in which case do-nothing's rising cost must be included and
the same treatment applied to every option. Appraising do-nothing on absolute cost while the
recommendation is on incremental net benefit is the "different units across options" error.

Rank on **NPV** at the organization's discount rate. ROI and payback are useful tie-breakers and
affordability checks, but a small option with a high ROI is not automatically the best use of
the money.

## Worked example (Helios)
Cashflows incremental to do-nothing, five-year appraisal, 10% discount rate (the data is in
`assets/cashflows-options-sample.csv`; run it with `--all` to reproduce the figures):

| Option                | Description                                                    | Whole-life cost | NPV @ 10%  | IRR    | ROI (undisc.) | Payback (undisc.) |
|-----------------------|----------------------------------------------------------------|-----------------|------------|--------|---------------|-------------------|
| Do nothing (baseline) | Ticket volumes keep rising; cost-to-serve grows ~8%/year       | 0               | 0          | n/a    | n/a           | n/a               |
| Do minimum            | FAQ page and macros on the existing site; small deflection     | $40,000         | $35,816    | 41.0%  | 150%          | 2.00 years        |
| **Recommended**       | Build the Helios self-service portal (SSO, self-service UI, KB) | $500,000        | $196,174   | 23.6%  | 86%           | 2.85 years        |
| Alternative           | Buy an off-the-shelf SaaS portal — faster, less tailored, higher run cost | $250,000 | $79,709 | 22.4% | 72%           | 2.75 years        |

Do-minimum has the best ROI and the shortest payback, but the recommended option creates two and
a half times the value of the alternative and five times that of do-minimum. The case therefore
recommends the portal, and the sensitivity step shows how far its benefits can fall (28%) or its
costs rise (39%) before that ranking is in doubt.

```bash
python .claude/skills/business-case/scripts/roi_npv.py .claude/skills/business-case/assets/cashflows-options-sample.csv --all --format md
```

Each option's net cashflows feed `scripts/roi_npv.py`, which ranks the options by NPV and prints
one comparison table; the `--format md` rows populate the options and financial-appraisal tables
in `assets/business-case-template.md`.

## Common mistakes
- Omitting "do nothing", or labelling it "do-minimum", so there is no baseline to compare against
  and two options pass for three.
- Loading the alternatives so the recommendation wins by construction.
- Comparing project cost only, ignoring multi-year run costs — or netting run costs into one
  option's benefit years and not another's.
- Using different appraisal periods, benefit units or cashflow bases across options.
- Picking the option with the best ROI or shortest payback rather than the highest NPV.
