# Career Skills: agent guide

Public repo of small [Agent Skills](https://agentskills.io/) that help one person turn scattered career notes into a **private** `career/` workspace and use it: facts, direction, growth, brand, resumes, job search. This repo ships instructions only; the user's data lives in their own private workspace.

## Mental model

The workspace has an **index** (`career/README.md`: links, source inventory, setup progress) and **canonical records** in five homes: `profile/` (facts, direction, preferences, development), `projects/` (assignments and side projects), `brand/` (positioning, visual guidance), `assets/` (drafts and approved reusable outputs), `research/` (saved companies, jobs, comparators). The index points; records hold facts. Details: [docs/WORKSPACE.md](docs/WORKSPACE.md).

Skill groups under `skills/`, each owning one question:

- `setup-career-skills`: create, import into or resume the workspace (the entry point).
- `career-evidence/`: what have I demonstrated? (`maintain-profile` owns facts.)
- `career-direction/`: what do I want? (`reflect`)
- `career-development/`: how do I grow? (`plan-development`: create or review a plan)
- `personal-brand/`: how do I present myself? (positioning, design brief → assets → review, audits)
- `job-hunt/`: how do I get there? (`build-resume`, `find-companies`, `find-jobs`)
- `ask-career-skills` (router: recommends, never runs) and `validate-workspace` (structural repair) are top-level helpers.

Groups are folders, not skills. Every leaf installs and runs alone.

## Priorities

Aim for a stable MVP: fewer, rock-solid skills over richness. Simplify or remove a skill when it adds little.

1. **Workspace creation and profile import**: `setup-career-skills`, `maintain-profile`, `validate-workspace`, and the `career/` contracts (record map, index, paths).
2. **Visual identity**: `personal-brand`, `define-design-brief`, `create-design-assets`, `review-design`.
3. **Opportunities**: `find-companies`, `find-jobs`, `build-resume`.

Secondary: `audit`, `plan-development`, `reflect` (kept: sole owner of profile/direction.md, which brand and job search consume), `ask-career-skills` (kept: router for the manual skills, zero context load). Removed for the MVP: `benchmark-profile`, `review-research`, `review-progress` (merged); re-add only with a demonstrated need.

## Quality bar for a skill

- **Distinct purpose**: one trigger, one responsibility, one completion boundary. A different platform, format or count (one vs. many) is a branch inside a skill, not a new skill. Merge or remove a skill that fails this; justify it in an issue.
- **Preserve the mental model**: facts, goals, positioning and publication stay separate; each fact has one canonical record; writes need permission and are verified.
- **Host-neutral wording**: no transcript-specific folder names or harness tool names in a SKILL.md. Fix the rule, not the test case.
- **Checkable `## Done when`** and a short `## Contract` (Input / Scope / Output).
- Write per Matt Pocock's [writing-for-agents](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents): descriptions are trigger pointers, positive phrasing, push branch-only material into `references/`.

### Scripts in skills

Use a script when a check or transform is deterministic (workspace index/link checks, templates); the SKILL.md tells the agent to run it and gives a by-reading fallback.

- Ship it inside the skill that uses it: `skills/<group>/<skill>/scripts/`, referenced from SKILL.md as `scripts/<name>.py`, so `npx skills add … --skill <name>` installs it. No cross-skill imports or repo paths at runtime; when two skills need one helper, keep verbatim copies (validator checks they match).
- Python 3 standard library only, cross-platform (`pathlib`, UTF-8, no shell-outs), harness-agnostic.
- Follow [PEP 8](https://peps.python.org/pep-0008/) and the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html): type hints, `argparse` CLI, small functions with docstrings, text plus `--json` output, exit codes 0 ok / 1 findings / 2 unusable input.
- Unit tests in `tests/test_<script>.py`. Check installs with `npx -y skills add <checkout> --skill <name> -a opencode -y` in a scratch dir.

Boundaries and invocation policy: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Routing and first session: [docs/USER-JOURNEY.md](docs/USER-JOURNEY.md). Terms: [GLOSSARY.md](GLOSSARY.md).

## Change workflow

1. Open or reuse a GitHub issue (problem, evidence with paths/quotes, fix, acceptance criteria).
2. One focused branch and PR per issue, body `Fixes #N`.
3. When responsibilities or triggers change, update `tests/cases.json`, README tables, docs and the `EXPECTED`/`MANUAL` sets in `scripts/validate_skills.py`.
4. Run `python3 scripts/validate_skills.py` and `python3 -m unittest discover -s tests -p 'test_*.py'` (needs `pyyaml`).
5. For behavior changes, run a live agent ([docs/EVALUATION.md](docs/EVALUATION.md)); static checks prove packaging only.

Evaluate at two levels, both with a synthetic persona in a scratch dir outside the repo:

- **Per skill**: each user-triggerable skill alone, from a natural prompt, checking its contract and `Done when`.
- **Full flow**: setup, then the priority skills on the same workspace, checking integration: shared files land where the record map says, the index contract holds (paths relative to root, section ownership), formats stay consistent, and no skill copies another's records.

Use synthetic personas only; keep real personal data out of this repo.

## Learnings

Append one dated line per lesson when you discover a problem worth not repeating.

- 2026-10-29: A fast path that listed "create exactly README + experience.md" made models dump every other fact into the index. Give setup an explicit fact → record map.
- 2026-10-29: Patching SKILL.md with phrases from one failing transcript (folder names, `question` tool, OpenCode paths) bloats the skill and generalizes poorly; state the host-neutral rule instead.
- 2026-10-29: Downstream skills copy the workspace's shape: if setup stores facts in README, `maintain-profile` edits README too. Fix the producer.
- 2026-10-29: OpenCode with the free `opencode/big-pickle` model runs skills headless and discovers `.opencode/skills/<name>/SKILL.md` symlinks to this checkout, so branch edits are tested live (see docs/EVALUATION.md).
- 2026-10-29: Shared files need an explicit owner. Without one, `personal-brand` rewrote setup's progress checkpoint and setup wrote source paths relative to the agent's start dir instead of the root.
- 2026-10-29: `audit-surface` vs `audit` was a count (one vs. many), not a responsibility; merged into `audit`.
- 2026-10-29: A contract that lives in one skill is invisible to the others; standalone `maintain-profile` invented a single `profile.md`. Shared contracts live in docs/WORKSPACE.md with validator-checked verbatim copies in the skills that write them.
- 2026-10-29: Deterministic checks belong in a shipped script, not prose: setup now runs `scripts/check_workspace.py`, and OpenCode found and ran it from the npx-installed `.agents/skills/` copy.
- 2026-10-29: Loading a module with `importlib` for tests requires registering it in `sys.modules` before `exec_module` when it defines dataclasses.
- 2026-10-29: Every file-producing skill needs a naming contract plus a check; without one a single session mixed `option-a_v1` and `at-a-v1` names and left render helpers in assets/.
- 2026-10-29: Free test models are often text-only; visual skills need an explicit can't-see-images branch or they burn the turn on improvised pixel analysis.
- 2026-10-29: Cut to 14 skills for the MVP; a removed skill's durable rules (e.g. research retention) stay in docs/WORKSPACE.md so nothing is lost.
- 2026-10-29: Web-search skills need an explicit stopping rule; without one find-jobs retried blocked sites (403/429) until timeout. With it, the run finished in ~2 min with 2 verified roles.
- 2026-10-29: A rule placed in a later section (`## Resume`) loses to the step the agent is executing; put stop-and-ask gates inside the step that routes to them. "Resume setup" is not approval to restructure.
- 2026-10-29: A fixed record header (Status/Checked/Source) in a references/ template made a free model's research records uniform on the first try; prefer templates over scripts until drift is shown.
- 2026-10-29: Without an explicit tool boundary, find-jobs scripted curl over 20 listing pages; say "host web tools, one page at a time".
- 2026-10-29: Weak free models (nemotron-lightning, flint) fail on harness behaviour (sub-agents wandering, out-of-dir writes), not skill wording. Record them in tests/SETUP-SCENARIOS.md; fix only what a host-neutral rule or a checker catches (e.g. empty records).
- 2026-10-29: OpenCode Zen free models work only inside the OpenCode client; pointing Codex at the Zen endpoint returns FreeUsageLimitError. A second harness needs the user's Codex or Claude login.
