#!/usr/bin/env python3
"""Lint the project-management Agent Skills catalog.

Read-only checker for the conventions in README.md. Standard library only.

Checks per skill (.claude/skills/<name>/SKILL.md):
  1. Folder name == frontmatter `name`.
  2. `name` is kebab-case, <=64 chars, no reserved words ("claude"/"anthropic").
  3. `description` present, <=1024 chars, third-person-ish, contains a "use when" cue.
  4. `metadata.related` entries all resolve to existing skills AND are reciprocal.
  5. SKILL.md body (after frontmatter) < 500 lines.
  6. Every references/ assets/ scripts/ path named in the body exists (no dead links),
     and every file in those folders is mentioned in the body (orphan -> warning).

Usage:
    python tools/lint_skills.py            # lint .claude/skills relative to repo root
    python tools/lint_skills.py PATH       # lint a specific skills directory
Exit code is non-zero if any errors (not warnings) are found.
"""
from __future__ import annotations

import os
import re
import sys

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED = ("claude", "anthropic")
FILE_REF_RE = re.compile(r"(references|assets|scripts)/([A-Za-z0-9_\-./]+)")


def split_frontmatter(text: str):
    """Return (frontmatter_lines, body_lines). Frontmatter is between the first two '---'."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], lines
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], lines[i + 1 :]
    return [], lines


def parse_frontmatter(fm_lines):
    """Minimal parser for our known frontmatter shape."""
    data = {"name": None, "description": None, "category": None, "phase": None, "related": []}
    i = 0
    n = len(fm_lines)
    while i < n:
        line = fm_lines[i]
        if re.match(r"^name:", line):
            data["name"] = line.split(":", 1)[1].strip().strip("\"'")
            i += 1
        elif re.match(r"^description:", line):
            rest = line.split(":", 1)[1].strip()
            if rest and rest[0] not in (">", "|"):
                data["description"] = rest.strip().strip("\"'")
                i += 1
            else:
                # block scalar: collect indented continuation lines
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
                if sub.startswith("related:"):
                    inside = sub.split(":", 1)[1].strip().strip("[]")
                    data["related"] = [x.strip().strip("\"'") for x in inside.split(",") if x.strip()]
                elif sub.startswith("category:"):
                    data["category"] = sub.split(":", 1)[1].strip()
                elif sub.startswith("phase:"):
                    data["phase"] = sub.split(":", 1)[1].strip()
                i += 1
        else:
            i += 1
    return data


def lint(skills_dir: str):
    errors, warnings = [], []
    if not os.path.isdir(skills_dir):
        print(f"error: skills directory not found: {skills_dir}", file=sys.stderr)
        return 2

    skills = sorted(
        d for d in os.listdir(skills_dir)
        if os.path.isfile(os.path.join(skills_dir, d, "SKILL.md"))
    )
    parsed = {}
    for name in skills:
        path = os.path.join(skills_dir, name, "SKILL.md")
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        fm_lines, body_lines = split_frontmatter(text)
        fm = parse_frontmatter(fm_lines)
        parsed[name] = (fm, body_lines, os.path.join(skills_dir, name))

    known = set(parsed)
    for name, (fm, body_lines, folder) in parsed.items():
        tag = f"[{name}]"
        # 1. folder == name
        if fm["name"] != name:
            errors.append(f"{tag} frontmatter name '{fm['name']}' != folder name '{name}'")
        # 2. name validity
        nm = fm["name"] or ""
        if not NAME_RE.match(nm):
            errors.append(f"{tag} name '{nm}' is not valid kebab-case")
        if len(nm) > 64:
            errors.append(f"{tag} name exceeds 64 chars")
        if any(w in nm for w in RESERVED):
            errors.append(f"{tag} name contains a reserved word")
        # 3. description
        desc = fm["description"] or ""
        if not desc:
            errors.append(f"{tag} missing description")
        else:
            if len(desc) > 1024:
                errors.append(f"{tag} description exceeds 1024 chars ({len(desc)})")
            if len(desc) < 40:
                warnings.append(f"{tag} description looks short ({len(desc)} chars)")
            if "use when" not in desc.lower():
                warnings.append(f"{tag} description has no 'use when' cue")
            # Ignore quoted user trigger phrases (e.g. "where do I start") before the
            # first/second-person check, so they don't cause false positives.
            desc_unquoted = re.sub(r'"[^"]*"', "", desc)
            if re.search(r"\b(I am|I can|I will|I'|you can|you should|you will)\b", desc_unquoted):
                warnings.append(f"{tag} description may not be third person")
        # 4. related reciprocity
        for rel in fm["related"]:
            if rel not in known:
                errors.append(f"{tag} related '{rel}' does not resolve to a skill")
            elif name not in parsed[rel][0]["related"]:
                errors.append(f"{tag} related '{rel}' is not reciprocal ({rel} does not list {name})")
        # 5. body length
        if len(body_lines) >= 500:
            errors.append(f"{tag} body is {len(body_lines)} lines (>= 500)")
        # 6. file references
        body_text = "\n".join(body_lines)
        for sub, rel in FILE_REF_RE.findall(body_text):
            ref_path = os.path.join(folder, sub, os.path.basename(rel))
            if not os.path.exists(os.path.join(folder, sub, rel)) and not os.path.exists(ref_path):
                errors.append(f"{tag} body references missing file '{sub}/{rel}'")
        for sub in ("references", "assets", "scripts"):
            subdir = os.path.join(folder, sub)
            if os.path.isdir(subdir):
                for fname in sorted(os.listdir(subdir)):
                    if fname.startswith("."):
                        continue
                    if fname not in body_text:
                        warnings.append(f"{tag} file '{sub}/{fname}' is never mentioned in SKILL.md")

    print(f"Linted {len(parsed)} skills in {skills_dir}")
    for w in warnings:
        print(f"  warning: {w}")
    for e in errors:
        print(f"  ERROR:   {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(".claude", "skills")
    raise SystemExit(lint(target))
