# Make-or-Buy, Contract Types and Risk Allocation

Every external purchase answers three questions in order: should this be bought at all
(make-or-buy), which contract type fits how precisely the work can be defined, and which
clauses put each risk with the party best able to manage it. The examples use the sample
Helios project (a fictional customer self-service portal used throughout this catalog). This
guide is not legal advice: your procurement and legal functions own the final terms (Helios:
Hana Sato, Legal & Compliance).

## 1. Make-or-buy
Decide per work package or capability, never once for the whole project. A "buy" needs a
reason on at least one criterion below, not just a lower day rate.

| Criterion | Favours MAKE when... | Favours BUY when... |
|---|---|---|
| Strategic value | it differentiates the product or must be owned long term | it is a commodity a specialist does better |
| Capability and capacity | the skills exist and are free in the window (`resource-management`) | the skills are scarce or the team is already full |
| Whole-life cost | build + run + maintain is lower over 3-5 years | subscription + integration + vendor management + exit is lower |
| Time to need | the team can deliver by the need-by date | a vendor delivers sooner, including the procurement lead time |
| Risk and control | you need tight control of quality, schedule or data | a specialist can carry the delivery risk under a contract |
| IP, data and lock-in | you must own the IP or the data model | open standards keep the switching cost low |

Compare whole-life cost, not price:
```
Cost(make) = build effort x rate + run and maintenance x years + internal overheads
Cost(buy)  = purchase or subscription x years + integration effort + vendor management
             (often 5-10% of contract value in your own people's time) + exit / switching cost
Break-even volume, when one option has the higher fixed cost and the lower unit cost:
  Q* = (fixed cost of make - fixed cost of buy) / (unit cost of buy - unit cost of make)
```
Below Q* buy; above it make. Record the decision and its reason in the vendor register; a
make decision that later turns into a buy is a change, not a quiet substitution.

**Helios decisions (made in Discovery, M1):**

| Item | Decision | Reason |
|---|---|---|
| Customer sign-in, password reset, MFA (1.3.1) | Buy: extend the existing identity provider, IdentityCo, to customer logins | Commodity security capability; an in-house credential store is high risk; scope assumption A1 says the current licence tier covers customer logins |
| SSO integration with the portal (1.3.1) | Make: Ben Adeyemi and Carla Diaz build it; IdentityCo supplies sandbox, configuration and support | The decision tree in `risk-management` gives build an EMV of -$77k against -$90k for the vendor's widget |
| Cloud hosting | Buy: call-off under the existing enterprise agreement | No new sourcing; usage cost watched under risk R004 |
| Portal UI, knowledge base, reporting | Make | Core to the 50% ticket-reduction benefit; skills in the team |

Added in delivery: once CR003 was approved (2026-06-30), an independent WCAG 2.2 AA audit was
bought on a $4,000 purchase order (one quote, below the $10,000 threshold).

## 2. Contract types and who carries the cost risk
```
Buyer carries the cost risk <----------------------------------------> Seller carries the cost risk
 CPFF    CPAF    CPIF    T&M (capped)    Unit price    FP-EPA    FPIF    FFP
```

| Type | How the price works | Use when | Watch for |
|---|---|---|---|
| Firm fixed price (FFP) | One price for a defined scope | Scope, acceptance criteria and dates can be written precisely | The seller prices risk in; every unclear sentence returns as a priced change |
| Fixed price incentive fee (FPIF) | Target cost + target fee; overrun or underrun shared by a ratio, up to a ceiling price | Fixed scope with real cost uncertainty | The point of total assumption (below) |
| Fixed price with economic price adjustment (FP-EPA) | Fixed price indexed to inflation, exchange rate or a commodity | Multi-year deals | Pick a published index and a review date |
| Unit price | A fixed rate per unit consumed (user, transaction, GB) | Hosting, licences, transactions | The seller holds the price risk, you hold the volume risk |
| Time and materials (T&M) | Rate card x time + materials, ideally with a not-to-exceed cap | Discovery, staff augmentation, scope that cannot yet be defined | Open-ended spend; you manage productivity; add a cap and a burn report |
| Cost-plus fixed fee (CPFF) | Allowable costs + a fixed fee | Research or high uncertainty | Needs audit rights; little incentive to save |
| Cost-plus incentive fee (CPIF) | Costs + a fee that moves with a share ratio around a target cost, within a minimum and maximum fee | Uncertain work with a measurable cost target | Agree what counts as an allowable cost |
| Cost-plus award fee (CPAF) | Costs + a fee awarded against subjective criteria | Performance that is hard to measure objectively | Write the award plan up front |

