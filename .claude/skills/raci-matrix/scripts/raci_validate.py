#!/usr/bin/env python3
"""Validate a responsibility assignment matrix (RACI, RASCI or DACI) and suggest fixes.

Reads the matrix from CSV or JSON, prints it back with canonical cells, then a validation
report, a per-role workload summary and a PASS/FAIL verdict. Standard library only.

LAYOUT
  One row per activity (WBS work package, deliverable or decision), one column per role.
  The activity column is the first column headed Activity, Task, Deliverable, Work package,
  WBS element, Work item, Decision, Item or Step (case-insensitive, plurals too), else the
  first column; --activity-col NAME overrides it. Every other column is a role, except the
  columns named with --ignore-col (notes, ids, dates).
  --transpose reads the other layout: one row per ROLE and one column per activity. The role
  names are then read from the first column headed Role, Person, People, Name, Who, Team,
  Owner or Stakeholder, else the first column (or --activity-col NAME).

CELLS  (case-insensitive)
  RACI   R Responsible - does the work          A Accountable - owns the outcome, signs it off
         C Consulted - two-way, before the work  I Informed - one-way, after the fact
  RASCI  RACI plus S Support - helps the Responsible       --variant rasci  (alias rasic)
  DACI   D Driver  A Approver  C Contributor  I Informed   --variant daci
  (--variant raci also answers to arci.)
  A cell holds one letter, letters run together ("AR"), letters or words joined by / , + &
  or spaces ("A/R", "Accountable, Responsible"), or nothing. Blank: "", "-", "n/a", "na",
  "none". Words accepted: Responsible, Accountable, Approver, Consulted, Contributor,
  Informed, Support, Supportive, Supporting, Driver.
  Anything else - N/A inside a combo, TBC, X, a tick, Yes, Review, a name, a number, a JSON
  true/false - is REJECTED with its line, activity and role: it is never mined for letters,
  so "N/A" can never be read as Accountable. A letter from another variant (S in plain RACI,
  D outside DACI, R in DACI) is rejected with a hint to change --variant. A header or cell
  that is a template placeholder such as <Role 1> is rejected too.

INPUT
  CSV: delimiter auto-detected (, ; tab |) or forced with --delimiter; a UTF-8 BOM and CRLF
  line ends are tolerated; blank lines are skipped; empty header cells at the END of the
  header (Excel's trailing commas) are dropped when their cells are blank. Rejected (exit 2):
  any other empty header cell, duplicate column names (case- and spacing-insensitive), a row
  with fewer or more cells than the header (ragged row), a header with one column only.
  JSON (pass --json, also on stdin): a list of objects, or {"activities": [...]}; one object
  per activity (per role with --transpose). The column list is the ordered union of the keys
  of ALL objects, so a key missing from one object is a blank cell, not a lost role.

CHECKS  (owner letter = A; doer letter = R, or D in DACI)
  ERROR  unnamed activity         a row with no activity name
  ERROR  duplicate activity       the same activity name twice (case-insensitive); both lines named
  ERROR  multiple accountable     more than one A on a row            (DACI: multiple approver)
  ERROR  no responsible           no R on a row                       (DACI: no driver - D >= 1
                                                                       replaces the R rule)
  ERROR  no accountable           no A on a row                       (DACI: no approver)
  WARN   contradictory cell       I combined with another letter (R/I, A/I, C/I, ...): Informed
                                  is told after the fact, so it conflicts with doing, owning or advising
  WARN   too many cooks           more than --max-ci roles are C or I on one row
  WARN   ghost role               a role column with no letter on any row
  WARN   overloaded               a role is A on more than --max-a-share of the rows
  WARN   single point of failure  a role is R (DACI: D) on every row
  WARN   layout                   the label column looks like roles (try --transpose), or the
                                  reverse with --transpose
  INFO   share checks skipped     overloaded and single point of failure need at least 3 rows
  --strict turns warnings into a FAIL (exit 1) for CI gates. INFO never fails.

FORMULAS
  A-share(role) = rows where the role holds A / rows        overloaded when A-share > --max-a-share
  R-share(role) = rows where the role holds R (D) / rows    single point of failure when R-share = 100%
  touches(role) = rows where the role holds any letter      ghost role when touches = 0
  too many cooks: count of roles holding C or I on the row > --max-ci

FIXES  (--fix prints a suggestion under each finding; --fix-out PATH also writes the ERROR fixes)
  multiple accountable  keep the A held by the least-loaded role (fewest A across the matrix; ties:
                        leftmost column); the others lose their A and become C if nothing is left
  no responsible        promote a C to R (RASCI: an S first), choosing the one with the fewest R;
                        if the row has neither, the A also becomes R (A/R)
  no accountable        the single R becomes A/R; with several R, the one with the fewest A
  Fixes run row by row on a working copy, so later choices count earlier fixes. --fix-out writes
  the input back in its own format, delimiter and layout with only the ERROR fixes applied and
  every other cell untouched; warnings need judgment and are only suggested. Unnamed and
  duplicate activities have no automatic fix. The exit code still reflects the INPUT.

OUTPUT  --format table (default) | json | csv | md
  table  the matrix, the validation report, the role summary and the verdict
  json   {"rows": [...], "findings": [...], "role_summary": [...], "summary": {...}}
  csv    the matrix with canonical cells plus result and issues columns on stdout; role-level
         findings and the verdict on stderr
  md     Markdown matrix, findings, role summary and verdict for assets/raci-template.md

EXIT CODES  0 PASS  -  1 FAIL (any ERROR, or any WARN with --strict)  -  2 bad input, bad
            option or internal error ("error: ..." on stderr, never a traceback)

EXAMPLES
  python .claude/skills/raci-matrix/scripts/raci_validate.py .claude/skills/raci-matrix/assets/raci-sample.csv
  python .claude/skills/raci-matrix/scripts/raci_validate.py .claude/skills/raci-matrix/assets/daci-decisions-sample.csv --variant daci
  python .claude/skills/raci-matrix/scripts/raci_validate.py my-raci.csv --fix --fix-out my-raci-fixed.csv
  python .claude/skills/raci-matrix/scripts/raci_validate.py my-raci.csv --ignore-col Notes --strict
  python .claude/skills/raci-matrix/scripts/raci_validate.py my-raci.json --json --format json
  cat my-raci.csv | python .claude/skills/raci-matrix/scripts/raci_validate.py - --format md
  python .claude/skills/raci-matrix/scripts/raci_validate.py roles-as-rows.csv --transpose
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
import unicodedata

BOM = "\ufeff"
JSON_KEY = "activities"
FORMATS = ("table", "json", "csv", "md")
DEFAULT_MAX_CI = 4
DEFAULT_MAX_A_SHARE = 0.5
MIN_ROWS_FOR_SHARE = 3
ACTIVITY_CLIP, ROLE_CLIP = 48, 20

VARIANTS = {
    "raci": {"name": "RACI", "letters": "ARCI", "owner": "A", "doer": "R", "rows": "activities",
             "no_doer": "nobody does the work", "no_owner": "nobody owns the outcome",
             "labels": {"A": "Accountable", "R": "Responsible", "C": "Consulted", "I": "Informed"}},
    "rasci": {"name": "RASCI", "letters": "ARSCI", "owner": "A", "doer": "R", "rows": "activities",
              "no_doer": "nobody does the work", "no_owner": "nobody owns the outcome",
              "labels": {"A": "Accountable", "R": "Responsible", "S": "Support", "C": "Consulted",
                         "I": "Informed"}},
    "daci": {"name": "DACI", "letters": "ADCI", "owner": "A", "doer": "D", "rows": "decisions",
             "no_doer": "nobody drives the decision", "no_owner": "nobody makes the decision",
             "labels": {"A": "Approver", "D": "Driver", "C": "Contributor", "I": "Informed"}},
}
VARIANT_ALIASES = {"raci": "raci", "arci": "raci", "rasci": "rasci", "rasic": "rasci", "daci": "daci"}
ALL_LETTERS = set("RASCID")
LETTER_NAMES = {"R": "Responsible", "A": "Accountable", "S": "Support", "C": "Consulted",
                "I": "Informed", "D": "Driver"}
LETTER_HOME = {"S": "rasci", "D": "daci", "R": "raci"}
WORDS = {
    "RESPONSIBLE": "R", "ACCOUNTABLE": "A", "APPROVER": "A", "CONSULTED": "C", "CONTRIBUTOR": "C",
    "INFORMED": "I", "SUPPORT": "S", "SUPPORTIVE": "S", "SUPPORTING": "S", "DRIVER": "D",
}
BLANKS = {"", "-", "\u2013", "\u2014", "n/a", "na", "none"}
MARKS = {"X", "Y", "YES", "TRUE", "1", "\u2713", "\u2714", "\u2715", "\u2717"}
SPLIT_RE = re.compile(r"[\s/,+&]+")
PLACEHOLDER_RE = re.compile(r"^<[^<>]*>$")
ACTIVITY_LABELS = {"activity", "activities", "task", "tasks", "deliverable", "deliverables",
                   "work package", "work packages", "wbs element", "work item", "decision",
                   "decisions", "item", "step"}
ROLE_LABELS = {"role", "roles", "person", "people", "name", "who", "team", "owner", "stakeholder",
               "raci role"}
LAYOUT_ROLE_LABELS = {"role", "roles", "person", "people", "who", "team", "stakeholder", "raci role"}
LEVEL_ORDER = {"ERROR": 0, "WARN": 1, "INFO": 2}


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


def clean(value):
    """Text with a stray BOM removed and every run of whitespace (newlines too) collapsed."""
    return " ".join(str(value).replace(BOM, "").split())


def _short(value, limit=60):
    text = repr(value)
    return text if len(text) <= limit else text[:limit - 1] + "\u2026"


def load_rows(text, as_json, json_key, delimiter=None):
    """Return a grid {kind, delimiter, headers, records=[(location, {column: raw})], wrapped}.

    CSV auto-detects , ; tab |. JSON: a list of objects or {json_key: [...]}; the headers are the
    ordered union of the keys of every object.
    """
    if not text.strip():
        raise ValueError("input is empty")
    if not as_json and text.lstrip()[:1] in ("[", "{"):
        raise ValueError("input looks like JSON; pass --json")
    if as_json:
        return _load_json(text, json_key)
    return _load_csv(text, delimiter or sniff_delimiter(text))


def _load_json(text, json_key):
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        hint = "" if text.lstrip()[:1] in ("[", "{") else " - the input does not start with [ or {; for CSV drop --json"
        raise ValueError(f"invalid JSON: {exc}{hint}")
    wrapped = isinstance(data, dict)
    if wrapped:
        if json_key not in data:
            raise ValueError(f"JSON object must contain a '{json_key}' list; found keys: {sorted(map(str, data))}")
        data = data[json_key]
    if not isinstance(data, list):
        raise ValueError(f"JSON must be a list of objects or {{'{json_key}': [...]}}")
    headers, folded, records = [], {}, []
    for n, item in enumerate(data, 1):
        if not isinstance(item, dict):
            raise ValueError(f"JSON item {n} is not an object: {_short(item)}")
        values = {}
        for key, value in item.items():
            name = clean(key)
            if not name:
                raise ValueError(f"JSON item {n} has an empty key; every role needs a name")
            fold = name.casefold()
            if fold in folded and folded[fold] != name or name in values:
                raise ValueError(f"JSON item {n}: key {name!r} clashes with {folded.get(fold, name)!r} "
                                 "(same name apart from case or spacing); use one spelling per column")
            folded[fold] = name
            values[name] = value
            if name not in headers:
                headers.append(name)
        records.append((f"item {n}", values))
    if not records:
        raise ValueError("JSON contains no items")
    return {"kind": "json", "delimiter": None, "headers": headers, "records": records, "wrapped": wrapped}


def _load_csv(text, delimiter):
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    header, last = None, 0
    for raw in reader:
        last = reader.line_num
        if any(cell.strip() for cell in raw):
            header = [clean(cell) for cell in raw]
            break
    if header is None:
        raise ValueError("input is empty (no header row)")
    width = len(header)
    while width > 1 and not header[width - 1]:
        width -= 1  # Excel's trailing commas
    header = header[:width]
    if width < 2:
        raise ValueError(f"only one column found in the header ({_short(header[0])}); a matrix needs an "
                         f"activity column and at least one role column - if the file uses another "
                         f"delimiter than {delimiter!r}, pass --delimiter")
    blank = [i + 1 for i, h in enumerate(header) if not h]
    if blank:
        raise ValueError(f"header column(s) {blank} have no name; give every role column a name")
    folded = {}
    for i, h in enumerate(header, 1):
        fold = h.casefold()
        if fold in folded:
            raise ValueError(f"duplicate column name {h!r} (columns {folded[fold]} and {i}); give each role "
                             "a unique name, e.g. 'Developer 1' and 'Developer 2'")
        folded[fold] = i
    records, ragged = [], []
    for raw in reader:
        line, last = last + 1, reader.line_num  # first physical line of a record that spans several
        if not any(cell.strip() for cell in raw):
            continue  # blank line
        if len(raw) > width and any(cell.strip() for cell in raw[width:]):
            extra = [cell.strip() for cell in raw[width:] if cell.strip()]
            ragged.append(f"line {line} has values beyond the last named column {_short(extra[:3])}")
            continue
        if len(raw) < width:
            ragged.append(f"line {line} has {len(raw)} of {width} cells")
            continue
        records.append((f"line {line}", {header[i]: raw[i].strip() for i in range(width)}))
    if ragged:
        more = f"; ... and {len(ragged) - 5} more" if len(ragged) > 5 else ""
        raise ValueError("ragged row(s): " + "; ".join(ragged[:5]) + more + f" - every row needs exactly one "
                         f"cell per column ({width}); leave unassigned cells empty, e.g. 'Task,A,R,,'")
    if not records:
        raise ValueError(f"no activity rows found (header: {header})")
    return {"kind": "csv", "delimiter": delimiter, "headers": header, "records": records, "wrapped": False}


# ----------------------------------------------------------------------------- cells and matrix
def fmt(letters, spec):
    """Canonical cell text in the variant's order: A first, then the doer, then S, C, I."""
    return "/".join(x for x in spec["letters"] if x in letters)


