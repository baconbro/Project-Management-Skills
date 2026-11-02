# Tailoring Messages to Audiences

Load this in steps 2–5 of the workflow: to decide what each audience gets, at what depth, in
which mode and channel, and how its feedback comes back. Examples use the sample Helios project
(a fictional customer self-service portal used throughout this catalog).

The same update lands very differently with an executive, a delivery team member and a customer.
Tailoring changes the *content, depth, framing, mode and channel* per audience while keeping the
facts identical. Mismatched messaging is the most common avoidable communication failure:
executives buried in detail tune out; teams given only headlines cannot act.

## Principles
1. **Change the framing, never the facts.** Every audience gets figures from one source — the
   weekly status report and the earned-value numbers behind it. Different numbers for different
   audiences destroy trust the first time two of them compare notes.
2. **Bottom line first.** Lead with the status and the ask; supporting detail follows for those
   who want it.
3. **One message, one ask.** If you need a decision, say which, from whom and by when.
4. **Internal before external; leaders before their teams.** Staff should never learn about a
   change from customers, nor a team from another department. Helios support agents hear about
   redeployment from Priya Nair, their own head of department, before anyone else.
5. **Bad news early, in person, then in writing.** Deliver it in an interactive setting, then
   confirm it in writing so the record matches what was said.
6. **Do not broadcast undecided problems.** Tell external audiences what is decided and what it
   means for them; tell internal decision-makers what is still open.
7. **Every message has a way back.** Each plan row names its feedback channel and who answers.

## Audience profiles

| Audience | Cares about | Depth and framing | Usual mode and channel | Feedback channel | Helios |
|---|---|---|---|---|---|
| Sponsor and steering committee | Outcomes, risks to them, decisions, money, dates | One page; RAG first, then the ask with options and a decide-by date; business impact, not technical cause | Interactive (1:1, steering) backed by a written pre-read | Decisions logged at the meeting | Dana Okoro weekly 1:1; bi-weekly steering |
| Approvers (security, legal) | What they must sign, when, and what changed since they last looked | Concise; their criteria and evidence; never a surprise at the gate | Push summary, Interactive at the gate | Findings logged as actions | Marcus Webb's fortnightly summary; Hana Sato's data-residency sign-off |
| Budget holder | Spend, forecast, reserve requests | Numbers with a one-line explanation; forecast flagged before steering | Push, Interactive before a reserve request | Questions answered within a set time | Finance's monthly EVM summary |
| Benefit owner and affected managers | The benefit, what changes for their people, their role in leading it | Detailed on the change, light on project mechanics | Interactive working sessions | Their concerns logged; they review staff messages | Priya Nair's bi-weekly working session |
| Delivery team | What to do next, dependencies, blockers, decisions that change their work | Detailed and specific; technical context welcome | Interactive (stand-up, sprint events) plus Pull (board) | Blockers raised the same day | Daily stand-up; sprint review every second Friday |
| Vendors | Milestones, blockers, acceptance, payment, changes | Contractual precision; only the contract owner instructs | Interactive working session and performance review | Actions logged; contract escalation ladder | IdentityCo weekly session and monthly review |
| Affected staff | What changes for me, when, what I must do, whom to ask | Plain language; "what this means for you"; no project jargon | Interactive briefing from their own leader, then Push and Pull (FAQ) | Huddle questions, pulse survey | 60 support agents' briefings and weekly huddle |
| Customers and end users | Impact, timing, what they must do, where to get help | Plain language, benefit-led, accessible | Push (email, in-product notice) with a feedback route | Feedback button, support queue, survey | 200 pilot customers' invitations and release notes |
| Neighbours (no action needed) | Dates and anything that collides with their plans | One line | Push to a distribution list, or Pull | Replies to a named owner | Marketing's GA launch list |

## One fact set, four framings (Helios, end of month 3)

The facts: overall AMBER at CPI 0.93 and SPI 0.92; the Identity / SSO integration work package is
RED after IdentityCo's sandbox outage (issue I001); EAC about $535,000 against the $500,000 BAC;
the steering committee decides IdentityCo's recovery plan and the reserve question (DEC002) on
2026-07-14.

