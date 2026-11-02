---
name: lessons-learned
description: >-
  Runs retrospectives and blameless post-mortems, finds root causes (5 whys, timelines)
  and turns lessons into owned, dated actions that are checked later. Use when running a
  sprint retrospective, project review or post-mortem, or when the same mistakes keep
  happening.
metadata:
  version: 1.1.0
  category: artifact
  phase: cross-cutting
  related: [project-delivery, project-closure, agile-delivery]
license: MIT
---

# Lessons Learned

## Overview
A lessons-learned practice turns what a team experienced, good and bad, into changes that
stick. The trap is a document nobody reads again. This skill runs the review (a sprint
retrospective, a phase or milestone review, a blameless post-mortem on one failure, or the
post-project review at closure), traces each lesson to evidence and a root cause, classifies
it, and then **operationalizes** it: one owner, a due date, the exact backlog, log or standard
it changes, and a dated check-back that confirms the change worked. It runs all through the
project, not only at the end. Examples follow the sample Helios project (a fictional customer
self-service portal used throughout this catalog): sponsor Dana Okoro, project manager Sam Lee,
two-week sprints inside fixed milestones, run hybrid.

## When to use this skill
- A sprint, release, phase or project is ending and the team should review how it worked.
- Something failed or nearly failed (a missed milestone, a rolled-back release, an incident)
  and needs a blameless post-mortem once it is resolved.
- The same problems keep coming back, or lessons are recorded but never acted on.
- Earlier lessons are due a check-back, or a new project wants the lessons of past ones.
- Do NOT use this for the whole close-out (acceptance, handover, contracts, finances) — use
  `project-closure` instead, which calls this skill for its post-project review.
- Do NOT use this to log or resolve a problem happening now — use `project-delivery` instead;
  come back here once it is resolved to learn from it.
- Do NOT use this to place the retrospective in the sprint cadence — use `agile-delivery`
  instead; for meeting mechanics such as timeboxing and the parking lot, use
  `meeting-management`.
- Do NOT use this to root-cause individual escaped defects — use `quality-management` instead;
  bring the recurring pattern here.

## Methodology fit
- **Waterfall:** a lessons review at each phase gate (an updated lessons log is a gate exit
  criterion), a timeline post-mortem when a milestone is missed, and a post-project review at
  closure. Actions land in the next phase's plan through the issue log or a change request and
  are checked at the next gate.
- **Agile:** a retrospective every sprint (about 90 minutes for two weeks, the team only),
  yielding one or two actions that enter the next sprint backlog and are checked when the next
  retrospective opens; a wider retrospective per release. A theme that recurs in three
  retrospectives is promoted to an organisational lesson.
- **Hybrid:** team retrospectives inside the sprints plus milestone reviews and post-mortems
  with stakeholders. Helios: a sprint review, then a team-only retrospective, every second
  Friday; a post-mortem on the two-week SSO slip on 2026-07-22; the M4 milestone review on
  2026-08-11; and the post-project review on 2026-11-04.

## Inputs you need
- The review type, the period covered, and the participants: the people who did the work, plus
  key stakeholders for phase and project reviews.
- A data pack that turns opinion into evidence: velocity and predictability (`agile-delivery`),
  CPI and SPI from the earned-value snapshot, defects, and the issue log, risks that occurred
  and change requests from `project-delivery`.
- The previous session's actions and every open lesson whose check-back date has arrived.
- Where organisational lessons live: the PMO's lessons repository and the owners of its
  standards, templates and checklists.
