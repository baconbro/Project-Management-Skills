#!/usr/bin/env python3
"""Critical path method (CPM) for a finish-to-start task network: early/late dates,
total and free float, every critical path, near-critical tasks, calendar dates, a text
Gantt chart and a Monte Carlo schedule-risk simulation. Standard library only.

INPUT COLUMNS / KEYS  (case-insensitive; extra columns are ignored)
    id            unique task identifier                   aliases: task_id, wbs, wbs_id, ref            (required)
    name          task name                                aliases: task, title, activity, description   (optional)
    duration      elapsed duration >= 0; 0 = milestone     aliases: dur, days, weeks                     (required)
    predecessors  ids this task depends on, finish-to-start; may be empty per row
                                                           aliases: preds, pred, predecessor, depends_on, deps, dependencies
                                                           (the column itself is required)
    optimistic    best-case duration  (O)  for --simulate  aliases: o, best, best_case                   (optional)
    most_likely   most-likely duration (M) for --simulate  aliases: m, likely, most likely, mostlikely, ml, mode
    pessimistic   worst-case duration (P)  for --simulate  aliases: p, worst, worst_case
    unit          unit label, one per file                 aliases: units, uom                           (optional)
  Durations are ELAPSED time in one unit (weeks, days ...), never effort; an 'effort' or
  'hours' column without a 'duration' column is rejected. Numbers tolerate '$', ',' and a
  trailing '%' ("1,500" -> 1500); nan, inf, negative and boolean values are rejected.
  Predecessors: "A;B", "A,B" or "A B" (whitespace splits only when no ',' or ';' is present,
  so ids containing spaces must be separated by ',' or ';'); in JSON a string or an array of
  ids. A task that lists itself, an unknown id, or a cycle is an error naming the loop.
  Three-point columns come as a set (all three or none); a row may leave them blank to keep
  its duration fixed in the simulation.
  CSV delimiter is auto-detected (, ; tab |); a UTF-8 BOM and CRLF line ends are tolerated.
  JSON is a list of objects or {"tasks": [...]} and always needs --json (a JSON file passed
  without it is rejected, not misread as CSV).

METHOD  (finish-to-start links only; model lag, SS/FF/SF and leads as explicit lag or
         milestone tasks - see references/dependency-types.md)
  forward pass   ES = max(EF of predecessors), 0 if none;   EF = ES + duration
  project        duration = max EF over all tasks
  backward pass  LF = min(LS of successors), project duration if none;   LS = LF - duration
  floats         TF (total float) = LS - ES;  critical when TF = 0
                 FF (free float)  = min(ES of successors) - EF  (project duration - EF when none)
                 FF can be used without delaying any successor; TF is shared along the chain.
  critical paths every gap-free chain of critical tasks (successor ES = predecessor EF) from a
                 critical task with no predecessors to one with no successors; all are listed
                 (up to 20) because a project only shortens when EVERY critical path shortens.
  --near-critical N   lists non-critical tasks with TF <= N (the second-tier drivers).
  --target T          compares the project duration with an imposed finish T (margin/shortfall).
  --start-date D      maps ES/EF/LS/LF to dates: start = first day of work, finish = last day of
                      work (a milestone has start = finish). Needs --unit days or weeks (or a
                      unit column). --workdays counts Mon-Fri only and skips --holidays FILE
                      (one YYYY-MM-DD per line, '#' comments allowed).
  --gantt             text Gantt after the table: '#' critical, '=' non-critical, '.' float
                      (EF..LF), a diamond for milestones; one column = duration / chart width.
  --simulate N        Monte Carlo: each trial draws every task that has O/M/P from a PERT-Beta
                      (--dist pert, default: alpha = 1 + 4(M-O)/(P-O), beta = 1 + 4(P-M)/(P-O))
                      or a triangular distribution (--dist triangular); other tasks keep their
                      duration. Reports mean, std, min, max, P10/P50/P80/P90 of the project
                      duration, P(duration <= deterministic duration) and <= --target, and a
                      criticality index CI% per task = share of trials in which TF was 0.
                      --seed K makes a run repeatable (a random seed is printed otherwise).

OUTPUT  --format table (default) | json (tasks + summary) | csv (one row per task) | md

EXIT CODES   0 success  -  2 bad input, bad option or internal error ("error: ..." on stderr)

EXAMPLES
  python .claude/skills/project-schedule/scripts/critical_path.py .claude/skills/project-schedule/assets/schedule-sample.csv --unit weeks
  python .claude/skills/project-schedule/scripts/critical_path.py .claude/skills/project-schedule/assets/schedule-sample.csv --unit weeks --near-critical 1 --gantt
  python .claude/skills/project-schedule/scripts/critical_path.py .claude/skills/project-schedule/assets/schedule-sample.csv --unit weeks --start-date 2027-01-04 --workdays --holidays holidays.txt
  python .claude/skills/project-schedule/scripts/critical_path.py .claude/skills/project-schedule/assets/schedule-sample.csv --unit weeks --simulate 10000 --seed 42 --target 20
  python .claude/skills/project-schedule/scripts/critical_path.py schedule.json --json --format json
  cat schedule.csv | python .claude/skills/project-schedule/scripts/critical_path.py - --format csv > schedule-dates.csv
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import difflib
import io
import json
import math
import random
import re
import shutil
import statistics
import sys
from collections import deque

BOM = "﻿"
JSON_KEY = "tasks"
EPS = 1e-9
MAX_PATHS = 20
MAX_TRIALS = 200_000
MAX_CAL_DAYS = 36_500
NAME_WIDTH = 32
DEFAULT_UNIT = "periods"
MILESTONE = "◆"

ID_ALIASES = ("id", "task_id", "wbs", "wbs_id", "ref")
NAME_ALIASES = ("name", "task", "title", "activity", "description")
DUR_ALIASES = ("duration", "dur", "days", "weeks")
PRED_ALIASES = ("predecessors", "preds", "pred", "predecessor", "depends_on", "deps", "dependencies")
O_ALIASES = ("optimistic", "o", "best", "best_case")
M_ALIASES = ("most_likely", "m", "likely", "most likely", "mostlikely", "ml", "mode")
P_ALIASES = ("pessimistic", "p", "worst", "worst_case")
UNIT_ALIASES = ("unit", "units", "uom")
EFFORT_COLUMNS = ("effort", "hours", "person_days", "person-days", "effort_days", "man_days")
SIM_LEVELS = (0.10, 0.50, 0.80, 0.90)


# ----------------------------------------------------------------------------- input helpers
def read_text(path):
    """Read a file, or stdin when path is '-', stripping a UTF-8 BOM (Excel 'CSV UTF-8')."""
    if path == "-":
        text = sys.stdin.read()
    else:
        with open(path, encoding="utf-8-sig", newline="") as fh:
            text = fh.read()
    return text.lstrip(BOM)


def sniff_delimiter(text):
    try:
        return csv.Sniffer().sniff(text[:4096], delimiters=",;\t|").delimiter
    except csv.Error:
        return ","


def load_rows(text, as_json, json_key):
    """Return (rows, headers). CSV auto-detects , ; tab |. JSON: list of objects or {json_key: [...]}."""
    if not as_json and text.lstrip()[:1] in ("[", "{"):
        raise ValueError("input looks like JSON; pass --json")
    if as_json:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON: {exc}")
        if isinstance(data, dict):
            if json_key not in data:
                raise ValueError(f"JSON object must contain a '{json_key}' list; found keys: {sorted(data)}")
            data = data[json_key]
        if not isinstance(data, list):
            raise ValueError(f"JSON must be a list of objects or {{'{json_key}': [...]}}")
        rows, headers = [], []
        for n, item in enumerate(data, 1):
            if not isinstance(item, dict):
                raise ValueError(f"JSON item {n} is not an object: {item!r}")
            row = {str(k).strip(): v for k, v in item.items()}
            rows.append(row)
            for k in row:
                if k not in headers:
                    headers.append(k)
        if not rows:
            raise ValueError("JSON contains no items")
        return rows, headers
    delim = sniff_delimiter(text)
    reader = csv.DictReader(io.StringIO(text), delimiter=delim)
    headers = [(h or "").strip() for h in (reader.fieldnames or [])]
    if not any(headers):
        raise ValueError("input is empty (no header row)")
    lowered = [h.lower() for h in headers if h]
    dupes = sorted({h for h in lowered if lowered.count(h) > 1})
    if dupes:
        raise ValueError(f"duplicate column names: {dupes}")
    rows = []
    for raw in reader:
        if raw.get(None):
            raise ValueError(f"line {reader.line_num}: more cells than header columns ({len(headers)})")
        row = {(k or "").strip(): (v.strip() if isinstance(v, str) else v) for k, v in raw.items() if k is not None}
        if all(v in (None, "") for v in row.values()):
            continue  # skip blank lines
        rows.append(row)
    if not rows:
        raise ValueError(f"no data rows found (headers: {headers})")
    return rows, headers


def _get(row, *names, default=None):
    """Case-insensitive lookup across accepted column aliases."""
    lowered = {str(k).lstrip(BOM).lower().strip(): v for k, v in row.items() if k is not None}
    for n in names:
        v = lowered.get(n.lower())
        if v not in (None, ""):
            return v
    return default


def require_columns(headers, groups):
    """groups = [("probability","prob","p"), ("impact","cost")]: each group needs one alias present."""
    present = {h.lower().lstrip(BOM).strip() for h in headers if h}
    missing = [g[0] for g in groups if not any(a.lower() in present for a in g)]
    if missing:
        raise ValueError(f"missing column(s): {missing}; found headers: {[h for h in headers if h]}")


def _num(raw, where, minimum=None, maximum=None, integer=False):
    """Parse a number tolerant of '$', ',', '€', '£', whitespace and a trailing '%' (which is stripped, value unchanged)."""
    if isinstance(raw, bool):
        raise ValueError(f"{where}: {raw!r} is a boolean, not a number")
    s = str(raw).strip()
    if s.endswith("%"):
        s = s[:-1]
    s = s.replace(",", "").replace("$", "").replace("€", "").replace("£", "").strip()
    try:
        v = float(s)
    except ValueError:
        raise ValueError(f"{where}: {raw!r} is not a number")
    if not math.isfinite(v):
        raise ValueError(f"{where}: {raw!r} is not a finite number")
    if integer and v != int(v):
        raise ValueError(f"{where}: {raw!r} must be a whole number")
    if minimum is not None and v < minimum:
        raise ValueError(f"{where}: {raw!r} is below the minimum {minimum:g}")
    if maximum is not None and v > maximum:
        raise ValueError(f"{where}: {raw!r} is above the maximum {maximum:g}")
    return v


# ----------------------------------------------------------------------------- formatting helpers
def _sanitize(value, width=None):
    """Collapse whitespace/newlines; truncate with an ellipsis when width is given."""
    s = re.sub(r"\s+", " ", str(value if value is not None else "")).strip()
    if width and len(s) > width:
        s = s[: width - 1] + "…"
    return s


def _snap(x):
    """Kill floating-point noise: |x| < EPS becomes 0.0 (never -0), else round to 6 places."""
    x = round(float(x), 6)
    return 0.0 if abs(x) < EPS else x


def _fmt(x):
    """Clean number: thousands separators, up to 4 decimals, no exponent, no -0."""
    s = f"{x:,.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _plain(x):
    """Machine-readable number for CSV: no separators, up to 6 decimals."""
    s = f"{x:.6f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _pct(x):
    return f"{x:.0f}%"


def _quantile(sorted_vals, p):
    """Inclusive linear-interpolation quantile of an already sorted list (0 < p < 1)."""
    n = len(sorted_vals)
    if n == 1:
        return sorted_vals[0]
    h = (n - 1) * p
    lo = int(math.floor(h))
    hi = min(lo + 1, n - 1)
    return sorted_vals[lo] + (h - lo) * (sorted_vals[hi] - sorted_vals[lo])


# ----------------------------------------------------------------------------- parsing
def _blank(raw):
    return raw is None or not str(raw).strip()


def _three_point(row, where):
    """Return (O, M, P) when the row carries all three values, None when it carries none."""
    o_raw, m_raw, p_raw = _get(row, *O_ALIASES), _get(row, *M_ALIASES), _get(row, *P_ALIASES)
    given = [x for x in (o_raw, m_raw, p_raw) if not _blank(x)]
    if not given:
        return None
    if len(given) < 3:
        raise ValueError(f"{where}: optimistic, most_likely and pessimistic must all be given or all be blank")
    o = _num(o_raw, f"{where}, column optimistic", minimum=0)
    m = _num(m_raw, f"{where}, column most_likely", minimum=0)
    p = _num(p_raw, f"{where}, column pessimistic", minimum=0)
    if not (o <= m <= p):
        raise ValueError(f"{where}: require optimistic <= most_likely <= pessimistic "
                         f"(got O={_fmt(o)}, M={_fmt(m)}, P={_fmt(p)})")
    return (o, m, p)


def parse_tasks(rows, headers):
    """Validate rows into task dicts (input order kept); predecessors are resolved afterwards."""
    present = {str(h).lower().lstrip(BOM).strip() for h in headers if h}
    if not any(a in present for a in DUR_ALIASES):
        found = [c for c in EFFORT_COLUMNS if c in present]
        if found:
            raise ValueError(f"column '{found[0]}' found but no 'duration': effort is not duration - convert it "
                             f"first (duration = effort / assigned FTE, see the estimation skill) and add a "
                             f"duration column")
    require_columns(headers, [ID_ALIASES, DUR_ALIASES, PRED_ALIASES])
    has_three = [any(a in present for a in g) for g in (O_ALIASES, M_ALIASES, P_ALIASES)]
    if any(has_three) and not all(has_three):
        raise ValueError("three-point columns must come as a set: optimistic, most_likely and pessimistic "
                         f"(found headers: {[h for h in headers if h]})")

    tasks, index = [], {}
    for i, row in enumerate(rows, start=1):
        tid = _sanitize(_get(row, *ID_ALIASES, default=""))
        if not tid:
            raise ValueError(f"row {i}: missing id (column id is blank)")
        if tid in index:
            raise ValueError(f"row {i}: duplicate task id '{tid}' (first used in row {index[tid] + 1})")
        where = f"row {i} ({tid})"
        dur_raw = _get(row, *DUR_ALIASES)
        if _blank(dur_raw):
            raise ValueError(f"{where}, column duration: value is missing")
        duration = _snap(_num(dur_raw, f"{where}, column duration", minimum=0))
        raw_preds = _get(row, *PRED_ALIASES)
        if isinstance(raw_preds, (list, tuple)):
            spec = ("list", [_sanitize(p) for p in raw_preds if not _blank(p)])
        else:
            spec = ("text", "" if raw_preds is None else str(raw_preds).strip())
        tasks.append({
            "id": tid,
            "name": _sanitize(_get(row, *NAME_ALIASES, default="")),
            "duration": duration,
            "preds_spec": spec,
            "three_point": _three_point(row, where) if all(has_three) else None,
            "unit": _sanitize(_get(row, *UNIT_ALIASES, default="")),
        })
        index[tid] = len(tasks) - 1
    return tasks


def _pred_hint(p, tid, ids, whitespace_split):
    lower = {i.lower(): i for i in ids}
    if p.lower() in lower:
        return f" (did you mean '{lower[p.lower()]}'? ids are case-sensitive)"
    close = difflib.get_close_matches(p, [i for i in ids if i != tid], n=1, cutoff=0.6)
    if close:
        return f" (did you mean '{close[0]}'?)"
    if whitespace_split and any(" " in i for i in ids):
        return " (ids containing spaces must be separated with ',' or ';', not whitespace)"
    return ""


def resolve_predecessors(tasks):
    """Turn each task's raw predecessor spec into a de-duplicated list of known ids."""
    ids = [t["id"] for t in tasks]
    known = set(ids)
    for t in tasks:
        kind, val = t["preds_spec"]
        whitespace_split = False
        if kind == "list":
            parts = val
        elif not val:
            parts = []
        elif re.search(r"[;,]", val):
            parts = [p for p in re.split(r"[;,]", val) if p.strip()]
        elif _sanitize(val) in known:
            parts = [val]
        else:
            parts, whitespace_split = val.split(), True
        preds = []
        for p in parts:
            p = _sanitize(p)
            if p == t["id"]:
                raise ValueError(f"task '{p}' lists itself as a predecessor")
            if p not in known:
                raise ValueError(f"task '{t['id']}' lists unknown predecessor '{p}'"
                                 + _pred_hint(p, t["id"], ids, whitespace_split))
            if p not in preds:
                preds.append(p)
        t["preds"] = preds
        del t["preds_spec"]
    return tasks


