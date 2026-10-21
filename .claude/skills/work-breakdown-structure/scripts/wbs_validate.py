#!/usr/bin/env python3
"""Validate a work breakdown structure (WBS) and turn it into the planning hand-offs.

Reads a WBS from CSV or JSON, infers every element's parent from its dotted id (the
parent of 1.3.2 is 1.3; an id without a dot is top level), prints the WBS as an indented
tree, then a validation report and a PASS/FAIL verdict. Optional flags suggest or write
corrected weights, roll the weights up into each element's share of the whole project,
allocate a budget to the work packages and control accounts, and export the work
packages in the estimation-worksheet format. Standard library only.

INPUT COLUMNS / KEYS  (case-insensitive; spacing, underscores and punctuation in a header are
ignored, so "WBS id", "wbs_id" and "wbsid" are one column, as are "Weight (%)" and "weight")
    id        dotted identifier: 1, 1.3, 1.3.2 ...     aliases: wbs id, wbs_id, wbs, code, wbs code, element id  (required)
    name      element name                            aliases: element, deliverable, title, work package, task (optional)
    weight    percent of the PARENT (effort/cost/value) aliases: weight (%), weight %, weight pct, pct, percent (optional)
    control account   id (or name) of the element where cost/schedule performance is measured     (optional)
    any other column (owner, description, acceptance criterion, ...) is carried through:
    --require checks it on work packages, --fix preserves it, --format md|csv|json prints it.
  Weights are finite numbers >= 0; a trailing '%', thousands separators and currency signs are
  stripped ("35%" -> 35); 'nan', 'inf', negatives and booleans are rejected; a blank weight
  means "not weighted". Ids: every dotted segment must be non-empty ("1.", "1..2" and blank
  ids are rejected) and spaces inside an id are removed ("1. 1" -> "1.1"). In JSON, ids MUST
  be strings: a number loses its trailing zeros (1.10 becomes 1.1) and is rejected with a hint.
  CSV: the delimiter is auto-detected (, ; tab |) or forced with --delimiter; a UTF-8 BOM and
  CRLF line ends are tolerated; blank lines are skipped. JSON: a list of objects or
  {"wbs": [...]}; pass --json (always, also for JSON on stdin).

CHECKS
  ERROR  duplicate id             the same id on two rows
  ERROR  orphan                   a dotted id whose parent id does not exist
  ERROR  100% rule                a parent's children must have weights summing to 100 (+/- --tolerance,
                                  default 0.1, applied to the rounded sum); the top level is checked the
                                  same way when several top-level elements carry weights
  ERROR  partly weighted          if ANY child of a parent has a weight, every child must have one
  ERROR  --require col[,col]      a work package (leaf) with a blank value in a required column
  WARN   single child             a parent with exactly one child is a rename, not a decomposition
  WARN   leading zeros            sibling ids that differ only by leading zeros (1.01 vs 1.1)
  WARN   root weight              a weight on a single top-level element is ignored (the root is 100%)
  WARN   several roots            more than one top-level element and none of them is weighted
  WARN   --max-children N         a parent with more than N children (flat list, no real structure)
  WARN   uneven decomposition     work packages whose levels differ by more than 2
  WARN   control account          a value that matches no element, or is not the element or an ancestor
  WARN   --max-leaf-share PCT     with --rollup: a work package above PCT% of the project (default 20)
  --strict turns warnings into a FAIL (exit 1) for CI gates.

FORMULAS
  share of project (--rollup)    share(root) = 100 (or its own weight when several roots are weighted);
                                 share(e) = share(parent) x weight(e) / 100; "n/a" when a weight on the chain is missing
  budget (--budget AMOUNT)       work package = AMOUNT x share / 100 rounded to the cent by largest remainder, so the
                                 work packages sum to exactly AMOUNT when their shares total 100 (within tolerance);
                                 a summary element = the sum of its children; a control account = the sum of the
                                 work packages assigned to it
  normalised weights (--suggest) w_i x 100 / sum(w), rounded to 0.1 by largest remainder so the result sums to exactly
                                 100.0 (33.3/33.3/33.3 -> 33.4/33.3/33.3); when the weighted siblings total less than
                                 100, the unweighted ones get the remainder split equally
  --fix OUT.csv                  writes the input with every fixable suggestion applied (normalised weights, stub rows
                                 for missing parents, renumbered duplicates, dropped root weight), all other columns
                                 untouched; the exit code still reflects the INPUT, so re-run the validator on OUT.csv

OUTPUT   --format table (default) | json | csv | md.  csv prints the element rows to stdout and the one-line
         verdict to stderr; md prints the WBS dictionary table for assets/wbs-template.md.

EXIT CODES   0 PASS  -  1 FAIL (errors, or warnings with --strict)  -  2 bad input, bad option or internal
             error ("error: ..." on stderr, never a traceback)

EXAMPLES
  python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py .claude/skills/work-breakdown-structure/assets/wbs-sample.csv
  python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py .claude/skills/work-breakdown-structure/assets/wbs-sample.csv --rollup --budget 500000
  python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py my-wbs.csv --suggest --fix my-wbs-fixed.csv
  python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py my-wbs.csv --require owner,acceptance --max-children 7 --strict
  python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py my-wbs.csv --export-estimation estimation-worksheet.csv
  python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py my-wbs.csv --format md > wbs-dictionary.md
  python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py my-wbs.json --json --format json
  cat my-wbs.csv | python .claude/skills/work-breakdown-structure/scripts/wbs_validate.py - --rollup --format csv > wbs-rollup.csv
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import os
import re
import sys

BOM = "﻿"
JSON_KEY = "wbs"
NAME_WIDTH = 42
DEFAULT_TOLERANCE = 0.1
DEFAULT_MAX_LEAF_SHARE = 20.0
MAX_LEVEL_SPREAD = 2

ID_ALIASES = ("id", "wbs id", "wbs_id", "wbs", "code", "wbs code", "element id")
NAME_ALIASES = ("name", "element", "deliverable", "title", "work package", "task")
WEIGHT_ALIASES = ("weight", "weight (%)", "weight %", "weight pct", "pct", "percent")
CONTROL_ACCOUNT_ALIASES = ("control account", "control_account", "ca id")
ESTIMATION_COLUMNS = ("id", "task", "unit", "technique", "optimistic", "most_likely",
                      "pessimistic", "assumptions", "estimators", "actual")
FORMATS = ("table", "json", "csv", "md")


# ----------------------------------------------------------------------------- input helpers
def _norm(key):
    """Header normalisation: BOM stripped, lower-cased, everything but a-z0-9 dropped."""
    return re.sub(r"[^a-z0-9]", "", str(key).lstrip(BOM).lower())


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


def load_rows(text, as_json, json_key, delimiter=None):
    """Return (rows, headers, lines). CSV auto-detects , ; tab | unless delimiter is given.
    JSON: a list of objects or {json_key: [...]}. lines holds the CSV line number per row
    (None for JSON) so errors can point at the editor line."""
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
        return rows, headers, [None] * len(rows)
    delim = delimiter or sniff_delimiter(text)
    reader = csv.DictReader(io.StringIO(text), delimiter=delim)
    headers = [(h or "").strip() for h in (reader.fieldnames or [])]
    if not any(headers):
        raise ValueError("input is empty (no header row)")
    normed = [_norm(h) for h in headers if h and _norm(h)]
    dupes = sorted({h for h in normed if normed.count(h) > 1})
    if dupes:
        raise ValueError(f"duplicate column names (after ignoring case and punctuation): {dupes}")
    rows, lines = [], []
    for raw in reader:
        if raw.get(None):
            raise ValueError(f"line {reader.line_num}: more cells than header columns ({len(headers)})")
        row = {(k or "").strip(): (v.strip() if isinstance(v, str) else v) for k, v in raw.items() if k is not None}
        if all(v in (None, "") for v in row.values()):
            continue  # skip blank lines
        rows.append(row)
        lines.append(reader.line_num)
    if not rows:
        raise ValueError(f"no data rows found (headers: {headers})")
    return rows, headers, lines


def _get(row, *names, default=None):
    """Case-insensitive lookup across accepted column aliases (spacing/punctuation ignored)."""
    lowered = {_norm(k): v for k, v in row.items() if k is not None}
    for n in names:
        v = lowered.get(_norm(n))
        if v not in (None, ""):
            return v
    return default


def require_columns(headers, groups):
    """groups = [("id","wbs id",...)]: each group needs one alias present; hints at the usual causes."""
    present = {_norm(h) for h in headers if h}
    missing = [g[0] for g in groups if not any(_norm(a) in present for a in g)]
    if missing:
        found = [h for h in headers if h]
        hints = [f"accepted names for '{g[0]}': {', '.join(g)}" for g in groups if g[0] in missing]
        if len(found) == 1:
            for d, label in ((";", "';'"), ("\t", "tab"), ("|", "'|'")):
                if d in found[0]:
                    hints.append(f"the header looks {label}-delimited; pass --delimiter {label.strip(chr(39))!r}")
                    break
        raise ValueError(f"missing column(s): {missing}; found headers: {found} ({'; '.join(hints)})")


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
    """Fixed decimals with thousands separators; never '-0.00'."""
    s = f"{x:,.{places}f}"
    return s.replace("-", "") if float(s.replace(",", "")) == 0 else s


def _fmt_w(x):
    """A weight/percent: at most two decimals, trailing zeros trimmed (35, 33.3, 12.75)."""
    r = round(x, 2)
    if r == int(r):
        return str(int(r))
    return f"{r:.2f}".rstrip("0").rstrip(".")


def _title(header):
    s = header.replace("_", " ").strip()
    return s[:1].upper() + s[1:]


def _table(headers, rows, numeric=()):
    """Aligned text table: numeric column indexes are right-aligned."""
    cells = [[_sanitize(h) for h in headers]] + [[_sanitize(c) for c in r] for r in rows]
    widths = [max(len(r[i]) for r in cells) for i in range(len(headers))]
    out = []
    for r in cells:
        out.append("  ".join(c.rjust(widths[i]) if i in numeric else c.ljust(widths[i])
                             for i, c in enumerate(r)).rstrip())
    return out


# ----------------------------------------------------------------------------- ids and parsing
def _is_int_seg(s):
    return s.isascii() and s.isdigit()


def _sort_key_of(eid):
    """Type-homogeneous sort key: numeric segments by value, others alphabetically after them."""
    return [(0, int(s), "") if _is_int_seg(s) else (1, 0, s.lower()) for s in eid.split(".")]


def _norm_id(eid):
    """Id with leading zeros removed from numeric segments (1.01 -> 1.1) to spot near-duplicates."""
    return ".".join(str(int(s)) if _is_int_seg(s) else s for s in eid.split("."))


def _parent_of(eid):
    return eid.rsplit(".", 1)[0] if "." in eid else None


def parse(rows, headers, lines):
    """Turn input rows into element dicts; raises ValueError naming row, id and column."""
    require_columns(headers, [ID_ALIASES])
    known = {_norm(a) for a in ID_ALIASES + NAME_ALIASES + WEIGHT_ALIASES}
    for h in headers:
        if h and _norm(h) not in known and ("weight" in _norm(h) or "percent" in _norm(h) or "%" in h):
            raise ValueError(f"column {h!r} looks like a weight column but is not an accepted name "
                             f"({', '.join(WEIGHT_ALIASES)}); rename it or drop it")
    extra_headers = [h for h in headers if h and _norm(h) and _norm(h) not in known]
    elements = []
    for i, (row, line) in enumerate(zip(rows, lines), start=1):
        where = f"row {i}" + (f" (line {line})" if line else "")
        rid_raw = _get(row, *ID_ALIASES)
        if rid_raw is None or (isinstance(rid_raw, str) and not rid_raw.strip()):
            raise ValueError(f"{where}: id is blank")
        if not isinstance(rid_raw, str):
            raise ValueError(f"{where}: id must be a string, got {rid_raw!r}; write it as \"{rid_raw}\" "
                             f"(JSON numbers lose their trailing zeros, so 1.10 would become 1.1)")
        segs = [s.strip() for s in rid_raw.strip().split(".")]
        if any(s == "" for s in segs):
            raise ValueError(f"{where}: id {rid_raw.strip()!r} has an empty segment (leading, trailing or double dot)")
        rid = ".".join(segs)
        where = f"row {i} ({rid}" + (f", line {line})" if line else ")")
        name = _sanitize(_get(row, *NAME_ALIASES, default=""))
        w_raw = _get(row, *WEIGHT_ALIASES)
        weight = None
        if w_raw is not None and not (isinstance(w_raw, str) and not w_raw.strip()):
            weight = _num(w_raw, f"{where}, column weight", minimum=0)
        extra = {h: _sanitize(row.get(h, "")) for h in extra_headers}
        elements.append({
            "row": i, "line": line, "raw": row,
            "id": rid, "parent": _parent_of(rid), "level": len(segs),
            "name": name, "weight": weight,
            "control_account": _sanitize(_get(row, *CONTROL_ACCOUNT_ALIASES, default="")),
            "extra": extra, "sort_key": _sort_key_of(rid), "norm_id": _norm_id(rid),
            "share": None, "budget": None, "ca_id": None,
        })
    return elements, extra_headers


# ----------------------------------------------------------------------------- analysis
def normalise(values, total=100.0, decimals=1):
    """Scale values to sum to `total`, rounded to `decimals` by largest remainder (exact sum)."""
    s = sum(values)
    if s <= 0:
        return None
    scale = 10 ** decimals
    target = round(total * scale)
    raw = [v / s * target for v in values]
    base = [math.floor(round(r, 6)) for r in raw]
    rem = target - sum(base)
    order = sorted(range(len(raw)), key=lambda i: raw[i] - base[i], reverse=True)
    for i in order[:max(rem, 0)]:
        base[i] += 1
    return [b / scale for b in base]


def _next_free_id(eid, taken):
    """Next unused sibling id: numeric last segment + 1 past the highest sibling, else a -2/-3 suffix."""
    parent = _parent_of(eid)
    last = eid.rsplit(".", 1)[-1]
    prefix = f"{parent}." if parent else ""
    if _is_int_seg(last):
        nums = [int(t.rsplit(".", 1)[-1]) for t in taken
                if _parent_of(t) == parent and _is_int_seg(t.rsplit(".", 1)[-1])]
        n = (max(nums) if nums else 0) + 1
        while f"{prefix}{n}" in taken:
            n += 1
        cand = f"{prefix}{n}"
    else:
        n = 2
        while f"{eid}-{n}" in taken:
            n += 1
        cand = f"{eid}-{n}"
    taken.add(cand)
    return cand


def _resolve_required(names, extra_headers):
    """Map --require names to ('label', getter) pairs; unknown names are an error."""
    resolved = []
    for req in names:
        key = _norm(req)
        if key in {_norm(a) for a in NAME_ALIASES}:
            resolved.append(("name", lambda e: e["name"]))
            continue
        if key in {_norm(a) for a in WEIGHT_ALIASES}:
            resolved.append(("weight", lambda e: e["weight"] is not None))
            continue
        exact = [h for h in extra_headers if _norm(h) == key]
        partial = [h for h in extra_headers if key and key in _norm(h)]
        match = exact or (partial if len(partial) == 1 else [])
        if not match:
            raise ValueError(f"--require: column '{req}' not found; columns present: "
                             f"{['id', 'name', 'weight'] + extra_headers}")
        h = match[0]
        resolved.append((h, lambda e, h=h: e["extra"].get(h, "")))
    return resolved


def analyse(elements, extra_headers, tol=DEFAULT_TOLERANCE, max_children=None, require=(),
            rollup=False, budget=None, max_leaf_share=DEFAULT_MAX_LEAF_SHARE):
    errors, warnings, notes, suggestions = [], [], [], []

    # duplicates
    by_id = {}
    for e in elements:
        if e["id"] in by_id:
            errors.append(f"duplicate id '{e['id']}' (row {e['row']} repeats row {by_id[e['id']]['row']})")
            e["duplicate"] = True
        else:
            by_id[e["id"]] = e
    idset = set(by_id)
    taken = set(idset)

    # children / leaves
    children, roots = {}, []
    for e in elements:
        if e["parent"] is None:
            roots.append(e)
        else:
            children.setdefault(e["parent"], []).append(e)
    for e in elements:
        e["is_leaf"] = e["id"] not in children
    leaves = [e for e in elements if e["is_leaf"]]

    # orphans -> stub suggestions for every missing ancestor
    stubs_seen = set()
    for e in elements:
        p = e["parent"]
        if p is None or p in idset:
            continue
        errors.append(f"orphan id '{e['id']}' (row {e['row']}): parent '{p}' does not exist")
        chain = []
        q = p
        while q is not None and q not in idset:
            chain.append(q)
            q = _parent_of(q)
        for m in reversed(chain):
            if m in stubs_seen:
                continue
            stubs_seen.add(m)
            taken.add(m)
            suggestions.append({"kind": "stub", "id": m, "name": f"<name for {m}>", "before": e, "fixable": True,
                                "message": f"add a row for the missing parent '{m}' above '{e['id']}' "
                                           f"(name it, e.g. '<name for {m}>') - or renumber '{e['id']}' "
                                           f"under an existing element"})

    # duplicates -> renumber suggestions (children stay with the first occurrence)
    for e in elements:
        if e.get("duplicate"):
            new = _next_free_id(e["id"], taken)
            suggestions.append({"kind": "renumber", "element": e, "new_id": new, "descendants": False,
                                "fixable": True,
                                "message": f"renumber the second '{e['id']}' (row {e['row']}) to '{new}' "
                                           f"(any children stay under the first '{e['id']}')"})

    # near-duplicates differing only by leading zeros
    groups = {}
    for e in elements:
        grp = groups.setdefault(e["norm_id"], [])
        if all(g["id"] != e["id"] for g in grp):
            grp.append(e)
    for grp in groups.values():
        if len(grp) > 1:
            ids = [g["id"] for g in grp]
            warnings.append(f"ids {ids} differ only by leading zeros - probable typo (they sort to the same position)")
            for g in grp[1:]:
                new = _next_free_id(g["id"], taken)
                suggestions.append({"kind": "renumber", "element": g, "new_id": new, "descendants": True,
                                    "fixable": True,
                                    "message": f"renumber '{g['id']}' (row {g['row']}) and its children to '{new}', "
                                               f"or merge it with '{grp[0]['id']}'"})

    # 100% rule per sibling group
    def check_group(label, kids):
        weighted = [k for k in kids if k["weight"] is not None]
        if not weighted:
            return None
        unweighted = [k for k in kids if k["weight"] is None]
        total = round(sum(k["weight"] for k in weighted), 6)
        if unweighted:
            errors.append(f"100% rule: {label} are only partly weighted (no weight on "
                          f"{', '.join(k['id'] for k in unweighted)}) - weight all siblings or none")
            remainder = round(100.0 - total, 6)
            if remainder > 0:
                split = normalise([1.0] * len(unweighted), total=remainder)
                suggestions.append({"kind": "weights", "targets": list(zip(unweighted, split)), "fixable": True,
                                    "message": f"{label}: the weighted siblings use {_fmt_w(total)}% - give the "
                                               f"remaining {_fmt_w(remainder)}% to "
                                               + ", ".join(f"{k['id']}={_fmt_w(w)}" for k, w in zip(unweighted, split))})
            else:
                norm = normalise([k["weight"] for k in weighted]) or normalise([1.0] * len(weighted))
                suggestions.append({"kind": "weights", "targets": [], "fixable": False,
                                    "message": f"{label}: the weighted siblings already use {_fmt_w(total)}% - either "
                                               f"remove {', '.join(k['id'] for k in unweighted)} or weight them and "
                                               f"rescale (weighted-only normalisation: "
                                               + ", ".join(f"{k['id']}={_fmt_w(w)}" for k, w in zip(weighted, norm))
                                               + ") - not applied by --fix"})
            return False
        if abs(total - 100.0) > tol + 1e-9:
            errors.append(f"100% rule: {label} have weights summing to {_fmt_w(total)} "
                          f"(off by {'+' if total > 100 else '-'}{_fmt_w(abs(total - 100.0))}; tolerance +/-{_fmt_w(tol)})")
            norm = normalise([k["weight"] for k in weighted]) or normalise([1.0] * len(weighted))
            suggestions.append({"kind": "weights", "targets": list(zip(weighted, norm)), "fixable": True,
                                "message": f"{label}: set "
                                           + ", ".join(f"{k['id']}={_fmt_w(w)}" for k, w in zip(weighted, norm))
                                           + (" (equal split - all weights were 0)" if total == 0 else " (normalised to 100)")})
            return False
        return True

    parents = sorted((p for p in children if p in idset), key=_sort_key_of)
    n_checked = 0
    for p in parents:
        kids = children[p]
        if check_group(f"children of '{p}'", kids) is not None:
            n_checked += 1
        if len(kids) == 1:
            warnings.append(f"single child: '{p}' has only one child ('{kids[0]['id']}') - a rename, not a decomposition")
        if max_children and len(kids) > max_children:
            warnings.append(f"'{p}' has {len(kids)} children (more than --max-children {max_children}) - "
                            f"group them under intermediate elements")
    top_checked = False
    if len(roots) > 1:
        if all(r["weight"] is None for r in roots):
            warnings.append(f"{len(roots)} top-level elements ({', '.join(r['id'] for r in roots)}) - a WBS "
                            f"usually has one project root; add it, or weight the top level so it can be checked")
        else:
            top_checked = check_group("top-level elements", roots) is not None
    elif roots and roots[0]["weight"] is not None:
        warnings.append(f"weight {_fmt_w(roots[0]['weight'])} on the single top-level element '{roots[0]['id']}' "
                        f"is ignored (the root is 100% by definition)")
        suggestions.append({"kind": "drop_weight", "element": roots[0], "fixable": True,
                            "message": f"remove the weight from '{roots[0]['id']}'"})

    # uneven decomposition
    if len(leaves) > 1:
        lo = min(leaves, key=lambda e: e["level"])
        hi = max(leaves, key=lambda e: e["level"])
        if hi["level"] - lo["level"] > MAX_LEVEL_SPREAD:
            warnings.append(f"uneven decomposition: work package '{lo['id']}' sits at level {lo['level']} while "
                            f"'{hi['id']}' sits at level {hi['level']} - branches differ by more than "
                            f"{MAX_LEVEL_SPREAD} levels")

    # required columns on work packages
    for label, getter in _resolve_required(require, extra_headers):
        for e in leaves:
            if not getter(e):
                errors.append(f"work package '{e['id']}' has no {label} (--require)")

    # control accounts
    name_index = {}
    for e in elements:
        if e["name"]:
            name_index.setdefault(e["name"].lower(), e["id"])
    for e in elements:
        ca = e["control_account"]
        if not ca:
            continue
        target = ca if ca in idset else name_index.get(ca.lower())
        if target is None:
            warnings.append(f"control account '{ca}' on '{e['id']}' matches no WBS id or name")
        elif not (e["id"] == target or e["id"].startswith(target + ".")):
            warnings.append(f"control account '{ca}' on '{e['id']}' is not that element or one of its ancestors")
        else:
            e["ca_id"] = target

    # shares of the whole project
    top_all_weighted = len(roots) > 1 and all(r["weight"] is not None for r in roots)
    for e in sorted(elements, key=lambda x: x["level"]):
        if e["parent"] is None:
            e["share"] = 100.0 if len(roots) == 1 else (e["weight"] if top_all_weighted else None)
        else:
            p = by_id.get(e["parent"])
            ps = p["share"] if p else None
            e["share"] = None if (ps is None or e["weight"] is None) else round(ps * e["weight"] / 100.0, 10)
    if rollup and max_leaf_share:
        for e in leaves:
            if e["share"] is not None and e["share"] > max_leaf_share + 1e-9:
                warnings.append(f"work package '{e['id']}' is {_fmt(e['share'])}% of the project (above "
                                f"--max-leaf-share {_fmt_w(max_leaf_share)}%) - decompose it further")
    allocable = [e for e in leaves if e["share"] is not None]
    leaf_total = round(sum(e["share"] for e in allocable), 6)

    # budget allocation
    if budget is not None:
        complete = bool(allocable) and len(allocable) == len(leaves) and abs(leaf_total - 100.0) <= tol + 1e-9
        cents = round(budget * 100)
        factor = 100.0 / leaf_total if complete else 1.0
        raw = [cents * e["share"] * factor / 100.0 for e in allocable]
        base = [math.floor(round(r, 6)) for r in raw]
        if complete:
            rem = cents - sum(base)
            order = sorted(range(len(raw)), key=lambda i: raw[i] - base[i], reverse=True)
            for i in order[:max(rem, 0)]:
                base[i] += 1
        for e, c in zip(allocable, base):
            e["budget"] = c / 100.0
        if not complete:
            missing = len(leaves) - len(allocable)
            notes.append(f"budget: work-package shares sum to {_fmt(leaf_total)}%"
                         + (f" and {missing} work package(s) have no share" if missing else "")
                         + f", so only {_fmt(sum(base) / 100.0)} of {_fmt(budget)} is allocated - fix the weights first")
        for e in sorted(elements, key=lambda x: -x["level"]):
            if not e["is_leaf"]:
                vals = [k["budget"] for k in children.get(e["id"], [])]
                e["budget"] = None if any(v is None for v in vals) else round(sum(vals), 2)

    stats = {
        "elements": len(elements), "work_packages": len(leaves),
        "levels": max((e["level"] for e in elements), default=0),
        "parents": len(parents), "parents_checked": n_checked, "top_level_checked": top_checked,
        "tolerance": tol, "budget": budget, "leaf_share_total": leaf_total if allocable else None,
        "work_packages_without_share": len(leaves) - len(allocable),
    }
    return {"elements": elements, "leaves": leaves, "children": children, "by_id": by_id,
            "errors": errors, "warnings": warnings, "notes": notes, "suggestions": suggestions, "stats": stats}


# ----------------------------------------------------------------------------- fixes and exports
def apply_fixes(elements, headers, suggestions):
    """Return (rows, headers, applied) with every fixable suggestion applied to copies of the input rows."""
    def find(aliases):
        return next((h for h in headers if _norm(h) in {_norm(a) for a in aliases}), None)
    headers_out = list(headers)
    id_h, name_h, w_h = find(ID_ALIASES), find(NAME_ALIASES), find(WEIGHT_ALIASES)
    new_ids = {id(e): e["id"] for e in elements}
    new_weights, stubs, applied = {}, [], []
    for s in suggestions:
        if not s.get("fixable"):
            continue
        if s["kind"] == "weights":
            for e, w in s["targets"]:
                new_weights[id(e)] = w
        elif s["kind"] == "drop_weight":
            new_weights[id(s["element"])] = None
        elif s["kind"] == "renumber":
            old, new = s["element"]["id"], s["new_id"]
            new_ids[id(s["element"])] = new
            if s["descendants"]:
                for x in elements:
                    if x is not s["element"] and x["id"].startswith(old + "."):
                        new_ids[id(x)] = new + x["id"][len(old):]
        elif s["kind"] == "stub":
            stubs.append(s)
        applied.append(s["message"])
    if new_weights and w_h is None:
        w_h = "weight"
        headers_out.append(w_h)
    if stubs and name_h is None:
        name_h = "name"
        headers_out.append(name_h)
    rows = []
    for e in elements:
        for s in stubs:
            if s["before"] is e:
                stub = {h: "" for h in headers_out}
                stub[id_h], stub[name_h] = s["id"], s["name"]
                rows.append(stub)
        row = {h: ("" if e["raw"].get(h) is None else str(e["raw"].get(h))) for h in headers_out}
        row[id_h] = new_ids[id(e)]
        if id(e) in new_weights:
            w = new_weights[id(e)]
            row[w_h] = "" if w is None else _fmt_w(w)
        rows.append(row)
    return rows, headers_out, applied


def write_csv(path, headers, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def estimation_rows(leaves):
    rows = []
    for e in sorted(leaves, key=lambda x: x["sort_key"]):
        row = {c: "" for c in ESTIMATION_COLUMNS}
        row["id"], row["task"] = e["id"], e["name"]
        rows.append(row)
    return rows


# ----------------------------------------------------------------------------- rendering
def _verdict(res, strict):
    n_err, n_warn = len(res["errors"]), len(res["warnings"])
    failed = n_err > 0 or (strict and n_warn > 0)
    line = f"{'FAIL' if failed else 'PASS'}: {n_err} error(s), {n_warn} warning(s)"
    if strict and n_warn and not n_err:
        line += " (--strict: warnings fail)"
    return failed, line


def _checked_line(st):
    if st["parents"] == 0 and not st["top_level_checked"]:
        return "100% rule not applicable (no parent has children)"
    if st["parents_checked"] == 0 and not st["top_level_checked"]:
        return f"100% rule NOT checked: no weights given ({st['parents']} parent(s) unweighted) - structural checks only"
    s = f"100% rule checked at {st['parents_checked']} of {st['parents']} parent(s)"
    if st["parents_checked"] < st["parents"]:
        s += f" ({st['parents'] - st['parents_checked']} unweighted)"
    if st["top_level_checked"]:
        s += " and at the top level"
    return s


def _share_cell(e):
    return "n/a" if e["share"] is None else _fmt(e["share"])


def _budget_cell(e):
    return "n/a" if e["budget"] is None else _fmt(e["budget"])


def _control_accounts(res):
    """Rows for the control-account table: (id, name, n work packages, share, budget)."""
    groups = {}
    for e in res["leaves"]:
        groups.setdefault(e["ca_id"], []).append(e)
    if list(groups) == [None]:
        return []
    out = []
    for ca in sorted((k for k in groups if k is not None), key=_sort_key_of):
        wps = groups[ca]
        shares = [w["share"] for w in wps]
        budgets = [w["budget"] for w in wps]
        out.append((ca, res["by_id"][ca]["name"], len(wps),
                    None if any(s is None for s in shares) else round(sum(shares), 6),
                    None if any(b is None for b in budgets) else round(sum(budgets), 2)))
    if None in groups:
        wps = groups[None]
        shares = [w["share"] for w in wps]
        budgets = [w["budget"] for w in wps]
        out.append(("(none)", "work packages without a control account", len(wps),
                    None if any(s is None for s in shares) else round(sum(shares), 6),
                    None if any(b is None for b in budgets) else round(sum(budgets), 2)))
    return out


def render_table(res, opts):
    st = res["stats"]
    show_share, show_budget = opts.rollup, st["budget"] is not None
    title = (f"Work breakdown structure: {st['elements']} element(s), {st['work_packages']} work package(s), "
             f"{st['levels']} level(s)")
    out = [title, "-" * len(title)]
    headers = ["id", "name", "type", "weight %"]
    numeric = {3}
    if show_share:
        headers.append("share %")
        numeric.add(4)
    if show_budget:
        headers.append("budget")
        numeric.add(len(headers) - 1)
    rows = []
    for e in sorted(res["elements"], key=lambda x: x["sort_key"]):
        row = ["  " * (e["level"] - 1) + e["id"], _sanitize(e["name"], NAME_WIDTH),
               "work package" if e["is_leaf"] else "summary",
               "-" if e["weight"] is None else _fmt_w(e["weight"])]
        if show_share:
            row.append(_share_cell(e))
        if show_budget:
            row.append(_budget_cell(e))
        rows.append(row)
    out += _table(headers, rows, numeric)

    if show_share:
        out += ["", "Work packages by share of project", "---------------------------------"]
        leaves = sorted(res["leaves"], key=lambda e: (-(e["share"] if e["share"] is not None else -1), e["sort_key"]))
        h2 = ["id", "name", "share %"] + (["budget"] if show_budget else [])
        rows = [[e["id"], _sanitize(e["name"], NAME_WIDTH), _share_cell(e)] + ([_budget_cell(e)] if show_budget else [])
                for e in leaves]
        total = ["total", f"{len(leaves)} work package(s)",
                 "n/a" if st["leaf_share_total"] is None or st["work_packages_without_share"] else _fmt(st["leaf_share_total"])]
        if show_budget:
            alloc = [e["budget"] for e in leaves]
            total.append("n/a" if any(b is None for b in alloc) else _fmt(sum(alloc)))
        rows.append(total)
        out += _table(h2, rows, {2, 3})
        cas = _control_accounts(res)
        if cas:
            out += ["", "Control accounts (where cost and schedule performance are measured)",
                    "-------------------------------------------------------------------"]
            h3 = ["account", "name", "work packages", "share %"] + (["budget"] if show_budget else [])
            rows = []
            for ca, name, n, share, bud in cas:
                row = [ca, _sanitize(name, NAME_WIDTH), str(n), "n/a" if share is None else _fmt(share)]
                if show_budget:
                    row.append("n/a" if bud is None else _fmt(bud))
                rows.append(row)
            out += _table(h3, rows, {2, 3, 4})

    out += ["", "Validation report", "-----------------"]
    for m in res["errors"]:
        out.append(f"  ERROR:   {m}")
    for m in res["warnings"]:
        out.append(f"  warning: {m}")
    for m in res["notes"]:
        out.append(f"  note:    {m}")
    if not (res["errors"] or res["warnings"] or res["notes"]):
        out.append("  (no issues)")
    if opts.suggest:
        out += ["", "Suggestions", "-----------"]
        if res["suggestions"]:
            for s in res["suggestions"]:
                out.append(f"  - {s['message']}")
        else:
            out.append("  (nothing to suggest)")
    for m in res.get("written", []):
        out.append(f"  {m}")
    out += ["", f"Checked: {_checked_line(st)}."]
    failed, line = _verdict(res, opts.strict)
    out.append(line)
    return "\n".join(out)


def element_rows(res, opts, extra_headers):
    rows = []
    for e in sorted(res["elements"], key=lambda x: x["sort_key"]):
        row = {"id": e["id"], "name": e["name"], "level": e["level"], "parent": e["parent"] or "",
               "type": "work package" if e["is_leaf"] else "summary", "weight": e["weight"]}
        if opts.rollup:
            row["share_pct"] = None if e["share"] is None else round(e["share"], 4)
        if res["stats"]["budget"] is not None:
            row["budget"] = e["budget"]
        for h in extra_headers:
            row[h] = e["extra"].get(h, "")
        rows.append(row)
    return rows


def render_json(res, opts, extra_headers):
    failed, line = _verdict(res, opts.strict)
    st = res["stats"]
    summary = {"status": "FAIL" if failed else "PASS", "verdict": line,
               "elements": st["elements"], "work_packages": st["work_packages"], "levels": st["levels"],
               "parents": st["parents"], "parents_checked": st["parents_checked"],
               "top_level_checked": st["top_level_checked"], "tolerance": st["tolerance"],
               "budget": st["budget"], "leaf_share_total": st["leaf_share_total"],
               "errors": res["errors"], "warnings": res["warnings"], "notes": res["notes"],
               "suggestions": [s["message"] for s in res["suggestions"]] if opts.suggest else [],
               "control_accounts": [{"id": ca, "name": n, "work_packages": k, "share_pct": s, "budget": b}
                                    for ca, n, k, s, b in _control_accounts(res)] if opts.rollup else [],
               "written": res.get("written", [])}
    return json.dumps({"rows": element_rows(res, opts, extra_headers), "summary": summary}, indent=2, ensure_ascii=False)


def render_csv(res, opts, extra_headers):
    rows = element_rows(res, opts, extra_headers)
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator="\n")
    writer.writeheader()
    for r in rows:
        r = dict(r)
        r["weight"] = "" if r["weight"] is None else _fmt_w(r["weight"])
        if "share_pct" in r:
            r["share_pct"] = "" if r["share_pct"] is None else f"{r['share_pct']:.4f}".rstrip("0").rstrip(".")
        if "budget" in r:
            r["budget"] = "" if r["budget"] is None else f"{r['budget']:.2f}"
        writer.writerow(r)
    return buf.getvalue().rstrip("\n")


def _md_cell(v):
    return _sanitize(v).replace("|", "\\|")


def _md_table(headers, rows):
    out = ["| " + " | ".join(_md_cell(h) for h in headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(_md_cell(c) for c in r) + " |")
    return out


def render_md(res, opts, extra_headers):
    st = res["stats"]
    show_share, show_budget = opts.rollup, st["budget"] is not None
    headers = ["WBS id", "Name", "Type", "Weight (%)"]
    if show_share:
        headers.append("Share of project (%)")
    if show_budget:
        headers.append("Budget")
    headers += [_title(h) for h in extra_headers]
    rows = []
    for e in sorted(res["elements"], key=lambda x: x["sort_key"]):
        row = [e["id"], e["name"], "work package" if e["is_leaf"] else "summary",
               "" if e["weight"] is None else _fmt_w(e["weight"])]
        if show_share:
            row.append(_share_cell(e))
        if show_budget:
            row.append(_budget_cell(e))
        row += [e["extra"].get(h, "") for h in extra_headers]
        rows.append(row)
    out = ["## WBS dictionary", ""] + _md_table(headers, rows)
    if show_share:
        cas = _control_accounts(res)
        if cas:
            out += ["", "## Control accounts", ""]
            h3 = ["Control account", "Name", "Work packages", "Share of project (%)"] + (["Budget"] if show_budget else [])
            rows = []
            for ca, name, n, share, bud in cas:
                row = [ca, name, str(n), "n/a" if share is None else _fmt(share)]
                if show_budget:
                    row.append("n/a" if bud is None else _fmt(bud))
                rows.append(row)
            out += _md_table(h3, rows)
    out += ["", "## Validation", ""]
    for m in res["errors"]:
        out.append(f"- ERROR: {m}")
    for m in res["warnings"]:
        out.append(f"- warning: {m}")
    for m in res["notes"]:
        out.append(f"- note: {m}")
    if opts.suggest:
        for s in res["suggestions"]:
            out.append(f"- suggestion: {s['message']}")
    if not (res["errors"] or res["warnings"] or res["notes"] or (opts.suggest and res["suggestions"])):
        out.append("- no issues")
    for m in res.get("written", []):
        out.append(f"- {m}")
    failed, line = _verdict(res, opts.strict)
    out += ["", f"**{line}** ({_checked_line(st)})"]
    return "\n".join(out)


# ----------------------------------------------------------------------------- CLI
def build_parser():
    parser = argparse.ArgumentParser(
        description="Validate a WBS (hierarchy, 100% rule, decomposition), suggest fixes, roll weights up "
                    "into shares and a budget, and export the work packages for estimation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("path", help="CSV or JSON WBS file, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="parse the input as JSON (a list of objects or {\"wbs\": [...]})")
    parser.add_argument("--delimiter", metavar="CHAR", help="CSV delimiter (default: auto-detect , ; tab |)")
    parser.add_argument("--tolerance", type=float, default=DEFAULT_TOLERANCE, metavar="PCT",
                        help="allowed deviation of a sibling group's weight sum from 100 (default %(default)s)")
    parser.add_argument("--suggest", action="store_true",
                        help="print suggestions: normalised weights for failing groups, stub rows for missing parents, "
                             "new numbers for duplicate ids")
    parser.add_argument("--fix", metavar="OUT.csv",
                        help="write the input with every fixable suggestion applied to OUT.csv (implies --suggest; "
                             "other columns are preserved; the exit code still reflects the input)")
    parser.add_argument("--rollup", action="store_true",
                        help="show each element's absolute share of the project, the work packages ranked by share, "
                             "and the control accounts")
    parser.add_argument("--budget", metavar="AMOUNT",
                        help="allocate AMOUNT to the work packages by rolled-up share (largest-remainder rounding to "
                             "the cent; implies --rollup)")
    parser.add_argument("--export-estimation", metavar="PATH",
                        help="write the work packages (id, task, blank O/M/P ...) in the estimation worksheet format "
                             "read by pert_estimate.py")
    parser.add_argument("--max-children", type=int, metavar="N",
                        help="warn when a parent has more than N children (default: off)")
    parser.add_argument("--max-leaf-share", type=float, default=DEFAULT_MAX_LEAF_SHARE, metavar="PCT",
                        help="with --rollup, warn when a work package exceeds PCT%% of the project (default %(default)s)")
    parser.add_argument("--require", metavar="COL[,COL]",
                        help="columns that every work package must fill, e.g. owner,acceptance (blank -> ERROR)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures (exit 1) for CI gates")
    parser.add_argument("--format", choices=FORMATS, default="table",
                        help="output format (default %(default)s); csv prints rows to stdout and the verdict to stderr")
    return parser


def _check_options(parser, args):
    if args.delimiter is not None and len(args.delimiter) != 1:
        parser.error("--delimiter must be a single character")
    if not math.isfinite(args.tolerance) or args.tolerance < 0 or args.tolerance >= 50:
        parser.error("--tolerance must be a finite percentage between 0 and 50")
    if not math.isfinite(args.max_leaf_share) or args.max_leaf_share <= 0 or args.max_leaf_share > 100:
        parser.error("--max-leaf-share must be a percentage above 0 and at most 100")
    if args.max_children is not None and args.max_children < 1:
        parser.error("--max-children must be a whole number of at least 1")
    budget = None
    if args.budget is not None:
        try:
            budget = _num(args.budget, "--budget", minimum=0)
        except ValueError as exc:
            parser.error(str(exc))
        if budget <= 0:
            parser.error("--budget must be greater than 0")
        args.rollup = True
    args.budget_value = budget
    args.require_list = [c.strip() for c in (args.require or "").split(",") if c.strip()]
    if args.require is not None and not args.require_list:
        parser.error("--require needs at least one column name")
    if args.fix:
        args.suggest = True
    for out in (args.fix, args.export_estimation):
        if out and args.path != "-" and os.path.abspath(out) == os.path.abspath(args.path):
            parser.error(f"refusing to overwrite the input file {args.path!r}; choose another output path")
    if args.fix and args.export_estimation and os.path.abspath(args.fix) == os.path.abspath(args.export_estimation):
        parser.error("--fix and --export-estimation must be different files")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    _check_options(parser, args)
    try:
        text = read_text(args.path)
        rows, headers, lines = load_rows(text, args.json, JSON_KEY, args.delimiter)
        elements, extra_headers = parse(rows, headers, lines)
        res = analyse(elements, extra_headers, tol=args.tolerance, max_children=args.max_children,
                      require=args.require_list, rollup=args.rollup, budget=args.budget_value,
                      max_leaf_share=args.max_leaf_share)
        res["written"] = []
        if args.fix:
            fixed_rows, fixed_headers, applied = apply_fixes(elements, headers, res["suggestions"])
            write_csv(args.fix, fixed_headers, fixed_rows)
            res["written"].append(f"wrote {args.fix} with {len(applied)} change(s) applied - re-run the validator on it")
        if args.export_estimation:
            write_csv(args.export_estimation, list(ESTIMATION_COLUMNS), estimation_rows(res["leaves"]))
            res["written"].append(f"wrote {len(res['leaves'])} work package(s) to {args.export_estimation} "
                                  f"for .claude/skills/estimation/scripts/pert_estimate.py")
        if args.format == "json":
            output = render_json(res, args, extra_headers)
        elif args.format == "csv":
            output = render_csv(res, args, extra_headers)
        elif args.format == "md":
            output = render_md(res, args, extra_headers)
        else:
            output = render_table(res, args)
        failed, verdict = _verdict(res, args.strict)
    except (OSError, ValueError, TypeError, UnicodeDecodeError, OverflowError, ZeroDivisionError,
            KeyError, IndexError, RecursionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(output)
    if args.format == "csv":
        print(verdict, file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
