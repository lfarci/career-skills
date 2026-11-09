---
name: maintain-profile
description: Maintain evidence-backed career facts (experience, skills, qualifications, achievements, interview stories and projects) and stated job criteria. Ask what to focus on when invoked without a specific request.
---

# Maintain a Canonical Career Profile

Maintain the user's private source of truth for experience, projects, achievements, stories, qualifications and supporting evidence, plus the criteria the user states for screening roles. Keep facts separate from career direction, development plans and public positioning. Use existing records if available; setup is optional.

## Contract
- **Input:** A requested task or, when unspecified, the user's intention; relevant facts, evidence and existing records if any.
- **Scope:** Establish the focus first, then examine or update only records needed for that task.
- **Output:** One clarifying question when unscoped; otherwise a targeted profile section, factual assessment or supported patch.

## Record map

Follow the workspace's existing layout when its index maps records. Otherwise, and when starting from nothing, put each fact in its record below (paths relative to the workspace root), creating a file only when it gets content. When you create a record, add its link under `Records` in the root `README.md`, creating a minimal index with only `Records` and `Source inventory` if none exists (`Setup progress` belongs to setup).

<!-- record-map -->
| Fact | Record |
| --- | --- |
| Name and contact details the user chose to import (name, e-mail, phone, main public links used on a resume) | `profile/facts/contact.md` |
| Employers, titles/grades, dates, internships; optional self-assessed responsibility level per role | `profile/facts/experience.md` |
| Degrees and schools | `profile/facts/education.md` |
| Certifications, licences, awards; expired or outgrown ones under `## Historical credentials` | `profile/facts/qualifications.md` |
| Skills and tools | `profile/facts/skills.md` |
| Spoken languages | `profile/facts/languages.md` |
| Dated achievements, recognition and feedback received (brag log) | `profile/facts/achievements.md` |
| Interview stories (Situation, Task, Action, Result), each linked to its project or achievement | `profile/facts/stories.md` |
| Current compensation package (salary, bonus, car or mobility, vouchers, insurance, pension) as a private baseline | `profile/facts/compensation.md` |
| Location, work mode, travel, commute, contract type | `profile/criteria/conditions.md` |
| Salary and package expectations for a next role: minimum and target, must-have benefits, trade-offs; only values the user sets | `profile/criteria/salary-expectations.md` |
| Must-haves, nice-to-haves and deal-breakers for screening a role or company | `profile/criteria/expectations.md` |
| Values and motivations: what matters, career-anchor ranking, work values | `profile/goals/values.md` |
| North star, goals, ideal job, target role and responsibility level, considered next steps, career-change options | `profile/goals/north-star.md` |
| Planned or target certifications and learning credentials (earned ones stay in `qualifications.md`) | `profile/goals/certifications.md` |
| Development plan: objectives, actions with estimated and actual dates, dated reviews | `profile/goals/development.md` |
| Client assignments, side projects, contributions and their outcomes | `projects/<project>.md`, linked from the role in `experience.md` |
| Positioning, bios, visual guidance | `brand/` (only when the source contains it) |
| Every public surface: URL, purpose, why targeted, emphasis (may repeat links from contact.md) | `brand/surfaces.md` |
| Reusable resumes, bios, banners | `assets/drafts/` or `assets/staged/` (approved) |
| Saved companies, job ads, comparator profiles | `research/` |
<!-- /record-map -->

The three profile layers and optional headings (role fields, brag-log entries, STAR stories, criteria sections) are in [profile layers](references/profile-layers.md). A workspace with the earlier flat `profile/` (for example `profile/experience.md`) stays valid through its index links: write there and keep its layout unless the user asks to standardize.

## Writing records

<!-- writing-rule -->
Records are read mostly by agents, so keep them token-efficient:
1. Dense, factual and scannable: lists and tables over prose; no preamble, filler, repeated context or narrative padding.
2. One home per fact: link to it instead of restating it.
3. Small files, split by topic.
4. Cut words, never information: keep facts, figures, dates, sources, decisions, TODOs, approved or "avoid" wording, approximations and caveats.
5. When you touch a record, condense nearby verbosity the same way; keep file names and anchors stable, or fix the links.
<!-- /writing-rule -->

## Steps

1. **Establish intent before investigating.** A bare invocation or “help with my profile” is not a request to audit or edit everything. If the conversation does not identify a task, ask **one short question**, such as: *“Would you like to add information, correct a fact, review accuracy, or start a profile?”* Stop there until the user responds. Reuse known context; never ask this again for an already-clear request.
2. **Choose a useful starting point.** If records exist but the requested focus is unclear, ask which area or outcome matters. If starting from scratch, ask what to capture first (work history, projects, skills or qualifications). Gather missing details conversationally, one relevant question at a time. Do not require a full questionnaire, setup process or new folder tree. If the user explicitly requests a full audit, that is a valid scope.
3. **Inspect only relevant evidence.** Find the applicable canonical record; compare new information with existing facts. Do not turn available workspace access into a general sweep, speculative corrections or an unrelated TODO list. Resolve contradictory sources where possible; otherwise mark the conflict. If the selected source path is stale or its canonical mapping is ambiguous, use `validate-workspace` when available to resolve only that structural blocker, then resume the requested profile task; otherwise offer a minimal path fix.
4. **Classify claims correctly.** Distinguish evidence status (user-confirmed, corroborated, inferred, unverified) from time status (current, historical, planned, superseded, unknown). Do not promote planned credentials, inflate skills or remove legitimate approximations. A credential that expired, lapsed or that the user has outgrown is historical: keep it under `## Historical credentials` in the qualifications record with issuer, date when known and why it is historical, rather than deleting it or listing it as current.
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
