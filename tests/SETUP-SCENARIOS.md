# Live setup scenarios

Three short live checks for `setup-career-skills`. Run them after any setup change; CI does not run an agent.

```bash
python3 scripts/run_setup_scenarios.py                                    # all three, Copilot
python3 scripts/run_setup_scenarios.py --harness codex --scenario 3       # one, Codex
python3 scripts/run_setup_scenarios.py --harness opencode --model github-copilot/<model>
```

The runner makes a fresh temp dir per scenario, installs only this skill in the harness's skills folder, seeds scenario 3, runs the chosen harness (exit 75 `HARNESS ERROR` when it is missing or out of quota: switch `--harness`/`--model`), and prints the reply tail and files left on disk. Score from files and tool trace, not from the reply. Synthetic data only.

## 1. Named folder and supplied role
Prompt names `career-skill-smoke` as the folder, grants writes and gives one ExampleCo role.
**Pass:** `career-skill-smoke/README.md` and `profile/experience.md` exist with only the supplied role; no nested `career/`; no empty files; README has Records, Source inventory and Setup progress; the agent did not re-ask folder or permission; ends with one question.

## 2. No destination
Prompt: "Use setup-career-skills to start my private career workspace."
**Pass:** asks where and in what form (Markdown default); no workspace reads or writes before the answer.

## 3. Resume a saved decision
Seeded `career-skill-resume/` with status `in progress` and next decision "choose one priority direction for the next review".
**Pass:** reads that README and its record only; no file changes; asks the saved decision with its saved wording; does not answer it or restart intake.

## Results

| Date | Model | 1 | 2 | 3 | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-10-29 | opencode/big-pickle | pass | pass | pass | checker run after writes |
| 2026-10-29 | opencode/nemotron-3.5-lightning-free | fail | pass | fail | created empty records (now a checker error); reworded the saved decision; a re-run wandered outside the scratch dir via a sub-agent, then timed out |
| 2026-10-29 | opencode/flint-40b-free | invalid | pass | timeout | wrote outside its scratch dir |

Models below big-pickle's level are not a support target yet: record their results, and change the skill only for failures that a host-neutral rule or the checker fixes, not to chase one transcript.
