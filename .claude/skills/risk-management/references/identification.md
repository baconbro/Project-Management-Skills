# Risk Identification Techniques

No single technique finds every risk. Combine a **divergent** technique (brainstorming,
pre-mortem) with a **convergent** one (checklists, assumptions and constraints analysis, SWOT)
so you cover both the unforeseen and the known-but-overlooked. Capture **threats** (negative
effect) and **opportunities** (positive effect) — identification is symmetric. Examples use the
sample Helios project (a fictional customer self-service portal used throughout this catalog).
Run the session with `assets/risk-workshop-template.md`.

## Risk or issue?
A risk is an *uncertain* future event or condition; an issue has already happened or is
certain. Test every candidate: "Has it happened, or is it certain to?" If yes, it goes to the
`project-delivery` issue log, not the register. "The vendor sandbox is down today" is an issue;
"the vendor may miss the sandbox date" is a risk.

## 1. Brainstorming by category
Get the right people together — team, product owner, operations, vendor, finance, security —
and generate risks without judging them. Frame by category so no area is forgotten (a simple
risk breakdown structure): scope, schedule, cost, technical, resourcing, vendor, security and
compliance, organizational change, benefits. Diverge first; cluster, de-duplicate and score
later. Helios' brainstorm produced, among others, "the identity-provider integration may slip"
(R001), "the lead engineer may leave" (R003) and the upside "the knowledge base may deflect
tickets earlier than planned" (R006).

## 2. Checklists
Reuse a structured list of risks that have hurt past projects of this type — from
`lessons-learned`, industry standards and your organization's own history. Checklists are fast
and catch what teams forget under pressure. Their weakness is that they only find risks someone
already knew about, so never run a checklist *alone*. Helios' checklist for portal projects
flagged hosting-cost overruns (R004) and usability rework (R005).

## 3. Assumptions and constraints analysis
Every plan rests on assumptions. Walk the assumptions and constraints log and ask of each
*what if this is false?* A doubtful assumption is a risk; a binding constraint is a source of
risk.
- Assumption A1 — "The existing identity provider supports customer logins without a license
  upgrade." If false, the SSO integration is reworked and slips: R001.
- Constraint CON-2 — "MVP live to the pilot cohort of 200 at M4, general availability at M6."
  Any slip on the 25-week critical path moves a committed date (Helios holds no schedule
  reserve before GA, and the SSO integration, knowledge base, reporting and training tasks
  have only 1 week of float each), so every critical or near-critical dependency on a vendor
  or another team is a candidate risk.
Make implicit assumptions explicit; that is where projects quietly fail. An assumption judged
safe still gets a validate-by date in the log.

## 4. Pre-mortem
Imagine the project has already failed, then work backwards to explain *why*. Because it gives
permission to voice doubts, the pre-mortem surfaces risks that optimism and politics suppress in
a normal review.
- Prompt: "It is general-availability day for Helios and it was a disaster. What happened?"
- Turn each story into a scoreable risk with a trigger: "the vendor sandbox came late" → R001;
  "new requirements kept arriving after sign-off" → R002.
- Run the reverse too — "Helios beat every target. Why?" — to surface opportunities (R006).
Run it once a plan exists but before commitments harden, and again before go-live.

## 5. SWOT
Strengths, weaknesses, opportunities, threats — a quick structured scan that deliberately
includes the upside.
- **Strengths / weaknesses** (internal, present): an incumbent identity provider; the team's
  first customer-facing SSO integration.
- **Opportunities / threats** (external, future): earlier ticket deflection (R006); a change to
  the identity provider's roadmap.
SWOT is a good warm-up that reminds the team to look for opportunities, not only threats.

## From identification to the register
Whatever the technique, the output is the same: specific, outcome-oriented risk statements in
**cause → event → effect** form — "*Because* the identity provider's customer-login support is
unproven (cause), *the integration may slip* (event), *delaying the M4 pilot and adding cost*
(effect)."

| Weak statement | Why it fails | Better |
|---|---|---|
| "Integration risk" | No event, no effect — cannot be owned or triggered | "Identity-provider integration slips past the agreed date, delaying the pilot" |
| "Budget" | A category, not a risk | "Cloud hosting costs exceed the budget as pilot traffic grows" |
| "The sandbox is down" | Already happening | Log it as an issue; the risk was "the sandbox may be late" |

**Nominate an owner at identification.** Every risk gets a named owner the day it is logged —
the person best placed to watch it and act, not the project manager by default (Helios: R002
Dana Okoro, who controls scope; R004 Finance; R006 Priya Nair, the benefit owner). The owner
watches the risk until responses are planned and then owns the response. Log each risk in your
copy of `.claude/skills/risk-register/assets/risk-register-template.csv` with its `type`,
`category` and `owner`; scoring comes in the next step, not during identification.

## Keep identifying
Identification is not a kickoff event. Repeat it at each milestone or stage gate, when the
scope or a contract changes, after a risk occurs, and in agile delivery at refinement and retros.
A register that has not grown since planning is a warning sign, not a success.
