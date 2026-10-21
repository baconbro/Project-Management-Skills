---
name: risk-register
description: >-
  Produces and maintains a project risk register — threats and opportunities with
  owners, triggers, responses, residual scores and status — and scores it by exposure
  (probability x impact, i.e. expected monetary value) into HIGH/MEDIUM/LOW bands with
  the bundled risk_score.py helper, which also simulates total threat exposure for
  reserve sizing and checks the register before a review. Use when the user wants to
  create, update, prioritize, or review a risk register or risk log, capture and rank
  project risks, compute exposure per risk and for the portfolio, or decide which
  risks to act on first. Triggers: "risk register", "risk log", "log a risk",
  "prioritize risks", "rank the risks", "risk exposure", "risk scoring",
  "probability-impact grid", "residual exposure". For the broader process of
  identifying, analyzing, responding to, and governing risk, use risk-management.
  Works for waterfall, agile, and hybrid projects.
metadata:
  version: 1.1.0
  category: artifact
  phase: cross-cutting
  related: [project-planning, project-delivery, risk-management, release-and-cutover]
license: MIT
---

# Risk Register

## Overview
The risk register is the living list of identified project risks — threats and
opportunities — with their probability, impact, owner, planned response, trigger, residual
score and status. Scoring it by exposure (probability x impact, i.e. the expected monetary
value or EMV) separates the few risks that need action now from the long tail, and gives
`cost-management` a defensible contingency figure instead of padding. The examples use the
sample Helios project (a fictional customer self-service portal used throughout this
catalog): six risks — five threats and one opportunity — scored against its $500,000 budget.

## When to use this skill
- The user wants to create, update, or review a risk register or risk log.
- The user wants to rank risks, compute exposure for one risk or the whole portfolio, or
  size a contingency reserve from the register.
- The user needs a top-N risk list for a status report or steering pack.
- Do NOT use this for the end-to-end risk *process* (identification workshops, choosing a
  response strategy, governance) — use `risk-management`, which links back here for the artifact.
- Do NOT use this for a problem that is already happening — that is an issue; log it in the
  `project-delivery` issue log.

## Methodology fit
- **Waterfall:** a formal register baselined in planning and re-scored at every stage gate;
  residual exposure after planned responses sizes the contingency reserve in the cost baseline.
- **Agile:** a lightweight risk list re-scored in sprint planning and retros; HIGH risks become
  spikes or backlog items with a named owner, and retired risks are closed each review.
- **Hybrid:** one register, two review loops — team-level delivery risks reviewed in sprint
  planning/retros and pulled into the backlog as spikes; programme-level risks (budget,
  contract, vendor, compliance) reviewed at stage gates/steering, with an agreed exposure
  threshold above which a team risk is escalated to the governance loop.

## Inputs you need
- The agreed **scales**: probability as a fraction (0.4) or a percent (40 or "40%"), or a
  1-5 score; impact in **one** unit for the whole register (money, days, story points) or a
  1-5 score. If the risk plan uses a 1-5 matrix, score with `--prob-scale 1-5 --impact-scale 1-5`.
- The **severity thresholds** from the sponsor's risk tolerance: by default HIGH >= 5% and
  MEDIUM >= 1% of the budget at completion (pass `--bac`), or explicit `--high`/`--medium`.
- For each risk: a specific description, `type` (threat or opportunity), category,
  probability, impact (always a positive magnitude — the type carries the sign), owner,
  response, trigger and status.
- Optional: `residual_probability`/`residual_impact` after the response, and
  `impact_min`/`impact_max` for a threat whose impact is a range (used by the simulation).
- From `risk-management`: the identified risk list and the chosen response strategies.

## Workflow
1. **Agree the scales and thresholds before scoring.** Decide with the sponsor whether
   probability is a fraction/percent or a 1-5 score, which single unit impact uses, and the
   HIGH/MEDIUM bands (default 5% / 1% of BAC; the Helios sample uses `--bac 500000`, i.e.
   HIGH >= $25,000, MEDIUM >= $5,000). Record them in the risk management plan from
   `risk-management` and pass the same `--bac`, `--high`/`--medium` or
   `--prob-scale`/`--impact-scale` flags to `scripts/risk_score.py` on every run. *Done:
   scales and thresholds are written down and everyone scoring the register uses the same ones.*
