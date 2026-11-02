# Change Request Fields

Field definitions, the status vocabulary, the 1-5 impact anchors, and the rules
`scripts/change_impact.py` applies. A change request (CR) is one self-contained record; the
change log is the list of all of them.

**Ownership.** `change-request` owns the CR form (`assets/change-request-template.md`) and the
change log artifact (`assets/change-log.csv`). `change-management` owns the governance around
them: the change-control process, CCB membership, the approval tolerances, and verifying that
baselines were updated. If the two ever disagree on a tolerance, the change-management plan wins;
pass its numbers to the script with `--pm-limit-cost`, `--pm-limit-days`, `--ccb-limit-cost` and
`--ccb-limit-days`.

## The change log (`assets/change-log.csv`)

One row per CR, never deleted (a rejected CR stays as evidence). The shipped file holds the six
change requests of the sample Helios project (a fictional customer self-service portal used
throughout this catalog). SSO for customer logins is in Helios's baseline; CR002 only extends it to
partner logins.

| Column | Required | Meaning | Helios CR002 |
| --- | --- | --- | --- |
| `id` | yes (unique) | Stable id, never reused | CR002 |
| `title` | yes | What changes, in plain words | Extend SSO to partner logins |
| `raised_by` / `date_raised` | yes | Who asked and when | Ava Chen / 2026-07-08 |
| `status` | yes | See the status vocabulary below | Under assessment |
| `scope_impact` `cost_impact` `schedule_impact` | scored | 1-5 rating each, anchors below | 3, 3, 4 |
| `quality_impact` `risk_impact` | scored if present | 1-5 rating each, anchors below | 3, 4 |
| `cost_value` | for routing | Money the change adds (+) or saves (-), one currency | 18000 |
| `schedule_days` | for routing | Working days added (+) or saved (-) on the affected path | 10 |
| `decided_by` / `decision_date` | after decision | Person or board, and the date | (blank: pending) |

Extra columns are allowed and passed through by `--format csv` and `--format json`. Ratings
accept decimals (3.5 when a change sits between two anchors); blanks, values outside 1-5,
`nan`/`inf` are rejected with the row, id and column named.

## Status vocabulary

| Status | Meaning | Script group |
| --- | --- | --- |
| Raised | Logged; not yet assessed | pending |
| Under assessment | Impact, options and recommendation in progress | pending |
| Approved | Decided yes (with any conditions recorded); not yet implemented | committed |
| Rejected | Decided no; the row stays as evidence | declined |
| Deferred | Not now; record the revisit date in the decision conditions | declined |
| Implemented | Work done; baseline updates not yet verified | committed |
| Closed | Implemented **and** verified, all affected baselines updated | committed |

A rejected or deferred CR is never set to Closed; Closed always means "done and verified". A
"request more information" decision is not a status: it returns the CR to `Under assessment`
with the questions, who answers each and a return date.

## Form fields (`assets/change-request-template.md`)

- **Identification** — id, title, project, raised by / date, status.
- **Justification** — reason / driver; benefit or business-case impact; cost of doing nothing;
  urgency (the date a decision is needed and what happens if it is later).
- **Impact assessment** — a 1-5 rating plus real units for scope, cost, schedule, quality and
  risk; cost value and schedule days; secondary risks introduced (log them in the risk
  register); resources affected; the score, impact band and authority from the script.
- **Options** — at least two, always including "do nothing", each with pros, cons, cost and days.
- **Recommendation** — the option advised and why.
- **Decision** — approval authority (PM / CCB / Sponsor), decision, decided by / date,
  conditions, funding source, baselines to update, implementation owner, verification
  (verified by / date) and the date the CR was closed.

## 1-5 impact anchors

Rate each dimension at the **highest** row whose condition the change meets; use .5 between two
rows. The bracketed figures calibrate the anchors to Helios (PM tolerance $5,000 and 2 days;
contingency reserve $40,000 inside the $500,000 BAC; management reserve $25,000 above it; MVP to
pilot at M4, general availability at M6) — recalibrate them to your own tolerances.

