# Planning sequence — inputs, outputs and loops

Load this to see why the planning steps run in their order, what each step needs and produces,
which later step consumes it, and when to loop back. Step numbers match the Workflow in
`SKILL.md`. Examples use the sample Helios project (a fictional customer self-service portal
used throughout this catalog).

## Why this order
- **Scope before the WBS.** You cannot decompose what has not been agreed; the scope statement
  from `scope-and-requirements` fixes the deliverables, exclusions and acceptance criteria.
- **WBS before make-or-buy and estimates.** Both are decided per work package.
- **Make-or-buy before estimates.** A bought package is a price and a lead time, not effort.
- **People before dates.** A duration depends on who does the work and how much of their week
  they have. A schedule built without capacity is invalidated the moment it is leveled.
- **Risks before reserves, reserves before the cost baseline.** Contingency is sized from
  analysed risks; a baseline set first holds a guessed or padded buffer.
- **Quality before cost.** Gates, reviews and tests are work that costs time and money.
- **Change control before the freeze.** A baseline with no process to protect it erodes from
  the first week.
- **One approval at the end.** Approving scope, schedule and cost separately lets them
  contradict each other; the sponsor approves the reconciled whole once.

## Step map
| # | Step | Skill(s) | Needs | Produces | Used by |
|---|---|---|---|---|---|
| 1 | Open the plan and the assumptions log | this skill | Approved charter | Plan skeleton; assumptions log | 2, 7, 12 |
| 2 | Agree the scope statement | `scope-and-requirements` | Charter; stakeholder register | Scope statement; traceability matrix | 3, 8 |
| 3 | Decompose the work | `work-breakdown-structure` | Deliverables | WBS and dictionary; work-package ids | 4–9 |
| 4 | Decide make-or-buy | `procurement-management` | Work packages | Decisions, routes, prices, lead times | 5, 6, 7, 9 |
| 5 | Estimate | `estimation` | Work packages; vendor prices | Effort and cost ranges; assumptions | 6, 9 |
| 6 | Staff and level the schedule | `raci-matrix`, `resource-management`, `project-schedule` | Estimates; owners; availability; lead times | RACI; leveled schedule; capacity gate | 7, 9, 10 |
| 7 | Risk and reserves | `risk-management`, `risk-register` | Plan so far; assumptions log | Register; contingency; management reserve; schedule reserve | 6 (loop), 9 |
| 8 | Quality | `quality-management` | Scope statement; WBS | Acceptance criteria; definition of done; gates | 6 (loop), 9 |
| 9 | Cost baseline | `cost-management` | Estimates; prices; leveled schedule; contingency | BAC; S-curve; earning rules; management reserve | 12 |
| 10 | Engagement and communications | `stakeholder-management`, `project-communication` | Register; RACI; milestones | Engagement strategy; communication plan | 12 |
| 11 | Change control | `change-management` | Proposed baselines; policy | Procedure; tolerances; reserve rules | 12 |
| 12 | Integrate and approve | this skill | All of the above | Approved, snapshotted baseline | `project-delivery` |

## Feedback loops — close them before step 12
| Trigger | Loop back to | Then re-run |
|---|---|---|
| Leveling cannot absorb an overload | Sponsor decision: scope (2), capacity (6) or date (6) | 9 |
| A risk response adds work (a spike, cross-training, a vendor clause) | 3 and 5 for the new work | 6, 9 |
| A gate, review or test is added | 5 and 6 | 9 |
| An assumption proves false | 7 (now a risk or an issue), or 2–6 if the plan must change | 9 |
| A vendor lead time is longer than the task's float | 6 | 7, 9 |
| A fixed date is missed after leveling | Compression in `project-schedule` (crash or fast-track) | 7 (new risk), 9 (cost) |
| BAC plus management reserve exceeds the charter range | Scope (2), approach, or a funding decision by the sponsor | 9 |

Helios closed two loops before approval: leveling the W6–W9 build peak moved knowledge-base
work within its float (step 6, no date change), and the cross-training response to R003 (lead
engineer leaves) became scheduled work, so the capacity check in step 6 was re-run before the
cost baseline.

## Agile and hybrid variants
| Step | Agile form | Skill |
|---|---|---|
| 2 | Product vision, release goal, constraints and exclusions; requirements as epics | `scope-and-requirements`, `agile-delivery` |
| 3 | Epics and features traced to WBS ids (`wbs_id` in the backlog) | `work-breakdown-structure`, `agile-delivery` |
| 5 | Story points by planning poker; effort only for non-team costs | `estimation` |
| 6 | A stable team; sprint capacity from availability; velocity-based release plan | `resource-management`, `agile-delivery` |
| 7 | HIGH risks become spikes or backlog items with an owner | `risk-register` |
| 8 | Definition of done and per-story acceptance criteria | `quality-management` |
| 9 | Run-rate budget: cost per sprint × planned sprints, inside a fixed envelope | `cost-management` |
| 12 | Baseline = prioritised backlog + release plan + definition of done | this skill |

**Hybrid (Helios):** steps 3, 6 and 9 run in full for the fixed elements (the Identity / SSO
integration, hardening and launch, and the compliance work) and at release level for the
self-service UI and knowledge base, whose Should and Could stories flex inside the release.
One BAC covers both, so earned value and the forecast stay whole.

## Re-planning
Re-entering the sequence mid-project (a large approved change, a recovery plan) starts at the
first step the change touches and runs every later step, then a new step 12. See
`baseline-guide.md` for when that is a re-baseline and when it is an approved change.
