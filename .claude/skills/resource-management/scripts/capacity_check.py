#!/usr/bin/env python3
"""Resource capacity check: utilization per person and per period, OVER / HIGH / OK / UNDER
flags on each person's peak period, headroom to a healthy target, a team view per period,
where each overload comes from, key-person risks and, with --level, a greedy reassignment
plan plus the residual the team cannot absorb. Standard library only.

ONE ROW = ONE ASSIGNMENT: a person's allocated work in a period (optionally for a project),
next to their capacity in that period. Rows are AGGREGATED per person, and per person and
period when a period column exists: allocated is summed; capacity is per person and period,
so it must agree across that person's rows in the same period (a blank capacity on extra
rows inherits it). A per-assignment export (one row per person, project and week) is checked
correctly. Names and periods are matched case-insensitively with whitespace collapsed.

INPUT COLUMNS / KEYS  (case-insensitive; extra columns are ignored)
  person     who                                   aliases: name, resource, member, employee  (required)
  capacity   what they can do in the period        aliases: cap, availability                 (required, >= 0)
  allocated  work assigned to them in the period   aliases: allocation, alloc, assigned, demand, load
                                                                                               (required, >= 0)
  role       primary role                          aliases: position, job_role                (optional)
  skills     other roles they can cover, separated by / ; or |   aliases: can_cover, covers, backup_for
  period     week, sprint or month (W6, Sprint 3, 2026-11)       aliases: week, sprint, month, iteration
  project    project or work package of the row    aliases: assignment, task, work_package, workstream
  unit       hours | days | percent | fte          aliases: units, uom                        (optional)
  capacity and allocated must be in ONE unit for the whole file (hours per week, days per
  sprint, percent of a full-time week, or FTE). Rows that mix units are refused: a unit
  column with two values, a '%' on some rows but not others, or a '%' on only one of a
  row's two numbers. A capacity of 0 is a leave period: OFF when nothing is allocated, OVER
  when work is. '$', EUR/GBP signs and a trailing '%' are stripped; ',' is a thousands separator
  before groups of three digits ("1,000" -> 1000) and a decimal comma before one or two digits
  ("37,5" -> 37.5); any other comma ("1.000,50") is rejected as ambiguous.
  With a period column every row needs a period. Periods keep their input order (W6 before
  W10). CSV delimiter is auto-detected (, ; tab |); a UTF-8 BOM and CRLF line ends are
  tolerated. JSON is a list of objects or {"resources": [...]}; pass --json (a .json file
  is detected by its extension; any other JSON text without --json is refused, never
  misread as CSV).

FORMULAS  (per person and period, after aggregation)
  utilization = allocated / capacity x 100           (shown to 0.1%, rounded half up)
  flag        = OVER  if utilization >  --threshold  (default 100: the plan is not deliverable)
                HIGH  if utilization >= --high       (default 90: no slack for the unexpected)
                UNDER if utilization <  --under      (default 50: spare capacity, or a part-timer)
                OK    otherwise                      (flags use the displayed, rounded value)
  headroom    = capacity x --target / 100 - allocated   (default target 80; negative = above it)
  FTE load    = sum of allocated / capacity over people  (unit-safe: "the work of N full-timers")
  A person's flag is the flag of their PEAK period (highest utilization; earliest on a tie),
  never an average: a team or quarter average hides a one-week overload.
  Key-person risk: an OVER person whose role nobody else holds as their role (backups who
  list the role under skills are named) -> log it in the risk register.

LEVELING  (--level; a proposal for the PM to confirm, not a decision)
  Within each period: every OVER person is brought down to the target (excess = allocated -
  capacity x target / 100); people below the target are filled up to it (spare). Moves are
  made in passes by match quality across all OVER people (same role, then a role listed
  under skills, then, only with --any-role, any other role, labelled cross-role); within a
  pass the largest excess goes first, to the receiver with the most spare. Without a role
  column any receiver qualifies. Whatever is left is the residual
  (above the target, and of that above capacity) that the team cannot absorb in that
  period: re-sequence within float, reduce scope, add capacity or extend the date.

OUTPUT  --format table (default) | md (markdown tables) | csv (one row per person and period
  with every computed field; --level adds moved, allocated_after, utilization_after_pct and
  flag_after) | json ({"people", "rows", "periods", "summary"[, "leveling"]}).

EXIT CODES  0 success  -  1 --fail-on gate failed (over: anyone OVER in any period; high:
  anyone OVER or HIGH), the report is still printed  -  2 bad input, bad option or internal
  error ("error: ..." on stderr). --fail-on judges the plan as given, before any --level moves.

EXAMPLES
  python .claude/skills/resource-management/scripts/capacity_check.py .claude/skills/resource-management/assets/resource-allocation-sample.csv
  python .claude/skills/resource-management/scripts/capacity_check.py .claude/skills/resource-management/assets/resource-allocation-sample.csv --level
  python .claude/skills/resource-management/scripts/capacity_check.py .claude/skills/resource-management/assets/resource-allocation-sample.csv --period W7 --level --any-role
  python .claude/skills/resource-management/scripts/capacity_check.py .claude/skills/resource-management/assets/resource-allocation-sample.csv --fail-on over
  python .claude/skills/resource-management/scripts/capacity_check.py allocation.json --json --format json
  cat allocation.csv | python .claude/skills/resource-management/scripts/capacity_check.py - --unit hours --high 85 --target 75 --format md
"""
from __future__ import annotations

import argparse
import codecs
import csv
import io
import json
import math
import re
import sys
import unicodedata
from decimal import ROUND_HALF_UP, Context, Decimal

BOM = "﻿"
JSON_KEYS = ("resources", "people")
EPS = 1e-9
MAX_VALUE = 1e9  # a capacity or allocation above a billion units is a data error, not a plan
DEC = Context(prec=60, rounding=ROUND_HALF_UP)