# ----------------------------------------------------------------------------- network
def _find_cycle(stuck, succ):
    """Iterative three-colour DFS restricted to the stuck nodes; returns one loop as a list."""
    color = {t: 0 for t in stuck}
    parent = {}
    for root in stuck:
        if color[root]:
            continue
        color[root] = 1
        stack = [(root, iter([s for s in succ[root] if s in color]))]
        while stack:
            node, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                color[node] = 2
                stack.pop()
                continue
            if color[nxt] == 0:
                color[nxt] = 1
                parent[nxt] = node
                stack.append((nxt, iter([s for s in succ[nxt] if s in color])))
            elif color[nxt] == 1:
                loop, cur = [node], node
                while cur != nxt:
                    cur = parent[cur]
                    loop.append(cur)
                loop.reverse()
                loop.append(nxt)
                return loop
    return None


def topo_sort(tasks, succ):
    """Kahn's algorithm keeping input order; on a cycle, name the actual loop."""
    order = [t["id"] for t in tasks]
    indeg = {t["id"]: len(t["preds"]) for t in tasks}
    queue = deque(tid for tid in order if indeg[tid] == 0)
    ordered = []
    while queue:
        tid = queue.popleft()
        ordered.append(tid)
        for s in succ[tid]:
            indeg[s] -= 1
            if indeg[s] == 0:
                queue.append(s)
    if len(ordered) != len(tasks):
        done = set(ordered)
        stuck = [tid for tid in order if tid not in done]
        loop = _find_cycle(stuck, succ)
        if loop:
            raise ValueError(f"cycle detected: {' -> '.join(loop)}")
        raise ValueError(f"cycle detected in dependencies involving: {', '.join(stuck)}")
    return ordered


