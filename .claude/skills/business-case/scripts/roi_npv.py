#!/usr/bin/env python3
"""Appraise an investment's cashflows: NPV, IRR, ROI, simple and discounted payback, a
discount-rate sensitivity sweep, optimism-bias stress factors, break-even (switching) values,
and a ranked comparison table when the sheet holds several options. Standard library only.

Reads one net cashflow per period (or gross benefit and cost columns) from CSV (delimiter
auto-detected: , ; tab |) or JSON (--json), prints a per-period table and the headline
financials, and exits 0. Notes and warnings go to stderr so stdout stays machine-readable.

INPUT COLUMNS / KEYS  (case-insensitive; spaces, hyphens and underscores in a header are
ignored, so "Cash Flow" == "cash_flow" == "cashflow"; a trailing "(unit)" is ignored; extra
columns are ignored; "row N" in messages = Nth data row, header excluded)
    period     whole-number period index; 0 = today, the up-front outlay, not discounted  REQUIRED
               aliases: t, year, yr. Calendar years (2026, 2027, ...) are accepted ONLY with
               --start-year YYYY, which rebases YYYY to period 0 and labels rows with the year.
    cashflow   net cash in the period: negative = cost, positive = benefit               REQUIRED*
               aliases: cf, net, net_cashflow, value, amount
    benefit    gross benefit in the period, a positive magnitude (inflow, saving)        *or these
    cost       gross cost in the period, a positive magnitude (outflow, spend)            two
    option     groups rows into options to compare (scenario, case, alternative)        optional
    note       free text shown in the period table (description, item, comment)         optional
    * give either a cashflow column (one NET figure per period) or benefit/cost columns
      (gross; net = benefit - cost). Several rows for the same option and period are netted
      (a note says so); a period missing between the first and the last counts as zero.

UNITS AND SCALES
    Money in any one consistent unit; "80,000", "$100", "€"/"£" and accounting negatives
    "(1,000)" are accepted. --rate is a fraction per period (0.10) or a percent ("10%"); a
    bare value >= 1 is refused as "looks like a percentage". Factors are multipliers
    (0.8 = benefits cut by 20%) or percents ("80%").

FORMULAS  (r = --rate, t = period index, CF(t) = net cashflow of period t)
    discounted(t)        = CF(t) / (1 + r) ** t
    NPV                  = sum of discounted(t)
    IRR                  = the r at which NPV = 0, found by bisection between -99% and 1,000%;
                           "n/a (no sign change)" when the net cashflows never change sign
    ROI (undiscounted)   = (sum of benefits - sum of costs) / sum of costs, where "costs" is
                           the gross cost column or, with a cashflow column only, the NET OUTLAY
                           (sum of the negative net periods). Net run costs into the benefit
                           years the same way for every option or the ROIs are not comparable.
    payback (undiscounted) = point at which the running cumulative CF reaches 0 after its LAST
                           dip below 0, interpolated inside that period (consecutive periods
                           only; a skipped period counts as zero); "not reached" when the
                           cumulative ends negative; "n/a (no outlay)" when nothing was spent
    discounted payback   = the same rule on the running cumulative of discounted(t)
    sensitivity          = NPV at each rate of START:STOP:STEP plus the rate at which NPV turns
                           negative (bisection between the two bracketing rates)
    stress               = benefits x --benefit-factor and costs x --cost-factor (0.8 / 1.2 by
                           default with --stress), shown beside the base case
    break-even           = the benefit shortfall and the cost overrun at which NPV = 0 (bisection
                           on the factor) and the discount rate at which it does (= the IRR)
    whole-life cost      = sum of costs over the appraisal period, undiscounted

EXIT CODES   0 appraised  ·  2 bad input or usage (message "error: ..." on stderr, never a traceback)

EXAMPLES
    python .claude/skills/business-case/scripts/roi_npv.py .claude/skills/business-case/assets/cashflows.csv --rate 0.10
    python .claude/skills/business-case/scripts/roi_npv.py .claude/skills/business-case/assets/cashflows.csv --all --sensitivity 0.05:0.20:0.025
    python .claude/skills/business-case/scripts/roi_npv.py .claude/skills/business-case/assets/cashflows-options-sample.csv --all --format md
    python .claude/skills/business-case/scripts/roi_npv.py cashflows.json --json --irr --discounted-payback --format json
    cat cashflows.csv | python .claude/skills/business-case/scripts/roi_npv.py - --rate 8% --stress
    python .claude/skills/business-case/scripts/roi_npv.py by-year.csv --start-year 2026 --break-even
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import sys
import unicodedata

BOM = "﻿"
JSON_KEY = "cashflows"
DEFAULT_RATE = "0.10"
MAX_PERIOD = 1000
CALENDAR_YEAR_MIN, CALENDAR_YEAR_MAX = 1900, 2200
STRESS_BENEFIT, STRESS_COST = 0.8, 1.2
MAX_FACTOR = 10.0
IRR_LO, IRR_HI = -0.99, 10.0
BISECT_ITER, BISECT_TOL = 200, 1e-10
MAX_SWEEP_POINTS = 1000
DEFAULT_OPTION = "Investment"
NOTE_WIDTH = 60

PERIOD_ALIASES = ("period", "t", "year", "yr", "periodindex", "periodno")
CASHFLOW_ALIASES = ("cashflow", "cf", "net", "netcashflow", "netcash", "netflow", "value", "amount")
BENEFIT_ALIASES = ("benefit", "benefits", "inflow", "inflows", "cashin", "saving", "savings", "revenue")
COST_ALIASES = ("cost", "costs", "outflow", "outflows", "cashout", "spend")
OPTION_ALIASES = ("option", "scenario", "case", "alternative", "variant")
NOTE_ALIASES = ("note", "notes", "description", "desc", "item", "comment", "label")

UNIT_SUFFIX_RE = re.compile(r"\s*\([^()]*\)\s*$")
SEPARATORS_RE = re.compile(r"[\s_\-]+")
ACCOUNTING_NEG_RE = re.compile(r"^\((.*)\)$")


# --------------------------------------------------------------------------- input helpers
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
            key = next((k for k in data if str(k).strip().lower() == json_key), None)
            if key is None:
                keys = {canon(k) for k in data}
                if any(a in keys for a in PERIOD_ALIASES):
                    data = [data]  # a single cashflow object
                else:
                    raise ValueError(f"JSON object must contain a '{json_key}' list; found keys: {sorted(data)}")
            else:
                data = data[key]
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


def canon(header):
    """Canonical header name: BOM, whitespace, '-', '_' and a trailing '(unit)' removed, lower-cased."""
    base = UNIT_SUFFIX_RE.sub("", str(header).lstrip(BOM).strip()).strip().lower()
    return SEPARATORS_RE.sub("", base)


def _get(row, *names, default=None):
    """Case-insensitive lookup across accepted column aliases (row keys already canonical)."""
    for n in names:
        v = row.get(n)
        if v not in (None, ""):
            return v
    return default


def _num(raw, where, minimum=None, maximum=None, integer=False):
    """Parse a number tolerant of '$', ',', '€', '£', whitespace, '(1,000)' accounting negatives and a
    trailing '%' (which is stripped, value unchanged)."""
    if isinstance(raw, bool):
        raise ValueError(f"{where}: {raw!r} is a boolean, not a number")
    s = str(raw).strip()
    if s.endswith("%"):
        s = s[:-1]
    s = s.replace(",", "").replace("$", "").replace("€", "").replace("£", "").strip()
    m = ACCOUNTING_NEG_RE.match(s)
    if m:
        s = "-" + m.group(1).strip()
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


def warn(msg):
    print(f"warning: {msg}", file=sys.stderr)


def note(msg):
    print(f"note: {msg}", file=sys.stderr)


# --------------------------------------------------------------------------- formatting
def _clean(x):
    return 0.0 if abs(x) < 5e-7 else x  # print 0.00, never -0.00


def money(x):
    if x is None:
        return "n/a"
    if math.isinf(x):
        return "inf" if x > 0 else "-inf"
    return f"{_clean(round(x, 2)):,.2f}"


def pct(x):
    return f"{_clean(round(x * 100.0, 4)):.2f}%"


def trim(x):
    return f"{x:.4f}".rstrip("0").rstrip(".") or "0"


def display_width(s):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def pad(s, width, right=False):
    gap = max(0, width - display_width(s))
    return (" " * gap + s) if right else (s + " " * gap)


def truncate(s, limit):
    if display_width(s) <= limit:
        return s
    out, w = "", 0
    for c in s:
        cw = display_width(c)
        if w + cw > limit - 1:
            break
        out += c
        w += cw
    return out + "…"


def sanitize(value):
    return " ".join(str(value).split()) if value is not None else ""


def text_table(cols, rows, indent=""):
    """cols = [(name, right_aligned)], rows = list of list of str. Returns aligned lines."""
    widths = [display_width(name) for name, _ in cols]
    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], display_width(cell))
    lines = [indent + "  ".join(pad(name, widths[i], right) for i, (name, right) in enumerate(cols)).rstrip(),
             indent + "  ".join("-" * w for w in widths)]
    for r in rows:
        lines.append(indent + "  ".join(pad(cell, widths[i], cols[i][1]) for i, cell in enumerate(r)).rstrip())
    return lines


def md_table(cols, rows):
    out = ["| " + " | ".join(name for name, _ in cols) + " |",
           "|" + "|".join(("---:" if right else "---") for _, right in cols) + "|"]
    for r in rows:
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
    return out


# --------------------------------------------------------------------------- parsing
def parse_flows(rows, headers, start_year):
    """Group, validate, rebase, net and gap-fill the rows. Returns (options, mode, has_option)
    where options = [{"name", "flows": [{"period", "year", "benefit", "cost", "note"}]}] in file order."""
    found = [h for h in headers if h]
    present = {canon(h) for h in found}
    if not any(a in present for a in PERIOD_ALIASES):
        raise ValueError(f"missing column(s): ['period']; found headers: {found}; accepted names: period, t, year, yr")
    has_cf = any(a in present for a in CASHFLOW_ALIASES)
    has_gross = any(a in present for a in BENEFIT_ALIASES + COST_ALIASES)
    if not (has_cf or has_gross):
        raise ValueError(
            f"missing column(s): ['cashflow'] (or benefit and cost); found headers: {found}; "
            "accepted names: cashflow, cf, net, amount - or benefit / cost as positive magnitudes"
        )
    mode = "net" if has_cf else "gross"
    if has_cf and has_gross:
        warn("both a cashflow column and benefit/cost columns found; using cashflow and ignoring benefit/cost")
    has_option = any(a in present for a in OPTION_ALIASES)

    entries = []
    for i, row in enumerate(rows, 1):
        norm = {canon(k): v for k, v in row.items() if k is not None and canon(k)}
        option = sanitize(_get(norm, *OPTION_ALIASES, default="")) if has_option else DEFAULT_OPTION
        if not option:
            raise ValueError(f"row {i}: option is empty; every row needs an option name when an option column is present")
        tag = f"row {i} ({option})" if has_option else f"row {i}"
        period_raw = _get(norm, *PERIOD_ALIASES)
        if period_raw is None:
            raise ValueError(f"{tag}, column period: value is empty")
        period = int(_num(period_raw, f"{tag}, column period", minimum=0, integer=True))
        if period > MAX_PERIOD and not (CALENDAR_YEAR_MIN <= period <= CALENDAR_YEAR_MAX):
            raise ValueError(f"{tag}, column period: {period} is implausible (max {MAX_PERIOD} periods, "
                             f"or a calendar year {CALENDAR_YEAR_MIN}-{CALENDAR_YEAR_MAX} with --start-year)")
        if mode == "net":
            cf_raw = _get(norm, *CASHFLOW_ALIASES)
            if cf_raw is None:
                raise ValueError(f"{tag}, column cashflow: value is empty")
            net = _num(cf_raw, f"{tag}, column cashflow")
            benefit, cost = (net, 0.0) if net >= 0 else (0.0, -net)
        else:
            b_raw = _get(norm, *BENEFIT_ALIASES)
            c_raw = _get(norm, *COST_ALIASES)
            if b_raw is None and c_raw is None:
                raise ValueError(f"{tag}: both benefit and cost are empty; enter at least one (0 is allowed)")
            benefit = _magnitude(b_raw, f"{tag}, column benefit") if b_raw is not None else 0.0
            cost = _magnitude(c_raw, f"{tag}, column cost") if c_raw is not None else 0.0
        entries.append({
            "row": i, "tag": tag, "option": option, "period": period, "raw_period": period,
            "benefit": benefit, "cost": cost, "note": sanitize(_get(norm, *NOTE_ALIASES, default="")),
        })

    # calendar years vs period indexes
    lo = min(e["period"] for e in entries)
    looks_year = [e["period"] >= CALENDAR_YEAR_MIN for e in entries]
    if start_year is None and lo >= CALENDAR_YEAR_MIN:
        raise ValueError(
            f"periods look like calendar years (first is {lo}); use a 0-based period index (0 = today) "
            f"or pass --start-year {lo} to rebase"
        )
    if any(looks_year) and not all(looks_year):
        raise ValueError("periods mix calendar years and period indexes; use one or the other")
    if start_year is not None and all(looks_year):
        for e in entries:
            e["period"] = e["raw_period"] - start_year
            if e["period"] < 0:
                raise ValueError(f"{e['tag']}, column period: {e['raw_period']} is before --start-year {start_year}")
    for e in entries:
        if e["period"] > MAX_PERIOD:
            raise ValueError(f"{e['tag']}, column period: {e['raw_period']} is implausible "
                             f"(max {MAX_PERIOD} periods after rebasing on --start-year {start_year})")

    # net duplicate periods per option, then fill gaps with zero flows
    options, order = {}, []
    for e in entries:
        bucket = options.setdefault(e["option"], {})
        if e["option"] not in order:
            order.append(e["option"])
        cell = bucket.setdefault(e["period"], {"benefit": 0.0, "cost": 0.0, "notes": [], "rows": 0})
        cell["benefit"] += e["benefit"]
        cell["cost"] += e["cost"]
        cell["rows"] += 1
        if e["note"]:
            cell["notes"].append(e["note"])
    result = []
    for name in order:
        bucket = options[name]
        label = f"option {name!r}" if has_option else "cashflows"
        n_rows = sum(c["rows"] for c in bucket.values())
        if n_rows > len(bucket):
            note(f"{label}: {n_rows} rows netted into {len(bucket)} periods (duplicate periods summed)")
        first, last = min(bucket), max(bucket)
        if first > 0 and start_year is None:
            warn(f"{label}: first period is {first}, not 0 - the up-front outlay is discounted by {first} "
                 f"period(s); use period 0 for today")
        missing = [p for p in range(first, last + 1) if p not in bucket]
        if missing:
            note(f"{label}: period(s) {missing} not listed; treated as zero cashflow")
        flows = []
        for p in range(first, last + 1):
            cell = bucket.get(p, {"benefit": 0.0, "cost": 0.0, "notes": []})
            benefit, cost = cell["benefit"], cell["cost"]
            if mode == "net":
                net = round(benefit - cost, 6)
                benefit, cost = (net, 0.0) if net >= 0 else (0.0, -net)
            flows.append({
                "period": p, "year": (start_year + p) if start_year is not None else None,
                "benefit": benefit, "cost": cost, "note": "; ".join(cell["notes"]),
            })
        result.append({"name": name, "flows": flows})
    return result, mode, has_option


def _magnitude(raw, where):
    v = _num(raw, where)
    if v < 0:
        raise ValueError(f"{where}: {raw!r} is negative; enter benefits and costs as positive magnitudes "
                         "(a cost belongs in the cost column, a benefit in the benefit column)")
    return v


# --------------------------------------------------------------------------- maths
def discount_factor(rate, t):
    """1 / (1 + rate) ** t, without raising on extreme rate/period combinations."""
    x = -t * math.log1p(rate)
    if x > 700:
        return float("inf")
    return math.exp(x)


def npv_at(flows, rate, bf=1.0, cf=1.0):
    total = 0.0
    for f in flows:
        net = f["benefit"] * bf - f["cost"] * cf
        if net != 0.0:
            total += net * discount_factor(rate, f["period"])
    return total


def payback_of(seq, total_cost):
    """seq = [(period, value)] over consecutive periods. Returns {"value", "status", "crossings", "final"}."""
    cum, result, crossings, was_negative = 0.0, None, 0, False
    for t, v in seq:
        prev = cum
        cum = round(cum + v, 6)
        if prev < 0 and cum >= 0:
            crossings += 1
            result = (t - 1) + (-prev / v)  # v > 0 here because the cumulative rose through zero
        elif cum < 0:
            was_negative = True
            result = None  # dipped below zero (again): the earlier crossing does not count
    if total_cost <= 0:
        return {"value": None, "status": "no outlay", "crossings": crossings, "final": cum}
    if cum < 0:
        return {"value": None, "status": "not reached", "crossings": crossings, "final": cum}
    if not was_negative:
        return {"value": 0.0, "status": "never negative", "crossings": crossings, "final": cum}
    return {"value": result, "status": "reached", "crossings": crossings, "final": cum}


def sign_changes(flows, bf=1.0, cf=1.0):
    signs = [math.copysign(1, f["benefit"] * bf - f["cost"] * cf) for f in flows
             if round(f["benefit"] * bf - f["cost"] * cf, 6) != 0.0]
    return sum(1 for a, b in zip(signs, signs[1:]) if a != b)


def bisect(func, lo, hi, iterations=BISECT_ITER, tol=BISECT_TOL):
    """Root of func between lo and hi (func(lo) and func(hi) must have opposite signs)."""
    f_lo = func(lo)
    for _ in range(iterations):
        mid = (lo + hi) / 2.0
        f_mid = func(mid)
        if f_mid == 0.0 or (hi - lo) / 2.0 < tol:
            return mid
        if (f_mid < 0) == (f_lo < 0):
            lo, f_lo = mid, f_mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def irr_of(flows, bf=1.0, cf=1.0):
    """Returns (irr or None, reason)."""
    changes = sign_changes(flows, bf, cf)
    if changes == 0:
        return None, "no sign change"
    func = lambda r: npv_at(flows, r, bf, cf)  # noqa: E731
    lo, hi = IRR_LO, IRR_HI
    f_lo, f_hi = func(lo), func(hi)
    if not (math.isfinite(f_lo) and math.isfinite(f_hi)):
        return None, "could not evaluate"
    if (f_lo < 0) == (f_hi < 0):
        grid = [lo + k * (hi - lo) / 400.0 for k in range(401)]
        values = [func(r) for r in grid]
        bracket = next(((grid[k], grid[k + 1]) for k in range(400)
                        if math.isfinite(values[k]) and math.isfinite(values[k + 1])
                        and (values[k] < 0) != (values[k + 1] < 0)), None)
        if bracket is None:
            return None, f"no root between {pct(IRR_LO)} and {pct(IRR_HI)}"
        lo, hi = bracket
    irr = bisect(func, lo, hi)
    reason = "" if changes == 1 else f"cashflows change sign {changes} times; the IRR may not be unique"
    return irr, reason


def evaluate(flows, rate, bf=1.0, cf=1.0):
    """Per-period rows and headline metrics for one option (optionally stressed by factors)."""
    rows, cum, dcum, tot_b, tot_c = [], 0.0, 0.0, 0.0, 0.0
    for f in flows:
        benefit, cost = f["benefit"] * bf, f["cost"] * cf
        net = benefit - cost
        disc = net * discount_factor(rate, f["period"]) if net != 0.0 else 0.0
        if not math.isfinite(disc):
            raise ValueError(f"discounting overflowed at period {f['period']} with rate {pct(rate)}; "
                             "check the periods and the rate")
        cum = round(cum + net, 6)
        dcum = round(dcum + disc, 6)
        tot_b += benefit
        tot_c += cost
        rows.append({
            "period": f["period"], "year": f["year"], "benefit": benefit, "cost": cost, "cashflow": net,
            "discounted": disc, "cumulative": cum, "discounted_cumulative": dcum, "note": f["note"],
        })
    npv = round(sum(r["discounted"] for r in rows), 6)
    tot_b, tot_c = round(tot_b, 6), round(tot_c, 6)
    return {
        "rows": rows,
        "npv": npv,
        "whole_life_cost": tot_c,
        "total_benefit": tot_b,
        "roi": ((tot_b - tot_c) / tot_c) if tot_c > 0 else None,
        "payback": payback_of([(r["period"], r["cashflow"]) for r in rows], tot_c),
        "discounted_payback": payback_of([(r["period"], r["discounted"]) for r in rows], tot_c),
        "irr": irr_of(flows, bf, cf),
        "first": rows[0]["period"], "last": rows[-1]["period"],
    }


def break_even(flows, rate, base):
    """Switching values: benefit shortfall and cost overrun at which NPV = 0, plus the rate (IRR)."""
    out = {"benefit_shortfall": None, "cost_overrun": None, "rate": base["irr"][0], "notes": {}}
    if base["npv"] < 0:
        out["notes"]["benefit_shortfall"] = out["notes"]["cost_overrun"] = "n/a (NPV already negative at base)"
        return out
    if base["total_benefit"] <= 0:
        out["notes"]["benefit_shortfall"] = "n/a (no benefits)"
    else:
        f = lambda b: npv_at(flows, rate, b, 1.0)  # noqa: E731
        if f(0.0) >= 0:
            out["notes"]["benefit_shortfall"] = "100% (NPV stays >= 0 with no benefits at all)"
        else:
            out["benefit_shortfall"] = 1.0 - bisect(f, 0.0, 1.0)
    if base["whole_life_cost"] <= 0:
        out["notes"]["cost_overrun"] = "n/a (no costs)"
    else:
        g = lambda c: npv_at(flows, rate, 1.0, c)  # noqa: E731
        if g(MAX_FACTOR) >= 0:
            out["notes"]["cost_overrun"] = f"more than {pct(MAX_FACTOR - 1)} (NPV still >= 0 at x{MAX_FACTOR:g} costs)"
        else:
            out["cost_overrun"] = bisect(g, 1.0, MAX_FACTOR) - 1.0
    return out


def sensitivity(options, rates):
    """NPV of every option at every rate, plus the switching rate at which NPV turns negative."""
    table = []
    for r in rates:
        table.append({"rate": r, "npv": {o["name"]: round(npv_at(o["flows"], r), 6) for o in options}})
    switching = {}
    for o in options:
        values = [row["npv"][o["name"]] for row in table]
        func = lambda r, fl=o["flows"]: npv_at(fl, r)  # noqa: E731
        found = None
        for k in range(len(rates) - 1):
            if values[k] >= 0 > values[k + 1]:
                found = ("negative above", bisect(func, rates[k], rates[k + 1]))
                break
            if values[k] < 0 <= values[k + 1]:
                found = ("positive above", bisect(func, rates[k], rates[k + 1]))
                break
        if found is None:
            if all(v >= 0 for v in values):
                found = ("stays >= 0", None)
            elif all(v < 0 for v in values):
                found = ("stays negative", None)
            else:
                found = ("changes sign", None)
        switching[o["name"]] = found
    return {"rates": rates, "table": table, "switching": switching}


# --------------------------------------------------------------------------- rendering
def unit_word(start_year):
    return "years" if start_year is not None else "periods"


def payback_text(pb, unit, start_year=None, rate=None):
    status, value = pb["status"], pb["value"]
    if status == "no outlay":
        return "n/a (no outlay to recover)"
    if status == "not reached":
        return f"not reached (cumulative ends at {money(pb['final'])})"
    if status == "never negative":
        return f"0.00 {unit} (cumulative never negative)"
    text = f"{value:.2f} {unit}"
    if start_year is not None:
        text += f" (reached in {start_year + math.ceil(value - 1e-9)})"
    if pb["crossings"] > 1:
        text += " - last crossing; the cumulative dipped below zero again after an earlier one"
    return text


def payback_cell(pb):
    if pb["status"] == "no outlay":
        return "n/a"
    if pb["status"] == "not reached":
        return "not reached"
    return f"{pb['value']:.2f}"


def irr_text(irr):
    value, reason = irr
    if value is None:
        return f"n/a ({reason})"
    return pct(value) + (f" ({reason})" if reason else "")


def irr_cell(irr):
    return pct(irr[0]) if irr[0] is not None else "n/a"


def roi_text(roi):
    return pct(roi) if roi is not None else "n/a (no outlay)"


def roi_label(mode):
    return "ROI (undiscounted, on gross cost)" if mode == "gross" else "ROI (undiscounted, on net outlay)"


def break_even_text(be):
    b, c, r = be["benefit_shortfall"], be["cost_overrun"], be["rate"]
    if b is None and c is None and r is None and be["notes"].get("benefit_shortfall", "").startswith("n/a"):
        return "n/a (" + "; ".join(n[len("n/a ("):-1] for n in
                                   (be["notes"]["benefit_shortfall"], be["notes"]["cost_overrun"])
                                   if n.startswith("n/a (")) + ")"
    parts = [f"benefits can fall {pct(b)}" if b is not None else f"benefits: {be['notes']['benefit_shortfall']}",
             f"costs can rise {pct(c)}" if c is not None else f"costs: {be['notes']['cost_overrun']}",
             f"discount rate up to {pct(r)} (the IRR)" if r is not None else "discount rate: n/a (no IRR)"]
    return " · ".join(parts) + " before NPV reaches 0"


def period_table_rows(rows, mode, start_year):
    cols = ([("Year", True)] if start_year is not None else []) + [("Period", True)]
    if mode == "gross":
        cols += [("Benefit", True), ("Cost", True)]
    cols += [("Cashflow", True), ("Discounted", True), ("Cumulative", True), ("Disc. cumulative", True), ("Note", False)]
    cells = []
    for r in rows:
        c = ([str(r["year"])] if start_year is not None else []) + [str(r["period"])]
        if mode == "gross":
            c += [money(r["benefit"]), money(r["cost"])]
        c += [money(r["cashflow"]), money(r["discounted"]), money(r["cumulative"]),
              money(r["discounted_cumulative"]), truncate(sanitize(r["note"]), NOTE_WIDTH)]
        cells.append(c)
    if not any(r["note"] for r in rows):
        cols, cells = cols[:-1], [c[:-1] for c in cells]
    return cols, cells


def summary_lines(opt, ctx):
    """Headline lines for one option (opt = evaluated option dict)."""
    rate, unit, start_year, mode = ctx["rate"], ctx["unit"], ctx["start_year"], ctx["mode"]
    res = opt["base"]
    span = (f"years {start_year + res['first']}-{start_year + res['last']}" if start_year is not None
            else f"periods {res['first']}-{res['last']}")
    head = f"Option: {opt['name']}" if ctx["has_option"] else "Cashflows"
    lines = [f"{head} ({span}, {len(res['rows'])} {unit})",
             f"  Whole-life cost (undiscounted): {money(res['whole_life_cost'])}   "
             f"Total benefit (undiscounted): {money(res['total_benefit'])}",
             f"  NPV @ {pct(rate)}: {money(res['npv'])}"]
    if ctx["irr"]:
        lines.append(f"  IRR: {irr_text(res['irr'])}")
    lines.append(f"  {roi_label(mode)}: {roi_text(res['roi'])}")
    lines.append(f"  Payback (undiscounted): {payback_text(res['payback'], unit, start_year)}")
    if ctx["discounted_payback"]:
        lines.append(f"  Payback (discounted @ {pct(rate)}): {payback_text(res['discounted_payback'], unit, start_year)}")
    if opt.get("break_even") is not None:
        lines.append(f"  Break-even (switching values): {break_even_text(opt['break_even'])}")
    if opt.get("stressed") is not None:
        bf, cf = ctx["benefit_factor"], ctx["cost_factor"]
        if ctx["multi"] and not ctx["detail"]:
            s = opt["stressed"]
            verdict = "still positive" if s["npv"] >= 0 else "turns negative"
            lines.append(f"  Stressed (benefits x{bf:.2f}, costs x{cf:.2f}): NPV {money(s['npv'])} ({verdict}), "
                         f"payback {payback_cell(s['payback'])}; pass --detail for the full base-vs-stressed table")
        else:
            lines.append(f"  Stress test (benefits x{bf:.2f}, costs x{cf:.2f}):")
            lines += stress_table_lines(res, opt["stressed"], ctx, indent="    ")
    return lines


def stress_rows(base, stressed, ctx):
    rate, unit = ctx["rate"], ctx["unit"]
    rows = [["Whole-life cost", money(base["whole_life_cost"]), money(stressed["whole_life_cost"])],
            ["Total benefit", money(base["total_benefit"]), money(stressed["total_benefit"])],
            [f"NPV @ {pct(rate)}", money(base["npv"]), money(stressed["npv"])]]
    if ctx["irr"]:
        rows.append(["IRR", irr_cell(base["irr"]), irr_cell(stressed["irr"])])
    rows.append([roi_label(ctx["mode"]), roi_text(base["roi"]), roi_text(stressed["roi"])])
    rows.append([f"Payback ({unit})", payback_cell(base["payback"]), payback_cell(stressed["payback"])])
    if ctx["discounted_payback"]:
        rows.append([f"Discounted payback ({unit})", payback_cell(base["discounted_payback"]),
                     payback_cell(stressed["discounted_payback"])])
    rows.append(["Still positive?", "yes" if base["npv"] >= 0 else "no", "yes" if stressed["npv"] >= 0 else "no"])
    return rows


def stress_cols(ctx):
    return [("Metric", False), ("Base", True), (f"Stressed (b x{ctx['benefit_factor']:.2f}, c x{ctx['cost_factor']:.2f})", True)]


def stress_table_lines(base, stressed, ctx, indent=""):
    return text_table(stress_cols(ctx), stress_rows(base, stressed, ctx), indent=indent)


def comparison_cols(ctx):
    unit = ctx["unit"]
    cols = [("Rank", True), ("Option", False), ("Whole-life cost", True), ("Total benefit", True),
            (f"NPV @ {pct(ctx['rate'])}", True)]
    if ctx["irr"]:
        cols.append(("IRR", True))
    cols.append(("ROI (undiscounted)", True))
    cols.append((f"Payback (undiscounted, {unit})", True))
    if ctx["discounted_payback"]:
        cols.append((f"Discounted payback ({unit})", True))
    if ctx["stress"]:
        cols.append((f"NPV stressed (b x{ctx['benefit_factor']:.2f}, c x{ctx['cost_factor']:.2f})", True))
    return cols


def comparison_rows(ranked, ctx):
    rows = []
    for rank, opt in enumerate(ranked, 1):
        res = opt["base"]
        c = [str(rank), opt["name"], money(res["whole_life_cost"]), money(res["total_benefit"]), money(res["npv"])]
        if ctx["irr"]:
            c.append(irr_cell(res["irr"]))
        c.append(roi_text(res["roi"]) if res["roi"] is not None else "n/a")
        c.append(payback_cell(res["payback"]))
        if ctx["discounted_payback"]:
            c.append(payback_cell(res["discounted_payback"]))
        if ctx["stress"]:
            c.append(money(opt["stressed"]["npv"]))
        rows.append(c)
    return rows


def ranking_lines(ranked, ctx):
    best = ranked[0]
    lines = [f"Best on NPV @ {pct(ctx['rate'])}: {best['name']} ({money(best['base']['npv'])})"]
    with_roi = [o for o in ranked if o["base"]["roi"] is not None]
    if with_roi:
        top = max(with_roi, key=lambda o: o["base"]["roi"])
        if top["name"] != best["name"]:
            lines.append(f"Best on ROI: {top['name']} ({pct(top['base']['roi'])}) - a higher ROI on a smaller outlay; "
                         "rank options on NPV, not ROI")
    if ctx["stress"]:
        flipped = [o["name"] for o in ranked if o["base"]["npv"] >= 0 > o["stressed"]["npv"]]
        if flipped:
            lines.append(f"Turns negative under stress: {', '.join(flipped)}")
    return lines


def sensitivity_cols(options, ctx):
    return [("Rate", True)] + [(f"NPV {o['name']}" if len(options) > 1 else "NPV", True) for o in options]


def sensitivity_rows(sens, options):
    return [[pct(row["rate"])] + [money(row["npv"][o["name"]]) for o in options] for row in sens["table"]]


def switching_lines(sens, options):
    parts = []
    for o in options:
        kind, value = sens["switching"][o["name"]]
        label = f" ({o['name']})" if len(options) > 1 else ""
        if kind in ("negative above", "positive above"):
            parts.append(f"NPV turns {kind} {pct(value)}{label}")
        elif kind == "stays >= 0":
            parts.append(f"NPV stays >= 0 across the range{label}")
        elif kind == "stays negative":
            parts.append(f"NPV is negative across the whole range{label}")
        else:
            parts.append(f"NPV changes sign more than once across the range{label}")
    return parts


def render_table(ctx, options, ranked, sens):
    out = []
    multi = len(options) > 1
    if multi:
        out.append(f"Options compared: {len(options)}, ranked by NPV @ {pct(ctx['rate'])} "
                   f"(cashflows are incremental to do-nothing; discount rate per {ctx['unit'][:-1]})")
        out += text_table(comparison_cols(ctx), comparison_rows(ranked, ctx))
        out += ranking_lines(ranked, ctx)
        out.append("")
    for opt in ranked:
        if not multi or ctx["detail"]:
            cols, cells = period_table_rows(opt["base"]["rows"], ctx["mode"], ctx["start_year"])
            if multi:
                out.append(f"Option: {opt['name']} - per-period detail")
            out += text_table(cols, cells)
            out.append("")
        out += summary_lines(opt, ctx)
        out.append("")
    if sens is not None:
        rates = sens["rates"]
        out.append(f"Sensitivity of NPV to the discount rate ({pct(rates[0])} to {pct(rates[-1])}, {len(rates)} rates)")
        out += text_table(sensitivity_cols(options, ctx), sensitivity_rows(sens, options))
        out += switching_lines(sens, options)
        out.append("")
    out.append(f"Discount rate: {pct(ctx['rate'])} per {ctx['unit'][:-1]}; period 0 = today (undiscounted); "
               "ROI and simple payback are undiscounted.")
    return "\n".join(out).rstrip()


def render_md(ctx, options, ranked, sens):
    out = [f"**Financial appraisal** - discount rate {pct(ctx['rate'])} per {ctx['unit'][:-1]}; "
           "NPV discounted, ROI and simple payback undiscounted; cashflows incremental to do-nothing.", ""]
    out += md_table(comparison_cols(ctx), comparison_rows(ranked, ctx))
    if len(options) > 1:
        out.append("")
        out += [f"- {ln}" for ln in ranking_lines(ranked, ctx)]
    for opt in ranked:
        out.append("")
        res = opt["base"]
        out.append(f"**{opt['name']}**")
        out.append("")
        lines = summary_lines(opt, ctx)[1:]
        for ln in lines:
            if ln.startswith("  Stress test"):
                break
            out.append(f"- {ln.strip()}")
        if opt.get("stressed") is not None and (len(options) == 1 or ctx["detail"]):
            out.append("")
            out += md_table(stress_cols(ctx), stress_rows(res, opt["stressed"], ctx))
        if len(options) == 1 or ctx["detail"]:
            cols, cells = period_table_rows(res["rows"], ctx["mode"], ctx["start_year"])
            out.append("")
            out += md_table(cols, cells)
    if sens is not None:
        out.append("")
        out.append(f"**Sensitivity of NPV to the discount rate** ({pct(sens['rates'][0])} to {pct(sens['rates'][-1])})")
        out.append("")
        out += md_table(sensitivity_cols(options, ctx), sensitivity_rows(sens, options))
        out.append("")
        out += [f"- {ln}" for ln in switching_lines(sens, options)]
    return "\n".join(out)


def _pb_json(pb):
    return {"value": None if pb["value"] is None else round(pb["value"], 4), "status": pb["status"],
            "crossings": pb["crossings"], "cumulative_end": round(pb["final"], 2)}


def _metrics_json(res):
    return {
        "whole_life_cost": round(res["whole_life_cost"], 2),
        "total_benefit": round(res["total_benefit"], 2),
        "npv": round(res["npv"], 2),
        "irr": None if res["irr"][0] is None else round(res["irr"][0], 6),
        "irr_note": res["irr"][1] or None,
        "roi": None if res["roi"] is None else round(res["roi"], 6),
        "payback": _pb_json(res["payback"]),
        "discounted_payback": _pb_json(res["discounted_payback"]),
    }


def render_json(ctx, options, ranked, sens):
    rows = []
    for opt in options:
        for r in opt["base"]["rows"]:
            rows.append({"option": opt["name"], "period": r["period"], "year": r["year"],
                         "benefit": round(r["benefit"], 2), "cost": round(r["cost"], 2),
                         "cashflow": round(r["cashflow"], 2), "discounted": round(r["discounted"], 2),
                         "cumulative": round(r["cumulative"], 2),
                         "discounted_cumulative": round(r["discounted_cumulative"], 2), "note": r["note"]})
    summary = {
        "discount_rate": ctx["rate"], "start_year": ctx["start_year"], "unit": ctx["unit"],
        "cashflow_mode": ctx["mode"], "roi_basis": "gross cost" if ctx["mode"] == "gross" else "net outlay",
        "ranking": [o["name"] for o in ranked], "best_on_npv": ranked[0]["name"],
        "stress_factors": ({"benefit_factor": ctx["benefit_factor"], "cost_factor": ctx["cost_factor"]}
                           if ctx["stress"] else None),
        "options": [],
    }
    for rank, opt in enumerate(ranked, 1):
        entry = {"option": opt["name"], "rank": rank, "first_period": opt["base"]["first"],
                 "last_period": opt["base"]["last"], **_metrics_json(opt["base"])}
        if opt.get("stressed") is not None:
            entry["stressed"] = _metrics_json(opt["stressed"])
        if opt.get("break_even") is not None:
            be = opt["break_even"]
            entry["break_even"] = {
                "benefit_shortfall": None if be["benefit_shortfall"] is None else round(be["benefit_shortfall"], 6),
                "cost_overrun": None if be["cost_overrun"] is None else round(be["cost_overrun"], 6),
                "discount_rate": None if be["rate"] is None else round(be["rate"], 6),
                "notes": be["notes"],
            }
        summary["options"].append(entry)
    if sens is not None:
        summary["sensitivity"] = {
            "rates": [round(r, 6) for r in sens["rates"]],
            "npv": [{"rate": round(row["rate"], 6), **{k: round(v, 2) for k, v in row["npv"].items()}}
                    for row in sens["table"]],
            "switching": {name: {"kind": kind, "rate": None if value is None else round(value, 6)}
                          for name, (kind, value) in sens["switching"].items()},
        }
    return json.dumps({"rows": rows, "summary": summary}, indent=2, ensure_ascii=False)


def render_csv(ctx, options):
    fieldnames = ["option", "period", "year", "benefit", "cost", "cashflow", "discounted", "cumulative",
                  "discounted_cumulative", "note"]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for opt in options:
        for r in opt["base"]["rows"]:
            writer.writerow({
                "option": opt["name"], "period": r["period"], "year": "" if r["year"] is None else r["year"],
                "benefit": f"{r['benefit']:.2f}", "cost": f"{r['cost']:.2f}", "cashflow": f"{r['cashflow']:.2f}",
                "discounted": f"{_clean(r['discounted']):.2f}", "cumulative": f"{_clean(r['cumulative']):.2f}",
                "discounted_cumulative": f"{_clean(r['discounted_cumulative']):.2f}", "note": r["note"],
            })
    return buf.getvalue().rstrip("\n")


# --------------------------------------------------------------------------- CLI
def build_parser():
    parser = argparse.ArgumentParser(
        prog="roi_npv.py",
        description="Appraise investment cashflows: NPV, IRR, ROI, simple and discounted payback, sensitivity, "
                    "stress factors, break-even values and a per-option comparison.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("path", help="CSV or JSON cashflows, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="parse the input as JSON (default: CSV, delimiter auto-detected)")
    parser.add_argument("--rate", default=DEFAULT_RATE, metavar="R",
                        help="discount rate per period as a fraction (0.10) or a percent ('10%%'); default 0.10")
    parser.add_argument("--start-year", type=int, default=None, metavar="YYYY",
                        help="calendar year of period 0: rebases rows written as calendar years and labels every "
                             "row with its year (payback is then reported in years)")
    parser.add_argument("--irr", action="store_true", help="also report the internal rate of return")
    parser.add_argument("--discounted-payback", action="store_true",
                        help="also report the payback on the discounted cumulative")
    parser.add_argument("--break-even", action="store_true",
                        help="report the switching values: benefit shortfall, cost overrun and discount rate at "
                             "which NPV = 0")
    parser.add_argument("--all", action="store_true", help="shorthand for --irr --discounted-payback --break-even")
    parser.add_argument("--sensitivity", metavar="START:STOP:STEP",
                        help="NPV at each discount rate of the sweep, e.g. 0.05:0.15:0.01 or 5%%:15%%:1%%, "
                             "with the rate at which NPV turns negative")
    parser.add_argument("--benefit-factor", metavar="F",
                        help="stress: multiply every benefit by F (0.8 or '80%%' = a 20%% shortfall)")
    parser.add_argument("--cost-factor", metavar="F", help="stress: multiply every cost by F (1.2 or '120%%' = a 20%% overrun)")
    parser.add_argument("--stress", action="store_true",
                        help=f"stress with the default factors (benefits x{STRESS_BENEFIT}, costs x{STRESS_COST}) "
                             "unless --benefit-factor / --cost-factor override them")
    parser.add_argument("--detail", action="store_true",
                        help="print the per-period table of every option when several are compared "
                             "(always printed for a single option)")
    parser.add_argument("--format", choices=["table", "json", "csv", "md"], default="table",
                        help="output format: aligned text (default), JSON (rows + summary), CSV of the per-period "
                             "rows (summary on stderr), or Markdown tables ready for the business-case template")
    return parser


def parse_fraction(raw, name, parser, kind="rate"):
    s = str(raw).strip()
    try:
        v = _num(s, name)
    except ValueError as exc:
        parser.error(str(exc))
    if s.endswith("%"):
        v /= 100.0
    if kind == "rate":
        if v >= 1.0:
            parser.error(f"{name} {s} looks like a percentage; pass a fraction per period such as {trim(v / 100)} "
                         f"or write {trim(v)}%")
        if v <= -1.0:
            parser.error(f"{name} must be greater than -100% (got {s})")
    else:  # factor
        if v <= 0:
            parser.error(f"{name} must be greater than 0 (got {s}); 0.8 or '80%' means benefits cut by 20%")
        if v > MAX_FACTOR:
            parser.error(f"{name} {s} is above the maximum x{MAX_FACTOR:g}")
    return v


def parse_sweep(raw, parser):
    parts = str(raw).split(":")
    if len(parts) != 3:
        parser.error(f"--sensitivity must be START:STOP:STEP (got {raw!r}), e.g. 0.05:0.15:0.01 or 5%:15%:1%")
    start = parse_fraction(parts[0], "--sensitivity START", parser)
    stop = parse_fraction(parts[1], "--sensitivity STOP", parser)
    try:
        step = _num(parts[2], "--sensitivity STEP")
    except ValueError as exc:
        parser.error(str(exc))
    if parts[2].strip().endswith("%"):
        step /= 100.0
    if step <= 0:
        parser.error(f"--sensitivity STEP must be greater than 0 (got {parts[2]})")
    if stop <= start:
        parser.error(f"--sensitivity STOP must be greater than START (got {parts[0]}:{parts[1]})")
    count = int(math.floor((stop - start) / step + 1e-9)) + 1
    if count > MAX_SWEEP_POINTS:
        parser.error(f"--sensitivity would evaluate {count} rates (max {MAX_SWEEP_POINTS}); use a larger STEP")
    return [round(start + k * step, 12) for k in range(count)]


def validate_options(parser, args):
    ctx = {
        "rate": parse_fraction(args.rate, "--rate", parser),
        "start_year": args.start_year,
        "irr": args.irr or args.all,
        "discounted_payback": args.discounted_payback or args.all,
        "break_even": args.break_even or args.all,
        "detail": args.detail,
        "format": args.format,
    }
    if args.start_year is not None and not (CALENDAR_YEAR_MIN <= args.start_year <= CALENDAR_YEAR_MAX):
        parser.error(f"--start-year must be a calendar year between {CALENDAR_YEAR_MIN} and {CALENDAR_YEAR_MAX} "
                     f"(got {args.start_year})")
    ctx["sweep"] = parse_sweep(args.sensitivity, parser) if args.sensitivity else None
    bf = parse_fraction(args.benefit_factor, "--benefit-factor", parser, kind="factor") if args.benefit_factor else None
    cf = parse_fraction(args.cost_factor, "--cost-factor", parser, kind="factor") if args.cost_factor else None
    ctx["stress"] = args.stress or bf is not None or cf is not None
    if ctx["stress"]:
        ctx["benefit_factor"] = bf if bf is not None else (STRESS_BENEFIT if args.stress else 1.0)
        ctx["cost_factor"] = cf if cf is not None else (STRESS_COST if args.stress else 1.0)
        if ctx["benefit_factor"] > 1.0 or ctx["cost_factor"] < 1.0:
            note(f"benefit factor {ctx['benefit_factor']:.2f} / cost factor {ctx['cost_factor']:.2f} is an upside "
                 "case, not a stress")
    else:
        ctx["benefit_factor"] = ctx["cost_factor"] = 1.0
    ctx["unit"] = unit_word(ctx["start_year"])
    return ctx


def appraise(parsed, ctx):
    """Evaluate every option (base, stressed, break-even) and rank by NPV."""
    options = []
    for o in parsed:
        base = evaluate(o["flows"], ctx["rate"])
        entry = {"name": o["name"], "flows": o["flows"], "base": base, "stressed": None, "break_even": None}
        if ctx["stress"]:
            entry["stressed"] = evaluate(o["flows"], ctx["rate"], ctx["benefit_factor"], ctx["cost_factor"])
        if ctx["break_even"]:
            entry["break_even"] = break_even(o["flows"], ctx["rate"], base)
        options.append(entry)
    ranked = sorted(options, key=lambda e: -e["base"]["npv"])  # stable: ties keep file order
    sens = sensitivity(options, ctx["sweep"]) if ctx["sweep"] else None
    return options, ranked, sens


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    ctx = validate_options(parser, args)
    try:
        text = read_text(args.path)
        rows, headers = load_rows(text, args.json, JSON_KEY)
        parsed, mode, has_option = parse_flows(rows, headers, ctx["start_year"])
        ctx["mode"], ctx["has_option"], ctx["multi"] = mode, has_option, len(parsed) > 1
        options, ranked, sens = appraise(parsed, ctx)
        if ctx["format"] == "json":
            output = render_json(ctx, options, ranked, sens)
        elif ctx["format"] == "csv":
            output = render_csv(ctx, options)
            for opt in ranked:
                for ln in summary_lines(opt, ctx):
                    print(ln, file=sys.stderr)
        elif ctx["format"] == "md":
            output = render_md(ctx, options, ranked, sens)
        else:
            output = render_table(ctx, options, ranked, sens)
    except (OSError, ValueError, TypeError, UnicodeDecodeError, OverflowError, ZeroDivisionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
