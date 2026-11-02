---
name: project-initiation
description: >-
  Runs the initiation phase from idea to a planning-ready project or phase:
  frames the problem and sponsor, commissions a business case (three options
  including do-nothing, every benefit with a measured baseline and an owner),
  chooses waterfall, agile or hybrid delivery, gets the charter signed,
  identifies stakeholders, passes an initiation gate with a recorded verdict,
  sets what the kickoff covers, and hands an initiation pack to planning. Use
  when the user is starting a project from an idea or mandate, wants
  initiation run end to end, or asks what is still missing before planning can
  begin. Triggers: "start a new project", "initiate a project", "stand up a
  project", "get a project off the ground", "initiation phase", "initiation
  gate", "are we ready to start planning", "what do I do before planning",
  "kickoff deck", "what should the kickoff cover". For the charter alone, use
  project-charter; for running the kickoff meeting itself, use
  meeting-management. Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.1.0
  category: phase
  phase: initiation
  related: [senior-pm, project-charter, business-case, stakeholder-management, project-planning, meeting-management]
license: MIT
---

# Project Initiation

## Overview
Initiation turns an idea into an authorized project that planning can start on: one sponsor
with funding authority, an investment justified against doing nothing, benefits that can be
proven later because their "before" number is measured now and someone outside the team owns
them, a delivery approach chosen on purpose, a signed charter, known stakeholders, and a team
that heard the same story at the kickoff. This skill is the conductor. It runs the specialist
skills in order, checks the result at one initiation gate (G0) with a recorded verdict, and
hands planning a complete initiation pack; the documents themselves are written in
`business-case`, `project-charter` and `stakeholder-management`, and the kickoff meeting is run
with `meeting-management`. The examples use the sample Helios project (a fictional customer
self-service portal used throughout this catalog): sponsor Dana Okoro (VP Customer Operations),
project manager Sam Lee, objective OBJ-1 (cut password-reset and order-status tickets by 50%
within 6 months of launch, benefit owner Priya Nair), a hybrid approach, charter v1.0 signed on
2026-04-02, gate G0 passed with conditions on 2026-04-06 and the kickoff on 2026-04-07.

## When to use this skill
- The user is starting a new project or phase from an idea, request or mandate and needs the
  ordered path to an authorized, planning-ready project.
- The user has fragments (an idea, a keen sponsor, a draft charter) and wants to know what is
  still missing before planning can begin.
- The user must prepare or hold the initiation gate, or decide what the kickoff covers and what
  goes in the deck.
- A project is already running but skipped initiation (no signed charter, no agreed objective):
  use the compressed route in `references/initiation-checklist.md` (section 7).
- Do NOT use this to produce one artifact on its own — go straight to `business-case`,
  `project-charter` or `stakeholder-management` instead.
- Do NOT use this for the kickoff meeting's mechanics (timeboxes, facilitation, minutes, action
  capture) — use `meeting-management` instead; this skill owns what the kickoff must say.
- Do NOT use this to build the plan, the RACI matrix or the baselines — use `project-planning`.
- Do NOT use this when the project's stage is unclear — use `senior-pm` to triage it first.

## Methodology fit
- **Waterfall:** a full business case and a formally signed charter; every gate item is Done,
  waived in writing or carried as an owned condition before any planning spend; a 60–90 minute
  kickoff with the wider stakeholder group; planning receives the whole scope to baseline.
- **Agile:** a lean case sized to the spend (outcome, funding envelope, leading measures) and a
  one-page brief with guardrails; the product owner and their decision rights are a gate item;
  the kickoff grows into a half-day team liftoff that adds the working agreement
  (`resource-management`) and a first backlog sketch (`agile-delivery`); planning receives a
  release goal and an ordered backlog, not a fixed scope.
- **Hybrid (Helios):** the case and charter fix the frame — OBJ-1, the $450k–$550k range,
  milestones M1/M4/M6 and SSO through the existing identity provider — while portal and
  knowledge-base features flex in two-week sprints ordered by the product owner, Ava Chen; the
  kickoff presents both the milestone frame and the sprint cadence, and planning baselines the
  frame and keeps the rest as a backlog.

## Inputs you need
- The idea or mandate, who asked for it, and the problem with evidence (volume, cost, delay,
  risk).
- A candidate sponsor: one executive who can fund the work and decide when it matters.
- The target outcome, the metric that will show it, and where today's value of that metric is
  measured (Helios: monthly password-reset and order-status tickets in the ticketing system,
  about 5,000 a month).
- A candidate benefit owner in the business who will still be accountable after the project
  closes.
- Hard constraints (deadline, budget ceiling, regulation, technology) and the organization's
  governance: who approves investments and projects, the discount rate, gate rules and the PM's
  usual authority.

If no sponsor can be named, stop at step 1: an unsponsored project cannot be authorized. If
nobody can name the metric or where it is measured, that is the first gap to close.

