# Career Skills: agent guide

Public repo of small [Agent Skills](https://agentskills.io/) that help one person turn scattered career notes into a **private** `career/` workspace and use it: facts, direction, growth, brand, resumes, job search. This repo ships instructions only; the user's data lives in their own private workspace.

## Mental model

The workspace has an **index** (`career/README.md`: links, source inventory, setup progress) and **canonical records** in five homes: `profile/` (facts, direction, preferences, development), `projects/` (assignments and side projects), `brand/` (positioning, visual guidance), `assets/` (drafts and approved reusable outputs), `research/` (saved companies, jobs, comparators). The index points; records hold facts. Details: [docs/WORKSPACE.md](docs/WORKSPACE.md).

Skill groups under `skills/`, each owning one question:

- `setup-career-skills`: create, import into or resume the workspace (the entry point).
- `career-evidence/`: what have I demonstrated? (`maintain-profile` owns facts; `review-research` maintains saved research.)
- `career-direction/`: what do I want? (`reflect`)
- `career-development/`: how do I grow? (`plan-development`, `review-progress`)
- `personal-brand/`: how do I present myself? (positioning, design brief → assets → review, audits, benchmarking)
- `job-hunt/`: how do I get there? (`build-resume`, `find-companies`, `find-jobs`)
- `ask-career-skills` (router: recommends, never runs) and `validate-workspace` (structural repair) are top-level helpers.

Groups are folders, not skills. Every leaf installs and runs alone.

## Priorities

Aim for a stable MVP: fewer, rock-solid skills over richness. Simplify or remove a skill when it adds little.

1. **Workspace creation and profile import**: `setup-career-skills`, `maintain-profile`, `validate-workspace`, and the `career/` contracts (record map, index, paths).
2. **Visual identity**: `personal-brand`, `define-design-brief`, `create-design-assets`, `review-design`.
3. **Opportunities**: `find-companies`, `find-jobs`, `build-resume`.

Nice-to-have, first candidates for simplification or removal: `benchmark-profile`, `review-research`, `audit`, `plan-development`, `review-progress`, `reflect`, `ask-career-skills`.

## Quality bar for a skill

- **Distinct purpose**: one trigger, one responsibility, one completion boundary. A different platform, format or count (one vs. many) is a branch inside a skill, not a new skill. Merge or remove a skill that fails this; justify it in an issue.
- **Preserve the mental model**: facts, goals, positioning and publication stay separate; each fact has one canonical record; writes need permission and are verified.
- **Host-neutral wording**: no transcript-specific folder names or harness tool names in a SKILL.md. Fix the rule, not the test case.
- **Checkable `## Done when`** and a short `## Contract` (Input / Scope / Output).
- Write per Matt Pocock's [writing-for-agents](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents): descriptions are trigger pointers, positive phrasing, push branch-only material into `references/`.

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
