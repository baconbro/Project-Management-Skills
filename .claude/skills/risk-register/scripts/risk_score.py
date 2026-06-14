#!/usr/bin/env python3
"""Score a risk register: exposure (prob x impact), EMV, and severity bands.

Reads a risk register from CSV or JSON and prints a table sorted by exposure
(highest first), plus portfolio totals. Standard library only.

Input columns / keys (case-insensitive, extra columns ignored):
    id            short risk identifier                    (optional)
    description   risk description                         (optional)
    probability   chance the risk occurs, 0..1 OR 0..100 (percent)
    impact        impact if it occurs (cost units, e.g. dollars or points)

Computed:
    exposure = probability * impact          (a.k.a. expected monetary value, EMV)
    severity = band derived from exposure relative to thresholds

Usage:
    python risk_score.py risks.csv
    python risk_score.py risks.json --json
    python risk_score.py risks.csv --high 50000 --medium 10000
    cat risks.csv | python risk_score.py -        # read from stdin
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys


def _norm_prob(value) -> float:
    """Accept probability as 0..1 or 0..100; return a 0..1 fraction."""
    p = float(value)
    if p > 1.0:
        p = p / 100.0
    if p < 0.0 or p > 1.0:
        raise ValueError(f"probability out of range after normalization: {p}")
    return p


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
            data = data.get("risks", [])
        if not isinstance(data, list):
            raise ValueError("JSON must be a list of risks or {'risks': [...]}")
        return [dict(r) for r in data]
    reader = csv.DictReader(io.StringIO(text))
    return [dict(r) for r in reader]


def severity(exposure: float, high: float, medium: float) -> str:
    if exposure >= high:
        return "HIGH"
    if exposure >= medium:
        return "MEDIUM"
    return "LOW"


def score(rows: list, high: float, medium: float) -> list:
    scored = []
    for i, row in enumerate(rows, start=1):
        rid = _get(row, "id", default=f"R{i:03d}")
        desc = _get(row, "description", "desc", "risk", default="")
        prob_raw = _get(row, "probability", "prob", "p")
        impact_raw = _get(row, "impact", "i", "cost")
        if prob_raw is None or impact_raw is None:
            raise ValueError(f"row {i}: missing probability or impact")
        prob = _norm_prob(prob_raw)
        impact = float(impact_raw)
        exposure = prob * impact
        scored.append(
            {
                "id": str(rid),
                "description": str(desc),
                "probability": prob,
                "impact": impact,
                "exposure": exposure,
                "severity": severity(exposure, high, medium),
            }
        )
    scored.sort(key=lambda r: r["exposure"], reverse=True)
    return scored


def render(scored: list) -> str:
    if not scored:
        return "No risks found in input."
    headers = ["ID", "Severity", "Prob", "Impact", "Exposure/EMV", "Description"]
    rows = [
        [
            r["id"],
            r["severity"],
            f"{r['probability']:.0%}",
            f"{r['impact']:,.0f}",
            f"{r['exposure']:,.2f}",
            (r["description"][:40] + "...") if len(r["description"]) > 43 else r["description"],
        ]
        for r in scored
    ]
    widths = [max(len(h), *(len(row[c]) for row in rows)) for c, h in enumerate(headers)]

    def line(cells):
        return "  ".join(c.ljust(widths[i]) for i, c in enumerate(cells))

    out = [line(headers), line(["-" * w for w in widths])]
    out += [line(r) for r in rows]
    total_emv = sum(r["exposure"] for r in scored)
    counts = {b: sum(1 for r in scored if r["severity"] == b) for b in ("HIGH", "MEDIUM", "LOW")}
    out.append("")
    out.append(f"Total EMV (portfolio exposure): {total_emv:,.2f}")
    out.append(f"Severity counts: HIGH={counts['HIGH']}  MEDIUM={counts['MEDIUM']}  LOW={counts['LOW']}")
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Score a risk register: exposure (prob x impact), EMV, severity bands.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Severity: exposure >= --high => HIGH; >= --medium => MEDIUM; else LOW.",
    )
    parser.add_argument("path", help="path to CSV/JSON risk register, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="parse input as JSON (default: CSV)")
    parser.add_argument("--high", type=float, default=50000.0, help="HIGH severity threshold (default 50000)")
    parser.add_argument("--medium", type=float, default=10000.0, help="MEDIUM severity threshold (default 10000)")
    args = parser.parse_args(argv)

    if args.medium > args.high:
        parser.error("--medium must be <= --high")

    try:
        text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
        scored = score(load_rows(text, args.json), args.high, args.medium)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(render(scored))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
