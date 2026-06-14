# Work Breakdown Structure: <Project Name>

- **Author:** <name>  |  **Version:** <n>  |  **Date:** <date>
- **Organizing principle:** <deliverable-oriented / phase-oriented>

## WBS dictionary
List every element top-down. Give each a dotted id, a deliverable-style name, and (for
leaf work packages) an owner and a completion criterion. Weight is the percent of the
parent's effort/cost/value and must sum to 100 across each parent's children.

| WBS id  | Name                         | Weight (%) | Owner     | Completion criterion / "done"          |
|---------|------------------------------|------------|-----------|----------------------------------------|
| 1       | <project>                    |            |           |                                        |
| 1.1     | <deliverable>                | <>         |           |                                        |
| 1.1.1   | <work package>               | <>         | <>        | <verifiable result>                    |
| 1.1.2   | <work package>               | <>         | <>        | <verifiable result>                    |
| 1.2     | <deliverable>                | <>         |           |                                        |
| 1.2.1   | <work package>               | <>         | <>        | <verifiable result>                    |
| 1.3     | <deliverable>                | <>         |           |                                        |
| 1.3.1   | <work package>               | <>         | <>        | <verifiable result>                    |

## Validation
Record the same data in `assets/wbs.csv`, then run:

```bash
python scripts/wbs_validate.py assets/wbs.csv
```

The tool prints the WBS as an indented tree and a pass/fail report. Fix every ERROR
(duplicate ids, orphans, weights not summing to 100) and review each warning (a parent
with only one child usually means the decomposition is incomplete).

## Sign-off
- [ ] Scope is 100% covered — no missing work, no out-of-scope work.
- [ ] Siblings are mutually exclusive (no overlap).
- [ ] Every leaf work package has an owner and a verifiable "done".
- [ ] Validator passes with no errors.
