#!/usr/bin/env python3
"""Test every helper script in the catalog against its bundled sample and the
hardening contract (README "Helper scripts"). Standard library only.

For each script it checks:
  * --help exits 0
  * the bundled sample runs (exit 0) and the output contains the expected markers
  * the canon Helios numbers the sample must produce (from --format json): NPV 196,173.88,
    IRR 23.61% and payback 2.85; the 25-week critical path A -> B -> D -> G -> H -> J;
    CPI 0.93, SPI 0.92, EAC 535,032, AMBER; threat EMV 94,300, residual 52,300 and a seed-42
    residual P50 of 40,000; PERT P50 451.83 and P80 468.63; WBS 1.3.1 budget 78,750
  * the same data via stdin ("-"), as JSON (--json), with a UTF-8 BOM, with CRLF line
    endings, semicolon-delimited, and semicolon-delimited with decimal commas ("0,4")
    all produce the SAME output as the plain sample
  * every --format the script offers exits 0, and --format json is valid JSON
  * bad input is rejected with `error: ...` on stderr and exit 2, never a traceback:
    empty file, header-only file, a `nan` value, JSON `true` and `Infinity` in a numeric
    field, an ambiguous number ("1.000,50"), malformed JSON, a JSON file passed without
    --json, a JSON list containing a non-object
  * validators and gates return exit 1 on a deliberately broken input: wbs_validate,
    raci_validate, issue_log_check, risk_score --check and capacity_check --fail-on over
  * script-specific cases: a terminal milestone is dated on the project finish date,
    duplicate PERT ids and duplicate EVM work packages are rejected, and the issue log's
    --format csv output re-imports to the identical file

Usage:
    python tools/test_scripts.py            # run everything
    python tools/test_scripts.py -k raci    # only scripts whose path contains "raci"
    python tools/test_scripts.py -v         # show every command
Exit code is non-zero if any check fails (or if -k matches no script).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(ROOT, ".claude", "skills")
DEFAULT_FORMATS = ["json", "csv", "md"]


def _opt(d, i=0):
    return d["summary"]["options"][i]


def _wbs_budget(d, wid):
    return next((r.get("budget") for r in d["rows"] if r.get("id") == wid), None)


def _blank_owner_of_first(rows):
    rows = [dict(r) for r in rows]
    rows[0]["owner"] = ""
    return rows


# script (relative to .claude/skills) -> sample input and what to expect of it.
#   markers      strings the default output must contain
#   numeric_col  a numeric column: nan, true and Infinity there must be rejected
#   comma_col    a numeric column rewritten with decimal commas in a ';' file (same output)
#   pins         [(extra args, [(label, getter on --format json output, expected)])]
#   broken       CSV text a validator must fail with exit 1
#   extra_fail   [(name, row transform or None, args, exit code)] on the sample
#   formats      the --format values to exercise (default json, csv, md)
REGISTRY = [
    {
        "script": "risk-register/scripts/risk_score.py",
        "sample": "risk-register/assets/risk-register-template.csv",
        "markers": ["R001", "EMV"],
        "numeric_col": "probability",
        "comma_col": "probability",
        "pins": [
            ([], [("total threat EMV", lambda d: d["summary"]["total_threat_emv"], 94300),
                  ("total residual threat EMV", lambda d: d["summary"]["total_residual_threat_emv"], 52300)]),
            (["--basis", "residual", "--simulate", "10000", "--seed", "42"],
             [("residual P50 (seed 42)", lambda d: d["simulation"]["p50"], 40000)]),
        ],
        "extra_fail": [
            ("check-passes", None, ["--check"], 0),
            ("check-fails-without-owner", _blank_owner_of_first, ["--check"], 1),
        ],
    },
    {
        "script": "estimation/scripts/pert_estimate.py",
        "sample": "estimation/assets/estimation-worksheet-sample.csv",
        "markers": ["Total", "95%"],
        "numeric_col": "most_likely",
        "comma_col": "most_likely",
        "pins": [
            ([], [("P50", lambda d: round(d["summary"]["one_sided"]["P50"], 2), 451.83),
                  ("P80", lambda d: round(d["summary"]["one_sided"]["P80"], 2), 468.63)]),
        ],
    },
    {
        "script": "project-schedule/scripts/critical_path.py",
        "sample": "project-schedule/assets/schedule-sample.csv",
        "markers": ["Critical path: A -> B -> D -> G -> H -> J", "Project duration: 25"],
        "numeric_col": "duration",
        "comma_col": "pessimistic",
        "pins": [
            (["--unit", "weeks"], [("project duration", lambda d: d["summary"]["project_duration"], 25),
                                   ("critical paths", lambda d: d["summary"]["critical_paths"],
                                    [["A", "B", "D", "G", "H", "J"]])]),
            (["--unit", "weeks", "--start-date", "2026-04-06", "--workdays"],
             [("finish date", lambda d: d["summary"]["calendar"]["finish_date"], "2026-09-25")]),
        ],
    },
    {
        "script": "cost-management/scripts/health_check.py",
        "sample": "cost-management/assets/evm-snapshot.csv",
        "markers": ["CPI", "AMBER"],
        "numeric_col": "ev",
        "comma_col": "ev",
        "pins": [
            ([], [("CPI", lambda d: round(d["summary"]["total"]["cpi"], 2), 0.93),
                  ("SPI", lambda d: round(d["summary"]["total"]["spi"], 2), 0.92),
                  ("EAC", lambda d: round(d["summary"]["total"]["eac"]), 535032),
                  ("BAC", lambda d: d["summary"]["total"]["bac"], 500000),
                  ("RAG", lambda d: d["summary"]["rag"], "AMBER")]),
        ],
    },
    {
        "script": "business-case/scripts/roi_npv.py",
        "sample": "business-case/assets/cashflows.csv",
        "markers": ["NPV"],
        "numeric_col": "cashflow",
        "comma_col": "cashflow",
        "pins": [
            (["--irr"], [("NPV", lambda d: _opt(d)["npv"], 196173.88),
                         ("IRR", lambda d: round(_opt(d)["irr"], 4), 0.2361),
                         ("payback", lambda d: _opt(d)["payback"]["value"], 2.85)]),
        ],
    },
    {
        "script": "work-breakdown-structure/scripts/wbs_validate.py",
        "sample": "work-breakdown-structure/assets/wbs-sample.csv",
        "markers": ["PASS"],
        "numeric_col": "weight",
        "comma_col": "weight",
        "pins": [
            (["--rollup", "--budget", "500000"], [("1.3.1 budget", lambda d: _wbs_budget(d, "1.3.1"), 78750)]),
        ],
        "broken": "id,name,weight\n1,Root,\n1.1,A,60\n1.1,Dup,30\n1.3.1,Orphan,10\n",
    },
    {
        "script": "raci-matrix/scripts/raci_validate.py",
        "sample": "raci-matrix/assets/raci-sample.csv",
        "markers": ["PASS"],
        "numeric_col": None,
        "broken": "Activity,Sponsor,PM,Dev\nWrite charter,A,A,R\nBuild portal,,,C\n",
    },
    {
        "script": "change-request/scripts/change_impact.py",
        "sample": "change-request/assets/change-log.csv",
        "markers": ["CR001"],
        "numeric_col": "cost_impact",
        "comma_col": "cost_value",
    },
    {
        "script": "resource-management/scripts/capacity_check.py",
        "sample": "resource-management/assets/resource-allocation-sample.csv",
        "markers": ["OVER"],
        "numeric_col": "allocated",
        "comma_col": "allocated",
        "extra_fail": [("fail-on-over", None, ["--fail-on", "over"], 1)],
    },
    {
        "script": "agile-delivery/scripts/velocity_forecast.py",
        "sample": "agile-delivery/assets/sprint-history-sample.csv",
        "markers": ["velocity"],
        "numeric_col": "completed_points",
        "comma_col": "completed_points",
    },
    {
        "script": "project-delivery/scripts/issue_log_check.py",
        "sample": "project-delivery/assets/issue-log-sample.csv",
        "markers": ["I001"],
        "numeric_col": None,
        "formats": ["json", "csv"],
        "broken": "id,type,description,owner,priority,status,due\nI1,issue,x,,High,Open,\nI1,risk,y,A and B,Urgent,Closed,2026-01-01\n",
    },
]

# Values that become a decimal-comma number without changing the parsed value.
COMMA_SAFE_RE = re.compile(r"^-?\d+(\.\d{1,2})?$")


class Result:
    def __init__(self):
        self.passed, self.failed = 0, []

    def ok(self, label, cond, info=""):
        if cond:
            self.passed += 1
        else:
            self.failed.append(f"{label}: {info}")


def run(args, stdin_text=None):
    proc = subprocess.run([sys.executable, *args], input=stdin_text, capture_output=True, text=True, timeout=120)
    return proc.returncode, proc.stdout, proc.stderr


def rows_of(text):
    reader = csv.DictReader(io.StringIO(text))
    return list(reader), reader.fieldnames or []


def write(tmp, name, text, encoding="utf-8"):
    path = os.path.join(tmp, name)
    with open(path, "w", encoding=encoding, newline="") as fh:
        fh.write(text)
    return path


def csv_text(headers, rows, delimiter=","):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=headers, delimiter=delimiter)
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def find_col(headers, name):
    return next((h for h in headers if name and h.lower() == name.lower()), None)


def decimal_comma(value):
    """'0.4' -> '0,4', '44' -> '44,0'; other cells (blank, 3+ decimals, text) unchanged."""
    s = (value or "").strip()
    if not COMMA_SAFE_RE.match(s):
        return value
    return s.replace(".", ",") if "." in s else s + ",0"


def test_script(entry, res, verbose):
    script = os.path.join(SK, entry["script"])
    label = entry["script"].split("/")[0]
    if not os.path.exists(script):
        res.ok(f"{label} exists", False, f"missing {script}")
        return
    sample = os.path.join(SK, entry["sample"])
    res.ok(f"{label} sample exists", os.path.exists(sample), f"missing {entry['sample']}")
    if not os.path.exists(sample):
        return
    with open(sample, encoding="utf-8-sig", newline="") as fh:
        text = fh.read()
    rows, headers = rows_of(text)

    def check(name, args, stdin_text=None, exit_code=0, out_contains=(), same_as=None, err_prefix=None,
              err_contains=None):
        code, out, err = run([script, *args], stdin_text)
        if verbose:
            print(f"    $ {os.path.basename(script)} {' '.join(args)} -> exit {code}")
        res.ok(f"{label} {name}: exit {exit_code}", code == exit_code, f"got {code}; stderr={err.strip()[:200]}")
        res.ok(f"{label} {name}: no traceback", "Traceback" not in err, err.strip()[:200])
        for m in out_contains:
            res.ok(f"{label} {name}: output mentions {m!r}", m in out, out[:200])
        if same_as is not None:
            res.ok(f"{label} {name}: identical output", out == same_as, "output differs from plain sample run")
        if err_prefix is not None:
            res.ok(f"{label} {name}: stderr starts with {err_prefix!r}", err.lstrip().startswith(err_prefix), err.strip()[:200])
        if err_contains is not None:
            res.ok(f"{label} {name}: stderr mentions {err_contains!r}", err_contains in err, err.strip()[:200])
        return out

    def check_json(name, args):
        out = check(name, [*args, "--format", "json"])
        try:
            return json.loads(out)
        except ValueError as exc:
            res.ok(f"{label} {name}: valid JSON", False, str(exc))
            return None

    with tempfile.TemporaryDirectory() as tmp:
        check("--help", ["--help"])
        base_out = check("sample", [sample], out_contains=entry["markers"])
        check("stdin", ["-"], stdin_text=text, same_as=base_out)
        bom = write(tmp, "bom.csv", "﻿" + text)
        check("bom", [bom], same_as=base_out)
        crlf = write(tmp, "crlf.csv", text.replace("\r\n", "\n").replace("\n", "\r\n"))
        check("crlf", [crlf], same_as=base_out)
        semi = write(tmp, "semi.csv", csv_text(headers, rows, ";"))
        check("semicolon", [semi], same_as=base_out)
        js = write(tmp, "data.json", json.dumps(rows))
        check("json", [js, "--json"], same_as=base_out)
        # A .json file without --json must either be auto-detected (identical output)
        # or rejected with a clear error -- never mis-parsed as CSV.
        code, out, err = run([script, js])
        res.ok(f"{label} json-without-flag: auto-detected or rejected",
               (code == 0 and out == base_out) or (code == 2 and err.lstrip().startswith("error:")),
               f"exit {code}; stderr={err.strip()[:200]}")
        res.ok(f"{label} json-without-flag: no traceback", "Traceback" not in err, err.strip()[:200])
        bad_js = write(tmp, "bad.json", "[1, 2]")
        check("json-non-object", [bad_js, "--json"], exit_code=2, err_prefix="error:")
        malformed = write(tmp, "malformed.json", '{"a": [1,')
        check("malformed-json", [malformed, "--json"], exit_code=2, err_prefix="error:")
        empty = write(tmp, "empty.csv", "")
        check("empty", [empty], exit_code=2, err_prefix="error:")
        header_only = write(tmp, "header.csv", text.splitlines()[0] + "\n")
        check("header-only", [header_only], exit_code=2, err_prefix="error:")

        col = find_col(headers, entry.get("numeric_col"))
        if entry.get("numeric_col"):
            res.ok(f"{label} numeric column {entry['numeric_col']!r} in sample", col is not None, f"headers {headers}")
        if col and rows:
            bad_rows = [dict(r) for r in rows]
            bad_rows[0][col] = "nan"
            nan_file = write(tmp, "nan.csv", csv_text(headers, bad_rows))
            check("nan", [nan_file], exit_code=2, err_prefix="error:")
            for name, value in (("json-true", True), ("json-infinity", float("inf"))):
                js_rows = [dict(r) for r in rows]
                js_rows[0][col] = value
                bad = write(tmp, f"{name}.json", json.dumps(js_rows))  # Infinity is what json.dumps writes
                check(name, [bad, "--json"], exit_code=2, err_prefix="error:")

        ccol = find_col(headers, entry.get("comma_col"))
        if entry.get("comma_col"):
            res.ok(f"{label} comma column {entry['comma_col']!r} in sample", ccol is not None, f"headers {headers}")
        if ccol and rows:
            comma_rows = [dict(r, **{ccol: decimal_comma(r[ccol])}) for r in rows]
            res.ok(f"{label} decimal-comma: sample has a value to rewrite",
                   any(c[ccol] != r[ccol] for c, r in zip(comma_rows, rows)), ccol)
            comma = write(tmp, "comma.csv", csv_text(headers, comma_rows, ";"))
            check("decimal-comma", [comma], same_as=base_out)
            amb_rows = [dict(r) for r in rows]
            amb_rows[0][ccol] = "1.000,50"
            amb = write(tmp, "ambiguous.csv", csv_text(headers, amb_rows, ";"))
            check("ambiguous-number", [amb], exit_code=2, err_prefix="error:", err_contains="ambiguous")

        for fmt in entry.get("formats", DEFAULT_FORMATS):
            if fmt == "json":
                check_json("format json", [sample])
            else:
                check(f"format {fmt}", [sample, "--format", fmt])

        for args, pins in entry.get("pins", []):
            data = check_json(f"pins {' '.join(args) or '(default)'}", [sample, *args])
            for name, getter, expected in pins:
                try:
                    got = getter(data) if data is not None else None
                except (KeyError, IndexError, TypeError) as exc:
                    got = f"<missing: {exc!r}>"
                res.ok(f"{label} canon {name} == {expected!r}", got == expected, f"got {got!r}")

        if entry.get("broken"):
            broken = write(tmp, "broken.csv", entry["broken"])
            check("broken-input-fails-validation", [broken], exit_code=1)
        for name, transform, args, exit_code in entry.get("extra_fail", []):
            path = sample
            if transform is not None:
                path = write(tmp, f"{name}.csv", csv_text(headers, transform(rows)))
            check(name, [path, *args], exit_code=exit_code)

        extra = EXTRA_CASES.get(label)
        if extra:
            extra(tmp, check, check_json, res, label, sample)


# ----------------------------------------------------------------------------- script-specific cases
def _schedule_cases(tmp, check, check_json, res, label, sample):
    ms = write(tmp, "milestone.csv", "id,name,duration,predecessors\nA,Build,5,\nM,Go-live,0,A\n")
    data = check_json("terminal milestone", [ms, "--unit", "days", "--start-date", "2026-05-11", "--workdays"])
    if data is not None:
        m = next(t for t in data["tasks"] if t["id"] == "M")
        finish = data["summary"]["calendar"]["finish_date"]
        res.ok(f"{label} terminal milestone dated on the project finish", m["finish"] == finish == "2026-05-15",
               f"milestone {m['finish']}, project finish {finish}")


def _pert_cases(tmp, check, check_json, res, label, sample):
    dup = write(tmp, "dup.csv", "id,optimistic,most_likely,pessimistic\nA,1,2,3\na,10,20,30\n")
    check("duplicate-id", [dup], exit_code=2, err_prefix="error:", err_contains="duplicate id")


def _evm_cases(tmp, check, check_json, res, label, sample):
    dup = write(tmp, "dup.csv", "task,pv,ev,ac,bac\nSSO,60000,45000,65000,78750\nSSO,60000,45000,65000,78750\n")
    check("duplicate-work-package", [dup], exit_code=2, err_prefix="error:", err_contains="duplicate work package")
    long_names = write(tmp, "long.csv", "task,pv,ev,ac,bac\n"
                       "WP 3.2 Customer self-service portal build - sprint A,10,10,10,100\n"
                       "WP 3.2 Customer self-service portal build - sprint B,10,5,10,100\n")
    data = check_json("long names stay distinct", [long_names])
    if data is not None:
        res.ok(f"{label} long names: two rows, BAC 200", len(data["rows"]) == 2 and data["summary"]["total"]["bac"] == 200,
               f"{len(data['rows'])} rows, BAC {data['summary']['total']['bac']}")


def _issue_log_cases(tmp, check, check_json, res, label, sample):
    first = check("csv round trip 1", [sample, "--as-of", "2026-07-10", "--format", "csv"])
    again = write(tmp, "round1.csv", first)
    second = check("csv round trip 2", [again, "--as-of", "2026-07-10", "--format", "csv"])
    res.ok(f"{label} csv output re-imports to the identical file", first == second, "second run differs")


EXTRA_CASES = {
    "project-schedule": _schedule_cases,
    "estimation": _pert_cases,
    "cost-management": _evm_cases,
    "project-delivery": _issue_log_cases,
}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="test_scripts.py",
                                     description="Test every helper script against its sample and the I/O contract.")
    parser.add_argument("-k", metavar="PATTERN", help="only scripts whose path contains PATTERN")
    parser.add_argument("-v", "--verbose", action="store_true", help="show every command")
    args = parser.parse_args(argv)
    selected = [e for e in REGISTRY if not args.k or args.k in e["script"]]
    if not selected:
        print(f"error: no script matches -k {args.k!r}", file=sys.stderr)
        return 1
    res = Result()
    for entry in selected:
        print(f"- {entry['script']}")
        test_script(entry, res, args.verbose)
    print(f"\n{res.passed} check(s) passed, {len(res.failed)} failed")
    for f in res.failed:
        print(f"  FAIL: {f}")
    return 1 if res.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
