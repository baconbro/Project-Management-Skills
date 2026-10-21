# Business Case: <Project name>

- **Author:** <name>  |  **Sponsor:** <name, title>  |  **Date:** <date>  |  **Version:** <n>
- **Decision sought:** <approve / reject / defer the investment>  |  **Funding ask:** <amount>

## 1. Executive summary
<Two or three sentences: the problem and what it costs each year, the recommended option, its
whole-life cost, and the headline return (NPV, IRR, payback). A busy approver should be able to
decide from this alone.>

## 2. Problem / opportunity
<What is wrong or possible today, who it affects, how often, what it costs, and the cost of
leaving it unaddressed per year. Evidence: numbers, not adjectives.>

## 3. Strategic alignment
<Which organizational goal or strategy this investment advances, and the measure it moves.>

## 4. Options analysis
See `.claude/skills/business-case/references/options-analysis.md`. Do-nothing is the baseline;
do-minimum, the recommended option and at least one alternative are compared against it on the
same criteria.

**Appraisal period:** <n> years. **Cashflow basis:** <all option cashflows are incremental to
do-nothing (do-nothing NPV = 0 by definition) / all options on absolute cashflows including
do-nothing's rising cost>. **Discount rate:** <rate> (<source: finance hurdle rate / cost of capital>).

| Option                  | Description | Whole-life cost | NPV | ROI (undiscounted) | Payback (undiscounted) | Risk | Feasibility |
|-------------------------|-------------|-----------------|-----|--------------------|------------------------|------|-------------|
| Do nothing (baseline)   | <status quo and how its cost grows> | <> | <0 if incremental> | <n/a> | <n/a> | <> | <> |
| Do minimum              | <smallest credible change> | <> | <> | <> | <> | <> | <> |
| **Recommended**         | <> | <> | <> | <> | <> | <> | <> |
| Alternative             | <> | <> | <> | <> | <> | <> | <> |

**Recommended option:** <which, and why it wins on NPV and the non-financial criteria>.

## 5. Benefits and dis-benefits
See `.claude/skills/business-case/references/benefits.md`. Every benefit has a baseline, a target,
a realisation date and a benefit owner. Keep the full list in a copy of
`.claude/skills/business-case/assets/benefits-register-sample.csv`.

| Benefit | Type (cashable / non-cashable / intangible) | Baseline (today) | Target | Leading measure | Lagging measure | Value p.a. | Realised by | Owner |
|---------|---------------------------------------------|------------------|--------|-----------------|-----------------|------------|-------------|-------|
| <>      | <>                                          | <>               | <>     | <>              | <>              | <>         | <date>      | <name> |

**Expected dis-benefits** (outcomes a stakeholder will see as negative):

| Dis-benefit | Who is affected | Measure | Mitigation | Owner |
|-------------|-----------------|---------|------------|-------|
| <>          | <>              | <>      | <>         | <name> |

## 6. Costs
<Build (one-off) and run (recurring) costs over the appraisal period. Whole-life, not just the
project price; state the optimism-bias uplift applied.>

| Cost item | Type (build / run) | Year 0 | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|-----------|--------------------|--------|--------|--------|--------|--------|--------|
| <>        | <>                 | <>     | <>     | <>     | <>     | <>     | <>     |

## 7. Financial appraisal
Record the net cashflows per period (period 0 = today's outlay) in a copy of
`.claude/skills/business-case/assets/cashflows.csv`, or one `option` per block in a copy of
`.claude/skills/business-case/assets/cashflows-options-sample.csv`, then run from the repo root:

```bash
python .claude/skills/business-case/scripts/roi_npv.py <your-cashflows.csv> --rate <0.10> --all --format md
```

Paste the comparison table it prints here (NPV is discounted; ROI and simple payback are
undiscounted; ROI's denominator is the gross cost column, or the net outlay when only net
cashflows are given):

| Rank | Option | Whole-life cost | Total benefit | NPV @ <rate> | IRR | ROI (undiscounted) | Payback (undiscounted, years) | Discounted payback (years) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| <> | <> | <> | <> | <> | <> | <> | <> | <> |

- **Headline (recommended option):** NPV <> at <rate>  ·  IRR <>  ·  ROI <> (undiscounted)  ·
  payback <> years (undiscounted), <> years discounted.

## 8. Sensitivity and switching values
See `.claude/skills/business-case/references/financial-appraisal.md`. Run the sweep and the stress
cases, then fill in:

```bash
python .claude/skills/business-case/scripts/roi_npv.py <your-cashflows.csv> --rate <0.10> --sensitivity <0.05:0.25:0.025> --stress --break-even
```

| Scenario                              | NPV | Payback (undiscounted) | Still positive? |
|---------------------------------------|-----|------------------------|-----------------|
| Base case                             | <>  | <>                     | <yes/no>        |
| Benefits -20%                         | <>  | <>                     | <>              |
| Costs +20%                            | <>  | <>                     | <>              |
| Benefits -20% and costs +20%          | <>  | <>                     | <>              |
| Discount rate +2 points               | <>  | <>                     | <>              |
| Benefits delayed <6-12> months        | <>  | <>                     | <>              |

- **Switching values:** benefits can fall <x>% · costs can rise <y>% · discount rate up to <IRR>
  before NPV reaches 0.
- **Optimism-bias adjustment:** <uplift applied to costs and haircut to benefits, and its source
  (e.g. reference-class data from past projects, HM Treasury Green Book ranges)>.
- **What this means:** <which downside cases the recommendation survives and which condition in
  section 11 covers the ones it does not>.

## 9. Risks and assumptions
<Top risks to the case and the key assumptions the numbers depend on (adoption rate, run cost,
start date). Full analysis lives in the risk register.>

## 10. Recommendation
<The clear ask, the funding required (full amount or first tranche), the conditions you propose,
and the next step on approval (charter, planning).>

## 11. Decision record
| Decision (approve / reject / defer) | Approver / board | Conditions | Funding released | Date |
|-------------------------------------|------------------|------------|------------------|------|
| <>                                  | <name, board>    | <e.g. re-approve at MVP gate if leading measure >= target> | <amount / tranche> | <date> |

- **Next re-approval point:** <stage gate or date>  |  **Benefits confirmed by:** <owner, date>
  (see `project-closure`).
