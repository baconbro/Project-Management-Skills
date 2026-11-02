---
name: project-communication
description: >-
  Builds the communication plan: who needs what, how and how often, from whom, feedback
  channels and an escalation ladder, then checks that messages land. Use when planning
  stakeholder updates, setting a reporting cadence or escalation path, or when people are
  surprised by decisions.
metadata:
  version: 1.1.0
  category: discipline
  phase: cross-cutting
  related: [project-planning, stakeholder-management, status-report, meeting-management, release-and-cutover]
license: MIT
---

# Project Communication

## Overview
Project communication moves the right information to the right people, in the right form and on
the right cadence, and brings signal back. It is the vehicle for the engagement strategy set in
`stakeholder-management`: that skill decides whom you must move and to what end; this one turns
each intention into an owned plan row — audience, purpose, message, mode (push, pull or
interactive), channel, frequency, owner, format, feedback channel and an effectiveness measure —
adds an escalation ladder whose triggers fire on the forecast, and then checks whether the
messages are landing and revises the plan. The plan is the document you circulate; the
stakeholder register behind it stays confidential. The worked example is the sample Helios
project (a fictional customer self-service portal used throughout this catalog): its ten
register rows (S01–S10), from the sponsor, Dana Okoro (VP Customer Operations), to the 200 pilot
customers, become 19 plan rows run by the project manager, Sam Lee, on a daily stand-up, a weekly
status report and a bi-weekly steering committee.

## When to use this skill
- The user needs a communication plan, communication matrix or reporting cadence, or must decide
  who needs to know what, how and how often.
- The user must tailor one update for executives, the delivery team, staff and customers.
- The user needs feedback channels or an escalation ladder with levels, triggers and time-boxes.
- Communication is failing: decisions stall, people say "nobody told me", reports go unread, or
  a sponsor hears bad news from someone else first.
- A milestone, a re-rated stakeholder, a RED dimension or an approaching release means the plan
  needs reviewing.
- Do NOT use this to decide who the stakeholders are and what engagement you need from each —
  use `stakeholder-management` instead; this skill schedules its strategy actions.
- Do NOT use this to write one status report or run one meeting — use `status-report` or
  `meeting-management` instead; this skill decides when they happen and for whom.
- Do NOT use this to time the cutover-day communications (runbook comms steps, command-center
  bridge updates, the go-live announcement, the rollback message) — use `release-and-cutover`
  instead; this skill gives it the audiences, channels, owners and escalation path.
- Do NOT use this to plan training, adoption or resistance work for a new way of working — use
  `change-management` instead.

## Methodology fit
- **Waterfall:** a formal communication plan baselined with the project management plan; a fixed
  cadence per audience; stage-gate reviews as the main interactive governance event; plan
  changes versioned and logged at each gate.
- **Agile:** the events carry team and product-owner communication (daily stand-up, sprint
  review, retrospective); boards and burnup charts radiate status as pull; a light plan covers
  only audiences outside the team, with the sprint review as their main channel; the plan is
  revisited at each release planning.
- **Hybrid (Helios):** sprint events inside the team; outside it a weekly status report
  (Friday), a bi-weekly steering committee (Tuesday) chaired by Dana Okoro with an extra session
  within 2 business days if any dimension turns RED, a weekly vendor working session with
  IdentityCo, and release communications at the M4 pilot and M6 general availability (GA)
  routed through `release-and-cutover`.

## Inputs you need
- The stakeholder register and engagement matrix from `stakeholder-management`: ids, quadrants,
  desired engagement, and each strategy action with its cadence and owner.
- The governance structure: sponsor, steering committee members, the PM's tolerances from
  `change-management`, and decision rights from `raci-matrix`.
- Milestones and the agreed governance cadence from `project-planning`; release dates from
  `release-and-cutover`; each vendor's contractual escalation ladder from
  `procurement-management`.
- The channels and tools people actually use, confidentiality and records rules, and language,
  accessibility and time-zone needs.

If no stakeholder register exists, run `stakeholder-management` first: a plan built without one
misses the quiet blockers.

