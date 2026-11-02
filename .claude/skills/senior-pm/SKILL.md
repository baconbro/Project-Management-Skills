---
name: senior-pm
description: >-
  Acts as the front door to the project-management catalog: triages a project's
  lifecycle stage and how it is doing against its baseline on scope, schedule,
  cost and risk, records it in a one-table project-state
  canvas, recommends waterfall, agile or hybrid, and routes by stage or symptom to at most
  two specialist skills with a first action. Holds the PM glossary, a routing map of all
  27 skills and the worked example. Use when the user is unsure where to start, asks for
  general project-management help, describes a project or a symptom without naming an
  artifact, asks whether a project is on track, or wants a methodology recommendation.
  Triggers: "help me manage a project", "where do I start", "is my project on track",
  "what should I do next", "which approach should I use", "waterfall or agile", "triage
  my project", "health check on my project", "what does this PM term mean". For running a
  baselined project day to day, use project-delivery. Works for waterfall, agile, and
  hybrid projects.
metadata:
  version: 1.1.0
  category: orchestrator
  phase: cross-cutting
  related: [project-initiation, project-planning, project-delivery, project-closure, risk-management, agile-delivery]
license: MIT
---

# Senior PM

## Overview
This skill is the triage desk for the whole catalog. It works out what stage a project is
in, reads its health against the baseline (or says plainly that there is no baseline to be
on track against), suggests how the work should be run, and sends the user to the specialist
skill that does the work. It does little itself: its value is asking the right questions,
recording the answers in one small canvas the user can bring back next time, and routing
well. Examples use the sample Helios project (a fictional customer self-service portal used
throughout this catalog); `references/helios-walkthrough.md` follows it from idea to closure
and is the catalog's worked example. Never treat Helios as the user's project.

## When to use this skill
- The user describes a project or a problem but names no artifact or phase.
- The user describes a symptom: "we are always late", "my vendor is late", "nobody knows who
  decides", "scope keeps growing", "we go live next week".
- The user asks "where do I start", "what should I do next" or "is my project on track".
- The user wants a methodology recommendation, a PM term explained, or to see how the whole
  lifecycle fits together.
- Do NOT use this once the stage and the need are clear: go straight to the phase skill
  (`project-initiation`, `project-planning`, `project-delivery`, `project-closure`) or the
  artifact skill named in `references/routing-map.md`.
- Do NOT use this to write the status report itself — use `status-report`; this skill only
  reads health well enough to route.

## Methodology fit
- **Waterfall:** recommend when scope is well understood, change is costly, and stage gates
  and sign-offs matter (regulated work, construction, fixed-price contracts). Health is read
  from milestone dates and earned value (CPI/SPI) against the approved baseline.
- **Agile:** recommend when requirements are uncertain, feedback changes direction, and the
  team can release in small increments. Health is read from the sprint goal hit rate and
  the velocity forecast against the release date (`agile-delivery`).
- **Hybrid:** recommend when outcomes, budget and key dates are fixed but delivery can be
  iterative — the most common real-world case, typically a customer-facing product with a
  committed launch date (Helios is one). Health is read both ways: milestones and earned
  value at the top, velocity inside the sprints.
- `references/methodology-selection.md` holds the decision checklist and the skill sequence
  for each approach.

## Inputs you need
A short description of the project and the outcome it is for; what exists today (business
case, charter, scope statement, plan, approved baseline, work in progress, accepted
deliverable); if the project is running, its latest position against the baseline (planned
versus forecast milestone dates, spend versus budget or PV/EV/AC, velocity and points left,
the top risks, open escalations); the single biggest problem or decision now; and any hard
constraint (deadline, budget, compliance). If the user brings a canvas from an earlier
conversation, start from it and ask only what changed. If the user cannot describe the
desired outcome at all, start at `project-initiation`.

