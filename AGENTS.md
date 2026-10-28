# Repository agent guidance

Edit independent leaf skills under `skills/<group>/<name>/SKILL.md` (setup and the navigation router are top-level exceptions).

- **Skill boundaries, names or invocation:** read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
- **Onboarding, workflow routing or next-step advice:** read [docs/USER-JOURNEY.md](docs/USER-JOURNEY.md).
- **Career records, authority, storage or privacy:** read [docs/WORKSPACE.md](docs/WORKSPACE.md).
- **Terminology questions:** consult [GLOSSARY.md](GLOSSARY.md).
- **Behavior changes:** update scenarios in [tests/cases.json](tests/cases.json); for invocation changes, update expectations in [scripts/validate_skills.py](scripts/validate_skills.py).
- **Agent evaluation:** use [docs/EVALUATION.md](docs/EVALUATION.md); structural CI is not proof of behavior.

Preserve independently installable skill packages and reviewable changes. Keep users' personal data out of this public repository. Run `python3 scripts/validate_skills.py` before opening a PR.
