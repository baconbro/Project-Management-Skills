# Issue management: one log for issues, actions, decisions and dependencies

Load this to keep the delivery log clean, to convert risks that occur into issues, to route
problems to the right specialist and to escalate well. The most common failure in delivery is
muddling item types and keeping them in several places, so nothing has one owner and one next
step. Use it with `assets/issue-log.csv` (fill-in) or `assets/issue-log-sample.csv` (sample).
Examples follow the sample Helios project (a fictional customer self-service portal used
throughout this catalog).

## The log is the system of record
The issue log is the one place where the project's issues, actions, decisions and
dependencies live. Meeting notes, chat threads and e-mails are capture tools, not records:
actions and decisions captured in a meeting (for example in `meeting-management`'s
`action-items.csv`) are merged into the log within a day, keeping the meeting's id in `links`,
and are then tracked only here. With the risk register (`risk-register`) and the assumptions
log (`project-planning`), it makes up a full RAID log; nothing is lost between them.

| Letter | Item | Lives in |
|---|---|---|
| R | Risks and opportunities | `risk-register` |
| A | Assumptions and constraints | `project-planning` assumptions log |
| I | Issues | this log, type `issue` |
| D | Decisions and dependencies | this log, types `decision` and `dependency` |
| — | Actions | this log, type `action` |

## The item types
- **Issue**: a problem happening **now** that threatens scope, schedule, cost, quality or
  benefits. It needs resolving. Defects that fail an acceptance criterion are issues.
  _Helios I001: "IdentityCo sandbox tenant down since 2026-06-12, blocking SSO integration
  testing."_
- **Action**: a task someone has committed to do, usually out of a meeting or as part of
  resolving an issue. It needs doing. _Helios ACT001: "Agree a dated recovery plan with
  IdentityCo's account manager and claim the sandbox delay credit."_
- **Decision**: a choice that is needed (open, with a decide-by date) or has been made
  (closed, with what was decided, by whom and why), recorded so it is not relitigated.
  _Helios DEC001: "Keep sprint S4 on its goal by testing against a stubbed identity provider
  until the sandbox returns." Decided by Ben Adeyemi with Ava Chen, 2026-06-16._
- **Dependency**: something another party owes the project by a date: a vendor deliverable,
  another team's release, a sign-off. Name the provider in the description and an owner on
  our side who chases it; `due` is the needed-by date. _Helios DEP001: "Support Operations
  (Priya Nair) releases 20 agents for UAT."_
- **Not here: risks and assumptions.** A risk is a future, uncertain event; it lives in the
  register until it occurs. An assumption is taken as true until validated; it lives in the
  assumptions log, and becomes an issue here if it proves false.

Rule of thumb: **risk = might happen; issue = is happening; action = to do; decision =
chosen or to be chosen; dependency = owed to us.**

## When a risk occurs
A materialised threat is the moment its planned response exists for. Do all four, the same day:
1. **Execute the planned response** (the contingency or fallback in the register), or decide
   a new one if none was planned.
2. **Set the risk's status to `Occurred`** in the register; never delete or simply close it,
   so the response and the outcome stay visible to `lessons-learned`.
3. **Open a linked issue** whose `links` column cites the risk id, with an owner, impact and
   due date; the response tasks become actions linked to that issue.
4. **Fund it correctly**: use contingency for an identified risk through change control;
   management reserve needs the sponsor.

Run `scripts/issue_log_check.py` with `--risks <register>`: it fails if an `Occurred` risk has
no linked issue, and warns when an issue links a risk the register still shows as `Open`.
When an opportunity's trigger fires, exploit it the same way and set it to `Realised` when
captured. _Helios: R001 (identity-provider integration slips, owner Sam Lee) occurred when the
IdentityCo sandbox went down on 2026-06-12. Sam Lee invoked the vendor service level agreed as
its mitigation (ACT001: dated recovery plan and delay credit), the team switched to a stub
(DEC001, ACT002), and issue I001 links R001._

## Logging items
Each row in `assets/issue-log.csv`:

