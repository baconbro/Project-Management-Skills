# Decision & Action Logging

The value of a meeting leaks away in the hours after it if decisions and actions are not
written down. Capture them live, in the room, not from memory afterwards.

## Decisions

Record every decision as it is made, with enough context that someone reading it in three
months understands it without asking you. Each decision needs:

- **What was decided** — the decision itself, stated plainly.
- **Why** — the rationale and the main alternatives considered. This is what stops the
  decision being relitigated later ("why did we pick X?").
- **Who decided** — the decider or the group, and the method (consent, vote, decider).
- **When** — the date.
- **Status / reversibility** — final, or revisit-by-date if provisional.

A one-line decision log entry: *"2026-06-14 — Decided to launch Helios with email/password
login and add SSO as a fast-follow (CR001), to protect the launch date. Decider: sponsor."*

## Action items

Every action must have an **owner** and a **due date** — an action with neither is a wish.
Track them in `assets/action-items.csv` with these columns:

| Column | Meaning |
| --- | --- |
| id | Short identifier, e.g. AI001 |
| action | What will be done, starting with a verb |
| owner | One named person (not a team) |
| due | Target date |
| status | open / in-progress / done / blocked |

Rules that keep the list honest:

- **One owner per action.** Shared ownership is no ownership — the RACI rule applies here
  too. If two people must act, split it into two actions.
- **Verb-first, specific.** "Confirm identity-provider sandbox access with vendor" beats
  "identity provider".
- **A due date, always.** "ASAP" is not a date.
- **Carry forward, never drop silently.** Open actions are reviewed at the top of the next
  meeting until they are done or explicitly cancelled.

## Closing the loop

- Read decisions and actions back at the end of the meeting so owners confirm them aloud.
- Circulate the notes within a day while context is fresh.
- Open with last meeting's actions next time; ageing, unactioned items are a signal to
  escalate or kill them, not to keep copying them forward.