def build_network(tasks):
    """Return (topological order, successors map) for validated tasks."""
    resolve_predecessors(tasks)
    succ = {t["id"]: [] for t in tasks}
    for t in tasks:
        for p in t["preds"]:
            succ[p].append(t["id"])
    return topo_sort(tasks, succ), succ


def passes(order, preds, succ, dur):
    """Forward and backward CPM passes; returns (es, ef, ls, lf, project_end)."""
    es, ef = {}, {}
    for tid in order:
        e = 0.0
        for p in preds[tid]:
            if ef[p] > e:
                e = ef[p]
        es[tid] = e
        ef[tid] = e + dur[tid]
    end = max(ef.values())
    ls, lf = {}, {}
    for tid in reversed(order):
        late = end
        for s in succ[tid]:
            if ls[s] < late:
                late = ls[s]
        lf[tid] = late
        ls[tid] = late - dur[tid]
    return es, ef, ls, lf, end


def critical_paths(order, preds, succ, es, ef, critical):
    """Enumerate gap-free chains through critical tasks; returns (paths, total_count, shared)."""
    pos = {tid: i for i, tid in enumerate(order)}
    tight_succ = {tid: sorted((s for s in succ[tid] if s in critical and abs(es[s] - ef[tid]) < EPS),
                              key=pos.get) for tid in critical}
    tight_pred = {tid: [p for p in preds[tid] if p in critical and abs(es[tid] - ef[p]) < EPS] for tid in critical}
    sources = [tid for tid in order if tid in critical and not preds[tid]]
    sinks = [tid for tid in order if tid in critical and not succ[tid]]
    cnt_out, cnt_in = {}, {}
    for tid in reversed(order):
        if tid in critical:
            cnt_out[tid] = 1 if not succ[tid] else sum(cnt_out[s] for s in tight_succ[tid])
    for tid in order:
        if tid in critical:
            cnt_in[tid] = 1 if not preds[tid] else sum(cnt_in[p] for p in tight_pred[tid])
    total = sum(cnt_out[s] for s in sources)
    shared = [tid for tid in order if tid in critical and total and cnt_in[tid] * cnt_out[tid] == total]

    paths = []
    for src in sources:
        stack = [(src, [src])]
        while stack and len(paths) < MAX_PATHS:
            node, path = stack.pop()
            nexts = tight_succ[node]
            if not nexts:
                paths.append(path)
                continue
            for s in reversed(nexts):
                stack.append((s, path + [s]))
        if len(paths) >= MAX_PATHS:
            break
    return paths, total, shared, sinks


