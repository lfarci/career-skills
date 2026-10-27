# Career Skills

Small, composable [Agent Skills](https://agentskills.io/) for understanding, maintaining, and presenting a professional identity—and finding suitable opportunities.

Each skill works independently and does not require GitHub, a particular AI harness, a proprietary profile format, or another skill. Skills use the tools the user's environment makes available; when a capability is missing, produce a reviewable local output instead of claiming to have taken an action.

## Skills

| Skill | Purpose | Invocation |
| --- | --- | --- |
| [`setup-career-skills`](skills/setup-career-skills/SKILL.md) | Discover existing records, assets, preferences, and progress tracker | Manual |
| [`reflect`](skills/career-direction/reflect/SKILL.md) | Explore and articulate professional identity and goals | Manual |
| [`maintain-profile`](skills/career-evidence/maintain-profile/SKILL.md) | Reconcile evidence and maintain factual career records | Discoverable |
| [`build-resume`](skills/job-hunt/build-resume/SKILL.md) | Author, tailor, and validate truthful resumes | Discoverable |
| [`plan-development`](skills/career-development/plan-development/SKILL.md) | Turn career direction and evidence gaps into a feasible growth plan | Manual |
| [`review-progress`](skills/career-development/review-progress/SKILL.md) | Review development evidence and adjust the plan | Manual |
| [`personal-brand`](skills/personal-brand/personal-brand/SKILL.md) | Define positioning, coordinate public messaging, and optionally maintain a small reusable visual brand kit | Manual |
| [`define-design-brief`](skills/personal-brand/define-design-brief/SKILL.md) | Interview about career visual needs and agree on an actionable brief | Manual |
| [`create-design-assets`](skills/personal-brand/create-design-assets/SKILL.md) | Explore concepts and produce scoped professional visual assets | Manual |
| [`benchmark-profile`](skills/personal-brand/benchmark-profile/SKILL.md) | Research relevant public profiles and resumes for evidence-backed improvements | Manual |
| [`review-design`](skills/personal-brand/review-design/SKILL.md) | Critique visual fit, craft and readiness against the brief | Manual |
| [`audit-surface`](skills/personal-brand/audit-surface/SKILL.md) | Audit an individual professional asset | Discoverable |
| [`audit`](skills/personal-brand/audit/SKILL.md) | Audit factual and observable visual alignment across multiple professional assets | Manual |
| [`review-research`](skills/career-evidence/review-research/SKILL.md) | Review retained references and archive under user guidance | Manual |
| [`find-companies`](skills/job-hunt/find-companies/SKILL.md) | Research employers matching career direction, location and constraints, with or without vacancies | Discoverable |
| [`find-jobs`](skills/job-hunt/find-jobs/SKILL.md) | Find and verify live vacancies matching the user's profile | Discoverable |

**Manual** means the user selects the named skill; **Discoverable** means an agent may select it for a matching task. Manual skills declare `disable-model-invocation: true` on supporting hosts. This field is not part of the core Agent Skills specification and some hosts may ignore it. See the [invocation policy](docs/ARCHITECTURE.md#invocation-policy).

### Organization

| Directory | Responsibility | Skills |
| --- | --- | --- |
| `career-direction/` | What do I want, and why? Private north star, interests and decisions | `reflect` |
| `career-evidence/` | What have I demonstrated? Experience, achievements and supporting records | `maintain-profile`, `review-research` |
| `career-development/` | How do I grow toward it? Action plans, practice and progress | `plan-development`, `review-progress` |
| `personal-brand/` | Public messaging, reusable text, visual identity and presentation quality | `personal-brand`, `define-design-brief`, `create-design-assets`, `review-design`, `benchmark-profile`, `audit-surface`, `audit` |
| `job-hunt/` | Application materials and opportunity search | `build-resume`, `find-jobs`, `find-companies` |
| `setup-career-skills/` | Cross-cutting workspace setup | `setup-career-skills` |

Groups organize the repository; they are not installable umbrella skills. Install individual leaf directories. Existing skill names are unchanged except for the design lifecycle split below. Paths for previously top-level skills have moved into their groups; update installation sources accordingly.

### Personal-brand lifecycle

`skills/personal-brand/` groups positioning (`personal-brand`), discovery (`define-design-brief`), production (`create-design-assets`) and critique (`review-design`). The umbrella is an organizational directory, not a skill or required orchestrator. Each leaf is an independently installable package; select the leaf directory when installing.

Use discovery → creation → review as needed, reusing the same brief and asset files. Enter at any stage with existing inputs; no compulsory chain or repeated interview. Creation owns visual concept selection and self-checks; review supplies independent critique. These skills focus on career-facing identities, profiles, portfolios, resumes and talks rather than general commercial branding or product UX.

The former `design-identity` package is replaced by these three design skills; update installed paths and invocations accordingly.

## Design principles

- **Facts, goals, and positioning are different:** a verified job history is not an aspiration or a marketing claim.
- **One canonical record:** respect the user's established source of truth, rather than require a new schema or duplicate it in every destination.
- **Independently useful:** a skill can work with pasted documents even without a preconfigured workspace.
- **Verify, don't invent:** preserve source links, date qualifiers, uncertainty, and claims that cannot be confirmed.
- **Reviewable mutations:** do not silently publish, apply for a job, alter public profiles, or create tracker items without authorization.
- **No mandatory provider:** files, repositories, issue trackers, and web integrations are replaceable capabilities.

## Shared career workspace

The entire workspace is private, including material prepared for public use. Its five homes are **profile/** (background, capabilities, direction and development), **projects/** (work accounts and evidence links), **brand/** (positioning, audiences and visual guidance), **assets/** (drafts, approved staged outputs and service descriptions), and **research/** (selected companies, opportunities and comparable profiles).

A workspace README maps these roles to existing canonical records. They are user-record concepts, not the installable skill categories above. Reuse shared bios, headlines and visual masters; staged material is not proof of publication. Inspect external surfaces where possible, and ask the user to reconcile differences. Research is selected before saving and reviewed on request; prefer guided archiving, with deletion manual.

Use local folders, GitHub repositories or any Markdown-capable storage. Keep existing paths when mapped; setup is optional. See the [portable workspace model](docs/WORKSPACE.md) for the layout and operating rules. No actual user notes are migrated by changing this reference model.

The [workspace decision specification](docs/CAREER-WORKSPACE-SPEC.md) captures the agreed behavior, rejected alternatives, testing boundaries and deferred work.

## Getting started

1. Install individual skills via your agent's workflow or `npx skills add lfarci/career-skills --skill <name>` ([Skills CLI](https://www.skills.sh/docs/cli)). Nested skills are independently installable; no repository-wide setup is required.
2. Run `setup-career-skills` if you have existing career notes, resumes, web profiles, or an issue tracker you want the skills to use consistently.
3. Run one task-focused skill. For example: *“Audit alignment among my resume, GitHub profile, website, and LinkedIn export.”*

Configuration discovered during setup belongs in the **user's chosen private workspace**, not in this public skill repository. See [architecture and contracts](docs/ARCHITECTURE.md) and [evaluation cases](tests/cases.json).

## Scope and status

This is an initial **behavioral-specification release**. The sixteen skill packages contain instructions and acceptance criteria, and a lightweight static validator checks the packaging. A full cross-harness benchmark and live integration tests are future work. Resume rendering requires an environment with suitable export tools; job discovery requires current-accessible job sources.

## Validation

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

This checks packaging, references, invocation intent and scenario inventory. It does not run an agent. See [behavioral evaluations](docs/EVALUATION.md) for live-agent smoke runs and human review.

## Contributing

Changes should maintain small, independently invocable skills with clear boundaries and testable completion criteria. Run the structural validator, update behavioral scenarios when changing responsibilities or triggers, and follow [AGENTS.md](AGENTS.md). Use synthetic examples rather than committing real career profiles or personal information.

## License

MIT. See [LICENSE](LICENSE).

