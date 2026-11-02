---
name: stakeholder-management
description: >-
  Identifies and analyzes stakeholders (register, power/interest grid, salience) and plans
  engagement with owners and actions. Use when working out who the stakeholders are,
  prioritizing them, or handling a disengaged sponsor or a stakeholder who is blocking the
  project.
metadata:
  version: 1.1.0
  category: discipline
  phase: cross-cutting
  related: [project-initiation, project-planning, raci-matrix, project-communication, project-charter, scope-and-requirements, procurement-management]
license: MIT
---

# Stakeholder Management

## Overview
Stakeholder management works out who can affect or is affected by the project, how much each
one matters, where they stand today, and what you will deliberately do — and who will do it —
to move them to where the project needs them. Projects rarely fail on the technology; they fail
because a key stakeholder was ignored, surprised or left unconvinced. This skill produces two
artifacts: a stakeholder register (power, interest, quadrant, current and desired engagement,
concerns, strategy, owner) and an engagement assessment matrix that ranks the gaps for the
sponsor. The worked example is the sample Helios project (a fictional customer self-service
portal used throughout this catalog): ten stakeholders from the sponsor, Dana Okoro (VP
Customer Operations), to the 200 pilot customers, with the benefit owner, Priya Nair (Head of
Support Operations), as priority one.

## When to use this skill
- The user is starting a project and needs to find everyone who is involved or affected.
- The user wants to rate, map or prioritize stakeholders (power/interest grid, salience, cube).
- A stakeholder is blocking, disengaged or over-engaged — including a sponsor who has gone
  quiet — and needs a deliberate plan with an owner.
- The register is stale: a milestone, a change request or a re-organization has moved people.
- Do NOT use this to assign who does, approves or is told about each piece of work — use
  `raci-matrix` instead.
- Do NOT use this to schedule messages, channels and reporting cadence — use
  `project-communication`, which turns the strategy built here into a communication plan.
- Do NOT use this to plan the adoption of a new way of working across a whole user group — use
  `change-management`; this skill supplies the group's current stance.

## Methodology fit
- **Waterfall:** a full register built in initiation, baselined with the plan in
  `project-planning`, and re-rated at every stage gate and whenever a change request touches a
  stakeholder's area; the engagement matrix is reviewed with the sponsor at each gate.
- **Agile:** the product owner carries day-to-day engagement and the sprint review is the main
  engagement event; keep a one-page map, re-rate it at release planning or every few sprints,
  and invite Keep Informed users to sprint reviews rather than sending them reports.
- **Hybrid (Helios):** the register fixes the sponsor, approvers and vendor at initiation;
  Manage Closely rows are reviewed at the bi-weekly steering committee, the approvers are
  engaged through the security and data-residency gates before the M4 pilot, and pilot
  customers and Support Operations through sprint reviews and usability rounds.

## Inputs you need
The charter (sponsor, PM and key stakeholders, from `project-charter`), the business case's
benefits and dis-benefits with their owners, the org chart, the approvers and gates, vendor
contracts and contacts (from `procurement-management`), and any history with these people. With
no sponsor named yet, run `project-initiation` first: a register cannot stand in for an
authorized sponsor.

## Workflow
1. **Identify everyone.** Copy `assets/stakeholder-register.csv` into your project folder (the
   bundled template stays blank) and walk the ten identification categories in
   `references/analysis-techniques.md`: sponsor, benefit owners, people whose work changes,
   users, approvers, budget holders, suppliers, dependencies, regulators, neighbours. Use a group
   row only when its members share interest and stance. Helios lists ten rows, S01–S10.
   *Done: every category is filled or explicitly empty, and each row has an id, name and role.*
2. **Rate power and interest H, M or L** with the scale in `references/analysis-techniques.md`.
   Interest is how much they care about and engage with the outcome, not how much it affects
   them; note a high impact in `key_concerns`. *Done: every row has both ratings and a one-line
   reason you could defend to the stakeholder.*
3. **Place each row on the grid by the mapping rule: M counts as High on both axes; only L falls
   in the low half.** Write the result in `quadrant`; override only upward, with the reason at
   the start of `strategy`. Check that the sponsor and every benefit owner land in Manage
   Closely — Helios' Priya Nair (power M, interest H) does. For contested priorities apply the
   salience model; for tactics, the stakeholder cube (both in the same reference). *Done: every
   quadrant matches the rule or carries an override reason, and no sponsor or benefit owner sits
   outside Manage Closely.*
4. **Assess current and desired engagement** (Unaware, Resistant, Neutral, Supportive, Leading)
   from observed evidence, using sections 1–2 of `references/engagement-playbook.md`. Desired is
   not always Leading: Helios needs Hana Sato (Legal & Compliance) Neutral, not a champion.
   *Done: both levels, and the evidence behind the current one, are recorded for every row.*
5. **Set the strategy and the owner.** For each row write verb-first actions with a cadence or
   date in `strategy`, the concern they answer in `key_concerns`, one named person in `owner`
   (playbook sections 4–6) and today's date in `last_reviewed`. Mark the register Confidential:
   it records candid judgements about people. Compare with
   `assets/stakeholder-register-sample.csv`. *Done: every row has a dated or cadenced action and
   a named owner, and each H or M power row's owner can get a meeting within a week.*
