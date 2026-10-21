# WBS dictionary: <Project Name>

- **Author:** <project manager>  |  **Version:** <n>  |  **Date:** <date>
- **Scope statement:** <one sentence from the charter or scope-and-requirements>
- **Organizing principle:** <deliverable-oriented (preferred) / phase-oriented>
- **Source file:** `<path to your copy of assets/wbs-template.csv>` — the CSV is the single
  source; this document is rendered from it, never edited by hand.
- **Weights mean:** <percent of the parent's effort / cost / value>
- **Budget at completion (BAC):** <amount and currency, from cost-management>

## WBS dictionary
Generate the table from the CSV (the headers below are the ones the validator accepts) and
paste it here:

```bash
python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py <your-wbs.csv> --rollup --budget <BAC> --format md
```

| WBS id | Name | Type | Weight (%) | Share of project (%) | Budget | Owner | Description | Acceptance criterion | Control account |
|---|---|---|---|---|---|---|---|---|---|
| <1> | <project name> | summary | | 100.00 | <BAC> | <project manager> | <scope statement> | <project-level success criterion> | |
| <1.1> | <project management element> | work package | <%> | <share> | <amount> | <project manager> | <planning, governance, reporting, closure> | <closure accepted> | <1.1> |
| <1.2> | <deliverable> | summary | <%> | <share> | <amount> | <deliverable owner> | <what this deliverable is> | | <1.2 when measured as one control account> |
| <1.2.1> | <work package> | work package | <%> | <share> | <amount> | <single accountable owner> | <scope of the work package> | <verifiable completion criterion> | <control account id> |
| <1.2.2> | <work package> | work package | <%> | <share> | <amount> | <single accountable owner> | <scope of the work package> | <verifiable completion criterion> | <control account id> |

Sample rows from the sample Helios project (a fictional customer self-service portal used
throughout this catalog) — `assets/wbs-sample.csv` run with `--rollup --budget 500000`:

| WBS id | Name | Type | Weight (%) | Share of project (%) | Budget | Owner | Description | Acceptance criterion | Control account |
|---|---|---|---|---|---|---|---|---|---|
| 1.3 | Portal build | summary | 45 | 45.00 | 225,000.00 | Ben Adeyemi | The portal application and its integrations | | |
| 1.3.1 | Identity / SSO integration | work package | 35 | 15.75 | 78,750.00 | Ben Adeyemi | Single sign-on with the identity provider (vendor sandbox due in week 6) | Pilot users authenticate through SSO in staging and the security review by Marcus Webb is passed | 1.3.1 |
| 1.3.2 | Self-service UI | work package | 30 | 13.50 | 67,500.00 | Devin Patel | Password reset and order status screens meeting WCAG 2.2 AA | Both journeys complete end to end on desktop and mobile | 1.3.2 |

## Control accounts
A control account is the element where cost and schedule performance (earned value in
`cost-management`) is measured and where one manager answers for the budget: a work
package, or a parent that groups several small ones. Every work package belongs to exactly
one. The validator prints this table under `--rollup`; add the manager.

| Control account | Name | Work packages | Share of project (%) | Budget | Control account manager |
|---|---|---|---|---|---|
| <1.1> | <project management> | <n> | <share> | <amount> | <name> |
| <1.2> | <deliverable grouping its work packages> | <n> | <share> | <amount> | <name> |
| <1.3.1> | <large work package measured on its own> | 1 | <share> | <amount> | <name> |

## Validation
Paste the verdict line of the latest run:

```bash
python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py <your-wbs.csv> --require owner,acceptance --strict
```

- **Result:** <PASS: 0 error(s), 0 warning(s)> on <date>
- **Warnings accepted and why:** <none / list each warning and the reason it is acceptable>

## Sign-off
- [ ] Scope is 100% covered — a project-management element is included and nothing out of
      scope appears.
- [ ] Every parent's children sum to 100 (siblings weighted all or none) and the validator
      passes.
- [ ] Siblings are mutually exclusive; no single-child parents.
- [ ] Every work package has an owner, a description, a verifiable acceptance criterion and
      a control account.
- [ ] Shares and budget per control account agreed with `cost-management`; ids handed to
      `estimation`, `project-schedule` and `raci-matrix`.
- **Approved by:** <sponsor> on <date>
