# Schedule Compression

Compression shortens the project **without reducing scope**. Two techniques exist — crashing
(buy time with resources) and fast-tracking (overlap work and accept rework risk) — and both
only work on tasks that sit on *every* critical path. Everything below uses the sample Helios
project (a fictional customer self-service portal used throughout this catalog) and
`assets/schedule-sample.csv`: critical path A → B → D → G → H → J, 25 weeks (2026-04-06 to
2026-09-25); C, E, F and I each have 1 week of float.

## 1. Confirm you need to compress
Run the network with the imposed finish as a target. Suppose the sponsor wanted the plan to
finish three weeks earlier, at week 22 (Friday 2026-09-04), to hold a schedule reserve before
the GA cutover on 2026-10-03:

```bash
python .claude/skills/project-schedule/scripts/critical_path.py .claude/skills/project-schedule/assets/schedule-sample.csv --unit weeks --target 22 --near-critical 1
```

`Target 22 weeks: MISSED by 3 weeks`. Before spending money, check the alternatives with the
sponsor: move the date, cut scope through `change-request`, or accept the risk. Compression is
the right answer when the date is fixed and the scope is not negotiable.

## 2. Crashing — add resources to critical tasks
Crashing trades money for time. For each critical or near-critical task that *can* be
shortened, record the normal and crashed duration and cost, then compute the **cost slope**:

    cost slope = (crash cost − normal cost) / (normal duration − crash duration)

Procedure:
1. Crash the critical task with the **cheapest slope** by one unit. A cheaper task that is not
   critical buys nothing: its float simply grows.
2. Re-run the tool. If a second path has become critical (the tool prints `Critical paths (2)`
   and `tasks on all of them`), the next unit must come from a task shared by every critical
   path, or from one task on each path.
3. Stop when the target is met, when no slope is cheaper than what a unit of time is worth to
   the business, or when a task cannot be crashed further (adding people to a late task can
   make it later — coordination overhead grows faster than output).

Illustrative Helios crash table (the costs are assumptions for the example, not canon):

| Task | Normal → crash (weeks) | Extra cost | Slope per week | Note |
|---|---|---|---|---|
| I Training & communications | 4 → 3 | $5,000 | $5,000 | second trainer (not critical: TF 1) |
| B UX design & prototype | 2 → 1 | $6,000 | $6,000 | second designer, one usability round |
| G System & UAT testing | 4 → 3 | $8,000 | $8,000 | second QA engineer, extra environment |
| E Knowledge base | 9 → 8 | $9,000 | $9,000 | content contractor (not critical: TF 1) |
| H Hardening & launch | 5 → 4 | $10,000 | $10,000 | performance-test contractor; the crash option pre-identified at baseline |
| F Reporting & analytics | 9 → 8 | $10,000 | $10,000 | analytics contractor (not critical: TF 1) |
| D Self-service UI | 10 → 9 | $12,000 | $12,000 | contract frontend developer |
| C Identity / SSO integration | 9 → 8 | $20,000 | $20,000 | vendor premium support (R001; not critical: TF 1); the crash Dana Okoro declined in DEC002 after the SSO slip |
| A, J | not crashable | — | — | workshops and sign-offs are fixed |

**Worked example, 25 → 22 weeks:**

