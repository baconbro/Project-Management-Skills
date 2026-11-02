---
name: project-charter
description: >-
  Writes the project charter that authorizes a project: sponsor, PM authority, SMART
  objectives, scope boundaries, milestones, budget range, top risks and cancellation
  criteria, with the sponsor's sign-off. Use when writing, reviewing or getting approval
  for a charter or project brief.
metadata:
  version: 1.1.0
  category: artifact
  phase: initiation
  related: [project-initiation, project-planning, stakeholder-management, business-case, scope-and-requirements]
license: MIT
---

# Project Charter

## Overview
A project charter is the short, authoritative document that brings a project into existence:
the sponsor commits funding and appoints the project manager, and both agree on why the
project exists, what success means, where its boundaries lie, what the PM may decide alone, who
approves what, and under which conditions it stops. Every later decision traces back to it.
This skill produces that document and verifies its approval; the initiation phase that
sequences the business case, charter, stakeholder analysis and kickoff is `project-initiation`.
A charter is authorized only when the sponsor signs a specific version: until then it is a
draft. The examples use the sample Helios project (a fictional customer self-service portal used
throughout this catalog): sponsor Dana Okoro, PM Sam Lee, objective OBJ-1 (cut password-reset and
order-status tickets by 50% within 6 months of launch), a $450k–$550k budget range, milestones
M1/M4/M6, and v1.0 approved on 2026-04-02 (`assets/charter-sample.md`).

## When to use this skill
- The user needs to write a charter, project brief or one-page mandate for a project or phase.
- The user has a draft charter and wants it reviewed, tightened or made ready for sign-off.
- The user must confirm whether a project is actually authorized (is the charter signed?).
- The user needs approval requirements, the PM's authority or stop/cancellation criteria
  written down for a sponsor.
- A project is already under way with no agreed statement of purpose and boundaries.
- Do NOT use this to run the whole initiation phase (business case, charter, stakeholders,
  kickoff in order) — use `project-initiation` instead.
- Do NOT use this to justify the investment financially — use `business-case`.
- Do NOT use this to write the detailed scope statement or requirements — use
  `scope-and-requirements`.
- Do NOT use this to build the plan or baselines — use `project-planning`; for a *team*
  charter (working agreement), use `resource-management`.

## Methodology fit
- **Waterfall:** a full charter, signed before planning starts; the signature is the gate into
  planning, the in/out-of-scope lists are the starting point for the scope baseline, and any
  change to a boundary after approval is re-signed as a new version.
- **Agile:** a one-page brief: sponsor and product owner (with the product owner's decision
  rights), outcome objectives, guardrails instead of fixed scope (team cost per sprint, latest
  date, compliance limits, exclusions), the first release goal and outcome-based stop rules; still
  signed by the sponsor.
- **Hybrid (Helios):** the charter fixes OBJ-1, the budget range, M1/M4/M6 and the fixed
  elements (SSO through the existing identity provider, data residency, accessibility); portal and
  knowledge-base features flex in sprints that the product owner, Ava Chen, orders inside those
  boundaries.

