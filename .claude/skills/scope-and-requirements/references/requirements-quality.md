# Requirements quality — types, good requirements, MoSCoW

Load this when you write, review or prioritise requirements. It covers how requirements
are classified, the checks every requirement must pass before it is baselined, how to
prioritise with MoSCoW, and the defects that cause most scope disputes. Examples use the
sample Helios project (a fictional customer self-service portal used throughout this
catalog).

## Levels and types
Requirements cascade from why to what. Keep each level separate so you can trace down
and up.

| Level | Answers | Helios example | Where it lives |
|---|---|---|---|
| Business requirement | Why are we doing this? | Cut password-reset and order-status tickets by 50% within 6 months of launch | Charter objective OBJ-1 |
| Stakeholder requirement | What does a group need? | "Agents want customers to stop calling about order status" | Elicitation notes |
| Solution: functional | What must the product do? | A signed-in customer can see the current status of an order | RTM, type `functional` |
| Solution: non-functional | How well, under what conditions? | All journeys conform to WCAG 2.2 AA | RTM, type `non-functional` |
| Transition | What is needed to move from today to the new state? | All support agents trained before the pilot opens | RTM, type `transition` |

- **Constraints** (fixed limits such as budget, a deadline or a data-residency policy) and
  **assumptions** (things believed true but not yet proven) are not requirements. Record
  them in the scope statement, give constraints an id (CON-n) so requirements can cite
  them, and give each assumption an owner and a validate-by date.
- **Project requirements** (bi-weekly steering, weekly status reporting) describe how the
  project is run. They belong in the project management plan, not in the RTM.

## Non-functional categories to probe
Non-functional requirements are the ones stakeholders forget to say, so ask for each
category explicitly: performance (Helios: 95% of pages load within 2 seconds at the
forecast peak), availability, security (no open high or critical penetration-test
findings at launch), privacy and data residency, accessibility (WCAG 2.2 AA), usability,
scalability, supportability and monitoring, compliance and audit, and localisation. A
category with no requirement should be a decision ("none needed for the pilot"), not an
omission.

## The checks every requirement must pass
| Check | Test it by asking | Fails | Passes |
|---|---|---|---|
| Necessary | Which objective (OBJ-n) or constraint (CON-n) does it serve? | "The portal has an animated mascot" | Traces to OBJ-1 |
| Atomic | Does it contain one need only (no "and" or "or" joining needs)? | "Reset passwords and view orders" | Split into REQ-001 and REQ-002 |
| Unambiguous | Would two readers build the same thing? | "Order status is shown quickly" | "...within 2 seconds for 95% of requests" |
| Verifiable | Can someone other than the author pass or fail it? | "The knowledge base is helpful" | "Each top-50 question returns its article in the top three results" |
| Solution-free | Does it say what, not how? | "Use a React carousel for articles" | "Customers see up to five suggested articles" |
| Feasible | Can it be built within the constraints? | "100% uptime" | "99.5% monthly availability" |
| Consistent | Does it contradict another requirement or a constraint? | Store data in any region vs CON-3 | Stored only in the approved region |
| Traceable | Does it have an id, a source, a WBS id and an acceptance test? | An e-mail from a stakeholder | RTM row REQ-004 |
| Prioritised | Does it carry a MoSCoW priority agreed with the decision-maker? | Everything "high" | Must / Should / Could / Won't |

Words that signal ambiguity and must be replaced by a number or a state: fast, easy,
user-friendly, intuitive, flexible, robust, secure, seamless, modern, as appropriate,
etc., and/or, minimise, maximise, support (as a verb with no behaviour), TBC.

A useful sentence pattern: *When* trigger, *the* system *shall* response, *within*
measure. "When a customer requests a password reset for a registered e-mail address, the
portal shall send a reset link within 60 seconds." Agile teams write the same need as a
user story with acceptance criteria; the quality checks above still apply.

## MoSCoW prioritisation
- **Must** — without it the release is unusable, unsafe, illegal or misses the objective.
  Test: "if this is missing, do we still launch?" If yes, it is not a Must.
- **Should** — important and expected, but the release still works without it, perhaps
  with a workaround.
- **Could** — desirable; the first thing dropped when time or money runs short.
- **Won't (this time)** — explicitly agreed as out of this release. Keep the row with its
  reason and where it went (phase 2, another project, rejected) so it is not re-raised as
  new.

Rules that make MoSCoW work:
1. The decision-maker is named before the session (Helios: product owner Ava Chen
   proposes, sponsor Dana Okoro confirms the Musts).
2. Keep Musts to roughly 60% of the estimated effort (DSDM guidance). Shoulds and
   Coulds are the scope contingency that protects the date; with 90% Musts there is
   nothing left to flex when a risk such as R001 (identity-provider slip) materialises.
3. Prioritise against the objective, not against who shouts loudest. Each Must should
   name the objective or constraint it protects.
4. Revisit priorities at each milestone; moving a requirement between Must and Won't
   after the baseline is a change request.

Alternatives when MoSCoW stalls: value against effort on a 2x2, the Kano model (basic,
performance, delighter) for customer-facing features, or a 100-point allocation where
each stakeholder group spreads 100 points across the candidate requirements.

## Anti-patterns
- Writing the solution as the requirement, which removes the team's design options.
- Compound requirements that pass half their test and cannot be marked done.
- Non-functional requirements left implicit and discovered in UAT.
- Requirements with no source: nobody can say who to ask or why it matters.
- Everything a Must, so the priority carries no information.
- Treating the RTM as write-once: statuses and links not updated after a change request.
