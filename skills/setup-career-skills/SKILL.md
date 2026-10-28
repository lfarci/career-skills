---
name: setup-career-skills
description: Set up a standardized private career/ workspace, optionally discovering existing resumes and career records as sources.
disable-model-invocation: true
---

# Setup Career Skills

Initialize a clean, **standardized** private `career/` workspace; existing notes, resumes and profiles may supply its initial content. Run only when requested. Read [workspace initialization and source rules](references/workspace-model.md) when building the workspace.

## Contract

- **Input:** Chosen storage location and write policy, optional existing career documents or accessible source locations.
- **Scope:** Initialize the five named homes as needed, build a source/index map, and selectively seed approved records; migrate a legacy tree only after a separate plan and approval.
- **Output:** `career/README.md` (or proposed equivalent when writing is unavailable), initial canonical records if authorized, source-import status and a concise summary.

## Steps

1. **Choose the destination.** Determine whether the user wants a fresh managed `career/` or to align an existing one. When unspecified, propose a fresh `career/` in their preferred private storage. If that path already holds records, preserve it: offer a different private location for a fresh root or a planned migration of the existing tree. Confirm where writes are allowed and whether a PR is required.
2. **Discover usable sources.** Inspect only user-supplied or permitted documents: old career notes, CVs, project records, qualifications, portfolio/LinkedIn exports and relevant repositories. Share a short source inventory and suggest the first useful subset. If nothing exists, ask one question about the first profile area to capture. Do not require importing anything.
3. **Plan canonical records.** Map approved source material into `profile/`, `projects/`, `brand/`, `assets/` or `research/` with the names from the reference. Keep **profile/experience.md for employer/role history** (including user-confirmed internships), **projects/ for assignments, engagements and project outcomes**; other profile records own qualifications, skills and direction. Compare selected source timelines for potentially omitted roles and ask only about concrete discrepancies; do not invent missing entries. Keep aspirations, brand wording, drafts and public state separate. Leave unselected originals untouched.
4. **Create or propose.** With task-specific write authorization, initialize `career/README.md` and **all five standard homes** (`profile/`, `projects/`, `brand/`, `assets/`, `research/`). In Git, give each home a short `README.md` identifying responsibility and initial status, so the folder actually exists in version control; do **not** invent factual content or add nested placeholder files. Import selected facts with provenance instead of bulk-copying the old tree. Record imported versus pending sources and permissions. For occupied-root migration, first show a path/link/collision plan and obtain explicit approval; `validate-workspace` is optional.
5. **Verify and conclude.** Check created paths/links and state exactly what was saved, skipped or blocked. Suggest **one optional next content task** when useful (e.g., `maintain-profile` to reconcile uncertain facts). `ask-career-skills` may help users choose, but neither skill is required to start a task directly.

## Done when

- The selected root and source-import permissions are recorded or their absence is explicit.
- The managed destination visibly contains `career/README.md` and five tracked standard home folders; only user-selected content records are created.
- Sources are traceable, originals preserved and conflicting claims not invented as established facts.
- Writes, migration and link checks are reported accurately; other skills remain independently usable.