| Step | Action | Duration | Critical path(s) after the step | Cumulative cost |
|---|---|---|---|---|
| 0 | baseline | 25 | A-B-D-G-H-J; near-critical C, E, F, I (TF 1 each) | $0 |
| 1 | crash B 2 → 1 (cheapest critical slope; I at $5,000 is cheaper but not critical) | 24 | A-B-D-G-H-J; C, E, F, I still TF 1 | $6,000 |
| 2 | crash G 4 → 3 (next cheapest critical) | 23 | A-B-D-G-H-J; C, E, F, I still TF 1 | $14,000 |
| 3 | crash H 5 → 4 (next cheapest critical: $10,000 beats D's $12,000) | 22 | **two** paths: A-B-D-G-H-J and A-B-D-G-I-J | $24,000 |

Reproduce step 3 by editing the durations in a copy of the sample (B 1, G 3, H 4) and running
the tool: it prints both paths and `tasks on all of them: A, B, D, G, J`. Crashing D instead
at step 3 would also reach 22 weeks, but for $12,000 rather than $10,000, and it would make C,
E and F critical as well (four critical paths). B, G and H are now at their crash limit and A
and J cannot be crashed, so a cut to 21 weeks needs D, the only crashable task on both
critical paths ($12,000, $36,000 in total). That leaves eight critical paths with C, E and F at
zero float, so the vendor-dependent SSO task loses its last week of float and risk R001
(0.4 × $120,000) becomes a near-certain schedule hit. That is the point to stop and take the
remaining gap to the sponsor.

## 3. Fast-tracking — overlap work that was sequential
Fast-tracking costs little money but adds **rework risk**. Candidates are the *discretionary*
links on the critical path (see `references/dependency-types.md`):

- Helios: start D *Self-service UI* after the first week of B *UX design* (structure agreed,
  prototype still in progress). Encode it as a split — `B1,UX design (structure),1,A`,
  `B2,UX design (prototype),1,B1`, `D,Self-service UI,10,B1` (C, E and F keep waiting for
  B2) — and re-run: the project shortens to 24 weeks, and the tool now shows **four**
  critical paths, because the paths through B2 and C, E or F also take 24 weeks. Log the
  consequence in `risk-register`: R005 *Minor UI rework after usability testing* rises from
  0.7 × $4,000 towards certainty, and C, E and F have lost their float.
- Never fast-track a mandatory link (testing before the code exists); never fast-track an
  external dependency you do not control.
- A lead encoded as a split keeps the overlap visible; folding it into a duration hides it.

## 4. Several critical paths
Once two or more paths are critical, shortening a task on only one of them changes nothing.
The tool lists every critical path (up to 20) and the tasks common to all of them; compress
those first. Use `--near-critical N` after every change: tasks within one unit of the critical
path are the ones that will turn critical next.

## 5. Schedule reserve
Compression consumes the margin that protected the finish date, so size and hold a reserve:

- From the simulation: `--simulate 10000 --seed 42` on the three-point columns gives Helios
  P50 26.94, **P80 28.25** and P90 28.95 weeks against a deterministic 25 (only 10% of trials
  finish by week 25). Reserve at P80 ≈ 3.25 weeks.
- From PERT only: `estimation`'s `pert_estimate.py --ids A,B,D,G,H,J` totals the critical
  chain (26.42 weeks expected, P80 27.70 on the normal approximation). It is lower than the
  simulation because one chain ignores merge bias: C, D, E and F run in parallel and any of
  them can finish last.

Hold the reserve **once**, at the end of the project or in front of a fixed milestone, and
show it in the baseline; do not spread it back into the task durations. Helios cannot: the
25-week plan ends on 2026-09-25 and only the cutover week separates it from GA on
2026-10-03. At baseline Dana Okoro accepted that knowingly: P(GA readiness by week 26) is 27%,
the 2-week M6 tolerance (to 2026-10-17) covers about P75 (P(≤ 28 weeks) = 75%), and the crash
of H above is ready if the forecast passes week 26. An accepted gap like this is recorded as a
sponsor decision, not hidden.

## 6. Interaction with resource leveling
Crashing adds demand on the same weeks: re-run the capacity check in `resource-management`
after every crash. Leveling an over-allocated person can lengthen the schedule again
(the *resource-constrained* critical path), so level first, then compress, then re-check.

## 7. Record the decision
Compression changes the baseline: raise it through `change-management`, update the cost
baseline in `cost-management` with the crash cost, add the rework and vendor risks to
`risk-register`, and re-baseline in `project-planning`.
