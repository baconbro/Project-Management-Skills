# Delivery cadence — the governance rhythm

Load this to set the daily/weekly/monthly rhythm that keeps a project in control during
delivery. The cadence is the heartbeat of monitoring and control: regular points to
measure progress, surface issues and risks, decide, and report. Examples use the running
sample project: **Helios**, a customer self-service portal.

## The control loop
Every cadence event runs the same loop: **measure** actuals → **compare** to the baseline
→ **decide** what to correct → **act** within change control. The frequency changes; the
loop does not.

## Daily
- **Purpose:** unblock the team and surface issues fast.
- **Waterfall:** a short check-in on today's tasks and blockers.
- **Agile:** the daily standup — what's done, what's next, what's blocked.
- **Hybrid:** standup for the delivery team; blockers needing a decision are flagged up.
- **Output:** updated task status; new items into `issue-log.csv`.

## Weekly
- **Purpose:** track progress against the baseline and manage the issue/risk picture.
- Review the `issue-log.csv` (issues, actions, decisions) — see `issue-management.md`.
- Re-review open risks; act on HIGH ones (see `risk-register`).
- Check schedule and cost variance (see `cost-management` for CPI/SPI).
- Process any change requests (see `change-management`).
- **Output:** a current view of progress, issues, risks; inputs for the status report.

## Monthly / per stage gate / per sprint review
- **Purpose:** report to stakeholders and steer.
- Produce a concise RAG `status-report`.
- Run the steering forum: decisions on escalations, scope, budget, and dates.
- Confirm benefits and milestones are on track; adjust the plan within change control.
- **Waterfall:** stage-gate go/no-go. **Agile:** sprint review + retrospective.
  **Hybrid:** milestone review up, sprint review down.
- **Output:** decisions, an updated plan, a communicated status.

## Setting the cadence
1. Match frequency to risk and pace: faster cadence for higher uncertainty or shorter
   iterations.
2. Give every recurring event a single owner, a fixed time, and a standing agenda (see
   `meeting-management`).
3. Keep events short and decision-oriented; status flows in writing, decisions happen live.
4. Review the cadence itself periodically — drop events that no longer earn their time.

## Anti-patterns
- A daily that becomes a status read-out instead of an unblocking session.
- A monthly steering meeting with no decisions, only updates.
- A cadence so heavy the team spends more time reporting than delivering.
