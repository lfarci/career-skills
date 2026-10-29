#!/usr/bin/env python3
"""Agent adapter for run_behavioral_evals.py: run one prompt in OpenCode inside a scratch dir.

Developer tool. Reads the prompt on stdin, creates a temporary directory with every
skill linked under .opencode/skills/, runs `opencode run`, and prints the reply plus
the files the agent left behind, so scoring can use files, not only text.

Usage (via the runner):
    python3 scripts/run_behavioral_evals.py \
        --agent-command 'python3 scripts/opencode_adapter.py --model opencode/big-pickle'
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
    """Copy every skill package into workdir/.opencode/skills/<name>."""
    target = workdir / ".opencode" / "skills"
    target.mkdir(parents=True)
    for skill in ROOT.joinpath("skills").rglob("SKILL.md"):
        shutil.copytree(skill.parent, target / skill.parent.name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model", default="opencode/big-pickle")
    parser.add_argument("--keep", action="store_true", help="keep the scratch directory")
    args = parser.parse_args()
    prompt = sys.stdin.read().replace("Use $", "Use the skill ")
    workdir = Path(tempfile.mkdtemp(prefix="career-eval-"))
    install(workdir)
    # OpenCode resolves its project from the Git root; without one it can attach to another
    # directory (observed: writes into the caller's repo). Make the scratch dir its own repo.
    subprocess.run(["git", "init", "-q"], cwd=workdir, check=False)
    opencode = shutil.which("opencode") or str(Path.home() / ".opencode" / "bin" / "opencode")
    result = subprocess.run(
        [opencode, "run", "-m", args.model, prompt],
        # OpenCode reads $PWD, not the OS cwd: without this it works in the caller's directory.
        cwd=workdir, env={**os.environ, "PWD": str(workdir)}, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    print(result.stdout)
    if not result.stdout.strip():
        # Seen when several free-model runs share one OpenCode install concurrently: run cases serially.
        print("[adapter] empty reply from opencode; stderr tail:\n" + result.stderr[-800:])
    files = [p.relative_to(workdir).as_posix() for p in sorted(workdir.rglob("*")) if p.is_file() and not {".opencode", ".git"} & set(p.parts)]
    print("\n--- files left by the agent ---\n" + ("\n".join(files) if files else "(none)"))
    print(f"--- scratch dir: {workdir}")
    if not args.keep:
        shutil.rmtree(workdir, ignore_errors=True)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
