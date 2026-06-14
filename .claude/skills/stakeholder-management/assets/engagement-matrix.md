# Engagement Assessment Matrix

Maps each stakeholder's **current** engagement against the **desired** level the project
needs. Mark current with `C` and desired with `D` in the row. Where C and D differ, an
engagement action is required to close the gap; the size of the gap sets the priority.

## Engagement levels (left = lowest, right = highest)

| Stakeholder            | Unaware | Resistant | Neutral | Supportive | Leading |
|------------------------|---------|-----------|---------|------------|---------|
| Dana Okoye (Sponsor)   |         |           |         | C          | D       |
| Marcus Bell (Security) |         |           | C       | D          |         |
| Priya Shah (Ops Lead)  |         | C         |         | D          |         |
| Beta Customers         |         |           | C       | D          |         |
| IdentityCo (Vendor)    |         |           | C       | D          |         |
| Finance Controller     | C       |           | D       |            |         |
| Web Platform Team      |         |           | C       | D          |         |
| Legal/Privacy Officer  | C       |           | D       |            |         |

## How to read it
- **C only (no gap):** maintain — do not over-invest.
- **C left of D:** raise engagement — the most common case; design a concrete action.
- **C right of D:** an over-engaged stakeholder consuming attention you need elsewhere;
  dial back gracefully.

## Closing the gaps (priority order by gap size and power)
1. **Priya Shah** — Resistant → Supportive. Biggest attitudinal gap on a high-interest
   stakeholder. Action: involve her in design, run the first pilot with her team, name
   the job-impact concern openly.
2. **Marcus Bell** — Neutral → Supportive on high power. Action: early threat-model review
   and a clear sign-off gate so security feels in control.
3. **Finance Controller / Legal** — Unaware → Neutral. Action: a single onboarding briefing
   plus a standing summary so they are never blindsided.

## Cadence
Re-run this matrix at each major milestone or stage gate. Engagement is not static —
a Supportive stakeholder can slide to Resistant after one bad surprise. Feed every required
action into `project-communication` so it becomes a scheduled message with an owner, and
confirm responsibilities in `raci-matrix`.
