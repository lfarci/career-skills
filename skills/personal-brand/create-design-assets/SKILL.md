---
name: create-design-assets
description: Create and refine versioned career visuals such as logos, icons and banners from an agreed design brief.
disable-model-invocation: true
---

# Create Design Assets

## Contract
- **Input:** The current design brief in brand/, selected concept/references and required asset uses.
- **Scope:** Explore agreed concepts, produce and verify visual outputs; do not redefine professional positioning.
- **Output:** Versioned options/sources in assets/drafts/; approved reusable masters/exports in assets/staged/; linked visual rules in brand/identity.md.

## Establish the input
- Read the current brief and requested deliverables. Ask only blocking gaps about purpose, audience, usage, desired impression or scope before suggesting directions. If discovery is needed, offer define-design-brief when available or ask those questions here; never require another skill.
- Reuse only references and choices the user explicitly makes the basis of this task. Do not infer a geometric/tech direction or preserve a website font from history alone. Keep work career-facing; personal-brand owns professional positioning.
- Confirm storage unless established; reuse discovery.md and existing conventions rather than copying records.

## Agree on a concept
- For logos, read [logo principles](references/logo-design-principles.md) for research, visual criteria and similarity limits.
- Present two or three distinct concepts in words first: ID A/B/C, central idea, relevance to the brief, possible construction and trade-off. Distinguish concept from style. Recommend with reasons; wait for selection before drafting. A concept explicitly selected in the current brief satisfies this step.
- Record concept decisions in discovery.md. If all fail, revisit the idea rather than polishing arbitrary shapes.

## Draft and refine
- Draft only selected concepts and scoped deliverables. Default to two or three distinct executions unless one is requested. Compare typography/layout for composition work and actual content/crops for banners; skip logo work if not requested.
- For logos, apply the monochrome, silhouette and construction criteria from the reference. Inspect drafts and remove near-duplicates.
- Compare under identical conditions and required sizes/backgrounds. Give concise rationale and trade-offs. Preserve accepted features; request feedback before refining. A preference selects a direction, not approval of future versions.
- Add typography, palette and applications when relevant; do not force typography-only or banner work through logo design. Generate full export kits only for selected versions.

## Verify and deliver
- Read [SVG guidance](references/svg-tooling.md) for vector masters and [package structure](references/asset-structure.md) for saving. Use image generation for raster drafts and vector tools/direct SVG for actual vector assets. Render and inspect; label unchecked work.
- Keep options and revisions separate with stable IDs (A/v1 is file `a-v1`); preserve alternatives and feedback. Deliver only scoped assets plus applicable visual rules in identity.md, linked to actual files. Document fonts/licences, palette, layout and logo rules as applicable.
- Verify scoped applications: rendered files, sizes, crops and applicable logo variants. Self-check independently of review-design.
- Before reporting, run `python3 scripts/check_assets.py <workspace-root>` from this skill's folder when Python 3 is available and fix every error (misnamed files, scratch files in assets/, missing identity.md). Without Python, check the same rules from [package structure](references/asset-structure.md) by listing files.
- Obtain explicit approval for an exact revision before marking approved; retain history. Do not publish beyond authorized scope or claim checks not performed.

## Done when
- Concept choice preceded drafts; versions, feedback and approval are traceable.
- Scoped source files/exports and applicable usage rules are saved and linked.
- Actual verification, missing capabilities and unfinished work are explicit.
