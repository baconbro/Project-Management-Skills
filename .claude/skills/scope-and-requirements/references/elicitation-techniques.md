# Elicitation techniques — choosing, running and closing elicitation

Load this when you plan how to gather requirements or need a technique for a specific
stakeholder group. Elicitation is not "asking people what they want": stakeholders
describe symptoms, solutions and wishes, and the analyst turns them into needs. Examples
use the sample Helios project (a fictional customer self-service portal used throughout
this catalog).

## Plan elicitation from the stakeholder register
1. Start from the stakeholder register built in `stakeholder-management`. Every
   stakeholder with high power or high interest gets at least one elicitation activity;
   regulators and approvers (security, legal) get one even when their interest is low,
   because their requirements are often non-negotiable.
2. For each group, write the questions you need answered, pick one primary and one
   confirming technique from the table below, and name who facilitates and who records.
3. Timebox it. Elicitation fills whatever time it is given; set an end date tied to a
   milestone (Helios: Discovery complete at M1, work package 1.2.1 Requirements & user
   research, 3 weeks on the critical path).

## Technique selector
| Technique | Best for | Watch out for | Helios use |
|---|---|---|---|
| One-to-one interviews | Individual goals, pain points, sensitive topics | Leading questions; one loud voice | 12 customer interviews from the pilot cohort |
| Facilitated workshops | Agreeing needs and priorities across groups | Groupthink; HiPPO decisions | 3 workshops with Support Operations led by Ava Chen |
| Observation (job shadowing) | Tacit steps people forget to mention | Observer effect; small sample | Half a day shadowing agents handling reset calls |
| Document analysis | Policies, contracts, regulations, current process | Outdated documents | Data-residency policy, security standard, accessibility policy |
| Data analysis | Sizing the problem, finding the real top needs | Data quality; correlation is not cause | Ticket export: 40% resets and order status, top-50 questions |
| Surveys | Breadth and quantification after interviews | Low response; unvalidated questions | Survey of 200 pilot customers on preferred channels |
| Prototyping | Uncovering usability needs; "I'll know it when I see it" | Prototype mistaken for the product | Clickable prototype, two usability rounds (work package 1.2.2) |
| Interface analysis | Systems the product must talk to | Hidden integration rules | Identity provider and order system APIs with Ben Adeyemi |
| Story mapping | Ordering a backlog by user journey and release | Losing non-functional needs | Journey map for reset, order status and knowledge base |
| Focus groups | Reactions of a user segment to an idea | Dominant participants | Optional; not used on Helios |

## Running a session
- **Before:** send the purpose, the questions and any material 2 days ahead; confirm the
  decision-maker for priorities if the session will prioritise.
- **During:** ask about the current process and its pain before the future; ask "why"
  until you reach an objective (the 5 whys work here too); capture exact wording and the
  source; park solutions as "candidate designs", not requirements.
- **After:** write the needs up within 48 hours and play them back to the source for
  confirmation. An unconfirmed need is a hypothesis, not a requirement.

## Turning raw input into requirements
| Stakeholder said | Kind of input | Requirement candidate |
|---|---|---|
| "We need a chatbot." | Solution | Ask why: customers wait for simple answers. Need: customers find answers to the top-50 questions without contacting support |
| "It must be fast." | Vague quality | Performance NFR with a number, agreed with operations |
| "Customers hate calling about orders." | Pain point | A signed-in customer can see the current status of an order |
| "Legal will block anything that stores data abroad." | Constraint | Record as CON-3 data residency; derive the NFR that enforces it |

## Handling conflicts and gaps
- Conflicting requirements: trace both to their objective; the one that serves the
  objective or a binding constraint wins. Escalate the rest to the named decision-maker
  instead of averaging them into an ambiguous compromise.
- Absent voices: if a group was not consulted, write it down as an assumption with an
  owner. Helios risk R002 (undocumented requirements expand scope) is exactly this
  failure; covering every register entry is its main mitigation.
- Saturation: stop when two consecutive sessions with a group produce no new need.

## Closing elicitation
Elicitation is complete for the baseline when every high-power or high-interest
stakeholder has been covered and has confirmed the playback, every non-functional
category has a requirement or a recorded "none needed", and open questions have owners and
dates. Further needs found later are welcome, but they enter through `change-request`
or, inside an agile release goal, through the product owner's backlog.

## Anti-patterns
- Asking only the sponsor and the loudest managers, never the end users or the people
  who will support the product.
- Recording solutions verbatim as requirements.
- One giant workshop instead of techniques matched to each group.
- No playback, so misunderstandings surface in UAT.
- Elicitation that never ends because no milestone closes it.