## Workflow
1. **Frame the request and confirm the sponsor.** Write the problem in two sentences with its
   size, the outcome wanted, the candidate sponsor and the route: full initiation for a new
   project, a re-check for a new phase, or the compressed route for a running project that
   skipped initiation (`references/initiation-checklist.md`, section 7). Open a copy of
   `assets/initiation-gate-record.md` and enter the project, route, sponsor and PM. *Done: one
   named sponsor has agreed to take the case forward, the problem has a number, and the route
   is recorded.*
2. **Justify the investment with `business-case`.** Compare at least three options including
   do-nothing (do-minimum is a separate option) on the same criteria and cashflow basis, and
   appraise them; on the Helios sample,
   `python .claude/skills/business-case/scripts/roi_npv.py .claude/skills/business-case/assets/cashflows-options-sample.csv --all`
   ranks the recommended portal first (NPV $196,174 at 10%). Then hold every benefit to the
   benefit test: a measure, a **measured baseline** (value, source and date), a target with a
   date, and a named **benefit owner** outside the project team who has accepted it. Measure the
   "before" number now: once delivery starts it moves, and the improvement can no longer be
   proven at closure (Helios B001: about 5,000 tickets a month today, formal baseline the 3
   months before launch, owner Priya Nair). If the case fails, record the stop or defer
   decision and end here.
   *Done: the funding decision is recorded with approver and date, and every row of the benefits
   register passes the benefit test (or a recorded waiver of the case names who waived it).*
3. **Choose the delivery approach.** For the recommended option (a buy option and a build
   option are delivered differently), answer the five questions and apply the overrides in
   `.claude/skills/senior-pm/references/methodology-selection.md`; ask `senior-pm` when the
   signals conflict. Record the approach, the Yes count, any override, the charter form, what
   planning will baseline and the governance cadence in section 2 of the gate record. Helios:
   4 Yes, and the fixed six-month date and budget make it hybrid. *Done: waterfall, agile or
   hybrid is recorded with its count, override and implications, ready for the charter header
   and kickoff slide 8.*
4. **Authorize the project with `project-charter`.** Feed it the recommended option, the
   budget range, the objective with its baseline and benefit owner, and the approach from
   step 3; name the PM and their authority; get the sponsor's decision on a specific version.
   Until it is signed, the charter authorizes no hiring, contracts or spend. *Done: the
   charter's Status reads Approved with the sponsor's name, version and date (Helios: v1.0,
   Dana Okoro, 2026-04-02) and the budget holder has confirmed the funding.*
5. **Identify the stakeholders with `stakeholder-management`.** Build the register from the
   charter's key stakeholders and the case's benefit owners and dis-benefits: power, interest,
   quadrant, engagement approach and a named owner per row. Check that the sponsor and every
   benefit owner sit in Manage Closely and that every approver is named, then derive the
   kickoff invite list from the register. *Done: the register exists, approvers and
   decision-makers are named, and every kickoff invitee has a reason to attend.*
6. **Pass the initiation gate (G0).** Walk the 24 items in
   `references/initiation-checklist.md` and record each in the gate record as Done (document,
   version and date as evidence), Waived (reason, risk left and who accepted it), Condition
   (safe to finish in planning) or Open. The blocking items — the problem, the three options,
   the benefit baselines and owners, the funding decision, the sponsor, the PM and the signed
   charter — must be Done. The sponsor records the verdict: Go, Go with conditions (each owned
   and dated no later than the baseline approval), Recycle (the step to redo and the re-gate
   date) or Stop. Compare with `assets/initiation-gate-record-sample.md`. *Done: no item is
   Open, every blocking item is Done, and the sponsor's verdict, conditions and date are
   recorded.*
7. **Prepare and hold the kickoff.** Take the content from `references/kickoff-agenda.md` and
   build the slides in a copy of `assets/kickoff-deck-outline.md` (Helios:
   `assets/kickoff-deck-sample.md`), drawing only on the signed charter, the case and the
   register. The roles slide is a **draft of roles** from the charter, labelled as such; the
   full RACI matrix is built in `project-planning` with `raci-matrix` once the work is
   decomposed. Run the meeting with `meeting-management`: its
   `.claude/skills/meeting-management/assets/agenda-template.md` for the timed agenda, a named
   decider and decision method, a parking lot for scope disputes, and live capture in copies of
   `.claude/skills/meeting-management/assets/decision-log.csv` and
   `.claude/skills/meeting-management/assets/action-items.csv`. *Done: the kickoff is held,
   every decision and action has one owner and a date, and the notes went out within one
   business day.*
8. **Hand off to planning.** Pass the initiation pack listed in section 6 of the gate record to
   `project-planning`: the signed charter, the approved business case with its benefits
   register, the stakeholder register, the delivery approach, the open assumptions, the gate
   conditions and waivers, and the kickoff decisions and actions (marked `local` until planning
   opens the issue log). Agree the first planning step with an owner and a date. *Done: the
   planning owner has acknowledged the pack and the first planning step has an owner and a date
   (Helios: Sam Lee opens the plan and assumptions log on 2026-04-08; baseline approval at M1,
   2026-05-08).*

