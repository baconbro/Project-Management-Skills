# RACI Rules

RACI assigns, for every activity, a clear role to each person or team. The letters:

| Letter | Role | Meaning |
| --- | --- | --- |
| **R** | Responsible | Does the work. There can be several. At least one is required. |
| **A** | Accountable | Owns the outcome and signs it off. **Exactly one** per activity. |
| **C** | Consulted | Gives input before the work is done — two-way dialogue. |
| **I** | Informed | Told about progress or the result after the fact — one-way. |

A person can hold more than one letter on an activity. The most common combo is `A/R`
(also written `AR`): the same person both owns the outcome and does the work. The
validator accepts `R`, `A`, `C`, `I`, blanks, and combos joined by `/`, space, or nothing.

## The core rules the validator enforces

1. **Exactly one Accountable per activity.**
   - Zero A's is an ERROR ("no accountability"): if no one owns the outcome, it drifts.
   - More than one A is an ERROR ("multiple accountable"): shared accountability means
     each person assumes the other has it, and nobody does.
2. **At least one Responsible per activity.** An activity with an A but no R has an owner
   and no doer — the work will not happen. This is an ERROR ("no responsible").
3. **Keep Consulted and Informed lean.** When more than four roles are C or I on a single
   activity, the validator WARNs ("too many cooks"): every consult adds a round trip, and
   decision-by-committee is the most common way a RACI grinds a project to a halt.
4. **Watch for an overloaded Accountable.** If one role is Accountable for more than half
   of all activities, the validator WARNs ("overloaded"): that role is a bottleneck and a
   single point of failure. Distribute accountability.

## Good practice

- Derive rows from the plan or WBS so every real activity is covered exactly once.
- Assign A first (one owner), then R (the doers), then trim C and I to who truly needs them.
- Prefer Informed over Consulted unless that role genuinely changes the decision.
- Review with the named people; an assignment nobody accepted is not real.

## Variants: RASCI and DACI

- **RASCI** adds **S = Support** — provides resources or help to the Responsible party,
  distinct from doing the work (R) or advising (C). Use it when a supporting team
  (e.g. infrastructure) materially assists but does not own the task.
- **DACI** is a decision-focused model: **Driver** (moves it forward), **Approver** (the
  single decision-maker, analogous to A), **Contributors** (like C), **Informed**. Prefer
  DACI for one-off decisions rather than ongoing delivery activities.

Stick to plain RACI unless the project genuinely needs the extra column — every added
letter is another judgment call per cell and another way to get the matrix wrong.
