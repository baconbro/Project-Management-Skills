# Retrospective Formats, Root Causes and Classification

Different formats surface different things. Match the format to the goal (broad reflection,
feelings, momentum, or root-causing one event), then classify what comes out on fixed scales
so lessons from different sessions and projects can be compared. Examples use the sample
Helios project (a fictional customer self-service portal used throughout this catalog).

## Choosing a format

| Goal | Format | Typical review | Length |
|---|---|---|---|
| Fast, action-oriented improvement | Start / Stop / Continue | Sprint retrospective | 60-90 min |
| Fuller reflection, including what was learned and missing | 4Ls | Release, phase or post-project review | 90-120 min |
| Momentum plus the risks ahead | Sailboat | Mid-project, before a big milestone | 60-90 min |
| Morale, friction, team dynamics | Mad / Sad / Glad | When the team is strained | 60 min |
| One significant failure, incident or near miss | Timeline post-mortem, then 5 whys | Within 5 business days of resolution | 90-120 min |
| The cause of one theme another format surfaced | 5 whys | Inside any session | 15-20 min per theme |

Rotate formats in recurring sprint retrospectives so they do not go stale. A post-implementation
review of *benefits* after go-live belongs to the benefits owner (`project-closure` hands it
over); its lessons part uses 4Ls or the timeline over the whole project.

## Start / Stop / Continue
Three columns: what should we **start** doing, **stop** doing, and **continue** doing?
- **Use when:** you want a quick retrospective that converts directly into behaviours; the
  simplest format and a safe default.
- **Strength:** every item already points at an action. **Watch for:** items that are
  symptoms ("stop missing dates"); take the top one through 5 whys.

## 4Ls: Liked, Learned, Lacked, Longed for
**Liked**: what went well. **Learned**: new knowledge or insight. **Lacked**: what was missing.
**Longed for**: what the team wished it had.
- **Use when:** you want a fuller reflection that captures learning and unmet needs, not just
  process tweaks. Good at the end of a phase, a release or the project.
- **Helios:** the post-project review on 2026-11-04 used 4Ls over the whole project and
  confirmed LL001-LL007.

## Sailboat (also called speedboat)
Draw a boat: **wind** (what propels the team), **anchors** (what holds it back), **rocks**
(risks ahead) and the **island** (the goal).
- **Use when:** the team is visual, or you want momentum and upcoming risks in one
  conversation. Copy each rock into the risk register through `risk-register`; it is a risk,
  not a lesson.

## Mad / Sad / Glad
Capture how events made people feel (**mad**, **sad** or **glad**), then discuss the causes
behind the strongest feelings.
- **Use when:** morale, friction or team dynamics are the issue. It surfaces signal that
  process formats miss and needs strong psychological safety; run the safety check first.

## 5 Whys
Take one specific problem and ask "why?" until you reach a cause the organisation can change
that would stop it recurring. Five is a guide, not a rule.

Three rules keep the chain honest:
1. **The "therefore" test.** Read the chain from the bottom up, joining each line with
   "therefore". Every link must be a sufficient cause of the line above. If a link only
   explains part of it, or explains something else, the chain has jumped.
2. **Branch when two causes contribute.** Most real failures have more than one cause; force
   them into one line and one of them disappears.
3. **Stop at what you control.** A vendor's internal failure is managed under the contract
   (`procurement-management`); the post-mortem asks what *we* planned, decided or lacked.
   Stop when the next "why?" leaves your organisation or the answer is a person ("Carla was
   slow") rather than a condition.

**Helios worked example.** Problem: "SSO working in test" was reached on 2026-07-17, two weeks
late, making WBS 1.3.1 Identity / SSO integration the RED work package at month 3 (SPI 0.75,
CPI 0.69). Two causes contributed, so the chain branches.

Branch A, the late start:
1. Why was SSO late? Integration testing against the real identity provider started late.
2. Why did it start late? Sandbox access arrived only after 1.3.1 had started in week 6.
3. Why did access arrive late? It was requested only after IdentityCo's contract was signed in
   week 5, and provisioning has a lead time.
4. Why was it requested so late? Nobody owned vendor onboarding; the plan had no onboarding
   tasks, owner or access lead times.
5. Why did the plan have none? The PMO standard plan template has no vendor-onboarding
   workstream, so every project starts without one. **Root cause** (lesson LL001).

Branch B, the stoppage:
1. Why else was SSO late? IdentityCo's sandbox was down from 2026-06-12 to 2026-07-06 (issue
   I001 in `project-delivery`), stopping real-provider tests.
