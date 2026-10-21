---
name: work-breakdown-structure
description: >-
  Decomposes project scope into a hierarchical work breakdown structure (WBS) of
  deliverables and verifiable work packages, applies the 100% rule, records the WBS
  dictionary (owner, acceptance criterion, control account) once in a CSV, and with
  the bundled wbs_validate.py helper validates hierarchy and weights, suggests
  corrected weights, rolls weights up to each element's share of the project and
  budget, and exports the work packages for estimation. Use when the user wants to
  build a WBS, break scope into deliverables or work packages, check that the
  breakdown covers 100% of the work, validate weights and parent-child structure,
  write a WBS dictionary, or allocate a budget by WBS weight. Triggers: "work
  breakdown structure", "WBS", "WBS dictionary",
  "decompose scope", "break down the project", "work packages", "100% rule",
  "deliverable breakdown", "control account". For sequencing the work packages into
  a timeline, use project-schedule. Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.1.0
  category: artifact
  phase: planning
  related: [project-planning, quality-management, project-schedule, estimation, raci-matrix, scope-and-requirements]
license: MIT
---

# Work Breakdown Structure

## Overview
A work breakdown structure (WBS) decomposes the total scope of a project into a hierarchy
of deliverables, down to **work packages** — the smallest elements that are estimated,
scheduled, assigned, and tracked. Every later plan (estimate, schedule, budget, RACI,
acceptance criteria) hangs off it, so the WBS must obey the **100% rule**: all the work and
only the work, at every level. This skill builds the hierarchy, weights it, records the WBS
dictionary once, and validates it with `scripts/wbs_validate.py`, which also rolls the
weights up to each element's share of the project and of the budget, tables the control
accounts, suggests corrected weights, and exports the work packages for `estimation`. The
worked example is the sample Helios project (a fictional customer self-service portal used
throughout this catalog): 16 elements, 11 work packages, and a $500,000 budget allocated
by weight.

## When to use this skill
- The user wants to build a WBS, break a project into deliverables, or define and number
  work packages.
- The user wants to check that a breakdown covers 100% of the scope, or to validate WBS
  ids, parent-child structure, and weights.
- The user wants a WBS dictionary (owner, description, acceptance criterion, control
  account per element) or wants to allocate a budget by WBS weight.
- Do NOT use this to write the scope statement or elicit requirements — use
  `scope-and-requirements`; the WBS decomposes a scope that already exists.
- Do NOT use this to sequence the work or compute durations and the critical path — use
  `project-schedule`.
- Do NOT use this to size the effort or cost of each work package — use `estimation`.
- Do NOT use this to assign Responsible and Accountable roles — use `raci-matrix`.

## Methodology fit
- **Waterfall:** a full deliverable-oriented WBS down to work-package level, weighted and
  baselined before estimating; level-2 elements or single large work packages become the
  control accounts at which `cost-management` measures earned value.
- **Agile:** the product and its epics form the upper levels; work packages are features or
  releases decomposed just-in-time per release, and weights are rough (story-point share)
  rather than cost shares — but every parent still sums to 100 so coverage can be checked.
- **Hybrid (Helios):** the contracted identity/SSO integration, testing and launch are
  decomposed up front with firm weights; the self-service UI and knowledge base stay coarse
  until the backlog is refined, yet still carry a weight so the 100% rule holds.

