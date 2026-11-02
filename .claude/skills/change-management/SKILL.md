---
name: change-management
description: >-
  Governs change in both senses: change CONTROL, the procedure that raises, logs,
  assesses, decides, communicates and verifies changes to the scope, schedule and
  cost baselines through a change control board (CCB), approval tolerances, an
  emergency route and change freezes; and change ADOPTION, sponsor-led readiness,
  ADKAR, resistance and reinforcement against adoption targets agreed before
  go-live. Use when the user wants to set up change control or a CCB, decide who
  approves which changes, stop scope creep, know who updates which baseline after
  approval, or plan adoption of a new way of working. Triggers: "change
  management", "change control process", "change control board", "CCB", "scope
  creep", "integrated change control", "approval tolerances", "emergency change",
  "change freeze", "ADKAR", "user adoption", "change readiness assessment",
  "resistance to change". For raising, scoring or logging one change request, use
  change-request. Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.1.0
  category: discipline
  phase: cross-cutting
  related: [project-planning, project-delivery, change-request, scope-and-requirements, release-and-cutover]
license: MIT
---

# Change Management

## Overview
"Change management" names two disciplines that share a word, and a project needs both.
**Change control** governs changes to the baselines (scope, schedule, cost, and the quality bar)
so nothing changes by accident or by the loudest voice: a written procedure, a change control
board (CCB) with tolerances, a decision that is communicated, and integrated change control, where
every affected baseline is updated together and verified. **Change adoption** governs how people
move to the new way of working the project delivers, because a flawless system nobody uses is a
failed project: readiness, the sponsor's visible actions, adoption targets, resistance and
reinforcement. This skill owns both processes. `change-request` owns the change request (CR)
form, the change log artifact and the impact scorer that this process decides on. The examples
use the sample Helios project (a fictional customer self-service portal used throughout this
catalog): Dana Okoro (VP Customer Operations, sponsor) chairs its CCB, Sam Lee (project manager)
keeps the change log, and 60 support agents must move their customers to self-service.

## When to use this skill
- The user needs a change control procedure, a CCB, approval tolerances, an emergency change
  route or change freezes, usually in planning before the baseline is frozen.
- Scope is creeping: changes are agreed in corridors, the board rubber-stamps or is bypassed, or
  rejected requests keep coming back.
- A change has been approved and the user needs to know who updates which baseline, how to verify
  it, and whether it is a re-baseline.
- The user must plan adoption, assess readiness, give the sponsor a visible role, set adoption
  targets, or overcome resistance to a new way of working.
- Do NOT use this to write, score or log one change request — use `change-request`, which owns
  the form, the change log and `change_impact.py`.
- Do NOT use this for go-live readiness criteria, the cutover runbook or hypercare — use
  `release-and-cutover`; this skill supplies the freezes, the emergency route and the adoption
  plan it checks.
- Do NOT use this to elicit or rewrite requirements — use `scope-and-requirements`; it updates
  the scope baseline after a change is approved here.

## Methodology fit
- **Waterfall:** a formal CCB with tolerances in money, days and impact band against frozen scope,
  schedule and cost baselines; every change through a CR; each affected baseline re-issued with a
  version after approval; adoption is a workstream that peaks at the big cutover.
- **Agile:** the product owner re-orders the backlog inside the release goal, sprint length and
  budget without a CR; change control covers only the fixed frame (budget, release date,
  contract, a committed Must, the definition of done). Adoption rides each increment, with user
  feedback at every sprint review and targets per release goal.
- **Hybrid:** Helios puts the M4 pilot (2026-08-07), M6 general availability (2026-10-03), the
  $500,000 BAC and the contracted SSO scope under the CCB, while self-service UI and
  knowledge-base Should and Could stories flex in the backlog; adoption is staged: pilot cohort
  of 200, then a 25% → 50% → 100% ramp.

## Inputs you need
- The approved baselines and their versions (scope statement and WBS, schedule, cost with the
  contingency and management reserve, the definition of done) from `project-planning`.
