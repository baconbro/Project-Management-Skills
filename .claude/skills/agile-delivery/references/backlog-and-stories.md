# Backlog and user stories

The product backlog is the single, ordered list of everything the product might need. The
product owner owns the order; the developers own the sizes; anyone may propose an item. The
examples come from the sample Helios project (a fictional customer self-service portal used
throughout this catalog); `assets/product-backlog-sample.csv` holds its GA backlog.

## Structure and traceability
- **Epic** — a large outcome that spans several sprints ("customers check order status
  without calling support"). In a hybrid project, map each epic to one WBS work package.
- **Story** — a slice of that outcome one team can finish inside one sprint.
- **Task** — the team's own breakdown of a story during the sprint; never tracked by the PM.
- Keep the `wbs_id` column on every story. It is what lets `cost-management` earn value per
  work package and lets a reviewer trace a story back to the scope baseline (Helios: 1.3.2
  Self-service UI, 1.3.3 Knowledge base, 1.3.4 Reporting & analytics).

## Writing a user story
Format: **As a** type of user, **I want** a capability **so that** a benefit. Then follow the
three Cs: the **card** (the sentence), the **conversation** (the detail agreed at refinement),
and the **confirmation** (the acceptance criteria that prove it works).

| Weak | Strong (HEL-152) |
|---|---|
| "Error handling for order search" | As a customer, I want a clear message when an order number is not found so that I do not raise a ticket. |
| No criteria | Given an unknown order number, when I search, then I see what to check and a link to contact support. |

The benefit clause is not decoration: if nobody can state it, the story probably should not
be built. Write from the user's side; "As a developer, I want a database table" is a task.

## INVEST — the test for a good story
| Letter | Test question | Symptom when it fails |
|---|---|---|
| **I**ndependent | Can it be built and released without another open story? | Stories that are only done "together" |
| **N**egotiable | Is the how still open to discussion? | A story that is really a fixed specification |
| **V**aluable | Would a user or the business notice it shipped? | Layer stories: "build the API" |
| **E**stimable | Can the team size it with confidence? | Wild planning-poker spreads: run a spike |
| **S**mall | Does it fit comfortably in one sprint (8 points or less for Helios)? | Carry-over every sprint |
| **T**estable | Can an acceptance test prove it? | "Fast", "intuitive", "user-friendly" |

## Acceptance criteria versus the definition of done
- **Acceptance criteria** are specific to one story, written as Given / When / Then, three
  to seven per story, including the unhappy path (HEL-141: a failed provider response shows a
  retry message).
- **The definition of done** applies to every story: reviewed, tested, accessible, deployed
  to test. It is owned by `quality-management`; a story is done only when both are met.
- Non-functional needs belong in acceptance criteria when they are story-specific (HEL-150:
  95% of pages within 2 seconds at peak load) and in the definition of done when universal
  (WCAG 2.2 AA for every page after CR003).

## Definition of ready (entry criteria for sprint planning)
An item may enter a sprint only when:
- [ ] The story statement names the user and the benefit, and the product owner can explain it.
- [ ] Acceptance criteria are written and agreed, including the unhappy path.
- [ ] The team has sized it (planning poker in `estimation`) and it fits in one sprint.
- [ ] Dependencies on other teams, vendors, data, or environments are resolved or scheduled.
- [ ] UX design, if needed, is available; open questions are answered or turned into a spike.

Keep the definition of ready short and treat it as a conversation aid, not a stage gate. A
heavy one turns refinement into a mini waterfall. Its most valuable line is dependencies:
Helios HEL-141 (SSO sign-in) is sized and has criteria but stays `refined`, not `ready`,
until the vendor's production tenant is live (risk R001).

## Splitting stories
| Pattern | How | Helios example |
|---|---|---|
| Workflow steps | One story per step of the journey | Request reset link / set new password |
| Business-rule variations | Simple rule first, exceptions later | Orders shipped / orders split across carriers |
| Happy then unhappy path | Ship success, then error handling | Order found (HEL-133) / not found (HEL-152) |
| Data variations | One data source or type at a time | Email reset first, SMS reset later |
| Interface or platform | One channel first | Web first, text message later (HEL-173) |
| Defer quality levels | Make it work, then make it fast | Search results, then typo tolerance (HEL-134) |
| Spike | Timeboxed research that ends in a decision | Identity-provider token format before HEL-141 |

Never split by technical layer (UI story, API story, database story): no slice is
demonstrable at the review, and none delivers value on its own.

## Ordering the backlog
- Order by **value, risk, and dependencies**: high-value, high-risk items early so the
  team learns while there is still time to react (Helios put SSO sign-in at the top of Must).
- **Cost of delay** sharpens value: what does a sprint of delay lose? WSJF (weighted
  shortest job first) = cost of delay ÷ job size, for when many items compete.
- **MoSCoW** labels a release, not the backlog order: Must (the release fails without it),
  Should (important, with a workaround), Could (if capacity allows), Won't (not this
  release: Helios live chat, deferred to phase 2 by CR001). Keep Must at no more than about
  60% of the release's points so Should and Could absorb a bad sprint; Helios GA is 60 of
  100 open points.
- The file order is the order: keep the priority labels consistent with it, or
  `velocity_forecast.py --backlog` will warn that the two disagree.

## Backlog health (DEEP)
- **Detailed appropriately** — ready detail for the next two sprints only; epics further out.
- **Estimated** — everything in the next two sprints is sized; unsized items understate the
  remaining work (the forecast lists them, as it does Helios HEL-181).
- **Emergent** — new learning enters continuously; the product owner reorders, no change
  request needed unless a milestone, the budget, or committed Must scope moves.
- **Prioritized** — a strict order at the top; a rough one further down.
Refinement takes at most about 10% of the team's capacity, typically one session a week.
