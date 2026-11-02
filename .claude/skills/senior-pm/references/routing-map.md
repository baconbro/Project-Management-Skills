# Routing map — situation to skill

Load this to send the user to the right skill. Rules, in order:

1. **Diagnose the stage first** (SKILL.md step 2); a symptom means different things in
   planning and in delivery.
2. **Pick the tier by the shape of the ask.** "Where do I start / what next in this phase" →
   the phase skill. "Set up the process for X" → the discipline skill. "Make me an X" or
   "compute X" → the artifact skill.
3. **Route to at most two skills**, name each in backticks, and give the first action and the
   artifact the user should expect back.
4. **Use the tie-break table** when a phrase matches two skills. Never invent a skill name:
   if nothing below fits, say so and route to the phase skill for the current stage.

## The 27 catalog skills

| Skill | Tier | Phase | What it does | Helper script |
|---|---|---|---|---|
| `senior-pm` | orchestrator | cross-cutting | Triage stage and health, recommend an approach, route (this skill) | — |
| `project-initiation` | phase | initiation | Stand up a project: need, business case, charter, stakeholders, kickoff | — |
| `project-planning` | phase | planning | Integrate scope, schedule, cost, resources, risk, quality and comms into one plan; approve the baseline | — |
| `project-delivery` | phase | delivery | Execute and control: progress vs baseline, one log of issues, actions, decisions and dependencies, acceptance, escalation; a one-day interim baseline for a running project without one | `issue_log_check.py` |
| `project-closure` | phase | closure | Acceptance, handover, benefits tracking, lessons, administrative and financial closure | — |
| `stakeholder-management` | discipline | cross-cutting | Identify, map (power/interest, salience) and engage stakeholders | — |
| `risk-management` | discipline | cross-cutting | The risk process: identify, analyse (incl. EMV, decision trees, Monte Carlo), respond, govern; size contingency | — |
| `cost-management` | discipline | cross-cutting | Cost baseline, reserves, S-curve, earned value, EAC and cost RAG | `health_check.py` |
| `quality-management` | discipline | cross-cutting | Quality plan, cost of quality, acceptance-criteria standard, definition of done, quality gates, process audits (QA) and the defect log (QC) | — |
| `project-communication` | discipline | cross-cutting | Communication plan: audiences, channels, cadence, escalation paths | — |
| `change-management` | discipline | cross-cutting | Change control (process, CCB, thresholds) and organizational adoption (readiness, resistance) | — |
| `agile-delivery` | discipline | delivery | Backlog, INVEST stories, definition of ready, sprints, velocity and the release forecast | `velocity_forecast.py` |
| `procurement-management` | discipline | cross-cutting | Make-or-buy, statement of work, RFI/RFQ/RFP, vendor selection, contract type, supplier performance, contract closure | — |
| `resource-management` | discipline | cross-cutting | Roles, staffing, team charter, capacity vs allocation, leveling, onboarding and release | `capacity_check.py` |
| `project-charter` | artifact | initiation | The charter that authorizes the project and names sponsor and PM | — |
| `business-case` | artifact | initiation | Options vs do-nothing, benefits, NPV/IRR/ROI/payback, funding decision | `roi_npv.py` |
| `scope-and-requirements` | artifact | planning | Requirements (MoSCoW, acceptance tests), scope statement, traceability matrix, scope validation | — |
| `work-breakdown-structure` | artifact | planning | Decompose scope into work packages (100% rule), WBS dictionary, budget by weight | `wbs_validate.py` |
| `estimation` | artifact | planning | Analogous, parametric, three-point/PERT, story points, planning poker; P50/P80 and reserve | `pert_estimate.py` |
| `project-schedule` | artifact | planning | Critical path, float, calendar dates, Gantt, compression, schedule-risk simulation | `critical_path.py` |
| `raci-matrix` | artifact | planning | RACI / RASCI / DACI with one Accountable per row | `raci_validate.py` |
| `risk-register` | artifact | cross-cutting | The register: owners, triggers, responses, EMV per risk, bands, residual exposure | `risk_score.py` |
| `status-report` | artifact | delivery | The periodic RAG status report and steering update | — |
| `change-request` | artifact | delivery | One change request from description to decision; the change log and its burden | `change_impact.py` |
| `meeting-management` | artifact | cross-cutting | Agendas, facilitation, timeboxing, decisions and action items for any meeting | — |
| `release-and-cutover` | artifact | delivery | Release strategy, go/no-go, cutover runbook, rollback, hypercare | — |
| `lessons-learned` | artifact | cross-cutting | Sprint and phase retrospectives, post-mortems and lessons with owners and follow-through, at any stage | — |

