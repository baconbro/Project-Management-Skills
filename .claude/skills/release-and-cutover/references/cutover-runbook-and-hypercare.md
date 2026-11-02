# Cutover runbook and hypercare

## Building the runbook
A cutover runbook is the minute-by-minute script for the window. Every step has one owner, a
planned start, a duration, the steps it waits for, the check that proves it worked and the
action that undoes it. Keep it as one row per step in `assets/cutover-runbook-template.csv` so
it can be sorted, filtered and timed. The worked example, `assets/cutover-runbook-sample.csv`, is
the general availability (GA) cutover of the sample Helios project (a fictional customer
self-service portal used throughout this catalog).

1. **Anchor on T0**, the moment users are first exposed to the new service. Plan each step as
   an offset (T-02:25, T+00:10) and convert to clock times last, so a date change is one edit.
2. **Use the standard phases in order:** prepare (bridge, roll call, backups) → freeze → deploy
   → data → configuration → technical verification → go-live checkpoint → release to users →
   business verification → rollback-window checkpoint → close and hand to hypercare. Keep the
   rollback steps in their own block (R1, R2...) with status `standby`.
3. **Right-size the steps:** 5-60 minutes, one named person as owner (never "IT" or "the
   vendor"), and a backup person for every step on the critical path. A step longer than an
   hour hides sub-steps that nobody is tracking.
4. **Write verifications as observations:** "10 of 10 test accounts sign in through SSO", not
   "check SSO". A step without a verification fails silently until users tell you.
5. **Give every step a rollback action** (the R-step that undoes it) or "None" with the reason:
   read-only check, nothing changed yet, administrative.
6. **Find the window's critical path** from the predecessors, run independent steps in
   parallel, and keep 20-30% contingency. Window = critical path + contingency + full rollback.
7. **Build in two checkpoints:** a go-live checkpoint before the first user-visible step, and a
   rollback-window checkpoint at least 30 minutes before the last safe rollback start.
8. **Add communication steps** at each checkpoint: bridge updates, the go-live announcement and
   the prepared rollback message, using the content agreed in `project-communication`.
9. **Version it.** Freeze the runbook at the go/no-go; any later change is a logged decision
   approved by the cutover lead.

## Rehearsals
- **Technical dry run** in a production-like environment: every step, the real scripts, timed.
- **Dress rehearsal:** the full runbook with the real people, the bridge and the comms, including
  the rollback block restored from a real backup.
- Replace planned durations with rehearsed ones and re-sequence if the critical path no longer
  fits. Rehearse again if the margin fell below 30 minutes or any step failed.
- Helios: the dress rehearsal on Saturday 2026-09-26 ran 25 minutes late because the search
  re-index took 40 minutes, not 15. Runbook v1.3 runs it in parallel with the SSO configuration
  (steps 8 and 9), and the rollback ran in 70 minutes against its 75-minute budget.

## The command center
- **Roles:** cutover lead (runs the clock, calls go-live or rollback), technical lead, scribe
  (logs every step's actual start, finish and outcome, and every decision), communications
  lead, business verifier and vendor liaison. One person may hold two roles, but the cutover
  lead owns only checkpoints and comms, never a technical step, so someone always watches the
  clock. Helios: Sam Lee leads, Ben Adeyemi is technical lead and vendor liaison, Elena Rossi
  is scribe, Priya Nair verifies for the business.
- **Cadence:** owners announce start and finish on the bridge; the lead gives a status every 30
  minutes and at each checkpoint; stakeholders get updates at the times in the runbook.
- **Deviation rule:** a step running more than 50% or 15 minutes over goes to the lead, who
  waits, skips it with a recorded risk, or invokes a rollback trigger. There are no improvised
  steps: an unplanned action is a logged decision with an owner.

## Hypercare
Hypercare is a time-boxed period of elevated support after go-live: the project team stays on
hand beside operations, fixes problems fast and transfers knowledge. It differs from a
**warranty** (a supplier's contractual duty to fix defects for a period) and from business-as-
usual support, though it often overlaps the warranty.

- **Duration:** typically 2-6 weeks, long enough to cover one full business cycle (a month-end,
  a billing run, the last ramp step) and the slowest-arriving defects. Helios: 4 weeks, the
  warranty period named in its WBS (1.5.2 Operational handover).
- **Entry:** go-live declared; on-call rota, triage path and dashboards working; known-error
  articles published.
- **Staffing:** heaviest in week 1 (extended hours, squad beside the service desk), tapering as
  incidents fall. The service desk shadows in week 1 and runs alone in the last week.
- **Severity and service levels:** response and restore targets per severity, agreed before
  go-live; every report routes service desk (L1) → hypercare squad (L2) → vendors (L3).
- **Daily stand-down (15 minutes):** incidents since yesterday, metrics against thresholds, the
  next ramp or decommission step, the next patch's content and new known errors.
- **Metrics:** stability (incidents by severity, availability), performance (page load, error
  rate), adoption (active users, completion of key journeys), business (deflection,
  satisfaction) and support load (contacts about the new service). Watch for silent failure:
  users who give up and phone the old channel never raise a defect.
- **Exit criteria are measured, not dated:** for example zero open severity-1/2 defects for 10
  consecutive business days, contacts below an agreed level, the service desk meeting its
  service levels without the squad, runbooks updated with every fix, go/no-go conditions and
  waivers closed, and the operations owner's signed acceptance. Extend week by week while any
  criterion fails; exit early when all are met.
- **Handover:** move open defects to the operations backlog with a priority and owner, stand the
  squad's on-call rota down, and send the exit record to `project-closure`, whose
  handover-to-operations step it completes.

## After hypercare
Hold a post-release review within two weeks of exit: planned versus actual timings, triggers
that came close, incidents and root causes, and what the go/no-go missed. Route the lessons to
`lessons-learned`, and confirm with the benefit owner that measurement against the business-case
baseline has started.
