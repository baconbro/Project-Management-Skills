---
name: project-schedule
description: >-
  Builds and analyzes a project schedule from task durations and finish-to-start
  dependencies, computing early/late dates, slack, the critical path, and total
  project duration with the bundled critical_path.py helper. Use when the user
  wants to build a schedule or timeline, sequence tasks, find the critical path
  or float, work out how long a project will take, or see which tasks drive the
  deadline. Triggers: "project schedule", "timeline", "critical path", "CPM",
  "slack", "float", "task dependencies", "how long will it take", "Gantt logic".
  Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: artifact
  phase: planning
  related: [project-planning, work-breakdown-structure, estimation]
license: MIT
---

# Project Schedule

## Overview
A schedule turns a list of tasks, their durations, and the dependencies between them into
a timeline. The critical path method (CPM) finds the longest chain of dependent tasks —
the **critical path** — whose length is the shortest possible project duration, and tells
you how much **slack** every other task has before it too delays the project.

## When to use this skill
- The user wants to build a schedule or timeline, or sequence tasks.
- The user wants the critical path, slack/float, or the total project duration.
- The user wants to know which tasks drive the deadline.
- Do NOT use this to break scope into work packages — use `work-breakdown-structure` first.
- Do NOT use this to size individual task durations — use `estimation`.

## Methodology fit
- **Waterfall:** a full network schedule with a baselined critical path and milestones.
- **Agile:** less central — use it for release-level planning and cross-team dependencies;
  iteration content is managed on the backlog, not a Gantt chart.
- **Hybrid:** schedule the fixed milestones and dependencies; leave iteration internals flexible.

## Inputs you need
A list of tasks (ideally the work packages from the WBS), a duration for each, and the
finish-to-start dependencies between them. Durations come from `estimation`. For non-FS
relationships or lead/lag, see `references/dependency-types.md`.

## Workflow
1. List the tasks — typically the work packages from `work-breakdown-structure` — and give
   each a unique id. *Done: every task has an id.*
2. Assign a **duration** to each task (from `estimation`) and record its **predecessors**
   (finish-to-start). Keep the dependency logic explicit. *Done: durations and links set.*
3. Choose the right **dependency type** for each link using `references/dependency-types.md`,
   and decide whether it is mandatory or discretionary. *Done: each link is justified.*
4. Record the network in `assets/schedule-template.csv` (columns `id,name,duration,predecessors`),
   then compute the schedule:
   ```bash
   python scripts/critical_path.py assets/schedule-template.csv
   ```
   The tool runs the forward and backward passes and prints ES/EF/LS/LF/slack per task,
   the critical path, and the total project duration. *Done: critical path and duration known.*
5. If the duration is too long, compress a **critical** task — crash it (add resources) or
   fast-track it (overlap by relaxing a discretionary dependency). Re-run and re-check.
   *Done: schedule meets the target or the constraint is documented.*
6. Protect the critical path and watch tasks with little slack; baseline the schedule.

## Quality checklist
- [ ] Every task has an id, a duration, and explicit predecessors.
- [ ] Dependency types are chosen deliberately (not all FS by default where work overlaps).
- [ ] The critical path and total project duration are computed, not guessed.
- [ ] Compression targets a critical task; non-critical changes only consume slack.
- [ ] No cycles and no references to unknown predecessors (the tool errors on both).

## Anti-patterns
- Padding every task instead of managing a single, visible schedule reserve.
- Crashing or fast-tracking a non-critical task and expecting the deadline to move.
- Hiding lag inside task durations so the schedule logic is opaque.
- Building a schedule before the scope (WBS) and durations (estimates) exist.

## Resources
- `references/dependency-types.md` — FS/SS/FF/SF, lead/lag, and mandatory vs. discretionary links.
- `assets/schedule-template.csv` — fill-in task network; also the sample input for the script.
- `scripts/critical_path.py` — computes ES/EF/LS/LF, slack, critical path, and duration. Run
  `python scripts/critical_path.py --help`.

## Related skills
- `project-planning` — the broader planning phase this schedule belongs to.
- `work-breakdown-structure` — supplies the tasks (work packages) this schedule sequences.
- `estimation` — supplies the task durations this schedule consumes.
