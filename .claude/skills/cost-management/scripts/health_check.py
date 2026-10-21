#!/usr/bin/env python3
"""Earned-value health check: CV/SV, CPI/SPI, EAC/ETC/VAC, TCPI, percent complete and
spent, a RAG verdict, and (with a period column) a CPI/SPI trend table and a text S-curve.

Reads one row per work package (planned value, earned value, actual cost and, ideally,
budget at completion) from CSV or JSON, prints a per-row table, a TOTAL row, the overall
RAG (Red/Amber/Green) status derived from CPI and SPI, and the forecast at completion.
Standard library only.

ALL VALUES ARE CUMULATIVE TO THE STATUS DATE, in one currency: PV = budget of the work
scheduled so far, EV = budget of the work done so far, AC = cost incurred so far. Do not
feed one period's increment on its own (the indices and EAC/ETC only hold for cumulative
figures); see --incremental for period files that hold increments.

INPUT COLUMNS / KEYS  (case-insensitive; extra columns are ignored)
    task     work-package name       aliases: name, work_package, item, id, wbs             (optional)
    pv       planned value           aliases: planned_value, planned value, planned          (required)
    ev       earned value            aliases: earned_value, earned value, earned             (required)
    ac       actual cost             aliases: actual_cost, actual cost, actual, spent        (required)
    bac      budget at completion    aliases: budget, budget_at_completion, budget at completion (optional)
    period   status period of the row (M3, 2026-07, Sprint 8 ...)  aliases: month, sprint, as_of (optional)
  pv/ev/ac must be finite numbers >= 0; bac must be > 0 and ev must not exceed bac.
  '$', ',', EUR/GBP signs and a trailing '%' are stripped ("80,000" -> 80000, "$100" -> 100).
  CSV delimiter is auto-detected (, ; tab |); a UTF-8 BOM and CRLF line ends are tolerated.
  JSON is a list of objects or {"rows": [...]}; pass --json for JSON input (a JSON file
  given without --json is refused with a hint, never misread as CSV).
  With a period column every row needs one. Each period's rows are a cumulative-to-date
  snapshot and the LAST period in input order is the headline; pass --incremental when the
  rows hold per-period increments instead (they are then accumulated; a task column is
  required and bac is the work package's total budget).

FORMULAS  (per row and for the TOTAL)
  CV  = EV - AC                     SV  = EV - PV            (negative = over budget / behind)
  CPI = EV / AC                     SPI = EV / PV            (1.0 = on plan; undefined when the divisor is 0)
  % complete = EV / BAC             % spent = AC / BAC
  EAC  cpi        = BAC / CPI                       current cost efficiency continues (default)
       atypical   = AC + (BAC - EV)                 the variance so far was a one-off
       composite  = AC + (BAC - EV) / (CPI x SPI)   cost AND schedule pressure persist
       all        = the three above as a range; the cpi figure is the headline
  ETC = EAC - AC                    VAC = BAC - EAC          (negative = forecast overrun)
  TCPI(BAC) = (BAC - EV) / (BAC - AC)   efficiency needed on the remaining work to land on BAC
  TCPI(EAC) = (BAC - EV) / (EAC - AC)   efficiency needed to land on the forecast EAC
  BAC for the TOTAL = sum of the row BACs, or --bac (a disagreement with the sum is warned about).
  When TCPI(BAC) exceeds the CPI to date by more than --tcpi-warn the forecast flags a re-plan.

RAG  (applied to BOTH CPI and SPI; --green / --amber change the bands)
  both >= 0.95 -> GREEN      either < 0.85 -> RED      otherwise -> AMBER
  A CPI or SPI of exactly 0 (money spent or time elapsed, nothing earned) is RED, not n/a.
  A row with only one index defined is rated on that index and marked '*'; a row with
  PV = EV = AC = 0 is 'not started'.

TREND / S-CURVE  (only with a period column)
  One line per period with cumulative PV/EV/AC, CPI, SPI, RAG and the CPI/SPI trend versus
  the previous period (improving / worsening when the index moves by more than 0.02), then a
  text S-curve: '#' = PV, '=' = EV, '$' = AC, scaled to 40 columns against BAC (or the peak).

OUTPUT  --format table (default) | json ({"rows": [...], "summary": {...}}) | csv (rows + TOTAL
  with every computed field, for hand-off to status-report) | md (markdown table + summary).
  --sort worst lists the rows with the lowest CPI/SPI first.

EXIT CODES   0 success  -  2 bad input, bad option or internal error ("error: ..." on stderr)

EXAMPLES
  python .claude/skills/cost-management/scripts/health_check.py .claude/skills/cost-management/assets/evm-snapshot.csv
  python .claude/skills/cost-management/scripts/health_check.py .claude/skills/cost-management/assets/evm-snapshot.csv --eac-method all --sort worst
  python .claude/skills/cost-management/scripts/health_check.py .claude/skills/cost-management/assets/evm-history-sample.csv
  python .claude/skills/cost-management/scripts/health_check.py snapshot.json --json --format json
  cat snapshot.csv | python .claude/skills/cost-management/scripts/health_check.py - --bac 500000 --format md
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import sys

BOM = "﻿"
JSON_KEY = "rows"
TASK_WIDTH = 40
CURVE_WIDTH = 40
TREND_DELTA = 0.02
TOLERANCE = 0.5  # money differences below this are "equal" (display rounds to whole units)
METHODS = ("atypical", "cpi", "composite")  # range display order: usually low -> high
METHOD_LABEL = {
    "cpi": "BAC / CPI",
    "atypical": "AC + (BAC - EV)",
    "composite": "AC + (BAC - EV) / (CPI x SPI)",
}

TASK_ALIASES = ("task", "name", "work_package", "work package", "item", "id", "wbs", "wbs_id")
PV_ALIASES = ("pv", "planned_value", "planned value", "planned")
EV_ALIASES = ("ev", "earned_value", "earned value", "earned")
AC_ALIASES = ("ac", "actual_cost", "actual cost", "actual", "spent")
BAC_ALIASES = ("bac", "budget", "budget_at_completion", "budget at completion")
PERIOD_ALIASES = ("period", "month", "sprint", "as_of", "as of")


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


def _has_column(headers, aliases):
    present = {h.lower().lstrip(BOM).strip() for h in headers if h}
    return any(a.lower() in present for a in aliases)


# ----------------------------------------------------------------------------- formatting helpers
def _sanitize(value, width=None):
    """Collapse whitespace/newlines; truncate with an ellipsis when width is given."""
    s = re.sub(r"\s+", " ", str(value if value is not None else "")).strip()
    if width and len(s) > width:
        s = s[: width - 1] + "…"
    return s


def _money(v):
    if v is None:
        return ""
    s = f"{v:,.0f}"
    return "0" if s in ("-0", "0") else s


def _idx(v):
    if v is None:
        return ""
    s = f"{v:.2f}"
    return "0.00" if s == "-0.00" else s


def _pct(v):
    if v is None:
        return ""
    s = f"{v:.1f}%"
    return "0.0%" if s == "-0.0%" else s


def _ratio(num, den):
    """num / den, or None when the divisor is 0 (the index is then undefined, not zero)."""
    return (num / den) if den else None


def _plain(v):
    """Compact number for CSV cells: up to 4 decimals, no trailing zeros, never exponent noise."""
    if v is None:
        return ""
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ----------------------------------------------------------------------------- core maths
def rag(cpi, spi, green, amber):
    """RAG from whichever of CPI / SPI are defined ('*' = rated on one index); None when neither is."""
    idx = [x for x in (cpi, spi) if x is not None]
    if not idx:
        return None
    if all(x >= green for x in idx):
        verdict = "GREEN"
    elif any(x < amber for x in idx):
        verdict = "RED"
    else:
        verdict = "AMBER"
    return verdict + ("*" if len(idx) == 1 else "")


def evm(pv, ev, ac, bac, method, green, amber):
    """Derived EVM metrics for one set of cumulative primitives (bac may be None)."""
    cpi = _ratio(ev, ac)
    spi = _ratio(ev, pv)
    m = {
        "pv": pv, "ev": ev, "ac": ac, "bac": bac,
        "cv": round(ev - ac, 6), "sv": round(ev - pv, 6),
        "cpi": cpi, "spi": spi,
        "pct_complete": None, "pct_spent": None,
        "eac_method": "cpi" if method == "all" else method,
        "eac": None, "etc": None, "vac": None, "eac_by": {},
        "tcpi_bac": None, "tcpi_eac": None,
        "rag": None, "note": "",
    }
    if bac is not None:
        remaining = bac - ev
        m["pct_complete"] = ev / bac * 100.0
        m["pct_spent"] = ac / bac * 100.0
        m["eac_by"] = {
            "cpi": (bac / cpi) if cpi else None,
            "atypical": ac + remaining,
            "composite": (ac + remaining / (cpi * spi)) if (cpi and spi) else None,
        }
        eac = m["eac_by"][m["eac_method"]]
        if eac is not None:
            m["eac"], m["etc"], m["vac"] = eac, eac - ac, bac - eac
        if bac - ac > TOLERANCE:
            m["tcpi_bac"] = remaining / (bac - ac)
        if eac is not None and eac - ac > TOLERANCE:
            m["tcpi_eac"] = remaining / (eac - ac)
    verdict = rag(cpi, spi, green, amber)
    if verdict is None:
        if pv == 0 and ev == 0 and ac == 0:
            m["rag"], m["note"] = "not started", "not started: PV, EV and AC are all 0"
        else:
            m["rag"], m["note"] = "n/a", "CPI and SPI are both undefined (PV and AC are 0)"
    else:
        m["rag"] = verdict
        if verdict.endswith("*"):
            m["note"] = "rated on one index only: " + ("CPI" if cpi is None else "SPI") + " is undefined (0/0)"
    if bac is not None and m["eac"] is None:
        why = {"cpi": "CPI is 0 or undefined", "atypical": "", "composite": "CPI x SPI is 0 or undefined"}[m["eac_method"]]
        m["note"] = (m["note"] + "; " if m["note"] else "") + f"EAC undefined ({why})"
    return m


def _cell(row, aliases, label, where):
    raw = _get(row, *aliases)
    if raw is None:
        raise ValueError(f"{where}, column {label}: value is missing")
    return _num(raw, f"{where}, column {label}", minimum=0)


def parse_records(rows, headers):
    """Validate every input row into {task, period, pv, ev, ac, bac}; returns (records, has_period)."""
    has_period = _has_column(headers, PERIOD_ALIASES)
    records = []
    for i, row in enumerate(rows, start=1):
        name = _sanitize(_get(row, *TASK_ALIASES, default=""), TASK_WIDTH) or f"Item {i}"
        period = _sanitize(_get(row, *PERIOD_ALIASES, default=""), 20) if has_period else ""
        where = f"row {i} ({name}" + (f", period {period}" if period else "") + ")"
        if has_period and not period:
            raise ValueError(f"{where}: period is blank; every row needs one when a period column is present")
        pv = _cell(row, PV_ALIASES, "pv", where)
        ev = _cell(row, EV_ALIASES, "ev", where)
        ac = _cell(row, AC_ALIASES, "ac", where)
        bac_raw = _get(row, *BAC_ALIASES)
        bac = None
        if bac_raw is not None:
            bac = _num(bac_raw, f"{where}, column bac", minimum=0)
            if bac == 0:
                raise ValueError(f"{where}, column bac: must be > 0 (leave it blank if the budget is unknown)")
        records.append({"task": name, "period": period, "pv": pv, "ev": ev, "ac": ac, "bac": bac})
    return records, has_period


def build_snapshots(records, has_period, incremental):
    """Ordered [(period, [record...])] where every record holds cumulative-to-date values."""
    if not has_period:
        return [("", records)]
    periods, by_period = [], {}
    for r in records:
        if r["period"] not in by_period:
            periods.append(r["period"])
            by_period[r["period"]] = []
        by_period[r["period"]].append(r)
    if not incremental:
        return [(p, by_period[p]) for p in periods]
    running, order, snapshots = {}, [], []
    for p in periods:
        for r in by_period[p]:
            cur = running.get(r["task"])
            if cur is None:
                cur = {"task": r["task"], "pv": 0.0, "ev": 0.0, "ac": 0.0, "bac": None}
                running[r["task"]] = cur
                order.append(r["task"])
            for k in ("pv", "ev", "ac"):
                cur[k] = round(cur[k] + r[k], 6)
            if r["bac"] is not None:
                cur["bac"] = r["bac"]
        snapshots.append((p, [dict(running[t], period=p) for t in order]))
    return snapshots


def _check_ev_within_bac(period, recs):
    for r in recs:
        if r["bac"] is not None and r["ev"] > r["bac"] + 1e-9:
            where = r["task"] + (f", period {period}" if period else "")
            raise ValueError(f"{where}: ev ({_money(r['ev'])}) exceeds bac ({_money(r['bac'])}); "
                             "earned value cannot exceed the budget at completion")


def _trend(prev, cur):
    if prev is None or cur is None:
        return "-"
    delta = cur - prev
    if delta > TREND_DELTA:
        return "improving"
    if delta < -TREND_DELTA:
        return "worsening"
    return "flat"


def period_trends(snapshots, green, amber):
    out, prev = [], None
    for period, recs in snapshots:
        pv = round(sum(r["pv"] for r in recs), 6)
        ev = round(sum(r["ev"] for r in recs), 6)
        ac = round(sum(r["ac"] for r in recs), 6)
        cpi, spi = _ratio(ev, ac), _ratio(ev, pv)
        entry = {
            "period": period, "pv": pv, "ev": ev, "ac": ac, "cpi": cpi, "spi": spi,
            "rag": rag(cpi, spi, green, amber) or "n/a",
            "cpi_trend": _trend(prev["cpi"] if prev else None, cpi),
            "spi_trend": _trend(prev["spi"] if prev else None, spi),
        }
        out.append(entry)
        prev = entry
    return out


def analyse(records, has_period, incremental, override_bac, method, green, amber, tcpi_warn, sort, warn):
    """Compute rows, TOTAL, forecast and (with periods) the trend; returns {"rows": [...], "summary": {...}}."""
    snapshots = build_snapshots(records, has_period, incremental)
    for period, recs in snapshots:
        _check_ev_within_bac(period, recs)
    period, head = snapshots[-1]

    rows = []
    for r in head:
        m = evm(r["pv"], r["ev"], r["ac"], r["bac"], method, green, amber)
        m["task"] = r["task"]
        m["period"] = period
        rows.append(m)
    if sort == "worst":
        def worst_key(m):
            idx = [x for x in (m["cpi"], m["spi"]) if x is not None]
            return (0, min(idx)) if idx else (1, 0.0)
        rows.sort(key=worst_key)

    tot_pv = round(sum(r["pv"] for r in head), 6)
    tot_ev = round(sum(r["ev"] for r in head), 6)
    tot_ac = round(sum(r["ac"] for r in head), 6)
    missing_bac = [r["task"] for r in head if r["bac"] is None]
    sum_bac = round(sum(r["bac"] for r in head if r["bac"] is not None), 6) if len(missing_bac) < len(head) else None

    notes, forecast_note = [], ""
    if override_bac is not None:
        total_bac = override_bac
        if not missing_bac and abs(override_bac - sum_bac) > TOLERANCE:
            warn(f"warning: --bac {_money(override_bac)} differs from the per-row bac sum {_money(sum_bac)}; "
                 "the TOTAL forecast uses --bac")
            notes.append(f"--bac {_money(override_bac)} differs from the per-row bac sum {_money(sum_bac)}; the TOTAL uses --bac")
        elif missing_bac:
            notes.append("per-row bac missing for: " + ", ".join(missing_bac) + "; the TOTAL forecast uses --bac")
        if tot_ev > override_bac + 1e-9:
            raise ValueError(f"total EV {_money(tot_ev)} exceeds --bac {_money(override_bac)}; "
                             "check --bac or the per-row bac column")
    elif not missing_bac:
        total_bac = sum_bac
    else:
        total_bac = None
        if sum_bac is None:
            forecast_note = "no BAC supplied (add a bac column or pass --bac TOTAL)"
        else:
            forecast_note = "bac missing for: " + ", ".join(missing_bac) + " (fill the column or pass --bac TOTAL)"

    total = evm(tot_pv, tot_ev, tot_ac, total_bac, method, green, amber)
    total["task"] = "TOTAL"
    total["period"] = period

    realism = None
    if total["tcpi_bac"] is not None and total["cpi"] is not None:
        gap = total["tcpi_bac"] - total["cpi"]
        if gap > tcpi_warn:
            verdict = "re-plan or re-baseline"
        elif gap > 0:
            verdict = "within reach"
        else:
            verdict = "achievable at today's efficiency"
        realism = {"gap": gap, "verdict": verdict}

    summary = {
        "period": period or None,
        "periods_seen": [p for p, _ in snapshots] if has_period else [],
        "values": "incremental, accumulated" if incremental else "cumulative-to-date",
        "total": total,
        "rag": total["rag"],
        "thresholds": {"green": green, "amber": amber, "tcpi_warn": tcpi_warn},
        "eac_method": method,
        "forecast_note": forecast_note,
        "realism": realism,
        "trend": period_trends(snapshots, green, amber) if has_period else [],
        "notes": notes,
    }
    return {"rows": rows, "summary": summary}


# ----------------------------------------------------------------------------- renderers
HEADERS = ["Task", "PV", "EV", "AC", "CV", "SV", "CPI", "SPI", "EAC", "VAC", "RAG"]


def _row_cells(m):
    return [
        _sanitize(m["task"], TASK_WIDTH),
        _money(m["pv"]), _money(m["ev"]), _money(m["ac"]),
        _money(m["cv"]), _money(m["sv"]),
        _idx(m["cpi"]), _idx(m["spi"]),
        _money(m["eac"]), _money(m["vac"]),
        m["rag"],
    ]


def _overrun_label(vac, bac):
    if abs(vac) <= TOLERANCE:
        return "on budget"
    verb = "overrun" if vac < 0 else "underrun"
    return f"{verb} of {_pct(abs(vac) / bac * 100.0)} of BAC"


def _summary_lines(result):
    s, t = result["summary"], result["summary"]["total"]
    th = s["thresholds"]
    out = []
    if s["period"]:
        seen = ", ".join(s["periods_seen"])
        out.append(f"Headline period: {s['period']} (latest of {seen}; values {s['values']})")
    cpi = _idx(t["cpi"]) or "n/a"
    spi = _idx(t["spi"]) or "n/a"
    out.append(f"Overall status: {t['rag']}   (CPI={cpi}, SPI={spi}; GREEN when both >= {th['green']:.2f}, "
               f"RED when either < {th['amber']:.2f}, else AMBER)")
    if t["pct_complete"] is not None:
        out.append(f"Progress:       {_pct(t['pct_complete'])} complete (EV / BAC), "
                   f"{_pct(t['pct_spent'])} of BAC spent (AC / BAC); BAC {_money(t['bac'])}")
    if t["bac"] is None:
        out.append(f"Forecast:       n/a - {s['forecast_note']}")
    else:
        head = t["eac_method"]
        if t["eac"] is None:
            why = "CPI is 0 (nothing earned yet)" if head == "cpi" else "CPI x SPI is 0 or undefined"
            out.append(f"Forecast ({head}):  EAC undefined - {why}; try --eac-method atypical")
        else:
            out.append(f"Forecast ({head}: EAC = {METHOD_LABEL[head]}):  EAC={_money(t['eac'])}  "
                       f"ETC={_money(t['etc'])}  VAC={_money(t['vac'])} ({_overrun_label(t['vac'], t['bac'])})")
        if s["eac_method"] == "all":
            eacs = [f"{_money(t['eac_by'][k]) if t['eac_by'][k] is not None else 'undefined'} ({k})" for k in METHODS]
            vacs = [f"{_money(t['bac'] - t['eac_by'][k]) if t['eac_by'][k] is not None else 'undefined'}" for k in METHODS]
            out.append("Forecast range: EAC " + " / ".join(eacs))
            out.append("                VAC " + " / ".join(vacs)
                       + "   [atypical = one-off variance, cpi = cost trend continues, composite = cost and schedule trends compound]")
        tcpi_bac = _idx(t["tcpi_bac"]) or "n/a (AC has reached BAC)"
        tcpi_eac = _idx(t["tcpi_eac"]) or "n/a"
        line = f"To-complete:    TCPI(BAC)={tcpi_bac}  TCPI(EAC)={tcpi_eac}  CPI to date={cpi}"
        if s["realism"]:
            gap = s["realism"]["gap"]
            if s["realism"]["verdict"] == "re-plan or re-baseline":
                line += (f"  -> the remaining work must run {gap:+.2f} more efficiently than to date to land on BAC "
                         f"(gap > {th['tcpi_warn']:.2f}): re-plan or re-baseline")
            elif s["realism"]["verdict"] == "within reach":
                line += f"  -> BAC within reach ({gap:+.2f} efficiency needed on the remaining work)"
            else:
                line += "  -> BAC achievable at today's efficiency"
        out.append(line)
    for n in s["notes"]:
        out.append(f"Note:           {n}")
    if any(m["rag"].endswith("*") for m in result["rows"]):
        out.append("*  rated on one index only; the other is undefined (0/0).")
    return out


def _trend_table(trend):
    headers = ["Period", "PV", "EV", "AC", "CPI", "SPI", "RAG", "CPI trend", "SPI trend"]
    rows = [[e["period"], _money(e["pv"]), _money(e["ev"]), _money(e["ac"]), _idx(e["cpi"]) or "n/a",
             _idx(e["spi"]) or "n/a", e["rag"], e["cpi_trend"], e["spi_trend"]] for e in trend]
    return headers, rows, {0, 6, 7, 8}


def _curve_lines(trend, bac):
    peak = max([bac or 0.0] + [max(e["pv"], e["ev"], e["ac"]) for e in trend])
    if peak <= 0:
        return ["S-curve / burn line: nothing planned, earned or spent yet."]
    unit = peak / CURVE_WIDTH
    title = f"S-curve / burn line (cumulative; 1 column = {_money(unit)}"
    title += f"; BAC {_money(bac)} = full width):" if bac else "; peak = full width):"
    lines = [title]
    width = max(len(e["period"]) for e in trend)
    for e in trend:
        for label, key, ch in (("PV", "pv", "#"), ("EV", "ev", "="), ("AC", "ac", "$")):
            n = int(round(e[key] / peak * CURVE_WIDTH))
            head = e["period"].rjust(width) if key == "pv" else " " * width
            lines.append(f"  {head}  {label} |{ch * n}{' ' * (CURVE_WIDTH - n)}| {_money(e[key])}")
    return lines


def _aligned(headers, rows, left):
    widths = [max(len(h), *(len(r[c]) for r in rows)) for c, h in enumerate(headers)]

    def line(cells):
        return "  ".join(c.ljust(widths[i]) if i in left else c.rjust(widths[i]) for i, c in enumerate(cells)).rstrip()

    return line, widths


def render_table(result):
    body = [_row_cells(m) for m in result["rows"]]
    total_row = _row_cells(result["summary"]["total"])
    line, widths = _aligned(HEADERS, body + [total_row], {0, len(HEADERS) - 1})
    out = [f"Earned-value health check (values cumulative to the status date; EAC method: {result['summary']['eac_method']})"]
    out += [line(HEADERS), line(["-" * w for w in widths])]
    out += [line(r) for r in body]
    out.append(line(["-" * w for w in widths]))
    out.append(line(total_row))
    out.append("")
    out += _summary_lines(result)
    trend = result["summary"]["trend"]
    if trend:
        out.append("")
        out.append("CPI / SPI trend by period (cumulative to each status date):")
        th, tr, tl = _trend_table(trend)
        tline, tw = _aligned(th, tr, tl)
        out += [tline(th), tline(["-" * w for w in tw])]
        out += [tline(r) for r in tr]
        out.append("")
        out += _curve_lines(trend, result["summary"]["total"]["bac"])
    return "\n".join(out)


def _md_table(headers, rows, left):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(":---" if i in left else "---:" for i in range(len(headers))) + "|"]
    for r in rows:
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
    return out


def render_md(result):
    body = [_row_cells(m) for m in result["rows"]]
    total_row = [f"**{c}**" if c else c for c in _row_cells(result["summary"]["total"])]
    out = [f"## Earned-value health check (EAC method: {result['summary']['eac_method']})", ""]
    out += _md_table(HEADERS, body + [total_row], {0, len(HEADERS) - 1})
    out += ["", "```"] + _summary_lines(result) + ["```"]
    trend = result["summary"]["trend"]
    if trend:
        out += ["", "### CPI / SPI trend by period", ""]
        th, tr, tl = _trend_table(trend)
        out += _md_table(th, tr, tl)
        out += ["", "```"] + _curve_lines(trend, result["summary"]["total"]["bac"]) + ["```"]
    return "\n".join(out)


CSV_COLUMNS = ["task", "period", "pv", "ev", "ac", "bac", "cv", "sv", "cpi", "spi", "pct_complete", "pct_spent",
               "eac_method", "eac", "etc", "vac", "tcpi_bac", "tcpi_eac", "rag", "note"]


def render_csv(result):
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=CSV_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for m in result["rows"] + [result["summary"]["total"]]:
        row = {c: m.get(c, "") for c in CSV_COLUMNS}
        for c in ("pv", "ev", "ac", "bac", "cv", "sv", "cpi", "spi", "pct_complete", "pct_spent",
                  "eac", "etc", "vac", "tcpi_bac", "tcpi_eac"):
            row[c] = _plain(m.get(c))
        row["task"] = _sanitize(m["task"])
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
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="health_check.py",
        description="Earned-value health check: CV/SV, CPI/SPI, EAC/ETC/VAC, TCPI, percent complete/spent, "
                    "a RAG verdict, and a CPI/SPI trend with a text S-curve when rows carry a period.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("path", help="CSV or JSON of work-package rows (pv, ev, ac[, bac][, period]), or '-' for stdin")
    parser.add_argument("--json", action="store_true",
                        help="parse the input as JSON (default: CSV); required for every JSON input")
    parser.add_argument("--bac", type=float, metavar="TOTAL",
                        help="budget at completion for the TOTAL; needed when rows have no bac column, "
                             "warned about when it disagrees with the per-row bac sum")
    parser.add_argument("--green", type=float, default=0.95, metavar="X",
                        help="GREEN when BOTH CPI and SPI are >= X (default 0.95)")
    parser.add_argument("--amber", type=float, default=0.85, metavar="Y",
                        help="RED when EITHER CPI or SPI is < Y; between Y and --green is AMBER (default 0.85)")
    parser.add_argument("--eac-method", choices=("cpi", "atypical", "composite", "all"), default="cpi",
                        help="forecast formula: cpi = BAC / CPI (default), atypical = AC + (BAC - EV), "
                             "composite = AC + (BAC - EV) / (CPI x SPI), all = print the three as a range")
    parser.add_argument("--tcpi-warn", type=float, default=0.10, metavar="GAP",
                        help="flag 're-plan or re-baseline' when TCPI(BAC) exceeds the CPI to date by more than GAP "
                             "(default 0.10)")
    parser.add_argument("--incremental", action="store_true",
                        help="rows with a period column hold per-period increments, not cumulative-to-date values; "
                             "they are accumulated in period order (needs a task column)")
    parser.add_argument("--sort", choices=("input", "worst"), default="input",
                        help="row order: input (default) or worst (lowest CPI/SPI first)")
    parser.add_argument("--format", choices=("table", "json", "csv", "md"), default="table",
                        help="output format: table (default), json (rows + summary), csv (rows + TOTAL with every "
                             "computed field), md (markdown table + summary)")
    args = parser.parse_args(argv)

    if args.bac is not None and (not math.isfinite(args.bac) or args.bac <= 0):
        parser.error(f"--bac must be a positive finite number (got {args.bac})")
    for flag, v in (("--green", args.green), ("--amber", args.amber)):
        if not math.isfinite(v) or not (0 < v <= 1.5):
            parser.error(f"{flag} must be a finite index threshold between 0 and 1.5 (got {v})")
    if args.amber > args.green:
        parser.error(f"--amber ({args.amber}) must be <= --green ({args.green})")
    if not math.isfinite(args.tcpi_warn) or args.tcpi_warn < 0:
        parser.error(f"--tcpi-warn must be a finite number >= 0 (got {args.tcpi_warn})")

    def warn(msg):
        print(msg, file=sys.stderr)

    if args.amber == args.green:
        warn(f"warning: --amber == --green ({args.green}); the AMBER band is empty")

    try:
        text = read_text(args.path)
        rows, headers = load_rows(text, args.json, JSON_KEY)
        require_columns(headers, [PV_ALIASES, EV_ALIASES, AC_ALIASES])
        records, has_period = parse_records(rows, headers)
        if args.incremental:
            if not has_period:
                raise ValueError("--incremental needs a period column (period / month / sprint / as_of)")
            if not _has_column(headers, TASK_ALIASES):
                raise ValueError("--incremental needs a task column to accumulate each work package by")
        result = analyse(records, has_period, args.incremental, args.bac, args.eac_method,
                         args.green, args.amber, args.tcpi_warn, args.sort, warn)
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
