#!/usr/bin/env python3
"""Shared helpers for running one prompt in a coding-agent CLI (Copilot, Codex or OpenCode).

Developer tool (not shipped with a skill). Standard library only, cross-platform.

The adapters (`copilot_adapter.py`, `codex_adapter.py`, `opencode_adapter.py`) and
`run_setup_scenarios.py` use this module so that scratch-dir setup, skill install,
process-tree kill, created-file diff and harness-error reporting live in one place.
A missing or unauthenticated harness exits with HARNESS_ERROR_EXIT (75), never as a
skill result.
"""
from __future__ import annotations

import argparse
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS_ERROR_EXIT = 75  # EX_TEMPFAIL: harness unavailable, rerun later
TIMEOUT_EXIT = 124
DEFAULT_HARNESS = "copilot"
# Stderr phrases meaning the plan ran out (quota, credits, rate limit), not that the skill failed.
QUOTA_MARKERS = ("usage limit", "quota exceeded", "insufficient credits", "rate limit exceeded",
                 "exceeded your", "out of credits")


@dataclass(frozen=True)
class Harness:
    """How to invoke one agent CLI headless.

    Attributes:
        name: Harness id used on the command line.
        binary: Executable name looked up on PATH.
        skills_dir: Project skills folder the harness discovers, relative to the workdir.
    """

    name: str
    binary: str
    skills_dir: str


HARNESSES: dict[str, Harness] = {
    "copilot": Harness("copilot", "copilot", ".agents/skills"),
    "codex": Harness("codex", "codex", ".agents/skills"),
    "opencode": Harness("opencode", "opencode", ".opencode/skills"),
}


class HarnessError(RuntimeError):
    """The harness is missing, unauthenticated or out of quota."""


def get(name: str) -> Harness:
    """Return the harness spec for name or raise ValueError."""
    try:
        return HARNESSES[name]
    except KeyError:
        raise ValueError(f"Unknown harness {name!r}; choose from {sorted(HARNESSES)}") from None


def find_binary(harness: Harness) -> str | None:
    """Return the harness executable path, or None when it is not installed."""
    found = shutil.which(harness.binary)
    if found or harness.name != "opencode":
        return found
    fallback = Path.home() / ".opencode" / "bin" / "opencode"
    return str(fallback) if fallback.is_file() else None


def agent_env(harness: Harness, workdir: Path) -> dict[str, str]:
    """Build the agent environment; raise HarnessError when credentials are missing."""
    # OpenCode reads $PWD, not the OS cwd: without it agents wrote into the caller's directory.
    env = {**os.environ, "PWD": str(workdir)}
    if harness.name == "copilot":
        if not any(env.get(k) for k in ("COPILOT_GITHUB_TOKEN", "GH_TOKEN", "GITHUB_TOKEN")):
            token = ""
            if shutil.which("gh"):
                token = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True,
                                       check=False).stdout.strip()
            if not token:
                raise HarnessError("copilot not authenticated (set GH_TOKEN or run `gh auth login`)")
            env["GH_TOKEN"] = token
    elif harness.name == "codex":
        if not (env.get("CODEX_API_KEY") or env.get("OPENAI_API_KEY")):
            status = subprocess.run([find_binary(harness) or "codex", "login", "status"],
                                    capture_output=True, text=True, check=False)
            if status.returncode != 0:
                raise HarnessError("codex not authenticated (run `codex login` or set CODEX_API_KEY)")
    return env


def build_command(harness: Harness, binary: str, prompt: str, model: str | None = None,
                  resume: bool = False) -> list[str]:
    """Return argv for one headless turn; resume continues the last session in the workdir.

    Continuation: Copilot `--continue`, Codex `exec resume --last`, OpenCode `run -c`.
    """
    if harness.name == "copilot":
        argv = [binary, "-p", prompt, "--allow-all-tools"]
        argv += ["--continue"] if resume else []
        return argv + (["--model", model] if model else [])
    if harness.name == "codex":
        # workspace-write lets the agent write inside the scratch dir only (--full-auto is retired).
        argv = [binary, "exec", "--sandbox", "workspace-write", "--skip-git-repo-check"]
        argv += ["--model", model] if model else []
        return argv + (["resume", "--last", prompt] if resume else [prompt])
    # Any provider OpenCode is logged in to: github-copilot/<m>, openai/<m>, openrouter/<m>, ...
    argv = [binary, "run", "--print-logs", *(["-m", model] if model else [])]
    return argv + (["-c"] if resume else []) + [prompt]


def install_skills(workdir: Path, harness: Harness, names: set[str] | None = None) -> None:
    """Copy skill packages (all, or only names) into the harness's project skills folder."""
    target = workdir.joinpath(*harness.skills_dir.split("/"))
    target.mkdir(parents=True, exist_ok=True)
    for skill in sorted(ROOT.joinpath("skills").rglob("SKILL.md")):
        if names is None or skill.parent.name in names:
            shutil.copytree(skill.parent, target / skill.parent.name, dirs_exist_ok=True)


