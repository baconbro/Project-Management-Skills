---
name: raci-matrix
description: >-
  Builds and validates a RACI responsibility assignment matrix that maps every
  activity to roles as Responsible, Accountable, Consulted, or Informed, using
  the bundled raci_validate.py helper to catch missing or duplicate
  accountability. Use when the user wants to create, review, or fix a RACI (or
  RASCI/DACI) matrix, clarify who does what, assign responsibility for tasks, or
  resolve confusion over ownership and decision rights. Triggers: "RACI",
  "RASCI", "DACI", "responsibility matrix", "responsibility assignment",
  "who does what", "accountability matrix", "roles and responsibilities". For
  the people behind the roles and their engagement, use stakeholder-management.
  Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: artifact
  phase: planning
  related: [stakeholder-management, project-planning]
license: MIT
---

# RACI Matrix

## Overview
A RACI matrix is a grid that assigns, for every activity, exactly one person who is
**Accountable** and at least one who is **Responsible**, plus anyone **Consulted** or
**Informed**. It turns vague "we own this together" agreements into unambiguous
ownership so nothing falls between the cracks and no two people think the other has it.

## When to use this skill
- The user wants to create, review, or repair a RACI / RASCI / DACI matrix.
- Ownership of tasks, deliverables, or decisions is unclear or contested.
- A plan exists but it is not obvious who decides, does, or is merely informed.
- Do NOT use this to analyze the stakeholders themselves (influence, interest,
  engagement) — use `stakeholder-management`.
- Do NOT use this to build the schedule or task list being assigned — use
  `project-planning`.

## Methodology fit
- **Waterfall:** a formal matrix covering plan activities and deliverables, signed off.
- **Agile:** lighter — team roles plus a RACI for cross-team or governance touchpoints
  (releases, security sign-off) rather than every backlog item.
- **Hybrid:** RACI for governance and external interfaces; the team self-organizes inside.

## Inputs you need
The list of activities or deliverables (from the plan or WBS) and the roles or named
people involved. If you do not yet have an activity list, build it in `project-planning`
first, then assign responsibility here.

## Workflow
1. List the **activities** as rows and the **roles** as columns. Open
   `assets/raci-template.csv`: the first column is the activity, every other column is a
   role. *Done: every plan activity appears exactly once as a row.*
2. Fill each cell with **R, A, C, I**, a combo like `A/R`, or blank. Apply the rules in
   `references/raci-rules.md`: exactly one **A** per activity, at least one **R**, and
   keep Consulted/Informed lean. *Done: no cell is ambiguous.*
3. Validate the matrix:
   ```bash
   python scripts/raci_validate.py assets/raci-template.csv
   ```
   The tool prints the matrix, then flags missing accountability, multiple accountables,
   missing responsibility, too many C/I, and roles overloaded with A. *Done: it reports
   PASS, or you fix every ERROR.*
4. Resolve each finding: split or merge an A so there is exactly one, add an R where work
   has no doer, and demote excess Consulted to Informed. Re-run until it passes.
5. Review the matrix with the named people so they accept their assignments, then baseline
   it alongside the plan. *Done: every A and R has agreed to it.*

## Quality checklist
- [ ] Every activity has exactly one Accountable and at least one Responsible.
- [ ] No activity is over-Consulted (decision-by-committee) — C/I kept lean.
- [ ] No single role is Accountable for an unreasonable share of activities.
- [ ] `raci_validate.py` reports PASS with no ERRORs.
- [ ] The named people have seen and accepted their assignments.

## Anti-patterns
- More than one A on an activity — accountability you cannot pin down is no accountability.
- An activity with R's but no A, or an A with no R doing the actual work.
- Marking everyone Consulted, which stalls every decision in a committee.
- One hero role Accountable for everything — a bottleneck and a single point of failure.

## Resources
- `references/raci-rules.md` — definitions of R/A/C/I, the validation rules, and RASCI/DACI variants.
- `assets/raci-template.csv` — fill-in matrix; also the sample input for the script.
- `scripts/raci_validate.py` — validates the matrix. Run `python scripts/raci_validate.py --help`.

## Related skills
- `stakeholder-management` — the people behind the roles, and how engaged each one is.
- `project-planning` — produces the activity list that becomes the rows of this matrix.
