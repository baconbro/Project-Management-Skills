# Retrospective Formats

Different formats surface different things. Match the format to the goal: broad reflection,
emotional honesty, momentum analysis, or root-causing a single failure. Rotating formats
also keeps a recurring retro from going stale.

## Start / Stop / Continue

Three columns: what should we **start** doing, **stop** doing, and **continue** doing?

- **Use when:** you want a fast, action-oriented retro that converts directly into
  behaviors. The simplest format and a safe default.
- **Strength:** every item already points at an action.

## 4Ls — Liked, Learned, Lacked, Longed for

- **Liked** — what went well. **Learned** — new knowledge or insight. **Lacked** — what was
  missing. **Longed for** — what the team wished it had.
- **Use when:** you want a fuller reflection that captures learning and unmet needs, not
  just process tweaks. Good at the end of a phase or release.

## Sailboat (a.k.a. speedboat)

Draw a boat: **wind** in the sails (what propels the team), **anchors** (what holds it
back), **rocks** (risks ahead), and the **island** (the goal).

- **Use when:** the team is more visual, or you want to discuss momentum and upcoming risks
  together, not just past events.

## Mad / Sad / Glad

Capture how events made people feel — **mad**, **sad**, or **glad** — then discuss the
causes behind the strongest feelings.

- **Use when:** morale, friction, or team dynamics are the issue. Surfaces emotional
  signal that process-focused formats miss. Needs strong psychological safety.

## 5 Whys

Take one specific problem and ask "why?" repeatedly (about five times) until you reach a
root cause rather than a symptom.

- **Use when:** a single significant failure needs root-causing — a missed milestone, a
  production incident. Pairs well with another format: use the broad format to find the
  problem, then 5 whys to dig into the biggest one.
- **Example (Helios):** UAT slipped -> why? Integration was late -> why? Identity-provider
  sandbox was unstable -> why? Access was requested late -> why? No one owned vendor
  setup -> root cause: vendor onboarding had no named owner in the plan.

## Choosing and running

- **Safety first.** Open with the Prime Directive: everyone did the best they could with
  what they knew. The retro examines the process, not people.
- **Time it well.** Run sprint retros while memory is fresh; run a closure review once the
  outcome is visible.
- **End with actions.** Whatever the format, every retro must produce categorized,
  owned follow-ups in `assets/lessons-learned.csv` — otherwise it was just a chat.
