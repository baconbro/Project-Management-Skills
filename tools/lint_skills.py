#!/usr/bin/env python3
"""Lint the project-management Agent Skills catalog.

Read-only checker for the conventions in README.md. Standard library only
(uses PyYAML for strict frontmatter parsing when it is installed, otherwise a
built-in minimal parser).

Checks per skill (.claude/skills/<name>/SKILL.md):
  0. Every folder under the skills directory has a SKILL.md (a case variant such as
     skill.md is an error: the skill would not load).
  1. Frontmatter parses (without PyYAML, a plain one-line name/description holding ": " or
     " #" is rejected, as YAML would reject it); only the keys name, description, license,
     compatibility, metadata and allowed-tools are allowed; license is MIT; allowed-tools is
     a string or a list of strings; folder name == `name`; name is kebab-case, <= 64 chars,
     without the reserved words "claude"/"anthropic".
  2. `description` present, <= 1024 chars, no XML angle brackets, third person,
     contains a "use when" cue; warns above 350 chars per skill or 8,000 for the
     whole catalog (Claude Code's skill-listing budget).
  3. `metadata.version` is semver; `category` and `phase` use the allowed values.
  4. `metadata.related` entries resolve to existing skills (never the skill itself) AND are
     reciprocal; the "## Related skills" bullets name exactly the same skills in the same order.
  5. Body < 500 lines and contains the canonical sections in order (headings inside code
     fences do not count); every numbered Workflow step ends with a "*Done: ...*" line.
  6. No placeholder text (TODO/TBD/FIXME/lorem) in SKILL.md.
  7. Every references/ assets/ scripts/ path named in the body exists (own folder, or
     another skill's folder when written as .claude/skills/<other>/...), and every
     file in those folders is mentioned in the body (orphan -> warning).
  8. Every helper script under scripts/ runs with --help (exit 0).
  9. Every Markdown file under references/ and assets/ (and the repo README.md) only
     points at files that exist: `.claude/skills/<s>/...` and README `$S/<s>/...` paths
     must resolve in the named skill; an unqualified references/ assets/ scripts/ path in a
     skill's own Markdown must resolve in THAT skill (README: in any skill); and a bare
     `file.csv`-style name in backticks must exist somewhere in the catalog (catches stale
     pointers after a file is renamed or removed).
 10. The README catalog matches the frontmatter: the "**N Agent Skills**" count, and one
     table row per skill whose tier (0 orchestrator, 1 phase, 2 discipline, 3 artifact)
     and phase agree with metadata.category and metadata.phase.

Usage:
    python tools/lint_skills.py            # lint .claude/skills relative to cwd
    python tools/lint_skills.py PATH       # lint a specific skills directory
    python tools/lint_skills.py --no-exec  # skip running scripts with --help
Exit code is non-zero if any errors (not warnings) are found; 2 if PATH is not a directory.
Install PyYAML (python -m pip install pyyaml) for the strict frontmatter parsing CI uses.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
RESERVED = ("claude", "anthropic")
# Claude Code lists every skill's name but fits descriptions into a budget of about 1% of
# the context window (8,000-character fallback) and drops the least-used ones first. Keep
# each description short and the whole catalog under the fallback so all 27 stay visible.
DESC_SOFT_MAX = 350
CATALOG_DESC_BUDGET = 8000
CATEGORIES = {"orchestrator", "phase", "discipline", "artifact"}
PHASES = {"initiation", "planning", "delivery", "closure", "cross-cutting"}
SECTIONS = [
    "Overview", "When to use this skill", "Methodology fit", "Inputs you need", "Workflow",
    "Quality checklist", "Anti-patterns", "Resources", "Related skills",
]
FILE_REF_RE = re.compile(r"(?:\.claude/skills/([a-z0-9-]+)/)?\b(references|assets|scripts)/([A-Za-z0-9_\-./]+)")
PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME|lorem ipsum)\b", re.I)
BULLET_SKILL_RE = re.compile(r"^\s*[-*]\s+`([a-z0-9-]+)`")
FULL_PATH_RE = re.compile(r"\.claude/skills/([a-z0-9-]+)(?:/([A-Za-z0-9_\-./]+))?")
BARE_FILE_RE = re.compile(r"`([A-Za-z0-9_\-.]+\.(?:md|csv|py|json))`")
# illustrative names used in examples, not files the catalog ships: exact generic names
# (out.csv, data.json, report.md ...) or a my-/your-/new-/fixed-/old-/bad-/broken- prefix
ILLUSTRATIVE = re.compile(r"^(OUT|out|data|input|output|report|plan|register|results?|bad|broken)\.(csv|md|json)$"
                          r"|^(my|your|new|fixed|old|bad|broken)[-_]|^SKILL\.md$|^README\.md$")
ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
LICENSE = "MIT"
TIER_CATEGORY = {"0": "orchestrator", "1": "phase", "2": "discipline", "3": "artifact"}
README_ROW_RE = re.compile(r"^\| (\d) · \w+ \| `([a-z0-9-]+)` \| ([a-z-]+) \|", re.M)
README_COUNT_RE = re.compile(r"\*\*(\d+) Agent Skills\*\*")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
TOP_KEY_RE = re.compile(r"^([A-Za-z0-9_][A-Za-z0-9_-]*)\s*:")

try:  # optional strict YAML parsing
    import yaml  # type: ignore
except Exception:  # pragma: no cover - PyYAML is optional
    yaml = None


def read_utf8(path, errors, tag):
    """File text, or None after recording an error when it is not UTF-8."""
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except UnicodeDecodeError as exc:
        errors.append(f"{tag} is not UTF-8 (bad byte at offset {exc.start}); re-save it as UTF-8")
        return None


def split_frontmatter(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, lines
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], lines[i + 1:]
    return None, lines


def _plain_scalar(value, key):
    """A one-line YAML value: quoted strings are unquoted; a plain scalar holding ': ' or ' #' is
    rejected, because YAML (and so Claude Code) would not read it as one string."""
    if value[:1] in ("'", '"'):
        return value.strip("\"'")
    if ": " in value or " #" in value or value.endswith(":"):
        raise ValueError(f'plain-scalar {key} contains ": " or " #"; use >- or quotes')
    return value


def parse_frontmatter_minimal(fm_lines):
    """Minimal parser for the catalog's frontmatter shape (fallback when PyYAML is absent)."""
    data = {"name": None, "description": None, "metadata": {}, "license": None, "keys": set()}
    i, n = 0, len(fm_lines)
    while i < n:
        line = fm_lines[i]
        top = TOP_KEY_RE.match(line)
        if top:
            data["keys"].add(top.group(1))
        if re.match(r"^name:", line):
            data["name"] = _plain_scalar(line.split(":", 1)[1].strip(), "name")
            i += 1
        elif re.match(r"^license:", line):
            data["license"] = line.split(":", 1)[1].strip()
            i += 1
        elif re.match(r"^description:", line):
            rest = line.split(":", 1)[1].strip()
            if rest and rest[0] not in (">", "|"):
                data["description"] = _plain_scalar(rest, "description")
                i += 1
            else:
                i += 1
                chunk = []
                while i < n and (fm_lines[i].startswith(" ") or fm_lines[i].strip() == ""):
                    chunk.append(fm_lines[i].strip())
                    i += 1
                data["description"] = " ".join(c for c in chunk if c)
        elif re.match(r"^metadata:", line):
            i += 1
            while i < n and (fm_lines[i].startswith(" ") or fm_lines[i].strip() == ""):
                sub = fm_lines[i].strip()
                if ":" in sub:
                    k, v = sub.split(":", 1)
                    v = v.strip()
                    if k.strip() == "related":
                        v = [x.strip().strip("\"'") for x in v.strip("[]").split(",") if x.strip()]
                    data["metadata"][k.strip()] = v
                i += 1
        else:
            i += 1
    return data


