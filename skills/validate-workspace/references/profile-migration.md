# Migrating a flat profile/ to layers

Use only when the user asks to standardize the layout. A flat `profile/`, or a single `goals/direction.md`, with working index links is valid as it is.

| Flat record | Layered record |
| --- | --- |
| `profile/contact.md`, `experience.md`, `education.md`, `qualifications.md`, `languages.md`, `skills.md` | same name under `profile/facts/` |
| `profile/preferences.md` | `profile/criteria/conditions.md`; current pay to `profile/facts/compensation.md`; salary targets to `profile/criteria/salary-expectations.md` |
| `profile/criteria/compensation.md` (earlier layered layout) | `profile/facts/compensation.md`; targets to `profile/criteria/salary-expectations.md` |
| opportunity-screening sections of `direction.md` | `profile/criteria/expectations.md` |
| `profile/direction.md` or `profile/goals/direction.md` | split into `profile/goals/values.md`, `north-star.md` and `certifications.md` (planned credentials, also from the development plan) |
| `profile/development.md` | `profile/goals/development.md` |
| other records (for example `goals.md`, `certifications.md`) | the layer whose meaning matches the content, not the file name; ask when unclear |

Plan, then apply after approval:

1. List each move, each split (which headings go where) and each new record. Create `achievements.md`, `stories.md` or `expectations.md` only when there is content or the user asks for a template; empty sections carry a `TODO` rather than invented content.
2. Move with history where the storage allows (for example `git mv`), so content stays traceable.
3. Rewrite every inbound link: the index, other records, and files outside the workspace root (for example a repository `TODO.md`). Relative links inside moved files gain one `../`.
4. Update the index `Records` and any source-inventory destinations; leave `Setup progress` wording to setup.
5. Run `scripts/check_workspace.py` and a link check over the whole repository, then report.