2. Why did one outage stop all integration testing? There was no fallback: the identity-provider
   stub was decided only after the outage (DEC001) and went live on 2026-06-22 (ACT002).
3. Why was no fallback planned? The test approach treated the vendor sandbox as always
   available. **Contributing cause**, in our control. The outage itself is IdentityCo's
   failure, handled under the contract with a delay credit and a recovery plan.

Therefore test, branch A bottom-up: no onboarding workstream in the template, *therefore*
nobody owned onboarding, *therefore* access was requested only after signature, *therefore*
the sandbox arrived after 1.3.1 started, *therefore* testing started late, *therefore* SSO was
late. Each link holds. Both branches end in one recommendation: the onboarding workstream in
the standard plan includes a named owner from the day of award, access lead times, and a stub
for every external integration. A chain that jumps would be "integration was late, because the
sandbox was unstable, because access was requested late": a late request explains a late start,
not an unstable sandbox.

## Timeline (blameless) post-mortem
Reconstruct what happened in time order, mark the decisions, find the contributing factors,
then root-cause the biggest. Use it for a missed milestone, a failed or rolled-back release,
a production incident, a near miss, or a failed phase. Fill `assets/post-mortem-template.md`.

1. **Hold it soon, after the fire is out:** within about five business days of resolution,
   with a facilitator who made none of the decisions under review.
2. **Draft the timeline from records before the meeting:** issue log, status reports, chat,
   tickets, deployment and monitoring logs. Facts with dates, each with its source.
3. **Walk the timeline with the people involved**, adding what they knew and expected at each
   point. Disagreements about facts are settled from the records, not by seniority.
4. **Mark the decision points.** For each: the options, the information available then, who
   decided and why. Judge a decision by what was known at the time, not by the outcome
   (hindsight bias).
5. **List the contributing factors:** conditions that, had they been absent, would have
   prevented the event or shortened it. Note for each whether it is in your control.
6. **Run 5 whys on the one or two biggest factors**, branching where needed.
7. **Record what went well:** detection, response, workarounds worth repeating.
8. **Write actions of two kinds:** *fix* (this project, owned in the issue log) and *prevent*
   (the organisation, owned in the lessons log). Each is verb-first, owned and dated.

Blameless does not mean no accountability: owners still own actions. It means the analysis
looks for conditions and decisions, not culprits, because people who expect blame hide the
facts the next project needs.

**Helios worked example (post-mortem held 2026-07-22 on the SSO slip):**

| When | What happened | Source | Decision point? |
|---|---|---|---|
| Week 5 | IdentityCo contract signed; sandbox requested only now; no onboarding owner | Vendor register V01 | No decision was made: a gap |
| Week 6 (2026-05-11) | 1.3.1 starts with sprint S1; no sandbox access yet | Sprint history; schedule | Start against documentation only |
| 2026-06-05 | M2 close: 1.3.1 RED (CPI 0.78, SPI 0.70), reported as AMBER | RAG history | Report AMBER only (see LL002) |
| 2026-06-12 | Sandbox goes down; R001 occurs; issue I001 opened | Issue log | Report AMBER only (see LL002) |
| 2026-06-16 | Plan sprint S4 around testing against a stub (decided during S3) | DEC001 | Sound given the information |
| 2026-06-22 | Identity-provider stub live in test | ACT002 | — |
| 2026-06-25 | Recovery plan agreed; $880 delay credit claimed | ACT001 | — |
| 2026-06-26 | 1.3.1 (RED since the M2 close) escalated as DEC002 | Issue log (DEC002) | Sponsor first told now |
| 2026-07-06 | Sandbox restored | Recovery plan | — |
| 2026-07-17 | SSO working in test, two weeks late | Earned-value milestone | — |

