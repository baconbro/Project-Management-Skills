# Engagement Playbook

How to turn the analysis into engagement: rate where each stakeholder stands on evidence, set
where you need them, rank the gaps, choose tactics and owners, handle the difficult cases, and
keep the register current. Examples use the sample Helios project (a fictional customer
self-service portal used throughout this catalog); see `assets/stakeholder-register-sample.csv`
and `assets/engagement-matrix-sample.md`.

## 1. Engagement levels: rate on evidence, not hope

| Level (score) | Meaning | Evidence you can observe |
|---|---|---|
| Unaware (0) | Does not know about the project or how it affects them | Has not been briefed; asks "what portal?" |
| Resistant (1) | Aware and opposed to the project or the change | Objects, delays approvals, skips sessions they should attend, lobbies others |
| Neutral (2) | Aware, neither supporting nor opposing | Attends and complies; no advocacy, no objection |
| Supportive (3) | Aware and in favour | Gives time and people, speaks for the project, accepts deliverables promptly |
| Leading (4) | Actively working for its success | Champions it, removes blockers, owns outcomes in their own area |

**Unaware is not an attitude.** Once informed, a stakeholder can land anywhere, so the first
action for every Unaware row is a briefing; re-rate straight after it.

Write the evidence, not the label ("missed 3 of 4 design reviews", not "difficult"). If you
have no evidence, you have not rated them yet — meet them.

## 2. Set the desired level

Not everyone needs to be Leading; over-engaging costs their time and yours.

| Stakeholder | Usual desired level | Helios |
|---|---|---|
| Sponsor, benefit owners | Leading | Dana Okoro, Priya Nair |
| Approvers and gatekeepers | Neutral (approve on the merits) or Supportive | Hana Sato: Neutral; Marcus Webb: Supportive |
| Suppliers and dependency owners | Supportive | IdentityCo, order management team |
| Users whose adoption drives the benefit | Supportive | Pilot customers, support agents |
| Monitor rows | Usually the current level | Marketing: Neutral stays Neutral |

**Current above desired** is a gap too: an over-engaged stakeholder steering design outside
their remit. Give the energy a defined channel (a review slot, a consulted role in
`raci-matrix`) and route their requests through change control.

## 3. Rank the gaps

Gap = desired score minus current score. Rank by:

1. **Quadrant** — Manage Closely, then Keep Satisfied, then Keep Informed, then Monitor.
2. **Gap size** — largest first within a quadrant.
3. **Need date** — the stakeholder whose sign-off or decision is due soonest.

Helios result: Priya Nair (Manage Closely, +2) first; Dana Okoro, then IdentityCo (+1 each, by
need date); then Finance, whose brief is needed for the M1 baseline approval, and Hana Sato,
whose sign-off is due before the M4 pilot (Keep Satisfied, +2 each); Marcus Webb and the order
management team (+1); then pilot customers (+3) and support agents (+2); Marketing has no gap.
The ranking is a default:
when one action unlocks another row — Priya Nair's agreement carries her 60 agents — say so in
the matrix.

## 4. Gap-closing tactics

| Move | Typical cause of the gap | Tactics | Helios |
|---|---|---|---|
| Unaware to aware | Nobody has told them | 1:1 briefing: what changes for them, what you need, by when; then re-rate | Hana Sato's 30-minute data-flow briefing; Finance's onboarding brief |
| Resistant to Neutral | A fear or loss: job, control, workload, blame | Listen first; name the concern openly; fix what you can concretely; give them a voice in design; ask for one small commitment | Agents: the redeployment plan for 6 FTE (dis-benefit D001) agreed before cutover and explained by Priya Nair |
| Neutral to Supportive | No reason to care yet | Show what is in it for them; involve them in the decisions that touch them; make the ask small and specific; give an early win | Marcus Webb: threat-model review in Discovery so the security gate holds no surprises |
| Supportive to Leading | Support without ownership | Give a visible role, decision rights and credit; co-present results | Dana Okoro co-presents the M4 pilot launch; Priya Nair signs off the benefit baseline and owns WBS 1.5 |
| Above desired | Energy aimed at the wrong place | Define their channel and decision boundary; route requests through change control | A pilot customer pushing for live chat (CR001, deferred) is thanked and pointed to phase 2 |

