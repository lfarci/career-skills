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
