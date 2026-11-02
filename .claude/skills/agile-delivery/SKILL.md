---
name: agile-delivery
description: >-
  Runs agile delivery: backlog and INVEST user stories, sprint planning and review,
  velocity and burnup, and a release forecast range with a cut line
  (velocity_forecast.py). Use when writing or splitting stories, planning a sprint, or
  forecasting how many sprints are left or what scope fits a date.
metadata:
  version: 1.0.0
  category: discipline
  phase: delivery
  related: [senior-pm, project-planning, project-delivery, quality-management, estimation, status-report, meeting-management, lessons-learned]
license: MIT
---

# Agile Delivery

## Overview
Agile delivery builds the product in short, fixed-length iterations (sprints), each ending in
a tested increment that stakeholders inspect. Time and cost per sprint are fixed; scope flexes
through an ordered product backlog. This skill covers the backlog and user stories, the
definition of ready, the sprint events, velocity and burnup, release forecasting with velocity
ranges, and the bridge that lets an agile team report into a baselined project. The numbers
come from the sample Helios project (a fictional customer self-service portal used throughout
this catalog), whose portal build runs as two-week sprints inside fixed milestones: MVP live
to pilot at M4 and general availability (GA) at M6.

## When to use this skill
- The user wants to write, split, or review user stories, or set up, refine, or order a
  product backlog with a definition of ready.
- The user wants to plan the next sprint: a sprint goal and a commitment sized from capacity
  and velocity.
- The user wants to run sprint planning, the stand-up, or the sprint review, or run Kanban.
- The user asks "how many sprints are left?" or "will the Must-haves make the date?", or wants
  velocity, burndown, or burnup tracked.
- The user runs an agile team inside a baselined (hybrid) project and needs earned value from
  story points, the line between backlog change and a change request, or sprint metrics in a
  status report.
- Do NOT use this to size stories — planning poker and story-point technique live in
  `estimation`.
- Do NOT use this to set the definition of done or acceptance-criteria standards — use
  `quality-management`.
- Do NOT use this to choose between waterfall, agile, and hybrid — use `senior-pm`.

## Methodology fit
- **Waterfall:** not applicable as the delivery model (a fixed scope baseline has no backlog
  to reorder), except for an iterative sub-stream, such as a UI built in sprints inside a
  stage-gated programme, reported upward as a work package with milestones.
- **Agile:** native. The ordered backlog, sprints, increments, and a velocity-range forecast
  are the plan; the release goal and date hold, scope flexes, and the product owner reorders
  without a change request.
- **Hybrid:** iterations inside milestones. The baseline fixes milestones and budget (Helios:
  M4, M6, $500,000 BAC); sprints deliver the build work packages; a change request is raised
  only when a milestone, the budget, or committed Must-have scope moves.

How the catalog's control concepts map onto agile delivery:

| Catalog concept | Agile equivalent | Step |
|---|---|---|
| Scope baseline | Release goal plus ordered backlog; Must items are the commitment | 2, 4 |
| Schedule baseline | Milestones and sprint cadence; forecast as a velocity range | 4, 8 |
| Earned value | Accepted ÷ planned points × work-package BAC, never raw points | 8 |
| Change control | Product owner reorders; change request when a milestone, budget, or Must scope moves | 6 |
| Status RAG | Release outlook GREEN / AMBER / RED from forecast versus sprints left | 8 |
| Quality gates | Definition of ready at entry, definition of done at exit | 3, 7 |

## Inputs you need
The release goal, milestones, and budget (from the charter or `project-planning`); a product
owner with authority to order the backlog; the team and each member's usual availability; the
definition of done from `quality-management`; the backlog or raw requirements; and, to
forecast, the sprint history (committed and completed points, dates, release scope after each
sprint). If no one can order the backlog, stop and get a product owner named: an unordered
backlog cannot be forecast.

## Workflow
1. **Set up the delivery frame.** Agree the sprint length (two weeks by default), the roles
   (product owner orders and accepts; a facilitator runs the events; developers own the how),
   the release goal, the fixed constraints, the definition of ready (in
   `references/backlog-and-stories.md`), and the definition of done. Helios: Ava Chen is
   product owner and Sam Lee facilitates; sprints follow the schedule network: S1–S5
   (2026-05-11 to 07-17) build the portal, S6 runs system test and the pilot UAT, S7 launches
   the M4 pilot on 2026-08-07 and stabilises it, and S8–S10 (to 2026-09-25) cover hardening,
   pilot feedback, approved changes and GA readiness. *Done: cadence, roles, release goal, and
   both definitions are written down and agreed with the product owner.*