## Inputs you need
The agreed scope and major deliverables (from `scope-and-requirements` or the charter), an
organizing principle (deliverable-oriented preferred), a weight per element (percent of its
parent's effort, cost, or value), an owner per work package, the acceptance criteria from
`quality-management`, and — to allocate — the budget at completion (BAC) and the level at
which `cost-management` will measure performance (control accounts).

## Workflow
1. **Choose the organizing principle and list level 1** — deliverables, not phases (see
   `references/decomposition-rules.md`). Always include a project-management element: it is
   real work and part of the 100%. Helios: 1.1 Project management, 1.2 Discovery & design,
   1.3 Portal build, 1.4 Test & launch, 1.5 Adoption & handover. *Done: one principle per
   level, and nothing the charter lists as out of scope.*
2. **Decompose each deliverable into work packages** named as nouns ("Identity / SSO
   integration", not "integrate SSO"), mutually exclusive, and sized by the 8/80 rule; stop
   when a package has one owner and a verifiable "done". A level-of-effort element such as
   project management may stay undecomposed. *Done: every leaf is a work package.*
3. **Weight the children of every parent to 100** (percent of the parent's effort, cost, or
   value). Helios level 1: 10 / 15 / 45 / 20 / 10; under Portal build: SSO 35, UI 30,
   knowledge base 20, reporting 15. Siblings are weighted all or none. *Done: every parent's
   children sum to 100.*
4. **Record the WBS dictionary once** in a copy of `assets/wbs-template.csv`: `id, name,
   weight` plus `owner`, `description`, `acceptance criterion` (from `quality-management`)
   and `control account` — the element where cost and schedule performance will be measured
   (the work package itself, or a parent such as Helios 1.2 Discovery & design).
   `assets/wbs-sample.csv` shows the whole Helios WBS filled in. The CSV is the single source;
   never retype it into another document. *Done: every work package has an owner, a
   description, an acceptance criterion and a control account.*
5. **Validate** the hierarchy, the weights and the dictionary columns:
   ```bash
   python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py .claude/skills/work-breakdown-structure/assets/wbs-sample.csv --require owner,acceptance
   ```
   The report lists ERRORs (duplicate ids, orphans, children not summing to 100 ± 0.1,
   partly weighted siblings, blank required columns) and warnings (single child,
   leading-zero ids such as 1.01 vs 1.1, uneven depth, more than `--max-children`). Add
   `--suggest` for largest-remainder normalised weights, stub rows for missing parents and
   new numbers for duplicates, and `--fix OUT.csv` to write them to a new file (review it,
   then re-validate). Fix every ERROR; justify each warning. *Done: PASS, with `--strict` in
   CI so warnings fail too.*
6. **Roll up and allocate** to see what each element really is and to seed the cost baseline:
   ```bash
   python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py .claude/skills/work-breakdown-structure/assets/wbs-sample.csv --rollup --budget 500000
   ```
   Share of project = product of the weights down the chain: Helios 1.3.1 Identity / SSO
   integration is 45% × 35% = 15.75% → $78,750 of the $500,000 BAC, exactly the BAC per work
   package that `cost-management` tracks; the work packages sum to the budget to the cent.
   The control-account table (1.1, 1.2, 1.3.1 … 1.5.2 for Helios) is the level earned value
   is measured at. A work package above 20% of the project (`--max-leaf-share`) is too big
   to track as one unit. *Done: shares and budget per work package and control account
   agreed with `cost-management`.*
7. **Publish and hand off.** `--format md` renders the dictionary table for
   `assets/wbs-template.md` (paste it, do not retype); `--export-estimation PATH` writes the
   work packages in the worksheet format `estimation` reads; the ids go to
   `project-schedule`, the owners to `raci-matrix`, the acceptance criteria back to
   `quality-management`. Re-run the validator whenever an approved change request alters
   scope. *Done: the WBS is baselined and every downstream artefact keys on its ids.*

## Quality checklist
- [ ] One organizing principle per level; deliverables and work packages are named as nouns.
- [ ] A project-management element is included.
- [ ] 100% of the scope and nothing else: every parent's children carry weights summing to
      100 (siblings weighted all or none) and no out-of-scope item from the charter appears.
- [ ] Siblings are mutually exclusive; no parent has a single child.
- [ ] Every work package has one owner, a description, a verifiable acceptance criterion,
      and a control account.
- [ ] Work packages respect the 8/80 rule and none exceeds about 20% of the project.
- [ ] `scripts/wbs_validate.py` passes with `--require owner,acceptance` and no unexplained
      warning.
- [ ] The dictionary, estimation worksheet, schedule, and cost baseline all key on the same
      WBS ids.

## Anti-patterns
- Phases or activities ("write code", "testing phase") instead of deliverables — the WBS
  says *what*, the schedule says *when*.
- Leaving out project management, so the 100% rule is quietly broken.
- Weights that sum to 100 only across the children that happen to have one.
- Overlapping siblings, which double-count effort and blur ownership.
- Maintaining the dictionary and the CSV as two documents until they drift apart.
- Decomposing one branch to level 5 while a sibling stops at level 2.
- Putting sequence, dates, or people's names in as elements — those belong to
  `project-schedule` and `raci-matrix`.

## Resources
- `references/decomposition-rules.md` — 100% rule, 8/80 rule, deliverable- vs
  phase-oriented decomposition, work-package definition, control accounts, numbering and
  weights, with the Helios WBS as the example.
- `assets/wbs-template.csv` — fill-in WBS and dictionary in one CSV (`<placeholders>`): id,
  name, weight, owner, description, acceptance criterion, control account.
- `assets/wbs-sample.csv` — sample WBS for the Helios project (deliverable-oriented, 16
  elements, 11 work packages, weights that reproduce the $500,000 BAC split); the default
  script input.
- `assets/wbs-template.md` — WBS dictionary document: scope, organizing principle, the
  dictionary table (same headers the validator accepts; generated with `--format md`),
  control accounts, validation result, and sign-off.
- `scripts/wbs_validate.py` — validates ids, hierarchy, the 100% rule (`--tolerance`),
  partly weighted siblings and `--require col,col`; warns on single children, leading-zero
  ids, uneven depth, `--max-children N` and `--max-leaf-share PCT`; `--suggest` and
  `--fix OUT.csv` for normalised weights, stub parents and renumbered duplicates; `--rollup`
  shares and control accounts; `--budget AMOUNT` allocation; `--export-estimation PATH`;
  `--strict`; `--json`; `--delimiter`; `--format table|json|csv|md`. Run
  `python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py --help`.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-planning` — the planning phase that commissions the WBS as its first step and
  baselines it together with the schedule and budget.
- `quality-management` — supplies the acceptance criteria recorded per work package in the
  dictionary, making each "done" verifiable.
- `project-schedule` — sequences the work packages by their WBS ids into the network and
  the critical path.
- `estimation` — sizes each work package; `--export-estimation` writes its worksheet from
  the WBS leaves.
- `raci-matrix` — maps the work packages, and the owners named in the dictionary, to
  Responsible and Accountable roles.
- `scope-and-requirements` — provides the scope statement and deliverables this skill
  decomposes, and the approved scope changes that re-shape it.
