---
name: personal-brand
description: Decide how the user presents themselves publicly (role and strengths to put forward, target surfaces) and draft publishable text (LinkedIn headline and About, GitHub profile README, site, X/Bluesky and freelance bios) for the surfaces the user confirms. Use only when the user asks for this skill by name.
---

# Personal Brand

The profile is the private truth; the personal brand is the public facet of that truth. It chooses **which role and which parts of the career to put forward**, **on which surfaces**, and writes the **text** people will read there. Every claim comes from the profile; every output is a draft until the user approves it. Visuals (palette, fonts, logo, banners) belong to `visual-identity`.

## Contract
- **Input:** profile/ and projects/ records, profile/direction.md, existing brand/ records and any live text the user supplies.
- **Scope:** Positioning, surface strategy and publishable text. Never change facts, never publish.
- **Output:** `brand/positioning.md`, `brand/surfaces.md` ([format](references/surfaces-record.md)), text drafts in `assets/drafts/copy/<surface>.md`, copied to `assets/staged/copy/` after approval.

## Steps

1. **Confirm surfaces.** Before any copy, know which public presences the user has or wants. If `brand/surfaces.md` exists, show its entries (name, status) and ask the user to confirm or correct them. Otherwise ask one short checklist question, for example: "Which of these do you have or want? LinkedIn · GitHub · personal website · X · Bluesky · Credly / Microsoft Learn · Malt or another freelance platform · other". When the request already lists the surfaces, restate them and treat that as the answer. Never guess a surface or a URL from the profile.
2. **Positioning.** From the records, propose the role to lead with, two or three evidence-backed strengths and the audiences (recruiters, clients, peers). Offer real alternatives when the records support more than one. Save the choice in positioning.md with a short canonical headline and bio.
3. **Surfaces record.** Write or update surfaces.md: one entry per confirmed surface with why, audience, emphasis and status (`active` exists or is being created now, `planned` later, `dropped` with the reason). Ask for missing URLs; leave them out rather than invent them.
4. **Copy.** Draft copy only for `active` surfaces the user confirmed; `planned` and `dropped` surfaces get none. Before drafting a surface, read only its reference: [LinkedIn](references/surfaces/linkedin.md), [GitHub profile README](references/surfaces/github.md), [personal website](references/surfaces/website.md), [X / Bluesky](references/surfaces/x-bluesky.md), [Malt / freelance platforms](references/surfaces/freelance.md), [Credly / Microsoft Learn](references/surfaces/credentials.md). The examples there are patterns: fill them from the records, never copy their wording or facts. Reuse the canonical headline and bio; adapt length and emphasis, not facts, and stay within the listed limits.
5. **Truth check.** Use only claims the records mark user-confirmed or that two sources agree on; mark single-source, conflicting or missing facts inline with `[CONFIRM]` and ask before staging. Keep each title with its employer and dates. Label goals as goals; leave private doubts, plans and constraints out. A blanket "approve whatever you draft" covers wording, not unverified claims.
6. **Hand off.** Show the drafts, stage only what the user approves, and say what to paste where. Suggest `audit` to compare live surfaces with the staged copy, and `visual-identity` for logo and banners on the same surfaces.

When the workspace has a root `README.md` index, add a link to each new record under `Records` and change nothing else there: `Setup progress` belongs to setup, so report your next steps in the reply.

## Done when
- positioning.md names the lead role, strengths and audiences, each traceable to profile records.
- The user confirmed the surface list (or the existing surfaces.md) before any copy was drafted.
- surfaces.md has one entry per confirmed surface with purpose, emphasis, status and a last-reviewed date.
- Each `active` surface in scope has a draft in `assets/drafts/copy/<surface>.md` and no other surface has one; staged copy contains only approved text and no unconfirmed claim.
- Nothing was published and no profile record changed.
