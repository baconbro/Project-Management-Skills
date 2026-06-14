# Earned Value Management (EVM)

EVM measures cost and schedule performance against the baseline using three primitives and a
handful of derived metrics. The power of EVM is that it compares against the *value of work
actually done*, so it can tell "behind" from "over budget" — which a burn-rate chart cannot.

## The three primitives
- **PV — Planned Value:** budgeted cost of work *scheduled* by now (read off the S-curve).
- **EV — Earned Value:** budgeted cost of work *actually completed* by now (% complete x its budget).
- **AC — Actual Cost:** what was *actually spent* on that completed work.

All three must be in the same units (usually dollars). **BAC** is the budget at completion
(the full baseline; the top of the S-curve).

## Variances (zero = on plan; negative = bad)
```
CV  = EV - AC      Cost Variance       (negative = over budget)
SV  = EV - PV      Schedule Variance   (negative = behind schedule)
```

## Performance indices (1.0 = on plan; < 1 = bad)
```
CPI = EV / AC      Cost Performance Index      ($ of value per $ spent)
SPI = EV / PV      Schedule Performance Index  ($ of value per $ planned)
```

## Forecasts
```
EAC  = BAC / CPI         Estimate at Completion (assumes current cost efficiency continues)
ETC  = EAC - AC          Estimate to Complete   (remaining cost)
VAC  = BAC - EAC         Variance at Completion (forecast over/under; negative = overrun)
TCPI = (BAC - EV) / (BAC - AC)   To-Complete Performance Index (efficiency needed to hit BAC)
```
If TCPI is much above 1.0, hitting the original budget is unrealistic — re-plan or re-baseline.

## Worked example (Helios, end of month 3)
Plan said $300,000 of work should be done (PV). The team completed work budgeted at $240,000
(EV) but spent $300,000 to do it (AC). BAC = $1,000,000.

| Metric | Formula | Value | Reading |
|--------|---------|-------|---------|
| CV  | EV - AC = 240k - 300k     | **-$60,000** | over budget |
| SV  | EV - PV = 240k - 300k     | **-$60,000** | behind schedule |
| CPI | EV / AC = 240k / 300k     | **0.80** | getting $0.80 of value per $1 spent |
| SPI | EV / PV = 240k / 300k     | **0.80** | 80% of planned progress |
| EAC | BAC / CPI = 1,000k / 0.80 | **$1,250,000** | projected total cost |
| ETC | EAC - AC = 1,250k - 300k  | **$950,000** | still to spend |
| VAC | BAC - EAC = 1,000k - 1,250k | **-$250,000** | forecast $250k overrun |

Verdict: CPI and SPI of 0.80 are both below 0.85 — this is a **RED** project. The forecast
overrun ($250k) and schedule slip both demand action now, not at the next gate.

## Reading the indices quickly
- CPI < 1 and SPI < 1: over budget *and* late (Helios above) — the worst quadrant.
- CPI > 1, SPI < 1: under budget but slow — maybe under-resourced.
- CPI < 1, SPI > 1: ahead but expensive — burning resource to stay on schedule.
- Both ≥ 1: healthy. `health_check.py` turns CPI/SPI into a RAG status using these bands.
