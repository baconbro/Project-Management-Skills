---
name: project-schedule
description: >-
  Builds and analyzes a schedule from durations and dependencies: critical path, float,
  calendar dates, a text Gantt, schedule-risk simulation and compression
  (critical_path.py). Use when building a timeline, finding the critical path, or asking
  how long the project will take or what drives the finish date.
metadata:
  version: 1.1.0
  category: artifact
  phase: planning
  related: [project-planning, work-breakdown-structure, estimation, resource-management]
license: MIT
---

# Project Schedule

## Overview
A schedule turns the list of tasks, their elapsed durations and the dependencies between
them into a timeline. The critical path method (CPM) runs a forward pass (earliest start and
finish), a backward pass (latest start and finish) and derives float: the **critical path**
is the longest chain of dependent tasks, its tasks have zero float, and its length is the
shortest possible project duration. This skill builds that network, turns it into dated
milestones, checks it against the people available, compresses it when the finish date is
too late, and quantifies schedule risk. The worked numbers come from the sample Helios project
(a fictional customer self-service portal used throughout this catalog): ten tasks (every WBS
work package except level-of-effort project management), finish-to-start links, a 25-week
critical path dated from Monday 2026-04-06.

## When to use this skill
- The user wants to build a schedule or timeline, or sequence tasks and milestones.
- The user wants the critical path, total/free float, the project duration, or to know which
  tasks drive the finish date.
- The user wants calendar dates for milestones, a check against an imposed deadline, or to
  crash / fast-track a schedule.
- The user wants schedule risk: P50/P80/P90 finish, a criticality index, a schedule reserve.
- Do NOT use this to break scope into work packages — use `work-breakdown-structure` first.
- Do NOT use this to size individual task durations — use `estimation`; this skill consumes
  its most-likely and three-point durations.
- Do NOT use this to check or level people's workload — use `resource-management`; this
  skill only shows which tasks can move (their float).

## Methodology fit
- **Waterfall:** a full network from the WBS work packages, baselined with dated milestones
  and a visible schedule reserve; total and free float reviewed weekly; compression by
  crashing or fast-tracking before any scope is cut.
- **Agile:** release-level only — milestones, cross-team and external dependencies, and
  fixed-date events (pilot, general availability) form the network; sprint content stays on
  the backlog and is never a task row.
- **Hybrid (Helios):** the contracted identity/SSO integration, testing and launch gates are
  scheduled as a network; the self-service UI and knowledge-base work appear as single tasks
  whose durations come from the team's throughput; schedule risk is held at project level,
  never padded into tasks.

## Inputs you need
The tasks (work packages from `work-breakdown-structure`, plus milestones and external
deliveries), one elapsed duration per task in a single unit — from `estimation`'s duration
worksheet, most-likely for the baseline and optimistic/most-likely/pessimistic for the risk
run — the finish-to-start predecessors, whether each link is mandatory, discretionary or
external, the start date and working calendar (holidays), any imposed dates, and the people
assigned (for the capacity check in `resource-management`).

## Workflow
1. **List tasks and milestones.** One row per work package from `work-breakdown-structure`,
   plus zero-duration milestones (kickoff, "MVP live to pilot", "General availability") and
   each external delivery the work waits on. Give every row a unique id — Helios uses A–J;
   WBS ids such as 1.3.1 also work; ids with spaces must then be separated by `;` in the
   predecessor cells. *Done: every work package, milestone and external delivery has an id.*
2. **Set durations in one unit.** Durations are elapsed time (weeks for Helios), never
   effort: 40 hours of effort shared by two people is 2.5 days of duration. Take the
   most-likely duration from `estimation` (`.claude/skills/estimation/assets/duration-worksheet-sample.csv`)
   and carry its optimistic/most-likely/pessimistic values for step 7; a duration of 0 marks a
   milestone. *Done: every task has one elapsed duration in the stated unit; milestones are 0.*