## Inputs you need
The sponsor (one executive with funding authority) and the PM; the approved business case or
its key figures (problem, recommended option, funding range, benefits and benefit owner,
switching values), or a recorded waiver; the target outcome with a baseline measure; a rough
timeline and fixed dates; known constraints (budget ceiling, regulation, technology) and
assumptions; the key stakeholders and who approves what; and the organization's governance
(who may authorize projects, steering committee, the PM's usual limits). With no sponsor, stop:
an unsponsored charter authorizes nothing — return to `project-initiation`. With no business
case and no waiver, run `business-case` first.

## Workflow
1. **Confirm the authority.** Name the sponsor and the PM in the header of a copy of
   `assets/charter-template.md`, reference the business case (or its waiver) and state the
   delivery approach. A committee is not a sponsor. *Done: one sponsor with funding authority
   and one PM are named, and the business case is referenced or its waiver recorded.*
2. **State the business need.** One or two plain sentences with the size of the pain, taken
   from the business case (section 1). *Done: a non-specialist can say why the project exists
   and what the problem costs.*
3. **Write objectives and success criteria.** SMART outcomes with an id, metric, baseline,
   target, date and benefit owner (section 2); see `references/charter-elements.md`. Helios:
   OBJ-1, measured on monthly ticket volume against the 3-month pre-launch average, owned by
   Priya Nair. *Done: every objective has all five parts and an id requirements can trace to.*
4. **Fence the scope at outcome level.** List in-scope outcomes and explicit exclusions with a
   reason and a destination (section 3). Keep requirements and features out: the detailed scope
   statement is written in planning with `scope-and-requirements`. *Done: both lists exist and
   every exclusion has a destination.*
5. **Set milestones, budget range, assumptions and constraints.** Three to six milestones with
   what must be true at each; a budget range with its basis, funding source and allowed
   pre-baseline spend; assumptions with owner and validate-by; constraints with owner (sections
   4–6). Helios: $450k–$550k including all reserves; A1–A5; CON-1–CON-4. *Done: no milestone
   without evidence, no budget without a source, no assumption without an owner.*
6. **Name the top risks and key stakeholders.** Three to five risks as cause → event → effect,
   rated H/M/L with an owner; stakeholders with what each approves, accepts or provides
   (sections 7–8). Full analysis belongs in `risk-register` and `stakeholder-management`.
   *Done: each risk and stakeholder row is complete.*
7. **Write the PM's authority, approval requirements and exit criteria.** PM limits in money and
   days and who decides above them (section 9); who approves the charter, baseline, each
   deliverable, release decisions, completion and business success; the normal exit; and the
   cancellation triggers with threshold, check point and checker (section 10). Helios: Sam Lee up
   to $5,000 and 2 working days; a stop decision by Dana Okoro if the cost forecast passes
   $550,000 with no recovery plan, or fewer than 40 of the 200 pilot customers (20%) complete a
   self-service journey within 4 weeks of M4. *Done: every approval names a person and every
   stop trigger has a threshold, a check point and a checker.*
8. **Review the draft.** Walk the rubric in `references/charter-review.md` (section 1), check
   consistency with the business case, and cut to one or two pages. *Done: every rubric line is
   PASS or named as an open point, and no `<placeholder>` is left.*
9. **Get and verify sign-off.** Walk the sponsor through objectives, boundaries, budget and
   section 10, then obtain a decision on the exact version. Verify it with the sign-off checklist
   in `references/charter-review.md` (section 2). Until it passes, the charter is a draft and
   authorizes no hiring, contracts or spend. *Done: the sponsor's name, decision, version and
   date are recorded in section 11, the evidence is filed, and Status reads Approved.*
10. **Hand off and protect it.** Distribute the approved charter; pass the objectives and
    boundaries to `scope-and-requirements`, the assumptions and constraints to
    `project-planning`, and the stakeholder list to `stakeholder-management`. Re-issue a new
    signed version whenever a boundary in `references/charter-review.md` (section 3) changes.
    *Done: the planning owners have the approved version, and the version history shows every
    change with its approver.*

## Quality checklist
- [ ] Exactly one named sponsor with funding authority and one named PM.
- [ ] The business case is referenced with its version, or a waiver names who waived it and why.
- [ ] The business need states the problem and its size in plain language.
- [ ] Every objective has an id, metric, baseline, target, date and benefit owner.
- [ ] In-scope items are outcomes, not requirements; every exclusion has a reason and a destination.
- [ ] Each milestone states what must be true; the budget is a range with basis and funding source.
- [ ] Every assumption has an owner and a validate-by date; every constraint has an owner.
- [ ] Three to five top risks, each cause → event → effect with an owner.
- [ ] The PM's authority is written in money and days, with who decides above it.
- [ ] Approval requirements name a person for the charter, baseline, deliverables, releases,
      completion and business success.
- [ ] Exit criteria and at least one measurable cancellation trigger with a checker are present.
- [ ] Sponsor sign-off recorded (name, decision, version, date), evidence filed, Status = Approved.
- [ ] One to two pages, no `<placeholder>` left, and consistent with the business case.

## Anti-patterns
- Treating an unsigned or out-of-date charter as authorization to spend, hire or contract.
- A committee or a sponsor with no budget authority: nobody can decide when it matters.
- Turning the charter into a detailed plan, schedule or requirements list — that is
  `project-planning` and `scope-and-requirements`.
- Omitting the out-of-scope list, the most common source of later scope fights.
- Vague objectives ("improve efficiency") with no baseline, target or owner.
- No stop rule, so the project can end only by finishing, however poor the forecast.
- A single precise budget figure before planning, or a range with no funding source.
- Editing an approved charter without re-approval.

## Resources
- `references/charter-elements.md` — definition, quality test and Helios example for each
  charter element, the charter versus neighbouring documents, and the lightweight agile variant.
- `references/charter-review.md` — 15-line review rubric, the sign-off verification checklist,
  when a change needs re-approval, and common review defects.
- `assets/charter-template.md` — fill-in charter (`<placeholders>`), sections 1–11 including PM
  authority, approval requirements, exit and cancellation criteria, sign-off and version history.
- `assets/charter-sample.md` — sample Helios charter v1.0 as approved by Dana Okoro.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-initiation` — the phase that sequences this charter after the business case and before the stakeholder analysis and kickoff; it receives the signed charter as its authorization gate.
- `project-planning` — receives the approved charter and carries its milestones, budget range, assumptions and constraints into the plan and baselines.
- `stakeholder-management` — turns the charter's key stakeholders and approvers into the full register and engagement strategy.
- `business-case` — supplies the need, recommended option, funding range and switching values the charter cites and its stop triggers reuse.
- `scope-and-requirements` — expands the charter's objectives and in/out-of-scope lists into the detailed scope statement and traceability matrix.
