#!/usr/bin/env python3
"""Three-point (PERT) estimation: expected value, standard deviation, and ranges.

Reads estimation items with optimistic / most-likely / pessimistic values from
CSV or JSON, computes the PERT mean and standard deviation per item, then totals
and confidence ranges for the whole estimate. Standard library only.

Input columns / keys (case-insensitive, extra columns ignored):
    id / task     item identifier or name                  (optional)
    optimistic    best-case estimate  (O)                  (required)
    most_likely   most-likely estimate (M)                 (required)
    pessimistic   worst-case estimate (P)                  (required)

Per item:
    E   = (O + 4M + P) / 6        PERT expected value (beta-distribution mean)
    std = (P - O) / 6             standard deviation
    var = std ** 2                variance

For the total:
    sum E, sum variance, total std = sqrt(sum variance)
    ranges about the total E:  ~68% = E +/- 1*std
                                90% = E +/- 1.645*std
                                95% = E +/- 1.96*std
    (lower bounds are clamped at 0)

Usage:
    python pert_estimate.py worksheet.csv
    python pert_estimate.py worksheet.json --json
    cat worksheet.csv | python pert_estimate.py -        # read from stdin
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import sys

Z_68 = 1.0
Z_90 = 1.645
Z_95 = 1.96


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
            data = data.get("items", data.get("tasks", []))
        if not isinstance(data, list):
            raise ValueError("JSON must be a list of items or {'items': [...]}")
        return [dict(r) for r in data]
    reader = csv.DictReader(io.StringIO(text))
    return [dict(r) for r in reader]


def _num(value, label: str, idx: int):
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"row {idx}: {label} '{value}' is not a number")


def estimate(rows: list) -> dict:
    items = []
    for i, row in enumerate(rows, start=1):
        ident = _get(row, "id", "task", "name", "item", default=f"T{i:03d}")
        o_raw = _get(row, "optimistic", "o", "best")
        m_raw = _get(row, "most_likely", "most likely", "mostlikely", "m", "likely")
        p_raw = _get(row, "pessimistic", "p", "worst")
        if o_raw is None or m_raw is None or p_raw is None:
            raise ValueError(f"row {i}: missing optimistic, most_likely, or pessimistic")
        o = _num(o_raw, "optimistic", i)
        m = _num(m_raw, "most_likely", i)
        p = _num(p_raw, "pessimistic", i)
        if not (o <= m <= p):
            raise ValueError(
                f"row {i} (id {ident}): require optimistic <= most_likely <= pessimistic "
                f"(got O={o:g}, M={m:g}, P={p:g})"
            )
        e = (o + 4.0 * m + p) / 6.0
        std = (p - o) / 6.0
        items.append(
            {
                "id": str(ident),
                "o": o,
                "m": m,
                "p": p,
                "e": e,
                "std": std,
                "var": std * std,
            }
        )
    if not items:
        raise ValueError("no estimation items found in input")

    sum_e = sum(it["e"] for it in items)
    sum_var = sum(it["var"] for it in items)
    total_std = math.sqrt(sum_var)
    return {
        "items": items,
        "sum_e": sum_e,
        "sum_var": sum_var,
        "total_std": total_std,
    }


def _band(e: float, std: float, z: float):
    lo = e - z * std
    return max(0.0, lo), e + z * std


def render(result: dict) -> str:
    items = result["items"]
    headers = ["ID", "O", "M", "P", "E", "Std"]
    table = [
        [
            it["id"],
            f"{it['o']:g}",
            f"{it['m']:g}",
            f"{it['p']:g}",
            f"{it['e']:.2f}",
            f"{it['std']:.2f}",
        ]
        for it in items
    ]
    widths = [max(len(h), *(len(row[c]) for row in table)) for c, h in enumerate(headers)]

    def line(cells):
        return "  ".join(c.ljust(widths[i]) if i == 0 else c.rjust(widths[i])
                         for i, c in enumerate(cells))

    out = [line(headers), line(["-" * w for w in widths])]
    out += [line(r) for r in table]

    e = result["sum_e"]
    std = result["total_std"]
    out.append("")
    out.append(f"Total expected (sum E):     {e:.2f}")
    out.append(f"Total variance (sum var):   {result['sum_var']:.2f}")
    out.append(f"Total std dev (sqrt var):   {std:.2f}")
    out.append("")
    out.append("Confidence ranges for the total estimate:")
    for label, z in (("~68%", Z_68), ("90%", Z_90), ("95%", Z_95)):
        lo, hi = _band(e, std, z)
        out.append(f"  {label:>5} (E +/- {z:g} std):  {lo:.2f} .. {hi:.2f}")
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Three-point (PERT) estimation: expected value, std dev, and ranges.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="E=(O+4M+P)/6, std=(P-O)/6; total std = sqrt(sum of variances).",
    )
    parser.add_argument("path", help="path to CSV/JSON worksheet, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="parse input as JSON (default: CSV)")
    args = parser.parse_args(argv)

    try:
        text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
        result = estimate(load_rows(text, args.json))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
