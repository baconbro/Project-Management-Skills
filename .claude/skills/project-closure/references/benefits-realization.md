# Benefits realization — make the value stick after delivery

Load this for step 5 of the workflow. Most benefits arrive **after** the project ends, so
closure must hand each one to a named owner with a measure, a baseline, a target, review
dates and a forum that will still exist when the reviews fall due. The benefits were promised
in the benefits register of `business-case`; this file covers what happens to them at and
after closure, including when no business case was ever written. Examples use the sample
Helios project (a fictional customer self-service portal used throughout this catalog).

## Why this matters
A project delivers an output (a portal); the organization wants an outcome (customers serve
themselves) and ultimately a benefit (fewer tickets, lower cost). If nobody owns the benefit
after go-live, the project can "succeed" while the investment never pays back, and nobody
learns that the business case was optimistic.

## From output to benefit
- **Output** — what the project produced. _Helios: the self-service portal is live to all customers._
- **Outcome** — the change in behaviour. _Helios: customers reset passwords and check orders themselves._
- **Benefit** — the measurable value. _Helios: password-reset and order-status tickets cut
  by 50% within 6 months of launch, about $300,000 a year of the ~$600,000 handling cost._
- **Dis-benefit** — a measurable negative some stakeholders feel. _Helios: 6 support agents
  (FTE) redeployed to the complex-case queue; a possible CSAT dip in the cutover month._

Benefits are not acceptance criteria. Accept the output in step 1; hand the benefit to its
owner here.

## The benefits handover (at closure)
1. **List the benefits.**
   - *With a business case:* copy every benefit and dis-benefit from its benefits register,
     with type, measure, baseline, target and date.
   - *Without a business case:* derive them from the charter objectives and success criteria
     (one benefit per objective that describes a change in the business, not a deliverable).
     Where there is no number, record the benefit **qualitatively**: what will be observably
     different, who will notice, and the first date someone will look. A qualitative benefit
     with an owner and a date is worth more than an invented figure.
2. **Check the baseline.** A target without a "before" number cannot be proven. If no
   baseline was taken, take one now from the earliest data available and say so; a late
   baseline is better than none.
3. **Confirm one benefits owner per benefit.** The owner is named in the `business-case`
   benefits register and confirmed at the initiation gate (G0 in `project-initiation`); here
   the owner accepts accountability in writing. Name an owner now only for a benefit the case
   left without one: usually in operations or the business, never the project team (it
   disbands at closure).
4. **Agree the review dates and the forum.** Typical points are +3, +6 and +12 months after
   go-live, until the benefit is realised or formally written off. The steering committee
   disbands at closure, so name the meeting that will receive the reviews (an operations
   review or a portfolio board) and its chair.
5. **Hand over the measurement method and tooling** (report, query, dashboard) so the owner
   can measure without the project team.
6. **Record the first readings.** Leading measures (adoption, deflection rate) usually move
   before closure; record them as the starting trend, not as proof.
7. **Record all of it** in section 7 of `assets/closure-report.md`.

## Tracking after closure
- Measure actual against target on the agreed dates and explain every gap.
- Keep tracking until each benefit is realised or formally written off, not just to go-live.
- Feed surprises (benefits over or under target, unforeseen dis-benefits) into
  `lessons-learned` and back to the business-case owner, so future cases are more honest.
- If a benefit cannot be realised without more work, that work is a new change or project,
  not a reason to reopen the closed one.

## Benefits handover table
Use this shape in section 7 of the closure report; one row per benefit or dis-benefit.

| Id | Benefit or dis-benefit | Measure | Baseline | Target and date | At closure | Owner | Reviews and forum |
|---|---|---|---|---|---|---|---|
| `<id>` | `<benefit>` | `<measure, leading and lagging>` | `<before value, or "none: taken on <date>">` | `<target> by <date>` | `<first reading or qualitative sign>` | `<name, role>` | `<dates>; <forum, chair>` |

### Sample: Helios at closure (2026-11-20)
Sample rows from the Helios closure report; the business case's register is the source.

| Id | Benefit or dis-benefit | Measure | Baseline | Target and date | At closure | Owner | Reviews and forum |
|---|---|---|---|---|---|---|---|
| B001 | Reduced ticket handling cost | Monthly password-reset and order-status tickets; weekly self-service deflection % | 5,000 a month (May-July 2026 average, before the pilot) | 2,500 a month (−50%) by 2027-04-03 | October 3,900 (−22%) during the ramp; deflection 31% in the last week | Priya Nair, Head of Support Operations | Monthly; formal 2027-01 and 2027-04; Customer Operations review, chair Dana Okoro |
| B002 | Faster issue resolution | Mean time to resolve the two ticket types | 26 h | Instant self-service; 2 h assisted, by 2027-01 | Assisted 9 h in October | Priya Nair | 2027-01; same forum |
| B003 | Higher customer satisfaction | Quarterly CSAT | 72% | 80% by 2027-10 | 73% in October | Dana Okoro, VP Customer Operations | 2027-01, 2027-04, 2027-10; same forum |
| D001 | Support agents redeployed (6 FTE) | FTE moved; attrition | 0 moved | 6 moved with no attrition by 2027-04 | 2 moved; redeployment plan signed | Priya Nair | 2027-01, 2027-04 |
| D002 | Temporary CSAT dip in the cutover month | CSAT in October 2026 | 72% | No more than 3 points down | No dip (73%); closed | Dana Okoro | Closed at closure |

## Anti-patterns
- Treating go-live as the finish line and never measuring whether benefits arrived.
- Leaving benefits owned by the project team, who disband at closure.
- Targets with no baseline, so "improvement" cannot be proven.
- Review dates with no forum, so the review never happens.
- Counting early leading measures as realised benefits.
- Ignoring dis-benefits until they become complaints.
