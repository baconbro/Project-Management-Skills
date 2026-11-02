# Kickoff — content, agenda and the split with meeting-management

Load this in step 7. A kickoff turns an authorized project into an aligned team: everyone leaves
able to say why the project exists, how success will be proven, where the boundaries are, who
decides what, how the work will run, and what happens next. This file owns the **content**: what
must be said, which signed document it comes from, and what must come out. The **mechanics** —
the agenda form, timeboxes, the decider and decision method, facilitator and scribe, parking lot,
live capture and notes — belong to `meeting-management`. Examples use the sample Helios project
(a fictional customer self-service portal used throughout this catalog).

## Entry conditions
- The charter is signed (gate item 17) and the G0 verdict is Go or Go with conditions. A
  "kickoff" before that is a pitch meeting, and anything it agrees can be undone by the sponsor.
- The deck is built in a copy of `assets/kickoff-deck-outline.md` from the signed charter, the
  approved business case, the gate record and the stakeholder register — nothing new is
  invented on the slides.

## What the kickoff must achieve
1. Everyone can state the problem and the objective, with its baseline, target and benefit
   owner, in one sentence.
2. Everyone has heard the scope boundaries, with the out-of-scope list read aloud.
3. Each person knows their own role and who decides what. This is a **draft of roles** taken
   from the charter; the RACI matrix is built in `project-planning` with `raci-matrix` once
   the work is decomposed, so do not present one here.
4. The delivery approach and the governance cadence are understood.
5. The top risks, the biggest assumptions and the stop triggers are known.
6. The first planning actions each have one owner and a date.

## Who to invite (from the stakeholder register)
| Register quadrant or role | At the kickoff |
|---|---|
| Sponsor | Attends and opens: why this matters and what success looks like |
| PM, product owner, core delivery team | Attend |
| Benefit owners | Attend; they own the outcome the team is building toward |
| Other Manage Closely rows (key supplier, critical dependency) | Attend, or record a waiver and brief them separately |
| Keep Satisfied approvers (security, legal, finance) | Attend for the items they decide or accept, or get a separate briefing |
| Keep Informed groups (end users, customers, front-line staff) | Not invited; reached through the communication plan (`project-communication`) |
| Monitor | Notes only |

Give every invitee a stated reason to attend; `meeting-management` (workflow step 2) explains how.
The stakeholder register itself is confidential: circulate the draft of roles, not the register.

## Pre-reads (two business days ahead)
- The signed charter.
- A one-page summary of the business case: problem, options compared, recommended option,
  benefits with baselines and owners.
- The agenda, built in a copy of `.claude/skills/meeting-management/assets/agenda-template.md`.

## Content agenda (60 minutes; waterfall or hybrid)
| Min | Item | Source | Deck slide | Outcome |
|---|---|---|---|---|
| 5 | Open: purpose of the meeting, introductions, how decisions will be made today | — | 1 | Everyone knows why they are here and who decides |
| 5 | Why we are here (the sponsor speaks) | Business case section 2 | 2 | The problem and the cost of doing nothing in numbers |
| 7 | Objective and benefits, and how we will prove them | Charter section 2; business case section 5 (benefits register) | 3 | Objective, baseline, target, date and benefit owner understood |
| 3 | Why this option | Business case section 4 (options) | 4 | The three options and do-nothing; why the recommendation won |
| 9 | Scope boundaries | Charter section 3 | 5 | Out-of-scope list read aloud; disputes parked for the sponsor |
| 5 | Milestones, budget range and stop triggers | Charter sections 4, 5 and 10 | 6 | Dates, range and what would stop the project are known |
| 5 | Team and roles (draft) | Charter sections 8 and 9 | 7 | Each person knows their role and who decides; the RACI follows in planning |
| 5 | Delivery approach and cadence | Gate record section 2 | 8 | Approach, ceremonies and reporting rhythm understood |
| 5 | Top risks and assumptions | Charter sections 6 and 7 | 9 | Owners know which assumptions they must validate and by when |
| 3 | How we will plan | Gate record section 6 | 10 | The path to the baseline and its approval date |
| 8 | Next steps: parking lot, actions, read-back | `meeting-management` capture | 11 | Every action has one owner and a date; the parking lot is empty |