## Route by stage

| Stage | Signals | Must exist before moving on | Route |
|---|---|---|---|
| Idea | "We've been asked to...", no sponsor or budget yet | A justified need and a funding decision | `project-initiation`, then `business-case` |
| Initiation | Sponsor known, no signed charter | Signed charter, stakeholder register, kickoff held | `project-initiation` (it calls `project-charter`, `stakeholder-management`) |
| Planning | Charter signed, no approved baseline | Approved scope, schedule and cost baselines | `project-planning` (it calls the planning artifacts) |
| Delivery | Baseline approved, work running | Accepted deliverables; go-live done | `project-delivery`; `release-and-cutover` no later than six weeks (T-6) before each go-live |
| Closure | Deliverables accepted, or work stopping early | Handover, lessons, contracts and finances closed | `project-closure`, then `lessons-learned` |

A project running without a baseline is in delivery with "no baseline" as its top gap: route
to `project-delivery`, whose first step builds a one-day, sponsor-approved interim baseline
(`.claude/skills/project-delivery/assets/rebaseline-template.md`) to report against at
once. Route to `project-planning` instead when work has not started, or when the interim
baseline must be replaced by a full re-plan.

## Route by intent

| The user wants to... | Go to |
|---|---|
| Figure out where to start, get a health check, pick an approach, decode a PM term | `senior-pm` (this skill) |
| Stand up a brand-new project from an idea | `project-initiation` |
| Decide whether the investment is worth it; compute NPV, IRR, payback | `business-case` |
| Authorize the project; write a one-page mandate | `project-charter` |
| Find out who the stakeholders are and how to engage them | `stakeholder-management` |
| Gather requirements, write the scope statement, settle in/out of scope, trace requirements | `scope-and-requirements` |
| Build the integrated plan and approve the baseline | `project-planning` |
| Break the scope into work packages | `work-breakdown-structure` |
| Estimate effort, duration or cost with a confidence range | `estimation` |
| Build a schedule, find the critical path or float, compress the timeline | `project-schedule` |
| Staff the team, check who is over-allocated, level workloads, write a team charter | `resource-management` |
| Assign who is Responsible / Accountable / Consulted / Informed | `raci-matrix` |
| Set a cost baseline and reserves, track earned value, forecast the final cost | `cost-management` |
| Set up the risk process, run a pre-mortem, choose responses, size contingency | `risk-management` |
| Create, score or rank the risk register | `risk-register` |
| Define done, acceptance criteria and quality gates | `quality-management` |
| Plan who hears what, when, and how | `project-communication` |
| Decide make or buy, write a statement of work or RFP, select or manage a vendor | `procurement-management` |
| Write user stories, order a backlog, plan a sprint, track velocity or a burnup, forecast sprints left | `agile-delivery` |
| Run day-to-day execution and monitor/control; log, own or escalate a problem happening now | `project-delivery` |
| Produce a RAG status report or steering update | `status-report` |
| Set up change control or drive adoption of a new way of working | `change-management` |
| Raise, assess or decide one specific change | `change-request` |
| Run a meeting: agenda, facilitation, decisions, actions | `meeting-management` |
| Plan a go-live, go/no-go, cutover runbook, rollback or hypercare | `release-and-cutover` |
| Close the project or a phase | `project-closure` |
| Track whether promised benefits arrive after delivery | `project-closure` |
| Run a retrospective or post-mortem at any stage and turn lessons into owned actions | `lessons-learned` |

## Route by symptom

