# Setup quick smoke: two-turn feedback loop

**Purpose:** Check the conversational behavior of PR #13's `setup-career-skills` in a real agent host without migrating actual career records.

**Preparation:** Install/load `skills/setup-career-skills/SKILL.md` from the PR branch into a **fresh agent session**. Use a disposable test workspace, not the user's existing notes. Verify the loaded skill revision (do not accidentally exercise the last installed `main` version). Keep the same agent session across both turns. This is a **live manual test**, not an existing CI evaluation or a substitute for OpenCode-specific tool traces.

## Turn 1: no sources supplied

Send this user request without any other setup instructions:

> Use `setup-career-skills` to help me start a private career workspace. My test repository has no career files yet. For now, let's discuss it without writing anything.

**Expected:** Agent makes a concrete start and asks **one useful question**, preferably about existing career sources or where they can be found. It should not create files, generate an extensive generic questionnaire, or claim setup is complete.

## Turn 2: selected source details

Reply **in the same agent session**:

> I have an old CV and project notes. For this synthetic test, the CV lists an internship at Northstar Labs (June–August 2022) and a full-time software engineer position at Atlas Software (September 2022–present). The project notes describe a customer cloud migration I worked on during my Atlas employment. Start by drafting work experience from these details. Do not edit files yet.

**Expected:** Agent drafts or proposes role-history content **including the internship**, keeps the customer migration as an assignment/project rather than a separate employer, and distinguishes source claims from independently verified evidence. It then gives a **brief checkpoint** (captured, missing/uncertain or deferred) and asks the next high-value question instead of treating this first batch as full onboarding completion. It must not claim any file was saved.

## Scorecard

| Check | Pass condition |
| --- | --- |
| Discover | First turn asks about existing sources or access without a long form |
| Respect scope | No file writes in either read-only turn; no claimed writes |
| Preserve facts | Internship and full-time role remain distinct; client assignment does not become another employer |
| Continue | After the draft, agent identifies a meaningful gap or next area and asks **one** follow-up question |
| Session continuity | Does not restart the interview or repeat previously answered questions |

Record the agent/version, PR commit, final responses and visible skill-loading trace. **Pass only on observed output**, not on the presence of guidance in SKILL.md. If the agent loads an old installed copy, mark the test invalid rather than failed. The first useful failure should lead to one focused skill edit, followed by another two-turn run.

Useful related scenarios: `setup-asks-about-existing-sources`, `setup-first-batch-does-not-end-intake`, `setup-role-history-with-internships`. For broader opt-in evaluations, see [Behavioral evaluations](../docs/EVALUATION.md).
