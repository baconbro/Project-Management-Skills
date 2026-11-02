---
name: resource-management
description: >-
  Plans the team and its capacity: roles, staffing, onboarding, team charter, allocation
  against capacity, leveling and release (capacity_check.py flags over-allocation and
  proposes moves). Use when staffing a project, checking who is overloaded, or leveling
  workloads.
metadata:
  version: 1.0.0
  category: discipline
  phase: cross-cutting
  related: [project-planning, project-delivery, project-schedule, estimation, raci-matrix]
license: MIT
---

# Resource Management

## Overview
Resource management makes sure the right people, with the right skills, are on the project
when the work needs them, and that nobody carries more than they can deliver. It turns the
effort estimates and the schedule into demand by role and week, sets that against each
person's real capacity, levels the peaks, agrees how the team will work together, and
releases people cleanly at the end. Numbers here come from the sample Helios project (a
fictional customer self-service portal used throughout this catalog): six people over the
build peak, weeks 6–9, where the team as a whole sits at a comfortable 77.6% while the
backend engineer peaks at 125%.

## When to use this skill
- The user needs to staff a project: which roles, how many people, from where, from when.
- The user asks whether anyone is over- or under-allocated, wants utilization by week or
  sprint, or must level or smooth workloads before baselining.
- The user wants a team charter, working agreement or ways of working, or must onboard,
  develop or release team members.
- The user is in delivery and the plan has changed: someone left, a task slipped, a new
  project is competing for the same people.
- Do NOT use this to decide who is Responsible or Accountable for each work package — use
  `raci-matrix`; this skill checks that those people have the hours.
- Do NOT use this to move task dates or find float — use `project-schedule`; this skill
  tells you which weeks are overloaded and how much must move.
- Do NOT use this to size the work itself — use `estimation`; this skill consumes its effort.

## Methodology fit
- **Waterfall:** a resource plan by role and week for the whole project, built from the
  WBS effort and the dated schedule; `--fail-on over` gates the baseline; leveling can move
  the finish date, so it goes to the sponsor as a decision.
- **Agile:** a stable, long-lived team whose sprint capacity is set from availability (leave,
  BAU, ceremonies) before sprint planning; the allocation file uses sprints as periods and
  the working agreement replaces most of the charter; the team, not the PM, levels within a
  sprint by re-planning the sprint backlog.
- **Hybrid (Helios):** weekly periods for the build peak, roles fixed by the RACI, the
  identity/SSO integration scheduled as a network while the UI and knowledge base flex
  inside their float; the team charter carries the agile working agreements.

## Inputs you need
The work packages and their Responsible roles (`work-breakdown-structure`, `raci-matrix`),
effort per work package (`estimation`), the task dates and float (`project-schedule`), the
people available with their primary role, the roles they can cover, their capacity per week
or sprint net of leave, BAU and other projects, any named or contracted people, the planning
target (default 80%), and how people are acquired (line managers, vendors, contractors).

## Workflow
1. **Derive demand by role.** From the WBS and the RACI list which roles each work package
   needs, how much effort (from `estimation`) and in which weeks (from `project-schedule`).
   Note single-holder roles. Helios: one backend engineer (Carla Diaz) and one frontend
   engineer (Devin Patel), both covered by the tech lead Ben Adeyemi.
   *Done: every work package has a role, an effort figure and a date window.*
2. **Set capacity per person and period.** Pick the grain (weeks for waterfall and hybrid,
   sprints for agile), one unit for the file, and net capacity: leave, public holidays, BAU
   and other projects come off first (Helios: Frank Müller 24 h in W8, Ben 32 h in W9).
   Plan new joiners at about half capacity at first. *Done: one capacity per person and
   period, in one stated unit.*
3. **Acquire and onboard.** Agree each internal allocation with the line manager in writing,
   route external people through a statement of work, and run the onboarding checklist in
   `references/team-charter-and-ways-of-working.md`. *Done: every role in step 1 has a named
   person, a start and an end date.*
4. **Agree the team charter.** Workshop `assets/team-charter-template.md` with the team at
   kickoff: purpose, roles and cover, decision rights, core hours, meetings, communication
   norms, definition of done, conflict path and the capacity rules. *Done: the charter is
   signed by the team and stored with the plan.*
5. **Build the allocation file.** Copy `assets/resource-allocation-template.csv`; write one
   row per person, period and assignment (project or work package). The script sums a
   person's rows per period, so per-project exports work as they are; capacity must agree
   across a person's rows in a period. The filled Helios file is
   `assets/resource-allocation-sample.csv`. A JSON export is read with `--json`, an old
   non-UTF-8 Excel export with `--encoding cp1252`, and a file without a unit column takes
   `--unit hours|days|percent|fte`; files that mix units are refused. *Done: every
   assignment from step 1 is in the file and the unit is stated.*
6. **Run the capacity check.**
   ```bash
   python .claude/skills/resource-management/scripts/capacity_check.py .claude/skills/resource-management/assets/resource-allocation-sample.csv
   ```
   It prints each person's peak period with OVER (> `--threshold`, 100), HIGH (>= `--high`,
   90), OK or UNDER (< `--under`, 50), headroom to `--target` (80), a person × period matrix,
   team capacity and FTE load per period, where each overload comes from, and key-person
   risks. Helios: Carla is OVER in W6–W8 (peak 125.0% in W7: 30 h SSO + 20 h knowledge
   base), Devin in W7–W8 (105.0%), Ava Chen HIGH in W8 (95.0%), Elena Rossi UNDER (peak
   45.0%), yet team utilization is 77.6%: the average hides the overload. Use `--period W7`
   to focus on one week. *Done: every OVER and HIGH person-period is listed with its cause.*
