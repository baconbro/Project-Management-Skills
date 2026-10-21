#!/usr/bin/env python3
"""Three-point (PERT) estimation: expected values, uncertainty drivers, confidence
levels, contingency reserve, and an optional PERT-Beta simulation of the total.

Reads estimation items with optimistic / most-likely / pessimistic values from a CSV
or JSON worksheet, computes the PERT mean and standard deviation per item, then the
totals, confidence ranges, one-sided commit levels and the reserve needed to commit
at a chosen confidence. Standard library only.

INPUT COLUMNS / KEYS  (case-insensitive; extra columns are carried or ignored)
    id            item identifier, ideally the WBS id        aliases: wbs, wbs_id, ref       (optional)
    task          item name                                  aliases: name, item, description (optional)
    unit          unit of O/M/P (person-days, weeks, USD...) aliases: units, uom              (optional)
    optimistic    best-case value  (O)                       aliases: o, best, min, low       (required)
    most_likely   most-likely value (M)                      aliases: m, likely, most likely, mostlikely, ml, mode (required)
    pessimistic   worst-case value (P)                       aliases: p, worst, max, high     (required)
    technique, assumptions, estimators, actual               basis-of-estimate columns; carried, not used by the math
  Values must be finite numbers >= 0 with O <= M <= P. '$', ',', EUR/GBP signs and a trailing
  '%' are stripped ("80,000" -> 80000, "$100" -> 100, "40%" -> 40). One unit per worksheet
  (mixed units are an error); --unit labels the totals when there is no unit column.
  CSV delimiter is auto-detected (, ; tab |); a UTF-8 BOM and CRLF line ends are tolerated.
  JSON is a list of objects or {"items": [...]}; files ending in .json parse as JSON
  automatically, otherwise pass --json (always needed for JSON on stdin).

FORMULAS
  per item    E = (O + 4M + P) / 6        std = (P - O) / 6        var = std^2
              Var% = var / sum(var)       share of the total variance = the uncertainty drivers
              flag 'wide'                 when (P - O) > 2 * M, i.e. the range is wider than twice M
  totals      sum E  = TOTAL EFFORT (or the duration of ONE strictly sequential chain)
              total std = sqrt(sum var)   items are assumed independent; correlated risks widen it
  two-sided   E +/- z * std  with z = 1 (~68%), 1.645 (90%), 1.960 (95%); a lower bound below 0
              is clamped at 0 and marked, which signals the normal approximation is poor
  one-sided   P-level = E + z(P) * std, z from the inverse normal CDF:
              P50 = E, P80 = E + 0.842 std, P90 = E + 1.282 std
              reserve at P = P-level - sum E  (the contingency needed to commit at that confidence)
  simulation  --simulate N draws every item from its PERT-Beta distribution:
              alpha = 1 + 4(M-O)/(P-O), beta = 1 + 4(P-M)/(P-O), value = O + Beta(alpha, beta) * (P-O);
              items with P == O contribute O. Reports mean, std, P10/P50/P80/P90/P95 of the simulated
              total and the empirical commit level(s) for --confidence.

  The sum is NOT the project duration when items run in parallel: feed the per-item E to
  project-schedule (critical_path.py) and total a single path with --ids.

EXIT CODES   0 success  -  2 bad input, bad option or internal error ("error: ..." on stderr)

EXAMPLES
  python .claude/skills/estimation/scripts/pert_estimate.py .claude/skills/estimation/assets/estimation-worksheet-sample.csv
  python .claude/skills/estimation/scripts/pert_estimate.py .claude/skills/estimation/assets/estimation-worksheet-sample.csv --confidence P80 --simulate 20000 --seed 42
  python .claude/skills/estimation/scripts/pert_estimate.py .claude/skills/estimation/assets/duration-worksheet-sample.csv --ids A,B,D,F,G,H,J
  python .claude/skills/estimation/scripts/pert_estimate.py items.json --json --format json
  cat worksheet.csv | python .claude/skills/estimation/scripts/pert_estimate.py - --format csv > estimates.csv
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import random
import re
import statistics
import sys

BOM = "﻿"
JSON_KEY = "items"
TASK_WIDTH = 40
MAX_TRIALS = 500_000
HIST_BINS = 15
HIST_WIDTH = 40

ID_ALIASES = ("id", "wbs", "wbs_id", "ref")
TASK_ALIASES = ("task", "name", "item", "description")
UNIT_ALIASES = ("unit", "units", "uom")
O_ALIASES = ("optimistic", "o", "best", "min", "low")
M_ALIASES = ("most_likely", "m", "likely", "most likely", "mostlikely", "ml", "mode")
P_ALIASES = ("pessimistic", "p", "worst", "max", "high")
CARRIED = ("technique", "assumptions", "estimators", "actual")

_NORMAL = statistics.NormalDist()
# (label, z) for the two-sided bands around the total; 90% / 95% from the inverse normal CDF.
TWO_SIDED = (("~68%", 1.0), ("90%", _NORMAL.inv_cdf(0.95)), ("95%", _NORMAL.inv_cdf(0.975)))
ONE_SIDED = (0.50, 0.80, 0.90)
SIM_LEVELS = (0.10, 0.50, 0.80, 0.90, 0.95)


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


def _fmt(x, places=2):
    s = f"{x:,.{places}f}"
    return "0." + "0" * places if s.strip("-") == "0." + "0" * places else s


def _pct(x):
    return f"{x:.1f}%"


def _level_label(p):
    return f"P{p * 100:g}"


def _quantile(sorted_vals, p):
    """Inclusive linear-interpolation quantile of an already sorted list (0 < p < 1)."""
    n = len(sorted_vals)
    if n == 1:
        return sorted_vals[0]
    h = (n - 1) * p
    lo = int(math.floor(h))
    hi = min(lo + 1, n - 1)
    return sorted_vals[lo] + (h - lo) * (sorted_vals[hi] - sorted_vals[lo])


# ----------------------------------------------------------------------------- core maths
def _cell(row, aliases, label, where):
    raw = _get(row, *aliases)
    if raw is None:
        raise ValueError(f"{where}, column {label}: value is missing")
    return _num(raw, f"{where}, column {label}", minimum=0)


def parse_items(rows):
    """Turn worksheet rows into validated item dicts with E, std and var."""
    items = []
    for i, row in enumerate(rows, start=1):
        ident = _get(row, *ID_ALIASES)
        name = _sanitize(_get(row, *TASK_ALIASES, default=""))
        if ident is None:
            ident = name or f"T{i:03d}"
        ident = _sanitize(ident)
        if name == ident:
            name = ""
        where = f"row {i} ({ident})"
        o = _cell(row, O_ALIASES, "optimistic", where)
        m = _cell(row, M_ALIASES, "most_likely", where)
        p = _cell(row, P_ALIASES, "pessimistic", where)
        if not (o <= m <= p):
            raise ValueError(
                f"{where}: require optimistic <= most_likely <= pessimistic "
                f"(got O={_fmt(o)}, M={_fmt(m)}, P={_fmt(p)})"
            )
        e = (o + 4.0 * m + p) / 6.0
        std = (p - o) / 6.0
        var = std * std
        if not (math.isfinite(e) and math.isfinite(var)):
            raise ValueError(f"{where}: values are too large to compute E and variance")
        item = {
            "id": ident,
            "task": name,
            "unit": _sanitize(_get(row, *UNIT_ALIASES, default="")),
            "optimistic": o,
            "most_likely": m,
            "pessimistic": p,
            "e": e,
            "std": std,
            "var": var,
            "flag": "wide" if (p - o) > 2.0 * m else "",
        }
        for col in CARRIED:
            item[col] = _sanitize(_get(row, col, default=""))
        items.append(item)
    return items


def select_items(items, ids):
    """Keep only the items whose id is in ids (case-insensitive); error on unknown ids."""
    if ids is None:
        return items
    wanted = [s.lower() for s in ids]
    known = {it["id"].lower() for it in items}
    unknown = [s for s in ids if s.lower() not in known]
    if unknown:
        raise ValueError(
            f"--ids: unknown id(s) {unknown}; known ids: {[it['id'] for it in items]}"
        )
    return [it for it in items if it["id"].lower() in wanted]


def estimate(rows, ids=None, unit_label=None, levels=()):
    """Validate rows, total the selected items and compute ranges, drivers and reserves."""
    items = select_items(parse_items(rows), ids)
    units = sorted({it["unit"] for it in items if it["unit"]})
    if len(units) > 1:
        raise ValueError(f"mixed units {units}: totals need one unit per worksheet (split the file or fix the unit column)")
    unit = unit_label or (units[0] if units else "")

    sum_e = round(sum(it["e"] for it in items), 6)
    sum_var = round(sum(it["var"] for it in items), 6)
    if not (math.isfinite(sum_e) and math.isfinite(sum_var)):
        raise OverflowError("totals overflow: the values are too large to sum")
    total_std = math.sqrt(sum_var)
    for it in items:
        it["var_pct"] = (it["var"] / sum_var * 100.0) if sum_var > 0 else 0.0

    bands = []
    for label, z in TWO_SIDED:
        raw_lo = sum_e - z * total_std
        bands.append({"label": label, "z": z, "low": max(0.0, raw_lo), "high": sum_e + z * total_std,
                      "clamped": raw_lo < 0})
    one_sided = {_level_label(p): sum_e + _NORMAL.inv_cdf(p) * total_std for p in ONE_SIDED}
    commits = [_commit(sum_e, sum_e + _NORMAL.inv_cdf(p) * total_std, p) for p in levels]
    drivers = sorted((it for it in items if it["var"] > 0), key=lambda it: -it["var"])[:3]
    return {
        "items": items,
        "summary": {
            "selected": ids is not None,
            "count": len(items),
            "unit": unit,
            "sum_e": sum_e,
            "sum_var": sum_var,
            "total_std": total_std,
            "two_sided": bands,
            "one_sided": one_sided,
            "commit": commits,
            "drivers": [{"id": it["id"], "var_pct": it["var_pct"]} for it in drivers],
            "simulation": None,
        },
    }


def _commit(sum_e, value, p):
    reserve = value - sum_e
    return {"level": _level_label(p), "p": p, "value": value, "reserve": reserve,
            "reserve_pct": (reserve / sum_e * 100.0) if sum_e > 0 else 0.0}


def simulate(items, trials, seed, levels=()):
    """Monte Carlo on the PERT-Beta distribution of every item; returns quantiles of the total."""
    rng = random.Random(seed)
    constant = 0.0
    variable = []
    for it in items:
        o, m, p = it["optimistic"], it["most_likely"], it["pessimistic"]
        span = p - o
        if span > 0:
            variable.append((o, span, 1.0 + 4.0 * (m - o) / span, 1.0 + 4.0 * (p - m) / span))
        else:
            constant += o
    totals = []
    for _ in range(trials):
        total = constant
        for o, span, alpha, beta in variable:
            total += o + rng.betavariate(alpha, beta) * span
        totals.append(total)
    totals.sort()
    mean = statistics.fmean(totals)
    sum_e = sum(it["e"] for it in items)
    quantiles = {_level_label(p): _quantile(totals, p) for p in SIM_LEVELS}
    return {
        "trials": trials,
        "seed": seed,
        "mean": mean,
        "std": statistics.pstdev(totals) if trials > 1 else 0.0,
        "min": totals[0],
        "max": totals[-1],
        "quantiles": quantiles,
        "commit": [_commit(sum_e, _quantile(totals, p), p) for p in levels],
        "histogram": _histogram(totals),
    }


def _histogram(totals):
    lo, hi = totals[0], totals[-1]
    if hi <= lo:
        return [{"low": lo, "high": hi, "count": len(totals)}]
    step = (hi - lo) / HIST_BINS
    counts = [0] * HIST_BINS
    for t in totals:
        counts[min(int((t - lo) / step), HIST_BINS - 1)] += 1
    return [{"low": lo + b * step, "high": lo + (b + 1) * step, "count": c} for b, c in enumerate(counts)]


# ----------------------------------------------------------------------------- renderers
def _table_rows(items):
    show_task = any(it["task"] for it in items)
    show_flag = any(it["flag"] for it in items)
    headers = ["ID"] + (["Task"] if show_task else []) + ["O", "M", "P", "E", "Std", "Var%"] + (["Flag"] if show_flag else [])
    rows = []
    for it in items:
        cells = [_sanitize(it["id"], TASK_WIDTH)] + ([_sanitize(it["task"], TASK_WIDTH)] if show_task else [])
        cells += [_fmt(it["optimistic"]), _fmt(it["most_likely"]), _fmt(it["pessimistic"]),
                  _fmt(it["e"]), _fmt(it["std"]), _pct(it["var_pct"])]
        if show_flag:
            cells.append(it["flag"])
        rows.append(cells)
    left = {0, 1} if show_task else {0}
    if show_flag:
        left.add(len(headers) - 1)
    return headers, rows, left


def _summary_lines(result):
    s = result["summary"]
    unit = f" {s['unit']}" if s["unit"] else ""
    scope = f"the {s['count']} selected items" if s["selected"] else f"all {s['count']} items"
    out = [f"Totals: serial sum of {scope} = total EFFORT, or the duration of ONE sequential chain"
           + (f" ({s['unit']})" if s["unit"] else "") + ":"]
    for label, value in (("Sum of E (expected total):", s["sum_e"]),
                         ("Sum of variances:", s["sum_var"]),
                         ("Total std dev (sqrt of sum):", s["total_std"])):
        out.append(f"  {label:<30}{_fmt(value):>14}")
    out.append("")
    out.append("Two-sided ranges around the total (normal approximation):")
    for band in s["two_sided"]:
        mark = "   (lower bound clamped at 0: skewed total, prefer --simulate)" if band["clamped"] else ""
        out.append(f"  {band['label']:>5} (E +/- {band['z']:.3f} std):  {_fmt(band['low'])} .. {_fmt(band['high'])}{mark}")
    out.append("")
    out.append("One-sided commit levels (normal approximation):")
    out.append("  " + "   ".join(f"{k} = {_fmt(v)}" for k, v in s["one_sided"].items()))
    for c in s["commit"]:
        out.append(f"  Commit at {c['level']}: {_fmt(c['value'])}{unit}  ->  reserve above sum E: "
                   f"{_fmt(c['reserve'])} ({_pct(c['reserve_pct'])} of E)")
    if s["drivers"]:
        out.append("")
        out.append("Top uncertainty drivers (share of total variance): "
                   + ", ".join(f"{d['id']} ({_pct(d['var_pct'])})" for d in s["drivers"]))
    sim = s["simulation"]
    if sim:
        out.append("")
        out.append(f"PERT-Beta simulation ({sim['trials']:,} trials, seed {sim['seed']}):")
        out.append(f"  mean {_fmt(sim['mean'])}   std {_fmt(sim['std'])}   min {_fmt(sim['min'])}   max {_fmt(sim['max'])}")
        out.append("  " + "   ".join(f"{k} = {_fmt(v)}" for k, v in sim["quantiles"].items()))
        for c in sim["commit"]:
            out.append(f"  Commit at {c['level']} (simulated): {_fmt(c['value'])}{unit}  ->  reserve above sum E: "
                       f"{_fmt(c['reserve'])} ({_pct(c['reserve_pct'])} of E)")
        peak = max(h["count"] for h in sim["histogram"]) or 1
        for h in sim["histogram"]:
            bar = "#" * int(round(h["count"] / peak * HIST_WIDTH))
            out.append(f"  {_fmt(h['low']):>12} .. {_fmt(h['high']):<12} {bar} {h['count']}")
    out.append("")
    out.append("Note: the total is the sum of the items = total EFFORT (or the duration of one strictly")
    out.append("sequential chain). The duration of parallel work comes from the critical path in")
    out.append("project-schedule; use --ids to total a single path. Items are assumed independent.")
    return out


def render_table(result):
    headers, rows, left = _table_rows(result["items"])
    widths = [max(len(h), *(len(r[c]) for r in rows)) for c, h in enumerate(headers)]

    def line(cells):
        return "  ".join(c.ljust(widths[i]) if i in left else c.rjust(widths[i]) for i, c in enumerate(cells)).rstrip()

    unit = result["summary"]["unit"]
    out = [f"Per-item PERT estimates" + (f" (unit: {unit})" if unit else "")]
    out += [line(headers), line(["-" * w for w in widths])]
    out += [line(r) for r in rows]
    out.append("")
    out += _summary_lines(result)
    return "\n".join(out)


def render_md(result):
    headers, rows, left = _table_rows(result["items"])
    unit = result["summary"]["unit"]
    out = ["## Per-item PERT estimates" + (f" (unit: {unit})" if unit else ""), ""]
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(":---" if i in left else "---:" for i in range(len(headers))) + "|")
    for r in rows:
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
    out.append("")
    out.append("```")
    out += _summary_lines(result)
    out.append("```")
    return "\n".join(out)


def render_csv(result):
    cols = ["id", "task", "unit", "technique", "optimistic", "most_likely", "pessimistic",
            "e", "std", "var", "var_pct", "flag"]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=cols, lineterminator="\n")
    writer.writeheader()
    unit = result["summary"]["unit"]
    for it in result["items"]:
        row = {c: it.get(c, "") for c in cols}
        row["unit"] = it["unit"] or unit
        for c in ("optimistic", "most_likely", "pessimistic", "e", "std", "var", "var_pct"):
            row[c] = f"{it[c]:.4f}".rstrip("0").rstrip(".")
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


def render_json(result):
    return json.dumps(_rounded(result), indent=2, ensure_ascii=False)


RENDERERS = {"table": render_table, "json": render_json, "csv": render_csv, "md": render_md}


# ----------------------------------------------------------------------------- CLI
def _parse_level(raw, parser):
    s = str(raw).strip().lower().lstrip("p").rstrip("%").strip()
    try:
        v = float(s)
    except ValueError:
        parser.error(f"--confidence {raw!r} is not a number (use 0.8, 80 or P80)")
    if not math.isfinite(v):
        parser.error(f"--confidence {raw!r} must be finite")
    if v > 1.0:
        v /= 100.0
    if not (0.0 < v < 1.0):
        parser.error(f"--confidence {raw!r} must be between 0 and 1 exclusive (e.g. 0.8, 80 or P80)")
    return round(v, 6)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="pert_estimate.py",
        description="Three-point (PERT) estimation: per-item E/std/variance share, totals, "
                    "confidence ranges, commit levels, contingency reserve and a PERT-Beta simulation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("path", help="CSV or JSON worksheet, or '-' for stdin (a .json extension selects JSON)")
    parser.add_argument("--json", action="store_true",
                        help="force JSON parsing (needed for JSON on stdin or without a .json extension)")
    parser.add_argument("--ids", metavar="ID[,ID...]",
                        help="total only these item ids, e.g. the critical-path chain (case-insensitive)")
    parser.add_argument("--confidence", metavar="P", action="append",
                        help="one-sided confidence to commit at (0.8, 80 or P80; repeatable): prints the "
                             "commit value and the reserve above sum E, analytic and, with --simulate, empirical")
    parser.add_argument("--simulate", metavar="N", type=int, default=0,
                        help=f"draw N PERT-Beta trials of the total (1..{MAX_TRIALS:,}; 10,000-50,000 is plenty) "
                             "and report mean, std, P10/P50/P80/P90/P95 and a histogram")
    parser.add_argument("--seed", metavar="K", type=int,
                        help="random seed for --simulate (default: random, printed so the run can be repeated)")
    parser.add_argument("--unit", metavar="LABEL",
                        help="unit label for the totals when the worksheet has no unit column (e.g. person-days)")
    parser.add_argument("--format", choices=("table", "json", "csv", "md"), default="table",
                        help="output format: table (default), json (items + summary), csv (per-item rows only, "
                             "for hand-off to project-schedule / cost-management), md (markdown table + summary)")
    args = parser.parse_args(argv)

    if args.simulate < 0 or args.simulate > MAX_TRIALS:
        parser.error(f"--simulate must be between 1 and {MAX_TRIALS:,} (got {args.simulate})")
    if args.seed is not None and args.simulate == 0:
        parser.error("--seed only makes sense with --simulate N")
    levels = [_parse_level(raw, parser) for raw in (args.confidence or [])]
    ids = None
    if args.ids is not None:
        ids = [s.strip() for s in args.ids.split(",") if s.strip()]
        if not ids:
            parser.error("--ids needs at least one id, e.g. --ids A,B,D")
    if args.unit is not None and not args.unit.strip():
        parser.error("--unit must not be blank")

    try:
        text = read_text(args.path)
        as_json = args.json or (args.path != "-" and args.path.lower().endswith(".json"))
        rows, headers = load_rows(text, as_json, JSON_KEY)
        require_columns(headers, [O_ALIASES, M_ALIASES, P_ALIASES])
        result = estimate(rows, ids=ids, unit_label=(args.unit.strip() if args.unit else None), levels=levels)
        if args.simulate:
            seed = args.seed if args.seed is not None else random.SystemRandom().randrange(1_000_000_000)
            result["summary"]["simulation"] = simulate(result["items"], args.simulate, seed, levels)
        print(RENDERERS[args.format](result))
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
