# Minimal visual brand kit (optional)

Read this only when a user asks about reusable visual identity or when visual consistency matters to a surface audit. Keep the record in the user's chosen workspace, not in the public skills repository.

## Suggested one-page inventory

Keep the kit in `brand/identity.md` (create it when needed). A Markdown table or short list is enough; fields may be omitted when unknown.

| Element | Approved asset or value | Intended uses / variants | Source location |
| --- | --- | --- | --- |
| Banner | Link/path to original | Website, LinkedIn crop, GitHub version | Link/path |
| Logo or avatar | Link/path to reusable source | Light/dark or square variants, if existing | Link/path |
| Icons | Icon set or relevant files | Favicon, profile, project thumbnails | Link/path |
| Palette | Hex values and short roles (e.g., primary/accent) | Background, headings, highlights | Note or design source |
| Fonts | Family names and safe fallbacks | Heading and body, when platform permits | License/source reference |

Avoid collecting the raw assets or font binaries in this public repository. Preserve their provenance and license if known. If there is no established visual identity, document existing choices and suggest at most a few practical improvements rather than inventing a large brand system.

## Palette and fonts for resumes and documents

When the user has a palette or fonts (existing or newly agreed), also record them in `brand/identity.md` as the shared brand-tokens block so `build-resume` can apply them. Write `status: pending` first, even for values the user calls their existing identity: values read from a note, file or site are not yet confirmed. Show the exact values, ask the user to confirm them, and switch to `status: approved` only after they do.

<!-- brand-tokens -->
Resume and document styling reads one fenced block in `brand/identity.md`. Visual-identity skills write it; `build-resume` reads it. One `key: value` per line; omit keys you have not decided.

```brand-tokens
status: approved          # approved | pending; pending tokens are not applied without the user's say-so
primary: #0F766E          # headings and section bars (contrast >= 3:1 on white)
accent: #B45309           # headline and highlights (contrast >= 3:1 on white)
text: #1F2937             # body text (contrast >= 4.5:1 on white)
muted: #4B5563            # dates, locations, secondary text (contrast >= 4.5:1 on white)
heading-font: Manrope     # installed font family name; licence link in prose below the block
body-font: Source Sans 3
```

Colours are `#RRGGBB`. Write the block with `status: pending` while concepts are drafts and switch to `approved` only when the user approves the palette and fonts. Values that fail the format or contrast rule are ignored with a warning, and the neutral default is used.
<!-- /brand-tokens -->

## Applying it

- Reuse an existing approved asset or a deliberate size/crop/contrast variant before making another.
- Optimize for recognizable identity, readable text and consistency across surfaces, not pixel-perfect sameness.
- Platform-provided fonts, avatar masks, crop dimensions, or limited styling controls are legitimate differences.
- Audit only visuals actually available for inspection; when an image or computed font cannot be verified, mark it unknown.
- Create or edit new banners, logos, icons or other graphics only when the user requests that output and appropriate tools are available.

