# RAG Criteria

Load this in steps 3, 4 and 7 of the workflow. A Red/Amber/Green (RAG) rating means something
only if the same written thresholds apply every period, the thresholds test the **forecast** as
well as performance to date, and the evidence is gathered *before* the colour is chosen. Rate
each dimension separately, then roll up. Examples use the sample Helios project (a fictional
customer self-service portal used throughout this catalog).

## 1. What the colours mean
| Rating | Meaning | What the reader must do |
|---|---|---|
| **GREEN** | The forecast is on plan: every key milestone, the cost at completion and the agreed scope land inside the baseline. | Nothing. Green is a claim backed by evidence, not the default. |
| **AMBER** | The forecast is off plan but still **inside tolerance**; the PM is managing it with a named owner and action. | Watch the trend; a decision may be needed soon. |
| **RED** | The forecast is **beyond tolerance**, or nothing within the PM's authority brings it back. | Decide: an exception above the PM is needed now. |

Not started is not GREEN, and no evidence is not GREEN: write "not rated — <evidence missing>"
and treat it as at least AMBER until the evidence exists. Always write the word; never rely on
colour alone (grayscale print, colour-blind readers).

## 2. Agree the tolerances before the first report
The colour bands below need two numbers per project, agreed with the sponsor and written in the
charter or project management plan. Never set or move them after a bad period.

| Tolerance | Where it comes from | Default if none is agreed | Helios |
|---|---|---|---|
| **Schedule** — how late a key milestone may be forecast before it is an exception | Charter milestones, risk appetite, the escalation ladder in `project-communication` | 2 weeks, or 10% of the remaining duration if smaller | 2 weeks on M4 or M6 |
| **Cost** — how far the estimate at completion (EAC) may exceed BAC | Charter budget range and stop triggers; `change-management` approval limits | +10% of BAC | $550,000: the top of the charter range and its stop trigger (= BAC + 10%) |

Also know the money ladder underneath, from `cost-management`: **BAC** (the cost baseline,
which already contains the contingency reserve) → **BAC + management reserve** (the whole
approved budget; the sponsor releases the reserve through change control) → **cost tolerance**
(the funding ceiling). Helios: $500,000 → $525,000 → $550,000.

## 3. Per-dimension thresholds
Rate each dimension on the **worse** of its index test and its forecast test. Index bands are
the same as `cost-management`'s `health_check.py` (GREEN at or above 0.95, RED below 0.85), and
they do not overlap.

| Dimension | Evidence | GREEN | AMBER | RED |
|---|---|---|---|---|
| **Schedule** | Key milestone forecast vs baseline; SPI; SPI(t) late in the project; release forecast for agile work | Every key milestone forecast on or before baseline, and SPI ≥ 0.95 | A key milestone forecast late but within the schedule tolerance, or 0.85 ≤ SPI < 0.95, or the pessimistic release forecast misses the date while the likely one meets it | A key milestone forecast beyond tolerance, or no option within the sponsor's authority keeps the end date, or SPI < 0.85 |
| **Cost** | EAC (with the formula used) vs BAC, BAC + management reserve and tolerance; VAC; CPI; TCPI | EAC ≤ BAC (VAC ≥ 0), and CPI ≥ 0.95 | EAC above BAC but within the cost tolerance (the contingency is forecast to run out; reserve or a re-plan is needed), or 0.85 ≤ CPI < 0.95 | EAC beyond the cost tolerance, or CPI < 0.85 |
| **Scope** | Change log (approved, pending, rejected); release cut line; requirements at risk | Agreed scope on track; no change request pending above the PM's tolerance; committed + pending changes fit in the remaining contingency | A change request pending above the PM's tolerance (CCB or sponsor decision), or committed + pending changes exceed the remaining contingency, or planned items forecast below the release cut line | A Must-have requirement or the project objective cannot be delivered within the baseline, or scope is changing without approved change requests |
| **Quality** | Quality gates, acceptance results and conditions, defect counts and trend | No gate failed or forecast to fail; every failing criterion, condition or blocking defect has an owner and a fix date before the next gate; defects within thresholds | Something the next gate depends on is overdue, unowned, or blocked with no dated plan to unblock it; or a deliverable was rejected at acceptance; or defects above threshold or rising two periods running | A gate has failed or will fail at the next milestone; a critical defect has no fix before go-live; or rework pushes a key milestone beyond tolerance |
| **Risk** *(optional fifth dimension)* | Risk register severity, triggers, response status | Every HIGH risk owned with its response on schedule; no trigger fired | A HIGH risk's trigger has fired or it is occurring, or a response is overdue | An occurring risk's impact is beyond tolerance and no response within the sponsor's authority remains |

