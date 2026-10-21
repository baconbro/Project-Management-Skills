# Resource capacity, utilization, and leveling

Load this to plan people onto work without over- or under-loading them. Use it alongside
`capacity_check.py`, which reads `assets/resource-allocation.csv` and flags over- and
under-allocated people. Examples use the running sample project: **Helios**, a customer
self-service portal.

## Core idea
- **Capacity** — how much a person can do in a period (e.g. 40 hours/week, or 100%).
- **Allocated** — how much work is assigned to them in that period, in the same unit.
- **Utilization** = allocated / capacity, as a percentage.
  - Over 100% = over-allocated; the plan is not deliverable as drawn.
  - Under ~50% = under-utilized; capacity is being wasted (or the person is a part-time
    specialist by design).

Keep capacity and allocation in **the same unit** — both hours-per-week, or both percent.
Mixing units makes utilization meaningless.

## Reading the capacity check
Run the helper and read the table sorted by utilization:
```bash
python scripts/capacity_check.py assets/resource-allocation.csv
python scripts/capacity_check.py assets/resource-allocation.csv --threshold 90 --under 40
```
- `OVER` rows are the priority — those people cannot deliver everything assigned.
- `UNDER` rows are spare capacity you can redirect.
- The totals (capacity vs. allocated) tell you if the whole team is over-committed even
  when individuals look fine.

## Leveling — fixing over-allocation
When the check flags `OVER`, level the plan with one or more of:
1. **Reassign** work to an `UNDER`-utilized person with the right skills.
2. **Re-sequence** so two heavy tasks for one person do not overlap (see `project-schedule`).
3. **Reduce scope** for the period (defer lower-priority work packages).
4. **Add capacity** (more people or hours) — usually the most expensive option.
5. **Extend the date** if the constraint allows.

Re-run the check after each change until no unresolved `OVER` remains.

## Practical guidance
- Plan to less than 100% sustained utilization; people need slack for meetings,
  context-switching, and the unexpected. ~80% allocated is healthier than 100%.
- Watch **key-person dependencies**: one person at 130% who is the only one who can do a
  task is a schedule risk — log it via `risk-management`.
- Account for non-project time (support, leave, holidays) when setting capacity.
- Confirm responsibilities match allocations using `raci-matrix` — the person doing the
  work should be the Responsible party.

## Anti-patterns
- Planning everyone at exactly 100% and assuming nothing will go wrong.
- Hiding over-allocation by averaging across a quarter when the overload is in one week.
- Mixing hours and percent in the same file so utilization is nonsense.
