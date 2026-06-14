---
name: project-closure
description: >-
  Formally closes a project or phase: confirms acceptance and sign-off, hands the
  product over to operations or the benefits owner, captures lessons, completes
  administrative and financial closure, and confirms benefits tracking against the
  business case. Use when the user is finishing a project or phase, needs to close
  out, hand over to operations, do a post-project review, or release the team.
  Triggers: "close the project", "project closeout", "phase closure", "handover to
  operations", "post-project review", "release the team", "wrap up the project",
  "final report". Links out to lessons-learned and business-case rather than
  duplicating them. Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: phase
  phase: closure
  related: [senior-pm, project-delivery, lessons-learned, business-case]
license: MIT
---

# Project Closure

## Overview
Closure is the disciplined end of a project or phase: it confirms the work was accepted,
hands the product to whoever runs and benefits from it, harvests lessons, ties off the
admin and money, and makes sure someone is on the hook for the benefits the business case
promised. Done well, closure prevents loose ends, captures learning, and frees the team
cleanly.

## When to use this skill
- The user is finishing a project or a phase and needs to close it out properly.
- The user needs acceptance/sign-off, a handover, a post-project review, or a final report.
- Do NOT use this while the project is still being executed — that is `project-delivery`.
- Do NOT use this to run only a lessons workshop — go straight to `lessons-learned`.

## Methodology fit
- **Waterfall:** a formal closure with final acceptance, a signed closure report, and a
  stage-gate sign-off.
- **Agile:** closure at the end of a release or the product's life — a final retrospective,
  a handover to product/ops, and benefits tracking; iterations closed continuously inside.
- **Hybrid:** formal acceptance and financial closure at the top; the team retrospective
  feeds `lessons-learned` (the right call for the Helios customer self-service portal).

## Inputs you need
The agreed acceptance criteria and deliverables, the issue/risk logs, the cost baseline and
actuals, the stakeholder and operations contacts, and the business case (for the benefits
to track). If deliverables are not yet accepted, finish that in `project-delivery` first.

## Workflow
1. **Confirm acceptance and sign-off.** Verify deliverables meet the agreed acceptance
   criteria and definition of done, and get the sponsor's/customer's formal acceptance.
   Record any accepted exceptions. *Done: signed acceptance with exceptions noted.* Uses
   `references/closure-checklist.md`.
2. **Hand over to operations / the benefits owner.** Transfer the product, documentation,
   and support arrangements to the team that will run it, and name the owner accountable
   for the benefits going forward. *Done: a named owner has accepted the handover.* Uses
   `references/benefits-realization.md`.
3. **Capture lessons.** Run a post-project review and record categorized, actionable
   lessons. *Done: lessons captured and routed to where they will be reused.* Uses
   `lessons-learned`.
4. **Complete administrative and financial closure.** Close open issues/actions, release
   the team and resources, reconcile final costs to the baseline, close contracts and
   accounts, and archive project records. *Done: nothing is left open or unpaid.* Uses
   `references/closure-checklist.md`.
5. **Confirm benefits tracking.** Compare delivered against the benefits promised in the
   business case, and confirm who tracks the remaining benefits and when they are reviewed
   (most benefits land after the project ends). *Done: a benefits-tracking owner and dates
   are agreed.* Uses `business-case` and `references/benefits-realization.md`.
6. **Issue the closure report.** Complete `assets/closure-report.md` summarizing outcomes,
   performance vs. baseline, lessons, handover, and benefits, and route it for sign-off.
   *Done: an approved closure report; the project is closed.* Uses `assets/closure-report.md`.

## Quality checklist
- [ ] Deliverables are formally accepted against the agreed criteria, with exceptions noted.
- [ ] The product is handed over to a named operations / benefits owner who accepted it.
- [ ] Lessons are captured and routed for reuse (`lessons-learned`).
- [ ] Issues/actions are closed, the team is released, and finances are reconciled.
- [ ] Benefits tracking has a named owner and review dates against the `business-case`.
- [ ] A closure report is completed and signed off.

## Anti-patterns
- "Closing" by stopping work, with open issues, unpaid invoices, and no sign-off.
- Skipping lessons learned because the project is over and everyone has moved on.
- Handing over to operations with no named owner, so support falls through the cracks.
- Declaring success at go-live and never checking whether the promised benefits arrived.

## Resources
- `references/closure-checklist.md` — acceptance, handover, admin, and financial closure items.
- `references/benefits-realization.md` — handover and tracking of benefits after delivery.
- `assets/closure-report.md` — fill-in final closure report template.

## Related skills
- `senior-pm` — routes here when a project or phase is ending and must be closed.
- `project-delivery` — the prior phase that hands an accepted project to closure.
- `lessons-learned` — captures and operationalizes the lessons this phase harvests (step 3).
- `business-case` — the source of the benefits this phase confirms are being tracked (step 5).