def parse_frontmatter(fm_lines):
    text = "\n".join(fm_lines)
    if yaml is not None:
        loaded = yaml.safe_load(text)  # raises on invalid YAML
        if not isinstance(loaded, dict):
            raise ValueError("frontmatter is not a mapping")
        md = loaded.get("metadata") or {}
        if not isinstance(md, dict):
            raise ValueError("metadata is not a mapping")
        related = md.get("related") or []
        if isinstance(related, str):
            related = [x.strip() for x in related.strip("[]").split(",") if x.strip()]
        md["related"] = [str(x) for x in related]
        tools = loaded.get("allowed-tools")
        if tools is not None and not (isinstance(tools, str)
                                      or (isinstance(tools, list) and all(isinstance(t, str) for t in tools))):
            raise ValueError("allowed-tools must be a string or a list of strings")
        return {
            "name": None if loaded.get("name") is None else str(loaded.get("name")),
            "description": None if loaded.get("description") is None else " ".join(str(loaded["description"]).split()),
            "metadata": {k: (str(v) if not isinstance(v, list) else v) for k, v in md.items()},
            "license": loaded.get("license"),
            "keys": {str(k) for k in loaded},
        }
    data = parse_frontmatter_minimal(fm_lines)
    data["metadata"].setdefault("related", [])
    return data


