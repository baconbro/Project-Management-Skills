---
name: cost-management
description: >-
  Builds and controls the project cost baseline: aggregates the work-package
  estimates from estimation up the WBS, sizes contingency and management reserve,
  time-phases the budget into an S-curve and BAC, fixes the earned-value earning
  rules, then tracks performance with earned-value management (CV/SV, CPI/SPI,
  EAC/ETC/VAC, TCPI, percent complete) and a RAG verdict using the bundled
  health_check.py helper. Use when the user wants to set a cost baseline,
  time-phase a budget, size reserves, track budget vs actuals, compute earned
  value, forecast the cost at completion, or rate cost health. Triggers: "cost
  management", "cost baseline", "budget", "earned value", "EVM", "CPI", "SPI",
  "EAC", "cost variance", "burn rate", "forecast at completion", "BAC", "TCPI",
  "management reserve", "over budget". For producing the underlying effort and
  cost estimates, use estimation; for the periodic narrative, use status-report.
  Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.1.0
  category: discipline
  phase: cross-cutting
  related: [project-planning, project-delivery, risk-management, estimation, business-case, status-report, procurement-management]
license: MIT
---

# Cost Management

## Overview
Cost management turns the work-package estimates into an approved, time-phased cost baseline,
keeps the reserves visible, and then measures whether the project is getting the value it pays
for. Earned-value management (EVM) answers what a burn chart cannot: for the work actually
done, are we over or under, ahead or behind — and what will the whole project cost? The worked
numbers use the sample Helios project (a fictional customer self-service portal used throughout
this catalog): BAC $500,000, and at the end of month 3 CPI 0.93, SPI 0.92, AMBER, with a forecast
at completion of about $535,000.

## When to use this skill
- The user wants to build, aggregate, or time-phase a cost baseline or S-curve, or set BAC.
- The user needs to size or separate contingency reserve from management reserve.
- The user wants to track budget vs actuals, compute CV/SV/CPI/SPI, forecast EAC/ETC/VAC, or
  check whether the remaining budget is achievable (TCPI).
- The user needs a cost RAG status or a CPI/SPI trend for a steering update.
- Do NOT use this to produce the underlying effort or cost estimates — use `estimation`; its
  per-work-package figures are the input here.
- Do NOT use this to size the contingency from the risks — use `risk-management` (EMV or a
  simulation of the register) and bring the figure here.
- Do NOT use this to write the periodic status narrative — feed CPI/SPI/EAC into
  `status-report`.
- Do NOT use this to justify the investment — `business-case` sets the envelope the baseline
  must fit.

## Methodology fit
- **Waterfall:** a full time-phased baseline with both reserves, EVM every reporting period and
  at each stage gate, re-baselined only through change control.
- **Agile:** the budget is a run-rate (cost per sprint x planned sprints) against a fixed
  envelope, and the backlog flexes to fit it. Where funders require EVM, keep EV in currency:
  EV = (story points accepted / planned release points) x BAC, with PV from the release plan's
  planned points per sprint — never raw points or percentages as EV against dollar PV/AC.
- **Hybrid:** baseline the committed scope with full EVM (in Helios, the build and launch work
  packages) and cap the discretionary scope as a run-rate; one BAC covers both so the forecast
  stays whole.

## Inputs you need
Work-package estimates (from `estimation`), the schedule for time-phasing (from
`project-schedule`), rate cards, vendor and licence prices (from `procurement-management`), the
charter budget range (from `business-case`), and a risk-based contingency figure (from
`risk-management`). To track performance you also need, per work package and cumulative to the
status date, **planned value (PV)**, **earned value (EV)** and **actual cost (AC)**, plus the
earning rule agreed for that package.

## Workflow
1. **Aggregate work-package costs — no reserves yet.** Roll the estimates up the WBS to control
   accounts and a project total, covering labour (effort x rate), licences, vendor fees and
   hosting. Helios: ten work packages, $460,000. See `references/cost-baselining.md`. *Done: a
   bottom-up total per control account and for the project.*
2. **Size the reserves.** Take the contingency from `risk-management` (post-response EMV or a
   simulation of the register — Helios $40,000) and set the management reserve by policy, held
   by the sponsor above the baseline (Helios $25,000). *Done: both reserves sized and recorded
   separately, not padded into the estimates.*
3. **Build the baseline.** Cost baseline = work-package costs + contingency = **BAC** (Helios
   $500,000; management reserve stays outside). Time-phase it per period in
   `assets/cost-baseline-template.csv` (`wbs_id, work_package, period, planned_cost`) and plot
   the cumulative planned cost as the **S-curve**. *Done: BAC and an S-curve that ends at it.*
4. **Fix the earning rule per work package.** Agree how EV is measured before tracking starts:
   0/100 for short packages, 50/50 for ones that straddle a period end, weighted milestones or
   physical percent complete for long ones, apportioned effort or level of effort only where
   unavoidable. See the table in `references/earned-value.md`. *Done: an earning rule recorded
   per work package so EV is a measurement, not a judgement call.*
