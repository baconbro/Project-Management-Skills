---
name: meeting-management
description: >-
  Plans, runs and follows up project meetings — kickoff, steering committee,
  daily stand-up, gate and sprint reviews, decision workshops: a one-line
  purpose, the right people, a timeboxed agenda, a decision method chosen
  before debate, a parking lot, and decisions and actions captured live and fed
  into the issue log. Use when the user wants to write an agenda, run or
  facilitate a meeting, fix meetings that overrun or decide nothing, prepare a
  steering committee, or record what a meeting decided and who acts by when.
  Triggers: "meeting agenda", "run a meeting", "facilitate a workshop",
  "parking lot", "kickoff meeting agenda", "steering committee meeting",
  "stand-up keeps overrunning", "meeting minutes", "action items from the
  meeting", "meeting decision log", "our meetings go nowhere". For
  retrospective formats, use lessons-learned; for the project's issue and
  decision log, use project-delivery; for which meetings exist and how often,
  use project-communication. Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.1.0
  category: artifact
  phase: cross-cutting
  related: [project-initiation, project-communication, agile-delivery]
license: MIT
---

# Meeting Management

## Overview
A project meeting is expensive — six people for an hour is most of a working day — and earns its
cost only when it ends with something an email could not produce: a decision, a shared plan, or a
problem solved. This skill makes each meeting deliberate from invitation to follow-through: a
one-line purpose, only the people needed, a timeboxed agenda with pre-reads, a decision method
chosen before the debate, a parking lot, and decisions and actions captured live and read back.
Meeting capture is not the record: within one business day every action and decision moves into
the issue log kept by `project-delivery`, the project's system of record, so the project never
runs two action lists. Examples follow the sample Helios project (a fictional customer
self-service portal used throughout this catalog): sponsor Dana Okoro (VP Customer Operations),
project manager Sam Lee, a daily stand-up, a weekly status report and a bi-weekly steering
committee.

## When to use this skill
- The user needs an agenda, or wants to plan, run or improve a kickoff, steering committee,
  stand-up, stage-gate or sprint review, change board or decision workshop.
- Meetings overrun, drift, reopen settled questions, or end without owners and dates.
- A meeting must produce a decision, and the user needs the decider, the method and a record of why.
- Decisions and actions from a meeting need capturing and carrying into the project's log.
- Do NOT use this to decide which meetings exist, for which audiences and how often — use
  `project-communication` instead; this skill runs the meetings that plan schedules.
- Do NOT use this for the content of the project kickoff (charter walk-through, roles, first
  planning steps) — use `project-initiation` instead; this skill runs the kickoff meeting itself.
- Do NOT use this to choose a retrospective format or follow its improvement actions — use
  `lessons-learned` instead, and `agile-delivery` for where the sprint retrospective sits in the
  cadence; this skill supplies only neutral facilitation.
- Do NOT use this as the project's action or decision tracker — use `project-delivery` instead;
  its issue log is the system of record that this skill's capture sheets feed.

## Methodology fit
- **Waterfall:** governance meetings on the stage calendar — the kickoff, a steering committee on
  a fixed cadence, and stage-gate reviews that decide go, go with conditions, recycle or stop
  against the exit criteria in `quality-management`; formal minutes for steering and gates,
  approved at the next meeting; changes above the PM's tolerance go to the change control board
  (`change-management`).
- **Agile:** `agile-delivery` sets and timeboxes the sprint events; this skill supplies their
  mechanics — the stand-up as a 15-minute planning huddle for the team, a review that shows
  working output against acceptance criteria, the product owner as decider on backlog questions,
  and light notes, with decisions on the board and in the log rather than in minutes.
- **Hybrid (Helios):** sprint events inside the team every two weeks; outside it a weekly vendor
  working session, a weekly control review, and a bi-weekly Tuesday steering committee chaired by
  Dana Okoro, with pre-reads two business days ahead and an extra session within two business
  days if any dimension turns RED. Sprint review outcomes feed the steering agenda, and every
  meeting writes to the one issue log.

## Inputs you need
- The purpose and the outcome needed: a decision, a plan, a solved problem, shared understanding.
- The decider and the decision rights (from `raci-matrix` or the charter) and the PM's tolerances
  (from `change-management`): they settle what this meeting may decide.
