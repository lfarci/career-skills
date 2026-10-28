---
name: validate-workspace
description: Validate career workspace structure on request, or repair stale source mappings, broken record links and ambiguous canonical paths that block another Career Skills task.
---

# Validate Career Workspace

Keep existing career records findable. Map the user's layout to the five logical areas (profile, projects, brand, assets, research); physical folder names are optional. Use this skill **on demand**, not as a prerequisite for other skills.

## Contract

- **Input:** An explicit workspace-validation request or a structural blocker encountered during another task; relevant files/index and existing permissions when available.
- **Scope:** Verify structural paths, links and canonical-record ownership; repair only authorized mappings. Career facts and published content belong to other skills.
- **Output:** One status (`valid`, `repaired`, `proposed` or `blocked`), checked scope, verified changes or patch, and the resolved path or next question.

## Steps

1. **Choose scope.** For a *task blocker*, examine only the failed record lookup or affected link. For an *explicit workspace review*, inspect the chosen index, its mapped existing records and their relevant links; report inaccessible areas. An absent index or uncreated logical home is valid when a task can use supplied records. Initial workspace configuration belongs to `setup-career-skills`.
2. **Verify the mapping.** Find the current canonical source and resolve applicable paths from the workspace index or supplied files. Check target existence, relative links and whether the same factual record has competing authorities. Separate actual broken references from intentional alternative layouts.
3. **Select a repair.** Prefer updating a stale index entry or link over relocating files. When the canonical owner is uncertain, ask one focused question. Before a move, rename, merge or deletion, present the affected paths, link updates and conflict/data-loss risks, and obtain specific approval.
4. **Apply within scope.** Make a narrow index/link correction only if the active user request and write policy authorize it; otherwise present a patch. Preserve unrelated changes and follow the provider's version/PR workflow. Verify that changed references resolve after the write.
5. **Return a result.** Use `valid` for checked mappings without defects, `repaired` for a confirmed fix, `proposed` for a fix awaiting approval/access and `blocked` when the required authority or files remain unknown. Name the affected paths and any unresolved question. When called from another task, return the resolved locator so the original task can continue; an unresolved blocker may instead require supplied evidence.

## Done when

- The requested scope has been checked; relevant mappings and access limits are explicit.
- The status matches observed evidence and actual write results.
- Any applied fix is authorized, verified and repeatable without further changes.
- Existing custom layouts and unrelated content remain intact.