## 3. Incentive arithmetic
**FPIF.** Target cost $100,000, target fee $10,000 (target price $110,000), share ratio 70/30
(buyer/seller), ceiling price $120,000.
```
Price paid              = min(ceiling, actual cost + target fee - seller share x (actual cost - target cost))
Point of total assumption (PTA) = (ceiling price - target price) / buyer share + target cost
                                = (120,000 - 110,000) / 0.70 + 100,000 = $114,286
```
Actual cost $95,000: price $106,500 (fee $11,500, the seller keeps 30% of the underrun).
Actual cost $112,000: price $118,400 (fee $6,400). Actual cost $118,000 is beyond the PTA, so
the price is capped at $120,000 and the fee falls to $2,000: above the PTA the seller pays
every extra dollar, and a seller near the PTA is a delivery risk to watch.

**CPIF.** Target cost $100,000, target fee $8,000, share 80/20, fee range $3,000-$12,000.
`Fee = target fee - seller share x (actual cost - target cost)`, clamped to the range. Actual
cost $90,000 gives a fee of $10,000 (total $100,000); $130,000 gives the minimum fee of $3,000
(total $133,000), because the formula's $2,000 is below the floor.

## 4. Agile and outcome-based contracts
- **Capped T&M per sprint or release:** pay for a stable team's time; the cap limits spend
  while your product owner decides what is built.
- **Fixed price per sprint (fixed capacity, variable scope):** price the team per sprint;
  scope flexes through the backlog. Add an exit right at any sprint boundary with a small
  early-exit fee, and allow swapping backlog items of equal size at no charge.
- **Target cost with pain/gain share:** an agreed target for a release; overruns and
  underruns are shared by a ratio, as in FPIF.
- **Fixed price per accepted increment:** payment follows increments accepted at the
  sprint review. Do not pay per story point; points are a team's sizing aid, not a currency,
  and they inflate once money depends on them.
The SOW still fixes the team and named roles, cadence, the Definition of Done, backlog
ownership (yours), acceptance at each sprint review, and exit and transition terms. Fixed
scope plus fixed price plus agile ceremonies is a waterfall contract in disguise.

## 5. Allocate risk through the terms
| Risk | Contract lever | Helios (IdentityCo) |
|---|---|---|
| Late delivery | Dated milestones; delay credits or liquidated damages (a genuine pre-estimate of loss); payment on acceptance | Sandbox due week 6; delay credit 5% of the late milestone's payment per week, capped at 15% |
| Poor quality | Acceptance criteria and a review period; warranty; retention | 10% retention released after a 4-week warranty |
| Service outage | Service level with credits and root-cause reports | Sandbox available 99.0% in business hours; P1 response within 1 business hour |
| Key person leaves | Named key-personnel clause; replacement needs your approval | Named integration engineer |
| Cost overrun | Contract type, cap, priced change control | Firm fixed price for the services |
| Data or security breach | Data-processing terms, residency, audit rights, breach notice, liability carve-outs | Data stays in the approved region (REQ-007); Marcus Webb's security review |
| Vendor failure or exit | Termination for convenience and for cause; transition assistance; data return; escrow | Data export and certified deletion at exit |
| Scope creep | Precise SOW and exclusions; change clause with priced amendments | Partner logins (CR002) excluded until a priced amendment |

Transferring a risk creates a secondary vendor-dependency risk; log it with `risk-management`.
Service credits rarely cover the real loss; they buy attention, not compensation, so keep
liability terms for loss that matters.

**Helios contract.** Firm fixed price $22,000 for IdentityCo's services, paid 30% when the
sandbox is connected, 40% when SSO works in test and 30% at production cut-over, of which 10%
is retained until the 4-week warranty ends. These mirror the weighted-milestone earning rule
for 1.3.1 in `cost-management`. Add a $6,000 customer-login subscription for M2-M6 at the
existing tier ($1,200 a month), giving $28,000 committed within the 1.3.1 budget.