class CellError(ValueError):
    """An invalid cell; kind is 'text' (free text), 'mark' (X, tick), 'foreign' (other variant) or 'type' (JSON)."""

    def __init__(self, message, kind):
        super().__init__(message)
        self.kind = kind


def parse_cell(value, spec):
    """Return the set of letters in a cell; raise CellError(reason) for anything else."""
    if value is None:
        return set()
    if isinstance(value, bool):
        raise CellError(f"{json.dumps(value)} is a JSON true/false, not a {spec['name']} value", "type")
    if isinstance(value, (int, float)):
        raise CellError(f"{value!r} is a number, not a {spec['name']} value", "type")
    if not isinstance(value, str):
        raise CellError(f"{_short(value)} is not text", "type")
    text = clean(value)
    if text.casefold() in BLANKS:
        return set()
    allowed = set(spec["letters"])
    letters = set()
    for token in SPLIT_RE.split(text.upper()):
        if not token:
            continue
        if token in WORDS:
            found = {WORDS[token]}
        elif set(token) <= ALL_LETTERS:
            found = set(token)
        else:
            if text.upper() in MARKS:
                raise CellError(f"{text!r} is not a {spec['name']} value - an X, tick or yes says someone is "
                                f"involved but not how; use {', '.join(spec['letters'])}", "mark")
            raise CellError(f"{text!r} is not a {spec['name']} value", "text")
        foreign = sorted(found - allowed, key="RASCID".index)
        if foreign:
            names = ", ".join(f"{x} ({LETTER_NAMES[x]})" for x in foreign)
            homes = sorted({LETTER_HOME.get(x, "raci") for x in foreign})
            raise CellError(f"{text!r}: {names} is not a {spec['name']} letter ({spec['name']} uses "
                            f"{', '.join(spec['letters'])}) - pass --variant {' or '.join(homes)}", "foreign")
        letters |= found
    return letters


