# Cost Baselining

The cost baseline is the approved, time-phased budget you measure performance against. It is
built bottom-up from estimates, time-phased into an S-curve, and frozen so that variances mean
something. Changing it afterwards requires change control.

## 1. Cost Aggregation
Roll estimates up the work breakdown structure:

```
Activity estimates  ->  Work-package cost  ->  Control-account cost  ->  Project cost estimate
```

Each level is the sum of the level below. Include all cost types — labour (rate x effort),
materials, licences, vendor fees, infrastructure. For Helios, the integration work package
aggregates engineering days x blended rate, the IdentityCo licence, and cloud hosting for the
auth service. Aggregating bottom-up (not top-down allocation) keeps the number defensible.

## 2. Reserves: contingency vs management
Two reserves, deliberately kept separate:

| Reserve | Covers | Sits | Controlled by | Sized from |
|---------|--------|------|---------------|------------|
| **Contingency** | Identified ("known-unknown") risks | *Inside* the cost baseline | Project manager | Summed EMV / simulation (`risk-management`) |
| **Management** | Unidentified ("unknown-unknown") risks | *Above* the baseline, in the budget | Sponsor | Policy % of baseline |

```
Cost baseline = Σ work-package costs + contingency reserve
Total budget  = Cost baseline + management reserve   (this total = BAC for EVM)
```

Never blend reserves into the estimates: if the buffer is invisible, you cannot tell a good
estimate that consumed contingency from a bad estimate that blew through it.

## 3. Time-phasing and the S-curve
Spread the baseline across the schedule to get **planned value (PV)** per period. Plotting
*cumulative* PV over time produces the classic **S-curve** — shallow at the start and end,
steep through the middle where most work happens.

```
Cost
 ^                                   ____------  BAC
 |                          __---''''
 |                  __--''''
 |          __--''''
 |   __--'''
 +------------------------------------------> Time
       (cumulative planned value = the S-curve)
```

The S-curve is the reference line for earned-value tracking: at any date it tells you how much
value *should* have been delivered (PV), which you compare against EV and AC. It also sets the
expected burn rate, so a flat or runaway actuals line is visible immediately.

## 4. Freeze and control
Once approved, the baseline is frozen. Real costs will diverge — that divergence is the *signal*
EVM measures. Re-baseline only through formal change control (see `change-management`); silently
moving the line destroys your ability to measure performance. Hand the time-phased PV and the
BAC to `references/earned-value.md` to track delivery.
