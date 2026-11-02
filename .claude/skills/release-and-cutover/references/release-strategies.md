# Release strategies

How users, data and support move from the old way of working to the new one. Choose the
strategy before writing readiness criteria or a runbook: it decides how much can fail at once,
how cheap a rollback is, and how long the support team runs two ways of working side by side.

## Deployment, release and cutover are different things
- **Deployment** puts new code or configuration into production. **Release** exposes it to
  users. **Cutover** is the controlled switch of users, data, interfaces and support from the
  old way to the new one, including retiring the old way.
- Feature flags, allow-lists and dark launches decouple the three: deploy on Saturday, release
  to 200 customers on Monday, switch the support channel for everyone a month later.
- An automated deployment pipeline does not remove the business cutover. Training, the support
  model, customer communication and decommissioning still need a plan, a decision and an owner.

## The strategies compared
| Strategy | How it works | Fits when | Watch out for | Rollback cost |
|---|---|---|---|---|
| Big-bang | Everyone moves at one moment; the old way stops | Old and new cannot coexist (one ledger, shared master data, a regulatory date); a rehearsed rollback exists | Largest blast radius; one window to get everything right; support floor flooded on day 1 | High once users transact in the new system: name the point of no return |
| Phased | Move in waves by site, region, customer segment, product line or module | Segments are separable; the organisation can absorb only so much change at once | Interfaces between old and new during coexistence; wave fatigue; the last wave gets least attention | Low for the current wave, high for completed waves |
| Pilot | One small, representative group goes first; a dated decision to scale follows | Adoption, behaviour or performance is uncertain and real evidence is worth a delay | A pilot of friendly users only; a "permanent pilot" with no scale decision date | Low: the pilot group returns to the old way |
| Parallel run | Old and new process the same live work for a period; outputs are compared | Errors are costly and hard to detect (payroll, billing, regulated calculations) | Double effort; which system is the source of truth; reconciliation workload | Lowest: the old system is still live |
| Feature flags / canary | Deploy dark, then release to a list or a percentage of users, widening on evidence | Software you control, with telemetry that shows a problem within minutes | Flag debt; untested flag combinations; flags that silently change behaviour | Very low: flip the flag |
| Blue-green | Two production environments; traffic switches from one to the other | Stateless services on infrastructure that supports it | Schema changes break the instant switch-back; the cost of two environments | Low for code, high once data changed |

Pilot and phased are business strategies; flags, canary and blue-green are technical patterns
that make them cheap. Most real releases combine one of each.

## The eight questions that decide it
1. **Can old and new coexist?** If only one system can hold the master record, the choice is
   big-bang or parallel run; if both can run, pilot or phased is usually safer.
2. **How reversible is it?** Name the point of no return. If it comes late or not at all,
   incremental strategies cost little; if it comes early, rehearse more and stage less.
3. **What is the blast radius of a defect?** Customers affected, money and regulatory exposure
   per hour of failure. Large blast radius argues for a pilot or a ramp.
4. **Who owns the data?** A system that only reads from systems of record rolls back by
   redirecting users. One that becomes the system of record needs migration, reconciliation
   and a rollback that reverses transactions.
5. **How much change can people absorb?** Training and service-desk capacity, seasonal peaks,
   other releases landing on the same users. The adoption plan in `change-management` sets this.
6. **What does dual running cost?** Licences, double keying, two support models. Expensive dual
   running argues for short phases or one well-rehearsed cutover.
7. **Which dates are fixed?** The old system's contract end, regulatory deadlines, blackout
   periods such as month-end close or peak trading.
8. **What do we still need to learn?** If adoption or performance at scale is uncertain, a
   pilot buys evidence before the irreversible step.

## Freezes and the cutover window
- State the start and end of each freeze: **code freeze** (release candidate fixed; only
  severity-1/2 fixes through the emergency change route), **change freeze** (no other change to
  the shared systems the release touches) and, when data moves, **business freeze** (no data
  entry the migration cannot reconcile).
- Pick the window by traffic (lowest), people (every step owner and vendor available, full
  support staffed the next business day) and calendar (no month-end, payroll run, sale or
  holiday).
- Size it as rehearsed critical path + 20-30% contingency + the full rollback duration. If it
  does not fit, move scope out of the cutover; never squeeze the rollback.
- Avoid a Friday-evening go-live with nobody on hand on Monday morning. A Saturday-morning
  cutover with a Monday business go-live gives a quiet day to verify.

## Transition requirements: the work beyond the build
Training, user access and provisioning, data conversion and reconciliation, the support model
and runbooks, known-error articles, contracts and licences for the new service, customer and
staff communications, and decommissioning the old way. Capture them as transition requirements
in `scope-and-requirements` so they are estimated, scheduled and tested like features.

## By methodology
- **Waterfall:** one or a few large cutovers at the end; the strategy is chosen in planning,
  rehearsed at least twice and approved at a stage gate.
- **Agile:** continuous delivery makes deployment routine and flag-driven; switching a channel
  or retiring a process is still a planned cutover tied to a release goal.
- **Hybrid:** releases at milestones, each staged behind flags, each with its own go/no-go; the
  strategy is fixed with the baseline and changed only through change control.

## Helios worked choice
The sample Helios project (a fictional customer self-service portal used throughout this
catalog) combines a pilot with a phased ramp:
- **Pilot at M4 ("MVP live to pilot"):** password reset by email, order status and the
  knowledge base, released by allow-list flag to the cohort of 200 pilot customers. The manual
  ticket channel stays open for everyone, so the fallback is the existing process.
- **General availability (GA) at M6:** release 2.0 adds SSO sign-in through the identity
  provider, the WCAG 2.2 AA uplift (CR003) and the deflection report. The customer flag ramps
  25% → 50% → 100% from Saturday 2026-10-03 to Monday 2026-10-12, each step gated on the
  hypercare metrics.
- **Why not big-bang:** R001 (identity-provider integration, the only HIGH risk) concentrates
  failure in SSO, and the business case accepts at most a 3-point CSAT dip in the cutover month
  (dis-benefit D002).
- **Why not a parallel run:** the portal reads from the order system and the identity provider
  and owns no master data, so redirecting users is the rollback; double keying would add cost
  and no safety.
- **Decommission last:** the ticket-form categories for password reset and order status close
  only after a week at 100%, and configuration can restore them if hypercare needs it.
