---
name: business-case
description: >-
  Builds the investment case for a project: the problem and the cost of inaction, options
  compared against the do-nothing baseline, benefits with baselines, targets, owners and
  dis-benefits, whole-life costs, a financial
  appraisal (NPV, IRR, ROI, payback, sensitivity, switching values, stress cases, per-option
  comparison) with the bundled roi_npv.py helper, then records the funding decision. Use
  when the user wants to justify, appraise, or get approval for an investment, weigh options
  against a baseline, quantify benefits and costs, test a case for optimism bias, or compute
  NPV/IRR/ROI/payback before committing funds. Triggers: "business case",
  "investment case", "cost-benefit analysis", "options analysis", "justify the project",
  "NPV", "IRR", "ROI", "payback period", "switching value", "do-nothing option", "benefits
  register". For authorizing the project once justified, use project-charter; for tracking
  spend after approval, use cost-management. Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.1.0
  category: artifact
  phase: initiation
  related: [project-initiation, project-closure, cost-management, project-charter]
license: MIT
---

# Business Case

## Overview
The business case answers "should we invest in this at all, and in which option?" It states
the problem with evidence, compares credible options against doing nothing, quantifies
benefits (with owners) and whole-life costs, reduces the decision to headline financials an
approver can act on, shows how much those financials can be wrong before the answer flips,
and records the funding decision. It is written before the project is authorized, re-approved
at every stage gate, and is the yardstick `project-closure` measures benefits against. The
worked numbers use the sample Helios project (a fictional customer self-service portal used
throughout this catalog): a $500,000 build that returns net benefits of $150k, $180k, $200k,
$200k and $200k over five years, appraised at a 10% discount rate.

## When to use this skill
- The user wants to justify an investment, compare options, or secure funding approval.
- The user asks for a "business case", "investment case", "cost-benefit analysis" or
  "options analysis", or for NPV, IRR, ROI or payback on a set of cashflows.
- A case exists but must be stress-tested (sensitivity, switching values, optimism bias)
  or re-approved at a stage gate.
- Do NOT use this to formally authorize the project once justified — use `project-charter`.
- Do NOT use this to baseline or track spend during delivery — use `cost-management`.

## Methodology fit
- **Waterfall:** a full case with options table, five-year appraisal and sensitivity, approved
  at the initiation gate and re-confirmed at each stage gate before the next tranche is released.
- **Agile:** a lightweight case that frames the outcome, the funding envelope and the leading
  benefit measures; refined as evidence from each release arrives and re-checked at every
  funding checkpoint (quarterly or per MVP milestone).
- **Hybrid:** the case fixes the funding envelope, the expected return and the switching values;
  the delivery approach stays flexible, and the decision record names the checkpoint at which
  the next tranche is released if the leading measures are on track.

## Inputs you need
- The problem or opportunity with evidence (volumes, cost, time, risk) and what it costs each
  year to leave it alone. Helios: 40% of support tickets are password resets and order-status
  questions, costing about $600,000 a year to handle.
- Candidate options: do-nothing (the baseline), do-minimum, the recommended option and at
  least one alternative.
- Benefits with a baseline, a target, a realisation date and a named benefit owner (Helios:
  cut those two ticket types by 50% within 6 months of launch; owner Priya Nair, Head of
  Support Operations), plus the dis-benefits stakeholders will raise.
- Build (one-off) and run (recurring) costs over the appraisal period, and the organization's
  discount or hurdle rate (Helios: 10%).
- The sponsor who will take the case to the approver (Helios: Dana Okoro, VP Customer
  Operations) and the board or budget holder that releases funds (Finance).

## Workflow
1. **State the problem and the cost of doing nothing.** Numbers, not adjectives: who is
   affected, how often, what it costs, and how that grows. *Done: a reader sees why action is
   needed and what inaction costs per year.*
2. **Build the options analysis** with `references/options-analysis.md`. Keep do-nothing as the
   baseline, add do-minimum as a separate option, the recommended option and at least one
   alternative, and score all of them on the same criteria. Decide the cashflow basis once and
   write it in the options table: every option's cashflows are *incremental to do-nothing* (so
   do-nothing has NPV 0 by definition), or every option is on absolute cashflows including
   do-nothing's rising cost. *Done: at least three real options scored on the same criteria and
   the same basis.*
3. **Identify benefits and dis-benefits** with `references/benefits.md`. Classify each benefit
   (cashable, non-cashable, intangible), record its baseline, target, leading and lagging
   measure, realisation date and owner in a copy of `assets/benefits-register-sample.csv`, and
   list the dis-benefits with an affected group and a mitigation. *Done: every benefit has a
   baseline, a target, a date and an owner; dis-benefits are named, not hidden.*
4. **Capture whole-life costs** — build (one-off) and run (recurring: licences, hosting,
   support, retraining) over the full appraisal period, not just the project price. Net the run
   cost into the benefit years the same way for every option. *Done: costs span the appraisal
   period and the netting rule is the same for every option.*
