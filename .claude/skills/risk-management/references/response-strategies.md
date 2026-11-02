# Risk Response Strategies

Once a risk is prioritized, choose a deliberate response, name who carries it out, and record
it: the one-line response, trigger and residual score in the register
(`.claude/skills/risk-register/assets/risk-register-template.csv`), and each action in the
response action log (`assets/risk-response-plan-template.csv`). Threats and opportunities each
have their own strategies, plus accept and escalate for both. Match the response to the
exposure — never spend more managing a risk than it could cost. Examples use the sample Helios
project (a fictional customer self-service portal used throughout this catalog).

## Threat strategies (negative risk)

| Strategy | What it means | Helios example |
|---|---|---|
| **Avoid** | Remove the threat by changing the plan, scope or approach, so it cannot occur. | No in-house customer credential store: customer sign-in is bought on the existing identity provider, which removes the threat of a home-built store failing a security review. |
| **Transfer** | Shift the financial impact (not the risk itself) to a third party through a contract, warranty or insurance. | R001: firm fixed price for IdentityCo's services, a dated sandbox, delay credits of 5% a week capped at 15%, payment on acceptance. `procurement-management` chooses the contract type and its risk allocation and tracks the dated sandbox in `.claude/skills/procurement-management/assets/vendor-onboarding-checklist.md`. The schedule impact stays with Helios. |
| **Mitigate** | Reduce probability and/or impact to an acceptable level. | R001: an integration spike in week 1 of the integration work, probability 0.4 → 0.2. R002: scope baselined at M1 with change control, 0.6 → 0.3. R003: pairing and documented designs, impact $80,000 → $40,000. |
| **Accept — active** | Take no action now, but set aside contingency and a contingent plan with a trigger. | R004: monthly invoice review; draw contingency if hosting runs above 110% of forecast. R005: one sprint of polish buffer if usability round 1 finds more than 5 medium issues. |
| **Accept — passive** | Document and review only; deal with it if it happens. | A LOW threat below the MEDIUM threshold whose response would cost more than its exposure. |
| **Escalate** | The threat is outside the project's authority or affects more than the project. | A possible enterprise-wide change to identity policy would alter every customer login: Sam Lee escalates it to the sponsor, Dana Okoro, who takes it to the steering committee / portfolio board. Once they accept ownership it leaves the project register, marked as escalated. |

**Acceptance is a choice, not a default.** Passive acceptance suits low-exposure risks; a HIGH
risk accepted passively is an unmanaged risk. Active acceptance always comes with contingency and
a contingent plan.

## Opportunity strategies (positive risk)

| Strategy | What it means | Helios example |
|---|---|---|
| **Exploit** | Make sure the opportunity definitely happens. | Put the portal link in the auto-reply to every password-reset and order-status ticket from pilot day, so deflection is designed in rather than hoped for. |
| **Share** | Partner with a party better placed to realize it and share the benefit. | Co-build the knowledge-base search with the platform team that will reuse it, splitting the effort and the benefit. |
| **Enhance** | Increase its probability and/or positive impact. | R006: publish the top-20 articles before the pilot and measure deflection, probability 0.3 → 0.5. |
| **Accept** | Welcome it if it arises, without pursuing it. | If early deflection frees support budget, take it — but do not bank it or net it off the reserve. |
| **Escalate** | The benefit is beyond the project's scope to capture. | A reusable self-service platform for other products: escalate to the sponsor so the portfolio funds and owns it. |

## Elements of a complete response
For every material risk, record:
- **Strategy and actions** — proactive actions done now, each with an action owner and a due date.
- **Trigger** — the observable early-warning sign that the risk is about to occur (R001: "Vendor
  sandbox not available by end of week 2 of the integration work, or unavailable at any time
  during it" — it fired on 2026-06-12, when the sandbox went down in week 5 of the integration).
- **Contingent plan** — what happens when the trigger fires, and who funds it (R001: build an
  identity-provider stub so sprint work continues, claim the delay credits, escalate).
- **Fallback plan** — what to do if the contingent plan fails too (R001: the escalation path in
  the risk management plan — management reserve, scope trade-off or re-baseline).
- **Cost and schedule effect** — the effort and money the response needs, and where it is funded:
  a work-package estimate, a contract (terms set with `procurement-management`), or the
  contingency.
- **Residual risk** — the probability and impact left after the response; accept it consciously
  and keep it in the register (`residual_probability`, `residual_impact`).
- **Secondary risk** — any *new* risk the response creates. Transferring R001 to IdentityCo
  creates a vendor-dependency risk: delay credits are capped at 15% and do not recover the
  schedule. Always ask "what new risk does this response create?"

## Is the response worth it?
Compare the cost of the response with the EMV it removes:

```
EMV removed = (inherent P x inherent impact) - (residual P x residual impact)
```

Helios R001: (0.4 x $120,000) - (0.2 x $120,000) = $24,000 removed for a spike costing about a
week of two engineers' time — clearly worth it. R005: $2,800 of exposure does not justify more
than a small buffer, hence active acceptance. Across the register, the planned responses cut
threat EMV from $94,300 to $52,300. A response that costs more than it removes needs another
reason — compliance, safety or reputation — written next to it.

## Choosing well
1. Size the response to the exposure (from the `risk-register` scores).
2. Prefer avoid or exploit for the highest-severity items where feasible; mitigate where not.
3. Name an owner and a trigger for every response — an unowned response is a wish.
4. Turn every proactive action into scheduled, funded work; responses that live only in the
   register do not happen.
5. Re-score after responses are planned; the residual exposure is what you govern and what sizes
   the contingency (`references/quantitative.md`).
6. Escalate to the sponsor, then the steering committee — never to "management" in general — and
   escalate the decision needed, with options and a recommendation.