2. **Log each risk.** Open `assets/risk-register-template.csv` (its rows are the Helios
   sample R001-R006 — replace them, keep the header) and add one row per risk with an id, a
   specific outcome-oriented description ("Identity-provider integration slips past the
   agreed date", not "integration risk"), `type`, `category`, `owner`, `status`, `raised`
   and `review_date`. *Done: every row has an id, description, type and owner.*
3. **Estimate inherent probability and impact** in the agreed scales, in the `probability`
   and `impact` columns of `assets/risk-register-template.csv`. Impact is the positive
   magnitude of the cost (threat) or benefit (opportunity) if the risk occurs; never enter a
   negative number. Cross-check the top few with the quantitative techniques in
   `risk-management`. *Done: every open row has a probability and an impact in the agreed unit.*
4. **Score and rank the register.** From the repo root:
   ```bash
   python .claude/skills/risk-register/scripts/risk_score.py .claude/skills/risk-register/assets/risk-register-template.csv --bac 500000
   ```
   The helper infers the probability scale once for the whole register (it refuses
   ambiguous values between 1 and 5 unless you pass `--prob-scale`), ranks by exposure,
   bands HIGH/MEDIUM/LOW and prints total threat EMV, total opportunity EMV and the net.
   For Helios: R001 is HIGH (0.4 x $120,000 = $48,000), total threat EMV $94,300, opportunity
   EMV $18,000. Rows whose status is Occurred/Retired/Realised/Closed are excluded and the
   count is printed (`--include-closed` scores them). `--top 5 --format md` gives a
   status-report snippet, `--format csv` writes rank/exposure/severity back beside the
   original columns, `--format json` feeds a pipeline. *Done: a ranked, banded register with
   the HIGH risks at the top and a portfolio EMV figure.*
5. **Assign owner, response and trigger; re-score residual exposure.** Every HIGH (and
   material MEDIUM) risk needs a named owner, a response chosen with `risk-management`
   (avoid/transfer/mitigate/accept for threats; exploit/share/enhance/accept for
   opportunities) and a trigger — the observable condition that fires the response. Fill
   `residual_probability`/`residual_impact` with the post-response estimate and re-run
   `scripts/risk_score.py` with `--basis residual` to band and rank on what you still carry.
   For Helios the planned responses cut threat EMV from $94,300 to $52,300. *Done: every
   HIGH/MEDIUM row has an owner, a response, a trigger and residual values.*
6. **Size the contingency reserve.** Summed EMV is the mean of a skewed distribution and
   under-covers most outcomes, so simulate:
   ```bash
   python .claude/skills/risk-register/scripts/risk_score.py .claude/skills/risk-register/assets/risk-register-template.csv --simulate 10000 --seed 42 --reserve 40000
   ```
   It reports mean, P50/P80/P90/P95, a histogram and P(total > reserve); add
   `impact_min`/`impact_max` columns to any threat whose impact is a range (triangular draw).
   Hand the P80 — or the confidence level the sponsor accepts — to `cost-management` as the
   contingency reserve. *Done: the reserve is justified by a confidence level, not by summed EMV.*
7. **Check the register before each review** with `scripts/risk_score.py --check`: it exits 1
   and lists every HIGH/MEDIUM risk with no owner, response or trigger, duplicate ids,
   probabilities of 0 or 100%, and threats whose residual exposure exceeds the inherent one.
   *Done: the check passes, or every listed problem has an owner and a date.*
8. **Review on cadence and close correctly.** Re-score on the agreed cadence (each sprint,
   each steering meeting, every stage gate — `project-delivery` step 4). When a trigger fires
   or a threat **materialises**: execute the planned response, set `status` to `Occurred` in
   `assets/risk-register-template.csv`, open an issue in the `project-delivery` issue log, and
   keep the row for `lessons-learned`. Set `Retired` when the risk window has passed and
   `Realised` when an opportunity is captured. Never delete rows. *Done: every closed row
   carries its closing status, and every materialised risk appears in the issue log.*

Status vocabulary: `Open` (scored) · `Occurred` (threat happened — now an issue) · `Retired`
(window passed or no longer relevant) · `Realised` (opportunity captured) · `Closed` (any other
closure). Only Open-like rows are scored.

## Quality checklist
- [ ] Scales and thresholds are agreed and recorded; every scoring run uses the same flags.
- [ ] Every row has a specific description, type, probability, impact in the agreed unit, and an owner.
- [ ] Impacts are positive magnitudes; upside risks are `type=opportunity`, never negative impacts.
- [ ] The register is scored and sorted by exposure, and `--check` passes.
- [ ] Every HIGH and material MEDIUM risk has a named owner, a response, a trigger and a residual score.
- [ ] The contingency reserve is sized from the simulation at an agreed confidence level.
- [ ] A review cadence is set; closed rows are retained with their closing status; materialised
      risks are mirrored in the issue log.

## Anti-patterns
- Vague risks ("integration risk") that cannot be owned, triggered or scored.
- Mixing impact units (dollars in one row, days in another) so exposure is meaningless.
- Entering threats as negative numbers to make the EMV "come out right" — the `type` column
  carries the sign.
- Scoring a 1-5 matrix against money thresholds (every risk comes out LOW) — pass the 1-5 scales.
- Leaving occurred or retired risks as Open so the portfolio EMV and the reserve stay inflated.
- Reserving the summed EMV and calling it "80% confidence".
- Treating every risk as HIGH — that defeats prioritization.
- A register created in planning and never re-scored.

## Resources
- `assets/risk-register-template.csv` — the register template with the Helios sample rows
  R001-R006 already filled in (replace the rows, keep the header); also the script's sample input.
- `scripts/risk_score.py` — scores exposure/EMV and bands, residual exposure, `--simulate`
  Monte Carlo, `--check`, `--top`, `--format table|json|csv|md`, `--bac`, `--prob-scale`,
  `--impact-scale`, `--basis`, `--include-closed`. Run
  `python .claude/skills/risk-register/scripts/risk_score.py --help` for columns, scales,
  formulas and exit codes.
- Unfamiliar term? See the PM glossary in the `senior-pm` skill.

## Related skills
- `project-planning` — where the register is first built and baselined, and where its reserve
  figure enters the cost baseline.
- `project-delivery` — re-scores the register on cadence; a materialised risk becomes an issue
  in its issue log.
- `risk-management` — the identify → analyze → respond → govern process that feeds this
  register and sizes responses from its scores.
- `release-and-cutover` — the go/no-go decision consumes the open HIGH risks and the
  cutover-specific risks logged here.
