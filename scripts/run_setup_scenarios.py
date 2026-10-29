#!/usr/bin/env python3
"""Run the live setup scenarios from tests/SETUP-SCENARIOS.md on a chosen agent CLI.

Developer tool (not shipped with a skill). Standard library only.

Usage:
    python3 scripts/run_setup_scenarios.py [--harness copilot|codex|opencode] [--model M] [--scenario 1 2 3]
    python3 scripts/run_setup_scenarios.py --scenario 2 --follow-up "Use ./career, Markdown."

Each scenario runs in a fresh git-initialised temp dir with only setup-career-skills
installed in the harness's project skills folder. Each --follow-up is sent as a further
turn in the same session (Copilot --continue, Codex exec resume --last, OpenCode run -c).
Prints the reply tail and the files left on disk. Scoring stays manual: compare against
the pass criteria in the doc. Exit 75 when the harness is missing or not authenticated.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness as h  # noqa: E402

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


def prepare(workdir: Path, scenario: str, spec: h.Harness) -> None:
    """Install the skill and seed scenario files."""
    h.install_skills(workdir, spec, {SKILL.name})
    if scenario == "3":
        root = workdir / "career-skill-resume"
        (root / "profile").mkdir(parents=True)
        (root / "README.md").write_text(SEED_README, encoding="utf-8")
        (root / "profile" / "experience.md").write_text(SEED_ROLE, encoding="utf-8")


def run(spec: h.Harness, binary: str, scenario: str, model: str | None, timeout: int,
        follow_ups: list[str]) -> int:
    """Run one scenario (plus follow-up turns) and print its observable result."""
    workdir = h.make_scratch(f"setup-scenario-{scenario}-")
    prepare(workdir, scenario, spec)
    env = h.agent_env(spec, workdir)
    code = 0
    for turn, prompt in enumerate([PROMPTS[scenario], *follow_ups]):
        argv = h.build_command(spec, binary, prompt, model, resume=turn > 0)
        stdout, stderr, code = h.run_agent(argv, workdir, env, timeout)
        reply = stdout + stderr if code else stdout
        print(f"### scenario {scenario} · turn {turn + 1} · {spec.name} {model or ''} · {workdir}")
        print("\n".join(line for line in reply.splitlines() if line.strip())[-1500:])
        if code:
            break
    for path in sorted(workdir.rglob("*")):
        parts = set(path.relative_to(workdir).parts)
        if path.is_file() and not {".git", spec.skills_dir.split("/")[0]} & parts:
            print(f"  file: {path.relative_to(workdir).as_posix()} ({path.stat().st_size} B)")
    return code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run live setup scenarios on Copilot, Codex or OpenCode.")
    parser.add_argument("--harness", choices=sorted(h.HARNESSES), default=h.DEFAULT_HARNESS,
                        help="agent CLI to run (default: %(default)s)")
    parser.add_argument("--model", help="model for the harness (default: the harness default)")
    parser.add_argument("--scenario", nargs="*", default=sorted(PROMPTS), choices=sorted(PROMPTS))
    parser.add_argument("--follow-up", action="append", default=[],
                        help="further user turn in the same session (repeatable)")
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args(argv)
    spec = h.get(args.harness)
    binary = h.find_binary(spec)
    if binary is None:
        print(f"HARNESS ERROR: {spec.name} not installed/authenticated ({spec.binary} not on PATH)")
        return h.HARNESS_ERROR_EXIT
    worst = 0
    for scenario in args.scenario:
        try:
            code = run(spec, binary, scenario, args.model, args.timeout, args.follow_up)
        except h.HarnessError as exc:
            print(f"HARNESS ERROR: {spec.name} not installed/authenticated: {exc}")
            return h.HARNESS_ERROR_EXIT
        if code == h.HARNESS_ERROR_EXIT:
            print(f"HARNESS ERROR: {spec.name} quota/credit limit; rerun with another --harness or --model.")
            return code
        worst = worst or code
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