PERSON_ALIASES = ("person", "name", "resource", "member", "employee")
CAPACITY_ALIASES = ("capacity", "cap", "availability")
ALLOCATED_ALIASES = ("allocated", "allocation", "alloc", "assigned", "demand", "load")
ROLE_ALIASES = ("role", "position", "job_role")
SKILLS_ALIASES = ("skills", "can_cover", "covers", "backup_for")
PERIOD_ALIASES = ("period", "week", "sprint", "month", "iteration")
PROJECT_ALIASES = ("project", "assignment", "task", "work_package", "workstream")
UNIT_ALIASES = ("unit", "units", "uom")
UNIT_SYNONYMS = {
    "h": "hours", "hr": "hours", "hrs": "hours", "hour": "hours", "hours": "hours",
    "d": "days", "day": "days", "days": "days", "pd": "days", "person-days": "days", "person days": "days",
    "%": "percent", "pct": "percent", "percent": "percent", "percentage": "percent",
    "fte": "fte",
}
FLAG_MARK = {"OVER": "*", "HIGH": "+", "UNDER": "-", "OK": "", "OFF": ""}


# ----------------------------------------------------------------------------- input helpers
def read_text(path, encoding="utf-8-sig"):
    """Read a file, or stdin when path is '-', stripping a UTF-8 BOM (Excel 'CSV UTF-8')."""
    if path == "-":
        data = sys.stdin.buffer.read() if hasattr(sys.stdin, "buffer") else sys.stdin.read()
        text = data.decode(encoding) if isinstance(data, bytes) else data
    else:
        with open(path, encoding=encoding, newline="") as fh:
            text = fh.read()
    return text.lstrip(BOM)


def sniff_delimiter(text):
    try:
        return csv.Sniffer().sniff(text[:4096], delimiters=",;\t|").delimiter
    except csv.Error:
        return ","


def load_rows(text, as_json, json_keys=JSON_KEYS):
    """Return (rows, headers). CSV auto-detects , ; tab |. JSON: list of objects or {json_key: [...]}."""
    if not as_json and text.lstrip()[:1] in ("[", "{"):
        raise ValueError("input looks like JSON; pass --json")
    if as_json:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON: {exc}")
        if isinstance(data, dict):
            key = next((k for k in json_keys if k in data), None)
            if key is None:
                raise ValueError(f"JSON object must contain a '{json_keys[0]}' list; found keys: {sorted(data)}")
            data = data[key]
        if not isinstance(data, list):
            raise ValueError(f"JSON must be a list of objects or {{'{json_keys[0]}': [...]}}")
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


# ',' before one or two trailing digits is a decimal comma ('2,5', '37,50'); before groups of three
# digits it is a thousands separator ('1,000', '12,345.67'); any other comma ('1.000,50') is ambiguous.
DECIMAL_COMMA_RE = re.compile(r"[-+]?\d+,\d{1,2}")
THOUSANDS_RE = re.compile(r"[-+]?\d{1,3}(?:,\d{3})+(?:\.\d+)?")


def _num(raw, where, minimum=None, maximum=None, integer=False):
    """Parse a number tolerant of '$', '€', '£', whitespace, a trailing '%' (stripped, value unchanged)
    and commas: '1,000' -> 1000 (thousands), '2,5' -> 2.5 (decimal comma), '1.000,50' -> error."""
    if isinstance(raw, bool):
        raise ValueError(f"{where}: {raw!r} is a boolean, not a number")
    s = str(raw).strip()
    if s.endswith("%"):
        s = s[:-1]
    s = s.replace("$", "").replace("€", "").replace("£", "").strip()
    if "," in s:
        if DECIMAL_COMMA_RE.fullmatch(s):
            s = s.replace(",", ".")
        elif THOUSANDS_RE.fullmatch(s):
            s = s.replace(",", "")
        else:
            raise ValueError(f"{where}: {raw!r} is ambiguous; use '.' as the decimal point and ',' only for thousands")
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
        raise ValueError(f"{where}: {raw!r} is above the maximum {maximum:,.0f}")
    return v


def _has_column(headers, aliases):
    present = {h.lower().lstrip(BOM).strip() for h in headers if h}
    return any(a.lower() in present for a in aliases)


def _text(value, where):
    """Scalar cell -> clean text (NFC, whitespace and newlines collapsed); '' when absent."""
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        raise ValueError(f"{where}: {value!r} must be text, not a {type(value).__name__}")
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", str(value))).strip()


def _skills(value, where):
    """Skills cell -> list of role names; accepts 'A / B', 'A; B', 'A | B' or a JSON list."""
    if value is None:
        return []
    items = value if isinstance(value, list) else re.split(r"\s*[/;|]\s*", _text(value, where))
    out = []
    for item in items:
        s = _text(item, where)
        if s and s.casefold() not in (o.casefold() for o in out):
            out.append(s)
    return out


def _unit(value, where):
    u = _text(value, where).lower()
    if u not in UNIT_SYNONYMS:
        raise ValueError(f"{where}: {value!r} is not a unit; use hours, days, percent or fte")
    return UNIT_SYNONYMS[u]


def _is_pct(raw):
    return raw is not None and not isinstance(raw, bool) and str(raw).strip().endswith("%")


# ----------------------------------------------------------------------------- formatting helpers
def _q(x, places):
    """Round half up (112.5 -> 113 at 0 places, 81.25 -> 81.3 at 1) so a flag is explainable from the table."""
    return DEC.quantize(Decimal(repr(float(x))), Decimal(1).scaleb(-places))


def _fmt(x, places=1, sign=False):
    if x is None:
        return "n/a"
    d = _q(x, places)
    if d == 0:
        d = abs(d)  # never print -0.0
    s = f"{d:,.{places}f}"
    return ("+" + s) if sign and d > 0 else s


def _pct(x):
    return "n/a" if x is None else _fmt(x, 1) + "%"


def _plain(v):
    """Compact number for CSV cells: up to 4 decimals, no trailing zeros, never exponent noise."""
    if v is None:
        return ""
    s = f"{float(v):.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _dw(s):
    """Display width: wide East Asian characters count 2, combining marks 0."""
    return sum(0 if unicodedata.combining(c) else (2 if unicodedata.east_asian_width(c) in "WF" else 1) for c in s)


