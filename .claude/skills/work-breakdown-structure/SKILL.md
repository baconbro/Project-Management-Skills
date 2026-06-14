---
name: work-breakdown-structure
description: >-
  Decomposes project scope into a hierarchical work breakdown structure (WBS) of
  deliverables and verifiable work packages, applying the 100% rule, and validates
  the hierarchy and weights with the bundled wbs_validate.py helper. Use when the
  user wants to build a WBS, break scope into deliverables or work packages,
  organize and number the scope, check that the breakdown covers 100% of the work,
  or validate WBS weights and parent-child structure. Triggers: "work breakdown
  structure", "WBS", "decompose scope", "break down the project", "work packages",
  "100% rule", "deliverable breakdown". Works for waterfall, agile, and hybrid
  projects.
metadata:
  version: 1.0.0
  category: artifact
  phase: planning
  related: [project-planning, project-schedule, estimation, quality-management]
license: MIT
---

# Work Breakdown Structure

## Overview
A work breakdown structure decomposes the total scope of a project into a hierarchy of
deliverables, broken down to the level of **work packages** — the small, verifiable units
that get estimated, scheduled, assigned, and tracked. A good WBS captures 100% of the
work and only that work, giving every later plan (schedule, estimate, budget) a complete
and shared foundation.

## When to use this skill
- The user wants to build a WBS or break a project's scope into deliverables.
- The user wants to define work packages, number the scope, or check coverage.
- The user wants to validate a WBS hierarchy or its weights against the 100% rule.
- Do NOT use this to sequence the work or compute durations — use `project-schedule`.
- Do NOT use this to size the effort of each package — use `estimation`.

## Methodology fit
- **Waterfall:** a full deliverable-oriented WBS baselined before scheduling.
- **Agile:** the upper levels (epics/features) act as a lightweight WBS; work packages map
  to backlog items and are decomposed just-in-time.
- **Hybrid:** stable deliverables are decomposed up front; volatile areas stay coarse.

## Inputs you need
The agreed scope (from the charter or scope statement), the major deliverables, and an
organizing principle (deliverable- or phase-oriented). Optionally, a weight per element
(percent of its parent's effort, cost, or value) so the 100% rule can be checked numerically.

## Workflow
1. Choose an **organizing principle** and list the top-level elements. Prefer
   deliverable-oriented over phase-oriented (see `references/decomposition-rules.md`).
   *Done: the first level is consistent.*
2. **Decompose** each deliverable into children until every leaf is a work package small
   enough to estimate and track (the 8/80 rule). Keep siblings mutually exclusive.
   *Done: every leaf is a verifiable work package.*
3. Apply the **100% rule**: children must add up to exactly their parent — no missing work,
   no extra work. If you assign weights, they must sum to 100 at each parent.
4. Give each leaf a single **owner** and a verifiable **completion criterion**, and record
   everything in `assets/wbs-template.md`. *Done: each work package has an owner and a "done".*
5. Capture the same data in `assets/wbs.csv` (dotted ids, names, optional weights) and
   validate:
   ```bash
   python scripts/wbs_validate.py assets/wbs.csv
   ```
   The tool prints the WBS as a tree and a pass/fail report. Fix every ERROR (duplicate
   ids, orphans, weights not summing to 100) and review each warning. *Done: validator passes.*
6. Hand the work packages to `estimation` and `project-schedule` as the planning unit.

## Quality checklist
- [ ] One consistent organizing principle per level.
- [ ] 100% of scope covered — no missing and no out-of-scope work.
- [ ] Siblings are mutually exclusive (no overlapping work).
- [ ] Every leaf work package has an owner and a verifiable completion criterion.
- [ ] Work packages respect the 8/80 rule (small enough to track, large enough to matter).
- [ ] `scripts/wbs_validate.py` passes with no errors.

## Anti-patterns
- Breaking the 100% rule — missing work or work that does not belong.
- Decomposing into actions ("write code") instead of deliverables ("authentication module").
- A parent with a single child — a rename, not a decomposition.
- Overlapping siblings, which double-count effort downstream.
- Putting sequence or dates in the WBS — that belongs to `project-schedule`.

## Resources
- `references/decomposition-rules.md` — 100% rule, 8/80 rule, work-package definition, and
  deliverable- vs. phase-oriented decomposition.
- `assets/wbs-template.md` — fill-in WBS dictionary with owners and completion criteria.
- `assets/wbs.csv` — fill-in WBS rows; also the sample input for the validator.
- `scripts/wbs_validate.py` — validates hierarchy and the 100% rule. Run
  `python scripts/wbs_validate.py --help`.

## Related skills
- `project-planning` — the broader planning phase this WBS feeds.
- `project-schedule` — sequences the work packages and computes the critical path.
- `estimation` — sizes the effort, duration, and cost of each work package.
- `quality-management` — defines the acceptance criteria that make each package verifiable.