| Column | Rule |
|---|---|
| `id` | Unique, never reused: `I###` issue, `ACT###` action, `DEC###` decision, `DEP###` dependency |
| `type` | `issue`, `action`, `decision` or `dependency` |
| `description` | Specific and self-contained; actions start with a verb; open decisions state the question and the options |
| `impact` | What it threatens (scope, schedule, cost, quality, benefits) and by how much |
| `owner` | Exactly one named person, never a team or "TBD"; for a decision, the person who decides |
| `priority` | High, Medium or Low (below) |
| `status` | `Open`, `In progress`, `Blocked`, `Closed`, `Transferred` |
| `raised` | Date logged |
| `due` | Resolve-by, do-by, decide-by or needed-by date; never "ASAP" |
| `links` | Risk, change request, vendor, WBS element, acceptance-log entry or meeting it relates to |
| `escalated_to` | The forum or person and date it went to; blank while the team can resolve it |
| `resolution` | **Required when Closed or Transferred**: how it was resolved; for a decision, what was decided, by whom and why; for a transfer, to whom |
| `closed` | Date closed |

An item with no owner is not managed; it is just noticed. An item closed without a resolution
cannot feed `lessons-learned` or prove to `project-closure` what was done.

## Prioritizing
- **High:** blocks delivery or threatens a milestone, the budget, a quality gate or an
  acceptance now. Review daily.
- **Medium:** material but not blocking; resolve within the weekly cadence.
- **Low:** minor; resolve when convenient or accept and close with that resolution.

## Routing: keep the item here, act through the specialist

| The item is about | Act through | What stays in this log |
|---|---|---|
| A change to scope, schedule, cost or a Must requirement | `change-request`, decided under `change-management` tolerances | The issue, linked to the CR id |
| A late or failing vendor, a contract dispute, invoice before acceptance | `procurement-management` (remedies, escalation ladder, acceptance before payment) | The issue, linked to the vendor id |
| Overload, a departure, a skills gap, onboarding, team conflict | `resource-management` (capacity check, leveling, team charter) | The issue or action |
| A failed acceptance criterion or definition of done | `quality-management` for the check, `scope-and-requirements` for the acceptance record | The defect as an issue; conditions as actions |
| A sprint impediment the team can clear | `agile-delivery` (the team's board) | Nothing, unless it needs the PM |
| A go-live readiness gap or a rollback | `release-and-cutover` | The issue; the go/no-go verdict as a decision |
| A risk that has not happened yet | `risk-register` | Nothing until it occurs |

_Helios I001 runs through `procurement-management`: Sam Lee, as contract owner, claimed the
$880 delay credit, held the milestone payment until acceptance and agreed IdentityCo's dated
recovery plan; the option to buy premium support to crash the task is a change request
(ACT004)._

## Escalation
Escalate when an item is beyond the team's authority, money or time, or threatens a baseline
commitment, and escalate **early**, with options rather than just the problem:
1. State the item, its impact and the deadline to decide.
2. Offer two or three options with their trade-offs and your recommendation.
3. Name the decision you need and who must make it.
4. Record the escalation in `escalated_to` and open a decision item if one is needed.
5. Take it to the next steering committee, or call an extra session if waiting would breach
   a milestone (see `delivery-cadence.md`).

Typical ladder: team, then PM (within the change tolerances), then the steering committee or
sponsor. A vendor item follows the contract's escalation ladder in parallel. If resolving an
item changes the baseline, it also goes through `change-request`, not just this log.

## Closing and transferring
- Close an item only with its resolution and date filled in; cancelled actions close with the
  reason.
- At project closure, every open item is closed or transferred to a named owner outside the
  project (usually operations), recorded as `Transferred` with the receiving owner in the
  resolution. `project-closure` checks this.

## Anti-patterns
- Logging everything as an "issue", so risks are never managed before they hit.
- Items with no owner, or with a whole team as owner.
- Two action lists (meeting notes and the log) that drift apart.
- Decisions made in meetings but never recorded, so they are reopened endlessly.
- Closing a risk when it occurs instead of executing its response and opening a linked issue.
- Closing an item with no resolution, so nobody can tell later what was done.
- Escalating a problem with no options, pushing the analysis onto the sponsor.
