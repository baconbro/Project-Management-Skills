# Methodology selection — waterfall vs. agile vs. hybrid

Load this to recommend a delivery approach. The goal is not dogma; it is to match the
approach to how much the requirements and the path are understood. Examples use the
running sample project: **Helios**, a customer self-service portal.

## The core question
How much is known up front, and how expensive is change?
- Known scope + costly change → lean **waterfall**.
- Uncertain scope + cheap, valuable feedback → lean **agile**.
- Fixed outcome/constraints + flexible path → lean **hybrid**.

## Waterfall — sequential, plan-driven
Phases run in order (initiate → plan → execute → close) with sign-offs between them.

Fits when:
- Requirements are stable and well understood before work starts.
- Change is expensive or risky (regulated, fixed-price, physical build, safety-critical).
- Stakeholders need predictable scope, cost, and dates and formal stage gates.

Signals you are in waterfall territory:
- A fixed-price contract or a hard regulatory deadline.
- "We know exactly what we need; just build it."
- Heavy compliance, audit, or documentation requirements.

## Agile — iterative, change-driven
Work is delivered in short increments; priorities are re-set each iteration from feedback.

Fits when:
- Requirements are uncertain or expected to evolve.
- Early, frequent delivery is valuable and feedback can change direction.
- A cross-functional team can work closely with an engaged product owner.

Signals you are in agile territory:
- "We are not sure what users want yet; we will learn as we go."
- Value comes from getting something usable in front of users quickly.
- The team can release in small increments without huge release overhead.

## Hybrid — fixed frame, iterative delivery
Outcomes, budget, and key dates are fixed at the top; delivery inside that frame is
iterative. The most common real-world choice — and the right call for Helios.

Fits when:
- Sponsors need committed outcomes/budget but scope detail is still emerging.
- Some parts are well understood (auth, hosting) and some are not (UX, content).
- Governance demands milestones and reporting, but the team wants iteration.

Signals you are in hybrid territory:
- "Launch must hit Q4 within this budget, but we will iterate on the features."
- A planned baseline at the top, sprints underneath.

## Quick decision checklist
Score each: Yes = agile-leaning, No = waterfall-leaning.
- [ ] Are requirements likely to change as we learn?
- [ ] Is early/partial delivery genuinely valuable to users?
- [ ] Can we release in small increments cheaply?
- [ ] Is the team cross-functional with an available product owner?
- [ ] Is change cheap rather than costly/risky?

Mostly Yes → **agile**. Mostly No → **waterfall**. A mix, or fixed
outcomes with uncertain detail → **hybrid**. When in doubt for a delivery project with
committed dates, default to **hybrid** and tighten toward one end as certainty grows.
