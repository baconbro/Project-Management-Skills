# Retrospective Record: `<sprint, phase, milestone or project name>`

Fill-in template: replace every `<placeholder>`. Use one record per session; for a single
failure or incident use `post-mortem-template.md` instead. Lessons and actions agreed here are
copied into the lessons log (`lessons-learned.csv`).

| Field | Value |
|---|---|
| Review type | `<sprint retrospective / phase or milestone review / post-project review>` |
| Period covered | `<YYYY-MM-DD>` to `<YYYY-MM-DD>` |
| Date and length | `<YYYY-MM-DD>`, `<n>` minutes |
| Facilitator | `<name - not the team's line manager>` |
| Participants | `<names>`; invited but absent: `<names or none>` |
| Format | `<Start/Stop/Continue / 4Ls / Sailboat / Mad/Sad/Glad / 5 whys>` |
| Safety check (optional) | `<average score 1-5, or not run>` |

Ground rules read at the start: the Prime Directive (everyone did the best job they could,
given what they knew at the time, their skills, the resources available and the situation at
hand); we examine the process, not people.

## 1. Check-back on earlier actions
Every action or lesson whose check-back date has arrived, before any new item.

| Lesson or action id | Action | Owner | Due | In the target? Used? Outcome changed? | Result | Next step |
|---|---|---|---|---|---|---|
| `<LL0nn>` | `<action>` | `<name>` | `<YYYY-MM-DD>` | `<yes/no, yes/no, yes/no>` | `<verified / not done / did not work>` | `<none / new date agreed / escalated to ... / back to 5 whys>` |

## 2. Data pack
- Delivery: `<committed vs completed points, predictability %, carry-over; or milestones met vs baseline>`
- Cost and schedule: `<CPI, SPI, variance of the worst work package>`
- Quality: `<escaped defects, failed acceptance criteria, rework>`
- Events in the period: `<issue ids, risks that occurred, change requests, escalations>`

## 3. What we found
| Item | Went well or to change | Votes | Theme |
|---|---|---|---|
| `<one observation, with its evidence>` | `<went well / to change>` | `<n>` | `<theme>` |

## 4. Root causes of the top themes
| Theme | Why chain (each answer explains the line above) | Root cause | Therefore test |
|---|---|---|---|
| `<theme>` | `<why 1 -> why 2 -> ...>` | `<cause in our control>` | `<passes / fails: investigate further>` |

## 5. Lessons and actions
At most one or two actions for a sprint retrospective.

| Lessons-log id | Kind | Category | Impact | Recommendation | Applies to | Owner | Due | Check-back by / date |
|---|---|---|---|---|---|---|---|---|
| `<LL0nn>` | `<improve / repeat>` | `<category>` | `<High / Medium / Low>` | `<verb-first change>` | `<target>` | `<name>` | `<YYYY-MM-DD>` | `<name>` / `<YYYY-MM-DD>` |

## 6. Routing
- Next sprint backlog: `<items added, and the product owner who added them, or none>`
- Issue log in `project-delivery` (beyond the team's authority): `<issue or action ids, or none>`
- Change request or risk register: `<ids, or none>`
- Organisational standards (path C): `<lessons-log ids and their target standards, or none>`

## 7. Close
Return on time invested (1-5): `<average>`. Next check-back: `<date of the next retrospective or gate>`.
