# Career Skills

Small, composable [Agent Skills](https://agentskills.io/) for understanding, maintaining, and presenting a professional identity—and finding suitable opportunities.

Each skill works independently and does not require GitHub, a particular AI harness, a proprietary profile format, or another skill. Skills use the tools the user's environment makes available; when a capability is missing, produce a reviewable local output instead of claiming to have taken an action.

## Skills

| Skill | Purpose | Intended invocation |
| --- | --- | --- |
| [`setup-career-skills`](skills/setup-career-skills/SKILL.md) | Discover existing records, assets, preferences, and progress tracker | Explicit setup |
| [`reflect`](skills/reflect/SKILL.md) | Explore and articulate professional identity and goals | Explicit reflection |
| [`maintain-profile`](skills/maintain-profile/SKILL.md) | Reconcile evidence and maintain factual career records | Reusable behavior |
| [`build-resume`](skills/build-resume/SKILL.md) | Author, tailor, and validate truthful resumes | Explicit authoring |
| [`personal-brand`](skills/personal-brand/SKILL.md) | Define professional positioning and coordinate its public expression | Explicit planning |
| [`audit-surface`](skills/audit-surface/SKILL.md) | Audit an individual professional asset | Reusable behavior |
| [`audit`](skills/audit/SKILL.md) | Audit alignment across multiple professional assets and track findings | Explicit audit |
| [`find-jobs`](skills/find-jobs/SKILL.md) | Find and verify live vacancies matching the user's profile | Explicit search |

An **explicit** skill is normally run when requested; a **reusable** skill is useful for an agent to discover and apply during a related task. Invocation flags vary by harness, so the files use portable skill metadata rather than relying on any one platform's invocation behavior.

## Design principles

- **Facts, goals, and positioning are different:** a verified job history is not an aspiration or a marketing claim.
- **One canonical record:** respect the user's established source of truth, rather than require a new schema or duplicate it in every destination.
- **Independently useful:** a skill can work with pasted documents even without a preconfigured workspace.
- **Verify, don't invent:** preserve source links, date qualifiers, uncertainty, and claims that cannot be confirmed.
- **Reviewable mutations:** do not silently publish, apply for a job, alter public profiles, or create tracker items without authorization.
- **No mandatory provider:** files, repositories, issue trackers, and web integrations are replaceable capabilities.

## Getting started

1. Install just the skill directories you want using your agent's Agent Skills workflow (or [skills.sh](https://skills.sh/)); no repository-wide setup is required.
2. Run `setup-career-skills` if you have existing career notes, resumes, web profiles, or an issue tracker you want the skills to use consistently.
3. Run one task-focused skill. For example: *“Audit alignment among my resume, GitHub profile, website, and LinkedIn export.”*

Configuration discovered during setup belongs in the **user's chosen private workspace**, not in this public skill repository. See [architecture and contracts](docs/ARCHITECTURE.md) and [evaluation cases](tests/cases.json).

## Scope and status

This is an initial **behavioral-specification release**. The eight skill packages contain instructions and acceptance criteria, and a lightweight static validator checks the packaging. A full cross-harness benchmark and live integration tests are future work. Resume rendering requires an environment with suitable export tools; job discovery requires current-accessible job sources.

## Validation

```bash
python3 scripts/validate_skills.py
```

## Contributing

Changes should maintain small, independently invocable skills with clear boundaries and testable completion criteria. Run the structural validator and add or update behavioral scenarios when changing responsibilities or triggers. Use synthetic examples rather than committing real career profiles or personal information.

## License

MIT. See [LICENSE](LICENSE).
