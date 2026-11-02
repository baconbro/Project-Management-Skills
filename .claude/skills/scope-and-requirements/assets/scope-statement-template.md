# Project Scope Statement — <project name>

<Fill-in template. Replace every angle-bracket placeholder; delete guidance lines in
angle brackets once answered. A worked example is in scope-statement-sample.md.>

| Field | Value |
|---|---|
| **Project** | <project name> |
| **Sponsor** | <name, title> |
| **Project manager** | <name> |
| **Product owner / requirements lead** | <name> |
| **Version / date** | <v0.1> / <YYYY-MM-DD> |
| **Status** | <Draft / Baselined / Superseded by vN> |
| **Charter** | <charter version and approval date> |
| **Requirements (RTM)** | <path or link to the requirements traceability CSV> |
| **WBS** | <path or link to the WBS CSV, once scope is decomposed> |

## 1. Product scope description
<2-4 sentences: what the product, service or result is, who uses it, the journeys or
capabilities it covers, and the solution boundary — which systems it touches and which it
deliberately does not.>

## 2. Objectives and constraints this scope serves
Requirements cite these ids in the RTM `objective` column; a requirement that serves none
of them is gold-plating.

| Id | Objective or constraint | Measure or limit | Owner |
|---|---|---|---|
| OBJ-1 | <business objective, copied from the charter> | <metric, baseline, target, by when> | <benefit owner> |
| OBJ-2 | <second objective, if any> | <metric, baseline, target, by when> | <owner> |
| CON-1 | <budget constraint> | <approved budget and reserves> | <sponsor or budget holder> |
| CON-2 | <schedule constraint> | <fixed dates or milestones> | <sponsor> |
| CON-3 | <regulatory, policy, technical or contractual constraint> | <the rule that applies> | <approver> |

## 3. Deliverables and acceptance criteria
List product deliverables and project deliverables (plans, reports, training, handover).
Add WBS ids once `work-breakdown-structure` has decomposed the scope.

| # | Deliverable | WBS id | Description | Acceptance criteria | Acceptor | Requirements |
|---|---|---|---|---|---|---|
| D1 | <deliverable name, a noun> | <1.x.y> | <what it is and what it includes> | <verifiable pass condition> | <one named person> | <REQ ids> |
| D2 | <deliverable name> | <1.x.y> | <description> | <verifiable pass condition> | <named person> | <REQ ids> |
| D3 | <deliverable name> | <1.x.y> | <description> | <verifiable pass condition> | <named person> | <REQ ids> |

## 4. Acceptance process (scope validation)
- **Verification first:** <who runs quality control and which evidence is attached
  (test results, audit reports) before a deliverable is offered for acceptance>
- **Acceptance:** <who signs, in which forum (sprint review, gate review, steering), and
  within how many working days of the request>
- **Outcomes:** accept / accept with conditions (named, dated follow-ups) / reject with
  reasons tied to a criterion.
- **Rejections:** a failed criterion returns as a defect; a new or changed need is raised
  as a change request.
- **Final acceptance:** <who accepts the whole product, and at which milestone>

## 5. Exclusions (out of scope)
Copy every out-of-scope item from the charter and add any found during elicitation.

| Excluded item | Reason | Where it goes |
|---|---|---|
| <item the project will not deliver> | <why it is excluded> | <later phase / other project / not planned / pending CR id> |
| <item> | <reason> | <destination> |

## 6. Assumptions
| # | Assumption | Owner | Validate by | Impact if false |
|---|---|---|---|---|
| A1 | <statement believed true but not yet proven> | <name> | <date or milestone> | <what changes; risk id if logged> |
| A2 | <assumption> | <name> | <date or milestone> | <impact> |

## 7. Requirements summary
Full list: <RTM path or link>. Counts by type and MoSCoW priority:

| Type | Must | Should | Could | Won't | Total |
|---|---|---|---|---|---|
| Functional | <n> | <n> | <n> | <n> | <n> |
| Non-functional | <n> | <n> | <n> | <n> | <n> |
| Transition | <n> | <n> | <n> | <n> | <n> |
| **Total** | <n> | <n> | <n> | <n> | <n> |

Must share of estimated effort: <percent> (guide: about 60%, so Shoulds and Coulds can
absorb a slip). Coverage checks from the traceability reference: <all passed / list
open hits with owners>.

## 8. Scope change control
- **Scope baseline:** this statement <version>, the RTM as at <date>, and the WBS
  <version>, approved by <sponsor> on <date>.
- **Needs a change request:** adding or removing a deliverable or exclusion, changing a
  Must or an acceptance criterion, or anything that moves a CON-n limit. Route via
  <change process and board>; tolerances <PM / CCB / sponsor limits>.
- **Within the product owner's authority:** <what may be reordered or swapped inside a
  release without a change request, e.g. Should and Could items of equal size>.

## 9. Acceptance log
| When | Deliverable / REQ ids | Evidence | Acceptor | Decision | Conditions and follow-ups |
|---|---|---|---|---|---|
| <date or milestone> | <D# / REQ ids> | <test ids, reports> | <name> | <Accepted / Accepted with conditions / Rejected> | <what, who, by when> |

## 10. Approval
| Role | Name | Decision | Date |
|---|---|---|---|
| Sponsor | <name> | <Approved / Rejected> | <date> |
| Project manager | <name> | <Agreed> | <date> |
| Product owner or customer representative | <name> | <Agreed> | <date> |
| Benefit owner | <name> | <Agreed> | <date> |
