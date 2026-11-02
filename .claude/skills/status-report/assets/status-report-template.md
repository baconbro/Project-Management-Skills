# Status Report — <project name> — <report no.>

Fill-in template. Replace every `<placeholder>`; delete the hint lines in italics. Rate with
`references/rag-criteria.md`, write with `references/writing-and-review.md`; a filled example is
`status-report-sample.md`. Write ratings as words (GREEN / AMBER / RED); colour is optional.

| | |
| --- | --- |
| **Project** | <project name> |
| **Status date / data cut-off** | <YYYY-MM-DD> / <YYYY-MM-DD, e.g. the weekly control review> |
| **Reporting period** | <YYYY-MM-DD> to <YYYY-MM-DD> |
| **Prepared by / sent** | <PM name> / <YYYY-MM-DD> |
| **Audience and distribution** | <e.g. steering committee pre-read; steering members and key stakeholders> |
| **Overall RAG** | **<GREEN / AMBER / RED>** — previous (<YYYY-MM-DD>): <rating> — trend: <↑ improving / → steady / ↓ worsening> (<the evidence that moved>) |
| **Red triggers** | <for an AMBER: the measurable condition and date that would turn it RED> |
| **Tolerances** | Schedule: <e.g. 2 weeks on any key milestone> · Cost: <e.g. EAC up to $X, the funding ceiling> |

## Summary
<Three sentences: the overall rating and the dimension that drives it; the one thing the reader
must know; the decision you need, from whom, by when.>

## Decisions needed
| Id | Decision | Options (effect on cost / dates / scope) | Recommendation | Decider | Decide by | If no decision |
| --- | --- | --- | --- | --- | --- | --- |
| <DEC id> | <question that can be answered> | <1 ...; 2 ...; 3 ...> | <option and why> | <one named person> | <YYYY-MM-DD> | <consequence> |

## RAG by dimension
*Every AMBER or RED row needs an owner, an action and a due date. Rate on the worse of the index
test and the forecast test.*

| Dimension | RAG (prev → now, trend) | Evidence: measure vs threshold | Forecast | Owner | Action / decision (due) |
| --- | --- | --- | --- | --- | --- |
| Schedule | <prev> → <now>, <trend> | <SPI x.xx; SPI(t) after ~60% complete; key milestone forecast vs tolerance> | <key milestone forecast dates> | <name> | <action> (<YYYY-MM-DD>) |
| Cost | <prev> → <now>, <trend> | <CPI x.xx; EAC vs BAC, BAC + management reserve and tolerance> | <EAC $x (formula); range $x–$x> | <name> | <action> (<YYYY-MM-DD>) |
| Scope | <prev> → <now>, <trend> | Pending CRs: <n> (<ids>), <$ cost>, <days>, decided by <CCB / sponsor> on <date>; committed + pending <$x> vs remaining contingency <$x> | <cut line holds / items below it> | <name> | <action> (<YYYY-MM-DD>) |
| Quality | <prev> → <now>, <trend> | <gates passed or failed; failing criteria and conditions with fix dates; defects vs threshold> | <next gate and whether it will pass> | <name> | <action> (<YYYY-MM-DD>) |
| <Risk (optional)> | <prev> → <now>, <trend> | <HIGH risks occurring or triggered; overdue responses> | <exposure not yet in the forecast> | <name> | <action> (<YYYY-MM-DD>) |

**RED work packages or interim milestones** (name them even when the dimension is AMBER):
- <WBS id and name> — <CPI / SPI or slip> — owner <name> — <action> (<YYYY-MM-DD>)

**Budget:** BAC <$x> · AC to date <$x> (<x>% of BAC) · EV <$x> (<x>% complete) · EAC <$x>
(<formula>) · VAC <$x> (<x>%) · TCPI(BAC) <x.xx> vs CPI <x.xx> · contingency <$x drawn / $x
undrawn of $x> · management reserve <$x undrawn of $x> · cost tolerance <$x> · EVM as at <date>

*Agile or hybrid work:* velocity <average / minimum / trailing-3>; <n> points left; <n> sprints
left; release forecast <likely / pessimistic sprints>, cut line <holds / items below it>.

## Milestones
| Milestone | Baseline | Forecast | Variance | RAG | Owner | Recovery action (due) |
| --- | --- | --- | --- | --- | --- | --- |
| <milestone> | <YYYY-MM-DD> | <YYYY-MM-DD or "met YYYY-MM-DD"> | <+n weeks / 0> | <rating> | <name> | <action> (<YYYY-MM-DD>) |

## Progress this period (outcomes, not activity)
- <Deliverable or result finished and accepted, with the date.>
- <Decision taken, with its id.>

## Changes this period
*Ids link to the change log. Show every pending request; it feeds the scope rating.*

| CR | Title | Status | Cost / days | Decided or to be decided by (date) |
| --- | --- | --- | --- | --- |
| <CR id> | <title> | <approved / pending / rejected / deferred> | <$x> / <n> | <CCB / sponsor> (<YYYY-MM-DD>) |

## Top risks and issues
*At most five, linked to the risk register and issue log; list what changed or what the reader
must act on.*

| Id | Type | Description | Severity, trend | Owner | Next action (due) |
| --- | --- | --- | --- | --- | --- |
| <R / I / DEP id> | <risk / issue / dependency> | <one line> | <HIGH / MEDIUM / LOW>, <trend> | <name> | <action> (<YYYY-MM-DD>) |

## Next period
- <What will be true by the next report> — <owner> — <YYYY-MM-DD>

## Links
<risk register> · <issue log> · <change log> · <EVM table / burnup> · <RAG history log>
