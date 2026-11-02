# RACI rules

A responsibility assignment matrix has one row per activity (a WBS work package, a deliverable
or a decision) and one column per role. Each cell says how that role takes part in that row.
The examples use the sample Helios project (a fictional customer self-service portal used
throughout this catalog); its matrix is `assets/raci-sample.csv`.

## The letters

| Letter | Role | Meaning |
| --- | --- | --- |
| **R** | Responsible | Does the work. Several are allowed; **at least one** is required. |
| **A** | Accountable | Owns the outcome and signs it off. **Exactly one** per row. |
| **C** | Consulted | Gives input *before* the work is done — two-way dialogue. |
| **I** | Informed | Told about progress or the result *after the fact* — one-way. |

A role can hold more than one letter on a row. The common combination is `A/R`: the same role
owns the outcome and does the work. `I` combined with anything else is a contradiction — a role
cannot do, own or shape the work and also merely be told about it afterwards.

## What a cell may contain

`scripts/raci_validate.py` reads cells case-insensitively and splits them on `/`, `,`, `+`, `&`
and spaces.

- **Accepted:** the letters of the chosen variant (`R`, `A`, `C`, `I`; plus `S` for RASCI; `D`
  instead of `R` for DACI), letters run together (`AR`), combinations (`A/R`, `A, R`, `A + R`),
  and the full words Responsible, Accountable, Approver, Consulted, Contributor, Informed,
  Support, Supportive, Supporting and Driver.
- **Blank:** an empty cell, `-`, `n/a`, `na`, `none`.
- **Rejected (the run stops, exit 2, naming line, activity and role):** everything else — `TBC`,
  `X`, a tick, `Yes`, `Review`, `Approve`, a person's name, a number, a JSON `true`/`false`, a
  `<placeholder>` left from the template, and a letter that belongs to another variant (`S` in
  plain RACI, `D` outside DACI, `R` in DACI). Cells are never mined for stray letters, so `N/A`
  can never count as an Accountable and `Informed` can never count as a Responsible.

Columns that are not roles (notes, WBS ids, dates) are skipped with `--ignore-col NAME`. A
matrix laid out with roles as rows is read with `--transpose`.

## The checks

| Level | Check | Rule | Why it matters |
| --- | --- | --- | --- |
| ERROR | no accountable | zero A on a row | nobody owns the outcome, so it drifts |
| ERROR | multiple accountable | more than one A | each owner assumes the other has it |
| ERROR | no responsible | zero R on a row | an owner and no doer — the work does not happen |
| ERROR | unnamed activity | a row without a name | it cannot be traced to the WBS |
| ERROR | duplicate activity | the same name twice | the row is assigned twice, possibly differently |
| WARN | contradictory cell | `I` with another letter (`R/I`, `A/I`, `C/I`) | almost always a copy-paste slip |
| WARN | too many cooks | more than `--max-ci` (default 4) roles are C or I on a row | every consult is a round trip; decision by committee stalls work |
| WARN | ghost role | a column with no letter anywhere | a stale or unexplained role |
| WARN | overloaded | a role is A on more than `--max-a-share` (default 0.5 = 50%) of the rows | one owner becomes the bottleneck |
| WARN | single point of failure | a role is R on every row | everything waits on one role |
| WARN | layout | the activity column looks like roles | the matrix is probably transposed |

The overloaded and single-point-of-failure checks need at least three rows; a small governance
matrix gets an INFO line instead of an unavoidable warning. `--strict` makes every warning fail
the run (exit 1), which suits a CI gate before the plan is baselined.

## How `--fix` chooses a repair

The validator works through the rows in order on a working copy, so each choice counts the
fixes already made above it.

1. **Multiple accountable** — keep the A held by the least-loaded role (fewest A across the
   matrix; ties go to the leftmost column). The other A's are removed; a role left with nothing
   becomes C, because it clearly cares about the outcome.
2. **No responsible** — promote a Consulted role to R (RASCI: a Support role first), choosing
   the one that is already R least often. If the row has no C, the A also becomes R (`A/R`).