def _clip(s, width):
    """Sanitize and truncate to a display width with an ellipsis."""
    s = re.sub(r"\s+", " ", str(s)).strip()
    if _dw(s) <= width:
        return s
    out, w = "", 0
    for c in s:
        cw = _dw(c)
        if w + cw > width - 1:
            break
        out, w = out + c, w + cw
    return out + "…"


def _aligned(headers, rows, right):
    widths = [max(_dw(h), *(_dw(r[c]) for r in rows)) if rows else _dw(h) for c, h in enumerate(headers)]

    def pad(c, i):
        gap = " " * max(0, widths[i] - _dw(c))
        return gap + c if i in right else c + gap

    def line(cells):
        return "  ".join(pad(c, i) for i, c in enumerate(cells)).rstrip()

    return [line(headers), line(["-" * w for w in widths])] + [line(r) for r in rows]


def _md(headers, rows, right):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---:" if i in right else ":---" for i in range(len(headers))) + "|"]
    for r in rows:
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
    return out


# ----------------------------------------------------------------------------- parsing and aggregation
def parse(rows, headers, unit_opt, warn):
    """Aggregate rows into cells keyed by (person, period); validate units and capacity agreement."""
    require_columns(headers, [PERSON_ALIASES, CAPACITY_ALIASES, ALLOCATED_ALIASES])
    has_period = _has_column(headers, PERIOD_ALIASES)
    has_project = _has_column(headers, PROJECT_ALIASES)
    has_role = _has_column(headers, ROLE_ALIASES)
    has_unit = _has_column(headers, UNIT_ALIASES)
    people, periods, cells = {}, {}, {}
    units_seen, pct_rows, plain_rows = {}, [], []
    for i, row in enumerate(rows, 1):
        person = _text(_get(row, *PERSON_ALIASES), f"row {i}, column person")
        if not person:
            raise ValueError(f"row {i}, column person: blank (every row needs a person)")
        where = f"row {i} ({person})"
        role = _text(_get(row, *ROLE_ALIASES), f"{where}, column role")
        skills = _skills(_get(row, *SKILLS_ALIASES), f"{where}, column skills")
        period = _text(_get(row, *PERIOD_ALIASES), f"{where}, column period") if has_period else ""
        if has_period and not period:
            raise ValueError(f"{where}, column period: blank (with a period column every row needs a period)")
        project = _text(_get(row, *PROJECT_ALIASES), f"{where}, column project") if has_project else ""
        cap_raw = _get(row, *CAPACITY_ALIASES)
        alloc_raw = _get(row, *ALLOCATED_ALIASES)
        if alloc_raw is None:
            raise ValueError(f"{where}, column allocated: blank (enter 0 when nothing is assigned)")
        row_unit = _unit(_get(row, *UNIT_ALIASES), f"{where}, column unit") if has_unit and _get(row, *UNIT_ALIASES) is not None else None
        if cap_raw is not None and _is_pct(cap_raw) != _is_pct(alloc_raw):
            raise ValueError(f"{where}: capacity {cap_raw!r} and allocated {alloc_raw!r} must be in the same unit "
                             f"(a '%' on one but not the other)")
        if _is_pct(alloc_raw):
            if row_unit not in (None, "percent"):
                raise ValueError(f"{where}: unit is {row_unit} but allocated {alloc_raw!r} carries a '%'")
            row_unit = "percent"
            pct_rows.append(i)
        elif row_unit is None:
            plain_rows.append(i)
        if row_unit:
            units_seen.setdefault(row_unit, []).append(i)
        capacity = None if cap_raw is None else _num(cap_raw, f"{where}, column capacity", minimum=0, maximum=MAX_VALUE)
        allocated = _num(alloc_raw, f"{where}, column allocated", minimum=0, maximum=MAX_VALUE)

        pkey, perkey = person.casefold(), period.casefold()
        p = people.setdefault(pkey, {"person": person, "roles": [], "skills": [], "order": len(people)})
        if role and role.casefold() not in (r.casefold() for r in p["roles"]):
            p["roles"].append(role)
        for s in skills:
            if s.casefold() not in (x.casefold() for x in p["skills"]):
                p["skills"].append(s)
        periods.setdefault(perkey, period)
        c = cells.setdefault((pkey, perkey), {"pkey": pkey, "perkey": perkey, "capacity": None, "cap_row": None,
                                              "allocated": 0.0, "rows": [], "assignments": {}})
        if capacity is not None:
            if c["capacity"] is None:
                c["capacity"], c["cap_row"] = capacity, i
            elif not math.isclose(c["capacity"], capacity, rel_tol=1e-9, abs_tol=1e-9):
                scope = f" in period {period}" if period else ""
                raise ValueError(f"{where}, column capacity: {_fmt(capacity)} differs from {_fmt(c['capacity'])} on "
                                 f"row {c['cap_row']} for the same person{scope}; capacity is per person and period "
                                 f"and must agree across their rows (allocations are summed)")
        c["allocated"] = round(c["allocated"] + allocated, 9)
        c["rows"].append(i)
        label = project or f"row {i}"
        c["assignments"][label] = round(c["assignments"].get(label, 0.0) + allocated, 9)

    for c in cells.values():
        if c["capacity"] is None:
            p = people[c["pkey"]]["person"]
            scope = f" in period {periods[c['perkey']]}" if has_period else ""
            raise ValueError(f"row {c['rows'][0]} ({p}), column capacity: blank on every row for this person{scope}")

    if len(units_seen) > 1:
        parts = [f"{u} (rows {', '.join(map(str, rs[:5]))}{', ...' if len(rs) > 5 else ''})" for u, rs in units_seen.items()]
        raise ValueError("rows mix units: " + " and ".join(parts) + "; use one unit for the whole file "
                         "(convert percent to hours as capacity x hours-per-period / 100)")
    if pct_rows and plain_rows and unit_opt != "percent":
        def few(rs):
            return ", ".join(map(str, rs[:5])) + (", ..." if len(rs) > 5 else "")
        raise ValueError(f"rows mix units: a '%' on rows {few(pct_rows)} but plain numbers on rows {few(plain_rows)}; "
                         f"use one unit for the whole file, or pass --unit percent if every row is percent")
    seen = next(iter(units_seen), None)
    if unit_opt and seen and seen != unit_opt:
        raise ValueError(f"--unit {unit_opt} contradicts the data, which is in {seen} (rows {units_seen[seen][0]}, ...)")
    unit = unit_opt or seen
    if unit is None:
        caps = sorted({round(c["capacity"], 6) for c in cells.values() if c["capacity"] > 0})
        if 100 in caps and len(caps) > 1:
            others = ", ".join(_fmt(x) for x in caps if x != 100)
            warn(f"warning: capacities include 100 and {others}; if some rows are percent and others hours the "
                 f"per-person utilization is still right but team totals are not; add a unit column or pass --unit")
    return {"people": people, "periods": periods, "cells": cells, "unit": unit,
            "has_period": has_period, "has_project": has_project, "has_role": has_role}


