#!/usr/bin/env python3
"""Score a project risk register: exposure (probability x impact = EMV), HIGH/MEDIUM/LOW
severity bands, residual (post-response) exposure, a Monte Carlo simulation of total threat
exposure for contingency sizing, and governance checks. Standard library only.

Reads the register from CSV (delimiter auto-detected: , ; tab |) or JSON (--json), prints
the risks sorted by exposure (highest first) with portfolio totals, and exits 0. Notes and
warnings go to stderr so stdout stays machine-readable.

INPUT COLUMNS / KEYS  (case-insensitive; a trailing "(unit)" in a header is ignored; extra
columns are passed through; "row N" in messages = Nth data row, header excluded)
    probability            chance it occurs  (aliases: prob, p, likelihood)             REQUIRED
    impact                 POSITIVE magnitude if it occurs (i, cost, consequence)       REQUIRED
    id                     short identifier (risk_id, ref); default R001, R002, ...    optional
    description            what could happen (desc, risk, title)                       optional
    type                   threat | opportunity (kind); default threat                 optional
    category               free text, e.g. Technical, Scope, Vendor                    optional
    owner, response, trigger, raised, review_date                                      optional
    residual_probability   post-response probability (res_prob, post_probability)       optional
    residual_impact        post-response impact (res_impact, post_impact)               optional
    impact_min, impact_max optimistic / pessimistic impact for --simulate (triangular)  optional
    status                 open (default) | occurred | retired | realised | closed ...  optional

A negative impact is rejected: store every impact as a positive magnitude and mark upside
risks with type=opportunity. Rows whose status is closed / occurred / retired / realised are
validated but excluded from scoring unless --include-closed is given.

SCALES
    --prob-scale auto      (default) inferred ONCE for the whole register: every value <= 1
                           -> fractions (0.4); any value > 5 -> percents (40). A value in the
                           ambiguous range 1 < p <= 5 is refused: pass --prob-scale percent
                           or --prob-scale 1-5. A cell written "40%" is always a percent.
    --prob-scale fraction  values must be 0-1      --prob-scale percent   values must be 0-100
    --prob-scale 1-5 --impact-scale 1-5   (always together) score = P x I on the 1-25 grid;
                           default bands HIGH >= 15, MEDIUM >= 8.
    --impact-scale units   (default) impact in ONE consistent unit (money, days, points).
                           Default bands HIGH >= 25,000 and MEDIUM >= 5,000 (5% / 1% of the
                           sample Helios BAC of $500,000). Prefer --bac B (bands = 5% / 1% of
                           your budget) or explicit --high / --medium.

FORMULAS
    exposure (EMV)      = probability x impact                  (magnitude; ranked and banded)
    residual exposure   = residual_probability x residual_impact (a missing residual field
                          falls back to the inherent value); --basis residual bands on it
    signed EMV          = -exposure for threats, +exposure for opportunities (the convention
                          used in quantitative risk analysis and decision trees)
    Net EMV             = total threat EMV - total opportunity EMV
    simulation trial    = sum of impact over the threats whose random draw < probability;
                          a threat with impact_min/impact_max draws triangular(min, max,
                          mode=impact). Reports mean, P50/P80/P90/P95, max, a histogram and
                          P(total > --reserve). Opportunities are not simulated.

EXIT CODES   0 scored  ·  1 --check found governance problems  ·  2 bad input or usage
             (message "error: ..." on stderr, never a traceback)

EXAMPLES
    python .claude/skills/risk-register/scripts/risk_score.py .claude/skills/risk-register/assets/risk-register-template.csv
    python .claude/skills/risk-register/scripts/risk_score.py register.json --json --top 5 --format md
    cat register.csv | python .claude/skills/risk-register/scripts/risk_score.py - --simulate 10000 --seed 42 --reserve 40000
    python .claude/skills/risk-register/scripts/risk_score.py matrix.csv --prob-scale 1-5 --impact-scale 1-5
    python .claude/skills/risk-register/scripts/risk_score.py register.csv --bac 500000 --basis residual --check
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import random
import re
import statistics
import sys
import unicodedata

BOM = "﻿"
JSON_KEY = "risks"

DEFAULT_HIGH, DEFAULT_MEDIUM = 25000.0, 5000.0  # 5% / 1% of the sample Helios BAC ($500,000)
GRID_HIGH, GRID_MEDIUM = 15.0, 8.0  # 1-25 P x I grid
BAC_HIGH_PCT, BAC_MEDIUM_PCT = 0.05, 0.01
MIN_TRIALS, MAX_TRIALS = 100, 5_000_000

CLOSED_STATUSES = {
    "closed", "retired", "realised", "realized", "occurred", "materialised", "materialized",
    "cancelled", "canceled", "done", "expired",
}
OPEN_STATUSES = {"open", "active", "monitoring", "watch", "new", "in progress", "accepted", "escalated"}
THREAT_WORDS = {"threat", "t", "negative", "neg", "downside", "-"}
OPPORTUNITY_WORDS = {"opportunity", "opp", "o", "positive", "pos", "upside", "+"}

PROB_ALIASES = ("probability", "prob", "p", "likelihood")
IMPACT_ALIASES = ("impact", "i", "cost", "consequence")
ID_ALIASES = ("id", "risk_id", "risk id", "ref")
DESC_ALIASES = ("description", "desc", "risk", "title")
TYPE_ALIASES = ("type", "kind")
CATEGORY_ALIASES = ("category", "cat")
OWNER_ALIASES = ("owner", "risk owner")
RESPONSE_ALIASES = ("response", "response plan", "mitigation")
TRIGGER_ALIASES = ("trigger", "trigger condition")
STATUS_ALIASES = ("status", "state")
RAISED_ALIASES = ("raised", "date raised", "date_raised")
REVIEW_ALIASES = ("review_date", "review date", "last_reviewed")
RES_PROB_ALIASES = ("residual_probability", "residual_prob", "res_prob", "post_probability", "post_prob")
RES_IMPACT_ALIASES = ("residual_impact", "res_impact", "post_impact")
IMPACT_MIN_ALIASES = ("impact_min", "min_impact", "impact_low", "optimistic_impact")
IMPACT_MAX_ALIASES = ("impact_max", "max_impact", "impact_high", "pessimistic_impact")
COMPUTED_COLUMNS = ("rank", "exposure", "severity", "residual_exposure", "signed_emv")

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


def canon(header):
    """Canonical header name: BOM and whitespace stripped, trailing '(unit)' removed, lower-cased."""
    return UNIT_SUFFIX_RE.sub("", str(header).lstrip(BOM).strip()).strip().lower()


def warn(msg):
    print(f"warning: {msg}", file=sys.stderr)


def note(msg):
    print(f"note: {msg}", file=sys.stderr)


# --------------------------------------------------------------------------- formatting
def _clean(x):
    return 0.0 if abs(x) < 5e-7 else x  # print 0.00, never -0.00


def money(x):
    return f"{_clean(round(x, 2)):,.2f}"


def fmt_num(x):
    x = _clean(x)
    return f"{x:,.0f}" if abs(x - round(x)) < 1e-9 else f"{x:,.2f}"


def fmt_prob(p, grid):
    if grid:
        return fmt_num(p)
    pct = p * 100.0
    return f"{pct:.0f}%" if abs(pct - round(pct)) < 1e-9 else f"{pct:.1f}%"


def fmt_pct(x):
    return f"{x * 100:.1f}%"


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


# --------------------------------------------------------------------------- parsing
def _prob_cell(raw, where):
    """Keep the raw probability until the register-wide scale is known."""
    had_pct = isinstance(raw, str) and raw.strip().endswith("%")
    value = _num(raw, where, minimum=0)
    return {"value": value, "pct": had_pct, "where": where, "raw": raw}


def _impact(raw, where, impact_scale):
    if impact_scale == "1-5":
        return _num(raw, where, minimum=1, maximum=5)
    v = _num(raw, where)
    if v < 0:
        raise ValueError(
            f"{where}: {raw!r} is negative; store impacts as positive magnitudes and set "
            "type=opportunity for upside risks"
        )
    return v


def parse_register(rows, headers, impact_scale):
    """First pass: validate every cell; probabilities stay raw for scale inference."""
    require_columns([canon(h) for h in headers], [PROB_ALIASES, IMPACT_ALIASES])
    parsed = []
    for i, row in enumerate(rows, 1):
        clean = {canon(k): v for k, v in row.items() if k is not None}
        rid = sanitize(_get(clean, *ID_ALIASES, default=f"R{i:03d}"))
        tag = f"row {i} ({rid})"
        type_raw = sanitize(_get(clean, *TYPE_ALIASES, default="threat")).lower()
        if type_raw in THREAT_WORDS:
            rtype = "threat"
        elif type_raw in OPPORTUNITY_WORDS:
            rtype = "opportunity"
        else:
            raise ValueError(f"{tag}, column type: {type_raw!r} is not 'threat' or 'opportunity'")
        prob_raw = _get(clean, *PROB_ALIASES)
        impact_raw = _get(clean, *IMPACT_ALIASES)
        if prob_raw is None:
            raise ValueError(f"{tag}: missing probability")
        if impact_raw is None:
            raise ValueError(f"{tag}: missing impact")
        p_cell = _prob_cell(prob_raw, f"{tag}, column probability")
        impact = _impact(impact_raw, f"{tag}, column impact", impact_scale)
        rp_raw = _get(clean, *RES_PROB_ALIASES)
        ri_raw = _get(clean, *RES_IMPACT_ALIASES)
        rp_cell = _prob_cell(rp_raw, f"{tag}, column residual_probability") if rp_raw is not None else None
        r_impact = _impact(ri_raw, f"{tag}, column residual_impact", impact_scale) if ri_raw is not None else None
        imin_raw = _get(clean, *IMPACT_MIN_ALIASES)
        imax_raw = _get(clean, *IMPACT_MAX_ALIASES)
        if (imin_raw is None) != (imax_raw is None):
            raise ValueError(f"{tag}: impact_min and impact_max must be given together")
        imin = imax = None
        if imin_raw is not None:
            imin = _impact(imin_raw, f"{tag}, column impact_min", impact_scale)
            imax = _impact(imax_raw, f"{tag}, column impact_max", impact_scale)
            if not (imin <= impact <= imax):
                raise ValueError(
                    f"{tag}: impact_min ({fmt_num(imin)}) <= impact ({fmt_num(impact)}) <= "
                    f"impact_max ({fmt_num(imax)}) must hold"
                )
        status = sanitize(_get(clean, *STATUS_ALIASES, default="Open"))
        st = status.lower()
        closed = st in CLOSED_STATUSES or st.startswith("closed")
        if not closed and st not in OPEN_STATUSES:
            warn(f"{tag}: unrecognised status {status!r}; scored as open")
        parsed.append(
            {
                "row": i,
                "id": rid,
                "description": sanitize(_get(clean, *DESC_ALIASES, default="")),
                "type": rtype,
                "category": sanitize(_get(clean, *CATEGORY_ALIASES, default="")),
                "owner": sanitize(_get(clean, *OWNER_ALIASES, default="")),
                "response": sanitize(_get(clean, *RESPONSE_ALIASES, default="")),
                "trigger": sanitize(_get(clean, *TRIGGER_ALIASES, default="")),
                "raised": sanitize(_get(clean, *RAISED_ALIASES, default="")),
                "review_date": sanitize(_get(clean, *REVIEW_ALIASES, default="")),
                "status": status,
                "closed": closed,
                "p_cell": p_cell,
                "impact": impact,
                "rp_cell": rp_cell,
                "r_impact": r_impact,
                "impact_min": imin,
                "impact_max": imax,
                "original": row,
            }
        )
    return parsed


def infer_prob_scale(cells, requested):
    """Decide the probability scale ONCE for the whole register (never per cell)."""
    if requested != "auto":
        return requested
    plain = [c for c in cells if not c["pct"]]
    if not plain:
        return "percent"  # every cell carries an explicit % sign
    top = max(plain, key=lambda c: c["value"])
    mx = top["value"]
    if mx <= 1.0:
        return "fraction"
    if mx <= 5.0:
        raise ValueError(
            f"{top['where']}: {top['raw']!r} is ambiguous (a percent or a 1-5 score?); "
            "pass --prob-scale percent or --prob-scale 1-5"
        )
    if mx > 100.0:
        raise ValueError(
            f"{top['where']}: {top['raw']!r} is above 100; probabilities must be fractions (0-1), "
            "percents (0-100) or 1-5 scores"
        )
    if any(c["value"] <= 1.0 for c in plain):
        warn(
            "probability column mixes values <= 1 and > 1; all read as percent (e.g. 0.5 -> 0.5%); "
            "pass --prob-scale fraction if that is wrong"
        )
    return "percent"


def to_fraction(cell, scale):
    """Convert a raw probability cell under the register-wide scale (1-5 scores stay 1-5)."""
    v, raw, where = cell["value"], cell["raw"], cell["where"]
    if cell["pct"]:
        if scale == "1-5":
            raise ValueError(f"{where}: {raw!r} has a % sign, which is not valid on a 1-5 scale")
        if v > 100.0:
            raise ValueError(f"{where}: {raw!r} is above 100%")
        return v / 100.0
    if scale == "fraction":
        if v > 1.0:
            raise ValueError(
                f"{where}: {raw!r} is above 1; under --prob-scale fraction probabilities are 0-1 "
                "(pass --prob-scale percent for 0-100 values)"
            )
        return v
    if scale == "percent":
        if v > 100.0:
            raise ValueError(f"{where}: {raw!r} is above 100%")
        return v / 100.0
    if v < 1.0 or v > 5.0:
        raise ValueError(f"{where}: {raw!r} is outside the 1-5 probability scale")
    return v


# --------------------------------------------------------------------------- scoring
def severity(exposure, high, medium):
    if exposure >= high:
        return "HIGH"
    if exposure >= medium:
        return "MEDIUM"
    return "LOW"


def score(parsed, scale, basis, high, medium):
    scored = []
    for r in parsed:
        p = to_fraction(r["p_cell"], scale)
        rp = to_fraction(r["rp_cell"], scale) if r["rp_cell"] is not None else None
        has_residual = rp is not None or r["r_impact"] is not None
        rp_eff = rp if rp is not None else p
        ri_eff = r["r_impact"] if r["r_impact"] is not None else r["impact"]
        exposure = round(p * r["impact"], 6)
        residual = round(rp_eff * ri_eff, 6) if has_residual else None
        basis_exposure = residual if (basis == "residual" and residual is not None) else exposure
        out = {k: v for k, v in r.items() if k not in ("p_cell", "rp_cell", "r_impact")}
        out.update(
            {
                "probability": p,
                "exposure": exposure,
                "signed_emv": (-exposure if r["type"] == "threat" else exposure) if exposure else 0.0,
                "residual_probability": rp_eff if has_residual else None,
                "residual_impact": ri_eff if has_residual else None,
                "residual_exposure": residual,
                "basis_exposure": basis_exposure,
                "severity": severity(basis_exposure, high, medium),
            }
        )
        scored.append(out)
    scored.sort(key=lambda r: (-r["basis_exposure"], r["id"]))
    for n, r in enumerate(scored, 1):
        r["rank"] = n
    return scored


def summarize(active, scored, shown, args, scale, high, medium, band_source, grid):
    threats = [r for r in active if r["type"] == "threat"]
    opps = [r for r in active if r["type"] == "opportunity"]
    total_t = round(sum(r["exposure"] for r in threats), 6)
    total_o = round(sum(r["exposure"] for r in opps), 6)
    has_residual = any(r["residual_exposure"] is not None for r in active)
    res_t = round(sum(r["residual_exposure"] if r["residual_exposure"] is not None else r["exposure"] for r in threats), 6)
    res_o = round(sum(r["residual_exposure"] if r["residual_exposure"] is not None else r["exposure"] for r in opps), 6)
    reduction = round(total_t - res_t, 6)
    counts = {b: sum(1 for r in active if r["severity"] == b) for b in ("HIGH", "MEDIUM", "LOW")}
    return {
        "probability_scale": scale,
        "impact_scale": args.impact_scale,
        "basis": args.basis,
        "band_high": high,
        "band_medium": medium,
        "band_source": band_source,
        "value_label": "score" if grid else "EMV",
        "risks_in_input": len(scored),
        "risks_scored": len(active),
        "risks_shown": len(shown),
        "excluded_closed": len(scored) - len(active),
        "threats": len(threats),
        "opportunities": len(opps),
        "total_threat_emv": total_t,
        "total_opportunity_emv": total_o,
        "net_emv": round(total_t - total_o, 6),
        "has_residual": has_residual,
        "total_residual_threat_emv": res_t if has_residual else None,
        "total_residual_opportunity_emv": res_o if has_residual else None,
        "threat_reduction": reduction if has_residual else None,
        "threat_reduction_pct": (reduction / total_t if total_t else 0.0) if has_residual else None,
        "severity_counts": counts,
    }


# --------------------------------------------------------------------------- simulation
def simulate(active, trials, seed, reserve, basis):
    rng = random.Random(seed)
    specs, ranged = [], 0
    for r in active:
        if r["type"] != "threat":
            continue
        use_residual = basis == "residual" and r["residual_exposure"] is not None
        p = r["residual_probability"] if use_residual else r["probability"]
        imp = r["residual_impact"] if use_residual else r["impact"]
        lo = hi = None
        if r["impact_min"] is not None:
            ratio = (imp / r["impact"]) if r["impact"] else 1.0
            lo, hi = r["impact_min"] * ratio, r["impact_max"] * ratio
            ranged += 1
        specs.append((p, imp, lo, hi))
    totals = []
    for _ in range(trials):
        total = 0.0
        for p, imp, lo, hi in specs:
            if rng.random() < p:
                total += rng.triangular(lo, hi, imp) if lo is not None else imp
        totals.append(total)
    totals.sort()
    q = statistics.quantiles(totals, n=100, method="inclusive")
    top = totals[-1]
    hist = []
    if top > 0:
        width = top / 10.0
        counts = [0] * 10
        for t in totals:
            counts[min(int(t / width), 9)] += 1
        hist = [
            {"from": round(k * width, 2), "to": round((k + 1) * width, 2), "share": counts[k] / trials}
            for k in range(10)
        ]
    result = {
        "trials": trials,
        "seed": seed,
        "basis": basis,
        "threats_simulated": len(specs),
        "threats_with_range": ranged,
        "mean": round(statistics.fmean(totals), 2),
        "p50": round(q[49], 2),
        "p80": round(q[79], 2),
        "p90": round(q[89], 2),
        "p95": round(q[94], 2),
        "max": round(top, 2),
        "reserve": reserve,
        "p_exceed_reserve": (sum(1 for t in totals if t > reserve) / trials) if reserve is not None else None,
        "histogram": hist,
    }
    return result


# --------------------------------------------------------------------------- governance checks
def run_checks(active, scored, grid):
    problems = []
    ids = [r["id"] for r in scored]
    for d in sorted({x for x in ids if ids.count(x) > 1}):
        problems.append(f"duplicate id {d!r} ({ids.count(d)} rows)")
    for r in active:
        tag = f"{r['id']} ({r['severity']} {r['type']})"
        if r["severity"] in ("HIGH", "MEDIUM"):
            if not r["owner"]:
                problems.append(f"{tag}: no owner")
            if not r["response"]:
                problems.append(f"{tag}: no response")
            if not r["trigger"]:
                problems.append(f"{tag}: no trigger")
        if not grid and r["probability"] >= 1.0:
            problems.append(f"{tag}: probability is 100% - that is an issue, not a risk; move it to the issue log")
        if r["probability"] <= 0.0:
            problems.append(f"{tag}: probability is 0 - retire it or re-estimate")
        if r["type"] == "threat" and r["residual_exposure"] is not None and r["residual_exposure"] > r["exposure"]:
            problems.append(
                f"{tag}: residual exposure {money(r['residual_exposure'])} exceeds inherent {money(r['exposure'])}"
            )
    return {"passed": not problems, "problems": problems}


# --------------------------------------------------------------------------- rendering
def table_columns(shown, args, grid):
    cols = [("ID", False), ("Severity", False), ("Type", False), ("Prob", True), ("Impact", True),
            ("Exposure", True)]
    if any(r["residual_exposure"] is not None for r in shown):
        cols.append(("Residual", True))
    if any(r["owner"] for r in shown):
        cols.append(("Owner", False))
    if args.include_closed:
        cols.append(("Status", False))
    cols.append(("Description", False))
    return cols


def table_cells(r, cols, grid):
    values = {
        "ID": r["id"],
        "Severity": r["severity"],
        "Type": r["type"],
        "Prob": fmt_prob(r["probability"], grid),
        "Impact": fmt_num(r["impact"]),
        "Exposure": money(r["exposure"]),
        "Residual": money(r["residual_exposure"]) if r["residual_exposure"] is not None else "-",
        "Owner": truncate(r["owner"], 16),
        "Status": r["status"],
        "Description": truncate(r["description"], 40),
    }
    return [values[name] for name, _ in cols]


def summary_lines(s, grid):
    label = s["value_label"]
    p_desc = {"fraction": "fractions (0-1)", "percent": "percents (0-100)", "1-5": "1-5 scores"}[s["probability_scale"]]
    i_desc = "1-5 scores" if grid else "units"
    lines = [
        f"Scale: probabilities read as {p_desc}; impacts as {i_desc}. "
        f"Bands: HIGH >= {money(s['band_high'])}, MEDIUM >= {money(s['band_medium'])} ({s['band_source']}).",
    ]
    if s["risks_shown"] < s["risks_scored"]:
        lines.append(f"Showing the top {s['risks_shown']} of {s['risks_scored']} scored risk(s); totals cover all scored risks.")
    lines.append(f"Total threat {label}:        {money(s['total_threat_emv'])}  ({s['threats']} threat(s))")
    lines.append(f"Total opportunity {label}:   {money(s['total_opportunity_emv'])}  ({s['opportunities']} opportunity(ies))")
    lines.append(f"Net {label} (threats - opportunities): {money(s['net_emv'])}")
    if s["has_residual"]:
        verb = "reduce" if s["threat_reduction"] >= 0 else "INCREASE"
        lines.append(
            f"Total residual threat {label}: {money(s['total_residual_threat_emv'])}  "
            f"(planned responses {verb} threat exposure by {money(abs(s['threat_reduction']))}, "
            f"{fmt_pct(abs(s['threat_reduction_pct']))}); residual opportunity {label}: "
            f"{money(s['total_residual_opportunity_emv'])}"
        )
    if s["basis"] == "residual":
        lines.append("Severity bands and ranking use RESIDUAL exposure (--basis residual).")
    c = s["severity_counts"]
    lines.append(f"Severity counts: HIGH={c['HIGH']}  MEDIUM={c['MEDIUM']}  LOW={c['LOW']}")
    if s["excluded_closed"]:
        lines.append(
            f"Excluded {s['excluded_closed']} closed/occurred/retired/realised risk(s) from scoring; "
            "pass --include-closed to score them."
        )
    return lines


def simulation_lines(sim):
    lines = [
        f"Monte Carlo of total threat exposure ({sim['basis']} values; {sim['trials']:,} trials; seed {sim['seed']}; "
        f"{sim['threats_simulated']} threat(s), {sim['threats_with_range']} with an impact_min/impact_max range):",
        f"  mean {money(sim['mean'])}   P50 {money(sim['p50'])}   P80 {money(sim['p80'])}   "
        f"P90 {money(sim['p90'])}   P95 {money(sim['p95'])}   max {money(sim['max'])}",
        f"  reserve for 80% confidence = {money(sim['p80'])}; for 90% confidence = {money(sim['p90'])}",
    ]
    if sim["reserve"] is not None:
        lines.append(
            f"  reserve {money(sim['reserve'])}: P(total > reserve) = {fmt_pct(sim['p_exceed_reserve'])}  "
            f"(covered in {fmt_pct(1 - sim['p_exceed_reserve'])} of trials)"
        )
    if sim["histogram"]:
        lines.append("  distribution of total exposure (share of trials):")
        for b in sim["histogram"]:
            bar = "#" * int(round(40 * b["share"]))
            lines.append(f"  {money(b['from']):>14} - {money(b['to']):>14} | {bar:<40} {fmt_pct(b['share']):>6}")
    else:
        lines.append("  every trial totalled 0.00 (no threats, or all probabilities are 0)")
    return lines


def check_lines(check):
    if check["passed"]:
        return ["Check: PASS - every HIGH/MEDIUM risk has an owner, a response and a trigger; "
                "ids are unique; no certain (100%) or impossible (0) risks."]
    lines = [f"Check: FAIL - {len(check['problems'])} problem(s):"]
    lines += [f"  - {p}" for p in check["problems"]]
    return lines


def render_table(shown, summary, sim, check, args, grid):
    cols = table_columns(shown, args, grid)
    rows = [table_cells(r, cols, grid) for r in shown]
    widths = [max(display_width(name), *(display_width(row[c]) for row in rows)) for c, (name, _) in enumerate(cols)]

    def line(cells):
        return "  ".join(pad(cell, widths[i], right=cols[i][1]) for i, cell in enumerate(cells)).rstrip()

    out = [line([name for name, _ in cols]), line(["-" * w for w in widths])]
    out += [line(r) for r in rows]
    out.append("")
    out += summary_lines(summary, grid)
    if sim:
        out.append("")
        out += simulation_lines(sim)
    if check is not None:
        out.append("")
        out += check_lines(check)
    return "\n".join(out)


def render_md(shown, summary, sim, check, args, grid):
    cols = table_columns(shown, args, grid)
    out = ["| " + " | ".join(name for name, _ in cols) + " |",
           "|" + "|".join(("---:" if right else "---") for _, right in cols) + "|"]
    for r in shown:
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in table_cells(r, cols, grid)) + " |")
    out.append("")
    out += [f"- {ln}" for ln in summary_lines(summary, grid)]
    if sim:
        out.append("")
        out.append("```")
        out += simulation_lines(sim)
        out.append("```")
    if check is not None:
        out.append("")
        out += [f"- {ln.strip()}" for ln in check_lines(check)]
    return "\n".join(out)


def render_json(shown, summary, sim, check):
    keys = ("rank", "id", "description", "type", "category", "probability", "impact", "exposure", "signed_emv",
            "severity", "residual_probability", "residual_impact", "residual_exposure", "impact_min", "impact_max",
            "owner", "response", "trigger", "status", "closed", "raised", "review_date")
    risks = [{k: r[k] for k in keys} for r in shown]
    payload = {"risks": risks, "summary": summary}
    if sim:
        payload["simulation"] = sim
    if check is not None:
        payload["check"] = check
    return json.dumps(payload, indent=2, ensure_ascii=False)


def render_csv(shown, headers):
    present = {canon(h): h for h in headers if h}
    fieldnames = [h for h in headers if h] + [c for c in COMPUTED_COLUMNS if c not in present]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for r in shown:
        row = {k: ("" if v is None else v) for k, v in r["original"].items() if k in fieldnames}
        computed = {
            "rank": r["rank"],
            "exposure": f"{r['exposure']:.2f}",
            "severity": r["severity"],
            "residual_exposure": f"{r['residual_exposure']:.2f}" if r["residual_exposure"] is not None else "",
            "signed_emv": f"{r['signed_emv']:.2f}",
        }
        for c, v in computed.items():
            row[present.get(c, c)] = v
        writer.writerow(row)
    return buf.getvalue().rstrip("\n")


# --------------------------------------------------------------------------- CLI
def build_parser():
    parser = argparse.ArgumentParser(
        description="Score a risk register: exposure (probability x impact = EMV), severity bands, residual "
                    "exposure, Monte Carlo of total threat exposure, governance checks.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("\n", 4)[4],
    )
    parser.add_argument("path", help="CSV or JSON risk register, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="parse the input as JSON (default: CSV)")
    parser.add_argument("--prob-scale", choices=["auto", "fraction", "percent", "1-5"], default="auto",
                        help="how to read the probability column (default auto: inferred once per register)")
    parser.add_argument("--impact-scale", choices=["units", "1-5"], default="units",
                        help="impact in consistent units (default) or 1-5 scores (requires --prob-scale 1-5)")
    parser.add_argument("--high", type=float, default=None, metavar="X",
                        help="HIGH band threshold on exposure (default 25,000 for units; 15 on the 1-5 grid)")
    parser.add_argument("--medium", type=float, default=None, metavar="X",
                        help="MEDIUM band threshold on exposure (default 5,000 for units; 8 on the 1-5 grid)")
    parser.add_argument("--bac", type=float, default=None, metavar="B",
                        help="budget at completion: sets HIGH >= 5%% and MEDIUM >= 1%% of B (units only)")
    parser.add_argument("--basis", choices=["inherent", "residual"], default="inherent",
                        help="band, rank and simulate on inherent (default) or residual (post-response) exposure")
    parser.add_argument("--include-closed", action="store_true",
                        help="also score rows whose status is closed/occurred/retired/realised")
    parser.add_argument("--top", type=int, default=None, metavar="N", help="show only the N highest exposures")
    parser.add_argument("--format", choices=["table", "json", "csv", "md"], default="table",
                        help="output format (default table); csv = input columns + rank/exposure/severity/...")
    parser.add_argument("--simulate", type=int, default=0, metavar="N",
                        help=f"run N Monte Carlo trials of total threat exposure (>= {MIN_TRIALS}; e.g. 10000)")
    parser.add_argument("--seed", type=int, default=None, metavar="K",
                        help="random seed for --simulate (a random seed is drawn and printed when omitted)")
    parser.add_argument("--reserve", type=float, default=None, metavar="X",
                        help="contingency reserve to test with --simulate: reports P(total > X)")
    parser.add_argument("--check", action="store_true",
                        help="governance check: owners/responses/triggers on HIGH+MEDIUM, unique ids, p=0 or "
                             "p=100%%, residual > inherent; exit 1 when any problem is found")
    return parser


def validate_options(parser, args):
    grid = args.prob_scale == "1-5"
    if grid != (args.impact_scale == "1-5"):
        parser.error("--prob-scale 1-5 and --impact-scale 1-5 must be used together (P x I grid); pass both or neither")
    for name in ("high", "medium", "bac", "reserve"):
        v = getattr(args, name)
        if v is not None and not math.isfinite(v):
            parser.error(f"--{name} must be a finite number")
    if args.high is not None and args.high < 0:
        parser.error("--high must be >= 0")
    if args.medium is not None and args.medium < 0:
        parser.error("--medium must be >= 0")
    if args.bac is not None and args.bac <= 0:
        parser.error("--bac must be > 0")
    if args.top is not None and args.top < 1:
        parser.error("--top must be >= 1")
    if args.simulate < 0 or (0 < args.simulate < MIN_TRIALS) or args.simulate > MAX_TRIALS:
        parser.error(f"--simulate must be between {MIN_TRIALS} and {MAX_TRIALS:,} trials (0 = off)")
    if args.simulate and grid:
        parser.error("--simulate needs impacts in units (money, days); it has no meaning on the 1-5 grid")
    if args.seed is not None and not args.simulate:
        parser.error("--seed requires --simulate")
    if args.reserve is not None:
        if not args.simulate:
            parser.error("--reserve requires --simulate")
        if args.reserve < 0:
            parser.error("--reserve must be >= 0")
    return grid


def resolve_bands(parser, args, grid):
    """Return (high, medium, source description)."""
    if grid:
        if args.bac is not None:
            parser.error("--bac applies to unit impacts only, not to the 1-5 grid")
        high = args.high if args.high is not None else GRID_HIGH
        medium = args.medium if args.medium is not None else GRID_MEDIUM
        source = "1-25 P x I grid defaults" if args.high is None and args.medium is None else "explicit --high/--medium"
    elif args.bac is not None:
        if args.high is not None or args.medium is not None:
            parser.error("pass either --bac or --high/--medium, not both")
        high, medium = BAC_HIGH_PCT * args.bac, BAC_MEDIUM_PCT * args.bac
        source = f"5% / 1% of --bac {money(args.bac)}"
    else:
        high = args.high if args.high is not None else DEFAULT_HIGH
        medium = args.medium if args.medium is not None else DEFAULT_MEDIUM
        source = "explicit --high/--medium"
        if args.high is None and args.medium is None:
            source = "defaults = 5% / 1% of the sample Helios BAC of 500,000; pass --bac or --high/--medium"
        elif args.medium is None:
            source = f"explicit --high, --medium at its default {money(DEFAULT_MEDIUM)}"
            if high <= DEFAULT_MEDIUM:
                medium = high / 5.0
                note(f"--medium not given and its default {money(DEFAULT_MEDIUM)} is not below --high; using --medium {money(medium)} (high / 5)")
                source = "explicit --high, --medium derived as high / 5"
        elif args.high is None:
            source = f"explicit --medium, --high at its default {money(DEFAULT_HIGH)}"
            if medium >= DEFAULT_HIGH:
                high = medium * 5.0
                note(f"--high not given and its default {money(DEFAULT_HIGH)} is not above --medium; using --high {money(high)} (medium x 5)")
                source = "explicit --medium, --high derived as medium x 5"
    if medium > high:
        given = []
        if args.high is None:
            given.append(f"--high defaulted to {money(high)}")
        if args.medium is None:
            given.append(f"--medium defaulted to {money(medium)}")
        hint = f" ({'; '.join(given)}; pass both flags)" if given else ""
        parser.error(f"--medium ({money(medium)}) must be <= --high ({money(high)}){hint}")
    return high, medium, source


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    grid = validate_options(parser, args)
    high, medium, band_source = resolve_bands(parser, args, grid)
    try:
        text = read_text(args.path)
        rows, headers = load_rows(text, args.json, JSON_KEY)
        parsed = parse_register(rows, headers, args.impact_scale)
        cells = [r["p_cell"] for r in parsed] + [r["rp_cell"] for r in parsed if r["rp_cell"] is not None]
        scale = infer_prob_scale(cells, args.prob_scale)
        if args.prob_scale == "auto" and scale == "percent" and any(not c["pct"] for c in cells):
            note("probabilities interpreted as percents (0-100) for the whole register; pass --prob-scale to override")
        scored = score(parsed, scale, args.basis, high, medium)
        active = [r for r in scored if args.include_closed or not r["closed"]]
        if not active:
            raise ValueError(
                f"all {len(scored)} risk(s) are closed/occurred/retired/realised; pass --include-closed to score them"
            )
        if args.basis == "residual" and not any(r["residual_exposure"] is not None for r in active):
            warn("--basis residual given but no residual_probability/residual_impact values found; using inherent values")
        if (not grid and args.high is None and args.medium is None and args.bac is None
                and max(r["impact"] for r in active) < 100):
            warn(
                f"largest impact is {fmt_num(max(r['impact'] for r in active))} but the severity bands are at the "
                f"money defaults ({money(high)} / {money(medium)}); pass --impact-scale 1-5 (with --prob-scale 1-5), "
                "--bac or --high/--medium"
            )
        shown = active[: args.top] if args.top else active
        summary = summarize(active, scored, shown, args, scale, high, medium, band_source, grid)
        sim = None
        if args.simulate:
            seed = args.seed if args.seed is not None else random.randrange(2**31)
            if args.seed is None:
                note(f"no --seed given; using seed {seed} (pass --seed {seed} to reproduce)")
            sim = simulate(active, args.simulate, seed, args.reserve, args.basis)
        check = run_checks(active, scored, grid) if args.check else None
        if args.format == "json":
            output = render_json(shown, summary, sim, check)
        elif args.format == "csv":
            output = render_csv(shown, headers)
            for ln in (simulation_lines(sim) if sim else []) + (check_lines(check) if check is not None else []):
                print(ln, file=sys.stderr)
        elif args.format == "md":
            output = render_md(shown, summary, sim, check, args, grid)
        else:
            output = render_table(shown, summary, sim, check, args, grid)
    except (OSError, ValueError, TypeError, UnicodeDecodeError, OverflowError, ZeroDivisionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(output)
    return 1 if (check is not None and not check["passed"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
