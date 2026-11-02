---
name: change-request
description: >-
  Writes and assesses one change request: impact on scope, cost, schedule, quality and
  risk, options, recommendation and approver, and keeps the change log (change_impact.py
  scores and routes requests). Use when raising, assessing, ranking or deciding a change.
metadata:
  version: 1.1.0
  category: artifact
  phase: delivery
  related: [project-delivery, change-management]
license: MIT
---

# Change Request

## Overview
A change request (CR) is the single, self-contained record of one proposed change to an agreed
baseline: what it is, why it is needed, what it does to scope, cost, schedule, quality and risk,
the options, a recommendation, and the decision with its funding and follow-through. Done well it
lets the right decision-maker say yes or no on evidence in minutes. This skill owns the CR form and
the change log artifact, `assets/change-log.csv`; `change-management` owns the governance around
them (the process, the change control board (CCB), its tolerances, and verification). The examples
use the sample Helios project (a fictional customer self-service portal used throughout this
catalog): its six change requests CR001-CR006 are the rows of the shipped change log. SSO for
customer logins is part of the Helios baseline; CR002 asks to extend it to partner logins.

## When to use this skill
- Someone proposes new scope, a cut, or a different approach, and you need its impact and a decision.
- The user wants to write, assess, or record the decision on one specific change request.
- The user wants to rank pending CRs by impact, see who must approve each one, or check whether
  the pending changes together fit the reserve.
- Do NOT use this to design the change-control process, constitute the CCB or set approval
  tolerances — use `change-management`, which links back here for the form and the log.
- Do NOT use this for a problem that has already happened — log it as an issue in
  `project-delivery`; raise a CR only if fixing it changes a baseline.

## Methodology fit
- **Waterfall:** every change to the signed-off scope, cost or schedule baseline gets a CR; it is
  assessed on all five dimensions and decided by the authority the tolerances name before any work
  starts, and the baselines are re-issued after approval.
- **Agile:** backlog reordering inside the agreed release goal is not a CR — the product owner
  decides. Raise a CR only when a change breaks a fixed constraint: the budget, the contract, the
  release date or a committed scope item; rate schedule impact in sprints converted to days.
- **Hybrid:** CRs for anything that moves the fixed frame (the Helios milestones M4 and M6, the
  $500,000 BAC, contracted scope); story-level churn stays in the backlog. Score the CR log at each
  steering meeting so the board sees the cumulative change burden, not one CR at a time.

## Inputs you need
- A plain-language description of the change, who raised it and when, and the urgency (the date
  a decision is needed by).
- The current baselines (scope/WBS, schedule, cost with contingency and management reserve) to
  rate impact against, and the 1-5 anchors in `references/change-request-fields.md`.
- The approval tolerances from `change-management` (Helios: the PM approves up to $5,000 and 2
  days; larger changes go to the CCB; HIGH-impact ones to the sponsor).
- Estimates in real units: cost value (+ adds, - saves) and schedule days; the affected tasks
  and whether they are on the critical path.

## Workflow
1. **Describe the change and give it an id.** Copy `assets/change-request-template.md`, take the
   next free id from `assets/change-log.csv`, and fill the header and section 1 in plain language,
   naming the deliverable or WBS element it touches. *Done: a reader who was not in the room
   understands what is being asked, and the CR has a unique id.*
2. **Justify it.** In section 2 of `assets/change-request-template.md` record the reason, the
   benefit or business-case effect, the cost of doing nothing and the needed-by date. *Done: the
   "why now" and the price of saying no are explicit.*
3. **Assess the impact on all five dimensions.** Rate scope, cost, schedule, quality and risk 1-5
   against the anchors in `references/change-request-fields.md` (decimals allowed) and give each
   a real-unit detail; estimate cost value and schedule days; log secondary risks in the risk
   register. *Done: five ratings, each with units and a one-line rationale.*
4. **Append the CR to `assets/change-log.csv`.** Add one row with `id`, `title`, `raised_by`,
   `date_raised`, `status` (Under assessment), the five `*_impact` ratings, `cost_value` and
   `schedule_days`. The shipped rows are the Helios sample — on a real project delete them and
   keep the header. *Done: the CR is in the log with every scored column filled.*
