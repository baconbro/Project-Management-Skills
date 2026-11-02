# Operationalizing Lessons

A lesson is learned only when something changes and stays changed. Most lessons die in one of
four places: no owner, no target (nobody knows which document or habit should change), no date,
or no check that the change worked. This reference closes all four. Examples use the sample
Helios project (a fictional customer self-service portal used throughout this catalog).

## 1. The lessons log
One row per lesson in a copy of `assets/lessons-learned.csv`; `assets/lessons-learned-sample.csv`
is the Helios log at closure.

| Column | What to write | Rule |
|---|---|---|
| `id` | LL001, LL002, ... | Never reused, even when a lesson is declined |
| `project` | Project name | Required once the log is pooled in an organisational repository |
| `date` | Date the lesson was captured | YYYY-MM-DD |
| `source` | `retro`, `review`, `meeting` or `incident` | Sprint retrospective; phase, milestone or post-project review; any other meeting (such as steering); post-mortem of an incident or failure |
| `category` | One of the eight categories | Where the root cause sits (`references/retrospective-formats.md`) |
| `kind` | `improve` or `repeat` | At least one `repeat` per review |
| `what_happened` | Facts and their effect, one or two sentences | Conditions and decisions, never a person as the cause |
| `root_cause` | The cause you can act on; for `repeat`, what made it work | Passes the "therefore" test |
| `evidence` | Metrics and record ids | At least one: a metric, an issue, risk or change id, a report date |
| `impact` | `High`, `Medium` or `Low` | On the impact scale |
| `recommendation` | Verb-first change to make, or practice to keep | Specific enough that someone else could check it was done |
| `applies_to` | The target that changes | Next sprint backlog, an issue-log id, the project plan, or a named standard, template or checklist |
| `owner` | One named person who makes the change | Agreed to the due date |
| `due_date` | When the change is made | YYYY-MM-DD |
| `status` | `open`, `in-progress`, `adopted`, `verified`, `declined` | See section 5 |
| `check_back_by` | Who confirms it worked | Preferably not the owner; must still be reachable after the project closes |
| `check_back_date` | When | Next retrospective, next gate, or about 90 days after adoption |
| `check_back_result` | What the check found, with evidence | Blank until checked; required for `verified` and `declined` |

Lessons that are recorded but not acted on (a Low that has not recurred) keep `owner`,
`due_date` and the check-back columns blank and stay `open` for pattern-spotting.

## 2. Writing a recommendation someone can adopt

| Weak | Adoptable |
|---|---|
| "Communicate better with the sponsor" | "Name the threatened milestone in any AMBER status line and tell the sponsor the same day" |
| "Plan vendors earlier" | "Add a vendor onboarding workstream to the standard plan: a named owner from the day of award, access lead times, a stub for each external integration" |
| "Shorter stand-ups" | "Hold stand-ups to 15 minutes against the sprint goal; problem-solving moves to a follow-on huddle" |
| "Testing was rushed" (a symptom) | "Provision a dedicated test environment with a named owner and a data refresh before each test cycle" |

Test each recommendation: does it name *what* changes, *where* (the `applies_to` target) and
*how you would see* that it happened?

## 3. Three routing paths