def analyze(tasks, topo, succ, near=None, target=None):
    """Deterministic CPM: per-task rows plus the summary block."""
    preds = {t["id"]: t["preds"] for t in tasks}
    dur = {t["id"]: t["duration"] for t in tasks}
    es, ef, ls, lf, end = passes(topo, preds, succ, dur)
    end = _snap(end)
    rows = []
    for t in tasks:
        tid = t["id"]
        tf = _snap(ls[tid] - es[tid])
        nxt = min((es[s] for s in succ[tid]), default=end)
        rows.append({
            "id": tid,
            "name": t["name"],
            "duration": t["duration"],
            "es": _snap(es[tid]), "ef": _snap(ef[tid]), "ls": _snap(ls[tid]), "lf": _snap(lf[tid]),
            "total_float": tf,
            "free_float": _snap(nxt - ef[tid]),
            "critical": tf == 0.0,
            "milestone": t["duration"] == 0.0,
        })
    critical = {r["id"] for r in rows if r["critical"]}
    paths, count, shared, _sinks = critical_paths(topo, preds, succ, es, ef, critical)
    summary = {
        "project_duration": end,
        "critical_tasks": [r["id"] for r in rows if r["critical"]],
        "critical_paths": paths,
        "critical_path_count": count,
        "shared_critical_tasks": shared,
        "milestones": [r["id"] for r in rows if r["milestone"]],
        "near_critical": None,
        "target": None,
        "calendar": None,
        "simulation": None,
    }
    if near is not None:
        hits = sorted((r for r in rows if not r["critical"] and r["total_float"] <= near + EPS),
                      key=lambda r: (r["total_float"], topo.index(r["id"])))
        summary["near_critical"] = {"threshold": near, "tasks": [{"id": r["id"], "total_float": r["total_float"]} for r in hits]}
    if target is not None:
        summary["target"] = {"value": target, "margin": _snap(target - end), "met": end <= target + EPS}
    return {"tasks": rows, "summary": summary}


