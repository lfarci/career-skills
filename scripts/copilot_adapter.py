#!/usr/bin/env python3
"""Agent adapter for run_behavioral_evals.py: run one prompt in GitHub Copilot CLI in a scratch dir.

Developer tool. Reads the prompt on stdin, copies the case fixtures from the current directory
into a fresh git-initialised scratch dir, installs every skill under .agents/skills/, runs
`copilot -p <prompt> --allow-all-tools`, and prints the reply (with tool trace and the AI-credit
line) plus the files the agent created or changed.

Auth: uses GH_TOKEN, or `gh auth token` when GH_TOKEN is unset. Each run spends Copilot credits.

Usage (via the runner, one case at a time):
    python3 scripts/run_behavioral_evals.py --agent-command 'python3 scripts/copilot_adapter.py'
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def install(workdir: Path) -> None:
    """Copy every skill package into workdir/.agents/skills/<name>."""
    target = workdir / ".agents" / "skills"
    target.mkdir(parents=True)
    for skill in ROOT.joinpath("skills").rglob("SKILL.md"):
        shutil.copytree(skill.parent, target / skill.parent.name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model", help="Copilot model (default: Copilot's own default)")
    parser.add_argument("--keep", action="store_true", help="keep the scratch directory")
    args = parser.parse_args()
    prompt = sys.stdin.read().replace("Use $", "Use the skill ")
    workdir = Path(tempfile.mkdtemp(prefix="career-eval-copilot-"))
    shutil.copytree(Path.cwd(), workdir, dirs_exist_ok=True)
    install(workdir)
    subprocess.run(["git", "init", "-q"], cwd=workdir, check=False)
    before = {p: p.read_bytes() for p in workdir.rglob("*") if p.is_file() and ".git" not in p.parts}
    env = {**os.environ, "PWD": str(workdir)}
    if not env.get("GH_TOKEN") and shutil.which("gh"):
        env["GH_TOKEN"] = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True,
                                         check=False).stdout.strip()
    copilot = shutil.which("copilot") or "copilot"
    command = [copilot, "-p", prompt, "--allow-all-tools", *(["--model", args.model] if args.model else [])]
    result = subprocess.run(command, cwd=workdir, env=env, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", check=False)
    print(result.stdout)
    if not result.stdout.strip():
        print("[adapter] empty reply from copilot; stderr tail:\n" + result.stderr[-800:])
    files = [p.relative_to(workdir).as_posix() for p in sorted(workdir.rglob("*"))
             if p.is_file() and before.get(p) != p.read_bytes() and not {".agents", ".git"} & set(p.parts)]
    print("\n--- files created or changed by the agent ---\n" + ("\n".join(files) if files else "(none)"))
    print(f"--- scratch dir: {workdir}")
    if not args.keep:
        shutil.rmtree(workdir, ignore_errors=True)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
