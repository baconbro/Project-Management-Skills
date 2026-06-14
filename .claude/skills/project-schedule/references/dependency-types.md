# Dependency Types

A schedule's logic is the set of dependencies between tasks. Getting the dependency
*type*, *lead/lag*, and *category* right is what makes the critical path meaningful.

## The four logical relationships
Each dependency links a predecessor to a successor. The two letters name which end of
each task is tied:

- **Finish-to-Start (FS):** the successor cannot start until the predecessor finishes.
  The default and by far the most common (e.g. "build" finishes before "test" starts).
  `scripts/critical_path.py` models FS dependencies.
- **Start-to-Start (SS):** the successor cannot start until the predecessor starts. Used
  for overlapping work (e.g. start "write content" once "design pages" has started).
- **Finish-to-Finish (FF):** the successor cannot finish until the predecessor finishes
  (e.g. "testing" cannot finish before "development" finishes).
- **Start-to-Finish (SF):** the successor cannot finish until the predecessor starts. Rare;
  used mostly for shift hand-overs.

## Lead and lag
- **Lag** is a deliberate *delay* on a dependency: "start UAT 2 days after build finishes"
  is FS + 2 days lag. Lag stretches the schedule.
- **Lead** is *overlap* (negative lag): "start testing 3 days before build finishes" is
  FS − 3 days lead. Lead compresses the schedule (a form of fast-tracking).

The critical path tool assumes zero lead/lag (pure FS). Bake any intended lag into task
durations or model it as a separate task if you need it reflected in the math.

## Mandatory vs. discretionary dependencies
- **Mandatory (hard logic):** inherent in the work — you cannot test code before it is
  written, cannot pour a foundation before digging. These cannot be reordered.
- **Discretionary (soft logic):** a preferred sequence the team chose, not a physical
  necessity (e.g. "do module A before module B" because the team knows A better). These
  *can* be re-sequenced to compress the schedule, and are the first place to look when
  fast-tracking.
- **External dependencies:** outside the project's control (a vendor delivery, a regulatory
  approval). Track them as risks as well as schedule links.

## Why the distinction matters
The critical path is the longest chain of dependent tasks; its length is the shortest
possible project duration. To shorten the project you must shorten a *critical* task —
either crash it (add resources) or fast-track it (overlap tasks by relaxing discretionary
dependencies or adding leads). Touching a non-critical task only consumes its slack.

## Common mistakes
- Modeling everything as FS when work genuinely overlaps (SS/FF), inflating the duration.
- Hiding lag inside FS links so the schedule logic is opaque.
- Treating discretionary links as mandatory, so the schedule looks impossible to compress.
- Ignoring external dependencies until they slip.
