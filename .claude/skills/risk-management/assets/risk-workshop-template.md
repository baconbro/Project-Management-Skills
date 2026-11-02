# Risk Identification Workshop — <project name>

Fill-in template for an identification workshop or a pre-mortem: replace every `<placeholder>`.
Technique guidance and worked examples are in `../references/identification.md`.

| Field | Value |
|---|---|
| **Session type** | `<identification workshop / pre-mortem / both>` |
| **Date, length** | `<yyyy-mm-dd>`, `<90 minutes>` |
| **Facilitator / scribe** | `<name>` / `<name>` |
| **Participants** | `<team members, product owner, operations, vendor, finance, security, compliance>` |
| **Pre-reads** | `<charter, scope or WBS, schedule, estimates, assumptions and constraints log, lessons learned, current register>` |
| **Register to update** | `<path to your copy of .claude/skills/risk-register/assets/risk-register-template.csv>` |

## Agenda
| Time | Step | Prompt or rule |
|---|---|---|
| 0:00-0:10 | Context and rules | A risk is uncertain and in the future; anything already happening goes to the issue log. Look for opportunities too. No debate on severity today. |
| 0:10-0:30 | Brainstorm by category | Work through the category prompts below; one risk per sticky note or row |
| 0:30-0:45 | Assumptions and constraints walk | For each line of the log: "What if this is false?" |
| 0:45-1:05 | Pre-mortem | "It is `<key milestone date>` and `<project>` has failed. What happened?" Then: "It beat every target. Why?" |
| 1:05-1:20 | Cluster and rewrite | Merge duplicates; rewrite each as cause → event → effect; move issues out |
| 1:20-1:30 | Owners and next steps | Nominate an owner per risk; agree when scoring happens (`<date>`) |

## Category prompts
- **Scope:** unclear or unstable requirements, unapproved additions, acceptance disputes.
- **Schedule:** critical-path dependencies, external dates, approvals, lead times.
- **Cost:** estimate uncertainty, price changes, consumption-based services.
- **Technical:** new technology, integrations, performance, data migration.
- **Resourcing:** key people, availability, skills, onboarding.
- **Vendor:** delivery, quality, contract terms, vendor viability.
- **Security and compliance:** data protection, accessibility, regulatory change.
- **Organizational change:** adoption, training, resistance, operational readiness.
- **Benefits and opportunities:** earlier, larger or reusable benefits; cheaper ways to deliver.

## Capture sheet
| # | Cause (because ...) | Event (... may ...) | Effect (leading to ...) | Threat / opportunity | Category | Proposed owner | Early-warning sign | Technique |
|---|---|---|---|---|---|---|---|---|
| 1 | `<cause>` | `<uncertain event>` | `<effect on an objective>` | `<threat / opportunity>` | `<category>` | `<name>` | `<observable sign>` | `<brainstorm / checklist / assumptions / pre-mortem / SWOT>` |

## Moved to the issue log (already happening)
| # | What is happening | Raised by | Issue id |
|---|---|---|---|
| 1 | `<description>` | `<name>` | `<id in the project-delivery issue log>` |

## Exit check
- [ ] At least four categories are represented.
- [ ] At least one opportunity is captured.
- [ ] Every risk is written as cause → event → effect and has a proposed owner.
- [ ] Everything already happening has moved to the issue log.
- [ ] Every risk is logged in the register by `<date>`, with its `type` and `owner`.
