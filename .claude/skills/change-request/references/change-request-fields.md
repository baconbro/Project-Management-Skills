# Change Request Fields

Each change request is one self-contained record. These are the fields and how to fill
them so the request can be scored by `scripts/change_impact.py` and decided quickly.

## Identification

- **id** — short unique identifier, e.g. `CR001`. Keep it stable once assigned.
- **description** — what the change is, in plain language. One or two sentences a reader
  who was not in the room can understand.
- **raised by / date** — who proposed it and when.

## Justification

- **reason** — the business or technical driver. Why is this needed, and why now?
- **cost of doing nothing** — what happens if the change is rejected. This is what makes a
  change worth approving, not just the upside of accepting it.

## Impact (the three scored dimensions)

Rate each of scope, cost, and schedule on a 1-5 scale. Quantify in real units (dollars,
days, story points) in the description where you can; the 1-5 rating is what the scorer
uses, the units are what the decision-maker trusts.

| Score | Meaning |
| --- | --- |
| 1 | Negligible — absorbed without noticeable effect |
| 2 | Minor — small, contained effect |
| 3 | Moderate — noticeable; needs replanning of part of the work |
| 4 | Major — significant effect on the baseline |
| 5 | Severe — threatens the agreed scope, budget, or deadline |

- **scope_impact** — how much the agreed deliverables change.
- **cost_impact** — effect on budget.
- **schedule_impact** — effect on milestones and the end date.

## Decision

- **options** — at least two, always including "do nothing", with their trade-offs.
- **recommendation** — which option you advise and why.
- **decision** — approved / rejected / deferred.
- **decided by / date** — who made the call and when. Route through `change-management`
  for the board and the master change log.

## Scoring

The weighted score is the impact-weighted average of the three dimensions:

    score = (w_scope*scope + w_cost*cost + w_schedule*schedule)
            / (w_scope + w_cost + w_schedule)

With default weights of 1.0 each it is the plain average. Raise a dimension's weight when
that dimension matters most to this project — e.g. `--w-schedule 2` near a fixed launch
date. Priority bands default to HIGH (>= 4), MEDIUM (>= 2.5), LOW otherwise, tunable with
`--high` and `--medium`. Priority orders the queue; it does not make the decision.
