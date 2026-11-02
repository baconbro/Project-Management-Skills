#!/usr/bin/env python3
"""Velocity, predictability, burnup and a release forecast from sprint history.

Reads one row per sprint (committed and completed story points, optional dates and
release scope), prints the per-sprint table, velocity statistics, predictability, a
three-scenario forecast of the sprints the remaining work needs, an optional
fixed-date check with a priority cut line, and a text burnup. Standard library only.

SPRINT HISTORY COLUMNS / KEYS  (case-insensitive; one row per sprint, oldest first)
    sprint            sprint name               aliases: sprint_name, sprint_id, iteration, name, id   (optional; default S1, S2, ...)
    committed_points  points committed at sprint planning
                                                aliases: committed, commitment, planned_points, planned (optional;
                                                when present, every completed sprint needs a value)
    completed_points  points of stories that met the definition of done and were accepted
                                                aliases: completed, velocity, done_points, done, accepted_points, delivered, actual (required)
    start, end        sprint dates, YYYY-MM-DD  aliases: start_date, sprint_start / end_date, sprint_end, finish (optional, both or neither)
    release_scope     total release scope in points at the END of that sprint (drives the burnup and the remaining work)
                                                aliases: scope, scope_points, total_scope, release_points (optional;
                                                a blank cell repeats the previous sprint's scope)
    sprint_goal       carried into the JSON/CSV output             aliases: goal
  Points are numbers >= 0 (decimals allowed); '$' and a trailing '%' are stripped, ',' is read as a
  thousands separator ('1,000' -> 1000) or a decimal comma ('2,5' -> 2.5), and '1.000,50' is refused. Only the
  LAST rows may leave completed_points blank: they are unfinished (in-progress or planned) sprints,
  shown but excluded from every statistic. Rows must be in sprint order; dated sprints must not overlap.
  CSV delimiter is auto-detected (, ; tab |); a UTF-8 BOM and CRLF line ends are tolerated. JSON is a list
  of objects or {"sprints": [...]}; a .json file is parsed as JSON automatically, otherwise pass --json.

PRODUCT BACKLOG (--backlog FILE; CSV, or JSON as a list or {"items": [...]}, detected from the content)
    id (story_id, key, ref) - points (story_points, estimate, size, sp; REQUIRED) - priority (moscow, rank,
    prio) - status (state) - story (title, summary, name)
  Open items = status not done/accepted/closed/complete/completed/released/resolved and not
  removed/cancelled/canceled/deferred/rejected/obsolete/duplicate; no status column = every item open.
  Priority is MoSCoW (Must/Should/Could/Won't, or M/S/C/W), High/Medium/Low, or a numeric rank (1 = first);
  Won't items are outside the release. Open items with blank points are unsized: listed, not counted.
  Items are taken in priority order, then file order within a priority.

FORMULAS
  delivered %        completed / committed x 100 per sprint; flagged when below --floor (default 80)
  predictability     sum(completed) / sum(committed) x 100 over completed sprints (the say/do ratio)
  velocity           mean, median, sample std dev, CV = std / mean, min, max, trailing-N mean (N = --window, default 3)
  remaining          --remaining N, else open sized points in --backlog, else last release_scope - cumulative completed
  scenarios          the mean, trailing-N mean and minimum velocities, sorted high to low, are labelled
                     optimistic / likely / pessimistic
  sprints needed     ceil(remaining / velocity), exact value shown too; velocity 0 = never
  finish date        end of the last completed sprint + sprints x cadence (median days between sprint starts,
                     or --sprint-days); needs start/end dates
  fixed date         --sprints-left N: capacity = velocity x N per scenario, shortfall = remaining - capacity;
                     with --backlog the cut line is drawn after the last item that fits in priority order
  release outlook    GREEN pessimistic forecast fits in N sprints - AMBER likely fits, pessimistic does not -
                     RED likely does not fit (or likely velocity is 0)
  scope growth       (last release_scope - first) / (sprints - 1); a positive rate is reported as a note
  burnup             per sprint: cumulative completed (#) against release scope (|), remaining shown as dots

  Story points are a team-relative sizing unit, not money: never use them as earned value directly
  (see the agile-delivery references for the per-work-package conversion).

EXIT CODES   0 success  -  2 bad input, bad option or internal error ("error: ..." on stderr)

EXAMPLES
  python .claude/skills/agile-delivery/scripts/velocity_forecast.py .claude/skills/agile-delivery/assets/sprint-history-sample.csv
  python .claude/skills/agile-delivery/scripts/velocity_forecast.py .claude/skills/agile-delivery/assets/sprint-history-sample.csv --backlog .claude/skills/agile-delivery/assets/product-backlog-sample.csv --sprints-left 4
  python .claude/skills/agile-delivery/scripts/velocity_forecast.py history.csv --remaining 120 --window 4 --format md
  python .claude/skills/agile-delivery/scripts/velocity_forecast.py history.json --json --format json
  cat history.csv | python .claude/skills/agile-delivery/scripts/velocity_forecast.py - --remaining 80
"""
from __future__ import annotations

import argparse
import csv
import datetime
import io
import json
import math
import re
import statistics
import sys

BOM = "﻿"
JSON_KEY = "sprints"
BACKLOG_JSON_KEY = "items"
MAX_POINTS = 99_999.0
MAX_REMAINING = 999_999.0
MAX_SPRINTS_FOR_DATES = 10_000
BAR_WIDTH = 40
NAME_WIDTH = 24
CV_WARN = 25.0
MAX_TIERS = 12