# ----------------------------------------------------------------------------- calendar
def _unit_days(unit, workdays):
    u = unit.lower()
    if "day" in u:
        return 1
    if "week" in u or u in ("w", "wk", "wks"):
        return 5 if workdays else 7
    return None


def parse_holidays(path):
    out = set()
    with open(path, encoding="utf-8-sig") as fh:
        for n, line in enumerate(fh, 1):
            s = line.split("#", 1)[0].strip()
            if not s:
                continue
            token = s.split()[0].strip(",;")
            try:
                out.add(dt.date.fromisoformat(token))
            except ValueError:
                raise ValueError(f"{path}, line {n}: '{s}' is not a date (expected YYYY-MM-DD)")
    return out


class Calendar:
    """Maps day offsets from a start date to dates, optionally over working days only."""

    def __init__(self, start, days_per_unit, workdays=False, holidays=()):
        self.start, self.dpu, self.workdays = start, days_per_unit, workdays
        self.holidays = set(holidays)
        self._days = [start]
        if workdays and not self.is_workday(start):
            raise ValueError(f"--start-date {start.isoformat()} is a {start.strftime('%A')}"
                             + (" holiday" if start in self.holidays else "") + "; pick a working day")

    def is_workday(self, d):
        return d.weekday() < 5 and d not in self.holidays

    def date_at(self, index):
        if index > MAX_CAL_DAYS:
            raise ValueError(f"schedule spans more than {MAX_CAL_DAYS:,} days; cannot map it to dates")
        if not self.workdays:
            return self.start + dt.timedelta(days=index)
        while len(self._days) <= index:
            d = self._days[-1] + dt.timedelta(days=1)
            while not self.is_workday(d):
                d += dt.timedelta(days=1)
            self._days.append(d)
        return self._days[index]

    def span(self, es, ef):
        """(start date, finish date): first and last day of work; a milestone has start = finish."""
        s = int(math.floor(es * self.dpu + EPS))
        f = max(s, int(math.ceil(ef * self.dpu - EPS)) - 1)
        return self.date_at(s), self.date_at(f)

    def holidays_skipped(self, last_index):
        if not self.workdays or last_index < 0:
            return 0
        last = self.date_at(last_index)
        return sum(1 for h in self.holidays if self.start <= h <= last and h.weekday() < 5)


def apply_calendar(result, cal, unit):
    end = result["summary"]["project_duration"]
    for r in result["tasks"]:
        start, finish = cal.span(r["es"], r["ef"])
        late_start, late_finish = cal.span(r["ls"], r["lf"])
        r.update({"start": start.isoformat(), "finish": finish.isoformat(),
                  "late_start": late_start.isoformat(), "late_finish": late_finish.isoformat()})
    _p_start, p_finish = cal.span(0.0, end) if end > 0 else (cal.start, cal.start)
    last_index = max(0, int(math.ceil(end * cal.dpu - EPS)) - 1)
    result["summary"]["calendar"] = {
        "start_date": cal.start.isoformat(),
        "finish_date": p_finish.isoformat(),
        "unit": unit,
        "days_per_unit": cal.dpu,
        "workdays_only": cal.workdays,
        "holidays_skipped": cal.holidays_skipped(last_index),
    }


# ----------------------------------------------------------------------------- simulation
def _draw(rng, dist, o, m, p):
    span = p - o
    if span <= 0:
        return o
    if dist == "triangular":
        return rng.triangular(o, p, m)
    alpha = 1.0 + 4.0 * (m - o) / span
    beta = 1.0 + 4.0 * (p - m) / span
    return o + rng.betavariate(alpha, beta) * span