5. **Score, route and check the burden.** From the repo root:
   ```bash
   python .claude/skills/change-request/scripts/change_impact.py .claude/skills/change-request/assets/change-log.csv --status pending --reserve-cost 40000 --sensitivity --explain
   ```
   `scripts/change_impact.py` ranks the CRs by weighted impact score, assigns the impact band
   (HIGH >= 4.0, MEDIUM >= 2.5, else LOW) and the authority (PM / CCB / Sponsor), totals committed
   and pending cost value and days against the reserve, and flags bands that flip when one weight
   is halved or doubled. Helios: CR002 scores 3.40 MEDIUM (CCB), CR004 2.60 MEDIUM but
   weight-sensitive, CR006 1.60 LOW (PM); committed + pending would draw $42,000 of the $40,000
   contingency. *Done: the CR has a score, band, authority and margin, and the burden is known.*
6. **Lay out options and recommend one.** In sections 4-5 of
   `assets/change-request-template.md` compare at least "do nothing" and one alternative with
   pros, cons, cost and days, then give a clear recommendation and its conditions. *Done: at
   least two options and one recommended option with a reason.*
7. **Route for decision and record it.** Take the CR to the authority named in step 5 through the
   `change-management` process; complete section 6 of `assets/change-request-template.md` — the
   decision, decider and date, conditions, funding source (contingency reserve, management reserve
   or new budget), baselines to update and implementation owner — and update `status`,
   `decided_by` and `decision_date` in `assets/change-log.csv`. *Done: decision, decider, date,
   funding and baselines are recorded on the form and in the log.*
8. **Implement, verify and close.** The implementation owner does the work (status Implemented);
   `change-management` verifies that every affected baseline was updated; record "verified by /
   date" in `assets/change-request-template.md` and set the status to Closed in
   `assets/change-log.csv`. *Done: the CR is Closed only after verification.*

Status vocabulary: Raised → Under assessment → Approved / Rejected / Deferred → Implemented →
Closed (implemented and verified). Rejected and Deferred rows stay in the log.

## Quality checklist
- [ ] The CR has a unique id, a plain-language description, a raiser, a date and a needed-by date.
- [ ] Justification states the reason, the benefit and the cost of doing nothing.
- [ ] All five dimensions are rated 1-5 against the anchors, each with real units.
- [ ] The CR is a row in `assets/change-log.csv` and `change_impact.py` has scored it.
- [ ] The decision went to the authority the script named (or the deviation is explained).
- [ ] At least two options (one is "do nothing") and a recommendation are recorded.
- [ ] Decision, decider, date, funding source, baselines to update and implementation owner are recorded.
- [ ] Closed only after verification that every affected baseline was updated.

## Anti-patterns
- Approving a change verbally with no record of impact, funding or decision.
- Reading the impact band as priority — a cheap, urgent regulatory change is LOW impact and may
  still go first; order the agenda by urgency and value.
- Rating every change HIGH so the bands, and the routing, lose meaning.
- Approving CRs one at a time until, together, they have quietly spent the whole contingency.
- Offering one option and calling it a decision.
- Marking a CR Closed when the work is done but the baselines were never updated.
- Deleting rejected or deferred CRs from the log, losing the audit trail.

## Resources
- `references/change-request-fields.md` — log columns, status vocabulary, form fields, the 1-5
  anchors per dimension, scoring, authority routing, funding sources, burden and sensitivity.
- `assets/change-request-template.md` — fill-in CR form with placeholders.
- `assets/change-request-sample.md` — sample: the completed Helios CR003 form.
- `assets/change-log.csv` — the change log, shipped with the six Helios sample CRs (replace the
  rows, keep the header); also the scorer's input.
- `scripts/change_impact.py` — weighted impact score, impact band, authority routing, change
  burden; flags `--w-scope --w-cost --w-schedule --w-quality --w-risk`, `--high --medium`,
  `--pm-limit-cost --pm-limit-days --ccb-limit-cost --ccb-limit-days`, `--reserve-cost
  --reserve-days`, `--status`, `--sort`, `--sensitivity`, `--explain`, `--json`, `--format
  table|json|csv|md`. Run
  `python .claude/skills/change-request/scripts/change_impact.py --help` for columns, formulas
  and exit codes.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-delivery` — where change requests arise during execution; issues that need a baseline
  change become CRs here, and the decisions feed its decision log and status reporting.
- `change-management` — the change-control process, CCB and tolerances that decide and verify
  each CR; this skill supplies the form, the change log and the impact scores it decides on.
