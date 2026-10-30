# Design records and assets

brand/identity.md holds the brief, concept choices, the design system and links to asset files; actual files live under assets/. Staged means approved for reuse, not published.

## File names

All paths relative to the workspace root:

| What | Path |
| --- | --- |
| Draft master | `assets/drafts/<kind>/<concept>-v<n>.<ext>`, e.g. `assets/drafts/logo/a-v2.svg` |
| Preview render | `assets/drafts/<kind>/previews/<concept>-v<n>-<size>.png`, e.g. `a-v2-32.png` |
| Approved copy | `assets/staged/<kind>/<concept>-v<n>[-<variant>].<ext>`, e.g. `logo/a-v2-mono.svg` |

`<kind>` is `logo` or `banner` (`favicon` when a site is confirmed; other kinds only when the user asks); `<concept>` is the lowercase concept ID (a, b, c); the selection "A/v2" is file `a-v2`. Lowercase, hyphens, no spaces. `assets/<drafts|staged>/resumes/` belongs to build-resume and is not checked here. Render helpers (HTML pages, scripts) go in a temporary folder outside the workspace.

## identity.md

Suggested sections, only those in use: `## Brief`, `## Design system` (palette roles, fonts with licence links, layout/UI rules), the brand-tokens block, `## Assets` (one line per file: purpose, format, size).

As soon as drafts exist, create or update brand/identity.md with `Status: pending`, the selected concept, and links to each draft master. After the user approves an exact version, copy it to assets/staged/, link the staged file, record palette, fonts (with licence links) and usage rules, and set `Status: approved <version>`. Keep the brand-tokens block below in step with that status: write it as `pending` with the drafts, `approved` only after the user approves the palette and fonts. Keep earlier versions; never overwrite an approved file.

## Brand tokens

<!-- brand-tokens -->
Resume and document styling reads one fenced block in `brand/identity.md`. `visual-identity` writes it; `build-resume` reads it. One `key: value` per line; omit keys you have not decided.

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

## Assets

Create only the kinds in scope: logo and banners for confirmed surfaces. Banners keep one master; per-surface crops derive from it as `<concept>-v<n>-<surface>.<ext>` in staged (e.g. `a-v1-linkedin.png`) or in drafts previews. Record purpose, format and pixel size (SVG: viewBox) next to each link. Verify saved files exist; a description is not an asset.
