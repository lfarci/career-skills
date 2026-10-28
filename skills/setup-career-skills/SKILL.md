---
name: setup-career-skills
description: "Guide me through setting up a standardized private career workspace: find existing sources, ask about missing information and import selected records step by step."
disable-model-invocation: true
---

# Setup Career Skills

**Guide the user through a resumable onboarding conversation**, not just directory creation. Initialize a private `career/` with five named homes. Existing notes, resumes, profiles and projects are potential sources; never import all of them without selection. Read [setup conversation and source rules](references/workspace-model.md) when starting or resuming.

## Contract

- **Input:** User's setup goal, preferred private storage and write policy when known, existing documents or permission to look for sources.
- **Scope:** Discover sources, identify meaningful gaps, scaffold the standard workspace and progressively import user-selected records. An occupied legacy root requires an explicit adoption choice.
- **Output:** A verified `career/README.md` (or proposed plan without write access), standard homes as needed, an import/gap status, and **a concrete next question or confirmed completion**.

## Steps

1. **Orient and resume.** Check the conversation and any existing `career/README.md` for the chosen destination, prior answers, imported content and pending work. Never repeat answered questions or restart setup after partial completion. If the destination is occupied, offer a separate private `career/` or an approved in-place migration; do not overwrite.
2. **Ask about existing sources.** Proactively ask whether the user has an old resume, notes, role/project history, certificates, portfolio or professional-profile exports, including where the agent may look. Use known accessible locations as suggestions rather than scanning indiscriminately. Inventory permitted sources briefly, flag unreadable ones and **ask whether anything important is missing**. If none exist, guide a small conversational intake from scratch.
3. **Plan coverage with the user.** Identify the highest-value initial information and compare it with selected sources: employers, roles, dates and internships; assignments/projects; skills and qualifications; education/languages; goals/preferences; brand/assets; optional research and publication destinations. Mark each relevant area as supported, missing, conflicting or deferred. **Ask one focused question at a time** to resolve important omissions or choose what to import next. Don't require complete information in every area or a fixed questionnaire.
4. **Create and import selectively.** Confirm private location, scope and write/PR permission. Create `career/README.md` and only the standard home folders needed for selected records; record other homes as pending in the index, without empty placeholders. Import supported claims with source references, evidence limits and uncertainty. Keep `profile/experience.md` for role history (including supported internships), detailed engagements and project outcomes under `projects/`; never bulk-copy or silently rewrite old sources.
5. **Review and continue.** After each import batch, check created paths/links and give a short checkpoint: **captured, still missing/uncertain, explicitly deferred, and recommended next focus**. Update `career/README.md` with source decisions and onboarding progress. **Do not treat an initial successful write as the end of guided setup**; ask the next useful question or offer to review another selected area. Respect a request to pause, skip or stop.
6. **Finish intentionally.** When the user confirms that the desired setup scope is covered, or explicitly chooses a minimal setup, summarize what is usable, which areas remain pending and what to do next. Mark the checkpoint as **ready**, **paused** or **blocked**, accurately distinguishing workspace creation from information completeness. Suggest one optional next workflow; setup and individual task skills remain independent.

## Done when

- The user was guided through source discovery, a meaningful gap review and their chosen import scope, or explicitly chose a shorter setup.
- The index and selected standard homes exist if writing was authorized; actual writes and link checks are verified.
- Sources, known gaps, decisions and resume point are traceable; originals and permissions are respected.
- A mere scaffold/first import is never described as a fully completed guided onboarding without the user's agreement.
