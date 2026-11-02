# Acceptance Record — <Project name>

Fill-in template for step 1 of `project-closure`. Use it when the project has no scope
statement acceptance log, when acceptance criteria are being agreed at closure, or when the
project is stopped early (Part T). Replace every `<placeholder>`; delete Part T if the project
completed, and delete the rows you do not need. Guidance: `references/acceptance-at-closure.md`
and, for a stopped project, `references/premature-closure.md`.

| Field | Value |
|---|---|
| Project | `<project name>` |
| Closure path | `<completed project / phase or stage (name it) / stopped early>` |
| Sponsor | `<name, role>` |
| Project manager | `<name>` |
| Record version and date | `<v1.0>`, `<YYYY-MM-DD>` |

## Part A — Acceptance criteria and their source
Source used (first that exists): `<scope statement vX / definition of done and gate criteria /
contract statement of work / charter / agreed at closure>`.
If agreed at closure: agreed with `<sponsor name>` on `<YYYY-MM-DD>`, before the evidence was
reviewed, by `<email / meeting minutes / signature>`.

| # | Deliverable | Criterion (observable, pass/fail) | Source | Acceptor |
|---|---|---|---|---|
| `<D1>` | `<deliverable>` | `<criterion 1>` | `<source>` | `<one named person>` |
| `<D1>` | `<deliverable>` | `<criterion 2>` | `<source>` | `<same acceptor>` |
| `<D2>` | `<deliverable>` | `<criterion>` | `<source>` | `<name>` |

Benefits are not criteria: outcomes that show only after go-live go to the benefits handover.

## Part B — Decisions
| # | Deliverable | Evidence | Decision | Acceptor | Date | Conditions or failed criterion |
|---|---|---|---|---|---|---|
| `<D1>` | `<deliverable>` | `<test summary / UAT sign-off / audit / hypercare exit record>` | `<accept / accept with conditions / reject>` | `<name>` | `<YYYY-MM-DD>` | `<"none" / condition ids / criterion #>` |
| `<D2>` | `<deliverable>` | `<evidence>` | `<decision>` | `<name>` | `<YYYY-MM-DD>` | `<...>` |

Requirements or features not built: `<ids>` formally deferred to `<backlog or owner>` on
`<YYYY-MM-DD>`.

## Part C — Conditions and known exceptions
Each row is also a row in the closeout log (`assets/closeout-log-template.csv`).

| Id | Deliverable | Condition or exception | Owner | Due | Closeout-log id |
|---|---|---|---|---|---|
| `<C1>` | `<D#>` | `<small, specific follow-up, or accepted defect>` | `<name>` | `<YYYY-MM-DD>` | `<id>` |

Rejected deliverables and what happens next: `<fix list with dates / accepted as exception
by sponsor / removed from scope by change request (id)>`.

## Part T — Termination confirmation (stopped-early closure only)
| Field | Value |
|---|---|
| Decision | `<stop now / stop at a defined point (name it)>` |
| Decided by, forum and date | `<name, role>`, `<forum>`, `<YYYY-MM-DD>` |
| Reason and evidence | `<re-appraisal result / breached tolerance / external event>` |
| Stop-work date and who instructs the team and vendors | `<YYYY-MM-DD>`, `<name>` |
| Salvaged work and receiving owners | `<work product → owner>`; `<work product → archive>` |
| Work discarded or decommissioned | `<item, how, by when>` |
| Contracts to terminate (through `procurement-management`) | `<vendor, notice date, termination cost>` |
| Other obligations (customers, data, regulators) | `<obligation → owner, date>` |
| Communications owner and date | `<name>`, `<YYYY-MM-DD>` |

## Part D — Sign-off
| Role | Name | Decision | Signature or reference | Date |
|---|---|---|---|---|
| Sponsor (final acceptance, or termination) | `<name>` | `<accepted / accepted with conditions / project terminated>` | `<signature / email ref>` | `<YYYY-MM-DD>` |
| Acceptor(s) | `<name>` | `<as in Part B>` | `<ref>` | `<YYYY-MM-DD>` |
| Project manager | `<name>` | Recorded | `<ref>` | `<YYYY-MM-DD>` |
