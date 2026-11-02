---
name: raci-matrix
description: >-
  Builds and validates a RACI, RASCI or DACI matrix with exactly one Accountable per
  activity, flagging overloaded roles and single points of failure (raci_validate.py). Use
  when settling who owns, does, is consulted on or is informed about each piece of work or
  decision.
metadata:
  version: 1.1.0
  category: artifact
  phase: planning
  related: [project-planning, stakeholder-management, work-breakdown-structure, resource-management]
license: MIT
---

# RACI Matrix

## Overview
A responsibility assignment matrix turns "we own this together" into named ownership: one row
per activity, work package or decision, one column per role, and in each cell **R**
(Responsible — does the work), **A** (Accountable — owns the outcome and signs it off), **C**
(Consulted — asked before, two-way) or **I** (Informed — told after, one-way). Two rules carry
most of the value: exactly one A per row and at least one R. This skill takes the rows from the
work breakdown structure, fills and validates the matrix with `scripts/raci_validate.py` — which
rejects any cell that is not a letter (so `N/A` or `TBC` can never pass as an A), suggests the
standard repairs, flags ghost and overloaded roles and single points of failure, and handles
the RASCI and DACI variants — and records each owner's acceptance. The worked example is the
sample Helios project (a fictional customer self-service portal used throughout this catalog):
eight rows that cover its whole WBS against six roles, from the Sponsor, Dana Okoro (VP
Customer Operations), to the Head of Support Operations, Priya Nair.

## When to use this skill
- The user wants to create, review, or repair a RACI, RASCI or DACI matrix, or check one that
  already lives in a spreadsheet.
- Ownership of a deliverable, work package or decision is unclear or disputed, or two people
  each think the other has it.
- A plan or WBS exists but it is not obvious who decides, who does, and who is only told.
- A one-off decision (a go/no-go gate, a policy choice) needs a single approver and a driver —
  use the DACI variant.
- Do NOT use this to decompose scope into the work packages that become the rows — use
  `work-breakdown-structure`.
- Do NOT use this to analyse stakeholders' power, interest or engagement — use
  `stakeholder-management`.
- Do NOT use this to check whether the people behind the roles have the hours — use
  `resource-management`.

## Methodology fit
- **Waterfall:** one row per work package or control account of the baselined WBS, signed off
  with the plan in `project-planning`, and re-validated whenever an approved change adds,
  splits or re-owns a work package.
- **Agile:** do not RACI backlog items — the Scrum roles already settle in-team ownership (the
  Product Owner is accountable for the backlog and value, the Developers for the increment).
  Keep a small RACI for cross-team and governance touchpoints (release approval, security
  sign-off, data-protection review) and a DACI for one-off decisions; below three rows the
  validator skips the share checks instead of warning.
- **Hybrid (Helios):** ownership of the governance-heavy rows is fixed up front — the identity/SSO
  integration with its vendor and security review, test and launch, adoption and handover —
  while the product owner and the team self-organise inside the build rows; the go/no-go gates
  sit in a DACI with the Sponsor as Approver.

## Inputs you need
The WBS work packages or deliverables, with the owner named in the WBS dictionary (from
`work-breakdown-structure`), or a list of decisions; the roles involved and the person holding
each (from the stakeholder register in `stakeholder-management`); the governance structure
(sponsor, steering committee); and the variant — RACI for delivery work, RASCI when a supporting
team materially helps, DACI for decisions. With no WBS yet, build it first: a RACI over an
incomplete activity list hides exactly the gaps it is meant to expose.

## Workflow
1. **Take the rows from the WBS.** One row per work package, or per deliverable when a single
   role owns all its packages; prefix each with its WBS id; cover all of the WBS and nothing
   else. Helios keeps 1.1, 1.2, 1.4 and 1.5 whole and splits 1.3 Portal build into its four
   work packages because ownership changes inside it — eight rows (`references/raci-rules.md`
   maps each to its WBS owner). *Done: every WBS element is covered by exactly one row.*
2. **Make the columns roles, not people,** and record who holds each role in section 2 of
   `assets/raci-template.md`. Include the business roles that own outcomes: Helios has a Head of
   Support Ops column because Priya Nair owns 1.5 Adoption & handover in the WBS dictionary.
   Choose the variant now. *Done: every role maps to one named person and the variant is set.*
3. **Fill the cells — A first, then R, then C and I sparingly.** Start from a copy of
   `assets/raci-template.csv` and replace every `<placeholder>` (the validator refuses unfilled
   ones). The WBS dictionary owner holds A or R on its row. Write R, A, C, I, a combination such
   as `A/R`, the full word, or leave the cell blank (`-`, `n/a`, `none` also mean blank).
   *Done: each row has one A and at least one R; every other cell is a deliberate C, I or blank.*
4. **Validate.**
   ```bash
   python .claude/skills/raci-matrix/scripts/raci_validate.py .claude/skills/raci-matrix/assets/raci-sample.csv
   ```
   The sample passes with no warnings. On your own file the ERRORs are no or multiple
   Accountable, no Responsible, and unnamed or duplicate activities; the warnings are
   contradictory cells such as `R/I`, more than `--max-ci` (default 4) C/I roles on a row, ghost
   roles, a role Accountable on more than `--max-a-share` (default 0.5 or `50%`) of the rows,
   and a role Responsible on every row. Any other cell text — `TBC`, `X`, `Review`, a name —
   stops the run with its line and role. Use `--ignore-col Notes` for columns that are not
   roles, `--activity-col NAME` when the activity column is not detected, `--transpose` when
   roles are rows, `--variant rasci` or `--variant daci` for the variants, and `--json` for JSON
   input. *Done: the run prints PASS.*
