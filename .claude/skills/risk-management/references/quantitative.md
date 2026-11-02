# Quantitative Risk Analysis

Qualitative analysis ranks risks on ordinal 1-5 scales; quantitative analysis puts money (or
time) on the risks that justify the effort and on the project as a whole. Use it for three
jobs only: to choose between response options, to find the risk that drives the total, and —
**after responses are planned** — to size the contingency reserve. Examples use the sample
Helios project (a fictional customer self-service portal used throughout this catalog) and its
register in `.claude/skills/risk-register/assets/risk-register-template.csv`.

## 1. Two different numbers: the P x I score and EMV

| | Qualitative P x I score | Expected monetary value (EMV) |
|---|---|---|
| Inputs | Probability rating 1-5 x impact rating 1-5 | Probability as a fraction x impact in currency |
| Result | A score of 1-25 with no unit | Money: the probability-weighted cost or benefit |
| Use | Rank and band the whole register (step 3) | Choose responses and size reserves (steps 4-6) |
| Can you add them up? | **No** — a sum of ordinal scores means nothing | Yes, within one direction (threats or opportunities) |
| Helios R001 | 3 x 5 = 15 → HIGH | 0.4 x $120,000 = $48,000 → HIGH |

Keep the register in one unit. If it holds 1-5 ratings, `risk_score.py --prob-scale 1-5
--impact-scale 1-5` gives a ranking score; its totals are not a reserve. Quantify the material
risks in currency before you size anything.

## 2. Record impacts as positive magnitudes; let the `type` column carry the direction
In the register every impact is a **positive magnitude** — the cost if a threat occurs, the
benefit if an opportunity occurs — and the `type` column says which it is. `risk_score.py`
rejects a negative impact and bands on magnitude, so a threat entered as -$120,000 would be
refused rather than silently banded LOW.

```
EMV (exposure) = probability x impact          (a positive number for every row)
```

| Id | Risk | Type | P | Impact | EMV |
|---|---|---|---:|---:|---:|
| R001 | Identity-provider integration slips past the agreed date | threat | 0.40 | $120,000 | **$48,000** |
| R002 | Undocumented requirements expand portal scope | threat | 0.60 | $40,000 | $24,000 |
| R003 | Lead engineer leaves mid-project | threat | 0.15 | $80,000 | $12,000 |
| R004 | Cloud hosting costs exceed the budget | threat | 0.50 | $15,000 | $7,500 |
| R005 | Minor UI rework after usability testing | threat | 0.70 | $4,000 | $2,800 |
| R006 | Knowledge base deflects tickets earlier than planned | opportunity | 0.30 | $60,000 | $18,000 |

**Score threats and opportunities separately.** Total threat EMV is **$94,300**; total
opportunity EMV is **$18,000**, reported on its own line. The net figure the script also
prints ($76,300) describes the portfolio; it is never the basis of a reserve, because the
opportunity may not happen and a reserve shrunk by uncertain upside runs dry exactly when the
threats land.

## 3. Decision trees — the one place signs are applied
When a decision branches into uncertain outcomes, draw a tree and fold back the EMV of each
branch. Here costs are written as negative and benefits as positive so that one tree can mix
them; the sign belongs to the tree, never to the register. Helios had to decide how to deliver
the identity / SSO integration (work package 1.3.1):

```
                         ┌ success (70%): -$50k   → EMV = 0.7(-50) + 0.3(-140) = -$77k
          ┌ Build ───────┤
 Decision ┤              └ rework  (30%): -$140k
          └ Buy widget ── certain: -$90k                              → -$90k
```

**Build** wins on expected value (-$77k beats -$90k) even though its worst case is worse, which
is why `procurement-management` records "make" for the integration. The tree also exposes the
appetite question: the sponsor must be able to absorb the 30% rework branch. Choosing Build
keeps that uncertainty inside the project, which is why R001 is on the register and owned there.

## 4. Sensitivity analysis and the tornado diagram
Swing one input at a time across its plausible range and see how far the total moves. Plotted
as horizontal bars sorted longest first, the swings form a **tornado diagram**. For Helios'
residual threats, the swing of each risk is "does not occur" ($0) to "occurs" (its residual
impact):

```
R001 Identity-provider slip   |████████████████████████████████████████| $120,000
R002 Scope expansion          |█████████████                           |  $40,000
R003 Lead engineer leaves     |█████████████                           |  $40,000
R004 Hosting over budget      |█████                                   |  $15,000
R005 Minor UI rework          |█                                       |   $4,000
```

R001 dominates, as it does the effort estimate (`estimation`: the SSO integration carries 39%
of the variance). The widest bar is where to buy certainty first (the week-1 integration spike)
and the risk most likely to overwhelm the reserve on its own.