SPRINT_ALIASES = ("sprint", "sprint_name", "sprint_id", "iteration", "name", "id")
COMMITTED_ALIASES = ("committed_points", "committed", "commitment", "planned_points", "planned")
COMPLETED_ALIASES = ("completed_points", "completed", "velocity", "done_points", "done",
                     "accepted_points", "delivered", "actual")
START_ALIASES = ("start", "start_date", "sprint_start")
END_ALIASES = ("end", "end_date", "sprint_end", "finish")
SCOPE_ALIASES = ("release_scope", "scope", "scope_points", "total_scope", "release_points")
GOAL_ALIASES = ("sprint_goal", "goal")

B_ID_ALIASES = ("id", "story_id", "key", "ref")
B_TITLE_ALIASES = ("story", "title", "summary", "name")
B_POINTS_ALIASES = ("points", "story_points", "estimate", "size", "sp")
B_PRIORITY_ALIASES = ("priority", "moscow", "rank", "prio")
B_STATUS_ALIASES = ("status", "state")

DONE_STATES = {"done", "accepted", "closed", "complete", "completed", "released", "resolved"}
DROPPED_STATES = {"removed", "cancelled", "canceled", "deferred", "rejected", "obsolete", "duplicate"}
MOSCOW = {"must": 1, "must have": 1, "m": 1, "should": 2, "should have": 2, "s": 2,
          "could": 3, "could have": 3, "c": 3, "won't": 4, "wont": 4, "won't have": 4,
          "wont have": 4, "will not": 4, "w": 4}
MOSCOW_LABELS = {1: "Must", 2: "Should", 3: "Could", 4: "Won't"}
HML = {"high": 1, "medium": 2, "med": 2, "low": 3}
HML_LABELS = {1: "High", 2: "Medium", 3: "Low"}
UNPRIORITIZED = "(no priority)"


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
        raise ValueError(f"{where}: {raw!r} is above the maximum {maximum:g}")
    return v


def has_column(headers, aliases):
    present = {h.lower().lstrip(BOM).strip() for h in headers if h}
    return any(a.lower() in present for a in aliases)


def _date(raw, where):
    s = str(raw).strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        try:
            return datetime.date.fromisoformat(s)
        except ValueError:
            pass
    raise ValueError(f"{where}: {raw!r} is not a calendar date in YYYY-MM-DD form "
                     f"(spreadsheets often reformat dates; re-export them as ISO dates)")


# ----------------------------------------------------------------------------- formatting helpers
def _sanitize(value, width=None):
    """Collapse whitespace/newlines; truncate with an ellipsis when width is given."""
    s = re.sub(r"\s+", " ", str(value if value is not None else "")).strip()
    if width and len(s) > width:
        s = s[: width - 1] + "…"
    return s


def _fmt(x, places=2):
    if x is None:
        return "n/a"
    s = f"{x:,.{places}f}"
    zero = "0." + "0" * places if places else "0"
    return zero if s.lstrip("-") == zero else s


def _pts(x):
    """Points: whole numbers without decimals, otherwise two decimals."""
    if x is None:
        return "n/a"
    if abs(x - round(x)) < 1e-9:
        return f"{int(round(x)):,}"
    return _fmt(x)


def _pct(x):
    return "n/a" if x is None else _fmt(x, 1) + "%"


def _day(d):
    return d.isoformat() if d else ""


def _plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")


