---
name: visual-identity
description: Define, record, create or review the user's visual identity, meaning a logo and banners for the surfaces they use (LinkedIn, X, GitHub, site) plus the palette and fonts those need. Use only when the user asks for this skill by name.
---

# Visual Identity

The visual identity is what the personal brand looks like. MVP scope: a **logo** (plus a favicon derived from it when there is a site) and **banners** for the surfaces the user confirmed, with just enough **design system** (palette, fonts) to make them consistent. One record holds it: `brand/identity.md`. Words, headlines and surface strategy belong to `personal-brand`; this skill only uses the text it is given.

## Contract
- **Input:** The user's request, references they explicitly select, existing `brand/identity.md`, `brand/surfaces.md` (which surfaces need visuals) and files under `assets/`.
- **Scope:** Brief, design system, asset creation and design review. Never edit facts or public copy, never publish.
- **Output:** `brand/identity.md` (brief, design system, brand-tokens block, links to assets); files in `assets/drafts/<kind>/`, approved copies in `assets/staged/<kind>/` ([naming](references/asset-structure.md)). A review returns findings only.

## Confirm surfaces first
Read `brand/identity.md` and `brand/surfaces.md` when they exist. Before planning assets, list the surfaces that need visuals: the `active` entries in surfaces.md, or, without it, ask one short checklist question (LinkedIn · X · Bluesky · GitHub · personal website · other). Plan assets only for confirmed surfaces: a logo, one banner master with a crop per confirmed surface ([sizes](references/banner-sizes.md)), a favicon only when a site is confirmed. Avatars, icon sets, social post templates and full UI kits are out of the MVP; offer them only when the user asks.

## Pick the branch
Do only what the request needs:

1. **Record an existing identity.** The user already has colours, fonts or files: record them as they are, link existing files, and write the brand-tokens block with `status: pending`. Show the exact values and set `approved` only after the user confirms them; "my existing identity" is not that confirmation.
2. **Brief.** Nothing agreed yet: ask one question at a time about the impression the logo and banners should leave and who sees them. Do not infer a style from a technical career or past experiments. Save answers, the confirmed surfaces and open choices under `## Brief` in identity.md.
3. **Design system.** Agree palette (roles + hex) and heading/body fonts with licences, only as far as the logo, banners and resume need. Write the brand-tokens block per the reference.
4. **Assets.** Per kind (logo, banner), present two or three concepts in words with a recommendation and wait for a choice before writing files. Selection is per kind: an approved logo constrains a banner but does not select one. Logos: read [logo principles](references/logo-design-principles.md). Vectors: read [SVG guidance](references/svg-tooling.md). Banners: one master, then one crop per confirmed surface with its safe area.
5. **Review.** Critique given files against the brief: fit, recognition, hierarchy, contrast, crops and safe areas, small-size legibility. Tie each finding to a file and a concrete fix; separate taste from failures. When you cannot view images, review the source and list visual judgments as **Unchecked**. A review edits nothing and approves nothing.

## Approve and verify
- Approval names an exact version (`a-v2`). Copy that file unchanged to `assets/staged/<kind>/`, link it in identity.md, keep earlier versions. A preference is a selection, not an approval.
- Render and inspect what you can; say which checks did not run.
- Before reporting, run `python3 scripts/check_assets.py <workspace-root>` from this skill's folder and fix every error. Without Python, check the naming rules by listing files.

When the workspace has a root `README.md` index, add a link to each new record under `Records`.

## Done when
- Assets were planned only for confirmed surfaces: logo, banner crops for those surfaces, favicon only with a site.
- identity.md states the brief, the design system decided so far and links every draft and staged file.
- Brand-tokens are `approved` only after the user confirmed those exact values.
- Concepts preceded files; approval is per exact version and traceable.
- `check_assets.py` passes, or the unrun checks are listed.
