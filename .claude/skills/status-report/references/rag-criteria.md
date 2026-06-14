# RAG Criteria

RAG (Red/Amber/Green) ratings only mean something if the same thresholds apply every
period. Rate each dimension — scope, schedule, cost, quality — separately, then roll up.

## Per-dimension thresholds

| Dimension | Green | Amber | Red |
| --- | --- | --- | --- |
| **Schedule** | On or ahead of baseline; SPI >= 0.95 | Slipping but recoverable in-period; SPI 0.85-0.95 | Key milestone or end date at risk; SPI < 0.85 |
| **Cost** | At or under budget; CPI >= 0.95 | Overspend recoverable within tolerance; CPI 0.85-0.95 | Forecast overrun beyond tolerance; CPI < 0.85 |
| **Scope** | Delivering agreed scope; no open change pressure | Change requests pending that may affect scope/dates | Scope changed or cannot be delivered as agreed |
| **Quality** | Defects/acceptance within thresholds | Quality trending down; defects rising but contained | Acceptance criteria failing; rework threatens delivery |

SPI = earned value / planned value; CPI = earned value / actual cost. Pull both from
`cost-management` when earned value is tracked. Where it is not, substitute a defensible
proxy (e.g. % milestones met on time) and say which proxy you used.

## Rolling up to an overall RAG

- The overall rating is **no greener than the worst material dimension**. One red on a
  dimension that matters makes the project amber or red, not green.
- A dimension that is red but already has an agreed recovery plan in motion may be
  reported amber — but say so explicitly and name the plan.
- State the **direction of travel**: an amber improving toward green reads very
  differently from an amber sliding toward red. Include last period's rating.

## Setting RAG honestly

- **Rate against the threshold, not against how you feel.** "We are working hard" is not
  green; "the milestone date still holds" is.
- **Green is a claim, not a default.** If you cannot point to evidence, it is at least
  amber. Silence and optimism are how a green project becomes a surprise red.
- **Escalate early.** Going amber the moment a risk becomes likely gives the sponsor time
  to act. A late jump from green to red destroys trust.
- **Be consistent across reports.** If a dimension was red last period and nothing
  changed, it is still red — do not quietly relabel it.

## Worked example (Helios)

The Helios self-service portal is on budget (CPI 1.0 -> cost Green) but the identity-
provider integration has slipped two weeks, putting the UAT milestone at risk (SPI 0.88
-> schedule Amber). Quality and scope are Green. Worst material dimension is schedule
Amber, so the **overall RAG is Amber**, direction flat, with a recovery plan to add an
integration engineer noted as the decision needed.