# ----------------------------------------------------------------------------- sprint history
def parse_history(rows, headers):
    """Validate the sprint rows and derive cumulative / remaining figures per completed sprint."""
    require_columns(headers, [COMPLETED_ALIASES])
    has_committed = has_column(headers, COMMITTED_ALIASES)
    has_start, has_end = has_column(headers, START_ALIASES), has_column(headers, END_ALIASES)
    if has_start != has_end:
        raise ValueError("give both a start and an end column (or neither); found only "
                         + ("start" if has_start else "end"))
    has_dates = has_start and has_end
    has_scope = has_column(headers, SCOPE_ALIASES)

    sprints, seen = [], {}
    first_open = None
    prev_scope = None
    cumulative = 0.0
    for i, row in enumerate(rows, start=1):
        name = _sanitize(_get(row, *SPRINT_ALIASES, default="")) or f"S{i}"
        where = f"row {i} ({name})"
        key = name.lower()
        if key in seen:
            raise ValueError(f"{where}, column sprint: duplicate sprint name (first used in row {seen[key]})")
        seen[key] = i

        raw_done = _get(row, *COMPLETED_ALIASES)
        completed = None if raw_done is None else _num(raw_done, f"{where}, column completed_points",
                                                       minimum=0, maximum=MAX_POINTS)
        if completed is None and first_open is None:
            first_open = (i, name)
        elif completed is not None and first_open is not None:
            raise ValueError(f"{where}: has completed points but an earlier sprint (row {first_open[0]}, "
                             f"{first_open[1]}) has none; only the last sprints may be unfinished")

        committed = None
        if has_committed:
            raw = _get(row, *COMMITTED_ALIASES)
            if raw is not None:
                committed = _num(raw, f"{where}, column committed_points", minimum=0, maximum=MAX_POINTS)
            elif completed is not None:
                raise ValueError(f"{where}, column committed_points: value is missing for a completed sprint")

        start = end = None
        if has_dates:
            raw_s, raw_e = _get(row, *START_ALIASES), _get(row, *END_ALIASES)
            if raw_s is None or raw_e is None:
                missing = "start" if raw_s is None else "end"
                raise ValueError(f"{where}, column {missing}: date is missing (fill start and end for every "
                                 f"sprint, or remove both columns)")
            start, end = _date(raw_s, f"{where}, column start"), _date(raw_e, f"{where}, column end")
            if end < start:
                raise ValueError(f"{where}: end {end} is before start {start}")
            if sprints and sprints[-1]["end"] and start <= sprints[-1]["end"]:
                raise ValueError(f"{where}: starts {start}, on or before the previous sprint ends "
                                 f"({sprints[-1]['end']}); rows must be in sprint order without overlap")

        scope = None
        if has_scope:
            raw = _get(row, *SCOPE_ALIASES)
            if raw is not None:
                scope = _num(raw, f"{where}, column release_scope", minimum=0, maximum=MAX_REMAINING)
            elif prev_scope is not None:
                scope = prev_scope
            elif completed is not None:
                raise ValueError(f"{where}, column release_scope: value is missing in the first sprint "
                                 f"(later blank cells repeat the previous sprint's scope)")
            if scope is not None:
                prev_scope = scope

        sprint = {
            "sprint": name,
            "start": start,
            "end": end,
            "status": "completed" if completed is not None else "unfinished",
            "committed": committed,
            "completed": completed,
            "pct_delivered": None,
            "flag": "",
            "cumulative": None,
            "scope": scope,
            "remaining": None,
            "goal": _sanitize(_get(row, *GOAL_ALIASES, default="")),
        }
        if completed is not None:
            cumulative = round(cumulative + completed, 6)
            sprint["cumulative"] = cumulative
            if committed is not None and committed > 0:
                sprint["pct_delivered"] = round(completed / committed * 100.0, 6)
            if scope is not None:
                if scope + 1e-9 < cumulative:
                    raise ValueError(f"{where}, column release_scope: {_pts(scope)} is below the cumulative "
                                     f"completed points ({_pts(cumulative)}); scope is the TOTAL release "
                                     f"scope, done plus remaining")
                sprint["remaining"] = round(scope - cumulative, 6)
        sprints.append(sprint)

    done = [s for s in sprints if s["status"] == "completed"]
    if not done:
        raise ValueError("no completed sprints: fill completed_points for every finished sprint")
    return sprints, {"has_committed": has_committed, "has_dates": has_dates, "has_scope": has_scope}


def cadence_days(sprints, override):
    """Calendar days per sprint: --sprint-days, else the median gap between sprint starts."""
    if override:
        return override, "--sprint-days"
    starts = [s["start"] for s in sprints if s["start"]]
    if len(starts) >= 2:
        gaps = [(b - a).days for a, b in zip(starts, starts[1:])]
        return int(round(statistics.median(gaps))), "median gap between sprint starts"
    dated = [s for s in sprints if s["start"]]
    if dated:
        length = (dated[0]["end"] - dated[0]["start"]).days + 1
        return int(math.ceil(length / 7.0) * 7), "single sprint length rounded up to whole weeks"
    return None, None


# ----------------------------------------------------------------------------- product backlog
def _priority(raw, where):
    """Return (scale, tier_number, label) for a priority cell."""
    if raw is None:
        return None, None, UNPRIORITIZED
    s = _sanitize(raw).lower().replace("’", "'")
    if s in MOSCOW:
        n = MOSCOW[s]
        return "moscow", n, MOSCOW_LABELS[n]
    if s in HML:
        n = HML[s]
        return "hml", n, HML_LABELS[n]
    try:
        v = _num(s, where, minimum=0)
    except ValueError:
        raise ValueError(f"{where}: {raw!r} is not a priority; use Must/Should/Could/Won't, "
                         f"High/Medium/Low, or a numeric rank (1 = first)")
    return "rank", v, f"rank {_pts(v)}"


def parse_backlog(rows, headers):
    require_columns(headers, [B_POINTS_ALIASES])
    has_status = has_column(headers, B_STATUS_ALIASES)
    items, scales = [], set()
    for i, row in enumerate(rows, start=1):
        ident = _sanitize(_get(row, *B_ID_ALIASES, default="")) or f"item {i}"
        where = f"backlog row {i} ({ident})"
        status = _sanitize(_get(row, *B_STATUS_ALIASES, default="")).lower()
        scale, tier, label = _priority(_get(row, *B_PRIORITY_ALIASES), f"{where}, column priority")
        if scale:
            scales.add(scale)
        raw_pts = _get(row, *B_POINTS_ALIASES)
        points = None if raw_pts is None else _num(raw_pts, f"{where}, column points", minimum=0, maximum=MAX_POINTS)
        if status in DONE_STATES:
            state = "done"
        elif status in DROPPED_STATES or (scale == "moscow" and tier == 4):
            state = "excluded"
        else:
            state = "open"
        items.append({"id": ident, "title": _sanitize(_get(row, *B_TITLE_ALIASES, default="")),
                      "points": points, "status": status or "", "state": state,
                      "scale": scale, "tier": tier, "label": label, "order": i})
    if len(scales) > 1:
        raise ValueError(f"backlog priority mixes scales {sorted(scales)}; use one of MoSCoW, "
                         f"High/Medium/Low, or numeric ranks")

    open_items = [it for it in items if it["state"] == "open"]
    sized = [it for it in open_items if it["points"] is not None]
    ordered = sorted(sized, key=lambda it: (it["tier"] is None, it["tier"] if it["tier"] is not None else 0,
                                            it["order"]))
    tiers = []
    for it in ordered:
        if not tiers or tiers[-1]["label"] != it["label"]:
            tiers.append({"label": it["label"], "points": 0.0, "items": 0})
        tiers[-1]["points"] = round(tiers[-1]["points"] + it["points"], 6)
        tiers[-1]["items"] += 1
    running = 0.0
    for t in tiers:
        running = round(running + t["points"], 6)
        t["cumulative"] = running
    return {
        "has_status": has_status,
        "open_points": round(math.fsum(it["points"] for it in sized), 6),
        "open_items": len(sized),
        "ordered": ordered,
        "tiers": tiers,
        "unsized": [it["id"] for it in open_items if it["points"] is None],
        "excluded": [{"id": it["id"], "points": it["points"], "reason": it["status"] or it["label"]}
                     for it in items if it["state"] == "excluded"],
        "done_points": round(math.fsum(it["points"] or 0.0 for it in items if it["state"] == "done"), 6),
        "order_differs": [it["order"] for it in ordered] != sorted(it["order"] for it in ordered),
    }


