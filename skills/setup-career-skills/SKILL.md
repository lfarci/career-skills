---
name: setup-career-skills
description: "Guide me through creating or resuming a private career workspace, discovering sources, and completing setup interactively."
disable-model-invocation: true
---

# Setup Career Skills

Guide **new creation or resumption** of a private, Markdown-first `career/` workspace. Ask **one useful question at a time**; create useful records, not merely a directory. Read [workspace setup rules](references/workspace-model.md) for ownership, validation and source handling.

## Contract

- **Input:** User's chosen workspace location, available sources and write permissions, as established during conversation.
- **Scope:** Create a new workspace or validate and resume an existing one. Never silently migrate or overwrite.
- **Output:** Verified index and approved records (or a proposal without write access), a short setup checkpoint and the next question.

## Steps

1. **Choose location first.** For a new setup conversation, ask where the workspace should live—even if the current repository has `career/`. Don't assume the current directory or invent `career-workspace/career/`. If the user already gave an explicit location or is resuming a previously confirmed location, don't repeat the question. Confirm permission before writes.
2. **Choose the path from what exists.** Inspect **only the selected location**. If empty, follow **New**. If a workspace exists, follow **Resume**. If the directory contains unrelated or ambiguous data, ask whether to adopt it or use another location; preserve everything.
3. **New:** Ask about existing CVs, notes, profiles, projects and credentials. Recommend a useful first subset; after approval, write `career/README.md` and selected canonical records under the standard homes. Avoid empty folders, unsupported facts or an index-only handoff unless the user explicitly requests that minimal scope.
4. **Resume:** **Validate before continuing:** check the workspace index, actual mapped files, relevant links, canonical ownership, saved setup status and pending imports. If available, `validate-workspace` can help with structural problems; otherwise perform these checks directly. Report defects and propose approved repairs **before further imports**. Do not require a validator installation, move old files or redo completed intake. Continue from the saved next question.
5. **Iterate and finish.** After each approved import or repair, verify files/links and update a short `career/README.md` checkpoint (captured, missing/conflicting, deferred, next decision; status `in progress`, `paused`, `ready` or `blocked`). Ask the next useful question. Only finish when the user confirms their chosen scope is sufficient, requests minimal setup or pauses; do not hand off unfinished intake to another skill.

## Done when

- The location and new/resume path are clear; an existing workspace was validated **before** resuming changes.
- Actual writes, source boundaries, pending gaps and the next action are accurately recorded.
- Existing material remains intact without unapproved moves, duplication or publication.