def _name(value, where):
    if value is None:
        return ""
    if isinstance(value, bool) or isinstance(value, (list, dict)):
        raise ValueError(f"{where}: a name must be text, got {_short(value)}")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{where}: a name must be text, got {value!r}")
    return clean(value)


def build_matrix(grid, spec, activity_col=None, ignore_cols=(), transpose=False):
    """Turn the grid into {label, roles, activities, transposed}; reject placeholders and invalid cells."""
    headers, records = grid["headers"], grid["records"]

    def find(name, flag):
        fold = clean(name).casefold()
        for h in headers:
            if h.casefold() == fold:
                return h
        raise ValueError(f"{flag} {name!r} matches no column; columns: {headers}")

    if activity_col:
        label = find(activity_col, "--activity-col")
    else:
        wanted = ROLE_LABELS if transpose else ACTIVITY_LABELS
        label = next((h for h in headers if h.casefold() in wanted), headers[0])
    ignored = []
    for name in ignore_cols:
        col = find(name, "--ignore-col")
        if col == label:
            raise ValueError(f"--ignore-col {name!r} is the {'role' if transpose else 'activity'} column itself")
        if col not in ignored:
            ignored.append(col)
    others = [h for h in headers if h != label and h not in ignored]
    if not others:
        raise ValueError(f"no {'activity' if transpose else 'role'} columns left besides {label!r}"
                         + (f" and the ignored {ignored}" if ignored else ""))

    placeholders = [f"header {h!r}" for h in headers if PLACEHOLDER_RE.match(h)]
    for loc, values in records:
        placeholders += [f"{loc}, column {col!r}" for col, v in values.items()
                         if isinstance(v, str) and PLACEHOLDER_RE.match(v.strip())]
    if placeholders:
        raise ValueError(f"{len(placeholders)} unfilled template placeholder(s), first at {placeholders[0]} - "
                         "replace every <...> with your own activities, roles and letters "
                         "(assets/raci-sample.csv shows a filled matrix)")

    bad, good, bad_per = [], {}, {}

    def cell(raw, role, where):
        try:
            letters = parse_cell(raw, spec)
        except CellError as exc:
            bad.append(f"{where}: {exc}")
            if exc.kind == "text":
                bad_per[role] = bad_per.get(role, 0) + 1
            return set()
        if letters:
            good[role] = good.get(role, 0) + 1
        return letters

    activities = []
    if not transpose:
        roles = others
        for idx, (loc, values) in enumerate(records):
            name = _name(values.get(label), f"{loc}, column {label!r}")
            cells = {r: cell(values.get(r), r, f"{loc}, activity {name or '(unnamed)'!r}, role {r!r}")
                     for r in roles}
            activities.append({"name": name, "loc": loc, "cells": cells, "record": idx, "column": None})
    else:
        roles, seen = [], {}
        for loc, values in records:
            role = _name(values.get(label), f"{loc}, column {label!r}")
            if not role:
                raise ValueError(f"{loc}: no role name in column {label!r}")
            fold = role.casefold()
            if fold in seen:
                raise ValueError(f"duplicate role {role!r} ({seen[fold]} and {loc}); give each role a unique name")
            seen[fold] = loc
            roles.append(role)
        for col in others:
            loc = f"column {headers.index(col) + 1}"
            cells = {}
            for (rloc, values), role in zip(records, roles):
                cells[role] = cell(values.get(col), role, f"{rloc} (role {role!r}), activity {col!r}")
            activities.append({"name": col, "loc": loc, "cells": cells, "record": None, "column": col})

    if bad:
        lines = [f"{len(bad)} cell(s) are not {spec['name']} values:"] + [f"  {m}" for m in bad[:15]]
        if len(bad) > 15:
            lines.append(f"  ... and {len(bad) - 15} more")
        words = ", ".join(f"{x} {spec['labels'][x]}" for x in spec["letters"])
        lines.append(f"Allowed: {words}; combos such as A/{spec['doer']}; or blank ('-', 'n/a', 'none').")
        for role in roles:
            if bad_per.get(role) and not good.get(role):
                lines.append(f"hint: {'row' if transpose else 'column'} {role!r} holds no {spec['name']} value at "
                             "all - " + (f"if it is not a role, delete that row" if transpose else
                                         f"if it is not a role, pass --ignore-col {role!r}"))
        raise ValueError("\n".join(lines))
    return {"label": label, "roles": roles, "activities": activities, "transposed": transpose,
            "ignored": ignored, "explicit_label": bool(activity_col)}


