# Traceability and scope validation

Load this when you build or audit the requirements traceability matrix (RTM), or when a
deliverable is ready for formal acceptance. Examples use the sample Helios project (a
fictional customer self-service portal used throughout this catalog) and its RTM in
`assets/requirements-traceability-sample.csv`.

## What the RTM is for
The RTM links each requirement **backward** to why it exists and **forward** to the work
and the test that deliver and prove it.

```
objective / constraint  <-  source  <-  REQUIREMENT  ->  WBS work package  ->  acceptance test  ->  acceptance
     (OBJ-1, CON-3)       (who, when)     (REQ-004)          (1.3.3)              (UAT-04)          (Priya Nair)
```

Backward links stop gold-plating (nothing is built that no objective needs) and let you
cut scope rationally. Forward links stop gaps (nothing agreed is left unbuilt or untested)
and make acceptance and closure a lookup instead of an argument.

## Columns and conventions
| Column | Content | Rule |
|---|---|---|
| `req_id` | REQ-001, REQ-002 ... | Never reused or renumbered, even when a row is rejected |
| `requirement` | One atomic, testable statement | Passes the checks in `references/requirements-quality.md` |
| `type` | functional, non-functional, transition | Constraints and assumptions go in the scope statement |
| `priority` | Must, Should, Could, Won't | Agreed with the named decision-maker |
| `source` | Stakeholder and elicitation event or document | A person you can go back to |
| `objective` | OBJ-n or CON-n from the scope statement | The backward trace; blank only on Won't rows |
| `wbs_id` | Work package id(s), several separated by `;` | Must exist in the WBS; blank only on Won't rows |
| `acceptance_test` | Test id and its pass condition | Mandatory for Musts; written with `quality-management` |
| `status` | See lifecycle below | Updated at every sprint review or status cycle |

## Status lifecycle
`proposed` -> `approved` (in the baseline) -> `in build` -> `verified` (passed its test in
quality control) -> `accepted` (formally signed off by the acceptor). Side exits:
`deferred` (Won't this time, with where it went) and `rejected` (with the decision
reference). After the baseline, a row only enters `approved`, or leaves it for
`deferred` or `rejected`, through an approved change request; record the CR id in
`source`.

## Coverage checks (run at baseline and at every milestone)
Filter the CSV in a spreadsheet, or sort it, and fix every hit before sign-off.

| # | Check | A hit means | Fix |
|---|---|---|---|
| 1 | In-scope row (Must/Should/Could) with a blank `objective` | Possible gold-plating | Link it to an objective or constraint, or make it Won't |
| 2 | In-scope row with a blank `wbs_id` | Agreed work nobody planned | Add it to a work package, or re-plan the WBS |
| 3 | `wbs_id` not present in the WBS file | Broken link after a WBS change | Correct the id; re-run the WBS validator |
| 4 | Product or transition WBS leaf with no requirement | Work no requirement asks for | Add the missing requirement or remove the work |
| 5 | Must with a blank `acceptance_test` | Cannot be validated | Write the test with `quality-management` |
| 6 | Won't row with a `wbs_id` | Out-of-scope work still planned | Remove the link and the planned work |
| 7 | Row `accepted` that was never `verified` | Acceptance without evidence | Verify first, then re-accept |

Check 4 applies to product and transition work packages only. Project-management,
discovery and test work packages (Helios 1.1, 1.2.1, 1.2.2 and 1.4.1) exist because of
how the project is run and are justified by the plan, not by a product requirement.
For Helios the remaining leaves (1.3.1 to 1.3.4, 1.4.2, 1.5.1, 1.5.2) each trace to at
least one requirement in the sample RTM.

## Agile and hybrid traceability
Do not copy every user story into the RTM. Keep the RTM at requirement or epic level and
link down to backlog items: Helios REQ-003 (SSO sign-in) is delivered by backlog story
HEL-141, REQ-006 (WCAG 2.2 AA) by HEL-142 and HEL-143. Stories carry their own acceptance
criteria; the RTM row's test is the requirement-level proof (often the UAT scenario). In
pure agile the backlog itself is the trace, with the product goal as the objective.

## Scope validation versus quality control
| | Quality control | Scope validation |
|---|---|---|
| Question | Was it built right (meets its specification)? | Is it the right thing, and do we accept it? |
| Done by | Delivery team and QA (Helios: Frank Müller) | The customer or acceptor named per deliverable |
| Timing | Continuously, before validation | When a deliverable is verified and ready |
| Output | Verified deliverable, defects | Accepted deliverable or a rejection with reasons |
| RTM status | `verified` | `accepted` |

Quality control normally comes first: do not ask an acceptor to sign off something that
has not passed its own tests. Both can fail independently: a deliverable can pass every
test and still be rejected because the requirement was wrong. That is a change request,
not a defect.

## Running formal acceptance
1. **Entry:** the deliverable's RTM rows are `verified`, the evidence (test results,
   audit reports) is attached, and the acceptor was named in the scope statement.
2. **Review:** the acceptor checks the deliverable against its acceptance criteria and
   the RTM rows, not against new expectations.
3. **Decision:** accept, accept with conditions (named, dated follow-ups), or reject
   with reasons tied to a criterion.
4. **Record:** add a line to the acceptance log in the scope statement (date, acceptor,
   evidence, decision) and set the RTM rows to `accepted`.
5. **Rejections:** a failed criterion goes back as a defect; a new or changed need goes
   to `change-request`.

Helios acceptors (one per deliverable, named in the scope statement): Ava Chen accepts
sprint increments at each review; Priya Nair accepts the self-service journeys, knowledge
base, reporting, testing, training and handover; Marcus Webb accepts the SSO integration
and hardening and launch, whose evidence includes Hana Sato's data-residency and
accessibility sign-offs; Dana Okoro accepts the product at general availability (M6).
Specialists who sign evidence are not extra acceptors. A deliverable can be accepted
before its Should or Could rows are built; those rows are accepted separately later.
`project-closure` then confirms every in-scope row is `accepted` or formally `deferred`.

## Anti-patterns
- An RTM built at the end to satisfy an audit, so it traces nothing that mattered.
- One RTM row per user story, so the matrix drowns in detail and is abandoned.
- Acceptance by silence ("no complaints in two weeks").
- Treating a passed UAT as acceptance without the named acceptor's signature.