| The user says... | Likely cause | Route (at most two) | First action |
|---|---|---|---|
| "Is my project on track?" | Unknown until read against a baseline | `senior-pm` health read; if no baseline, `project-delivery` (running) or `project-planning` (not started) | Fill the canvas; rate each dimension |
| "The project is already running with no baseline" | Planning skipped or never approved | `project-delivery` | Build the one-day interim baseline and get the sponsor to approve it |
| "Log this issue" / "who do I escalate this to?" (a problem happening now) | No issue log or escalation route | `project-delivery`, then `project-communication` for the escalation ladder | Log it with one owner, priority and due date; escalate when it exceeds the owner's authority |
| "We are always late" | No critical path, optimistic estimates, or hidden dependencies | `project-schedule`, then `estimation` | Find the critical path and float; re-estimate the drivers at P80 |
| "We are over budget" | Cost variance not tracked or reserve not sized | `cost-management` | Run the earned-value check; forecast EAC |
| "Scope keeps growing" | No baseline or no change threshold | `change-management`, then `scope-and-requirements` | Baseline the scope statement if none exists; otherwise set the CR threshold and CCB and route every unapproved addition through `change-request` (approve, defer or reject); never re-baseline to absorb creep |
| "Nobody agrees what is in scope" / "is this in scope?" | No scope statement or exclusions | `scope-and-requirements` | Check the signed in/out list and the RTM; if absent, write it and get it signed; a new item goes to `change-request` |
| "Nobody knows who decides" | Missing or contradictory accountability | `raci-matrix` | One Accountable per deliverable and decision (DACI for decisions) |
| "The team is overloaded" / "who is overloaded?" / "burned out" | Peaks above capacity, one person on everything | `resource-management` | Run the capacity check; level within float |
| "My vendor is late" | Weak contract remedies or no supplier management | `procurement-management`, then `project-delivery` | Apply the contract remedies; log the issue |
| "Should we build or buy?" / "write an RFP or SOW" | No make-or-buy decision or sourcing plan | `procurement-management` | Decide make-or-buy per work package; write the SOW, then pick RFI, RFQ or RFP |
| "We go live next week" / "plan the cutover" / "do we need a rollback plan?" | Readiness not evidenced | `release-and-cutover` | Run go/no-go against readiness criteria; rehearse the runbook and rollback |
| "Plan the next sprint" / "how many sprints are left?" / "write user stories" / "show velocity or a burnup" | Velocity not used for forecasting; stories not ready | `agile-delivery` | Forecast as a range with `velocity_forecast.py`; plan to capacity; split stories with INVEST |
| "Our estimates are always wrong" | Single-point guesses, no basis of estimate | `estimation` | Three-point estimates with P50/P80 |
| "The sponsor has gone quiet" or "a stakeholder is blocking us" | Engagement gap | `stakeholder-management` | Re-map power/interest; plan the engagement step |
| "People are surprised by decisions" | No communication plan or escalation path | `project-communication` | Set audiences, cadence and escalation |
| "Our meetings go nowhere" | No purpose, agenda or decision log | `meeting-management` | Purpose, timeboxed agenda, decisions and actions captured |
| "Defects keep reaching UAT" | Vague acceptance criteria, no gates | `quality-management` | Write Given/When/Then criteria; set gate exit criteria |
| "Something big might go wrong" | Unmanaged threat | `risk-management`, then `risk-register` | Score it; choose a response; check the reserve |
| "Users will not adopt the new system" | No readiness or reinforcement plan | `change-management` | Readiness assessment and adoption plan |
| "We keep making the same mistakes" | Lessons captured but not actioned | `lessons-learned` | Assign owners and dates to each lesson |
| "Is this still worth doing?" | Benefits or costs moved | `business-case`, then `project-closure` if stopping | Re-run the appraisal with the current forecast |

## Tie-breaks for shared triggers

