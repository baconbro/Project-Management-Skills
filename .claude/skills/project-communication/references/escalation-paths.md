# Escalation Paths

An escalation path is the agreed route for raising an issue or decision to someone with the
authority or information to resolve it, *before* it does damage. Defined in advance, escalation
is healthy and fast; left undefined, issues either fester at the wrong level or leap straight to
the sponsor as a surprise. Every communication plan needs one.

## The three ingredients
1. **Levels** — the ladder of who handles what.
2. **Triggers** — the conditions that move an issue up a level.
3. **Time-boxes** — how long it may sit at a level before it must move.

## Example escalation ladder (Helios)

| Level | Owner | Handles | Trigger to escalate up | Time-box |
|-------|-------|---------|------------------------|----------|
| 1 | Team / lead | Day-to-day blockers, technical choices | Not resolved within the team; cross-team dependency | 1 working day |
| 2 | Project manager | Cross-team issues, scope/schedule/cost within tolerance | Breaches a tolerance; needs a decision the PM can't make | 2 working days |
| 3 | Sponsor (VP of Support) | Tolerance breaches, priority conflicts, funding | Strategic conflict; needs budget or scope change beyond mandate | 3 working days |
| 4 | Steering committee / portfolio | Cross-project conflict, major change, business risk | Enterprise impact; affects other projects | Next steering meeting |

Keep the ladder short. Most issues should resolve at level 1 or 2; if everything reaches the
sponsor, the lower levels are not empowered.

## Triggers: when to escalate
Escalate on *defined conditions*, not on mood. Good triggers are objective:
- A tolerance is breached (schedule slip > X days, forecast cost over baseline + reserve).
- A decision is needed that is outside the current level's authority.
- A risk has materialized and the response exceeds the level's means.
- A time-box has expired with no resolution.
- A dependency on another team or vendor is blocked.

## Time-boxes: stop issues from rotting
Each level holds an issue only for its time-box; if unresolved, it *must* move up — escalation is
a duty, not an admission of failure. Time-boxes prevent the two failure modes: hoarding an issue
too long, and panic-escalating instantly.

## Good escalation hygiene
- Escalate the **decision needed**, not just the problem ("need a go/no-go on launching without
  reporting by Thursday"), with options and a recommendation.
- Escalate *early and small* rather than *late and large*.
- Record the escalation and its outcome so the path is auditable.
- Pair the path with the cadence in `assets/communication-plan.csv` so people know the route
  before they need it — and surface live escalations through `status-report`.
