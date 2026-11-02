---
name: risk-management
description: >-
  Runs the risk process: risk plan and appetite, identification workshops and pre-mortems,
  quantification, response strategies, a contingency reserve sized at a confidence level,
  and risk governance. Use when setting up risk management, choosing responses, or
  deciding how much contingency to hold.
metadata:
  version: 1.1.0
  category: discipline
  phase: cross-cutting
  related: [senior-pm, project-planning, risk-register, cost-management, procurement-management]
license: MIT
---

# Risk Management

## Overview
A risk is an *uncertain* future event or condition that, if it occurs, would push at least
one project objective off course — downward (a threat) or upward (an opportunity). Something
that has already happened is an issue, not a risk. Risk management decides in advance what
could happen and what the project will do about it: it owns the plan, the judgment (how to
find risks, weigh them, choose and fund responses, and size the reserve) and the governance
rhythm, while the living list of risks and its scoring script live in `risk-register`. The
examples use the sample Helios project (a fictional customer self-service portal used
throughout this catalog): five threats and one opportunity, R001-R006, against a $500,000
budget at completion (BAC) that holds a $40,000 contingency reserve.

## When to use this skill
- The user wants to set up risk management or write a risk management plan: scales, risk
  appetite, thresholds, roles, review cadence and escalation.
- The user wants to run a risk identification workshop, a pre-mortem or an assumptions analysis.
- The user must choose a response strategy for a threat or an opportunity, or decide whether
  a response is worth what it costs.
- The user asks how much contingency to hold, at what confidence, or wants a decision tree to
  compare options under uncertainty.
- Do NOT use this to create, score or check the register — use `risk-register`, which owns
  the template and `risk_score.py`; this skill links to them and never duplicates them.
- Do NOT use this for a problem that is already happening — that is an issue: log it and
  execute the planned response in the `project-delivery` issue log.
- Do NOT use this to place reserves in the cost baseline or track their drawdown in earned
  value — use `cost-management`.

## Methodology fit
- **Waterfall:** a formal risk management plan approved with the baseline; identification at
  the start of each stage; quantitative analysis before the baseline is set; contingency held
  inside BAC; the register re-scored at every steering meeting and stage gate.
- **Agile:** risk work rides the cadence — risks raised at stand-up, refinement and retros,
  re-scored at sprint planning; HIGH threats become spikes ordered early in the backlog;
  the reserve is a capacity buffer or a scope cut line from the `agile-delivery` forecast
  rather than money; a risk burndown (open threat exposure per sprint) shows progress.
- **Hybrid (Helios):** one plan, two loops — team delivery risks at two-week sprint planning,
  programme risks (vendor, budget, compliance) at the bi-weekly steering committee; a money
  contingency protects the fixed parts (the identity-provider integration and its contract)
  while user-interface and knowledge-base scope flexes.

## Inputs you need
- The charter's objectives, constraints and top risks, and the sponsor's tolerance for cost,
  schedule and compliance exposure.
