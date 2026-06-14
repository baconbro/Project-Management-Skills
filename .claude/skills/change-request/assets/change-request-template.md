# Change Request — <CR ID>

| | |
| --- | --- |
| **Change ID** | CR001 |
| **Title** | <short title> |
| **Project** | Helios — customer self-service portal |
| **Raised by / date** | <name> / <date> |
| **Status** | Open / Approved / Rejected / Deferred |

## 1. Description
<What is being asked, in plain language. One or two sentences someone outside the room
can understand. Example: Add single sign-on so customers log in with their corporate
identity provider instead of a separate portal password.>

## 2. Justification
- **Reason / driver:** <why this is needed, and why now.>
- **Cost of doing nothing:** <what happens if this is rejected.>

## 3. Impact assessment
Rate each 1-5 (see `references/change-request-fields.md`); quantify in real units.

| Dimension | Score (1-5) | Detail (units) |
| --- | --- | --- |
| Scope | 4 | Adds an auth flow; touches login and onboarding screens |
| Cost | 4 | ~$25k integration + licensing |
| Schedule | 5 | ~3 weeks; pushes UAT |

(Run `python scripts/change_impact.py assets/change-log.csv` to score and prioritize.)

## 4. Options
| # | Option | Pros | Cons |
| --- | --- | --- | --- |
| A | Do nothing | No cost, no delay | Customers keep a separate password; raiser's need unmet |
| B | Implement SSO now | Meets the need; better UX | +$25k, +3 weeks, delays UAT |
| C | Defer SSO to a fast-follow release | Protects launch date | Two logins at launch; rework risk |

## 5. Recommendation
<Which option you advise and why, in one or two sentences.>

## 6. Decision
| | |
| --- | --- |
| **Decision** | Approved / Rejected / Deferred |
| **Decided by** | <name / change board> |
| **Date** | <date> |
| **Conditions / notes** | <e.g. approved subject to added budget> |

Route the recorded decision through `change-management` for the master change log.
