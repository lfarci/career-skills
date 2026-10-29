---
name: maintain-profile
description: Maintain evidence-backed career facts (experience, skills, qualifications and projects). Ask what to focus on when invoked without a specific request.
---

# Maintain a Canonical Career Profile

Maintain the user's private source of truth for experience, projects, achievements, qualifications and supporting evidence. Keep facts separate from career direction, development plans and public positioning. Use existing records if available; setup is optional.

## Contract
- **Input:** A requested task or, when unspecified, the user's intention; relevant facts, evidence and existing records if any.
- **Scope:** Establish the focus first, then examine or update only records needed for that task.
- **Output:** One clarifying question when unscoped; otherwise a targeted profile section, factual assessment or supported patch.

## Record map

Follow the workspace's existing layout when its index maps records. Otherwise, and when starting from nothing, put each fact in its record below (paths relative to the workspace root), creating a file only when it gets content. When you create a record, add its link under `Records` in the root `README.md`, creating a minimal index with only `Records` and `Source inventory` if none exists (`Setup progress` belongs to setup).

<!-- record-map -->
| Fact | Record |
| --- | --- |
| Name and contact details the user chose to import (name, e-mail, phone, main public links used on a resume) | `profile/contact.md` |
| Employers, titles/grades, dates, internships | `profile/experience.md` |
| Degrees and schools | `profile/education.md` |
| Certifications, licences, awards | `profile/qualifications.md` |
| Skills and tools | `profile/skills.md` |
| Spoken languages | `profile/languages.md` |
| Goals, north star, considered next steps | `profile/direction.md` |
| Location, work mode, commute, contract, salary preferences | `profile/preferences.md` |
| Client assignments, side projects, contributions and their outcomes | `projects/<project>.md`, linked from the role in `experience.md` |
| Positioning, bios, visual guidance | `brand/` (only when the source contains it) |
| Every public surface: URL, purpose, why targeted, emphasis (may repeat links from contact.md) | `brand/surfaces.md` |
| Reusable resumes, bios, banners | `assets/drafts/` or `assets/staged/` (approved) |
| Saved companies, job ads, comparator profiles | `research/` |
<!-- /record-map -->

## Steps

1. **Establish intent before investigating.** A bare invocation or “help with my profile” is not a request to audit or edit everything. If the conversation does not identify a task, ask **one short question**, such as: *“Would you like to add information, correct a fact, review accuracy, or start a profile?”* Stop there until the user responds. Reuse known context; never ask this again for an already-clear request.
2. **Choose a useful starting point.** If records exist but the requested focus is unclear, ask which area or outcome matters. If starting from scratch, ask what to capture first (work history, projects, skills or qualifications). Gather missing details conversationally, one relevant question at a time. Do not require a full questionnaire, setup process or new folder tree. If the user explicitly requests a full audit, that is a valid scope.
3. **Inspect only relevant evidence.** Find the applicable canonical record; compare new information with existing facts. Do not turn available workspace access into a general sweep, speculative corrections or an unrelated TODO list. Resolve contradictory sources where possible; otherwise mark the conflict. If the selected source path is stale or its canonical mapping is ambiguous, use `validate-workspace` when available to resolve only that structural blocker, then resume the requested profile task; otherwise offer a minimal path fix.
4. **Classify claims correctly.** Distinguish evidence status (user-confirmed, corroborated, inferred, unverified) from time status (current, historical, planned, superseded, unknown). Do not promote planned credentials, inflate skills or remove legitimate approximations.
5. **Separate review from editing.** A request to review is read-only unless the user also requests changes. For an authorized update, make the smallest evidence-backed change consistent with the user's instruction and permissions. Prior workspace write access alone is not a request to perform an unsolicited cleanup. Never expose private or client-sensitive details on public surfaces.
6. **Close concisely.** Report what was checked, what changed or remains proposed, and only the conflicts relevant to the selected goal. Flag downstream surfaces when materially affected, but do not modify or publish them without a separate request.

## Output

- **No stated task:** Just the intent question, not a workspace audit.
- **Existing records:** Focused read-only findings or a minimal patch with source and evidence status.
- **No existing records:** A user-selected first section or a small plan, without inventing details.
- **No write access:** A proposed patch, never a claim of completion.

## Done when

- The user's intention determines the work; no unrequested review or edit was performed.
- Every changed fact has support, and repeated input causes no duplicates or needless edits.
- Unresolved conflicts and actual write status are explicit.
- Private facts, aspirations and public messaging remain distinct.
