# Setup reference: new or resume

## Location and routing

Confirm the **exact workspace root** before reading workspace data. If the user says “create a folder named `career-workspace`”, use `career-workspace/README.md` and `career-workspace/profile/`, **not** `career-workspace/career/`. If they instead select a repository as the *parent*, propose `<repo>/career/` as the root. Don't assume an existing `career/` is chosen. Reuse a root already specified or confirmed; state the resolved path before writes, asking again only for a genuinely ambiguous parent-vs-root choice. Do not create an empty folder as a separate setup milestone unless explicitly requested.

**New:** Selected destination is empty or absent. Ask about accessible existing CVs, career notes, resumes, portfolios, project records, GitHub/LinkedIn exports and credentials. Inventory only approved sources, recommend the first *useful* import, and ask one focused question. With permission, create `<chosen-root>/README.md` plus selected records; don't conclude after creating an empty scaffold. The user may explicitly choose index-only setup.

**Resume:** Selected destination has an existing managed `career/` or partial records. Before creating or importing anything, verify:
- `<chosen-root>/README.md` existence and recorded root, permissions, source map and onboarding status; if missing, inspect existing records and propose a minimal index repair.
- Referenced canonical files, links and folders **actually** exist; unused homes need not exist.
- Canonical ownership is unambiguous: no conflicting active profile/brand/project records, accidental duplicate roots, or unexplained imports.
- Which records are captured, missing, conflicting or deferred, and the last pending user decision.

Return a **short validation result** (usable / issues needing repair / blocked) and the specific next question. If blocked, resolve or propose a targeted correction first. The optional `validate-workspace` skill can assist with difficult structure/links; it is not required and its use must not turn a resume into automatic reorganization. A usable older layout can stay as-is until the user requests standardization. Preserve prior permissions, answers and records. Don't ask the same question again.

If the chosen destination contains unrelated files or uncertain ownership, ask whether to adopt it, choose another location or plan an approved migration. No overwriting, moving or deleting without a separate proposal and approval. Git `D career/...` after a rename can represent deleted *tracked paths*, not present directories: inspect the filesystem.

## Source coverage and safe cutover

Review the chosen root's index and source map first, then read detailed files **only as needed** to produce the selected records. For “set up everything available”, inventory each relevant area and record what was imported, summarized, linked, unavailable or deferred; avoid dumping every file into the conversation. A consolidated summary is useful but **does not replace its full evidence**. Never claim sources can be deleted or safely replaced just because the new index covers every area. Keep original sources or preserve enough traceable evidence for future work; explain dependencies on paths outside the workspace.

If the user explicitly approves replacing/moving an existing workspace, first identify source files, destination collisions and external dependencies. Preserve source content as agreed, update provenance links, then verify links **both within the new workspace and pointing into it from the rest of the accessible repository**, plus links in any moved archive/backup. Fix or report stale references before describing the cutover as complete. If only part of the repository is accessible, label verification partial; do not claim global link integrity. Structural migration is a separate user-approved operation, never an automatic consequence of import.

## Standard records and authority

The managed root uses these **home names as needed**, not as mandatory empty folders:
- `profile/`: background, employer/role history (including supported internships), skills, credentials, goals, development.
- `projects/`: consulting engagements, assignments, contributions, outcomes and project evidence.
- `brand/`: messaging, positioning and visual guidance.
- `assets/`: staged/draft reusable materials and service descriptions.
- `research/`: selected employers, roles and comparators.

`profile/experience.md` owns jobs and dates, not detailed client engagements. Distinguish facts from plans, branding and published state. Preserve original sources with provenance; import only user-selected claims, never auto-sync or bulk-copy a legacy tree. Do not invent credentials, impact metrics or project maturity.

## Lightweight progress checkpoint

Keep `<chosen-root>/README.md` readable: destination, authorized write policy, source map, captured/pending/deferred areas, setup status (`in progress`, `ready`, `paused`, `blocked`) and one next decision. Do not keep an elaborate migration log or repeat the whole interview. After each approved batch, verify what was written and ask **one** useful next question. The user can stop, pause or skip categories. No external publication is inferred.
