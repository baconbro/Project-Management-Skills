---
name: change-management
description: >-
  Governs change in both senses — change CONTROL (the process to raise, assess,
  decide, and verify scope, cost, and schedule changes via a change control
  board and integrated change control) and organizational change ADOPTION
  (readiness, ADKAR-style adoption, resistance, reinforcement). Use when the
  user wants to set up a change control process, run a change control board,
  protect a baseline from scope creep, or plan adoption and overcome resistance
  to a new way of working. Triggers: "change management", "change control",
  "change control board", "CCB", "scope creep", "integrated change control",
  "ADKAR", "adoption", "readiness", "resistance", "organizational change". For
  scoring a single change request, use change-request. Works for waterfall,
  agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: discipline
  phase: cross-cutting
  related: [project-delivery, change-request]
license: MIT
---

# Change Management

## Overview
"Change management" means two distinct disciplines that share a name, and a good project needs
both. **Change control** governs changes to the project's *baselines* — scope, cost, schedule —
so nothing changes by accident or by the loudest voice. **Change adoption** governs how *people*
move to the new way of working the project delivers, because a flawless system nobody adopts is
a failed project. This skill owns both processes; the single-change artifact and its impact
scorer live in `change-request`.

## When to use this skill
- The user needs a change control process, a change control board, or baseline protection.
- The user is fighting scope creep or needs integrated change control.
- The user must plan adoption, assess readiness, or overcome resistance to a new way of working.
- Do NOT use this to raise or score one specific change — use `change-request`, which owns the
  request form and the impact-scoring helper. This skill is the surrounding process.

## Methodology fit
- **Waterfall:** a formal change control board with documented impact analysis against frozen baselines.
- **Agile:** change is welcomed via the backlog — the product owner re-prioritizes; only baselines
  outside the backlog (budget, contract scope) need a CCB. Adoption rides on incremental releases.
- **Hybrid:** baselines under formal control; in-iteration change via the backlog; adoption planned per release.

## Inputs you need
The approved baselines (scope, cost, schedule), the governance structure and decision authority
(who sits on the CCB), and — for adoption — an understanding of who must change behaviour and how
ready they are. Pull the affected stakeholders and their stance from `stakeholder-management`.

## Workflow
1. **Set up change control.** Define the process — raise → log → assess impact → decide (CCB) →
   implement → verify — and name the board and its authority and tolerances. See
   `references/change-control-process.md`. *Done: a documented process and a constituted CCB.*
2. **Protect the baselines.** Establish that scope, cost, and schedule change *only* through this
   process (integrated change control): every approved change updates all affected baselines
   together. *Done: baselines frozen; the only door in is change control.*
3. **Run each change** through `change-request` — that skill captures the request and scores its
   impact; this process decides, records, and verifies it. *Done: each change has a logged
   decision and a verification.*
4. **Plan adoption.** For the organizational change the project delivers, assess readiness and
   work the ADKAR sequence — Awareness, Desire, Knowledge, Ability, Reinforcement. See
   `references/adoption-readiness.md`. *Done: an adoption plan keyed to readiness gaps.*
5. **Manage resistance.** Identify resistance early, find its root cause, and address it
   (involvement, communication, addressing real concerns) rather than overriding it. *Done:
   resistance sources named with a response each.*
6. **Reinforce.** After go-live, sustain the change — measure adoption, celebrate wins, fix
   what frustrates users, and remove the old way so people cannot drift back. *Done: a
   reinforcement plan so the change sticks.*

## Quality checklist
- [ ] A change control process and a constituted CCB with defined authority exist.
- [ ] Scope, cost, and schedule baselines change only through integrated change control.
- [ ] Every change is logged, decided, and verified (via `change-request`).
- [ ] Adoption is planned against readiness using an ADKAR-style sequence.
- [ ] Resistance is identified by root cause, not just overridden.
- [ ] A reinforcement plan sustains the change after go-live.

## Anti-patterns
- Treating change control and adoption as the same thing — they need different plans and skills.
- Accepting scope changes verbally with no impact assessment ("just a small tweak") — pure scope creep.
- A CCB that rubber-stamps everything, or one so slow it gets bypassed.
- Launching the system and assuming people will adopt it because it is better.
- Crushing resistance instead of understanding it — resistance often signals a real, unaddressed risk.
- Declaring victory at go-live with no reinforcement, so users drift back to the old way.

## Resources
- `references/change-control-process.md` — raise → log → assess → decide (CCB) → implement → verify; baselines.
- `references/adoption-readiness.md` — ADKAR, stakeholder readiness, resistance, and reinforcement.

## Related skills
- `change-request` — the single-change form and impact scorer this process drives.
- `project-delivery` — where changes are controlled and adoption happens during execution.