Contributing factors: no onboarding owner (in control), no test fallback (in control), the
vendor outage (vendor's control, managed under the contract), a weekly status that rated
dimensions only, so 1.3.1's RED at the M2 close never reached the sponsor (in control). Went
well: the stub decision kept S4 on its goal; the service level in the contract gave an
immediate remedy. Actions: LL001 (prevent) and LL002 (prevent).

## Running the session
Facilitation mechanics (timebox, parking lot, reading actions back) are in `meeting-management`.
What is specific to retrospectives:
- **Shape (90 minutes for a two-week sprint):** set the stage and check back on the previous
  actions, 10 min; gather data, 25 min; generate insights and root causes, 25 min; decide one
  or two actions, 20 min; close, 10 min.
- **Safety first.** Open with Norm Kerth's Prime Directive: everyone did the best job they
  could, given what they knew at the time, their skills, the resources available and the
  situation at hand. When trust is low, run an anonymous safety check (1 = I will say nothing,
  5 = I will say anything); if most answers are 2 or lower, change the room (no managers) or
  work on safety before content.
- **Silent writing before discussion** so that quiet voices count; cluster into themes; give
  each person three dot votes to pick the top two or three themes.
- **Bring data:** the data pack turns "testing was rushed" into "false test failures from stale
  QA data in the last week of sprint S4 (I003)".
- **Keep what went well.** Practices that worked must be repeated on purpose, so they become
  `repeat` lessons.
- **Close** with the actions read back and a return-on-time-invested vote (1-5); persistent low
  scores mean the format or the follow-through needs changing.

## Classifying lessons
Give every lesson a **kind**, a **category** and an **impact** so patterns appear across
sessions and projects, and so it is clear which lessons to act on.

**Kind:** `improve` (went badly; change something) or `repeat` (went well; make it standard).

**Category:** pick the one area where the root cause sits, not where the symptom showed.

| Category | Use for root causes in |
|---|---|
| planning | Estimates, sequencing, lead times, buffers, resourcing assumptions, the plan template |
| scope | Requirements, scope boundaries, acceptance criteria content, scope change |
| communication | Reporting, escalation, stakeholder information flow, decisions not shared |
| technical | Architecture, design, tools, reuse, engineering practices |
| process | Ways of working, ceremonies and meetings, governance and approval routines |
| people | Skills, staffing, onboarding of team members, workload, team dynamics |
| quality | Test strategy and environments, reviews, defects, quality gates |
| vendor | Supplier selection, contracts, vendor onboarding, third-party dependencies |

Helios: LL005 (stand-ups ran over 30 minutes) is `process`, a meeting routine, not `people`;
LL007 (support-agent training planned to finish on launch day) is `planning`, a missing buffer
in the plan, not `quality`; LL004 (shared QA environment with stale data) is `quality`, a test
environment.

**Impact scale:** rate the effect the event had, or for a `repeat` lesson the gain or protection
it gave.

| Impact | Definition | Helios example |
|---|---|---|
| High | Moved or threatened a baseline (milestone, budget, committed scope), drew contingency or management reserve, or put a go-live or acceptance decision at risk | LL001: SSO two weeks late, 1.3.1 RED; LL007: training gap became go-live condition C1 |
| Medium | Rework, delay or cost absorbed inside tolerances with no baseline change, or a problem recurring across two or more sprints; for `repeat`, a measurable gain within a work package | LL003: knowledge base ahead of plan (SPI 1.10); LL004: test re-runs from stale QA data in sprint S4 |
| Low | Friction or inefficiency with no measurable effect on schedule, cost, scope or quality | LL005: stand-ups running long |

**Which lessons to act on:** every High; a Medium that recurs or is cheap to fix; a Low only
when it recurs (three sprint retrospectives in a row, or a second project). Record the rest
for pattern-spotting without an action.