2. **Build the product backlog.** Copy `assets/product-backlog-template.csv`: one row per
   story in "As a … I want … so that …" form, Given/When/Then acceptance criteria, MoSCoW
   priority, status, and the `wbs_id` that traces it to the scope baseline. Order by value,
   risk, and dependencies. `assets/product-backlog-sample.csv` is the Helios GA backlog after
   S6: 19 open sized stories (Must 60, Should 24, Could 16 points), one unsized, and live
   chat marked Won't (deferred to phase 2 by CR001). *Done: every item has an id, story,
   priority, and status, and the top is in strict order.*
3. **Refine to ready.** Each week (at most 10% of capacity) split large items with the INVEST
   patterns in `references/backlog-and-stories.md`, size them with planning poker in
   `estimation`, and check them against the definition of ready, keeping about two sprints of
   ready work. Sized is not ready: Helios HEL-141 (SSO sign-in) stays `refined` until the
   vendor's production tenant is live (risk R001). *Done: the next two sprints of items meet
   the definition of ready and none of them is unsized.*
4. **Forecast the release.** Run the forecast against the backlog and the sprints left:
   ```bash
   python .claude/skills/agile-delivery/scripts/velocity_forecast.py .claude/skills/agile-delivery/assets/sprint-history-sample.csv --backlog .claude/skills/agile-delivery/assets/product-backlog-sample.csv --sprints-left 4
   ```
   It prints the velocity statistics, three scenarios (optimistic, likely, pessimistic),
   finish dates, the capacity and cut line per scenario, sprints to finish each priority
   tier, and the release outlook. Helios: velocity 22–31, trailing-3 28.00; 100 points left;
   4 sprints likely (2026-09-25), 5 pessimistic (2026-10-09) against 4 available, so AMBER.
   At the pessimistic velocity the cut line falls after HEL-170: Must, Should, and one Could
   story (87 points) fit and three Could stories (13 points) do not, so GA commits to Must and
   Should. Before three sprints exist, forecast by hand from a planned or borrowed velocity
   with a wide range (`references/metrics-and-forecasting.md`). *Done: a forecast quoted as a
   range with dates, a cut line, and the release commitment agreed with the product owner.*
5. **Plan the sprint.** Fill `assets/sprint-plan-template.md` in sprint planning (agenda in
   `references/ceremonies.md`): goal first, then capacity (available ÷ usual days × trailing-3
   velocity), then ready items in backlog order up to that capacity, one stretch item, and the
   skipped items with reasons. Helios S7, the pilot-launch sprint: 38 of 45 usual days (leave
   and pilot support) × 28.00 = 23.6, so 21 points (HEL-142, HEL-143, HEL-153, HEL-152), with
   the spare capacity kept for pilot defects; HEL-141 is skipped as not ready. *Done: one
   sprint goal, a commitment no larger than planning capacity, and every committed item
   ready.*
6. **Run the sprint.** Hold the 15-minute daily stand-up against the sprint goal, keep the
   board and sprint burndown visible, and clear blockers the day they appear. Apply the
   mid-sprint change rule: the goal holds; urgent work enters only by swapping out work of
   equal size with the product owner; a request that moves a milestone, the budget, or Must
   scope goes to `project-delivery` for a change request. *Done: blockers have owners within
   a day and every in-sprint scope change is agreed by the product owner.*
7. **Review and improve.** At the sprint review demonstrate only items that meet the
   definition of done, against their acceptance criteria; the product owner accepts or
   rejects each one; feedback enters the backlog. Append committed, completed, and release
   scope to the sprint history (format of `assets/sprint-history-sample.csv`; unfinished
   sprints may sit at the end with `completed_points` blank). Run the retrospective with a
   format from `lessons-learned` and put one or two owned actions into the next sprint.
   *Done: the sprint-history row is added, accepted stories are done, and each improvement
   action has an owner and a backlog item.*
8. **Report and bridge to the baseline.** Re-run the forecast after every review:
   ```bash
   python .claude/skills/agile-delivery/scripts/velocity_forecast.py .claude/skills/agile-delivery/assets/sprint-history-sample.csv --backlog .claude/skills/agile-delivery/assets/product-backlog-sample.csv --sprints-left 4 --format md
   ```
   and paste the velocity range, burnup, and outlook into the `status-report` (the outlook
   rule is in `references/metrics-and-forecasting.md`; the outlook and cut line need
   `--sprints-left N`). Where earned value is tracked,
   convert per work package: EV = accepted ÷ planned points × package BAC. At the end of S4
   (the month-3 snapshot) Helios Self-service UI had 57 of 81 points accepted, so EV =
   $47,500 of $67,500, matching `cost-management`. Watch the scope line: Helios grew from 246
   to 264 points (3.6 per sprint), which would push the likely forecast to 5 sprints. Escalate
   a RED outlook to the steering committee with options. *Done: the status report carries the
   range, burnup, and outlook; points-based EV reconciles with `cost-management`; any RED is
   escalated with options.*

