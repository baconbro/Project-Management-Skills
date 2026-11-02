# Meeting types and standing agendas

Load this to choose the right meeting for a purpose, to build its agenda from a standing
pattern, or to audit recurring meetings. Each type below states what the meeting is for, who
attends, its cadence and timebox, what it decides, and which skill owns its content; this skill
owns the mechanics (agenda, facilitation, capture, follow-through). Examples follow the sample
Helios project (a fictional customer self-service portal used throughout this catalog).

## Choosing the meeting
| Type | Purpose | Who | Cadence and timebox | Decides? | Content owned by |
| --- | --- | --- | --- | --- | --- |
| Kickoff | Align on purpose, scope, roles and ways of working; agree first actions | Sponsor, PM, core team, key stakeholders | Once per project or phase; 30–90 min | A few ways-of-working choices | `project-initiation` |
| Daily stand-up | Re-plan the day toward the goal; coordinate; surface blockers | The people doing the work | Daily; 15 min | Only the day's plan | `agile-delivery` (cadence) |
| Steering committee | Decide what exceeds the PM's tolerance; steer back to the baseline | Sponsor (chair), senior stakeholders, PM | Bi-weekly or monthly; 60 min | Yes, mainly | `status-report`, `project-delivery` |
| Stage-gate or milestone review | Go, go with conditions, recycle or stop against exit criteria | Gate approvers, PM, leads with evidence | At each gate; 60–90 min | Yes | `quality-management`; a release go/no-go: `release-and-cutover` |
| Sprint review or demo | Inspect working output against acceptance criteria; adapt the backlog | Team, product owner, stakeholders | End of each sprint; 1–2 h | Product owner accepts or rejects | `agile-delivery` |
| Change control board | Decide change requests above the PM's tolerance | CCB chair and members | A fixed slot, held when a request is pending; 30 min | Yes | `change-management`, `change-request` |
| Decision workshop or working session | Solve one problem or make one decision with the people who hold the knowledge | 3–8 people | As needed; 45–120 min | Yes, by the named decider | This skill |
| Vendor working session | Work open vendor actions, service levels and dependencies | PM or tech lead, supplier's delivery lead | Weekly; 30–45 min | Within the contract | `procurement-management` |
| Retrospective | Improve how the team works | The team only | End of each sprint or phase; 60–90 min | The team's own experiments | `lessons-learned`, `agile-delivery` |

If the purpose is only to share information, none of these is needed: send a written update.

## Kickoff
- **Content:** the charter walk-through, scope boundaries, roles and the path to planning come
  from `project-initiation` (its kickoff agenda and deck outline).
- **This skill adds:** named roles, a decision method for ways-of-working choices, a parking lot
  for scope disputes (each one becomes an action for the sponsor rather than a debate), first
  actions with owners and dates, and notes within one business day.
- **Smells:** a slide marathon with no questions; scope disputes argued in the room; no actions.

## Daily stand-up: a planning and coordination huddle
- **Purpose:** the people doing the work re-plan the next 24 hours toward the sprint or iteration
  goal, agree who works with whom, and surface blockers. It is not a status meeting: nobody
  reports to the project manager, and no minutes are written beyond the board and any new blocker
  in the issue log.
- **Who:** the team doing the work. The product owner and the PM may attend and listen; other
  stakeholders listen only. The facilitator is not the audience.
- **Timebox:** 15 minutes, same time, same place or link, every working day.
- **Format:** walk the board right to left (items closest to done first), asking what stops each
  item moving; or each person covers progress toward the goal, today's plan, and what is in the way.
- **Rules:** a blocker is raised the day it appears and gets an owner. Anything needing discussion
  moves to a follow-up huddle straight afterwards with only the people needed; decisions taken
  there are logged like any other. Helios: the stub decision (D003, issue-log DEC001) was taken in
  the follow-up after the 2026-06-16 stand-up by Ben Adeyemi with Ava Chen.
- **Smells:** people facing the PM while they speak; yesterday's activity with no plan for today;
  problem-solving that stretches the huddle to 30 minutes; the same blocker three days running; a
  board nobody updates.
- **Outside agile:** the same huddle works as a daily or twice-weekly coordination check in a
  waterfall build, test or cutover phase.

## Steering committee
- **Purpose:** decide what exceeds the PM's tolerance, steer the project back to its baseline, and
  remove obstacles only senior people can. Status is read before the meeting, not in it.
- **Inputs:** the status report as a pre-read; a decision paper per decision item (question,
  options, recommendation, decider, decide-by date); change requests above tolerance; the
  "for steering" list from the issue-log check in `project-delivery`.
- **Standing agenda (60 min):** open and open actions by exception (5); questions on the status
  pre-read (5); decisions in decide-by order (30–35); risks and dependencies needing sponsor
  action (5–10); parking lot (5); read-back (5).
- **Outputs:** decisions with rationale and options considered, actions with owners and dates,
  formal minutes approved at the next meeting's opening item.