# ----------------------------------------------------------------------------- validation
def _pct(x):
    return f"{100 * x:.1f}%"


def _n(count, plural):
    """'1 activity', '8 activities', '1 decision', '6 roles'."""
    if count == 1:
        plural = plural[:-3] + "y" if plural.endswith("ies") else plural[:-1]
    return f"{count} {plural}"


def _fix_row(i, w, roles, spec, a_live, d_live, changed):
    """Apply the ERROR fixes for one row to the working copy w; return {kind: suggestion text}."""
    owner, doer, lab = spec["owner"], spec["doer"], spec["labels"]
    col = {r: k for k, r in enumerate(roles)}
    out = {}

    def change(role, new):
        old = fmt(w[role], spec) or "blank"
        w[role] = set(new)
        changed[(i, role)] = set(new)
        return f"{role} {old} -> {fmt(new, spec)}"

    owners = [r for r in roles if owner in w[r]]
    if len(owners) > 1:
        keep = min(owners, key=lambda r: (a_live[r], col[r]))
        moves = []
        for r in owners:
            if r != keep:
                a_live[r] -= 1
                moves.append(change(r, (w[r] - {owner}) or {"C"}))
        out["multi"] = (f"keep {keep} as {owner} (least loaded: {a_live[keep]} {owner} across the matrix); "
                        f"change {', '.join(moves)}")
    if not any(doer in w[r] for r in roles):
        pool, src = [], ""
        if "S" in spec["letters"]:
            pool, src = [r for r in roles if "S" in w[r]], "S"
        if not pool:
            pool, src = [r for r in roles if "C" in w[r]], "C"
        if pool:
            pick = min(pool, key=lambda r: (d_live[r], col[r]))
            before = d_live[pick]
            d_live[pick] += 1
            out["doer"] = (f"promote a {lab[src]} role: {change(pick, (w[pick] - {src}) | {doer})} "
                           f"(fewest {doer} elsewhere: {before})")
        else:
            own = [r for r in roles if owner in w[r]]
            if own:
                d_live[own[0]] += 1
                out["doer"] = f"the {lab[owner]} also does the work: {change(own[0], w[own[0]] | {doer})}"
            else:
                out["doer"] = (f"no automatic fix - nobody on this row is {lab['C']} or {lab[owner]}; "
                               f"name the role that does the work")
    if not any(owner in w[r] for r in roles):
        doers = [r for r in roles if doer in w[r]]
        if doers:
            pick = min(doers, key=lambda r: (a_live[r], col[r]))
            why = (f"the only {lab[doer]}" if len(doers) == 1 else
                   f"the {lab[doer]} with the fewest {owner}: {a_live[pick]}")
            a_live[pick] += 1
            out["owner"] = f"{change(pick, w[pick] | {owner})} ({why})"
        else:
            out["owner"] = f"no automatic fix - nobody on this row is {lab[doer]}; name one owner ({owner})"
    return out