def simulate(tasks, topo, succ, trials, seed, dist, det_end, target=None):
    preds = {t["id"]: t["preds"] for t in tasks}
    base = {t["id"]: t["duration"] for t in tasks}
    samplers = [(t["id"],) + t["three_point"] for t in tasks if t["three_point"]]
    if not samplers:
        raise ValueError("--simulate needs optimistic/most_likely/pessimistic values on at least one task")
    rng = random.Random(seed)
    ends = []
    crit = {tid: 0 for tid in base}
    for _ in range(trials):
        dur = dict(base)
        for tid, o, m, p in samplers:
            dur[tid] = _draw(rng, dist, o, m, p)
        es, _ef, ls, _lf, end = passes(topo, preds, succ, dur)
        ends.append(end)
        for tid in base:
            if abs(ls[tid] - es[tid]) < EPS:
                crit[tid] += 1
    ends.sort()
    n = float(trials)
    return {
        "trials": trials,
        "seed": seed,
        "distribution": dist,
        "sampled_tasks": len(samplers),
        "mean": statistics.fmean(ends),
        "std": statistics.pstdev(ends) if trials > 1 else 0.0,
        "min": ends[0],
        "max": ends[-1],
        "quantiles": {f"P{int(p * 100)}": _quantile(ends, p) for p in SIM_LEVELS},
        "p_within_deterministic": sum(1 for e in ends if e <= det_end + EPS) / n,
        "p_within_target": (sum(1 for e in ends if e <= target + EPS) / n) if target is not None else None,
        "criticality": {tid: crit[tid] / n * 100.0 for tid in base},
    }


# ----------------------------------------------------------------------------- renderers
def _table(result, unit):
    s = result["summary"]
    cal, sim = s["calendar"], s["simulation"]
    headers = ["ID", "Name", "Dur"]
    headers += ["Start", "Finish", "Late start", "Late finish"] if cal else ["ES", "EF", "LS", "LF"]
    headers += ["TF", "FF", "Critical"]
    if sim:
        headers.append("CI%")
    rows = []
    for r in result["tasks"]:
        cells = [_sanitize(r["id"], NAME_WIDTH), _sanitize(r["name"], NAME_WIDTH), _fmt(r["duration"])]
        if cal:
            cells += [r["start"], r["finish"], r["late_start"], r["late_finish"]]
        else:
            cells += [_fmt(r["es"]), _fmt(r["ef"]), _fmt(r["ls"]), _fmt(r["lf"])]
        cells += [_fmt(r["total_float"]), _fmt(r["free_float"]), "yes" if r["critical"] else ""]
        if sim:
            cells.append(_pct(sim["criticality"][r["id"]]))
        rows.append(cells)
    left = {0, 1, 9}
    return headers, rows, left


def _summary_lines(result, unit):
    s = result["summary"]
    u = f" {unit}"
    out = []
    paths = s["critical_paths"]
    if s["critical_path_count"] == 1 and paths:
        out.append(f"Critical path: {' -> '.join(paths[0])}")
    elif paths:
        out.append(f"Critical paths ({s['critical_path_count']}):")
        out += [f"  {' -> '.join(p)}" for p in paths]
        if s["critical_path_count"] > len(paths):
            out.append(f"  ... and {s['critical_path_count'] - len(paths)} more "
                       f"(critical tasks: {', '.join(s['critical_tasks'])})")
        out.append("Note: the project only shortens when EVERY critical path shortens"
                   + (f"; tasks on all of them: {', '.join(s['shared_critical_tasks'])}"
                      if s["shared_critical_tasks"] else "; no single task is on all of them") + ".")
    else:
        out.append("Critical path: (none)")
    out.append(f"Project duration: {_fmt(s['project_duration'])}{u}")
    if s["milestones"]:
        out.append("Milestones (duration 0): " + ", ".join(s["milestones"]))
    nc = s["near_critical"]
    if nc is not None:
        listed = ", ".join(f"{t['id']} (TF {_fmt(t['total_float'])})" for t in nc["tasks"]) or "none"
        out.append(f"Near-critical (0 < TF <= {_fmt(nc['threshold'])}{u}): {listed}")
    tg = s["target"]
    if tg is not None:
        if tg["met"]:
            out.append(f"Target {_fmt(tg['value'])}{u}: met with {_fmt(tg['margin'])}{u} to spare")
        else:
            out.append(f"Target {_fmt(tg['value'])}{u}: MISSED by {_fmt(-tg['margin'])}{u} "
                       f"- compress a task on every critical path or move the target")
    cal = s["calendar"]
    if cal is not None:
        start = dt.date.fromisoformat(cal["start_date"])
        finish = dt.date.fromisoformat(cal["finish_date"])
        mode = (f"working days Mon-Fri, {cal['holidays_skipped']} holiday(s) skipped" if cal["workdays_only"]
                else "calendar days, no weekends or holidays skipped")
        one = cal["unit"][:-1] if cal["unit"].lower().endswith("s") else cal["unit"]
        out.append(f"Calendar: start {start.isoformat()} ({start.strftime('%a')}), 1 {one} = "
                   f"{cal['days_per_unit']} {'working' if cal['workdays_only'] else 'calendar'} day(s), "
                   f"{mode}; project finish {finish.isoformat()} ({finish.strftime('%a')})")
    sim = s["simulation"]
    if sim is not None:
        q = sim["quantiles"]
        out.append(f"Simulation ({sim['trials']:,} trials, seed {sim['seed']}, {sim['distribution']} on "
                   f"{sim['sampled_tasks']} task(s) with O/M/P):")
        out.append(f"  project duration mean {_fmt(sim['mean'])}, std {_fmt(sim['std'])}, "
                   f"min {_fmt(sim['min'])}, max {_fmt(sim['max'])}{u}")
        out.append("  " + "   ".join(f"{k} = {_fmt(v)}" for k, v in q.items()) + u)
        out.append(f"  P(duration <= deterministic {_fmt(s['project_duration'])}{u}) = "
                   f"{_pct(sim['p_within_deterministic'] * 100)}")
        if sim["p_within_target"] is not None:
            out.append(f"  P(duration <= target {_fmt(s['target']['value'])}{u}) = {_pct(sim['p_within_target'] * 100)}")
        out.append("  CI% = criticality index: share of trials in which the task had zero total float")
    out.append("TF = total float (shared along the chain); FF = free float (usable without delaying any successor).")
    return out


