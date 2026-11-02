# Resource capacity, utilization, leveling and smoothing

Load this to put people onto work without over- or under-loading them, and to read
`scripts/capacity_check.py`. Worked numbers come from the sample Helios project (a fictional
customer self-service portal used throughout this catalog): six people over the first four
build weeks, W6–W9, in `assets/resource-allocation-sample.csv`. W1 is the week of 2026-04-06,
so W6 starts on 2026-05-11 with sprint S1, when the four build tasks C, D, E and F of
`project-schedule` all begin.

## Before the numbers: roles, skills and cover
- Derive **demand by role** from the work packages (`work-breakdown-structure`) and the
  Responsible column of the RACI (`raci-matrix`): which roles, how many hours, in which weeks.
- Record each person's **primary role** and the other roles they can genuinely **cover**
  (the `skills` column). This is a minimal skills matrix: a role with one holder and no
  cover is a single point of failure whatever the utilization says.
- Helios: Carla Diaz is the only backend engineer and Devin Patel the only frontend
  engineer; Ben Adeyemi (tech lead) covers both, Elena Rossi (UX) can cover frontend work.

## Capacity, allocation, utilization
- **Capacity** = what a person can give the project in the period, **net** of leave, public
  holidays, business-as-usual duties and other projects. A full-time week is rarely 40
  productive project hours: decide whether the file holds gross hours (and keep the target
  near 80%) or focus hours (about 6 a day, and accept a higher target).
- **Allocated** = work assigned in the period, from effort estimates (`estimation`) spread
  over the task dates (`project-schedule`), in the **same unit** as capacity.
- **Utilization** = allocated / capacity. **FTE load** = the sum of allocated / capacity
  across people: "this week holds the work of 4.95 full-timers". It stays meaningful even
  when capacities differ.
- Capacity 0 is a leave period: `OFF` when nothing is allocated, `OVER` when work is.

## Shape the file so peaks are visible
- One row per **person × period × assignment**; the script sums allocations per person and
  period and insists that capacity agrees across a person's rows in the same period.
- Choose the grain that matches the plan: weeks for a waterfall or hybrid schedule, sprints
  for agile teams. A single row per person over a quarter is only acceptable for a short,
  flat period: averaging hides the week that breaks.
- One unit for the whole file. A `unit` column (hours, days, percent, fte) makes it explicit;
  the script refuses files that mix units because team totals would add hours to percent.

## Reading the check
```bash
python .claude/skills/resource-management/scripts/capacity_check.py .claude/skills/resource-management/assets/resource-allocation-sample.csv
```
| Band | Default | Meaning | Action |
|---|---|---|---|
| OVER | > 100% | the plan is not deliverable as drawn | level before baselining |
| HIGH | >= 90% | deliverable only if nothing goes wrong | watch; no new work |
| OK | 50–89.9% | healthy; ~80% is the target | none |
| UNDER | < 50% | spare capacity, or a part-timer by design | redirect or confirm |

- Each person's flag is their **peak period**, not their average. The matrix shows every
  period; the team table gives capacity, allocation, headroom and FTE load per period.
- **Where the OVER load comes from** lists the assignments behind each overload: the input
  to the leveling conversation.
- **Key-person risk** names an OVER person whose role nobody else holds; log it in
  `risk-register` and name the backup.

**The averaging trap, in Helios numbers.** Team utilization over the four weeks is 77.6%,
comfortably under the 80% target, yet five person-periods are OVER. Carla Diaz peaks at
125.0% in W7 (50 h: 30 SSO + 20 knowledge base). Devin Patel averages 97.5% over the four
weeks (156 of 160 h, HIGH) while he is at 105.0% in both W7 and W8: one row per person
would have hidden his overload entirely.

## Leveling versus smoothing
- **Resource smoothing** moves work only within its float, so the finish date holds; it
  removes peaks only where float exists.
- **Resource leveling** resolves over-allocation even when that delays the critical path;
  the end date can move, so it needs the sponsor's agreement and a re-run of the schedule.
- Try, in order: (1) reassign to someone with spare capacity who holds or covers the role;
  (2) re-sequence within float (smoothing); (3) split or reduce scope for the period;
  (4) add capacity (overtime briefly, a contractor, a borrowed specialist); (5) extend the
  date (leveling proper). Re-run the check after every change.

## The leveling helper (`--level`)
```bash
python .claude/skills/resource-management/scripts/capacity_check.py .claude/skills/resource-management/assets/resource-allocation-sample.csv --level
```
Within each period every OVER person is brought down to the `--target` (80%) and people
below it are filled up to it, best match first: same role, then a role listed under skills,
then (only with `--any-role`) anyone, marked cross-role. Helios: 34 hours move (Carla → Ben
6/6/2 in W6–W8, Devin → Elena 10/10 in W7–W8); Devin is resolved; Carla keeps a residual of
30 hours above the target, 6 of them above capacity (4 in W7, 2 in W8). Same-period
reassignment cannot fix that, so smoothing does: the knowledge base (schedule task E) runs
W6–W14 with 1 week of total float, so move 6 hours of its backend work into W9–W10, inside
its own window, and re-run for those weeks; no date in `project-schedule` moves.

Read the plan as a proposal: all of Carla's moves land on Ben, who is also the lead
engineer behind R003 (lead engineer leaves) and the only cover for both engineers. Leveling
concentrates key-person exposure; update the risk response, not just the spreadsheet.

## Gate and monitor
- Before baselining: `--fail-on over` exits 1 while anyone is OVER in any period; use
  `--fail-on high` for teams that must protect slack (on-call, regulated releases).
- In delivery: re-run weekly on the forecast for the next 4–6 weeks; export with
  `--format md` for the status report or `--format csv` for a spreadsheet.

## Anti-patterns
- Planning everyone at 100% and calling it efficient; the first sick day breaks the plan.
- Averaging a quarter, or the whole team, so a one-week overload disappears.
- Mixing hours and percent in one file, or entering gross hours against a focus-hour target.
- Leveling onto the one generalist until they become the bottleneck and the key-person risk.
- Treating UNDER as idle without checking part-time agreements and BAU duties.
