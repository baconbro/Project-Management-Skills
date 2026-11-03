# Project Management Skills

A methodology-agnostic catalog of **27 Agent Skills** that turn Claude into a **senior
project manager**. It helps anyone **initiate, plan, deliver and close** a project, whether
the project runs as waterfall, agile or hybrid.

The skills use the [Agent Skills](https://code.claude.com/docs/en/skills) format, which
works in Claude Code, Claude Desktop and Web, Cowork, Codex and other AI agents.

**What's inside**
- **27 skills** that link to each other.
- **11 helper scripts**: dependency-free Python that does the arithmetic (NPV, PERT,
  critical path, earned value, Monte Carlo and more).
- **100+ templates and filled samples** that you can copy.
- **60+ reference guides**.
- **One worked example**, "Helios", that runs through every skill.
- **Tooling**: a linter, a script test harness and CI that keep the catalog consistent.

## Install

The catalog is packaged as one plugin, `project-management-skills`, so it installs the same way
everywhere you use Claude. Pick your surface.

**Claude.ai, Claude Desktop and Cowork**

- From Anthropic's directory, once the listing is live: open **Customize → Plugins →
  Discover**, search for *Project Management Skills* and add it. A plugin added there also
  reaches your Claude Code sessions as a synced plugin.
- From a file: download `project-management-skills-plugin.zip` from the latest
  [release](https://github.com/baconbro/Project-Management-Skills/releases) and use
  **Customize → Plugins → Add → Upload plugin**. To install single skills instead, the same
  release has one ZIP per skill for **Customize → Skills → + → Create skill → Upload a skill**.
- Team and Enterprise: an Owner can publish the plugin for the organisation under
  **Organization settings → Plugins & skills** and set it to *Installed by default*.

**Claude Code**

```text
/plugin marketplace add baconbro/Project-Management-Skills
/plugin install project-management-skills@baconbro-pm-skills
```

Or in one step on Claude Code 2.1.275 or later:
`/plugin install project-management-skills --marketplace baconbro/Project-Management-Skills`.
Update with `/plugin update project-management-skills@baconbro-pm-skills`. Plugin skills carry
the plugin's name, so the front door is `/project-management-skills:senior-pm`; plain-language
triggering works exactly as before.

**Copy the folder, no plugin**

Copy `.claude/skills/` into your repository, or into `~/.claude/skills/` for every project.
Claude Code discovers skills in `.claude/skills/` in the directory where you start it and in
every parent directory up to the repository root, and invokes them as `/senior-pm`. Do not
combine this with the plugin in the same repository, or each skill loads twice.

**What the plugin contains and runs.** Everything is text: `SKILL.md` instructions, Markdown
references, CSV and Markdown templates, and standard-library Python scripts that run locally on
the files you give them. There are no hooks, MCP servers, executables or network calls, and
nothing is sent anywhere.

## Quick start

1. Install the skills (above).
2. Describe what you need in plain language and the right skill triggers on its own. You can
   also start the front door explicitly with `/senior-pm`.
3. The helper scripts need only **Python 3**, with nothing to install. Every script supports
   `--help`. If your system only has `python3` (stock macOS, Debian/Ubuntu), use `python3`
   wherever the commands say `python`.

All 27 descriptions together fit in about 7,600 characters, so the whole catalog fits Claude
Code's skill-listing budget. That budget is about 1% of the context window and is shared
with any other skills you have installed. If `/context` shows skill descriptions being
dropped, raise `skillListingBudgetFraction` in your settings, or set skills you never use to
`"name-only"` under `skillOverrides`.

**Example conversation**

> **You:** "I've been asked to launch a customer self-service portal. Where do I start?"
> **Claude (`senior-pm`):** asks a few triage questions, records the answers in a one-table
> project-state canvas and recommends a hybrid approach. It then sends you to
> `project-initiation`, which takes you through `business-case` and `project-charter` to
> authorize the work, and on to `project-planning` to build the baseline.

**Try the helpers on the sample data** (from the repo root):

```bash
python .claude/skills/project-schedule/scripts/critical_path.py .claude/skills/project-schedule/assets/schedule-sample.csv --unit weeks --gantt
python .claude/skills/cost-management/scripts/health_check.py .claude/skills/cost-management/assets/evm-snapshot.csv
python .claude/skills/risk-register/scripts/risk_score.py .claude/skills/risk-register/assets/risk-register-template.csv --bac 500000
```

## How it works

- **Four tiers.**
  - `senior-pm`, the orchestrator and front door.
  - Four **lifecycle phase** skills: initiation, planning, delivery and closure.
  - Nine **disciplines**, such as risk, cost, resources and procurement.
  - Thirteen focused **artifact** skills, such as charter, WBS, schedule, status report and
    cutover runbook. You can use any of these on its own.
- **Front door and routing.** `senior-pm` triages the project's lifecycle stage and its health
  against the baseline. It then routes you to at most two specialist skills, each with a first
  action. Its `references/routing-map.md` maps every request and symptom to a skill.
- **Progressive disclosure.** A `SKILL.md` stays short. Deeper guidance lives in
  `references/*.md`, which Claude reads only when needed. `assets/` holds the files you fill
  in, and `scripts/` holds tools that run without loading their code into context.
- **Done criteria.** Every workflow step ends with *Done:*, the evidence that the step is
  complete. Every skill also has a quality checklist and a list of anti-patterns.
- **Templates and samples.** Blank fill-in files are named `*-template.*` or carry
  `<placeholders>`. Filled versions of the Helios example are named `*-sample.*`. When a CSV is
  also a script's sample input, it holds the Helios rows: replace the rows and keep the header.
  `cost-management/assets/cost-baseline-template.csv` is also pre-filled with the Helios rows
  in the same way.
- **Methodology-agnostic.** Every skill has a *Methodology fit* section that shows how it adapts
  to waterfall, agile and hybrid delivery.

## Skill catalog

| Tier | Skill | Phase | What it does | Helper script | Triggers when you say… |
|---|---|---|---|---|---|
| 0 · Orchestrator | `senior-pm` | cross-cutting | Triages the project's stage and health, keeps a project-state canvas, recommends waterfall, agile or hybrid, routes to the right skill, and holds the PM glossary and the Helios walkthrough | — | "where do I start", "is my project on track", "waterfall or agile" |
| 1 · Lifecycle | `project-initiation` | initiation | Takes an idea to a planning-ready project: business case, delivery approach, signed charter, stakeholders, an initiation gate with a recorded verdict, and the kickoff | — | "start a new project", "initiation gate", "what should the kickoff cover" |
| 1 · Lifecycle | `project-planning` | planning | Builds the integrated plan and baseline in one ordered pass (scope, WBS, make-or-buy, estimates, staffing, schedule, risk, quality, cost, communications, change control) and reconciles the parts for one approval | — | "project management plan", "set the baseline", "reconcile the plan" |
| 1 · Lifecycle | `project-delivery` | delivery | Runs a baselined project day to day: tracks progress, accepts deliverables, keeps one issue/action/decision/dependency log, escalates, and sets an interim baseline for a running project that has none | `issue_log_check.py` | "track progress against the baseline", "log an issue", "project already running with no baseline" |
| 1 · Lifecycle | `project-closure` | closure | Gets formal acceptance, hands over to operations, disposes of open items and contracts, reconciles final cost, and runs the post-project review and closure report, including for a cancelled project | — | "close the project", "handover to operations", "cancel the project" |
| 2 · Discipline | `stakeholder-management` | cross-cutting | Builds the stakeholder register, places each stakeholder on the power/interest grid by an explicit rule, compares current with desired engagement, and assigns engagement actions | — | "stakeholder analysis", "the sponsor has gone quiet", "a stakeholder is blocking us" |
| 2 · Discipline | `risk-management` | cross-cutting | Runs the risk process: a risk plan with appetite and thresholds, identification, quantification, responses, a contingency reserve sized at a confidence level, and governance | — | "risk workshop", "pre-mortem", "how much contingency" |
| 2 · Discipline | `cost-management` | cross-cutting | Sets the cost baseline and reserves, then controls cost with earned value (CPI/SPI, EAC, TCPI) and a RAG verdict | `health_check.py` | "earned value", "CPI", "forecast at completion", "over budget" |
| 2 · Discipline | `resource-management` | cross-cutting | Plans the team: roles, capacity versus allocation, leveling and smoothing, the team charter, onboarding and release | `capacity_check.py` | "who is over-allocated", "resource leveling", "team charter" |
| 2 · Discipline | `quality-management` | cross-cutting | Plans quality, separates assurance from control, sets the cost of quality, definition of done, quality gates, process audits and the defect log | — | "definition of done", "quality gate", "QA vs QC" |
| 2 · Discipline | `project-communication` | cross-cutting | Builds the communication plan: who needs what, in which mode, channel and cadence, plus the escalation ladder and checks that messages land | — | "communication plan", "who needs to know", "escalation path" |
| 2 · Discipline | `change-management` | cross-cutting | Governs change control (CCB, tolerances, emergency route, freezes) and change adoption (ADKAR, readiness, resistance) | — | "change control board", "scope creep", "user adoption" |
| 2 · Discipline | `agile-delivery` | delivery | Runs the backlog, stories, sprints, velocity and burnup, forecasts a release as a range with a cut line, and maps story points onto hybrid baselines | `velocity_forecast.py` | "plan the next sprint", "how many sprints are left", "user stories" |
| 2 · Discipline | `procurement-management` | cross-cutting | Covers make-or-buy, statements of work, RFI/RFQ/RFP, weighted vendor scoring, contract type and risk allocation, then vendor performance, acceptance and closure | — | "make or buy", "statement of work", "my vendor is late" |
| 3 · Artifact | `project-charter` | initiation | Writes the charter that authorizes the project, with SMART objectives, PM authority, boundaries and cancellation criteria, and checks the sponsor's sign-off | — | "project charter", "project brief", "cancellation criteria" |
| 3 · Artifact | `business-case` | initiation | Builds the investment case: options against do-nothing, benefits with owners, whole-life cost, NPV/IRR/ROI/payback, sensitivity and the funding decision | `roi_npv.py` | "business case", "NPV", "IRR", "do-nothing option" |
| 3 · Artifact | `scope-and-requirements` | planning | Elicits requirements with MoSCoW priorities and acceptance tests, writes the scope statement, builds the traceability matrix, and runs scope validation | — | "requirements gathering", "scope statement", "is this in scope" |
| 3 · Artifact | `work-breakdown-structure` | planning | Decomposes scope into work packages (100% rule) with a WBS dictionary, validates and rolls up weights, and exports the packages for estimation | `wbs_validate.py` | "WBS", "work packages", "100% rule" |
| 3 · Artifact | `estimation` | planning | Estimates with analogous, parametric, PERT, story-point and Delphi techniques, gives P50/P80/P90 commit levels, and runs a PERT-Beta simulation | `pert_estimate.py` | "estimate", "three-point", "P80", "planning poker" |
| 3 · Artifact | `project-schedule` | planning | Finds the critical path and float, maps tasks to calendar dates, draws a text Gantt, runs a Monte Carlo schedule risk, and supports compression | `critical_path.py` | "critical path", "Gantt chart", "how long will the project take" |
| 3 · Artifact | `raci-matrix` | planning | Builds and validates a RACI, RASCI or DACI with one Accountable per row, suggests fixes, and summarises each role's workload | `raci_validate.py` | "RACI", "who is accountable for", "decision rights" |
| 3 · Artifact | `risk-register` | cross-cutting | Keeps the register of threats and opportunities and scores it by EMV into bands, with residual exposure, a Monte Carlo reserve and pre-review checks | `risk_score.py` | "risk register", "rank the risks", "risk exposure" |
| 3 · Artifact | `status-report` | delivery | Writes the evidence-first status report: RAG ratings against tolerances on the forecast, trend, owners for amber and red items, and decisions requested | — | "status report", "RAG status", "why is my project amber" |
| 3 · Artifact | `change-request` | delivery | Takes one change request from description to recorded decision, keeps the change log, and scores impact, approval route and change burden | `change_impact.py` | "change request", "assess a change", "who approves this change" |
| 3 · Artifact | `release-and-cutover` | delivery | Covers release strategy, go-live readiness, the go/no-go verdict, a rehearsed cutover runbook with rollback triggers, and hypercare through to handover | — | "go/no-go decision", "cutover runbook", "we go live next week" |
| 3 · Artifact | `meeting-management` | cross-cutting | Runs kickoffs, steering committees, stand-ups and workshops with a purpose, a timeboxed agenda, a decision method, and live decisions and actions | — | "meeting agenda", "steering committee meeting", "our meetings go nowhere" |
| 3 · Artifact | `lessons-learned` | cross-cutting | Runs retrospectives and blameless post-mortems, finds root causes, and turns lessons into owned, dated actions that are later checked | — | "retrospective", "post-mortem", "5 whys" |

### The lifecycle at a glance

| Stage | Start with | Then, as needed |
|---|---|---|
| Initiate | `project-initiation` | `business-case` → `project-charter` → `stakeholder-management`, `meeting-management` (kickoff) |
| Plan | `project-planning` | `scope-and-requirements` → `work-breakdown-structure` → `procurement-management` → `estimation` → `raci-matrix` + `resource-management` + `project-schedule` (leveled together) → `risk-management` / `risk-register` → `quality-management` + `release-and-cutover` (transition plan) → `cost-management` → `stakeholder-management` → `project-communication` → `change-management` |
| Deliver | `project-delivery` | `agile-delivery`, `status-report`, `change-request`, `risk-register`, `cost-management`, `meeting-management`, `release-and-cutover` |
| Close | `project-closure` | `lessons-learned`, `procurement-management` (contract closure) |

Not sure where you are? Ask `senior-pm`.

## Helper scripts

Every script is Python 3 and uses the **standard library only**. They all follow one input and
output contract:

- **Input.** A CSV or JSON file (`--json`), or `-` to read stdin. Scripts strip a UTF-8 BOM,
  accept CRLF line endings, and detect `,` `;` tab or `|` as the delimiter. Numbers may contain
  `$` and `%`. A `,` followed by groups of three digits is a thousands separator (`1,000`,
  `12,345.67`); a `,` followed by one or two digits is a decimal comma (`2,5` is 2.5, `37,50`
  is 37.5). Any other comma, such as `1.000,50`, is rejected as ambiguous. The scripts also
  reject `nan`, `inf`, booleans, values above each script's upper bound (for example 1e15 for
  money) and missing columns, and the error message lists the headers they found.
  `--format json` output never contains `NaN` or `Infinity`.
- **Output.** `--format table` (the default), `json`, `csv` or `md` (`issue_log_check.py` offers
  table, json and csv). Use `md` to paste into a status report and `json` to feed a pipeline.
- **Exit codes.** `0` means ok. `1` means a validation failure from a checker (`wbs_validate`,
  `raci_validate`, `issue_log_check`, `risk_score --check`, `capacity_check --fail-on`). `2`
  means bad input, reported as `error: …` on stderr and never as a traceback.
- **Help.** `--help` documents the columns, formulas and exit codes, with examples.

| Script | Skill | Computes | Notable options |
|---|---|---|---|
| `roi_npv.py` | `business-case` | NPV, IRR, ROI, simple and discounted payback, per-option comparison ranked by NPV | `--irr` `--break-even` (switching values) `--sensitivity` `--stress` `--all` |
| `pert_estimate.py` | `estimation` | PERT mean, standard deviation and variance share per item, P50/P80/P90 commit levels, contingency reserve | `--confidence P80` `--simulate N` `--ids` (one chain) |
| `critical_path.py` | `project-schedule` | ES/EF/LS/LF, total and free float, every critical path, near-critical tasks, calendar dates, Gantt | `--unit weeks` `--gantt` `--start-date` `--workdays` `--target` `--simulate N` |
| `wbs_validate.py` | `work-breakdown-structure` | Hierarchy and 100% rule checks, suggested weights, roll-up to shares of the project and budget | `--suggest` `--fix OUT.csv` `--rollup --budget` `--export-estimation` |
| `raci_validate.py` | `raci-matrix` | Exactly one A, at least one R (DACI: one D), contradictory cells, ghost and overloaded roles, single points of failure, role workload | `--variant raci\|rasci\|daci` `--fix` `--fix-out` `--transpose` |
| `capacity_check.py` | `resource-management` | Utilization per person and period, OVER/HIGH/OK/UNDER flags, headroom, key-person risk, leveling plan | `--level` `--target` `--period` `--fail-on over` |
| `risk_score.py` | `risk-register` | Exposure and EMV bands, residual exposure, net EMV, Monte Carlo of total threat exposure, governance checks | `--bac` `--basis residual` `--simulate N --reserve X` `--check` `--top N` |
| `health_check.py` | `cost-management` | CV/SV, CPI/SPI, EAC/ETC/VAC, TCPI, percent complete, RAG verdict, trend and text S-curve over periods | `--eac-method all` `--bac` `--incremental` `--sort worst` |
| `change_impact.py` | `change-request` | Weighted five-dimension impact band, routing to PM, CCB or sponsor, change burden against reserve, sensitivity to the weights | `--reserve-cost` `--pm-limit-cost` `--sensitivity` `--explain` |
| `velocity_forecast.py` | `agile-delivery` | Velocity and predictability, burnup, sprints left as optimistic, likely and pessimistic, scope-growth warning | `--backlog` `--remaining` `--sprints-left` (cut line) `--window` |
| `issue_log_check.py` | `project-delivery` | Issue-log hygiene, plus items overdue, due soon, blocked or awaiting steering, and each owner's open load | `--as-of` `--days` `--risks` (cross-check the register) `--strict` |

Each command below runs on the bundled Helios sample, from the repo root:

```bash
S=.claude/skills
python $S/business-case/scripts/roi_npv.py $S/business-case/assets/cashflows.csv --irr --break-even
python $S/business-case/scripts/roi_npv.py $S/business-case/assets/cashflows-options-sample.csv
python $S/estimation/scripts/pert_estimate.py $S/estimation/assets/estimation-worksheet-sample.csv --confidence P80
python $S/project-schedule/scripts/critical_path.py $S/project-schedule/assets/schedule-sample.csv --unit weeks --gantt
python $S/work-breakdown-structure/scripts/wbs_validate.py $S/work-breakdown-structure/assets/wbs-sample.csv --rollup --budget 500000
python $S/raci-matrix/scripts/raci_validate.py $S/raci-matrix/assets/raci-sample.csv
python $S/resource-management/scripts/capacity_check.py $S/resource-management/assets/resource-allocation-sample.csv --level
python $S/risk-register/scripts/risk_score.py $S/risk-register/assets/risk-register-template.csv --bac 500000
python $S/risk-register/scripts/risk_score.py $S/risk-register/assets/risk-register-template.csv --basis residual --simulate 10000 --seed 42 --reserve 40000
python $S/cost-management/scripts/health_check.py $S/cost-management/assets/evm-snapshot.csv
python $S/cost-management/scripts/health_check.py $S/cost-management/assets/evm-history-sample.csv
python $S/change-request/scripts/change_impact.py $S/change-request/assets/change-log.csv --reserve-cost 40000
python $S/agile-delivery/scripts/velocity_forecast.py $S/agile-delivery/assets/sprint-history-sample.csv --backlog $S/agile-delivery/assets/product-backlog-sample.csv
python $S/project-delivery/scripts/issue_log_check.py $S/project-delivery/assets/issue-log-sample.csv --as-of 2026-07-10
```

## The worked example: Helios

Every skill uses the same **fictional** project, so the artifacts agree with each other and you
can follow one story from idea to closure. Helios is a customer self-service portal that cuts
password-reset and order-status tickets by 50%. Its key numbers:

| | |
|---|---|
| Sponsor and PM | Dana Okoro (VP Customer Operations), sponsor; Sam Lee, project manager |
| Business case | Invest $500,000, NPV $196,174 at 10%, IRR 23.6%, payback 2.85 years |
| Budget | BAC $500,000, which includes $40,000 of contingency (about P50 of the residual risk simulation); $25,000 of management reserve sits above BAC |
| Schedule | 6 months. Critical path of 25 weeks (A→B→D→G→H→J), 2026-04-06 to 2026-09-25; pilot (M4) 2026-08-07; GA cutover (M6) 2026-10-03. No schedule reserve before GA: the simulated P80 is 28.25 weeks, and the 2-week M6 tolerance covers about P75 |
| Risk | Six risks R001-R006, one of them an opportunity. Threat EMV is $94,300, or $52,300 after responses |
| Month-3 health | CPI 0.93, SPI 0.92, so **AMBER**; EAC about $535,000 |
| Change | Change requests CR001-CR006; SSO stays in the baseline |

For the end-to-end story, with each stage's artifacts and commands, see
[`senior-pm/references/helios-walkthrough.md`](.claude/skills/senior-pm/references/helios-walkthrough.md).

## Methodology guidance

| Need | Waterfall | Agile | Hybrid |
|---|---|---|---|
| Authorize | Formal `project-charter`, signed before planning starts | Lightweight charter or project brief | The charter fixes outcomes and constraints; the approach stays flexible |
| Define scope | Scope statement and traceability matrix (`scope-and-requirements`), then the full WBS | Product backlog of INVEST stories (`agile-delivery`), MoSCoW priorities | Baseline the scope statement and grow the detail through the backlog |
| Plan and estimate | `project-planning` baseline, PERT (`estimation`), critical path (`project-schedule`) | Rolling wave, story points and planning poker, velocity forecast | Baseline milestones and budget, and run sprints inside them |
| Staff | `resource-management` capacity and leveling | A stable team with sprint capacity | Both |
| Track | Earned value (`cost-management`) and `status-report` | Velocity range and burnup (`agile-delivery`) with `status-report` | Map points to earned value and keep one status report |
| Change | CCB and tolerances (`change-management`), `change-request` | Re-order the backlog; the product owner decides within the sprint goal | Control the baseline and flex the backlog below the cut line |
| Release | Big-bang or phased cutover (`release-and-cutover`) | Incremental releases and feature flags | A pilot, then general availability |
| Close | `project-closure` and `lessons-learned` | Sprint retrospectives, then a final review | Both |

For a recommendation based on your project, ask **`senior-pm`**. Its
`references/methodology-selection.md` explains how it chooses.

## Repository layout

```
.claude/skills/<skill-name>/
├── SKILL.md            # the instructions Claude follows (< 500 lines)
├── references/*.md     # deeper guides, loaded only when needed
├── assets/*            # fill-in templates and filled Helios samples (.md, .csv)
└── scripts/*.py        # dependency-free helpers, run on demand
.claude-plugin/plugin.json       # the plugin manifest: name, version, where the skills are
.claude-plugin/marketplace.json  # lets Claude Code install the plugin from this repository
tools/lint_skills.py    # checks the catalog's conventions
tools/test_scripts.py   # tests every helper script against its sample and the I/O contract
.github/workflows/validate.yml   # lint, tests and plugin validation on PRs and pushes to main
.github/workflows/release.yml    # on a version tag, builds the plugin and per-skill ZIPs
```

## Quality checks and CI

```bash
python tools/lint_skills.py      # conventions: exits non-zero on any error
python tools/test_scripts.py     # 688 checks across the 11 helper scripts
```

Install PyYAML (`python -m pip install pyyaml`) for the same strict frontmatter parsing CI
uses. Without it the linter falls back to a minimal parser and says so.

**The linter** checks the following:
- Every folder under `.claude/skills/` has a `SKILL.md`; a lowercase or other case variant is
  an error, because the skill would not load.
- Frontmatter: name, description, version, category and phase; `license: MIT`; no top-level
  keys other than `name`, `description`, `license`, `compatibility`, `metadata` and
  `allowed-tools`, which must be a string or a list of strings.
- Related links resolve, never point at the skill itself, are reciprocal, and match the
  *Related skills* bullets in the same order.
- The canonical sections are present and in order, every Workflow step has a *Done:* line,
  and the body stays under 500 lines.
- No placeholder text such as `TODO` or `TBD` in SKILL.md.
- Every file the skills name exists: references in SKILL.md, pointers inside `references/` and
  `assets/` Markdown, and paths in this README. A `$S/<skill>/…` or `.claude/skills/<skill>/…`
  path must exist in that skill, and an unqualified path in a skill's own Markdown must exist
  in that skill. Files that SKILL.md never mentions are flagged.
- This README's skill count and catalog table match the frontmatter (tier and phase per skill).
- Every CSV under `assets/` is UTF-8 and has as many cells on every row as its header, which
  catches an unquoted comma inside a cell.
- The skill descriptions stay inside Claude Code's skill-listing budget (a warning above 350
  characters per skill or 8,000 for the catalog).