## Workflow
1. **Run the intake and fill the canvas.** Ask, in order: (a) What outcome are you after?
   (b) What exists today? (c) If work is running: where do you stand against the baseline —
   scope (approved and pending changes), schedule (milestones hit or slipped, forecast finish
   versus the deadline), cost (spend versus budget, CPI/SPI or EAC if known), risk (top risk,
   any HIGH risk or issue without a response)? (d) What is the biggest problem or decision
   right now? (e) Any fixed deadline, budget or compliance constraint? Record the answers in
   this canvas (`assets/project-state-template.md` is the full version with the artifact
   checklist; `assets/project-state-sample.md` is Helios at month 3):

   | Stage | Baseline exists? (scope / schedule / cost) | RAG (overall + worst dimension) | Top risk or issue | Next decision (who, by when) |
   |---|---|---|---|---|
   | `<idea / initiation / planning / delivery / closure>` | `<approved / draft / none>` for each | `<GREEN / AMBER / RED / unknown>` | `<one line, with owner>` | `<decision, decider, date>` |

   *Done: every cell is filled or marked "unknown" with the question that would fill it.*
2. **Diagnose the stage.** No approved business case or charter → initiation; charter but no
   approved baseline → planning; baseline approved and work executing → delivery;
   deliverables accepted, go-live done or work stopping → closure. A project that is running
   without a baseline is in delivery with "no baseline" as its top gap (`project-delivery`
   builds a one-day interim baseline for it). Tick the stage's
   artifacts in the template's checklist; each missing one is a gap. *Done: one stage named,
   with the evidence that placed it and the missing artifacts listed.*
3. **Read health against the baseline.** Rate scope, schedule, cost and risk separately with
   the `status-report` thresholds: GREEN when CPI and SPI are both ≥ 0.95, RED when either is
   < 0.85, else AMBER; scope AMBER while change requests are pending; risk RED when a HIGH
   risk has no owner or response. Roll up no greener than the worst material dimension. If
   the user has PV/EV/AC, run
   `python .claude/skills/cost-management/scripts/health_check.py <evm.csv>`
   (Helios sample: `python .claude/skills/cost-management/scripts/health_check.py .claude/skills/cost-management/assets/evm-snapshot.csv`
   → CPI 0.93, SPI 0.92, AMBER). If the team runs sprints, run
   `python .claude/skills/agile-delivery/scripts/velocity_forecast.py <sprint-history.csv> --sprints-left <N>`
   for the release outlook. With no numbers, use a named proxy (share of milestones met on
   date). With no baseline, the answer to "is it on track" is "unknown — there is nothing to
   be on track against": that is the top gap. *Done: a one-line RAG per dimension and overall,
   with the evidence and the top gap named.*
4. **Recommend a methodology** with the checklist in `references/methodology-selection.md`.
   *Done: waterfall, agile or hybrid recommended with the one or two signals that drove it.*
5. **Route by stage or symptom.** Use the stage gaps from step 2 or the symptom table below;
   `references/routing-map.md` covers all 27 skills, tie-breaks for shared triggers and
   multi-skill sequences. Name at most two skills, each with its first action and the
   artifact it should leave behind.

   | The user says... | Route to | First action |
   |---|---|---|
   | "Is my project on track?" (running, no baseline) | `project-delivery` | Build the one-day interim baseline; sponsor approves it |
   | "Is my project on track?" (not started, no baseline) | `project-planning` | Baseline scope, schedule and cost |
   | "Log or escalate this problem" (happening now) | `project-delivery` | Log it with one owner and due date; escalate past the owner's authority |
   | "We are always late" | `project-schedule`, then `cost-management` | Find the critical path; read SPI and the forecast |
   | "We are over budget" | `cost-management` | Run the earned-value check; size the EAC |
   | "Scope keeps growing" | `change-management`, then `scope-and-requirements` | Set the change threshold; re-baseline scope |
   | "Is this in scope?" | `scope-and-requirements` | Check the signed in/out list; route a new item to `change-request` |
   | "My vendor is late" | `procurement-management` | Apply the contract remedies; log the issue |
   | "Should we build or buy?" / "write an RFP or SOW" | `procurement-management` | Decide make-or-buy per work package; write the SOW |
   | "We go live next week" | `release-and-cutover` | Run the go/no-go against readiness criteria |
   | "Plan the next sprint" / "how many sprints left?" / "write user stories" | `agile-delivery` | Forecast from velocity; plan to capacity |
   | "Who is overloaded?" | `resource-management` | Run the capacity check; level the peaks |
   | "Nobody knows who decides" | `raci-matrix` | One Accountable per deliverable and decision |
   | "The sponsor has gone quiet" | `stakeholder-management` | Re-map power/interest; plan a 1:1 |
   | "Something big might go wrong" | `risk-management` | Score it; choose a response; check the reserve |

   *Done: the user has one or two named skills, a first action and the artifact to expect.*
