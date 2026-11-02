# Post-mortem: `<event name>`

Fill-in template for a blameless timeline post-mortem: replace every `<placeholder>`. Hold it
within about five business days of resolution, facilitated by someone who made none of the
decisions under review. The method is in the timeline post-mortem section of
`references/retrospective-formats.md`; the Helios example there (the two-week SSO slip) shows a
completed timeline and a branching 5 whys.

Blameless: we look for the conditions and decisions that let this happen, judged on what was
known at the time. Owners still own actions.

| Field | Value |
|---|---|
| Event | `<what happened, in one sentence>` |
| Detected / resolved | `<YYYY-MM-DD>` / `<YYYY-MM-DD>` |
| Impact | `<High / Medium / Low on the impact scale>`: `<effect on milestones, cost, scope, quality, customers>` |
| Linked records | `<issue, risk and change request ids; incident tickets; status reports>` |
| Facilitator | `<name>` |
| Participants | `<names>` |
| Review date | `<YYYY-MM-DD>` |

## 1. Timeline
Drafted from records before the session, then corrected with the people involved.

| When | What happened (fact) | Source record | What we knew or expected then | Decision point? |
|---|---|---|---|---|
| `<date or time>` | `<event>` | `<log, ticket, report>` | `<knowledge at the time>` | `<yes: see section 2 / no / a gap: no decision was made>` |

## 2. Decision points
| When | Decision | Options considered | Information available then | Who decided | Sound given that information? What would have helped? |
|---|---|---|---|---|---|
| `<date>` | `<decision>` | `<options>` | `<information>` | `<name or forum>` | `<assessment>` |

## 3. What went well
- `<detection, response or workaround worth repeating>`

## 4. Contributing factors
| Factor | Category | In our control? | Evidence |
|---|---|---|---|
| `<condition that, had it been absent, would have prevented or shortened the event>` | `<category>` | `<yes / no: whose>` | `<record>` |

## 5. Root cause (5 whys on the biggest factors)
Problem: `<the event and its measured effect>`

Branch `<A>`:
1. Why? `<answer>`
2. Why? `<answer>`
3. Why? `<answer>`
4. Why? `<answer>`
5. Why? `<answer>` **Root cause:** `<cause in our control>`

Therefore test (read bottom-up, joining each line with "therefore"): `<passes / where it breaks>`.
Add a branch for each other contributing cause.

## 6. Actions
| Lessons-log id | Fix (this project) or prevent (organisation) | Recommendation | Applies to | Owner | Due | Check-back by / date |
|---|---|---|---|---|---|---|
| `<LL0nn>` | `<fix / prevent>` | `<verb-first change>` | `<issue-log id / standard, template or checklist>` | `<name>` | `<YYYY-MM-DD>` | `<name>` / `<YYYY-MM-DD>` |

## 7. Sharing
Reviewed with `<sponsor or steering committee, date>`; shared with `<teams or PMO>`; lessons
copied into the lessons log on `<YYYY-MM-DD>`.
