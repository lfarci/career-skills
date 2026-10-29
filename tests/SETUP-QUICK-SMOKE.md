# Setup quick smoke: natural two-turn onboarding

**Purpose:** Test the minimal real-user prompt and chosen-folder semantics in a disposable repository. Test resumption separately with `setup-resume-invalid-workspace-before-import`.

For small-model cases with reproducible prompts, expected behavior, and trace-based scoring, see [Manual setup scenarios for small models](SETUP-SMALL-MODEL-SCENARIOS.md).

**Preparation:** Install/load the `skills/setup-career-skills/SKILL.md` revision under test into a **fresh agent session**. Use a disposable test workspace, not the user's existing notes. Verify the loaded skill revision (do not accidentally exercise the last installed `main` version). Keep the same agent session across both turns. This is a **live manual test**, not an existing CI evaluation or a substitute for OpenCode-specific tool traces.

## Turn 1: no sources supplied

Send this user request without any other setup instructions:

> Use setup-career-skills to help me set up my career workspace.

**Expected:** Agent first asks **where to initialize**, without assuming the current repository or inspecting existing records.

## Turn 2: folder selection

Reply **in the same agent session**:

> Create a folder named `career-workspace` here.

**Expected:** The agent treats `career-workspace/` as the workspace **root**; it must not invent `career-workspace/career/`. It may inspect the chosen target and ask about existing sources, but should not count an empty folder as completed setup. A later approved import should create `career-workspace/README.md` plus meaningful records directly under its standard homes.

## Scorecard

| Check | Pass condition |
| --- | --- |
| Destination | First turn asks the user where to initialize, even if a career folder seems available |
| Exact root | The named folder is the root; no unrequested nested `career/` |
| Useful setup | Directory creation alone is not setup completion; next question concerns relevant sources |
| Continue | Agent asks **one** useful follow-up question without restarting |
| Session continuity | Does not restart the interview or repeat previously answered questions |

Record the agent/version, PR commit, final responses and visible skill-loading trace. **Pass only on observed output**, not on the presence of guidance in SKILL.md. If the agent loads an old installed copy, mark the test invalid rather than failed. The first useful failure should lead to one focused skill edit, followed by another two-turn run.

Useful related scenarios: `setup-named-folder-is-root`, `setup-consolidation-is-not-lossless`, `setup-cutover-checks-inbound-links`, `setup-first-batch-does-not-end-intake`. For broader opt-in evaluations, see [Behavioral evaluations](../docs/EVALUATION.md).