6. **Hand off.** Give the filled canvas back so the next conversation starts from it; offer
   `references/helios-walkthrough.md` to a first-timer who wants to see the whole lifecycle;
   point to `references/pm-glossary.md` for any unfamiliar term. *Done: canvas returned,
   next skill named, no term left unexplained.*

## Quality checklist
- [ ] The intake questions were asked (or already answered) and every canvas cell is filled or marked "unknown" with the question that would fill it.
- [ ] Exactly one stage is named, with the evidence that placed it and the stage's missing artifacts.
- [ ] Scope, schedule, cost and risk are rated separately against the baseline (CPI/SPI, milestone slip, velocity forecast or a named proxy), and the overall RAG is no greener than the worst material dimension — or the read says "no baseline".
- [ ] A methodology is recommended with the signal(s) behind it.
- [ ] At most two skills are named in backticks, each exists in `references/routing-map.md`, and each has a first action and an expected artifact.
- [ ] Every helper command given is repo-root-relative and points at the user's file or a named sample.
- [ ] Helios appears only as the labelled sample, never as the user's project.

## Anti-patterns
- Calling a project green because artifacts exist (a plan, a register) while it is 30% over
  budget — existence is not health; read the variance.
- Answering "is my project on track" without a baseline; say there is nothing to measure
  against and route to `project-delivery` for an interim baseline if work is running, or to
  `project-planning` if it has not started.
- Routing before diagnosing the stage — the wrong skill wastes the user's time.
- Recommending a methodology by default (always "agile") instead of from the signals.
- Dumping the catalog on the user; route to one or two skills, not ten.
- Doing the downstream work here (writing the charter, building the plan) instead of
  handing off — this skill triages, the specialist skills deliver.
- Re-triaging from zero when the user already has a canvas; ask what changed.
- Copying Helios numbers into the user's answer.

## Resources
- `references/routing-map.md` — all 27 skills by tier, routing by stage, intent and symptom, tie-breaks for shared triggers, and common multi-skill sequences.
- `references/methodology-selection.md` — when waterfall, agile or hybrid fits, a scored checklist, and the skill sequence and gates for each approach.
- `references/pm-glossary.md` — concise definitions of the PM terms used across the catalog, each pointing to the skill that owns it.
- `references/helios-walkthrough.md` — the catalog's worked example: the sample Helios project from idea to closure, naming the skill, artifact and helper command at each step.
- `assets/project-state-template.md` — fill-in project-state canvas with the per-dimension health read and the artifact checklist by stage.
- `assets/project-state-sample.md` — sample canvas for Helios as at 2026-07-10, the week after the month-3 close (AMBER).
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-initiation` — route here at the idea or initiation stage; it returns the business case, signed charter and stakeholder register that move the canvas to planning.
- `project-planning` — route here once the project is authorized and before work starts, or for a full re-plan; it returns the approved scope, schedule and cost baselines the health read measures against.
- `project-delivery` — route here when the project is executing, including one already running without a baseline (its first step builds a one-day interim baseline); its issue log of issues, actions, decisions and dependencies and its weekly RAG keep the canvas current.
- `project-closure` — route here when deliverables are accepted or work is stopping; it closes the canvas with acceptance, handover, benefits tracking and lessons.
- `risk-management` — route here when the canvas's top-risk cell dominates (a HIGH risk without a response, or exposure beyond the contingency reserve); it returns responses and reserve sizing.
- `agile-delivery` — route here when the approach is agile or hybrid; its velocity forecast gives the schedule reading for the health read when there is no earned value.
