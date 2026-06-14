---
name: project-initiation
description: >-
  Stands up a new project end-to-end through the initiation phase: validates the
  need, authorizes the work, identifies stakeholders, runs a kickoff, and hands
  off a ready project to planning. Use when the user is starting a project from an
  idea, needs to get a project off the ground, wants to run initiation or a
  kickoff, or is unsure what initiation steps remain before planning can begin.
  Triggers: "start a project", "initiate a project", "stand up a project", "get
  a project off the ground", "project kickoff", "initiation phase", "what do I
  do before planning". Orchestrates the artifact skills (business-case, charter,
  stakeholder analysis) in sequence rather than duplicating them. Works for
  waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: phase
  phase: initiation
  related: [senior-pm, project-charter, business-case, stakeholder-management, project-planning]
license: MIT
---

# Project Initiation

## Overview
Initiation is the phase that turns an idea into an authorized project with a named
sponsor, a justified investment, a clear mandate, identified stakeholders, and a team
aligned at kickoff. This skill sequences that work and hands off a planning-ready
project; the deep artifact work lives in the specialist skills it calls.

## When to use this skill
- The user is starting a brand-new project or phase from an idea or mandate.
- The user asks to "initiate", "stand up", or "kick off" a project end-to-end.
- The user has fragments (an idea, a sponsor) but no ordered path to a real project.
- Do NOT use this to build the detailed plan and baseline — use `project-planning`.
- Do NOT use this to write only the charter, only the business case, or only the
  stakeholder analysis — go straight to `project-charter`, `business-case`, or
  `stakeholder-management` for a single artifact.

## Methodology fit
- **Waterfall:** full initiation with a formally signed charter and a stage gate before
  planning.
- **Agile:** lightweight initiation — a project brief, a product vision, and an engaged
  product owner instead of fixed scope.
- **Hybrid:** fix the outcome, budget, and key dates in the charter; leave the delivery
  approach iterative (the right call for the Helios customer self-service portal).

## Inputs you need
The project idea or mandate, a candidate sponsor, the business problem or opportunity, a
rough target outcome, and any hard constraints (deadline, budget, compliance). If no
sponsor can be named or no outcome can be described, that is the first gap to close.

## Workflow
1. **Validate the need.** Confirm the problem is real and worth solving and run
   `business-case` to justify the investment (options, benefits, NPV/ROI/payback). If the
   case is weak, stop here — an unjustified project should not be authorized.
   *Done: a recommended option with a benefit and a cost is agreed.* Uses `business-case`.
2. **Authorize the project.** Run `project-charter` to name the sponsor and PM and capture
   objectives, scope boundaries, milestones, budget range, and success criteria, then get
   the sponsor's sign-off. *Done: a signed/agreed charter exists.* Uses `project-charter`.
3. **Identify stakeholders.** Run `stakeholder-management` to list stakeholders and map
   power/interest and engagement, so the kickoff invites the right people.
   *Done: a stakeholder list with an engagement approach.* Uses `stakeholder-management`.
4. **Confirm initiation is complete.** Walk `references/initiation-checklist.md` and close
   any open item before the kickoff. *Done: every checklist item is checked or waived with
   a reason.* Uses `references/initiation-checklist.md`.
5. **Run the kickoff.** Use `references/kickoff-agenda.md` and present from
   `assets/kickoff-deck-outline.md` to align the team on purpose, scope, roles, and the
   plan-building approach. *Done: kickoff held; actions and owners recorded.* Uses
   `references/kickoff-agenda.md` and `assets/kickoff-deck-outline.md`.
6. **Hand off to planning.** Pass the charter, stakeholder list, and kickoff actions to
   `project-planning` to build the integrated plan and baseline. *Done: planning owns the
   next step.* Hands off to `project-planning`.

## Quality checklist
- [ ] The need is validated with a business case (or an explicit waiver).
- [ ] A charter is agreed with a named sponsor AND named project manager.
- [ ] Stakeholders are identified with an engagement approach.
- [ ] Every item on `references/initiation-checklist.md` is closed or waived.
- [ ] A kickoff is held and actions/owners are recorded.
- [ ] The project is handed off to `project-planning` with a clear first step.

## Anti-patterns
- Kicking off before the project is justified or authorized — kickoff is not step one.
- Authorizing a project with no sponsor able to fund and decide.
- Skipping stakeholder identification, then discovering missing decision-makers later.
- Sliding into detailed planning here instead of handing off to `project-planning`.

## Resources
- `references/initiation-checklist.md` — gate checklist for completing initiation.
- `references/kickoff-agenda.md` — a timed kickoff-meeting agenda.
- `assets/kickoff-deck-outline.md` — slide-by-slide kickoff deck outline to fill in.

## Related skills
- `senior-pm` — routes here when a project needs to be stood up from scratch.
- `business-case` — validates the need this phase authorizes (step 1).
- `project-charter` — authorizes the project within this phase (step 2).
- `stakeholder-management` — identifies the stakeholders this phase aligns (step 3).
- `project-planning` — the next phase this initiation hands off to.
