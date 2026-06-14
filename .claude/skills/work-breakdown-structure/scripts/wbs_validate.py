#!/usr/bin/env python3
"""Validate a work breakdown structure: hierarchy, the 100% rule, and decomposition.

Reads a WBS from CSV or JSON, infers each element's parent from its dotted id
(parent of 1.1.2 is 1.1; top-level ids like 1, 2 have no parent), prints the WBS
as an indented tree, then a validation report and a pass/fail line. Stdlib only.

Input columns / keys (case-insensitive, extra columns ignored):
    id        dotted identifier, e.g. 1, 1.1, 1.1.2     (required)
    name      element name                              (optional)
    weight    numeric percent of its parent             (optional)

Checks:
    duplicate ids                                   -> ERROR
    a non-top id whose parent id does not exist     -> ERROR (orphan)
    100% rule: when a parent's children carry       -> ERROR if not ~100
        weights, those weights must sum to 100        (tolerance 0.1)
    a parent with exactly one child                 -> WARN (no real decomposition)

Usage:
    python wbs_validate.py wbs.csv
    python wbs_validate.py wbs.json --json
    cat wbs.csv | python wbs_validate.py -            # read from stdin
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys

TOLERANCE = 0.1


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
            data = data.get("wbs", data.get("elements", []))
        if not isinstance(data, list):
            raise ValueError("JSON must be a list of elements or {'wbs': [...]}")
        return [dict(r) for r in data]
    reader = csv.DictReader(io.StringIO(text))
    return [dict(r) for r in reader]


def parent_id(eid: str):
    """Parent of a dotted id, or None for a top-level id."""
    if "." not in eid:
        return None
    return eid.rsplit(".", 1)[0]


def parse(rows: list) -> list:
    elements = []
    for i, row in enumerate(rows, start=1):
        rid = _get(row, "id", "wbs", "code")
        if rid is None:
            raise ValueError(f"row {i}: missing id")
        rid = str(rid).strip()
        name = str(_get(row, "name", "element", "deliverable", default=""))
        weight_raw = _get(row, "weight", "pct", "percent")
        weight = None
        if weight_raw is not None:
            try:
                weight = float(weight_raw)
            except (TypeError, ValueError):
                raise ValueError(f"row {i} (id {rid}): weight '{weight_raw}' is not numeric")
        elements.append({"id": rid, "name": name, "weight": weight})
    return elements


def validate(elements: list) -> dict:
    errors, warnings = [], []
    ids = [e["id"] for e in elements]
    idset = set()

    # (a) duplicate ids
    seen = set()
    for eid in ids:
        if eid in seen:
            errors.append(f"duplicate id '{eid}'")
        seen.add(eid)
        idset.add(eid)

    # (b) orphans: a non-top id whose parent does not exist
    for e in elements:
        par = parent_id(e["id"])
        if par is not None and par not in idset:
            errors.append(f"orphan id '{e['id']}': parent '{par}' does not exist")

    # group children by parent
    children: dict = {}
    for e in elements:
        par = parent_id(e["id"])
        if par is not None:
            children.setdefault(par, []).append(e)

    # (c) 100% rule, (d) single-child warning
    for par, kids in sorted(children.items()):
        weighted = [k for k in kids if k["weight"] is not None]
        if weighted:
            total = sum(k["weight"] for k in weighted)
            if abs(total - 100.0) > TOLERANCE:
                errors.append(
                    f"100% rule: children of '{par}' have weights summing to "
                    f"{total:g} (expected 100)"
                )
        if len(kids) == 1:
            warnings.append(
                f"single child: '{par}' has only one child "
                f"('{kids[0]['id']}') — no real decomposition"
            )

    return {"errors": errors, "warnings": warnings}


def render_tree(elements: list) -> str:
    out = []
    for e in sorted(elements, key=lambda x: [int(p) if p.isdigit() else p
                                             for p in x["id"].split(".")]):
        depth = e["id"].count(".")
        indent = "  " * depth
        wt = f"  ({e['weight']:g}%)" if e["weight"] is not None else ""
        name = f" {e['name']}" if e["name"] else ""
        out.append(f"{indent}{e['id']}{name}{wt}")
    return "\n".join(out)


def render(elements: list, result: dict) -> str:
    out = ["Work Breakdown Structure", "------------------------"]
    out.append(render_tree(elements))
    out.append("")
    out.append("Validation report")
    out.append("-----------------")
    for e in result["errors"]:
        out.append(f"  ERROR:   {e}")
    for w in result["warnings"]:
        out.append(f"  warning: {w}")
    if not result["errors"] and not result["warnings"]:
        out.append("  (no issues)")
    out.append("")
    n_err, n_warn = len(result["errors"]), len(result["warnings"])
    status = "PASS" if n_err == 0 else "FAIL"
    out.append(f"{status}: {n_err} error(s), {n_warn} warning(s)")
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a WBS: hierarchy, the 100% rule, and decomposition.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Parent is inferred from the dotted id; top-level ids have no parent.",
    )
    parser.add_argument("path", help="path to CSV/JSON WBS, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="parse input as JSON (default: CSV)")
    args = parser.parse_args(argv)

    try:
        text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
        elements = parse(load_rows(text, args.json))
        if not elements:
            raise ValueError("no WBS elements found in input")
        result = validate(elements)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(render(elements, result))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