## Workflow
1. **List audiences and what they need, from the register.** Copy `assets/communication-plan.csv`
   into your project folder (the bundled template stays blank). Write one row per audience and
   vehicle, put the register ids in `stakeholder_ids`, and state in `purpose` why they need it
   and what you need back (a decision, a sign-off, an action, awareness or feedback). Group
   people into one audience only when they need the same message at the same time; add the
   audiences the register omits — the delivery team, and the release and closure audiences.
   Helios: S01–S10 plus the team become 19 rows in `assets/communication-plan-sample.csv`.
   *Done: every register id appears in at least one row, and every row states its purpose.*
2. **Tailor the message.** In `message`, write what each audience gets at a depth and framing it
   can act on: the sponsor the bottom line and the ask, the team the detail, customers the
   impact, the timing and what they must do (`references/audience-tailoring.md`). Change the
   framing, never the facts: every figure comes from one source, the weekly status report and
   the earned-value numbers behind it. *Done: each row's message fits its audience, and every
   status figure traces to the same source.*
3. **Choose mode, channel and frequency.** Set `mode` to Push, Pull or Interactive by the rule
   in `references/audience-tailoring.md`: decisions, conflict and bad news need Interactive,
   routine updates Push, reference detail Pull. Pick a `channel` the audience already monitors
   and a `frequency` that matches its decision rhythm and the project's risk. Helios: daily
   stand-up, weekly status report, bi-weekly steering committee. *Done: every row has a mode,
   channel and frequency; every Manage Closely stakeholder has an Interactive row; nothing an
   audience must act on relies on Pull alone.*
4. **Assign an owner and a format.** In your copy of `assets/communication-plan.csv`, put one
   named person in `owner` — not "the team" or "PMO" — and the template or format in `format`
   (one-page status report, pre-read and decision log, plain-language note). *Done: every row
   has one named owner and a format.*
5. **Define the feedback channel.** In `feedback_channel`, say how signal comes back, where it
   lands and who answers by when: questions logged as actions, a reply-to with a named reader
   and a response time, a pulse survey, a feedback button triaged each sprint (feedback routes
   per audience in `references/audience-tailoring.md`). *Done: every row names where feedback
   lands and who answers it.*
6. **Set the escalation ladder.** Copy and fill `assets/escalation-ladder-template.md` using
   `references/escalation-paths.md`: three or four levels, each with a named owner, an authority
   limit taken from the tolerances in `change-management`, triggers on the forecast and a
   time-box, with each vendor's contractual ladder in parallel. Escalate cost while contingency
   remains: Helios goes to the sponsor when the forecast overrun is more than the remaining
   contingency can absorb (EAC above the $500,000 BAC) or more than half of the $40,000
   contingency is drawn before M4 — never only when the forecast passes the baseline plus all
   reserves. *Done: every level has an owner, an authority limit, objective triggers and a
   time-box, and the ladder is published with the plan.*
7. **Wire the plan to its vehicles and route the release.** Put every recurring row on a
   calendar: the written report through `status-report`; stand-ups, steering and reviews through
   `meeting-management`. Before a go-live, add release rows here (audiences, channels, owner,
   approved go-live and rollback message templates; Helios row C18 in
   `assets/communication-plan-sample.csv`) and hand the timed cutover-day communications to
   `release-and-cutover`. Publish the plan with the baseline in
   `project-planning`. *Done: every recurring row is on a calendar with its owner, release rows
   point to the cutover runbook, and the plan is where every audience can find it.*
8. **Monitor whether messages land, and revise.** Give every key audience (at least each Manage
   Closely and Keep Satisfied stakeholder) an observable `effectiveness_measure` with a target —
   decisions on time, no surprises, questions answered, a pulse score — never sends or opens.
   Ask about surprises at the weekly control review, sample two or three audiences a month, and
   review the whole plan at each milestone (Helios: M1, M4, M6) and on a trigger: a stakeholder
   re-rated or added by `stakeholder-management`, a dimension or work package turning RED, a change
   that touches an audience, a measure missed twice, or a release or closure approaching
   (`references/monitoring-and-revision.md`). Record each review in
   `assets/communication-review-log.csv` (Helios: `assets/communication-review-log-sample.csv`),
   change the rows and tell the affected audiences. *Done: every key audience has a measure with
   a target, every milestone and trigger has a log entry, and the log names the next review.*

