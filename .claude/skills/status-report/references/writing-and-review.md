# Writing and Reviewing the Status Report

Load this in steps 1, 5, 6 and 8 of the workflow. A status report exists to get decisions made
and to stop surprises; everything in it should help a busy reader answer three questions in 30
seconds: *Where are we against the plan? What will happen if nothing changes? What do you need
from me?* Examples use the sample Helios project (a fictional customer self-service portal used
throughout this catalog); its filled report is `assets/status-report-sample.md`.

## 1. Anatomy, top to bottom (bottom line first)
| Section | What good looks like | Common failure |
|---|---|---|
| **Header** | Project, report number, status date, data cut-off, period, author, audience, distribution | No status date, so nobody knows how old the figures are |
| **Overall RAG** | Word plus colour, previous rating, trend arrow, and the red triggers for an AMBER | A colour with no previous rating or trend |
| **Summary** | Three sentences: the rating and why; the one thing the reader must know; the ask | A paragraph of activity |
| **Decisions needed** | Each with options, a recommendation, a decider, a decide-by date and what happens if nobody decides | "Support needed" with no decision named |
| **RAG by dimension** | Each row: measure, threshold met, forecast, owner and action for every AMBER or RED | A colour per row with no evidence |
| **Budget line** | BAC, AC, EV or % complete, EAC (formula), VAC, contingency and management reserve position, tolerance | "On budget" based on spend alone |
| **Milestones** | Baseline, forecast, variance, RAG, owner, recovery action | Forecast column copied from the baseline |
| **Progress** | Outcomes finished and accepted this period | "We held 12 meetings" |
| **Changes** | Approved, pending (with cost, days, decider, date), rejected or deferred this period | Pending changes invisible until they are approved |
| **Risks and issues** | The few the reader must act on or know, linked to the registers | The whole register pasted in |
| **Next period** | What will be true by the next report, with owners and dates | "Continue work" |

Keep it to one page or one screen. Detail goes behind links (EVM table, issue log, change log,
burnup), never above the decisions.

## 2. Writing a decision ask
A decision ask has six parts. Without them the steering committee discusses and does not decide.

1. **The decision** in one line, as a question that can be answered.
2. **Options** — two or three, each with its effect on cost, dates and scope.
3. **Recommendation** — which option and why, in one sentence.
4. **Decider** — one named person (a committee is not a decider; its chair is).
5. **Decide by** — the date after which options close.
6. **If no decision** — the concrete consequence.

Helios (2026-07-10 report): *DEC002 — approve IdentityCo's dated recovery plan, and draw
management reserve now or later? Options: (1) approve the plan and release management reserve
through change control; (2) also crash SSO with IdentityCo premium support, a $20,000 change
request (ACT004) that protects the M4 date but takes the CPI forecast to about $555,000, past the
$550,000 stop line; (3) trade scope through change control to stay inside BAC. Recommendation:
(1) now, and size the reserve draw once SSO works in test on 2026-07-17. Decider: Dana Okoro.
Decide by: 2026-07-14 steering. If no decision: the M4 pilot slips and the overrun grows unfunded.*

## 3. One fact set, several audiences
The figures never change between audiences; the depth and the framing do (see
`project-communication` for the full tailoring guide and the communication plan rows).

| Audience | Format | Leads with |
|---|---|---|
| Steering committee | The full one-page report as a pre-read, two business days ahead | Decisions, then RAG and trend |
| Sponsor 1:1 | The same report, discussed before it is sent: no bad news first read in writing | Anything turning AMBER or RED, and what you need from her |
| Delivery team | The report plus the sprint and issue detail behind it | Actions, blockers, dates that changed |
| Budget holder | The budget line and forecast, flagged the same week the forecast passes BAC | EAC, VAC and any reserve request |
| Portfolio or executive roll-up | One line: overall RAG, trend, the top issue, the ask | The ask |

Helios one-liner for the portfolio: *"Helios AMBER ↓ (prev AMBER): SSO vendor slip, EAC about
$535k vs $500k BAC; steering decides the recovery plan and reserve on 2026-07-14."*