# ----------------------------------------------------------------------------- analysis
def sprints_needed(remaining, velocity):
    """Return (exact, whole) sprints; (None, None) when the velocity is zero and work remains."""
    if remaining <= 0:
        return 0.0, 0
    if velocity <= 0:
        return None, None
    exact = round(remaining / velocity, 6)
    return exact, int(math.ceil(exact))


def _add_sprints(anchor, sprints, cadence):
    if anchor is None or cadence is None or sprints is None or sprints > MAX_SPRINTS_FOR_DATES:
        return None
    try:
        return anchor + datetime.timedelta(days=sprints * cadence)
    except OverflowError:
        return None


def cut_line(ordered, capacity):
    """Longest prefix of the ordered open items that fits within capacity."""
    total, last = 0.0, None
    fitted = 0
    for it in ordered:
        if round(total + it["points"], 6) > capacity + 1e-9:
            break
        total = round(total + it["points"], 6)
        last = it["id"]
        fitted += 1
    below = ordered[fitted:]
    return {"cut_after": last, "points_above": total, "items_below": [it["id"] for it in below],
            "points_below": round(math.fsum(it["points"] for it in below), 6)}


def analyse(sprints, flags, args, backlog):
    done = [s for s in sprints if s["status"] == "completed"]
    unfinished = [s["sprint"] for s in sprints if s["status"] != "completed"]
    v = [s["completed"] for s in done]
    n = len(v)
    mean = round(math.fsum(v) / n, 6)
    window = min(args.window, n)
    trailing = round(math.fsum(v[-window:]) / window, 6)
    std = statistics.stdev(v) if n >= 2 else None
    cv = (std / mean * 100.0) if (std is not None and mean > 0) else None
    i_min = min(range(n), key=lambda k: v[k])
    i_max = max(range(n), key=lambda k: v[k])
    notes = []

    pred = None
    if flags["has_committed"]:
        tot_c = round(math.fsum(s["committed"] for s in done), 6)
        tot_d = round(math.fsum(v), 6)
        for s in done:
            if s["pct_delivered"] is not None:
                if s["pct_delivered"] < args.floor - 1e-9:
                    s["flag"] = f"below {_fmt(args.floor, 0)}% floor"
                elif s["pct_delivered"] > 100 + 1e-9:
                    s["flag"] = "pulled in extra work"
            elif s["completed"] > 0:
                s["flag"] = "nothing committed"
        below = [s["sprint"] for s in done if s["flag"].startswith("below")]
        pred = {"committed": tot_c, "completed": tot_d,
                "pct": round(tot_d / tot_c * 100.0, 6) if tot_c > 0 else None,
                "floor_pct": args.floor, "below_floor": below}
    else:
        notes.append("No committed column: predictability (completed / committed) is not computed.")

    cadence, cadence_src = cadence_days(sprints, args.sprint_days)
    anchor = done[-1]["end"]
    if args.sprint_days and not flags["has_dates"]:
        notes.append("--sprint-days needs start/end dates to anchor finish dates; none projected.")

    # remaining work
    remaining, source = None, None
    scope_remaining = done[-1]["remaining"] if flags["has_scope"] else None
    if args.remaining is not None:
        remaining, source = args.remaining, "--remaining"
    elif backlog is not None:
        remaining, source = backlog["open_points"], "open sized items in the backlog"
    elif scope_remaining is not None:
        remaining, source = scope_remaining, f"release_scope column after {done[-1]['sprint']}"
    if remaining is not None and scope_remaining is not None and source != f"release_scope column after {done[-1]['sprint']}":
        if abs(remaining - scope_remaining) > 1e-6:
            notes.append(f"Remaining from {source} ({_pts(remaining)}) differs from the release_scope column "
                         f"({_pts(scope_remaining)} after {done[-1]['sprint']}): reconcile the backlog and the burnup.")

    candidates = [("average", mean), (f"trailing-{args.window} average", trailing), ("minimum", float(v[i_min]))]
    order = sorted(range(3), key=lambda k: -candidates[k][1])
    scenarios = []
    for label, k in zip(("optimistic", "likely", "pessimistic"), order):
        basis, vel = candidates[k]
        sc = {"scenario": label, "basis": basis, "velocity": vel}
        if remaining is not None:
            exact, whole = sprints_needed(remaining, vel)
            sc.update({"sprints_exact": exact, "sprints": whole,
                       "finish": _add_sprints(anchor, whole, cadence)})
        scenarios.append(sc)

    fixed = None
    if args.sprints_left is not None and remaining is not None:
        left = args.sprints_left
        rows = []
        for sc in scenarios:
            capacity = round(sc["velocity"] * left, 6)
            row = {"scenario": sc["scenario"], "capacity": capacity,
                   "fits": remaining <= capacity + 1e-9,
                   "shortfall": round(max(0.0, remaining - capacity), 6)}
            if backlog is not None and args.remaining is None:
                row.update(cut_line(backlog["ordered"], capacity))
            rows.append(row)
        likely, pess = scenarios[1], scenarios[2]
        if remaining <= 0:
            outlook, reason = "GREEN", "no work remains"
        elif likely["sprints"] is None or likely["sprints"] > left:
            outlook = "RED"
            reason = ("the likely forecast needs " + ("an unbounded number of sprints" if likely["sprints"] is None
                      else f"{likely['sprints']} sprints") + f" but only {left} remain: cut scope or move the date "
                      f"through change control")
        elif pess["sprints"] is None or pess["sprints"] > left:
            outlook = "AMBER"
            reason = (f"the likely forecast fits in {left} sprints but the pessimistic one needs "
                      + ("an unbounded number" if pess["sprints"] is None else str(pess["sprints"]))
                      + ": keep enough low-priority scope below the cut line")
        else:
            outlook, reason = "GREEN", f"even the pessimistic forecast fits in {left} sprints"
        fixed = {"sprints_left": left, "release_by": _add_sprints(anchor, left, cadence),
                 "scenarios": rows, "outlook": outlook, "reason": reason}
    elif args.sprints_left is not None:
        notes.append("--sprints-left needs remaining work: pass --remaining, --backlog, or a release_scope column.")

    tiers = None
    if backlog is not None:
        tiers = []
        if len(backlog["tiers"]) > MAX_TIERS:
            notes.append(f"{len(backlog['tiers'])} distinct priority levels: the by-priority table is omitted "
                         f"(it is shown for up to {MAX_TIERS}); use the cut line, or group ranks into tiers.")
        else:
            for t in backlog["tiers"]:
                entry = {"through": t["label"], "points": t["points"], "cumulative": t["cumulative"],
                         "items": t["items"]}
                for sc in scenarios:
                    entry[sc["scenario"]] = sprints_needed(t["cumulative"], sc["velocity"])[1]
                tiers.append(entry)
        if backlog["unsized"]:
            notes.append(f"{_plural(len(backlog['unsized']), 'open backlog item')} without points not counted: "
                         f"{', '.join(backlog['unsized'])}. Size these in refinement; the remaining work is understated.")
        if backlog["order_differs"]:
            notes.append("The backlog file order differs from its priority order; the forecast follows priority, "
                         "then file order. Re-order the backlog so the two agree.")
        if not backlog["has_status"]:
            notes.append("The backlog has no status column: every item is treated as open.")

    # burnup data
    burn_scope_src = None
    if flags["has_scope"]:
        burn_scope_src = "release_scope column"
    elif remaining is not None:
        total = round(done[-1]["cumulative"] + remaining, 6)
        for s in done:
            s["scope"] = total
            s["remaining"] = round(total - s["cumulative"], 6)
        burn_scope_src = "constant scope assumed: cumulative done + remaining"

    growth = None
    if flags["has_scope"] and n >= 2 and done[0]["scope"] is not None:
        first, last = done[0]["scope"], done[-1]["scope"]
        rate = round((last - first) / (n - 1), 6)
        growth = {"first": first, "last": last, "per_sprint": rate}
        if rate > 0 and remaining:
            net = scenarios[1]["velocity"] - rate
            pct = (last - first) / first * 100.0 if first > 0 else None
            if net > 0:
                net_sprints = sprints_needed(remaining, net)[1]
                effect = f"the likely forecast becomes {net_sprints} sprints"
            else:
                effect = "the release never finishes at the likely velocity"
            notes.append(f"Release scope grew from {_pts(first)} to {_pts(last)} points"
                         + (f" (+{_fmt(pct, 1)}%)" if pct is not None else "")
                         + f", {_fmt(rate)} points per sprint. The forecast assumes no further growth; "
                         f"if growth continues at this rate, {effect}.")

    if n < 3:
        notes.append(f"Only {_plural(n, 'completed sprint')}: treat the forecast as low-confidence until there "
                     f"are at least 3.")
    if window < args.window:
        notes.append(f"The trailing-{args.window} average uses the {_plural(window, 'completed sprint')} available.")
    if cv is not None and cv > CV_WARN:
        notes.append(f"Velocity varies a lot (CV {_fmt(cv, 1)}%): quote the range, not the likely figure, and find "
                     f"the cause (team changes, unready stories, carry-over).")
    if v[i_min] == 0:
        notes.append(f"{done[i_min]['sprint']} completed 0 points, so the pessimistic forecast is unbounded; "
                     f"drop a cancelled sprint from the history.")
    if unfinished:
        notes.append(f"Unfinished sprint(s) excluded from the statistics: {', '.join(unfinished)}.")
    if remaining is None:
        notes.append("No remaining work given: pass --remaining N, --backlog FILE, or add a release_scope column "
                     "to forecast.")
    if not flags["has_dates"]:
        notes.append("No start/end dates: finish dates are not projected.")

    return {
        "sprints": sprints,
        "summary": {
            "completed_sprints": n,
            "unfinished_sprints": unfinished,
            "velocity": {"mean": mean, "median": float(statistics.median(v)), "std": std, "cv_pct": cv,
                         "min": float(v[i_min]), "min_sprint": done[i_min]["sprint"],
                         "max": float(v[i_max]), "max_sprint": done[i_max]["sprint"],
                         "trailing": trailing, "trailing_window": args.window,
                         "trailing_sprints": [s["sprint"] for s in done[-window:]]},
            "predictability": pred,
            "cadence_days": cadence if flags["has_dates"] or args.sprint_days else None,
            "cadence_source": cadence_src if flags["has_dates"] or args.sprint_days else None,
            "last_completed_end": anchor,
            "remaining": remaining,
            "remaining_source": source,
            "forecast": scenarios,
            "fixed_date": fixed,
            "backlog": None if backlog is None else {
                "open_points": backlog["open_points"], "open_items": backlog["open_items"],
                "done_points": backlog["done_points"], "unsized": backlog["unsized"],
                "excluded": backlog["excluded"], "by_priority": tiers},
            "scope_growth": growth,
            "burnup_scope_source": burn_scope_src,
            "notes": notes,
        },
    }


