#!/usr/bin/env python3
"""Validate a RACI responsibility assignment matrix.

Reads a matrix from CSV or JSON, prints it back, then checks each activity for
exactly one Accountable and at least one Responsible, warns on over-Consulted
activities and overloaded roles, and reports an overall PASS/FAIL. Standard
library only.

Input shape:
    The FIRST column is the activity/task name. EVERY remaining column is a role.
    Cells contain R, A, C, I, a blank, or a combo like "A/R", "AR", or "A R"
    (any of R/A/C/I in one cell). Cell text is case-insensitive.

CSV:  first header cell is the activity column label; the rest are role names.
JSON: a list of objects, or {"activities": [...]}, each object mapping the
      activity-name field plus one key per role to its cell value. The first key
      of the first object is treated as the activity-name column.

Rules:
    ERROR  no accountability     : an activity with zero A
    ERROR  multiple accountable  : an activity with more than one A
    ERROR  no responsible        : an activity with zero R
    WARN   too many cooks        : an activity with more than --max-ci roles as C or I
    WARN   overloaded            : a role Accountable on more than --max-a-share of activities

Usage:
    python raci_validate.py matrix.csv
    python raci_validate.py matrix.json --json
    python raci_validate.py matrix.csv --max-ci 4 --max-a-share 0.5
    cat matrix.csv | python raci_validate.py -        # read from stdin
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys

VALID = {"R", "A", "C", "I"}


def parse_cell(value) -> set:
    """Return the set of R/A/C/I letters in a cell, case-insensitively."""
    if value is None:
        return set()
    letters = {ch.upper() for ch in str(value) if ch.upper() in VALID}
    return letters


def load_matrix(text: str, as_json: bool):
    """Return (activity_label, role_names, rows) where each row is
    {"activity": str, "cells": {role: set_of_letters}}."""
    if as_json:
        data = json.loads(text)
        if isinstance(data, dict):
            data = data.get("activities", [])
        if not isinstance(data, list) or not data:
            raise ValueError("JSON must be a non-empty list of activity objects")
        first = dict(data[0])
        keys = list(first.keys())
        if not keys:
            raise ValueError("activity objects have no fields")
        activity_label, role_names = keys[0], keys[1:]
        rows = []
        for obj in data:
            obj = dict(obj)
            rows.append(
                {
                    "activity": str(obj.get(activity_label, "")),
                    "cells": {r: parse_cell(obj.get(r)) for r in role_names},
                }
            )
        return activity_label, role_names, rows

    reader = csv.reader(io.StringIO(text))
    header = next(reader, None)
    if not header:
        raise ValueError("empty CSV input")
    activity_label, role_names = header[0], [h.strip() for h in header[1:]]
    if not role_names:
        raise ValueError("matrix needs at least one role column")
    rows = []
    for raw in reader:
        if not raw or all(c.strip() == "" for c in raw):
            continue
        cells = {role_names[i]: parse_cell(raw[i + 1] if i + 1 < len(raw) else "")
                 for i in range(len(role_names))}
        rows.append({"activity": raw[0].strip(), "cells": cells})
    if not rows:
        raise ValueError("matrix has no activity rows")
    return activity_label, role_names, rows


def validate(role_names, rows, max_ci: int, max_a_share: float):
    """Return a list of findings: (level, activity_or_role, code, message)."""
    findings = []
    for row in rows:
        act = row["activity"] or "(unnamed)"
        a_roles = [r for r, s in row["cells"].items() if "A" in s]
        r_roles = [r for r, s in row["cells"].items() if "R" in s]
        ci_roles = [r for r, s in row["cells"].items() if s & {"C", "I"}]
        if len(a_roles) == 0:
            findings.append(("ERROR", act, "no accountability",
                             "no role is Accountable (A)"))
        elif len(a_roles) > 1:
            findings.append(("ERROR", act, "multiple accountable",
                             "more than one Accountable: " + ", ".join(a_roles)))
        if len(r_roles) == 0:
            findings.append(("ERROR", act, "no responsible",
                             "no role is Responsible (R)"))
        if len(ci_roles) > max_ci:
            findings.append(("WARN", act, "too many cooks",
                             f"{len(ci_roles)} roles are C or I (max {max_ci})"))

    total = len(rows)
    if total:
        for role in role_names:
            a_count = sum(1 for row in rows if "A" in row["cells"].get(role, set()))
            if a_count > max_a_share * total:
                findings.append(("WARN", role, "overloaded",
                                 f"Accountable on {a_count}/{total} activities "
                                 f"(over {max_a_share:.0%})"))
    return findings


def render_matrix(activity_label, role_names, rows) -> str:
    headers = [activity_label] + role_names

    def cell_text(letters):
        return "/".join(L for L in ("A", "R", "C", "I") if L in letters)

    table = [[row["activity"]] + [cell_text(row["cells"][r]) for r in role_names]
             for row in rows]
    widths = [max(len(headers[c]), *(len(r[c]) for r in table)) if table else len(headers[c])
              for c in range(len(headers))]

    def line(cells):
        return "  ".join(c.ljust(widths[i]) for i, c in enumerate(cells))

    out = [line(headers), line(["-" * w for w in widths])]
    out += [line(r) for r in table]
    return "\n".join(out)


def render_report(findings) -> str:
    errors = [f for f in findings if f[0] == "ERROR"]
    warns = [f for f in findings if f[0] == "WARN"]
    out = ["", "Validation report:"]
    if not findings:
        out.append("  (no issues)")
    for level, subject, code, msg in findings:
        out.append(f"  {level:5}  {subject}: {code} - {msg}")
    out.append("")
    status = "FAIL" if errors else "PASS"
    out.append(f"Result: {status}  ({len(errors)} error(s), {len(warns)} warning(s))")
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a RACI matrix: one A and at least one R per activity.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exit code is non-zero on validation FAIL (any ERROR) or bad input.",
    )
    parser.add_argument("path", help="path to CSV/JSON RACI matrix, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="parse input as JSON (default: CSV)")
    parser.add_argument("--max-ci", type=int, default=4,
                        help="WARN above this many C/I roles per activity (default 4)")
    parser.add_argument("--max-a-share", type=float, default=0.5,
                        help="WARN if a role is A on more than this share of activities (default 0.5)")
    args = parser.parse_args(argv)

    try:
        text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
        activity_label, role_names, rows = load_matrix(text, args.json)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    findings = validate(role_names, rows, args.max_ci, args.max_a_share)
    print(render_matrix(activity_label, role_names, rows))
    print(render_report(findings))
    return 1 if any(f[0] == "ERROR" for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