## 5. Difficult situations

- **The sponsor has gone quiet.** Symptoms: missed steering meetings, decisions slipping.
  Ask for 15 minutes with one decision and the cost of delaying it; reconnect the decision to
  the objective (Helios: the 50% ticket cut); if it persists, ask openly whether the project is
  still a priority and take the answer to the steering committee — do not quietly work around
  the sponsor. Log the slipping decision in the issue log kept with `project-delivery`.
- **An active blocker (saboteur).** Meet 1:1, never first in a public forum. Separate their
  position ("no portal") from their interest ("no job losses"); answer the interest. Offer a
  defined channel of influence. If they block without a legitimate claim, escalate through the
  sponsor with evidence, and tell them you are doing so.
- **A quiet blocker (time bomb or tripwire).** Agrees in meetings, does not act. Ask for
  specific, dated commitments and check them; involve their team directly.
- **Two powerful stakeholders want opposite things.** Do not arbitrate yourself. Frame the
  trade-off against the objective and the baseline, take it to the sponsor or steering as a
  decision, and record it in the decision log.
- **A vendor.** The contract sets the formal relationship (`procurement-management`); engagement
  covers the rest: named contacts at working, management and executive level and a written
  escalation path. Helios: IdentityCo's account manager, then its executive sponsor, then Dana
  Okoro.
- **A stakeholder changes role or leaves.** The successor starts as Unaware whatever their
  predecessor's stance; re-run the row from the identification step.

## 6. Choose the owner

The owner is one named person accountable for moving the stakeholder from current to desired —
not a team, not "the project".

- Pick the person with access and credibility: approvers are usually owned by the specialist
  who speaks their language (Helios: Ben Adeyemi owns Marcus Webb and the order management
  team); executives by the PM with the sponsor's backing.
- A stakeholder can own a group they lead (Helios: Priya Nair owns the support agents' row).
- Keep each owner to three or four Manage Closely relationships.
- Every row in the H or M power half must have an owner who can get a meeting within a week.

Helios owners: Sam Lee (S01, S02, S04, S05, S06), Ben Adeyemi (S03, S09), Ava Chen (S07, S10),
Priya Nair (S08).

## 7. Review cadence and re-rating triggers

- **Cadence.** Manage Closely rows at every steering committee (Helios: bi-weekly); the other
  rows monthly; the whole register and the engagement matrix at each milestone or stage gate
  (Helios: M1, M4, M6). Stamp `last_reviewed` on every row you review.
- **Re-rate immediately when:** a change request touches their area (CR002, partner logins,
  re-rates IdentityCo and Marcus Webb); their area turns RED (the SSO work package re-rates
  IdentityCo and Dana Okoro); someone misses a commitment; a sign-off they own falls due; a
  person changes role.
- Record every move (who, from, to, evidence) in the review history of
  `assets/engagement-matrix.md`.

## 8. Confidentiality and ethics

- The register records candid judgements about named people: mark it Confidential, store it
  with restricted access (PM, sponsor, row owners) and never circulate it.
- The shareable artifact is the communication plan built in `project-communication`.
- Write observable facts, not labels, so the register would survive being read by the person
  it describes.
- Engagement is open persuasion. Do not manipulate, withhold information a stakeholder is
  entitled to, or play stakeholders off against each other.

## 9. Register field guide

| Column | Content |
|---|---|
| `id` | S01, S02, ... — stable; reused by `raci-matrix` and `project-communication` |
| `name` | A person, or a group whose members share interest and stance |
| `role` | Job title and role on the project |
| `category` | sponsor, benefit owner, approver, budget holder, supplier, dependency, customer, user, neighbour, team |
| `power`, `interest` | H, M or L (scale in `references/analysis-techniques.md`) |
| `quadrant` | From the mapping rule (M counts as High); upward overrides explained in `strategy` |
| `current_engagement`, `desired_engagement` | Unaware, Resistant, Neutral, Supportive or Leading |
| `key_concerns` | What they care about or fear, including a high impact the interest rating misses |
| `strategy` | Concrete actions with a cadence or date — verbs, not adjectives |
| `owner` | One named person |
| `last_reviewed` | YYYY-MM-DD of the last review of this row |