def classify(capacity, allocated, bands):
    """(utilization or None, flag). Flags compare the utilization rounded to 0.1% (as displayed)."""
    if capacity <= 0:
        return None, ("OVER" if allocated > EPS else "OFF")
    util = allocated / capacity * 100.0
    u = float(_q(util, 1))
    if u > bands["threshold"]:
        return util, "OVER"
    if u >= bands["high"]:
        return util, "HIGH"
    if u < bands["under"]:
        return util, "UNDER"
    return util, "OK"


def _load_key(c):
    if c["utilization"] is None:
        return math.inf if c["allocated"] > EPS else -math.inf
    return c["utilization"]


def analyse(model, bands, period_filter):
    people, periods, cells = model["people"], model["periods"], model["cells"]
    if period_filter is not None:
        key = re.sub(r"\s+", " ", period_filter).strip().casefold()
        if not model["has_period"]:
            raise ValueError("--period needs a period column in the input")
        if key not in periods:
            raise ValueError(f"period {period_filter!r} not found; periods in the input: {', '.join(periods.values())}")
        periods = {key: periods[key]}
        cells = {k: c for k, c in cells.items() if k[1] == key}
        people = {k: p for k, p in people.items() if any(ck[0] == k for ck in cells)}
    target = bands["target"]
    order = list(periods)
    for c in cells.values():
        c["person"] = people[c["pkey"]]["person"]
        c["period"] = periods[c["perkey"]]
        c["utilization"], c["flag"] = classify(c["capacity"], c["allocated"], bands)
        c["headroom"] = c["capacity"] * target / 100.0 - c["allocated"]

    def cells_of(pkey):
        return [cells[(pkey, k)] for k in order if (pkey, k) in cells]

    summaries = []
    for pkey, p in people.items():
        pcs = cells_of(pkey)
        peak = max(pcs, key=_load_key)
        summaries.append({
            "person": p["person"], "roles": p["roles"], "skills": p["skills"],
            "peak_period": peak["period"], "capacity": peak["capacity"], "allocated": peak["allocated"],
            "utilization": peak["utilization"], "headroom": peak["headroom"], "flag": peak["flag"],
            "periods_over": [c["period"] for c in pcs if c["flag"] == "OVER"],
            "periods_high": [c["period"] for c in pcs if c["flag"] == "HIGH"],
            "periods_under": [c["period"] for c in pcs if c["flag"] == "UNDER"],
            "_key": pkey, "_load": _load_key(peak),
        })
    summaries.sort(key=lambda s: (-s["_load"], s["person"].casefold()))

    team = []
    for k in order:
        pcs = [c for c in cells.values() if c["perkey"] == k]
        cap = sum(c["capacity"] for c in pcs)
        alloc = sum(c["allocated"] for c in pcs)
        team.append({
            "period": periods[k], "people": len(pcs), "capacity": round(cap, 6), "allocated": round(alloc, 6),
            "utilization": (alloc / cap * 100.0) if cap > 0 else None,
            "headroom": round(sum(c["headroom"] for c in pcs), 6),
            "fte_load": round(sum(c["allocated"] / c["capacity"] for c in pcs if c["capacity"] > 0), 6),
            "over": sum(c["flag"] == "OVER" for c in pcs), "high": sum(c["flag"] == "HIGH" for c in pcs),
            "under": sum(c["flag"] == "UNDER" for c in pcs),
        })

    ordered_cells = sorted(cells.values(), key=lambda c: (order.index(c["perkey"]), people[c["pkey"]]["order"]))
    over_cells = [c for c in ordered_cells if c["flag"] == "OVER"]
    tot_cap = sum(t["capacity"] for t in team)
    tot_alloc = sum(t["allocated"] for t in team)

    key_person = []
    if model["has_role"]:
        for s in summaries:
            if not s["periods_over"]:
                continue
            for role in s["roles"]:
                rk = role.casefold()
                others = [q["person"] for q in people.values()
                          if q["person"] != s["person"] and rk in (r.casefold() for r in q["roles"])]
                if others:
                    continue
                backups = [q["person"] for q in people.values()
                           if q["person"] != s["person"] and rk in (x.casefold() for x in q["skills"])]
                key_person.append({"person": s["person"], "role": role, "periods_over": s["periods_over"],
                                   "backups": backups})

    def names(flag):
        return [s["person"] for s in summaries if s["flag"] == flag]

    summary = {
        "unit": model["unit"], "periods": [periods[k] for k in order], "has_period": model["has_period"],
        "bands": dict(bands),
        "people_count": len(summaries),
        "over_people": names("OVER"), "high_people": names("HIGH"), "under_people": names("UNDER"),
        "ok_people": names("OK"), "off_people": names("OFF"),
        "over_person_periods": len(over_cells),
        "high_person_periods": sum(c["flag"] == "HIGH" for c in cells.values()),
        "total_capacity": round(tot_cap, 6), "total_allocated": round(tot_alloc, 6),
        "team_utilization": (tot_alloc / tot_cap * 100.0) if tot_cap > 0 else None,
        "team_headroom": round(sum(t["headroom"] for t in team), 6),
        "avg_fte_load": round(sum(t["fte_load"] for t in team) / len(team), 6) if team else 0.0,
        "key_person_risks": key_person,
    }
    return {"people": summaries, "cells": ordered_cells, "over_cells": over_cells, "team": team,
            "summary": summary, "model": model, "people_map": people, "order": order}


