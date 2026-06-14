#!/usr/bin/env python3
"""Score change requests by weighted impact and assign a priority band.

Reads change requests from CSV or JSON and prints a table sorted by score
(highest first), plus a count by priority. Standard library only.

Input columns / keys (case-insensitive, extra columns ignored):
    id              short change identifier                  (optional)
    description     what the change is                       (optional)
    scope_impact    impact on scope,    integer 1..5
    cost_impact     impact on cost,     integer 1..5
    schedule_impact impact on schedule, integer 1..5

Computed:
    score    = (w_scope*scope + w_cost*cost + w_schedule*schedule)
               / (w_scope + w_cost + w_schedule)
    priority = HIGH (score >= --high), MEDIUM (score >= --medium), else LOW

Usage:
    python change_impact.py changes.csv
    python change_impact.py changes.json --json
    python change_impact.py changes.csv --w-cost 2 --w-schedule 1.5
    python change_impact.py changes.csv --high 4 --medium 2.5
    cat changes.csv | python change_impact.py -        # read from stdin
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys


def _get(row: dict, *names: str, default=None):
    """Case-insensitive lookup across possible column names."""
    lowered = {k.lower().strip(): v for k, v in row.items() if k is not None}
    for n in names:
        if n in lowered and lowered[n] not in (None, ""):
            return lowered[n]
    return default


def _impact(value, field: str, row_num: int) -> int:
    """Parse an impact cell as an integer in 1..5."""
    try:
        n = int(float(value))
    except (TypeError, ValueError):
        raise ValueError(f"row {row_num}: {field} is not a number: {value!r}")
    if n < 1 or n > 5:
        raise ValueError(f"row {row_num}: {field} must be 1..5, got {n}")
    return n


def load_rows(text: str, as_json: bool) -> list:
    if as_json:
        data = json.loads(text)
        if isinstance(data, dict):
            data = data.get("changes", [])
        if not isinstance(data, list):
            raise ValueError("JSON must be a list of changes or {'changes': [...]}")
        return [dict(r) for r in data]
    reader = csv.DictReader(io.StringIO(text))
    return [dict(r) for r in reader]


def priority(score: float, high: float, medium: float) -> str:
    if score >= high:
        return "HIGH"
    if score >= medium:
        return "MEDIUM"
    return "LOW"


def score_rows(rows: list, weights: dict, high: float, medium: float) -> list:
    w_total = weights["scope"] + weights["cost"] + weights["schedule"]
    if w_total <= 0:
        raise ValueError("weights must sum to a positive value")
    scored = []
    for i, row in enumerate(rows, start=1):
        cid = _get(row, "id", default=f"CR{i:03d}")
        desc = _get(row, "description", "desc", "change", default="")
        scope = _impact(_get(row, "scope_impact", "scope"), "scope_impact", i)
        cost = _impact(_get(row, "cost_impact", "cost"), "cost_impact", i)
        sched = _impact(_get(row, "schedule_impact", "schedule"), "schedule_impact", i)
        value = (
            weights["scope"] * scope
            + weights["cost"] * cost
            + weights["schedule"] * sched
        ) / w_total
        scored.append(
            {
                "id": str(cid),
                "description": str(desc),
                "scope": scope,
                "cost": cost,
                "schedule": sched,
                "score": value,
                "priority": priority(value, high, medium),
            }
        )
    scored.sort(key=lambda r: r["score"], reverse=True)
    return scored


def render(scored: list) -> str:
    if not scored:
        return "No change requests found in input."
    headers = ["ID", "Priority", "Scope", "Cost", "Sched", "Score", "Description"]
    rows = [
        [
            r["id"],
            r["priority"],
            str(r["scope"]),
            str(r["cost"]),
            str(r["schedule"]),
            f"{r['score']:.2f}",
            (r["description"][:40] + "...") if len(r["description"]) > 43 else r["description"],
        ]
        for r in scored
    ]
    widths = [max(len(h), *(len(row[c]) for row in rows)) for c, h in enumerate(headers)]

    def line(cells):
        return "  ".join(c.ljust(widths[i]) for i, c in enumerate(cells))

    out = [line(headers), line(["-" * w for w in widths])]
    out += [line(r) for r in rows]
    counts = {b: sum(1 for r in scored if r["priority"] == b) for b in ("HIGH", "MEDIUM", "LOW")}
    out.append("")
    out.append(f"Priority counts: HIGH={counts['HIGH']}  MEDIUM={counts['MEDIUM']}  LOW={counts['LOW']}")
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Score change requests by weighted scope/cost/schedule impact and priority.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Priority: score >= --high => HIGH; >= --medium => MEDIUM; else LOW.",
    )
    parser.add_argument("path", help="path to CSV/JSON change log, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="parse input as JSON (default: CSV)")
    parser.add_argument("--w-scope", type=float, default=1.0, help="weight for scope impact (default 1.0)")
    parser.add_argument("--w-cost", type=float, default=1.0, help="weight for cost impact (default 1.0)")
    parser.add_argument("--w-schedule", type=float, default=1.0, help="weight for schedule impact (default 1.0)")
    parser.add_argument("--high", type=float, default=4.0, help="HIGH priority threshold (default 4.0)")
    parser.add_argument("--medium", type=float, default=2.5, help="MEDIUM priority threshold (default 2.5)")
    args = parser.parse_args(argv)

    if args.medium > args.high:
        parser.error("--medium must be <= --high")

    weights = {"scope": args.w_scope, "cost": args.w_cost, "schedule": args.w_schedule}
    try:
        text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
        scored = score_rows(load_rows(text, args.json), weights, args.high, args.medium)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(render(scored))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
