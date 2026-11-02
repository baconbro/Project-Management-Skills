# Vendor Performance, Contract Change and Contract Closure

Signing the contract transfers some risk; it does not transfer accountability. The project
still answers for the vendor's dates, quality and cost, so a senior PM manages a vendor the
way they manage a workstream: onboarded on time, measured against what the contract says,
paid only for accepted work, changed only through control, and closed formally. The examples
use the sample Helios project (a fictional customer self-service portal used throughout this
catalog) and its identity-provider vendor, IdentityCo.

## 1. Onboard from award, not from day one
Access requests, security inductions and test environments have lead times that can exceed
the time between signature and the first milestone. Start `assets/vendor-onboarding-checklist.md`
the day the award is approved, with one named onboarding owner. Helios learned this the hard
way: nobody owned vendor onboarding, sandbox access was requested only after signature in
week 5, and the integration was delayed (lesson LL001 in `lessons-learned`).

## 2. Govern the relationship
| Forum | Helios participants | Cadence | Content |
|---|---|---|---|
| Working session | Ben Adeyemi and IdentityCo's integration engineer | Weekly | Progress to milestones, blockers, incidents, the shared tracker |
| Performance review | Sam Lee and IdentityCo's account manager | Monthly | Service-level and KPI report, acceptance and invoices, risks, changes, look-ahead |
| Executive review | Dana Okoro and IdentityCo's executive sponsor | At stage gates (M4, M6) or on escalation | Relationship health, unresolved escalations, renewal |

The weekly joint sync and the escalation path also appear in the project's communication plan
(`project-communication`) and in the vendor's row of the stakeholder register.

## 3. Measure what the contract says
| KPI | Measure | Typical target |
|---|---|---|
| Milestones on time | Contract milestones accepted by their due date | 100% |
| First-pass acceptance | Deliverables accepted without rework | 90% or more |
| Service availability | Uptime of the contracted service or environment in the agreed hours | As contracted (Helios sandbox 99.0% in business hours) |
| Response and resolution | Time to respond to and fix incidents by priority | As contracted (Helios P1 response within 1 business hour) |
| Key-personnel continuity | Named people still assigned | No unapproved change |
| Invoice accuracy | Invoices matching the order and the accepted deliverables | 100% |

Rate each contract Green, Amber or Red at the monthly review and record it in the vendor
register. Two consecutive Red months, or one missed critical milestone, triggers a formal
performance review with a written recovery plan.

## 4. Accept before you pay
- Inspect each deliverable against the SOW's acceptance criteria inside the review period.
  Watch for deemed-acceptance clauses: silence can count as acceptance.
- **Three-way match:** approve an invoice only when the purchase order, the acceptance record
  and the invoice agree. A milestone reached but not accepted is not payable.
- Approved invoices become actual cost in `cost-management`; contracted but unbilled amounts
  are commitments, and accepted but uninvoiced work is accrued so the forecast stays honest.

## 5. Change the contract the controlled way
- Any change to scope, price, dates or terms is decided by the project's change process
  (`change-request`) first, then recorded in a contract amendment signed by authorised
  signatories on both sides. No work starts on an unsigned change.
- Ask the vendor to price the change before the decision. Helios CR002 (extend SSO to partner
  logins) cannot be assessed until IdentityCo quotes an amendment to its SOW.
- Only the contract owner instructs the vendor. "Could you also just..." from a team member is
  a **constructive change**: the vendor can later claim it as extra work.

## 6. Under-performance, claims and disputes
Escalation ladder (written into the SOW, with time limits at each level):

| Level | Buyer | Vendor | Resolve within |
|---|---|---|---|
| 1 | Ben Adeyemi (tech lead) | Integration engineer | 2 business days |
| 2 | Sam Lee (project manager, contract owner) | Account manager | 5 business days |
| 3 | Dana Okoro (sponsor) | Executive sponsor | 10 business days |
| 4 | Legal (Hana Sato) | Legal | The contract's dispute-resolution clause: negotiation, mediation, then arbitration or the courts |

Remedies, in rising order: a documented concern; a recovery plan with dates; service or delay
credits; withholding payment for unaccepted deliverables (never for accepted ones); a formal
cure notice; partial termination or step-in; termination for cause, only after the exit plan
is ready. Keep a contemporaneous record (dates, notices, instructions, impacts, emails) and
meet every contractual notice period, because claims are won on records, not recollection.

**Helios by the end of month 3.** The sandbox went down (issue I001), blocking integration
testing; "SSO working in test" slipped two weeks, and 1.3.1 is the RED work package in the
earned-value snapshot (EV $45,000 against PV $60,000, AC $65,000). Sam Lee logged the outage
against the sandbox availability service level, claimed the delay credit on that milestone
(2 weeks x 5% of its $8,800 payment = $880), held the milestone payment until SSO is accepted in
test, and agreed a dated recovery plan with IdentityCo's account manager. The credit is small
against the $20,000 cost variance on 1.3.1, which is why the recovery plan, not the credit, is
the remedy that matters. Buying IdentityCo's premium support to crash the task (the $20,000
option in `project-schedule`) would be a contract change and goes through `change-request`.

## 7. Close the contract
Close every contract, including early terminations, with this checklist:
- [ ] Every deliverable accepted, or open items settled in a signed closure agreement.
- [ ] Final invoice matched and paid; retention released when the warranty ends.
- [ ] Claims, credits and disputes settled in writing.
- [ ] Access revoked (accounts, VPN, repositories, buildings); equipment returned.
- [ ] Data returned or its deletion certified; confidentiality obligations noted.
- [ ] Licences, subscriptions and warranties transferred to their operational owner.
- [ ] Contract file archived for the retention period your policy sets.
- [ ] Vendor performance review written (scores against the KPIs, would we buy again?).
- [ ] Procurement lessons recorded and the closure reported to `project-closure`.

Helios closes the IdentityCo services contract after the 4-week warranty that follows
general availability at M6; the customer-login subscription continues as an operating
contract owned by the operations owner named at handover.
