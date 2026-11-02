# Initiation checklist — the G0 gate before planning

Load this in step 6 to decide whether a project has finished initiation and may move to
`project-planning`. It is a stage gate, not a to-do list. Each item gets one status:
- **Done** — with evidence someone else could check (document, version, date).
- **Waived** — not needed for this project, with a one-line reason, the risk it leaves and the
  person who accepted it.
- **Condition** — not finished yet but safe to finish during planning; it becomes a gate
  condition with an owner and a due date (section 6).
- **Open** — not done and not acceptable to carry; the gate cannot pass.

Record the result in a copy of `assets/initiation-gate-record.md`; the item numbers below are
the same in the record. The PM prepares the gate; the sponsor decides the verdict. Examples use
the sample Helios project (a fictional customer self-service portal used throughout this
catalog); its filled record is `assets/initiation-gate-record-sample.md`.

Items marked **(B)** are blocking: they must be Done. They can be neither waived nor carried as
conditions, because without them the project is not justified or not authorized.

## 1. Need and justification (workflow step 2, `business-case`)
| # | Item | Passes when (evidence) | Helios |
|---|---|---|---|
| 1 (B) | The problem is stated with its size and the yearly cost of doing nothing | Business case section 2 gives volumes, cost and growth in numbers, not adjectives | 40% of tickets are password resets and order-status questions, about $600,000 a year, growing about 8% a year |
| 2 (B) | At least three options, including do-nothing, are compared on the same criteria and cashflow basis | The options table lists do-nothing (the baseline), do-minimum as a separate option, the recommended option and at least one alternative, and states the basis | Do nothing, do minimum (FAQ page), build the portal (recommended), buy a SaaS portal |
| 3 | The recommended option has whole-life cost, NPV at a stated rate and switching values | The appraisal output and the sensitivity run are attached | NPV $196,174 at 10%; benefits can fall 28% or costs rise 39% before NPV reaches zero |
| 4 (B) | Every benefit has a measure, a **measured baseline** (value, source, date) and a target with a date | Each row of the benefits register has all of them. If the formal baseline window is later (for example "the 3 months before launch"), record today's measured value **and** the rule for the formal window | B001: about 5,000 tickets a month of the two types (ticketing system, December 2025 – February 2026); formal baseline = average of the 3 months before launch; target 50% lower 6 months after launch |
| 5 (B) | Every benefit has a named **benefit owner** outside the project team who has accepted it | The owner column names a person in the business (not the PM or a team member), with dated acceptance (signature, email or minutes) | Priya Nair, Head of Support Operations, for B001 and B002; Dana Okoro for B003 |
| 6 | Dis-benefits are named with the affected group, a measure and a mitigation | Dis-benefit rows exist in the register | 6 FTE of agents redeployed; a temporary CSAT dip at cutover |
| 7 (B) | The funding decision is recorded | Approver, decision, conditions, funding released, date and the next re-approval point are written in the case's decision record (or a waiver of the case names who waived it and why) | Approved by Dana Okoro on 2026-03-20 within $450k–$550k; re-appraised at M1, M4 and M6 |

A benefit without a measured "before" number cannot be proven at `project-closure`, and the
number moves as soon as delivery starts. Measure it now, even roughly, and refine it later.

## 2. Delivery approach (workflow step 3)
| # | Item | Passes when (evidence) | Helios |
|---|---|---|---|
| 8 | The approach is chosen for the recommended option with the checklist count and any override | Section 2 of the gate record cites the five-question checklist in `.claude/skills/senior-pm/references/methodology-selection.md` | 4 Yes, 1 No; the fixed six-month date and budget override to hybrid |
| 9 | Its implications are recorded and the charter states the same approach | Gate record section 2 names the charter form, what planning will baseline and the governance cadence; the charter header matches | Full charter; baseline the frame, backlog the rest; daily stand-up, weekly status report, bi-weekly steering committee |
| 10 | Agile or hybrid: a product owner is named with decision rights and the time to use them | The charter or the register names the product owner and what they decide (waterfall: mark it Done with the note "not applicable") | Ava Chen orders the backlog and accepts increments at sprint reviews |

## 3. Authorization (workflow step 4, `project-charter`)
| # | Item | Passes when (evidence) | Helios |
|---|---|---|---|
| 11 (B) | One sponsor with funding authority is named | The charter names one person, not a committee, who confirmed the authority | Dana Okoro, VP Customer Operations |
| 12 (B) | A PM is named, has accepted, and has written authority | The charter states the PM's limits in money and days and who decides above them | Sam Lee: changes up to $5,000 and 2 working days |
| 13 | Objectives are SMART and match the business case | Each has an id, metric, baseline, target, date and benefit owner, the same as the benefits register | OBJ-1, owner Priya Nair |
| 14 | Scope boundaries are explicit | In-scope outcomes and an out-of-scope list with a reason and a destination per exclusion | Live chat out of scope (phase 2 candidate) |
| 15 | Milestones, budget range, assumptions and constraints are captured | Three to six milestones with what must be true; a range with basis and funding source; assumptions with an owner and validate-by date | M1/M4/M6; $450k–$550k; A1–A5; CON-1–CON-4 |
| 16 | Top risks and stop triggers are written | Three to five risks with owners; cancellation criteria with threshold, check point and checker | Three risks; stop triggers on cost forecast, switching values, identity provider and pilot adoption |
| 17 (B) | The charter is signed on a specific version and funding is confirmed | Status Approved; the sponsor's name, decision, version and date in the sign-off table; the budget holder's confirmation | v1.0 approved by Dana Okoro on 2026-04-02; Finance confirmed the same day |

