---
name: visual-identity
description: Define, record, create or review the user's visual identity (palette, fonts, layout/UI rules, logo, avatar, banners). Use only when the user asks for this skill by name.
---

# Visual Identity

The visual identity is what the personal brand looks like: a small **design system** (palette, fonts, layout and UI rules) plus **assets** tied to the person (logo, avatar, icons, reusable banners for posts and accounts). One record holds it: `brand/identity.md`. Words, headlines and surface strategy belong to `personal-brand`; this skill only uses the text it is given.

## Contract
- **Input:** The user's request, references they explicitly select, existing `brand/identity.md` and files under `assets/`.
- **Scope:** Brief, design system, asset creation and design review. Never edit facts or public copy, never publish.
- **Output:** `brand/identity.md` (brief, design system, brand-tokens block, links to assets); files in `assets/drafts/<kind>/`, approved copies in `assets/staged/<kind>/` ([naming](references/asset-structure.md)). A review returns findings only.

## Pick the branch
Read `brand/identity.md` first when it exists, then do only what the request needs:

1. **Record an existing identity.** The user already has colours, fonts or files: record them as they are, link existing files, and write the brand-tokens block with `status: pending`. Show the exact values and set `approved` only after the user confirms them; "my existing identity" is not that confirmation.
2. **Brief.** Nothing agreed yet: ask one question at a time about what to create or improve and why, audience, where it will be used and the impression it should leave. Do not infer a style from a technical career or past experiments. Save answers, scope and open choices under `## Brief` in identity.md.
3. **Design system.** Agree palette (roles + hex), heading/body fonts with licences, and layout/UI rules (spacing, type scale, light/dark, do/don't) only as far as the user's surfaces need. Write the brand-tokens block per the reference.
4. **Assets.** Per kind (logo, banner, avatar, icon), present two or three concepts in words with a recommendation and wait for a choice before writing files. Selection is per kind: an approved logo constrains a banner but does not select one. Logos: read [logo principles](references/logo-design-principles.md). Vectors: read [SVG guidance](references/svg-tooling.md). Banners keep one master; platform crops derive from it.
5. **Review.** Critique given files against the brief: fit, recognition, hierarchy, contrast, crops and safe areas, small-size legibility. Tie each finding to a file and a concrete fix; separate taste from failures. When you cannot view images, review the source and list visual judgments as **Unchecked**. A review edits nothing and approves nothing.

## Approve and verify
- Approval names an exact version (`a-v2`). Copy that file unchanged to `assets/staged/<kind>/`, link it in identity.md, keep earlier versions. A preference is a selection, not an approval.
- Render and inspect what you can; say which checks did not run.
- Before reporting, run `python3 scripts/check_assets.py <workspace-root>` from this skill's folder and fix every error. Without Python, check the naming rules by listing files.

When the workspace has a root `README.md` index, add a link to each new record under `Records`.

## Done when
- identity.md states the brief, the design system decided so far and links every draft and staged file.
- Brand-tokens are `approved` only after the user confirmed those exact values.
- Concepts preceded files; approval is per exact version and traceable.
- `check_assets.py` passes, or the unrun checks are listed.
