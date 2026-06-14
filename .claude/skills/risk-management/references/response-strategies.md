# Risk Response Strategies

Once a risk is prioritized, choose a deliberate response, assign an owner, and capture a
concrete action in `risk-register`. Threats and opportunities each have their own set of
strategies plus a shared "escalate/accept" path. The strategy should match the risk's
severity — do not spend more managing a risk than the risk could cost.

## Threat strategies (negative risk)

| Strategy   | What it means                                              | Helios example |
|------------|------------------------------------------------------------|----------------|
| **Avoid**  | Eliminate the threat by changing the plan or scope.        | Drop the riskiest custom integration; use the vendor's hosted widget instead. |
| **Transfer** | Shift impact (not the risk itself) to a third party.     | Contractual SLA / penalty with IdentityCo; insurance; fixed-price subcontract. |
| **Mitigate** | Reduce probability and/or impact to acceptable levels.   | Run an integration spike in week 1 to retire technical uncertainty early. |
| **Accept** | Take no proactive action; deal with it if it occurs.       | Minor UI polish risk — hold a sprint of buffer (active) or just monitor (passive). |
| **Escalate** | The risk is outside the project's authority; raise it.   | Enterprise-wide identity policy change — escalate to `senior-pm` / portfolio. |

**Active vs passive accept:** active acceptance sets up a contingency reserve or plan;
passive acceptance simply documents and monitors. Acceptance is a *choice*, not a default.

## Opportunity strategies (positive risk)

| Strategy   | What it means                                              | Helios example |
|------------|------------------------------------------------------------|----------------|
| **Exploit** | Make sure the opportunity definitely happens.             | Assign your best engineer to ship the reusable auth module that other teams want. |
| **Share**   | Partner so a third party better placed can help realize it.| Co-build the component with the platform team and split the benefit. |
| **Enhance** | Increase probability and/or positive impact.              | Add analytics so the ticket-deflection upside is measured and amplified. |
| **Accept**  | Welcome it if it arises, without actively pursuing it.     | If early deflection frees budget, use it — but do not bank on it. |
| **Escalate**| Benefit is beyond the project's scope to capture; raise it.| A reusable platform capability — escalate so the portfolio funds and owns it. |

## Residual and secondary risk
- **Residual risk:** what remains after the response is applied — accept it consciously and
  keep it in the register.
- **Secondary risk:** a *new* risk introduced *by* your response (transferring to a vendor
  creates vendor-dependency risk). Always ask "what new risk does this response create?"

## Choosing well
1. Size the response to the exposure (from `risk-register` scoring).
2. Prefer avoid/exploit for the highest-severity items where feasible.
3. Name an owner and a trigger for every chosen response — an unowned response is a wish.
4. Re-score after responses are planned; the post-response exposure is what you govern.
