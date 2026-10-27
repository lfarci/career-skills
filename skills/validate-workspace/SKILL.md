---
name: validate-workspace
description: Validate and adapt Career Skills workspace mappings when a canonical record path, index entry, folder ownership or relative link is missing, stale or inconsistent. Use on concrete structural drift, including during another skill's task; do not run before every task.
---

# Validate Career Workspace

Diagnose and minimally repair how a user's private career records are organized. This is **on-demand maintenance**, not first-time setup, a scheduled audit, or a prerequisite for other skills.

The five logical homes (profile, projects, brand, assets, research) describe **responsibilities**, not required folder names. An existing layout is valid when its mapping is clear.

## Contract
- **Input:** The reported structural issue or explicit validation request, accessible workspace root/index and relevant source paths, plus existing write permissions.
- **Scope:** Map ownership, test paths and relative links, and adapt only the affected workspace structure. Do not reconcile career facts, rewrite content, publish assets or manage research retention.
- **Output:** A concise valid/needs-attention result, minimal confirmed correction or proposed patch, and any blocking question.

## Steps

1. **Check the trigger.** Run if the user asks to validate/reorganize a career workspace, or another active career task encounters a concrete missing/stale index, broken path, ambiguous canonical owner or structural change. If the paths relevant to the active task work, do not scan, migrate or report unrelated housekeeping. An absent index alone is not an error when supplied files suffice.
2. **Read just enough to diagnose.** Inspect the chosen workspace index (usually a career README) and the affected files/links. Check which existing records map to profile/, projects/, brand/, assets/ and research/, where the canonical authority lives, and which access/write boundaries apply. Treat uncreated, unused homes as valid. Accept existing names, nested directories and Markdown-capable providers.
3. **Distinguish problems from preferences.** Flag genuinely stale paths, invalid relative links, duplicate or conflicting authority, and records assigned to unclear roles. Do not flag a valid custom layout merely because it differs from the reference tree. Do not interpret staged assets as published or projects as proven achievements.
4. **Choose the smallest adaptation.** Prefer repairing a workspace-index link or mapping to moving files or creating folders. If a canonical owner is ambiguous, ask one focused question rather than guessing. Moving, renaming, deleting, merging or reorganizing user files needs specific approval, a link-update plan and a check for data loss; never do it opportunistically during another skill's task.
5. **Respect the requested task and permissions.** A narrow index/link fix may be applied only when the user's current instruction and write policy authorize those exact changes; otherwise supply a reviewable patch. Existing broad access is not an instruction to restructure. Preserve unrelated edits and follow the storage provider's conflict or PR workflow. Check affected links after any actual write.
6. **Return to the original task.** Report only verified findings, what actually changed (or remains proposed), and remaining blockers. If called while another skill is working, let that work continue using the resolved path; do not launch a profile audit, other skill or full setup.

## Done when

- The requested paths and canonical mappings were checked or inaccessible items were clearly reported.
- Valid alternative layouts and intentionally absent areas were left intact.
- Repairs are minimal, authorized, confirmed and idempotent; no unrequested content edits or migrations.
- Other skills remain usable without this skill, a workspace index or setup.