| Audience | Framing | What they get |
|---|---|---|
| Dana Okoro and the steering committee | Decision | "Helios is AMBER (CPI 0.93, SPI 0.92). SSO integration is RED after the vendor's sandbox outage; the forecast is about $535,000 against the $500,000 budget and the M4 pilot date is at risk. Decision needed on 2026-07-14: approve IdentityCo's recovery plan and decide on management reserve — options and recommendation in the attached note." |
| Delivery team | Action | "SSO tests run against the stub until the sandbox returns, then repeat against the real provider; SSO work is now on the critical path, so it takes priority in sprint planning. Blockers to Ben Adeyemi the same day." |
| Finance | Numbers, early | "Forecast at completion about $535,000 against the $500,000 BAC (variance about -$35,000), driven by work package 1.3.1. A management-reserve request may reach steering on 2026-07-14; this is the advance flag." |
| Pilot customers and support agents | Nothing yet | No message: nothing has changed for them and nothing is decided. Once the pilot date is confirmed, they hear the date and what to do — and they hear it before any public announcement. |

## Communication modes (how information moves)

| Mode | What it is | Good for | Weak for | Helios example |
|---|---|---|---|---|
| **Push** | The sender delivers to named recipients | Routine updates, records, broad notices | Decisions, conflict, checking understanding | Weekly status report, release notes, Finance's cost summary |
| **Pull** | Recipients fetch it when they want | Reference detail, the long tail of information | Anything someone must act on by a date | Project dashboard, intranet FAQ, sprint board |
| **Interactive** | Real-time, two-way exchange | Decisions, alignment, conflict, bad news, nuance | Large audiences, a durable record on its own | Steering committee, 1:1, stand-up, sprint review, agent briefings |

Rule of thumb: the more a message depends on *shared understanding* — decisions, conflict,
sensitive or bad news — the more interactive it must be. Use push for routine information and a
written record; use pull for detail nobody needs on a schedule. Never let something an audience
must act on rely on pull alone.

**Mode mix by quadrant** (quadrants from `stakeholder-management`):

| Quadrant | Minimum mix |
|---|---|
| Manage Closely | At least one Interactive row, plus a written Push record |
| Keep Satisfied | Push summary at their cadence; Interactive at their gates and before any change in their area |
| Keep Informed | Push with a feedback route, plus Pull for detail; Interactive (a demo, a briefing) at major changes |
| Monitor | Pull, or a Push distribution list; re-rate at the next milestone |

## Choosing a channel
- Use a channel the audience **already monitors**; a new tool nobody opens is a dead letter.
- Match **richness** to sensitivity: face to face or video for bad news and conflict, written
  for facts and records.
- Decide whether it must be **synchronous** (a decision, a negotiation) or can be asynchronous.
- Decisions need a **durable record**: confirm in writing anything decided in a conversation.
- Check **reach and access**: shift workers, external customers and vendors may not see internal
  channels; time zones, languages and accessibility needs apply. Helios release notes meet the
  same WCAG 2.2 AA standard as the portal (CR003).

## Writing the message
A message an audience can act on has five parts:
1. **Headline** — the status or the news in one sentence.
2. **The ask** — what you need from them, by when, or "no action needed".
3. **Why it matters to them** — impact in their terms.
4. **What happens next** — dates and owners.
5. **How to respond** — the feedback channel and who answers.

## Tailoring checklist
- Could this audience act on the message as written? (right depth)
- Does the framing match what *they* care about, not what *you* find interesting?
- Are the figures the same as in the weekly status report?
- Is the channel one they actually monitor, and is the mode right for the content?
- Is there a way for them to respond, and does someone own the answer?

## Communication plan field guide

Columns of `assets/communication-plan.csv` (sample: `assets/communication-plan-sample.csv`):

| Column | Content |
|---|---|
| `id` | C01, C02, ... — stable; referenced by the review log |
| `audience` | A named person or a group that needs the same message at the same time |
| `stakeholder_ids` | Register ids separated by semicolons (S01;S02); `team` for the project team, which the register does not list |
| `purpose` | Why they need it and what you need back: a decision, a sign-off, an action, awareness or feedback |
| `message` | What they get, at the depth and framing they can act on; figures from the weekly status report |
| `mode` | Push, Pull or Interactive — one per row; a vehicle with a pre-read and a meeting is two rows or an Interactive row whose format names the pre-read |
| `channel` | The medium: meeting, 1:1, email, dashboard, in-product notice, briefing |
| `frequency` | A cadence (daily, weekly, bi-weekly, monthly) or an event (at a milestone, on a trigger) |
| `owner` | One named person who produces it |
| `format` | The template or form: one-page status report, pre-read and decision log, plain-language note |
| `feedback_channel` | How signal comes back, where it lands, and who answers by when |
| `effectiveness_measure` | An observable measure with a target that shows the message landed — not sends or opens (`references/monitoring-and-revision.md`) |
