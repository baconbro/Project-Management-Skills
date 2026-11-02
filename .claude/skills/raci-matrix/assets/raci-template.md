# Responsibility assignment matrix — <project name>

> Fill-in template. Replace every `<placeholder>`. The matrix itself lives in the CSV that
> `raci_validate.py` reads; paste its `--format md` output into section 3 instead of retyping
> it. `raci-sample.csv` and `daci-decisions-sample.csv` show the sample Helios project (a
> fictional customer self-service portal used throughout this catalog) filled in.

| Field | Value |
| --- | --- |
| Project | <project name> |
| Variant | <RACI / RASCI / DACI> |
| Rows taken from | <WBS version and date, or decision log reference> |
| Matrix file | <path to the CSV or JSON the validator reads> |
| Maintained by | <project manager name> |
| Version and date | <version> · <date> |

## 1. How to read this matrix

**R** Responsible — does the work · **A** Accountable — owns the outcome and signs it off
(exactly one per row) · **C** Consulted — asked before, two-way · **I** Informed — told after,
one-way. <Add S Support for RASCI, or use D Driver / A Approver / C Contributor / I Informed for
DACI.>

## 2. Roles and the people who hold them

| Role (column) | Person | Stakeholder register id | Capacity checked (resource-management) |
| --- | --- | --- | --- |
| <role> | <name> | <S01> | <yes / over-allocated in weeks n-m> |
| <role> | <name> | <S02> | <yes / over-allocated in weeks n-m> |

## 3. Matrix

<Paste the output of: python .claude/skills/raci-matrix/scripts/raci_validate.py <your-matrix.csv> --format md>

## 4. Validation

- Result: <PASS / FAIL> (<n> errors, <n> warnings) on <date>, options: <e.g. --strict --max-ci 4>
- Warnings accepted, each with its justification and owner:

| Warning | Why it is acceptable | Owner | Linked risk or action |
| --- | --- | --- | --- |
| <e.g. Tech lead R on 6 of 8 rows> | <reason> | <name> | <risk id, e.g. R003> |

## 5. Acceptance

Every role holding an A or an R confirms the rows below.

| Role | Person | Rows where A or R | Accepted on | Comment |
| --- | --- | --- | --- | --- |
| <role> | <name> | <WBS ids> | <date> | <comment> |

## 6. Change history

| Version | Date | Change | Trigger |
| --- | --- | --- | --- |
| <1.0> | <date> | <baselined with the project plan> | <planning baseline> |
| <1.1> | <date> | <what changed> | <change request id, WBS change, or role handover> |
