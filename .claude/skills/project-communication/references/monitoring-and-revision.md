# Monitoring and Revising the Communication Plan

Load this in step 8 of the workflow. A communication plan is a hypothesis: that these messages,
through these channels at this cadence, will leave each audience informed enough to decide, act
or support. Monitoring tests the hypothesis; revision fixes what the test shows. Sending is
activity; communication has happened only when the audience understood the message and acted on
it. Examples use the sample Helios project (a fictional customer self-service portal used
throughout this catalog).

## Signals that a message landed

| Signal | What it shows | Strength | Helios measure and target |
|---|---|---|---|
| Decisions taken by their decide-by date | The decider understood the ask and had what they needed | Strong | Every steering decision by its decide-by date (C02) |
| Surprises: "I didn't know", or news reaching someone outside the ladder | A gap in reach, timing or mode | Strong (lagging) | No problem reaches Dana Okoro before Sam Lee has raised it (C01) |
| Ask-back: two or three recipients can state the key message and the ask | Understanding, not just receipt | Strong | Spot-check at the sponsor 1:1 and the agents' huddle |
| Behaviour: people do what the message asked | The message changed something | Strongest (lagging) | Portal-related contacts at L1 falling week on week in hypercare (C18) |
| Repeated questions on the same topic | The message was unclear, missing, or hard to find | Medium | Huddle questions answered within 1 week and moved into the FAQ (C13) |
| Feedback-channel response time | The way back works | Medium | Replies to the status report answered within 1 business day (C03) |
| Pulse survey ("I know what changes for me and when") | Self-reported understanding in a large group | Medium | At least 70% of support agents agree before cutover (C13) |
| Engagement moves in the stakeholder register | Communication plus engagement working together | Medium (slow) | Priya Nair moving from Neutral toward Leading (C04) |
| The right people attend and contribute | Reach for interactive rows | Weak to medium | At least one invited stakeholder at every sprint review (C12) |
| Sends, opens, page views | Activity only | Weak | Never a target on its own |

Give every key audience — at least each Manage Closely and Keep Satisfied stakeholder — one
strong or medium measure with a target in the plan's `effectiveness_measure` column. A weak signal
can support a strong one but never replace it.

## Review rhythm
- **Weekly (five minutes in the control review):** Did anyone say "I didn't know"? Is any
  feedback older than its response time? Did any decision miss its decide-by date?
- **Monthly sample:** pick two or three audiences, check their measures against target, and
  ask-back a few recipients.
- **Every milestone:** review the whole plan (Helios: M1, M4 and M6) together with the
  stakeholder register re-rating in `stakeholder-management`.
- **On a trigger, at once:**
  - a stakeholder is re-rated, added or changes role (Helios: Marketing re-rated at M4 starts
    the GA launch row);
  - a dimension or a work package turns RED (Helios: SSO, RED since the M2 close and escalated
    as DEC002 in month 3, tightened Finance's forecast flag);
  - an approved change touches an audience, or a proposed one would (a smaller pilot cohort
    changes who is invited and what they are told);
  - a measure misses its target twice in a row;
  - a release approaches (no later than six weeks (T-6) before go-live, add the release rows
    and hand the timed cutover-day steps to `release-and-cutover`) or closure approaches (add
    the closure notice).

## Diagnosing a message that is not landing

| Symptom | Likely cause | Fix |
|---|---|---|
| The sponsor is surprised at steering | Push only, or the pre-read arrived too late | A 1:1 before steering; pre-read 2 business days ahead; lead with the decision |
| Decisions slip past their decide-by date | The ask is buried, or the wrong person is asked | Put the decision in the first line, with options and the named decider |
| The same questions come back every week | The message is unclear or the answer is hard to find | Plain language; an FAQ (pull) fed by the questions; answer in the next push |
| Staff hear about changes from customers | Wrong sequence | Internal before external; leaders brief their teams first |
| Feedback goes somewhere other than the channel you set | The channel is not where people already are | Add the channel they use (Helios: pilot support tickets) and triage both |
| The status report goes unread | Too long, too late, or no ask | One page, Friday, decisions first; ask-back at the 1:1 |
| A vendor misses a blocker | Informal updates, no shared tracker | A weekly working session with a shared tracker and logged actions |
| Different audiences quote different numbers | Figures taken from different sources | One source: the weekly status report |

## Revising the plan
1. Change the affected rows in your copy of `assets/communication-plan.csv` — mode, channel,
   frequency, message, owner or feedback channel — and add rows for new audiences.
2. Retire a row only after asking its audience; silence is not consent to stop.
3. Raise the plan version and log the review in `assets/communication-review-log.csv`: the
   trigger, rows, measure, target, what you observed, the verdict (Landing, Partly landing, Not
   landing, New row), the change and the next review date.
4. Tell each affected audience what changes and when ("from next week the cost summary
   includes a forecast flag whenever EAC exceeds BAC").
5. If the change alters governance — the steering cadence, the escalation ladder, a tolerance —
   take it through the sponsor and record it in `project-planning`'s plan.

## Helios: reviews from M1 to the release window
`assets/communication-review-log-sample.csv` records seven reviews, plan versions 1.1 to 1.5:
- **M1 (2026-05-08):** the steering cadence was confirmed as bi-weekly through GA, with an extra
  session within 2 business days if any dimension turns RED (DEC003).
- **Monthly sample (2026-06-05):** only 41% of support agents knew what would change for them —
  not landing — because no message yet covered redeployment; briefings were booked for the week
  the redeployment plan is agreed, and huddle questions now feed an FAQ.
- **Trigger (2026-06-30):** SSO escalated as DEC002; Finance received the forecast flag two weeks
  before the 2026-07-14 steering decision, and the vendor review moved to the week before each
  steering.
- **Monthly sample (2026-07-03):** agents' pulse up to 58% (partly landing); six pilot customers
  joined the usability test.
- **M4 review (2026-08-11):** pilot problems arrived as support tickets rather than through the
  feedback button, so pilot-tagged tickets joined the feedback channel; Marketing's GA row
  started.
- **Trigger (2026-08-21):** six weeks (T-6) before the 2026-10-03 cutover, the GA release row
  (C18) was added with Priya Nair as owner, and its timed steps went into the
  `release-and-cutover` runbook.

`assets/communication-plan-sample.csv` shows the plan at version 1.5, after these changes.
