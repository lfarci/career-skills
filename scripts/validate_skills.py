#!/usr/bin/env python3
"""Offline validation of skill packaging, invocation intent and scenario inventory."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED = {
    "setup-career-skills", "plan-development", "review-progress", "review-research",
    "reflect", "maintain-profile", "build-resume", "personal-brand", "benchmark-profile",
    "define-design-brief", "create-design-assets", "review-design",
    "audit", "find-jobs", "find-companies", "validate-workspace", "ask-career-skills",
}
MANUAL = {
    "reflect", "review-research", "plan-development",
    "review-progress", "personal-brand", "benchmark-profile", "define-design-brief",
    "create-design-assets", "review-design", "ask-career-skills",
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
        try:
            metadata = yaml.safe_load(head)
        except yaml.YAMLError as exc:
            errors.append(f"{name}: invalid YAML frontmatter: {exc}")
            continue
        if not isinstance(metadata, dict):
            errors.append(f"{name}: YAML frontmatter must be a mapping")
            continue
        if metadata.get("name") != name:
            errors.append(f"{name}: frontmatter name mismatch")
        description = metadata.get("description")
        if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
            errors.append(f"{name}: description must be a string of 1-1024 characters")
        if name in MANUAL and metadata.get("disable-model-invocation") is not True:
            errors.append(f"{name}: manual skill needs disable-model-invocation: true")
        if name not in MANUAL and "disable-model-invocation" in metadata:
            errors.append(f"{name}: discoverable skill must omit the manual-only flag")
        oa = path.parent / "agents" / "openai.yaml"
        implicit = (yaml.safe_load(oa.read_text(encoding="utf-8")) or {}).get("policy", {}).get("allow_implicit_invocation") if oa.is_file() else None
        if name in MANUAL and implicit is not False:
            errors.append(f"{name}: manual skill needs agents/openai.yaml with policy.allow_implicit_invocation: false")
        if name not in MANUAL and implicit is False:
            errors.append(f"{name}: discoverable skill must not disable implicit invocation in openai.yaml")
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
    workspace = ROOT / "docs" / "WORKSPACE.md"
    if not workspace.is_file() or any(
        heading not in workspace.read_text(encoding="utf-8")
        for heading in ("## Standard managed layout", "## Initialize from existing sources", "## Adopt and migrate an existing career tree")
    ):
        errors.append("Missing standardized workspace initialization and adoption guidance")
    journey = ROOT / "docs" / "USER-JOURNEY.md"
    if not journey.is_file() or "```mermaid" not in journey.read_text(encoding="utf-8"):
        errors.append("Missing Mermaid user journey diagram")
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
