---
name: scope-and-requirements
description: >-
  Defines what the project will deliver: requirements with MoSCoW priorities and
  acceptance tests, the scope statement and exclusions, a traceability matrix, and formal
  acceptance of deliverables. Use when gathering requirements, writing a scope statement,
  or deciding whether something is in scope.
metadata:
  version: 1.0.0
  category: artifact
  phase: planning
  related: [project-planning, stakeholder-management, quality-management, change-management, project-charter, work-breakdown-structure]
license: MIT
---

# Scope and Requirements

## Overview
Scope and requirements work turns the charter's high-level boundaries into an agreed,
testable definition of what the project will deliver. It produces two artifacts. The
**scope statement** describes the product scope, the deliverables with their acceptance
criteria and a named acceptor, the explicit exclusions, the assumptions and the
constraints. The **requirements traceability matrix (RTM)** links every requirement
backward to the objective or constraint that justifies it and forward to the work package
that builds it and the test that proves it. Together with the WBS and WBS dictionary from
`work-breakdown-structure`, they form the scope baseline that `change-management`
protects. The skill also covers **scope validation**, the formal acceptance of finished
deliverables by the customer, which is a different act from quality control. Keep
*product scope* (the features and qualities of the result) apart from *project scope*
(the work needed to deliver it). The examples use the sample Helios project (a fictional
customer self-service portal used throughout this catalog): one objective (cut
password-reset and order-status tickets by 50% within 6 months of launch), 11
deliverables, and an RTM extract of 12 requirements.

## When to use this skill
- The user needs to gather, elicit, write or prioritise requirements, or to turn
  stakeholder wish lists into testable statements.
- The user wants a scope statement, or needs to settle what is in and out of scope before
  planning starts.
- The user wants to build or audit a requirements traceability matrix, or to find
  requirements with no work package or no test.
- A deliverable is finished and needs formal acceptance, or a stakeholder disputes
  whether something was ever in scope.
- Do NOT use this to authorize the project or set its first in/out-of-scope lists — use
  `project-charter`; this skill refines what the charter fixed.
- Do NOT use this to decompose the agreed scope into work packages — use
  `work-breakdown-structure`.
- Do NOT use this to write the Definition of Done or design quality gates — use
  `quality-management`.
- Do NOT use this to assess a new requirement after the baseline — raise it with
  `change-request`; to write or split user stories, use `agile-delivery`.

## Methodology fit
- **Waterfall:** elicit and analyse the full requirement set up front; baseline the scope
  statement and RTM with sponsor sign-off before design; keep the RTM current through
  system test and UAT; validate scope at each phase gate.
- **Agile:** the product goal is the objective and requirements emerge as backlog items
  refined just in time; the scope statement shrinks to a product vision, fixed
  constraints and explicit exclusions; the RTM stays at epic level and links to stories;
  the product owner validates scope at every sprint review by accepting the increment.
- **Hybrid (Helios):** baseline the deliverables, the compliance requirements and the
  Musts at M1; let Should and Could items flex inside the backlog as scope contingency;
  link RTM rows to stories (REQ-006 accessibility to HEL-142 and HEL-143); accept
  increments at sprint reviews and deliverables formally at the M4 pilot go/no-go and the
  M6 general-availability gates.

## Inputs you need
The approved charter (objectives, in-scope and out-of-scope lists, milestones, budget,
assumptions and constraints), the stakeholder register and engagement strategy from
`stakeholder-management`, the business case benefits if one exists, source documents
(policies, standards, contracts, current-process descriptions, operational data such as
ticket volumes), the delivery approach, the named decision-maker for priorities, and the
change-control tolerances from `change-management`. With no approved charter, run
`project-charter` first; with no stakeholder register, build one before eliciting.

## Workflow
1. **Plan elicitation from the stakeholder register.** Give every high-power or
   high-interest stakeholder, and every approver such as security or legal, at least one
   technique from the selector in `references/elicitation-techniques.md`, with a
   facilitator and an end milestone. Helios: 12 customer interviews, 3 Support Operations
   workshops, ticket analysis, agent shadowing, policy review and two prototype rounds,
   closed at M1. *Done: the plan covers every high-power or high-interest stakeholder and
   has an end date.*
