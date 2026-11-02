---
name: status-report
description: >-
  Writes evidence-based project status reports: RAG ratings against tolerances on the
  forecast, trend, owners and actions for amber and red items, and decisions needed. Use
  when writing or reviewing a status report, weekly update or steering pack, or explaining
  a RAG rating.
metadata:
  version: 1.1.0
  category: artifact
  phase: delivery
  related: [project-delivery, cost-management, project-communication, agile-delivery]
license: MIT
---

# Status Report

## Overview
A status report is the short, regular update that tells its readers where the project stands
against its baseline, what will happen if nothing changes, and which decisions are needed from
them. Its job is to get decisions made and prevent surprises, not to narrate activity. This
skill builds the report evidence-first: it gathers the measures for each dimension, rates scope,
schedule, cost and quality against written tolerances using forecasts (the estimate at
completion and milestone forecast dates) as well as to-date indices, compares the ratings with
the last report, rolls them up, and writes a one-page report that leads with the RAG and the
decisions. The numbers come from the specialist skills; this skill interprets and reports them.
The examples use the sample Helios project (a fictional customer self-service portal used
throughout this catalog): the weekly report of 2026-07-10, pre-read for the 2026-07-14 steering
committee, is AMBER and worsening at CPI 0.93, SPI 0.92 and an EAC of about $535,000 against a
$500,000 BAC (`assets/status-report-sample.md`).

## When to use this skill
- The user needs to write a weekly or monthly status report, a steering pack or pre-read, or a
  highlight report between stage gates.
- The user needs to set, defend or challenge a RAG rating, or explain why a project is amber.
- The user wants someone else's report reviewed for honesty (the "watermelon" check) or gaps.
- The user has earned-value, sprint, issue and change data and needs one page a sponsor can act on.
- Ratings drift between periods and need a previous rating, a trend and red triggers.
- Do NOT use this to decide who receives which report, how often and through which channel, or
  to build the escalation ladder — use `project-communication`.
- Do NOT compute earned value, EAC or the reserves here — use `cost-management` and report its
  results.
- Do NOT use this to triage an unfamiliar project and route it to the next skill — use
  `senior-pm`.
- Do NOT use this to log, chase or escalate a live issue — use `project-delivery`; for sprint
  planning and velocity, use `agile-delivery`.

## Methodology fit
- **Waterfall:** rate against the baselined milestones and the monthly EVM close; schedule on
  milestone forecasts, and past about 60% complete on earned schedule SPI(t) instead of SPI; the
  report is the highlight report between gates, and a tolerance forecast to be breached is
  escalated at once through `project-communication`'s ladder, not held for the next report.
- **Agile:** report after each sprint review: sprint goal met or not, increment accepted or not,
  the velocity range, the burnup, and the release outlook against the sprints left and the cut
  line from `agile-delivery`; cost as spend to date plus cost per sprint times the sprints still needed;
  scope from backlog changes and the cut line; quality from the definition of done.
- **Hybrid (Helios):** the governance layer carries the RAG, milestones M1, M4 and M6, and EVM on
  the baselined work packages; sprint metrics sit underneath as evidence for the schedule and
  scope rows. The report goes out every Friday from the Thursday control review and, every second
  week, doubles as the Tuesday steering pre-read.

## Inputs you need
The approved baseline (key milestones, BAC, contingency and management reserve) and the schedule
and cost tolerances agreed with the sponsor (charter, project management plan or escalation
ladder); the latest earned-value output from `cost-management` (CPI, SPI, EAC range, VAC, TCPI,
trend) or the proxy you will use; milestone forecasts from the schedule; the issue log, change
log and risk register as of the status date; quality evidence (gates, acceptance results,
defects); sprint history for agile work; the audience, cadence and send date from the
communication plan; and last period's report and RAG history. With no approved baseline there is
nothing to be on or off track against: say so and build an interim baseline with
`project-delivery` first. With no tolerances, propose the defaults in
`references/rag-criteria.md` (section 2) and have the sponsor confirm them before the first
rating.