6. **Rank the gaps and review them with the sponsor.** Copy `assets/engagement-matrix.md`, mark
   C and D, compute each gap and rank by quadrant, then gap size, then need date (playbook
   section 3). `assets/engagement-matrix-sample.md` shows Helios: Priya Nair (Neutral to
   Leading) is priority one because her 60 agents will move only once she leads. *Done: the
   matrix is ranked, the sponsor has reviewed it, and what they agreed is recorded with a date.*
7. **Hand off.** Give `project-communication` every action with a cadence, as a
   communication-plan row with the same owner; give `raci-matrix` the register ids and the
   people behind each role; give `scope-and-requirements` every high-power or high-interest
   stakeholder for the elicitation plan; match supplier rows to contract contacts in
   `procurement-management`. *Done: the handoff checklist in the matrix is ticked.*
8. **Review on cadence and on triggers.** Review Manage Closely rows at each steering committee
   (Helios: bi-weekly), the rest monthly, and everything at each milestone (M1, M4, M6); re-rate
   at once when a change request touches someone's area, their area turns RED, a commitment is
   missed, a sign-off falls due or a person changes role (playbook section 7). Stamp
   `last_reviewed` and log each move in the matrix's review history. *Done: no row's
   `last_reviewed` is older than its cadence, and every move has evidence.*

## Quality checklist
- [ ] Every identification category is covered or explicitly empty; resistors and quiet
      blockers are listed, not only supporters.
- [ ] Every row has power and interest rated H, M or L, and `quadrant` follows the mapping rule
      (M counts as High) or its strategy starts with an upward-override reason.
- [ ] The sponsor and every benefit owner are in Manage Closely.
- [ ] Every row has current and desired engagement, and each current level rests on stated
      evidence.
- [ ] Every row has one named person as `owner` and a strategy with at least one dated or
      cadenced action — no adjectives such as "keep engaged".
- [ ] The engagement matrix is ranked by quadrant, gap size and need date, and the sponsor's
      review is dated.
- [ ] The register and matrix are marked Confidential and stored with restricted access.
- [ ] The handoffs to `project-communication`, `raci-matrix` and `scope-and-requirements` are
      done.
- [ ] Every `last_reviewed` date is within its row's review cadence.

## Anti-patterns
- Treating the register as a one-time initiation artifact that is never re-rated.
- Reading M as Low, so the benefit owner or a critical vendor lands in Keep Informed or Monitor.
- Confusing interest with power — a loud, low-power voice is not a priority by volume — or with
  impact: a highly affected group that has not yet heard of the change still needs engaging.
- Listing only supporters and ignoring resistors and quiet blockers.
- Strategies written as adjectives ("keep engaged") with no action, date or owner, or owned by
  "the team".
- Setting every desired level to Leading, which wastes approvers' time and yours.
- Circulating the register: it records judgements about people; share the communication plan.
- Collapsing engagement into communication — engagement is the intent, the comms plan is the
  vehicle.

## Resources
- `references/analysis-techniques.md` — identification prompts, the power and interest scale,
  the H/M/L-to-quadrant mapping rule with the Helios placements, and the seven salience types
  and eight stakeholder-cube types, each with a Helios example.
- `references/engagement-playbook.md` — engagement levels and their evidence, desired levels,
  gap ranking, gap-closing tactics, difficult situations (a quiet sponsor, active and quiet
  blockers, conflicting stakeholders, vendors), choosing owners, review cadence and triggers,
  confidentiality, and the register field guide.
- `assets/stakeholder-register.csv` — fill-in register with `<placeholders>`: power, interest,
  quadrant, current and desired engagement, key concerns, strategy, owner and last reviewed.
- `assets/stakeholder-register-sample.csv` — sample register for Helios: ten stakeholders,
  every quadrant consistent with the mapping rule, each with a named owner.
- `assets/engagement-matrix.md` — fill-in engagement assessment matrix: current-versus-desired
  grid, ranked gap actions, sponsor agreements, review history and handoff checklist.
- `assets/engagement-matrix-sample.md` — sample matrix for Helios, with Priya Nair as priority
  one.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-initiation` — calls this skill in its stakeholder step and carries the register and
  engagement approach into the kickoff.
- `project-planning` — refreshes the engagement strategy here before building the
  communication plan, and baselines the register with the plan.
- `raci-matrix` — takes the register ids and the people behind each role and turns them into
  role-level responsibilities; this skill keeps their engagement, not their accountabilities.
- `project-communication` — turns each strategy action into a scheduled message with the same
  owner, audience, channel and cadence.
- `project-charter` — names the sponsor, project manager and key stakeholders this register
  starts from.
- `scope-and-requirements` — plans elicitation from the high-power and high-interest rows, and
  sends back stakeholders whose requests were excluded or deferred for follow-up engagement.
- `procurement-management` — supplies each vendor's contract contacts and escalation path for
  its supplier row (Helios: IdentityCo, S05).