def validate(matrix, spec, max_ci, max_a_share):
    roles, acts = matrix["roles"], matrix["activities"]
    owner, doer, lab, word = spec["owner"], spec["doer"], spec["labels"], spec["rows"]
    total = len(acts)
    counts = {r: {x: 0 for x in spec["letters"]} for r in roles}
    touches = {r: 0 for r in roles}
    for act in acts:
        for r in roles:
            for x in act["cells"][r]:
                counts[r][x] += 1
            touches[r] += bool(act["cells"][r])
    findings = []

    def add(level, scope, code, subject, loc, message, fix=None, row=None):
        findings.append({"level": level, "scope": scope, "code": code, "subject": subject,
                         "location": loc, "message": message, "fix": fix, "_row": row})

    work = [{r: set(act["cells"][r]) for r in roles} for act in acts]
    a_live = {r: counts[r][owner] for r in roles}
    d_live = {r: counts[r][doer] for r in roles}
    changed = {}
    passive = [r for r in roles if counts[r][owner] == 0 and counts[r][doer] == 0]
    seen = {}
    for i, act in enumerate(acts):
        name, loc, cells = act["name"], act["loc"], act["cells"]
        subj = name or "(unnamed)"
        if not name:
            add("ERROR", "row", "unnamed-activity", subj, loc, "row has no activity name",
                "no automatic fix - name it after the WBS work package, deliverable or decision it covers", i)
        else:
            key = name.casefold()
            if key in seen:
                add("ERROR", "row", "duplicate-activity", name, loc,
                    f"same activity as {seen[key]}; each activity must appear exactly once",
                    "no automatic fix - merge the two rows, or make the names distinct (e.g. prefix the WBS id)", i)
            else:
                seen[key] = loc
        fixes = _fix_row(i, work[i], roles, spec, a_live, d_live, changed)
        owners = [r for r in roles if owner in cells[r]]
        if len(owners) > 1:
            add("ERROR", "row", f"multiple-{lab[owner].lower()}", subj, loc,
                f"{len(owners)} roles are {lab[owner]}: {', '.join(owners)} - exactly one is allowed",
                fixes.get("multi"), i)
        if not any(doer in cells[r] for r in roles):
            add("ERROR", "row", f"no-{lab[doer].lower()}", subj, loc,
                f"no role is {lab[doer]} ({doer}) - {spec['no_doer']}", fixes.get("doer"), i)
        if not owners:
            add("ERROR", "row", f"no-{lab[owner].lower()}", subj, loc,
                f"no role is {lab[owner]} ({owner}) - {spec['no_owner']}", fixes.get("owner"), i)
        for r in roles:
            s = cells[r]
            if "I" in s and len(s) > 1:
                rest = s - {"I"}
                add("WARN", "row", "contradictory-cell", subj, loc,
                    f"{r} is {fmt(s, spec)}: {lab['I']} (told after the fact) conflicts with "
                    + "/".join(lab[x] for x in spec["letters"] if x in rest),
                    f"keep one: {r} -> {fmt(rest, spec)}, or I alone if they only need the result", i)
        ci = [r for r in roles if cells[r] & {"C", "I"}]
        if len(ci) > max_ci:
            need = len(ci) - max_ci
            pool = [r for r in ci if cells[r] == {"I"}] + [r for r in ci if cells[r] == {"C"} and r in passive]
            if len(pool) >= need:
                fix = (f"remove {', '.join(pool[:need])} from this row (Informed, or never {owner}/{doer} "
                       "anywhere) and reach them through the communication plan instead")
            else:
                fix = f"remove {need} of {', '.join(ci)} - keep only roles whose input changes the outcome"
            add("WARN", "row", "too-many-cooks", subj, loc,
                f"{len(ci)} roles are C or I (max {max_ci}): {', '.join(ci)}", fix, i)

    for r in roles:
        if touches[r] == 0:
            add("WARN", "role", "ghost-role", r, "", f"holds no letter on any {word[:-3] + 'y' if word.endswith('ies') else word[:-1]}",
                f"assign {r} where they genuinely contribute, or delete the column")
    if total >= MIN_ROWS_FOR_SHARE:
        for r in roles:
            a = counts[r][owner]
            if a / total > max_a_share + 1e-9:
                need = a - math.floor(max_a_share * total + 1e-9)
                hand, load = [], {x: counts[x][owner] for x in roles}
                for act in acts:
                    if len(hand) == need:
                        break
                    if owner in act["cells"][r]:
                        pool = [x for x in roles if x != r and doer in act["cells"][x]]
                        if pool:
                            pick = min(pool, key=lambda x: (load[x], roles.index(x)))
                            load[pick] += 1
                            hand.append(f"{act['name'] or act['loc']!r} -> {pick}")
                if hand:
                    fix = f"hand {owner} to the least-loaded {lab[doer]}: " + "; ".join(hand)
                    if len(hand) < need:
                        fix += f"; and name new owners for {need - len(hand)} more"
                else:
                    fix = f"name other owners for {need} of the {a} {word} where {r} is {owner}"
                add("WARN", "role", "overloaded", r, "",
                    f"{lab[owner]} on {a}/{total} {word} ({_pct(a / total)} > {_pct(max_a_share)})", fix)
        for r in roles:
            if counts[r][doer] == total:
                add("WARN", "role", "single-point-of-failure", r, "",
                    f"{lab[doer]} on all {total} {word} - everything waits on this one role",
                    f"add a second {lab[doer]} or hand {doer} to another role on some {word}")
    else:
        add("INFO", "matrix", "share-checks-skipped", "matrix", "",
            f"overloaded and single-point-of-failure checks need at least {MIN_ROWS_FOR_SHARE} {word} "
            f"(found {_n(total, word)})")
    label = matrix["label"].casefold()
    if not matrix["explicit_label"] and not matrix["transposed"] and label in LAYOUT_ROLE_LABELS:
        add("WARN", "matrix", "layout", "matrix", "",
            f"the activity column {matrix['label']!r} looks like a list of roles",
            "if roles are rows and activities are columns, re-run with --transpose")
    if not matrix["explicit_label"] and matrix["transposed"] and label in ACTIVITY_LABELS:
        add("WARN", "matrix", "layout", "matrix", "",
            f"--transpose reads column {matrix['label']!r} as role names, but it looks like activities",
            "drop --transpose")
    findings.sort(key=lambda f: LEVEL_ORDER[f["level"]])
    summary = []
    for r in roles:
        summary.append({"role": r, "counts": dict(counts[r]), "touches": touches[r],
                        "share": {owner: round(counts[r][owner] / total, 3), doer: round(counts[r][doer] / total, 3)}})
    return {"findings": findings, "role_summary": summary, "changed": changed, "work": work, "total": total}