## 4. Stakeholders (workflow step 5, `stakeholder-management`)
| # | Item | Passes when (evidence) | Helios |
|---|---|---|---|
| 18 | The register covers every identification category | Sponsor, benefit owners, users, people whose work changes, approvers, budget holder, suppliers, dependencies, regulators, neighbours: each filled or explicitly empty; every key row has power, interest, quadrant, engagement approach and an owner | S01–S10 |
| 19 | The sponsor and every benefit owner sit in Manage Closely | Their quadrant in the register | Dana Okoro (S01) and Priya Nair (S02) |
| 20 | Decision-makers and sign-off authorities are named | Every acceptor and approver in the charter appears in the register | Marcus Webb (SSO and security), Hana Sato (data residency, accessibility), Finance (funding) |
| 21 | No critical role is missing | Product owner, tech lead, benefit owner and the key supplier contact are named people | Ava Chen, Ben Adeyemi, Priya Nair, IdentityCo's account manager |

## 5. Readiness to plan (workflow steps 7–8)
| # | Item | Passes when (evidence) | Helios |
|---|---|---|---|
| 22 | The kickoff is scheduled; every Manage Closely row and every approver is invited or briefed separately; the signed charter goes out as the pre-read | Invitation sent with the date, attendees and each one's reason to attend (`kickoff-agenda.md`) | Kickoff 2026-04-07; IdentityCo not invited (waiver W1) |
| 23 | A shared project space holds the initiation pack, with access agreed | The location is written in the gate record; the stakeholder register is restricted | Helios project space; register restricted to Sam Lee, Dana Okoro and row owners |
| 24 | The planning owner, the first planning step and the target baseline approval are agreed | Gate record section 6 names them with dates | Sam Lee; `project-planning` step 1 on 2026-04-08; baseline approval at M1 (2026-05-08) |

## 6. The verdict
The PM walks the list with the evidence open, then the sponsor decides one of:

| Verdict | When | What to record |
|---|---|---|
| **Go** | Every item is Done or Waived | Sponsor, date |
| **Go with conditions** | Every blocking item is Done; every other item is Done, Waived or Condition. The sponsor may also attach a follow-up condition to a Done item | Each condition with an owner and a due date no later than the baseline approval; planning tracks them to closure |
| **Recycle** | Any item is Open, or a blocking item is not Done | The workflow step to redo, who does it and the re-gate date |
| **Stop** | The case fails, no sponsor will take it, or the sponsor decides not to proceed | The reason; file the case so the decision is not relitigated |

Rules:
- A waiver needs a one-line reason, the risk it leaves and the person who accepted it, normally
  the sponsor. Blocking items (B) cannot be waived.
- A condition is not a waiver: it is work that still has to be done, with an owner and a date.
- Re-run the gate if the charter is re-signed or the case is re-appraised before planning starts.

## 7. Scaling the gate
| Situation | Route | What changes |
|---|---|---|
| New project, waterfall or hybrid | Full: all 24 items | Nothing; this is the default |
| New project, agile or small spend | Lean | Items 3 and 6 may be one line each; the charter is a one-page brief with guardrails; item 10 is mandatory; the kickoff becomes a liftoff |
| New phase of an existing project | Re-check | Items 1–7 are re-checked against the latest figures (has a switching value been crossed?); the charter is confirmed or re-signed; the register is re-rated; the benefit baseline is not re-measured unless its definition changed |
| Running project that skipped initiation | Compressed, one to two weeks | Name the sponsor; write the charter for what is actually being done; measure the benefit baseline now and note in the record that the true "before" value may be lost; build the register; then hand to `project-planning`, or to `project-delivery` for a one-day interim baseline if work cannot pause |

## 8. Common gaps caught here
- Enthusiastic stakeholders but no accountable sponsor, or a committee named as sponsor.
- A benefit target with no measured "before" number, or the PM named as benefit owner.
- "Options" that are only the recommendation versus do-nothing.
- A charter with objectives but no out-of-scope list, inviting later scope fights.
- A kickoff scheduled before the charter is signed.
- A delivery approach nobody chose, so the governance is improvised later.
- A kickoff invite list taken from the org chart instead of the register, so an approver is
  missing.