## Quality checklist
- [ ] One sponsor with funding authority and one PM are named in the charter and the gate record.
- [ ] The business case compares at least three options, including do-nothing, on the same
      basis, and its funding decision names the approver, conditions and date (or a waiver of
      the case names who waived it and why).
- [ ] Every benefit has a measure, a measured baseline with source and date, a target with a
      date, and a named benefit owner outside the project team who has accepted it.
- [ ] The delivery approach is recorded with the checklist count, any override and its
      implications, and the charter header states the same approach.
- [ ] The charter is signed on a specific version, Status reads Approved, and funding is
      confirmed by the budget holder.
- [ ] The stakeholder register gives every key stakeholder power, interest, quadrant, an
      engagement approach and an owner; the sponsor and each benefit owner are Manage Closely.
- [ ] No gate item is Open and every blocking item is Done; every waiver has a reason and an
      accepter; the verdict, each condition's owner and due date, and the sponsor's decision
      date are recorded.
- [ ] Every figure in the kickoff deck matches the signed charter and the approved case, the
      roles slide is labelled a draft, and each kickoff action has one owner and a date.
- [ ] The initiation pack is acknowledged by the planning owner, with the first planning step,
      its owner and its date.
- [ ] No `<placeholder>` is left in the copied templates, and Helios figures appear only in the
      labelled samples.

## Anti-patterns
- Holding the kickoff before the charter is signed: an aligned team on an unauthorized project
  is wasted effort, and kickoff is not step one.
- A sponsor who cannot fund or decide, or a committee in the sponsor's seat.
- Benefits with a target but no measured "before" number, or with the PM as benefit owner, so
  the closure review cannot prove anything and nobody owns the result after handover.
- Two options passed off as three by merging do-nothing and do-minimum.
- Never choosing the delivery approach, so the charter form, the governance and the baseline
  are improvised later.
- Presenting a full RACI at the kickoff before the work is decomposed; show a draft of roles.
- A slide-marathon kickoff where scope disputes are argued in the room instead of parked for
  the sponsor.
- Waivers with no reason or accepter, or a gate "passed" while a blocking item is open.
- Sliding into requirements, estimates or a schedule here instead of handing off to
  `project-planning`.

## Resources
- `references/initiation-checklist.md` — the G0 gate: 24 items in five groups (need and
  benefits, delivery approach, authorization, stakeholders, readiness to plan), the evidence
  that passes each, the blocking items, the verdict rules, scaling for agile, a new phase or a
  running project that skipped initiation, and common gaps.
- `references/kickoff-agenda.md` — what the kickoff must achieve, entry conditions, who to
  invite from the register, pre-reads, a 60-minute content agenda tied to the deck, variants
  (small team, agile liftoff, large programme, remote), what a kickoff may and may not decide,
  the split with `meeting-management`, and the Helios kickoff of 2026-04-07.
- `assets/initiation-gate-record.md` — fill-in gate record (`<placeholders>`): header,
  delivery-approach decision, the 24 items with status and evidence, waivers, verdict and
  conditions, the initiation pack for planning, and sign-off.
- `assets/initiation-gate-record-sample.md` — sample Helios gate record: Go with conditions on
  2026-04-06, one waiver, two conditions and the pack handed to planning.
- `assets/kickoff-deck-outline.md` — fill-in 11-slide kickoff deck (`<placeholders>`), with the
  source of every slide and a draft-of-roles slide.
- `assets/kickoff-deck-sample.md` — sample Helios kickoff deck content for 2026-04-07.
- Cross-skill files used: `.claude/skills/business-case/scripts/roi_npv.py` (step 2; run it with
  `--help` for its inputs), `.claude/skills/senior-pm/references/methodology-selection.md`
  (step 3), and the agenda template and capture sheets of `meeting-management` (step 7).
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `senior-pm` — routes an idea-stage project here, supplies the methodology checklist used in
  step 3, and moves its project-state canvas to planning on this skill's G0 verdict.
- `project-charter` — writes and verifies the charter in step 4; this skill feeds it the
  recommended option, budget range, objective with baseline and benefit owner, and the delivery
  approach, and treats the signed version as the authorization gate item.
- `business-case` — builds and decides the investment case in step 2; this skill holds it to
  three options and to a measured baseline and an accepted owner for every benefit before G0.
- `stakeholder-management` — builds the register in step 5; this skill takes from it the
  approvers, the Manage Closely check for sponsor and benefit owners, and the kickoff invite list.
- `project-planning` — receives the initiation pack in step 8 (charter, case and benefits
  register, stakeholder register, approach, conditions, kickoff actions) and builds the plan,
  the RACI matrix and the baselines.
- `meeting-management` — runs the kickoff meeting in step 7 (agenda, decider and method, parking
  lot, capture of decisions and actions, notes); this skill supplies what the kickoff must cover.