3. **No accountable** — the single R becomes `A/R`; with several R's, the one with the fewest A.

`--fix-out PATH` writes exactly these ERROR fixes into a copy of the input — same format,
delimiter and layout, every other cell untouched. Warnings get a suggestion but are never
applied, because they need judgment. The fixes are mechanical: confirm each with the people
involved before you accept the file.

## Reading the role summary

After the report the validator prints one line per role: the count of each letter, how many
rows the role touches, its A-share and its R-share.

- **Touches 0** — a ghost role: assign it or delete the column.
- **High A-share** — an accountability bottleneck. Hand A to the role that is R on some of those
  rows.
- **High R-share** — a delivery concentration even when no rule is broken. In the Helios sample
  the Tech lead is R on 6 of 8 rows (75%); that is the key-person exposure the risk register
  holds as R003 (lead engineer leaves), so tie it to that risk and check the load with
  `resource-management`.
- **No A at all** for a senior role is normal: in Helios the Sponsor, Dana Okoro, owns no work
  package — her accountability is the go/no-go decisions in the DACI matrix.

## Building the rows from the WBS

Take the rows from the WBS so that every piece of work is covered exactly once, and split a
deliverable into its work packages only where ownership changes inside it. Prefix each row with
its WBS id. The WBS dictionary owner holds A or R on the row; when the A differs, say why. In
Helios, "Tech lead" stands for the engineering team (Ben Adeyemi, Carla Diaz, Devin Patel):

| Row | WBS dictionary owner | A in the sample | Note |
| --- | --- | --- | --- |
| 1.1 Project management | Sam Lee | Project manager | |
| 1.2 Discovery & design | Ava Chen | Product owner | |
| 1.3.1 Identity / SSO integration | Ben Adeyemi | Tech lead | security review by Marcus Webb is part of acceptance |
| 1.3.2 Self-service UI | Devin Patel | Tech lead | Devin is R inside the Tech lead's team |
| 1.3.3 Knowledge base | Carla Diaz | Product owner | Carla builds it (R); the product owner owns the content outcome |
| 1.3.4 Reporting & analytics | Carla Diaz | Product owner | the dashboard evidences the 50% ticket-reduction benefit |
| 1.4 Test & launch | Frank Müller | QA engineer | Ben Adeyemi is R for hardening and launch |
| 1.5 Adoption & handover | Priya Nair | Head of Support Ops | Ben Adeyemi is R for the operational handover |

## Good practice

- Assign A first (one owner), then R (the doers), then add C and I only where they change the
  outcome or genuinely need to know. Prefer Informed over Consulted, and blank over Informed
  when the communication plan already reaches that role.
- Use roles as columns and map them to people separately, so the matrix survives a change of
  personnel.
- Review the matrix with the named people; an assignment nobody accepted is not real.
- Re-validate whenever the WBS changes or a role changes hands.

## Variants: RASCI and DACI

- **RASCI** (`--variant rasci`, alias `rasic`) adds **S = Support**: a team that provides
  resources or help to the Responsible party without owning the task (for example an
  infrastructure team). The RACI rules apply unchanged; S is counted in the role summary and is
  the first candidate when a row has no R.
- **DACI** (`--variant daci`) is for decisions rather than delivery work: **D = Driver** (moves
  the decision forward), **A = Approver** (the one decision-maker), **C = Contributor**, **I =
  Informed**. Rules: exactly one Approver per decision and at least one Driver (the Driver rule
  replaces the R rule). Most teams name a single Driver. The Helios sample
  `assets/daci-decisions-sample.csv` has the Sponsor as Approver for both go/no-go gates (MVP
  live to pilot at M4, general availability at M6), the Security lead (Marcus Webb) approving
  the SSO session-timeout policy, and the Head of Support Operations (Priya Nair) approving the
  knowledge-base articles for launch.

Stick to plain RACI unless the project genuinely needs the extra letter; every added letter is
another judgment call per cell and another way to get the matrix wrong.