def verdict(res, strict):
    errors = sum(1 for f in res["findings"] if f["level"] == "ERROR")
    warns = sum(1 for f in res["findings"] if f["level"] == "WARN")
    failed = errors > 0 or (strict and warns > 0)
    tail = "; --strict: warnings fail" if strict and warns and not errors else ""
    return failed, errors, warns, f"Result: {'FAIL' if failed else 'PASS'}  ({errors} error(s), {warns} warning(s){tail})"


# ----------------------------------------------------------------------------- output
def _width(text):
    return sum(0 if unicodedata.combining(ch) else 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
               for ch in text)


def _clip(text, limit):
    text = clean(text)
    if _width(text) <= limit:
        return text
    out, used = "", 0
    for ch in text:
        w = _width(ch)
        if used + w > limit - 1:
            break
        out, used = out + ch, used + w
    return out + "\u2026"


def _pad(text, width, right=False):
    gap = " " * max(0, width - _width(text))
    return gap + text if right else text + gap


def _text_table(headers, rows, right=()):
    widths = [max([_width(h)] + [_width(r[i]) for r in rows]) for i, h in enumerate(headers)]

    def line(cells):
        return "  ".join(_pad(c, widths[i], i in right) for i, c in enumerate(cells)).rstrip()

    return [line(headers), "  ".join("-" * w for w in widths)] + [line(r) for r in rows]


def _row_status(res, i):
    levels = [f["level"] for f in res["findings"] if f["_row"] == i and f["level"] != "INFO"]
    return "ERROR" if "ERROR" in levels else "WARN" if "WARN" in levels else "OK"


def _where(f):
    if f["scope"] == "row":
        return f"{f['location']}  {f['subject']}"
    if f["scope"] == "role":
        return f"role {f['subject']!r}"
    return "matrix"


def _out_label(matrix):
    return "Activity" if matrix["transposed"] else matrix["label"]


def _title(matrix, spec, res):
    src = (f"roles read from column {matrix['label']!r} (--transpose)" if matrix["transposed"]
           else f"activity column {matrix['label']!r}")
    return f"{spec['name']} matrix: {_n(res['total'], spec['rows'])} x {_n(len(matrix['roles']), 'roles')} ({src})"


def _summary_rows(res, spec):
    owner, doer = spec["owner"], spec["doer"]
    hdr = ["Role"] + list(spec["letters"]) + ["Touches", f"{owner}-share", f"{doer}-share"]
    rows = [[s["role"]] + [str(s["counts"][x]) for x in spec["letters"]]
            + [str(s["touches"]), _pct(s["share"][owner]), _pct(s["share"][doer])] for s in res["role_summary"]]
    return hdr, rows


def render_table(matrix, res, spec, opts):
    roles = matrix["roles"]
    out = [_title(matrix, spec, res), ""]
    headers = [_clip(_out_label(matrix), ACTIVITY_CLIP)] + [_clip(r, ROLE_CLIP) for r in roles]
    rows = [[_clip(a["name"] or "(unnamed)", ACTIVITY_CLIP)] + [fmt(a["cells"][r], spec) for r in roles]
            for a in matrix["activities"]]
    out += _text_table(headers, rows)
    out += ["", "Validation report:"]
    if not res["findings"]:
        out.append("  (no issues)")
    for f in res["findings"]:
        out.append(f"  {f['level']:<5}  {_where(f)}: {f['code'].replace('-', ' ')} - {f['message']}")
        if opts.fix and f["fix"]:
            out.append(f"         fix: {f['fix']}")
    hdr, srows = _summary_rows(res, spec)
    out += ["", f"Role summary ({_n(res['total'], spec['rows'])}):"]
    out += _text_table(hdr, [[_clip(r[0], ROLE_CLIP + 4)] + r[1:] for r in srows], right=set(range(1, len(hdr))))
    out += ["", verdict(res, opts.strict)[3]]
    return "\n".join(out)


