# Charter elements — definitions and examples

Load this when you need a precise definition of a charter element, a test for whether it is
written well, or an example of how to phrase it. Each heading maps to a section of
`assets/charter-template.md` (section numbers in brackets). The examples come from the sample
Helios project (a fictional customer self-service portal used throughout this catalog); its
complete charter is `assets/charter-sample.md`.

## What a charter is, and what it is not
A charter authorizes a project: it names the sponsor who funds it and the project manager who
runs it, says why it exists and what success means, and fences the work at a high level. It is
signed once at the end of initiation and changed only by re-approval.

| Document | Answers | Skill |
|---|---|---|
| Business case | Should we invest, and in which option? | `business-case` |
| **Charter** | Is the project authorized, who is accountable, what are its boundaries and stop rules? | `project-charter` |
| Scope statement | Exactly which deliverables, with which acceptance criteria and exclusions? | `scope-and-requirements` |
| Project management plan | How, when and for how much, against which baselines? | `project-planning` |
| Team charter (working agreement) | How does the team work together? | `resource-management` |

## Header: sponsor, project manager, business case, approach
- **Sponsor:** the single accountable executive who funds the project, owns the business
  outcome and decides beyond the PM's authority. One name, not a committee; someone with the
  budget to commit. *Example: "Sponsor: Dana Okoro, VP Customer Operations."*
- **Project manager:** the person accountable for delivery. The charter is what appoints them.
- **Business case:** the reference and approval of the case the charter rests on, or a
  recorded waiver (who waived it, when, why). *Example: "Helios business case v1.0: NPV
  $196,174 at 10%, payback 2.85 years; funding $450k–$550k."*
- **Delivery approach:** what is fixed and what may flex. *Example: "Hybrid — outcome, budget
  range, M1/M4/M6 and SSO fixed; features flex in two-week sprints."*

## Business need [1]
Why the project exists, in language a non-specialist understands, tied to a measurable pain or
opportunity. Test: could the sponsor say it to the board in one breath?
> *Example: "40% of support tickets are password resets and order-status questions that
> customers could answer themselves; handling them costs about $600k a year."*

## Objectives and success criteria [2]
Objectives are outcomes, not activities, written SMART (Specific, Measurable, Achievable,
Relevant, Time-bound). A success criterion is complete only with a metric, a baseline, a target,
a date and an owner who will measure it. Give each objective an id (OBJ-1) so requirements can
trace to it later.
> *Example: "OBJ-1: cut password-reset and order-status tickets by 50% within 6 months of
> launch, measured as monthly ticket volume against the 3-month pre-launch average; benefit
> owner Priya Nair."*
> *Weak: "Improve customer experience" — no metric, baseline, target or date.*

## Scope boundaries [3]
- **In scope:** outcomes and major deliverables, at the level a sponsor would recognise. Not
  requirements, not features, not tasks: the detailed scope statement is produced in planning
  with `scope-and-requirements`, which must cover every in-scope item listed here.
- **Out of scope:** explicit exclusions with a reason and a destination (later phase, another
  project, not planned). This list prevents the most expensive disputes.
> *Example: "Live chat with agents — out of scope: it moves contacts rather than deflecting
> them; phase 2 candidate."*

## High-level milestones [4]
A handful of checkpoints, each with what must be true when it is reached. Not a schedule:
dates and the critical path come from `project-schedule` in planning.
> *Example: "M1 Discovery complete; M4 MVP live to the 200 pilot customers; M6 general
> availability."*

## Budget range and funding [5]
An order-of-magnitude range, its basis and its funding source; say whether the range includes
reserves and what may be spent before the baseline exists. Precise costing and reserves are
set in planning with `cost-management`.
> *Example: "$450,000 – $550,000 including all reserves, from the Customer Operations
> investment budget; discovery only until the baseline is approved."* (Helios later sets BAC at
> $500,000 with a $25,000 management reserve above it: $525,000, inside the range.)