- **When the steering committee also acts on change requests:** take them as a separate item
  under the change control board's rules (`change-management`) and record them in the change log.
- **Helios:** bi-weekly on Tuesdays, chaired by Dana Okoro, with an extra session within two
  business days if any dimension turns RED (D001). See `assets/agenda-sample.md` for the
  2026-07-14 agenda.

## Stage-gate or milestone review
- **Purpose:** decide whether the project passes a gate — go, go with conditions, recycle or
  stop — against exit criteria agreed in advance. Evidence is presented per criterion; opinions
  are not evidence.
- **Standing agenda (60–90 min):** the criteria and the evidence for each; open issues and risks
  carried into the next stage; the plan and baseline for the next stage; the verdict, with each
  condition owned and dated.
- **Owned elsewhere:** the gate's criteria in `quality-management`; a release go/no-go in
  `release-and-cutover`. Helios: gate G1 on 2026-05-08 approved the baseline at M1.

## Sprint review or demo
- **Purpose:** inspect working output against its acceptance criteria with stakeholders and adapt
  the backlog; show done items only, on working software.
- **This skill adds:** inviting the right stakeholders, holding the timebox, and capturing
  feedback as backlog items and actions. Helios: at the sprint S4 review on 2026-07-03, Ava Chen
  accepted the increment with conditions, which became action AI006 (issue-log ACT005); process
  audit QA-03 (`quality-management`) later logged that as a lapse, because two stories failing
  the definition of done should have been returned as not done.

## Change control board
- **Purpose:** decide change requests above the PM's tolerance within the remaining contingency;
  the process, tolerances and membership live in `change-management`, each request's assessment
  in `change-request`, and decisions in the change log.
- **Helios:** Tuesdays at 14:00 for 30 minutes, held only when a request is pending; Dana Okoro
  decides after hearing the members (CR003 approved with conditions on 2026-06-30, D004).

## Decision workshop or working session
- **Purpose:** one problem or one decision, with the 3–8 people who hold the knowledge.
- **Standing agenda (as shares of the time):** frame the question, the decider and the method
  (10%); generate options, silently first (25%); agree criteria and evaluate the options (40%);
  decide, or write the recommendation for the decider (15%); actions and read-back (10%).
- **Output:** a decision-log row with every option considered, or a recommendation with a
  decide-by date for the decider.

## Vendor working session
- **Purpose:** work the supplier's open actions, service levels and dependencies at working level;
  contractual remedies and escalation belong to `procurement-management`.
- **Helios:** weekly, Ben Adeyemi with IdentityCo; the recovery-plan action (AI001, issue-log
  ACT001) came from the session of 2026-06-12.

## Retrospective
- **Purpose:** improve how the team works, not what it builds. Formats (start-stop-continue,
  sailboat, 5 whys), lessons and following actions through belong to `lessons-learned`; its place
  in the sprint belongs to `agile-delivery`.
- **This skill supplies only facilitation:** a neutral facilitator who is not the team's manager,
  a team-only room unless the team invites others, a held timebox, and one or two owned actions.
  Retrospective actions go into the next sprint's backlog, not the issue log.

## The Helios meeting calendar
| Meeting | When | Owner or chair | Feeds |
| --- | --- | --- | --- |
| Daily stand-up | Daily, 15 min | The delivery team runs it; Sam Lee facilitates | Blockers to Sam Lee the same day; new issue-log items |
| Vendor working session | Weekly | Ben Adeyemi with IdentityCo | Vendor actions in the issue log |
| Weekly control review | Thursday | Sam Lee | The Friday status report; the "for steering" list |
| Sprint review and retrospective | Every second Friday | Ava Chen | Accepted increment; backlog items; lessons |
| Steering committee | Bi-weekly Tuesday, 60 min; extra session within 2 business days if RED | Dana Okoro (chair); Sam Lee facilitates | Decisions and actions merged into the issue log |
| Change control board | Tuesday 14:00, 30 min, when a request is pending | Dana Okoro | Decisions in the change log |

The weekly status report (Friday) is written, not a meeting; the cadence itself is set in the
communication plan (`project-communication`).

## Auditing a recurring meeting (keep, change or kill)
Run this at each milestone, or when a meeting keeps overrunning or nobody can say what it is for.

1. **Cost:** attendees × hours × loaded hourly rate × occurrences to the next milestone. Six
   people for an hour every two weeks is 13 meetings and 78 person-hours, about ten
   person-days, over six months.
2. **Purpose:** can the owner state it in one sentence, and is it still true?
3. **Output:** count the decisions and owned actions from the last four occurrences. None means
   it is an information meeting: replace it with a written update.
4. **Attendance:** who has not spoken or acted on anything in four occurrences? They move to the
   notes list.
5. **Timebox:** how often did it overrun, and which item caused it?
6. **Verdict:** keep, change (shorter, less frequent, fewer people, new standing agenda) or kill;
   tell the owner of the communication plan so the plan and calendars change.
