# Change Control Plan — <project name>

Fill-in template: replace every `<placeholder>`. Guidance is in
`references/change-control-process.md`; a completed example is
`assets/change-control-plan-sample.md`. The CR form and the change log belong to the
`change-request` skill; this plan is the procedure that governs them.

| Field | Value |
|---|---|
| Version / date | <1.0> / <YYYY-MM-DD> |
| Prepared by | <project manager> |
| Approved by | <sponsor>, on <YYYY-MM-DD> (before the baseline freeze) |
| Change log | <where the log lives, e.g. a copy of `change-log.csv` from the `change-request` skill> |

## 1. Baselines under control
| Baseline | Version and date | Contents | Baseline owner |
|---|---|---|---|
| Scope | <v1.0, YYYY-MM-DD> | <scope statement, traceability matrix, WBS and dictionary> | <name> |
| Schedule | <v1.0, YYYY-MM-DD> | <milestones, critical path, schedule reserve> | <name> |
| Cost | <v1.0, YYYY-MM-DD> | <BAC incl. contingency reserve; management reserve held above BAC> | <name> |
| Quality | <v1.0, YYYY-MM-DD> | <definition of done, gate exit criteria> | <name> |

## 2. What needs a change request
- **Needs a CR:** <changes to deliverables, Must requirements, acceptance criteria, exclusions,
  baselined milestones, budgets or reserves, the definition of done, a vendor statement of work>
- **Does not need a CR:** <backlog re-ordering inside the release goal by the product owner;
  re-sequencing inside float with no milestone effect; clerical corrections>

## 3. Roles
| Role | Who | Responsibility |
|---|---|---|
| Requester | <anyone> | Raises the CR with a reason and a needed-by date |
| Change log keeper | <project manager> | Logs, routes, tracks status, verifies and closes |
| CCB chair | <sponsor or named delegate> | Decides CCB-level changes after hearing the members |
| CCB members | <names and roles> | Assess and advise; never decide their own request |
| Consulted per change | <e.g. finance, security, compliance, quality lead> | Advise when the change touches their area |
| Quorum | Chair or delegate + PM + at least <n> members | Without quorum, defer or escalate |

## 4. Approval tolerances
| Authority | Decides when | Funding it may commit |
|---|---|---|
| PM | LOW band, cost up to <amount> and up to <days> working days | <contingency up to the limit, or a saving> |
| CCB | Above the PM limits, within the remaining contingency, no move of <key milestone> | <contingency> |
| Sponsor | HIGH band, or management reserve or new budget, or a move of <key milestone>, or a change to an objective | <management reserve; requests new budget> |

Pass the same limits to the scorer: `--pm-limit-cost <amount> --pm-limit-days <days>
--ccb-limit-cost <undrawn contingency> --reserve-cost <contingency>`.

## 5. Cadence, emergency route and freezes
- **CCB slot:** <day, time, length; held only when a request is pending>
- **Sponsor-level decisions:** <steering committee cadence, and the extra-session rule>
- **Decision time targets:** PM <n> business days; CCB <next slot>; sponsor <next steering>
- **Emergency route:** <name> approves severity-1/2 fixes and urgent security or compliance
  changes within <hours> hours; a retrospective CR is raised within 1 business day and ratified
  at the next CCB
- **Change freezes:** for each release, code freeze from <date>; change freeze on <systems>
  from <date time> to <date time>; exceptions approved by <name> through the emergency route

## 6. Flow, decisions and status
Raise → Log → Assess → Decide → Communicate → Implement → Verify & close.

| Outcome | Log `status` | Must be recorded |
|---|---|---|
| Approve (with or without conditions) | Approved | Conditions, funding source, baselines to update, implementation owner, due date |
| Reject | Rejected | Reason, and what new evidence would justify re-raising it |
| Defer | Deferred | Reason, revisit date or trigger, where it is parked |
| Request more information | back to Under assessment | Questions, who answers, return date |

Lifecycle: Open (`Raised`) → Assessed (`Under assessment`) → Decided (`Approved` / `Rejected` /
`Deferred`) → Implemented → Closed (verified). Rejected and deferred CRs are closed at the
decision with their reason and stay in the log.

## 7. Communicating decisions
- **Within:** <1 business day> of the decision, in writing, by <channel>.
- **To:** the requester; <owners of affected baselines>; the implementation owner; <finance when
  a reserve is drawn>; <risk owner>; <contract owner for vendor changes>.
- **Content:** decision, rationale, conditions, funding, next steps and dates; for a rejection,
  what would change the answer; for a deferral, the revisit date.
- **Then:** reported in <the weekly status report> and at <stand-up / sprint review>.

Message: "<CR id> <title> was <decision> by <decider> on <date>. Rationale: <one or two
sentences>. Conditions: <conditions or none>. Funding: <source and amount>. Next: <owner> updates
<baselines> by <date>. Questions to <PM name>."

## 8. Updating baselines after approval
| Baseline | Updated by (name) | Using skill | Re-check |
|---|---|---|---|
| Scope statement, requirements, traceability | <name> | `scope-and-requirements` | Every changed requirement traces to a work package and a test |
| WBS and dictionary | <name> | `work-breakdown-structure` | `wbs_validate.py` passes |
| Schedule | <name> | `project-schedule` | `critical_path.py`; milestones still met |
| Cost and reserves | <name> | `cost-management` | `health_check.py`; contingency left: <amount> |
| Quality | <name> | `quality-management` | Gate criteria still testable |
| Risk register | <name> | `risk-register` | `risk_score.py`; secondary risks logged |
| Resources | <name> | `resource-management` | `capacity_check.py`; no one over-allocated |
| Contracts | <name> | `procurement-management` | Contract change signed before work starts |

Re-baseline (replace the whole remaining baseline) only with the sponsor's approval, when
variances against the current one no longer mean anything.

## 9. Verification, closure and reporting
- **Verified by:** <PM>, within <5> business days of Implemented: each baseline named in the
  decision has a new version citing the CR id, and the numbers agree across baselines.
- **Reported:** decided and pending CRs in <the weekly status report>; the change burden against
  the contingency at <each steering committee>.
- **Process health:** time from raise to decision; changes found without a CR (target 0);
  emergency-route uses; re-raised rejections.

## 10. Approval
| Name | Role | Decision | Date |
|---|---|---|---|
| <sponsor> | Sponsor | <approved> | <YYYY-MM-DD> |
| <project manager> | Project manager | <prepared> | <YYYY-MM-DD> |
