# Setup reference: new or resume

## Location and routing

Always establish the user's chosen private workspace location **before examining workspace data**. A `career/` in the current repository is not implicit consent to use it. If the user names the destination in their request, respect it without a redundant question; on an established resume, reuse its recorded location. Do not invent a second nested root to avoid an occupied one.

**New:** Selected destination is empty or absent. Ask about accessible existing CVs, career notes, resumes, portfolios, project records, GitHub/LinkedIn exports and credentials. Inventory only approved sources, recommend the first *useful* import, and ask one focused question. With permission, create `career/README.md` plus selected records; don't conclude after creating an empty scaffold. The user may explicitly choose index-only setup.

**Resume:** Selected destination has an existing managed `career/` or partial records. Before creating or importing anything, verify:
- `career/README.md` existence and recorded root, permissions, source map and onboarding status; if missing, inspect existing records and propose a minimal index repair.
- Referenced canonical files, links and folders **actually** exist; unused homes need not exist.
- Canonical ownership is unambiguous: no conflicting active profile/brand/project records, accidental duplicate roots, or unexplained imports.
- Which records are captured, missing, conflicting or deferred, and the last pending user decision.

Return a **short validation result** (usable / issues needing repair / blocked) and the specific next question. If blocked, resolve or propose a targeted correction first. The optional `validate-workspace` skill can assist with difficult structure/links; it is not required and its use must not turn a resume into automatic reorganization. A usable older layout can stay as-is until the user requests standardization. Preserve prior permissions, answers and records. Don't ask the same question again.

If the chosen destination contains unrelated files or uncertain ownership, ask whether to adopt it, choose another location or plan an approved migration. No overwriting, moving or deleting without a separate proposal and approval. Git `D career/...` after a rename can represent deleted *tracked paths*, not present directories: inspect the filesystem.

## Standard records and authority

The managed root uses these **home names as needed**, not as mandatory empty folders:
- `profile/`: background, employer/role history (including supported internships), skills, credentials, goals, development.
- `projects/`: consulting engagements, assignments, contributions, outcomes and project evidence.
- `brand/`: messaging, positioning and visual guidance.
- `assets/`: staged/draft reusable materials and service descriptions.
- `research/`: selected employers, roles and comparators.

`profile/experience.md` owns jobs and dates, not detailed client engagements. Distinguish facts from plans, branding and published state. Preserve original sources with provenance; import only user-selected claims, never auto-sync or bulk-copy a legacy tree. Do not invent credentials, impact metrics or project maturity.

## Lightweight progress checkpoint

Keep `career/README.md` readable: destination, authorized write policy, source map, captured/pending/deferred areas, setup status (`in progress`, `ready`, `paused`, `blocked`) and one next decision. Do not keep an elaborate migration log or repeat the whole interview. After each approved batch, verify what was written and ask **one** useful next question. The user can stop, pause or skip categories. No external publication is inferred.
