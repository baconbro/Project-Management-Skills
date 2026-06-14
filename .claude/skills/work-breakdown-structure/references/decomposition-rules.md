# Decomposition Rules

A work breakdown structure (WBS) decomposes the total scope of a project into a
hierarchy of deliverables and the work packages that produce them. These rules keep
the decomposition complete, non-overlapping, and verifiable.

## The 100% rule
The WBS captures **100% of the scope** — all the work, and *only* the work, needed to
deliver the project. At every level, the children must add up to exactly their parent:
no more (no gold-plating, no out-of-scope work) and no less (no missing work). When
children carry numeric weights (percent of the parent's effort, cost, or value), those
weights must sum to 100 at each parent. `scripts/wbs_validate.py` enforces this.

## Mutually exclusive
Sibling elements must not overlap. A piece of work belongs to exactly one element. Overlap
causes double-counting in estimates and confusion over ownership. If two elements seem to
share work, the boundary is wrong — redraw it.

## The 8/80 rule
A work package — a leaf element — should be small enough to estimate, assign, and track,
but not so small that managing it costs more than doing it. A common heuristic is that a
work package takes between **8 and 80 hours** of effort (roughly one day to two weeks). If
a package is bigger than 80 hours, decompose it further; if many are under 8 hours, you
have decomposed too far.

## Deliverable- vs. phase-oriented
- **Deliverable-oriented:** the first level groups the *things produced* (e.g. Portal UI,
  Ticketing Service, Knowledge Base). Preferred — it ties the WBS to outcomes and the 100%
  rule is easy to check.
- **Phase-oriented:** the first level groups by *stage* (Design, Build, Test, Release).
  Useful for stage-gated delivery, but watch for the same deliverable reappearing across
  phases, which risks overlap.
Pick one organizing principle per level and stay consistent.

## Work package definition
A **work package** is the lowest element in the WBS — the unit that is estimated,
scheduled, assigned to one owner, and tracked to completion. A good work package has:
- a single accountable owner,
- a clear, verifiable completion criterion ("done" is unambiguous),
- an effort/cost estimate (it is the unit `estimation` and `project-schedule` consume),
- a deliverable or outcome, named with a noun, not a vague activity.

## What the WBS is not
The WBS lists *what* is produced, not *when* or *in what order* — sequencing and durations
belong to `project-schedule`. It is not an org chart and not a task list of every action.

## Common mistakes
- Breaking the 100% rule: missing work, or work that does not belong.
- Overlapping siblings, so effort is double-counted.
- Decomposing to actions ("write code") instead of deliverables ("authentication module").
- A parent with a single child — that is a rename, not a decomposition.
- Mixing deliverable and phase organization at the same level.
