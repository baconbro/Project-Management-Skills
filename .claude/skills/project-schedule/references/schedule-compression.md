# Schedule Compression

Compression shortens the project **without reducing scope**. Two techniques exist — crashing
(buy time with resources) and fast-tracking (overlap work and accept rework risk) — and both
only work on tasks that sit on *every* critical path. Everything below uses the sample Helios
project (a fictional customer self-service portal used throughout this catalog) and
`assets/schedule-sample.csv`: critical path A → B → D → F → G → H → J, 18 weeks.

## 1. Confirm you need to compress
Run the network with the imposed finish as a target:

```bash
python .claude/skills/project-schedule/scripts/critical_path.py .claude/skills/project-schedule/assets/schedule-sample.csv --unit weeks --target 15 --near-critical 1
```

`Target 15 weeks: MISSED by 3 weeks`. Before spending money, check the alternatives with the
sponsor: move the date, cut scope through `change-request`, or accept the risk. Compression is
the right answer when the date is fixed and the scope is not negotiable.

## 2. Crashing — add resources to critical tasks
Crashing trades money for time. For each critical task that *can* be shortened, record the
normal and crashed duration and cost, then compute the **cost slope**:

    cost slope = (crash cost − normal cost) / (normal duration − crash duration)

Procedure:
1. Crash the critical task with the **cheapest slope** by one unit.
2. Re-run the tool. If a second path has become critical (the tool prints `Critical paths (2)`
   and `tasks on all of them`), the next unit must come from a task shared by every critical
   path, or from one task on each path.
3. Stop when the target is met, when no slope is cheaper than what a unit of time is worth to
   the business, or when a task cannot be crashed further (adding people to a late task can
   make it later — coordination overhead grows faster than output).

Illustrative Helios crash table (the costs are assumptions for the example, not canon):

| Task | Normal → crash (weeks) | Extra cost | Slope per week | Note |
|---|---|---|---|---|
| B UX design & prototype | 2 → 1 | $6,000 | $6,000 | second designer, one usability round |
| G System & UAT testing | 4 → 3 | $8,000 | $8,000 | second QA engineer, extra environment |
| F Reporting & analytics | 2 → 1 | $10,000 | $10,000 | analytics contractor |
| D Self-service UI | 4 → 3 | $12,000 | $12,000 | contract frontend developer |
| C Identity / SSO integration | 5 → 4 | $20,000 | $20,000 | vendor premium support (R001) |
| A, H, J | not crashable | — | — | workshops, security review and sign-offs are fixed |

**Worked example, 18 → 15 weeks:**

| Step | Action | Duration | Critical path(s) after the step | Cumulative cost |
|---|---|---|---|---|
| 0 | baseline | 18 | A-B-D-F-G-H-J; near-critical C (TF 1), I (TF 1) | $0 |
| 1 | crash B 2 → 1 (cheapest, on every path) | 17 | A-B-D-F-G-H-J; C and I still TF 1 | $6,000 |
| 2 | crash G 4 → 3 (next cheapest, shared) | 16 | A-B-D-F-G-H-J; C TF 1, I TF 1 | $14,000 |
| 3 | crash D 4 → 3 | 15 | **two** paths: A-B-D-F-G-H-J and A-B-C-G-H-J | $26,000 |

Reproduce step 3 by editing the durations in a copy of the sample and running the tool: it
prints both paths and `tasks on all of them: A, B, G, H, J`. B and G are already at their
crash limit and A, H, J cannot be crashed, so a cut to 14 weeks would need F (or D) **and** C
together — at least $30,000 — and would crash the vendor-dependent SSO task that step 3 has
already stripped of its float: risk R001 (0.4 × $120,000) would become a near-certain schedule
hit. That is the point to stop and take the remaining gap to the sponsor.

## 3. Fast-tracking — overlap work that was sequential
Fast-tracking costs little money but adds **rework risk**. Candidates are the *discretionary*
links on the critical path (see `references/dependency-types.md`):

- Helios: start D *Self-service UI* after the first week of B *UX design* (structure agreed,
  prototype still in progress). Encode it as a split — `B1,UX design (structure),1,A`,
  `B2,UX design (prototype),1,B1`, `D,Self-service UI,4,B1` (C and E keep waiting for B2) —
  and re-run: the project shortens to 17 weeks, and the tool now shows **two** critical
  paths, because the SSO path A-B1-B2-C-G-H-J is also 17. Log the consequence in
  `risk-register`: R005 *Minor UI rework after usability testing* rises from 0.7 × $4,000
  towards certainty, and C has lost its float.
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
  P50 ≈ 19.3, **P80 ≈ 20.4** and P90 ≈ 21.0 weeks against a deterministic 18. Reserve at P80 ≈
  2.4 weeks.
- From PERT only: `estimation`'s `pert_estimate.py --ids A,B,D,F,G,H,J` totals the critical
  chain (19.17 weeks expected, with its standard deviation).

Hold the reserve **once**, at the end of the project or in front of a fixed milestone, and
show it in the baseline. Helios's charter window of 6 months leaves room for it above the
18-week network; do not spread it back into the task durations.

## 6. Interaction with resource leveling
Crashing adds demand on the same weeks: re-run the capacity check in `resource-management`
after every crash. Leveling an over-allocated person can lengthen the schedule again
(the *resource-constrained* critical path), so level first, then compress, then re-check.

## 7. Record the decision
Compression changes the baseline: raise it through `change-management`, update the cost
baseline in `cost-management` with the crash cost, add the rework and vendor risks to
`risk-register`, and re-baseline in `project-planning`.
