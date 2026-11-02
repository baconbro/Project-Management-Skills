# PM glossary — key terms across the catalog

Load this for a short, precise definition of a term used by any skill in the catalog; each
entry names the skill that owns the concept. Every skill's Resources section points here.
Worked figures come from the sample Helios project (a fictional customer self-service portal
used throughout this catalog): BAC $500,000, end-of-month-3 snapshot PV $255,000, EV
$235,500, AC $252,000.

Sections: [Lifecycle and governance](#lifecycle-and-governance) ·
[Scope and requirements](#scope-and-requirements) · [Agile delivery](#agile-delivery) ·
[Schedule](#schedule) · [Estimation](#estimation) · [Cost and earned value](#cost-and-earned-value) ·
[Business case](#business-case) · [Risk](#risk) · [People and responsibility](#people-and-responsibility) ·
[Procurement](#procurement) · [Release and cutover](#release-and-cutover) ·
[Quality](#quality) · [Change and closure](#change-and-closure)

## Lifecycle and governance
- **Waterfall / agile / hybrid** — sequential plan-driven delivery / iterative delivery
  re-planned each increment / a fixed frame (outcome, budget, dates) with iterative delivery
  inside it. See `senior-pm` (`references/methodology-selection.md`).
- **Baseline** — the approved version of scope, schedule and cost that progress is measured
  against (together, the performance measurement baseline). It changes only through change
  control (re-baselining). See `project-planning`.
- **Charter** — the short document that authorizes a project, names the sponsor and PM, and
  states purpose, scope boundaries and success criteria. See `project-charter`.
- **Sponsor** — the single accountable executive who funds the project, owns the business
  outcome and decides beyond the PM's tolerance (Helios: Dana Okoro).
- **Product owner** — in agile delivery, the person who orders the backlog and accepts
  stories on behalf of users (Helios: Ava Chen). See `agile-delivery`.
- **Steering committee** — the senior forum that reviews status, decides escalations and
  approves changes beyond the PM's tolerance (Helios: bi-weekly). See `meeting-management`.
- **Stage gate (phase gate)** — a formal go/no-go checkpoint between phases, judged on exit
  criteria. Typical of waterfall; hybrid keeps a few.
- **Tolerance** — the deviation (cost, time, scope) the PM may absorb before escalating.
- **Assumption** — something taken as true for planning without proof (e.g. "the identity
  vendor's sandbox is available in week 1"). Log it with an owner and a date to validate; a
  false assumption becomes a risk or an issue. Kept in the assumptions log; see `project-planning`,
  `project-charter`, `scope-and-requirements`.
- **Constraint** — a fixed limit the project must work within: deadline, budget ceiling,
  regulation, technology.
- **Dependency** — a link between two pieces of work (or to something outside the project)
  that dictates order. See `project-schedule`.
- **Issue / action / decision / dependency** — a problem happening now that needs resolving /
  a committed task with one owner and a due date / a recorded choice with who decided, when
  and why / something the project needs from outside the team by a date. All four item types
  live in one issue log, checked by `issue_log_check.py`. See `project-delivery`.
- **Risk vs issue** — a risk is an uncertain future event; an issue is already happening. A
  risk that occurs becomes an issue. See `risk-management`, `project-delivery`.
- **RAG** — Red/Amber/Green rating per dimension (scope, schedule, cost, quality, risk); the
  catalog's default bands are GREEN when CPI and SPI are both >= 0.95, RED when either is
  < 0.85, else AMBER, and the overall rating is no greener than the worst material dimension.
  See `status-report`.
- **Escalation path** — who hears about a problem next, and within what time, when it exceeds
  someone's authority. See `project-communication`.
- **MVP (Minimum Viable Product)** — the smallest releasable increment that delivers value and
  produces learning (Helios: MVP live to pilot at M4).
- **Interim baseline** — a one-day, sponsor-approved baseline (scope list, remaining
  milestones, budget to date and to complete, open risks) for a project already running
  without one, so progress can be measured at once. See `project-delivery`.

## Scope and requirements
- **Requirement types** — functional (what the product does), non-functional (how well:
  performance, security, accessibility), transition (what is needed to move to the new state:
  data migration, training). See `scope-and-requirements`.
- **MoSCoW** — prioritization into Must, Should, Could and Won't (this time); Won't items are
  recorded with where they go (Helios: live chat to phase 2). See `scope-and-requirements`,
  `agile-delivery`.
- **Scope statement** — deliverables, acceptance criteria, exclusions, assumptions and
  constraints, signed by the sponsor. See `scope-and-requirements`.
- **Requirements traceability matrix (RTM)** — the table linking each requirement backward to
  its objective and source and forward to its WBS work package and acceptance test; it proves
  coverage and shows what a change touches. See `scope-and-requirements`.
- **Scope validation vs quality control** — formal acceptance of finished deliverables by the
  named acceptor (customer or sponsor) / checking that the work meets the quality requirements
  before that. See `scope-and-requirements`, `quality-management`.
- **WBS (Work Breakdown Structure)** — a deliverable-oriented hierarchy of the whole scope.
  See `work-breakdown-structure`.
- **Work package** — the lowest WBS element, estimated, scheduled, costed and assigned to one owner.
- **WBS dictionary** — per element: description, owner, acceptance criterion, control account.
- **Control account** — the point in the WBS where scope, budget and actual cost are
  integrated and earned value is measured.
- **100% rule** — the children of every WBS element add up to 100% of the parent's work: nothing
  missing, nothing extra.
- **8/80 rule** — a heuristic that a work package should take between 8 and 80 hours of effort.
- **SMART** — objectives that are Specific, Measurable, Achievable, Relevant and Time-bound
  (Helios: cut the two ticket types by 50% within 6 months of launch).

## Agile delivery
- **Product backlog** — the single ordered list of work for the product. See `agile-delivery`.
- **User story / INVEST** — a small requirement written from a user's view; a good one is
  Independent, Negotiable, Valuable, Estimable, Small and Testable.
- **DoR (Definition of Ready)** — the criteria a backlog item must meet before the team pulls
  it into a sprint (clear acceptance criteria, sized, dependencies cleared). See `agile-delivery`.
- **DoD (Definition of Done)** — the criteria every item or increment must meet to count as
  complete (tested, reviewed, documented, deployable). See `quality-management`.
- **Sprint (iteration) / increment** — a fixed timebox (Helios: two weeks) / the usable, done
  output of it, shown at the sprint review. See `agile-delivery`.
- **Story points** — a relative size of effort, complexity and uncertainty; only comparable
  within one team. See `estimation`.
- **Velocity** — story points of items meeting the definition of done completed per sprint;
  forecast with its spread, never as a single number (Helios: mean 27.33, range 22-31). See
  `agile-delivery`.
- **Burndown / burnup** — work remaining over time / work completed against total scope; a
  burnup shows scope growth separately from progress. See `agile-delivery`.
- **Cut line** — the point in the ordered backlog below which items do not fit the dates at a
  given velocity (Helios: after HEL-170 at the pessimistic velocity). See `agile-delivery`.
- **Cycle time** — elapsed time from starting an item to done; report a percentile ("85% of
  stories finish within 6 working days"), not the mean. See `agile-delivery`.
- **WIP limit** — a cap on the items in progress at once, per person or workflow stage (Kanban);
  cutting work in progress is the cheapest way to cut cycle time. See `agile-delivery`.

## Schedule
- **Critical path** — the longest chain of dependent activities; it sets the shortest possible
  duration, and any slip on it slips the finish (Helios: A → B → D → F → G → H → J, 18 weeks).
  See `project-schedule`.
- **Float (slack)** — how far an activity can slip. *Total float*: without delaying the
  project finish (zero on the critical path; Helios task C, SSO integration, has 1 week).
  *Free float*: without delaying any successor's early start.
- **Near-critical** — a path or task with small float that can become critical after a slip.
- **Finish-to-start (FS)** — the successor starts after the predecessor finishes; the default
  dependency type.
- **Milestone** — a zero-duration checkpoint marking a significant event (Helios: M1, M4, M6).
- **Crashing / fast-tracking** — shortening the schedule by adding resources to critical tasks
  / by overlapping tasks that were planned in sequence (more risk, rework).
- **Resource leveling vs smoothing** — moving work to remove over-allocation even if the finish
  moves / moving work only within float so the finish does not. See `resource-management`.
- **Gantt chart** — bars on a calendar showing each task's dates and dependencies.

## Estimation
- **Analogous / parametric** — estimate from a similar past project / from a unit rate times a
  quantity (e.g. hours per screen). See `estimation`.
- **Three-point / PERT** — optimistic (O), most likely (M) and pessimistic (P) values;
  PERT mean = (O + 4M + P) / 6, standard deviation ≈ (P - O) / 6.
- **P50 / P80 / P90** — the value with a 50% / 80% / 90% chance of not being exceeded; commit at
  a stated confidence and hold the gap to the mean as reserve.
- **Planning poker / wideband Delphi** — team estimation by simultaneous reveal / by anonymous
  rounds with discussion between them.
- **Basis of estimate** — the written assumptions, method and sources behind an estimate.

## Cost and earned value
- **EVM (Earned Value Management)** — compares planned value (PV), earned value (EV) and actual
  cost (AC) to measure schedule and cost performance and forecast the outcome. See
  `cost-management`.
- **BAC (Budget at Completion)** — the total cost baseline, including contingency reserve and
  excluding management reserve (Helios: $500,000).
- **PV (Planned Value)** — the budget for the work scheduled to be done by the status date.
- **EV (Earned Value)** — the budget for the work actually done by the status date
  (% complete x the work's budget).
- **AC (Actual Cost)** — the cost actually incurred for the work done by the status date.
- **CV / SV** — cost variance EV - AC / schedule variance EV - PV, in money; negative is bad
  (Helios: CV -$16,500, SV -$19,500).
- **CPI / SPI** — cost performance index EV / AC / schedule performance index EV / PV; below 1
  means over budget / behind schedule (Helios: 0.93 / 0.92 → AMBER).
- **EAC / ETC / VAC** — estimate at completion (typically BAC / CPI) / estimate to complete
  (EAC - AC) / variance at completion (BAC - EAC) (Helios: EAC ≈ $535,000, VAC ≈ -$35,000).
- **TCPI (To-Complete Performance Index)** — the CPI the remaining work needs to land on BAC:
  (BAC - EV) / (BAC - AC) (Helios: 1.07 against a CPI of 0.93, a signal to re-plan).
- **S-curve** — cumulative planned cost over time; actuals and earned value plotted against it.
- **Cost baseline** — the time-phased budget, including contingency, against which cost
  performance is measured.
- **Contingency reserve vs management reserve** — contingency is held *inside* the cost
  baseline (in BAC) for identified risks and its drawdown is managed by the PM (Helios:
  $40,000, about P50 of a simulation of the residual register; P80 $99,000; the $52,300
  summed residual EMV is the mean, not the reserve; the sponsor accepted the gap to P80). A
  forecast EAC above BAC has already used the whole contingency. Management reserve is held *above* the baseline (not in BAC) by the sponsor for
  unidentified risks, and using it needs a baseline change (Helios: $25,000). Cost baseline +
  management reserve = total budget (Helios: $525,000). See `cost-management`, `risk-management`.

## Business case
- **Do-nothing option** — the baseline every option is compared with. See `business-case`.
- **Discount rate** — the rate per period used to bring future cashflows to today's value;
  use your finance team's hurdle rate and state it (the catalog's examples use 10%).
- **Appraisal period** — the number of periods over which costs and benefits are counted.
- **NPV (Net Present Value)** — the sum of discounted cashflows; positive means the investment
  beats the discount rate (Helios: $196,174 at 10% over periods 0-5).
- **IRR (Internal Rate of Return)** — the discount rate at which NPV is zero (Helios: 23.6%).
- **ROI** — net gain divided by cost (Helios: 86%, undiscounted).
- **Payback / discounted payback** — the time until cumulative (discounted) cashflow turns
  positive (Helios: 2.85 / 3.47 periods).
- **Switching value / sensitivity** — how far one input can move before the decision flips /
  how the result moves as inputs change.
- **Optimism bias** — the tendency to underestimate cost and time and overstate benefits;
  counter it with stress cases.
- **Benefit / disbenefit / benefit owner** — a measurable improvement / a measurable negative
  outcome that must be managed / the person who owns realizing it after handover (Helios:
  Priya Nair). See `business-case`, `project-closure`.

## Risk
- **Threat / opportunity** — an uncertain event with a negative / positive effect on
  objectives. See `risk-management`.
- **EMV (Expected Monetary Value)** — probability x monetary impact, in currency (Helios R001:
  0.4 x $120,000 = $48,000). Summed EMV, or a simulation of the register, informs the
  contingency reserve; it is the quantitative measure. See `risk-register`, `risk-management`.
- **Qualitative exposure score (P x I)** — a probability rating times an impact rating on 1-5
  scales (score 1-25), used only to rank and band the register; it is not money and must not
  be summed into a reserve. See `risk-register`.
- **Risk register** — the log of risks with owner, trigger, response, residual score and
  status. See `risk-register`.
- **Risk owner / trigger** — the one person who manages the risk / the early-warning sign that
  it is about to occur.
- **Response strategies** — threats: avoid, mitigate, transfer, accept, escalate;
  opportunities: exploit, enhance, share, accept, escalate.
- **Residual / secondary risk** — the exposure left after the response / a new risk the
  response itself creates.
- **Risk appetite / threshold** — how much risk the organization will take / the level above
  which a risk must be escalated or treated.
- **Pre-mortem** — imagining the project has failed and listing why, to surface risks early.
- **Decision tree / Monte Carlo** — EMV of alternative choices across chance branches /
  thousands of random trials of the register or schedule to get a distribution.

## People and responsibility
- **RACI / RASCI / DACI** — a matrix marking who is Responsible, Accountable (exactly one),
  Consulted and Informed for each activity; RASCI adds Support; DACI (Driver, Approver,
  Contributor, Informed) is used for decisions. See `raci-matrix`.
- **Stakeholder register** — who is affected or has influence, with their interest, power,
  current and desired engagement. See `stakeholder-management`.
- **Power/interest grid** — a 2x2 placing stakeholders to choose the strategy: manage closely,
  keep satisfied, keep informed, monitor.
- **Salience** — a stakeholder's priority from their power, legitimacy and urgency.
- **Capacity / allocation / utilization** — hours a person can work in a period / hours
  assigned / allocation divided by capacity. See `resource-management`.
- **Key-person risk** — work that depends on one person with no backup.
- **Team charter (working agreement)** — how the team works together: hours, tools, decisions,
  norms. Not the project charter. See `resource-management`.

## Procurement
- **Make-or-buy** — deciding per work package whether to do the work in-house or buy it from a
  supplier, on capability, cost, risk and control. See `procurement-management`.
- **SOW (Statement of Work)** — what the supplier must deliver, to what acceptance criteria and
  service levels, by when. See `procurement-management`.
- **RFI / RFQ / RFP** — request for information (market scan) / for quotation (price for a
  defined item) / for proposal (solution and price, scored). See `procurement-management`.
- **Contract types** — firm fixed price (supplier carries the cost risk; Helios: IdentityCo),
  time and materials (buyer carries it, rates fixed), cost-plus (buyer reimburses cost plus a
  fee and carries most of the risk). See `procurement-management`.
- **Vendor scorecard** — weighted scoring of bids after pass/fail gates, with due diligence.
- **Retention** — a share of payment held back until acceptance or a warranty period ends.

## Release and cutover
- **Release strategy** — big-bang, phased, pilot, parallel run or feature-flag ramp. See
  `release-and-cutover`.
- **Go/no-go decision** — the decision, by a named approver, that a release is ready: GO, CONDITIONAL GO
  or NO-GO, judged against readiness criteria.
- **Cutover** — the timed, owned sequence of steps that switches from the old way to the new
  at go-live, written in a cutover runbook and rehearsed.
- **Rollback / rollback trigger** — the planned reversal to the last good state / the
  quantified, time-boxed condition (Helios: SSO sign-in success below 95% over 15 minutes)
  that lets the cutover lead call it without escalating. A rollback also has a last safe start time.
- **Change freeze** — a window in which no other changes may be made to the affected systems.
- **Dress rehearsal** — a full run of the cutover runbook with the real people, bridge and
  communications, including the rollback, used to replace planned step times with rehearsed
  ones. See `release-and-cutover`.
- **Feature flag** — a switch that releases deployed code to a list or a share of users without
  a new deployment (Helios: GA ramped 25% → 50% → 100%). See `release-and-cutover`.
- **Hypercare** — a period of heightened support straight after go-live, with measured exit
  criteria, before the service is handed to business-as-usual (BAU) operations.
- **Point of no return (PONR)** — the cutover step after which rollback would lose data or break
  a commitment; push it late and hold a go-live checkpoint just before it. See
  `release-and-cutover`.

## Quality
- **Acceptance criteria** — the conditions a deliverable or story must meet to be accepted,
  often written as Given / When / Then. See `quality-management`.
- **Quality gate** — a checkpoint with entry and exit criteria that work must pass to proceed.
- **UAT (User Acceptance Testing)** — testing by users or their representatives that the
  product meets their needs before acceptance.
- **Quality vs grade** — meeting requirements (low quality is always a problem) / the category
  or feature level (low grade may be fine).
- **Cost of quality (COQ)** — the cost of achieving quality (prevention and appraisal: reviews,
  tests, audits) plus the cost of failing to (internal and external failure); used to decide
  what is good enough. See `quality-management`.
- **Defect removal efficiency (DRE)** — defects found before release ÷ (found before release +
  found in the first 30 days after) × 100; Helios targets ≥ 90%. See `quality-management`.
- **Escaped defect** — a defect found after release (pilot or production); a severity-1/2
  escape triggers a process audit. See `quality-management`.
- **Quality assurance (QA) vs quality control (QC)** — process-focused prevention (audits that
  the agreed way of working is followed) / product-focused detection (inspecting and testing
  deliverables, logging defects, enforcing gate exit criteria). See `quality-management`.

## Change and closure
- **Change request** — a formal proposal to change the baseline, assessed for impact and
  decided by the right authority. See `change-request`.
- **CCB (Change Control Board)** — the forum that approves, rejects, defers or requests more
  information on changes to the baseline beyond the PM's tolerance (Helios: CR002 sent back
  for more information on 2026-07-14). See `change-management`.
- **Integrated change control** — assessing a change's effect on scope, schedule, cost, quality
  and risk together before deciding.
- **Scope creep** — uncontrolled growth of scope without matching time, cost or approval.
- **ADKAR** — Awareness, Desire, Knowledge, Ability, Reinforcement: the stages a person moves
  through to adopt a change. See `change-management`.
- **Retrospective / lessons learned** — a team review of what to keep and change / the recorded
  lessons with owners and follow-up. See `lessons-learned`.
- **Post-project review** — the review at closure of delivery against the baseline and of
  benefits against the business case. See `project-closure`.
- **Benefits realization** — tracking after delivery that the promised benefits arrive (Helios:
  the 50% ticket reduction, measured by Priya Nair). See `project-closure`.