- The audience and the cadence slot from the communication plan (`project-communication`).
- Pre-reads: the latest status report (`status-report`), escalation notes, and change requests
  with their impact assessments (`change-request`).
- Open actions and decisions due, from the issue log (`project-delivery`), or from
  `assets/action-items.csv` when no issue log exists.
- Practical constraints: time zones, remote or hybrid attendance, recording and confidentiality.

If nobody can say what the meeting must decide or produce, stop at step 1: that is the finding.

## Workflow
1. **Decide whether to meet, and why.** Write the purpose and the outcome in one sentence each
   ("Decide ...", "Agree ..."). If the purpose is only to inform, send a written update instead
   (`status-report`). Pick the meeting type and its standing agenda in
   `references/meeting-types.md`. *Done: a one-line purpose and outcome exist, or the meeting is
   replaced by a written update.*
2. **Name the decider and the roles, then invite only who is needed.** Invite the decider, the
   people who contribute what the outcome needs, and anyone who must hear it live; everyone else
   gets the notes. Name the facilitator, scribe and timekeeper (`references/facilitation.md`).
   *Done: every invitee has a stated reason to attend and every role has a name.*
3. **Build and send the agenda.** Copy `assets/agenda-template.md`. Give every item a timebox, an
   owner, a type (Decide, Discuss or Inform) and the outcome it must reach; put decisions first,
   status as a pre-read with questions only, last meeting's open actions at the top and the
   read-back at the end. Send it with the pre-reads two business days ahead of a decision
   meeting (Helios: the Friday before the Tuesday steering, `assets/agenda-sample.md`).
   *Done: agenda and pre-reads sent on time; every item has a timebox, an owner and an outcome.*
4. **Open and facilitate.** Open with the purpose, outcomes and ground rules; hold the timeboxes;
   park off-topic points; draw out quiet voices (`references/facilitation.md`). Before debating
   a decision, choose the method and say it aloud: **decider decides after input** (the default
   for most project choices), **consent**, **consensus** (only when everyone's support is needed
   for it to stick) or **majority vote** (a tie-break between acceptable options). Run a stand-up
   as a planning and coordination huddle, not a status meeting. *Done: every item ended on time
   or by an explicit choice to extend, park or take offline, and each decision named its method
   and decider first.*
5. **Capture decisions and actions live.** Write each decision in the agenda's decision table,
   then in `assets/decision-log.csv` (rationale, options considered, decided by, meeting, status,
   method, revisit date if provisional or deferred). Write each action in
   `assets/action-items.csv`: verb first, one named owner, `source_meeting`, `raised_on` and a
   due date. Rules are in `references/decision-logging.md`; Helios rows are in
   `assets/decision-log-sample.csv` and `assets/action-items-sample.csv`. *Done: no decision or
   action exists only in someone's head.*
6. **Close.** Review the parking lot — each item gets an owner and a next step, or is dropped by
   agreement — then read back every decision and action so owners confirm them aloud.
   *Done: owners accepted their actions in the room and the parking lot is empty.*
7. **Feed the system of record and follow through.** Within one business day, send
   action-oriented notes and merge every decision and action into the issue log
   (`.claude/skills/project-delivery/assets/issue-log.csv`), writing its id back in `log_ref`;
   change-request decisions go to the change log (`change-request`), retrospective improvement
   actions to the next sprint backlog and `lessons-learned`. Before the next meeting, run the
   issue-log check from `project-delivery` on your log and open the agenda with its overdue,
   blocked and "for steering" items; on the Helios sample it lists DEC002, I001 and ACT003:
   `python .claude/skills/project-delivery/scripts/issue_log_check.py .claude/skills/project-delivery/assets/issue-log-sample.csv --as-of 2026-07-10`.
   An action that slips twice, or is carried through two meetings without progress, is
   escalated, re-planned or closed with a reason. *Done: notes sent, every captured row has a `log_ref`, and
   no open action has been copied forward a third time.*
8. **Audit recurring meetings.** At each milestone, or when a meeting keeps overrunning, run the
   keep, change or kill audit in `references/meeting-types.md` (cost, purpose, output,
   attendance, timebox) and tell the owner of the communication plan. *Done: every recurring
   meeting has a verdict and the calendar matches it.*

