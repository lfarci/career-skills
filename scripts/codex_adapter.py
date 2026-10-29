#!/usr/bin/env python3
"""Agent adapter for run_behavioral_evals.py: run one prompt in codex inside a scratch dir.

Developer tool. Codex CLI (`codex exec --sandbox workspace-write`). Auth via `codex login` or CODEX_API_KEY/OPENAI_API_KEY.
Reads the prompt on stdin, copies the case fixtures from cwd into a git-initialised scratch dir,
installs every skill, runs the agent and prints the reply plus the files it created or changed.
Exits 75 with "HARNESS ERROR" when codex is missing or not authenticated. Logic lives in harness.py.

Usage (via the runner):
    python3 scripts/run_behavioral_evals.py --harness codex --case-id <id>
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import adapter_main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(adapter_main("codex"))
