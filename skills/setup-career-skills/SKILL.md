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

<!-- record-map -->
| Fact | Record |
| --- | --- |
| Name and contact details the user chose to import (name, e-mail, phone, public links) | `profile/contact.md` |
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
<!-- /record-map -->

Keep each record plain Markdown with headings and relative links. Note the source file and its date beside imported facts; mark approximations and conflicts instead of resolving them silently. A newer user-confirmed fact supersedes an older goal or note: record the fact, keep the older entry dated as superseded, and mention the change. A goal stays a goal: "considering AZ-305" belongs in `direction.md`, not `qualifications.md`.

Contact details (e-mail, phone, address) stay in their source unless the user asks to import them; then they go to `profile/contact.md`, never the index.

## Steps

0. **Know your host.** Infer lightly from the tools and environment you have: Claude Code (`.claude/`, `CLAUDE.md`), Codex (`.codex/`, `AGENTS.md`), OpenCode (`.opencode/`, `AGENTS.md`), Cursor (`.cursor/`), or generic. Note which file read/write and command tools exist and whether Python 3 runs; adapt the steps below to them. Nothing here requires a specific host; when unsure, proceed as generic.
1. **Resolve the root and form.** Ask where the workspace should live and in what form, unless the user already said. The default and recommended form is **Markdown files in a private local folder or private Git repository**; mention other storage (for example Google Docs) only when the host has tools for it, as a less-supported option. The folder the user names is the root itself; create no nested `career/` inside it. When the user names a parent repository, propose its `career/` folder. When no destination is named, ask where the workspace should live and wait before reading or writing anything. Use an ordinary directory; Git worktrees, branches and new repositories are separate requests.
2. **Route.** Inspect only the root. Absent or empty means **New**. A root with an index or records means **Resume**: run the Resume checks below *before* any import, and when the result is `needs repair`, end this turn with the move plan and one approval question. "Resume setup" alone approves continuing, not restructuring. Ambiguous existing material: ask whether to use it or choose another root.
3. **Inventory sources.** When the user has not mentioned sources yet, first ask one question: do they have existing resumes, notes, profile exports or project documents, and where are they? Read only sources the user named or approved; for archives such as a LinkedIn export zip, follow the archive rule in [workspace rules](references/workspace-model.md). List each one with what it could contribute and its proposed record(s), then recommend a first batch. When the user already approved reading and writing, import that batch directly; otherwise ask which sources to import. Only when the user says there are no sources, ask one focused question about the user's current role and history instead of creating an empty scaffold.
4. **Import the batch.** Write the selected facts into records using the record map. Write only what the sources support: no invented duties, metrics, dates or credentials.
5. **Write the index.** Create or update `README.md` from the [index template](references/index-template.md): root, write policy, homes in use, a link to every record, the source inventory (`imported` / `pending` / `excluded` with destination), and a **Setup progress** block with status (`in progress`, `paused`, `ready`, `blocked`), gaps and one next decision. The index links records; it holds no copied facts.
6. **Verify.** When Python 3 can run, run `python3 scripts/check_workspace.py <root>` from this skill's folder (add `--json` for structured output); exit code 0 means usable, 1 lists errors to fix, warnings name unlinked records. Otherwise re-read or list every written file and check the index links resolve by reading. A write counts only after this check. Without a working write or read tool, report the blocker and offer the content as a proposal.
7. **Ask the next question.** Summarize verified files and gaps, then ask one useful question in plain text, such as an unimported source, a missing role, or an assignment worth a project record. The first batch rarely completes onboarding: continue batch by batch until the user says the scope is enough or pauses, then set the status.

When you cannot obtain the user's answer (a question tool fails or the session ends), stop and put the pending question in your final reply. A next decision saved in the index is a pending question, never permission to pick an answer: ask it with its saved wording and change it only after the user answers.

## Resume

Read the root `README.md` first, then only the records it links. Run `scripts/check_workspace.py <root>` when Python is available. Check links resolve, records have one owner, and the saved next decision. Report `usable`, `needs repair` or `blocked`, then continue from the saved decision without re-asking answered questions. An index that holds facts directly (older setups; the checker names its content sections) is `needs repair`: list the proposed records and moves, then wait for approval before changing any file, unless the user's request already authorizes restructuring. Move contact details only when the user asks. Structural fixes follow the repair rule:

<!-- repair-rule -->
1. A request to check, review or resume is read-only for structure: report the status and the proposed fix, then ask before changing files.
2. A link to a renamed or moved record: update the link and the index entry; the user's file name and location win.
3. Rename or move a record to its standard name only when the user explicitly asks to standardize the layout.
<!-- /repair-rule -->

`validate-workspace` can help with difficult structural problems when installed; setup works without it.

Consult [workspace rules](references/workspace-model.md) for source handling details. Read [cutover checks](references/cutover.md) only when the user asks to move, archive or replace an existing workspace.

## Done when

- Every imported fact lives in exactly one canonical record named by the record map, with its source.
- The index links every record, lists sources with their decision, and saves status plus one next decision; it contains no copied facts or contact details.
- All writes were verified; writes stayed within the approved root; nothing was published.
- An unanswered decision, including one restored from the index, stays unanswered.
