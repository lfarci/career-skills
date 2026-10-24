---
name: setup-career-skills
description: Configure career skills by discovering the user's existing professional records, public profiles, preferred progress tracker, storage and publication boundaries. Use when the user asks to set up, initialize or configure the career-skills collection.
---

# Setup Career Skills

Discover the user's existing ecosystem before prescribing any structure. Run this on request, not automatically before every skill.

## Steps

1. Inspect available workspace files, repository configuration, existing career notes and accessible profile sources. Report what you discovered. Never ask the user for a fact that is already available and unambiguous.
2. Collect **only missing decisions**, conversationally in small, related groups:
   - Where are canonical professional facts kept? If nowhere, offer plain Markdown in a user-selected private location.
   - Which public assets exist (resume, website, LinkedIn, GitHub, portfolio, credentials)? Which are read-only or writable?
   - Where should ongoing work be tracked (GitHub Issues, another tracker, Markdown checklist, or nowhere)? Which repository/project and labels, if applicable?
   - What are the privacy boundaries, languages, target roles and audiences? These are optional and may remain unanswered.
   - Should suggestions be proposed only, or are edits to designated private records authorized? Public publication always requires explicit approval.
3. Record a small human-readable workspace configuration in the user's chosen location. Use Markdown by default. Store references and preferences; link to source records rather than copying confidential profile data. Never commit the user's configuration to the public career-skills repository.
4. Summarize discovered assets, canonical authority, tracker destination, permissions, and unresolved questions. Validate linked paths and accessible integrations where possible.

## Output

A `Career Skills Setup` summary with canonical source, asset inventory, progress tracker and privacy/write policies, plus the chosen configuration file location (or a proposed document if writing is unavailable).

## Done when

- Every configured source and tracker is explicitly identified or marked as unset.
- Existing folders and repositories are respected; no mandatory schema migration.
- No credentials, API tokens, sensitive documents or private personal details are duplicated into public configuration.
- Skills can still run independently if setup was skipped or incomplete.