# ----------------------------------------------------------------------------- renderers
def _grid(headers, rows, left):
    widths = [max(len(h), *(len(r[c]) for r in rows)) if rows else len(h) for c, h in enumerate(headers)]

    def line(cells):
        return "  ".join(c.ljust(widths[i]) if i in left else c.rjust(widths[i])
                         for i, c in enumerate(cells)).rstrip()

    return [line(headers), line(["-" * w for w in widths])] + [line(r) for r in rows]


def _md_table(headers, rows, left):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(":---" if i in left else "---:" for i in range(len(headers))) + "|"]
    out += ["| " + " | ".join(c.replace("|", "\\|") for c in r) + " |" for r in rows]
    return out


def _history_table(result):
    sprints = result["sprints"]
    s = result["summary"]
    dated = any(sp["start"] for sp in sprints)
    committed = s["predictability"] is not None
    scoped = s["burnup_scope_source"] is not None
    headers = ["Sprint"] + (["Start", "End"] if dated else []) + (["Committed"] if committed else []) \
        + ["Completed"] + (["Delivered"] if committed else []) + ["Cum. done"] \
        + (["Scope", "Remaining"] if scoped else []) + ["Flag"]
    rows = []
    for sp in sprints:
        fin = sp["status"] == "completed"
        cells = [_sanitize(sp["sprint"], NAME_WIDTH)]
        if dated:
            cells += [_day(sp["start"]), _day(sp["end"])]
        if committed:
            cells.append(_pts(sp["committed"]) if sp["committed"] is not None else "")
        cells.append(_pts(sp["completed"]) if fin else "")
        if committed:
            cells.append(_pct(sp["pct_delivered"]) if fin else "")
        cells.append(_pts(sp["cumulative"]) if fin else "")
        if scoped:
            cells += [_pts(sp["scope"]) if fin and sp["scope"] is not None else "",
                      _pts(sp["remaining"]) if fin and sp["remaining"] is not None else ""]
        cells.append(sp["flag"] if fin else "unfinished (excluded)")
        rows.append(cells)
    left = {0, len(headers) - 1} | ({1, 2} if dated else set())
    return headers, rows, left


