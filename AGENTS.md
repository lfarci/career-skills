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
- 2026-10-29: "Approved" carries over between deliverables unless the skill says selection is per kind; an approved logo made the agent skip banner concepts.
- 2026-10-29: Two skills that repair the same files need one shared, validator-checked rule; otherwise one fixes the link and the other renames the file. A saved write policy is not a request to write.
- 2026-10-29: Tests that hard-code case counts or old ids break on every prune; assert the current core contracts instead.
- 2026-10-29: Give agents a build script, not a format: with `build_resume.py` a free model produced a verified one-page PDF first try, but it put dates inside `organization` until SKILL.md showed a JSON example and the script warned about empty `dates`. Exit codes (0 PDF, 3 no engine) keep agents from claiming a PDF that does not exist.
- 2026-10-29: OpenCode resolves its project from `$PWD`, not the process cwd; an eval harness that only sets `cwd=` lets agents write into the caller's repo. Set both, run free-model cases serially (parallel runs returned empty replies), and check `git status` after every eval.
- 2026-10-29: XeTeX/Tectonic cannot load variable fonts (most Google Fonts installs), so a brand font "installed" per fc-list can still break the build; check for static files first and retry without each font. Scripts should also skip and flag empty sections: a free model left Education empty while the record existed.
- 2026-10-29: `subprocess.run(timeout=)` kills only the direct child; an adapter's `opencode run` grandchild survived 13 min past its limit and overlapped the next case. Start agents in their own process group and kill the tree.
- 2026-10-29: GitHub Copilot CLI runs the skills unchanged (it reads `.agents/skills/`, which `npx skills add -a github-copilot` writes) and authenticates with `GH_TOKEN=$(gh auth token)`. Setup, check_workspace.py and build_resume.py all worked first try, so the skills and scripts are harness-agnostic. Copilot used about 3–7 AI credits per run.
- 2026-10-29: Job boards (Indeed, StepStone, Jobat, Glassdoor) and many employer sites return 403/429 to agents, and LinkedIn's ToS forbid scraping; public ATS board APIs (Greenhouse, Lever, Ashby, Recruitee, SmartRecruiters) answer 200 JSON. Storing `Jobs board: <ats>:<slug>` in company records let find-jobs' `search_jobs.py` return 11 verified Belgian openings in 5 s, and big-pickle used it unprompted.
- 2026-10-29: A contract gap shows up only when a downstream skill needs the fact: Copilot built resume.json from a complete workspace but stopped at "name is required" because no record owned the name. Every fact a skill consumes needs a row in the record map.
- 2026-10-29: Eval prompts that describe files need those files: without fixtures 15 of 38 cases were unscoreable or sent the agent hunting through other folders. Fixtures also exposed their own bugs (an invalid `Status: complete`), so validate fixtures with the same checker the skills use.
- 2026-10-29: With the root confirmed and no sources mentioned, Copilot asked about the current role first and offered existing files as an aside. Setup now asks whether existing material exists, and where, before any role-history question (#72).
- 2026-10-29: OpenCode's free big-pickle model hits a "Free usage limit reached" error after a few dozen cases; `opencode run` then retries silently until the runner's timeout (exit 124). Before counting a timeout as a skill result, grep ~/.local/share/opencode/log/ for that message. The adapter now stops on it and exits 75 with "HARNESS ERROR" (#77).
- 2026-10-29: `disable-model-invocation: true` made manual skills unreachable in Copilot CLI prompt mode even when named, and Codex/OpenCode v1 ignore it. Manual intent now lives in the description plus Codex's openai.yaml (#75).
- 2026-10-29: Given "approve whatever you draft", personal-brand staged a new title over the previous employer's work and a one-source leadership claim; the audit caught both. Blanket approval covers wording, not unverified claims (#79).
- 2026-10-29: `npx skills add lfarci/career-skills --skill '*' -y --copy -a <agent>` installs all 14 skills for opencode, github-copilot and codex (.agents/skills/) and claude-code (.claude/skills/); the README Getting started is tested against that (#81).
