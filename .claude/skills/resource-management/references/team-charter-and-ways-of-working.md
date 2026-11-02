# Team charter and ways of working

Load this to acquire, onboard, organise, develop and release the people behind the capacity
numbers. Fill `assets/team-charter-template.md` with the result. Examples use the sample
Helios project (a fictional customer self-service portal used throughout this catalog).

## Acquire the team
- **Start from the demand by role** (see `references/resource-capacity.md`), not from who is
  free. For each role decide: internal or external, full- or part-time, start and end week.
- **Internal people** come through their functional (line) managers. Agree the allocation in
  writing (percent or hours per week, for which weeks) and what happens when BAU spikes.
  In a matrix organisation the project manager borrows capacity; the line manager keeps the
  person's development and appraisal.
- **External people** (contractors, a vendor team) need a statement of work, onboarding
  lead time and an exit date; route the contract through procurement.
- **Pre-assignment**: some people are named in the business case or the contract (Helios:
  the identity-provider vendor's integration engineer); record them as constraints.
- **Virtual and distributed teams**: write down the overlap hours you can rely on; capacity
  outside them is not available for pairing or meetings.

## Onboard in the first week
- Access: accounts, repositories, environments, tools, the shared drive, the team channel.
- Context: charter, business case summary, plan, RACI, risk register, definition of done.
- People: a buddy, a 30-minute meeting with the product owner and the tech lead.
- A first small task that finishes within a week, so they ship something early.
- Capacity: plan new joiners at about 50% for their first sprint or two weeks.

## The team charter (working agreement)
A one- to two-page agreement the team writes together at kickoff and revisits each phase or
every few sprints. It covers:
| Element | Helios example |
|---|---|
| Purpose and outcomes | Cut password-reset and order-status tickets by 50% within 6 months of launch |
| Roles and decision rights | Product owner Ava Chen owns backlog order; tech lead Ben Adeyemi owns technical design; RACI in `raci-matrix` |
| Core hours and availability | 10:00–15:00 overlap; leave on the shared calendar 2 weeks ahead |
| Meetings | Daily 15-minute stand-up; weekly status report; bi-weekly steering committee |
| Communication norms | Chat for quick questions (reply within 4 working hours); decisions recorded in the decision log |
| Definition of done | Linked from `quality-management`; nothing is "done" without passing QA |
| Decision-making | Consult, then the named owner decides; disagree and commit |
| Conflict and escalation | Talk directly first, then the PM, then the sponsor (Dana Okoro) |
| Capacity rules | Plan to 80%; no one OVER in any week; changes to allocations go to the PM |

Keep it specific. "We communicate openly" is not an agreement; "blockers are raised at
stand-up the same day" is.

## Develop the team
- **Stages**: forming, storming, norming, performing, adjourning (Tuckman). Expect storming
  after the first missed date; the charter is the reference point that shortens it.
- **Cross-training** reduces key-person risk: pair Ben with Carla on the identity
  integration so two people understand it, and record the cover in the `skills` column.
- **One-to-ones** every two weeks for full-time members; recognition in the weekly review.
- **Feedback** on behaviours against the charter, not on personality.

## Handle conflict
| Mode | When it fits |
|---|---|
| Collaborate (problem-solve) | important issue, time to find a joint answer; the default |
| Compromise | equal power, a temporary settlement is acceptable |
| Accommodate | the issue matters more to the other party; preserve the relationship |
| Force (direct) | an emergency or a safety, legal or compliance line |
| Avoid (withdraw) | trivial issue, or a cooling-off period before collaborating |
Most project conflict is about priorities, schedules and resources rather than personalities;
settle priority conflicts with the product owner and the plan, not by who shouts loudest.

## Release people
- Plan releases as carefully as starts: an end week per person in the allocation file.
- Before release: knowledge transfer (runbooks, design notes, a recorded walkthrough),
  outstanding actions handed over, access removed, final feedback to the line manager.
- Update capacity: a released person's rows go to 0 so later weeks are checked honestly.
- At closure, recognise contributions and capture team lessons in the retrospective.

## Anti-patterns
- Acquiring whoever is free instead of the skills the work needs.
- A charter written by the project manager alone and never reread.
- Onboarding by "read the wiki" with no buddy and no first task.
- Releasing a specialist the week before the testing they are needed for.
