# Portable career workspace

Use ordinary Markdown, relative links and the user's existing storage. This is a logical model, not a mandatory schema, folder migration or dependency on GitHub.

## Mental model

| Area | Question | Canonical records | Primary writers |
| --- | --- | --- | --- |
| Direction | What do I want, and why? | North star, interests, preferences, constraints, decisions | reflect |
| Evidence | What have I demonstrated? | Experience, achievements, projects, skills and qualifications with sources | maintain-profile |
| Development | How do I grow toward it? | Prioritized actions, practice, evidence milestones, progress reviews | plan-development, review-progress |
| Personal brand | How do I present myself publicly? | Selected positioning, reusable text, surface inventory, design brief and assets | personal-brand and design skills |
| Job hunt | Which opportunities do I pursue? | Target employers, verified roles, fit notes and tailored application materials | find-companies, find-jobs, build-resume |

Direction chooses priorities; evidence grounds claims; development closes selected gaps. Brand and applications draw on selected evidence and direction. Benchmarks and opportunity research can suggest gaps, but do not redefine goals or prove capabilities. Completed practice feeds evidence only after its outcome is supported. Keep records private by default; public-ready wording is still a draft until publication is authorized.

## Start small

For a new workspace, offer this layout; create only the files needed for the requested work:

```text
career/
  README.md                    # workspace index and source map
  direction.md                 # north star, interests, choices
  evidence.md                  # factual profile and linked sources
  development.md               # actions and dated reviews
  personal-brand/
    messaging.md               # reusable text and surface links
  job-hunt/
    targets.md                 # employers, roles and research dates
```

Split a growing record into a folder only when useful. Projects, credentials, resumes and design assets can stay in existing locations; link them. Design work can use discovery.md, identity.md and versioned assets without a second copy of the professional profile. A file may serve several roles with clearly labelled sections.

## Workspace index

Use an existing career README or chosen index. Record only what is needed:

- Workspace location: local root or provider/repository and base directory; relevant branch/write workflow if applicable.
- Source map: each area, canonical file/section or folder, purpose, and visibility. Include existing evidence/project sources and external public surfaces as links; label unknown or read-only sources.
- Boundaries: private records versus approved public messaging; edits allowed, proposal-only locations and publication permissions.
- Optional tracker: Markdown task list, issue tracker or none. Do not create a parallel task list when a canonical tracker exists.
- Unresolved mappings and decisions, without credentials or unnecessary personal data.

For existing notes, map roles instead of renaming folders: profile/goals.md may hold direction; profile/experience.md and personal-projects/ may hold evidence; personal-brand/ may hold messaging and visuals. Ask where development and job research should live when first needed. Do not embed a real user's repository or private file names in distributable skills.

## Record conventions

- Use readable headings and relative links; YAML, IDs, databases and a fixed template are optional, not required.
- For material claims, retain the source, date/period where relevant, evidence status and whether the claim is current, historical, planned or superseded.
- For decisions, record the choice, rationale and unresolved alternatives. For actions, record the outcome, next step, status and evidence/review point as needed.
- For reusable text, identify audience, source facts, intended surfaces and draft/approved status. Approval of wording is distinct from authorization to publish it.
- For employer/job research, retain source links, checked dates and unknowns. For design, preserve option/revision and approval status.
- Update canonical records incrementally; link outputs and evidence rather than copying entire records between areas. Preserve superseded decisions or version history.

## Storage and operations

Local files, Git repositories and any provider capable of storing Markdown are equivalent destinations. Resolve links relative to the record or workspace root, not an agent's working directory. Provider-specific links can supplement portable relative links. No service, connector, git workflow or issue tracker is mandatory.

Before editing, read the relevant current records, resolve authority conflicts and use the destination's available version/conflict controls. For GitHub, respect the selected branch/PR policy; for files, preserve unrelated edits. Confirm writes and links after saving. If access is read-only or unavailable, provide a proposed patch or document without claiming it was saved.

When setup is skipped, a skill can use a supplied file or pasted brief. Ask only for missing authority, storage or scope decisions relevant to that task; do not force full workspace setup. Never reorganize existing notes merely to match this example.
