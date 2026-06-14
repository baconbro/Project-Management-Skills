#!/usr/bin/env python3
"""Compute the critical path of a finish-to-start task network (CPM).

Reads tasks with durations and predecessors from CSV or JSON, runs the forward
and backward passes of the critical path method, and prints a per-task table
(ES/EF/LS/LF/slack and a Critical? flag), the critical path, and the total
project duration. Stdlib only.

Input columns / keys (case-insensitive, extra columns ignored):
    id            task identifier                                  (required)
    name          task name                                        (optional)
    duration      task duration, a non-negative number             (required)
    predecessors  ids this task depends on (finish-to-start),
                  separated by space / comma / semicolon, may be empty

Method (finish-to-start dependencies):
    forward pass : ES = max(EF of predecessors), 0 if none; EF = ES + duration
    project end  : max EF over all tasks
    backward pass: LF = min(LS of successors), project end if none; LS = LF - duration
    slack        : LS - ES; a task is critical when slack == 0

Errors:
    a predecessor id that is not a known task   -> ERROR
    a cycle in the dependencies                 -> ERROR

Usage:
    python critical_path.py schedule.csv
    python critical_path.py schedule.json --json
    cat schedule.csv | python critical_path.py -        # read from stdin
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys

EPS = 1e-9


def _get(row: dict, *names: str, default=None):
    """Case-insensitive lookup across possible column names."""
    lowered = {k.lower().strip(): v for k, v in row.items() if k is not None}
    for n in names:
        if n in lowered and lowered[n] not in (None, ""):
            return lowered[n]
    return default


def load_rows(text: str, as_json: bool) -> list:
    if as_json:
        data = json.loads(text)
        if isinstance(data, dict):
            data = data.get("tasks", [])
        if not isinstance(data, list):
            raise ValueError("JSON must be a list of tasks or {'tasks': [...]}")
        return [dict(r) for r in data]
    reader = csv.DictReader(io.StringIO(text))
    return [dict(r) for r in reader]


def _split_preds(raw) -> list:
    if raw is None:
        return []
    text = str(raw)
    for sep in (",", ";"):
        text = text.replace(sep, " ")
    return [p.strip() for p in text.split() if p.strip()]


def parse(rows: list) -> dict:
    tasks = {}
    order = []
    for i, row in enumerate(rows, start=1):
        tid = _get(row, "id", "task", "task_id")
        if tid is None:
            raise ValueError(f"row {i}: missing id")
        tid = str(tid).strip()
        if tid in tasks:
            raise ValueError(f"duplicate task id '{tid}'")
        dur_raw = _get(row, "duration", "dur", "days", "effort")
        if dur_raw is None:
            raise ValueError(f"row {i} (id {tid}): missing duration")
        try:
            dur = float(dur_raw)
        except (TypeError, ValueError):
            raise ValueError(f"row {i} (id {tid}): duration '{dur_raw}' is not a number")
        if dur < 0:
            raise ValueError(f"row {i} (id {tid}): duration must be >= 0")
        name = str(_get(row, "name", "title", default=""))
        preds = _split_preds(_get(row, "predecessors", "preds", "depends_on", "deps"))
        tasks[tid] = {"id": tid, "name": name, "duration": dur, "preds": preds}
        order.append(tid)
    if not tasks:
        raise ValueError("no tasks found in input")

    for t in tasks.values():
        for p in t["preds"]:
            if p not in tasks:
                raise ValueError(f"task '{t['id']}' lists unknown predecessor '{p}'")
    return {"tasks": tasks, "order": order}


def topo_sort(tasks: dict, succ: dict) -> list:
    """Kahn's algorithm; raises on a cycle."""
    indeg = {tid: len(t["preds"]) for tid, t in tasks.items()}
    queue = [tid for tid, d in indeg.items() if d == 0]
    ordered = []
    while queue:
        tid = queue.pop(0)
        ordered.append(tid)
        for s in succ[tid]:
            indeg[s] -= 1
            if indeg[s] == 0:
                queue.append(s)
    if len(ordered) != len(tasks):
        stuck = sorted(t for t in tasks if t not in ordered)
        raise ValueError(f"cycle detected in dependencies involving: {', '.join(stuck)}")
    return ordered


