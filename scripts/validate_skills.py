#!/usr/bin/env python3
"""Offline static package validation for Career Skills (not a behavioral evaluator)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED = {
    "setup-career-skills", "reflect", "maintain-profile", "build-resume",
    "personal-brand", "define-design-brief", "create-design-assets", "review-design", "audit-surface", "audit", "find-jobs",
}


def main() -> int:
    errors: list[str] = []
    packages = {p.parent.name: p for p in SKILLS.rglob("SKILL.md")}
    actual = set(packages)
    if actual != EXPECTED:
        errors.append(f"Skill inventory mismatch; missing={sorted(EXPECTED-actual)}, extra={sorted(actual-EXPECTED)}")
    for name in sorted(EXPECTED):
        path = packages.get(name, SKILLS / name / "SKILL.md")
        if not path.is_file():
            errors.append(f"Missing {path.relative_to(ROOT)}")
            continue
        contents = path.read_text(encoding="utf-8")
        if not contents.startswith("---\n"):
            errors.append(f"{name}: missing opening YAML frontmatter")
            continue
        pieces = contents.split("---\n", 2)
        if len(pieces) < 3:
            errors.append(f"{name}: missing closing YAML frontmatter")
            continue
        head, body = pieces[1], pieces[2]
        match_name = re.search(r"^name:\s*(\S+)\s*$", head, flags=re.MULTILINE)
        match_description = re.search(r"^description:\s*(.+)$", head, flags=re.MULTILINE)
        if not match_name or match_name.group(1) != name:
            errors.append(f"{name}: invalid frontmatter name")
        if not match_description or not match_description.group(1).strip():
            errors.append(f"{name}: empty frontmatter description")
        if len(body.strip()) < 250:
            errors.append(f"{name}: unexpectedly short skill body")
        if "## Done when" not in body:
            errors.append(f"{name}: missing observable completion criteria")
    data = json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))
    covered = {case["skill"] for case in data["cases"]}
    if covered != EXPECTED:
        errors.append(f"Behavioral case coverage mismatch: {sorted(EXPECTED-covered)}")
    for case in data["cases"]:
        if not case.get("prompt") or not case.get("expect"):
            errors.append(f"Invalid test case: {case.get('id')}")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Validated {len(EXPECTED)} skill packages and {len(data['cases'])} documented behavioral cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