def unfenced(lines):
    """The lines outside ``` / ~~~ code fences (a heading inside a fence is not a heading)."""
    out, inside = [], False
    for ln in lines:
        if FENCE_RE.match(ln):
            inside = not inside
            continue
        if not inside:
            out.append(ln)
    return out


def body_sections(body_lines):
    return [ln[3:].strip() for ln in unfenced(body_lines) if ln.startswith("## ")]


def section_text(body_lines, title):
    out, inside = [], False
    for ln in unfenced(body_lines):
        if ln.startswith("## "):
            inside = ln[3:].strip() == title
            continue
        if inside:
            out.append(ln)
    return "\n".join(out)


def related_bullets(body_lines):
    names, inside = [], False
    for ln in unfenced(body_lines):
        if ln.startswith("## "):
            inside = ln[3:].strip() == "Related skills"
            continue
        if inside:
            m = BULLET_SKILL_RE.match(ln)
            if m:
                names.append(m.group(1))
    return names


def lint(skills_dir: str, run_scripts: bool = True):
    errors, warnings = [], []
    if not os.path.isdir(skills_dir):
        print(f"error: skills directory not found: {skills_dir}", file=sys.stderr)
        return 2
    skills = sorted(d for d in os.listdir(skills_dir) if os.path.isfile(os.path.join(skills_dir, d, "SKILL.md")))
    # 0. folders that would not load as a skill
    for d in sorted(os.listdir(skills_dir)):
        full = os.path.join(skills_dir, d)
        if d in skills or d.startswith((".", "__")) or not os.path.isdir(full):
            continue
        variants = [f for f in os.listdir(full) if f.lower() == "skill.md"]
        if variants:
            errors.append(f"[{d}] no SKILL.md (found {variants[0]}): the skill will not load; rename it to SKILL.md")
        else:
            warnings.append(f"[{d}] folder has no SKILL.md and is not a skill")
    parsed = {}
    empty_fm = {"name": None, "description": None, "metadata": {"related": []}, "license": LICENSE, "keys": set()}
    for name in skills:
        path = os.path.join(skills_dir, name, "SKILL.md")
        text = read_utf8(path, errors, f"[{name}] SKILL.md")
        if text is None:
            parsed[name] = (dict(empty_fm), [])
            continue
        fm_lines, body_lines = split_frontmatter(text)
        if fm_lines is None:
            errors.append(f"[{name}] SKILL.md has no frontmatter block")
            parsed[name] = (dict(empty_fm), body_lines)
            continue
        try:
            fm = parse_frontmatter(fm_lines)
        except Exception as exc:  # invalid YAML
            errors.append(f"[{name}] frontmatter does not parse: {exc}")
            fm = dict(empty_fm)
        parsed[name] = (fm, body_lines)

    known = set(parsed)
    for name, (fm, body_lines) in parsed.items():
        tag = f"[{name}]"
        folder = os.path.join(skills_dir, name)
        md = fm.get("metadata") or {}
        related = list(md.get("related") or [])
        # 1. top-level keys, license, name
        unknown = sorted(set(fm.get("keys") or ()) - ALLOWED_KEYS)
        if unknown:
            errors.append(f"{tag} frontmatter key(s) {unknown} not allowed (allowed: {sorted(ALLOWED_KEYS)}); "
                          "claude.ai uploads and the Skills API reject them - put custom fields under metadata")
        if fm.get("license") != LICENSE:
            errors.append(f"{tag} license is {fm.get('license')!r}; the catalog convention is {LICENSE!r}")
        if fm["name"] != name:
            errors.append(f"{tag} frontmatter name '{fm['name']}' != folder name '{name}'")
        nm = fm["name"] or ""
        if not NAME_RE.match(nm):
            errors.append(f"{tag} name '{nm}' is not valid kebab-case")
        if len(nm) > 64:
            errors.append(f"{tag} name exceeds 64 chars")
        if any(w in nm for w in RESERVED):
            errors.append(f"{tag} name contains a reserved word")
        # 2. description
        desc = fm.get("description") or ""
        if not desc:
            errors.append(f"{tag} missing description")
        else:
            if len(desc) > 1024:
                errors.append(f"{tag} description exceeds 1024 chars ({len(desc)})")
            if "<" in desc or ">" in desc:
                errors.append(f"{tag} description contains XML angle brackets")
            if len(desc) < 40:
                warnings.append(f"{tag} description looks short ({len(desc)} chars)")
            if len(desc) > DESC_SOFT_MAX:
                warnings.append(f"{tag} description is {len(desc)} chars (> {DESC_SOFT_MAX}); long descriptions "
                                "eat the skill-listing budget and get dropped")
            if "use when" not in desc.lower():
                warnings.append(f"{tag} description has no 'use when' cue")
            unquoted = re.sub(r'"[^"]*"', "", desc)
            if re.search(r"\b(I am|I can|I will|I'|you can|you should|you will)\b", unquoted):
                warnings.append(f"{tag} description may not be third person")
        # 3. metadata values
        ver = str(md.get("version") or "")
        if not SEMVER_RE.match(ver):
            errors.append(f"{tag} metadata.version '{ver}' is not semver")
        if str(md.get("category")) not in CATEGORIES:
            errors.append(f"{tag} metadata.category '{md.get('category')}' not in {sorted(CATEGORIES)}")
        if str(md.get("phase")) not in PHASES:
            errors.append(f"{tag} metadata.phase '{md.get('phase')}' not in {sorted(PHASES)}")
        # 4. related reciprocity + bullets
        for rel in related:
            if rel == name:
                errors.append(f"{tag} lists itself in related")
            elif rel not in known:
                errors.append(f"{tag} related '{rel}' does not resolve to a skill")
            elif name not in (parsed[rel][0].get("metadata") or {}).get("related", []):
                errors.append(f"{tag} related '{rel}' is not reciprocal ({rel} does not list {name})")
        if rel_bullets := related_bullets(body_lines):
            if rel_bullets != related:
                errors.append(f"{tag} 'Related skills' bullets {rel_bullets} != metadata.related {related}")
        elif related:
            errors.append(f"{tag} 'Related skills' section has no skill bullets")
        # 5. body length + sections
        if len(body_lines) >= 500:
            errors.append(f"{tag} body is {len(body_lines)} lines (>= 500)")
        found = body_sections(body_lines)
        order = [s for s in found if s in SECTIONS]
        missing = [s for s in SECTIONS if s not in found]
        if missing:
            errors.append(f"{tag} missing canonical section(s): {missing}")
        elif order != SECTIONS:
            errors.append(f"{tag} canonical sections out of order: {order}")
        if "Workflow" in found:
            steps = [st for st in re.split(r"\n(?=\d+\. )", section_text(body_lines, "Workflow")) if re.match(r"\d+\. ", st)]
            if not steps:
                errors.append(f"{tag} Workflow has no numbered steps")
            for st in steps:
                if "*Done:" not in st:
                    errors.append(f"{tag} Workflow step {st.split('.', 1)[0]} does not end with a '*Done: ...*' line")
        # 6. placeholders
        body_text = "\n".join(body_lines)
        for m in PLACEHOLDER_RE.finditer(body_text):
            errors.append(f"{tag} placeholder text '{m.group(0)}' left in SKILL.md")
            break
        # 7. file references
        seen_refs = set()
        for other, sub, rel in FILE_REF_RE.findall(body_text):
            rel = rel.rstrip(".,;:)")
            key = (other, sub, rel)
            if key in seen_refs:
                continue
            seen_refs.add(key)
            base = os.path.join(skills_dir, other) if other else folder
            if not os.path.exists(os.path.join(base, sub, rel)):
                where = f".claude/skills/{other}/" if other else ""
                errors.append(f"{tag} body references missing file '{where}{sub}/{rel}'")
        for sub in ("references", "assets", "scripts"):
            subdir = os.path.join(folder, sub)
            if os.path.isdir(subdir):
                for dirpath, dirnames, filenames in os.walk(subdir):
                    dirnames[:] = [d for d in dirnames if not d.startswith((".", "__"))]
                    for fname in sorted(filenames):
                        if fname.startswith(".") or fname.endswith((".pyc",)):
                            continue
                        if not re.search(r"(?<![\w-])" + re.escape(fname), body_text):
                            relp = os.path.relpath(os.path.join(dirpath, fname), folder)
                            warnings.append(f"{tag} file '{relp}' is never mentioned in SKILL.md")
        if "glossary" not in body_text.lower():
            warnings.append(f"{tag} Resources has no pointer to the PM glossary")
        # 8. scripts run with --help
        scripts_dir = os.path.join(folder, "scripts")
        if run_scripts and os.path.isdir(scripts_dir):
            for fname in sorted(os.listdir(scripts_dir)):
                if fname.endswith(".py"):
                    try:
                        proc = subprocess.run([sys.executable, os.path.join(scripts_dir, fname), "--help"],
                                              capture_output=True, text=True, timeout=30)
                        if proc.returncode != 0:
                            errors.append(f"{tag} scripts/{fname} --help exited {proc.returncode}: {proc.stderr.strip()[:200]}")
                    except Exception as exc:  # pragma: no cover
                        errors.append(f"{tag} scripts/{fname} --help failed to run: {exc}")

    total_desc = sum(len(fm.get("description") or "") for fm, _ in parsed.values())
    if total_desc > CATALOG_DESC_BUDGET:
        warnings.append(f"[catalog] descriptions total {total_desc} chars (> {CATALOG_DESC_BUDGET}); Claude Code "
                        "may drop some from the skill listing")

    # 9. pointers inside supporting Markdown files and the repo README
    all_basenames = set()
    for dirpath, dirnames, filenames in os.walk(skills_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith((".", "__"))]
        all_basenames.update(filenames)
    docs = []
    for name in skills:
        for fname in set(BARE_FILE_RE.findall(FULL_PATH_RE.sub("", "\n".join(parsed[name][1])))):
            if fname not in all_basenames and not ILLUSTRATIVE.search(fname):
                errors.append(f"[{name}] SKILL.md names '{fname}', which exists nowhere in the catalog")
        for sub in ("references", "assets"):
            subdir = os.path.join(skills_dir, name, sub)
            for dirpath, dirnames, filenames in os.walk(subdir) if os.path.isdir(subdir) else []:
                docs += [(name, os.path.join(dirpath, f)) for f in sorted(filenames) if f.endswith(".md")]
    readme = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(skills_dir))), "README.md")
    if os.path.isfile(readme):
        docs.append((None, readme))
    for owner, doc in docs:
        shown = os.path.relpath(doc, os.path.join(skills_dir, owner)) if owner else "README.md"
        tag = f"[{owner}] {shown}" if owner else "[README.md]"
        text = read_utf8(doc, errors, tag)
        if text is None:
            continue
        if owner is None:  # README commands write $S for .claude/skills
            text = re.sub(r"\$\{?S\}?/", ".claude/skills/", text)
        seen = set()
        for other, rest in FULL_PATH_RE.findall(text):
            rest = rest.rstrip(".,;:)/")
            if (other, rest) in seen:
                continue
            seen.add((other, rest))
            target = os.path.join(skills_dir, other, rest) if rest else os.path.join(skills_dir, other)
            if not os.path.exists(target):
                errors.append(f"{tag} points at missing '.claude/skills/{other}{'/' + rest if rest else ''}'")
        stripped = FULL_PATH_RE.sub("", text)
        for _, sub, rel in FILE_REF_RE.findall(stripped):
            rel = rel.rstrip(".,;:)/")
            if not rel or "<" in rel or (sub, rel) in seen:
                continue
            seen.add((sub, rel))
            if owner:  # a skill's own Markdown points into that skill; write .claude/skills/<s>/... otherwise
                if not os.path.exists(os.path.join(skills_dir, owner, sub, rel)):
                    elsewhere = [s for s in skills if os.path.exists(os.path.join(skills_dir, s, sub, rel))]
                    hint = (f" (it exists in {elsewhere[0]}: write .claude/skills/{elsewhere[0]}/{sub}/{rel})"
                            if elsewhere else "")
                    errors.append(f"{tag} points at missing '{sub}/{rel}'{hint}")
            elif not any(os.path.exists(os.path.join(skills_dir, s, sub, rel)) for s in skills):
                errors.append(f"{tag} points at missing '{sub}/{rel}'")
        for fname in set(BARE_FILE_RE.findall(stripped)):
            if fname in all_basenames or ILLUSTRATIVE.search(fname):
                continue
            errors.append(f"{tag} names '{fname}', which exists nowhere in the catalog")

    # 10. README catalog vs frontmatter
    if os.path.isfile(readme):
        rtext = read_utf8(readme, [], "[README.md]") or ""
        rows = README_ROW_RE.findall(rtext)
        count = README_COUNT_RE.search(rtext)
        if count and int(count.group(1)) != len(skills):
            errors.append(f"[README.md] says **{count.group(1)} Agent Skills** but the catalog has {len(skills)}")
        if rows:
            listed = [r[1] for r in rows]
            dupes = sorted({n for n in listed if listed.count(n) > 1})
            if dupes:
                errors.append(f"[README.md] catalog table lists {dupes} more than once")
            if set(listed) != set(skills):
                missing, extra = sorted(set(skills) - set(listed)), sorted(set(listed) - set(skills))
                errors.append(f"[README.md] catalog table differs from the skill folders: missing {missing}, "
                              f"unknown {extra}")
            for tier, sname, phase in rows:
                if sname not in parsed:
                    continue
                md = parsed[sname][0].get("metadata") or {}
                if TIER_CATEGORY.get(tier) != str(md.get("category")):
                    errors.append(f"[README.md] row {sname}: tier {tier} ({TIER_CATEGORY.get(tier)}) != "
                                  f"metadata.category {md.get('category')!r}")
                if phase != str(md.get("phase")):
                    errors.append(f"[README.md] row {sname}: phase {phase!r} != metadata.phase {md.get('phase')!r}")

    print(f"Linted {len(parsed)} skills in {skills_dir}" + ("" if yaml else " (PyYAML not installed: using minimal frontmatter parser)"))
    for w in warnings:
        print(f"  warning: {w}")
    for e in errors:
        print(f"  ERROR:   {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="lint_skills.py",
                                     description="Lint the project-management Agent Skills catalog (read-only).")
    parser.add_argument("path", nargs="?", default=os.path.join(".claude", "skills"),
                        help="skills directory (default: .claude/skills relative to the current directory)")
    parser.add_argument("--no-exec", action="store_true", help="do not run every helper script with --help")
    args = parser.parse_args(argv)
    return lint(args.path, run_scripts=not args.no_exec)


if __name__ == "__main__":
    raise SystemExit(main())
