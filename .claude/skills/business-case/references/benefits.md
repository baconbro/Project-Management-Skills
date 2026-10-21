# Benefits and Dis-benefits

Benefits are the *reason* for the investment. A business case that lists costs but hand-waves
benefits cannot be justified. Make every benefit measurable (baseline and target), owned, and
time-bound — and name the dis-benefits before an affected stakeholder does. The examples use
the sample Helios project (a fictional customer self-service portal used throughout this
catalog).

## Benefit types
- **Tangible (cashable):** directly measurable in money — reduced cost, increased revenue,
  avoided cost. These, net of run costs, become the positive cashflows in
  `assets/cashflows.csv` and feed `scripts/roi_npv.py`.
- **Tangible (non-cashable):** measurable but not a cash saving — e.g. hours freed that are
  redeployed rather than removed from the budget. Quantify, but do not double-count as cash.
- **Intangible:** real but hard to price — customer satisfaction, brand, employee morale,
  compliance posture. State the measure even if you cannot price it.

## Baseline, target, date, owner
Every benefit needs five things or it will quietly evaporate:
- **Baseline (today):** the measured starting point. Helios: the three months of ticket volume
  before launch, and the ~$600,000 a year it costs to handle password-reset and order-status
  tickets (40% of all tickets).
- **Target:** the level and the date. Helios: those two ticket types cut by 50% within 6 months
  of launch.
- **Leading measure:** moves early and predicts the benefit (portal sign-ups, self-service
  adoption rate, deflection rate per week). Use it during delivery to confirm the benefit is on
  track — it is what the decision record's conditions should reference.
- **Lagging measure:** confirms the benefit after the fact (monthly ticket volume, annual
  cost-to-serve, CSAT). Use it at `project-closure` and the benefits review to prove realisation.
- **Benefit owner:** the person — usually in the business, not the project — accountable for
  realising the benefit after the project closes. Helios: Priya Nair, Head of Support Operations.

Record all of them in a copy of `assets/benefits-register-sample.csv`; it is the single list the
closure review confirms against.

## Dis-benefits
A **dis-benefit** is a measurable outcome that one or more stakeholders perceive as negative,
even though the investment as a whole is worthwhile: agent redeployment, temporary service
disruption during cutover, retraining load, a dip in a satisfaction score while users adapt.
Record each with the affected group, a measure, an owner and a mitigation, and net material
ones against the benefits. Cases that hide dis-benefits are challenged by exactly the people
who will experience them; cases that name them usually get a smoother approval.

## Worked example (Helios)
| Benefit                        | Type         | Baseline (today)                                   | Target                              | Leading measure              | Lagging measure                 | Value p.a. | Realised by          | Owner                |
|--------------------------------|--------------|----------------------------------------------------|-------------------------------------|------------------------------|---------------------------------|------------|----------------------|----------------------|
| Reduced ticket handling cost   | Cashable     | ~$600k/yr on password-reset and order-status tickets | -50% of those tickets (~$300k/yr)   | Self-service deflection %    | Monthly ticket volume by type   | $300,000   | 6 months after launch | Priya Nair           |
| Faster issue resolution        | Non-cashable | 26 h mean time-to-resolve for those ticket types   | Instant self-service; 2 h assisted  | Tickets resolved via portal  | Mean time-to-resolve            | hours freed, redeployed | 3 months after launch | Priya Nair     |
| Higher customer satisfaction   | Intangible   | CSAT 72% on support interactions                   | CSAT 80%                            | Portal NPS pulse             | Quarterly CSAT                  | —          | 12 months after launch | Dana Okoro          |

| Dis-benefit                                  | Who is affected     | Measure                       | Mitigation                                   | Owner       |
|----------------------------------------------|---------------------|-------------------------------|----------------------------------------------|-------------|
| 6 FTE of support agents redeployed           | Support agents      | FTE moved, attrition           | Redeployment plan to complex-case queue      | Priya Nair  |
| Temporary CSAT dip during cutover            | Customers           | CSAT in cutover month          | Pilot cohort of 200, staged rollout          | Dana Okoro  |

The cashable benefit less the portal's run cost gives the net cashflows in `assets/cashflows.csv`:
$150k in year 1 (ramp-up), $180k in year 2, then $200k a year.

## Common mistakes
- Claiming benefits with no baseline, so "improvement" can never be proven.
- Counting the same saving twice (once as cash, once as freed time).
- No benefit owner, so nobody is accountable after the project ends.
- No realisation date, so the benefit is "still coming" forever.
- Optimism bias — inflating benefits to clear the investment hurdle (test it with the
  sensitivity step and the stress factors in `financial-appraisal.md`).
- Omitting dis-benefits, so the first stakeholder challenge derails the approval.