def _public(f, with_fix):
    d = {k: v for k, v in f.items() if not k.startswith("_")}
    if not with_fix:
        d.pop("fix")
    return d


def render_json(matrix, res, spec, opts):
    failed, errors, warns, _ = verdict(res, opts.strict)
    rows = []
    for i, a in enumerate(matrix["activities"]):
        rows.append({"activity": a["name"], "location": a["loc"],
                     "cells": {r: fmt(a["cells"][r], spec) for r in matrix["roles"]},
                     "result": _row_status(res, i)})
    doc = {
        "variant": opts.variant_key,
        "layout": "roles-as-rows" if matrix["transposed"] else "activities-as-rows",
        "label_column": matrix["label"],
        "ignored_columns": matrix["ignored"],
        "roles": matrix["roles"],
        "rows": rows,
        "findings": [_public(f, opts.fix) for f in res["findings"]],
        "role_summary": res["role_summary"],
        "summary": {"result": "FAIL" if failed else "PASS", "errors": errors, "warnings": warns,
                    "infos": sum(1 for f in res["findings"] if f["level"] == "INFO"),
                    "activities": res["total"], "roles": len(matrix["roles"]), "strict": opts.strict,
                    "max_ci": opts.max_ci_value, "max_a_share": opts.max_a_share_value},
    }
    return json.dumps(doc, indent=2, ensure_ascii=False)


def render_csv(matrix, res, spec, opts):
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow([_out_label(matrix)] + matrix["roles"] + ["result", "issues"])
    for i, a in enumerate(matrix["activities"]):
        issues = " | ".join(f"{f['code']}: {f['message']}" + (f" (fix: {f['fix']})" if opts.fix and f["fix"] else "")
                            for f in res["findings"] if f["_row"] == i)
        writer.writerow([a["name"]] + [fmt(a["cells"][r], spec) for r in matrix["roles"]]
                        + [_row_status(res, i), issues])
    side = [f"{f['level']}  {_where(f)}: {f['code'].replace('-', ' ')} - {f['message']}"
            + (f" (fix: {f['fix']})" if opts.fix and f["fix"] else "")
            for f in res["findings"] if f["_row"] is None]
    return buf.getvalue().rstrip("\n"), side


def _md(text):
    return clean(text).replace("|", "\\|")


def render_md(matrix, res, spec, opts):
    roles = matrix["roles"]
    out = [f"**{_md(_title(matrix, spec, res))}**", ""]
    out.append("| " + " | ".join(_md(h) for h in [_out_label(matrix)] + roles) + " |")
    out.append("| --- | " + " | ".join(":---:" for _ in roles) + " |")
    for a in matrix["activities"]:
        out.append("| " + " | ".join([_md(a["name"] or "(unnamed)")] + [fmt(a["cells"][r], spec) or " " for r in roles])
                   + " |")
    out += ["", "**Validation**", ""]
    if not res["findings"]:
        out.append("- no issues")
    for f in res["findings"]:
        line = f"- **{f['level']}** {_md(_where(f))}: {f['code'].replace('-', ' ')} - {_md(f['message'])}"
        if opts.fix and f["fix"]:
            line += f" *Fix:* {_md(f['fix'])}"
        out.append(line)
    hdr, srows = _summary_rows(res, spec)
    out += ["", f"**Role summary** ({_n(res['total'], spec['rows'])})", ""]
    out.append("| " + " | ".join(hdr) + " |")
    out.append("| --- | " + " | ".join("---:" for _ in hdr[1:]) + " |")
    out += ["| " + " | ".join([_md(r[0])] + r[1:]) + " |" for r in srows]
    out += ["", f"**{verdict(res, opts.strict)[3]}**"]
    return "\n".join(out)


def write_fixed(path, grid, matrix, res, spec):
    """Write the input with the ERROR fixes applied; return the number of cells changed."""
    records = [dict(values) for _, values in grid["records"]]
    acts, roles = matrix["activities"], matrix["roles"]
    for (i, role), letters in sorted(res["changed"].items(), key=lambda kv: (kv[0][0], roles.index(kv[0][1]))):
        text = fmt(letters, spec)
        if matrix["transposed"]:
            records[roles.index(role)][acts[i]["column"]] = text
        else:
            records[acts[i]["record"]][role] = text
    if grid["kind"] == "json":
        payload = {JSON_KEY: records} if grid["wrapped"] else records
        body = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    else:
        buf = io.StringIO()
        writer = csv.writer(buf, delimiter=grid["delimiter"], lineterminator="\n")
        writer.writerow(grid["headers"])
        for values in records:
            writer.writerow(["" if values.get(h) is None else values.get(h) for h in grid["headers"]])
        body = buf.getvalue()
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(body)
    return len(res["changed"])


# ----------------------------------------------------------------------------- CLI
class _Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"error: {message}\n")
        self.print_usage(sys.stderr)
        raise SystemExit(2)