def cpm(parsed: dict) -> dict:
    tasks = parsed["tasks"]
    succ = {tid: [] for tid in tasks}
    for t in tasks.values():
        for p in t["preds"]:
            succ[p].append(t["id"])

    topo = topo_sort(tasks, succ)
    es, ef, ls, lf = {}, {}, {}, {}

    # forward pass
    for tid in topo:
        es[tid] = max((ef[p] for p in tasks[tid]["preds"]), default=0.0)
        ef[tid] = es[tid] + tasks[tid]["duration"]

    project_end = max(ef.values())

    # backward pass
    for tid in reversed(topo):
        lf[tid] = min((ls[s] for s in succ[tid]), default=project_end)
        ls[tid] = lf[tid] - tasks[tid]["duration"]

    slack = {tid: ls[tid] - es[tid] for tid in tasks}
    critical = {tid for tid in tasks if abs(slack[tid]) < EPS}

    rows = []
    for tid in parsed["order"]:
        rows.append(
            {
                "id": tid,
                "name": tasks[tid]["name"],
                "duration": tasks[tid]["duration"],
                "es": es[tid],
                "ef": ef[tid],
                "ls": ls[tid],
                "lf": lf[tid],
                "slack": slack[tid],
                "critical": tid in critical,
            }
        )

    cpath = trace_critical_path(tasks, succ, es, ef, critical)
    return {"rows": rows, "project_end": project_end, "critical_path": cpath}


def trace_critical_path(tasks, succ, es, ef, critical) -> list:
    """Trace one critical path: a critical start (ES==0) to a critical end task.

    At each step move to a critical successor whose ES equals this task's EF, so
    the path is a continuous finish-to-start chain with no float.
    """
    starts = sorted(tid for tid in critical if abs(es[tid]) < EPS)
    if not starts:
        return []
    path = []
    current = starts[0]
    while True:
        path.append(current)
        nexts = sorted(
            s for s in succ[current]
            if s in critical and abs(es[s] - ef[current]) < EPS
        )
        if not nexts:
            break
        current = nexts[0]
    return path


def _fmt(x: float) -> str:
    return f"{x:g}"


def render(result: dict) -> str:
    rows = result["rows"]
    headers = ["ID", "Name", "Dur", "ES", "EF", "LS", "LF", "Slack", "Critical?"]
    table = [
        [
            r["id"],
            (r["name"][:24]) if len(r["name"]) > 24 else r["name"],
            _fmt(r["duration"]),
            _fmt(r["es"]),
            _fmt(r["ef"]),
            _fmt(r["ls"]),
            _fmt(r["lf"]),
            _fmt(r["slack"]),
            "yes" if r["critical"] else "",
        ]
        for r in rows
    ]
    widths = [max(len(h), *(len(row[c]) for row in table)) for c, h in enumerate(headers)]

    def line(cells):
        out = []
        for i, c in enumerate(cells):
            out.append(c.ljust(widths[i]) if i in (0, 1, 8) else c.rjust(widths[i]))
        return "  ".join(out)

    out = [line(headers), line(["-" * w for w in widths])]
    out += [line(r) for r in table]
    out.append("")
    cp = result["critical_path"]
    out.append(f"Critical path: {' -> '.join(cp) if cp else '(none)'}")
    out.append(f"Project duration: {_fmt(result['project_end'])}")
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Compute the critical path (CPM) of a finish-to-start task network.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Dependencies are finish-to-start; predecessors may be space/comma/semicolon separated.",
    )
    parser.add_argument("path", help="path to CSV/JSON tasks, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="parse input as JSON (default: CSV)")
    args = parser.parse_args(argv)

    try:
        text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
        result = cpm(parse(load_rows(text, args.json)))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
