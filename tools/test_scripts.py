#!/usr/bin/env python3
"""Test every helper script in the catalog against its bundled sample and the
hardening contract (README "Helper scripts"). Standard library only.

For each script it checks:
  * --help exits 0
  * the bundled sample runs (exit 0) and the output contains the expected markers
  * the same data via stdin ("-"), as JSON (--json), with a UTF-8 BOM, with CRLF line
    endings and semicolon-delimited all produce the SAME output as the plain sample
  * bad input is rejected with `error: ...` on stderr and exit 2, never a traceback:
    empty file, header-only file, a `nan` value, a JSON file passed without --json,
    a JSON list containing a non-object
  * validators (wbs_validate, raci_validate) return exit 1 on a deliberately broken input

Usage:
    python tools/test_scripts.py            # run everything
    python tools/test_scripts.py -k raci    # only scripts whose path contains "raci"
    python tools/test_scripts.py -v         # show every command
Exit code is non-zero if any check fails.
"""
from __future__ import annotations

import csv
import io
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(ROOT, ".claude", "skills")

# script (relative to .claude/skills) -> sample input, expected stdout markers, broken input (validators)
REGISTRY = [
    {
        "script": "risk-register/scripts/risk_score.py",
        "sample": "risk-register/assets/risk-register-template.csv",
        "markers": ["R001", "EMV"],
        "numeric_col": "probability",
    },
    {
        "script": "estimation/scripts/pert_estimate.py",
        "sample": "estimation/assets/estimation-worksheet.csv",
        "markers": ["Total", "95%"],
        "numeric_col": "most_likely",
    },
    {
        "script": "project-schedule/scripts/critical_path.py",
        "sample": "project-schedule/assets/schedule-template.csv",
        "markers": ["Critical path", "18"],
        "numeric_col": "duration",
    },
    {
        "script": "cost-management/scripts/health_check.py",
        "sample": "cost-management/assets/evm-snapshot.csv",
        "fallback_sample": "cost-management/assets/cost-baseline.csv",
        "markers": ["CPI", "AMBER"],
        "numeric_col": "ev",
    },
    {
        "script": "business-case/scripts/roi_npv.py",
        "sample": "business-case/assets/cashflows.csv",
        "markers": ["NPV"],
        "numeric_col": "cashflow",
    },
    {
        "script": "work-breakdown-structure/scripts/wbs_validate.py",
        "sample": "work-breakdown-structure/assets/wbs.csv",
        "markers": ["PASS"],
        "numeric_col": "weight",
        "broken": "id,name,weight\n1,Root,\n1.1,A,60\n1.1,Dup,30\n1.3.1,Orphan,10\n",
    },
    {
        "script": "raci-matrix/scripts/raci_validate.py",
        "sample": "raci-matrix/assets/raci-template.csv",
        "markers": ["PASS"],
        "numeric_col": None,
        "broken": "Activity,Sponsor,PM,Dev\nWrite charter,A,A,R\nBuild portal,,,C\n",
    },
    {
        "script": "change-request/scripts/change_impact.py",
        "sample": "change-request/assets/change-log.csv",
        "markers": ["CR001"],
        "numeric_col": "cost_impact",
    },
    {
        "script": "resource-management/scripts/capacity_check.py",
        "sample": "resource-management/assets/resource-allocation.csv",
        "markers": ["OVER"],
        "numeric_col": "allocated",
    },
    {
        "script": "agile-delivery/scripts/velocity_forecast.py",
        "sample": "agile-delivery/assets/sprint-history-sample.csv",
        "markers": ["velocity"],
        "numeric_col": "completed_points",
        "optional": True,
    },
]


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


def test_script(entry, res, verbose):
    script = os.path.join(SK, entry["script"])
    label = entry["script"].split("/")[0]
    if not os.path.exists(script):
        if entry.get("optional"):
            print(f"  skip {label}: script not present")
            return
        res.ok(f"{label} exists", False, f"missing {script}")
        return
    sample = os.path.join(SK, entry["sample"])
    if not os.path.exists(sample) and entry.get("fallback_sample"):
        sample = os.path.join(SK, entry["fallback_sample"])
    res.ok(f"{label} sample exists", os.path.exists(sample), sample)
    if not os.path.exists(sample):
        return
    with open(sample, encoding="utf-8-sig", newline="") as fh:
        text = fh.read()
    rows, headers = rows_of(text)

    def check(name, args, stdin_text=None, exit_code=0, out_contains=(), same_as=None, err_prefix=None):
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
        return out

    with tempfile.TemporaryDirectory() as tmp:
        check("--help", ["--help"])
        base_out = check("sample", [sample], out_contains=entry["markers"])
        check("stdin", ["-"], stdin_text=text, same_as=base_out)
        bom = write(tmp, "bom.csv", "﻿" + text)
        check("bom", [bom], same_as=base_out)
        crlf = write(tmp, "crlf.csv", text.replace("\r\n", "\n").replace("\n", "\r\n"))
        check("crlf", [crlf], same_as=base_out)
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=headers, delimiter=";")
        w.writeheader()
        w.writerows(rows)
        semi = write(tmp, "semi.csv", buf.getvalue())
        check("semicolon", [semi], same_as=base_out)
        js = write(tmp, "data.json", json.dumps(rows))
        check("json", [js, "--json"], same_as=base_out)
        check("json-without-flag", [js], exit_code=2, err_prefix="error:")
        bad_js = write(tmp, "bad.json", "[1, 2]")
        check("json-non-object", [bad_js, "--json"], exit_code=2, err_prefix="error:")
        empty = write(tmp, "empty.csv", "")
        check("empty", [empty], exit_code=2, err_prefix="error:")
        header_only = write(tmp, "header.csv", text.splitlines()[0] + "\n")
        check("header-only", [header_only], exit_code=2, err_prefix="error:")
        if entry.get("numeric_col") and rows:
            col = next((h for h in headers if h.lower() == entry["numeric_col"].lower()), None)
            if col:
                bad_rows = [dict(r) for r in rows]
                bad_rows[0][col] = "nan"
                buf = io.StringIO()
                w = csv.DictWriter(buf, fieldnames=headers)
                w.writeheader()
                w.writerows(bad_rows)
                nan_file = write(tmp, "nan.csv", buf.getvalue())
                check("nan", [nan_file], exit_code=2, err_prefix="error:")
        if entry.get("broken"):
            broken = write(tmp, "broken.csv", entry["broken"])
            check("broken-input-fails-validation", [broken], exit_code=1)


def main(argv):
    verbose = "-v" in argv
    pattern = None
    if "-k" in argv:
        pattern = argv[argv.index("-k") + 1]
    res = Result()
    for entry in REGISTRY:
        if pattern and pattern not in entry["script"]:
            continue
        print(f"- {entry['script']}")
        test_script(entry, res, verbose)
    print(f"\n{res.passed} check(s) passed, {len(res.failed)} failed")
    for f in res.failed:
        print(f"  FAIL: {f}")
    return 1 if res.failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