## Quality checklist
- [ ] Every stakeholder register id appears in at least one row's `stakeholder_ids`, and the
      delivery team, release and closure audiences have rows.
- [ ] Every row has a purpose, message, mode, channel, frequency, owner, format and feedback
      channel; no cell is blank and no owner is a group.
- [ ] `mode` is Push, Pull or Interactive on every row; each Manage Closely stakeholder has an
      Interactive row; nothing that requires action relies on Pull alone.
- [ ] Every status, cost and schedule figure in the plan's messages comes from one source.
- [ ] Cadences match the governance agreed in `project-planning` (Helios: daily stand-up, weekly
      status report, bi-weekly steering committee) and every recurring row is on a calendar.
- [ ] The escalation ladder has named owners, authority limits, forecast-based triggers and
      time-boxes, and its cost trigger fires while contingency remains.
- [ ] Release rows exist before the go/no-go, with approved go-live and rollback message
      templates, and their timings sit in the `release-and-cutover` runbook.
- [ ] Every key audience has an effectiveness measure with a target; the review log has an entry
      for each milestone and trigger and a next review date.
- [ ] The plan contains no confidential judgements copied from the stakeholder register.

## Anti-patterns
- One message and one channel for everyone: executives drown in detail, the team starves of it.
- All push and no pull or interactive — broadcasting with no feedback channel, or bad news sent
  by email before anyone has heard it in person.
- Tailoring the facts instead of the framing, so the sponsor, Finance and the team hold
  different numbers.
- A plan with no named owners, so "someone" sends updates and no one does.
- Escalation triggers that fire only when the money is gone ("forecast over baseline plus
  reserve"), by which time the sponsor has no options left.
- Measuring sends and open rates: activity is not communication; a message has landed when the
  audience understood it and acted.
- Writing the plan once during planning and never revising it as people, risks and phases change.
- Telling customers about an undecided internal problem, or letting staff hear about a change
  from customers first.
- Circulating the confidential stakeholder register instead of the plan.

## Resources
- `references/audience-tailoring.md` — tailoring principles, audience profiles, one Helios fact
  set framed for four audiences, push/pull/interactive and the mode mix per quadrant, channel
  choice, message structure, and the communication-plan field guide.
- `references/escalation-paths.md` — levels, authority, forecast-based triggers and time-boxes;
  the Helios ladder and trigger table; why "baseline plus reserve" is too late; parallel vendor
  and cutover routes; the escalation note with the Helios DEC002 example.
- `references/monitoring-and-revision.md` — signals that a message landed (strong and weak),
  the review rhythm and revision triggers, diagnosing messages that do not land, and how to
  revise the plan.
- `assets/communication-plan.csv` — fill-in plan with `<placeholders>`; columns `id, audience,
  stakeholder_ids, purpose, message, mode, channel, frequency, owner, format, feedback_channel,
  effectiveness_measure`.
- `assets/communication-plan-sample.csv` — sample Helios plan at version 1.5: 19 rows covering
  S01–S10, the delivery team, the GA release and closure.
- `assets/escalation-ladder-template.md` — fill-in escalation ladder: levels and authority,
  triggers by dimension, parallel routes, the escalation note, and the rules everyone agrees to.
- `assets/communication-review-log.csv` — fill-in log of effectiveness reviews: date, review
  type, trigger, plan rows, measure, target, observed, verdict, change made, owner, plan version
  and next review.
- `assets/communication-review-log-sample.csv` — sample Helios review log from the M1 baseline
  approval to the GA release window.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-planning` — calls this skill in its engagement and communications step, sets the
  governance cadence the plan schedules, and baselines the plan and escalation ladder with the
  project management plan.
- `stakeholder-management` — supplies the register ids, quadrants and each strategy action with
  its cadence and owner; its re-ratings trigger a plan review here.
- `status-report` — the weekly written vehicle this plan schedules and the single source of the
  figures every audience receives.
- `meeting-management` — runs the live vehicles this plan schedules (stand-up, steering
  committee, sprint review) and logs their decisions and actions.
- `release-and-cutover` — takes the release audiences, channels, owners and escalation ladder
  from here and owns the timed cutover-day communications: runbook comms steps, bridge updates,
  the go-live announcement and the rollback message.
