# Methodology selection — waterfall vs. agile vs. hybrid

Load this to recommend a delivery approach (SKILL.md step 4) and to show the user the skill
sequence that approach implies. The goal is not dogma: match the approach to how much of the
requirements and the path are understood, and how expensive change is. The worked example is
the sample Helios project (a fictional customer self-service portal used throughout this
catalog); it is an illustration, not a default.

## The core question
How much is known up front, and how expensive is change?
- Known scope + costly change → lean **waterfall**.
- Uncertain scope + cheap, valuable feedback → lean **agile**.
- Fixed outcome, budget or date + uncertain detail → lean **hybrid**.

## Waterfall — sequential, plan-driven
Phases run in order (initiate → plan → execute → close) with sign-offs between them.

Fits when:
- Requirements are stable and well understood before work starts.
- Change is expensive or risky (regulated, fixed-price, physical build, safety-critical).
- Stakeholders need predictable scope, cost and dates and formal stage gates.

Signals you are in waterfall territory:
- A fixed-price contract or a hard regulatory deadline with a defined deliverable.
- "We know exactly what we need; just build it."
- Heavy compliance, audit or documentation requirements; a physical or one-shot release.

How health is read: milestone dates and earned value (CPI/SPI) against the approved baseline.

## Agile — iterative, change-driven
Work is delivered in short increments; priorities are re-set each iteration from feedback.

Fits when:
- Requirements are uncertain or expected to evolve.
- Early, frequent delivery is valuable and feedback can change direction.
- A cross-functional team can work closely with an engaged product owner.

Signals you are in agile territory:
- "We are not sure what users want yet; we will learn as we go."
- Value comes from getting something usable in front of users quickly.
- The team can release in small increments without heavy release overhead.

How health is read: sprint goals met, velocity and its spread, the release forecast as a
range against the date, and the burnup (scope growth is visible).

## Hybrid — fixed frame, iterative delivery
Outcomes, budget and key dates are fixed at the top; delivery inside that frame is
iterative. The most common real-world choice for a product with a committed launch date.

Fits when:
- Sponsors need committed outcomes or budget but scope detail is still emerging.
- Some parts are well understood (identity, hosting, contracts) and some are not (UX, content).
- Governance demands milestones and reporting, but the team wants iteration.

Signals you are in hybrid territory:
- "Launch must hit the date within this budget, but we will iterate on the features."
- A planned baseline at the top, sprints underneath; a vendor deliverable on a fixed price
  beside an in-house team working in sprints.

How health is read: milestones and earned value at the top, velocity inside the sprints;
both feed one RAG in `status-report`.

**Example.** Helios is hybrid: the six-month date and the $500,000 BAC are fixed, the
identity integration is a bounded vendor deliverable, while the self-service UX and the
knowledge-base content are learned with pilot customers in two-week sprints.

## Quick decision checklist
Answer each question; count the Yes answers.
- [ ] Are requirements likely to change as we learn?
- [ ] Is early or partial delivery genuinely valuable to users?
- [ ] Can we release in small increments cheaply?
- [ ] Is the team cross-functional with an available product owner?
- [ ] Is change cheap rather than costly or risky?

4-5 Yes → **agile**. 0-1 Yes → **waterfall**. 2-3 Yes → **hybrid**. Two overrides:
a fixed-price contract or regulatory sign-off covering the *whole* deliverable pulls that
part to waterfall whatever the count; a fixed date or budget with 4-5 Yes makes it
**hybrid** (iterate inside the frame, report against milestones). State the count and the
override, if any, as the signal behind the recommendation. Re-check at each phase gate and
tighten toward one end as certainty grows.

## Skill sequence by approach

The same skills apply to all three; what changes is the order, the depth and what each gate
needs to see. Hand the user one or two skills at a time, not the whole sequence.

| Step | Waterfall | Agile | Hybrid | Gate artifact |
|---|---|---|---|---|
| 1 Justify | `business-case` in full | Lean case or product vision; `business-case` sized to the spend | `business-case` for the fixed frame | Funding decision |
| 2 Authorize | `project-charter`, formally signed | Lightweight charter: outcome and guardrails | `project-charter` fixes outcome, budget, date | Signed charter |
| 3 Stakeholders | `stakeholder-management` | Same, with the product owner named | Same | Stakeholder register |
| 4 Scope | `scope-and-requirements` → full scope statement and RTM | Product backlog and definition of ready in `agile-delivery` | Baseline the fixed deliverables and compliance requirements; backlog for the rest | Signed scope statement or ordered backlog |
| 5 Decompose and estimate | `work-breakdown-structure` → `estimation` (three-point) | Story points and planning poker (`estimation`) | WBS to level 2-3 for the frame; story points inside | WBS or sized backlog |
| 6 Time | `project-schedule` critical path | Sprint cadence; `agile-delivery` forecast | Milestones from `project-schedule`; sprints underneath | Schedule baseline or release forecast |
| 7 People and money | `resource-management`, `raci-matrix`, `cost-management` | Stable team capacity (`resource-management`); cost per sprint | All three; cost baseline at the top | Approved baseline (`project-planning`) |
| 8 Risk, quality, comms | `risk-register`, `quality-management`, `project-communication` | Risks on the board; definition of done; sprint review as the main channel | All, lighter inside the sprints | Plans approved |
| 9 Control | `project-delivery` with earned value, `status-report`, `change-management` | Sprint review, retrospective, velocity; backlog re-ordering replaces most change requests | Earned value plus velocity; change control on the baseline, backlog flex inside | Weekly status; change log |
| 10 Release | `release-and-cutover` big-bang or phased | Frequent small releases; `release-and-cutover` for the big ones | Pilot, then a phased or flag ramp | Go/no-go verdict |
| 11 Close | `project-closure` + `lessons-learned` | Final retrospective; `project-closure` light | Both | Closure report |

`helios-walkthrough.md` follows the hybrid column end to end on the sample Helios project.
