---
name: setup-career-skills
description: "Guide me through creating or resuming a private career workspace, discovering sources, and completing setup interactively."
disable-model-invocation: true
---

# Setup Career Skills

Guide **new creation or resumption** of a private, Markdown-first career workspace (usually named `career/`). Ask **one useful question at a time**; create useful records, not merely a directory. Read [workspace setup rules](references/workspace-model.md) for ownership, validation and source handling.

## Contract

- **Input:** User's chosen workspace location, available sources and write permissions, as established during conversation.
- **Scope:** Create a new workspace or validate and resume an existing one. Never silently migrate or overwrite.
- **Output:** Verified index and approved records (or a proposal without write access), a short setup checkpoint and the next question.

## Steps

1. **Choose the exact root first.** Ask where the workspace should live, even if the current repository has `career/`. Treat a **folder named by the user as the workspace root itself**, not a parent for another `career/`; if they choose a repository as the parent, propose its `career/` folder. State the resolved path before writing, and clarify only genuine ambiguity. Reuse an explicitly confirmed location on resume. Do not create an empty directory as a substitute for onboarding.
2. **Select New or Resume.** Inspect **only the chosen root**, not an assumed `career/` elsewhere. If empty, follow **New**; if it contains a managed workspace, follow **Resume**. If it contains unrelated or ambiguous data, ask whether to adopt it or choose another root; preserve everything.
3. **New:** Ask about existing CVs, notes, profiles, projects and credentials. Inspect indexes first, then relevant approved sources. Recommend a useful initial import; after approval, write `README.md` at the **chosen root** plus selected records in `profile/`, `projects/`, etc. Avoid empty scaffolds, unsupported facts or an index-only handoff unless explicitly requested.
4. **Resume:** **Validate before continuing:** check the chosen root's index, mapped files, local links, canonical ownership, setup status and pending imports. Use `validate-workspace` if helpful, not as a dependency. Propose targeted repairs before further imports; preserve previous answers and avoid automatic reorganization.
5. **Iterate and finish.** Verify every approved batch and update the root `README.md` checkpoint (captured, missing/conflicting, deferred, next decision; status `in progress`, `paused`, `ready` or `blocked`). A summary import is **not a lossless migration**: keep source dependencies explicit. Before an approved root replacement, verify preserved originals and **inbound links from elsewhere**, not only links inside the new workspace. Ask the next useful question until the user confirms sufficient scope or pauses.

## Done when

- The location and new/resume path are clear; an existing workspace was validated **before** resuming changes.
- Actual writes, source boundaries, pending gaps and the next action are accurately recorded.
- Existing material remains intact without unapproved moves, duplication or publication.
