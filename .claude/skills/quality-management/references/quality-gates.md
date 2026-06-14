# Quality Gates

A quality gate is a checkpoint where work must meet defined criteria before it may proceed.
Gates make quality a *decision* with an owner, not something that quietly erodes under
schedule pressure. Each gate has **entry criteria** (what must be true to start the gate
review) and **exit criteria** (what must be true to pass).

## Entry and exit criteria

```
        entry criteria met            exit criteria met
  Work ───────────────────►  GATE  ───────────────────►  Next phase / release
                              │
                              └── not met ──► rework, or escalate for a decision
```

- **Entry criteria:** preconditions for the review to even happen — e.g. "code complete, unit
  tests green, criteria written". Failing entry means the gate is not ready; do not convene it.
- **Exit criteria:** the pass conditions — e.g. "all acceptance criteria pass, no open critical
  defects, security sign-off obtained". Failing exit means rework or an explicit waiver decision.

### Example: Helios "ready for UAT" gate
| | Criteria |
|---|---|
| **Entry** | Feature complete; unit + integration tests passing; acceptance criteria documented |
| **Exit** | All acceptance criteria pass; 0 critical / 0 high defects open; accessibility scan clean; product owner sign-off |

## Gate reviews
A gate review is the meeting (or async check) where the criteria are assessed and a decision is
recorded. Outcomes:
- **Pass** — proceed.
- **Conditional pass** — proceed with named, time-boxed follow-ups logged.
- **Fail** — rework and re-review.
- **Waiver** — proceed despite a miss, by an authorized approver, with the risk documented.
  Waivers must be rare and visible; routine waivers mean the gate is theatre.

Name the approver(s) per gate. In agile the recurring gate is the iteration review/demo; in
waterfall it is a phase-end gate; in hybrid you mix both.

## Quality vs Grade — keep them separate
- **Quality** = conformance to requirements; *low quality is always a problem* (defects, things
  that do not meet their acceptance criteria).
- **Grade** = the level of features/capability; *low grade can be perfectly acceptable* (a basic
  but defect-free tool).
A cheap economy car can be high quality (no defects, does what it promises) and low grade (few
features). Helios's MVP is deliberately low grade — fewer self-service flows — but must be high
quality. Gates enforce quality; grade is a scope decision made elsewhere. Never let a team trade
quality for grade by smuggling defects past a gate to add features.
