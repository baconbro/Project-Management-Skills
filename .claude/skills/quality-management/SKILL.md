---
name: quality-management
description: >-
  Defines and assures project quality — acceptance criteria, a definition of
  done, quality gates with entry/exit criteria, review and test cadence, and
  quality metrics — so that "done" is unambiguous and verifiable. Use when the
  user wants to set acceptance criteria, write a definition of done, design
  quality gates or gate reviews, plan reviews/testing, pick quality metrics, or
  decide what "good enough" means. Triggers: "quality management", "quality
  plan", "acceptance criteria", "definition of done", "DoD", "quality gate",
  "exit criteria", "quality metrics", "Given/When/Then", "quality vs grade".
  Works for waterfall, agile, and hybrid projects. Distinct from cost or
  schedule control.
metadata:
  version: 1.0.0
  category: discipline
  phase: cross-cutting
  related: [project-planning, work-breakdown-structure]
license: MIT
---

# Quality Management

## Overview
Quality management is the discipline of defining what "good" means *before* work starts and
then assuring it as work proceeds. It splits into **quality planning** (acceptance criteria,
definition of done, gates, metrics) and **quality assurance/control** (reviews, testing,
gate decisions). Done well, it removes the endless "is this finished?" argument by making the
answer checkable.

## When to use this skill
- The user needs acceptance criteria, a definition of done, or quality gates.
- The user wants to plan review/test cadence or choose quality metrics.
- The user is arguing about whether something is "done" or "good enough".
- Do NOT use this to decompose the work into deliverables — use `work-breakdown-structure`,
  whose work packages this skill attaches criteria to.
- Do NOT use this to schedule or resource the work — use `project-planning`.

## Methodology fit
- **Waterfall:** a quality management plan with documented acceptance criteria and formal gate
  reviews between phases.
- **Agile:** a shared **Definition of Done** plus per-story acceptance criteria, checked every
  iteration; the gate is the demo / review.
- **Hybrid:** a lightweight quality plan for the whole, with a DoD applied inside delivery.

## Inputs you need
The scope and deliverables (from `work-breakdown-structure`), stakeholder expectations and any
regulatory or contractual standards, and the project's risk appetite (how much rework is
tolerable). Quality criteria should trace to a real stakeholder need, not to perfectionism.

## Workflow
1. **Set quality objectives and metrics.** Decide what quality means here and how it is
   measured — defect density, escaped defects, test coverage, accessibility score, performance
   budget. *Done: a short list of measurable quality metrics with targets.*
2. **Write acceptance criteria** for each deliverable — measurable, testable conditions, in
   Given/When/Then or checklist form. See `references/acceptance-criteria.md`. *Done: every
   significant deliverable has criteria a reviewer could pass/fail objectively.*
3. **Agree a Definition of Done.** Capture the cross-cutting bar every work item must clear
   (tested, reviewed, documented, accessible) in `assets/definition-of-done.md`. *Done: a DoD
   the whole team has agreed and can recite.*
4. **Design quality gates.** Define entry and exit criteria for each gate and who decides at
   the review. Distinguish **quality** (conformance) from **grade** (feature level). See
   `references/quality-gates.md`. *Done: gates with explicit entry/exit criteria and named
   approvers.*
5. **Set review and test cadence.** Decide when reviews, tests, and gate checks happen and who
   runs them — peer review, test stages, demos, audits. *Done: a quality cadence on the calendar.*
6. **Assure and control.** Run the reviews/tests, measure the metrics, and gate releases on the
   criteria — escalate failures rather than waiving them silently. *Done: gates are enforced and
   metrics tracked, not aspirational.*

## Quality checklist
- [ ] Quality metrics with explicit targets are defined.
- [ ] Every significant deliverable has measurable, testable acceptance criteria.
- [ ] A Definition of Done is agreed and applied uniformly.
- [ ] Quality gates have entry/exit criteria and named approvers.
- [ ] A review/test cadence is scheduled, not ad hoc.
- [ ] Quality and grade are not conflated.

## Anti-patterns
- "Looks good to me" sign-offs with no written, testable criteria.
- A Definition of Done that exists on a wiki but is ignored at crunch time.
- Confusing low grade (few features) with low quality (defects) — they are different decisions.
- Gates that always pass because failing one is "too disruptive" — that is not a gate.
- Gold-plating: adding quality nobody asked for at the expense of scope or schedule.

## Resources
- `references/acceptance-criteria.md` — Given/When/Then and checklist styles; making criteria measurable.
- `references/quality-gates.md` — entry/exit criteria, gate reviews, and quality vs grade.
- `assets/definition-of-done.md` — a reusable Definition of Done template.

## Related skills
- `work-breakdown-structure` — defines the deliverables this skill attaches acceptance criteria to.
- `project-planning` — schedules the reviews, tests, and gates this skill specifies.
