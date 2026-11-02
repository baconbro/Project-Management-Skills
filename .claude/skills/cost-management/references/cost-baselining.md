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
for the auth service. The eleven Helios work packages, on ten cost lines (1.2.1 and 1.2.2 are
costed at control account 1.2, Discovery & design), sum to **$460,000**. Aggregating bottom-up
(not allocating a top-down number) keeps the figure defensible.

## 2. Size the reserves — then add only one of them to the baseline
| Reserve | Covers | Sits | Controlled by | Sized from | Helios |
|---------|--------|------|---------------|------------|--------|
| **Contingency** | Identified ("known-unknown") risks | *Inside* the cost baseline — inside BAC | Project manager (Sam Lee) | A simulation of the residual (post-response) register, read at the confidence the sponsor accepts (`risk-management`, `risk-register`) | $40,000 — about P50; the sponsor accepted the gap to P80 ($99,000), and summed residual threat EMV ($52,300) is the mean, not the reserve |
| **Management** | Unidentified ("unknown-unknown") risks | *Above* the baseline, in the total budget — **not** in BAC | Sponsor (Dana Okoro) | Policy % of the baseline | $25,000 |

Estimating uncertainty (the commit-level reserve from `estimation`) belongs in the same
contingency, not in a second reserve; where it is material, model it with the residual risks
rather than adding the two percentiles. The work-package costs from section 1 are at expected
values, so the estimating reserve either enters the risk simulation as an uncertainty line or is
held as a separate, named line inside the contingency, never both; record which you chose.

```
Cost baseline = Σ work-package costs + contingency reserve   = BAC for EVM (the top of the S-curve)
Total budget  = Cost baseline + management reserve           (NOT BAC — MR is never planned as PV nor earned as EV)
Helios:  $460,000 + $40,000 = BAC $500,000;  + $25,000 MR = total budget $525,000 (inside the charter's $450k–$550k)
```

Never blend reserves into the estimates: if the buffer is invisible you cannot tell a good
estimate that consumed contingency from a bad one that blew through it. Releasing management
reserve is a change (`change-management`): a release for unplanned in-scope work raises BAC; a
release that funds an overrun on baselined work raises the funded budget but not BAC, so CV and
CPI stay measured against the original BAC (Helios funded its $18,600 overrun this way on
2026-09-08).

**Where the contingency is held.** Helios distributed its $40,000 to the work packages in
proportion to WBS weight when the baseline was approved, so each row's BAC in
`assets/evm-snapshot.csv` is weight x $500,000 and the per-row BACs sum to the whole baseline
(1.3.1 Identity / SSO integration: 45% x 35% x $500,000 = $78,750). Many organisations hold it
instead as a single undistributed line drawn down through change control. Either way it is
inside BAC and visible, and each package's share is recorded separately from the estimate it
protects. The Helios split (work = weight x $460,000, contingency = weight x $40,000):

| Work package | Weight of BAC | Work | Contingency share | Row BAC |
|---|---:|---:|---:|---:|
| 1.1 Project management | 10% | 46,000 | 4,000 | 50,000 |
| 1.2 Discovery & design | 15% | 69,000 | 6,000 | 75,000 |
| 1.3.1 Identity / SSO integration | 15.75% | 72,450 | 6,300 | 78,750 |
| 1.3.2 Self-service UI | 13.5% | 62,100 | 5,400 | 67,500 |
| 1.3.3 Knowledge base | 9% | 41,400 | 3,600 | 45,000 |
| 1.3.4 Reporting & analytics | 6.75% | 31,050 | 2,700 | 33,750 |
| 1.4.1 System & UAT testing | 14% | 64,400 | 5,600 | 70,000 |
| 1.4.2 Hardening & launch | 6% | 27,600 | 2,400 | 30,000 |
| 1.5.1 Training & communications | 5% | 23,000 | 2,000 | 25,000 |
| 1.5.2 Operational handover | 5% | 23,000 | 2,000 | 25,000 |
| **Total** | **100%** | **460,000** | **40,000** | **500,000** |

PV and EV include each share, so the contingency balance is kept in the contingency log, and
every draw is a logged budget transfer between packages (CR003 $12,000 into 1.3.2; R001 $25,000
into 1.3.1; R004 $3,000 for hosting above forecast). Spreading by weight rather than by risk
leaves 1.3.1, which carries R001, only $6,300 of its own; the log, not the row, shows what is
left to draw.

