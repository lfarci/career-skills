#!/usr/bin/env python3
"""Run the live setup scenarios from tests/SETUP-SCENARIOS.md with the OpenCode CLI.

Developer tool (not shipped with a skill). Standard library only.

Usage:
    python3 scripts/run_setup_scenarios.py --model opencode/big-pickle [--scenario 1 2 3]

Each scenario runs in a fresh temporary directory with only setup-career-skills
installed under .agents/skills/. Prints the reply tail and the files left on disk.
Scoring stays manual: compare against the pass criteria in the doc.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "setup-career-skills"

PROMPTS = {
    "1": (
        "Use setup-career-skills to create a workspace in a new folder named career-skill-smoke here.\n\n"
        "You can write local files.\n\nFor now, use only this fictional career information:\n\n"
        "I worked at ExampleCo as a Software Engineer from January 2024 to December 2025.\n\nStart the setup."
    ),
    "2": "Use setup-career-skills to start my private career workspace.",
    "3": "Use setup-career-skills to resume career-skill-resume here. Continue from its saved next decision.",
}
SEED_README = (
    "# Career workspace\n\n## Records\n- [Experience](profile/experience.md)\n\n"
    "## Setup progress\nStatus: in progress\nNext decision: choose one priority direction for the next review\n"
)
SEED_ROLE = "# Experience\n\n## ExampleCo, Software Engineer\n- Jan 2024 to Dec 2025\n"


def prepare(workdir: Path, scenario: str) -> None:
    """Install the skill and seed scenario files."""
    shutil.copytree(SKILL, workdir / ".agents" / "skills" / SKILL.name)
    if scenario == "3":
        root = workdir / "career-skill-resume"
        (root / "profile").mkdir(parents=True)
        (root / "README.md").write_text(SEED_README, encoding="utf-8")
        (root / "profile" / "experience.md").write_text(SEED_ROLE, encoding="utf-8")


def run(model: str, scenario: str, timeout: int) -> None:
    """Run one scenario and print its observable result."""
    workdir = Path(tempfile.mkdtemp(prefix=f"setup-scenario-{scenario}-"))
    prepare(workdir, scenario)
    opencode = shutil.which("opencode") or str(Path.home() / ".opencode" / "bin" / "opencode")
    try:
        result = subprocess.run(
            [opencode, "run", "-m", model, PROMPTS[scenario]],
            cwd=workdir, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
        )
        reply = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        reply = f"TIMEOUT after {timeout}s"
    print(f"### scenario {scenario} · {model} · {workdir}")
    print("\n".join(line for line in reply.splitlines() if line.strip())[-1500:])
    for path in sorted(workdir.rglob("*")):
        if path.is_file() and ".agents" not in path.parts:
            print(f"  file: {path.relative_to(workdir).as_posix()} ({path.stat().st_size} B)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run live setup scenarios with OpenCode.")
    parser.add_argument("--model", default="opencode/big-pickle")
    parser.add_argument("--scenario", nargs="*", default=sorted(PROMPTS), choices=sorted(PROMPTS))
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    for scenario in args.scenario:
        run(args.model, scenario, args.timeout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
