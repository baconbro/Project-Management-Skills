---
name: risk-register
description: >-
  Produces and maintains a project risk register and scores it by exposure
  (probability x impact / expected monetary value) into HIGH/MEDIUM/LOW severity
  bands using the bundled risk_score.py helper. Use when the user wants to create,
  update, prioritize, or review a risk register or risk log, capture and rank
  project risks, compute risk exposure or EMV, or decide which risks to act on
  first. Triggers: "risk register", "risk log", "log a risk", "prioritize risks",
  "risk exposure", "risk scoring", "EMV". For the broader process of identifying,
  analyzing, responding to, and governing risk, use risk-management. Works for
  waterfall, agile, and hybrid projects.
metadata:
  version: 1.0.0
  category: artifact
  phase: cross-cutting
  related: [risk-management, project-delivery]
license: MIT
---

# Risk Register

## Overview
The risk register is the living list of identified project risks with their probability,
impact, owner, response, and status. Scoring it by exposure focuses attention on the few
risks that actually matter instead of an undifferentiated list.

## When to use this skill
- The user wants to create, update, or review a risk register or risk log.
- The user wants to prioritize or rank risks, or compute exposure / EMV.
- Do NOT use this for the end-to-end risk *process* (identification techniques, response
  strategies, governance) — use `risk-management`, which links back here for the artifact.

## Methodology fit
- **Waterfall:** a formal register reviewed at stage gates.
- **Agile:** a lightweight risk list reviewed each sprint/iteration; high-severity risks
  may become backlog items.
- **Hybrid:** same register, reviewed on whatever cadence the project runs.

## Inputs you need
For each risk: a short description, a **probability** (0-1 or a percentage), and an
**impact** in consistent units (e.g. dollars or story points). Owner, response, and
status are recommended but optional for scoring.

## Workflow
1. Open `assets/risk-register-template.csv` and add one row per risk. Keep descriptions
   specific and outcome-oriented ("Identity-provider integration slips past the agreed
   date"), not vague ("integration risk").
2. Estimate **probability** (how likely) and **impact** (cost if it occurs) for each risk.
   Use consistent impact units across the register.
3. Score and rank the register:
   ```bash
   python scripts/risk_score.py assets/risk-register-template.csv
   ```
   The tool prints risks sorted by exposure (highest first), assigns HIGH/MEDIUM/LOW
   bands, and reports total portfolio EMV. Adjust bands with `--high` / `--medium`.
4. Assign an **owner** and a **response** to every HIGH (and material MEDIUM) risk. For
   choosing the response type (avoid/transfer/mitigate/accept), use `risk-management`.
5. Set a review cadence and re-score after each update. Closed risks stay in the register
   marked closed, so lessons are not lost.

## Quality checklist
- [ ] Every risk has a specific description, a probability, and an impact in consistent units.
- [ ] The register is scored and sorted by exposure.
- [ ] Every HIGH risk has a named owner and a response.
- [ ] A review cadence is set; closed risks are retained, not deleted.

## Anti-patterns
- Vague risks that cannot be acted on or scored.
- Mixing impact units (dollars in one row, "days" in another) so exposure is meaningless.
- A register that is created once and never reviewed.
- Treating every risk as HIGH — that defeats prioritization.

## Resources
- `assets/risk-register-template.csv` — fill-in register; also the sample input for the script.
- `scripts/risk_score.py` — scores exposure/EMV and severity bands. Run `python scripts/risk_score.py --help`.

## Related skills
- `risk-management` — the full identify → analyze → respond → govern process around this register.
- `project-delivery` — where the register is monitored and acted on during execution.
