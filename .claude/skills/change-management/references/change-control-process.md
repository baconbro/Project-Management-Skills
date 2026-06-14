# Change Control Process

Change control is the process that protects the project's baselines from uncontrolled change.
The point is not to prevent change — change is inevitable and often good — but to ensure every
change is *visible, assessed, decided, and reflected in the baselines*. Without it, scope creep
silently consumes the budget and schedule until the project is late and over with no one able to
say why.

## The end-to-end flow

```
  Raise  ->  Log  ->  Assess impact  ->  Decide (CCB)  ->  Implement  ->  Verify
   |          |             |                  |               |             |
 anyone   change log   scope/cost/sched   approve / reject  do the work   confirm done
                       + risk + options     / defer                       & baselines updated
```

1. **Raise.** Anyone can request a change; capture it on a change request form (`change-request`
   owns this) — what, why, who, urgency.
2. **Log.** Record it in the change log with a unique ID and status. Nothing is "informal".
3. **Assess impact.** Analyze the effect on scope, cost, schedule, quality, and risk, and lay
   out options. `change-request` scores the impact; do not skip this even for "small" changes.
4. **Decide (CCB).** The change control board approves, rejects, or defers — within its authority.
5. **Implement.** Do the approved work; update plans and assignments.
6. **Verify.** Confirm the change was made *and* that all affected baselines were updated.

## The Change Control Board (CCB)
A group with the authority to decide changes. Define:
- **Membership:** sponsor or delegate, PM, and the right technical/business voices.
- **Authority & tolerances:** what the PM may approve alone vs what needs the CCB vs the sponsor
  (e.g. PM approves changes under $5k and 2 days within reserve; larger goes to the CCB).
- **Cadence:** a regular slot plus an emergency path so urgent changes are not stuck for weeks.
A CCB that rubber-stamps everything adds no control; one that is too slow gets bypassed. Tune the
tolerances so routine changes flow and only material ones reach the board.

## Integrated change control
The discipline of ensuring a change is reflected *across all affected baselines at once*. Approve
a scope addition and you must also update the schedule, the cost baseline, the resource plan, and
the risk register — together, not piecemeal. Helios example: adding SSO for a second identity
provider is not just "more dev"; it extends the schedule, raises cost (and consumes contingency),
changes the test scope, and adds a vendor-dependency risk. Integrated change control makes all of
those move as one decision.

## Baselines
- A **baseline** is the approved version of scope, schedule, or cost that you measure against.
- Baselines are *frozen*; the *only* legitimate way to change one is through this process.
- Re-baselining (a formal reset) happens only on a major approved change, and is itself logged.
- Cost performance (`cost-management`) is measured against the cost baseline — silently moving
  the baseline destroys the ability to measure performance, which is why change control guards it.
