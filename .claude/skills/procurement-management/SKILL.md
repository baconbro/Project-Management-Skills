---
name: procurement-management
description: >-
  Plans and runs project procurement: make-or-buy per work package, statements
  of work with deliverables, acceptance and service levels, sourcing by RFI,
  RFQ or RFP with pass/fail gates, weighted vendor scoring with a
  switching-weight check and due diligence, the contract type (fixed price,
  time and materials, cost-plus, agile) and its risk allocation, then vendor
  onboarding, performance, acceptance before payment, contract changes,
  disputes and closure. Use when the user wants to decide whether to build or
  buy, write a statement of work or an RFP, select a vendor, choose a contract
  type, manage a late or failing supplier, or close out a contract.
  Triggers: "procurement plan", "make or buy", "build or buy", "statement of
  work", "SOW", "RFP", "RFQ", "vendor selection", "vendor scorecard", "fixed
  price or time and materials", "supplier performance", "my vendor is late",
  "close the contract". For contract costs in the budget, use
  cost-management. Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: discipline
  phase: cross-cutting
  related: [project-planning, project-delivery, project-closure, stakeholder-management, risk-management, cost-management]
license: MIT
---

# Procurement Management

## Overview
Procurement management obtains the goods and services a project should not produce itself,
on terms that put each risk with the party best able to manage it. It runs as a lifecycle:
**plan** (make-or-buy, what to buy and by when), **define** (a statement of work with
deliverables, acceptance criteria and service levels), **source** (an RFI, RFQ or RFP judged
against gates and weights fixed in advance), **contract** (the contract type and the clauses
that allocate risk), **manage** (onboarding, performance against service levels, acceptance
before payment, contract changes, disputes) and **close** (final acceptance, payment, records
and a vendor review). A senior PM owns the project's side of every contract even when a
procurement or legal function signs it: the vendor delivers inside the project's baseline,
so its slips are the project's slips. The examples use the sample Helios project (a fictional
customer self-service portal used throughout this catalog), which buys customer sign-in from
its existing identity provider, IdentityCo, for work package 1.3.1 Identity / SSO integration
and builds the integration in-house. This skill is not legal advice: contract terms belong to
your legal and procurement functions (Helios: Hana Sato, Legal & Compliance).

## When to use this skill
- The user must decide whether to build a capability in-house or buy it, or what to buy for
  a work package.
- The user needs a statement of work, an RFI, RFQ or RFP pack, evaluation criteria or a
  vendor scorecard, or must justify a direct award.
- The user must choose between fixed price, time and materials, cost-plus or an agile
  contract, or wants to know who carries which risk under each.
- A vendor is late, missing service levels, disputing acceptance or asking for more money,
  or a contract needs to change.
- A contract must be closed: deliverables accepted, final payment, warranty, access and data.
- Do NOT use this to build the cost baseline or track earned value — use `cost-management`;
  this skill supplies the contract values and the approved invoices.
- Do NOT use this to identify and score vendor risks — use `risk-management`; this skill
  writes the chosen responses into contract terms.
- Do NOT use this to staff the project with your own people or check their capacity — use
  `resource-management`.
- Do NOT use this to decide whether a change to the baseline is approved — use
  `change-request`; this skill then amends the contract to match.

## Methodology fit
- **Waterfall:** make-or-buy and the procurement plan are part of the baseline; a full-scope
  SOW and a formal RFP; firm fixed price is common because scope is fixed early; acceptance
  against the SOW at each milestone; every change is a priced, signed amendment.
- **Agile:** buy a team's capacity and outcomes rather than a fixed specification: capped
  time and materials or a fixed price per sprint; the SOW fixes the team, cadence, Definition
  of Done, backlog ownership by your product owner and an exit right at any sprint boundary;
  acceptance happens at each sprint review and payment follows accepted increments.
- **Hybrid (Helios):** fixed price for the bounded vendor deliverables (IdentityCo's sandbox,
  configuration and go-live support, with dated milestones and credits) while the in-house
  team builds the integration in sprints; contract milestones become baseline milestones and
  the payment milestones mirror the earned-value milestones for 1.3.1.

## Inputs you need
The scope statement and WBS with acceptance criteria per work package
(`scope-and-requirements`, `work-breakdown-structure`), need-by dates from the schedule, the
budget per work package, the risk register, the organisation's procurement policy (approval
thresholds, approved suppliers or frameworks, delegated signing authority, standard terms),
the security, data-protection and accessibility standards that apply, and named contacts in
procurement, legal, security and finance. Without a scope statement, write one first: you
cannot buy what you cannot describe.