## 5. Simulation: why summed EMV is not a reserve
Summed EMV is the **mean** of a skewed, lumpy distribution: in most outcomes few or none of the
risks occur, and in a few several do. Holding the mean leaves the project short in a large share
of outcomes. Simulate instead — `risk_score.py` draws each threat against its probability
(opportunities are not simulated) and reports percentiles:

```bash
python .claude/skills/risk-register/scripts/risk_score.py .claude/skills/risk-register/assets/risk-register-template.csv --basis residual --simulate 10000 --seed 42 --reserve 40000
```

| Helios total threat exposure | Mean | P50 | P80 | P90 |
|---|---:|---:|---:|---:|
| Inherent (before responses) | $94,300 | $59,000 | $164,000 | $179,000 |
| Residual (after planned responses) | $52,300 | $40,000 | $99,000 | $139,000 |

A $40,000 reserve covers about 52% of the residual outcomes (P(total > $40,000) is about 48%).
Add `impact_min`/`impact_max` columns to any threat whose impact is a range (the script draws a
triangular value), and use the same idea on durations in `project-schedule` for the schedule
reserve. Without a tool, reason the same way: estimate optimistic, most likely and pessimistic
values and talk in confidence levels, not single points.

## 6. Size the contingency reserve — after responses are planned
1. **Plan responses first** and re-score each threat's residual probability and impact. A
   reserve sized on inherent exposure over-funds every risk you then mitigate, avoid or transfer.
2. **Put proactive response costs in the work-package estimates.** A spike, a pairing rota or a
   contract clause is planned work, not contingency. Contingent plans (fallbacks run only when a
   trigger fires) are paid from contingency unless their cost is already part of the impact.
3. **Read the reserve at the plan's confidence level** — P80 from the simulation by default.
   Without a simulation, use summed residual threat EMV times an uplift agreed in the plan.
   Summed residual EMV is the mean loss: funding below it is a sponsor decision, never a default.
4. **Check single-risk dominance.** A threat whose residual impact exceeds the reserve cannot be
   absorbed if it fires; reduce its impact further or pre-agree what happens when it does.
5. **Report opportunities separately.** Their EMV never reduces the reserve; a realised benefit
   is taken through change control and the business case.
6. **Record the figure, its confidence and any accepted gap** in the risk management plan, signed
   by the sponsor, and hand the figure to `cost-management`.

**Helios worked example.** Residual threat EMV is $52,300 and P80 is $99,000. The work packages
cost $460,000, so funding P80 would have lifted BAC to $559,000 — above the $500,000 investment
the business case appraised and above the charter's $550,000 ceiling. Sam Lee put three options
to Dana Okoro: fund P80 and re-appraise the business case; cut exposure further; or hold BAC at
$500,000 and accept the gap with a decision path. She chose the third: contingency **$40,000**
(about P50, 52% coverage). Even counting the $25,000 management reserve — meant for unidentified
risks — identified-risk coverage reaches only about 76%. The plan records the gap: R001's residual
impact ($120,000) alone exceeds the reserve, so if its trigger fires Sam Lee escalates to the
steering committee within two working days with three options — release management reserve, a
scope trade-off through change control, or a re-baseline.

## 7. Contingency, management and schedule reserves

| Reserve | Covers | Sized by | Sits | Controlled by | Helios |
|---|---|---|---|---|---|
| Contingency | Identified risks ("known-unknowns"), after responses | Residual simulation at the plan's confidence | Inside the cost baseline (BAC) | Project manager (Sam Lee) | $40,000 |
| Management reserve | Unidentified risks ("unknown-unknowns") | Policy (Helios: 5% of BAC) | Above BAC, in the total budget | Sponsor (Dana Okoro), released through change control | $25,000 |
| Schedule reserve | Duration uncertainty on the critical path | `project-schedule` simulation | Held once before the milestone it protects | Project manager | About 2.4 weeks (P80 20.4 vs 18 weeks) |

See `cost-management` for how the reserves sit in and above the baseline and how drawdown is
recorded.

## 8. Reserve analysis during delivery
At each review compare the contingency still unspent with the residual threat exposure still
open. Retire risks whose window has passed and re-run the simulation on what remains. When the
remaining reserve falls below the exposure at the agreed confidence, escalate before it runs out,
not after. Helios at the end of month 3: R001 has occurred (issue I001 in the `project-delivery`
issue log), the forecast at completion is about $535,000 (VAC about -$35,000) and the overrun is
about to consume the $40,000 contingency, so the escalation path in the plan has been used and
the decision sits with the steering committee.
