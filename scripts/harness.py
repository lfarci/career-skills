"""Run one prompt headless in Copilot, Codex or OpenCode inside a scratch dir.

Developer tool, standard library only. A missing binary, missing login or quota message
exits 75 with "HARNESS ERROR": not a skill result; rerun with another --harness/--model.
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
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS_ERROR_EXIT = 75
DEFAULT_HARNESS = "copilot"
HARNESSES = {"copilot": ".agents/skills", "codex": ".agents/skills", "opencode": ".opencode/skills"}
QUOTA_MARKERS = ("usage limit", "quota exceeded", "insufficient credits", "rate limit exceeded",
                 "exceeded your", "out of credits")


class HarnessError(RuntimeError):
    """The harness is missing, not logged in or out of quota."""


def find_binary(name: str) -> str:
    """Return the harness executable or raise HarnessError."""
    found = shutil.which(name)
    home_opencode = Path.home() / ".opencode" / "bin" / "opencode"
    if not found and name == "opencode" and home_opencode.is_file():
        found = str(home_opencode)
    if not found:
        raise HarnessError(f"{name} not installed/authenticated ({name} not on PATH)")
    return found


def agent_env(name: str, workdir: Path) -> dict[str, str]:
    """Environment for the agent; raise HarnessError when credentials are missing."""
    env = {**os.environ, "PWD": str(workdir)}  # OpenCode reads $PWD, not the OS cwd
    if name == "copilot" and not any(env.get(k) for k in ("COPILOT_GITHUB_TOKEN", "GH_TOKEN", "GITHUB_TOKEN")):
        token = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True,
                               check=False).stdout.strip() if shutil.which("gh") else ""
        if not token:
            raise HarnessError("copilot not installed/authenticated (set GH_TOKEN or `gh auth login`)")
        env["GH_TOKEN"] = token
    if name == "codex" and not (env.get("CODEX_API_KEY") or env.get("OPENAI_API_KEY")):
        if subprocess.run([find_binary("codex"), "login", "status"], capture_output=True, check=False).returncode:
            raise HarnessError("codex not installed/authenticated (run `codex login`)")
    return env


def build_command(name: str, binary: str, prompt: str, model: str | None = None,
                  resume: bool = False) -> list[str]:
    """Argv for one turn; resume continues the last session in the workdir."""
    if name == "copilot":
        return [binary, "-p", prompt, "--allow-all-tools", *(["--continue"] if resume else []),
                *(["--model", model] if model else [])]
    if name == "codex":
        argv = [binary, "exec", "--sandbox", "workspace-write", "--skip-git-repo-check",
                *(["--model", model] if model else [])]
        return argv + (["resume", "--last", prompt] if resume else [prompt])
    # OpenCode: any logged-in provider, e.g. github-copilot/<m>, openai/<m>, openrouter/<m>.
    return [binary, "run", "--print-logs", *(["-m", model] if model else []),
            *(["-c"] if resume else []), prompt]


def make_scratch(name: str, seed: Path | None = None, skills: set[str] | None = None) -> Path:
    """Git-initialised temp dir with seed files and skills in the harness's skills folder."""
    workdir = Path(tempfile.mkdtemp(prefix=f"career-eval-{name}-"))
    if seed is not None:
        shutil.copytree(seed, workdir, dirs_exist_ok=True)
    target = workdir / HARNESSES[name]
    for skill in ROOT.joinpath("skills").rglob("SKILL.md"):
        if skills is None or skill.parent.name in skills:
            shutil.copytree(skill.parent, target / skill.parent.name)
    subprocess.run(["git", "init", "-q"], cwd=workdir, check=False)  # keep the agent out of other repos
    return workdir


def kill_tree(process: subprocess.Popen) -> None:
    """Kill a process started with new_group_kwargs() and all its descendants."""
    if os.name == "nt":
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(process.pid)], capture_output=True, check=False)
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def new_group_kwargs() -> dict:
    """Popen kwargs that start the child in its own process group."""
    if os.name == "nt":
        return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    return {"start_new_session": True}


def run_agent(argv: list[str], cwd: Path, env: dict[str, str], timeout: int | None) -> tuple[str, str, int]:
    """Run argv; return (stdout, stderr tail, code). 124 on timeout, 75 on a quota message."""
    out = tempfile.TemporaryFile(mode="w+", encoding="utf-8", errors="replace")
    proc = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=out,
                            stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace",
                            **new_group_kwargs())
    tail: list[str] = []
    quota = threading.Event()

    def watch() -> None:  # some CLIs retry silently on quota errors until killed
        for line in proc.stderr:
            tail[:] = (tail + [line])[-20:]
            if any(m in line.lower() for m in QUOTA_MARKERS):
                quota.set()
                kill_tree(proc)

    reader = threading.Thread(target=watch, daemon=True)
    reader.start()
    try:
        code = proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        kill_tree(proc)
        code = 124
    reader.join(timeout=5)
    out.seek(0)
    return out.read(), "".join(tail), HARNESS_ERROR_EXIT if quota.is_set() else code


def adapter_main(name: str, argv: list[str] | None = None) -> int:
    """Adapter: prompt on stdin, run in a scratch copy of cwd, print reply and changed files."""
    parser = argparse.ArgumentParser(description=f"Run one stdin prompt in {name}.")
    parser.add_argument("--model")
    parser.add_argument("--keep", action="store_true", help="keep the scratch directory")
    parser.add_argument("--timeout", type=int)
    args = parser.parse_args(argv)
    prompt = sys.stdin.read().replace("Use $", "Use the skill ")
    try:
        binary = find_binary(name)
        workdir = make_scratch(name, seed=Path.cwd())
        env = agent_env(name, workdir)
    except HarnessError as exc:
        print(f"[adapter] HARNESS ERROR: {exc}")
        return HARNESS_ERROR_EXIT
    before = {p: p.read_bytes() for p in workdir.rglob("*") if p.is_file()}
    stdout, stderr, code = run_agent(build_command(name, binary, prompt, args.model), workdir, env, args.timeout)
    if code == HARNESS_ERROR_EXIT:
        print(f"[adapter] HARNESS ERROR: {name} reported a quota/credit limit; rerun with another "
              f"--harness or --model.\n{stderr[-800:]}")
    else:
        print(stdout or f"[adapter] empty reply from {name}; stderr tail:\n{stderr[-800:]}")
    skip = {".git", HARNESSES[name].split("/")[0]}
    files = [p.relative_to(workdir).as_posix() for p in sorted(workdir.rglob("*")) if p.is_file()
             and not skip & set(p.relative_to(workdir).parts) and before.get(p) != p.read_bytes()]
    print("\n--- files created or changed by the agent ---\n" + ("\n".join(files) or "(none)"))
    print(f"--- scratch dir: {workdir}")
    if not args.keep:
        shutil.rmtree(workdir, ignore_errors=True)
    return code
