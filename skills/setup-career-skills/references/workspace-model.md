# Setup conversation and source reference

## Start or resume

`setup-career-skills` is an interactive, **resumable** onboarding workflow. Read the existing `career/README.md` first when present. If the user says only “set up my career workspace”, make a helpful recommendation then ask **one high-value question** about sources or destination based on what is already known. If the user explicitly requests an index-only/minimal setup, do that and mark other areas deferred; do not force a lengthy interview.

## Source discovery and intake

Suggest relevant candidate sources: previous CVs/resume repositories, existing career notes, professional role histories, project files, credential records, portfolio, website, GitHub/LinkedIn profiles and exports. Ask which can be read, where, and whether another useful source is missing. Inventory authorized sources and summarize their expected value before importing. Don't search private storage indiscriminately or bulk-copy entire legacy trees.

With no source available, collect a small first area conversationally. With sources, assess coverage and source conflicts for the **selected scope**. Look for role dates, internship omissions, projects/assignments, skills, qualifications, education, languages, direction/preferences, brand/assets and optional market research. These are **prompts for gaps**, not all required fields. If a selected source mentions an experience missing from the proposed role history, explicitly ask about it before concluding.

Follow-up examples (choose only the best next question, adapting known context):
- “I found your old resume and project notes. Do you have any other career records you want considered before we choose what to import?”
- “Your resume lists two internships not yet in the new experience file. Should we include them in the first pass?”
- “We've captured your roles, skills and certifications. Education and languages are not yet covered. Would you like to handle those next, or defer them?”
- “The workspace structure is ready. Would you like a quick minimal handoff, or should we continue populating your profile from the sources?”

Do not ask the same question twice, and do not make every optional category a blocker.

## Physical workspace and ownership

The **managed** private root is `career/`, indexed by `career/README.md`. Scaffold `profile/`, `projects/`, `brand/`, `assets/` and `research/` with a brief `README.md` in each (purpose and pending/ready status), because Git cannot track empty directories. Create substantive content only when selected. `profile/experience.md` owns employers, roles/grades and dates, including source-supported internships; detailed engagements and project outcomes belong under `projects/`. Keep facts, aspirations, public wording, drafts and published state distinct.

If `career/` is already occupied, offer a fresh private destination elsewhere or a controlled in-place migration with a path/link/collision plan and explicit approval. Old documents are **sources**, not competing maintained copies; preserve them. After a Git-tracked root rename, `D career/...` entries may be deleted tracked paths rather than folders physically in the new root. Verify actual files.

## Checkpoint and completion

Keep a **short onboarding section** in `career/README.md` (no rigid schema):
- Status: `in progress`, `ready`, `paused` or `blocked`.
- Sources: imported, pending, skipped/declined, plus provenance and evidence limits.
- Coverage: relevant area + captured/missing/conflicting/deferred; do not inventory irrelevant personal details.
- Next action: the specific user-selected area or one unresolved question, and granted write/PR permission.

After **each selected batch**, report what's done, a significant gap or uncertainty, and the next useful **one-question** follow-up. A successful file write proves only that batch; it does not conclude the conversation. Resume later from saved state. Finish only when the user confirms their chosen scope is sufficient, explicitly chooses an index-only setup, or pauses; report pending information honestly. No write access: provide proposed paths/content without claiming persistence.

No publication or external synchronization is inferred. Don't silently promote planned credentials, unsupported metrics or client-confidential details. `maintain-profile` owns subsequent factual corrections, but setup can ask and reconcile initial intake facts directly without requiring that skill.