## Variants
- **Small agile team (up to about eight people):** 30–45 minutes; cut slides 4 and 6 to one
  line each, and keep the out-of-scope list.
- **Agile liftoff (half day):** this 60-minute content block, then the team's working agreement
  with `resource-management`, then a first backlog sketch and a draft definition of done with
  `agile-delivery` and `quality-management`.
- **Large waterfall programme:** 90 minutes with one slide per workstream, or a sponsor-led
  kickoff followed by workstream kickoffs that reuse slides 2–6 unchanged.
- **Remote or hybrid attendance:** follow the remote guidance in
  `.claude/skills/meeting-management/references/facilitation.md`; send the deck as a pre-read.

## What a kickoff may and may not decide
- **May decide** ways of working: meeting slots, where documents live, team tools, the sprint
  length when the approach is agile or hybrid. Name the method and the decider before each one.
- **May not decide** changes to the objective, scope boundaries, budget range or milestones.
  Those change the signed charter and need the sponsor's re-approval (`project-charter`), so
  park them as an action for the sponsor instead of debating them in the room.

## Who does what
| This skill (content) | `meeting-management` (mechanics) |
|---|---|
| What each item covers and the signed source it comes from | The agenda form, timeboxes and an owner per item |
| The invite list drawn from the register | A stated reason per invitee; facilitator, scribe and timekeeper named |
| Which decisions to expect (ways of working only) | The decision method named before debate; the decision log |
| Scope disputes go to the sponsor | The parking lot and its review before the close |
| The actions that start planning | Action capture, read-back, notes within one business day, the move into the issue log |

## After the kickoff
- Send the notes within one business day (`meeting-management`).
- Keep decisions and actions in copies of
  `.claude/skills/meeting-management/assets/decision-log.csv` and
  `.claude/skills/meeting-management/assets/action-items.csv` with `log_ref` set to `local`;
  they move into the issue log (`project-delivery`) when planning opens it.
- Give `stakeholder-management` what the meeting revealed: who engaged, which concerns came up.
- Hand off to `project-planning` (workflow step 8).

## Helios example (sample)
- **When and where:** Tuesday 2026-04-07, 10:00–11:00, Operations boardroom and video link.
- **Roles:** Dana Okoro opens and decides; Sam Lee facilitates and keeps time; Frank Müller is
  the scribe.
- **Attendees:** Dana Okoro, Sam Lee, Priya Nair (benefit owner), Ava Chen, Ben Adeyemi, Carla
  Diaz, Devin Patel, Elena Rossi, Frank Müller; Marcus Webb and Hana Sato for slides 5–7.
  Finance receives the notes. IdentityCo is not invited: its contract extension for customer
  sign-in is a planning-stage make-or-buy decision, so its account manager is briefed at the
  first vendor working session (gate waiver W1).
- **Decisions:** KD1 — daily stand-up at 09:30 and two-week sprints with the review and
  retrospective every second Friday (team consent, Ava Chen deciding if consent fails);
  KD2 — steering committee bi-weekly on Tuesdays from 2026-04-21, 60 minutes, chaired by Dana
  Okoro (decided by Dana Okoro after input).
- **Parking lot:** Priya Nair asked whether agent headcount will change (dis-benefit D001) →
  action K3 for Dana Okoro. Devin Patel asked about live chat → out of scope in the charter
  (phase 2 candidate); dropped by agreement.
- **Actions:**

  | Id | Action | Owner | Due |
  |---|---|---|---|
  | K1 | Open the project management plan and the assumptions log (`project-planning` step 1) | Sam Lee | 2026-04-10 |
  | K2 | Schedule the three Support Operations requirements workshops, co-led with Priya Nair | Ava Chen | 2026-04-10 |
  | K3 | Meet Priya Nair in person to agree the 50% target, the benefit baseline method and the redeployment approach (gate condition C1) | Dana Okoro | 2026-05-08 |
  | K4 | Book the threat-model review with Marcus Webb during Discovery | Ben Adeyemi | 2026-04-17 |
  | K5 | Give Hana Sato a 30-minute briefing on the portal's data flows | Sam Lee | 2026-04-24 |

The slide content is in `assets/kickoff-deck-sample.md`; the gate record that preceded the
meeting is `assets/initiation-gate-record-sample.md`.