| Path | Comes from | Where the action goes | Who checks, and when |
|---|---|---|---|
| **A. Team (agile)** | Sprint or iteration retrospective | One or two actions into the next sprint backlog, added by the product owner, so they compete for capacity like any other work (`agile-delivery`) | The team, opening the next retrospective |
| **B. Project** | Phase or milestone review, post-mortem, or a retro item beyond the team's authority | An action in the `project-delivery` issue log with owner and due date; a baseline change through `change-request`; a new threat into the risk register | The project manager at the weekly control review, and at the next gate |
| **C. Organisation** | Any review, when the root cause sits in a standard, template, checklist or way of working shared across projects | The lessons log, `applies_to` naming the standard and its owner; at closure through `project-closure` into the PMO repository | The PMO Lead (or the standard's owner) about 90 days after adoption, and at the next project's planning |

Rules:
- Retrospective improvement actions go to the sprint backlog, not the issue log; only an
  impediment the team cannot clear, or a decision above the team, goes to the issue log.
- A lesson can take more than one path: fix it in this project (B) and prevent it in the next
  (C). Record it once, with both targets in `applies_to`.
- **Promote recurring themes.** The same root cause in three retrospectives, or in two
  projects, becomes a path C lesson even if each occurrence was Low.
- Mid-project lessons do not wait for closure: a path C change can be made while the project
  runs, and the project itself can adopt it at once.

## 4. Lessons in: using past lessons at the start
Learning pays off when the next project reads the log. At initiation and planning, search the
repository by `category` and `applies_to` for the kind of work ahead (a vendor integration,
a go-live, a new team), and turn each relevant lesson into a plan task, a checklist item or a
risk with an owner (`project-planning`, `risk-management`). Recording which past lessons
were used gives the check-back its evidence.

## 5. Status lifecycle

| Status | Meaning | Moves on when |
|---|---|---|
| `open` | Captured; no action started (or recorded only, for pattern-spotting) | An owner accepts the action and the due date |
| `in-progress` | The owner is making the change | The change is in the target |
| `adopted` | The change is in the target: backlog item done, template published, issue-log action closed | The check-back confirms it was used and worked |
| `verified` | The check-back found the change in use and the problem gone, or the practice repeated | Final |
| `declined` | Decided not to act, with the reason and who decided in `check_back_result` | Final; reopen only as a new id |

"Done" is not a status: a template edit nobody uses is `adopted`, not `verified`.

## 6. The check-back
On each `check_back_date`, ask three questions and record the evidence in `check_back_result`:
1. **Is the change in the target?** The backlog item is done, the template has the section,
   the checklist has the line.
2. **Was it used?** The next sprint ran with it, or the next project's plan contains it.
3. **Did the outcome change?** The metric moved, or the problem has not recurred.

Outcomes:
- All three yes: `verified`.
- Not done: re-plan once with a new date and the owner's agreement; if it slips again,
  escalate (to the product owner for a sprint action, the steering committee for a project
  action, the PMO Lead for an organisational one).
- Done but did not work: the root cause was wrong; take it back through 5 whys with the new
  evidence and write a new recommendation.

Healthy-system measures, reviewed by the PMO each quarter: the share of actionable lessons
`verified` within 90 days of adoption; retrospective actions done by the next retrospective;
and recurrence, the same root cause showing up in a later project's log.

## 7. Helios routing (log at closure, 2026-11-20)

| Id | Lesson | Path | Target | Status |
|---|---|---|---|---|
| LL001 | Vendor onboarding had no owner; SSO two weeks late | B, then C | PMO standard plan template: vendor onboarding workstream | in-progress; Sam Lee checks on 2027-02-03 |
| LL002 | 1.3.1 RED at the M2 close; sponsor told of the threat to M4 only at the DEC002 escalation | B, then C | Helios reporting rule from 2026-07-03; PMO status-report standard | adopted |
| LL003 | Reused API design put the knowledge base ahead of plan | C | Engineering standards library | adopted |
| LL004 | Shared QA environment with stale data | B, then C | Issue I003; PMO test-strategy checklist | in-progress |
| LL005 | Stand-ups ran over 30 minutes | A | Sprint S3 backlog; team working agreement | verified at the S3 retrospective |
| LL006 | Out-of-scope list settled late requests | C | Charter template (required element) | verified: already required |
| LL007 | Agent training planned to finish on launch day | C | PMO standard plan template | in-progress |

At closure the log went to `project-closure`: the post-project review on 2026-11-04 confirmed
LL001-LL007 and the top five went into section 8 of the closure report. Every lesson not yet
`verified` has a check-back on 2027-02-03 by someone who stays reachable after the team is
released: the PMO Lead, except for LL001, which the PMO Lead owns and Sam Lee checks.