# ----------------------------------------------------------------------------- leveling
def _match(giver, receiver, has_role):
    """2 = shares a primary role, 1 = covers a giver role via skills, 0 = other role (or no role data)."""
    if not has_role:
        return 0
    groles = {r.casefold() for r in giver["roles"]}
    if groles & {r.casefold() for r in receiver["roles"]}:
        return 2
    if groles & {s.casefold() for s in receiver["skills"]}:
        return 1
    return 0


MATCH_LABEL = {2: "same role", 1: "skills", 0: "cross-role"}


def level(result, bands, any_role):
    target = bands["target"]
    people, model = result["people_map"], result["model"]
    restrict = model["has_role"] and not any_role
    moves, residual = [], []
    for c in result["cells"]:
        c["allocated_after"] = c["allocated"]
    for k in result["order"]:
        pcs = [c for c in result["cells"] if c["perkey"] == k]

        def limit(c):
            return c["capacity"] * target / 100.0

        givers = sorted([c for c in pcs if c["flag"] == "OVER"],
                        key=lambda c: (-(c["allocated"] - limit(c)), c["person"].casefold()))
        receivers = [c for c in pcs if c["capacity"] > 0 and c["flag"] != "OVER" and c["allocated"] < limit(c) - EPS]
        # Best matches first across ALL givers: same role, then skills, then (only with --any-role) cross-role,
        # so a cross-role move never takes spare capacity that a skilled receiver could have used.
        ranks = (2, 1) if restrict else ((2, 1, 0) if model["has_role"] else (0,))
        for rank in ranks:
            for g in givers:
                gp = people[g["pkey"]]
                while g["allocated_after"] - limit(g) > EPS:
                    need = g["allocated_after"] - limit(g)
                    cands = []
                    for r in receivers:
                        spare = limit(r) - r["allocated_after"]
                        if spare > EPS and _match(gp, people[r["pkey"]], model["has_role"]) == rank:
                            cands.append((-round(spare, 6), r["person"].casefold(), r, spare))
                    if not cands:
                        break
                    cands.sort(key=lambda t: t[:2])
                    _, _, r, spare = cands[0]
                    amount = round(min(need, spare), 9)
                    g_before, r_before = g["allocated_after"], r["allocated_after"]
                    g["allocated_after"] = round(g_before - amount, 9)
                    r["allocated_after"] = round(r_before + amount, 9)
                    moves.append({
                        "period": g["period"], "amount": amount, "from": g["person"], "to": r["person"],
                        "from_util_before": g_before / g["capacity"] * 100 if g["capacity"] > 0 else None,
                        "from_util_after": g["allocated_after"] / g["capacity"] * 100 if g["capacity"] > 0 else None,
                        "to_util_before": r_before / r["capacity"] * 100,
                        "to_util_after": r["allocated_after"] / r["capacity"] * 100,
                        "match": MATCH_LABEL[rank] if model["has_role"] else "no role data",
                    })
        for g in givers:
            left = g["allocated_after"] - limit(g)
            if left > EPS:
                residual.append({"period": g["period"], "person": g["person"], "above_target": round(left, 9),
                                 "above_capacity": round(max(0.0, g["allocated_after"] - g["capacity"]), 9)})
    for c in result["cells"]:
        c["moved"] = round(c["allocated_after"] - c["allocated"], 9)
        c["utilization_after"], c["flag_after"] = classify(c["capacity"], c["allocated_after"], bands)
    over_after = [c for c in result["cells"] if c["flag_after"] == "OVER"]
    return {
        "target": target, "restricted_to_roles": restrict, "moves": moves, "residual": residual,
        "moved_total": round(sum(m["amount"] for m in moves), 6),
        "residual_above_target": round(sum(r["above_target"] for r in residual), 6),
        "residual_above_capacity": round(sum(r["above_capacity"] for r in residual), 6),
        "over_person_periods_after": len(over_after),
        "over_people_after": sorted({c["person"] for c in over_after}, key=str.casefold),
    }


# ----------------------------------------------------------------------------- rendering
def _unit_label(result):
    return result["summary"]["unit"] or "units"


def _places(result):
    caps = [c["capacity"] for c in result["cells"]]
    return 2 if result["summary"]["unit"] == "fte" or (caps and max(caps) <= 5) else 1


def _roles(s):
    return " / ".join(s["roles"])


def _multi(result):
    return result["summary"]["has_period"] and len(result["summary"]["periods"]) > 1


def _person_table(result):
    pl = _places(result)
    per = _multi(result)
    headers = ["Person", "Role"] + (["Peak"] if per else []) + ["Capacity", "Allocated", "Util%", "Headroom", "Flag"]
    headers += ["OVER/HIGH"] if per else []
    rows = []
    for s in result["people"]:
        r = [_clip(s["person"], 24), _clip(_roles(s), 20)] + ([_clip(s["peak_period"], 12)] if per else [])
        r += [_fmt(s["capacity"], pl), _fmt(s["allocated"], pl), _pct(s["utilization"]),
              _fmt(s["headroom"], pl, sign=True), s["flag"]]
        r += [f"{len(s['periods_over'])}/{len(s['periods_high'])}"] if per else []
        rows.append(r)
    right = set(range(3 if per else 2, 3 + 4 if per else 2 + 4))
    if per:
        right.add(len(headers) - 1)
    return headers, rows, right


def _matrix(result):
    order, cells = result["order"], {(c["pkey"], c["perkey"]): c for c in result["cells"]}
    headers = ["Person"] + [_clip(result["model"]["periods"][k], 10) for k in order]
    rows = []
    for s in result["people"]:
        r = [_clip(s["person"], 24)]
        for k in order:
            c = cells.get((s["_key"], k))
            if c is None:
                r.append("—")
            elif c["flag"] == "OFF":
                r.append("off")
            elif c["utilization"] is None:
                r.append("no cap*")
            else:
                r.append(_pct(c["utilization"]) + FLAG_MARK[c["flag"]])
        rows.append(r)
    rows.append(["Team"] + [_pct(t["utilization"]) for t in result["team"]])
    return headers, rows, set(range(1, len(headers)))


