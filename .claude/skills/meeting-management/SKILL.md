---
name: meeting-management
description: >-
  Runs effective project meetings — kickoff, steering committee, stand-up,
  review, and retrospective — by setting a clear purpose and agenda, facilitating
  with timeboxing and a parking lot, and capturing decisions and action items so
  nothing is lost. Use when the user wants to plan, run, or improve a meeting,
  write an agenda, facilitate a session, timebox a discussion, or capture
  decisions and follow-up actions. Triggers: "meeting agenda", "run a meeting",
  "facilitate", "kickoff meeting", "stand-up", "steering committee", "retro",
  "action items", "meeting notes", "decision log". For the wider communication
  plan and stakeholder reporting, use project-communication. Works for waterfall,
  agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: artifact
  phase: cross-cutting
  related: [project-communication]
license: MIT
---

# Meeting Management

## Overview
Project meetings are where alignment and decisions happen — or where time goes to die. The
difference is preparation and discipline: a meeting with a stated purpose, a timeboxed
agenda, active facilitation, and captured decisions and actions earns its cost. One without
them does not. This skill makes every meeting deliberate.

## When to use this skill
- The user wants to plan, run, or improve a kickoff, steering, stand-up, review, or retro.
- The user needs an agenda, facilitation help, or a way to capture decisions and actions.
- Meetings are running long, drifting, or producing no follow-through.
- Do NOT use this for the overall communication plan, audiences, and reporting cadence —
  use `project-communication`.
- Do NOT use this to design a retrospective for closure lessons — use `lessons-learned`
  for the formats and follow-up (this skill runs the meeting; that one operationalizes it).

## Methodology fit
- **Waterfall:** scheduled governance meetings — kickoff, stage-gate reviews, steering.
- **Agile:** the ceremonies — planning, daily stand-up, review/demo, retrospective —
  timeboxed and outcome-focused.
- **Hybrid:** agile team ceremonies plus periodic governance/steering meetings.

## Inputs you need
The meeting's purpose, the right attendees (and only them), the decisions or outcomes you
need, any pre-reads, and a timebox. For recurring meetings, the open action items from
last time. The agenda template is in `assets/agenda-template.md`.

## Workflow
1. State the **purpose and desired outcome** in one sentence. If you cannot, the meeting
   should be an email. *Done: a one-line purpose and a clear outcome exist.*
2. Invite **only the people who decide, contribute, or must hear it live**; everyone else
   gets the notes. Fill `assets/agenda-template.md` with timeboxed items, an owner per
   item, and any pre-reads. *Done: agenda sent ahead with timeboxes and owners.*
3. **Facilitate** to the agenda using the techniques in `references/facilitation.md`:
   open with the purpose, hold timeboxes, use a parking lot for off-topic items, and pick
   a decision method (consent, majority, or decider-decides) before debating. *Done: the
   meeting stayed on its timeboxes; off-topic items went to the parking lot.*
4. **Capture decisions and actions as they happen**, following
   `references/decision-logging.md`: every decision recorded with its rationale, every
   action with an owner and a due date. *Done: no decision or action left in someone's
   head.*
5. **Close** by reading back the decisions and action items so owners confirm them, then
   log actions in `assets/action-items.csv`. *Done: owners verbally accepted their actions.*
6. **Follow through**: circulate notes within a day and review open actions at the start of
   the next meeting. *Done: notes sent; actions carried forward until closed.*

## Quality checklist
- [ ] The meeting has a one-line purpose and a desired outcome.
- [ ] Only necessary attendees invited; agenda sent ahead with timeboxes and owners.
- [ ] Timeboxes were held and off-topic items parked, not lost.
- [ ] Every decision is logged with its rationale.
- [ ] Every action has an owner and a due date in `assets/action-items.csv`.
- [ ] Notes circulated promptly; open actions reviewed next time.

## Anti-patterns
- A standing meeting with no agenda that no one would miss if cancelled.
- Inviting everyone "to be safe", so no one feels responsible to contribute.
- Reopening a decided point because the decision was never written down.
- Action items with no owner or no date — i.e. no action items.
- Letting the loudest voice set the agenda in the room instead of the stated purpose.

## Resources
- `references/facilitation.md` — roles, timeboxing, the parking lot, and decision methods.
- `references/decision-logging.md` — how to record decisions and actions so they survive.
- `assets/agenda-template.md` — fill-in timeboxed agenda for any meeting type.
- `assets/action-items.csv` — action-item tracker (id, action, owner, due, status).

## Related skills
- `project-communication` — the wider reporting plan and stakeholder channels these meetings serve.