| Rating | Scope | Cost | Schedule | Quality | Risk |
| --- | --- | --- | --- | --- | --- |
| 1 Negligible | No deliverable, requirement or acceptance criterion changes | Absorbed in existing estimates, no reserve drawn; or a saving | No task moves beyond its estimate range | No effect on acceptance criteria, tests or gates | No new risk; an existing risk unchanged or reduced |
| 2 Minor | Small change inside one work package; acceptance criteria unchanged | Within PM tolerance [<= $5,000] | Within PM tolerance [<= 2 days] or fully absorbed by float; no milestone moves | Minor test-plan change (test cases added or dropped) | A new LOW risk or a small rise in an existing one |
| 3 Moderate | One deliverable's features or acceptance criteria change | Draws contingency beyond PM tolerance, CCB decides [$5,001-$20,000] | Uses float or buffer beyond tolerance; an interim milestone moves, M4 and M6 hold | New acceptance criteria, or a regression/UAT cycle re-run | A new MEDIUM risk, or an existing risk's exposure rises materially |
| 4 Major | Several deliverables change, or a work package is added | Over half the contingency, or management reserve needed [$20,001-$40,000] | A critical-path task or the M4 pilot milestone moves; M6 holds | A non-functional target (performance, security, accessibility) or a gate's exit criteria change | A new HIGH risk, or a new dependency on the critical path |
| 5 Severe | A new deliverable (level-2 WBS element) added or one removed; an objective affected | Exceeds the contingency: new budget, business-case review or re-baseline [> $40,000] | General availability (M6) or a contractual milestone moves | A compliance, regulatory or safety obligation affected; acceptance re-planned | Threatens a project objective or exceeds the sponsor's risk appetite |

Helios check: CR001 (live chat, $60,000, 20 days) rates 5/5/5/3/3; CR005 (analytics vendor swap,
$4,000, 5 days on the critical Reporting & analytics task) rates 2/2/4/2/3.

## Scoring and the impact band

    score = (w_scope*scope + w_cost*cost + w_schedule*schedule + w_quality*quality + w_risk*risk)
            / (sum of the weights of the dimensions present)

All weights default to 1.0 (a plain average); raise one when that dimension matters most, e.g.
`--w-schedule 2` near a fixed launch date. Weights must be finite, above 0 and at most 1000.
Quality and risk are scored only when their columns exist, so an older three-column log still
works.

The **impact band** is HIGH (score >= 4.0), MEDIUM (>= 2.5) or LOW, tunable with `--high` and
`--medium` (1 <= medium < high <= 5). It measures impact **magnitude** — how hard the change hits
the baselines — not urgency and not business value. A cheap, urgent regulatory change is LOW
impact and may still be first on the agenda. Use the band to decide how deep the assessment goes
and who must approve; order the CCB agenda by urgency (needed-by date) and benefit. Equal scores
are ordered by id (CR2 before CR10) so the ranking never depends on file order.

## Approval authority

Printed when `cost_value` and/or `schedule_days` exist. Defaults follow the Helios tolerances in
`change-management`: the PM approves LOW-band changes of up to $5,000 and 2 working days
(inclusive) within contingency; the CCB decides above that; HIGH impact, a draw on management
reserve or a move of M6 goes to the sponsor.

| Authority | Rule | Helios example |
| --- | --- | --- |
| PM | LOW band **and** cost value within `--pm-limit-cost` (5,000) **and** days within `--pm-limit-days` (2); savings count by size; a blank value is never within tolerance | CR006 (-$3,000, 0 days, LOW) |
| CCB | Everything that is neither PM nor Sponsor | CR002, CR003, CR004, CR005 |
| Sponsor | HIGH band, or above the optional `--ccb-limit-cost` / `--ccb-limit-days` | CR001 (HIGH, $60,000) |

## Funding source

- **Contingency reserve** — inside the cost baseline, so drawing it moves money into a work
  package and leaves BAC unchanged (Helios: $40,000 inside the $500,000 BAC). Fits a change that
  is an identified risk materialising (Helios R002, undocumented requirements expand scope). Every
  dollar drawn is a dollar less of risk cover: tell the cost and risk owners.
- **Management reserve** — above the baseline and the sponsor's to release (Helios: $25,000).
  Using it raises BAC, so the cost baseline is re-issued.
- **New budget** — beyond both reserves; revisit the business case and re-baseline.
- **None** — the change saves money or is absorbed; record where a saving goes.

## Change burden

`change_impact.py` sums `cost_value` and `schedule_days` over the whole log by status group:
committed (Approved, Implemented, Closed), pending (Raised, Under assessment) and declined
(Rejected, Deferred; shown, not counted). With `--reserve-cost` it reports how much of the reserve
the committed and the committed-plus-pending changes would use. Helios with `--reserve-cost 40000`:
committed $12,000 (30.0%), committed + pending $42,000 (105.0%, over by $2,000) — each pending CR
looks affordable alone, together they overdraw the contingency. Summed days are an upper bound
because changes on parallel paths do not add; check the critical path in `project-schedule`.

## Sensitivity and explanation

- `--sensitivity` adds **Margin** (score minus the nearest threshold: +0.10 vs MEDIUM means 0.10
  above the MEDIUM line) and **Stable** (whether the band survives halving or doubling any one
  weight; if not, the perturbations that flip it). Helios: CR004 and CR005 sit 0.10 above MEDIUM
  and drop to LOW when scope (CR004) or schedule (CR005) is half-weighted — debate their ratings
  before relying on the band.
- `--explain` prints the formula with the numbers, each dimension's share of the score, the band
  rule that applied and the authority reason, so a board member can audit any row.
