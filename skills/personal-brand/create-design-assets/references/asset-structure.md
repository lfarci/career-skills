# Design records and assets

brand/discovery.md holds interview answers and concept choices; brand/identity.md holds visual rules and links to asset files; actual files live under assets/. Staged means approved for reuse, not published.

## File names

All paths relative to the workspace root:

| What | Path |
| --- | --- |
| Draft master | `assets/drafts/<kind>/<concept>-v<n>.<ext>`, e.g. `assets/drafts/logo/a-v2.svg` |
| Preview render | `assets/drafts/<kind>/previews/<concept>-v<n>-<size>.png`, e.g. `a-v2-32.png` |
| Approved copy | `assets/staged/<kind>/<concept>-v<n>[-<variant>].<ext>`, e.g. `logo/a-v2-mono.svg` |

`<kind>` is `logo`, `banner`, `avatar`, `icon` or `palette`; `<concept>` is the lowercase concept ID (a, b, c); the selection "A/v2" is file `a-v2`. Lowercase, hyphens, no spaces. Render helpers (HTML pages, scripts) go in a temporary folder outside the workspace.

## identity.md

As soon as drafts exist, create or update brand/identity.md with `Status: pending`, the selected concept, and links to each draft master. After the user approves an exact version, copy it to assets/staged/, link the staged file, record palette, fonts (with licence links) and usage rules, and set `Status: approved <version>`. Keep earlier versions; never overwrite an approved file.

## Assets

Create only the kinds in scope. Banners keep one generic master; platform crops derive from it. Record purpose, format and pixel size (SVG: viewBox) next to each link. Verify saved files exist; a description is not an asset.
