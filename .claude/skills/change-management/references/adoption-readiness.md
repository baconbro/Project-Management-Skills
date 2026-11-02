# Adoption and Readiness

Delivering a system or process is only half the job; the other half is getting people to use
it. Adoption (organizational change management) moves people from the current way of working to
the new one, and it is planned and measured like any other deliverable. Examples use the sample
Helios project (a fictional customer self-service portal used throughout this catalog): a
technically perfect portal that its 60 support agents quietly work around, still resetting
passwords by hand when customers phone, has failed, because the benefit (password-reset and
order-status tickets down 50% within 6 months of launch) never arrives. Write the plan with
`assets/adoption-plan-template.md`; `assets/adoption-plan-sample.md` is the Helios plan.

## The sponsor's active, visible role
Active and visible sponsorship is the most consistently reported success factor in
organizational change. People take their cue from the executive who owns the outcome, not from
the project manager's emails. The sponsor's part is specific, scheduled and seen:

| ADKAR step | Sponsor action (not delegable to the PM) | Helios: Dana Okoro, VP Customer Operations |
|---|---|---|
| Awareness | Explains the case for change in person, in business terms | Presents the case (40% of tickets, about $600k a year, the 50% target) at the Customer Operations all-hands on 2026-05-14 |
| Desire | Agrees the target with the managers who must deliver it; answers "what happens to me?" | Agrees the 50% target with Priya Nair in person before the M1 baseline (2026-05-08); with her, briefs every agent team on the redeployment plan in the week of 2026-08-03 |
| Knowledge / Ability | Is seen using or endorsing the new way; protects time for training | Co-presents the M4 pilot launch on 2026-08-07; confirms agents' training time is protected from queue targets |
| Reinforcement | Asks for the adoption numbers at every review; removes the old path; recognises adopters | Reviews the adoption dashboard at each bi-weekly steering from M4; announces the retirement of the old ticket-form categories (2026-10-19); chairs the monthly Customer Operations review of benefit B001 |

The PM schedules these actions, drafts the material and tracks them like tasks; the sponsor
delivers them. Middle managers (Helios: Priya Nair, Head of Support Operations) carry the same
message to their teams, which is why the sponsor and they must agree first. A sponsor who will
not take visible actions is a risk: log it in the risk register and raise it at steering.

## ADKAR: the individual change sequence
People change one at a time, in order. ADKAR names the five steps each person must complete; an
adoption gap is usually a *specific* missing step, which tells you the fix.

| Step | The person... | Gap symptom | Lever |
|------|---------------|-------------|-------|
| **A — Awareness** | knows *why* the change is happening | "Why are we doing this?" | The sponsor communicates the case for change |
| **D — Desire** | *wants* to participate and support it | "What's in it for me? I'd rather not." | Address what's in it for them, involve, surface concerns |
| **K — Knowledge** | knows *how* to change | "I don't know how to use it." | Training, documentation, job aids |
| **A — Ability** | *can* do it in practice | "I learned it but I'm slow / it's hard." | Coaching, practice, support, time |
| **R — Reinforcement** | *sustains* the new behaviour | "I've slipped back to the old way." | Targets and measures, recognition, remove the old path |

Diagnose at the weakest step: training (Knowledge) does nothing if the real blocker is Desire.

## Readiness assessment
Before each release, rate how ready each affected group is to adopt, High / Medium / Low:
- **Impact:** how much does their day-to-day work change? (bigger change = more support needed)
- **Attitude:** supportive, neutral or resistant today? (take the current stance from
  `stakeholder-management`)
- **Capacity:** do they have the time, skills and tools to absorb the change now?
- **History:** how have past changes gone here? (change fatigue is real)

Readiness is Low when impact is high and attitude or capacity is low. Record the evidence
(interviews, survey, training records) and the group's weakest ADKAR step. High-impact,
resistant groups get the most deliberate plan: Helios support agents are high impact (their
daily work changes and 6 FTE move to the complex-case queue), resistant (job security) and
stretched (20 of them are released for UAT), so their weakest step is Desire, not Knowledge.

## Adoption targets, agreed before go-live
"Measure adoption" means nothing without a target set in advance. Before go-live, the sponsor
and the benefit owner agree, for each affected group, at least one adoption target with a
measure, a baseline, a target value, a date, a data source and an owner. Use both kinds:
- **Leading (behaviour) measures** that move within weeks: people trained, journeys completed,
  active users, share of contacts handled the new way.
- **Lagging (benefit) measures** from the business case that move over months: tickets avoided,
  cost saved.

Helios agreed its targets at the steering committee of 2026-07-28, before the M4 pilot: all 60
agents trained before go-live; at least 60% of the 200 pilot customers completing a self-service
journey within 4 weeks of M4; at least 80% of started reset and order-status journeys completed
during hypercare; weekly self-service deflection of at least 30% by 2026-10-30 and 40% by
2027-01-31; and the benefit itself, the two ticket types down from 5,000 to 2,500 a month by
2027-04-03. The leading targets become go/no-go and hypercare criteria in `release-and-cutover`;
the benefit is tracked by its owner after `project-closure`.

## Resistance management
Resistance is information, not an obstacle to crush. Keep a resistance log (source, what you
see, root cause, type, response, owner) and treat each entry as a signal:
- **Find the root cause:** fear of job loss, extra workload, lost status, a genuine flaw, or
  simply not being consulted.
- **Respond to the cause, not the symptom:** involvement and early input prevent more resistance
  than any amount of persuasion after the fact.
- **Engage influencers:** a respected sceptic who turns becomes your best advocate.
- **Distinguish** "this is badly designed" (fix the product: raise a defect, or a CR through
  `change-request` if it changes a baseline) from "I don't want to change" (work the ADKAR
  steps). The first kind of resistance is a gift.

Helios: the agents' fear of job loss was answered by the redeployment plan (6 FTE to the
complex-case queue, no attrition, dis-benefit D001), signed before cutover and explained in
person by Dana Okoro and Priya Nair; their complaint that knowledge-base articles were wrong for
order-status edge cases was a genuine flaw and went to the product backlog.

## Reinforcement: making it stick
Adoption decays without reinforcement. From go-live until the targets are met:
- **Measure** against the agreed targets every week and act on what the numbers show.
- **Recognise and celebrate** early adopters and wins, with the sponsor visibly involved.
- **Remove the old path** where feasible, on a date the sponsor announces, so reverting is not
  an easy option (Helios: the password-reset and order-status ticket-form categories retire on
  2026-10-19, after a full week at 100% inside thresholds; Priya Nair decides).
- **Close the loop** on feedback: fix the friction users hit, or they will abandon the new way.
- **Hand over ownership:** reinforcement outlives the project. Name who owns the measures and
  actions after handover (Helios: Priya Nair as benefit owner, reviewed monthly at the Customer
  Operations review chaired by Dana Okoro).

Plan the training and communication work as WBS deliverables (Helios: 1.5.1 Training &
communications) and run them through `project-delivery` so they are owned, not assumed.

## By approach
- **Waterfall:** one adoption plan for the big release; readiness assessed at T-4 weeks and
  checked at the go/no-go; reinforcement runs through hypercare and beyond.
- **Agile:** adoption rides each increment; early users give feedback at every sprint review;
  readiness and targets are set per release goal.
- **Hybrid (Helios):** the plan is staged per release: pilot cohort of 200 at M4, then a 25% →
  50% → 100% ramp at GA from 2026-10-03 to 2026-10-12, each step gated on the adoption and
  hypercare measures.