Risk is optional because a risk that occurs becomes an issue and already shows in the dimension
it hits; cost and schedule rate the forecast, the risks section reports what is *not yet* in it.
Use the row when your governance asks for a risk colour.

## 4. Schedule: why SPI alone misleads
- **SPI converges to 1.0.** SPI = EV / PV, and both end at BAC, so SPI drifts toward 1.0 in the
  final third however late the project finishes; a project can show SPI 0.98 while its end date
  has moved a month. Once EV / BAC passes about 60%, rate schedule on the forecast dates and on
  earned schedule only, and say so in the report.
- **Earned schedule** converts SPI into time. ES = the time at which planned value equalled
  today's EV (interpolate on the cumulative PV curve); AT = actual time elapsed.
  `SPI(t) = ES / AT` and `SV(t) = ES - AT` (in months or weeks), and SPI(t) does not converge.
- **Milestone forecasts beat both.** Re-forecast every key milestone from the schedule logic
  (`project-schedule`): a late task with float left does not move the milestone; a slip beyond
  its float does, by the excess.
- **Helios, end of month 3** (`.claude/skills/cost-management/assets/evm-history-sample.csv`):
  cumulative PV is $161,666 at M2 and $255,000 at M3; EV is $235,500. ES = 2 + (235,500 −
  161,666) / (255,000 − 161,666) = **2.79 months**, SPI(t) = 2.79 / 3 = **0.93**, SV(t) =
  −0.21 months, or **−0.8 weeks** on the period calendar (month 3 is weeks 10–13, so ES = 9 +
  0.791 × 4 = 12.16 weeks against 13 elapsed). That agrees with the schedule logic: "SSO working
  in test", an interim milestone inside Identity / SSO integration (task C, baseline
  2026-07-03), is forecast 2 weeks late, so C finishes 2026-07-24, one week past its late finish
  of 2026-07-17 (1 week of float). M4 is therefore forecast 1 week late, and so is M6, because
  the plan holds no schedule reserve before GA. Helios is 47% complete, so SPI still carries
  information.

## 5. Cost: rate the forecast, not just the index
- **Pick the EAC formula that matches the cause** (`.claude/skills/cost-management/references/earned-value.md`):
  BAC / CPI when the trend will continue (default), AC + (BAC − EV) for a one-off variance, the
  composite when cost and schedule pressure compound. State which one you rated on.
- **When the EAC range straddles a threshold**, rate on the formula you believe, show the range,
  and name the condition that would make you switch — that becomes a red trigger (section 8).
- **Read VAC against the money ladder.** VAC < 0 means the contingency inside BAC is forecast to
  run out; beyond BAC + management reserve, even the sponsor's reserve cannot cover it and the
  steering committee must re-plan or re-baseline; beyond the tolerance it is RED.
- **Check realism with TCPI.** If TCPI(BAC) is more than 0.10 above the CPI achieved so far,
  landing on BAC is not credible; the cumulative CPI rarely improves much after about 20%
  complete. Report the re-plan, not the hope.
- **Agile work without EVM:** forecast cost as spend to date + cost per sprint × sprints still
  needed (likely and pessimistic) and test that against the same ladder.

## 6. Scope and quality: show the pending pressure
- The scope row always carries a **pending change requests** line: how many, their ids, their
  cost and days, who decides and when, and committed + pending against the remaining
  contingency. Pending changes are where the next slip comes from.
- Approved changes are not scope pressure once they are in the baseline and funded; changes being
  built without approval are RED (creep), however small.
- Quality rates the evidence the next gate needs. A fix date that depends on a blocked item
  counts only while the blocker itself has an owned, dated plan; once that plan slips or an item
  goes overdue, the dimension is AMBER.

## 7. Rolling up to the overall RAG
1. The overall rating is **no greener than the worst material dimension**. A dimension is
   material when it can move an objective, a committed milestone or the funding envelope —
   normally all four.
2. A RED work package or interim milestone makes its dimension **at least AMBER**, and is listed
   by name in the report with its owner and action, even when the dimension is AMBER.
3. A **recovery plan changes the colour only when it is approved, funded and already in the
   forecast.** A proposed plan is a decision request, not a rating. Do not report "red with a plan"
   as amber.
