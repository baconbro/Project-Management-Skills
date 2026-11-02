# Change Request — CR003: Accessibility (WCAG 2.2 AA) uplift (sample)

Completed sample for the sample Helios project (a fictional customer self-service portal used
throughout this catalog). It matches row CR003 of `assets/change-log.csv`. Use
`assets/change-request-template.md` for a new CR.

| Field | Value |
| --- | --- |
| **Change ID** | CR003 |
| **Title** | Accessibility (WCAG 2.2 AA) uplift |
| **Project** | Helios customer self-service portal |
| **Raised by / date** | Hana Sato, Legal & Compliance / 2026-06-09 |
| **Status** | Approved |

## 1. Description
Bring every customer-facing portal screen (password reset, order status, knowledge base) up to
WCAG 2.2 level AA and add an accessibility check to the definition of done. Touches WBS 1.3.2
Self-service UI and 1.3.3 Knowledge base.

## 2. Justification
- **Reason / driver:** the company's accessibility policy now requires WCAG 2.2 AA for all new
  customer channels; the baselined acceptance criteria only cover WCAG 2.1 A.
- **Benefit / business-case impact:** keeps the portal usable for every customer the 50% ticket
  reduction depends on; no change to the business-case benefit figures.
- **Cost of doing nothing:** a non-compliant launch, legal exposure, and a retrofit after general
  availability estimated at three times the cost.
- **Urgency:** decide before the Self-service UI build passes its midpoint (2026-07-03);
  afterwards the retrofit cost applies.

## 3. Impact assessment
| Dimension | Rating (1-5) | Detail (real units) |
| --- | --- | --- |
| Scope | 3 | Acceptance criteria of one deliverable (Self-service UI) change; knowledge base templates reused |
| Cost | 3 | $12,000 (accessibility audit $4,000 plus 8 person-days of front-end rework); above the $5,000 PM tolerance |
| Schedule | 2 | +2 working days on Self-service UI, recovered by running the audit in parallel with UAT preparation; no milestone moves |
| Quality | 4 | New non-functional target (WCAG 2.2 AA) added to the definition of done and the UAT exit criteria |
| Risk | 2 | Reduces compliance risk; adds a minor risk that a third-party widget fails the audit |

- **Cost value:** +12,000 · **Schedule days:** +2
- **Secondary risks introduced:** third-party date-picker widget may fail WCAG 2.2 AA (LOW;
  logged in the risk register, owner Devin Patel)
- **Resources affected:** Devin Patel (front end, 8 days), Elena Rossi (UX review, 2 days),
  Frank Müller (accessibility test cases in UAT)
- **Score / impact band / authority:** 2.80 / MEDIUM / CCB — stable under weight changes
  (+0.30 above the MEDIUM line)

## 4. Options
| # | Option | Pros | Cons | Cost / days |
| --- | --- | --- | --- | --- |
| A | Do nothing | No cost, no delay | Non-compliant launch; legal exposure; retrofit later | 0 / 0 |
| B | Full WCAG 2.2 AA uplift now | Compliant at launch; one build cycle | Draws contingency; +2 days on the UI task | $12,000 / 2 |
| C | Uplift password reset only; the rest after GA | Cheaper now | Partial compliance; two releases of rework | $5,000 now + $9,000 later / 1 |

## 5. Recommendation
Option B: it is cheaper than C overall, keeps the launch compliant, and fits inside the
contingency because accessibility gaps are the undocumented-requirements risk (R002)
materialising.

## 6. Decision
| Field | Value |
| --- | --- |
| **Approval authority** | CCB (MEDIUM band; $12,000 is above the $5,000 PM tolerance) |
| **Decision** | Approved with conditions |
| **Decided by / date** | CCB, chaired by Dana Okoro (Sponsor) / 2026-06-30 |
| **Conditions / rationale** | Audit runs in parallel with UAT preparation so no milestone moves; widget risk tracked to closure |
| **Funding source** | Contingency reserve — $12,000 of $40,000 (BAC stays $500,000) |
| **Baselines to update** | Scope (1.3.2 acceptance criteria), cost (move $12,000 from contingency to the 1.3.2 control account), schedule (+2 days on Self-service UI), quality plan (definition of done), risk register (new widget risk) |
| **Implementation owner** | Devin Patel — due 2026-07-31 |
| **Verification** | Frank Müller runs the WCAG 2.2 AA audit in UAT; Sam Lee confirms all five baselines updated — verified by: pending |
| **Closed** | Pending (status moves to Implemented, then Closed after verification) |