def make_scratch(prefix: str, seed: Path | None = None) -> Path:
    """Create a git-initialised scratch dir, optionally seeded from a directory's files."""
    workdir = Path(tempfile.mkdtemp(prefix=prefix))
    if seed is not None:
        shutil.copytree(seed, workdir, dirs_exist_ok=True)
    # Without its own Git root an agent can attach to an enclosing repo and write there.
    subprocess.run(["git", "init", "-q"], cwd=workdir, check=False)
    return workdir


def snapshot(workdir: Path) -> dict[Path, bytes]:
    """Return file contents keyed by path, excluding .git."""
    return {p: p.read_bytes() for p in workdir.rglob("*") if p.is_file() and ".git" not in p.parts}


def changed_files(workdir: Path, before: dict[Path, bytes], harness: Harness) -> list[str]:
    """List files the agent created or changed, ignoring .git and the installed skills."""
    skip = {".git", harness.skills_dir.split("/")[0]}
    return [p.relative_to(workdir).as_posix() for p in sorted(workdir.rglob("*"))
            if p.is_file() and not skip & set(p.relative_to(workdir).parts)
            and before.get(p) != p.read_bytes()]


def new_group_kwargs() -> dict:
    """Popen kwargs that start the child in its own process group/session."""
    if os.name == "nt":
        return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    return {"start_new_session": True}


def kill_tree(process: subprocess.Popen) -> None:
    """Kill a process and every descendant (its own process group/session)."""
    if os.name == "nt":
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(process.pid)], capture_output=True, check=False)
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def run_agent(argv: list[str], cwd: Path, env: dict[str, str],
              timeout: int | None = None) -> tuple[str, str, int]:
    """Run argv in its own process group; return (stdout, stderr tail, exit code).

    Exit 124 on timeout and HARNESS_ERROR_EXIT when a quota marker appears on stderr (some
    CLIs retry silently on quota errors); the whole process tree is killed in both cases.
    """
    reply = tempfile.TemporaryFile(mode="w+", encoding="utf-8", errors="replace")
    proc = subprocess.Popen(argv, cwd=cwd, env=env, stdout=reply, stderr=subprocess.PIPE,
                            stdin=subprocess.DEVNULL,
                            text=True, encoding="utf-8", errors="replace", **new_group_kwargs())
    tail: list[str] = []
    stopped = threading.Event()

    def watch() -> None:
        for line in proc.stderr:
            tail.append(line)
            del tail[:-20]
            if any(marker in line.lower() for marker in QUOTA_MARKERS):
                stopped.set()
                kill_tree(proc)
                break

    reader = threading.Thread(target=watch, daemon=True)
    reader.start()
    try:
        code = proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        kill_tree(proc)
        proc.wait()
        code = TIMEOUT_EXIT
        tail.append(f"Timed out after {timeout}s; process tree killed\n")
    reader.join(timeout=5)
    if stopped.is_set():
        code = HARNESS_ERROR_EXIT
        tail.append("HARNESS ERROR: quota/credit limit reported\n")
    reply.seek(0)
    return reply.read(), "".join(tail), code


def adapter_main(name: str, argv: list[str] | None = None) -> int:
    """Adapter entry point: prompt on stdin, run it in a scratch copy of cwd, print reply and files."""
    harness = get(name)
    parser = argparse.ArgumentParser(description=f"Run one prompt from stdin in {name} inside a scratch dir.")
    parser.add_argument("--model", help=f"{name} model (default: the harness default)")
    parser.add_argument("--keep", action="store_true", help="keep the scratch directory")
    parser.add_argument("--timeout", type=int, default=None, help="seconds before the agent is killed")
    args = parser.parse_args(argv)
    prompt = sys.stdin.read().replace("Use $", "Use the skill ")
    binary = find_binary(harness)
    if binary is None:
        print(f"[adapter] HARNESS ERROR: {name} not installed/authenticated ({harness.binary} not on PATH)")
        return HARNESS_ERROR_EXIT
    workdir = make_scratch(f"career-eval-{name}-", seed=Path.cwd())  # case fixtures the runner placed in cwd
    try:
        install_skills(workdir, harness)
        before = snapshot(workdir)
        try:
            env = agent_env(harness, workdir)
        except HarnessError as exc:
            print(f"[adapter] HARNESS ERROR: {name} not installed/authenticated: {exc}")
            return HARNESS_ERROR_EXIT
        stdout, stderr, code = run_agent(build_command(harness, binary, prompt, args.model), workdir, env,
                                         args.timeout)
        if code == HARNESS_ERROR_EXIT:
            print(f"[adapter] HARNESS ERROR: {name} reported a quota/credit limit; not a skill result. "
                  "Rerun with another --harness or --model.\n" + stderr[-800:])
        else:
            print(stdout)
            if not stdout.strip():
                print(f"[adapter] empty reply from {name}; stderr tail:\n" + stderr[-800:])
        files = changed_files(workdir, before, harness)
        print("\n--- files created or changed by the agent ---\n" + ("\n".join(files) if files else "(none)"))
        print(f"--- scratch dir: {workdir}")
        return code
    finally:
        if not args.keep:
            shutil.rmtree(workdir, ignore_errors=True)