## Workflow
1. **Plan procurement and decide make-or-buy.** Walk the WBS and list every work package
   that might be bought (services, licences, hosting, audits, contractors). Decide each one
   on the six criteria and the whole-life cost comparison in
   `references/contract-types-and-risk.md`, not on day rates. For each buy, record the
   sourcing route your policy thresholds require (applied to whole-life value), the need-by
   date and the lead time, and log it as `planned` in `assets/vendor-register-template.csv`.
   Helios: buy customer sign-in on the existing identity provider, build the integration
   in-house (the `risk-management` decision tree favours build at an EMV of -$77k against
   -$90k for the vendor's widget), call off hosting under the enterprise agreement, and buy a
   $4,000 accessibility audit for CR003 on a purchase order. *Done: every candidate work
   package has a recorded decision and reason, and every buy has a route, an owner and a
   need-by date in the register.*
2. **Write the statement of work.** Fill `assets/statement-of-work-template.md`: objectives,
   in-scope and excluded work, deliverables each with an acceptance criterion, a named
   acceptor and a due date, service levels with credits, both parties' obligations (what you
   must provide, and by when), governance and the escalation ladder, price and payment tied
   to accepted deliverables, change control, security and data terms, and exit. Reuse the
   acceptance criteria from the scope statement rather than inventing new ones. *Done: a
   reviewer outside the project can tell what the vendor must deliver, how it will be
   accepted and what it will be paid, and no placeholder remains.*
3. **Choose the contract type and allocate the risk.** Match the type to how precisely the
   scope can be written, using the contract-type table and risk spectrum in
   `references/contract-types-and-risk.md` (and its target-price, share-ratio and point of
   total assumption arithmetic for incentive contracts). Turn each vendor risk in the
   register into a clause: delay credits, retention, key personnel, data terms, exit
   assistance. Have legal review the terms. Helios: firm fixed price of $22,000 for
   IdentityCo's services plus a $6,000 subscription at the existing tier (scope assumption
   A1), payments of 30/40/30% on the 1.3.1 milestones with 10% retained through a 4-week
   warranty, and delay credits that make risk R001's transfer response enforceable. *Done:
   the type is justified in one sentence and every open vendor risk maps to a contract term
   or an accepted residual.*
4. **Fix gates and weighted criteria before going to market.** Pick RFI, RFQ, RFP or a
   justified direct award with the route table in `references/vendor-evaluation.md`. In
   `assets/vendor-scorecard-template.csv` list the pass/fail gates (legal, security, data
   residency) and four to seven weighted criteria summing to 100, each with a 0-5 scoring
   guide; price is scored on whole-life cost. The panel signs off the weights before the pack
   is issued. *Done: gates, weights and scoring guides are approved and dated before any
   proposal is opened.*
5. **Evaluate, test and select.** Check gates first and drop any vendor that fails one, however
   cheap. Evaluators score alone, then moderate to a consensus with evidence; compute weighted
   totals (sum of weight x score / 5), run the switching-weight sensitivity, take references
   and complete due diligence (financial health, security assurance, data protection,
   insurance, conflicts of interest), all as set out in `references/vendor-evaluation.md`.
   `assets/vendor-scorecard-sample.csv` is the Helios evaluation: IdentityCo 80.1, SignInCo
   73.5, AuthHostCo 66.0; the result flips only if integration effort fell from 20 to 9 or
   delivery support rose from 15 to 31.5, so the award stood, and IdentityCo's weak delivery
   support became contract terms. *Done: a recommendation names the winner, the margin, the
   closest flip and the due-diligence results, and the delegated authority has approved it.*
6. **Negotiate, award and commit.** Negotiate price, payment milestones, service levels and
   credits, named key personnel and exit terms; the authorised signatory signs before any
   work starts. Debrief unsuccessful bidders on their own scores. Pass the contract value to
   `cost-management` as a commitment, the vendor's contacts and escalation path to
   `stakeholder-management`, contract milestones to the schedule, and residual vendor risks
   to `risk-management`; set the vendor's row in your copy of
   `assets/vendor-register-template.csv` to `awarded`. *Done: a signed contract and a
   purchase order exist, and the cost baseline, schedule, stakeholder register and risk
   register all reflect them.*
7. **Onboard the vendor.** Name one onboarding owner and work through
   `assets/vendor-onboarding-checklist.md` from the day of award: contracts and PO, named
   contacts and the escalation ladder, access and environment lead times, security induction,
   ways of working and a first checkpoint. Helios learned this the hard way: nobody owned
   onboarding, the sandbox was requested late and the integration slipped (lesson LL001 in
   `lessons-learned`). *Done: every checklist item is ticked or has an owner and a date before
   the first vendor milestone falls due.*
8. **Manage performance, acceptance, change and disputes.** Run the cadence and KPIs in
   `references/vendor-performance-and-closure.md`: a weekly working session, a monthly
   performance review against the service levels, executive reviews at stage gates. Accept
   each deliverable against the SOW before approving its invoice (three-way match of order,
   acceptance and invoice) and pass approved invoices to `cost-management` as actual cost.
   Route every change to scope, price or dates through `change-request` first, then a signed
   amendment; only the contract owner instructs the vendor. Escalate under-performance up the
   ladder and apply remedies in rising order, updating the vendor register monthly. Helios,
   end of month 3 (`assets/vendor-register-sample.csv`): a sandbox outage (issue I001) put
   "SSO working in test" two weeks late and 1.3.1 RED in the earned-value snapshot (EV
   $45,000 against PV $60,000); Sam Lee claimed the $880 delay credit, held that milestone
   payment until acceptance and agreed a dated recovery plan with IdentityCo. *Done: every
   active contract has a current RAG, every paid invoice matches an accepted deliverable,
   and every amendment cites an approved change request.*
