---
name: setup-career-skills
description: "Guide me through setting up a standardized private career workspace: find existing sources, ask about missing information and import selected records step by step."
disable-model-invocation: true
---

# Setup Career Skills

**Guide the user through a resumable onboarding conversation**, not just directory creation. Initialize a private `career/` with five named homes. Existing notes, resumes, profiles and projects are potential sources; never import all of them without selection. Read [setup conversation and source rules](references/workspace-model.md) when starting or resuming.

## Contract

- **Input:** User's setup goal, **explicitly confirmed destination**, write policy and optionally existing sources.
- **Scope:** Discover sources, identify meaningful gaps, scaffold the standard workspace and progressively import user-selected records. An occupied legacy root requires an explicit adoption choice.
- **Output:** A verified `career/README.md` (or proposed plan without write access), standard homes as needed, an import/gap status, and **a concrete next question or confirmed completion**.

## Steps

1. **Ask where to initialize first.** On every new setup, **ask the user to choose the workspace location before inspecting or initializing any directory**, even if a `career/` already exists in the current repository or a destination seems obvious. Offer a concise choice of current private repository, another repository or local storage; do not select one silently. If the user already specified an exact location in this request, confirm that choice rather than asking them to repeat it. For a previously confirmed in-progress setup, reuse the recorded destination instead of restarting this question. **No writes until the user approves them.**
2. **Inspect the chosen destination and resume.** After the location is confirmed, inspect only that destination and the relevant existing `career/README.md`, if present, to understand progress. If it already contains a workspace, ask whether to **continue/adopt it, migrate it with an approved plan or choose another location**; never overwrite or silently create a second root. Preserve previous answers and permissions.
3. **Ask about existing sources.** Proactively ask whether the user has an old resume, notes, role/project history, certificates, portfolio or professional-profile exports, including where the agent may look. Use known accessible locations as suggestions rather than scanning indiscriminately. Inventory permitted sources briefly, flag unreadable ones and **ask whether anything important is missing**. If none exist, guide a small conversational intake from scratch.
4. **Plan coverage with the user.** Identify the highest-value initial information and compare it with selected sources: employers, roles, dates and internships; assignments/projects; skills and qualifications; education/languages; goals/preferences; brand/assets; optional research and publication destinations. Mark each relevant area as supported, missing, conflicting or deferred. **Ask one focused question at a time** to resolve important omissions or choose what to import next. Don't require complete information in every area or a fixed questionnaire.
5. **Create and import selectively.** Confirm private location, scope and write/PR permission. Create `career/README.md` and only the standard home folders needed for selected records; record other homes as pending in the index, without empty placeholders. Import supported claims with source references, evidence limits and uncertainty. Keep `profile/experience.md` for role history (including supported internships), detailed engagements and project outcomes under `projects/`; never bulk-copy or silently rewrite old sources.
6. **Review and continue.** After each import batch, check created paths/links and give a short checkpoint: **captured, still missing/uncertain, explicitly deferred, and recommended next focus**. Update `career/README.md` with source decisions and onboarding progress. **Do not treat an initial successful write as the end of guided setup**; ask the next useful question or offer to review another selected area. Respect a request to pause, skip or stop.
7. **Finish intentionally.** When the user confirms that the desired setup scope is covered, or explicitly chooses a minimal setup, summarize what is usable, which areas remain pending and what to do next. Mark the checkpoint as **ready**, **paused** or **blocked**, accurately distinguishing workspace creation from information completeness. Suggest one optional next workflow; setup and individual task skills remain independent.

## Done when

- The user explicitly chose or confirmed the destination before any setup inspection or creation, and was guided through source discovery and the chosen import scope (or opted for shorter setup).
- The index and selected standard homes exist if writing was authorized; actual writes and link checks are verified.
- Sources, known gaps, decisions and resume point are traceable; originals and permissions are respected.
- A mere scaffold/first import is never described as a fully completed guided onboarding without the user's agreement.
