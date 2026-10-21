# Earned Value Management (EVM)

EVM measures cost and schedule performance against the baseline using three primitives and a
handful of derived metrics. Its power is that it compares against the *value of the work
actually done*, so it can tell "behind" from "over budget" — which a burn-rate chart cannot.
The worked numbers below are the sample Helios project (a fictional customer self-service
portal used throughout this catalog) at the end of month 3: the rows of
`assets/evm-snapshot.csv`.

## The three primitives (all cumulative to the status date, all in one currency)
- **PV — Planned Value:** budgeted cost of the work *scheduled* to be done by now (read off the
  S-curve in `cost-baselining.md`).
- **EV — Earned Value:** budgeted cost of the work *actually done* by now, credited with the work
  package's earning rule (below) — never the money spent, never raw story points.
- **AC — Actual Cost:** cost actually incurred for the work performed to date, including
  partially complete work.

**BAC** (budget at completion) is the total of the cost baseline — work-package costs plus the
contingency reserve — and the top of the S-curve. Management reserve sits above the baseline and
is **not** in BAC; releasing it moves money into the baseline through change control and re-sets
BAC. Record PV, EV and AC cumulative-to-date, not as this period's increment: the indices and
every forecast formula below only hold for cumulative figures.

## Earning rules (agree one per work package before tracking starts)
| Rule | EV is credited... | Use for |
|------|-------------------|---------|
| **0/100** | 100% only when the package is complete | short packages (one or two periods) — Helios 1.5.2 Operational handover |
| **50/50** (or 25/75) | half at start, the rest at completion | short packages that straddle a period end — Helios 1.5.1 Training & communications |
| **Weighted milestones** | a fixed % at each verifiable milestone | long packages with interim deliverables — Helios 1.3.1 Identity / SSO integration: sandbox connected 30%, SSO working in test 70%, production cut-over 100% |
| **Physical % complete** | objectively counted output (screens built, test cases passed) | packages with countable units — Helios 1.4.1 System & UAT testing by test cases passed |
| **Apportioned effort** | in proportion to a related discrete package | QA or review effort tied to a build package |
| **Level of effort (LOE)** | EV = PV every period | management and support work only — Helios 1.1 Project management; never for deliverables (LOE can never show a schedule variance) |

Pick the rule when the baseline is set and record it next to the work package. A subjective
"percent complete" is the most common way EVM is gamed; the rule makes EV a measurement, not an
opinion.

## Variances (zero = on plan; negative = bad)
```
CV = EV - AC      Cost Variance       (negative = over budget)
SV = EV - PV      Schedule Variance   (negative = behind schedule)
```

## Performance indices (1.0 = on plan; below 1 = bad)
```
CPI = EV / AC     Cost Performance Index      (value earned per unit spent)
SPI = EV / PV     Schedule Performance Index  (value earned per unit planned)
```
**Caveat:** SV and SPI are in currency, not days, and converge to 0 / 1.0 as the project nears
completion no matter how late it finishes (EV and PV both end at BAC). Read them alongside the
milestone forecast dates in `status-report` (or earned schedule) and do not rely on SPI in the
final third of the project. A CPI or SPI of exactly 0 (money spent or time elapsed, nothing
earned) is a defined, worst-possible value — RED, not "unknown".

## Forecasts
```
EAC (typical variance, default)   = BAC / CPI                       current cost efficiency continues
EAC (atypical / one-off variance) = AC + (BAC - EV)                 the rest of the work goes to plan
EAC (cost AND schedule persist)   = AC + (BAC - EV) / (CPI x SPI)   both pressures compound
EAC (re-estimate)                 = AC + bottom-up ETC              the original estimate no longer holds
ETC = EAC - AC        VAC = BAC - EAC        (VAC negative = forecast overrun)
TCPI(BAC) = (BAC - EV) / (BAC - AC)   efficiency needed on the remaining work to land on the original budget
TCPI(EAC) = (BAC - EV) / (EAC - AC)   efficiency needed to land on the accepted EAC
```
State which EAC assumption you used and why. `scripts/health_check.py --eac-method
cpi|atypical|composite|all` computes the first three (`all` prints them as a range); the
bottom-up re-estimate comes from `estimation`. When TCPI(BAC) is well above the CPI achieved so
far (the script flags a gap above 0.10, tunable with `--tcpi-warn`), landing on BAC is
unrealistic — re-plan or re-baseline through `change-management` rather than hoping.

## Worked example (Helios, end of month 3)
Plan said $255,000 of work should be done (PV). The team completed work budgeted at $235,500
(EV) and spent $252,000 doing it (AC). BAC = $500,000 (`assets/evm-snapshot.csv`).

| Metric | Formula | Value | Reading |
|--------|---------|-------|---------|
| CV  | EV - AC = 235,500 - 252,000 | **-$16,500** | over budget |
| SV  | EV - PV = 235,500 - 255,000 | **-$19,500** | behind schedule |
| CPI | EV / AC = 235,500 / 252,000 | **0.93** | $0.93 of value per $1 spent |
| SPI | EV / PV = 235,500 / 255,000 | **0.92** | 92% of planned progress |
| % complete / % spent | EV / BAC, AC / BAC | **47.1% / 50.4%** | spend is running ahead of progress |
| EAC | BAC / CPI = 500,000 / 0.9345 | **$535,032** | projected total cost (cost trend continues) |
| ETC | EAC - AC = 535,032 - 252,000 | **$283,032** | still to spend |
| VAC | BAC - EAC = 500,000 - 535,032 | **-$35,032** | forecast overrun of 7% of BAC |
| EAC range | atypical / CPI / composite | **$516.5k / $535.0k / $558.5k** | a $42k spread — the reserve conversation depends on which cause you believe |
| TCPI(BAC) | (BAC - EV) / (BAC - AC) = 264,500 / 248,000 | **1.07** | the remaining work must run 7% more efficiently than plan — and 13 points above the 0.93 achieved: re-plan |
| TCPI(EAC) | (BAC - EV) / (EAC - AC) = 264,500 / 283,032 | **0.93** | the CPI-based EAC only needs today's efficiency to hold |

Verdict: CPI 0.93 and SPI 0.92 both sit in the 0.85–0.95 band — Helios is **AMBER** overall,
with the contingency reserve ($40,000) about to be consumed by the forecast overrun. Per work
package, Identity / SSO integration is **RED** (CPI 0.69, SPI 0.75: the identity-provider slip,
risk R001, has materialised) and Reporting & analytics is RED because it waits on the UI;
Knowledge base is ahead (1.10 / 1.10). The sponsor conversation is about SSO, not the average.

## Reading the indices quickly
- CPI < 1 and SPI < 1: over budget *and* late (Helios overall, SSO in particular) — the worst quadrant.
- CPI > 1, SPI < 1: under budget but slow — maybe under-resourced.
- CPI < 1, SPI > 1: ahead but expensive — burning resource to hold the schedule.
- Both ≥ 1: healthy (Helios Knowledge base).
- **RAG bands** (the same as `status-report`): GREEN when CPI *and* SPI ≥ 0.95; RED when either
  is < 0.85; otherwise AMBER. `scripts/health_check.py` applies them per row and to the TOTAL
  (`--green` / `--amber` override them).
- **Direction of travel** matters as much as the colour: with a `period` column
  (`assets/evm-history-sample.csv`) the script prints a CPI/SPI trend — Helios CPI 1.05 → 1.00
  → 0.93 is a worsening AMBER, which reads very differently from a recovering one.
