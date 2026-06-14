#!/usr/bin/env python3
"""Earned-value health check: CV/SV, CPI/SPI, EAC/ETC/VAC, and a RAG verdict.

Reads rows of work (planned value, earned value, actual cost, optional budget)
from CSV or JSON and prints a per-row table, a TOTAL row, and an overall
RAG (Red/Amber/Green) status derived from CPI and SPI. Standard library only.

Input columns / keys (case-insensitive, extra columns ignored):
    task   short work-item name                      (optional)
    pv     planned value (budgeted cost of scheduled work)   REQUIRED
    ev     earned value  (budgeted cost of completed work)   REQUIRED
    ac     actual cost   (actually spent)                    REQUIRED
    bac    budget at completion for the item         (optional)

Computed per row and for the TOTAL:
    CV  = EV - AC          CPI = EV / AC
    SV  = EV - PV          SPI = EV / PV
If BAC is known (per-row sum, or supplied via --bac for the total):
    EAC = BAC / CPI        VAC = BAC - EAC        ETC = EAC - AC

RAG (configurable via --green / --amber, applied to BOTH CPI and SPI):
    both >= --green                 -> GREEN
    either <  --amber               -> RED
    otherwise                       -> AMBER

Usage:
    python health_check.py cost-baseline.csv
    python health_check.py cost-baseline.json --json
    python health_check.py cost-baseline.csv --bac 800000
    python health_check.py cost-baseline.csv --green 0.95 --amber 0.85
    cat cost-baseline.csv | python health_check.py -        # read from stdin
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
            data = data.get("tasks", data.get("rows", []))
        if not isinstance(data, list):
            raise ValueError("JSON must be a list of rows or {'tasks': [...]}")
        return [dict(r) for r in data]
    reader = csv.DictReader(io.StringIO(text))
    return [dict(r) for r in reader]


def rag(cpi: float, spi: float, green: float, amber: float) -> str:
    if cpi >= green and spi >= green:
        return "GREEN"
    if cpi < amber or spi < amber:
        return "RED"
    return "AMBER"


def evm(pv: float, ev: float, ac: float, bac):
    """Return the derived EVM metrics for one set of primitives."""
    m = {
        "pv": pv,
        "ev": ev,
        "ac": ac,
        "bac": bac,
        "cv": ev - ac,
        "sv": ev - pv,
        "cpi": (ev / ac) if ac else None,
        "spi": (ev / pv) if pv else None,
        "eac": None,
        "etc": None,
        "vac": None,
    }
    if bac is not None and m["cpi"]:
        m["eac"] = bac / m["cpi"]
        m["etc"] = m["eac"] - ac
        m["vac"] = bac - m["eac"]
    return m


def compute(rows: list, override_bac, green: float, amber: float) -> tuple:
    scored = []
    tot_pv = tot_ev = tot_ac = 0.0
    tot_bac = 0.0
    have_bac = True
    for i, row in enumerate(rows, start=1):
        name = _get(row, "task", "name", "id", default=f"Item {i}")
        pv_raw = _get(row, "pv", "planned_value", "planned")
        ev_raw = _get(row, "ev", "earned_value", "earned")
        ac_raw = _get(row, "ac", "actual_cost", "actual")
        if pv_raw is None or ev_raw is None or ac_raw is None:
            raise ValueError(f"row {i}: missing one of pv, ev, ac")
        pv, ev, ac = float(pv_raw), float(ev_raw), float(ac_raw)
        bac_raw = _get(row, "bac", "budget", "budget_at_completion")
        bac = float(bac_raw) if bac_raw is not None else None
        if bac is None:
            have_bac = False
        else:
            tot_bac += bac
        m = evm(pv, ev, ac, bac)
        m["task"] = str(name)
        m["rag"] = rag(m["cpi"], m["spi"], green, amber) if m["cpi"] and m["spi"] else "n/a"
        scored.append(m)
        tot_pv += pv
        tot_ev += ev
        tot_ac += ac

    if override_bac is not None:
        total_bac = override_bac
    elif have_bac:
        total_bac = tot_bac
    else:
        total_bac = None
    total = evm(tot_pv, tot_ev, tot_ac, total_bac)
    total["task"] = "TOTAL"
    total["rag"] = rag(total["cpi"], total["spi"], green, amber) if total["cpi"] and total["spi"] else "n/a"
    return scored, total


def _money(v):
    return "" if v is None else f"{v:,.0f}"


def _index(v):
    return "" if v is None else f"{v:.3f}"


def render(scored: list, total: dict) -> str:
    headers = ["Task", "PV", "EV", "AC", "CV", "SV", "CPI", "SPI", "EAC", "VAC", "RAG"]
    def row_cells(m):
        return [
            m["task"],
            _money(m["pv"]), _money(m["ev"]), _money(m["ac"]),
            _money(m["cv"]), _money(m["sv"]),
            _index(m["cpi"]), _index(m["spi"]),
            _money(m["eac"]), _money(m["vac"]),
            m["rag"],
        ]
    body = [row_cells(m) for m in scored]
    total_row = row_cells(total)
    widths = [
        max(len(headers[c]), len(total_row[c]), *(len(r[c]) for r in body))
        for c in range(len(headers))
    ] if body else [max(len(headers[c]), len(total_row[c])) for c in range(len(headers))]

    def line(cells):
        out = []
        for c, cell in enumerate(cells):
            out.append(cell.ljust(widths[c]) if c == 0 else cell.rjust(widths[c]))
        return "  ".join(out)

    lines = [line(headers), line(["-" * w for w in widths])]
    lines += [line(r) for r in body]
    lines.append(line(["-" * w for w in widths]))
    lines.append(line(total_row))
    lines.append("")
    lines.append(f"Overall status: {total['rag']}   (CPI={_index(total['cpi'])}, SPI={_index(total['spi'])})")
    if total["eac"] is not None:
        verb = "overrun" if total["vac"] < 0 else "underrun"
        lines.append(
            f"Forecast: EAC={_money(total['eac'])}  ETC={_money(total['etc'])}  "
            f"VAC={_money(total['vac'])} ({verb})"
        )
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Earned-value health check: CV/SV, CPI/SPI, EAC/ETC/VAC, RAG verdict.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="RAG: both CPI and SPI >= --green => GREEN; either < --amber => RED; else AMBER.",
    )
    parser.add_argument("path", help="path to CSV/JSON of work rows (pv,ev,ac[,bac]), or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="parse input as JSON (default: CSV)")
    parser.add_argument("--bac", type=float, default=None,
                        help="total budget at completion, overrides per-row BAC sum")
    parser.add_argument("--green", type=float, default=0.95, help="GREEN threshold for CPI and SPI (default 0.95)")
    parser.add_argument("--amber", type=float, default=0.85, help="RED-below threshold for CPI and SPI (default 0.85)")
    args = parser.parse_args(argv)

    if args.amber > args.green:
        parser.error("--amber must be <= --green")

    try:
        text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
        rows = load_rows(text, args.json)
        if not rows:
            raise ValueError("no rows found in input")
        scored, total = compute(rows, args.bac, args.green, args.amber)
    except (OSError, ValueError, ZeroDivisionError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(render(scored, total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