## 3. Time-phase the baseline into the S-curve
Spread each work package's budget over the periods it is scheduled in (`project-schedule`) to
get **planned value (PV)** per period. The dated network sets each package's window; within a
window the budget is phased by the sprint plan (`agile-delivery`), which is usually back-loaded,
not spread in a straight line. Phasing linearly across the window would plan value the sprints
do not intend to produce yet, and the first period close would show a schedule variance that is
only a phasing error. Every package's planned periods must lie inside its window.

Helios closes an EVM period six times, named M1–M6 like the milestones: M1 2026-05-08 (weeks
1–5), M2 06-05 (weeks 6–9), M3 07-03 (weeks 10–13), M4 07-31 (weeks 14–17), M5 08-28 (weeks
18–21) and M6 10-02 (weeks 22–26, including the cutover week). The pilot (milestone M4,
2026-08-07) therefore falls in period M5. Windows from the 25-week network started on
2026-04-06:

| Work package (network task) | Network window | Planned in |
|---|---|---|
| 1.1 Project management | the whole project (level of effort) | M1–M6 |
| 1.2 Discovery & design (A, B) | 2026-04-06 to 05-08 | M1 |
| 1.3.1 Identity / SSO (C), 1.3.2 Self-service UI (D), 1.3.3 Knowledge base (E) | 05-11 to 07-10 (UI to 07-17) | M2–M4 |
| 1.3.4 Reporting & analytics (F) | 05-11 to 07-10; deflection dashboard in sprint S5 | M3–M4 |
| 1.4.1 System & UAT testing (G) | 07-20 to 08-14 (pilot UAT, pilot launch, stabilisation) | M4–M5 |
| 1.4.2 Hardening & launch (H), 1.5.1 Training & communications (I) | 08-17 to 09-18 (training to 09-11) | M5–M6 |
| 1.5.2 Operational handover (J) | 09-21 to 09-25 | M6 |

`assets/cost-baseline-template.csv` holds the Helios rows (`wbs_id, work_package, period,
planned_cost`; replace them with yours, keep the header). Cumulative planned cost is the
**S-curve**:

| Period | Planned cost | Cumulative PV | What is happening |
|--------|-------------:|--------------:|-------------------|
| M1 | 83,333 | 83,333 | Requirements & user research and UX prototype; *Discovery complete* milestone |
| M2 | 78,333 | 161,666 | Identity / SSO, UI and knowledge-base build start |
| M3 | 93,334 | 255,000 | Build continues; reporting starts — the PV in the EVM snapshot |
| M4 | 113,333 | 368,333 | Build completes (UI on 07-17); system test and pilot UAT |
| M5 | 68,333 | 436,666 | *MVP live to pilot* (2026-08-07) and stabilisation; hardening and training start |
| M6 | 63,334 | 500,000 | Hardening, training and handover; cutover week; *General availability* at the 2026-10-03 cutover — BAC |

```
Cost
 ^                                   ____------  BAC $500,000
 |                          __---''''
 |                  __--''''                      steepest in M4 (build completes,
 |          __--''''                              testing starts), flatter in M5-M6
 |   __--'''
 +------------------------------------------> Time (M1 .. M6)
       (cumulative planned value = the S-curve)
```

At any status date the S-curve tells you how much value *should* have been delivered (PV),
which you compare against EV and AC. It also sets the expected burn rate, so a flat or runaway
actuals line is visible immediately. `scripts/health_check.py` draws this curve to date, PV
against EV and AC, from a period file (`assets/evm-history-sample.csv`, M1–M3). The full planned
curve to BAC is the cumulative sum of `assets/cost-baseline-template.csv` by period (Helios:
83,333 / 161,666 / 255,000 / 368,333 / 436,666 / 500,000).

## 4. Fix the earning rules
Before approval, agree how earned value will be measured for each work package — 0/100, 50/50,
weighted milestones, physical percent complete, accepted story points, apportioned effort, or
level of effort — and record the rule with the work package (see the table in
`earned-value.md`). The rules are part of the baseline: freezing PV but leaving EV to judgement
makes every later index arguable.

## 5. Freeze and control
Once the sponsor approves it, the baseline is frozen. Real costs will diverge — that divergence
is the *signal* EVM measures. Re-baseline only through formal change control
(`change-management`); silently moving the line destroys your ability to measure performance.
Hand the time-phased PV, the BAC and the earning rules to `earned-value.md` to track delivery,
and report the result through `status-report`.
