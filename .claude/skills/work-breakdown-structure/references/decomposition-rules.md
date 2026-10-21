# Decomposition Rules

A work breakdown structure (WBS) decomposes the total scope of a project into a hierarchy
of deliverables and the work packages that produce them. These rules keep the decomposition
complete, non-overlapping, and verifiable. Examples use the sample Helios project (a
fictional customer self-service portal used throughout this catalog); the full WBS is in
`assets/wbs-sample.csv`.

## The 100% rule
The WBS captures **100% of the scope** — all the work, and *only* the work, needed to
deliver the project. At every level the children add up to exactly their parent: no more
(no gold-plating, no out-of-scope work such as Helios CR001 live chat, deferred to phase 2)
and no less (no missing work). When children carry weights (percent of the parent's
effort, cost, or value) they must sum to 100 at each parent, and **siblings are weighted
all or none**: an unweighted sibling next to weighted ones is either 0% of the parent (then
why is it there?) or proof that the split is wrong. `scripts/wbs_validate.py` enforces both.

Include a **project-management element** (planning, baselines, governance, reporting,
closure). It is real work that consumes budget and is tracked by earned value, so leaving
it out breaks the 100% rule silently. Helios: 1.1 Project management = 10%.

## Mutually exclusive
Sibling elements must not overlap. A piece of work belongs to exactly one element. Overlap
causes double-counting in estimates and confusion over ownership. If two elements seem to
share work, the boundary is wrong — redraw it.

## The 8/80 rule
A work package — a leaf element — should be small enough to estimate, assign, and track,
but not so small that managing it costs more than doing it. A common heuristic is that a
work package takes between **8 and 80 hours** of effort (roughly one day to two weeks); for
a six-month project like Helios, a few person-weeks each. If a package is bigger than that,
decompose it further; if many are under 8 hours, you have decomposed too far. At project
level, a single work package above roughly 20% of the project is too large to track as one
unit (`--max-leaf-share` warns). Decompose branches to comparable depths: one branch at
level 5 while its sibling stops at level 2 usually means one of them is wrong.

## Deliverable- vs phase-oriented
- **Deliverable-oriented:** the first level groups the *things produced*. Helios: Discovery
  & design, Portal build, Test & launch, Adoption & handover, plus Project management.
  Preferred — it ties the WBS to outcomes and the 100% rule is easy to check.
- **Phase-oriented:** the first level groups by *stage* (Design, Build, Test, Release).
  Useful for stage-gated delivery, but watch for the same deliverable reappearing across
  phases, which risks overlap.
Pick one organizing principle per level and stay consistent. Whatever the principle, name
every element as a **noun** ("Identity / SSO integration", "Knowledge base"), never as an
activity ("integrate SSO", "write articles").

## Work package definition
A **work package** is the lowest element in the WBS — the unit that is estimated,
scheduled, assigned to one owner, and tracked to completion. A good work package has:
- a single accountable owner,
- a description that says what is in and out,
- a verifiable acceptance criterion ("done" is unambiguous; see `quality-management`),
- an effort/cost estimate (it is the unit `estimation` and `project-schedule` consume),
- a control account it reports into.
**Level-of-effort elements** (project management, support) are legitimate work packages
that are not decomposed; estimate them parametrically, as a share of the delivery effort.

## Control accounts
A **control account** is the WBS element where cost and schedule performance (earned value)
are measured and where one manager answers for the budget. It is a work package, or a
parent that groups several small ones. Every work package belongs to exactly one. Helios:
1.1 Project management; 1.2 Discovery & design (grouping 1.2.1 and 1.2.2); 1.3.1–1.3.4,
1.4.1, 1.4.2, 1.5.1 and 1.5.2 each measured on their own — exactly the ten lines of the
earned-value snapshot in `cost-management`. Record it in the `control account` column of
the CSV; the validator rolls shares and budget up per control account under `--rollup`.

## Numbering and weights
- Ids are dotted: level 1 is `1`, level 2 `1.3`, level 3 `1.3.2`; the parent is the id
  minus its last segment. Never reuse an id, never leave a segment empty (`1.` or `1..2`),
  and avoid leading zeros (`1.01` and `1.1` collide in sorted lists). Keep ids stable once
  baselined: a removed package leaves a gap, a new one takes the next free number.
- Weights are the percent of the **parent**, not of the project. Share of project = the
  product of the weights down the chain: Helios 1.3.1 = 45% × 35% = 15.75%. With a BAC of
  $500,000 that is $78,750 — the per-work-package BAC that `cost-management` uses.
- Allocating a budget by weight uses largest-remainder rounding so the work packages add up
  to the budget exactly; a 33.3 / 33.3 / 33.3 split is accepted (tolerance 0.1) and
  normalises to 33.4 / 33.3 / 33.3.

## The Helios WBS (weights = % of parent)
```
1      Helios customer self-service portal
1.1    Project management                 10
1.2    Discovery & design                 15
1.2.1    Requirements & user research       60
1.2.2    UX design & prototype              40
1.3    Portal build                       45
1.3.1    Identity / SSO integration         35
1.3.2    Self-service UI                    30
1.3.3    Knowledge base                     20
1.3.4    Reporting & analytics              15
1.4    Test & launch                      20
1.4.1    System & UAT testing               70
1.4.2    Hardening & launch                 30
1.5    Adoption & handover                10
1.5.1    Training & communications          50
1.5.2    Operational handover               50
```

## What the WBS is not
The WBS lists *what* is produced, not *when* or *in what order* — sequencing and durations
belong to `project-schedule`. It is not an org chart, not a task list of every action, and
not a cost report; it is the skeleton those artefacts hang on.

## Common mistakes
- Breaking the 100% rule: missing work (most often project management), or work that does
  not belong.
- Weighting only some siblings, so the sum "works" while a package is silently 0%.
- Overlapping siblings, so effort is double-counted.
- Decomposing to actions ("write code") instead of deliverables ("authentication module").
- A parent with a single child — that is a rename, not a decomposition.
- Mixing deliverable and phase organization at the same level.
- Keeping the dictionary in a separate document that drifts from the CSV.
