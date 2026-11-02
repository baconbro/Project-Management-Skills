# Initiation gate record (G0) — Helios (sample)

> **Sample, not a template.** The G0 record of the sample Helios project (a fictional customer
> self-service portal used throughout this catalog), as decided by the sponsor on 2026-04-06
> and completed at the handoff to planning on 2026-04-08. Do not copy its values; copy
> `initiation-gate-record.md` for your own project.

## 1. Header
| Field | Value |
|---|---|
| **Project** | Helios customer self-service portal |
| **Route** | Full initiation (new project) |
| **Sponsor** | Dana Okoro, VP Customer Operations — Customer Operations investment budget |
| **Project manager** | Sam Lee |
| **Business case** | v1.0, approved by Dana Okoro on 2026-03-20 |
| **Charter** | v1.0, Approved, signed by Dana Okoro on 2026-04-02 |
| **Stakeholder register** | v0.1, 2026-04-03, in the Helios project space (restricted to Sam Lee, Dana Okoro and the row owners) |
| **Project space** | Helios project space, folder "01 Initiation" |
| **Gate held** | 2026-04-06 — prepared by Sam Lee, decided by Dana Okoro |

## 2. Delivery approach
| Field | Value |
|---|---|
| **Option being delivered** | Build the Helios self-service portal (the recommended option) |
| **Checklist count** | 4 Yes of 5: requirements will change as pilot customers react; early delivery is valuable; increments are cheap to release; a product owner is available. No: change is costly for the identity-provider contract |
| **Override** | Fixed six-month date and $450k–$550k budget with 4 Yes → hybrid |
| **Approach** | Hybrid |
| **Charter form** | Full charter |
| **What planning will baseline** | The frame: OBJ-1, the budget, M1/M4/M6 and the fixed elements (SSO through the existing identity provider, the compliance requirements, the Must requirements); Should and Could features as a backlog that flexes inside it |
| **Governance cadence** | Daily stand-up; two-week sprints with review and retrospective every second Friday; weekly status report (Friday); bi-weekly steering committee (Tuesday) |
| **Product owner (agile or hybrid)** | Ava Chen — orders the backlog and accepts increments at sprint reviews |

## 3. Gate items
| # | Item | Status | Evidence (document, version, date) or waiver / condition id |
|---|---|---|---|
| 1 (B) | Problem, size, cost of doing nothing | Done | Business case v1.0 §2: 40% of tickets are password resets and order-status questions (about 5,000 a month), about $600,000 a year; do-nothing cost grows about 8% a year |
| 2 (B) | Three or more options incl. do-nothing | Done | Business case v1.0 §4: do nothing (baseline), do minimum (FAQ page and macros), build the portal (recommended), buy a SaaS portal; all incremental to do-nothing, five years at 10% |
| 3 | Whole-life cost, NPV, switching values | Done | `roi_npv.py` output attached: NPV $196,174, IRR 23.6%, payback 2.85 years; benefits can fall 28% or costs rise 39% before NPV reaches zero |
| 4 (B) | Measured baselines and targets | Done | Business case v1.0 §5 and benefits register v1.0: B001 about 5,000 tickets a month of the two types (ticketing-system extract, December 2025 – February 2026), formal baseline = average of the 3 months before launch, target 50% lower 6 months after launch; B002 26 h mean time-to-resolve → instant self-service, 2 h assisted; B003 CSAT 72% → 80% |
| 5 (B) | Benefit owners outside the team, accepted | Done | Priya Nair (B001, B002) and Dana Okoro (B003), accepted at the business-case approval on 2026-03-20; follow-up C1 |
| 6 | Dis-benefits with mitigation | Done | D001 6 FTE of agents redeployed (Priya Nair: redeployment plan before cutover); D002 CSAT dip at cutover (Dana Okoro: pilot of 200, then staged rollout) |
| 7 (B) | Funding decision recorded | Done | Business case §11: approved by Dana Okoro on 2026-03-20 within $450k–$550k; Discovery released to M1; re-appraised at M1, M4 and M6 |
| 8 | Approach with count and override | Done | Section 2 above |
| 9 | Implications recorded; charter matches | Done | Section 2 above; charter v1.0 header reads Hybrid |
| 10 | Product owner with decision rights | Done | Charter v1.0 §8: Ava Chen |
| 11 (B) | One sponsor with funding authority | Done | Charter v1.0: Dana Okoro, VP Customer Operations |
| 12 (B) | PM named, accepted, authority | Done | Charter v1.0 §9 and §11: Sam Lee accepted on 2026-04-02; up to $5,000 and 2 working days |
| 13 | SMART objectives match the case | Done | Charter v1.0 §2: OBJ-1 = benefit B001, owner Priya Nair |
| 14 | Scope boundaries | Done | Charter v1.0 §3: six in-scope outcomes; six exclusions, each with a reason and a destination (live chat: phase 2 candidate) |
| 15 | Milestones, range, assumptions, constraints | Done | Charter v1.0 §4–6: M1/M4/M6; $450k–$550k from the Customer Operations investment budget; A1–A5 with owners; CON-1–CON-4 |
| 16 | Top risks and stop triggers | Done | Charter v1.0 §7: three risks with owners; §10: five stop triggers with threshold, check point and checker |
| 17 (B) | Charter signed; funding confirmed | Done | Charter v1.0 §11: Approved by Dana Okoro on 2026-04-02; Finance confirmed the same day |
| 18 | Register covers every category | Done | Register v0.1: S01–S10, all ten categories filled, each key row with power, interest, quadrant, approach and owner |
| 19 | Sponsor and benefit owners in Manage Closely | Done | S01 Dana Okoro and S02 Priya Nair: Manage Closely; follow-up C2 |
| 20 | Decision-makers named | Done | S03 Marcus Webb (SSO and security), S04 Hana Sato (data residency, accessibility), S06 Finance (funding) |
| 21 | No critical role missing | Done | Ava Chen (product owner), Ben Adeyemi (tech lead), Priya Nair (benefit owner), IdentityCo's account manager (S05) |
| 22 | Kickoff scheduled; invitees | Waived | W1. Kickoff 2026-04-07 invitation sent 2026-04-03 with charter v1.0 as the pre-read; every other Manage Closely row and the approvers invited |
| 23 | Shared project space | Done | Helios project space, "01 Initiation"; register restricted |
| 24 | Planning owner, first step, baseline date | Done | Section 6 below |

