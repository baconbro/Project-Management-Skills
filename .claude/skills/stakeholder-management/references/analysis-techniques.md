# Stakeholder Analysis Techniques

How to find every stakeholder and decide how much attention each one gets. Start with the
identification prompts, rate everyone on the power/interest grid, and use the salience model
and the stakeholder cube only when the grid cannot separate two cases or cannot tell you which
tactic to use. Examples use the sample Helios project (a fictional customer self-service portal
used throughout this catalog); its full register is `assets/stakeholder-register-sample.csv`.

## 1. Identify: prompts that find the missing stakeholders

Walk every category below; an empty category is a question to answer, not a pass.

| Category | Ask | Helios |
|---|---|---|
| Sponsor and governance | Who funds, authorizes, chairs the steering committee? | Dana Okoro, VP Customer Operations (sponsor) |
| Benefit owners | Who owns each benefit in the business case after the project closes? | Priya Nair, Head of Support Operations |
| People whose work changes | Who gains, loses or changes tasks? Check the dis-benefits | 60 support agents; 6 FTE move to the complex-case queue |
| Users and customers | Who will use the output, inside and outside? | 200 pilot customers, then all customers at GA |
| Approvers and gatekeepers | Who must sign off: security, legal, privacy, accessibility, architecture? | Marcus Webb (Security lead), Hana Sato (Legal & Compliance) |
| Budget holders | Who releases or can withdraw money? | Finance (budget holder for the $500,000 BAC) |
| Suppliers and partners | Which vendors, contractors or partners deliver or integrate? | IdentityCo (identity-provider vendor) |
| Dependencies | Which teams or systems must change or give access? | Order management team (order API) |
| Regulators and external bodies | Which laws, regulators, auditors or unions apply? | Covered through Legal & Compliance for Helios |
| Neighbours | Which projects compete for the same people, systems or customers? | Marketing (GA launch campaign) |

Techniques: follow the money (who pays, who saves), follow the data (who owns each system
touched), follow the sign-offs (every gate has an approver), and ask each stakeholder you meet
"who else should I talk to?" until no new names appear.

**Granularity.** Use an individual when one person holds the power (a sponsor, an approver);
use a group when its members share the same interest and stance (pilot customers). Split a
group as soon as its members' stances differ — for example, team leads who back the portal and
agents who fear it.

## 2. Power / interest grid

Rate each stakeholder on two axes:

- **Power** — ability to change the project's outcome, budget, scope, timing or continuation:
  formal authority, control of money or people, a sign-off or veto, critical expertise, or
  influence over someone who has these.
- **Interest** — how much they care about and actively engage with the outcome.
- **Impact is a separate axis.** How much the outcome *affects* them is impact, not interest.
  The two diverge: a highly affected group that has not yet heard of the change (for example,
  agents before the portal is announced) is low interest, so the grid places it in Monitor even
  though it needs proactive engagement. Record the impact in `key_concerns` and use the upward
  override below.

**Rating scale (H/M/L)**

| Rating | Power | Interest |
|---|---|---|
| H | Can stop, fund, re-scope or cancel (sponsor, budget holder, approver with a veto) | Follows the project actively, asks questions, attends without being chased |
| M | Can delay, or strongly influences someone rated H (delegated sign-off, vendor, dependency owner) | Engages when their own area is touched |
| L | Can comment but cannot block | Pays attention only when something goes wrong |

```
                 POWER
                   ^
         Keep      |     Manage
         Satisfied |     Closely
                   |
       ------------+------------>  INTEREST
                   |
         Monitor   |     Keep
         (minimal) |     Informed
                   |
```

### The mapping rule: from H/M/L to the four quadrants

**M counts as High on both axes; only L falls in the low half.**

| Power \ Interest | L | M | H |
|---|---|---|---|
| **H** | Keep Satisfied | Manage Closely | Manage Closely |
| **M** | Keep Satisfied | Manage Closely | Manage Closely |
| **L** | Monitor | Keep Informed | Keep Informed |

- **Why M goes up.** Placing someone too high costs a few extra conversations; placing them too
  low costs a surprise objection at a gate. A 3x3 grid adds nine strategies for little gain.
