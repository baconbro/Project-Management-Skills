# Decision and action logging

Load this when capturing what a meeting decided and who will do what, and when moving that into
the project's log. The value of a meeting leaks away in the hours after it if decisions and
actions are not written down: capture them live, in the room, not from memory afterwards.
Examples follow the sample Helios project (a fictional customer self-service portal used
throughout this catalog).

## Capture sheet versus system of record
Meeting capture — the decision and action tables on the agenda, `assets/decision-log.csv` and
`assets/action-items.csv` — is where the scribe writes during and straight after the meeting. It
is not where the project tracks work. The **system of record** is the issue log kept by
`project-delivery` (`.claude/skills/project-delivery/assets/issue-log.csv`): one place for the
project's issues, actions, decisions and dependencies. Within one business day of the meeting,
every captured row is merged there and the log's id is written back in `log_ref`. The project
then tracks the item only in the log, so it never runs two action lists.

| Captured in the meeting | Goes to | Owning skill |
| --- | --- | --- |
| Action | Issue log, type `action` | `project-delivery` |
| Decision on a project matter | Issue log, type `decision`, closed with the outcome; the full rationale stays in the decision log | `project-delivery` |
| Decision on a change request | Change log (status, decided by, date) | `change-request` |
| A new problem happening now | Issue log, type `issue` | `project-delivery` |
| A new risk or opportunity | Risk register | `risk-register` |
| A retrospective improvement action | The next sprint's backlog; recurring themes to the lessons log | `agile-delivery`, `lessons-learned` |
| A parking-lot item | An owner and a next step: a later agenda, an action, or dropped | this skill |

When the project keeps no issue log (a one-off workshop, a very small project), the two capture
files are the log: write `local` in `log_ref` and run the ageing rules below on them directly.

## Recording a decision
Record each decision as it is made, with enough context that someone reading it in three months
understands it without asking. `assets/decision-log.csv` has these columns:

| Column | Meaning |
| --- | --- |
| id | Sequential, D001 onwards; never reused |
| date | The date the decision was taken |
| decision | What was decided, stated plainly so it stands alone |
| rationale | Why: the deciding reasons, the evidence, any conditions, and any recorded dissent |
| options_considered | Every option weighed, at least two, with the chosen one marked; this is what stops the decision being relitigated |
| decided_by | The named decider, or the forum and its chair |
| meeting | Where it was decided: meeting name and date |
| status | Final, Provisional, Deferred, Superseded by Dnnn, or Reversed |
| method | Decider decides after input, consent, consensus, or majority vote |
| revisit_by | For a Provisional or Deferred decision, the date it comes back; blank when Final |
| log_ref | The issue-log `DEC` id or change-log `CR` id once merged; blank until then |

Rules:
- **Never edit or delete a decision.** A changed decision is a new row whose status is Final and
  whose rationale names what changed; the old row becomes "Superseded by Dnnn".
- **A deferral is a decision.** "Not today" is recorded with what is missing, who provides it and
  the revisit date, so it cannot drift.
- **Reopen only with new information**, through the decider, as a new agenda item.
- **Weak:** "SSO discussed; agreed to look at options." **Strong:** the row below.

Helios one-line form of D002: *"2026-06-16 — Deferred CR001, the live-chat widget, to phase 2.
At $60,000 and 20 days it would need more than the whole $40,000 contingency and would push the
M4 pilot; live chat is outside the chartered scope. Options: approve now, defer to phase 2,
reject. Decided by Dana Okoro (sponsor), decider decides after input, at the steering committee.
Final; recorded in the change log as CR001."* Single sign-on itself is in the baseline and was
never deferred. The full Helios set is in `assets/decision-log-sample.csv`; D005 shows a
deferral with its revisit date.

## Recording an action
Every action needs an **owner** and a **due date**; an action with neither is a wish.
`assets/action-items.csv` has these columns:

| Column | Meaning |
| --- | --- |
| id | Sequential, AI001 onwards |
| action | What will be done, starting with a verb, understandable by someone who was not there |
| owner | One named person, not a team |
| source_meeting | The meeting that raised it: name and date |
| raised_on | The date it was captured; never changes, so the action's true age stays visible |
| due | The do-by date |
| status | Open, In progress, Blocked or Closed — the issue log's own values, so the transfer is mechanical |
| notes | What blocks it (with the blocker's id), or how it closed: done, or cancelled and why |
| log_ref | The issue-log `ACT` id once merged; blank until then; `local` when there is no issue log |

Rules:
- **One owner per action.** If two people must act, split it into two actions.
- **Verb-first and specific.** "Agree a dated recovery plan with IdentityCo's account manager and
  claim the sandbox delay credit" beats "IdentityCo".
- **A date, always.** "ASAP" and "next week" are not dates.
- **Closed means done or cancelled with a reason**, never silently dropped.

## Moving rows into the issue log
| Capture column | Issue-log column |
| --- | --- |
| action / decision | `description` (for a decision, the question that was decided) |
| owner / decided_by | `owner` |
| source_meeting / meeting, and the capture id | `links` (for example "Steering 2026-06-30; AI005") |
| raised_on / date | `raised` |
| due / revisit_by | `due` |
| status | `status` (a Final decision is Closed; a Deferred one stays Open with `revisit_by` as `due`) |
| decision, decided_by, rationale, options_considered | `resolution`: what was decided, who decided, why, and the alternatives rejected |
| notes | `resolution` when the action closes |
| — | `impact` and `priority`, set by the PM at transfer |

Helios: AI005, raised at the steering committee of 2026-06-30, became ACT004 with links
"Steering 2026-06-30; I001; DEC002". Before each meeting, run the issue-log check from
`project-delivery` and open the agenda with what it lists:

```
python .claude/skills/project-delivery/scripts/issue_log_check.py .claude/skills/project-delivery/assets/issue-log-sample.csv --as-of 2026-07-10
```

As of 2026-07-10 it lists DEC002 and I001 for steering and ACT003 as blocked, which is exactly
what items 1 and 3 of `assets/agenda-sample.md` take.

## Ageing and carrying forward
- **Age** = the as-of date minus `raised_on`; in a spreadsheet, `=TODAY()-E2` with `raised_on` in
  column E. Rolling `due` forward never resets the age.
- **Open each meeting with actions by exception:** overdue, blocked, or due before the next
  meeting. Do not read the whole list.
- **First slip:** the owner gives a new date and a reason, recorded in `notes`.
- **Second slip, or carried through two meetings without progress:** escalate to whoever can
  unblock it, re-plan it as a new action, or close it as cancelled with a reason. Never copy it
  forward a third time.
- **Blocked:** name the blocker's id in `notes` and take it to the next forum that can unblock it.
- Helios, as of 2026-07-10: AI003 (ACT003), raised 2026-06-16, is 24 days old and blocked by issue
  I001, so it goes to the 2026-07-14 steering committee with DEC002 instead of being copied
  forward again.

## Notes, not transcripts
- Write action-oriented notes: purpose, attendees, decisions, actions, parking lot, and key points
  only where they explain a decision. Send them within one business day, while context is fresh.
- Governance meetings (steering committee, change control board, gate reviews) keep formal
  minutes: attendance and quorum, decisions with dissent recorded in the rationale, approved as
  the first item of the next meeting.
- Agree at the close what is shared with whom; keep confidential points (commercial positions,
  people matters) out of the general notes.