## 4. Waivers
| Id | Item # | What is not done | Why that is acceptable | Risk it leaves | Accepted by | Date |
|---|---|---|---|---|---|---|
| W1 | 22 | IdentityCo (S05, Manage Closely) is not invited to the kickoff | Extending its contract to customer sign-in is a planning-stage make-or-buy decision, not yet signed; its account manager is briefed at the first vendor working session with slides 2–6 of the kickoff deck | The vendor hears the scope second-hand and late | Dana Okoro | 2026-04-06 |

## 5. Verdict and conditions
| Field | Value |
|---|---|
| **Verdict** | Go with conditions |
| **Decided by** | Dana Okoro, 2026-04-06 |
| **Reason** | Justified and authorized; the benefit owner's commitment to the target and the sponsor's review of the engagement gaps still need closing before the baseline |

| Id | Condition | Item # | Owner | Due (no later than the baseline approval) | Status |
|---|---|---|---|---|---|
| C1 | Priya Nair agrees the 50% target in person with Dana Okoro and signs off the benefit baseline method (monthly volume of the two ticket types from the ticketing system; formal window = the 3 months before launch) | 5 | Dana Okoro | 2026-05-08 | Open — kickoff action K3 |
| C2 | Review the ranked engagement matrix with the sponsor | 19 | Sam Lee | 2026-04-15 | Open |

## 6. Initiation pack handed to planning
| Item | Version and location | Received by, date |
|---|---|---|
| Signed charter | v1.0, "01 Initiation" | Sam Lee (planning owner); copy to Ava Chen for requirements, 2026-04-08 |
| Approved business case and benefits register | v1.0, "01 Initiation" | Sam Lee, 2026-04-08; copy to Finance |
| Stakeholder register and engagement approach (restricted) | v0.1, "01 Initiation" | Sam Lee, 2026-04-08 |
| Delivery approach | Section 2 of this record | Sam Lee and Ava Chen, 2026-04-08 |
| Open assumptions and constraints | Charter v1.0 §6 (A1–A5, CON-1–CON-4) | Sam Lee, for the assumptions log, 2026-04-08 |
| Gate conditions and waivers | Sections 4–5 of this record | Sam Lee, 2026-04-08 |
| Kickoff decisions and actions | KD1–KD2 and K1–K5 in the kickoff capture sheets, `log_ref` = local | Sam Lee, 2026-04-08 |

- **First planning step:** `project-planning` step 1 — open the project management plan and the
  assumptions log — owner Sam Lee — starts 2026-04-08.
- **Target baseline approval:** M1 (Discovery complete), 2026-05-08, by Dana Okoro.

## 7. Sign-off
| Role | Name | Decision | Date |
|---|---|---|---|
| Sponsor | Dana Okoro | Go with conditions | 2026-04-06 |
| Project manager | Sam Lee | Prepared | 2026-04-06 |
| Planning owner (pack received) | Sam Lee | Acknowledged | 2026-04-08 |