2. **Elicit, then play back.** Run the sessions as described in "Running a session" in
   `references/elicitation-techniques.md`: record each need with its source, park
   solutions as candidate designs, and confirm the write-up with the source within 48
   hours. *Done: every need has a named source and a confirmed playback.*
3. **Write the requirements.** Classify each need as functional, non-functional or
   transition; record constraints and assumptions separately; make each requirement
   atomic, unambiguous, verifiable and solution-free with the nine checks in
   `references/requirements-quality.md`; probe every non-functional category. *Done:
   every requirement passes the nine checks and each non-functional category has a
   requirement or a recorded "none needed".*
4. **Prioritise with MoSCoW.** Apply the MoSCoW rules in
   `references/requirements-quality.md` with the named decision-maker (Helios: Ava Chen
   proposes, Dana Okoro confirms the Musts). Keep Musts near 60% of estimated effort and
   keep every Won't row with its reason and destination (Helios REQ-012 live chat,
   deferred to phase 2 by CR001). *Done: every requirement has a priority and the sponsor
   has confirmed the Musts.*
5. **Attach an acceptance test.** Fill the `acceptance_test` column of the RTM with a test
   id and a pass condition per requirement, worded with `quality-management` so it
   matches the acceptance criteria and the Definition of Done, and name one acceptor per
   deliverable. *Done: every Must has a pass/fail test and every deliverable a named
   acceptor.*
6. **Write the scope statement.** Copy `assets/scope-statement-template.md` and fill the
   product scope, objectives and constraints (OBJ-n and CON-n ids that the RTM cites),
   deliverables with acceptance criteria and acceptor, exclusions with where each one
   goes, assumptions with owners and validate-by dates, and the requirements summary.
   `assets/scope-statement-sample.md` shows the Helios version. *Done: every charter
   in-scope item maps to a deliverable, every charter exclusion is listed, and no
   placeholder remains.*
7. **Build the traceability matrix.** Copy `assets/requirements-traceability-template.csv`
   and record each requirement with its source and objective (backward) and its WBS id
   and acceptance test (forward); `assets/requirements-traceability-sample.csv` is the
   Helios extract. Once `work-breakdown-structure` has numbered the work packages, run the
   seven coverage checks in `references/traceability-and-scope-validation.md`. *Done: no
   in-scope row lacks an objective or WBS id, no Must lacks a test, and every product and
   transition work package traces to a requirement.*
8. **Baseline and hand off.** Get the sponsor's approval in section 10 of the scope
   statement (Helios: Dana Okoro at M1), then hand the deliverables to
   `work-breakdown-structure`, the acceptance tests to `quality-management` and the
   baseline to `change-management`. *Done: a signed, versioned scope statement and RTM,
   with the baseline date recorded in the project plan.*
9. **Control requirements during delivery.** Route every new or changed requirement,
   exclusion or acceptance criterion through `change-request`, following section 8 of the
   scope statement; after approval update the RTM row, the scope statement version and
   the WBS together. Helios: CR003 raised accessibility to WCAG 2.2 AA (scope statement
   v1.1); CR004's Spanish knowledge base stays excluded until it is decided. Update RTM
   statuses at every sprint review or status cycle. *Done: every post-baseline RTM change
   cites an approved CR or falls within the product owner's documented authority.*
10. **Validate scope.** When quality control has moved a deliverable's rows to `verified`,
    ask its named acceptor to accept it against its criteria, following "Running formal
    acceptance" in `references/traceability-and-scope-validation.md`. Record the decision
    in the acceptance log (section 9 of the scope statement) and set the rows to
    `accepted`; failed criteria return as defects and new needs go to `change-request`.
    *Done: every finished deliverable has an acceptance-log entry, and at closure every
    in-scope row is accepted or formally deferred.*