5. **Repair with the suggested fixes.** `--fix` prints a repair under each finding: keep the
   least-loaded of several A's, promote a Consulted role to R when nobody does the work, make
   the single R also the A. `--fix-out my-raci-fixed.csv` writes those ERROR fixes into a copy
   (same format, delimiter and layout; nothing else changes). They are mechanical suggestions —
   confirm each with the people involved, then re-run, adding `--strict` in CI so warnings fail
   too. *Done: no errors, and every remaining warning fixed or justified in section 4 of
   `assets/raci-template.md`.*
6. **Read the role summary** printed after the report: each role's A, R, C and I counts, the
   rows it touches, and its A-share and R-share. In Helios the Tech lead is R on 6 of 8 rows
   (75%) — no rule is broken, but it is the key-person exposure the risk register holds as R003
   (lead engineer leaves), so link the two and check the load in `resource-management`. The
   Sponsor is A on no work package because her accountability is the go/no-go decisions:
   ```bash
   python .claude/skills/raci-matrix/scripts/raci_validate.py .claude/skills/raci-matrix/assets/daci-decisions-sample.csv --variant daci
   ```
   *Done: ghost roles removed, and every concentration rebalanced or tied to a risk and owner.*
7. **Publish, get acceptance, keep it current.** Paste the `--format md` output into section 3
   of `assets/raci-template.md` (`--format json` or `--format csv` feed other tools), walk every
   A and R through their rows, and record their acceptance; baseline the matrix with the plan in
   `project-planning`. Re-validate whenever the WBS changes or a role changes hands. *Done: every
   A and R has accepted in writing and the matrix version matches the WBS version.*

## Quality checklist
- [ ] Every row is a WBS element (prefixed with its id) or a decision, and the rows cover the
      whole WBS exactly once.
- [ ] Columns are roles, and each role maps to one named person in `assets/raci-template.md`.
- [ ] Every row has exactly one A and at least one R (DACI: one Approver, at least one Driver).
- [ ] On each work package the WBS dictionary owner holds A or R, or the difference is explained.
- [ ] No row has more than four C/I roles, and no cell combines I with another letter.
- [ ] No role is Accountable on more than half the rows or Responsible on all of them; no ghost
      columns.
- [ ] `scripts/raci_validate.py` reports PASS (with `--strict` when the matrix gates a baseline),
      and every accepted warning is justified with an owner.
- [ ] Every A and R has accepted their rows, with the date recorded.

## Anti-patterns
- Two A's on a row "to be safe" — shared accountability means each assumes the other has it.
- An A with no R: an owner and no doer, so the work does not happen.
- Writing `N/A`, `TBC`, `X` or "Review" instead of deciding — decide, or leave the cell blank.
- Everyone Consulted on everything, which turns every decision into a committee.
- People's names as columns, so the matrix breaks whenever someone leaves; use roles.
- One hero role Accountable on most rows, or Responsible on all of them — a bottleneck and a
  single point of failure.
- A RACI over every backlog item in an agile team; keep it for governance and interfaces.
- Decisions and delivery work mixed in one matrix — put the decisions in a DACI.

## Resources
- `references/raci-rules.md` — the letters, accepted and rejected cell values, every check and
  why it matters, how `--fix` chooses a repair, reading the role summary, building rows from the
  WBS (the Helios row-to-owner table), and the RASCI and DACI rules.
- `assets/raci-template.csv` — fill-in matrix with `<placeholders>` for activities, roles and
  letters; the validator refuses it until every placeholder is replaced.
- `assets/raci-sample.csv` — sample RACI for the Helios project: 8 rows covering the whole WBS
  x 6 roles; passes with no warnings; the default script input.
- `assets/daci-decisions-sample.csv` — sample DACI for four Helios decisions (the M4 and M6
  go/no-go gates, the SSO session-timeout policy, the launch knowledge-base articles); run it
  with `--variant daci`.
- `assets/raci-template.md` — the publishable document: roles-to-people table, the matrix
  (pasted from `--format md`), validation result and accepted warnings, acceptance sign-off,
  and change history.
- `scripts/raci_validate.py` — validates the matrix with strict cell parsing; options
  `--variant raci|rasci|daci`, `--json`, `--delimiter CHAR`, `--activity-col NAME`,
  `--ignore-col NAMES`, `--transpose`, `--max-ci N`, `--max-a-share SHARE`, `--fix`,
  `--fix-out PATH`, `--strict`, `--format table|json|csv|md`; exit 0 PASS, 1 FAIL, 2 bad input.
  Run `python .claude/skills/raci-matrix/scripts/raci_validate.py --help`.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-planning` — commissions this matrix in its planning step and baselines it alongside
  the schedule and budget.
- `stakeholder-management` — supplies the people behind each role from the stakeholder
  register; this matrix turns them into role-level responsibilities.
- `work-breakdown-structure` — provides the work packages that become the rows, and the
  dictionary owner who holds A or R on each.
- `resource-management` — checks that the roles carrying many R's (the role summary's
  R-share) have the capacity behind them.