def _velocity_lines(s):
    v, p = s["velocity"], s["predictability"]
    window_names = v["trailing_sprints"]
    span = window_names[0] if len(window_names) == 1 else f"{window_names[0]}-{window_names[-1]}"
    lines = [
        ("Average (mean)", _fmt(v["mean"])),
        ("Median", _fmt(v["median"])),
        ("Min / max", f"{_pts(v['min'])} ({v['min_sprint']}) / {_pts(v['max'])} ({v['max_sprint']})"),
        (f"Trailing-{v['trailing_window']} average", f"{_fmt(v['trailing'])} ({span})"),
        ("Std dev / CV", f"{_fmt(v['std'])} / {_pct(v['cv_pct'])}" if v["std"] is not None else "n/a (one sprint)"),
    ]
    if p is not None:
        below = p["below_floor"]
        lines.append(("Predictability",
                      f"{_pct(p['pct'])} of committed points delivered ({_pts(p['completed'])} of "
                      f"{_pts(p['committed'])}); {len(below)} of {_plural(s['completed_sprints'], 'sprint')} below the "
                      f"{_fmt(p['floor_pct'], 0)}% floor" + (f" ({', '.join(below)})" if below else "")))
    if s["cadence_days"]:
        lines.append(("Sprint cadence", f"{s['cadence_days']} days ({s['cadence_source']})"))
    return lines


def _forecast_table(s):
    dated = s["last_completed_end"] is not None and s["cadence_days"]
    headers = ["Scenario", "Basis", "Velocity", "Sprints (exact)", "Sprints"] + (["Finishes"] if dated else [])
    rows = []
    for sc in s["forecast"]:
        never = sc["sprints"] is None
        cells = [sc["scenario"].capitalize(), sc["basis"], _fmt(sc["velocity"]),
                 "never" if never else _fmt(sc["sprints_exact"]), "never" if never else str(sc["sprints"])]
        if dated:
            cells.append(_day(sc["finish"]) or "n/a")
        rows.append(cells)
    return headers, rows, {0, 1}


