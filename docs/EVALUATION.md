# Behavioral evaluations

Structural CI checks packaging, frontmatter, references and case coverage. It cannot prove that agents select the correct skills or follow their instructions.

## How to validate a change

1. **Critical review first.** The agent maintaining this repo reads each changed skill against the quality bar in AGENTS.md (one purpose, checkable `Done when`, host-neutral wording, record map) and the validator. This catches most problems.
2. **A few targeted live runs** on whichever subscription has credits: the one or two cases or setup scenarios the change touches. Check files written, not only the reply.
3. **Full smoke suite: optional**, for larger refactors.

## Choosing the engine

Both runners take `--harness {copilot,codex,opencode}` (default `copilot`) and `--model` (passed through; default is the harness's own default). No engine is hardcoded.

```bash
cd /tmp   # never from the checkout
python3 $REPO/scripts/run_behavioral_evals.py --harness copilot --case-id <id> --output /tmp/evr/<id>.json
python3 $REPO/scripts/run_setup_scenarios.py --harness copilot --scenario 2 --follow-up "Use ./career, Markdown."
python3 $REPO/scripts/run_behavioral_evals.py --review /tmp/evr/<id>.json
```

`--agent-command '<cmd>'` still overrides `--harness` with any adapter that reads the prompt on stdin. Adapters (`scripts/<harness>_adapter.py`, shared logic in `scripts/harness.py`) copy the case fixtures into a git-initialised scratch dir, install every skill, run the agent and print the reply plus the files it created or changed. `--follow-up` turns continue the same session: Copilot `--continue`, Codex `codex exec resume --last`, OpenCode `run -c`.

**One plan running out never blocks testing.** When a harness is missing, not logged in, or reports a quota/credit/rate limit, the run stops with exit 75 and `HARNESS ERROR: <harness> ...`. That is not a skill result: rerun with another `--harness` or `--model`. There is no automatic fallback.

### GitHub Copilot CLI (default; verified 2026-10-29, Copilot CLI 1.0.105)

```bash
npm i -g @github/copilot
export GH_TOKEN=$(gh auth token)              # adapters do this when GH_TOKEN is unset
```

Copilot discovers `.agents/skills/` (also `.github/skills/`, `.claude/skills/`) and personal skills in `~/.copilot/skills/` or `~/.agents/skills/`; keep personal folders empty during evals. Runs use `copilot -p <prompt> --allow-all-tools`; without `-s` the output shows each tool call, which is how to confirm a bundled script ran. Each run spends Copilot AI credits (about 3–7).

### Codex CLI (the owner's ChatGPT/Codex account)

```bash
npm i -g @openai/codex
codex login                                   # or CODEX_API_KEY / OPENAI_API_KEY for one run
codex login status                            # exit 0 when logged in
```

Runs use `codex exec --sandbox workspace-write --skip-git-repo-check <prompt>` in the scratch dir (`--full-auto` is retired). Codex reads `.agents/skills/`. Not yet verified live.

### OpenCode (optional, any provider)

OpenCode is not tied to its free Zen models: `-m provider/model` runs any provider it is logged in to, e.g. `github-copilot/<model>` (Copilot subscription), `openai/<model>`, `openrouter/<model>`. Log in with `opencode auth login`; list with `opencode auth list` and `opencode models`. Without `--model`, OpenCode uses its configured default. Free models (`opencode/big-pickle`) hit "Free usage limit reached" after a few dozen cases and are not a default. OpenCode takes its project from `$PWD`; the adapter sets it and uses `.opencode/skills/`. Run cases serially.

### Manual multi-turn sessions

```bash
mkdir /tmp/cp && cd /tmp/cp && git init -q
npx -y skills add ~/path/to/career-skills --skill setup-career-skills -a github-copilot -y   # -> .agents/skills/
copilot -p "Use the setup-career-skills skill. ..." --allow-all-tools
copilot --continue -p "..." --allow-all-tools
```

Each case's synthetic files live in `tests/fixtures/<case-id>/` (regenerate with `python3 tests/make_fixtures.py`). Smoke cases are listed in `tests/eval-smoke.json`; score each `assessments[].status` as `pass`, `fail` or `unknown` with evidence, then `--review` (exit 0 all pass, 1 any fail, 2 any unscored). Transcripts are gitignored.

## Interpreting results

Run identical scenarios on each relevant harness. Record host/version, installed skill set, invocation evidence, resulting artifacts and access limits. Direct calls default to `$skill` syntax; adapt for hosts with different syntax.

Discovery scenarios do not name skills. Manual-only behavior is host-specific and not guaranteed across clients. Use an unassisted baseline when feasible. This smoke suite is a small regression check, not a statistical benchmark; human assessment remains necessary.

Workspace validation is a **discoverable structural exception handler**, not an always-on audit. Test both a task-driven broken path and a directly requested workspace review. The smoke set covers these plus a valid custom layout. Check the agent's skill-loading trace, status accuracy, write authorization, file/links verification, and return to the original task. A successful static test or fluent response alone does not prove delegation.

Negative smoke case `workspace-healthy-resume-no-helper` checks that working profile paths do not activate the validator while an ordinary resume task proceeds. The expected result is based on **invocation traces**, not just the assistant's final text.

The opt-in smoke set includes an explicit `ask-career-skills` navigation case. Review the returned recommendation and agent trace: the router should **recommend**, not invoke, other skills or write files.

**Standard workspace adoption smoke:** Test clean `career/` initialization from selected old sources, explicit physical migration of an occupied `career/`, and router selection for a first-time workspace. Verify actual file writes and absence of bulk copies, link integrity, preservation of originals, scope/approval, and no automatic publication. These scenarios remain opt-in agent tests, not proof of observed behavior.

Setup regression tests from a real agent session cover Git's deleted legacy paths after renaming an old career root, creation of only the needed standard home directories, and separation of role history (including internships) from assignments/project details. Review physical files and staged Git changes, not only an editor's deleted-path display. These remain behavioral scenarios requiring actual host execution.

**Guided onboarding lifecycle:** Test that `setup-career-skills` asks about existing sources at the outset, maintains a concise captured/missing/deferred checkpoint after a first successful import and offers a focused next question, and resumes from that checkpoint without repeating the interview. An index-only request is a valid explicit shortcut. A successful `patch` and link check do **not** prove the guided session is finished. Live-agent testing requires multi-turn observation; mock-runner tests verify only scenario packaging and plumbing.

For setup changes, run the three [live setup scenarios](../tests/SETUP-SCENARIOS.md) with `scripts/run_setup_scenarios.py`; results are recorded in that file.