## Assumptions and constraints [6]
- **Assumptions:** things taken as true without proof. Give each an id, an owner, a
  validate-by date and the consequence if false; `project-planning` carries them into the
  assumptions log, and a dangerous one becomes a risk.
- **Constraints:** fixed limits on time, budget, resources, technology or compliance.
> *Example assumption: "A1: the existing identity provider supports customer logins without a
> license upgrade; Ben Adeyemi; validate by week 6 in the vendor sandbox."*
> *Example constraint: "CON-3: customer personal data stored and processed only in the
> approved region; Hana Sato."*

## Top risks [7]
Three to five threats, written cause → event → effect, rated High/Medium/Low, each with an
owner. No scoring or reserves here: identification, scoring and responses belong in
`risk-management` and `risk-register`.
> *Example: "The identity-provider integration is unproven and vendor lead times are long →
> SSO slips → the M4 pilot moves. Likelihood M, impact H, owner Sam Lee."*

## Key stakeholders [8]
The people and groups who approve, accept, fund or are affected, with what each approves or
provides. Not a full analysis: the register and power/interest map come from
`stakeholder-management`.
> *Example: "Marcus Webb, Security lead — accepts SSO and the security review."*

## Project manager authority and governance [9]
What the PM decides alone, the limits (money, days) above which they escalate, who decides
above that, and the governance cadence. Write limits as numbers; `change-management` later turns
them into change-control tolerances, so the two must agree.
> *Example: "Sam Lee decides team assignments, the order of work and changes up to $5,000 and
> 2 working days; the change control board decides above that within contingency; Dana Okoro
> decides HIGH-impact changes, management reserve and any move of M4 or M6."*

## Approval requirements [10]
Who approves or accepts each thing that must be approved: the charter, the baseline, each
deliverable, release decisions, project completion and business success. Separate *project
success* (delivered as agreed, accepted by the sponsor) from *business success* (the objective
met, declared by the benefit owner, often months after closure).
> *Example: "Each deliverable is accepted by the acceptor named in the scope statement;
> Dana Okoro signs the M4 and M6 go/no-go and final acceptance; Priya Nair declares OBJ-1 met
> 6 months after general availability."*

## Exit and cancellation criteria [10]
- **Normal exit:** the conditions under which the project is finished and handed over.
- **Cancellation criteria (stop triggers):** measurable conditions that force a continue,
  re-scope or stop decision, each with a threshold, a check point and a person who checks it.
  Only the sponsor (or the body that authorized the project) decides to stop; the PM's duty is
  to raise the trigger promptly with a recommendation. Good triggers come from the budget range
  ceiling, the business case switching values, a critical assumption, an early adoption signal
  and the benefit owner's continued commitment. Stopping on a trigger is governance working, not
  failure; `project-closure` runs a premature closure.
> *Example: "Fewer than 40 of the 200 pilot customers (20%) have completed a self-service
> journey 4 weeks after M4 → Dana Okoro decides continue, re-scope or stop."*
> *Example: "Forecast total cost above $550,000 with no recovery plan agreed at the next
> steering committee."*

## Sign-off [11]
The charter is authorized when the sponsor named in the header records a decision on a
specific version: name, decision, version and date (a signature, or an approval e-mail or
workflow record filed with the charter). "Approved with conditions" authorizes only what the
conditions do not block. A charter that is written but never signed off is a draft, not a
mandate: no hiring, contracts or spend beyond what the sponsor allowed in writing.
`references/charter-review.md` has the sign-off verification and the re-approval rules.

## Lightweight (agile) charter
For an agile team the same decisions fit on one page, often called a project brief or product
vision: the sponsor and product owner (with the product owner's decision rights), the outcome
objectives and how they are measured, guardrails instead of fixed scope (budget or team cost
per sprint, the latest date, compliance limits, the out-of-scope list), the first release goal,
and stop rules tied to outcomes (for example: if two consecutive releases do not move the
objective's metric, the sponsor reviews whether to continue). It still needs a sponsor's
signature.
