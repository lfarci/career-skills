# Behavioral evaluations

Structural CI checks packaging, frontmatter, references and case coverage. It cannot prove that agents select the correct skills or follow their instructions.

## Opt-in smoke suite

`tests/cases.json` contains synthetic scenarios covering every skill. `tests/eval-smoke.json` selects a small set for an actual agent run: automatic discovery, explicit invocation and unrelated negative cases.

1. Install the relevant skills into an isolated test workspace on the agent under test. Select the branch being reviewed and confirm nested leaf discovery; the Skills CLI accepts `npx skills add lfarci/career-skills --skill find-jobs` on the default branch. For pre-merge testing, use a local checkout or installer branch/ref support.
2. Configure an agent command or thin adapter that reads a user prompt from stdin and prints the response on stdout. Run it with the actual installed skills. The runner does **not** paste SKILL.md into the prompt.
3. Run the suite:

   ```bash
   python3 scripts/run_behavioral_evals.py --agent-command 'YOUR_AGENT_ADAPTER_COMMAND'
   ```

4. Inspect `eval-results/smoke.json`, responses, artifacts and available skill-loading/tool traces. Score each `assessments[].status` as `pass`, `fail` or `unknown`, with evidence. A response alone cannot prove whether a skill was loaded.
5. Summarize the scored results:

   ```bash
   python3 scripts/run_behavioral_evals.py --review eval-results/smoke.json
   ```

Exit status: 0 if all criteria pass, 1 if any fail, 2 if any remain unscored/unknown. Agent-command failures make the run fail. Transcripts are gitignored because they may contain sensitive output.

## OpenCode recipe (free model, headless)

```bash
curl -fsSL https://opencode.ai/install | bash        # installs ~/.opencode/bin/opencode
export PATH=$HOME/.opencode/bin:$PATH
opencode models | grep free                          # e.g. opencode/big-pickle, no credentials needed
mkdir -p /tmp/eval/.opencode/skills && cd /tmp/eval && git init -q
for f in $(find ~/path/to/career-skills/skills -name SKILL.md); do d=$(dirname $f); ln -sfn $d .opencode/skills/$(basename $d); done
# add a synthetic persona under ./old-notes, then:
opencode run -m opencode/big-pickle "I want to set up my private career workspace using setup-career-skills. My old notes are in ./old-notes."
opencode run -c -m opencode/big-pickle "Create it in a new folder named career here. Yes, you may read old-notes and write local files."
```

Symlinks make the checked-out branch the version under test. `-c` continues the last session for multi-turn flows. Inspect the files written under `career/`, not only the reply.

### Smoke set through the runner

```bash
cd /tmp   # never from the checkout
for id in $(python3 -c "import json;s=json.load(open('$REPO/tests/eval-smoke.json'));print(' '.join(c['id'] for k in ('existing_cases','negative_cases') for c in s[k]))"); do
  python3 $REPO/scripts/run_behavioral_evals.py --agent-command "python3 $REPO/scripts/opencode_adapter.py" \
    --case-id $id --harness-label "opencode big-pickle" --timeout 420 --output /tmp/evr/$id.json
done
```

Each case's synthetic files live in `tests/fixtures/<case-id>/` (regenerate with `python3 tests/make_fixtures.py`); the runner copies them into the case's scratch directory and adapters copy their cwd into their own workdir. For Copilot use `--agent-command "python3 $REPO/scripts/copilot_adapter.py"`; each case costs Copilot AI credits, so run the full set only with the owner's approval.

Run cases one at a time: concurrent free-model runs returned empty replies. OpenCode takes its project from `$PWD`, so the adapter and runner set it to a fresh scratch dir; with only `cwd` changed, agents wrote into the checkout.

### GitHub Copilot CLI (verified 2026-10-29, Copilot CLI 1.0.105)

