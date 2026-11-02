# Change Request — <CR id>: <short title>

Fill-in template: replace every `<placeholder>`. Field definitions and the 1-5 anchors are in
`references/change-request-fields.md`; a completed example is `assets/change-request-sample.md`.

| Field | Value |
| --- | --- |
| **Change ID** | <next free id in assets/change-log.csv, e.g. CR007> |
| **Title** | <short title, as in the change log> |
| **Project** | <project name> |
| **Raised by / date** | <name, role> / <YYYY-MM-DD> |
| **Status** | <Raised / Under assessment / Approved / Rejected / Deferred / Implemented / Closed> |

## 1. Description
<What is being asked, in plain language: one or two sentences a reader who was not in the room
understands. Name the deliverable or WBS element it touches.>

## 2. Justification
- **Reason / driver:** <the business, regulatory or technical reason, and why now>
- **Benefit / business-case impact:** <benefit gained or protected, in units; effect on the business case>
- **Cost of doing nothing:** <what happens if this is rejected>
- **Urgency:** <date a decision is needed by, and what a later decision costs>

## 3. Impact assessment
Rate each dimension 1-5 against the anchors (decimals such as 3.5 allowed) and quantify it.

| Dimension | Rating (1-5) | Detail (real units) |
| --- | --- | --- |
| Scope | <1-5> | <deliverables, WBS elements or acceptance criteria affected> |
| Cost | <1-5> | <amount; what it buys> |
| Schedule | <1-5> | <working days; tasks and milestones affected; float used> |
| Quality | <1-5> | <acceptance criteria, quality gates or test cycles affected> |
| Risk | <1-5> | <risks created, raised or reduced> |

- **Cost value:** <+amount added or -amount saved> · **Schedule days:** <+days added or -days saved>
- **Secondary risks introduced:** <description; risk-register id once logged>
- **Resources affected:** <people or teams, effort and when>
- **Score / impact band / authority:** <from change_impact.py, e.g. 2.80 / MEDIUM / CCB>

Append this CR as a row of `assets/change-log.csv` first, then score it from the repo root:

```bash
python .claude/skills/change-request/scripts/change_impact.py .claude/skills/change-request/assets/change-log.csv --explain --sensitivity
```

## 4. Options
| # | Option | Pros | Cons | Cost / days |
| --- | --- | --- | --- | --- |
| A | Do nothing | <pros> | <cons> | <0 / 0> |
| B | <option> | <pros> | <cons> | <amount / days> |
| C | <option, e.g. partial or deferred> | <pros> | <cons> | <amount / days> |

## 5. Recommendation
<The option advised and why, in one or two sentences, with any conditions.>

## 6. Decision
| Field | Value |
| --- | --- |
| **Approval authority** | <PM / CCB / Sponsor, from the Authority column and the change-management tolerances> |
| **Decision** | <Approved / Approved with conditions / Rejected / Deferred until YYYY-MM-DD> |
| **Decided by / date** | <name or board> / <YYYY-MM-DD> |
| **Conditions / rationale** | <conditions attached, or why rejected or deferred> |
| **Funding source** | <contingency reserve / management reserve / new budget / none> — <amount> |
| **Baselines to update** | <scope (WBS, acceptance criteria) / schedule / cost / quality plan / risk register / other> |
| **Implementation owner** | <name> — due <YYYY-MM-DD> |
| **Verification** | <how completion and the baseline updates are checked> — verified by <name> / <YYYY-MM-DD> |
| **Closed** | <YYYY-MM-DD, when status is set to Closed in the change log> |

After each status change, update the CR's row in `assets/change-log.csv` (`status`, `decided_by`,
`decision_date`). The change-control process that decides and verifies the CR is `change-management`.
