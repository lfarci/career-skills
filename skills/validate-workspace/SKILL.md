---
name: validate-workspace
description: Validate career workspace structure on request, or repair stale source mappings, broken record links and ambiguous canonical paths that block another Career Skills task.
---

# Validate Career Workspace

Keep career records findable and, when requested, align an existing workspace to the standard physical `career/` homes: `profile/`, `projects/`, `brand/`, `assets/`, `research/`. Legacy paths can remain operational via mappings until an authorized migration. Use this skill **on demand**, not as a prerequisite for other skills.

## Contract

- **Input:** An explicit workspace-validation request or a structural blocker encountered during another task; relevant files/index and existing permissions when available.
- **Scope:** Verify structural paths, links and canonical-record ownership; repair only authorized mappings. Career facts and published content belong to other skills.
- **Output:** One status (`valid`, `repaired`, `proposed` or `blocked`), checked scope, verified changes or patch, and the resolved path or next question.

## Steps

1. **Choose scope.** For a *task blocker*, check only the failed lookup/link; a working legacy mapping does not trigger migration. For an *explicit workspace review*, inspect the index and mapped existing records; when the user asks for **standardization**, also compare physical homes with the standard `career/` layout. Report inaccessible areas. An uncreated unused home or absent index does not block work from supplied records. Initial workspace creation and source imports belong to `setup-career-skills`.
2. **Verify the mapping.** For a review, run `python3 scripts/check_workspace.py <root>` from this skill's folder when Python 3 is available (exit 0 usable, 1 errors listed, 2 root missing; `--json` for structured output); otherwise check by reading. Resolve existing canonical paths and relevant links, identify competing authorities, and separate broken references from usable legacy mappings. For an explicit alignment request, inventory proposed moves, path collisions and affected inbound/outbound links before editing.
3. **Select a repair.** For a broken link, prefer a small index/link fix. For user-requested standardization, propose relocation to canonical home names, including link updates, conflicts and history preservation (use a reviewable PR when relevant). Ask about ambiguous ownership. Moving, renaming, merging or deleting requires a specific approved plan.
4. **Apply within scope.** Make a narrow index/link correction only if the active user request and write policy authorize it; otherwise present a patch. Preserve unrelated changes and follow the provider's version/PR workflow. Verify that changed references resolve after the write.
5. **Return a result.** Use `valid` for checked mappings without defects, `repaired` for a confirmed fix, `proposed` for a fix awaiting approval/access and `blocked` when the required authority or files remain unknown. Name the affected paths and any unresolved question. When called from another task, return the resolved locator so the original task can continue; an unresolved blocker may instead require supplied evidence.

## Done when

- The requested scope has been checked; relevant mappings and access limits are explicit.
- The status matches observed evidence and actual write results.
- Any applied fix is authorized, verified and repeatable without further changes.
- Existing custom layouts and unrelated content remain intact.
