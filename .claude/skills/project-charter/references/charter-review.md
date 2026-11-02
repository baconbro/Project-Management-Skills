# Charter review, sign-off verification and re-approval

Load this when reviewing a charter (your own draft or someone else's), checking that a charter
is genuinely approved, or deciding whether a change needs the sponsor's re-approval. Examples
use the sample Helios project (a fictional customer self-service portal used throughout this
catalog); its approved charter is `assets/charter-sample.md`.

## 1. Review rubric
Rate each line PASS or FAIL and record the fix for every FAIL. A charter goes to the sponsor
only with no FAIL left, or with each remaining FAIL named in the cover note as an open point.

| # | Check | FAIL looks like | Fix |
|---|---|---|---|
| 1 | One named sponsor with budget authority | "Steering committee" or "IT and Operations" as sponsor; a sponsor who cannot fund it | Name one executive; if none will sign, stop and go back to `project-initiation` |
| 2 | Named PM with written authority | PM unnamed, or authority "as needed" | Name the PM; write limits in money and days (section 9) |
| 3 | Business case referenced or waived | No case and no recorded waiver | Reference the approved case, or record who waived it and why |
| 4 | Business need is plain and measurable | Solution described instead of problem ("build a portal") | State the pain and its size first |
| 5 | Every objective has metric, baseline, target, date, owner | "Improve satisfaction"; target without baseline | Rewrite SMART; give it an id (OBJ-n) |
| 6 | In scope stays at outcome level | A feature list or requirements in the charter | Keep outcomes; move detail to the scope statement (`scope-and-requirements`) |
| 7 | Out-of-scope list exists with destinations | No exclusions, or exclusions with no reason | Add the items stakeholders are most likely to assume are included |
| 8 | Milestones are few and testable | A task schedule, or milestones with no "what must be true" | Keep 3–6 milestones with an evidence statement each |
| 9 | Budget is a range with basis and funding source | A single precise figure before planning; no source | Give a range, its basis, whether reserves are included, and pre-baseline spend |
| 10 | Assumptions have owner and validate-by | Assumptions with nobody to check them | Add owner, date and consequence if false |
| 11 | Top risks are 3–5, cause → event → effect, owned | "Resource risk"; 25 risks copied from a register | Rewrite the top few; leave the rest for `risk-register` |
| 12 | Approval requirements name a person per item | "The business will sign off" | Name who approves the charter, baseline, deliverables, releases, completion, benefits |
| 13 | Exit and cancellation criteria are measurable | No stop rule, or "if the project fails" | Add triggers with a threshold, a check point and who checks |
| 14 | Consistent with the business case | Budget range, benefit or dates differ from the approved case | Align, or explain the change and get it approved |
| 15 | One to two pages, no `<placeholder>` left | Template text still present; ten pages | Cut detail to planning artifacts; fill or delete every placeholder |

## 2. Sign-off verification
Run this before anyone treats the charter as authority to spend, hire, contract or kick off.
Every item must hold; otherwise the status is Draft.

- [ ] The approver in section 11 is the sponsor named in the header (not a delegate without a
      written delegation).
- [ ] The decision is recorded as Approved, or Approved with conditions with each condition
      listed and an owner and due date for each.
- [ ] The approved version equals the current version of the document; no edits since.
- [ ] The approval is dated and the evidence (signature, e-mail or workflow record) is filed
      with the charter.
- [ ] The header Status reads Approved and the version history has the approval line.
- [ ] The PM has accepted the appointment and the budget holder has confirmed the funding.
- [ ] The approved charter is distributed to the key stakeholders and stored where the project
      records live.

Helios: Dana Okoro approved v1.0 on 2026-04-02 with no conditions; Sam Lee accepted the
appointment and Finance confirmed funding the same day; Status set to Approved, and the
charter was circulated before the kickoff.

## 3. Changing an approved charter
The charter changes rarely. Re-approval by the sponsor (new version, new sign-off line) is
required when any of these change:
- an objective, its target or its date;
- an in-scope outcome or an exclusion (not the detail inside the scope statement);
- the budget range, or a fixed milestone such as M4 or M6;
- the sponsor, the PM or the PM's authority;
- the approval requirements or the cancellation criteria.

Changes inside the boundaries (a requirement, a date that keeps the milestone, a cost inside the
range) go through change control (`change-request`, `change-management`), not a charter
revision. After baselining, a change that crosses a charter boundary is both: a change request
that the sponsor decides, followed by a charter re-issue.

Helios: CR001 (live-chat widget) was deferred to phase 2 at the steering committee on
2026-06-16 because live chat is outside the chartered scope; approving it would have needed a
charter revision as well as the change request. CR006 (cut the pilot cohort from 200 to 50)
saves money and is LOW on cost, but it changes the chartered 200-customer pilot and the
cancellation criterion that counts against it, so it is Dana Okoro's decision with a charter
re-issue if approved, not the PM's (it was withdrawn: the pilot ran with the full cohort of 200).

## 4. Common defects found in review
- A sponsor who never reads the charter: sign-off is a formality, so the first real decision
  arrives as an escalation. Walk the sponsor through sections 2, 3, 5 and 10 before asking for
  the signature.
- Exit criteria that only describe success: a project with no stop rule can end only by
  finishing, however poor the forecast becomes.
- PM authority that conflicts with the later change-control tolerances: set them once here and
  reuse the numbers in `change-management`.
- A charter rewritten as a plan: schedules, WBS and detailed costs belong in `project-planning`.