- Every script's `--help` runs.

**The test harness** runs each script in these ways and checks the result:
- On its sample, and again through stdin, as JSON, with a BOM, with CRLF line endings, with
  semicolons and with semicolons plus decimal commas. All of these must give identical output.
- The canon Helios numbers the samples must produce, such as NPV $196,173.88, the 25-week
  critical path A→B→D→G→H→J, CPI 0.93 and SPI 0.92 (AMBER), and threat EMV $94,300.
- Every `--format` the script offers, with valid JSON from `--format json`.
- On empty, header-only, `nan`, JSON `true` and `Infinity`, ambiguous-number (`1.000,50`) and
  malformed-JSON input, which must give a clean `error:` and exit 2.
- For the validators and gates (`wbs_validate`, `raci_validate`, `issue_log_check`,
  `risk_score --check`, `capacity_check --fail-on over`), on a deliberately broken input, which
  must exit 1.

## Conventions and contributing

Every skill has the same shape, which keeps the set consistent:

- **Frontmatter.**
  - Required: `name`, which is kebab-case, equals the folder name, is at most 64 characters and
    contains no reserved words.
  - Required: `description`, which is third person and has no angle brackets. It says what
    the skill does and when to use it ("Use when…") in one or two sentences of at most about
    300 characters. Claude Code shows every skill's name but fits the descriptions into a
    small listing budget, so the whole catalog stays under 8,000 characters (the linter
    warns above 350 per skill). The detailed trigger phrases and the "use another skill
    for…" redirections go in the body's *When to use this skill* section.
  - Also: `metadata` (`version`; `category` of orchestrator, phase, discipline or artifact;
    `phase`; `related`) and `license: MIT`.
- **Body sections, in this order:** Overview · When to use this skill · Methodology fit · Inputs
  you need · Workflow (numbered steps, each ending with *Done:*) · Quality checklist ·
  Anti-patterns · Resources · Related skills.
- **Cross-links are reciprocal.** If skill A lists B in `related`, B lists A. Refer to skills by
  their exact backticked folder name.
- **Templates and samples are separate files** (`*-template`, `*-sample`). Samples follow the
  Helios example.
- **Scripts follow the I/O contract** described under [Helper scripts](#helper-scripts). Each
  ships with a sample input in `assets/` and an entry in `tools/test_scripts.py`.

Before you open a pull request, run `python tools/lint_skills.py` and
`python tools/test_scripts.py`.

## License

MIT — see [LICENSE](LICENSE).