- A copy of `assets/lessons-learned.csv` (or the project's running log).

## Workflow
1. **Choose the review type and the format.** The type (sprint retrospective, phase or
   milestone review, post-mortem, post-project review) sets who attends, which data to bring
   and where actions go in step 6. Pick the format from the selection table in
   `references/retrospective-formats.md`: start/stop/continue for a quick sprint retrospective,
   4Ls for a phase or project, sailboat for momentum and risks, mad/sad/glad for team strain, a
   timeline post-mortem plus 5 whys for one failure. Helios used 4Ls for the post-project review.
   *Done: review type, period, participants and format are written in the session record.*
2. **Prepare the evidence and a safe room.** Copy `assets/retrospective-record-template.md`, or
   `assets/post-mortem-template.md` for a single failure, and fill the data pack; for a
   post-mortem, draft the timeline from records first. Book a facilitator who is not the team's
   line manager and, for a post-mortem, made none of the decisions under review. Open with the Prime Directive and,
   when trust is low, an anonymous safety check; then hold the check-back of step 7 on every
   action now due. *Done: the data pack is circulated, ground rules are stated, and due actions
   are marked in section 1 of the record.*
3. **Gather what went well and what did not.** Silent writing first so quiet voices count, then
   cluster into themes and dot-vote the top two or three. Ground every item in the data pack
   ("SPI 0.75 on 1.3.1", not "SSO was a mess") and keep the went-well items: they are lessons to
   repeat. *Done: every participant contributed, the top themes are voted, and at least one
   went-well item is recorded.*
4. **Find the root cause of each top theme.** Ask why until you reach a cause in your control
   that would stop it recurring; check the chain with the "therefore" test, branch when two
   causes contribute, and stop at a condition, never a person (5 whys and the timeline method in
   `references/retrospective-formats.md`). Helios: the SSO slip branched into a late start (no
   onboarding owner, so the sandbox was requested only after contract signature in week 5) and a
   stoppage (the sandbox outage, I001, with no test fallback); both feed lesson LL001. *Done:
   each top theme has a root cause that passes the therefore test, or is marked as a symptom
   still to investigate.*
5. **Classify and rate.** Give each lesson a kind (`improve` or `repeat`), one of the eight
   categories (planning, scope, communication, technical, process, people, quality, vendor,
   chosen by where the root cause sits) and an impact on the High/Medium/Low scale; act on every
   High, on a Medium that recurs or is cheap, and on a Low only when it recurs. Helios: LL005
   (stand-ups ran over 30 minutes) is process/Low; LL007 (agent training with no catch-up
   for absentees, which became a go-live condition) is planning/High. *Done: every lesson has a
   kind, category and impact, and the ones to act on are marked.*
6. **Operationalize: write the action and route it.** For each lesson to act on, write a
   verb-first recommendation, the target it changes (`applies_to`), one owner, a due date, who
   checks back and when, and record it in the copy of `assets/lessons-learned.csv`
   (`assets/lessons-learned-sample.csv` is the Helios log). Route by path
   (`references/operationalizing-lessons.md`):
   - **Sprint retrospective (agile path):** one or two actions, each added to the next sprint
     backlog by the product owner so it competes for capacity (`agile-delivery`); the next
     retrospective checks them. Helios: the S2 retrospective (2026-06-05) put the 15-minute
     stand-up timebox (LL005) into sprint S3.
   - **Beyond the team, mid-project** (phase or milestone review, post-mortem, an impediment the
     team cannot clear): an action in the `project-delivery` issue log
     (`.claude/skills/project-delivery/assets/issue-log.csv`) with owner and due date, a change
     request for any baseline change, a new threat into the risk register. Helios: LL004's root
     cause (one shared QA environment) was attached to issue I003.
   - **Organisational lessons:** name the standard, template or checklist in `applies_to` and
     agree the change with its owner, usually the PMO Lead; adopt it in this project too.
   *Done: every lesson to act on has a recommendation, target, owner, due date and check-back;
   sprint actions are backlog items and project actions are issue-log items.*
7. **Check back and close the loop.** On each check-back date ask: is the change in the target,
   was it used, did the outcome change? Record the evidence in `check_back_result`; mark
   `verified` only with evidence. Re-plan an undone action once, then escalate it (product owner,
   steering committee or PMO Lead); send one that did not work back to step 4. Check sprint
   actions as the next retrospective opens, project actions at the weekly control review or the
   next gate, and organisational lessons about 90 days after adoption. Helios: LL005 was verified
   at the S3 retrospective (2026-06-19): stand-ups averaged 14 minutes. *Done: no lesson past its
   check-back date is left unchecked, and none is marked verified without evidence.*
8. **Hand off the log.** Mid-project, the log stays live with the project: open project actions
   sit in the `project-delivery` issue log and are reviewed weekly, and the lessons log is
   reviewed at each milestone or gate. At closure, hand the log to `project-closure`, whose
   post-project review confirms it and puts the top lessons in section 8 of
   `.claude/skills/project-closure/assets/closure-report.md`; before the team is released, give
   every open lesson an owner and a check-back person who stay reachable after the project
   (usually the PMO Lead) and store the log in the PMO repository with `project` filled. Helios:
   the review on 2026-11-04 confirmed LL001-LL007, and the open ones are checked on 2027-02-03.
   *Done: mid-project, the log is current and its open actions are in the issue log; at closure,
   the log is in the repository, the top lessons are in the closure report, and no open lesson
   lacks a reachable owner and a dated check-back.*

## Quality checklist
- [ ] The session record names the review type, period, participants and a format that fits the goal.
- [ ] The session opened with the check-back: every action due is marked verified, not done or did not work.
- [ ] Ground rules were stated and every participant contributed; no lesson names a person as its cause.
- [ ] Every `improve` lesson has a root cause that passes the therefore test and at least one piece of evidence (a metric or a record id).
- [ ] Each session record keeps at least one went-well item, and each phase or project review logs at least one `repeat` lesson.
- [ ] Every lesson has a kind, a category from the defined list and an impact from the scale.
- [ ] Every lesson acted on has a verb-first recommendation, an `applies_to` target, one owner, a due date, a check-back person and a check-back date.
- [ ] A sprint retrospective produced no more than two actions, each an item in the next sprint backlog.
- [ ] Actions beyond the team's authority are in the `project-delivery` issue log; any baseline change went through change control.
- [ ] No lesson is `verified` or `declined` without a `check_back_result`.
- [ ] At closure, the log went to `project-closure` and every open lesson has an owner and a check-back person reachable after the project.

## Anti-patterns
- A lessons document with no owners or dates: a list of regrets nobody acts on.
- Lessons only at closure, after the team has dispersed and memory has faded.
- Blaming individuals, which guarantees the next session is silent.
- Stopping at symptoms ("testing was rushed") instead of root causes ("one shared QA
  environment with nobody refreshing its data").
- A why-chain that jumps causes: a late access request explains a late start, not an unstable
  sandbox.
- Ten retrospective actions and none done; or actions that never enter the backlog, so they
  never get capacity.
- Marking a lesson done when a template was edited, without checking it was used and worked.
- Only capturing what went wrong; what went well must be repeated on purpose.
- Routing a mid-project sprint retrospective through closure: its actions belong in the next
  sprint.

## Resources
- `references/retrospective-formats.md` — choosing a format by goal; start/stop/continue, 4Ls,
  sailboat, mad/sad/glad; 5 whys with the therefore test and the branching Helios example; the
  timeline (blameless) post-mortem with the Helios SSO timeline; running the session; the
  categories and the impact scale.
- `references/operationalizing-lessons.md` — the lessons-log columns and rules, writing an
  adoptable recommendation, the three routing paths (sprint backlog, issue log, organisation),
  lessons in at the next project, the status lifecycle, the check-back, health measures and the
  Helios routing table.
- `assets/lessons-learned.csv` — fill-in lessons log (`<placeholders>`), one template row per
  path; columns `id, project, date, source, category, kind, what_happened, root_cause, evidence,
  impact, recommendation, applies_to, owner, due_date, status, check_back_by, check_back_date,
  check_back_result`.
- `assets/lessons-learned-sample.csv` — sample: the Helios lessons log LL001-LL007 at closure
  (2026-11-20).
- `assets/retrospective-record-template.md` — fill-in record of one retrospective or review:
  check-back, data pack, findings and votes, root causes, lessons and actions, routing.
- `assets/post-mortem-template.md` — fill-in blameless post-mortem: impact, timeline, decision
  points, contributing factors, 5 whys, fix and prevent actions.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-delivery` — keeps the issue log where project-level actions from reviews and
  post-mortems are owned mid-project, supplies the issue, risk and change records that ground
  root causes, and calls this skill at milestones and retrospectives (its step 10).
- `project-closure` — runs the post-project review through this skill (its step 6), puts the top lessons in
  its closure report and archives the log; this skill hands it the log with every open lesson
  owned and dated for a check-back after closure.
- `agile-delivery` — places the sprint retrospective in the cadence (its step 7) and supplies velocity and
  predictability as evidence; this skill supplies the format and follow-through, and its one or
  two actions enter the next sprint backlog.
