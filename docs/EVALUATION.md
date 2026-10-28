# Behavioral evaluations

Structural CI checks packaging, frontmatter, references and case coverage. It cannot prove that agents select the correct skills or follow their instructions.

## Opt-in smoke suite

`tests/cases.json` contains synthetic scenarios covering all 16 skills. `tests/eval-smoke.json` selects a small set for an actual agent run: automatic discovery, explicit invocation and unrelated negative cases.

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

## Interpreting results

Run identical scenarios on each relevant harness. Record host/version, installed skill set, invocation evidence, resulting artifacts and access limits. Direct calls default to `$skill` syntax; adapt for hosts with different syntax.

Discovery scenarios do not name skills. Manual-only behavior is host-specific and not guaranteed across clients. Use an unassisted baseline when feasible. This smoke suite is a small regression check, not a statistical benchmark; human assessment remains necessary.

Workspace validation is a **discoverable structural exception handler**, not an always-on audit. Test both a task-driven broken path and a directly requested workspace review. The smoke set covers these plus a valid custom layout. Check the agent's skill-loading trace, status accuracy, write authorization, file/links verification, and return to the original task. A successful static test or fluent response alone does not prove delegation.

Negative smoke case `workspace-healthy-resume-no-helper` checks that working profile paths do not activate the validator while an ordinary resume task proceeds. The expected result is based on **invocation traces**, not just the assistant's final text.

The opt-in smoke set includes an explicit `ask-career-skills` navigation case. Review the returned recommendation and agent trace: the router should **recommend**, not invoke, other skills or write files.

**Standard workspace adoption smoke:** Test clean `career/` initialization from selected old sources, explicit physical migration of an occupied `career/`, and router selection for a first-time workspace. Verify actual file writes and absence of bulk copies, link integrity, preservation of originals, scope/approval, and no automatic publication. These scenarios remain opt-in agent tests, not proof of observed behavior.

Setup regression tests from a real OpenCode session cover Git's deleted legacy paths after renaming an old career root, creation of only the needed standard home directories, and separation of role history (including internships) from assignments/project details. Review physical files and staged Git changes, not only an editor's deleted-path display. These remain behavioral scenarios requiring actual host execution.

**Guided onboarding lifecycle:** Test that `setup-career-skills` asks about existing sources at the outset, maintains a concise captured/missing/deferred checkpoint after a first successful import and offers a focused next question, and resumes from that checkpoint without repeating the interview. An index-only request is a valid explicit shortcut. A successful `patch` and link check do **not** prove the guided session is finished. Live-agent testing requires multi-turn observation; mock-runner tests verify only scenario packaging and plumbing.