- At least a draft scope or WBS, estimates, schedule and budget: risks are judged against
  objectives, so you need something to judge them against. If you came from `project-planning`
  step 7 you have them; if not, draft them first (that skill's earlier steps), then return.
- The assumptions and constraints log — every assumption is a candidate risk.
- Lessons learned and risk checklists from similar projects; vendor and contract terms from
  `procurement-management`; any existing register.

## Workflow
1. **Plan risk management.** Copy `assets/risk-management-plan-template.md` and agree with the
   sponsor: 1-5 probability and impact scales with money and schedule anchors (for ranking),
   the currency used to quantify, the HIGH/MEDIUM thresholds (default 5% / 1% of BAC), risk
   appetite per objective, the confidence level the contingency must reach (P80 by default),
   the management reserve policy, roles, the review cadence and the escalation ladder (risk
   owner → project manager → sponsor → steering committee) with its triggers. Helios:
   `assets/risk-management-plan-sample.md`. *Done: the sponsor has approved the plan, and
   every `risk-register` run will use its scales and thresholds.*
2. **Identify risks and nominate an owner for each.** Combine a divergent technique
   (brainstorm by category, pre-mortem) with a convergent one (checklist, assumptions and
   constraints analysis, SWOT) — see `references/identification.md` and run the session with
   `assets/risk-workshop-template.md`. Write each risk as cause → event → effect, capture
   opportunities as well as threats, move anything already happening to the issue log, and
   name the owner best placed to manage each risk (not the PM by default). Log every risk in
   your copy of `.claude/skills/risk-register/assets/risk-register-template.csv` with its
   `type` and `owner`. Helios: assumption A1 ("the existing identity provider supports customer
   logins") became R001, owner Sam Lee; R006 is an opportunity owned by Priya Nair. *Done: the
   list spans at least four categories, holds at least one opportunity, and every row has an
   owner from the day it was logged.*
3. **Analyse qualitatively — rank.** Rate each risk on the plan's 1-5 scales, place it on the
   probability-impact matrix (score 1-25; HIGH >= 15, MEDIUM >= 8) and note proximity — how
   soon it could strike. A register of 1-5 ratings ranks with `risk_score.py --prob-scale 1-5
   --impact-scale 1-5`; that score orders risks, is never money and is never summed into a
   reserve. Helios (matrix in the plan sample): R001 3 x 5 = 15 HIGH; R002 12, R004 9, R003 8,
   R006 8 MEDIUM; R005 4 LOW. *Done: every risk has a band; HIGH and MEDIUM form the shortlist.*
4. **Quantify the material risks.** For the shortlist, estimate probability as a fraction and
   impact in currency as a positive magnitude (the `type` column carries the direction), so
   exposure is a true expected monetary value (EMV), then score:
   ```bash
   python .claude/skills/risk-register/scripts/risk_score.py .claude/skills/risk-register/assets/risk-register-template.csv --bac 500000
   ```
   Report threat and opportunity EMV separately; use a decision tree where a choice between
   options is at stake and sensitivity analysis to find the risk that drives the total
   (`references/quantitative.md`). Helios: R001 is 40% x $120,000 = $48,000 (HIGH); threat EMV
   $94,300; opportunity EMV $18,000, never netted off. *Done: every material risk has a
   monetary EMV, and the threat and opportunity totals are stated separately.*
5. **Plan responses.** Pick a strategy per material risk — threats: avoid, transfer, mitigate,
   accept, escalate; opportunities: exploit, share, enhance, accept, escalate
   (`references/response-strategies.md`). For each, name the action owner, the proactive
   actions, a contingent plan with its trigger for anything accepted actively, the cost, and
   any secondary risk, and check that the response costs less than the EMV it removes.
   Record one row per action in `assets/risk-response-plan-template.csv` (Helios:
   `assets/risk-response-plan-sample.csv`), and the response, trigger and
   `residual_probability`/`residual_impact` in the register; re-score with `--basis residual`
   and run `--check`. Helios: planned responses cut threat EMV from $94,300 to $52,300. *Done:
   every HIGH and MEDIUM risk has a strategy, an owner, a trigger and a residual estimate, and
   `--check` passes.*
6. **Size the contingency reserve from the residual threat exposure.** Summed residual EMV is
   the mean loss, not a reserve. Simulate the residual threats:
   ```bash
   python .claude/skills/risk-register/scripts/risk_score.py .claude/skills/risk-register/assets/risk-register-template.csv --basis residual --simulate 10000 --seed 42 --reserve 40000
   ```
   Read the reserve at the plan's confidence level, flag any single threat whose residual
   impact exceeds it, and never reduce it by opportunity EMV. Proactive response costs belong
   in the work-package estimates; contingent-plan costs come out of contingency. Set the
   management reserve by policy. If the sponsor funds less than the analysis supports, record
   the gap and a pre-agreed decision path in the plan. Helios: summed residual EMV $52,300
   (simulated mean $52,030), P50 $40,000, P80 $99,000; funding P80 would have lifted BAC above
   the $500,000 the business case appraised, so Dana Okoro approved $40,000 (about 52%
   coverage) with an escalation path for R001, plus a $25,000 management reserve. *Done: the contingency, its confidence level
   and any accepted gap are signed by the sponsor in the risk management plan.*
7. **Implement responses: build them into the plan, schedule and budget.** Turn every
   proactive action into a scheduled activity with an owner, effort and cost (re-run the
   `project-planning` estimate and schedule steps for what it touches); write transfer
   responses into contracts through `procurement-management`; pass the contingency (inside
   BAC) and management reserve (above it) to `cost-management`; arm each contingent plan
   with its trigger and funding source. Track each action's status in your copy of
   `assets/risk-response-plan-template.csv` and verify its effect by re-scoring. Helios: the
   integration spike sits in work package 1.3.1, the delay credits in the IdentityCo contract,
   and the $40,000 inside the $500,000 BAC. *Done: every response action appears in the
   schedule and budget (or a contract) with an owner, and the contingency is inside the cost
   baseline.*
8. **Govern and monitor.** Run the cadence from the plan: `--check` before each review,
   `--top 5 --format md` for the weekly status report, fresh identification at each
   milestone and a pre-mortem before go-live. Watch triggers; when one fires, execute the
   contingent plan, open an issue in the `project-delivery` issue log and set the risk to
   `Occurred`. Compare contingency drawdown with the remaining residual exposure, retire
   risks whose window has passed, and escalate on the plan's triggers to the sponsor, then
   the steering committee, with the decision needed and options (ladder in
   `.claude/skills/project-communication/references/escalation-paths.md`). Feed what you
   learn to `lessons-learned`. Helios: R001 occurred on 2026-06-12 (issue I001); the stub and
   the delay credit were executed, but the slip reached the steering committee late (DEC002,
   raised 2026-06-26 against a 2026-06-16 due date). *Done: reviews
   happen on cadence, every fired trigger has an issue and an executed response, and reserve
   drawdown is reported against remaining exposure.*

## Quality checklist
- [ ] A sponsor-approved plan states scales, thresholds, appetite, the contingency confidence
      level, roles, cadence and the escalation ladder with triggers.
- [ ] Identification used at least one divergent and one convergent technique and covers at
      least four categories and at least one opportunity.
- [ ] Every risk is a cause → event → effect statement with a named owner since it was logged;
      nothing already happening is logged as a risk.
- [ ] 1-5 P x I scores are used only to rank; no reserve or total is built from them.
- [ ] Every material risk has a monetary EMV with a positive impact and a `type`; threat and
      opportunity totals are reported separately.
- [ ] Every HIGH and MEDIUM risk has a strategy, an owner, a trigger and a residual estimate,
      and `risk_score.py --check` passes.
- [ ] Each response costs less than the EMV it removes, or the exception is justified.
- [ ] The contingency is sized from residual threat exposure at the plan's confidence level,
      after responses were planned, without netting opportunities; any funded gap is signed.
- [ ] Every response action is scheduled and funded (or contracted) with an owner, and the
      contingency is inside the cost baseline.
- [ ] Reviews run on cadence; every fired trigger is an issue; escalations reach the sponsor or
      steering committee with a decision request.

## Anti-patterns
- Identifying risks once at kickoff and never revisiting them.
- Logging only threats and ignoring opportunities worth pursuing.
- Logging things that have already happened as risks — they are issues.
- Leaving risks unowned until response planning, so nobody watches them in between.
- Defaulting every risk to "accept and monitor" — passive acceptance is a conscious choice
  for low-exposure risks, not a default for the HIGH ones.
- Summing 1-5 P x I scores and calling the result a contingency figure.
- Entering threats as negative impacts, or netting opportunity EMV off the reserve.
- Sizing contingency before responses are planned, or holding the summed EMV as "80% confidence".
- Responses that live only in the register — never scheduled, funded or verified.
- Spending more on a response than the exposure it removes.
- Escalating to "management" in general instead of to the named sponsor or steering
  committee, with the decision needed.
- Confusing the process (this skill) with the artifact — duplicating the register or its script.

## Resources
- `references/identification.md` — brainstorming by category, checklists, assumptions and
  constraints analysis, pre-mortem, SWOT, good risk statements and owner nomination.
- `references/response-strategies.md` — threat and opportunity strategies with Helios
  examples, contingent plans, cost-effectiveness, residual and secondary risk, escalation.
- `references/quantitative.md` — score vs EMV, the positive-magnitude `type` convention,
  decision trees, sensitivity, simulation, contingency sizing after responses, reserve analysis.
- `assets/risk-management-plan-template.md` — fill-in risk management plan.
- `assets/risk-management-plan-sample.md` — sample Helios plan with the sponsor's contingency decision.
- `assets/risk-workshop-template.md` — agenda, prompts and capture sheet for an
  identification workshop or pre-mortem.
- `assets/risk-response-plan-template.csv` — fill-in response action log (one row per action).
- `assets/risk-response-plan-sample.csv` — sample Helios response actions as at month 3.
- Scoring, residual exposure, simulation and checks come from `risk-register`:
  `python .claude/skills/risk-register/scripts/risk_score.py --help`.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `senior-pm` — routes users here when uncertainty dominates the project-state canvas (a HIGH
  risk without a response, or exposure beyond the reserve); takes back responses and reserves.
- `project-planning` — calls this skill at its step 7 with the draft scope, estimates and
  schedule; takes back the register, the response actions to schedule and the reserves.
- `risk-register` — the register template and `risk_score.py` this process fills, scores
  (EMV, residual exposure, simulation) and checks.
- `cost-management` — receives the contingency (inside BAC) and the management reserve (above
  it), and reports drawdown back for reserve analysis.
- `procurement-management` — writes transfer responses into contract terms and uses the
  make-or-buy decision tree; hands back vendor risks and each transfer's secondary risks.
