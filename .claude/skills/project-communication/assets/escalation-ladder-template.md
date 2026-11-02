# Escalation Ladder — <project name>

Fill-in template. Copy it into your project folder before filling it, so the bundled template
stays blank, and replace every `<placeholder>`. A filled ladder and trigger table for the sample
Helios project (a fictional customer self-service portal used throughout this catalog) are in
`references/escalation-paths.md`. Publish the filled ladder with the communication plan so people
know the route before they need it.

| Version | As of | Owner | Approved by |
|---|---|---|---|
| <n.n> | <YYYY-MM-DD> | <project manager> | <sponsor name>, <YYYY-MM-DD> |

## 1. Levels and authority

Take each authority limit from the change-control tolerances agreed in `change-management`. Keep
the ladder to three or four levels; most items should resolve at level 1 or 2.

| Level | Owner (named) | May decide alone | Time-box at this level | How to reach them | Deputy when absent |
|---|---|---|---|---|---|
| 1 | <team lead or work-package owner> | <technical choices and blockers inside the sprint or work package> | <1 working day> | <stand-up; team chat channel> | <name> |
| 2 | <project manager> | <changes up to $ amount and n days; contingency draws for fired risk triggers and approved changes> | <2 working days> | <channel> | <name> |
| 3 | <sponsor> | <management reserve; milestone moves beyond the PM's tolerance; scope trade-offs> | <2 working days> | <channel> | <name> |
| 4 | <steering committee or portfolio board> | <re-baselining; cross-project conflicts; anything beyond the sponsor's authority> | <next meeting, or an extra session within n business days> | <channel> | <chair's delegate> |

## 2. Triggers — escalate on the forecast, not on the actual

Each trigger must be objective: a number, a date or a named event. Set the cost trigger so that
it fires while contingency remains, not when the forecast passes the baseline plus all reserves.

| Dimension | Escalate to level 2 when | Escalate to level 3 when | Escalate to level 4 when |
|---|---|---|---|
| Schedule | <a task's forecast slip exceeds its float> | <a milestone's forecast slip exceeds n weeks> | <a committed date cannot be met by any option within the sponsor's authority> |
| Cost | <any unplanned spend above an amount> | <the forecast overrun is more than the remaining contingency can absorb (EAC above BAC); more than n% of contingency drawn before a named milestone; a decision needs management reserve> | <a request beyond the management reserve; a re-baseline> |
| Scope and quality | <a request outside the sprint goal or work package> | <a Must-have requirement or an acceptance criterion at risk> | <a change to the objectives or a deliverable> |
| Risk and compliance | <a risk trigger fires> | <a new HIGH risk; a security or compliance risk rated at a set band or above> | <an enterprise-level risk or a regulatory breach> |
| Time-box | <unresolved at level 1 after its time-box> | <unresolved at level 2 after its time-box> | <unresolved at level 3 after its time-box> |
| RAG | <a work package turns AMBER> | <any dimension turns RED> | <overall RED for n consecutive reports> |

## 3. Parallel and special routes

| Route | Ladder | Notes |
|---|---|---|
| Vendor (from the contract) | <level 1: name and vendor contact, resolve within n days; level 2; level 3; level 4> | <runs alongside the project ladder; only the contract owner instructs the vendor> |
| Cutover and go-live | <the command-center route and rollback authority set in the release-and-cutover runbook> | <rollback triggers are pre-authorized: the cutover lead calls a rollback without escalating> |
| Security or privacy incident | <incident process and contact> | <starts at once; the project ladder is informed, not asked> |
| Out of hours or urgent | <who, by which channel, within what time> | <channel> |

## 4. Escalation note (copy one per escalation)

- **Item:** <issue or decision id from the issue log> — <one-line title>
- **What happened and the impact:** <facts and forecast: cost, schedule, scope, quality, risk>
- **Decision needed:** <one sentence> · **Decider:** <name and level> · **Decide by:** <YYYY-MM-DD>
- **Options:**
  1. <option> — <cost, time and risk>
  2. <option> — <cost, time and risk>
  3. <option, including "do nothing"> — <cost, time and risk>
- **Recommendation and why:** <one option and the reason>
- **If no decision by the date:** <consequence>
- **Raised by and date:** <name>, <YYYY-MM-DD> · **Recorded in the issue log's `escalated_to`:** <yes or no>

## 5. Rules everyone agrees to

- Escalation is a duty, not an admission of failure: when a time-box expires, the item moves up.
- Escalate the decision needed, with options and a recommendation, not just the problem.
- Escalate early and small rather than late and large; a forecast breach is enough.
- Do not skip a level without telling the level you skipped.
- Record every escalation and its outcome in the issue log, and report open escalations in the
  status report.
- <any project-specific rule>
