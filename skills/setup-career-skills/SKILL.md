---
name: setup-career-skills
description: "Create, import into, or resume a private career workspace (career/ with profile, projects, brand, assets, research). Use when the user wants to organize career notes, old resumes or profile exports into one workspace, or continue a saved setup."
---

# Setup Career Skills

Turn the user's scattered career material into a private workspace made of two things: an **index** (`README.md` at the root) and **canonical records** in the standard homes. The index points; records hold facts. Ask one question at a time and touch only the root and sources the user approved.

## Contract

- **Input:** A confirmed workspace root, approved sources or facts supplied in the conversation, and write permission.
- **Output:** Verified canonical records, an index that links them with a source inventory and setup checkpoint, and one next question; or one specific blocker.

## Record map

Every imported fact goes into a canonical record, never into the index. Create a file only when it receives content.

| Fact | Record |
| --- | --- |
| Employers, titles/grades, dates, internships | `profile/experience.md` |
| Degrees and schools | `profile/education.md` |
| Certifications, licences, awards | `profile/qualifications.md` |
| Skills and tools | `profile/skills.md` |
| Spoken languages | `profile/languages.md` |
| Goals, north star, considered next steps | `profile/direction.md` |
| Location, work mode, commute, contract, salary preferences | `profile/preferences.md` |
| Client assignments, side projects, contributions and their outcomes | `projects/<project>.md`, linked from the role in `experience.md` |
| Positioning, bios, visual guidance | `brand/` (only when the source contains it) |
| Reusable resumes, bios, banners | `assets/drafts/` or `assets/staged/` (approved) |
| Saved companies, job ads, comparator profiles | `research/` |

Keep each record plain Markdown with headings and relative links. Note the source file and its date beside imported facts; mark approximations and conflicts instead of resolving them silently. A goal stays a goal: "considering AZ-305" belongs in `direction.md`, not `qualifications.md`.

Contact details (e-mail, phone, address) stay in their source unless the user asks to import them; then they go to `profile/contact.md`, never the index.

## Steps

1. **Resolve the root.** The folder the user names is the root itself; create no nested `career/` inside it. When the user names a parent repository, propose its `career/` folder. When no destination is named, ask where the workspace should live and wait before reading or writing anything. Use an ordinary directory; Git worktrees, branches and new repositories are separate requests.
2. **Route.** Inspect only the root. Absent or empty means **New**. A root with an index or records means **Resume** (see below). Ambiguous existing material: ask whether to use it or choose another root.
3. **Inventory sources.** Read only sources the user named or approved. List each one with what it could contribute and its proposed record(s), then recommend a first batch. When the user already approved reading and writing, import that batch directly; otherwise ask which sources to import. With no sources at all, ask one focused question about the user's current role and history instead of creating an empty scaffold.
4. **Import the batch.** Write the selected facts into records using the record map. Write only what the sources support: no invented duties, metrics, dates or credentials.
5. **Write the index.** Create or update `README.md` from the [index template](references/index-template.md): root, write policy, homes in use, a link to every record, the source inventory (`imported` / `pending` / `excluded` with destination), and a **Setup progress** block with status (`in progress`, `paused`, `ready`, `blocked`), gaps and one next decision. The index links records; it holds no copied facts.
6. **Verify.** Re-read or list every written file and check the index links resolve. A write counts only after this check. Without a working write or read tool, report the blocker and offer the content as a proposal.
7. **Ask the next question.** Summarize verified files and gaps, then ask one useful question in plain text, such as an unimported source, a missing role, or an assignment worth a project record. The first batch rarely completes onboarding: continue batch by batch until the user says the scope is enough or pauses, then set the status.

When you cannot obtain the user's answer (a question tool fails or the session ends), stop and put the pending question in your final reply. A next decision saved in the index is a pending question, never permission to pick an answer.

## Resume

Read the root `README.md` first, then only the records it links. Check links resolve, records have one owner, and the saved next decision. Report `usable`, `needs repair` or `blocked`, then continue from the saved decision without re-asking answered questions. An index that holds facts directly (older setups) is `needs repair`: propose moving those facts into records before importing more. `validate-workspace` can help with difficult structural problems when installed; setup works without it.

Consult [workspace rules](references/workspace-model.md) for source handling details. Read [cutover checks](references/cutover.md) only when the user asks to move, archive or replace an existing workspace.

## Done when

- Every imported fact lives in exactly one canonical record named by the record map, with its source.
- The index links every record, lists sources with their decision, and saves status plus one next decision; it contains no copied facts or contact details.
- All writes were verified; writes stayed within the approved root; nothing was published.
- An unanswered decision, including one restored from the index, stays unanswered.