9. **Close the contract.** Confirm every deliverable is accepted or settled in writing,
   release retention when the warranty ends, settle claims and credits, revoke access,
   recover or certify deletion of data, transfer subscriptions and warranties to their
   operational owner, archive the file and write a vendor performance review, following the
   closure checklist in `references/vendor-performance-and-closure.md`; report the result to
   `project-closure`. Helios closes IdentityCo's services contract after the 4-week warranty
   that follows general availability at M6. *Done: the register row reads `closed` with the
   closure date, final cost and performance rating, and no invoice, claim or access right is
   left open.*

## Quality checklist
- [ ] Every bought work package has a recorded make-or-buy reason and a whole-life cost
      comparison.
- [ ] Every SOW deliverable has an acceptance criterion, a named acceptor and a due date, and
      every payment is tied to an accepted deliverable.
- [ ] The SOW lists the buyer's own obligations with owners and dates.
- [ ] The contract type is justified, and each open vendor risk maps to a contract term or an
      accepted residual.
- [ ] Gates, weights (summing to 100) and scoring guides were approved and dated before any
      proposal was opened.
- [ ] The weighted totals reproduce from the scorecard, and the recommendation states the
      margin, the closest flip and the due-diligence results.
- [ ] An authorised signatory signed before work started, and the contract value is recorded
      as a commitment in the cost baseline.
- [ ] The onboarding checklist has one named owner and was started on the day of award.
- [ ] Every paid invoice matches an accepted deliverable, and every amendment cites an
      approved change request.
- [ ] Every contract is in the vendor register with an owner, value, dates, service levels and
      a current status; closed rows record final acceptance, final payment, revoked access,
      data disposition and a performance rating.

## Anti-patterns
- Choosing on day rate alone, ignoring integration effort, vendor management and exit cost.
- Fixed price over a vague SOW: every unclear sentence comes back as a priced change.
- Changing the weights after reading the proposals so a preferred vendor wins.
- Opening price before quality is scored, so the cheapest bid anchors the panel.
- Letting work start on a handshake or a letter of intent; the leverage goes before the
  contract is signed.
- Paying for milestones that were reached but never accepted.
- Team members instructing the vendor informally ("could you also add..."), creating
  constructive changes and later claims.
- Treating service credits as compensation: they buy attention, not recovery of the loss.
- No named onboarding owner, so access and sandboxes arrive after the vendor's start date
  (Helios lesson LL001).
- Closing the project while contracts, retention and vendor access stay open.

## Resources
- `references/contract-types-and-risk.md` — make-or-buy criteria and whole-life cost, contract
  types on the risk spectrum, FPIF/CPIF arithmetic, agile contracts, risk-allocating clauses.
- `references/vendor-evaluation.md` — sourcing routes and thresholds, the RFP process, gates,
  anchored scoring, whole-life price score, switching weights, due diligence, Helios example.
- `references/vendor-performance-and-closure.md` — onboarding, governance cadence, KPIs,
  acceptance before payment, contract change, escalation and remedies, closure checklist.
- `assets/statement-of-work-template.md` — fill-in statement of work (`<placeholders>`).
- `assets/vendor-scorecard-template.csv` — fill-in scorecard (`<placeholders>`): criterion,
  weight, vendor_a, vendor_b, vendor_c, scoring_basis, with gates, totals and rank.
- `assets/vendor-scorecard-sample.csv` — sample Helios identity-provider evaluation of three
  fictional vendors.
- `assets/vendor-register-template.csv` — fill-in register (`<placeholders>`) of every
  contract from planned to closed.
- `assets/vendor-register-sample.csv` — sample Helios register at the end of month 3.
- `assets/vendor-onboarding-checklist.md` — fill-in onboarding checklist (`<placeholders>`)
  with one named owner, started on the day of award.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-planning` — runs this skill's make-or-buy and procurement plan as its procurement
  step, and takes back vendor lead times, contract milestones and committed costs for the
  integrated baseline.
- `project-delivery` — the monitor-and-control cycle in which vendor reviews, acceptance,
  contract changes and escalations run; vendor issues such as Helios I001 land in its issue
  log.
- `project-closure` — receives each closed contract (final acceptance, final payment,
  released retention, revoked access, vendor review) as part of administrative closure.
- `stakeholder-management` — records each vendor as a stakeholder with its engagement target,
  named contacts and escalation path (Helios: IdentityCo, S05).
- `risk-management` — supplies the vendor and contract risks and the chosen responses that
  this skill writes into contract terms, and takes back the secondary vendor-dependency risk
  each transfer creates.
- `cost-management` — takes contract values as commitments in the cost baseline and approved
  invoices as actual cost; vendor price changes flow into its estimate at completion.
