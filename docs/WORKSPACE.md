# Career workspace

Use ordinary Markdown and links in any user-selected storage: local files, a Git repository, Drive, OneDrive or another Markdown-capable provider. The entire workspace is private, including assets intended for external use. The layout describes career records, not installable skill categories.

## Five homes

| Directory | Owns | Related skills |
| --- | --- | --- |
| profile/ | Background, capabilities, aspirations, preferences and development | reflect, maintain-profile, plan-development, review-progress |
| projects/ | Career-oriented project records and links to actual work | maintain-profile; other skills consume selected project evidence |
| brand/ | Positioning, audiences, messaging principles, design briefs and visual rules | personal-brand, define-design-brief, create-design-assets, review-design |
| assets/ | Reusable external-facing outputs, drafts, approved staged material and surface descriptions | personal-brand, build-resume, design skills, audits |
| research/ | User-selected company, opportunity and comparator references; archived research | find-companies, find-jobs, benchmark-profile, review-research |

Profile grounds brand and growth decisions; projects can supply evidence. Brand guides assets. Selected research informs market understanding, targeting, presentation and development. Research about someone else never proves a personal capability. A project is not automatically evidence: link the repository, outcome or feedback supporting a particular claim.

## Reference layout

```text
career/
  README.md
  profile/
    experience.md
    education.md
    qualifications.md
    languages.md
    skills.md
    direction.md
    preferences.md
    development.md
  projects/
    project-name.md
  brand/
    positioning.md
    identity.md
  assets/
    drafts/
    staged/
    services.md
  research/
    companies/
    opportunities/
    profiles/
    archive/
```

Create only needed records; combine or split files when useful. direction.md can hold north star, values, motivations, interests and goals. development.md holds actions, evidence milestones and dated progress reviews. Project records describe purpose, status, contribution, skills used, learning, relevance to a resume and links to work; do not copy source code or the project's backlog.

brand/ contains guidance, not a second asset library. identity.md can describe fonts, palette, logo and composition rules, linking actual sources under assets/. Design interview answers can live in brand/discovery.md. Existing conventions take precedence when mapped clearly.

## Assets and services

- drafts/ contains proposed text and visual work; staged/ contains the latest explicitly approved reusable versions. Neither proves publication. Preserve meaningful option/revision history without a mandatory final/ directory.
- Organize by content/use (bios, headlines, resumes, logos, banners) only when needed. Reuse a shared bio or headline across surfaces; create separate adaptations only for intentional differences. Link rather than duplicate common content or visual masters.
- services.md describes each external surface: service and account/name, URL or source repository, purpose/audience, staged asset references, available ways to inspect/update it, access limitations and relevant permissions. Split into per-service records if useful; do not assume APIs, scraping or automation work.
- Live surfaces establish actual published state; the profile establishes supported personal facts and intentions. Source code can help inspect a website but does not prove what is deployed. A staged asset is not a published snapshot.
- Compare accessible live content, or user-provided exports/pasted text, with the relevant staged material. State source and inspection date/limits; do not require a historical snapshot store. If there is a difference, ask whether to update the workspace, the external surface or leave an intentional adaptation. Do not guess which side changed.
- Flag factual incoherence before importing public edits into the profile. Importing wording does not establish the truth of a new credential, role or achievement. Publication requires the user's authorization; manually copying staged material is a valid workflow.

## Research selection and retention

- Present a shortlist first; the user may save some, all or none, or supply references directly. An explicit instruction to save a defined set also authorizes retention. Do not save every discovered result automatically.
- Keep one useful record per selected company, opportunity or comparator; link an opportunity to its company rather than duplicating the company description. profiles/ includes professional profiles, portfolios and resume references; a comparison across several may be a linked summary.
- Save sources, checked dates, useful findings, why the user retained the reference, relevance/fit, unknowns and next decisions as applicable. Store links to other people's resumes, not copied resume files. Keep only useful observations, not every query, page or intermediate thought.
- Research is a long-term reference library. An expired job may still explain market requirements; an older profile can remain useful inspiration. Age alone does not make a record disposable.
- review-research runs on request. Prefer archiving under user guidance, retaining useful history and updating affected links. Deletion is manual. During unrelated work, an agent noticing stale content asks whether the user wants it reviewed; it does not silently archive, delete or start background maintenance.

## Workspace index and record rules

Use the existing career README or another chosen index to map these five homes to actual canonical files/sections and link projects, services and optional trackers. Record the storage root/provider and branch/PR policy where applicable, read/write boundaries, external publication permissions and unresolved mappings. Never store credentials in it.

For existing notes, map before moving: profile/goals.md may already hold direction; an existing personal-projects/ may map to projects/ and personal-brand/ to brand/. Renaming the reference layout does not authorize migrating user files. Ask only relevant missing decisions; do not require complete setup.

Use readable headings and relative links; no mandatory YAML, IDs or database. Separate facts, user preferences, interpretations and aspirations. Retain source/date and current/planned/superseded status where material. Decisions include rationale; actions include next steps and evidence/review points. Preserve uncertainty and meaningful history.

Before editing, read current canonical records and preserve unrelated changes. Use available version/conflict controls and the chosen write workflow. Confirm saves and links; when writes are unavailable, provide a proposed patch without claiming success. Skills remain useful from pasted input or selected files without an index, another skill or a specific provider.

## On-demand workspace validation

Use `validate-workspace` **only when needed**: a configured path no longer resolves, a relative link is broken, the chosen index is stale, or two candidates claim to be the same canonical record. Direct user requests for workspace validation also qualify. A normal working layout, even with custom folder names or uncreated homes, needs no scan or refactor.

The validator reads the relevant index and records, checks only affected mappings, and prefers updating the mapping or link to moving files. Missing setup does not block another skill from using supplied records. Do not infer permission to reorganize or delete from repository write access; structural moves need explicit authorization. A task that only requires an index link may use an already-authorized narrow fix, otherwise provide a patch for approval.

Initial discovery and configuration belong to `setup-career-skills`; factual updates belong to `maintain-profile`. `validate-workspace` handles structural integrity and hands the resolved paths back to the active workflow. Invocation between skills depends on the agent host; none may require the validator to be installed.

## Skill contracts and paths

Each SKILL.md defines a concise Input / Scope / Output contract: required records or supplied material, the responsibility boundary, and the destination/result. Contract paths are relative to the chosen career workspace root and are defaults; the workspace index maps them to existing files. They are not installation paths or mandatory filenames. Without an index, use supplied inputs and clarify only missing authority or destination decisions relevant to the task.

Keep workspace-wide structure and lifecycle rules here. Skill contracts name only their own inputs and outputs; they do not repeat all five homes, storage-provider instructions or unrelated lifecycle rules. A skill remains independently usable from its task-specific contract and workflow; no runtime schema, mandatory setup skill or full-workspace read is required.
