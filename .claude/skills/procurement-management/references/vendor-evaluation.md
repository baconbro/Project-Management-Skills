# Vendor Evaluation: Sourcing, Weighted Scoring and Due Diligence

A defensible selection fixes how vendors will be judged before any proposal arrives, applies
those rules the same way to every bidder, and tests whether the winner would still win if
reasonable people weighted things differently. The worked example is the sample Helios
project (a fictional customer self-service portal used throughout this catalog) choosing a
customer-identity vendor for work package 1.3.1 Identity / SSO integration; the three vendors
are fictional.

## 1. Pick the sourcing route
| Route | Ask the market for | Use when | Decided on |
|---|---|---|---|
| RFI (request for information) | Capabilities, approaches, indicative prices; no commitment | You do not yet know what the market offers or how to specify it | A shortlist for an RFP |
| RFQ (request for quotation) | A price for a fully specified item | The specification is complete and suppliers are interchangeable | Lowest compliant price |
| RFP (request for proposal) | A solution and a price | The need is known but solutions differ between vendors | Weighted quality and price |
| Direct award | Nothing; you negotiate with one supplier | Below the policy threshold, a call-off from an existing framework, or a documented sole-source reason | A justification signed by the delegated authority |

Thresholds come from your procurement policy and apply to the **whole-life value**
(including renewals and run costs), not the first invoice. Helios's (fictional) policy: a
purchase order on one quote below $10,000, three written quotes from $10,000 to $50,000, an
RFP above $50,000. IdentityCo's project cost was $28,000, but with three years' run cost the
commitment was $70,000, which put it in the RFP band, even though it was the incumbent.

## 2. Run the process
1. Write the pack: background, the statement of work, gates, criteria and weights, a price
   schedule asking for whole-life cost, standard terms, timeline and submission format.
2. Issue it to every bidder at the same time; answer clarification questions in writing and
   share the anonymised answers with all bidders.
3. Close at the deadline; most policies reject late bids.
4. Check gates, score quality, open price, moderate, take references and due diligence, hold
   demonstrations, optionally ask for a best and final offer (BAFO), recommend, award, and
   debrief the unsuccessful bidders.

Plan backward from the need-by date: an RFQ takes two to three weeks, a full RFP often six to
twelve. Helios ran a compressed RFP because sign-in requirements were already settled: issued
in week 1, proposals in week 3, decision in week 4, contract signed in week 5, sandbox due in
week 6 when 1.3.1 starts.

## 3. Build the scorecard before the market sees it
- **Gates first.** Pass/fail legal, security and regulatory musts. A vendor that fails a gate
  is out however cheap it is; do not score it.
- **Four to seven weighted criteria** summing to 100, signed off by the panel before the RFP
  is issued and never changed after proposals are opened.
- **A scoring guide per criterion**, anchored on this 0-5 scale:

| Score | Meaning |
|---|---|
| 0 | No response, or unacceptable |
| 1 | Major gaps; significant delivery risk |
| 2 | Partly meets; notable gaps or weak evidence |
| 3 | Meets the requirement, with evidence |
| 4 | Meets fully and adds some value |
| 5 | Exceeds, proven by a demonstration or a reference |

- **Price on whole-life cost** (project cost plus three to five years' run and exit cost):
  `price score = 5 x lowest compliant whole-life cost / this vendor's whole-life cost`.
  Keep price in a separate envelope until quality is scored so it cannot anchor the panel.

## 4. Score, moderate and total
Each evaluator scores alone and writes the evidence; a moderation meeting agrees one
consensus score per cell, discussing every spread of two points or more, and records why. Do
not simply average: an unexplained outlier is either a missed fact or a bias.
```
Weighted total (out of 100) = sum over criteria of (weight x score) / 5
```

## 5. Test the result: switching weights
Let M be the leader's raw margin over the runner-up, M = sum(w x s_leader) - sum(w x s_runner-up).
Changing one weight (and renormalising the others) produces a tie when:
```
Raise criterion k where the runner-up scores higher:  delta = M / (s_runner-up,k - s_leader,k)
Lower criterion k where the leader scores higher:     delta = M / (s_leader,k - s_runner-up,k)
```
If a plausible change of weight flips the result, or the margin is under about 5 points out
of 100, treat it as a close call: references, demonstrations, risk and a BAFO decide, and the
recommendation says so. A criterion that nearly flips the result is also where the winner is
weakest; write the protection into the contract.

## 6. References and due diligence
- **References:** at least two clients of similar size and scope. Ask whether it was on time,
  how problems were handled, whether the named people stayed, and whether they would buy again.
- **Financial health:** two years of accounts or a credit report; dependence on one client;
  for a small vendor, consider escrow or step-in rights.
- **Security and data:** a current ISO/IEC 27001 certificate or SOC 2 Type II report, a security
  questionnaire, data residency, sub-processors and breach history.
- **Legal and compliance:** professional-indemnity and cyber insurance, sanctions and
  anti-bribery checks, ownership of their components' IP, and signed conflict-of-interest
  declarations from every evaluator.
- **Capacity:** the named team is available on your dates.

## 7. Helios worked example
`assets/vendor-scorecard-sample.csv` holds the moderated scores. All three vendors passed the
gates (data residency, security assurance, SAML 2.0 / OpenID Connect support).

| Criterion (weight) | IdentityCo | SignInCo | AuthHostCo |
|---|---|---|---|
| Functional fit (25) | 4 | 5 | 3 |
| Integration effort (20) | 5 | 2 | 3 |
| Security and compliance (15) | 4 | 4 | 3 |
| Delivery support (15) | 2 | 4 | 3 |
| Whole-life cost (15): $70,000 / $95,000 / $66,000 | 4.7 | 3.5 | 5.0 |
| Viability and references (10) | 4 | 3 | 3 |
| **Weighted total** | **80.1** | **73.5** | **66.0** |

IdentityCo's three run years are priced at its quoted annual renewal of $14,000, not 12 x the
$1,200 monthly project-phase rate.

IdentityCo: (25x4 + 20x5 + 15x4 + 15x2 + 15x4.7 + 10x4) / 5 = 400.5 / 5 = 80.1. Its raw margin
over SignInCo is 400.5 - 367.5 = 33. Delivery support flips the result if raised by
33 / (4 - 2) = 16.5, from 15 to 31.5; integration effort flips it if lowered by
33 / (5 - 2) = 11, from 20 to 9. Neither is a plausible re-weighting, so the award stood, and
IdentityCo's weakest score (delivery support, the weakness behind risk R001) became contract terms:
a dated sandbox, a named integration engineer and delay and service credits. Had AuthHostCo
failed the data-residency gate, it would have been excluded before scoring despite being
cheapest.

## 8. Fairness and debrief
Give every bidder the same information, keep all contact inside the process, and log every
clarification. Debrief unsuccessful bidders on their own scores and the reasons, never on a
rival's price or proposal. Keep the scorecard, evidence and approvals with the contract file.