## Workflow
1. **Fix the audience, period and cut-off.** Take the audience, cadence and send date from the
   communication plan; a sponsor wants exceptions and decisions, a team wants detail (see
   `references/writing-and-review.md`, section 3). Fill the header of a copy of
   `assets/status-report-template.md`. *Done: audience, status date, data cut-off, period and
   send date are written in the header.*
2. **Gather the evidence per dimension, before any colour.** Run the specialist helpers on the
   same status date (shown on the Helios samples; the change log and sprint history samples run
   past 2026-07-10, so use only rows up to your status date):
   ```bash
   python .claude/skills/cost-management/scripts/health_check.py .claude/skills/cost-management/assets/evm-history-sample.csv --eac-method all
   python .claude/skills/project-delivery/scripts/issue_log_check.py .claude/skills/project-delivery/assets/issue-log-sample.csv --as-of 2026-07-10
   python .claude/skills/change-request/scripts/change_impact.py .claude/skills/change-request/assets/change-log.csv --reserve-cost 40000
   python .claude/skills/agile-delivery/scripts/velocity_forecast.py .claude/skills/agile-delivery/assets/sprint-history-sample.csv --sprints-left 4
   ```
   Add the milestone forecasts from the schedule and the quality evidence (gates, acceptance,
   defects). Without earned value, pick a proxy from `references/writing-and-review.md`
   (section 4) and name it. *Done: every dimension has its measures with values, sources and
   the status date, and no rating has been chosen yet.*
3. **Rate each dimension against `references/rag-criteria.md`.** Rate on the worse of the index
   test and the forecast test (EAC against BAC, BAC plus management reserve and the cost
   tolerance; milestone forecast against the schedule tolerance); past about 60% complete use
   SPI(t) and forecast dates, not SPI. Name every RED work package or interim milestone, and
   for each AMBER or RED item write an owner, an action with a due date, and a red trigger.
   Helios: four dimensions AMBER; 1.3.1 Identity / SSO integration and 1.3.4 Reporting &
   analytics RED. *Done: each dimension has a rating, the threshold that decided it, and an
   owner, action and red trigger wherever it is not GREEN.*
4. **Compare with the last report.** Append this period's rows to the RAG history log, a copy
   of `assets/rag-history-template.csv` (filled example: `assets/rag-history-sample.csv`), and
   take each previous rating and trend arrow from the last rows. A colour may change only with a
   changed measure; an unchanged RED stays RED. *Done: every dimension and the overall rating
   show previous rating and trend, each backed by a row in the log.*
5. **Summarise progress, milestones and changes.** List outcomes finished and accepted, not
   activity; give each key milestone its baseline, forecast, variance, RAG, owner and recovery
   action; list the changes this period with the pending-change-requests line (ids, cost, days,
   decider, date, committed plus pending against the remaining contingency) that feeds the scope
   rating. *Done: milestone, progress and changes sections filled; no forecast is a copy of the
   baseline.*
6. **List the top risks and issues and write the decision asks.** At most five, linked to the
   risk register and issue log, each with owner and next action. Write every decision with its
   six parts: decision, options, recommendation, decider, decide-by date, consequence of no
   decision (`references/writing-and-review.md`, section 2). *Done: every decision has all six
   parts and every listed item an owner and a dated action.*
7. **Roll up the overall RAG and write the summary.** The overall rating is no greener than the
   worst material dimension; a recovery plan counts only when it is approved, funded and already
   in the forecast. Add the previous rating, trend and red triggers, then write the three-sentence
   summary. Helios: AMBER, previous AMBER, ↓ worsening; red if SSO is not working in test by
   2026-07-24 or the EAC passes $550,000. *Done: the overall rating, previous rating, trend, red
   triggers and summary are written and consistent with the dimension table.*
8. **Check, brief and send.** Cut to one page, run the review checklist in
   `references/writing-and-review.md` (section 7), brief the sponsor in person on any new AMBER or
   RED before sending, send as the communication plan says, and log each decision ask as a
   decision item in the issue log (`project-delivery`). To review someone else's report, run
   steps 2–3 on its evidence and the same checklist. *Done: every checklist line passes, the
   report is sent on time, and its decision items are logged.*