5. **Record the cashflows and run the appraisal.** Copy `assets/cashflows.csv` (one net
   cashflow per period, period 0 = today's outlay) or, to compare several options in one run,
   `assets/cashflows-options-sample.csv` (an `option` column). From the repo root:
   ```bash
   python .claude/skills/business-case/scripts/roi_npv.py .claude/skills/business-case/assets/cashflows.csv --rate 0.10 --all
   python .claude/skills/business-case/scripts/roi_npv.py .claude/skills/business-case/assets/cashflows-options-sample.csv --all --format md
   ```
   The helper prints the per-period discounted and cumulative values, then NPV, IRR, ROI and
   payback; with several options it ranks them by NPV in one comparison table, and `--format md`
   emits rows you can paste into the template. Read the labels: NPV is discounted at `--rate`;
   ROI and simple payback are **undiscounted** (ROI's denominator is the gross cost column, or
   the net outlay when you give only net cashflows), so `--discounted-payback` is there when the
   approver expects it. Helios: NPV $196,174, IRR 23.6%, ROI 86%, payback 2.85 years, discounted
   payback 3.47 years. Rows written as calendar years need `--start-year 2026`; a rate written
   as `10` is refused — pass `0.10` or `10%`. *Done: headline financials computed per option on
   the same basis.*
6. **Stress the case: sensitivity, switching values and optimism bias.** Run
   ```bash
   python .claude/skills/business-case/scripts/roi_npv.py .claude/skills/business-case/assets/cashflows.csv --sensitivity 0.05:0.25:0.025 --stress --break-even
   ```
   and read `references/financial-appraisal.md`. Report the *switching values* — the benefit
   shortfall, cost overrun and discount rate at which NPV reaches 0 — and the stressed case
   (benefits x0.8, costs x1.2 by default; `--benefit-factor`/`--cost-factor` for your own).
   Apply an explicit optimism-bias uplift to costs and haircut to benefits and say where it came
   from. Helios: benefits can fall 28% or costs rise 39% before NPV turns negative; the combined
   0.8/1.2 stress takes NPV to -$43,061, so the recommendation must carry a condition. *Done: the
   recommendation survives the downside cases, or the exposure is stated and a condition set.*
7. **Fill `assets/business-case-template.md`** — problem, options table, benefits and
   dis-benefits, costs, financial appraisal (paste the `--format md` table), sensitivity and
   switching values, risks and assumptions, and a clear recommendation with the funding ask.
   *Done: no angle-bracket placeholder left.*
8. **Present the case and record the decision.** Take it to the approver or investment board
   with the sponsor; record in section 11 of the template the decision (approve / reject /
   defer), the approver, the conditions, the funding released (full or first tranche) and the
   date, plus the next re-approval point. Hand the approved figures to `project-charter` (budget
   range), `cost-management` (the funding envelope the baseline must fit) and `project-closure`
   (the benefits register to confirm against). *Done: decision recorded, dated and conditioned.*

## Quality checklist
- [ ] Problem stated with evidence and the yearly cost of doing nothing.
- [ ] Do-nothing kept as the baseline; do-minimum, recommended and an alternative compared on
      the same criteria and the same cashflow basis, stated in the table.
- [ ] Every benefit has a type, a baseline, a target, a realisation date, a leading and a
      lagging measure, and a named owner; dis-benefits listed with a mitigation.
- [ ] Costs are whole-life (build + run) over the full appraisal period, netted consistently.
- [ ] NPV computed at a stated discount rate; ROI and simple payback labelled undiscounted
      (discounted payback given where the approver expects it); IRR reported.
- [ ] Sensitivity run; switching values and the optimism-bias adjustment recorded; the case
      tested at a benefit haircut and a cost overrun.
- [ ] A clear recommendation and funding ask, with no unresolved placeholders.
- [ ] Decision recorded with approver, conditions, funding released and date.

## Anti-patterns
- Merging do-nothing and do-minimum into one row so two options pass for three.
- Appraising do-nothing on absolute cost and the recommendation on incremental benefit — the
  numbers are not comparable.
- Loading the alternatives so the recommendation wins by construction.
- Counting only project cost and ignoring multi-year run costs, or netting run costs into one
  option's benefits and not another's.
- Inflating benefits to clear the hurdle (optimism bias), leaving them unowned, or claiming
  them with no baseline so "improvement" can never be proven.
- Ranking options on ROI or payback instead of NPV — a tiny option with a high ROI is not the
  best use of the money.
- A single-point case with no sensitivity, so nobody knows how wrong it can be before the
  answer changes.
- A case that is filed but never decided, or approved with conditions nobody tracks.

## Resources
- `references/options-analysis.md` — the mandatory options (do-nothing baseline, do-minimum,
  recommended, alternative), the scoring criteria and the cashflow basis, with the Helios comparison.
- `references/benefits.md` — benefit types, baseline/target/date/owner, leading and lagging
  measures, dis-benefits, and the Helios benefit table.
- `references/financial-appraisal.md` — discount rate, NPV/IRR/ROI/payback formulas, sensitivity,
  switching values, optimism bias, and how to read the helper's output.
- `assets/business-case-template.md` — fill-in template with options, benefits and dis-benefits,
  financial appraisal, sensitivity and switching values, and the decision record.
- `assets/cashflows.csv` — the Helios sample cashflows (one net cashflow per period); copy it,
  replace the rows, keep the header. Also the script's sample input.
- `assets/cashflows-options-sample.csv` — the four Helios options in one sheet (`option` column)
  for a ranked comparison.
- `assets/benefits-register-sample.csv` — the Helios benefits and dis-benefits with baseline,
  target, measures, value, owner and date; the register `project-closure` confirms against.
- `scripts/roi_npv.py` — NPV, IRR, ROI, simple and discounted payback, `--sensitivity`,
  `--stress`/`--benefit-factor`/`--cost-factor`, `--break-even`, `--start-year`, per-option
  comparison and `--format table|json|csv|md`. Run
  `python .claude/skills/business-case/scripts/roi_npv.py --help` for columns, formulas and exit codes.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-initiation` — the phase that commissions this case and sequences it before the charter.
- `project-closure` — confirms at the end of the project that the benefits promised here were
  realized, using the benefits register.
- `cost-management` — receives the approved funding envelope and whole-life cost as the ceiling
  the cost baseline must fit.
- `project-charter` — formally authorizes the project this case justifies and carries its budget
  range and objective.
