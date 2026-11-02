# Meeting agenda and notes — <meeting name>

> Fill-in template: replace every `<placeholder>` and delete the rows you do not need. The same
> page is the agenda you send ahead and the sheet the scribe fills in live. A filled example
> is `agenda-sample.md`.

## Meeting
| | |
| --- | --- |
| **Project** | <project name> |
| **Meeting type** | <kickoff / stand-up / steering committee / stage-gate review / sprint review / change control board / decision workshop / other> |
| **Date, time and length** | <YYYY-MM-DD>, <start>–<end> (<minutes> min) |
| **Place or link** | <room and video link> |
| **Chair and decider** | <name and role - who decides; name a different decider per item if it differs> |
| **Facilitator / timekeeper** | <name> / <name> |
| **Scribe** | <name - not the facilitator; rotates> |
| **Attendees** | <name - role - why needed: decides / contributes / must hear it live> |
| **For one item only** | <name - item number> |
| **Receives the notes** | <names or distribution list - and any limits on what each may see> |

## Purpose (one sentence)
<Decide ... / Agree ... / Solve ... — if the honest purpose is "update", send a written update instead.>

## Outcomes needed by the end
- <decision, plan or answer 1>
- <decision, plan or answer 2>

## Pre-reads (sent by <YYYY-MM-DD> — two business days ahead for a decision meeting)
- <document> — <owner> — <what to look at and the question it supports>

## Agenda
| # | Time | Min | Item | Type | Owner | Method and decider | Outcome needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | <hh:mm> | 5 | Open: purpose, outcomes, decision methods; open actions by exception (overdue or blocked) | Inform | <facilitator> | — | Shared context; each blocked action has a next step |
| 2 | <hh:mm> | <min> | <decision item, written as the question to answer> | Decide | <presenter> | <decider decides after input / consent / consensus / majority vote> — <decider> | <decision logged with rationale> |
| 3 | <hh:mm> | <min> | <discussion item> | Discuss | <owner> | — | <owner and next step agreed> |
| 4 | <hh:mm> | <min> | <information item: questions on the pre-read only> | Inform | <owner> | — | <questions answered or logged> |
| 5 | <hh:mm> | 5 | Parking lot review | — | <facilitator> | — | Each item has an owner and next step, or is dropped |
| 6 | <hh:mm> | 5 | Read back decisions and actions | — | <scribe> | — | Owners confirm aloud |

Rules: decisions come first; status is a pre-read, not an item to read aloud; there is no "any
other business" item; the minutes add up to the meeting length.

## Parking lot
| Item | Raised by | Next step (later meeting / action / dropped) | Owner |
| --- | --- | --- | --- |
| <off-topic point> | <name> | <next step> | <name> |

## Decisions (captured live, then copied to `decision-log.csv`)
| id | Decision | Rationale | Options considered | Decided by | Method | Status / revisit by |
| --- | --- | --- | --- | --- | --- | --- |
| <D001> | <what was decided> | <why> | <options, chosen one marked> | <name> | <method> | <Final / Provisional / Deferred> <YYYY-MM-DD> |

## Action items (captured live, then copied to `action-items.csv`)
`source_meeting` is this meeting and `raised_on` is today's date for every row.

| id | Action (verb first) | Owner (one person) | Due | Notes |
| --- | --- | --- | --- | --- |
| <AI001> | <action> | <name> | <YYYY-MM-DD> | <dependency or blocker> |

## Close and follow-up
- [ ] Parking lot reviewed: every item has an owner and a next step, or was dropped by agreement.
- [ ] Decisions and actions read back; each owner confirmed aloud.
- [ ] Agreed what is shared with whom, and what stays confidential.
- [ ] Notes sent by <YYYY-MM-DD — within one business day>.
- [ ] Every decision and action merged into the issue log (decisions on change requests into the
      change log) and its id written to `log_ref` by <YYYY-MM-DD>.
- [ ] Next meeting <YYYY-MM-DD>: its agenda opens with this meeting's open actions.