| Phrase or situation | Primary skill | Secondary (only for) |
|---|---|---|
| Retro, retrospective, post-mortem (any stage) | `lessons-learned` (format, lessons, owners) | `meeting-management` to facilitate the session; `agile-delivery` for where the sprint retrospective sits in the cadence |
| Kickoff | `project-initiation` (project kickoff purpose and content) | `meeting-management` to run the meeting; `resource-management` for the team's working agreement |
| Charter | `project-charter` (authorizes the project) | `resource-management` for a *team* charter or working agreement |
| Contingency reserve, management reserve | `risk-management` sizes contingency from risk exposure | `cost-management` places reserves in or above the baseline and tracks drawdown; `change-request` when a change draws on it; `estimation` supplies the estimate range it is sized against |
| EMV, expected monetary value | `risk-register` computes EMV per risk and totals with `risk_score.py` | `risk-management` for decision trees, Monte Carlo and reserve sizing |
| Probability x impact score (1-5 grid) | `risk-register` (qualitative ranking) | `risk-management` to set the scales and thresholds |
| Steering, steering committee | `meeting-management` (agenda, decisions, actions) | `status-report` for the steering update's content; `project-delivery` for governance in execution |
| Status, project health, on track | `senior-pm` to triage "is it on track?" | `status-report` to write the report; `project-delivery` to run the control loop |
| Issue, issue log, escalation | `project-delivery` (one log of issues, actions, decisions and dependencies) | `risk-register` while it is still a risk; `project-communication` for the escalation ladder; `meeting-management` for actions captured in a meeting |
| Baseline (none exists) | `project-delivery` when work is already running (interim baseline) | `project-planning` before work starts or for a full re-plan; `change-request` to change an approved baseline |
| Change control, CCB, scope creep | `change-management` (procedure, board, tolerances) | `change-request` to raise and assess each change |
| Change request, one specific change | `change-request` (form, impact assessment, change log) | `change-management` for the board's decision and adoption |
| Acceptance criteria, definition of done | `quality-management` | `scope-and-requirements` for acceptance tests per requirement and formal deliverable sign-off; `agile-delivery` for the definition of ready |
| Story points, planning poker | `estimation` | `agile-delivery` for velocity and sprints left |
| How long will it take | `project-schedule` (network duration) | `agile-delivery` for sprints left on a backlog; `estimation` for one item's effort |
| Budget | `cost-management` (baseline and control) | `business-case` for whether to invest; `procurement-management` for contract price |
| Handover to operations | `release-and-cutover` (service handover after hypercare) | `project-closure` for the project handover, benefits owner and close |
| Who | `raci-matrix` (who is accountable) | `resource-management` (who is on the team), `stakeholder-management` (who is affected), `project-communication` (who hears what) |
| Vendor, supplier | `procurement-management` | `stakeholder-management` for engaging the vendor; `risk-register` for vendor risks |
| Capacity, over-allocation | `resource-management` (`capacity_check.py`) | `project-planning` uses it as a baseline gate |
| Benefits | `business-case` (benefits register before approval) | `project-closure` for benefits tracking after delivery |
| Plan (which one?) | `project-planning` (integrated plan) | sprint plan → `agile-delivery`; comms plan → `project-communication`; cutover plan → `release-and-cutover`; procurement plan → `procurement-management`; staffing plan → `resource-management` |

## Common sequences

Use these when the user needs more than one step; still hand over one or two skills at a time.

- **Idea to authorized project:** `project-initiation` → `business-case` → `project-charter`
  → `stakeholder-management` → kickoff (`project-initiation` with `meeting-management`).
- **Building the baseline:** `scope-and-requirements` → `work-breakdown-structure` →
  `procurement-management` (make-or-buy) → `estimation` → `resource-management` +
  `raci-matrix` + `project-schedule` (leveled together) → `risk-management` /
  `risk-register` (reserves) → `quality-management` → `cost-management` →
  `project-communication` → `change-management` → `project-planning` approves.
- **Weekly control loop:** `cost-management` earned value or `agile-delivery` velocity →
  `risk-register` update → `project-delivery` issue log check → `status-report` → steering
  via `meeting-management` → `change-request` when needed.
- **A change arrives:** `change-request` (assess) → `change-management` (CCB decision) →
  re-baseline through `project-planning`, `project-schedule` and `cost-management`.
- **Buying part of the work:** `procurement-management` (make-or-buy, SOW, selection) →
  `risk-register` (vendor risks) → `cost-management` (contract costs) → contract closure in
  `project-closure`.
- **Going live:** `quality-management` (gates) → `release-and-cutover` (go/no-go, cutover,
  hypercare) → `project-closure`.
- **Closing:** `project-closure` (acceptance, handover, benefits handed to their owners
  against the `business-case` register) → `lessons-learned`.

`references/helios-walkthrough.md` shows the whole sequence on the sample Helios project.
