# Skills

Small, composable [Agent Skills](https://agentskills.io/) for understanding, maintaining, and presenting a professional identity—and finding suitable opportunities.

Each skill works independently and does not require GitHub, a particular AI harness, a proprietary profile format, or another skill. Skills use the tools the user's environment makes available; when a capability is missing, they produce a reviewable local output instead of claiming to have taken an action.

## Skill list

| Skill | Purpose | Invocation |
| --- | --- | --- |
| [`setup-career-skills`](../skills/setup-career-skills/SKILL.md) | Create or resume a private career workspace from selected sources | Discoverable |
| [`ask-career-skills`](../skills/ask-career-skills/SKILL.md) | Recommend which career workflow to use after setup or at any point | Manual |
| [`validate-workspace`](../skills/validate-workspace/SKILL.md) | Validate workspace structure or repair broken mappings during another task | Discoverable |
| [`reflect`](../skills/career-direction/reflect/SKILL.md) | Explore and articulate professional identity and goals | Manual |
| [`maintain-profile`](../skills/career-evidence/maintain-profile/SKILL.md) | Ask for a focus when needed, then review or update factual career records | Discoverable |
| [`build-resume`](../skills/job-hunt/build-resume/SKILL.md) | Author, tailor, and validate truthful resumes | Discoverable |
| [`plan-development`](../skills/career-development/plan-development/SKILL.md) | Create a growth plan or review progress against it | Manual |
| [`personal-brand`](../skills/personal-brand/personal-brand/SKILL.md) | Choose the role and strengths to show publicly and on which surfaces; draft headlines, bios, LinkedIn About and GitHub README text | Manual |
| [`visual-identity`](../skills/personal-brand/visual-identity/SKILL.md) | Record or design a design system (palette, fonts, UI rules) and assets (logo, banners), or review them | Manual |
| [`audit`](../skills/personal-brand/audit/SKILL.md) | Audit one or several professional surfaces for facts, consistency and visual drift | Discoverable |
| [`find-companies`](../skills/job-hunt/find-companies/SKILL.md) | Research employers matching career direction, location and constraints, with or without vacancies | Discoverable |
| [`find-jobs`](../skills/job-hunt/find-jobs/SKILL.md) | Find and verify live vacancies matching the user's profile | Discoverable |

**Manual** means the user selects the named skill; **Discoverable** means an agent may select it for a matching task. Manual skills say so in their description and set Codex's `allow_implicit_invocation: false`; they omit `disable-model-invocation`, which on some hosts makes a skill unreachable even by name. See the [invocation policy](ARCHITECTURE.md#invocation-policy).

## Organization

| Directory | Responsibility | Skills |
| --- | --- | --- |
| `career-direction/` | What do I want, and why? Private north star, interests and decisions | `reflect` |
| `career-evidence/` | What have I demonstrated? Experience, achievements and supporting records | `maintain-profile` |
| `career-development/` | How do I grow toward it? Action plans, practice and progress | `plan-development` |
| `personal-brand/` | Public presentation: content and surfaces, visual identity, live-surface checks | `personal-brand`, `visual-identity`, `audit` |
| `job-hunt/` | Application materials and opportunity search | `build-resume`, `find-jobs`, `find-companies` |
| `setup-career-skills/` | Cross-cutting workspace setup | `setup-career-skills` |
| `ask-career-skills/` | Optional navigation among independent skills | `ask-career-skills` |
| `validate-workspace/` | On-demand structural validation and mapping repairs | `validate-workspace` |

Groups organize the repository; they are not installable umbrella skills. Install individual leaf directories. Paths for previously top-level skills have moved into their groups; update installation sources accordingly.

## Brand area

Profile is the private truth. `personal-brand` is its public facet: which role and strengths to put forward, which surfaces to target (`brand/surfaces.md`: GitHub, personal site, LinkedIn, Credly, Microsoft Learn…) and the text for each. `visual-identity` is how that brand looks: design system, brand tokens (read by `build-resume`) and assets. `audit` checks live surfaces against all three.

Removed for the MVP: `benchmark-profile` and `review-research` (research retention rules stay in docs/WORKSPACE.md); `review-progress` is now the review branch of `plan-development`. `audit-surface` was merged into `audit` (one or several surfaces). `define-design-brief`, `create-design-assets` and `review-design` were merged into `visual-identity`; the visual brand kit moved from `personal-brand` to it (#99).

## Design principles

- **Facts, goals, and positioning are different:** a verified job history is not an aspiration or a marketing claim.
- **One canonical record:** in a managed workspace, selected facts have one authoritative record under the standard `career/` homes. Earlier documents remain linked sources, not competing managed copies.
- **Independently useful:** a skill can work with pasted documents even without a preconfigured workspace.
- **Verify, don't invent:** preserve source links, date qualifiers, uncertainty, and claims that cannot be confirmed.
- **Reviewable mutations:** do not silently publish, apply for a job, alter public profiles, or create tracker items without authorization.
- **No mandatory provider:** files, repositories, issue trackers, and web integrations are replaceable capabilities.

## Shared career workspace

The entire workspace is private, including material prepared for public use. Its five homes are **profile/** (background, capabilities, direction and development), **projects/** (work accounts and evidence links), **brand/** (positioning, target surfaces and visual identity), **assets/** (drafts and approved staged copy, visuals and resumes), and **research/** (selected companies, opportunities and comparable profiles).

A managed workspace uses the **physical** `career/` root with these standardized directory names, creating each home when needed. `career/README.md` is its entry point and can map homes not yet populated. Existing resumes, old notes, project records and profile exports are potential **sources** to populate new canonical Markdown records: select and verify them rather than bulk-copying or silently moving the originals. Reuse approved assets; staged material is not proof of publication. Research is retained selectively.

Use a private local folder, GitHub repository or another Markdown-capable provider. `setup-career-skills` defaults to a **fresh `career/`** in a selected private location; if one already exists, it offers a different destination or a planned, approved migration in place. An existing custom layout remains usable while migration is pending, and standalone task skills never require setup. See [workspace initialization and adoption](WORKSPACE.md#initialize-from-existing-sources).

When an active skill encounters a **broken source mapping or link**, it may load `validate-workspace` for a scoped repair, **if installed and supported by the agent host**. Direct user requests for workspace validation are supported too. An existing layout with working paths should not be migrated during unrelated tasks; users can request physical alignment explicitly. See the [task execution flow](ARCHITECTURE.md#task-execution-flow).

For agent-driven repair during other skills, install `validate-workspace` alongside those leaf skills (for example, `npx skills add lfarci/career-skills --skill validate-workspace`). Installing a task skill alone does not install the helper; its absence should never block the task.

The [workspace decision specification](CAREER-WORKSPACE-SPEC.md) captures the agreed behavior, rejected alternatives, testing boundaries and deferred work.

## Example: adopting an old career tree

An existing `career/personal-projects/`, `career/personal-brand/` and root `career/services.md` can remain as source material while the user reviews a proposed move to `career/projects/`, `career/brand/` and `career/brand/surfaces.md`. The agent inventories content and links, gets approval, then verifies the chosen changes in a reviewable PR. **No files in the public Career Skills repository are migrated by this documentation change.**

## After setup: suggested journey

There is **no required flow** after `setup-career-skills`. Reconcile facts with `maintain-profile` if needed, clarify direction with `reflect` if needed, then work directly on development, brand, job search or research.

See the [user journey with Mermaid diagram and routing guide](USER-JOURNEY.md). Use `ask-career-skills` at any time for a single recommended next action, without invoking any other skill.

Configuration discovered during setup belongs in the **user's chosen private workspace**, not in this public skill repository. See [architecture and contracts](ARCHITECTURE.md), [workspace](WORKSPACE.md), [user journey](USER-JOURNEY.md) and [evaluation cases](../tests/cases.json).

## Scope and status

This is an initial **behavioral-specification release**. The skill packages contain instructions and acceptance criteria, and a lightweight static validator checks the packaging. A full cross-harness benchmark and live integration tests are future work. Resume rendering requires an environment with suitable export tools; job discovery requires current-accessible job sources.

## Validation

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

This checks packaging, references, invocation intent and scenario inventory. It does not run an agent. See [behavioral evaluations](EVALUATION.md) for live-agent smoke runs and human review.