5. **Baseline and commit.** Get the sponsor to approve the baseline and the earning rules; it is
   now the line you measure against. *Done: baseline approved and frozen — changes only via
   `change-management`.*
6. **Measure performance each period.** Record **cumulative-to-date** PV, EV and AC per work
   package (not this period's increment) in the layout of `assets/evm-snapshot.csv` and run:
   ```bash
   python .claude/skills/cost-management/scripts/health_check.py .claude/skills/cost-management/assets/evm-snapshot.csv
   ```
   It prints per-row and TOTAL CV, SV, CPI, SPI, EAC and VAC with a RAG verdict, then the TOTAL
   percent complete and spent, ETC and TCPI. Add a `period` column (as in
   `assets/evm-history-sample.csv`) for a CPI/SPI trend table and a text S-curve. *Done: current
   CPI/SPI, a RAG status and the direction of travel.*
7. **Forecast.** Choose the EAC formula that matches the cause of the variance — `--eac-method
   cpi` when the cost trend will continue (default), `atypical` for a one-off, `composite` when
   cost and schedule pressure compound, `all` to print the range — and check the realism line:
   if TCPI(BAC) is far above the CPI achieved so far, the original budget is not landable. Helios:
   EAC $516k–$558k, TCPI 1.07 vs CPI 0.93 → re-plan. *Done: a defensible forecast with its
   assumption stated, compared against BAC and the reserves.*
8. **Control and report.** Investigate the worst variances first (`--sort worst`), act on them,
   and feed the RAG, forecast and trend into `status-report` and `project-delivery` (`--format
   json` or `csv` hands the numbers over). Re-baseline through `change-management` when the
   forecast exceeds the reserves. *Done: variances explained, actions owned, numbers reported.*

## Quality checklist
- [ ] Work-package costs are aggregated bottom-up before any reserve is added.
- [ ] Contingency (inside BAC) and management reserve (outside BAC) are sized, distinct and justified.
- [ ] The baseline is time-phased per period and the S-curve ends at BAC.
- [ ] An earning rule is recorded per work package.
- [ ] The baseline is approved and changed only through change control.
- [ ] PV, EV and AC are captured cumulative-to-date each period; CV/SV/CPI/SPI are computed.
- [ ] A forecast (EAC/ETC/VAC) exists with its EAC assumption stated, and TCPI has been checked for realism.
- [ ] The RAG status follows the bands (GREEN both ≥ 0.95, RED either < 0.85, else AMBER) and is reported via `status-report` with its trend.

## Anti-patterns
- Tracking actuals vs budget only (burn rate) with no earned value — you cannot tell late from over.
- Folding contingency into the estimates, or counting management reserve in BAC, so the real
  estimate and the buffers are indistinguishable.
- Letting "percent complete" be whatever the team feels instead of a fixed earning rule.
- Entering this period's spend instead of cumulative figures, which breaks ETC and every index.
- Treating EAC as the original budget no matter how bad CPI gets — denial, not forecasting.
- Mixing value units (dollars for PV/AC, points or percentages for EV) so the indices are meaningless.
- Reporting a single colour with no variance analysis, forecast or trend behind it.

## Resources
- `references/cost-baselining.md` — aggregation, sizing and placing the reserves (BAC excludes
  management reserve), the Helios time-phased S-curve, earning rules, freeze and control.
- `references/earned-value.md` — PV/EV/AC, earning rules, CV/SV/CPI/SPI with caveats, the four
  EAC formulas, TCPI, the RAG bands, and the Helios worked example (CPI 0.93 / SPI 0.92 / AMBER).
- `assets/cost-baseline-template.csv` — time-phased planned cost (`wbs_id, work_package,
  period, planned_cost`), pre-filled with the Helios sample rows (replace them, keep the header).
- `assets/evm-snapshot.csv` — the Helios EVM snapshot at the end of month 3, values cumulative
  to the status date (`task, pv, ev, ac, bac`); the script's sample input.
- `assets/evm-history-sample.csv` — the same snapshot with a `period` column (M1–M3) for the
  trend table and S-curve.
- `scripts/health_check.py` — CV/SV, CPI/SPI, EAC/ETC/VAC, TCPI, percent complete and spent, RAG
  per row and overall; `--eac-method cpi|atypical|composite|all`, `--bac`, `--green`/`--amber`,
  `--tcpi-warn`, `--sort worst`, `--incremental`, `--json`, `--format table|json|csv|md`. Run
  `python .claude/skills/cost-management/scripts/health_check.py --help` for columns, aliases,
  formulas and exit codes.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-planning` — the planning phase that sets this cost baseline (its step 4) alongside scope and schedule.
- `project-delivery` — where the baseline is tracked each period and variances are acted on.
- `risk-management` — sizes the contingency reserve that goes inside the baseline and sets the management reserve policy.
- `estimation` — produces the per-work-package estimates this skill aggregates into the baseline.
- `business-case` — sets the investment envelope and ROI the baseline and forecast must respect.
- `status-report` — reports the CPI/SPI, forecast and RAG produced here to the sponsor and steering committee.
- `procurement-management` — supplies the vendor and licence prices in the baseline and the invoices that become actual cost.
