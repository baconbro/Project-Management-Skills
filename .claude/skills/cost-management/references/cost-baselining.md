# Cost Baselining

The cost baseline is the approved, time-phased budget you measure performance against. It is
built bottom-up from the `estimation` outputs, has its reserves sized *before* one of them is
added, is time-phased into an S-curve, and is frozen so that variances mean something. The
figures below are the sample Helios project (a fictional customer self-service portal used
throughout this catalog).

## 1. Aggregate work-package costs (no reserves yet)
Roll estimates up the work breakdown structure:

```
Activity estimates  ->  Work-package cost  ->  Control-account cost  ->  Project cost estimate
```

Each level is the sum of the level below. Include every cost type — labour (effort x rate),
materials, licences, vendor fees, infrastructure. Helios work package 1.3.1 Identity / SSO
integration aggregates engineering person-days x the blended rate, the identity-provider licence
and the vendor's integration fee (bought through `procurement-management`), and cloud hosting
for the auth service. The ten Helios work packages sum to **$460,000**. Aggregating bottom-up
(not allocating a top-down number) keeps the figure defensible.

## 2. Size the reserves — then add only one of them to the baseline
| Reserve | Covers | Sits | Controlled by | Sized from | Helios |
|---------|--------|------|---------------|------------|--------|
| **Contingency** | Identified ("known-unknown") risks | *Inside* the cost baseline — inside BAC | Project manager (Sam Lee) | Summed post-response EMV or a simulation of the register (`risk-management`, `risk-register`) | $40,000 |
| **Management** | Unidentified ("unknown-unknown") risks | *Above* the baseline, in the total budget — **not** in BAC | Sponsor (Dana Okoro) | Policy % of the baseline | $25,000 |

```
Cost baseline = Σ work-package costs + contingency reserve   = BAC for EVM (the top of the S-curve)
Total budget  = Cost baseline + management reserve           (NOT BAC — MR is never planned as PV nor earned as EV)
Helios:  $460,000 + $40,000 = BAC $500,000;  + $25,000 MR = total budget $525,000 (inside the charter's $450k–$550k)
```

Never blend reserves into the estimates: if the buffer is invisible you cannot tell a good
estimate that consumed contingency from a bad one that blew through it. Releasing management
reserve into the baseline is a change (`change-management`) that re-sets BAC.

**Where the contingency is held.** Helios distributed its $40,000 to the work packages in
proportion to WBS weight when the baseline was approved, so each row's BAC in
`assets/evm-snapshot.csv` is weight x $500,000 and the per-row BACs sum to the whole baseline
(1.3.1 Identity / SSO integration: 45% x 35% x $500,000 = $78,750). Many organisations hold it
instead as a single undistributed line drawn down through change control. Either way it is
inside BAC, visible, and recorded separately from the estimates it protects.

## 3. Time-phase the baseline into the S-curve
Spread each work package's budget over the periods it is scheduled in (`project-schedule`) to
get **planned value (PV)** per period. `assets/cost-baseline-template.csv` holds the Helios rows
(`wbs_id, work_package, period, planned_cost`; replace them with yours, keep the header).
Cumulative planned cost is the **S-curve**:

| Period | Planned cost | Cumulative PV | What is happening |
|--------|-------------:|--------------:|-------------------|
| M1 | 53,333 | 53,333 | Requirements & user research; *Discovery complete* milestone |
| M2 | 108,333 | 161,666 | UX prototype; Identity / SSO, UI and knowledge-base build start |
| M3 | 93,334 | 255,000 | Build continues; reporting starts — the PV in the EVM snapshot |
| M4 | 113,333 | 368,333 | Build completes; UAT starts; *MVP live to pilot* milestone |
| M5 | 68,333 | 436,666 | UAT, hardening, training |
| M6 | 63,334 | 500,000 | Launch and handover; *General availability* — BAC |

```
Cost
 ^                                   ____------  BAC $500,000
 |                          __---''''
 |                  __--''''                      shallow at the start and end,
 |          __--''''                              steep through the build months
 |   __--'''
 +------------------------------------------> Time (M1 .. M6)
       (cumulative planned value = the S-curve)
```

At any status date the S-curve tells you how much value *should* have been delivered (PV),
which you compare against EV and AC. It also sets the expected burn rate, so a flat or runaway
actuals line is visible immediately. `scripts/health_check.py` draws the same curve from a
period file (`assets/evm-history-sample.csv`).

## 4. Fix the earning rules
Before approval, agree how earned value will be measured for each work package — 0/100, 50/50,
weighted milestones, physical percent complete, apportioned effort, or level of effort — and
record the rule with the work package (see the table in `earned-value.md`). The rules are part
of the baseline: freezing PV but leaving EV to judgement makes every later index arguable.

## 5. Freeze and control
Once the sponsor approves it, the baseline is frozen. Real costs will diverge — that divergence
is the *signal* EVM measures. Re-baseline only through formal change control
(`change-management`); silently moving the line destroys your ability to measure performance.
Hand the time-phased PV, the BAC and the earning rules to `earned-value.md` to track delivery,
and report the result through `status-report`.
