---
name: business-case
description: >-
  Builds and justifies the investment case for a project: the problem,
  an options analysis (including do-nothing), tangible and intangible benefits,
  whole-life costs, and a financial appraisal (NPV, ROI, payback) using the
  bundled roi_npv.py helper. Use when the user wants to justify, appraise, or
  get approval for an investment, weigh options against a baseline, quantify
  benefits and costs, or compute NPV/ROI/payback before committing funds.
  Triggers: "business case", "investment case", "cost-benefit analysis",
  "options analysis", "justify the project", "NPV", "ROI", "payback period",
  "do-nothing option". Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: artifact
  phase: initiation
  related: [project-charter, project-initiation, cost-management, project-closure]
license: MIT
---

# Business Case

## Overview
The business case is the document that answers "should we invest in this at all?" It
states the problem, compares credible options against doing nothing, quantifies the
benefits and whole-life costs, and reduces the decision to a few headline numbers
(NPV, ROI, payback) an approver can act on. It is written before the project is
authorized and is revisited whenever the investment is questioned.

## When to use this skill
- The user wants to justify an investment or secure funding approval.
- The user asks for a "business case", "cost-benefit analysis", or "options analysis".
- The user needs NPV, ROI, or payback computed for a set of cashflows.
- Do NOT use this to formally authorize the project once justified — use `project-charter`.
- Do NOT use this to track spend during delivery — use `cost-management`.

## Methodology fit
- **Waterfall:** a full business case approved at a stage gate before planning starts.
- **Agile:** a lightweight case framing the investment and expected benefits; refined as
  evidence arrives and re-checked at funding checkpoints.
- **Hybrid:** the case fixes the funding envelope and expected return; the delivery
  approach stays flexible.

## Inputs you need
The problem or opportunity with evidence, the candidate options (including do-nothing),
the expected benefits with measures and owners, the build and run costs over an appraisal
period, and a discount rate. If the costs and benefits are not yet known well enough to
compare options, gather them before appraising.

## Workflow
1. State the **problem / opportunity** with evidence — numbers, not adjectives — and the
   cost of leaving it unaddressed. *Done: a reader sees why action is needed.*
2. Build the **options analysis** using `references/options-analysis.md`. Compare at least
   three options and always include **do-nothing** as the baseline. *Done: each option is
   scored on the same criteria.*
3. Identify **benefits** using `references/benefits.md`: classify each as tangible or
   intangible, give it a leading and a lagging measure, and name a **benefit owner**.
   *Done: every benefit is measurable and owned.*
4. Capture **whole-life costs** — build (one-off) and run (recurring) over the appraisal
   period, not just the project price. *Done: costs span the full appraisal period.*
5. Record net cashflows per period in `assets/cashflows.csv` (period 0 = the up-front
   outlay), then run the appraisal:
   ```bash
   python scripts/roi_npv.py assets/cashflows.csv --rate 0.10
   ```
   The tool prints per-period discounted values and a running cumulative, then NPV, ROI,
   and payback period. Adjust the discount rate with `--rate`. *Done: headline financials
   computed.*
6. Fill `assets/business-case-template.md` with the problem, options table, benefits,
   costs, financials, risks, and a clear **recommendation**. *Done: no placeholder left.*

## Quality checklist
- [ ] Problem stated with evidence, not adjectives.
- [ ] At least three options compared, including do-nothing, on consistent criteria.
- [ ] Every benefit has a type, a leading and a lagging measure, and a named owner.
- [ ] Costs are whole-life (build + run) over the full appraisal period.
- [ ] NPV, ROI, and payback computed at a stated discount rate.
- [ ] A clear recommendation and funding ask, with no unresolved placeholders.

## Anti-patterns
- Omitting the do-nothing baseline, so there is nothing to compare against.
- Loading the alternatives so the recommendation wins by construction.
- Counting only project cost and ignoring multi-year run costs.
- Inflating benefits to clear the hurdle (optimism bias) or leaving them unowned.

## Resources
- `references/options-analysis.md` — the mandatory options and how to score them.
- `references/benefits.md` — benefit types, leading/lagging measures, and benefit owner.
- `assets/business-case-template.md` — fill-in business-case template.
- `assets/cashflows.csv` — fill-in cashflow sheet; also the sample input for the script.
- `scripts/roi_npv.py` — computes NPV, ROI, and payback. Run `python scripts/roi_npv.py --help`.

## Related skills
- `project-charter` — formally authorizes the project this case justifies.
- `project-initiation` — the broader phase this case sits inside.
- `cost-management` — tracks the budget and spend once the investment is approved.
- `project-closure` — confirms the benefits this case promised were realized.