def _team_table(result):
    pl = _places(result)
    headers = ["Period", "People", "Capacity", "Allocated", "Util%", "Headroom", "FTE load", "OVER", "HIGH", "UNDER"]
    rows = [[_clip(t["period"], 12), str(t["people"]), _fmt(t["capacity"], pl), _fmt(t["allocated"], pl),
             _pct(t["utilization"]), _fmt(t["headroom"], pl, sign=True), _fmt(t["fte_load"], 2),
             str(t["over"]), str(t["high"]), str(t["under"])] for t in result["team"]]
    return headers, rows, set(range(1, len(headers)))


def _breakdown_lines(result):
    if not result["over_cells"]:
        return []
    if not (result["model"]["has_project"] or any(len(c["rows"]) > 1 for c in result["over_cells"])):
        return []
    pl = _places(result)
    per = result["summary"]["has_period"]
    out = []
    for c in result["over_cells"]:
        parts = "; ".join(f"{_clip(lbl, 40)} {_fmt(v, pl)}" for lbl, v in c["assignments"].items())
        head = f"{c['period']}  " if per else ""
        out.append(f"{head}{c['person']}: {_fmt(c['allocated'], pl)} of {_fmt(c['capacity'], pl)} "
                   f"({_pct(c['utilization'])}) = {parts}")
    return out


def _plural(n, one, many):
    return f"{n} {one if n == 1 else many}"


def _summary_lines(result, gate):
    s, pl = result["summary"], _places(result)
    b = s["bands"]
    unit = _unit_label(result)
    per = s["has_period"]
    lines = []
    for flag, key in (("OVER", "over_people"), ("HIGH", "high_people"), ("UNDER", "under_people")):
        who = s[key]
        extra = ""
        if flag == "OVER" and _multi(result):
            extra = f" in {_plural(s['over_person_periods'], 'person-period', 'person-periods')}"
        lines.append(f"{flag + ':':<7}{_plural(len(who), 'person', 'people')}{extra}"
                     + (f" ({', '.join(who)})" if who else ""))
    lines.append(f"Team: {_fmt(s['total_allocated'], pl)} of {_fmt(s['total_capacity'], pl)} {unit} allocated "
                 f"({_pct(s['team_utilization'])}); headroom to the {_fmt(b['target'])}% target "
                 f"{_fmt(s['team_headroom'], pl, sign=True)} {unit}")
    lines.append(f"Load: {_fmt(s['avg_fte_load'], 2)} FTE-equivalent of work"
                 + (" per period on average" if _multi(result) else "")
                 + f" on {_plural(s['people_count'], 'person', 'people')}")
    for k in s["key_person_risks"]:
        backup = f"backup via skills: {', '.join(k['backups'])}" if k["backups"] else "no backup in the file"
        when = f" in {', '.join(k['periods_over'])}" if per else ""
        lines.append(f"Key-person risk: {k['person']} is OVER{when} and the only {k['role']} ({backup}); "
                     f"log it in the risk register")
    if s["over_people"] and s["team_utilization"] is not None and s["team_utilization"] <= b["threshold"]:
        lines.append(f"Note: team utilization {_pct(s['team_utilization'])} looks deliverable, yet "
                     f"{_plural(len(s['over_people']), 'person is', 'people are')} OVER; a total hides individual "
                     f"peaks, so act on the per-person view.")
    if not per:
        lines.append("Note: no period column, so this is one flat period; for plans longer than a week or "
                     "sprint add a period column so peaks are not averaged away.")
    if gate:
        lines.append(gate["line"])
    return lines


def _no_move_text(lv):
    """Why leveling found no move: roles matter only when receivers are restricted to them."""
    if lv["restricted_to_roles"]:
        return "No move possible: nobody with spare capacity holds or covers the roles of the OVER people."
    return "No move possible: nobody else has spare capacity below the target in the OVER people's periods."


def _level_tables(lv, result):
    pl = _places(result)
    unit = _unit_label(result)
    if lv["restricted_to_roles"]:
        rule = "; receivers must hold the role or list it under skills"
    elif result["model"]["has_role"]:
        rule = "; same role first, then skills, then other roles (--any-role, marked cross-role)"
    else:
        rule = "; no role column, so skills are not checked"
    intro = (f"Leveling plan (target {_fmt(lv['target'])}%): greedy within each period; OVER people are brought "
             f"down to the target, people below it are filled up to it{rule}. Confirm every move with the people "
             f"involved.")
    move_h = ["Period", "Move", "From", "Before -> after", "To", "Before -> after", "Match"]
    move_r = [[_clip(m["period"], 12), _fmt(m["amount"], pl), _clip(m["from"], 20),
               "no capacity" if m["from_util_before"] is None else
               f"{_pct(m['from_util_before'])} -> {_pct(m['from_util_after'])}", _clip(m["to"], 20),
               f"{_pct(m['to_util_before'])} -> {_pct(m['to_util_after'])}", m["match"]] for m in lv["moves"]]
    res_h = ["Period", "Person", "Above target", "Above capacity"]
    res_r = [[_clip(r["period"], 12), _clip(r["person"], 24), _fmt(r["above_target"], pl),
              _fmt(r["above_capacity"], pl)] for r in lv["residual"]]
    totals = [f"Moved {_fmt(lv['moved_total'], pl)} {unit}; residual {_fmt(lv['residual_above_target'], pl)} above the "
              f"target, of which {_fmt(lv['residual_above_capacity'], pl)} above capacity.",
              (f"After the moves: {_plural(len(lv['over_people_after']), 'person', 'people')} OVER "
               f"({', '.join(lv['over_people_after'])}) in "
               f"{_plural(lv['over_person_periods_after'], 'person-period', 'person-periods')}"
               if lv["over_people_after"] else "After the moves: nobody is OVER")
              + f" (before: {_plural(result['summary']['over_person_periods'], 'person-period', 'person-periods')})."]
    if lv["residual_above_capacity"] > EPS:
        totals.append("The residual above capacity is not deliverable as planned: re-sequence within float "
                      "(project-schedule), reduce scope, add capacity or extend the date.")
    elif lv["residual_above_target"] > EPS:
        totals.append("Everything above capacity is absorbed; the residual above the target is sustained load "
                      "to watch or re-sequence.")
    return intro, (move_h, move_r, {1}), (res_h, res_r, {2, 3}), totals


