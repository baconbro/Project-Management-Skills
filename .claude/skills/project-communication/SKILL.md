---
name: project-communication
description: >-
  Designs the project communication plan — audiences, channels, cadence, message
  tailoring, feedback loops, and escalation paths — so the right people get the
  right information in the right way at the right time. Use when the user wants
  to build a communication plan, decide who hears what and how often, tailor
  messages to executives versus the team versus customers, set up feedback or
  escalation routes, or fix communication breakdowns. Triggers: "communication
  plan", "comms plan", "stakeholder communication", "who needs to know",
  "reporting cadence", "escalation path", "communication matrix", "keep people
  informed". Turns the engagement strategy from stakeholder-management into
  scheduled messages. Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: discipline
  phase: cross-cutting
  related: [stakeholder-management, status-report, meeting-management]
license: MIT
---

# Project Communication

## Overview
Project communication is the discipline of moving the right information to the right people, in
the right form, on the right cadence — and getting signal back. It is the *vehicle* for the
engagement intentions set in `stakeholder-management`: that skill decides who you must influence
and to what end; this skill turns those intentions into a scheduled, owned plan. Most
"project" failures are really communication failures.

## When to use this skill
- The user needs a communication plan, comms matrix, or reporting cadence.
- The user must tailor messaging to different audiences (exec / team / customer).
- The user needs feedback loops or escalation paths defined.
- Do NOT use this to decide *who* the stakeholders are and *what stance* you need from them —
  use `stakeholder-management`, whose engagement strategy this plan operationalizes.
- Do NOT design a single recurring report or meeting here — use `status-report` and
  `meeting-management`; this skill schedules them as part of the whole.

## Methodology fit
- **Waterfall:** a formal communication management plan with a fixed cadence per audience.
- **Agile:** built-in events (standup, review, retro) plus a light plan for outside-team audiences;
  radiate information (boards, dashboards) over scheduled reports.
- **Hybrid:** team comms via agile events; governance and external comms via a planned cadence.

## Inputs you need
The stakeholder register and engagement strategy (from `stakeholder-management`), the governance
structure (who escalates to whom), and the available channels and tools. If you do not yet know
who the audiences are or what they need, run `stakeholder-management` first.

## Workflow
1. **List audiences and their information needs.** Pull each audience and its desired engagement
   from `stakeholder-management`; for each, state what they need to know and *why*. *Done: every
   key stakeholder group has a stated information need.*
2. **Choose the message and tailor it.** Decide the content and depth per audience — executives
   want outcomes and decisions; the team wants detail; customers want impact and timing. Pick a
   communication mode (push / pull / interactive). See `references/audience-tailoring.md`. *Done:
   each audience has a tailored message and mode.*
3. **Choose channels and cadence.** Match channel to audience and urgency (steering deck, email
   digest, chat, dashboard, demo) and set how often each fires. *Done: channel and frequency set
   per audience.*
4. **Assign owners and formats.** Name who produces each communication and in what format, and
   record it all in `assets/communication-plan.csv`. *Done: every entry has an owner and a format.*
5. **Define feedback loops.** For each audience, define how information comes *back* (office
   hours, retro, survey, comments) — communication is two-way. *Done: a return path per audience.*
6. **Define escalation paths.** Set the levels, triggers, and time-boxes for raising issues and
   decisions. See `references/escalation-paths.md`. *Done: a clear escalation ladder with triggers.*
7. **Schedule the vehicles.** Wire the plan to the recurring vehicles — `status-report` for the
   written cadence and `meeting-management` for the live one. *Done: the plan is on the calendar.*

## Quality checklist
- [ ] Every key audience has a stated information need and a tailored message.
- [ ] A communication mode (push/pull/interactive) is chosen per audience.
- [ ] Channel, frequency, owner, and format are recorded for every entry.
- [ ] Feedback loops give each audience a way to respond.
- [ ] Escalation paths have levels, triggers, and time-boxes.
- [ ] Recurring items are wired to `status-report` and `meeting-management`.

## Anti-patterns
- One channel and one message for everyone — execs drown in detail, the team starves of it.
- All push, no pull or interactive — broadcasting with no feedback loop.
- A plan with no owners, so "someone" sends updates and no one does.
- No escalation path, so issues either fester or jump straight to the sponsor unfiltered.
- Confusing activity (lots of messages) with communication (the message landed and was understood).

## Resources
- `references/audience-tailoring.md` — exec vs team vs customer messaging; push/pull/interactive.
- `references/escalation-paths.md` — escalation levels, triggers, and time-boxes.
- `assets/communication-plan.csv` — fill-in plan: audience, what, channel, frequency, owner, format.

## Related skills
- `stakeholder-management` — produces the engagement strategy this plan operationalizes.
- `status-report` — the recurring written vehicle this plan schedules.
- `meeting-management` — the recurring live vehicle this plan schedules.
