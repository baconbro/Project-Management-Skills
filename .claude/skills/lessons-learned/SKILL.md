---
name: lessons-learned
description: >-
  Captures, categorizes, and operationalizes project lessons — running a
  retrospective, classifying what went well and badly, and assigning follow-up
  owners so improvements actually happen instead of sitting in a document. Use
  when the user wants to run a retrospective or post-mortem, capture lessons
  learned, hold a project review, or turn what the team learned into concrete
  improvements with owners. Triggers: "lessons learned", "retrospective", "retro",
  "post-mortem", "post-implementation review", "what went well", "start stop
  continue", "5 whys", "continuous improvement". For the full project close-out and
  handover around this, use project-closure. Works for waterfall, agile, and
  hybrid projects.
metadata:
  version: 1.0.0
  category: artifact
  phase: closure
  related: [project-closure]
license: MIT
---

# Lessons Learned

## Overview
A lessons-learned exercise turns a project's experience — good and bad — into improvements
the organization actually adopts. The trap is recording lessons in a document nobody reads
again. The discipline that matters is **operationalizing** them: classifying each lesson and
giving it an owner and a follow-up, so the next project is genuinely better.

## When to use this skill
- The user wants to run a retrospective, post-mortem, or post-implementation review.
- A project, phase, or sprint is ending and its lessons should be captured and acted on.
- Recurring problems suggest the team is not learning between projects.
- Do NOT use this for the whole project close-out — sign-off, handover, contract closure,
  archiving — use `project-closure`, which calls this skill for the lessons step.

## Methodology fit
- **Waterfall:** a structured lessons-learned review at phase gates and at project close.
- **Agile:** a retrospective every sprint/iteration, plus a larger one at release.
- **Hybrid:** sprint retros for the team plus a milestone/closure review for the whole
  project and its stakeholders.

## Inputs you need
The participants (the people who did the work, plus key stakeholders), the period under
review, and any data — metrics, the risk register, status reports, the change log — that
turns opinion into evidence. The lessons log is `assets/lessons-learned.csv`.

## Workflow
1. **Pick a retrospective format** that fits the situation from
   `references/retrospective-formats.md` (start/stop/continue, 4Ls, sailboat,
   mad-sad-glad, 5 whys). Match the format to the goal: broad reflection vs. root-causing
   one failure. *Done: a format chosen and shared with participants.*
2. **Create a safe space.** State that this is about the process, not blaming people
   (Norm Kerth's Prime Directive). Without psychological safety you get silence and polite
   half-truths. *Done: ground rules stated.*
3. **Gather lessons** using the format — what went well, what did not, and why. Use data to
   ground claims and **5 whys** to reach root causes, not symptoms. *Done: lessons captured
   from the whole group, not just the loudest voices.*
4. **Classify** each lesson by category (e.g. planning, communication, technical, process,
   people) and rate its impact, so patterns and the lessons worth acting on stand out.
   *Done: every lesson has a category and an impact.*
5. **Operationalize** — for each lesson worth acting on, write a concrete **recommendation**,
   assign an **owner**, and set a **status**. A lesson with no owner is just a memory. Record
   them in `assets/lessons-learned.csv`. *Done: actionable lessons have an owner and status.*
6. **Hand off and follow up.** Feed recommendations into standards, checklists, or the next
   project's plan, and store the log in the organization's asset repository via
   `project-closure`. *Done: lessons routed somewhere they will be reused.*

## Quality checklist
- [ ] A retrospective format was chosen to fit the goal.
- [ ] The session was framed as blameless; the whole group contributed.
- [ ] Lessons are grounded in data and traced to root causes, not symptoms.
- [ ] Each lesson is categorized and impact-rated.
- [ ] Every actionable lesson has a recommendation, an owner, and a status.
- [ ] The log is handed off to be reused, not filed and forgotten.

## Anti-patterns
- A lessons-learned document with no owners — a list of regrets nobody acts on.
- Blaming individuals, which guarantees the next session is silent.
- Stopping at symptoms ("testing was rushed") instead of root causes ("UAT had no
  dedicated environment").
- Only capturing what went wrong; the things that went well must be repeated on purpose.
- Holding the retro and never feeding the lessons into anything that changes.

## Resources
- `references/retrospective-formats.md` — start/stop/continue, 4Ls, sailboat, mad-sad-glad, 5 whys, and when to use each.
- `assets/lessons-learned.csv` — lessons log (id, category, what_happened, impact, recommendation, owner, status).

## Related skills
- `project-closure` — the full close-out and handover this lessons step feeds into.