- The governance: the sponsor, who sits on the board, decision rights and reserve rules.
- The CR form, the change log and its scores from `change-request`.
- For adoption: the affected groups and their stance from `stakeholder-management` (Helios:
  support agents, Resistant), the benefit and its baseline from `business-case`, the release
  dates from `release-and-cutover`, and the transition requirements (training, support model)
  from `scope-and-requirements`.

## Workflow
1. **Write the change control procedure.** Copy `assets/change-control-plan-template.md`: list
   the baselines under control, what needs a CR and what the product owner or PM may change
   alone, and the flow raise → log → assess → decide → communicate → implement → verify and
   close (`references/change-control-process.md`). *Done: a written procedure that says what
   needs a CR and what does not.*
2. **Constitute the CCB and set tolerances.** Name the chair (normally the sponsor), members,
   quorum and slot; set PM, CCB and sponsor tiers; define the emergency route and the change
   freezes before each release. Helios: PM up to $5,000 and 2 days from contingency; CCB on
   Tuesdays above that within contingency; sponsor for HIGH impact, management reserve or a move
   of M6. *Done: tolerances and routes agreed by the sponsor before the baseline freeze.*
3. **Freeze the baselines and announce the only door in.** At baseline approval (Helios v1.0,
   2026-05-08) record each baseline's version in section 1 of the change control plan and tell
   the team and stakeholders how to raise a change. *Done: versions recorded; everyone knows that change control is the only
   way a baseline moves.*