def _fixed_table(fd):
    has_cut = any("cut_after" in r for r in fd["scenarios"])
    headers = ["Scenario", "Capacity", "Fits", "Shortfall"] + (["Cut line (last item in)", "Below the line"]
                                                              if has_cut else [])
    rows = []
    for r in fd["scenarios"]:
        cells = [r["scenario"].capitalize(), _pts(r["capacity"]), "yes" if r["fits"] else "no", _pts(r["shortfall"])]
        if has_cut:
            if not r["items_below"]:
                cut, below = (f"{r['cut_after']} (all fit)" if r["cut_after"] else "nothing open"), "none"
            else:
                cut = f"{r['cut_after'] or 'nothing fits'} ({_pts(r['points_above'])} pts)"
                below = f"{len(r['items_below'])} items, {_pts(r['points_below'])} pts"
            cells += [cut, below]
        rows.append(cells)
    return headers, rows, {0, 2} | ({4, 5} if has_cut else set())


def _tier_table(s):
    headers = ["Through", "Items", "Points", "Cumulative", "Optimistic", "Likely", "Pessimistic"]
    rows = []
    for t in s["backlog"]["by_priority"]:
        rows.append([t["through"], str(t["items"]), _pts(t["points"]), _pts(t["cumulative"])]
                    + ["never" if t[k] is None else str(t[k]) for k in ("optimistic", "likely", "pessimistic")])
    return headers, rows, {0}


def _burnup_lines(result):
    done = [sp for sp in result["sprints"] if sp["status"] == "completed"]
    scoped = result["summary"]["burnup_scope_source"] is not None
    top = max([sp["cumulative"] for sp in done] + ([sp["scope"] for sp in done if sp["scope"] is not None]
                                                   if scoped else []))
    name_w = max(len(_sanitize(sp["sprint"], NAME_WIDTH)) for sp in done)
    label_w = max(len(f"{_pts(sp['cumulative'])}/{_pts(sp['scope'])}" if scoped and sp["scope"] is not None
                      else _pts(sp["cumulative"])) for sp in done)
    out = []
    for sp in done:
        filled = int(round(sp["cumulative"] / top * BAR_WIDTH)) if top > 0 else 0
        if scoped and sp["scope"] is not None:
            end = int(round(sp["scope"] / top * BAR_WIDTH)) if top > 0 else 0
            bar = "#" * filled + "." * max(0, end - filled) + "|"
            label = f"{_pts(sp['cumulative'])}/{_pts(sp['scope'])}"
            pct = f"  {_pct(sp['cumulative'] / sp['scope'] * 100.0) if sp['scope'] > 0 else 'n/a'} done"
        else:
            bar, label, pct = "#" * filled, _pts(sp["cumulative"]), ""
        out.append(f"{_sanitize(sp['sprint'], NAME_WIDTH).ljust(name_w)}  {label.rjust(label_w)}  {bar}{pct}")
    return out


def _sections(result):
    """Yield (title, kind, payload) blocks shared by the table and markdown renderers."""
    s = result["summary"]
    blocks = []
    n_unf = len(s["unfinished_sprints"])
    blocks.append((f"Sprint history: {_plural(s['completed_sprints'], 'completed sprint')}"
                   + (f" + {n_unf} unfinished" if n_unf else "") + " (story points)", "table", _history_table(result)))
    blocks.append(("Velocity statistics (velocity = points completed per sprint)", "pairs", _velocity_lines(s)))
    if s["remaining"] is not None:
        blocks.append((f"Forecast: {_pts(s['remaining'])} points remaining ({s['remaining_source']})",
                       "table", _forecast_table(s)))
    fd = s["fixed_date"]
    if fd is not None:
        if fd["sprints_left"] == 0:
            title = "Fixed date: no sprints left before the release"
        else:
            title = f"Fixed date: {_plural(fd['sprints_left'], 'sprint')} left before the release" + (
                f" (the last one ends {_day(fd['release_by'])})" if fd["release_by"] else "")
        blocks.append((title, "table", _fixed_table(fd)))
        blocks.append((None, "text", [f"Release outlook: {fd['outlook']} - {fd['reason']}."]))
    if s["backlog"] is not None and s["backlog"]["by_priority"]:
        bl = s["backlog"]
        excl = bl["excluded"]
        title = (f"Release forecast by priority: sprints to finish everything through each priority "
                 f"({_plural(bl['open_items'], 'open sized item')}, {_pts(bl['open_points'])} pts"
                 + (f"; excluded: " + ", ".join(f"{e['id']} ({_pts(e['points']) + ' pts, ' if e['points'] is not None else ''}"
                                                f"{e['reason']})" for e in excl) if excl else "")
                 + ")")
        blocks.append((title, "table", _tier_table(s)))
    src = s["burnup_scope_source"]
    blocks.append(("Burnup: # cumulative completed, . remaining, | release scope"
                   + (f" ({src})" if src and src != "release_scope column" else ""), "burnup", _burnup_lines(result)))
    if s["notes"]:
        blocks.append(("Notes", "notes", s["notes"]))
    return blocks


def render_table(result):
    out = []
    for title, kind, payload in _sections(result):
        if title:
            out.append(title)
        if kind == "table":
            out += _grid(*payload)
        elif kind == "pairs":
            w = max(len(k) for k, _ in payload)
            out += [f"  {k.ljust(w)}  {val}" for k, val in payload]
        elif kind == "notes":
            out += [f"  - {n}" for n in payload]
        elif kind == "burnup":
            out += ["  " + ln for ln in payload]
        else:
            out += payload
        out.append("")
    return "\n".join(out).rstrip()


