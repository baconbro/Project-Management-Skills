---
name: project-charter
description: >-
  Creates a project charter that formally authorizes a project, names the
  sponsor and project manager, and captures objectives, scope boundaries,
  high-level milestones, budget, assumptions, top risks, and success criteria.
  Use when the user wants to start, authorize, or kick off a project, write or
  review a charter or project brief, define a project's purpose, scope,
  objectives, or sponsor, or needs a one-page mandate before planning begins.
  Triggers: "project charter", "project brief", "authorize a project", "project
  mandate", "kickoff document", "start a new project", "project one-pager".
  Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: artifact
  phase: initiation
  related: [project-initiation, business-case, stakeholder-management, project-planning]
license: MIT
---

# Project Charter

## Overview
A project charter is the short, authoritative document that authorizes a project to
exist, appoints the project manager, and aligns the sponsor and stakeholders on why
the project exists and what "done" means. It is the reference point every later
decision traces back to.

## When to use this skill
- The user is starting, authorizing, or kicking off a new project or phase.
- The user asks for a "charter", "project brief", "mandate", or "one-pager".
- A project is already underway but has no agreed statement of purpose and scope.
- Do NOT use this to justify the investment financially — use `business-case`.
- Do NOT use this to build the detailed plan — use `project-planning`.

## Methodology fit
- **Waterfall:** full charter, formally signed off before planning starts.
- **Agile:** lightweight charter / project brief — objectives and guardrails, not fixed scope.
- **Hybrid:** charter fixes outcomes and constraints; the delivery approach stays flexible.

## Inputs you need
Sponsor name, the business need or problem, the target outcome, a rough budget and
timeline, known constraints and assumptions, and the key stakeholders. If the business
need is unclear or unjustified, pause and run `business-case` first.

## Workflow
1. Confirm the **sponsor** and the **project manager**. A charter without a named
   sponsor is not authorized — flag this explicitly. *Done: both are named.*
2. State the **business need / problem** in 1-2 sentences, pulling from the business
   case if one exists. *Done: a non-technical reader understands why this project exists.*
3. Define **objectives** as SMART outcomes plus **success criteria** (how success is
   measured). *Done: each objective is measurable.*
4. Set **scope boundaries** — in-scope outcomes and an explicit out-of-scope list. The
   out-of-scope list prevents the most expensive disputes. *Done: both lists present.*
5. Capture **high-level milestones, budget range, key assumptions, constraints**, and
   the **top risks** (qualitative only — full analysis belongs in `risk-management`).
6. List **key stakeholders** and the PM's **authority level**. For a full analysis,
   hand off to `stakeholder-management`.
7. Fill `assets/charter-template.md`, keep it to ~1-2 pages, and route it to the
   sponsor for sign-off. *Done: template complete with no placeholder left unfilled.*

## Quality checklist
- [ ] Named sponsor AND named project manager.
- [ ] Business need stated in plain language.
- [ ] Objectives are measurable with explicit success criteria.
- [ ] Both in-scope and out-of-scope lists are present.
- [ ] Milestones, budget range, assumptions, constraints, and top risks captured.
- [ ] Fits on ~1-2 pages with no unresolved placeholders.

## Anti-patterns
- Turning the charter into a detailed plan or schedule — that is `project-planning`.
- Omitting out-of-scope items, the most common source of later scope fights.
- Vague objectives ("improve efficiency") with no measure of success.
- Writing a charter with no sponsor able to authorize and fund the work.

## Resources
- `references/charter-elements.md` — definition and an example of each charter element.
- `assets/charter-template.md` — fill-in-the-blanks charter template.

## Related skills
- `business-case` — establishes the financial justification this charter assumes.
- `project-initiation` — the broader phase this charter sits inside.
- `stakeholder-management` — deeper analysis of the stakeholders listed here.
- `project-planning` — the next step once the charter is authorized.
