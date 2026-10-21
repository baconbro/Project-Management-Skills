#!/usr/bin/env python3
"""Lint the project-management Agent Skills catalog.

Read-only checker for the conventions in README.md. Standard library only
(uses PyYAML for strict frontmatter parsing when it is installed, otherwise a
built-in minimal parser).

Checks per skill (.claude/skills/<name>/SKILL.md):
  1. Frontmatter parses; folder name == `name`; name is kebab-case, <= 64 chars,
     without the reserved words "claude"/"anthropic".
  2. `description` present, <= 1024 chars, no XML angle brackets, third person,
     contains a "use when" cue.
  3. `metadata.version` is semver; `category` and `phase` use the allowed values.
  4. `metadata.related` entries resolve to existing skills AND are reciprocal; the
     "## Related skills" bullets name exactly the same skills in the same order.
  5. Body < 500 lines and contains the canonical sections in order.
  6. No placeholder text (TODO/TBD/FIXME/lorem) in SKILL.md.
  7. Every references/ assets/ scripts/ path named in the body exists (own folder, or
     another skill's folder when written as .claude/skills/<other>/...), and every
     file in those folders is mentioned in the body (orphan -> warning).
  8. Every helper script under scripts/ runs with --help (exit 0).

Usage:
    python tools/lint_skills.py            # lint .claude/skills relative to cwd
    python tools/lint_skills.py PATH       # lint a specific skills directory
    python tools/lint_skills.py --no-exec  # skip running scripts with --help
Exit code is non-zero if any errors (not warnings) are found.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
RESERVED = ("claude", "anthropic")
CATEGORIES = {"orchestrator", "phase", "discipline", "artifact"}
PHASES = {"initiation", "planning", "delivery", "closure", "cross-cutting"}
SECTIONS = [
    "Overview", "When to use this skill", "Methodology fit", "Inputs you need", "Workflow",
    "Quality checklist", "Anti-patterns", "Resources", "Related skills",
]
FILE_REF_RE = re.compile(r"(?:\.claude/skills/([a-z0-9-]+)/)?\b(references|assets|scripts)/([A-Za-z0-9_\-./]+)")
PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME|lorem ipsum)\b", re.I)
BULLET_SKILL_RE = re.compile(r"^\s*[-*]\s+`([a-z0-9-]+)`")

try:  # optional strict YAML parsing
    import yaml  # type: ignore
except Exception:  # pragma: no cover - PyYAML is optional
    yaml = None


def split_frontmatter(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, lines
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], lines[i + 1:]
    return None, lines


def parse_frontmatter_minimal(fm_lines):
    """Minimal parser for the catalog's frontmatter shape (fallback when PyYAML is absent)."""
    data = {"name": None, "description": None, "metadata": {}, "license": None}
    i, n = 0, len(fm_lines)
    while i < n:
        line = fm_lines[i]
        if re.match(r"^name:", line):
            data["name"] = line.split(":", 1)[1].strip().strip("\"'")
            i += 1
        elif re.match(r"^license:", line):
            data["license"] = line.split(":", 1)[1].strip()
            i += 1
        elif re.match(r"^description:", line):
            rest = line.split(":", 1)[1].strip()
            if rest and rest[0] not in (">", "|"):
                data["description"] = rest.strip("\"'")
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
        return {
            "name": None if loaded.get("name") is None else str(loaded.get("name")),
            "description": None if loaded.get("description") is None else " ".join(str(loaded["description"]).split()),
            "metadata": {k: (str(v) if not isinstance(v, list) else v) for k, v in md.items()},
            "license": loaded.get("license"),
        }
    data = parse_frontmatter_minimal(fm_lines)
    data["metadata"].setdefault("related", [])
    return data


def body_sections(body_lines):
    return [ln[3:].strip() for ln in body_lines if ln.startswith("## ")]


def related_bullets(body_lines):
    names, inside = [], False
    for ln in body_lines:
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
    parsed = {}
    for name in skills:
        path = os.path.join(skills_dir, name, "SKILL.md")
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        fm_lines, body_lines = split_frontmatter(text)
        if fm_lines is None:
            errors.append(f"[{name}] SKILL.md has no frontmatter block")
            parsed[name] = ({"name": None, "description": None, "metadata": {"related": []}}, body_lines)
            continue
        try:
            fm = parse_frontmatter(fm_lines)
        except Exception as exc:  # invalid YAML
            errors.append(f"[{name}] frontmatter does not parse: {exc}")
            fm = {"name": None, "description": None, "metadata": {"related": []}}
        parsed[name] = (fm, body_lines)

    known = set(parsed)
    for name, (fm, body_lines) in parsed.items():
        tag = f"[{name}]"
        folder = os.path.join(skills_dir, name)
        md = fm.get("metadata") or {}
        related = list(md.get("related") or [])
        # 1. name
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
            if rel not in known:
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
                        if fname not in body_text:
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

    print(f"Linted {len(parsed)} skills in {skills_dir}" + ("" if yaml else " (PyYAML not installed: using minimal frontmatter parser)"))
    for w in warnings:
        print(f"  warning: {w}")
    for e in errors:
        print(f"  ERROR:   {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    run_scripts = "--no-exec" not in sys.argv
    target = args[0] if args else os.path.join(".claude", "skills")
    raise SystemExit(lint(target, run_scripts))
