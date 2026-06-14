# Benefits

Benefits are the *reason* for the investment. A business case that lists costs but
hand-waves benefits cannot be justified. Make every benefit measurable, owned, and
time-bound.

## Benefit types
- **Tangible (cashable):** directly measurable in money — reduced cost, increased
  revenue, avoided cost. These feed the financials and `scripts/roi_npv.py`.
- **Tangible (non-cashable):** measurable but not a cash saving — e.g. hours freed that
  are redeployed rather than removed from the budget. Quantify, but do not double-count
  as cash.
- **Intangible:** real but hard to price — customer satisfaction, brand, employee
  morale, compliance posture. State the measure even if you cannot price it.

## Leading vs. lagging measures
- **Leading measures** move early and predict the benefit (e.g. portal sign-ups,
  self-service adoption rate). Use them to confirm the benefit is on track.
- **Lagging measures** confirm the benefit after the fact (e.g. annual cost-to-serve,
  call volume, CSAT). Use them to prove the benefit was realized.

A good benefit pairs a leading indicator (early signal) with a lagging indicator (proof).

## Every benefit needs a benefit owner
The **benefit owner** is the person — usually in the business, not the project — who is
accountable for actually realizing the benefit after the project closes. Without an
owner, benefits quietly evaporate. Record owner, baseline, target, measure, and the date
the benefit is expected to land.

## Worked example (Helios)
| Benefit                         | Type        | Leading measure        | Lagging measure       | Owner            |
|---------------------------------|-------------|------------------------|-----------------------|------------------|
| Reduced call-center handling    | Tangible $  | Self-service adoption %| Annual cost-to-serve  | Head of Support  |
| Faster issue resolution         | Tangible    | Tickets via portal     | Mean time-to-resolve  | Support Ops Lead |
| Higher customer satisfaction    | Intangible  | Portal NPS pulse       | Annual CSAT score     | Head of CX       |

The cashable benefits become the positive cashflows in `assets/cashflows.csv`.

## Common mistakes
- Claiming benefits with no baseline, so "improvement" can never be proven.
- Counting the same saving twice (once as cash, once as freed time).
- No benefit owner, so nobody is accountable after the project ends.
- Optimism bias — inflating benefits to clear the investment hurdle.
