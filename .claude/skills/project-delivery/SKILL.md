---
name: project-delivery
description: >-
  Runs a baselined project day to day: tracks progress against the baseline,
  verifies and accepts finished deliverables, keeps one log of issues, actions,
  decisions and dependencies (checked by the bundled issue_log_check.py helper),
  executes risk responses when risks occur, controls change, escalates, and
  prepares go-live and the handover to closure; builds a one-day interim
  baseline for a running project that has none. Use when the user is executing a
  plan, keeping a running project in control, logging or escalating a problem
  happening now, accepting a finished deliverable, or taking over a mid-flight
  project with no baseline. Triggers: "we are in delivery", "execute the plan",
  "monitor and control", "track progress against the baseline", "issue log",
  "log an issue", "escalate a blocker", "a risk has happened", "project already
  running with no baseline". For writing the status report itself, use
  status-report; for sprint mechanics, use agile-delivery. Works for waterfall,
  agile, and hybrid projects.
metadata:
  version: 1.1.0
  category: phase
  phase: delivery
  related: [senior-pm, project-planning, status-report, change-management, cost-management, risk-register, project-closure, lessons-learned, change-request, agile-delivery, release-and-cutover, procurement-management, resource-management]
license: MIT
---

# Project Delivery

## Overview
Delivery is where the plan meets reality: the team builds, and the project manager runs one
loop on a fixed cadence — measure actuals, compare them to the baseline, decide, act within
change control. This skill runs that loop and owns three things no other skill does: the
**issue log**, the system of record for issues, actions, decisions and dependencies; the
**verify-and-accept step** that turns "built" into "accepted" deliverable by deliverable; and
the **escalation path** to the steering committee. Everything else is routed to its
specialist. Examples follow the sample Helios project (a fictional customer self-service
portal used throughout this catalog): sponsor Dana Okoro, project manager Sam Lee, BAC
$500,000, six months, run hybrid.

## When to use this skill
- The baseline is approved and work is running; the user needs to keep it in control.
- A problem is happening now and needs logging, one owner or escalation, or a decision must
  be recorded so it is not reopened.
- A deliverable or sprint increment is finished and must be verified and accepted.
- The project is already under way with no baseline and a status is due: build the interim
  baseline in step 1 instead of restarting planning.
- Do NOT use this to build the plan or set the full baseline — use `project-planning`.
- Do NOT use this for sprint planning, backlog refinement or velocity forecasts — use
  `agile-delivery`; this skill consumes their results.
- Do NOT use this for one artifact on its own: the report (`status-report`), one change
  (`change-request`), earned value (`cost-management`), the risk register (`risk-register`).
- Do NOT use this for the go/no-go, cutover runbook or hypercare — use `release-and-cutover`;
  or to close the project — use `project-closure`.

## Methodology fit
- **Waterfall:** control against the full baseline with earned value; a stage-gate review
  decides whether the next stage starts; deliverables are accepted at gates; every baseline
  change needs a change request.
- **Agile:** the sprint is the control loop: stand-up, review (the product owner accepts the
  increment against the definition of done), retrospective. Progress is burnup and velocity
  from `agile-delivery`; re-ordering the backlog absorbs most change without a request. The
  issue log holds impediments the team cannot clear and decisions above the team.
- **Hybrid:** milestones, budget and Must scope are baselined and reported up with earned
  value; sprints run underneath; a change request is needed only when a change touches that
  fixed frame. Helios runs this way: daily stand-up, two-week sprints, weekly status report,
  bi-weekly steering committee.

## Inputs you need
- The approved baseline from `project-planning`: scope statement and WBS, schedule and
  milestones, cost baseline and reserves, plus the risk register, assumptions log,
  communication plan and change-control tolerances.
- Actuals each period: progress, cost to date from finance, sprint results.
- Each deliverable's acceptance criteria, the definition of done and the named acceptor.
- A copy of `assets/issue-log.csv`.
- No approved baseline but work is running? Do not restart full planning: step 1 builds an
  interim baseline in about a day from what already exists.

## Workflow
1. **Fix what you control against.** If an approved baseline exists, record its version and
   date. If the project is running without one, fill `assets/rebaseline-template.md` following
   `references/mid-flight-rebaseline.md`: scope list with an acceptor per deliverable,
   remaining milestone dates, budget to date (approved, actual, committed, estimate to
   complete) and the open risks and issues; the sponsor approves it as an interim baseline and
   you report against it at once. A baseline that exists but can no longer be met is a formal
   re-baseline through `change-request` and `change-management`, not this shortcut.
   *Done: a dated, sponsor-approved baseline (full or interim) to measure against.*
2. **Set the cadence and open the log.** Agree the daily, weekly and steering rhythm in
   `references/delivery-cadence.md`, each event with one owner and a standing agenda. Copy
   `assets/issue-log.csv` as the single system of record: actions and decisions captured in
   meetings are merged into it within a day, so there is one list. *Done: the cadence is on
   the calendar with owners and one issue log exists.*
