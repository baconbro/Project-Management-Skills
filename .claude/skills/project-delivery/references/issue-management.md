# Issue management — issue vs. risk vs. action vs. decision

Load this to keep the delivery log clean and to escalate well. The most common failure in
delivery is muddling these four item types, so nothing has a clear owner or next step. Use
it with `issue-log.csv`. Examples use the running sample project: **Helios**, a customer
self-service portal.

## The four types
- **Issue** — a problem happening **now** that threatens scope, schedule, cost, or quality.
  It needs resolving. _e.g. "The identity-provider sandbox is down, blocking auth testing."_
- **Risk** — a **future, uncertain** event that may threaten the project. It needs a
  response before it occurs. Risks live in the `risk-register`; an issue is a risk that has
  materialized. _e.g. "The identity provider may not be ready by the test window."_
- **Action** — a task someone has committed to do, usually out of a meeting. It needs
  doing. _e.g. "Ben to confirm the auth go-live date with the vendor by Friday."_
- **Decision** — a choice that has been made (or is needed) and should be recorded so it is
  not relitigated. _e.g. "Decided: launch with email login only; SSO deferred to phase 2."_

Rule of thumb: **risk = might happen; issue = is happening; action = to do; decision =
chosen.** When a risk occurs, close it in the register and open an issue.

## Logging items
Record each item in `issue-log.csv` with:
- `id`, `type` (issue/action/decision), `description`
- `owner` (exactly one), `priority`, `status`, `due`, `raised`

Every open item must have a single owner and a next step. An item with no owner is not
managed; it is just noticed.

## Prioritizing
- **High:** blocks delivery or risks a milestone, budget, or quality gate now.
- **Medium:** material but not blocking; resolve within the cadence.
- **Low:** minor; resolve when convenient or accept.

Work High items first; review them daily, Medium weekly.

## Escalation
Escalate when an item is beyond the team's authority, money, or time to resolve, or when it
threatens a baseline commitment. Escalate **early** with options, not just the problem:
1. State the item, its impact, and the deadline to decide.
2. Offer 2-3 options with trade-offs.
3. Name the decision you need and from whom.
4. Take it to the steering forum on the agreed cadence (see `delivery-cadence.md`).

If resolving an item changes the baseline (scope, schedule, cost), route it through a
`change-request` and `change-management`, not just the issue log.

## Anti-patterns
- Logging everything as an "issue" so risks are never managed before they hit.
- Items with no owner, or with a whole team as owner.
- Decisions made in meetings but never recorded, so they are reopened endlessly.
- Escalating a problem with no options, pushing the analysis onto the sponsor.