## Quality checklist
- [ ] Every high-power or high-interest stakeholder in the register was consulted and
      confirmed the playback of their needs.
- [ ] Every RTM row has an id, a type, a MoSCoW priority and a named source; every
      in-scope row also has an objective or constraint id.
- [ ] No requirement joins two needs with "and"/"or" or uses an ambiguity word (fast,
      user-friendly, secure) without a measurable threshold.
- [ ] Every Must has an acceptance test with a pass condition, and every deliverable has
      exactly one named acceptor.
- [ ] Musts are near 60% of estimated effort and the sponsor has confirmed them.
- [ ] Every charter out-of-scope item appears in the exclusions with a destination, and
      Won't rows stay in the RTM.
- [ ] Every assumption has an owner and a validate-by date.
- [ ] The RTM passes all seven coverage checks against the current WBS.
- [ ] The scope statement and RTM carry a version, a baseline date and the sponsor's
      approval.
- [ ] Every accepted deliverable has an acceptance-log entry naming the evidence, the
      acceptor and the decision.

## Anti-patterns
- Recording stakeholder solutions ("we need a chatbot") as requirements instead of the
  need behind them.
- A scope statement with no exclusions, so anything not refused counts as promised.
- Everything a Must: the priority carries no information and nothing can flex when a
  risk such as R001 (identity-provider integration slips) materializes.
- Non-functional requirements left implicit and discovered in UAT or at the security
  review.
- An RTM built after the fact for an audit, or one row per user story so the matrix is
  abandoned.
- Treating a passed test as acceptance (quality control is not scope validation), or
  accepting by silence.
- Accepting "small" requirements verbally after the baseline, which is how Helios risk
  R002 (undocumented requirements expand scope) materializes.
- Mixing constraints and assumptions into the requirement list, so nobody validates the
  assumptions.

## Resources
- `references/elicitation-techniques.md` — planning elicitation from the stakeholder
  register, a technique selector with Helios uses, running sessions, turning raw input
  into requirements, conflicts, and when to stop.
- `references/requirements-quality.md` — requirement levels and types, non-functional
  categories, the nine checks with failing and passing examples, ambiguity words, MoSCoW
  rules and alternatives.
- `references/traceability-and-scope-validation.md` — RTM columns and status lifecycle,
  the seven coverage checks, agile traceability, scope validation versus quality control,
  and running formal acceptance.
- `assets/scope-statement-template.md` — fill-in scope statement (`<placeholders>`):
  objectives and constraints, deliverables with acceptance criteria and acceptor,
  exclusions, assumptions, requirements summary, change control, acceptance log, approval.
- `assets/scope-statement-sample.md` — sample Helios scope statement as at the M4 pilot
  go/no-go review, including accepted, conditional and pending acceptances.
- `assets/requirements-traceability-template.csv` — fill-in RTM (`<placeholders>`) with
  the columns req_id, requirement, type, priority, source, objective, wbs_id,
  acceptance_test, status.
- `assets/requirements-traceability-sample.csv` — sample RTM: 12 Helios requirements of
  all three types and all four priorities, traced to the WBS ids in
  `.claude/skills/work-breakdown-structure/assets/wbs-sample.csv`.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-planning` — the planning phase that starts from this scope baseline and
  integrates it with the schedule, cost and resource baselines.
- `stakeholder-management` — supplies the register that drives elicitation, and takes
  back the stakeholders whose requests were excluded or deferred for follow-up
  engagement.
- `quality-management` — turns each requirement's acceptance test into acceptance
  criteria, the Definition of Done and quality gates; its quality control verifies a
  deliverable before scope validation here accepts it.
- `change-management` — protects the scope baseline produced here; every post-baseline
  change to a requirement, exclusion or acceptance criterion goes through its process.
- `project-charter` — provides the objectives, first in/out-of-scope lists, assumptions
  and constraints that the scope statement refines.
- `work-breakdown-structure` — decomposes the deliverables in the scope statement into
  work packages whose ids the RTM traces to.
