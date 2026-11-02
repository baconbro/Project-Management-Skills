# Agile metrics and forecasting

Metrics exist to forecast and to start conversations, not to grade people. The numbers below
come from the sample Helios project (a fictional customer self-service portal used throughout
this catalog): `assets/sprint-history-sample.csv` run through `scripts/velocity_forecast.py`.

## Velocity and predictability
- **Velocity** = story points of the items that met the definition of done and were
  accepted at the review. No partial credit: an 8-point story 90% done counts 0 and returns
  to the backlog (re-sized if the remaining work changed).
- **Predictability** (say/do ratio) = completed ÷ committed. A settled team lands at 80–100%
  most sprints. Below 80% means over-commitment or unready work; well over 100% means it
  sandbagged or pulled in extra work.
- Helios S1–S6: velocities 22, 27, 31, 29, 25, 30 → mean 27.33, median 28.00, trailing-3
  28.00, range 22–31, coefficient of variation 12.4% (stable; above about 25%, quote only the
  range). Predictability 89.1% (164 of 184); only S1, the new team's first sprint, fell below
  the 80% floor (73.3%).
- Velocity belongs to one team doing one kind of work. Never compare teams, never set a
  velocity target, never convert points to hours: all three inflate points and destroy the
  forecast.

## Burndown versus burnup
| Chart | Plots | Good for | Hides |
|---|---|---|---|
| Sprint burndown | Points or tasks left in this sprint, per day | Daily stand-up: are we on track for the goal? | Nothing within a sprint |
| Release burndown | Points left in the release, per sprint | A fixed scope | Scope growth looks like slow progress |
| Release burnup | Cumulative done against total scope, per sprint | Any release where scope changes | Nothing: both lines are visible |

Helios S5 shows why burnup wins: the team completed 25 points, but CR003 (accessibility
uplift, approved 2026-06-30) added 12 points of scope, so the remaining work fell only from
137 to 124. A burndown shows a 13-point sprint; the burnup shows a 25-point sprint and a
scope line that stepped up. Over S1–S6 scope grew from 246 to 264 points (+3.6 per sprint).

## Flow metrics (Kanban, or alongside sprints)
- **Cycle time** — from start of work to done, per item; report the 85th percentile
  ("85% of stories finish within 6 working days"), not the mean.
- **Throughput** — items finished per week. **WIP** — items started and not finished.
- **Little's law:** average cycle time = average WIP ÷ average throughput. Cutting WIP is the
  cheapest way to cut cycle time.
- A **cumulative flow diagram** shows bottlenecks as a widening band (for example, "in test").

## Forecasting a release
Forecast with a velocity **range**, never one number:
1. Remaining work = open, sized points in the release (or release scope − cumulative done).
2. Three velocities from the history: the mean, the trailing-3 mean (recent reality), and the
   minimum. Sorted high to low, they give the optimistic, likely, and pessimistic scenarios.
3. Sprints needed = ceil(remaining ÷ velocity); finish = end of the last completed sprint +
   sprints × sprint length.
4. Against a fixed date (`--sprints-left N`), capacity = velocity × N; the **cut line** is the
   last backlog item, in priority order, that fits.

Helios after S6, 100 points remaining (Must 60, Should 24, Could 16), four sprints to GA:

| Scenario | Velocity | Sprints | Finishes | Capacity in 4 sprints | Cut line |
|---|---:|---:|---|---:|---|
| Optimistic (trailing-3) | 28.00 | 4 | 2026-09-25 | 112 | everything fits |
| Likely (mean) | 27.33 | 4 | 2026-09-25 | 109.33 | everything fits |
| Pessimistic (minimum) | 22.00 | 5 | 2026-10-09 | 88 | after HEL-170: 3 Could stories (13 pts) below |

Must and Should (84 points) fit even at the pessimistic velocity, so GA commits to them and
treats Could as stretch. If scope keeps growing at 3.6 points a sprint, the likely forecast
becomes 5 sprints, so scope intake must be traded (in for out) from here on.

Before three sprints of history exist, forecast from a planned first sprint or a similar
team's velocity and widen the range (for example ±40%); narrow it as real sprints arrive.
For stochastic forecasts, resample past sprint velocities (or weekly throughput) in a Monte
Carlo simulation and quote P50/P85 dates; the three-scenario method above is the minimum.

## Reporting: the release outlook as a RAG line
| Outlook | Rule | Action |
|---|---|---|
| GREEN | The pessimistic forecast fits in the sprints left | Report and carry on |
| AMBER | The likely forecast fits; the pessimistic one does not | Agree the cut line; keep enough Could scope below it |
| RED | The likely forecast does not fit | Escalate with options: cut scope, add a sprint, or change the milestone through change control |

Helios after S6 is AMBER. The `status-report` line reads: "Velocity 22–31 (trailing-3 28);
100 points left for GA; 4 sprints likely, 5 pessimistic, 4 available; Must and Should fit
at the pessimistic velocity — AMBER."

## Why story points are not earned value
Points are a team-relative size with no currency and no baseline; one point of reporting work
can cost more than one point of UI work. Never divide points by points and present the result
as SPI, and never add points to dollars. To earn value on agile work, convert per work package:
EV = accepted points ÷ planned points for the package × package BAC (planned value: the points
the release plan scheduled by that date, converted the same way). Helios at the end of S4
(2026-07-03), the month-3 earned-value snapshot:

| Work package | BAC | Planned points | $ per point | Planned by S4 | Accepted by S4 | PV | EV |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1.3.2 Self-service UI | 67,500 | 81 | 833.33 | 60 | 57 | 50,000 | 47,500 |
| 1.3.3 Knowledge base | 45,000 | 60 | 750.00 | 40 | 44 | 30,000 | 33,000 |
| 1.3.4 Reporting & analytics | 33,750 | 27 | 1,250.00 | 12 | 8 | 15,000 | 10,000 |
| **Total** | 146,250 | 168 | | 112 | 109 | 95,000 | 90,500 |

These are exactly the PV and EV figures `cost-management` reports in the month-3 snapshot.
The dollar-weighted SPI for the three packages is 0.95; the raw points ratio (109 ÷ 112) is
0.97 and overstates progress because reporting, the most expensive work per point, is the
furthest behind. An approved change re-baselines the planned points and the BAC together.