## 4. When earned value is not tracked
Say which proxy you used, and keep using the same one.
- **Schedule:** milestone forecast vs baseline (the strongest proxy); milestones due this period
  met on their baseline date (for example "1 of 2 due"); for agile work the release forecast
  range against the sprints left (`agile-delivery`).
- **Cost:** spend to date as a % of budget against physical % complete — spend running ahead of
  progress is the warning; forecast = spend to date + run-rate × periods remaining.
- **Scope:** points or items added and removed since the baseline; changes pending.

Spend alone is never a cost measure: being 50% spent says nothing until you know how much of
the work is done.

## 5. Agile and hybrid reporting
- Report after the sprint review: sprint goal met or not, increment accepted or not, velocity as
  a range (average, minimum, trailing three), the release forecast against the sprints left and
  the cut line from `agile-delivery`'s `velocity_forecast.py`.
- Velocity is a forecasting input, not a productivity score: never compare teams by it or set
  targets on it.
- In hybrid projects the governance layer (milestones, EVM on the baselined work packages, RAG)
  sits on top and the sprint metrics are the evidence underneath. Helios on 2026-07-10: four
  sprints done (22, 27, 31, 29 points; average 27.25, minimum 22), 149 points left including
  CR003's 12, six sprints to the release (S5–S10, the last ending 2026-09-25): the likely forecast
  fits, the pessimistic one needs a seventh sprint (2026-10-09, after the 2026-10-03 GA cutover)
  and is 17 points short — so M6 is AMBER and 17 points of low-priority scope stay below the cut
  line.

## 6. Delivering bad news
- Tell the sponsor in person before the report goes out; the written report confirms what was
  said. Nobody should meet a RED for the first time in their inbox or at steering.
- Bring the decision with the problem: options and a recommendation, not just the bad news.
- AMBER early is a service, not a failure: it buys the sponsor time while options are cheap.
- Do not soften the colour to protect the team; protect the team by asking for help early.

## 7. Reviewing someone else's report
Use this when the user asks you to review or challenge a report. Mark each line PASS or FAIL
with the evidence.

1. Status date, period, cut-off and audience are stated.
2. Each dimension's colour cites a measure and the threshold it met (`rag-criteria.md`).
3. Cost and schedule are rated on the forecast (EAC/VAC, milestone forecasts), not to-date
   indices alone; after about 60% complete, not on SPI.
4. The overall rating is no greener than the worst material dimension.
5. The previous rating and a trend are shown, and any colour change has a changed measure.
6. Every AMBER or RED dimension, milestone and work package has an owner, an action and a date.
7. The scope row shows pending change requests with cost, days, decider and date.
8. Each decision has options, a recommendation, a decider, a decide-by date and a consequence.
9. Figures match the EVM output, issue log and change log of the same status date.
10. Risks and issues are linked to the registers, not duplicated.
11. Progress lists outcomes, not activity, and the whole fits one page or screen.
12. Ratings are written as words, readable without colour.

**Watermelon tests** — green outside, red inside. Challenge the report if any is true:
- GREEN cost with a negative VAC, or GREEN schedule with a key milestone forecast late.
- GREEN overall while a work package or interim milestone is RED and unnamed.
- SPI near 1.0 late in the project while the finish date has moved.
- The same AMBER for four or more reports with no owner, action or red trigger.
- A RED that turned GREEN without an approved change or a new forecast.
- Decisions "pending" for several reports with no decide-by date.

## 8. Cadence, cut-off and record
- Fix a data cut-off (Helios: the Thursday weekly control review in `project-delivery`) and a send
  time (Helios: Friday, weekly; on steering weeks it is the pre-read for the Tuesday meeting).
- Version and archive each report; append its ratings to the RAG history log (a copy of
  `rag-history-template.csv` in this skill's assets) in the same sitting so the next report's
  trend arrows have evidence.
- Log every decision the report asks for as a decision item in the issue log, and every
  decision taken in response, so the report and the log never disagree.
