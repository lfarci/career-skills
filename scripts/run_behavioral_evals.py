#!/usr/bin/env python3
"""Run opt-in agent smoke evaluations, keeping behavioral scoring separate from CI."""
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import tempfile
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from harness import DEFAULT_HARNESS, HARNESSES, kill_tree, new_group_kwargs  # noqa: E402
FIXTURES = ROOT / "tests" / "fixtures"
DEFAULT_OUT = ROOT / "eval-results" / "smoke.json"


def scenarios() -> list[dict]:
    cases = {
        case["id"]: case
        for case in json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))["cases"]
    }
    smoke = json.loads((ROOT / "tests" / "eval-smoke.json").read_text(encoding="utf-8"))
    return [
        {**cases[item["id"]], "mode": item["mode"]}
        for item in smoke["existing_cases"]
    ] + list(smoke["negative_cases"])


def review(path: Path) -> int:
    results = json.loads(path.read_text(encoding="utf-8"))["results"]
    passed = failed = pending = 0
    for item in results:
        for criterion in item["assessments"]:
            status = criterion["status"]
            if status in {"pass", "fail"} and not criterion.get("evidence", "").strip():
                print(f"Missing evidence for {item['id']}: {criterion['criterion']}", file=sys.stderr)
                pending += 1
            elif status == "pass":
                passed += 1
            elif status == "fail":
                failed += 1
            elif status in {"pending", "unknown"}:
                pending += 1
            else:
                raise ValueError(f"Unsupported status: {status}")
    print(f"Behavioral criteria: {passed} pass, {failed} fail, {pending} pending/unknown")
    return 1 if failed else 2 if pending else 0


def run_with_timeout(argv: list[str], prompt: str, timeout: int, cwd: str,
                     env: dict[str, str]) -> tuple[str, str, int]:
    """Run the agent command; on timeout kill its whole process tree and return exit code 124."""
    group = new_group_kwargs()
    process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, encoding="utf-8", errors="replace", cwd=cwd, env=env, **group)
    try:
        out, err = process.communicate(prompt, timeout=timeout)
        return out, err, process.returncode
    except subprocess.TimeoutExpired:
        kill_tree(process)
        out, err = process.communicate()
        return out or "", (err or "") + f"\nTimed out after {timeout}s; process tree killed", 124


def run(command: str, output: Path, selected: set[str], timeout: int, label: str) -> int:
    argv = shlex.split(command)
    if not argv:
        raise ValueError("Agent command cannot be empty")
    cases = scenarios()
    unknown = selected - {case["id"] for case in cases}
    if unknown:
        raise ValueError(f"Unknown smoke IDs: {sorted(unknown)}")
    if timeout < 1:
        raise ValueError("Timeout must be positive")
    results: list[dict] = []
    for case in cases:
        if selected and case["id"] not in selected:
            continue
        prompt = case["prompt"]
        if case["mode"] == "explicit":
            prompt = "Use $" + case["skill"] + " for this task. " + prompt
        print(f"Running {case['id']} ({case['mode']})...", flush=True)
        scratch = tempfile.mkdtemp(prefix="career-eval-run-")  # never run an agent inside this repo
        fixture = FIXTURES / case["id"]
        if fixture.is_dir():  # synthetic files the prompt describes
            shutil.copytree(fixture, scratch, dirs_exist_ok=True)
        try:
            response, stderr, exit_code = run_with_timeout(
                argv, prompt, timeout, cwd=scratch, env={**os.environ, "PWD": scratch})
        except OSError as exc:
            response, stderr, exit_code = "", f"Could not start agent: {exc}", 127
        results.append({
            "id": case["id"], "skill": case.get("skill"), "mode": case["mode"],
            "prompt": prompt, "response": response, "stderr": stderr,
            "exit_code": exit_code,
            "assessments": [
                {"criterion": expectation, "status": "pending", "evidence": ""}
                for expectation in case["expect"]
            ],
        })
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "harness": label, "results": results,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved {len(results)} unscored responses: {output}")
    print("Inspect responses, artifacts and skill traces. Score every criterion before --review.")
    return 0 if all(item["exit_code"] == 0 for item in results) else 1


def harness_command(harness: str, model: str | None = None) -> str:
    """Return the adapter command line for a harness id (copilot, codex or opencode)."""
    if harness not in HARNESSES:
        raise ValueError(f"Unknown harness {harness!r}; choose from {sorted(HARNESSES)}")
    argv = [sys.executable, str(ROOT / "scripts" / f"{harness}_adapter.py")]
    return shlex.join(argv + (["--model", model] if model else []))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harness", choices=sorted(HARNESSES), default=DEFAULT_HARNESS,
                        help="agent CLI to run (default: %(default)s); maps to scripts/<harness>_adapter.py")
    parser.add_argument("--model", help="model passed to the harness adapter (default: the harness default)")
    parser.add_argument("--agent-command", help="override: any agent or adapter reading the prompt from stdin")
    parser.add_argument("--case-id", action="append", default=[], help="Restrict to smoke case (repeatable)")
    parser.add_argument("--harness-label", help="agent and host version (default: harness and model)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--review", type=Path, help="Summarize manually scored transcript JSON")
    args = parser.parse_args()
    if args.review is not None:
        return review(args.review)
    command = args.agent_command or harness_command(args.harness, args.model)
    label = args.harness_label or ("custom agent command" if args.agent_command
                                   else " ".join(filter(None, [args.harness, args.model])))
    return run(command, args.output, set(args.case_id), args.timeout, label)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