def render_gantt(result, unit, width):
    rows = result["tasks"]
    end = result["summary"]["project_duration"]
    if end <= 0:
        return ["Gantt: every task has zero duration; nothing to draw"]
    labels = [f"{_sanitize(r['id'], 12)} {_sanitize(r['name'], 24)}".rstrip() for r in rows]
    label_w = max(len(x) for x in labels)
    area = max(30, min(80, width - label_w - 4))
    scale = area / end
    step = next((c for c in (0.5, 1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 5000, 10000)
                 if c * scale >= 6), max(1.0, end))
    ruler = [" "] * (area + 1)
    k = 0.0
    while k <= end + EPS:
        label = _fmt(k)
        pos = min(int(round(k * scale)), area + 1 - len(label))
        if all(ruler[pos + j] == " " for j in range(len(label))):
            for j, ch in enumerate(label):
                ruler[pos + j] = ch
        k += step
    out = [f"Gantt (1 column = {_fmt(end / area)} {unit}; # critical, = non-critical, . float to LF, "
           f"{MILESTONE} milestone)",
           f"{'':<{label_w}}  {''.join(ruler).rstrip()}",
           f"{'':<{label_w}}  {'-' * (area + 1)}"]
    for label, r in zip(labels, rows):
        bar = [" "] * (area + 1)
        if r["milestone"]:
            bar[min(area, int(round(r["es"] * scale)))] = MILESTONE
        else:
            s = int(math.floor(r["es"] * scale + EPS))
            e = max(s + 1, int(math.ceil(r["ef"] * scale - EPS)))
            f = int(math.ceil(r["lf"] * scale - EPS))
            fill = "#" if r["critical"] else "="
            for j in range(s, min(e, area + 1)):
                bar[j] = fill
            for j in range(e, min(f, area + 1)):
                bar[j] = "."
        out.append(f"{label:<{label_w}}  {''.join(bar).rstrip()}")
    return out


def render_table(result, unit, gantt_width=None):
    headers, rows, left = _table(result, unit)
    widths = [max(len(h), *(len(r[c]) for r in rows)) for c, h in enumerate(headers)]

    def line(cells):
        return "  ".join(c.ljust(widths[i]) if i in left else c.rjust(widths[i]) for i, c in enumerate(cells)).rstrip()

    out = [f"Schedule (CPM, finish-to-start; durations in {unit})", line(headers), line(["-" * w for w in widths])]
    out += [line(r) for r in rows]
    out.append("")
    out += _summary_lines(result, unit)
    if gantt_width:
        out.append("")
        out += render_gantt(result, unit, gantt_width)
    return "\n".join(out)


def render_md(result, unit, gantt_width=None):
    headers, rows, left = _table(result, unit)
    out = [f"## Schedule (CPM, finish-to-start; durations in {unit})", ""]
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(":---" if i in left else "---:" for i in range(len(headers))) + "|")
    for r in rows:
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
    out += ["", "```"] + _summary_lines(result, unit) + ["```"]
    if gantt_width:
        out += ["", "```"] + render_gantt(result, unit, gantt_width) + ["```"]
    return "\n".join(out)


def render_csv(result, unit, gantt_width=None):
    cols = ["id", "name", "unit", "duration", "es", "ef", "ls", "lf", "total_float", "free_float", "critical",
            "milestone", "start", "finish", "late_start", "late_finish", "criticality_pct"]
    sim = result["summary"]["simulation"]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=cols, lineterminator="\n")
    writer.writeheader()
    for r in result["tasks"]:
        row = {c: r.get(c, "") for c in cols}
        row["unit"] = unit
        for c in ("duration", "es", "ef", "ls", "lf", "total_float", "free_float"):
            row[c] = _plain(r[c])
        row["critical"] = "yes" if r["critical"] else "no"
        row["milestone"] = "yes" if r["milestone"] else "no"
        row["criticality_pct"] = _plain(round(sim["criticality"][r["id"]], 2)) if sim else ""
        writer.writerow(row)
    return buf.getvalue().rstrip("\n")


