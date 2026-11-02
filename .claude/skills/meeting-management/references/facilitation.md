# Facilitation

Load this when preparing to run a meeting, or when one keeps going wrong. Facilitation is the
discipline of helping a group reach its outcome efficiently: the facilitator owns the process,
the group owns the content, and the decider owns the decision. Examples follow the sample Helios
project (a fictional customer self-service portal used throughout this catalog).

## Roles
Name every role on the agenda before the meeting. One person may hold two roles in a small
meeting, but the scribe should not also facilitate.

| Role | Does | Helios steering committee |
| --- | --- | --- |
| Chair and decider | Holds the meeting's authority; makes or confirms each decision; named before the discussion starts | Dana Okoro (sponsor) |
| Facilitator | Runs the agenda and the process, stays neutral on content, draws out quiet voices, curbs dominant ones | Sam Lee (project manager) |
| Timekeeper | Calls the time at each timebox; often the facilitator, but a separate timekeeper spares the facilitator from being the only one enforcing the clock | Sam Lee |
| Scribe | Captures decisions, actions and parking-lot items live, on a screen everyone can see; the role rotates | Ava Chen (product owner) |
| Item owner | Prepares the pre-read and the options, presents, answers questions; never chairs their own item | Ben Adeyemi on DEC002 |

- When the facilitator has a stake in an item (a PM presenting their own recovery plan), say so,
  or hand that item to a neutral facilitator.
- Use a neutral facilitator who is not the team's manager for charged sessions: conflict, a
  failed release, a retrospective.

## Before the meeting
- Write the purpose and the outcome in one sentence each; choose the standing agenda for the
  meeting type in `meeting-types.md`.
- Ask each item owner: "What do you need from this group?" If the answer is "nothing", the item
  is a written update.
- For a decision item, the pre-read states the question, the options with their consequences, a
  recommendation, the decider and the decide-by date (the escalation-note format in
  `project-communication`).
- Send the agenda and pre-reads two business days ahead for a decision meeting, one business day
  for others. A pre-read sent the night before has not been sent.
- Prepare the shared capture page (the agenda in `assets/agenda-template.md`), the video link and
  the screen share before people arrive.

## Opening (the first five minutes)
1. The purpose and the outcomes needed by the end.
2. The agenda and its timeboxes. A missing item goes to the parking lot or a later meeting, never
   to "any other business".
3. Who decides each decision item, and by which method.
4. Ground rules, agreed once with a new group: one conversation at a time; devices away unless
   needed; challenge ideas, not people; decisions and actions are written down.
5. Last meeting's open actions, by exception only: those overdue or blocked, each given a next step.

## Timeboxing
- Put a duration on every agenda item; start on time even if people are late, and do not recap
  for latecomers.
- Two minutes before an item's timebox ends, ask: "Can we reach the outcome in two minutes?" If
  not, the group chooses explicitly: extend (and say what is cut), park it, or take it offline
  with named people and a date. The default is to park, never to overrun silently.
- Short meetings force focus: book 25 or 50 minutes rather than 30 or 60, and end early when the
  outcomes are reached.

## The parking lot
- Keep a visible parking lot for important points that are off-topic for this meeting.
  Capturing them lets the group move on without anyone feeling dismissed.
- In remote meetings, the chat is the parking lot's inbox; the facilitator reads it at the end of
  each item.
- Review it before the close: each item gets an owner and a next step (a later agenda, an action,
  or "dropped" by agreement). An unreviewed parking lot is a graveyard.

## Decision methods
Choose the method before debating, and say aloud which one you are using.

| Method | Use when | How | Watch for |
| --- | --- | --- | --- |
| **Decider decides after input** (the default) | One accountable owner exists and speed matters — most project choices | Each contributor speaks; the decider then states the decision and the reason in the room | "Input theatre": if the decider has already decided, say so and treat the item as Inform |
| **Consent** | A workable, reversible decision is needed fast; good enough beats perfect | A proposal, then "Any objection we cannot live with?" An objection must name the harm and suggest an amendment | Counting silence as consent, especially remotely: ask each person by name |
| **Consensus** | The decision needs everyone's active support to stick, such as a team working agreement | Discuss until everyone can support it; test with fist of five | The slowest method, and one holdout is a veto: set a fallback |
| **Majority vote** | A split group of equals needs a tie-break between options that are all acceptable | State the options, one vote each, simple majority | The losing side disengages; never vote on facts or on a choice one person is accountable for |

- Default to "decider decides after input" for most project choices; reserve consensus for the
  few decisions that truly need everyone's support.
- Always set a fallback: if consent or consensus is not reached by the end of the timebox, the
  named decider decides.
- Disagree and commit: once decided, record any dissent in the rationale, then everyone acts on
  the decision.
- Helios: the stub decision (D003, issue-log DEC001) was taken by consent — Ben Adeyemi proposed
  and Ava Chen and Carla Diaz had no objection; CR003 (D004) was decided by the CCB chair, Dana
  Okoro, after hearing the members.

## Getting everyone's input
- **Round-robin:** everyone speaks once before anyone speaks twice.
- **Silent writing first:** three to five minutes writing ideas alone before any discussion, so the
  group does not anchor on the first or loudest idea.
- **1-2-4-all:** alone, then pairs, then fours, then the whole group; useful above eight people.
- **Fist of five:** a show of zero to five fingers to test support; anyone at two or below explains.
- **Dot voting:** narrows a long list of options to a shortlist; it informs the decider, it does
  not decide.
- Ask the most senior person to speak last, so others do not simply echo them.

## Difficult moments
| Symptom | Move |
| --- | --- |
| One person dominates | Switch to round-robin; "Let's hear from someone who hasn't spoken yet"; talk to them at the break |
| Silence after a proposal | Ask people by name, or use silent writing; never record silence as agreement |
| A settled decision is reopened | Show the decision-log entry and its rationale; reopen only with new information, via the decider, as a new agenda item |
| Discussion sinks into detail or problem-solving | "Does everyone here need this?" Take it offline with named people and record an action |
| The decider is absent | Check whether a named delegate holds the authority; if not, turn the item into a recommendation with a decide-by date rather than make a decision that will be reversed |
| Conflict turns personal | Restate the shared goal, separate positions from interests, take a break, follow up one to one |
| Time is running out with decisions left | Take the decision with the nearest decide-by date; give the rest a forum and a date |
| Side conversations and multitasking | Restate the norm; shorten the meeting rather than tolerate it |

## Remote and hybrid meetings
- If anyone is remote, everyone joins from their own device, so remote attendees are not second
  class.
- Keep the capture page on the shared screen throughout; the scribe types where everyone can see.
- Use the raise-hand feature for turns and ask remote people first.
- Ask for cameras on during decision items; read the room through explicit checks, not faces.
- Rotate inconvenient time-zone slots; never take a decision that affects a region without its input.
- Hold remote meetings to 50 minutes without a break; workshops get a 10-minute break every hour.
- Ask consent before recording; a recording never replaces the notes.

## Closing (the last five minutes)
1. Review the parking lot: an owner and next step for each item, or dropped by agreement.
2. Read back each decision (what, who decided, by which method) and each action (what, who, by
   when); owners confirm aloud.
3. Agree what is communicated, by whom and to whom, and what stays confidential.
4. Check the outcome: "Did we get what we came for?" A recurring meeting that keeps missing its
   outcome needs the audit in `meeting-types.md`.
5. End on time, or early.
