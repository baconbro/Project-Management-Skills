#!/usr/bin/env python3
"""Check resource capacity: utilization, and over/under-allocation flags.

Reads a resource allocation file from CSV or JSON and prints a table sorted by
utilization (highest first), plus team totals and counts of over- and
under-allocated people. Standard library only.

Input columns / keys (case-insensitive, extra columns ignored):
    person      name of the person                        (optional)
    role        their role                                (optional)
    capacity    how much they can do in the period        (required, > 0)
    allocated   how much work is assigned in the period   (required, >= 0)

capacity and allocated must be in the SAME unit (e.g. hours-per-week, or percent).

Computed:
    utilization = allocated / capacity * 100   (a percentage)
    flag        = OVER  if utilization > --threshold (default 100)
                  UNDER if utilization < --under     (default 50)
                  OK    otherwise

Usage:
    python capacity_check.py resource-allocation.csv
    python capacity_check.py resources.json --json
    python capacity_check.py resource-allocation.csv --threshold 90 --under 40
    cat resource-allocation.csv | python capacity_check.py -      # read from stdin
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


def load_rows(text: str, as_json: bool) -> list:
    if as_json:
        data = json.loads(text)
        if isinstance(data, dict):
            data = data.get("resources", data.get("people", []))
        if not isinstance(data, list):
            raise ValueError("JSON must be a list of resources or {'resources': [...]}")
        return [dict(r) for r in data]
    reader = csv.DictReader(io.StringIO(text))
    return [dict(r) for r in reader]


def flag(util: float, threshold: float, under: float) -> str:
    if util > threshold:
        return "OVER"
    if util < under:
        return "UNDER"
    return "OK"


def analyze(rows: list, threshold: float, under: float) -> list:
    out = []
    for i, row in enumerate(rows, start=1):
        person = _get(row, "person", "name", "resource", default=f"Person {i}")
        role = _get(row, "role", default="")
        cap_raw = _get(row, "capacity", "cap")
        alloc_raw = _get(row, "allocated", "allocation", "alloc")
        if cap_raw is None or alloc_raw is None:
            raise ValueError(f"row {i}: missing capacity or allocated")
        capacity = float(cap_raw)
        allocated = float(alloc_raw)
        if capacity <= 0:
            raise ValueError(f"row {i}: capacity must be > 0 (got {capacity})")
        if allocated < 0:
            raise ValueError(f"row {i}: allocated must be >= 0 (got {allocated})")
        util = allocated / capacity * 100.0
        out.append(
            {
                "person": str(person),
                "role": str(role),
                "capacity": capacity,
                "allocated": allocated,
                "utilization": util,
                "flag": flag(util, threshold, under),
            }
        )
    out.sort(key=lambda r: r["utilization"], reverse=True)
    return out


def render(people: list) -> str:
    if not people:
        return "No resources found in input."
    headers = ["Person", "Role", "Capacity", "Allocated", "Util%", "Flag"]
    rows = [
        [
            p["person"],
            (p["role"][:20] if len(p["role"]) <= 20 else p["role"][:17] + "..."),
            f"{p['capacity']:,.0f}",
            f"{p['allocated']:,.0f}",
            f"{p['utilization']:.0f}%",
            p["flag"],
        ]
        for p in people
    ]
    widths = [max(len(h), *(len(row[c]) for row in rows)) for c, h in enumerate(headers)]

    def line(cells):
        return "  ".join(c.ljust(widths[i]) for i, c in enumerate(cells))

    out = [line(headers), line(["-" * w for w in widths])]
    out += [line(r) for r in rows]

    over = sum(1 for p in people if p["flag"] == "OVER")
    under = sum(1 for p in people if p["flag"] == "UNDER")
    total_cap = sum(p["capacity"] for p in people)
    total_alloc = sum(p["allocated"] for p in people)
    team_util = (total_alloc / total_cap * 100.0) if total_cap else 0.0
    out.append("")
    out.append(f"Over-allocated:  {over}")
    out.append(f"Under-allocated: {under}")
    out.append(
        f"Total capacity: {total_cap:,.0f}   Total allocated: {total_alloc:,.0f}"
        f"   Team utilization: {team_util:.0f}%"
    )
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Check resource capacity: utilization and over/under-allocation flags.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Flags: util > --threshold => OVER; util < --under => UNDER; else OK.",
    )
    parser.add_argument("path", help="path to CSV/JSON allocation file, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="parse input as JSON (default: CSV)")
    parser.add_argument(
        "--threshold", type=float, default=100.0,
        help="OVER if utilization exceeds this percent (default 100)",
    )
    parser.add_argument(
        "--under", type=float, default=50.0,
        help="UNDER if utilization is below this percent (default 50)",
    )
    args = parser.parse_args(argv)

    if args.under > args.threshold:
        parser.error("--under must be <= --threshold")

    try:
        text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
        people = analyze(load_rows(text, args.json), args.threshold, args.under)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(render(people))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