def render_md(result):
    out = []
    for title, kind, payload in _sections(result):
        if title:
            out += [f"### {title}", ""]
        if kind == "table":
            out += _md_table(*payload)
        elif kind == "pairs":
            out += [f"- **{k}:** {val}" for k, val in payload]
        elif kind == "notes":
            out += [f"- {n}" for n in payload]
        elif kind == "burnup":
            out += ["```"] + payload + ["```"]
        else:
            out += [f"**{payload[0]}**"]
        out.append("")
    return "\n".join(out).rstrip()


def render_csv(result):
    cols = ["sprint", "start", "end", "status", "committed", "completed", "pct_delivered", "flag",
            "cumulative", "scope", "remaining", "goal"]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=cols, lineterminator="\n")
    writer.writeheader()
    for sp in result["sprints"]:
        row = {}
        for c in cols:
            val = sp.get(c)
            if isinstance(val, datetime.date):
                val = val.isoformat()
            elif isinstance(val, float):
                val = f"{val:.4f}".rstrip("0").rstrip(".")
            row[c] = "" if val is None else val
        writer.writerow(row)
    return buf.getvalue().rstrip("\n")


def _jsonable(obj):
    if isinstance(obj, float):
        r = round(obj, 4)
        return 0.0 if r == 0 else r
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    return obj


def render_json(result):
    return json.dumps(_jsonable(result), indent=2, ensure_ascii=False, allow_nan=False)


RENDERERS = {"table": render_table, "json": render_json, "csv": render_csv, "md": render_md}


# ----------------------------------------------------------------------------- CLI
def _load(path, force_json, json_key):
    text = read_text(path)
    as_json = force_json or (path != "-" and path.lower().endswith(".json"))
    return load_rows(text, as_json, json_key)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="velocity_forecast.py",
        description="Velocity, predictability, burnup and a release forecast (optimistic / likely / "
                    "pessimistic sprints to finish) from sprint history.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("path", help="sprint history as CSV or JSON, or '-' for stdin (a .json extension selects JSON)")
    parser.add_argument("--json", action="store_true",
                        help="force JSON parsing of the sprint history (needed for JSON on stdin)")
    parser.add_argument("--remaining", metavar="N",
                        help="points still to deliver (overrides the release_scope column; not with --backlog)")
    parser.add_argument("--backlog", metavar="FILE",
                        help="product backlog CSV/JSON: sums the open sized points by priority and draws the cut line")
    parser.add_argument("--sprints-left", metavar="N", type=int,
                        help="sprints available before the release date: capacity, shortfall and cut line per "
                             "scenario, plus a GREEN/AMBER/RED release outlook")
    parser.add_argument("--window", metavar="N", type=int, default=3,
                        help="sprints in the trailing average (default 3, range 1-52)")
    parser.add_argument("--floor", metavar="PCT", default="80",
                        help="flag sprints that delivered less than this %% of their commitment (default 80, range 0-100)")
    parser.add_argument("--sprint-days", metavar="N", type=int,
                        help="calendar days per sprint for finish dates (default: median gap between sprint starts)")
    parser.add_argument("--format", choices=("table", "json", "csv", "md"), default="table",
                        help="output: table (default), json (sprints + summary), csv (per-sprint rows), "
                             "md (markdown for a sprint review or status report)")
    args = parser.parse_args(argv)

    if args.remaining is not None:
        try:
            args.remaining = _num(args.remaining, "--remaining", minimum=0, maximum=MAX_REMAINING)
        except ValueError as exc:
            parser.error(str(exc))
    if args.remaining is not None and args.backlog:
        parser.error("use either --remaining or --backlog, not both")
    if args.sprints_left is not None and not 0 <= args.sprints_left <= 1000:
        parser.error(f"--sprints-left must be between 0 and 1000 (got {args.sprints_left})")
    if not 1 <= args.window <= 52:
        parser.error(f"--window must be between 1 and 52 (got {args.window})")
    try:
        args.floor = _num(args.floor, "--floor", minimum=0, maximum=100)
    except ValueError as exc:
        parser.error(str(exc))
    if args.sprint_days is not None and not 1 <= args.sprint_days <= 366:
        parser.error(f"--sprint-days must be between 1 and 366 (got {args.sprint_days})")
    if args.backlog == "-" and args.path == "-":
        parser.error("only one input can come from stdin ('-')")
    if args.backlog is not None and not args.backlog.strip():
        parser.error("--backlog needs a file path")

    try:
        rows, headers = _load(args.path, args.json, JSON_KEY)
        sprints, flags = parse_history(rows, headers)
        backlog = None
        if args.backlog:
            text = read_text(args.backlog)
            try:
                b_rows, b_headers = load_rows(text, text.lstrip()[:1] in ("[", "{"), BACKLOG_JSON_KEY)
            except ValueError as exc:  # name the file: two inputs can fail the same way
                raise ValueError(f"--backlog {args.backlog}: {exc}")
            backlog = parse_backlog(b_rows, b_headers)
        result = analyse(sprints, flags, args, backlog)
        print(RENDERERS[args.format](result))
    except UnicodeDecodeError as exc:
        print(f"error: input is not UTF-8 text (bad byte at offset {exc.start}); re-save it as 'CSV UTF-8'",
              file=sys.stderr)
        return 2
    except (OSError, ValueError, TypeError, OverflowError, ZeroDivisionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