## Quality checklist
- [ ] The agenda states a one-line purpose and outcome; every item has a timebox, an owner, a
      type (Decide, Discuss, Inform) and an outcome, and the timeboxes add up to the length.
- [ ] The decider, facilitator, scribe and timekeeper were named before the meeting; every
      invitee has a stated reason to attend.
- [ ] Pre-reads went out at least two business days before a decision meeting; nobody read
      status aloud.
- [ ] The decision method and the decider were named before each decision was debated.
- [ ] Every row in `decision-log.csv` has a rationale, at least two options considered, a named
      decider, a meeting, a status and a method; Provisional and Deferred rows have `revisit_by`.
- [ ] Every row in `action-items.csv` starts with a verb and has one named owner, a
      `source_meeting`, a `raised_on` date and a due date.
- [ ] The parking lot was reviewed: every item has an owner and next step, or was dropped.
- [ ] Decisions and actions were read back and owners confirmed them before the close.
- [ ] Notes went out within one business day, and every captured row has a `log_ref` to the issue
      log or the change log (or `local` where no issue log exists).
- [ ] No open action has been carried through two meetings without progress, escalation or a new plan.
- [ ] The stand-up ends within 15 minutes; its problem-solving happened in follow-ups.
- [ ] Every recurring meeting was audited at the last milestone.

## Anti-patterns
- A recurring meeting with no purpose or agenda that nobody would miss if it were cancelled.
- Inviting everyone "to be safe", so nobody feels responsible and the decider is outnumbered by
  observers.
- Reading the status report aloud instead of sending it ahead and spending the time on decisions.
- The stand-up as a status report to the PM, or as a problem-solving session that runs 30 minutes.
- Debating before naming the decider and the method, then finding at the end that nobody can decide.
- An "any other business" slot where unprepared items ambush the group; use the parking lot.
- Actions with no owner, a team as owner, or "ASAP" as the date.
- A second action list in the meeting notes that never reaches the issue log — two lists, neither
  trusted.
- Copying the same overdue action forward meeting after meeting instead of escalating or closing it.
- Reopening a settled decision because its rationale and the options rejected were never written down.

## Resources
- `references/meeting-types.md` — purpose, attendees, cadence, timebox and standing agenda per
  meeting type; the stand-up as a coordination huddle; the Helios meeting calendar; the keep,
  change or kill audit for recurring meetings.
- `references/facilitation.md` — roles, preparation, opening, timeboxing, the parking lot, the four
  decision methods with the default and a fallback, participation techniques, difficult moments,
  remote and hybrid meetings, and the close.
- `references/decision-logging.md` — capture sheet versus system of record, routing table, decision
  and action columns, the transfer into the issue log, ageing rules, and notes versus minutes.
- `assets/agenda-template.md` — fill-in agenda and live capture sheet (`<placeholders>`): roles,
  purpose, pre-reads, timeboxed items, parking lot, decisions, actions, close and follow-up.
- `assets/agenda-sample.md` — sample Helios steering committee agenda for 2026-07-14 (DEC002,
  contingency priority for CR002, DEP002).
- `assets/decision-log.csv` — fill-in decision log: id, date, decision, rationale,
  options_considered, decided_by, meeting, status, method, revisit_by, log_ref.
- `assets/decision-log-sample.csv` — sample Helios decision log as of 2026-07-10: five decisions,
  including a deferral, each traced to its issue-log or change-log id.
- `assets/action-items.csv` — fill-in action capture sheet: id, action, owner, source_meeting,
  raised_on, due, status, notes, log_ref.
- `assets/action-items-sample.csv` — sample Helios actions as of 2026-07-10: six actions from five
  meetings, one blocked and ageing, each traced to its issue-log id.
- Cross-skill helper used in step 7: `python .claude/skills/project-delivery/scripts/issue_log_check.py --help`
  for its columns and options.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-initiation` — owns the kickoff's content (charter walk-through, roles, the path to
  planning); this skill runs the kickoff meeting and captures its first decisions and actions.
- `project-communication` — decides which meetings exist, for whom and how often, and the
  escalation ladder that routes items to steering; this skill runs each meeting and sends its
  decisions and notes back to those audiences.
- `agile-delivery` — places sprint planning, the daily stand-up, the sprint review and the
  retrospective in the sprint cadence; this skill supplies their facilitation mechanics and the
  capture of their decisions and actions.