def render_table(result, gate, lv):
    s = result["summary"]
    b = s["bands"]
    periods = s["periods"]
    span = ""
    if s["has_period"]:
        shown = ", ".join(periods) if len(periods) <= 6 else f"{periods[0]} … {periods[-1]}"
        span = f", {_plural(len(periods), 'period', 'periods')} ({shown})"
    unit = s["unit"] or "not stated (add a unit column or pass --unit)"
    out = [f"Resource capacity check: {_plural(s['people_count'], 'person', 'people')}{span}; unit: {unit}",
           f"Bands: OVER > {_fmt(b['threshold'])}%  HIGH >= {_fmt(b['high'])}%  UNDER < {_fmt(b['under'])}%  "
           f"target {_fmt(b['target'])}% (headroom = capacity x target - allocated)", ""]
    h, r, right = _person_table(result)
    out.append("Per person (flag and values at each person's peak period)" if _multi(result) else "Per person")
    out += _aligned(h, r, right)
    if _multi(result):
        out += ["", "Utilization by period (* OVER, + HIGH, - UNDER)"]
        h, r, right = _matrix(result)
        lines = _aligned(h, r, right)
        out += lines[:-1] + [lines[1], lines[-1]]  # rule above the Team row
        out += ["", "Team by period"]
        h, r, right = _team_table(result)
        out += _aligned(h, r, right)
    bd = _breakdown_lines(result)
    if bd:
        out += ["", "Where the OVER load comes from"] + ["  " + x for x in bd]
    out += ["", "Summary"] + _summary_lines(result, gate)
    if lv is not None:
        out.append("")
        if not lv["moves"] and not lv["residual"]:
            out.append("Leveling plan: nothing to level, nobody is OVER.")
        else:
            intro, moves, res, totals = _level_tables(lv, result)
            out.append(intro)
            if moves[1]:
                out += _aligned(*moves)
            else:
                out.append(_no_move_text(lv))
            if res[1]:
                out += ["", "Residual the team cannot absorb in the same period"] + _aligned(*res)
            out += [""] + totals
    return "\n".join(out)


def render_md(result, gate, lv):
    s = result["summary"]
    b = s["bands"]
    out = ["## Resource capacity check", "",
           f"{_plural(s['people_count'], 'person', 'people')}"
           + (f", periods {', '.join(s['periods'])}" if s["has_period"] else "")
           + f"; unit: {_unit_label(result)}. Bands: OVER > {_fmt(b['threshold'])}%, HIGH >= {_fmt(b['high'])}%, "
           f"UNDER < {_fmt(b['under'])}%, target {_fmt(b['target'])}%.", ""]
    out += _md(*_person_table(result))
    if _multi(result):
        h, r, right = _matrix(result)
        r[-1] = [f"**{c}**" for c in r[-1]]
        out += ["", "### Utilization by period (* OVER, + HIGH, - UNDER)", ""] + _md(h, r, right)
        out += ["", "### Team by period", ""] + _md(*_team_table(result))
    bd = _breakdown_lines(result)
    if bd:
        out += ["", "### Where the OVER load comes from", ""] + [f"- {x}" for x in bd]
    out += ["", "### Summary", ""] + [f"- {' '.join(x.split())}" for x in _summary_lines(result, gate)]
    if lv is not None:
        out += ["", "### Leveling plan", ""]
        if not lv["moves"] and not lv["residual"]:
            out.append("Nothing to level, nobody is OVER.")
        else:
            intro, moves, res, totals = _level_tables(lv, result)
            out += [intro, ""]
            out += _md(*moves) if moves[1] else [_no_move_text(lv)]
            if res[1]:
                out += ["", "Residual the team cannot absorb in the same period:", ""] + _md(*res)
            out += [""] + [f"- {x}" for x in totals]
    return "\n".join(out)


CSV_COLUMNS = ["person", "role", "skills", "period", "capacity", "allocated", "utilization_pct", "headroom", "flag",
               "assignments"]
CSV_LEVEL = ["moved", "allocated_after", "utilization_after_pct", "flag_after"]


def render_csv(result, gate, lv):
    buf = io.StringIO()
    cols = CSV_COLUMNS + (CSV_LEVEL if lv is not None else [])
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    people = result["people_map"]
    for c in result["cells"]:
        p = people[c["pkey"]]
        row = {"person": c["person"], "role": " / ".join(p["roles"]), "skills": " / ".join(p["skills"]),
               "period": c["period"], "capacity": _plain(c["capacity"]), "allocated": _plain(c["allocated"]),
               "utilization_pct": "" if c["utilization"] is None else str(_q(c["utilization"], 1)),
               "headroom": _plain(c["headroom"]), "flag": c["flag"],
               "assignments": "; ".join(f"{k}={_plain(v)}" for k, v in c["assignments"].items())}
        if lv is not None:
            row.update({"moved": _plain(c["moved"]), "allocated_after": _plain(c["allocated_after"]),
                        "utilization_after_pct": "" if c["utilization_after"] is None else str(_q(c["utilization_after"], 1)),
                        "flag_after": c["flag_after"]})
        w.writerow(row)
    return buf.getvalue().rstrip("\n")


def _rounded(obj):
    if isinstance(obj, float):
        v = round(obj, 4)
        return 0.0 if v == 0 else v
    if isinstance(obj, dict):
        return {k: _rounded(v) for k, v in obj.items() if not str(k).startswith("_")}
    if isinstance(obj, list):
        return [_rounded(v) for v in obj]
    return obj


