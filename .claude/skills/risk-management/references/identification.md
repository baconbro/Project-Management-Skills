# Risk Identification Techniques

No single technique finds every risk. Combine a divergent technique (brainstorming,
pre-mortem) with a convergent one (checklists, assumptions analysis) so you cover both the
unknown and the known-but-overlooked. Capture both **threats** (negative) and
**opportunities** (positive) — identification is symmetric.

## 1. Brainstorming
Get the right people in a room (or board) and generate risks without judging them. Frame by
category to avoid tunnel vision: scope, schedule, cost, technical, resourcing, vendor,
security, regulatory, organizational change. For Helios, a brainstorm surfaced "identity
vendor misses the integration date", "agents resist the new tool", and the upside "self-service
deflects enough tickets to fund phase 2 early". Diverge first, cluster and score later.

## 2. Checklists
Reuse a structured list of risks that have hurt past projects of this type. Checklists are
fast and catch the obvious things teams forget under pressure. The weakness is that they only
find risks someone already knew about — never run a checklist *alone*. Source checklists from
lessons-learned, industry standards, and your own portfolio history.

## 3. Assumptions and Constraints Analysis
Every plan rests on assumptions. List them, then ask of each: *what if this is false?* A false
assumption is a risk; a binding constraint is a source of risk.
- Assumption: "IdentityCo's SSO API is stable." Risk if false: integration rework, slip.
- Constraint: "Launch must precede the renewal cycle." Risk: any delay compounds in cost.
Make implicit assumptions explicit — they are where projects quietly fail.

## 4. Pre-Mortem
Imagine the project has already failed spectacularly, then work backwards to explain *why*.
Because it gives permission to voice doubts, the pre-mortem surfaces risks that optimism and
politics suppress in a normal review.
- Prompt: "It is launch day for Helios and it was a disaster. What happened?"
- Harvest each story into a concrete, scoreable risk with a trigger.
Run it after a plan exists but before commitments harden.

## 5. SWOT
Strengths, Weaknesses, Opportunities, Threats — a quick structured scan that deliberately
includes the upside.
- **Strengths / Weaknesses:** internal, present (skilled team; first integration of this kind).
- **Opportunities / Threats:** external, future (reusable component for other products; vendor
  roadmap change).
SWOT is a good warm-up that reminds the team to look for opportunities, not only threats.

## From identification to the register
Whatever the technique, the output is the same: a list of specific, outcome-oriented risk
statements. Write them in cause–event–effect form — "*Because* the vendor API is new (cause),
*integration may slip* (event), *delaying launch and adding cost* (effect)." Log them into
`risk-register` for scoring; do not analyze severity here.
