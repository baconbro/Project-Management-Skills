# Premature closure — stopping a project well

Load this when a project is being cancelled, terminated or stopped before it finishes. Good
reasons to stop include: the business case no longer holds (benefits fell or costs rose past
the switching values), the strategy or the organization changed, a critical dependency or
supplier disappeared, the product failed a gate it cannot pass, funding was withdrawn, or a
better option appeared. Stopping a project that can no longer deliver its value is
governance working, not failure. PRINCE2 calls this premature closure; the PMBOK Guide's
close project or phase process covers terminated projects as well. Either way, a stopped
project still needs a decision record, a salvage review, closed obligations, lessons and a
closure report. The examples use the sample Helios project (a fictional customer
self-service portal used throughout this catalog); Helios actually finished, so its example
in section 6 is hypothetical.

## 1. Who decides
Only the sponsor, or the body that authorised the project (investment board, portfolio
committee), can stop it. The project manager's job is to recommend early and with evidence:
- the re-appraisal in `business-case` shows a switching value crossed or the net present value
  negative on the current forecast;
- a tolerance is breached with no credible recovery plan;
- the benefit owner withdraws, or the problem the project solves has gone away;
- a supplier or dependency fails in a way that cannot be replaced inside the tolerances.

Sunk cost is not a reason to continue: only the cost still to spend and the benefits still
obtainable matter. A **pause** (stop work, keep the structure, decide again by a set date)
is not a closure; record it as a pause with its review date, and do not release the team or
terminate contracts until the decision is final.

## 2. The termination decision record (replaces acceptance in step 1)
Record it in Part T of a copy of `assets/acceptance-record-template.md`, signed by the
decider:
- **Decision:** stop now, or stop at a defined point (for example "after the current sprint").
- **Decider and date**, and the forum in which it was taken.
- **Reason and evidence:** the re-appraisal, the breached tolerance, the external event.
- **Stop-work date:** when the team and the vendors stop work, and who tells them.
- **Salvage decisions** (section 3) and **obligations to close** (section 4).
- **Who communicates** the decision to the team, customers and stakeholders, and when.

Completed work that is kept is still accepted formally, in Part B, against criteria agreed
with the sponsor (see `references/acceptance-at-closure.md`).

## 3. Salvage review
For every deliverable or work product, record its state, its value if kept, the decision and
the receiving owner. Salvage is often worth more than it looks.

| Work product | State | Options |
|---|---|---|
| Research, requirements, designs | Complete or partial | Archive for reuse by the next attempt; hand to the product or business owner |
| Code, configuration, environments | Partial | Finish a usable slice ("complete to salvage"), archive the repository, or decommission |
| Something already live (a pilot) | Live | Keep it running (hand over to operations with an owner) or decommission it on a plan; a decommission can need its own cutover and communications (`release-and-cutover`) |
| Data | Collected | Keep under the owner's retention rules, return it, or delete it with a certificate |
| Licences, subscriptions, hardware | Bought | Transfer to another owner, cancel at the next notice date, or return |
| People's skills and knowledge | Built | Record in lessons; release people to work that can use them |

## 4. Obligations and wind-down
- **Contracts:** give notice under each contract's termination terms through
  `procurement-management`; accept and pay for work delivered, settle termination costs,
  credits and retention, revoke access and recover or delete data. Notice periods are often
  the longest item on the critical path of a closure, so start them on the decision date.
- **Commitments:** cancel open purchase orders, stop recurring charges (cloud, licences) and
  accrue termination costs before the cost codes are closed.
- **People:** tell the team in person before the wider announcement, explain the reason,
  recognise the work, keep the post-project review blameless, and give line managers
  feedback and release dates. A stopped project's team is the most likely to leave the
  organization; treat the release with care.
- **Customers and stakeholders:** list every promise made (pilot users, partners, other
  teams waiting on an output) and tell each one what happens now; the communication plan in
  `project-communication` gives the channels.
- **Risks, issues and changes:** close them, or transfer the ones that outlive the project
  (for example a data-retention obligation) to a named owner.
- **Legal and regulatory:** records retention, privacy obligations, any regulator or auditor
  that must be told.

## 5. How steps 2-8 change
| Step | On a stopped project |
|---|---|
| 2 Handover | Only salvaged items and anything left live are handed over, each to a named owner who signs |
| 3 Open items | Add the terminated contracts, stop-work instructions, data disposition and decommission tasks to the closeout log |
| 4 Finances | Include termination costs and accruals; return the unspent budget and reserves; report the cost to stop against the cost to finish |
| 5 Benefits | Record each benefit as forgone, partly realised (for example by a pilot that keeps running) or transferred to another initiative, and tell the portfolio or the business-case owner |
| 6 Review | Mandatory, blameless and early: stopped projects teach the most, and the team disperses fast |
| 7 Team and records | Release with care (section 4); archive the decision record and the salvage register with the project records |
| 8 Report | Closure type `stopped early`; the report states the reason, the decider, the salvage and the cost to stop |

## 6. Helios illustration (hypothetical)
Suppose that at the end of month 3, instead of the two-week sandbox outage that actually
happened, IdentityCo had announced it was withdrawing the sign-in interface Helios depended
on, and a replacement provider would add about $200,000 (+40% on the $500,000 BAC, beyond the
39% cost switching value in the business case). Sam Lee (project manager) re-runs the
appraisal with `business-case`, recommends stopping the portal, and Dana Okoro (Sponsor, VP
Customer Operations) decides at the steering committee to stop at the end of the current
sprint. The termination record then shows:
- **Salvage:** finish the knowledge base (73% earned: $33,000 of its $45,000 budget) as a
  public help centre handed to Priya Nair, since it can deflect tickets without sign-in;
  archive the research, scope statement and prototype for a later attempt; archive the
  self-service UI code.
- **Contracts:** terminate the IdentityCo services contract under its terms, paying only the
  accepted "sandbox connected" milestone and claiming the delay credit already due; revoke the
  sandbox access.
- **Benefits:** B001 (the 50% ticket cut) partly realised through the help centre and
  re-baselined by Priya Nair; the other benefits forgone.
- **Lessons:** the dependency on a single identity provider without an exit plan.

## Anti-patterns
- Letting a project drift for months after everyone knows it should stop ("zombie project").
- Stopping by email: no decision record, no salvage review, no contract notices.
- Discarding completed work that could have been handed over or reused.
- Skipping lessons because the subject is uncomfortable.
- Releasing the team before the post-project review and the salvage handover are done.