def render_json(result, gate, lv):
    people = result["people_map"]
    rows = []
    for c in result["cells"]:
        row = {"person": c["person"], "roles": people[c["pkey"]]["roles"], "period": c["period"] or None,
               "capacity": c["capacity"], "allocated": c["allocated"], "utilization": c["utilization"],
               "headroom": c["headroom"], "flag": c["flag"], "source_rows": c["rows"],
               "assignments": [{"project": k, "allocated": v} for k, v in c["assignments"].items()]}
        if lv is not None:
            row.update({"moved": c["moved"], "allocated_after": c["allocated_after"],
                        "utilization_after": c["utilization_after"], "flag_after": c["flag_after"]})
        rows.append(row)
    summary = dict(result["summary"])
    if gate:
        summary["gate"] = {k: v for k, v in gate.items() if k != "line"}
    doc = {"people": result["people"], "rows": rows, "periods": result["team"], "summary": summary}
    if lv is not None:
        doc["leveling"] = lv
    return json.dumps(_rounded(doc), indent=2, ensure_ascii=False, allow_nan=False)


RENDERERS = {"table": render_table, "json": render_json, "csv": render_csv, "md": render_md}


# ----------------------------------------------------------------------------- CLI
def _check_pct(parser, name, v, allow_zero=False):
    if not math.isfinite(v):
        parser.error(f"{name} must be a finite percentage (got {v})")
    if v < 0 or (v == 0 and not allow_zero) or v > 1000:
        low = "0" if allow_zero else "more than 0"
        parser.error(f"{name} must be a percentage from {low} to 1000 (got {_plain(v)})")
    if 0 < v <= 1:
        parser.error(f"{name} is a percentage such as {int(v * 100) or 1}, not a fraction (got {_plain(v)})")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="capacity_check.py",
        description="Resource capacity check: utilization per person and period, OVER/HIGH/OK/UNDER flags on "
                    "each person's peak, headroom to a target, team view per period, and a greedy leveling plan.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("path", help="CSV or JSON of allocation rows (person, capacity, allocated[, role, skills, "
                                     "period, project, unit]), or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="parse the input as JSON (a .json file is detected)")
    parser.add_argument("--threshold", type=float, default=100.0, metavar="PCT",
                        help="OVER when utilization exceeds PCT (default 100)")
    parser.add_argument("--high", type=float, default=90.0, metavar="PCT",
                        help="HIGH when utilization is at least PCT and not OVER (default 90)")
    parser.add_argument("--under", type=float, default=50.0, metavar="PCT",
                        help="UNDER when utilization is below PCT (default 50; 0 disables)")
    parser.add_argument("--target", type=float, default=80.0, metavar="PCT",
                        help="healthy sustained utilization for headroom and leveling (default 80)")
    parser.add_argument("--unit", choices=("hours", "days", "percent", "fte"),
                        help="unit of capacity and allocated (labels the output; must agree with a unit column)")
    parser.add_argument("--period", metavar="P", help="check one period only (needs a period column)")
    parser.add_argument("--level", action="store_true",
                        help="propose a greedy reassignment from OVER people to people below the target in the "
                             "same period, and report the residual that cannot be absorbed")
    parser.add_argument("--any-role", action="store_true",
                        help="with --level, also move work to people of another role (labelled cross-role)")
    parser.add_argument("--fail-on", choices=("over", "high"),
                        help="exit 1 when anyone is OVER (over) or OVER/HIGH (high) in any period: a baseline gate")
    parser.add_argument("--format", choices=("table", "json", "csv", "md"), default="table",
                        help="output format (default table)")
    parser.add_argument("--encoding", default="utf-8-sig",
                        help="input file encoding (default utf-8-sig; e.g. cp1252 for an old Excel export)")
    args = parser.parse_args(argv)

    _check_pct(parser, "--threshold", args.threshold)
    _check_pct(parser, "--high", args.high)
    _check_pct(parser, "--under", args.under, allow_zero=True)
    _check_pct(parser, "--target", args.target)
    if not args.under < args.high <= args.threshold:
        parser.error(f"bands must satisfy --under < --high <= --threshold "
                     f"(got {_plain(args.under)} < {_plain(args.high)} <= {_plain(args.threshold)})")
    if args.target > args.threshold:
        parser.error(f"--target ({_plain(args.target)}) must not exceed --threshold ({_plain(args.threshold)})")
    if args.any_role and not args.level:
        parser.error("--any-role only applies with --level")
    try:
        codecs.lookup(args.encoding)
    except LookupError:
        parser.error(f"--encoding: unknown encoding {args.encoding!r}")

    def warn(msg):
        print(msg, file=sys.stderr)

    if args.high == args.threshold:
        warn(f"warning: --high equals --threshold ({_plain(args.high)}); HIGH only catches exactly that utilization")

    bands = {"threshold": args.threshold, "high": args.high, "under": args.under, "target": args.target}
    try:
        text = read_text(args.path, args.encoding)
        as_json = args.json or (args.path != "-" and args.path.lower().endswith(".json"))
        rows, headers = load_rows(text, as_json)
        model = parse(rows, headers, args.unit, warn)
        result = analyse(model, bands, args.period)
        lv = level(result, bands, args.any_role) if args.level else None
        gate = None
        if args.fail_on:
            s = result["summary"]
            bad = s["over_person_periods"] + (s["high_person_periods"] if args.fail_on == "high" else 0)
            what = "OVER" if args.fail_on == "over" else "OVER or HIGH"
            verdict = "FAIL" if bad else "PASS"
            gate = {"fail_on": args.fail_on, "verdict": verdict, "count": bad,
                    "line": f"Gate --fail-on {args.fail_on}: {verdict} "
                            f"({_plural(bad, 'person-period', 'person-periods')} {what})"}
        print(RENDERERS[args.format](result, gate, lv))
        if gate and args.format == "csv":
            warn(gate["line"])
    except UnicodeDecodeError as exc:
        bad_byte = exc.object[exc.start:exc.start + 1].hex() if isinstance(exc.object, (bytes, bytearray)) else "?"
        print(f"error: {args.path} is not {args.encoding} text (byte 0x{bad_byte} at offset {exc.start}); "
              f"re-save it as 'CSV UTF-8' or pass --encoding cp1252", file=sys.stderr)
        return 2
    except (OSError, ValueError, TypeError, OverflowError, ZeroDivisionError, ArithmeticError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 1 if gate and gate["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
