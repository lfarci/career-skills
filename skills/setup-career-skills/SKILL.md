---
name: setup-career-skills
description: "Create or resume a private career workspace when the user explicitly asks; treat a named folder as the root, import approved facts, and save setup progress."
---

# Setup Career Skills

Use this workflow only for an explicit setup or resume request. Ask one question at a time. Read and change only the selected workspace and sources the user approved.

## Contract

- **Input:** A confirmed workspace root, approved career facts or sources, and permission for requested local writes.
- **Output:** Verified useful records plus a resumable README checkpoint, or one specific blocker.

## Fast path: named folder, facts, and write permission

When the user names a new folder, says local writes are allowed, and supplies career facts, those choices are already confirmed. Do not ask to confirm the folder or permission. Create a plain directory with the host's `mkdir` or file tool. This is not a request for a Git repository, branch, task, or worktree: do not call worktree or repository-creation tools. Create exactly:

- `<named-folder>/README.md`
- `<named-folder>/profile/experience.md`

Treat `<named-folder>` itself as the root. Do not add `<named-folder>/career/`. Record only supplied facts; save progress in the README; verify both files; then ask one next decision.

## Run protocol

1. **Resolve the root.** A user-named folder is the root itself. If no destination is named, ask where to put the workspace and stop before inspecting or writing anything. Never assume the current directory or a suggested default is the destination. If the question tool errors, is unavailable, or receives no answer, stop and report that the root is undecided; create no workspace files. If the selected root contains unrelated or ambiguous material, ask whether to use it or choose another root.
2. **Route.** Inspect only the selected root. An absent or empty root is New. A root with a career README or records is Resume. Preserve existing files; never silently overwrite, move, or delete them. A workspace folder is an ordinary directory, not a Git worktree or new repository.
3. **Import.** Career facts supplied in the conversation are an approved source. When local writes are authorized, import supported facts now without asking again. Put employer and role history in `profile/experience.md`. Do not invent duties, technologies, credentials, achievements, or dates. If no facts or approved sources are available, ask one focused question and wait; do not make an empty scaffold. If that question tool errors or the user has not answered, stop without creating any files.
4. **Save progress.** After every approved import, create or update the root `README.md`. Record root, sources used, records created, captured facts, missing/deferred information, status (`in progress`, `paused`, `ready`, or `blocked`), and one next decision.
5. **Use supported tools safely.** Use only file or shell tools actually listed by the host. Do not invent APIs or use a code-execution runtime for filesystem work. Do not use worktree, branch, task, or repository-creation tools for ordinary workspace folders. Do not issue delete or move commands during ordinary setup. Never call a question tool to re-confirm a destination or write permission already supplied by the user.
6. **Verify before reporting.** After writing, read the files or list the workspace to confirm the exact paths and contents. A write is complete only after the host reports success and the follow-up read/listing confirms it. If no supported write or verification tool is available, report the blocker; do not claim completion.
7. **Stop at the next decision.** Summarize verified files and remaining gaps, then ask one useful next question. Do not continue into a broad onboarding interview unless the user answers.

## Resume checks

Before importing into an existing workspace, check its README, mapped files, local links, record ownership, and saved next decision. Report whether it is usable, needs repair, or is blocked. Preserve existing choices, avoid duplicate records, and resume at the saved decision.

Consult [workspace rules](references/workspace-model.md) when mapping sources, records, or prior progress. Read [cutover checks](references/cutover.md) only when the user requests and authorizes moving, archiving, or replacing an existing workspace. Preserve original evidence and external references.

## Done when

The selected root has a verified index and useful approved records, or one specific blocker is reported. The README accurately saves progress and the next decision.

Writes stay within the approved scope. Publication requires separate approval.