3. **Track progress against the baseline.** Weekly, compare actuals with the baseline on
   scope, schedule and cost, using earned value from `cost-management`:
   ```bash
   python .claude/skills/cost-management/scripts/health_check.py .claude/skills/cost-management/assets/evm-snapshot.csv
   ```
   Helios, end of month 3: CPI 0.93, SPI 0.92, AMBER; EAC about $535,000; the variance is
   driven by the RED work package 1.3.1 Identity / SSO integration (CPI 0.69, the vendor
   slip), with Reporting & analytics also RED on a small budget. In sprints add velocity and
   burnup from `agile-delivery`. Count accepted work, not hours burned. *Done: variance and
   forecast are known per dimension, with the work package driving them.*
4. **Verify and accept each deliverable.** When a deliverable or increment is finished, run
   quality control first: test and review it against its acceptance criteria and the
   definition of done (`.claude/skills/quality-management/assets/definition-of-done.md`) at the
   gate `quality-management` defined. Then the named acceptor decides — accepted, accepted
   with conditions, or rejected — following scope validation in `scope-and-requirements`,
   recorded with its evidence in the acceptance log of the scope statement (on an interim
   baseline, in the scope list of `assets/rebaseline-template.md`). Log each failed
   criterion as an issue, each condition as a dated action, each new need as a change request.
   A passed test is not acceptance; silence is not acceptance. Helios: Ava Chen accepted the
   sprint S4 increment on condition of two contrast fixes, logged as ACT005. *Done: every
   finished deliverable has an acceptance-log entry and its conditions and defects are owned
   log items, the evidence `project-closure` relies on for final acceptance.*
5. **Run the issue log.** Triage new items daily; review the whole log weekly. Each item has a
   type, one owner, an impact, a priority, a due date (decide-by for decisions, needed-by for
   dependencies) and links to the risk, change, vendor or WBS element it touches; closed items
   record their resolution and date. Rules and routing: `references/issue-management.md`.
   Before each weekly review run:
   ```bash
   python .claude/skills/project-delivery/scripts/issue_log_check.py .claude/skills/project-delivery/assets/issue-log-sample.csv --as-of 2026-07-10
   ```
   It exits 1 on any item without one owner, a valid type, priority, status or due date, or
   closed without a resolution, and lists overdue, due-soon (`--days`, default 7), blocked and
   for-steering items and each owner's load. Helios on 2026-07-10: 14 items, 9 open, PASS; I003
   is 2 days overdue, 6 items fall due within 7 days, ACT003 is blocked, and DEC002 and I001
   go to steering. *Done: the check passes and every overdue item has a new agreed date or an
   escalation.*
6. **Monitor risk; when one occurs, execute its response.** Re-score on the cadence with
   `risk-register` and check the register before each review:
   ```bash
   python .claude/skills/risk-register/scripts/risk_score.py .claude/skills/risk-register/assets/risk-register-template.csv --check
   ```
   When a trigger fires or a threat materialises: execute the planned response the same day,
   set the risk to `Occurred` (never delete it), and open an issue whose `links` cites the risk
   id; contingency is drawn only through change control. `issue_log_check.py --risks <register>`
   fails if an occurred risk has no linked issue and warns when an issue links a risk still
   `Open`: run on the Helios samples it flags R001, which the register (a baseline snapshot)
   still shows as Open although I001 records that it occurred. *Done: the register is current
   and every occurred risk has a linked issue with its response under way.*
7. **Control change.** Raise each proposed change to the baseline as a change request with
   `change-request` and decide it under the tolerances in `change-management` (PM, change
   control board or sponsor). Re-ordering the backlog inside the fixed frame needs no request;
   changing a Must, a milestone or the budget does. Update the baseline only after approval.
   *Done: no baseline change without a logged, decided request.*
