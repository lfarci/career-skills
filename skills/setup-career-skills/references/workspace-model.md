# Career workspace rules

Read this reference when importing career sources, choosing canonical records or resuming a previous setup. The **chosen folder itself** is the workspace root. An existing `career/` in the current repository is not automatically the selected destination.

## Record ownership

Create these homes **as needed**, directly under the chosen root:

- `profile/`: identity, employers/grades/dates (including supported internships), skills, qualifications and goals.
- `projects/`: consulting assignments, personal projects, contributions and evidence.
- `brand/`: positioning, audiences and visual guidance.
- `assets/`: staged and draft reusable materials.
- `research/`: selected companies, opportunities and comparisons.

`profile/experience.md` holds employer and role history, while assignments and their outcomes belong in `projects/` when selected. Distinguish verified or user-reported facts from aspirations, messaging and live publication. Reuse supported facts without inventing achievements, dates or credentials.

## New: source handling

Ask which sources the user authorizes you to read. Start with indexes and summaries of CVs, prior notes, resumes, portfolios, project records and credentials; open detailed records only for the approved import or a relevant conflict. Recommend a useful first subset. Extract selected claims into canonical records and link original evidence. Preserve uncertainty and separate grade from functional role. A summary does not replace its supporting source. The user may choose minimal index-only setup.

**Archives** (for example a LinkedIn data export `.zip`): list the members first (Python's standard `zipfile` works on every OS), then read only the files the batch needs, such as `Profile.csv`, `Positions.csv`, `Education.csv`, `Skills.csv`, `Languages.csv`, `Certifications.csv`, `Projects.csv`. Read members in place or extract to a temporary folder outside the workspace; never unpack into the root. Messages, connections, invitations, contacts and ad data concern other people or are private: list them as `excluded` and do not open them. The archive itself is the source in the inventory.

**Existing workspace as a source** (its own index, records, or homes such as `personal-brand/`): map each of its files to a record, one to one where possible, and carry the content over rather than a summary; note in the inventory any file only partly carried and what stayed behind. When the user may prefer one workspace instead of two, mention restructuring the old one in place (Resume, then the repair rule) as the alternative.

When the user expressly asks to create the chosen folder first, create it with available permission **and continue** into source discovery; an empty directory is not the end of setup.

## Resume: validation

Before changing an existing workspace:

- Check root `README.md`, including source map, authorized writes and saved next decision. If absent, inspect existing records and propose an index repair.
- Resolve referenced files and local links; note missing material and conflicting canonical owners. Unused homes need not exist.
- Recover captured, pending and deferred areas, and prior answers. Report `usable`, `needs repair` or `blocked` and the smallest next action.

A usable legacy layout can remain operational. `validate-workspace` is optional for difficult structural issues, not required for normal setup. Preserve current user choices instead of restarting the interview.

## Lightweight checkpoint

The root `README.md` records the destination, approved source and write scope, captured/pending/deferred areas, setup status (`in progress`, `paused`, `ready`, `blocked`) and **one next decision**. After each approved import, verify the actual files and links, then update this checkpoint. Stop only when the user pauses or confirms that the selected setup scope is complete.