## Quality checklist
- [ ] One named product owner orders the backlog; release goal and constraints are written.
- [ ] Every story has a story statement, Given/When/Then acceptance criteria, a priority, and
      a status; nothing in the next two sprints is unsized.
- [ ] Every committed item met the definition of ready, external dependencies included.
- [ ] Commitment ≤ trailing velocity × capacity factor, under a single sprint goal.
- [ ] Velocity counts only accepted, done stories; the sprint history has one row per sprint.
- [ ] The forecast is quoted as optimistic / likely / pessimistic with dates, never one date.
- [ ] Against a fixed date, a cut line is agreed and Must scope fits at the pessimistic
      velocity, or the outlook is reported AMBER or RED with options.
- [ ] Earned value comes from accepted ÷ planned points per work package, never raw points.
- [ ] Each retrospective yields at least one owned action that appears in the next sprint.

## Anti-patterns
- Setting velocity targets or comparing velocity across teams; points inflate and the
  forecast dies.
- Partial credit for unfinished stories, or silent carry-over that hides missed commitments.
- One finish date from average velocity, ignoring the range and scope growth.
- A release burndown on a release whose scope keeps changing; use a burnup.
- Splitting stories by technical layer so nothing is demonstrable at the review.
- A stand-up that is a status report to the project manager.
- "Agile means no plan": no release goal, no forecast, no cut line, then surprise at the
  milestone.
- A change request for every backlog reorder, or none when a milestone actually moves.

## Resources
- `references/backlog-and-stories.md` — backlog structure and WBS traceability, the user-story
  format, INVEST, acceptance criteria versus done, the definition of ready, splitting
  patterns, ordering (value, risk, WSJF, MoSCoW), and backlog health.
- `references/ceremonies.md` — purpose, timebox, agenda, outputs, and warning signs for each
  sprint event; Kanban cadences; aligning sprints with steering in a hybrid project.
- `references/metrics-and-forecasting.md` — velocity, predictability, burndown versus burnup,
  flow metrics, velocity-range forecasting with a cut line, the release-outlook RAG rule, and
  why story points are not earned value (with the per-package conversion).
- `assets/product-backlog-template.csv` — fill-in backlog (`<placeholders>`): id, story,
  acceptance_criteria, points, priority, status, sprint, wbs_id.
- `assets/product-backlog-sample.csv` — sample Helios GA backlog after sprint 6; input for
  `--backlog`.
- `assets/sprint-plan-template.md` — fill-in sprint plan (goal, capacity, commitment, done,
  risks, ceremonies, change rule, end-of-sprint record) with a labelled Helios sprint 7 sample.
- `assets/sprint-history-sample.csv` — sample Helios sprint history S1–S6 (committed,
  completed, dates, release scope, goal); the default script input.
- `scripts/velocity_forecast.py` — per-sprint table, velocity statistics, predictability,
  three-scenario forecast with finish dates, and text burnup. Options: `--remaining N` (points
  left), `--backlog FILE` (open points by priority, cut line), `--sprints-left N` (fixed-date
  check and outlook), `--window N` (trailing average, default 3), `--floor PCT` (flag sprints
  under this % of commitment, default 80), `--sprint-days N`, `--json`,
  `--format table|json|csv|md`; exit 0, or 2 with an `error:` line. Run
  `python .claude/skills/agile-delivery/scripts/velocity_forecast.py --help`.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `senior-pm` — recommends agile or hybrid delivery and routes sprint, backlog, and velocity
  questions here.
- `project-planning` — sets the milestones, budget, and rolling-wave plan the release goal
  sits inside, and takes the release forecast into the baseline.
- `project-delivery` — the monitoring-and-control loop that receives sprint outcomes and
  forecasts and raises change requests when a milestone, budget, or Must scope moves.
- `quality-management` — owns the definition of done and the acceptance-criteria standard
  every story is accepted against.
- `estimation` — sizes stories in points with planning poker; this skill turns those sizes and
  velocity into sprint commitments and release forecasts.
- `status-report` — carries the velocity range, burnup, and release outlook as the agile RAG
  line for the steering committee.
- `meeting-management` — facilitation mechanics (agenda, timebox, decisions, actions) for the
  sprint events defined here.
- `lessons-learned` — retrospective formats and action follow-through; each sprint's
  retrospective feeds it.
