---
name: change-request
description: >-
  Captures and assesses a single change request from description through to a
  decision, documenting justification, scope/cost/schedule impact, options, a
  recommendation, and the recorded decision, and scoring impact with the bundled
  change_impact.py helper. Use when the user wants to raise, write, assess, or
  decide a change request, evaluate the impact of a proposed change, prioritize
  change requests, or capture a scope change for approval. Triggers: "change
  request", "CR", "raise a change", "scope change", "change impact", "assess a
  change", "variation request", "change control form". For the governance process,
  board, and change log around it, use change-management. Works for waterfall,
  agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: artifact
  phase: delivery
  related: [change-management]
license: MIT
---

# Change Request

## Overview
A change request is the single, self-contained record of one proposed change: what it is,
why it is needed, what it costs in scope, money, and time, the options considered, a
recommendation, and the decision made. Done well it lets a decision-maker say yes or no on
evidence in minutes — not relitigate the whole project.

## When to use this skill
- The user wants to raise, document, or assess one specific change.
- Someone proposes new scope, and you need its impact and a decision.
- The user wants to score or prioritize several pending change requests.
- Do NOT use this for the change-control *process*, the change board, thresholds, or the
  ongoing change log governance — use `change-management`, which links here for the form.

## Methodology fit
- **Waterfall:** a formal CR raised against a baseline; assessed and approved before work.
- **Agile:** most change is absorbed by reprioritizing the backlog; raise a CR only when a
  change affects the agreed scope, budget, contract, or release commitment.
- **Hybrid:** CRs for anything that breaches the fixed baseline; backlog churn stays inside
  the team.

## Inputs you need
A clear description of the proposed change, who raised it and why, and an honest estimate
of its impact on **scope, cost, and schedule** (each rated 1-5). Options and a
recommendation make the decision faster. A sample change log lives in
`assets/change-log.csv`; field definitions are in `references/change-request-fields.md`.

## Workflow
1. **Describe** the change in plain language and record who raised it and when. *Done: a
   reader who was not in the room understands what is being asked.*
2. **Justify** it: the business or technical reason, and what happens if it is rejected.
   *Done: the "why now" is explicit.*
3. **Assess impact** on scope, cost, and schedule. Rate each 1-5 (see
   `references/change-request-fields.md`) and quantify in real units where you can
   (dollars, days). *Done: all three impacts rated with rationale.*
4. **Score and prioritize** the request (or a batch of them):
   ```bash
   python scripts/change_impact.py assets/change-log.csv
   ```
   The tool computes a weighted impact score and a HIGH/MEDIUM/LOW priority. Adjust the
   dimension weights with `--w-scope` / `--w-cost` / `--w-schedule` and bands with
   `--high` / `--medium`. *Done: each CR has a score and a priority.*
5. **Lay out options** (including "do nothing") with their trade-offs, then give a clear
   **recommendation**. *Done: at least two options and a recommended one.*
6. **Record the decision** — approved, rejected, or deferred — with who decided and when,
   in `assets/change-request-template.md`. Route through `change-management` for the board
   and the master change log. *Done: decision, decider, and date captured.*

## Quality checklist
- [ ] Description and raiser are clear to someone who was not involved.
- [ ] Justification states the reason and the cost of doing nothing.
- [ ] Scope, cost, and schedule impacts are each rated and quantified where possible.
- [ ] `change_impact.py` has scored the request into a priority.
- [ ] At least two options (including do-nothing) and a recommendation.
- [ ] The decision, decision-maker, and date are recorded.

## Anti-patterns
- Approving a change verbally with no record of impact or decision.
- Rating every change HIGH so priority loses meaning.
- Estimating cost and schedule impact with no rationale or units.
- Offering one option and calling it a decision.
- Leaving a CR "open" forever with no decision and no owner.

## Resources
- `references/change-request-fields.md` — field definitions and the 1-5 impact scale.
- `assets/change-request-template.md` — fill-in single change request form.
- `assets/change-log.csv` — sample change requests; also the input for the scorer.
- `scripts/change_impact.py` — scores weighted impact and priority. Run `python scripts/change_impact.py --help`.

## Related skills
- `change-management` — the change-control process, board, thresholds, and master log this form feeds.