7. **Level or smooth.**
   ```bash
   python .claude/skills/resource-management/scripts/capacity_check.py .claude/skills/resource-management/assets/resource-allocation-sample.csv --level
   ```
   The helper moves work, within each period, from OVER people down to the target onto
   people below it who hold the role or list it under skills (`--any-role` also allows
   other roles, marked cross-role), and reports what cannot be absorbed. Helios: 34 hours
   move (Carla → Ben, Devin → Elena), Devin is resolved, Carla keeps 6 hours above capacity
   in W7–W8, so smooth: move that knowledge-base work into W9–W10 within its 3 weeks of
   float in `project-schedule`. Follow the option order in `references/resource-capacity.md`
   and re-run after each change. *Done: no OVER remains, or the residual is a decision
   (scope, capacity or date) taken by the sponsor.*
8. **Gate the baseline and log the exposure.**
   ```bash
   python .claude/skills/resource-management/scripts/capacity_check.py .claude/skills/resource-management/assets/resource-allocation-sample.csv --fail-on over --format md
   ```
   Exit 1 while anyone is OVER in any period (`--fail-on high` also fails on HIGH). Hand the
   resource plan to `project-planning` and log every key-person line in `risk-register`
   (Helios: Carla's backend role has Ben as its only cover, and Ben is the lead engineer in
   R003, so the response is cross-training, not more hours on Ben).
   *Done: the gate passes and the key-person risks have owners and responses.*
9. **Monitor in delivery.** Re-run weekly on the forecast for the next 4–6 weeks; changes to
   allocations that move dates or cost go through change control in `project-delivery`; paste
   `--format md` output into the status report, or use `--format csv|json` for spreadsheets
   and dashboards. *Done: the forecast weeks are checked every week and overloads are
   raised before they happen.*
10. **Release people.** Plan each person's end week, complete knowledge transfer and the
    release checklist in the charter, set their later capacity to 0, and recognise the
    contribution at closure. *Done: nobody leaves with undocumented knowledge or open actions.*

## Quality checklist
- [ ] Every work package has a role, an effort figure and a date window; single-holder roles
      are listed with their cover.
- [ ] Capacity is net of leave, holidays, BAU and other projects, per person and period, in
      one unit stated in the file.
- [ ] The allocation file has a period column whose grain matches the plan (weeks or sprints).
- [ ] `capacity_check.py` runs without errors; no person is OVER in any period, or each
      residual is an explicit sponsor decision.
- [ ] Sustained utilization is planned near the target (80%); HIGH people have no new work.
- [ ] Every leveling move was confirmed with the people involved, and the schedule was re-run
      where work moved between weeks.
- [ ] Key-person risks are in the risk register with an owner and a cross-training response.
- [ ] The team charter is filled, signed by the team and has a review date.
- [ ] Every person has a start and an end date, and a release checklist exists.

## Anti-patterns
- Planning everyone at 100% (or "110% because they are committed").
- Checking one flat number per person per quarter, or the team total, so a one-week
  overload disappears.
- Mixing hours and percent, or gross hours against a focus-hour target.
- Leveling every overload onto the one generalist until they become the bottleneck.
- Acquiring whoever is free instead of the skills the work needs.
- A charter written by the PM alone and never reread.
- Releasing a specialist the week before the testing they are needed for.

## Resources
- `references/resource-capacity.md` — roles and cover, capacity and units, reading the
  check, the averaging trap, leveling versus smoothing, `--level`, gating; Helios W6–W9.
- `references/team-charter-and-ways-of-working.md` — acquiring, onboarding, the charter
  elements with a Helios example, team development, conflict modes, releasing people.
- `assets/resource-allocation-template.csv` — fill-in allocation file (`<placeholders>`):
  person, role, skills, period, project, capacity, allocated, unit.
- `assets/resource-allocation-sample.csv` — sample Helios allocation, six people, weeks
  6–9, one row per assignment; the default script input.
- `assets/team-charter-template.md` — fill-in team charter and working agreement.
- `scripts/capacity_check.py` — utilization per person and period with OVER/HIGH/OK/UNDER on
  the peak; `--threshold`, `--high`, `--under`, `--target`, `--unit`, `--period P`,
  `--level` with `--any-role`, `--fail-on over|high`, `--json` input, `--encoding`,
  `--format table|json|csv|md`. Run
  `python .claude/skills/resource-management/scripts/capacity_check.py --help`.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-planning` — receives the leveled resource plan and the passed capacity gate as
  part of the integrated baseline.
- `project-delivery` — runs the weekly re-check on the forecast and routes allocation changes
  that move dates or cost through change control.
- `project-schedule` — supplies the task dates and float that allocations follow, and takes
  back the work re-sequenced within float when leveling cannot absorb it.
- `estimation` — supplies the effort per work package that becomes demand by role and week.
- `raci-matrix` — supplies the Responsible roles behind the demand; this skill checks those
  people have the capacity, especially roles with a high R-share.
