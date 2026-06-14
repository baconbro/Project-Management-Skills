---
name: status-report
description: >-
  Produces a concise, audience-fit project status report with an overall RAG
  (Red/Amber/Green) rating plus progress, milestones, top risks and issues,
  decisions needed, and next steps, pulling schedule and cost health from
  cost-management earned value where available. Use when the user wants to write,
  prepare, or review a status report, status update, progress report, or
  steering-committee update, set or justify a RAG / traffic-light status, or
  summarize where a project stands. Triggers: "status report", "status update",
  "progress report", "RAG status", "traffic light", "steering update", "weekly
  report", "project health". For the broader reporting and communication plan,
  use project-communication. Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: artifact
  phase: delivery
  related: [project-delivery, project-communication, cost-management]
license: MIT
---

# Status Report

## Overview
A status report is the short, regular update that tells stakeholders where the project
stands: an honest overall RAG rating, progress since last time, milestone health, the
risks and issues that matter, the decisions you need from them, and what happens next.
Its job is to enable decisions, not to narrate activity.

## When to use this skill
- The user wants to write or review a status report, progress update, or steering pack.
- The user needs to set or defend a RAG / traffic-light rating.
- A regular reporting cadence is due (weekly team, monthly sponsor, steering committee).
- Do NOT use this to design the overall reporting plan, audiences, and channels — use
  `project-communication`.
- Do NOT compute earned value or budget variance here — pull those from `cost-management`
  and report the result.

## Methodology fit
- **Waterfall:** milestone- and phase-based progress against the baseline plan.
- **Agile:** report by sprint/increment — velocity, burndown, increment value delivered.
- **Hybrid:** RAG and milestones at the governance level; sprint metrics underneath.

## Inputs you need
The reporting period and audience, progress since the last report, milestone dates
(baseline vs. forecast), the current top risks and issues, any decisions you need, and —
where available — schedule and cost health (SPI/CPI or variance) from `cost-management`.
A small metrics sample lives in `assets/status-report.csv`.

## Workflow
1. Fix the **audience and period**. A sponsor wants exceptions and decisions; a team
   wants detail. Write to the reader. *Done: audience and dates stated.*
2. Set the **overall RAG honestly** using the objective thresholds in
   `references/rag-criteria.md` across scope, schedule, cost, and quality — the overall
   rating is no greener than its worst material dimension. *Done: RAG set with a reason.*
3. Pull **schedule and cost health** from `cost-management` (SPI/CPI or variance) if
   earned value is tracked; otherwise state progress against the baseline plainly.
   *Done: schedule and cost lines have evidence, not vibes.*
4. Summarize **progress and milestones**: what completed this period, what is next, and
   each key milestone's baseline vs. forecast date with its own RAG.
5. List the **top risks and issues** (link to the risk register, do not duplicate it) and
   the **decisions needed** with a clear ask and a deadline. *Done: every red/amber has an
   owner and an action.*
6. Fill `assets/status-report-template.md`, keep it to one page or one screen, and lead
   with the RAG and the decisions. *Done: a busy reader gets the picture in 30 seconds.*

## Quality checklist
- [ ] Audience and reporting period are stated.
- [ ] Overall RAG is justified against `references/rag-criteria.md` and no greener than its worst dimension.
- [ ] Schedule and cost health cite evidence (earned value / variance) where available.
- [ ] Milestones show baseline vs. forecast; every amber/red has an owner and action.
- [ ] Decisions needed are explicit, with an ask and a deadline.
- [ ] Fits one page/screen; leads with status and decisions, not a wall of narrative.

## Anti-patterns
- "Watermelon" reports — green on the outside, red on the inside — that hide bad news.
- Reporting activity ("we held 12 meetings") instead of outcomes and forecast.
- A RAG with no criteria behind it, so green means nothing.
- Burying the one decision you need under three pages of narrative.
- Recreating the full risk register in the report instead of linking to it.

## Resources
- `references/rag-criteria.md` — objective Green/Amber/Red thresholds and how to rate honestly.
- `assets/status-report-template.md` — fill-in one-page status report.
- `assets/status-report.csv` — sample metric/value/rag data the report summarizes.

## Related skills
- `project-delivery` — the execution phase this report monitors and informs.
- `project-communication` — the reporting plan, audiences, and channels around this report.
- `cost-management` — supplies the earned-value schedule and cost health reported here.
