# Sprint ceremonies

Each event exists to inspect something and adapt. If an event produces no decision or change,
shorten it or fix its agenda rather than skip it. Timeboxes below are for a two-week sprint
(the Scrum Guide's one-month maximums, scaled down). For facilitation mechanics — agendas,
parking lots, decision and action logs — use `meeting-management`; for retrospective formats
and following actions through, use `lessons-learned`.

| Event | Timebox | Attendees | Main output |
|---|---|---|---|
| Sprint planning | 4 h | Product owner, developers, facilitator | Sprint goal and committed items |
| Daily stand-up | 15 min | Developers (others listen) | Today's plan toward the goal; blockers named |
| Backlog refinement | at most 10% of capacity | Product owner, developers | Ready, sized items for the next two sprints |
| Sprint review | 2 h | Team plus stakeholders | Accepted increment; updated backlog and forecast |
| Retrospective | 1.5 h | The team only | One or two owned improvement actions |

## Sprint planning
- **Purpose:** agree why this sprint matters, what will be done, and how.
- **Inputs:** ordered backlog with ready items, trailing velocity, the capacity table, the
  definition of done, last retrospective's actions.
- **Agenda:** (1) product owner proposes the goal and the release context, 15 min;
  (2) capacity and reference velocity, 10 min; (3) select ready items in order up to the
  planning capacity, 60–90 min; (4) developers break items into tasks and confirm the
  commitment, 60–90 min; (5) confirm goal, commitment, and stretch, 10 min.
- **Outputs:** a completed `assets/sprint-plan-template.md`.
- **Smells:** committing to the best sprint on record; no goal, only a list; unready items
  accepted "to keep people busy"; the product owner absent.

## Daily stand-up
- **Purpose:** re-plan the next 24 hours toward the sprint goal. It is not a status report
  to the project manager.
- **Format:** walk the board right to left (closest to done first) and ask what stops each
  item moving; or each person covers progress toward the goal, plan, and impediments.
- **Rules:** same time and place, 15 minutes hard stop; problem-solving moves to a follow-up
  with only the people needed; a blocker is raised the day it appears and has an owner.
- **Smells:** people reporting to the facilitator; the sprint burndown flat for three days
  without anyone saying so; the same blocker repeated.

## Backlog refinement
- **Purpose:** turn the top of the backlog into ready items: split, clarify acceptance
  criteria, size (planning poker in `estimation`), surface dependencies.
- **Cadence:** one session a week; aim for about two sprints of ready work.
- **Output:** items marked `ready` in the backlog; spikes raised for what cannot be sized.

## Sprint review
- **Purpose:** inspect the increment with stakeholders and adapt the backlog and forecast.
- **Agenda:** (1) goal and what was done versus committed, 10 min; (2) demonstrate done
  items only, on working software, against their acceptance criteria, 45 min; (3) feedback and
  new ideas into the backlog, 30 min; (4) burnup, release forecast, and what comes next,
  20 min; (5) product owner accepts or rejects each item, 15 min.
- **Outputs:** accepted stories marked done; a new sprint-history row (committed, completed,
  release scope); the re-run forecast from `velocity_forecast.py`.
- **Smells:** slides instead of software; showing work that is not done; no stakeholders.

## Retrospective
- **Purpose:** improve how the team works, not what it builds.
- **Agenda:** set the stage, gather data (include the sprint metrics: delivered %, carry-over,
  blockers), generate insights, decide one or two actions, close. Rotate formats.
- **Output:** each action has an owner and appears as an item in the next sprint, so it
  competes for capacity like any other work. Recurring themes feed `lessons-learned`.
- **Smells:** ten actions and none done; the same complaint every sprint; managers present
  when the team does not want them.

## Kanban: the flow-based alternative
Use Kanban when work arrives continuously and unpredictably (support, operations, a small
maintenance stream). There are no sprints: visualize the workflow, limit work in progress
(WIP) per column, and pull work when capacity frees up.
- **Replenishment** (weekly): the product owner refills the "ready" column in order.
- **Daily stand-up**: same as Scrum, focused on flow and blocked items.
- **Service delivery review** (every two to four weeks): cycle time, throughput, aging items.
- **Forecasting** uses throughput (items per week) rather than story points; see
  `references/metrics-and-forecasting.md`.

## Hybrid: aligning the cadences
In a hybrid project the sprint events feed the governance rhythm instead of duplicating it.
The sample Helios project (a fictional customer self-service portal used throughout this
catalog) runs two-week sprints alongside a **bi-weekly** steering committee and a **weekly**
status report:
- Hold steering once per sprint, in the sprint's second week, and give it the latest review's
  forecast and burnup, so the sponsor (Dana Okoro) decides on current figures (Helios: steering
  on the Tuesday of each sprint's second week, e.g. S4 review Friday 2026-07-03 → steering
  Tuesday 2026-07-14).
- The weekly status report quotes the last review's figures mid-sprint and does not invent a
  mid-sprint velocity.
- Milestones (M4 pilot, M6 general availability) are release goals: the sprint review before
  each one checks the cut line, and a slipping Must item is escalated to steering then.
- The project manager may facilitate the events, but the product owner (Ava Chen) alone
  orders the backlog and accepts work.