```bash
npm i -g @github/copilot                      # `copilot` binary
export GH_TOKEN=$(gh auth token)              # reuses an existing `gh` login with Copilot access
mkdir /tmp/cp && cd /tmp/cp && git init -q
npx -y skills add ~/path/to/career-skills --skill setup-career-skills -a github-copilot -y   # -> .agents/skills/
copilot skill list                            # confirm the skill is listed under Project skills
copilot -p "Use the setup-career-skills skill. ..." --allow-all-tools      # add -s for the reply only
copilot --resume=<id> -p "..." --allow-all-tools                          # continue a session
```

Copilot discovers project skills in `.github/skills/`, `.agents/skills/` or `.claude/skills/`, and personal ones in `~/.copilot/skills/` or `~/.agents/skills/`; keep the personal folders empty during evals so only the installed skills are used. In prompt mode Copilot cannot load skills marked `disable-model-invocation: true` (ask-career-skills and the personal-brand skills) through its skill tool, and `/skill-name` is not expanded; it then reads the SKILL.md from `.agents/skills/` itself, which worked in every smoke case. Without `-s` the output shows each tool call, which is how to confirm a bundled script ran. Verified: setup import, validate-workspace running `scripts/check_workspace.py`, and build-resume compiling a PDF with Tectonic.

### Other harnesses

Free Zen models answer only through the OpenCode client (direct API calls return `FreeUsageLimitError`), so other harnesses need their own credentials:

- **Codex CLI** (`npm i -g @openai/codex`): `codex login` (ChatGPT plan) or `OPENAI_API_KEY`; install skills with `npx skills add lfarci/career-skills --skill <name> -a codex`; run `codex exec "<prompt>"`.
- **Claude Code** (`npm i -g @anthropic-ai/claude-code`): Anthropic login or `ANTHROPIC_API_KEY`; install with `-a claude-code`; run `claude -p "<prompt>"`.

## Interpreting results

Run identical scenarios on each relevant harness. Record host/version, installed skill set, invocation evidence, resulting artifacts and access limits. Direct calls default to `$skill` syntax; adapt for hosts with different syntax.

Discovery scenarios do not name skills. Manual-only behavior is host-specific and not guaranteed across clients. Use an unassisted baseline when feasible. This smoke suite is a small regression check, not a statistical benchmark; human assessment remains necessary.

Workspace validation is a **discoverable structural exception handler**, not an always-on audit. Test both a task-driven broken path and a directly requested workspace review. The smoke set covers these plus a valid custom layout. Check the agent's skill-loading trace, status accuracy, write authorization, file/links verification, and return to the original task. A successful static test or fluent response alone does not prove delegation.

Negative smoke case `workspace-healthy-resume-no-helper` checks that working profile paths do not activate the validator while an ordinary resume task proceeds. The expected result is based on **invocation traces**, not just the assistant's final text.

The opt-in smoke set includes an explicit `ask-career-skills` navigation case. Review the returned recommendation and agent trace: the router should **recommend**, not invoke, other skills or write files.

**Standard workspace adoption smoke:** Test clean `career/` initialization from selected old sources, explicit physical migration of an occupied `career/`, and router selection for a first-time workspace. Verify actual file writes and absence of bulk copies, link integrity, preservation of originals, scope/approval, and no automatic publication. These scenarios remain opt-in agent tests, not proof of observed behavior.

Setup regression tests from a real OpenCode session cover Git's deleted legacy paths after renaming an old career root, creation of only the needed standard home directories, and separation of role history (including internships) from assignments/project details. Review physical files and staged Git changes, not only an editor's deleted-path display. These remain behavioral scenarios requiring actual host execution.

**Guided onboarding lifecycle:** Test that `setup-career-skills` asks about existing sources at the outset, maintains a concise captured/missing/deferred checkpoint after a first successful import and offers a focused next question, and resumes from that checkpoint without repeating the interview. An index-only request is a valid explicit shortcut. A successful `patch` and link check do **not** prove the guided session is finished. Live-agent testing requires multi-turn observation; mock-runner tests verify only scenario packaging and plumbing.

For setup changes, run the three [live setup scenarios](../tests/SETUP-SCENARIOS.md) with `scripts/run_setup_scenarios.py`; results are recorded in that file.
