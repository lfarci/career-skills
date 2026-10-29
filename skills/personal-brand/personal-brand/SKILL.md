---
name: personal-brand
description: Decide how the user presents themselves publicly (role and strengths to put forward, target surfaces) and draft publishable text such as headlines, bios, LinkedIn About, experience descriptions and GitHub profile READMEs. Use only when the user asks for this skill by name.
---

# Personal Brand

The profile is the private truth; the personal brand is the public facet of that truth. It chooses **which role and which parts of the career to put forward**, **on which surfaces**, and writes the **text** people will read there. Every claim comes from the profile; every output is a draft until the user approves it. Visuals (palette, fonts, logo, banners) belong to `visual-identity`.

## Contract
- **Input:** profile/ and projects/ records, profile/direction.md, existing brand/ records and any live text the user supplies.
- **Scope:** Positioning, surface strategy and publishable text. Never change facts, never publish.
- **Output:** `brand/positioning.md`, `brand/surfaces.md` ([format](references/surfaces.md)), text drafts in `assets/drafts/copy/<surface>.md`, copied to `assets/staged/copy/` after approval.

## Steps

1. **Positioning.** From the records, propose the role to lead with, two or three evidence-backed strengths and the audiences (recruiters, clients, peers). Offer real alternatives when the records support more than one. Save the choice in positioning.md with a short canonical headline and bio.
2. **Surfaces.** Inventory the user's public presences (for example GitHub profile README, personal site, LinkedIn, Credly, Microsoft Learn transcript). For each, record why to target it (or drop it), its audience, what to emphasise and its status. Ask about surfaces you cannot find; never guess URLs.
3. **Copy.** For the requested surfaces, draft the pieces each needs: headline, About/bio, role descriptions as published, README sections, site copy. Reuse the canonical headline and bio; adapt length and emphasis per surface, not facts.
4. **Truth check.** Use only claims the records mark user-confirmed or that two sources agree on; mark single-source or conflicting claims inline and ask before staging. Keep each title with its employer and dates. Label goals as goals; leave private doubts, plans and constraints out. A blanket "approve whatever you draft" covers wording, not unverified claims.
5. **Hand off.** Show the drafts, stage only what the user approves, and say what to paste where. Suggest `audit` to compare live surfaces with the staged copy.

When the workspace has a root `README.md` index, add a link to each new record under `Records`.

## Done when
- positioning.md names the lead role, strengths and audiences, each traceable to profile records.
- surfaces.md has one entry per known surface with purpose, emphasis, status and a last-reviewed date.
- Each requested surface has a draft in `assets/drafts/copy/`; staged copy contains only approved text and no unconfirmed claim.
- Nothing was published and no profile record changed.
