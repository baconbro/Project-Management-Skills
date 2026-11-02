# Engagement Assessment Matrix — <project name>

**Confidential.** This matrix records candid judgements about named people. Share it with the
sponsor and the row owners only; the communication plan is the document you circulate.

| Version | As of | Prepared by | Reviewed with the sponsor |
|---|---|---|---|
| <n.n> | <YYYY-MM-DD> | <project manager> | <sponsor name>, <YYYY-MM-DD> |

## How to fill it
1. Copy this file into your project folder before filling it, so the bundled template stays blank.
2. Add one row per row of your stakeholder register, with the same id, quadrant and owner.
3. Mark the current level `C` and the desired level `D`; when they are the same, write `C D` in
   one cell.
4. Gap = desired score minus current score (Unaware 0, Resistant 1, Neutral 2, Supportive 3,
   Leading 4). A negative gap means over-engaged.
5. Rank the gaps by quadrant (Manage Closely, Keep Satisfied, Keep Informed, Monitor), then by
   gap size, then by the date you need the stakeholder. Replace every `<placeholder>`.

## 1. Current (C) versus desired (D) engagement

| Id | Stakeholder (role) | Quadrant | Unaware | Resistant | Neutral | Supportive | Leading | Gap | Owner |
|---|---|---|---|---|---|---|---|---|---|
| <S01> | <name (role)> | <quadrant> | <C, D or blank> | <C, D or blank> | <C, D or blank> | <C, D or blank> | <C, D or blank> | <+n> | <owner> |
| <S02> | <name (role)> | <quadrant> | <C, D or blank> | <C, D or blank> | <C, D or blank> | <C, D or blank> | <C, D or blank> | <+n> | <owner> |
| <S03> | <name (role)> | <quadrant> | <C, D or blank> | <C, D or blank> | <C, D or blank> | <C, D or blank> | <C, D or blank> | <+n> | <owner> |

## 2. Closing the gaps (priority order)

| Priority | Id | Stakeholder | From → to | Concern to address | Action | Owner | Due |
|---|---|---|---|---|---|---|---|
| 1 | <S0n> | <name> | <current> → <desired> | <key concern from the register> | <concrete action, verb first> | <owner> | <date or milestone> |
| 2 | <S0n> | <name> | <current> → <desired> | <key concern from the register> | <concrete action, verb first> | <owner> | <date or milestone> |
| <no gap> | <S0n> | <name> | <level> (no gap) | <key concern> | <maintain; re-rate trigger> | <owner> | <next review> |

<Note any dependency between rows, for example a group that will only move once its leader does.>

## 3. How to read it
- **C and D in one cell (no gap):** maintain; do not over-invest.
- **C left of D:** raise engagement with the action in section 2.
- **C right of D:** over-engaged; give the stakeholder a defined channel and dial back gracefully.
- **Unaware:** brief them first, then re-rate; they can land anywhere once informed.

## 4. What the sponsor agreed
- <decision or priority agreed with the sponsor, with the date>

## 5. Review history

| Date | Reviewed by | Moves (id: from → to) | Evidence | Next review |
|---|---|---|---|---|
| <YYYY-MM-DD> | <names> | <S0n: Neutral → Supportive, or "first assessment"> | <observed behaviour> | <date or milestone> |

## 6. Handoffs
- [ ] Every action with a cadence passed to `project-communication` as a communication-plan row
      with the same owner.
- [ ] Register ids and the people who hold each role passed to `raci-matrix`.
- [ ] Every high-power or high-interest stakeholder, and every approver, passed to
      `scope-and-requirements` for the elicitation plan.
- [ ] Every supplier row matched to its contract contacts in `procurement-management`.