def _rounded(obj):
    if isinstance(obj, float):
        return round(obj, 4)
    if isinstance(obj, dict):
        return {k: _rounded(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_rounded(v) for v in obj]
    return obj


def render_json(result, unit, gantt_width=None):
    payload = {"unit": unit, "tasks": result["tasks"], "summary": result["summary"]}
    return json.dumps(_rounded(payload), indent=2, ensure_ascii=False)


RENDERERS = {"table": render_table, "json": render_json, "csv": render_csv, "md": render_md}


# ----------------------------------------------------------------------------- CLI
def _finite(parser, value, flag, minimum=None, strict=False):
    if not math.isfinite(value):
        parser.error(f"{flag} must be a finite number (got {value})")
    if minimum is not None and (value < minimum or (strict and value <= minimum)):
        parser.error(f"{flag} must be {'greater than' if strict else 'at least'} {minimum:g} (got {value:g})")
    return value


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="critical_path.py",
        description="Critical path method (CPM) for a finish-to-start task network: ES/EF/LS/LF, total and "
                    "free float, every critical path, near-critical tasks, calendar dates, a text Gantt "
                    "and a Monte Carlo schedule-risk simulation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("path", help="CSV or JSON task list, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="parse the input as JSON (default: CSV)")
    parser.add_argument("--unit", metavar="LABEL",
                        help=f"duration unit label, e.g. weeks or days (default: a 'unit' column, else '{DEFAULT_UNIT}'); "
                             "days or weeks are required for --start-date")
    parser.add_argument("--near-critical", metavar="N", type=float,
                        help="also list non-critical tasks whose total float is <= N units")
    parser.add_argument("--target", metavar="T", type=float,
                        help="imposed finish in units: report the margin or shortfall (and, with --simulate, "
                             "the probability of meeting it)")
    parser.add_argument("--start-date", metavar="YYYY-MM-DD",
                        help="map ES/EF/LS/LF to dates from this start date (needs --unit days or weeks)")
    parser.add_argument("--workdays", action="store_true",
                        help="with --start-date: count Mon-Fri only (1 week = 5 working days) and skip --holidays")
    parser.add_argument("--holidays", metavar="FILE",
                        help="with --workdays: file of non-working dates, one YYYY-MM-DD per line ('#' comments ok)")
    parser.add_argument("--gantt", action="store_true",
                        help="print a text Gantt chart after the table (table and md formats)")
    parser.add_argument("--simulate", metavar="N", type=int, default=0,
                        help=f"run N Monte Carlo trials (1..{MAX_TRIALS:,}) on the optimistic/most_likely/pessimistic "
                             "columns: P10/P50/P80/P90 project duration and a criticality index per task")
    parser.add_argument("--seed", metavar="K", type=int,
                        help="random seed for --simulate (default: random, printed so the run can be repeated)")
    parser.add_argument("--dist", choices=("pert", "triangular"),
                        help="distribution for --simulate: pert (PERT-Beta, default) or triangular")
    parser.add_argument("--format", choices=("table", "json", "csv", "md"), default="table",
                        help="output format: table (default), json (tasks + summary), csv (one row per task, "
                             "for hand-off to project-planning / status-report), md (markdown table + summary)")
    args = parser.parse_args(argv)

    if args.unit is not None and not args.unit.strip():
        parser.error("--unit must not be blank")
    if args.near_critical is not None:
        _finite(parser, args.near_critical, "--near-critical", minimum=0)
    if args.target is not None:
        _finite(parser, args.target, "--target", minimum=0, strict=True)
    if args.simulate < 0 or args.simulate > MAX_TRIALS:
        parser.error(f"--simulate must be between 1 and {MAX_TRIALS:,} (got {args.simulate})")
    if args.seed is not None and args.simulate == 0:
        parser.error("--seed only makes sense with --simulate N")
    if args.dist is not None and args.simulate == 0:
        parser.error("--dist only makes sense with --simulate N")
    start_date = None
    if args.start_date is not None:
        try:
            start_date = dt.date.fromisoformat(args.start_date.strip())
        except ValueError:
            parser.error(f"--start-date {args.start_date!r} is not a date (expected YYYY-MM-DD)")
    if args.workdays and start_date is None:
        parser.error("--workdays needs --start-date")
    if args.holidays is not None and not args.workdays:
        parser.error("--holidays needs --workdays (and --start-date)")

    try:
        try:
            sys.stdout.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
        text = read_text(args.path)
        rows, headers = load_rows(text, args.json, JSON_KEY)
        tasks = parse_tasks(rows, headers)
        units = sorted({t["unit"] for t in tasks if t["unit"]})
        if len(units) > 1:
            raise ValueError(f"mixed units {units}: one duration unit per file (or override with --unit)")
        unit = args.unit.strip() if args.unit else (units[0] if units else DEFAULT_UNIT)
        topo, succ = build_network(tasks)
        result = analyze(tasks, topo, succ, near=args.near_critical, target=args.target)
        if start_date is not None:
            dpu = _unit_days(unit, args.workdays)
            if dpu is None:
                raise ValueError(f"--start-date needs durations in days or weeks: pass --unit days or --unit weeks "
                                 f"(current unit: '{unit}')")
            holidays = parse_holidays(args.holidays) if args.holidays else ()
            apply_calendar(result, Calendar(start_date, dpu, args.workdays, holidays), unit)
        if args.simulate:
            seed = args.seed if args.seed is not None else random.SystemRandom().randrange(1_000_000_000)
            result["summary"]["simulation"] = simulate(tasks, topo, succ, args.simulate, seed, args.dist or "pert",
                                                       result["summary"]["project_duration"], args.target)
        gantt_width = shutil.get_terminal_size((100, 24)).columns if args.gantt else None
        print(RENDERERS[args.format](result, unit, gantt_width))
    except UnicodeDecodeError as exc:
        print(f"error: {args.path} is not UTF-8 text (bad byte at offset {exc.start}); "
              f"re-save it as 'CSV UTF-8'", file=sys.stderr)
        return 2
    except (OSError, ValueError, TypeError, OverflowError, ZeroDivisionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
