# Charter elements — definitions and examples

Load this when you need a precise definition of a charter element or an example of
how to phrase it. Every element below maps to a section of `assets/charter-template.md`.

Examples use a running sample project: **Helios**, a customer self-service portal.

## Sponsor
The single accountable executive who authorizes and funds the project and owns the
business outcome. One name, not a committee.
> *Example: "Sponsor: Dana Okoro, VP Customer Operations."*

## Project manager
The person accountable for delivery, with a stated level of authority (what they can
decide alone vs. what needs sponsor approval).
> *Example: "PM: Sam Lee. Authority: may reallocate within the approved budget; budget increases > 10% require sponsor approval."*

## Business need / problem statement
Why the project exists, in plain language a non-specialist understands. Tie it to a
measurable pain or opportunity.
> *Example: "40% of support tickets are password resets and order-status questions that customers could self-serve. This costs ~$600k/year in handling time."*

## Objectives and success criteria
Objectives are SMART outcomes (Specific, Measurable, Achievable, Relevant, Time-bound).
Success criteria state how each objective will be measured.
> *Example objective: "Cut password-reset and order-status tickets by 50% within 6 months of launch."*
> *Example success criterion: "Measured by monthly ticket volume in the support system vs. the 3-month pre-launch baseline."*

## Scope boundaries
- **In scope:** the outcomes and deliverables the project will produce.
- **Out of scope:** explicitly excluded items. This list resolves the most expensive disputes later.
> *Example out-of-scope: "Native mobile apps, live chat, and back-office CRM changes are out of scope for this release."*

## High-level milestones
A handful of dated checkpoints, not a detailed schedule. Detailed scheduling is `project-schedule`.
> *Example: "Discovery complete — M1; MVP portal live to pilot group — M4; General availability — M6."*

## Budget range
An order-of-magnitude figure or range, with the basis of the estimate. Precise costing is `cost-management`.
> *Example: "$450k-$550k, funded from the FY operations improvement budget."*

## Assumptions and constraints
- **Assumptions:** things taken as true for planning (validate them later).
- **Constraints:** fixed limits on time, budget, resources, technology, or compliance.
> *Example assumption: "The existing identity provider can support customer logins without a license upgrade."*
> *Example constraint: "Must comply with the company's data-residency policy; launch must not slip past Q4."*

## Top risks
The few biggest threats, named qualitatively. Full identification, scoring, and response
planning belong in `risk-management` and `risk-register`.
> *Example: "Identity-provider integration is unproven; vendor lead times are long."*

## Key stakeholders
The groups and individuals who must be informed or engaged. A full power/interest
analysis belongs in `stakeholder-management`.
> *Example: "Support operations, customers (pilot cohort), security, legal/compliance, marketing."*

## Sign-off
The charter is authorized when the sponsor approves it. Record the name and date.
A charter that is written but never signed off is a draft, not a mandate.