8. **Route vendor and people problems.** Keep the item in the log and act through the
   specialist: a late or failing supplier to `procurement-management` (contract remedies,
   escalation ladder, acceptance before payment; Helios I001 brought an $880 delay credit and
   IdentityCo's dated recovery plan); overload, a departure, a skills gap or team conflict to
   `resource-management` (capacity check, leveling, onboarding; for example if R003, the lead
   engineer leaving, occurs). *Done: each vendor or people item names the specialist's next
   action and its owner.*
9. **Report status.** Weekly, hand variance, forecast, acceptances, top risks and issues and
   the decisions needed to `status-report` for a RAG report on the same thresholds every week.
   Helios: AMBER overall, SSO RED, direction worsening. *Done: this week's report is out on time.*
10. **Steer and escalate.** Escalate early, with options and a decide-by date, when an item
    exceeds the team's authority, money or time or threatens a baseline. Build the steering
    agenda from the check's "for steering" list, take decisions at the steering committee
    (`meeting-management` runs the meeting) and write each one back as a closed decision with
    who decided and why. Capture lessons as they surface, at milestones and retrospectives,
    with `lessons-learned`. *Done: every escalation has a decision or a dated next step in the log.*
11. **Prepare go-live.** About four weeks before any go-live, start `release-and-cutover` for
    readiness criteria, the go/no-go, the cutover runbook and hypercare. Delivery keeps the log
    and steering running underneath: the go/no-go verdict is logged as a decision and release
    problems as issues. *Done: `release-and-cutover` owns the go-live plan and the verdict is
    in the log.*
12. **Hand over to closure.** When every in-scope deliverable has been accepted or formally
    deferred, go-live and hypercare are complete, and every open item is closed or
    transferred to a named owner, hand `project-closure` the issue log, acceptance log, change
    log, risk register and actuals. *Done: closure takes over with no unowned item.*

## Quality checklist
- [ ] Progress is measured against a dated, approved baseline (full or interim), not "feels on track".
- [ ] Stand-up, weekly review, weekly status report and steering run on schedule, each with an owner.
- [ ] One issue log is the system of record; meeting actions and decisions reach it within a day.
- [ ] `issue_log_check.py` passes: every item has one owner, a type, priority and due date; every closed item has a resolution.
- [ ] Every finished deliverable has an acceptance-log entry with evidence and the acceptor's decision; conditions and defects are log items.
- [ ] Every occurred risk is set to `Occurred`, its response is running, and an issue links its id.
- [ ] No baseline change without a decided change request.
- [ ] Vendor and people items name the specialist skill's next action and owner.
- [ ] Every escalation has a decision or a dated next step recorded as a decision item.
- [ ] Go-live runs through `release-and-cutover`; its go/no-go verdict is a logged decision.

## Anti-patterns
- Reporting green by gut feel instead of measuring against the baseline.
- Two action lists (meeting notes and the log) that drift apart; decisions left in chat.
- Closing an item with no resolution, so nobody can tell later what was done or why.
- Treating a passed test, or silence, as acceptance.
- Closing a risk when it occurs instead of executing its response and opening a linked issue.
- Sending a mid-flight project back through full planning when a status is due tomorrow.
- Letting scope drift in through the backlog or a vendor conversation without a change request.
- Escalating a problem with no options or decide-by date.
- Confusing activity with progress: hours burned is not value delivered.

## Resources
- `references/delivery-cadence.md` — daily, weekly and steering rhythm by methodology, the
  weekly control agenda and the Helios calendar.
- `references/issue-management.md` — issue, action, decision and dependency versus risk and
  assumption; logging rules, risk-to-issue conversion, routing to specialists, escalation, closing.
- `references/mid-flight-rebaseline.md` — the one-day interim baseline for a running project
  that has none, and how to report on it tomorrow.
- `assets/issue-log.csv` — fill-in issue log (`<placeholders>`): id, type, description,
  impact, owner, priority, status, raised, due, links, escalated_to, resolution, closed.
- `assets/issue-log-sample.csv` — sample Helios log as of 2026-07-10 (14 items); the
  script's sample input.
- `assets/rebaseline-template.md` — fill-in interim baseline: scope list, milestones, budget to
  date, open risks and issues, gaps, reporting basis, approval.
- `scripts/issue_log_check.py` — log hygiene check plus overdue, due-soon, blocked,
  for-steering and per-owner lists; `--as-of`, `--days`, `--risks`, `--strict`, `--format
  table|json|csv`. Run `python .claude/skills/project-delivery/scripts/issue_log_check.py
  --help` for columns, rules and exit codes.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `senior-pm` — routes a baselined, executing project here, and re-triages from this log, the change log and the weekly RAG.
- `project-planning` — hands over the approved baseline, risk register and assumptions log; runs the full or rolling-wave re-plan that replaces an interim baseline.
- `status-report` — turns this loop's variance, acceptances, risks, issues and decisions into the weekly RAG report (step 9).
- `change-management` — sets the tolerances and the change control board that decide baseline changes raised here (step 7).
- `cost-management` — supplies earned value, the forecast and the cost RAG each period (step 3).
- `risk-register` — re-scored each cycle; an occurred risk becomes an issue in this log that cites its id (step 6).
- `project-closure` — receives the acceptance log, the issue log with nothing unowned, the change log and actuals, and obtains final acceptance (step 12).
- `lessons-learned` — captures lessons from milestones, retrospectives and resolved items while delivery runs (step 10).
- `change-request` — raises and assesses each change an issue or decision here would make to the baseline (step 7).
- `agile-delivery` — runs sprints, backlog and velocity inside the frame this skill controls; impediments and fixed-frame changes come back here (steps 3 and 4).
- `release-and-cutover` — runs go-live from about four weeks out; its go/no-go verdict and release issues come back to this log (step 11).
- `procurement-management` — acts on the vendor issues logged here: remedies, escalation ladder, acceptance before payment (step 8).
- `resource-management` — acts on the people issues logged here: overload, departures, onboarding and leveling (step 8).
