#!/usr/bin/env python3
"""Offline validation of skill packaging, invocation intent and scenario inventory."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED = {
    "setup-career-skills", "plan-development", "review-progress", "review-research",
    "reflect", "maintain-profile", "build-resume", "personal-brand", "benchmark-profile",
    "define-design-brief", "create-design-assets", "review-design", "audit-surface",
    "audit", "find-jobs", "find-companies", "validate-workspace",
}
MANUAL = {
    "setup-career-skills", "reflect", "review-research", "plan-development",
    "review-progress", "personal-brand", "benchmark-profile", "define-design-brief",
    "create-design-assets", "review-design", "audit",
}


def main() -> int:
    errors: list[str] = []
    files = list(SKILLS.rglob("SKILL.md"))
    packages = {p.parent.name: p for p in files}
    if len(packages) != len(files):
        errors.append("Duplicate leaf skill package names")
    actual = set(packages)
    if actual != EXPECTED:
        errors.append(f"Skill inventory mismatch: missing={sorted(EXPECTED-actual)}, extra={sorted(actual-EXPECTED)}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for name in sorted(EXPECTED):
        path = packages.get(name)
        if path is None:
            continue
        contents = path.read_text(encoding="utf-8")
        front = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", contents, flags=re.DOTALL)
        if not front:
            errors.append(f"{name}: invalid frontmatter boundaries")
            continue
        head, body = front.groups()
        declared = re.search(r"^name:\s*(\S+)\s*$", head, re.MULTILINE)
        description = re.search(r"^description:\s*(.+)$", head, re.MULTILINE)
        disable = re.search(r"^disable-model-invocation:\s*(\S+)\s*$", head, re.MULTILINE)
        if not declared or declared.group(1) != name:
            errors.append(f"{name}: frontmatter name mismatch")
        if not description or not 1 <= len(description.group(1).strip(" '\"")) <= 1024:
            errors.append(f"{name}: description must contain 1-1024 characters")
        if name in MANUAL and (not disable or disable.group(1) != "true"):
            errors.append(f"{name}: manual skill needs disable-model-invocation: true")
        if name not in MANUAL and disable is not None:
            errors.append(f"{name}: discoverable skill must omit the manual-only flag")
        if "## Contract" not in body or "## Done when" not in body:
            errors.append(f"{name}: missing contract or completion criteria")
        if len(body.strip()) < 250:
            errors.append(f"{name}: unexpectedly short skill body")
        for rel in re.findall(r"\]\((references/[^)#]+)", body):
            if not (path.parent / rel).is_file():
                errors.append(f"{name}: broken bundled reference {rel}")
        match = re.search(r"^\| \[" + re.escape(chr(96) + name + chr(96)) + r"\].* \| (Manual|Discoverable) \|$", readme, re.MULTILINE)
        if not match or (match.group(1) == "Manual") != (name in MANUAL):
            errors.append(f"{name}: README invocation policy mismatch")

    cases = json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))["cases"]
    covered = {case["skill"] for case in cases}
    if covered != EXPECTED:
        errors.append(f"Behavioral coverage mismatch: {sorted(EXPECTED-covered)}")
    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate behavioral case IDs")
    for case in cases:
        if not case.get("prompt") or not case.get("expect"):
            errors.append(f"Invalid case: {case.get('id')}")
    smoke = json.loads((ROOT / "tests" / "eval-smoke.json").read_text(encoding="utf-8"))
    known = {case["id"]: case for case in cases}
    seen: set[str] = set()
    for item in smoke["existing_cases"]:
        case_id, mode = item["id"], item["mode"]
        if case_id not in known or case_id in seen:
            errors.append(f"Unknown or duplicated smoke case: {case_id}")
        elif mode == "discovery" and known[case_id]["skill"] in MANUAL:
            errors.append(f"{case_id}: manual skill cannot be a discovery case")
        elif mode not in {"discovery", "explicit"}:
            errors.append(f"{case_id}: unrecognized invocation mode")
        seen.add(case_id)
    for item in smoke["negative_cases"]:
        if item["id"] in seen or item.get("skill") is not None or not item.get("expect"):
            errors.append(f"Invalid negative case: {item['id']}")
        if item.get("mode") != "discovery" or not item.get("prompt"):
            errors.append(f"Invalid negative discovery case: {item['id']}")
        seen.add(item["id"])
    if not (ROOT / "AGENTS.md").is_file() or not (ROOT / "docs" / "EVALUATION.md").is_file():
        errors.append("Missing agent guidance or evaluation documentation")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Validated {len(EXPECTED)} packages, {len(cases)} documented cases and {len(seen)} live-agent smoke cases.")
    print("Structural checks do not establish actual agent behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