3. **Link the network finish-to-start.** Record predecessors as ids separated by `;`. The
   helper models finish-to-start links with zero lag; express lag, lead and SS/FF/SF overlaps
   as explicit lag or milestone tasks using `references/dependency-types.md`, never by
   changing a work task's duration. Classify each link mandatory / discretionary / external:
   discretionary links are the fast-tracking candidates, external ones also go to the risk
   register. *Done: every link is FS, justified and classified.*
4. **Compute the critical path.** Copy `assets/schedule-template.csv`, fill it (the filled
   Helios version is `assets/schedule-sample.csv`), and run:
   ```bash
   python .claude/skills/project-schedule/scripts/critical_path.py .claude/skills/project-schedule/assets/schedule-sample.csv --unit weeks --near-critical 1
   ```
   Per task it prints ES/EF/LS/LF, total float (TF, shared along the chain), free float (FF,
   usable without delaying any successor) and the critical flag, then every critical path,
   the tasks common to all of them, and the duration. Helios: A → B → D → G → H → J =
   25 weeks; C *Identity / SSO integration*, E *Knowledge base*, F *Reporting & analytics*
   and I *Training & communications* each have 1 week of float, so all four are
   near-critical. When two or more paths are critical the tool says so —
   only a task on every one of them can shorten the project. *Done: critical path(s), float
   per task and the project duration are computed, not guessed.*
5. **Make it a calendar and check it.** State the start date and working calendar, then
   re-run with dates and a Gantt:
   ```bash
   python .claude/skills/project-schedule/scripts/critical_path.py .claude/skills/project-schedule/assets/schedule-sample.csv --unit weeks --start-date 2026-04-06 --workdays --gantt
   ```
   `--workdays` counts Monday–Friday (one week = 5 working days) and, with
   `--holidays <your-holidays.txt>` (one YYYY-MM-DD per line, `#` comments allowed), skips
   those dates; without `--workdays`, units map to calendar days. Helios: B ends Friday
   2026-05-08 (M1 *Discovery complete*), C–F start 2026-05-11 with sprint S1, G runs
   2026-07-20 to 08-14 and holds the pilot launch (M4, Friday 2026-08-07), and J ends Friday
   2026-09-25, leaving only the cutover week before general availability (M6, Saturday
   2026-10-03). Compare every milestone's date with its imposed date, and use `--target N`
   for a must-finish duration: a miss means negative float, which only step 6 or a
   scope/date decision can remove. Then run the capacity check
   (`python .claude/skills/resource-management/scripts/capacity_check.py` on the assignments)
   and, where someone is over-allocated, move tasks within their free float first, then their
   total float, and re-run; if the float is not enough, the schedule lengthens — better to
   know now than after baselining. *Done: dated schedule with milestones, every imposed date
   met or escalated, no one over-allocated.*
6. **Compress only if the date is missed.** Follow `references/schedule-compression.md`:
   crash the critical task with the cheapest cost slope, or fast-track a discretionary link
   on the critical path (encode the overlap as a split task and log the rework risk).
   Re-run after every change and watch `--near-critical`: the Helios worked example goes
   from 25 to 22 weeks by crashing B, G and H, the cheapest critical slope each time, for an
   illustrative $24,000 and ends with two critical paths, the signal to stop. *Done: the
   target is met with the cost and risk recorded, or the constraint is escalated to the
   sponsor.*
7. **Quantify schedule risk and size the reserve.** With the three-point columns filled:
   ```bash
   python .claude/skills/project-schedule/scripts/critical_path.py .claude/skills/project-schedule/assets/schedule-sample.csv --unit weeks --simulate 10000 --seed 42 --target 26
   ```
   Each trial draws every task from its PERT-Beta (`--dist triangular` for a triangular)
   distribution and recomputes the critical path. Helios: P50 ≈ 26.9, P80 ≈ 28.2, P90 ≈ 29.0
   weeks; only 10% of futures finish within the deterministic 25 and 27% by week 26, the
   cutover week. The criticality index (CI%) shows A, B, G and J critical in every trial, H
   in 90%, D in 52%, C in 25%, E 12%, F 11% and I 10%: four parallel build tasks of similar
   length take turns driving the finish (merge bias), so the deterministic date is
   optimistic. Reserve at P80 ≈ 28.2 − 25 ≈ 3.2 weeks, held once and visibly, not spread
   into tasks. Helios has no room for it before GA: the sponsor accepted the 27% at baseline,
   with the 2-week M6 tolerance (to 2026-10-17) covering about P75 and a crash of H ready.
   *Done: commit level, reserve or accepted risk, and watch-list are written down.*
