# Business Case: <Project Name>

- **Author:** <name>  |  **Sponsor:** <name>  |  **Date:** <date>  |  **Version:** <n>
- **Decision sought:** <approve / reject / defer the investment>

## 1. Executive summary
<Two or three sentences: the problem, the recommended option, the cost, and the headline
return (NPV / ROI / payback). A busy approver should be able to decide from this alone.>

## 2. Problem / opportunity
<What is wrong or possible today, who it affects, and the cost of leaving it unaddressed.
Use evidence — numbers, not adjectives.>

## 3. Strategic alignment
<Which organizational goal or strategy this investment advances.>

## 4. Options analysis
See `references/options-analysis.md`. Compare at least three options including "do nothing".

| Option            | Description            | Whole-life cost | NPV   | ROI   | Payback | Risk   |
|-------------------|------------------------|-----------------|-------|-------|---------|--------|
| Do nothing        | <baseline>             | <>              | <>    | <>    | <>      | <>     |
| Do minimum        | <>                     | <>              | <>    | <>    | <>      | <>     |
| **Recommended**   | <>                     | <>              | <>    | <>    | <>      | <>     |
| Alternative       | <>                     | <>              | <>    | <>    | <>      | <>     |

**Recommended option:** <which, and why it wins>.

## 5. Benefits
See `references/benefits.md`. Every benefit has a measure and a benefit owner.

| Benefit         | Type (tangible/intangible) | Leading measure | Lagging measure | Owner |
|-----------------|----------------------------|-----------------|-----------------|-------|
| <>              | <>                         | <>              | <>              | <>    |

## 6. Costs
<Build (one-off) and run (recurring) costs over the appraisal period. Whole-life, not
just the project price.>

| Cost item        | Type (build/run) | Year 0 | Year 1 | Year 2 | ... |
|------------------|------------------|--------|--------|--------|-----|
| <>               | <>               | <>     | <>     | <>     |     |

## 7. Financial appraisal
Record net cashflows per period in `assets/cashflows.csv`, then run:

```bash
python scripts/roi_npv.py assets/cashflows.csv --rate 0.10
```

- **NPV:** <>   **ROI:** <>   **Payback:** <>   **Discount rate:** <>

## 8. Risks and assumptions
<Top risks to the case and the key assumptions the numbers depend on. Full analysis lives
in the risk register.>

## 9. Recommendation
<The clear ask, the funding required, and the next step on approval.>
