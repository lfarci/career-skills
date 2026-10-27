---
name: maintain-profile
description: Maintain an evidence-backed career profile by adding or correcting experience, qualifications and projects, or reviewing factual accuracy. Ask for the user's goal before acting when the request is open-ended.
---

# Maintain a Canonical Career Profile

Help the user maintain a truthful private record of experience, projects, achievements, qualifications, feedback and supporting sources. Keep facts distinct from career aspirations, development plans and public positioning. Reuse their existing source of truth, if any; a configured workspace is optional.

**Intent before investigation:** A bare skill invocation or a general request for profile help is not authorization to audit everything or change records.

## Contract
- **Input:** The user's intended task (possibly not stated yet), available testimony or evidence, and relevant existing records if any.
- **Scope:** First establish the requested focus; then work only on selected factual records, keeping other career workflows separate.
- **Output:** When intent is unclear, a concise next question. Otherwise, a focused assessment, new profile section or supported change proposal/patch, with sources and unresolved conflicts.

## Steps

1. **Establish intent first.** If the user has not named a task, ask one short question before examining files or making edits, such as: *"What would you like to do with your career profile: add information, correct something, review its accuracy, or build one from scratch?"* Use known conversation context to avoid repeating answers. If the requested outcome is already clear, proceed directly without a generic interview.
2. **Agree on a manageable focus.** When the user has existing records, ask which part or outcome deserves attention before starting a broad review. For a new profile, ask what to capture first (for example work history, projects, skills or qualifications); gather essential facts conversationally rather than demanding a full questionnaire or creating a folder tree. One relevant question at a time is preferable to a long checklist. Do not force setup.
3. **Read only what serves that focus.** Locate the relevant canonical record and check any supplied evidence. If multiple sources disagree, identify the authority or ask about the specific conflict. Do not crawl the whole workspace or create an unrelated TODO list merely because records are available.
4. **Review facts carefully.** Distinguish evidence status (user-confirmed, independently corroborated, inferred, unverified) from time status (current, historical, planned, superseded, unknown). Preserve uncertainty, approximate metrics and the distinction between planned and earned qualifications.
5. **Separate review from editing.** If the user requested a review, present prioritized findings before proposing changes; a review request alone does not authorize edits. For a specified update, propose the smallest supported change and apply it only when the task and existing write permissions authorize it. A general setup permission does not make an unrequested audit or cleanup an intended task. When authorization is unclear, ask before applying.
6. **Close the chosen task concisely.** State what was checked, what was proposed or actually changed, and only the relevant unresolved questions. Mention downstream public surfaces only if the chosen fact materially affects them; do not rewrite or publish those surfaces without a separate request.

## Output

- **No clear task:** One short question to identify intent, not an unsolicited audit or patch.
- **Existing profile:** Targeted assessment or minimal evidence-backed change, with record references and important conflicts.
- **Starting from scratch:** A user-chosen first section or a brief plan for it, using only supplied facts.
- **No write permission:** Reviewable proposed patch, accurately labeled as unapplied.

## Done when

- The requested scope was confirmed or the necessary first question was asked before any unrequested audit or edit.
- User-directed facts and records, not workspace availability, determined the work performed.
- Every changed fact is supported by confirmation or labeled source evidence; re-running does not create duplicates.
- Unresolved conflicts, limitations and the actual write status are explicit.
- Aspirations, sensitive records and public positioning remain distinct; no downstream publication was inferred.