4. **Decide each change.** Each request is raised, logged and scored with `change-request`,
   which owns the change log artifact (`.claude/skills/change-request/assets/change-log.csv`);
   give its scorer the plan's limits so the routing matches (Helios after CR003: $28,000 of
   contingency undrawn):
   ```bash
   python .claude/skills/change-request/scripts/change_impact.py .claude/skills/change-request/assets/change-log.csv --pm-limit-cost 5000 --pm-limit-days 2 --ccb-limit-cost 28000 --reserve-cost 40000
   ```
   The named authority chooses approve, reject, defer or request more information and records
   the rationale, conditions and funding (Helios: CR003 approved, CR005 rejected, CR001 deferred
   to phase 2, CR002 sent back for IdentityCo's quote). *Done: every CR has a decision, decider
   and date, or a dated question outstanding.*
5. **Communicate the decision.** Within one business day, in writing, tell the requester and
   every affected owner the decision, rationale and conditions, then list it in the weekly
   status report (message format in `assets/change-control-plan-template.md`). *Done: no
   decision is known only to the people in the room.*
6. **Implement through every affected baseline.** Use the "After approval" table in
   `references/change-control-process.md`: scope via `scope-and-requirements` and
   `work-breakdown-structure`, schedule via `project-schedule`, cost via `cost-management`,
   quality via `quality-management`, risk via `risk-register`, people via `resource-management`.
   Re-baseline only if the test in `.claude/skills/project-planning/references/baseline-guide.md`
   says so. *Done: each affected baseline has a new version citing the CR id.*
7. **Verify and close, and watch the burden.** Within five business days of `Implemented`, check
   every affected baseline, record "verified by / date", set `Closed`; rejected and deferred CRs
   stay closed at the decision with their reason. Report the change burden against the
   contingency at each steering (`change_impact.py --reserve-cost`). *Done: nothing is Closed
   unverified, and the board sees the cumulative burden (Helios: 105% of the contingency if every
   pending CR were approved).*
8. **Assess change readiness.** Copy `assets/adoption-plan-template.md`; rate each affected group
   on impact, attitude, capacity and history, and find its weakest ADKAR step
   (`references/adoption-readiness.md`). *Done: every affected group has a readiness rating, its
   weakest step and the evidence.*
9. **Plan adoption with the sponsor and set targets.** Schedule the sponsor's visible actions per
   ADKAR step, plan the actions for each gap as WBS work, and agree adoption targets (measure,
   baseline, target, date, source, owner) with the sponsor and benefit owner; hand the go-live
   criteria to `release-and-cutover`. `assets/adoption-plan-sample.md` is the Helios plan.
   *Done: an adoption plan keyed to readiness gaps, with named sponsor actions and an adoption
   target and date agreed before go-live.*
10. **Manage resistance.** Log each source with its root cause in the resistance log (section 6
    of the adoption plan); fix genuine flaws (defect or CR) and work the ADKAR step for
    reluctance, rather than overriding it. *Done: every resistance source has a root cause, a
    response and an owner.*
11. **Reinforce until the targets are met.** Following section 8 of the adoption plan, measure
    against the targets weekly, recognise adopters with the sponsor, retire the old path on an
    announced date (Helios: 2026-10-19), close the feedback loop, and hand the measures to the
    benefit owner. *Done: targets met or a dated corrective action; the old way retired; an
    owner named after handover.*

## Quality checklist
- [ ] The procedure states what needs a CR and what the product owner or PM may change alone.
- [ ] The CCB has a named chair, members, quorum and slot; the emergency route has a response
      time; each release has dated change freezes.
- [ ] PM, CCB and sponsor tolerances are written in money, days and impact band, and the same
      numbers are passed to `change_impact.py`.
- [ ] Every decision is approve, reject, defer or request more information, with rationale,
      conditions, decider and date, and the requester and affected owners were told in writing.
- [ ] Every approved change has a new version of each affected baseline citing the CR id, and
      none is Closed before verification.
- [ ] Rejected and deferred CRs stay in the log with a reason; deferrals have a revisit date.
- [ ] The cumulative change burden against the contingency is reported at each steering.
- [ ] Every affected group has a readiness rating and its weakest ADKAR step.
- [ ] Sponsor actions are dated, and adoption targets were agreed before go-live.
- [ ] Every resistance source has a root cause, a response and an owner.
- [ ] The old way has a retirement date, and reinforcement has an owner after handover.

## Anti-patterns
- Treating change control and adoption as one thing; they need different plans and owners.
- Accepting changes verbally with no impact assessment ("just a small tweak").
- A CCB that rubber-stamps everything, or one so slow that people go around it; no emergency route.
- Deciding without telling the requester, so the same request returns next month.
- Updating the scope but not the schedule and cost, so the baselines contradict each other and
  earned value stops meaning anything.
- Calling every approved change a re-baseline, or quietly editing a baseline to match reality.
- A sponsor who delegates adoption to the PM's emails and is never seen using or backing the change.
- "Measure adoption" after go-live with no target agreed beforehand.
- Crushing resistance instead of understanding it; it often signals a real, unaddressed flaw.
- Declaring victory at go-live with no reinforcement, so users drift back to the old way.

## Resources
- `references/change-control-process.md` — what needs a CR, the flow, decision outcomes,
  communication, the status lifecycle, CCB, tolerances, emergency route and freezes, integrated
  change control, who updates which baseline, re-baseline test, verification, agile, process health.
- `references/adoption-readiness.md` — the sponsor's visible role, ADKAR, readiness assessment,
  adoption targets, resistance and reinforcement.
- `assets/change-control-plan-template.md` — fill-in change control plan with placeholders.
- `assets/change-control-plan-sample.md` — sample: the Helios change control plan and its first
  decisions (CR001, CR002, CR003, CR005).
- `assets/adoption-plan-template.md` — fill-in adoption plan: sponsor actions, readiness, targets,
  actions, resistance log, go-live criteria, reinforcement.
- `assets/adoption-plan-sample.md` — sample: the Helios adoption plan agreed before the M4 pilot.
- No script of its own: the scorer this process drives belongs to `change-request`; run
  `python .claude/skills/change-request/scripts/change_impact.py --help` for its flags.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-planning` — agrees this procedure and its tolerances before the baseline freeze (its
  step 11) and hands over the baselines it protects; re-plans when a change is a re-baseline.
- `project-delivery` — where changes and resistance surface during execution; its step 7 routes
  baseline changes here, and it runs the adoption work as planned deliverables.
- `change-request` — owns the CR form, the change log and the impact/authority scorer
  (`change_impact.py`); this process decides, communicates and verifies what it records.
- `scope-and-requirements` — owns the scope statement and traceability matrix updated after an
  approved scope change, and the transition requirements the adoption plan delivers.
- `release-and-cutover` — receives the change freezes, the emergency route and the adoption
  readiness criteria; its go/no-go and hypercare check them and measure the adoption targets.
