# Dependency Types — and how to encode them for the tool

A schedule's logic is the set of dependencies between tasks. Getting the dependency *type*,
*lead/lag* and *category* right is what makes the critical path meaningful.

`scripts/critical_path.py` computes **finish-to-start (FS) links with zero lag only**. Every
other relationship is encoded as explicit lag or milestone tasks, so that it stays visible in
the network, in the Gantt and in the math. **Never fold a lag, lead or overlap into a work
task's duration**: the logic becomes invisible, the duration no longer matches the effort it
was estimated from, and the float of every neighbour is wrong. The examples use the sample
Helios project (a fictional customer self-service portal used throughout this catalog) and the
ids of `assets/schedule-sample.csv`.

## The four logical relationships
Each dependency links a predecessor to a successor. The two letters name which end of each
task is tied:

- **Finish-to-Start (FS):** the successor cannot start until the predecessor finishes. The
  default and by far the most common — B *UX design & prototype* starts when A *Requirements
  & user research* finishes. This is what the tool models directly.
- **Start-to-Start (SS):** the successor cannot start until the predecessor starts (usually
  with a lag). Used for overlapping work — E *Knowledge base* content could start one week
  after B *UX design* has started, once the page structure is known.
- **Finish-to-Finish (FF):** the successor cannot finish until the predecessor finishes —
  I *Training & communications* cannot finish before H *Hardening & launch* finishes, because
  the final screens must be in the training material.
- **Start-to-Finish (SF):** the successor cannot finish until the predecessor starts. Rare;
  used for hand-overs — the manual password-reset desk (successor) cannot be shut down until
  the portal's go-live (predecessor) has started.

## Lead and lag
- **Lag** is a deliberate *delay* on a dependency: "start UAT two weeks after the build
  finishes" (waiting for the vendor's test tenant) is FS + 2 weeks lag. Lag stretches the
  schedule.
- **Lead** is *overlap* (negative lag): "start testing one week before the build finishes" is
  FS − 1 week lead. Lead compresses the schedule — it is fast-tracking made explicit (see
  `references/schedule-compression.md`).

## Encoding rules for the FS-only tool
| Relationship | Encode as explicit FS tasks | Helios example rows (`id,name,duration,predecessors`) |
|---|---|---|
| FS + lag *n* | a **lag task** of duration *n* between the two; zero resources, named "Lag: ..." | `L1,Lag: vendor test tenant,2,C` and `G,System & UAT testing,4,L1;D;E;F` |
| FS − lead *n* (overlap) | **split the predecessor** into P1 (duration − *n*) and P2 (*n*); the successor depends on P1; P2 keeps the old successors | `G1,System & UAT testing (to pilot launch),3,C;D;E;F` · `G2,System & UAT testing (stabilisation),1,G1` · `I,Training & communications,4,G1` · `H,...,5,G2` |
| SS + lag *n* | split the predecessor into P1 (first *n*) and P2 (rest); the successor depends on P1 | `B1,UX design (structure),1,A` · `B2,UX design (prototype),1,B1` · `E,Knowledge base,9,B1` · `C,...,9,B2` · `D,...,10,B2` · `F,...,9,B2` |
| FF + lag *n* | split the successor into S1 (all but the last *n*) and S2 (last *n*); S2 depends on the predecessor and on S1 | `I1,Training material,3,G` · `I2,Training delivery,1,I1;H` · `J,Operational handover,1,H;I2` |
| SF | add a zero-duration **start milestone** for the predecessor; the successor's final part depends on it | `M5,Portal go-live,0,H` · `K2,Close manual reset desk,0.5,K1;M5` |
| Milestone or imposed date | a zero-duration task; compare its computed date with the imposed one (SKILL.md step 5, `--target`) | `G1,System test & pilot UAT,3,C;D;E;F` · `M4,MVP live to pilot,0,G1` · `G2,Pilot stabilisation,1,M4` |

The splits keep the effort-to-duration link intact (each part is estimated on its own), show
up as separate bars in `--gantt`, and let the tool report float for each part. Give lag tasks
no resource so the capacity check in `resource-management` ignores them.

## Mandatory vs. discretionary vs. external
- **Mandatory (hard logic):** inherent in the work — G *System & UAT testing* cannot start
  before the code it tests exists. These cannot be reordered.
- **Discretionary (soft logic):** a preferred sequence the team chose, not a physical
  necessity — Helios starts C, D, E and F only when the whole prototype (B) is agreed at
  M1, although the build could start on the agreed page structure (the SS row above).
  Discretionary links *can* be re-sequenced or overlapped, and are the first place to look
  when fast-tracking.
- **External:** outside the project's control — the identity-provider sandbox for C
  (risk R001), legal sign-off inside H. Model the delivery as a milestone the task depends
  on, and track it in `risk-register` as well as in the schedule.

Record the category in an extra column of the schedule CSV (for example `category`); the tool
ignores columns it does not know, so the classification travels with the network.

## Why the distinction matters
The critical path is the longest chain of dependent tasks; its length is the shortest
possible project duration. To shorten the project you must shorten a *critical* task on
*every* critical path — crash it (add resources) or fast-track it (overlap by relaxing a
discretionary link, encoded as a split). Touching a non-critical task only consumes its float.
`references/schedule-compression.md` walks through both techniques on Helios.

## Common mistakes
- Modeling everything as FS when work genuinely overlaps (SS/FF), inflating the duration —
  use the split-task encodings above instead of pretending the overlap does not exist.
- Folding lag or lead into a task's duration so the logic is opaque and the duration no
  longer matches the estimate.
- Treating discretionary links as mandatory, so the schedule looks impossible to compress.
- Ignoring external dependencies until they slip — milestone them and log the risk.
- Forgetting that a lag task has no resources and no effort; it must not inflate the cost
  baseline.
