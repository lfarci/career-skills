---
name: setup-career-skills
description: "Create or resume a private career workspace through guided setup."
disable-model-invocation: true
---

# Setup Career Skills

Create or resume a private Markdown career workspace. Guide the user **one question at a time**. Consult [workspace rules](references/workspace-model.md) when mapping sources, records or prior progress.

## Contract

- **Input:** Confirmed destination, approved career sources and permissions.
- **Output:** Verified workspace records or a scoped proposal, with a resumable setup checkpoint.

## Steps

1. **Locate.** Ask where to initialize, unless the location was already confirmed. A user-named folder is the **root itself** (`career-workspace/README.md`); when the user chooses a repository as a *parent*, propose `<repo>/career/`. State the resolved path. **Done when:** the exact root is confirmed.
2. **Route.** Inspect the chosen root: an empty location starts **New**; existing career records start **Resume**. For unrelated or ambiguous contents, ask whether to adopt them or choose another root. **Done when:** the path is unambiguous and existing content is accounted for.
3. **New.** Ask about existing CVs, notes, projects and credentials. Inspect approved source indexes first, then relevant detail. Recommend a useful initial import. With permission, create `README.md` and selected records **directly under the chosen root**, using `profile/`, `projects/`, etc. **Done when:** the approved records and links are verified, or the user explicitly chose index-only setup.
4. **Resume.** Validate `README.md`, mapped records, links, ownership and saved setup status **before further imports**. Report whether the workspace is usable, needs repair or is blocked. Propose targeted fixes with approval, then return to the saved next decision. **Done when:** the validation result and next action are clear.
5. **Continue.** After each approved batch, verify actual files and update the root `README.md` checkpoint: captured, missing/conflicting, deferred, status and next decision. Ask one useful next question. **Done when:** the user confirms their chosen scope is sufficient or pauses, with an accurate checkpoint.

## Done when

The chosen root has a verified index and approved records (or an explicitly minimal scope); progress, remaining gaps and the next decision are recorded, or a specific blocker is reported.

## Exceptional operations

A summarized import still depends on its source evidence. If the user approves replacing or moving an existing workspace, follow the separate [cutover checks](references/cutover.md) first. Preserve originals and external references.

Writes stay within the approved scope; publication needs separate approval.
