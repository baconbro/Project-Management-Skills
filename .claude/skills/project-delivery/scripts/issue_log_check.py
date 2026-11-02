#!/usr/bin/env python3
"""Check a project issue log (issues, actions, decisions, dependencies) before the weekly review:
hygiene problems that leave an item unmanaged, then what is overdue, due soon, blocked or waiting
for a steering decision, and each owner's open load. Standard library only.

Reads the log from CSV (delimiter auto-detected: , ; tab |) or JSON (a list of objects or
{"items": [...]}; detected automatically, --json forces it) and prints a report. Warnings and
problems are part of the report; nothing is written back to the log.

INPUT COLUMNS / KEYS
  Case-insensitive; spaces and hyphens count as underscores. "row N" in messages means the Nth
  data row, header excluded. Other columns are kept and passed through to --format csv.
    id            unique item id, e.g. I001, ACT001, DEC001, DEP001 (ref, item_id)       REQUIRED
    type          issue, action, decision or dependency (item_type, kind)                REQUIRED
    description   what the item is (desc, summary, title)                                 REQUIRED
    owner         exactly ONE named person (assignee, responsible)                        REQUIRED
    priority      High, Medium or Low (H/M/L and Critical=High accepted) (prio)           REQUIRED
    status        Open, In progress, Blocked, Closed or Transferred (state); Done,
                  Resolved, Decided and Cancelled count as Closed                         REQUIRED
    due           YYYY-MM-DD: resolve-by (issue), do-by (action), decide-by (decision),
                  needed-by (dependency) (due_date, needed_by, decide_by)                 REQUIRED
    impact        what the item threatens: scope, schedule, cost, quality, benefits       optional
    raised        YYYY-MM-DD the item was logged (date_raised, opened, created)           optional
    links         risk, change, vendor, WBS or meeting references, e.g. "R001; V01"       optional
    escalated_to  the forum or person it is escalated to, blank if within the team        optional
    resolution    how it was resolved; for a decision what was decided, by whom, why      optional*
    closed        YYYY-MM-DD the item was closed (date_closed, closed_on)                 optional
  * optional as a column, but every Closed or Transferred item needs one.

RULES
  problem (fails the check, exit 1):
    missing or duplicate id; type not one of the four (a "risk" belongs in the risk register,
    an "assumption" in the project-planning assumptions log); blank description; owner blank,
    a group ("team", "all", "TBD") or more than one person ("A and B", "A/B", "A, B"; text in
    brackets is ignored, so "Hana Sato (Legal & Compliance)" is one owner);
    priority or status not in the vocabulary; an open item with no due date; a date that is
    not YYYY-MM-DD; a Closed or Transferred item with no resolution; with --risks, a risk
    whose register status is Occurred but no issue in the log links its id.
  warning (reported, does not fail):
    closed item with no closed date; open issue or dependency with no impact; overdue High
    item not escalated; due or closed date before the raised date; with --risks, an issue
    that links a risk still Open in the register (set it to Occurred, execute its response).
  attention lists (open items only, i.e. Open, In progress, Blocked):
    overdue       due < as-of date
    due soon      as-of <= due <= as-of + --days
    blocked       status Blocked
    for steering  open decisions, and open items with escalated_to filled in
    by owner      open, High and overdue counts and the oldest open item's age in days

OPTIONS
  path            CSV/JSON issue log, or - for stdin
  --json          parse the input as JSON even if it does not start with [ or {
  --as-of DATE    status date, YYYY-MM-DD (default: today)
  --days N        due-soon window in days, 0-366 (default 7)
  --risks PATH    risk register CSV/JSON (columns id and status) to cross-check occurred risks
  --strict        also fail (exit 1) when any open item is overdue
  --format table|json|csv
                  table (default, aligned text), json (the full report), csv (the input columns
                  plus group, days_to_due, days_open, attention, problems; re-importable: those
                  computed columns are recomputed, so a second run gives the same file)

EXIT CODES
  0  no problems (overdue items alone do not fail unless --strict)
  1  problems found (or, with --strict, an open item is overdue)
  2  bad input or usage: "error: ..." on stderr, never a traceback

EXAMPLES (from the repo root)
  python .claude/skills/project-delivery/scripts/issue_log_check.py .claude/skills/project-delivery/assets/issue-log-sample.csv --as-of 2026-07-10
  python .claude/skills/project-delivery/scripts/issue_log_check.py my-log.csv --days 14 --risks my-risks.csv --strict
  cat my-log.csv | python .claude/skills/project-delivery/scripts/issue_log_check.py - --format json
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import re
import sys

BOM = "﻿"
JSON_KEYS = ("items", "issues", "log", "rows")
DESC_WIDTH = 58

ALIASES = {
    "id": ("id", "ref", "item_id", "item"),
    "type": ("type", "item_type", "kind"),
    "description": ("description", "desc", "summary", "title"),
    "owner": ("owner", "assignee", "responsible"),
    "priority": ("priority", "prio"),
    "status": ("status", "state"),
    "due": ("due", "due_date", "needed_by", "decide_by", "target_date"),
    "impact": ("impact",),
    "raised": ("raised", "date_raised", "opened", "created", "logged"),
    "links": ("links", "link", "refs", "references", "source"),
    "escalated_to": ("escalated_to", "escalation", "escalated"),
    "resolution": ("resolution", "outcome", "resolution_note"),
    "closed": ("closed", "date_closed", "closed_on", "closed_date"),
}
REQUIRED = ("id", "type", "description", "owner", "priority", "status", "due")

TYPES = {
    "issue": "issue", "problem": "issue", "blocker": "issue", "impediment": "issue", "defect": "issue",
    "action": "action", "action item": "action", "task": "action",
    "decision": "decision",
    "dependency": "dependency", "dep": "dependency",
}
MISPLACED_TYPES = {
    "risk": "risks belong in the risk register (risk-register); log an issue when one occurs",
    "opportunity": "opportunities belong in the risk register (risk-register)",
    "assumption": "assumptions belong in the assumptions log (project-planning); log an issue if one proves false",
    "constraint": "constraints belong in the assumptions log (project-planning)",
}
PRIORITIES = {"high": "High", "h": "High", "critical": "High", "medium": "Medium", "med": "Medium",
              "m": "Medium", "low": "Low", "l": "Low"}
STATUSES = {
    "open": "Open", "new": "Open", "pending": "Open", "raised": "Open", "to do": "Open", "todo": "Open",
    "not started": "Open", "decision needed": "Open", "awaiting decision": "Open",
    "in progress": "In progress", "in-progress": "In progress", "wip": "In progress", "doing": "In progress",
    "ongoing": "In progress", "active": "In progress",
    "blocked": "Blocked", "on hold": "Blocked",
    "closed": "Closed", "done": "Closed", "complete": "Closed", "completed": "Closed", "resolved": "Closed",
    "decided": "Closed", "cancelled": "Closed", "canceled": "Closed",
    "transferred": "Transferred", "handed over": "Transferred",
}
OPEN_STATUSES = {"Open", "In progress", "Blocked"}
GROUP_OWNERS = {"team", "the team", "all", "everyone", "everybody", "tbd", "tba", "tbc", "n/a", "na",
                "none", "unassigned", "?", "-", "nobody"}
MULTI_OWNER_RE = re.compile(r"\s(?:and|&|\+)\s|[/;,&+]")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TYPE_ORDER = ("issue", "action", "decision", "dependency")
PRIO_ORDER = {"High": 0, "Medium": 1, "Low": 2}


# --------------------------------------------------------------------------- input helpers
def read_text(path):
    """Read a file, or stdin when path is '-', stripping a UTF-8 BOM (Excel 'CSV UTF-8')."""
    if path == "-":
        text = sys.stdin.read()
    else:
        with open(path, encoding="utf-8-sig", newline="") as fh:
            text = fh.read()
    return text.lstrip(BOM)


def norm_key(name):
    """'Escalated To' -> 'escalated_to'."""
    k = str(name).lstrip(BOM).strip().lower()
    return re.sub(r"[\s\-]+", "_", k).strip("_")


def sniff_delimiter(text):
    try:
        return csv.Sniffer().sniff(text[:4096], delimiters=",;\t|").delimiter
    except csv.Error:
        return ","


def load_rows(text, force_json, what):
    """Return (rows, headers). JSON is used when forced or when the text starts with [ or {."""
    if not text.strip():
        raise ValueError(f"{what} is empty")
    if force_json or text.lstrip()[:1] in ("[", "{"):
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{what}: invalid JSON: {exc}")
        if isinstance(data, dict):
            key = next((k for k in data if str(k).lower() in JSON_KEYS + ("risks",)), None)
            if key is None:
                raise ValueError(f"{what}: a JSON object must hold a list under one of "
                                 f"{list(JSON_KEYS) + ['risks']}; found keys {sorted(map(str, data))}")
            data = data[key]
        if not isinstance(data, list):
            raise ValueError(f"{what}: JSON must be a list of objects")
        rows, headers = [], []
        for n, item in enumerate(data, 1):
            if not isinstance(item, dict):
                raise ValueError(f"{what}: JSON item {n} is not an object: {item!r}")
            row = {}
            for k, v in item.items():
                key = str(k).strip()
                if isinstance(v, (dict, list)):
                    raise ValueError(f"{what}: JSON item {n}, key {key!r}: expected text, got {type(v).__name__}")
                row[key] = "" if v is None else str(v).strip()
                if key not in headers:
                    headers.append(key)
            rows.append(row)
        if not rows:
            raise ValueError(f"{what} has no items")
        return rows, headers
    reader = csv.DictReader(io.StringIO(text), delimiter=sniff_delimiter(text))
    headers = [(h or "").strip() for h in (reader.fieldnames or [])]
    if not any(headers):
        raise ValueError(f"{what} has no header row")
    lowered = [norm_key(h) for h in headers if h]
    dupes = sorted({h for h in lowered if lowered.count(h) > 1})
    if dupes:
        raise ValueError(f"{what}: duplicate column names {dupes}")
    rows = []
    for raw in reader:
        if raw.get(None):
            raise ValueError(f"{what}, line {reader.line_num}: more cells than header columns "
                             f"({len(headers)}); quote any text that contains the delimiter")
        row = {(k or "").strip(): (v.strip() if isinstance(v, str) else "") for k, v in raw.items() if k is not None}
        if all(v == "" for v in row.values()):
            continue
        rows.append(row)
    if not rows:
        raise ValueError(f"{what} has a header but no data rows")
    return rows, headers


def column_map(headers, what, required):
    """Map canonical field -> actual header name."""
    present = {norm_key(h): h for h in headers if h}
    found = {}
    for field, aliases in ALIASES.items():
        for a in aliases:
            if a in present:
                found[field] = present[a]
                break
    missing = [f for f in required if f not in found]
    if missing:
        raise ValueError(f"{what}: missing column(s) {missing}; found {[h for h in headers if h]}. "
                         f"Expected at least: {', '.join(required)}")
    return found


def parse_date(raw):
    if not raw:
        return None, False
    if not DATE_RE.match(raw):
        return None, True
    try:
        return dt.date.fromisoformat(raw), False
    except ValueError:
        return None, True


def natural_key(text):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", text or "")]


def clip(text, width):
    text = " ".join(str(text).split())
    return text if len(text) <= width else text[: width - 3] + "..."


# --------------------------------------------------------------------------- analysis
def parse_items(rows, cols):
    items, problems, warnings = [], [], []
    seen = {}
    has = {f: f in cols for f in ALIASES}
    for n, row in enumerate(rows, 1):
        g = {f: (row.get(h) or "").strip() for f, h in cols.items()}
        iid = g.get("id", "")
        label = f"row {n}" + (f" ({iid})" if iid else "")
        it = {"row": n, "id": iid or f"row-{n}", "raw": row, "problems": [], "warnings": []}

        def prob(msg):
            it["problems"].append(msg)
            problems.append(f"{label}: {msg}")

        def warn(msg):
            it["warnings"].append(msg)
            warnings.append(f"{label}: {msg}")

        if not iid:
            prob("no id")
        elif iid.lower() in seen:
            prob(f"duplicate id (also row {seen[iid.lower()]})")
        else:
            seen[iid.lower()] = n
        traw = g.get("type", "").lower()
        if traw in TYPES:
            it["type"] = TYPES[traw]
        else:
            it["type"] = traw or "?"
            if traw in MISPLACED_TYPES:
                prob(f"type '{g['type']}': {MISPLACED_TYPES[traw]}")
            else:
                prob(f"type '{g.get('type', '')}' is not issue, action, decision or dependency")
        it["description"] = g.get("description", "")
        if not it["description"]:
            prob("no description")
        owner = g.get("owner", "")
        it["owner"] = owner or "(none)"
        if not owner:
            prob("no owner: an item with no owner is noticed, not managed")
        elif owner.lower() in GROUP_OWNERS:
            prob(f"owner '{owner}' is not a named person")
        elif MULTI_OWNER_RE.search(re.sub(r"\([^()]*\)", "", owner)):
            prob(f"owner '{owner}' names more than one person: split the item or pick one owner")
        praw = g.get("priority", "").lower()
        it["priority"] = PRIORITIES.get(praw, g.get("priority", "") or "?")
        if praw not in PRIORITIES:
            prob(f"priority '{g.get('priority', '')}' is not High, Medium or Low")
        sraw = " ".join(g.get("status", "").lower().replace("_", " ").split())
        it["status"] = STATUSES.get(sraw, g.get("status", "") or "?")
        if sraw not in STATUSES:
            prob(f"status '{g.get('status', '')}' is not Open, In progress, Blocked, Closed or Transferred")
        it["open"] = it["status"] in OPEN_STATUSES
        it["done"] = it["status"] in ("Closed", "Transferred")
        for field in ("due", "raised", "closed"):
            value, bad = parse_date(g.get(field, ""))
            it[field] = value
            if bad:
                prob(f"{field} '{g[field]}' is not a date (use YYYY-MM-DD)")
        if it["open"] and it["due"] is None and not g.get("due"):
            prob("open item with no due date")
        it["impact"] = g.get("impact", "")
        it["links"] = g.get("links", "")
        it["escalated_to"] = g.get("escalated_to", "")
        it["resolution"] = g.get("resolution", "")
        if it["done"] and not it["resolution"]:
            prob(f"{it['status']} with no resolution: record how it was resolved"
                 + (" (for a decision: what, who, why)" if it["type"] == "decision" else ""))
        if it["done"] and has["closed"] and it["closed"] is None and not g.get("closed"):
            warn("closed with no closed date")
        if it["open"] and has["impact"] and it["type"] in ("issue", "dependency") and not it["impact"]:
            warn(f"open {it['type']} with no impact: say what it threatens")
        if it["raised"]:
            if it["due"] and it["due"] < it["raised"]:
                warn("due date is before the raised date")
            if it["closed"] and it["closed"] < it["raised"]:
                warn("closed date is before the raised date")
        items.append(it)
    if not has["resolution"]:
        warnings.append("log: no 'resolution' column, so closed items carry no record of what was done or decided")
    if any(i["done"] for i in items) and not has["closed"]:
        warnings.append("log: no 'closed' column, so closure dates are not recorded")
    if not has["impact"]:
        warnings.append("log: no 'impact' column, so items do not say what they threaten")
    return items, problems, warnings


def cross_check_risks(items, risk_rows, risk_headers, problems, warnings):
    present = {norm_key(h): h for h in risk_headers if h}
    id_col = next((present[a] for a in ("id", "risk_id", "ref") if a in present), None)
    st_col = next((present[a] for a in ("status", "state") if a in present), None)
    if id_col is None or st_col is None:
        raise ValueError(f"risk register: needs id and status columns; found {[h for h in risk_headers if h]}")
    issues = [i for i in items if i["type"] == "issue"]
    summary = {"occurred": [], "occurred_without_issue": [], "linked_but_open": []}
    for row in risk_rows:
        rid = (row.get(id_col) or "").strip()
        status = (row.get(st_col) or "").strip().lower()
        if not rid:
            continue
        pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(rid) + r"(?![A-Za-z0-9])", re.I)
        linking = [i["id"] for i in issues if pat.search(i["links"]) or pat.search(i["description"])]
        if status == "occurred":
            summary["occurred"].append(rid)
            if not linking:
                summary["occurred_without_issue"].append(rid)
                problems.append(f"risk {rid} is Occurred in the register but no issue in the log links it: "
                                "open an issue with the risk id in links")
        elif status in ("open", "active", "") and linking:
            summary["linked_but_open"].append(rid)
            warnings.append(f"{', '.join(linking)} links {rid}, which is still {row.get(st_col) or 'blank'} in the "
                            "risk register: if it has occurred, set it to Occurred and execute its response")
    return summary


def analyse(items, as_of, days):
    open_items = [i for i in items if i["open"]]
    for i in items:
        i["days_to_due"] = (i["due"] - as_of).days if (i["open"] and i["due"]) else None
        end = i["closed"] if (i["done"] and i["closed"]) else as_of
        i["days_open"] = (end - i["raised"]).days if i["raised"] else None
        flags = []
        if i["days_to_due"] is not None and i["days_to_due"] < 0:
            flags.append("overdue")
        elif i["days_to_due"] is not None and i["days_to_due"] <= days:
            flags.append("due-soon")
        if i["status"] == "Blocked":
            flags.append("blocked")
        if i["open"] and (i["type"] == "decision" or i["escalated_to"]):
            flags.append("for-steering")
        i["attention"] = flags

    def by_due(i):
        return (i["due"] or dt.date.max, PRIO_ORDER.get(i["priority"], 3), natural_key(i["id"]))

    overdue = sorted([i for i in open_items if "overdue" in i["attention"]], key=by_due)
    due_soon = sorted([i for i in open_items if "due-soon" in i["attention"]], key=by_due)
    blocked = sorted([i for i in open_items if "blocked" in i["attention"]], key=by_due)
    steering = sorted([i for i in open_items if "for-steering" in i["attention"]], key=by_due)
    owners = {}
    for i in open_items:
        o = owners.setdefault(i["owner"], {"owner": i["owner"], "open": 0, "high": 0, "overdue": 0, "oldest_days": None})
        o["open"] += 1
        o["high"] += i["priority"] == "High"
        o["overdue"] += "overdue" in i["attention"]
        if i["days_open"] is not None:
            o["oldest_days"] = max(o["oldest_days"] or 0, i["days_open"])
    owner_rows = sorted(owners.values(), key=lambda o: (-o["overdue"], -o["high"], -o["open"], o["owner"].lower()))
    types = []
    for t in TYPE_ORDER + tuple(sorted({i["type"] for i in items} - set(TYPE_ORDER))):
        sub = [i for i in items if i["type"] == t]
        if not sub:
            continue
        op = [i for i in sub if i["open"]]
        types.append({"type": t, "total": len(sub), "open": len(op),
                      "high_open": sum(1 for i in op if i["priority"] == "High"),
                      "overdue": sum(1 for i in op if "overdue" in i["attention"]),
                      "due_soon": sum(1 for i in op if "due-soon" in i["attention"])})
    return {"overdue": overdue, "due_soon": due_soon, "blocked": blocked, "steering": steering,
            "owners": owner_rows, "types": types, "open_count": len(open_items),
            "done_count": sum(1 for i in items if i["done"])}


def overdue_unescalated(report, warnings):
    for i in report["overdue"]:
        if i["priority"] == "High" and not i["escalated_to"]:
            msg = f"row {i['row']} ({i['id']}): High and {-i['days_to_due']} day(s) overdue but not escalated"
            i["warnings"].append(msg.split(": ", 1)[1])
            warnings.append(msg)


# --------------------------------------------------------------------------- output
def aligned(header, rows):
    widths = [max(len(str(c)) for c in col) for col in zip(header, *rows)] if rows else [len(h) for h in header]
    fmt = lambda cells: "  ".join(str(c).ljust(w) for c, w in zip(cells, widths)).rstrip()
    out = [fmt(header), fmt(["-" * w for w in widths])]
    out += [fmt(r) for r in rows]
    return out


def item_rows(items, extra):
    rows = []
    for i in items:
        due = i["due"].isoformat() if i["due"] else "-"
        base = [i["id"], i["type"], i["priority"], i["owner"], due]
        rows.append(base + [extra(i), clip(i["description"], DESC_WIDTH)])
    return rows


def when(i):
    d = i["days_to_due"]
    if d is None:
        return "-"
    if d < 0:
        return f"{-d}d late"
    return "today" if d == 0 else f"in {d}d"


def render_table(items, report, problems, warnings, args, as_of, risk_summary, result):
    out = [f"Issue log check - as of {as_of.isoformat()} (due-soon window {args.days} days)",
           f"{len(items)} items: {report['open_count']} open, {report['done_count']} closed or transferred", ""]
    out += aligned(["Type", "Total", "Open", "High open", "Overdue", "Due soon"],
                   [[t["type"], t["total"], t["open"], t["high_open"], t["overdue"], t["due_soon"]] for t in report["types"]])
    sections = (
        (f"OVERDUE ({len(report['overdue'])})", report["overdue"], "Late", when),
        (f"DUE IN THE NEXT {args.days} DAYS ({len(report['due_soon'])})", report["due_soon"], "When", when),
        (f"BLOCKED ({len(report['blocked'])})", report["blocked"], "When", when),
        (f"FOR STEERING ({len(report['steering'])}) - open decisions and escalated items", report["steering"],
         "Escalated to", lambda i: i["escalated_to"] or "-"),
    )
    for title, sub, col, fn in sections:
        out += ["", title]
        out += aligned(["ID", "Type", "Priority", "Owner", "Due", col, "Description"], item_rows(sub, fn)) if sub else ["none"]
    out += ["", "OPEN ITEMS BY OWNER"]
    if report["owners"]:
        out += aligned(["Owner", "Open", "High", "Overdue", "Oldest (days)"],
                       [[o["owner"], o["open"], o["high"], o["overdue"],
                         "-" if o["oldest_days"] is None else o["oldest_days"]] for o in report["owners"]])
    else:
        out += ["none"]
    if risk_summary is not None:
        out += ["", f"RISK CROSS-CHECK: {len(risk_summary['occurred'])} occurred risk(s) in the register, "
                    f"{len(risk_summary['occurred_without_issue'])} without a linked issue"]
    out += ["", f"PROBLEMS ({len(problems)})"] + ([f"- {p}" for p in problems] or ["none"])
    out += ["", f"WARNINGS ({len(warnings)})"] + ([f"- {w}" for w in warnings] or ["none"])
    out += ["", result]
    return "\n".join(out)


def item_json(i):
    return {"id": i["id"], "row": i["row"], "type": i["type"], "description": i["description"],
            "owner": i["owner"], "priority": i["priority"], "status": i["status"],
            "due": i["due"].isoformat() if i["due"] else None, "days_to_due": i["days_to_due"],
            "days_open": i["days_open"], "impact": i["impact"], "links": i["links"],
            "escalated_to": i["escalated_to"], "attention": i["attention"],
            "problems": i["problems"], "warnings": i["warnings"]}


def render_json(items, report, problems, warnings, args, as_of, risk_summary, status):
    data = {
        "as_of": as_of.isoformat(), "window_days": args.days, "result": status,
        "summary": {"items": len(items), "open": report["open_count"], "closed_or_transferred": report["done_count"],
                    "overdue": len(report["overdue"]), "due_soon": len(report["due_soon"]),
                    "blocked": len(report["blocked"]), "for_steering": len(report["steering"]),
                    "problems": len(problems), "warnings": len(warnings), "by_type": report["types"]},
        "overdue": [item_json(i) for i in report["overdue"]],
        "due_soon": [item_json(i) for i in report["due_soon"]],
        "blocked": [item_json(i) for i in report["blocked"]],
        "for_steering": [item_json(i) for i in report["steering"]],
        "owners": report["owners"], "problems": problems, "warnings": warnings,
        "items": [item_json(i) for i in items],
    }
    if risk_summary is not None:
        data["risk_cross_check"] = risk_summary
    return json.dumps(data, indent=2, ensure_ascii=False)


def render_csv(items, headers):
    buf = io.StringIO()
    extra = ["group", "days_to_due", "days_open", "attention", "problems"]
    # computed columns already in the input (a re-imported csv output) are dropped and written fresh
    base = [h for h in headers if h and h.strip().lower() not in extra]
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(base + extra)
    for i in items:
        group = "open" if i["open"] else ("done" if i["done"] else "unknown")
        w.writerow([i["raw"].get(h, "") for h in base] + [
            group, "" if i["days_to_due"] is None else i["days_to_due"],
            "" if i["days_open"] is None else i["days_open"], ";".join(i["attention"]), "; ".join(i["problems"])])
    return buf.getvalue().rstrip("\n")


# --------------------------------------------------------------------------- main
def build_parser():
    doc = (__doc__ or "Check a project issue log.\n\n").split("\n\n", 1)
    epilog = re.sub(r"\nOPTIONS\n.*?\n(?=EXIT CODES)", "\n", doc[1], flags=re.S)
    p = argparse.ArgumentParser(prog="issue_log_check.py", description=doc[0].replace("\n", " "),
                                formatter_class=argparse.RawDescriptionHelpFormatter, epilog=epilog)
    p.add_argument("path", help="CSV/JSON issue log, or - for stdin")
    p.add_argument("--json", action="store_true", help="parse the input as JSON (auto-detected when it starts with [ or {)")
    p.add_argument("--as-of", default=None, metavar="DATE", help="status date YYYY-MM-DD (default: today)")
    p.add_argument("--days", type=int, default=7, metavar="N", help="due-soon window in days, 0-366 (default 7)")
    p.add_argument("--risks", default=None, metavar="PATH",
                   help="risk register CSV/JSON (id, status) to check every Occurred risk has a linked issue")
    p.add_argument("--strict", action="store_true", help="also fail (exit 1) when any open item is overdue")
    p.add_argument("--format", choices=("table", "json", "csv"), default="table", help="output format (default table)")
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.as_of is None:
        as_of = dt.date.today()
    else:
        as_of, bad = parse_date(args.as_of.strip())
        if bad or as_of is None:
            parser.error(f"--as-of must be a date YYYY-MM-DD, got {args.as_of!r}")
    if not 0 <= args.days <= 366:
        parser.error(f"--days must be between 0 and 366, got {args.days}")
    if args.risks is not None and args.risks == "-" and args.path == "-":
        parser.error("only one of the log and --risks can be read from stdin")
    try:
        try:
            sys.stdout.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
        try:
            text = read_text(args.path)
        except UnicodeDecodeError as exc:
            raise ValueError(f"{args.path} is not UTF-8 text ({exc.reason}); save it as UTF-8 / 'CSV UTF-8'")
        rows, headers = load_rows(text, args.json, "issue log")
        cols = column_map(headers, "issue log", REQUIRED)
        items, problems, warnings = parse_items(rows, cols)
        risk_summary = None
        if args.risks is not None:
            try:
                rtext = read_text(args.risks)
            except UnicodeDecodeError as exc:
                raise ValueError(f"{args.risks} is not UTF-8 text ({exc.reason})")
            rrows, rheaders = load_rows(rtext, False, "risk register")
            risk_summary = cross_check_risks(items, rrows, rheaders, problems, warnings)
        report = analyse(items, as_of, args.days)
        overdue_unescalated(report, warnings)
        failed = bool(problems) or (args.strict and bool(report["overdue"]))
        if problems:
            result = f"RESULT: FAIL - {len(problems)} problem(s) leave items unmanaged; fix them before the review"
        elif failed:
            result = f"RESULT: FAIL (--strict) - {len(report['overdue'])} open item(s) overdue"
        else:
            result = "RESULT: PASS - every item is typed, owned, prioritised and dated; closed items record a resolution"
        status = "FAIL" if failed else "PASS"
        if args.format == "json":
            print(render_json(items, report, problems, warnings, args, as_of, risk_summary, status))
        elif args.format == "csv":
            print(render_csv(items, headers))
        else:
            print(render_table(items, report, problems, warnings, args, as_of, risk_summary, result))
    except (OSError, ValueError, TypeError, OverflowError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
