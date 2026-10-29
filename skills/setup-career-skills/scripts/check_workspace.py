#!/usr/bin/env python3
"""Check a Career Skills Markdown workspace: index, local links and record coverage.

Standard library only; works on Windows, macOS and Linux.

Usage:
    python3 check_workspace.py <workspace-root> [--json]

Exit codes: 0 no errors, 1 errors found, 2 root unusable.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from urllib.parse import unquote

HOMES = ("profile", "projects", "brand", "assets", "research")
STATUSES = ("in progress", "paused", "ready", "blocked")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
EXTERNAL = ("http://", "https://", "mailto:", "#")


@dataclass
class Report:
    """Result of a workspace check."""

    root: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    records: int = 0

    @property
    def status(self) -> str:
        return "needs repair" if self.errors else "usable"


def local_links(text: str) -> list[str]:
    """Return local link targets (without anchors) found in Markdown text."""
    targets = []
    for raw in LINK.findall(text):
        if raw.startswith(EXTERNAL):
            continue
        target = unquote(raw.split("#", 1)[0])
        if target:
            targets.append(target)
    return targets


def section(text: str, heading: str) -> str:
    """Return the body of a '## heading' section, or an empty string."""
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S | re.I)
    return match.group(1) if match else ""


def check_links(root: Path, report: Report) -> None:
    """Report broken local links in every Markdown file under the root."""
    for md in sorted(root.rglob("*.md")):
        text = md.read_text(encoding="utf-8", errors="replace")
        for target in local_links(text):
            if not (md.parent / target).exists():
                report.errors.append(f"{md.relative_to(root).as_posix()}: broken link -> {target}")


def check_index(root: Path, index: Path, report: Report) -> None:
    """Check index sections, setup status and that every record is linked."""
    text = index.read_text(encoding="utf-8", errors="replace")
    records_body = section(text, "Records")
    if not records_body:
        report.warnings.append("README.md: no '## Records' section")
    linked = {(root / t).resolve() for t in local_links(text)}
    for home in HOMES:
        for md in sorted((root / home).rglob("*.md")) if (root / home).is_dir() else []:
            report.records += 1
            if md.resolve() not in linked:
                report.warnings.append(f"{md.relative_to(root).as_posix()}: record not linked from README.md")
    progress = section(text, "Setup progress")
    if progress:
        status = re.search(r"Status:\s*([a-z ]+)", progress, re.I)
        if not status or status.group(1).strip().lower() not in STATUSES:
            report.errors.append(f"README.md: Setup progress status must be one of {', '.join(STATUSES)}")
    for child in sorted(root.iterdir()):
        if child.is_dir() and not child.name.startswith(".") and child.name not in HOMES:
            report.warnings.append(f"{child.name}/: not a standard home (fine if mapped in the index)")


def check(root: Path) -> Report:
    """Run every check against a workspace root."""
    report = Report(root=root.as_posix())
    index = root / "README.md"
    if not index.is_file():
        report.errors.append("README.md: missing workspace index")
    else:
        check_index(root, index, report)
    check_links(root, report)
    return report


def render(report: Report) -> str:
    """Format a report as plain text."""
    lines = [f"Workspace: {report.root}", f"Status: {report.status}", f"Records: {report.records}"]
    lines += [f"ERROR {e}" for e in report.errors] + [f"WARN  {w}" for w in report.warnings]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("root", type=Path, help="workspace root folder (the folder holding README.md)")
    parser.add_argument("--json", action="store_true", help="print a JSON report")
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        print(f"Workspace root not found: {args.root}", file=sys.stderr)
        return 2
    report = check(args.root)
    if args.json:
        print(json.dumps({**asdict(report), "status": report.status}, indent=2))
    else:
        print(render(report))
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