def build_parser():
    parser = _Parser(
        description="Validate a RACI / RASCI / DACI matrix: exactly one A and at least one R (DACI: D) per "
                    "row, lean C/I, no contradictory cells, ghost or overloaded roles, or single points of "
                    "failure; suggest fixes and summarise each role's workload.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("path", help="CSV or JSON matrix file, or '-' for stdin")
    parser.add_argument("--json", action="store_true",
                        help='parse the input as JSON (a list of objects or {"activities": [...]})')
    parser.add_argument("--delimiter", metavar="CHAR",
                        help="CSV delimiter (default: auto-detect , ; tab |); 'tab' or '\\t' for a tab")
    parser.add_argument("--variant", default="raci", metavar="{raci,rasci,daci}",
                        help="letters and rules: raci (alias arci), rasci (alias rasic; adds S Support), daci "
                             "(D Driver, A Approver, C Contributor, I Informed; D >= 1 replaces the R rule) "
                             "(default raci)")
    parser.add_argument("--activity-col", metavar="NAME",
                        help="column holding the activity names (default: the first column headed Activity, "
                             "Task, Deliverable, Work package, Decision ... else the first column); with "
                             "--transpose, the column holding the role names")
    parser.add_argument("--ignore-col", metavar="NAME[,NAME]", action="append", default=[],
                        help="columns that are neither the activity nor a role (notes, WBS id, dates); "
                             "comma-separated or repeated")
    parser.add_argument("--transpose", action="store_true",
                        help="the input has one row per ROLE and one column per activity")
    parser.add_argument("--max-ci", default=str(DEFAULT_MAX_CI), metavar="N",
                        help="WARN 'too many cooks' when more than N roles are C or I on one row "
                             "(whole number >= 0, default %(default)s)")
    parser.add_argument("--max-a-share", default=str(DEFAULT_MAX_A_SHARE), metavar="SHARE",
                        help="WARN 'overloaded' when a role is A on more than SHARE of the rows: a fraction "
                             "above 0 and at most 1 (0.5) or a percentage (50%%); default %(default)s; needs "
                             f"at least {MIN_ROWS_FOR_SHARE} rows")
    parser.add_argument("--fix", action="store_true",
                        help="print a suggested fix under each finding (ERROR fixes are deterministic: keep "
                             "the least-loaded A, promote a C to R, promote the single R to A/R)")
    parser.add_argument("--fix-out", metavar="PATH",
                        help="also write the input with the ERROR fixes applied to PATH (same format, "
                             "delimiter and layout; implies --fix; the exit code still reflects the input)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures (exit 1) for CI gates")
    parser.add_argument("--format", choices=FORMATS, default="table",
                        help="output format (default %(default)s); csv prints rows to stdout and the "
                             "role-level findings and verdict to stderr")
    return parser


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


def check_options(parser, args):
    key = VARIANT_ALIASES.get(str(args.variant).strip().lower())
    if key is None:
        parser.error(f"--variant must be raci, rasci or daci (aliases: arci, rasic); got {args.variant!r}")
    args.variant_key = key
    if args.delimiter is not None:
        if args.delimiter.lower() in ("tab", "\\t"):
            args.delimiter = "\t"
        if len(args.delimiter) != 1 or args.delimiter in ('"', "\r", "\n"):
            parser.error("--delimiter must be a single character other than a quote or newline (or 'tab')")
        if args.json:
            parser.error("--delimiter applies to CSV input only; drop it when passing --json")
    try:
        args.max_ci_value = int(_num(args.max_ci, "--max-ci", minimum=0, integer=True))
    except ValueError as exc:
        parser.error(f"{exc} (a whole number of C/I roles >= 0)")
    raw = str(args.max_a_share).strip()
    try:
        share = _num(raw, "--max-a-share")
    except ValueError as exc:
        parser.error(str(exc))
    if raw.endswith("%"):
        share /= 100
    if not 0 < share <= 1:
        parser.error(f"--max-a-share must be a fraction above 0 and at most 1 (e.g. 0.5) or a percentage such "
                     f"as 50%; got {args.max_a_share!r}")
    args.max_a_share_value = round(share, 6)
    args.ignore_list = [c.strip() for item in args.ignore_col for c in item.split(",") if c.strip()]
    if args.ignore_col and not args.ignore_list:
        parser.error("--ignore-col needs at least one column name")
    if args.activity_col is not None and not args.activity_col.strip():
        parser.error("--activity-col needs a column name")
    if args.fix_out:
        args.fix = True
        if args.path != "-":
            same = os.path.abspath(args.fix_out) == os.path.abspath(args.path)
            try:
                same = same or (os.path.exists(args.fix_out) and os.path.samefile(args.fix_out, args.path))
            except OSError:
                pass
            if same:
                parser.error(f"refusing to overwrite the input file {args.path!r}; choose another --fix-out path")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    check_options(parser, args)
    spec = VARIANTS[args.variant_key]
    side = []
    try:
        text = read_text(args.path)
        grid = load_rows(text, args.json, JSON_KEY, args.delimiter)
        matrix = build_matrix(grid, spec, args.activity_col, args.ignore_list, args.transpose)
        res = validate(matrix, spec, args.max_ci_value, args.max_a_share_value)
        note = None
        if args.fix_out:
            n = write_fixed(args.fix_out, grid, matrix, res, spec)
            manual = sum(1 for f in res["findings"] if f["level"] == "ERROR" and f["fix"]
                         and f["fix"].startswith("no automatic fix"))
            note = (f"wrote {args.fix_out}: {n} cell(s) changed by the ERROR fixes"
                    + (f", {manual} error(s) still need a manual fix" if manual else "")
                    + " - review it, then re-run the validator on it")
        if args.format == "json":
            output = render_json(matrix, res, spec, args)
        elif args.format == "csv":
            output, side = render_csv(matrix, res, spec, args)
        elif args.format == "md":
            output = render_md(matrix, res, spec, args)
        else:
            output = render_table(matrix, res, spec, args)
        failed, _, _, line = verdict(res, args.strict)
    except (OSError, ValueError, TypeError, UnicodeDecodeError, OverflowError, ZeroDivisionError,
            KeyError, IndexError, RecursionError, csv.Error) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(output)
    if args.format == "csv":
        for s in side + [line]:
            print(s, file=sys.stderr)
    if note:
        print(note, file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