## Quality checklist
- [ ] Audience, status date, data cut-off and period are stated in the header.
- [ ] Schedule and cost tolerances are written in the report and were agreed before this period.
- [ ] Every dimension cites its measure and the threshold in `references/rag-criteria.md` it met.
- [ ] Cost is rated on EAC/VAC as well as CPI, with the EAC formula named and the range shown.
- [ ] Schedule is rated on milestone forecasts as well as SPI; past about 60% complete, on
      forecasts and SPI(t), not SPI.
- [ ] The overall rating is no greener than the worst material dimension, and no proposed (not
      yet approved) recovery plan is counted.
- [ ] Previous rating and trend are shown and match the last rows of the RAG history log.
- [ ] Every AMBER or RED dimension, milestone and work package has an owner, an action and a date,
      and every AMBER dimension a red trigger.
- [ ] The scope row shows pending change requests with cost, days, decider and date, and
      committed plus pending against the remaining contingency.
- [ ] The budget line shows BAC, AC, EV or % complete, EAC, VAC, contingency and management
      reserve.
- [ ] Every decision has options, a recommendation, a decider, a decide-by date and a consequence.
- [ ] Figures match the EVM output, issue log and change log of the same status date.
- [ ] Ratings are written as words; the report fits one page or screen and lists outcomes, not
      activity.

## Anti-patterns
- "Watermelon" reports: green on the outside, red on the inside — a GREEN cost line with a
  negative VAC, a GREEN schedule with a milestone forecast late.
- Choosing the colour first and gathering evidence to fit it.
- Rating on to-date indices alone: SPI drifts to 1.0 near the end however late the project is.
- Counting a proposed recovery plan as delivered ("red, but we have a plan, so amber").
- Moving the thresholds or tolerances after a bad period, or quietly re-baselining.
- The same AMBER for weeks with no owner, action or red trigger.
- Reporting activity ("we held 12 meetings") instead of outcomes and forecasts.
- Burying the one decision you need, or asking for "support" without options or a date.
- Different numbers for different audiences, or a RED the sponsor first reads in writing.
- Colour-only ratings that vanish in grayscale print and for colour-blind readers.
- Pasting the whole risk register into the report instead of linking to it.

## Resources
- `references/rag-criteria.md` — what each colour means, tolerances and their defaults, the
  per-dimension thresholds (index and forecast tests), why SPI misleads late and how to use
  earned schedule, the roll-up rules, trend and red triggers, and the Helios worked example.
- `references/writing-and-review.md` — anatomy of the report, the six-part decision ask, one
  fact set for several audiences, proxies when earned value is not tracked, agile and hybrid
  reporting, delivering bad news, and the review checklist with watermelon tests.
- `assets/status-report-template.md` — fill-in one-page report (`<placeholders>`) with owner and
  action columns, budget line, milestones, changes this period and decisions.
- `assets/status-report-sample.md` — sample Helios weekly report of 2026-07-10 (AMBER, worsening).
- `assets/rag-history-template.csv` — fill-in RAG history log, one row per dimension per report
  (`report_date, period, dimension, rag, trend, evidence, threshold, owner, action, due`).
- `assets/rag-history-sample.csv` — sample Helios history from the M1 close to 2026-07-10.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-delivery` — runs the weekly control review whose issue-log check, milestone forecasts and change status feed this report, and logs the decisions it asks for as decision items.
- `cost-management` — supplies CPI, SPI, the EAC range, VAC, TCPI and the CPI/SPI trend from its health_check.py helper; this skill turns them into the cost and schedule ratings without recomputing them.
- `project-communication` — sets who receives this report, when and through which channel, the audience framing, and the escalation ladder whose tolerances the RAG thresholds share.
- `agile-delivery` — supplies velocity, the release forecast range and the cut line from its velocity_forecast.py helper, the evidence for the schedule and scope ratings of agile and hybrid work.
