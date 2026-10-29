#!/usr/bin/env python3
"""Check visual asset files in a Career Skills workspace against the naming contract.

Contract (relative to the workspace root):
    assets/drafts/<kind>/<concept>-v<n>.<ext>
    assets/drafts/<kind>/previews/<concept>-v<n>-<size>.<ext>
    assets/staged/<kind>/<concept>-v<n>[-<variant>].<ext>
and every draft or staged master is linked from brand/identity.md.
Kinds owned by other skills (assets/<drafts|staged>/resumes/ from build-resume)
are skipped.

Standard library only; works on Windows, macOS and Linux.

Usage:
    python3 check_assets.py <workspace-root> [--json]

Exit codes: 0 no errors, 1 errors found, 2 root unusable.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VISUAL = {".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf"}
MASTER = re.compile(r"^[a-z0-9]+-v\d+(-[a-z0-9]+)*\.[a-z0-9]+$")
PREVIEW = re.compile(r"^[a-z0-9]+-v\d+-[a-z0-9]+\.[a-z0-9]+$")
OTHER_KINDS = {"resumes"}  # written by build-resume; not design assets
SCRATCH = {".html", ".htm", ".js", ".py", ".sh", ".tmp", ".log"}


def classify(rel: Path) -> str | None:
    """Return an error message for a file under assets/, or None when it follows the contract."""
    parts = rel.parts
    if len(parts) > 3 and parts[1] in {"drafts", "staged"} and parts[2] in OTHER_KINDS:
        return None
    if rel.suffix.lower() in SCRATCH:
        return f"{rel.as_posix()}: scratch/render file; keep helpers outside the workspace"
    if rel.suffix.lower() not in VISUAL:
        return None
    if len(parts) < 4 or parts[1] not in {"drafts", "staged"}:
        return f"{rel.as_posix()}: expected assets/<drafts|staged>/<kind>/<file>"
    if parts[-2] == "previews":
        ok = PREVIEW.match(parts[-1])
    else:
        ok = len(parts) == 4 and MASTER.match(parts[-1])
    return None if ok else f"{rel.as_posix()}: name must look like <concept>-v<n>.<ext> (previews: <concept>-v<n>-<size>.<ext>)"


def check(root: Path) -> dict[str, list[str]]:
    """Check every file under assets/ and the identity links."""
    errors: list[str] = []
    warnings: list[str] = []
    identity = root / "brand" / "identity.md"
    linked = identity.read_text(encoding="utf-8", errors="replace") if identity.is_file() else ""
    masters = []
    assets = root / "assets"
    for path in sorted(p for p in assets.rglob("*") if p.is_file()) if assets.is_dir() else []:
        rel = path.relative_to(root)
        problem = classify(rel)
        if problem:
            errors.append(problem)
        elif (rel.suffix.lower() in VISUAL and "previews" not in rel.parts
              and not (len(rel.parts) > 3 and rel.parts[2] in OTHER_KINDS)):
            masters.append(rel)
    if masters and not identity.is_file():
        errors.append("brand/identity.md: missing; add a 'Status: pending' entry linking the drafts")
    for rel in masters:
        if identity.is_file() and Path(*rel.parts[1:]).as_posix() not in linked and rel.as_posix() not in linked:
            warnings.append(f"{rel.as_posix()}: not linked from brand/identity.md")
    return {"errors": errors, "warnings": warnings}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("root", type=Path, help="workspace root folder")
    parser.add_argument("--json", action="store_true", help="print a JSON report")
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        print(f"Workspace root not found: {args.root}", file=sys.stderr)
        return 2
    result = check(args.root)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("Assets: " + ("needs repair" if result["errors"] else "ok"))
        print("\n".join([f"ERROR {e}" for e in result["errors"]] + [f"WARN  {w}" for w in result["warnings"]]))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
