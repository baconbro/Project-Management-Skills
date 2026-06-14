#!/usr/bin/env python3
"""Evaluate an investment's cashflows: NPV, ROI, and payback period.

Reads a stream of period cashflows from CSV or JSON and prints a per-period
table (discounted value and running cumulative), then the headline financials:
net present value, return on investment, and payback period. Stdlib only.

Input columns / keys (case-insensitive, extra columns ignored):
    period      integer period index, 0-based (0 = today / up-front outlay)
    cashflow    net cash in that period; negative = cost, positive = benefit

Computed:
    discounted = cashflow / (1 + rate) ** period
    cumulative = running sum of undiscounted cashflow (used for payback)
    NPV        = sum of discounted cashflows
    ROI        = (sum positive cashflows - sum |negative cashflows|)
                 / sum |negative cashflows|
    payback    = first period where cumulative >= 0 (interpolated to a fraction)

Usage:
    python roi_npv.py cashflows.csv
    python roi_npv.py cashflows.json --json
    python roi_npv.py cashflows.csv --rate 0.08
    cat cashflows.csv | python roi_npv.py -        # read from stdin
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
            data = data.get("cashflows", [])
        if not isinstance(data, list):
            raise ValueError("JSON must be a list of cashflows or {'cashflows': [...]}")
        return [dict(r) for r in data]
    reader = csv.DictReader(io.StringIO(text))
    return [dict(r) for r in reader]


def evaluate(rows: list, rate: float) -> dict:
    flows = []
    for i, row in enumerate(rows, start=1):
        period_raw = _get(row, "period", "t", "year")
        cf_raw = _get(row, "cashflow", "cash_flow", "cf", "net")
        if period_raw is None or cf_raw is None:
            raise ValueError(f"row {i}: missing period or cashflow")
        period = int(float(period_raw))
        if period < 0:
            raise ValueError(f"row {i}: period must be >= 0 (got {period})")
        cf = float(cf_raw)
        flows.append((period, cf))

    flows.sort(key=lambda x: x[0])

    table = []
    cumulative = 0.0
    npv = 0.0
    pos_sum = 0.0
    neg_abs_sum = 0.0
    prev_cumulative = 0.0
    payback = None
    for period, cf in flows:
        discounted = cf / (1.0 + rate) ** period
        npv += discounted
        prev_cumulative = cumulative
        cumulative += cf
        if cf > 0:
            pos_sum += cf
        else:
            neg_abs_sum += abs(cf)
        # payback: first period where cumulative crosses to >= 0
        if payback is None and cumulative >= 0:
            if cf != 0 and prev_cumulative < 0:
                # interpolate the fraction of this period needed to break even
                frac = -prev_cumulative / cf
                payback = (period - 1) + frac
            else:
                payback = float(period)
        table.append(
            {
                "period": period,
                "cashflow": cf,
                "discounted": discounted,
                "cumulative": cumulative,
            }
        )

    roi = (pos_sum - neg_abs_sum) / neg_abs_sum if neg_abs_sum else float("nan")
    return {
        "table": table,
        "npv": npv,
        "roi": roi,
        "payback": payback,
        "pos_sum": pos_sum,
        "neg_abs_sum": neg_abs_sum,
        "rate": rate,
    }


def render(result: dict) -> str:
    table = result["table"]
    if not table:
        return "No cashflows found in input."
    headers = ["Period", "Cashflow", "Discounted", "Cumulative"]
    rows = [
        [
            str(r["period"]),
            f"{r['cashflow']:,.2f}",
            f"{r['discounted']:,.2f}",
            f"{r['cumulative']:,.2f}",
        ]
        for r in table
    ]
    widths = [max(len(h), *(len(row[c]) for row in rows)) for c, h in enumerate(headers)]

    def line(cells):
        return "  ".join(c.rjust(widths[i]) if i else c.ljust(widths[i]) for i, c in enumerate(cells))

    out = [line(headers), line(["-" * w for w in widths])]
    out += [line(r) for r in rows]
    out.append("")
    out.append(f"Discount rate: {result['rate']:.2%}")
    out.append(f"NPV: {result['npv']:,.2f}")
    roi = result["roi"]
    out.append(f"ROI: {roi:.2%}" if roi == roi else "ROI: n/a (no costs)")
    if result["payback"] is None:
        out.append("Payback: never (cumulative cashflow stays negative)")
    else:
        out.append(f"Payback period: {result['payback']:.2f} periods")
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate investment cashflows: NPV, ROI, and payback period.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="period 0 = today (no discounting); negative cashflow = cost.",
    )
    parser.add_argument("path", help="path to CSV/JSON cashflows, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="parse input as JSON (default: CSV)")
    parser.add_argument(
        "--rate", type=float, default=0.10,
        help="annual discount rate as a fraction (default 0.10 = 10%%)",
    )
    args = parser.parse_args(argv)

    if args.rate <= -1.0:
        parser.error("--rate must be greater than -1")

    try:
        text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
        result = evaluate(load_rows(text, args.json), args.rate)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
