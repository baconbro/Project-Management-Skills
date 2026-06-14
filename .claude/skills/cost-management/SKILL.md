---
name: cost-management
description: >-
  Estimates, baselines, and controls project cost, and tracks performance with
  earned-value management and forecasting using the bundled health_check.py
  helper. Use when the user wants to build a cost baseline, aggregate or
  time-phase costs into an S-curve, set contingency or management reserve, track
  budget vs actuals, compute CV/SV/CPI/SPI, forecast EAC/ETC/VAC, or give a
  cost a RAG status. Triggers: "cost management", "cost baseline", "budget",
  "earned value", "EVM", "CPI", "SPI", "EAC", "cost variance", "burn rate",
  "forecast at completion", "BAC". Pulls estimates from estimation and reports
  through status-report. Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: discipline
  phase: cross-cutting
  related: [project-planning, estimation, business-case, status-report, project-delivery]
license: MIT
---

# Cost Management

## Overview
Cost management is the discipline of working out what the project will cost, agreeing that
number as a baseline, and then measuring whether you are getting the value you are paying for.
Earned-value management answers the question a raw budget-vs-actuals burn chart cannot: *are
we ahead or behind, and over or under, for the work actually done?*

## When to use this skill
- The user wants to build, aggregate, or time-phase a cost baseline or S-curve.
- The user wants to track budget vs actuals, compute EVM metrics, or forecast at completion.
- The user needs to size or distinguish contingency vs management reserve.
- Do NOT use this to produce the underlying activity estimates — use `estimation`, whose
  outputs are the inputs here.
- Do NOT use this to write the periodic status narrative — feed these numbers into
  `status-report`.

## Methodology fit
- **Waterfall:** a formal cost baseline and full EVM reported at stage gates.
- **Agile:** cost tracked as run-rate / cost-per-sprint against a budget; EVM applied with
  story points or scope% as the value measure when funders require it.
- **Hybrid:** baseline the committed scope; track discretionary scope on a rolling budget.

## Inputs you need
Activity or work-package estimates (from `estimation`), the schedule (for time-phasing), rate
cards, and a risk-based contingency figure (from `risk-management`). To track performance you
also need, per work item, **planned value (PV)**, **earned value (EV)**, and **actual cost (AC)**.

## Workflow
1. **Aggregate costs.** Roll work-package estimates up the WBS to a total, add contingency
   reserve, and time-phase the result to draw the **S-curve** (cumulative PV). See
   `references/cost-baselining.md`. *Done: a time-phased cost baseline and total budget (BAC).*
2. **Set reserves.** Separate **contingency reserve** (in the baseline, for known risks) from
   **management reserve** (above the baseline, for unknowns). *Done: both reserves named and
   sized, not blended into padding.*
3. **Baseline and commit.** Get the cost baseline approved; it becomes the line you measure
   against. *Done: baseline approved and frozen (changes only via change control).*
4. **Measure performance.** Each period, record PV, EV, and AC per work item and compute the
   variances and indices. Run the helper:
   ```bash
   python scripts/health_check.py assets/cost-baseline.csv
   ```
   It prints per-row and TOTAL CV, SV, CPI, SPI, then EAC/ETC/VAC and a RAG verdict. See
   `references/earned-value.md` for every formula and a worked example. *Done: current CPI/SPI
   and a forecast at completion.*
5. **Forecast.** Use CPI to project **EAC** (estimate at completion) and **ETC** / **VAC**;
   compare against the budget and reserves. *Done: a defensible forecast, not a hope.*
6. **Control.** Investigate variances, act on the worst, and feed the RAG status and forecast
   into `status-report` and `project-delivery`. *Done: variances explained and acted on.*

## Quality checklist
- [ ] Costs are aggregated up the WBS and time-phased into an S-curve / BAC.
- [ ] Contingency and management reserves are distinct and justified.
- [ ] The cost baseline is approved and changed only through change control.
- [ ] PV, EV, and AC are captured per period; CV/SV/CPI/SPI are computed.
- [ ] A forecast (EAC/ETC/VAC) exists and is compared against budget and reserves.
- [ ] A RAG status is derived and reported via `status-report`.

## Anti-patterns
- Tracking actuals vs budget only (burn rate) with no earned value — you cannot tell late from over.
- Folding contingency into estimates so the real estimate and the buffer are indistinguishable.
- Treating EAC as the original budget no matter how bad CPI gets — denial, not forecasting.
- Mixing value units (dollars for PV/AC, % for EV) so the indices are meaningless.
- Reporting a single colour with no variance analysis behind it.

## Resources
- `references/cost-baselining.md` — cost aggregation, reserves, and the S-curve.
- `references/earned-value.md` — PV/EV/AC, CV/SV/CPI/SPI, EAC/ETC/VAC/TCPI with a worked example.
- `assets/cost-baseline.csv` — sample EVM input; also the sample the script runs on.
- `scripts/health_check.py` — computes EVM metrics, forecasts, and a RAG verdict. Run `python scripts/health_check.py --help`.

## Related skills
- `estimation` — produces the activity estimates that feed the cost baseline.
- `project-planning` — where the baseline is integrated with scope and schedule.
- `business-case` — sets the budget envelope and ROI this baseline must respect.
- `status-report` — the vehicle that reports cost performance and RAG status.
- `project-delivery` — where cost is controlled and variances are acted on.
