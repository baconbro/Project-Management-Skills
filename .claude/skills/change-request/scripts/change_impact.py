#!/usr/bin/env python3
"""Score change requests (CRs) by weighted impact, band them, route each one to the PM, the
change control board (CCB) or the sponsor, total the change burden against a reserve, and test
how sensitive each band is to the weights. Standard library only.

Reads a change log from CSV (delimiter auto-detected: , ; tab |) or JSON (--json) and prints the
CRs ranked by impact score (highest first) with an impact band each, plus a summary. Warnings go
to stderr, so stdout stays machine-readable.

INPUT COLUMNS / KEYS
  Case-insensitive; spaces and hyphens count as underscores and a trailing "(unit)" is ignored,
  so "Scope Impact" and "Cost value ($)" both match. Other columns (raised_by, date_raised,
  decided_by, ...) are passed through to --format csv and json. "row N" in messages means the
  Nth data row, header excluded.
    scope_impact     1-5 rating, decimals allowed (aliases: scope, scope_score)      REQUIRED
    cost_impact      1-5 rating (cost, cost_score)                                   REQUIRED
    schedule_impact  1-5 rating (schedule, schedule_score, time_impact)              REQUIRED
    quality_impact   1-5 rating (quality_score); scored only if the column exists    optional
    risk_impact      1-5 rating (risk_score); scored only if the column exists       optional
    id               CR identifier (cr_id, change_id, cr, ref); blank -> row-N       optional
    title            what the change is (description, desc, summary, change)         optional
    status           Raised, Under assessment, Approved, Rejected, Deferred,
                     Implemented, Closed (alias: state); blank -> Raised             optional
    cost_value       money the change adds (+) or saves (-) in one currency
                     (cost_delta, cost_change, cost_amount, change_cost); "$" "," ok  optional
    schedule_days    working days the change adds (+) or saves (-)
                     (days, schedule_delta_days, delay_days)                          optional
  A rating is the impact MAGNITUDE on that dimension: 1 negligible, 2 minor, 3 moderate,
  4 major, 5 severe. Per-dimension anchors are in
  .claude/skills/change-request/references/change-request-fields.md. Ratings outside 1-5,
  blank ratings, nan/inf and booleans are rejected; 3.5 is kept as 3.5 (no truncation).

FORMULAS
  score        = sum(w_d x rating_d) / sum(w_d) over the scored dimensions (a weighted mean, 1-5)
  impact band  = HIGH if score >= --high (default 4.0), MEDIUM if score >= --medium (default
                 2.5), else LOW. The band is impact MAGNITUDE - how hard the change hits the
                 baselines - NOT urgency or business value. It sets how deep the assessment goes
                 and who must approve; order the CCB agenda by urgency and value.
  order        = score descending, then id ascending (natural order: CR2 before CR10).
  authority    shown when cost_value and/or schedule_days exist:
                 Sponsor  band HIGH, or |cost_value| > --ccb-limit-cost, or |schedule_days| >
                          --ccb-limit-days (both CCB limits are optional)
                 PM       band LOW and |cost_value| <= --pm-limit-cost and |schedule_days| <=
                          --pm-limit-days. A blank value is unknown and never inside the PM
                          tolerance; an absent column is not tested. Savings count by magnitude.
                 CCB      everything else
  burden       sums of cost_value and schedule_days over the WHOLE log (--status does not filter
               it), by status group: committed = approved, implemented, closed; pending = raised,
               under assessment; declined = rejected, deferred, withdrawn (shown, not counted).
               With --reserve-cost R: committed / R, (committed + pending) / R and the headroom;
               --reserve-days does the same for days. Summed days are an upper bound: changes on
               parallel paths do not simply add, so check the critical path.
  sensitivity  --sensitivity: margin = score - the nearest band threshold (+ above it, - below);
               stable = the band is unchanged when any ONE scored weight is halved or doubled
               (one at a time, x0.5 and x2); otherwise the perturbations that flip it are listed.
  explain      --explain: each dimension's share of the score = w_d x rating_d / sum(w x rating),
               the band rule that applied, and the authority reason.

OPTIONS
  path                    CSV/JSON change log, or - for stdin
  --json                  parse the input as JSON: a list of objects or {"changes": [...]}
  --w-scope/--w-cost/--w-schedule/--w-quality/--w-risk W
                          dimension weights, finite, > 0 and <= 1000 (default 1.0 each); the
                          quality/risk weights apply only when that column exists
  --high H, --medium M    band thresholds, finite, 1 <= M < H <= 5 (defaults 4.0 and 2.5)
  --pm-limit-cost C       PM approval tolerance in money (default 5000; >= 0)
  --pm-limit-days D       PM approval tolerance in working days (default 2; >= 0)
  --ccb-limit-cost C      above this, the sponsor decides (optional; must exceed the PM limit)
  --ccb-limit-days D      above this, the sponsor decides (optional; must exceed the PM limit)
  --reserve-cost R        reserve available to fund changes, e.g. the contingency (> 0)
  --reserve-days R        schedule reserve available to absorb changes (> 0)
  --status LIST           show only these statuses or groups (comma-separated): pending,
                          committed, declined, all, or a status such as approved
  --sort score|id|input   row order (default score)
  --sensitivity           add Margin and Stable columns
  --explain               add the score breakdown and authority reason per CR
  --format table|json|csv|md
                          table (default, aligned text), json ({"changes": [...], "summary":
                          {...}}), csv (the input columns plus computed ones, re-importable as
                          the log), md (GitHub table for a status report or CCB pack)

EXIT CODES
  0  scored (also when --status matches no CR)
  2  bad input or usage: "error: ..." on stderr, never a traceback
  (1 is not used: this is a scorer, not a validator.)

EXAMPLES (from the repo root)
  CSV:    python .claude/skills/change-request/scripts/change_impact.py .claude/skills/change-request/assets/change-log.csv
  JSON:   python .claude/skills/change-request/scripts/change_impact.py changes.json --json
  stdin:  cat changes.csv | python .claude/skills/change-request/scripts/change_impact.py -
  CCB:    python .claude/skills/change-request/scripts/change_impact.py .claude/skills/change-request/assets/change-log.csv --status pending --reserve-cost 40000 --sensitivity --explain --format md
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
JSON_KEY = "changes"

DEFAULT_HIGH, DEFAULT_MEDIUM = 4.0, 2.5
DEFAULT_PM_COST, DEFAULT_PM_DAYS = 5000.0, 2.0
MAX_WEIGHT = 1000.0
TITLE_WIDTH, ID_WIDTH, STATUS_WIDTH, FLIPS_WIDTH = 48, 20, 18, 40
BANDS = ("HIGH", "MEDIUM", "LOW")
AUTHORITIES = ("PM", "CCB", "Sponsor")

# key, canonical column, table header, aliases, required
DIMENSIONS = (
    ("scope", "scope_impact", "Scope", ("scope_impact", "scope", "scope_score"), True),
    ("cost", "cost_impact", "Cost", ("cost_impact", "cost", "cost_score"), True),
    ("schedule", "schedule_impact", "Sched", ("schedule_impact", "schedule", "schedule_score", "time_impact"), True),
    ("quality", "quality_impact", "Qual", ("quality_impact", "quality_score"), False),
    ("risk", "risk_impact", "Risk", ("risk_impact", "risk_score"), False),
)
ID_ALIASES = ("id", "cr_id", "change_id", "cr", "ref")
TITLE_ALIASES = ("title", "description", "desc", "summary", "change")
STATUS_ALIASES = ("status", "state")
COST_VALUE_ALIASES = ("cost_value", "cost_delta", "cost_change", "cost_amount", "change_cost")
DAYS_ALIASES = ("schedule_days", "days", "schedule_delta_days", "delay_days")
ALL_ALIASES = {a for d in DIMENSIONS for a in d[3]} | set(
    ID_ALIASES + TITLE_ALIASES + STATUS_ALIASES + COST_VALUE_ALIASES + DAYS_ALIASES)
COMPUTED_COLUMNS = ("rank", "score", "impact_band", "authority", "authority_reason", "margin",
                    "nearest_boundary", "stable", "flips", "explanation")

STATUS_GROUPS = {
    "pending": {"raised", "new", "open", "submitted", "logged", "draft", "under assessment",
                "assessing", "in assessment", "under review", "in review", "pending",
                "pending decision", "awaiting decision", "escalated"},
    "committed": {"approved", "approved with conditions", "conditionally approved", "implemented",
                  "in progress", "in implementation", "implementing", "verified", "closed",
                  "done", "complete", "completed"},
    "declined": {"rejected", "deferred", "withdrawn", "cancelled", "canceled", "superseded",
                 "on hold"},
}
GROUP_LABELS = {
    "committed": "committed (approved, implemented, closed)",
    "pending": "pending decision (raised, under assessment)",
    "declined": "declined (rejected, deferred) - not counted",
}
UNIT_SUFFIX_RE = re.compile(r"\s*\([^()]*\)\s*$")


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


def norm_key(name):
    """'Scope Impact' -> 'scope_impact'; 'Cost value ($)' -> 'cost_value'."""
    k = UNIT_SUFFIX_RE.sub("", str(name).lstrip(BOM).strip().lower())
    return re.sub(r"[\s\-]+", "_", k).strip("_")


def require_columns(headers, groups):
    """groups = [("scope_impact", "scope"), ...]: each group needs one alias present (after norm_key)."""
    present = {norm_key(h) for h in headers if h}
    missing = [g[0] for g in groups if not any(norm_key(a) in present for a in g)]
    if missing:
        accepted = "; ".join(f"{g[0]}: {', '.join(g)}" for g in groups if g[0] in missing)
        raise ValueError(f"missing column(s): {missing} (accepted names - {accepted}); "
                         f"found headers: {[h for h in headers if h]}")


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


def is_blank(value):
    return value is None or (isinstance(value, str) and value.strip() == "")


def clean_text(value):
    """Collapse whitespace and newlines; None -> ''."""
    return "" if value is None else " ".join(str(value).split())


def natural_key(text):
    """'CR2' sorts before 'CR10'. re.split with a group alternates text / digits, so types align."""
    parts = re.split(r"(\d+)", text.lower())
    return tuple(int(p) if i % 2 else p for i, p in enumerate(parts))


def status_key(text):
    return " ".join(re.sub(r"[_\-]+", " ", text.lower()).split())


def status_group(text):
    key = status_key(text)
    if key == "":
        return "pending"
    for group, words in STATUS_GROUPS.items():
        if key in words:
            return group
    return None


# --------------------------------------------------------------------------- formatting
def fmt_num(v, decimals=2):
    """Thousands separators, up to `decimals` places, no trailing zeros, never '-0'."""
    if v is None:
        return ""
    s = f"{v:,.{decimals}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def fmt_signed(v):
    r = round(v, 2)
    return "0.00" if r == 0 else f"{r:+.2f}"


def fmt_pct(v):
    r = round(v, 1)
    return "0.0%" if r == 0 else f"{r:.1f}%"


def plural(n, word):
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def clip(text, width):
    text = clean_text(text)
    return text if len(text) <= width else text[: width - 1] + "…"


def md_cell(text):
    return clean_text(text).replace("|", "\\|")


def json_number(v):
    if v is None:
        return None
    r = round(v, 6)
    return int(r) if r == int(r) else r


# --------------------------------------------------------------------------- scoring
def weighted_score(ratings, weights, dims):
    num = sum(weights[d] * ratings[d] for d in dims)
    den = sum(weights[d] for d in dims)
    return round(num / den, 6)


def band_of(score, high, medium):
    s = round(score, 6)
    if s >= round(high, 6):
        return "HIGH"
    if s >= round(medium, 6):
        return "MEDIUM"
    return "LOW"


def sensitivity(rec, weights, dims, high, medium):
    flips = []
    for d in dims:
        for factor in (0.5, 2.0):
            trial = dict(weights)
            trial[d] = weights[d] * factor
            b = band_of(weighted_score(rec["ratings"], trial, dims), high, medium)
            if b != rec["band"]:
                flips.append(f"{d} x{fmt_num(factor)}->{b}")
    d_high, d_med = rec["score"] - high, rec["score"] - medium
    if abs(d_high) <= abs(d_med):
        return round(d_high, 6), "HIGH", flips
    return round(d_med, 6), "MEDIUM", flips


def size(v, unit=""):
    """'18,000' or, for a saving, '-3,000 (size 3,000)': tolerances compare magnitudes."""
    return f"{fmt_num(v)}{unit}" if v >= 0 else f"{fmt_num(v)}{unit} (size {fmt_num(-v)}{unit})"


def route(rec, lim, has_cost, has_days):
    """Return (authority, reason)."""
    cv, dd = rec["cost_value"], rec["schedule_days"]
    if rec["band"] == "HIGH":
        return "Sponsor", "impact band HIGH (a HIGH-impact change goes to the sponsor)"
    if has_cost and lim["ccb_cost"] is not None and cv is not None and abs(cv) > lim["ccb_cost"]:
        return "Sponsor", f"cost value {size(cv)} > CCB limit {fmt_num(lim['ccb_cost'])}"
    if has_days and lim["ccb_days"] is not None and dd is not None and abs(dd) > lim["ccb_days"]:
        return "Sponsor", f"schedule {size(dd, ' days')} > CCB limit {fmt_num(lim['ccb_days'])} days"
    reasons, inside = [], [f"impact band {rec['band']}"]
    if rec["band"] != "LOW":
        reasons.append(f"impact band {rec['band']} (the PM decides alone only LOW-band changes)")
    if has_cost:
        if cv is None:
            reasons.append("cost value blank (unquantified)")
        elif abs(cv) > lim["pm_cost"]:
            reasons.append(f"cost value {size(cv)} > PM limit {fmt_num(lim['pm_cost'])}")
        else:
            inside.append(f"cost value {size(cv)} <= {fmt_num(lim['pm_cost'])}")
    if has_days:
        if dd is None:
            reasons.append("schedule days blank (unquantified)")
        elif abs(dd) > lim["pm_days"]:
            reasons.append(f"schedule {size(dd, ' days')} > PM limit {fmt_num(lim['pm_days'])} days")
        else:
            inside.append(f"schedule {size(dd, ' days')} <= {fmt_num(lim['pm_days'])} days")
    if reasons:
        return "CCB", "; ".join(reasons)
    return "PM", "within PM tolerance: " + ", ".join(inside)


def explain(rec, weights, dims, high, medium):
    terms = " + ".join(f"{fmt_num(weights[d], 4)}x{fmt_num(rec['ratings'][d])}" for d in dims)
    total_w = fmt_num(sum(weights[d] for d in dims), 4)
    contrib = {d: weights[d] * rec["ratings"][d] for d in dims}
    whole = sum(contrib.values())
    shares = {d: 100.0 * contrib[d] / whole for d in dims}
    drivers = ", ".join(f"{d} {shares[d]:.0f}%" for d in sorted(dims, key=lambda k: (-contrib[k], dims.index(k))))
    if rec["band"] == "HIGH":
        rule = f">= {high:.2f}"
    elif rec["band"] == "MEDIUM":
        rule = f">= {medium:.2f} and < {high:.2f}"
    else:
        rule = f"< {medium:.2f}"
    text = f"score {rec['score']:.2f} = ({terms}) / {total_w} -> {rec['band']} ({rule}); drivers: {drivers}"
    if rec.get("authority"):
        text += f"; authority {rec['authority']}: {rec['authority_reason']}"
    return text, {d: round(shares[d], 2) for d in dims}


# --------------------------------------------------------------------------- parsing rows
def parse_log(rows, headers):
    """Normalise headers, validate every row and return (records, context)."""
    norm_map = {}
    for h in headers:
        if not h:
            continue
        n = norm_key(h)
        if n in norm_map and norm_map[n] != h:
            raise ValueError(f"columns {norm_map[n]!r} and {h!r} both mean {n!r}; keep one")
        norm_map[n] = h
    require_columns(headers, [d[3] for d in DIMENSIONS if d[4]])
    present = set(norm_map)
    dims = [d[0] for d in DIMENSIONS if d[4] or any(a in present for a in d[3])]
    ctx = {
        "dims": dims,
        "has_id": any(a in present for a in ID_ALIASES),
        "has_status": any(a in present for a in STATUS_ALIASES),
        "has_cost": any(a in present for a in COST_VALUE_ALIASES),
        "has_days": any(a in present for a in DAYS_ALIASES),
        "warnings": [],
        "headers": [h for h in headers if h],
        "passthrough": [h for h in headers if h and norm_key(h) not in ALL_ALIASES
                        and norm_key(h) not in COMPUTED_COLUMNS],
    }
    records, seen, missing_ids = [], {}, []
    for i, row in enumerate(rows, 1):
        nrow = {norm_key(k): v for k, v in row.items() if k}
        raw_id = _get(nrow, *ID_ALIASES)
        cid = clean_text(raw_id) if not is_blank(raw_id) else ""
        if not cid:
            cid = f"row-{i}"
            missing_ids.append(i)
        else:
            low = cid.lower()
            if low in seen:
                ctx["warnings"].append(f"duplicate id {cid!r} in rows {seen[low]} and {i}; "
                                       "give every CR a unique id in the change log")
            else:
                seen[low] = i
        ratings = {}
        for key, column, _hdr, aliases, _req in DIMENSIONS:
            if key not in dims:
                continue
            where = f"row {i} ({cid}), column {column}"
            value = _get(nrow, *aliases)
            if is_blank(value):
                raise ValueError(f"{where}: blank; rate it 1-5 (see references/change-request-fields.md)")
            ratings[key] = _num(value, where, minimum=1, maximum=5)
        status_raw = clean_text(_get(nrow, *STATUS_ALIASES, default=""))
        group = status_group(status_raw)
        if group is None:
            ctx["warnings"].append(
                f"row {i} ({cid}): unknown status {status_raw!r} counted as pending; use Raised, "
                "Under assessment, Approved, Rejected, Deferred, Implemented or Closed")
            group = "pending"
        cost_value = schedule_days = None
        if ctx["has_cost"]:
            v = _get(nrow, *COST_VALUE_ALIASES)
            if not is_blank(v):
                cost_value = _num(v, f"row {i} ({cid}), column cost_value")
        if ctx["has_days"]:
            v = _get(nrow, *DAYS_ALIASES)
            if not is_blank(v):
                schedule_days = _num(v, f"row {i} ({cid}), column schedule_days")
        records.append({
            "index": i, "id": cid, "title": clean_text(_get(nrow, *TITLE_ALIASES, default="")),
            "status": status_raw or ("Raised" if ctx["has_status"] else ""), "group": group,
            "ratings": ratings, "cost_value": cost_value, "schedule_days": schedule_days,
            "raw": row,
        })
    if missing_ids:
        shown = ", ".join(str(n) for n in missing_ids[:10]) + (" ..." if len(missing_ids) > 10 else "")
        where = f"row {shown}" if len(missing_ids) == 1 else f"rows {shown}"
        ctx["warnings"].append(f"{plural(len(missing_ids), 'row')} without an id ({where}) shown as "
                               "row-N; give every CR a unique id in the change log")
    return records, ctx


def burden(records, ctx, reserve_cost, reserve_days):
    out = {}
    for g in ("committed", "pending", "declined"):
        sel = [r for r in records if r["group"] == g]
        out[g] = {
            "count": len(sel),
            "cost_value": round(sum(r["cost_value"] for r in sel if r["cost_value"] is not None), 6),
            "schedule_days": round(sum(r["schedule_days"] for r in sel if r["schedule_days"] is not None), 6),
            "unquantified_cost": sum(1 for r in sel if ctx["has_cost"] and r["cost_value"] is None),
            "unquantified_days": sum(1 for r in sel if ctx["has_days"] and r["schedule_days"] is None),
        }
    cp = {k: (round(out["committed"][k] + out["pending"][k], 6) if k in ("cost_value", "schedule_days")
              else out["committed"][k] + out["pending"][k]) for k in out["committed"]}
    out["committed_plus_pending"] = cp
    for key, reserve, name in (("cost_value", reserve_cost, "reserve_cost"), ("schedule_days", reserve_days, "reserve_days")):
        has = ctx["has_cost"] if key == "cost_value" else ctx["has_days"]
        if reserve is None or not has:
            continue
        out[name] = {
            "reserve": reserve,
            "committed_pct": round(100.0 * out["committed"][key] / reserve, 2),
            "committed_plus_pending_pct": round(100.0 * cp[key] / reserve, 2),
            "headroom": round(reserve - cp[key], 6),
        }
    return out


# --------------------------------------------------------------------------- output
def columns(ctx, args):
    cols = [("#", "rank"), ("ID", "id"), ("Score", "score"), ("Impact band", "band")]
    cols += [(d[2], d[0]) for d in DIMENSIONS if d[0] in ctx["dims"]]
    if ctx["has_status"]:
        cols.append(("Status", "status"))
    if ctx["has_cost"]:
        cols.append(("Cost value", "cost_value"))
    if ctx["has_days"]:
        cols.append(("Days", "schedule_days"))
    if ctx["has_cost"] or ctx["has_days"]:
        cols.append(("Authority", "authority"))
    if args.sensitivity:
        cols += [("Margin", "margin"), ("Stable", "stable")]
    cols.append(("Title", "title"))
    return cols


def cell(rec, key, table):
    if key == "rank":
        return str(rec["rank"])
    if key == "id":
        return clip(rec["id"], ID_WIDTH) if table else clean_text(rec["id"])
    if key == "score":
        return f"{rec['score']:.2f}"
    if key == "band":
        return rec["band"]
    if key in rec["ratings"]:
        return fmt_num(rec["ratings"][key])
    if key == "status":
        return clip(rec["status"], STATUS_WIDTH) if table else rec["status"]
    if key in ("cost_value", "schedule_days"):
        return fmt_num(rec[key]) if rec[key] is not None else "?"
    if key == "authority":
        return rec.get("authority", "")
    if key == "margin":
        return f"{fmt_signed(rec['margin'])} vs {rec['nearest']}"
    if key == "stable":
        text = "yes" if not rec["flips"] else "no: " + "; ".join(rec["flips"])
        return clip(text, FLIPS_WIDTH) if table else text
    if key == "title":
        return clip(rec["title"], TITLE_WIDTH) if table else clean_text(rec["title"])
    return ""


def summary_lines(shown, records, ctx, args, summ):
    weights = ", ".join(f"{d} {fmt_num(summ['weights'][d], 4)}" for d in ctx["dims"])
    bc = summ["band_counts"]
    lines = [
        f"Impact bands: HIGH {bc['HIGH']}, MEDIUM {bc['MEDIUM']}, LOW {bc['LOW']} "
        f"(HIGH >= {args.high:.2f}, MEDIUM >= {args.medium:.2f}). The band is impact magnitude, "
        "not urgency or business value: it sets assessment depth and approval authority.",
        f"Score = weighted mean of the 1-5 ratings; weights: {weights}. Ties are ordered by id.",
    ]
    if "authority" in summ:
        a = summ["authority"]
        within = ([f"cost {fmt_num(a['pm_limit_cost'])}"] if ctx["has_cost"] else []) + \
                 ([f"{fmt_num(a['pm_limit_days'])} days"] if ctx["has_days"] else [])
        rule = f"PM if band LOW and within {' and '.join(within)}; Sponsor if band HIGH"
        if a["ccb_limit_cost"] is not None and ctx["has_cost"]:
            rule += f" or cost above {fmt_num(a['ccb_limit_cost'])}"
        if a["ccb_limit_days"] is not None and ctx["has_days"]:
            rule += f" or days above {fmt_num(a['ccb_limit_days'])}"
        rule += "; otherwise CCB"
        c = a["counts"]
        lines.append(f"Authority: PM {c['PM']}, CCB {c['CCB']}, Sponsor {c['Sponsor']} ({rule}).")
    if args.sensitivity:
        s = summ["sensitivity"]
        names = ", ".join(s["sensitive_ids"]) if s["sensitive_ids"] else "none"
        lines.append(f"Sensitivity: {s['sensitive']} of {s['of']} bands change when one weight is "
                     f"halved or doubled ({names}).")
    if summ["status_filter"]:
        lines.append(f"Showing {len(shown)} of {len(records)} CRs (--status {','.join(summ['status_filter'])}).")
    return lines


def burden_rows(summ, ctx):
    b = summ["burden"]
    rows = []
    for key, label in (("committed", GROUP_LABELS["committed"]), ("pending", GROUP_LABELS["pending"]),
                       ("committed_plus_pending", "committed + pending"), ("declined", GROUP_LABELS["declined"])):
        g = b[key]
        cost = fmt_num(g["cost_value"]) if ctx["has_cost"] else "-"
        days = fmt_num(g["schedule_days"]) if ctx["has_days"] else "-"
        unq = []
        if g["unquantified_cost"]:
            unq.append(f"{g['unquantified_cost']} without cost value")
        if g["unquantified_days"]:
            unq.append(f"{g['unquantified_days']} without days")
        rows.append([label, plural(g["count"], "CR"), cost, days, "; ".join(unq)])
    notes = []
    for name, unit in (("reserve_cost", ""), ("reserve_days", " days")):
        if name in b:
            r = b[name]
            head = r["headroom"]
            tail = (f"headroom {fmt_num(head)}{unit}" if head >= 0 else f"OVER by {fmt_num(-head)}{unit}")
            notes.append(f"vs --{name.replace('_', '-')} {fmt_num(r['reserve'])}{unit}: committed uses "
                         f"{fmt_pct(r['committed_pct'])}; committed + pending would use "
                         f"{fmt_pct(r['committed_plus_pending_pct'])} ({tail})")
    if ctx["has_days"]:
        notes.append("Summed days are an upper bound: changes on parallel paths do not simply add.")
    return rows, notes


def aligned(header, rows, right=()):
    widths = [max(len(header[c]), *(len(r[c]) for r in rows)) if rows else len(header[c]) for c in range(len(header))]

    def line(cells):
        out = [(cells[c].rjust(widths[c]) if c in right else cells[c].ljust(widths[c])) for c in range(len(cells))]
        return "  ".join(out).rstrip()

    return [line(header), line(["-" * w for w in widths])] + [line(r) for r in rows]


def render_table(shown, records, ctx, args, summ):
    cols = columns(ctx, args)
    header = [c[0] for c in cols]
    body = [[cell(r, c[1], True) for c in cols] for r in shown]
    numeric = {i for i, c in enumerate(cols) if c[1] in ("rank", "score", "cost_value", "schedule_days")
               or c[1] in ctx["dims"]}
    out = aligned(header, body, right=numeric) if shown else ["No change requests match the --status filter."]
    out.append("")
    out += summary_lines(shown, records, ctx, args, summ)
    if "burden" in summ:
        rows, notes = burden_rows(summ, ctx)
        header = ["Status group", "CRs", "Cost value", "Days", "Unquantified"]
        if not any(r[4] for r in rows):
            header, rows = header[:4], [r[:4] for r in rows]
        out.append("")
        out.append(f"Change burden over the whole log ({plural(len(records), 'CR')}):")
        out += ["  " + ln for ln in aligned(header, rows, right={2, 3})]
        out += ["  " + n for n in notes]
    if args.explain and shown:
        out.append("")
        out.append("Explanation:")
        for r in shown:
            out.append(f"  {r['id']}: {r['explanation']}")
    return "\n".join(out)


def render_md(shown, records, ctx, args, summ):
    cols = columns(ctx, args)
    out = []
    if shown:
        out.append("| " + " | ".join(c[0] for c in cols) + " |")
        out.append("| " + " | ".join("---:" if c[1] in ("rank", "score", "cost_value", "schedule_days")
                                     or c[1] in ctx["dims"] else "---" for c in cols) + " |")
        for r in shown:
            out.append("| " + " | ".join(md_cell(cell(r, c[1], False)) for c in cols) + " |")
    else:
        out.append("_No change requests match the --status filter._")
    out.append("")
    out += [f"- {md_cell(ln)}" for ln in summary_lines(shown, records, ctx, args, summ)]
    if "burden" in summ:
        rows, notes = burden_rows(summ, ctx)
        width = 5 if any(r[4] for r in rows) else 4
        head = ["Status group", "CRs", "Cost value", "Days", "Unquantified"][:width]
        align = ["---", "---:", "---:", "---:", "---"][:width]
        out += ["", f"**Change burden over the whole log ({plural(len(records), 'CR')})**", "",
                "| " + " | ".join(head) + " |", "| " + " | ".join(align) + " |"]
        out += ["| " + " | ".join(md_cell(x) for x in r[:width]) + " |" for r in rows]
        out += [""] + [f"- {md_cell(n)}" for n in notes]
    if args.explain and shown:
        out += ["", "**Explanation**", ""]
        out += [f"- **{md_cell(r['id'])}**: {md_cell(r['explanation'])}" for r in shown]
    return "\n".join(out)


def computed_fields(r, ctx, args):
    out = {"rank": r["rank"], "score": f"{r['score']:.2f}", "impact_band": r["band"]}
    if ctx["has_cost"] or ctx["has_days"]:
        out["authority"] = r["authority"]
        if args.explain:
            out["authority_reason"] = r["authority_reason"]
    if args.sensitivity:
        out.update({"margin": f"{r['margin']:.2f}" if round(r["margin"], 2) != 0 else "0.00",
                    "nearest_boundary": r["nearest"], "stable": "yes" if not r["flips"] else "no",
                    "flips": "; ".join(r["flips"])})
    if args.explain:
        out["explanation"] = r["explanation"]
    return out


def render_csv(shown, ctx, args):
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    base = [h for h in ctx["headers"] if norm_key(h) not in COMPUTED_COLUMNS]
    extra = list(computed_fields(shown[0], ctx, args)) if shown else ["rank", "score", "impact_band"]
    writer.writerow(base + extra)
    for r in shown:
        raw = r["raw"]
        values = ["" if raw.get(h) is None else clean_text(raw.get(h)) for h in base]
        comp = computed_fields(r, ctx, args)
        writer.writerow(values + [comp[k] for k in extra])
    return buf.getvalue().rstrip("\n")


def render_json(shown, ctx, args, summ):
    items = []
    for r in shown:
        item = {"rank": r["rank"], "id": r["id"], "title": r["title"], "status": r["status"],
                "status_group": r["group"], "score": round(r["score"], 4), "impact_band": r["band"]}
        for key, column, _h, _a, _req in DIMENSIONS:
            if key in ctx["dims"]:
                item[column] = json_number(r["ratings"][key])
        if ctx["has_cost"]:
            item["cost_value"] = json_number(r["cost_value"])
        if ctx["has_days"]:
            item["schedule_days"] = json_number(r["schedule_days"])
        if ctx["has_cost"] or ctx["has_days"]:
            item["authority"] = r["authority"]
            item["authority_reason"] = r["authority_reason"]
        if args.sensitivity:
            item.update({"margin": round(r["margin"], 4) + 0.0, "nearest_boundary": r["nearest"],
                         "stable": not r["flips"], "flips": r["flips"]})
        if args.explain:
            item["contributions_pct"] = r["contributions"]
            item["explanation"] = r["explanation"]
        taken = {k.lower() for k in item}
        for h in ctx["passthrough"]:
            if h.lower() not in taken:
                item[h] = r["raw"].get(h)
        items.append(item)
    return json.dumps({JSON_KEY: items, "summary": summ}, indent=2, ensure_ascii=False)


# --------------------------------------------------------------------------- CLI
def build_parser():
    doc = (__doc__ or "Score change requests by weighted impact.\n\n").split("\n\n", 1)  # None under python -OO
    epilog = re.sub(r"\nOPTIONS\n.*?\n(?=EXIT CODES)", "\n", doc[1], flags=re.S)
    p = argparse.ArgumentParser(
        prog="change_impact.py", description=doc[0].replace("\n", " "),
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=epilog)
    p.add_argument("path", help="CSV/JSON change log, or - for stdin")
    p.add_argument("--json", action="store_true", help="parse the input as JSON: a list of objects or {\"changes\": [...]}")
    for key, column, _h, _a, _req in DIMENSIONS:
        p.add_argument(f"--w-{key}", type=float, default=None, metavar="W",
                       help=f"weight for {column} (default 1.0; finite, > 0, <= {MAX_WEIGHT:g})")
    p.add_argument("--high", type=float, default=DEFAULT_HIGH, help="HIGH band threshold (default 4.0)")
    p.add_argument("--medium", type=float, default=DEFAULT_MEDIUM, help="MEDIUM band threshold (default 2.5)")
    p.add_argument("--pm-limit-cost", type=float, default=None, metavar="C",
                   help="PM approval tolerance in money (default 5000)")
    p.add_argument("--pm-limit-days", type=float, default=None, metavar="D",
                   help="PM approval tolerance in working days (default 2)")
    p.add_argument("--ccb-limit-cost", type=float, default=None, metavar="C",
                   help="above this |cost_value| the sponsor decides (optional)")
    p.add_argument("--ccb-limit-days", type=float, default=None, metavar="D",
                   help="above this |schedule_days| the sponsor decides (optional)")
    p.add_argument("--reserve-cost", type=float, default=None, metavar="R",
                   help="reserve available to fund changes, e.g. the contingency (optional)")
    p.add_argument("--reserve-days", type=float, default=None, metavar="R",
                   help="schedule reserve available to absorb changes (optional)")
    p.add_argument("--status", default=None, metavar="LIST",
                   help="show only these statuses/groups, comma-separated: pending, committed, declined, all, "
                        "or a status such as approved")
    p.add_argument("--sort", choices=("score", "id", "input"), default="score", help="row order (default score)")
    p.add_argument("--sensitivity", action="store_true",
                   help="add Margin (to the nearest threshold) and Stable (band under one weight x0.5/x2)")
    p.add_argument("--explain", action="store_true", help="add the score breakdown and authority reason per CR")
    p.add_argument("--format", choices=("table", "json", "csv", "md"), default="table",
                   help="output format (default table)")
    return p


def validate_args(p, args):
    weights = {}
    for key, _c, _h, _a, _r in DIMENSIONS:
        w = getattr(args, f"w_{key}")
        if w is None:
            w = 1.0
        if not math.isfinite(w) or w <= 0 or w > MAX_WEIGHT:
            p.error(f"--w-{key} must be a finite number > 0 and <= {MAX_WEIGHT:g}, got {w}")
        weights[key] = w
    for opt in ("high", "medium"):
        if not math.isfinite(getattr(args, opt)):
            p.error(f"--{opt} must be a finite number")
    if not 1 <= args.medium < args.high <= 5:
        p.error(f"thresholds must satisfy 1 <= --medium < --high <= 5 (scores run 1-5), "
                f"got --medium {args.medium} and --high {args.high}")
    lim = {"pm_cost": DEFAULT_PM_COST if args.pm_limit_cost is None else args.pm_limit_cost,
           "pm_days": DEFAULT_PM_DAYS if args.pm_limit_days is None else args.pm_limit_days,
           "ccb_cost": args.ccb_limit_cost, "ccb_days": args.ccb_limit_days}
    for opt, val in (("pm-limit-cost", lim["pm_cost"]), ("pm-limit-days", lim["pm_days"])):
        if not math.isfinite(val) or val < 0:
            p.error(f"--{opt} must be a finite number >= 0, got {val}")
    for opt, val, floor in (("ccb-limit-cost", lim["ccb_cost"], lim["pm_cost"]),
                            ("ccb-limit-days", lim["ccb_days"], lim["pm_days"])):
        if val is not None and (not math.isfinite(val) or val <= floor):
            p.error(f"--{opt} must be a finite number above the PM limit ({fmt_num(floor)}), got {val}")
    for opt in ("reserve_cost", "reserve_days"):
        val = getattr(args, opt)
        if val is not None and (not math.isfinite(val) or val <= 0):
            p.error(f"--{opt.replace('_', '-')} must be a finite number > 0, got {val}")
    status_filter = None
    if args.status is not None:
        items = [status_key(s) for s in args.status.split(",") if s.strip()]
        known = set(STATUS_GROUPS) | {"all"} | set().union(*STATUS_GROUPS.values())
        bad = [s for s in items if s not in known]
        if not items or bad:
            p.error(f"--status: unknown value(s) {bad or [args.status]}; use pending, committed, declined, all, "
                    "or a status such as raised, under assessment, approved, rejected, deferred, implemented, closed")
        status_filter = None if "all" in items else items
    return weights, lim, status_filter


def keep(rec, status_filter):
    if status_filter is None:
        return True
    key = status_key(rec["status"]) or "raised"
    return any(f == rec["group"] or f == key for f in status_filter)


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    weights, lim, status_filter = validate_args(parser, args)
    try:
        try:
            sys.stdout.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
        try:
            text = read_text(args.path)
        except UnicodeDecodeError as exc:
            raise ValueError(f"{args.path} is not UTF-8 text ({exc.reason}); save it as UTF-8 / 'CSV UTF-8'")
        try:
            rows, headers = load_rows(text, args.json, JSON_KEY)
        except ValueError as exc:
            if "more cells than header" in str(exc):
                raise ValueError(f"{exc}; quote any text that contains the delimiter, e.g. \"Add SSO, MFA\"")
            raise
        records, ctx = parse_log(rows, headers)
        dims = ctx["dims"]
        for key, column, _h, _a, _r in DIMENSIONS:
            if key not in dims and getattr(args, f"w_{key}") is not None:
                ctx["warnings"].append(f"--w-{key} ignored: the log has no {column} column")
        money = ctx["has_cost"] or ctx["has_days"]
        if not money:
            for opt in ("pm_limit_cost", "pm_limit_days", "ccb_limit_cost", "ccb_limit_days", "reserve_cost", "reserve_days"):
                if getattr(args, opt) is not None:
                    ctx["warnings"].append(f"--{opt.replace('_', '-')} ignored: the log has no cost_value or schedule_days column")
        else:
            for opt, has in (("ccb_limit_cost", ctx["has_cost"]), ("reserve_cost", ctx["has_cost"]),
                             ("ccb_limit_days", ctx["has_days"]), ("reserve_days", ctx["has_days"])):
                if getattr(args, opt) is not None and not has:
                    col = "cost_value" if opt.endswith("cost") else "schedule_days"
                    ctx["warnings"].append(f"--{opt.replace('_', '-')} ignored: the log has no {col} column")
        active_w = {d: weights[d] for d in dims}
        for r in records:
            r["score"] = weighted_score(r["ratings"], active_w, dims)
            r["band"] = band_of(r["score"], args.high, args.medium)
        shown = [r for r in records if keep(r, status_filter)]
        if args.sort == "score":
            shown.sort(key=lambda r: (-r["score"], natural_key(r["id"]), r["index"]))
        elif args.sort == "id":
            shown.sort(key=lambda r: (natural_key(r["id"]), r["index"]))
        for rank, r in enumerate(shown, 1):
            r["rank"] = rank
            if money:
                r["authority"], r["authority_reason"] = route(r, lim, ctx["has_cost"], ctx["has_days"])
            if args.sensitivity:
                r["margin"], r["nearest"], r["flips"] = sensitivity(r, active_w, dims, args.high, args.medium)
            if args.explain:
                r["explanation"], r["contributions"] = explain(r, active_w, dims, args.high, args.medium)
        summ = {
            "count": len(shown), "log_count": len(records), "status_filter": status_filter,
            "dimensions": dims, "weights": active_w, "thresholds": {"high": args.high, "medium": args.medium},
            "band_counts": {b: sum(1 for r in shown if r["band"] == b) for b in BANDS},
        }
        if money:
            summ["authority"] = {
                "pm_limit_cost": lim["pm_cost"], "pm_limit_days": lim["pm_days"],
                "ccb_limit_cost": lim["ccb_cost"], "ccb_limit_days": lim["ccb_days"],
                "counts": {a: sum(1 for r in shown if r["authority"] == a) for a in AUTHORITIES},
            }
            summ["burden"] = burden(records, ctx, args.reserve_cost, args.reserve_days)
        if args.sensitivity:
            sens = [r["id"] for r in shown if r["flips"]]
            summ["sensitivity"] = {"sensitive": len(sens), "of": len(shown), "sensitive_ids": sens}
        summ["warnings"] = ctx["warnings"]
        for w in ctx["warnings"]:
            print(f"warning: {w}", file=sys.stderr)
        if not shown and status_filter:
            print(f"note: no change request matches --status {args.status}", file=sys.stderr)
        if args.format == "json":
            print(render_json(shown, ctx, args, summ))
        elif args.format == "csv":
            print(render_csv(shown, ctx, args))
        elif args.format == "md":
            print(render_md(shown, records, ctx, args, summ))
        else:
            print(render_table(shown, records, ctx, args, summ))
    except (OSError, ValueError, TypeError, UnicodeDecodeError, OverflowError, ZeroDivisionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