- **Overrides go upward only, with the reason written in `strategy`** (for example, "Override
  from Monitor: high impact, not yet aware"). Never override downward: if an M rating feels too
  high, re-rate it L and say why.
- **Sanity check.** The sponsor and every benefit owner must land in Manage Closely. If your
  ratings put them anywhere else, the ratings are wrong, not the rule.

**Helios placements** (from `assets/stakeholder-register-sample.csv`)

| Id | Stakeholder | Power | Interest | Quadrant | Why |
|---|---|---|---|---|---|
| S01 | Dana Okoro, VP Customer Operations (sponsor) | H | H | Manage Closely | Funds the project and chairs steering |
| S02 | Priya Nair, Head of Support Operations (benefit owner) | M | H | Manage Closely | No budget authority, but signs off requirements and UAT and owns the 50% benefit; M counts as High |
| S03 | Marcus Webb, Security lead | H | L | Keep Satisfied | Security sign-off can stop the pilot; engages only at gates |
| S04 | Hana Sato, Legal & Compliance | M | L | Keep Satisfied | Data-residency sign-off can delay the pilot |
| S05 | IdentityCo (identity-provider vendor) | M | M | Manage Closely | Delivers work package 1.3.1; Helios is one customer among many |
| S06 | Finance (budget holder) | H | L | Keep Satisfied | Releases funds; looks only at variances |
| S07 | Pilot customers (cohort of 200) | L | H | Keep Informed | First real users; cannot block |
| S08 | Support agents (60) | L | H | Keep Informed | Care intensely about their jobs; adoption runs through Priya Nair |
| S09 | Order management team | M | L | Keep Satisfied | Controls access to the order API |
| S10 | Marketing | L | L | Monitor | Involved only in the GA launch campaign |

Reading M as Low would have put Priya Nair — the benefit owner and priority one in the
engagement matrix — in Keep Informed, and IdentityCo in Monitor.

### Default strategy per quadrant

- **Manage Closely** — involve in decisions, consult before you commit, never surprise them.
  Helios: weekly 1:1 with Dana Okoro; Priya Nair co-leads the requirements workshops.
- **Keep Satisfied** — give exactly what they need through formal gates and concise updates;
  their interest spikes when something touches their area. Helios: Marcus Webb's threat-model
  review and security sign-off gate; Finance's monthly cost summary.
- **Keep Informed** — keep them in the loop and listen; they are advocates and a source of
  ground truth. Helios: pilot-customer onboarding, release notes and a feedback survey.
- **Monitor** — minimal, periodic contact and a trigger to re-rate. Helios: Marketing joins the
  GA launch distribution and is re-rated at M4.

The quadrant sets the default intensity; the engagement gap (current versus desired, see
`references/engagement-playbook.md`) adds the specific actions. A Keep Informed group that is
Resistant still needs deliberate work, not just a newsletter.

**Re-plot** whenever the project changes: a Monitor stakeholder becomes Keep Satisfied the
moment their system becomes a dependency.

## 3. Salience model (Mitchell, Agle & Wood, 1997)

Use when the grid cannot decide who comes first — competing claims, someone loud but powerless,
or someone powerful whose claim is doubtful. Rate three attributes yes or no:

- **Power** — can impose their will on the project.
- **Legitimacy** — has a rightful claim (contract, law, ownership, formal role, being affected).
- **Urgency** — the claim is time-sensitive and important to them now.

| Attributes | Class | Type | Treatment | Helios example |
|---|---|---|---|---|
| Power only | Latent | **Dormant** | Monitor; watch for the moment they gain a claim or urgency | IdentityCo's executive sponsor: can pull people off the account, but has no claim on Helios decisions until an escalation |
| Legitimacy only | Latent | **Discretionary** | Courtesy contact; no pressure to act | Marketing: a fair interest in launch messaging, no power over delivery, no urgency before GA |
| Urgency only | Latent | **Demanding** | Acknowledge quickly; do not let the noise displace priorities | A pilot customer pressing daily for live chat, which CR001 deferred to phase 2 |
| Power + legitimacy | Expectant | **Dominant** | Keep satisfied through formal channels and gates | Marcus Webb, Hana Sato and Finance in their normal state |
| Legitimacy + urgency | Expectant | **Dependent** | They rely on others' power: find them a powerful ally rather than deferring them | Support agents facing the 6-FTE redeployment before cutover; Priya Nair carries their case to steering |
| Power + urgency | Expectant | **Dangerous** | Can coerce: do not bargain informally; route the demand through change control and the sponsor | A senior manager outside the project insisting live chat goes into the pilot "or I escalate" |
| All three | Definitive | **Definitive** | Top priority — act immediately | Dana Okoro at every decision; Hana Sato once the data-residency sign-off falls due before the M4 pilot |

Salience moves. Hana Sato is **Dominant** (power and legitimacy) for most of the project; when
the data-residency sign-off becomes due before the M4 pilot she gains urgency and becomes
**Definitive** — act that week. The support agents are **Dependent**: legitimate and urgent but
without power, so the answer is a powerful sponsor for their concern, not a lower priority.

## 4. Stakeholder cube (Murray-Webster & Simon, 2006)

Use when you need a tactic, not just a priority. The cube has three binary axes:

- **Power** — influential / insignificant (apply the mapping rule: H and M are influential).
- **Interest** — active / passive: how actively they engage with the project.
- **Attitude** — backer / blocker: whether they support or oppose it. Judge the lean of a
  Neutral stakeholder from evidence; if you cannot tell, treat them as a potential blocker.

Interest and attitude are different questions: an active blocker and a passive backer need
opposite treatment, which is exactly what the cube separates.

| Power | Interest | Attitude | Type | Tactic | Helios example |
|---|---|---|---|---|---|
| Influential | Active | Backer | **Saviour** | Meet their needs; use them to unblock | Dana Okoro |
| Influential | Passive | Backer | **Sleeping giant** | Engage to awaken their support before you need it | Finance: funded the case, rarely engages |
| Influential | Active | Blocker | **Saboteur** | Engage 1:1 to understand and disarm; escalate only with evidence | None today; Priya Nair would become one if her concerns went unanswered — one reason she is priority one |
| Influential | Passive | Blocker | **Time bomb** | Find the concern and defuse it before they activate | Hana Sato while unaware of the data flows: a blocker-in-waiting at the M4 pilot gate |
| Insignificant | Active | Backer | **Friend** | Use as a confidant and sounding board | Pilot customers who volunteer for the usability rounds |
| Insignificant | Passive | Backer | **Acquaintance** | Keep informed | Marketing |
| Insignificant | Active | Blocker | **Irritant** | Engage to remove the cause of the irritation; do not dismiss it | Agents criticising the portal on the intranet |
| Insignificant | Passive | Blocker | **Tripwire** | Understand their needs so they do not trip you up | Team leads who quietly keep telling customers to phone in |

## 5. Choosing a technique

| Situation | Use |
|---|---|
| Triage, most projects, every register | Power/interest grid with the mapping rule |
| Competing or doubtful claims; "who really counts right now?" | Salience model |
| Choosing differentiated tactics for supporters versus opponents | Stakeholder cube |
| Highly affected but disengaged groups | Grid plus the upward impact override |
