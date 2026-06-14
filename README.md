# Project Management Skills

A methodology-agnostic catalog of **22 Agent Skills** that turn Claude into a **senior
project manager** — able to help anyone **initiate, plan, deliver, and close** a project,
whether it runs as waterfall, agile, or hybrid.

Built in the [Agent Skills](https://code.claude.com/docs/en/skills) format for Claude Code,
Claude Desktop/Web, Cowork, Codex, and other AI agents.

## What this is

Each skill is a self-contained folder under `.claude/skills/` with a `SKILL.md` (the
instructions Claude follows), plus optional ready-to-fill **templates**, deeper **reference
guides**, and dependency-free **Python helper scripts**. The skills cross-link into one
coherent system and are designed to be installed together. **`senior-pm` is the front door**:
ask it where to start and it routes you to the right skill.

## Quick start

1. Copy the `.claude/skills/` folder into your project (or into `~/.claude/skills/` to make
   the skills available everywhere). Claude Code auto-discovers skills from `.claude/skills/`
   in the working directory and every parent directory.
2. Just describe what you need in plain language — skills trigger automatically. Or start the
   orchestrator explicitly with `/senior-pm`.
3. Helper scripts need only **Python 3** (standard library, nothing to install). Every script
   supports `--help`.

**Example conversation**

> **You:** "I've been asked to launch a customer self-service portal. Where do I start?"
> **Claude (`senior-pm`):** asks a few triage questions, recommends a hybrid approach, then
> routes you to `project-initiation` → `project-charter` to authorize the work, and on to
> `project-planning` to build the plan.

## How it works

- **Four tiers.** `senior-pm` (orchestrator) → four **lifecycle phase** skills (initiation,
  planning, delivery, closure) → six cross-cutting **disciplines** (stakeholders, risk, cost,
  quality, communication, change) → eleven focused **artifact** skills (charter, WBS, schedule,
  status report, …) you can invoke on their own.
- **Progressive disclosure.** A `SKILL.md` stays short; depth lives in `references/*.md` that
  Claude reads only when needed, fill-in templates in `assets/`, and runnable tools in
  `scripts/` that execute without loading their code into context.
- **Methodology-agnostic.** Every skill has a *Methodology fit* section showing how it adapts
  for waterfall, agile, and hybrid. Ask `senior-pm` for a recommendation.

## Skill catalog

| Tier | Skill | Phase | What it does | Helper script | Triggers when you say… |
|---|---|---|---|---|---|
| 0 · Orchestrator | `senior-pm` | cross-cutting | Diagnose stage & health, recommend methodology, route to the right skill | — | "help me run my project", "where do I start", "what's the next PM step" |
| 1 · Lifecycle | `project-initiation` | initiation | Stand up a project: business case, charter, stakeholders, kickoff | — | "start a project", "kick off", "new initiative" |
| 1 · Lifecycle | `project-planning` | planning | Build the integrated plan & baseline (scope, schedule, cost, resources, risk, quality, comms) | `capacity_check.py` | "plan the project", "build a project plan", "are we over-allocated" |
| 1 · Lifecycle | `project-delivery` | delivery | Execute and monitor/control: progress, issues, changes, status, steering | — | "we're in delivery", "track progress", "manage execution" |
| 1 · Lifecycle | `project-closure` | closure | Close out: acceptance, handover, benefits, lessons, admin/financial closure | — | "close the project", "wrap up", "project closure" |
| 2 · Discipline | `stakeholder-management` | cross-cutting | Identify, analyze, and engage stakeholders (power/interest, engagement) | — | "stakeholder analysis", "power/interest grid", "engagement plan" |
| 2 · Discipline | `risk-management` | cross-cutting | End-to-end risk process: identify, analyze, respond, govern | — | "manage risk", "risk response", "risk strategy" |
| 2 · Discipline | `cost-management` | cross-cutting | Estimate, baseline, and control budget; earned value & forecasting | `health_check.py` | "budget", "earned value", "is the project on budget" |
| 2 · Discipline | `quality-management` | cross-cutting | Acceptance criteria, definition of done, quality gates, reviews | — | "definition of done", "quality plan", "acceptance criteria" |
| 2 · Discipline | `project-communication` | cross-cutting | Communication plan: audiences, channels, cadence, escalation | — | "communication plan", "comms plan", "who do we update" |
| 2 · Discipline | `change-management` | cross-cutting | Govern change: change-control process and organizational adoption | — | "change control", "manage change", "adoption" |
| 3 · Artifact | `project-charter` | initiation | Produce a charter that authorizes the project | — | "project charter", "project brief", "mandate" |
| 3 · Artifact | `business-case` | initiation | Justify the investment: options, benefits, NPV/ROI/payback | `roi_npv.py` | "business case", "ROI", "is it worth it" |
| 3 · Artifact | `work-breakdown-structure` | planning | Decompose scope into verifiable work packages (100% rule) | `wbs_validate.py` | "WBS", "break down the scope", "work packages" |
| 3 · Artifact | `project-schedule` | planning | Build/analyze the schedule; critical path, slack, duration | `critical_path.py` | "schedule", "critical path", "timeline", "Gantt" |
| 3 · Artifact | `estimation` | planning | Estimate effort/duration/cost (analogous, parametric, PERT, story points) | `pert_estimate.py` | "estimate", "PERT", "three-point", "story points" |
| 3 · Artifact | `raci-matrix` | planning | Build and validate a responsibility assignment matrix | `raci_validate.py` | "RACI", "who's responsible", "responsibility matrix" |
| 3 · Artifact | `risk-register` | cross-cutting | Produce/maintain the risk register; score by exposure/EMV | `risk_score.py` | "risk register", "risk log", "prioritize risks" |
| 3 · Artifact | `status-report` | delivery | Produce concise RAG status reports | — | "status report", "weekly update", "RAG status" |
| 3 · Artifact | `change-request` | delivery | Capture and assess a single change through to a decision | `change_impact.py` | "change request", "raise a change", "change impact" |
| 3 · Artifact | `meeting-management` | cross-cutting | Agendas, facilitation, decisions, and action items | — | "meeting agenda", "run a standup", "steering committee" |
| 3 · Artifact | `lessons-learned` | closure | Capture, categorize, and operationalize lessons | — | "lessons learned", "retrospective", "post-mortem" |

## Helper scripts

All scripts are Python 3, **standard library only** (no install), accept **CSV or JSON**
(`--json`) plus `-` for stdin, and print an aligned table. Run any with `--help`.

| Script | Skill | Computes | Example |
|---|---|---|---|
| `risk_score.py` | `risk-register` | Exposure (prob × impact), EMV, HIGH/MEDIUM/LOW bands | `python .claude/skills/risk-register/scripts/risk_score.py .claude/skills/risk-register/assets/risk-register-template.csv` |
| `pert_estimate.py` | `estimation` | Three-point PERT mean/std + confidence ranges | `python .claude/skills/estimation/scripts/pert_estimate.py .claude/skills/estimation/assets/estimation-worksheet.csv` |
| `critical_path.py` | `project-schedule` | Critical path, slack, project duration (CPM) | `python .claude/skills/project-schedule/scripts/critical_path.py .claude/skills/project-schedule/assets/schedule-template.csv` |
| `health_check.py` | `cost-management` | Earned value: CV/SV/CPI/SPI/EAC + RAG | `python .claude/skills/cost-management/scripts/health_check.py .claude/skills/cost-management/assets/cost-baseline.csv` |
| `roi_npv.py` | `business-case` | NPV, ROI, payback period | `python .claude/skills/business-case/scripts/roi_npv.py .claude/skills/business-case/assets/cashflows.csv` |
| `wbs_validate.py` | `work-breakdown-structure` | 100% rule, orphans, duplicate IDs | `python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py .claude/skills/work-breakdown-structure/assets/wbs.csv` |
| `raci_validate.py` | `raci-matrix` | Exactly one A, at least one R, overload checks | `python .claude/skills/raci-matrix/scripts/raci_validate.py .claude/skills/raci-matrix/assets/raci-template.csv` |
| `change_impact.py` | `change-request` | Weighted scope/cost/schedule impact score | `python .claude/skills/change-request/scripts/change_impact.py .claude/skills/change-request/assets/change-log.csv` |
| `capacity_check.py` | `project-planning` | Utilization, over/under-allocation flags | `python .claude/skills/project-planning/scripts/capacity_check.py .claude/skills/project-planning/assets/resource-allocation.csv` |

## Methodology guidance

| Need | Waterfall | Agile | Hybrid |
|---|---|---|---|
| Authorize | Formal `project-charter`, signed off before planning | Lightweight charter / project brief | Charter fixes outcomes; approach stays flexible |
| Plan | Full `project-planning` baseline up front | Rolling-wave; backlog + `estimation` (story points) | Baseline the fixed parts, iterate the rest |
| Schedule | `project-schedule` critical path, Gantt | Iteration/sprint cadence | Milestones + iterations |
| Track | `cost-management` earned value, `status-report` | Burndown + `status-report` | Both |
| Change | `change-management` formal change control | Re-prioritize the backlog | Control baselined scope, flex the rest |
| Close | `project-closure` + `lessons-learned` | Iteration retro + final `lessons-learned` | Both |

Not sure which applies? Ask **`senior-pm`** for a recommendation based on your project.

## Repository layout

```
.claude/skills/<skill-name>/
├── SKILL.md            # the instructions Claude follows (< 500 lines)
├── references/*.md     # deeper guides, loaded only when needed
├── assets/*            # fill-in templates (.md) and sample data (.csv)
└── scripts/*.py        # dependency-free helpers, run on demand
tools/lint_skills.py    # validates the catalog's conventions
```

## Conventions / contributing

Every skill follows the same shape so the set stays consistent:

- **Frontmatter.** Required `name` (kebab-case, equals the folder name, ≤ 64 chars, no reserved
  words) and `description` (third person, ≤ 1024 chars, says **what** it does **and when** to use
  it with trigger synonyms). Plus `metadata` (`version`, `category` =
  orchestrator/phase/discipline/artifact, `phase`, `related`) and `license: MIT`.
- **Body sections** (in order): Overview · When to use this skill · Methodology fit · Inputs you
  need · Workflow · Quality checklist · Anti-patterns · Resources · Related skills.
- **Cross-links are reciprocal.** If skill A lists B in `related`, B lists A. Reference skills by
  their exact backticked folder name.
- **Scripts are stdlib-only**, take CSV/JSON, support `--help`, and ship with a sample input in
  `assets/` that doubles as the template.

Validate everything with the linter (folder/name match, frontmatter rules, reciprocal links,
dead/orphan file links, body length):

```bash
python tools/lint_skills.py
```

## License

MIT — see [LICENSE](LICENSE).
