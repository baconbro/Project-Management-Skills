# Acceptance at closure — getting a real "yes"

Load this for step 1 of the workflow. Formal acceptance is the moment the people who asked
for the work agree, in writing, that it meets the criteria they agreed. It is not the same as
verification: a passed test or a signed-off UAT shows the product *works*; acceptance is the
named acceptor's decision that it is *what was asked for* (scope validation). A project
cannot close without it, and nobody else will obtain it for you: this step is where it
happens, whether or not acceptance criteria were ever written. The examples use the sample
Helios project (a fictional customer self-service portal used throughout this catalog).

## 1. Where the criteria come from
Use the first source that exists, and say in the acceptance record which one you used.

| Order | Source | Owning skill | What to take |
|---|---|---|---|
| 1 | Scope statement: deliverables table and acceptance log | `scope-and-requirements` | Each deliverable's acceptance criteria and named acceptor; the acceptances already logged during delivery; the traceability matrix rows still not `accepted` or `deferred` |
| 2 | Definition of done, quality-gate exit criteria, UAT sign-off | `quality-management` | The thresholds the evidence must meet (for example zero open severity-1/2 defects) |
| 3 | A contract's statement of work, for bought deliverables | `procurement-management` | The contractual acceptance criteria; the vendor is paid only on acceptance |
| 4 | The charter's objectives and success criteria | `project-charter` | The outcomes the sponsor authorised; turn them into checklist criteria (section 2) |
| 5 | Nothing written | — | Agree acceptance with the sponsor now (section 2) |

Interim acceptances count. Deliverables are normally accepted one by one during delivery
(in `project-delivery`, recorded in the scope statement's acceptance log), at sprint reviews
or at stage gates; final acceptance confirms the set is complete and decides only what is
left. If nothing was accepted during delivery, every deliverable is decided here.

## 2. No criteria were ever agreed: agree them now
This is the common case on small or informally run projects. Do not send the project back to
delivery to "get criteria" — agree them here, in this order:
1. **List what was produced** (from the WBS, the release notes or a walk round the team) and
   **what was asked for** (charter, kickoff notes, the original request or email).
2. **Write two to five checklist-style criteria per deliverable.** Each is observable and
   pass/fail: "the 150 migrated articles are searchable by title and keyword", not "the
   knowledge base is good". Derive them from the charter's success criteria where they exist,
   otherwise from the original request. The checklist and Given/When/Then styles are
   described in `quality-management`.
3. **Keep benefits out.** An outcome that only shows months after go-live ("tickets fall
   50%") is a benefit for step 5, not an acceptance criterion. Accept the product that makes
   the benefit possible; hand the benefit to its owner.
4. **Agree the criteria with the sponsor in writing before anyone looks at the evidence.**
   Criteria written after the result is known get bent to fit it, and a sponsor who sees the
   product first tends to raise the bar on the spot.
5. **Record them** in Part A of a copy of `assets/acceptance-record-template.md`, marked
   "agreed at closure on <date>", with the sponsor's agreement.
6. **Log the gap as a lesson** in `lessons-learned`: criteria agreed at the end are weaker
   than criteria agreed at the start.

If the sponsor will not agree any criteria, escalate to whoever authorised the project; an
acceptance nobody will define cannot be given, and the project cannot close cleanly.

## 3. Running the acceptance decision
1. **Entry:** the evidence for each deliverable is attached (test summary, UAT sign-off,
   audit or review reports, the hypercare exit record for a live service), and each
   deliverable has exactly one named acceptor. Specialists who sign evidence (security,
   legal) are not extra acceptors.
2. **Review:** the acceptor checks the deliverable against the agreed criteria only. A new
   expectation is a change request or a phase-2 backlog item, not a reason to reject.
3. **Decision per deliverable:**
   - **Accept.**
   - **Accept with conditions:** small, specific follow-ups, each with an owner and a due
     date, entered in the closeout log. A condition that is really unfinished scope is a
     rejection in disguise.
   - **Reject:** with the failed criterion named. Then choose: fix it on a short, dated fix
     list (only that item goes back to the team, the project does not reopen), accept it as
     a known exception owned by the sponsor, or remove it from scope through
     `change-request`.
4. **Record:** in the scope statement's acceptance log if the project has one, otherwise in
   Part B of the acceptance record. Final acceptance of the product or project is signed by
   the sponsor (Part D).
5. **Deadline:** give acceptors a response window (five working days is typical). Silence is
   not acceptance; at the deadline, escalate to the sponsor. "Deemed acceptance" applies only
   where a contract says so.

## 4. When acceptance stalls
| Symptom | Likely cause | Move |
|---|---|---|
| Acceptor never available | Acceptance seen as low priority, or the wrong acceptor | Sponsor delegates acceptance in writing to a named person |
| "Accept once it is live for a while" | Acceptance confused with benefit | Accept now with a dated condition, or accept at hypercare exit; move the outcome to benefits tracking |
| New requests at the review | Expectations grew during delivery | Record them as change requests or phase-2 backlog items; judge only the agreed criteria |
| Defects found at the review | Verification gap | Severity-1/2: fix list with dates, then re-present. Minor: accept with conditions |
| Acceptor disputes the criteria | Criteria were never really agreed | Go back to section 2, agree them in writing, then decide |

## 5. Helios final acceptance
- **Criteria source:** the scope statement (order 1), with acceptors named per deliverable;
  UAT and test thresholds from the definition of done.
- **During delivery:** Ava Chen accepted increments at each sprint review. The named
  acceptors signed D2 and D3 at M1 and D5, D6 and D8 at the M4 pilot go/no-go (the scope
  statement's acceptance log); D7 Reporting & analytics was accepted by Priya Nair at M5 once a closed month of
  pilot data reconciled, D10 Training & communications by Priya Nair at the M6 go/no-go, D9
  Hardening & launch by Marcus Webb after the GA readiness reviews and the cutover, and D4
  Identity / SSO integration by Marcus Webb after the first production SSO sign-ins at GA on
  2026-10-03.
- **Final acceptance:** Dana Okoro (Sponsor, VP Customer Operations) accepted the product on
  2026-10-14, after the ramp to 100% of customers, with one condition: Priya Nair (Head of
  Support Operations) to accept D11 Operational handover at hypercare exit. Priya Nair signed
  on 2026-10-30 and the condition closed.
- **Requirements:** every in-scope traceability row was `accepted`, except REQ-011 (a Could),
  which was formally deferred to the product backlog Ava Chen now owns.
- **Last deliverable:** D1 Project management outputs is accepted by the sponsor's
  signature on the closure report itself (step 8).

## Anti-patterns
- Sending the user "back to delivery" to obtain acceptance once the work is built; any
  acceptance still missing, and final acceptance, are obtained at closure.
- Treating a passed UAT as acceptance without the acceptor's signature.
- Acceptance by silence ("no complaints in two weeks").
- Criteria written, or tightened, after the evidence has been seen.
- Accepting everything "with conditions" to hit a date, then never closing the conditions.