4. After a sponsor-approved re-baseline, rate against the new baseline and footnote the change
   for as long as readers compare with the old one.

## 8. Previous rating, trend and red triggers
- Record each period's ratings in a copy of `assets/rag-history-template.csv` (one row per
  dimension per report). The trend arrow compares this report's evidence with the last row:
  **↑ improving**, **→ steady**, **↓ worsening** — written as words too.
- A dimension that was RED last period and whose evidence has not changed is still RED; do not
  quietly relabel it. A colour change needs a changed measure in the log.
- For every AMBER dimension, write its **red trigger**: the measurable condition, and its date,
  that would turn it RED. Readers then see the cliff edge before the project reaches it.
- When EVM is closed monthly but the report is weekly, carry the latest close forward, label it
  ("EVM as at the month-3 close"), and let the trend for cost and schedule move only with new
  evidence (a new close, a milestone forecast, a fired trigger).

## 9. Setting RAG honestly
- **Evidence first, colour second.** Rate against the threshold, not against effort or mood.
- **Green is a claim.** If you cannot point to the measure that makes it green, it is at least
  amber.
- **Escalate early.** Turning amber when the forecast first leaves plan gives the sponsor time to
  act; a late jump from green to red destroys trust. Tell the sponsor before the report goes out.
- **Same rules every period, same numbers for every audience.** The figures in the report must
  match the EVM output, issue log and change log of the same status date.

## 10. Worked example: Helios weekly report of 2026-07-10
The steering pre-read for the bi-weekly steering committee of 2026-07-14. EVM is as at the
month-3 close (`cost-management`: CPI 0.93, SPI 0.92, AMBER); the other evidence is as at
2026-07-10. The filled report is `assets/status-report-sample.md`; the history behind the trend
arrows is `assets/rag-history-sample.csv`.

| Dimension | Evidence | Test that decided it | Rating, trend |
|---|---|---|---|
| Schedule | SPI 0.92, SPI(t) 0.93; "SSO working in test" (interim milestone in task C) forecast 2026-07-17 (+2 weeks), so C finishes 2026-07-24, 1 week past its late finish; M4 forecast 2026-08-14 and M6 2026-10-10 (+1 week each, no schedule reserve before GA); the pessimistic release forecast also misses M6 | M4 and M6 slips inside the 2-week tolerance; SPI in 0.85–0.95 | **AMBER**, → steady |
| Cost | EAC $535,032 (BAC / CPI; range $516,500–$558,468), VAC −$35,032 (−7.0%), TCPI(BAC) 1.07 vs CPI 0.93 | EAC above BAC and above BAC + management reserve ($525,000) by about $10,000, still inside the $550,000 tolerance; CPI in 0.85–0.95 | **AMBER**, → steady |
| Scope | CR002 partner logins pending ($18,000, 10 days, MEDIUM, CCB on 2026-07-14); $28,000 of contingency undrawn after CR003, while the SSO crash option ($20,000) and CR002 together need $38,000 | Pending change above the PM's tolerance; committed + pending beyond the remaining contingency | **AMBER**, ↓ worsening |
| Quality | Stale QA data (I003) 2 days overdue, so test results are unreliable; real-provider journey tests (ACT003) still blocked until SSO works in test; I002 and the two S4 acceptance conditions due 2026-07-17; no gate failed | Something the M4 gate depends on is overdue (GREEN at 2026-07-03, when every item still had a dated fix) | **AMBER**, ↓ worsening |
| Work packages | 1.3.1 Identity / SSO integration RED (CPI 0.69, SPI 0.75); 1.3.4 Reporting & analytics RED (CPI 0.71, SPI 0.67) | Listed by name with owners (Ben Adeyemi, Carla Diaz) | — |

Roll-up: no dimension is RED, the worst is AMBER, so the **overall RAG is AMBER — previous
(2026-07-03) AMBER, trend ↓ worsening**: scope and quality worsened this week, while cost and
schedule hold where the month-3 close left them (CPI 1.00 → 0.93 and SPI 0.94 → 0.92 since the
month-2 close). The recovery plan for SSO is
not counted: it is the decision requested (DEC002). **Red triggers:** SSO not working in test by
2026-07-24 (each week past the plan's 2026-07-17 moves M4 and M6 a week, so both would then be
more than 2 weeks late), or an EAC above $550,000 — the composite forecast is already there if the
schedule slip keeps adding cost, and the $20,000 crash option on top of the CPI forecast
($555,000) would cross it too.