8. **Baseline and hand off.** Freeze the dated schedule as the schedule baseline in
   `project-planning`; export it with `--format csv` (one row per task with dates and float)
   or `--format md` for the plan and status reporting. During delivery re-run with actual
   durations: a slip inside a task's free float affects no one, inside its total float it
   consumes float shared with successors, beyond it the finish date moves. Helios: "SSO
   working in test" slipped 2 weeks (forecast 2026-07-17), pushing C to finish 2026-07-24,
   one week past its late finish, so G and M4 would move a week; running the real-provider
   retest and UAT preparation in parallel in sprint S6 (fast-tracking) absorbed it and M4
   held on 2026-08-07. *Done: baseline stored, export shared, re-run cadence agreed.*

## Quality checklist
- [ ] Every work package and milestone has a unique id, one elapsed duration in the stated
      unit (0 for milestones) and explicit finish-to-start predecessors.
- [ ] No lag, lead or overlap is hidden inside a duration; every non-FS relationship is an
      explicit lag or milestone task and the conversion is noted.
- [ ] Each link is classified mandatory / discretionary / external; external ones are also
      in the risk register.
- [ ] Critical path(s), total and free float, and the duration come from the tool; multiple
      critical paths are acknowledged in the compression plan.
- [ ] Start date, working calendar and holidays are stated; milestone dates are checked
      against imposed dates.
- [ ] Capacity was checked with `resource-management` and nobody is over-allocated after
      leveling within float.
- [ ] Compression touched only tasks on every critical path, with cost and rework risk
      recorded.
- [ ] The schedule reserve is sized from the simulation (or PERT) and held once, visibly.
- [ ] The dated baseline is frozen and exported; the re-run cadence is agreed.

## Anti-patterns
- Padding every task instead of managing one visible schedule reserve.
- Folding lag or overlap into durations so the logic is opaque and the estimate no longer
  matches the duration.
- Crashing a task on one critical path while a parallel path is equally long, then expecting
  the finish date to move.
- Reading total float as free float and letting one slip push the whole chain.
- Treating effort as duration (the tool rejects an `effort` column for this reason).
- Scheduling before the WBS and estimates exist, or baselining before the capacity check.
- Leaving the schedule in abstract units and never mapping it to dates a sponsor can read.

## Resources
- `references/dependency-types.md` — FS/SS/FF/SF, lead/lag, mandatory vs. discretionary vs.
  external links, and the table for encoding each as explicit FS tasks for the tool.
- `references/schedule-compression.md` — crashing by cost slope, fast-tracking, multiple
  critical paths, schedule reserve, resource leveling; Helios worked example 25 → 22 weeks.
- `assets/schedule-template.csv` — fill-in network (`<placeholders>`): id, name, duration,
  predecessors, optional optimistic/most_likely/pessimistic.
- `assets/schedule-sample.csv` — sample Helios network: ten tasks in weeks with three-point
  durations; the default script input.
- `scripts/critical_path.py` — ES/EF/LS/LF, total and free float, every critical path;
  `--unit`, `--near-critical N`, `--target T`, `--start-date` with `--workdays` and
  `--holidays FILE`, `--gantt`, `--simulate N --seed K --dist pert|triangular`, `--json`
  input, `--format table|json|csv|md`. Run
  `python .claude/skills/project-schedule/scripts/critical_path.py --help`.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-planning` — the planning phase that commissions this schedule and freezes it as
  the schedule baseline.
- `work-breakdown-structure` — supplies the work packages (and their ids) this network
  sequences.
- `estimation` — supplies the per-task durations and the three-point values the simulation
  draws from.
- `resource-management` — checks and levels the people assigned to these tasks before the
  schedule is baselined.
