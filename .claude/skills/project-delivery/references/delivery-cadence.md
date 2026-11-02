# Delivery cadence: the governance rhythm

Load this to set the daily, weekly and steering rhythm that keeps a running project in
control. The cadence is the heartbeat of monitoring and control: fixed points at which you
measure progress, surface issues and risks, accept finished work, decide and report.
Examples follow the sample Helios project (a fictional customer self-service portal used
throughout this catalog), which runs hybrid: daily stand-up, two-week sprints, a weekly
status report and a bi-weekly steering committee chaired by the sponsor, Dana Okoro.

## The control loop
Every cadence event runs the same loop: **measure** actuals, **compare** them to the
baseline, **decide** what to correct, **act** within change control. The frequency changes;
the loop does not. Status flows in writing before the meeting; the meeting is for decisions.

## Daily: unblock
- **Purpose:** remove blockers and surface new problems within a day.
- **Waterfall:** a 15-minute check-in on today's tasks and blockers per workstream.
- **Agile:** the daily stand-up run by the team (see `agile-delivery`); impediments the team
  cannot clear itself go to the PM.
- **Hybrid:** stand-up for each delivery team; anything needing a decision above the team is
  flagged to the PM the same day.
- **PM actions:** triage new items into the issue log (type, one owner, priority, due date);
  re-check High items.
- **Output:** updated task status; new items in the issue log.

## Weekly: control
- **Purpose:** measure progress against the baseline and keep the issue and risk picture
  current. Run it the day before the status report is due.
- **Standing agenda (60 minutes or less):**
  1. Run `scripts/issue_log_check.py` on the log; agree new dates or escalation for every
     overdue item, and confirm owners of items due in the next 7 days.
  2. Merge the week's meeting actions and decisions into the log (one list, not two).
  3. Earned value and forecast from `cost-management` (CPI, SPI, EAC and the RED work
     package); in sprints, velocity and burnup from `agile-delivery`.
  4. Acceptance: which deliverables finished this week, which passed their quality checks,
     which were formally accepted, and which conditions and defects are now logged items.
  5. Risk: re-score changed risks with `risk-register`; for any risk whose trigger fired,
     confirm the response is running and a linked issue exists.
  6. Assumptions due for validation this week in the `project-planning` assumptions log; an
     assumption that proves false becomes an issue (and a risk if its effect is still uncertain).
  7. Dependencies needed in the next two weeks: chase the provider now, not on the due date.
  8. Change requests raised or awaiting decision (`change-request`, `change-management`).
  9. Vendor and people items: the weekly vendor working session (`procurement-management`);
     the capacity re-check against the forecast (`resource-management`).
  10. Decisions and escalations for the next steering committee.
- **Output:** the inputs for this week's `status-report`; an updated log and register.

## Steering and gates: decide
- **Purpose:** take decisions beyond the PM's authority and steer the project back toward its
  baseline, or agree to change it through change control.
- **Frequency:** at least monthly; bi-weekly when the project is short, fast-moving or AMBER.
  Add an extra session when a dimension turns RED rather than waiting for the next slot.
- **Standing agenda:** decisions first (the check's "for steering" list), each with options, a
  recommendation and a decide-by date; then the RAG report and trend; then risks needing
  sponsor action; then change requests above the PM's tolerance; then upcoming milestones,
  acceptances and go-live readiness.
- **Waterfall:** the stage-gate review decides whether the next stage starts.
  **Agile:** the sprint review (the product owner accepts the increment) and the retrospective;
  a periodic product or portfolio review steers above the team.
  **Hybrid:** milestone review up, sprint review down.
- **Output:** recorded decisions (closed decision items with their resolution), owned actions,
  an updated plan within change control, a communicated status.

## Milestones: accept and learn
- Confirm every deliverable due at the milestone has an acceptance-log entry (accepted,
  accepted with conditions, or rejected with a logged defect).
- Re-run the business-case appraisal with the current EAC and benefit forecast
  (`business-case`) and log the sponsor's continue/stop decision against the charter's stop
  triggers (Helios: at M4 and M6).
- Hold a short lessons session or use the retrospective; record lessons with `lessons-learned`
  while people still remember why things happened.
- No later than six weeks (T-6) before any go-live, with the release strategy from planning,
  start `release-and-cutover` and add its readiness checkpoints to the weekly agenda.

## The Helios calendar

| Event | When | Owner | Inputs | Outputs |
|---|---|---|---|---|
| Stand-up (per team) | Daily, 15 minutes | The delivery team runs it; Sam Lee (PM) facilitates | Sprint board | Blockers to Sam Lee; new log items |
| Weekly control review | Thursday | Sam Lee (PM) | Issue log check, EVM, velocity, register, change log | Status report inputs |
| Status report | Friday, weekly | Sam Lee | Weekly control review | RAG report to the steering members and stakeholders |
| Sprint review (stakeholders invited), then team-only retrospective | Every second Friday | Ava Chen (review); the team, facilitated by Sam Lee (retrospective) | Increment, definition of done | Increment accepted or not; lessons |
| Steering committee | Bi-weekly Tuesday | Dana Okoro (sponsor) | Status report, "for steering" list, change requests | Decisions logged as closed decision items |
| Vendor working session | Weekly | Ben Adeyemi (tech lead) with IdentityCo | Vendor register, open vendor items | Vendor actions in the log |

At the end of month 3 the steering committee of 2026-07-14 has two items from the log: DEC002
(approve IdentityCo's recovery plan and decide on management reserve) and I001 (the sandbox
outage, escalated). Earned value reads CPI 0.93, SPI 0.92: AMBER.

## Setting the cadence
1. Match frequency to risk and pace: faster for higher uncertainty, shorter iterations or a
   project already AMBER; slower once the work is stable.
2. Give every recurring event a single owner, a fixed slot and a standing agenda; run the
   meetings with `meeting-management`.
3. Keep events short and decision-oriented: status goes out in writing before the meeting.
4. Write the cadence into the communication plan so stakeholders know when to expect what.
5. Review the cadence each quarter or phase and drop events that no longer earn their time.

## Anti-patterns
- A stand-up that becomes a status read-out for the PM instead of an unblocking session.
- A steering meeting with updates and no decisions, or decisions nobody writes down.
- A second action list in meeting notes that never reaches the issue log.
- Checking dependencies on the day they are due instead of two weeks before.
- A cadence so heavy that the team spends more time reporting than delivering.
