# Identity package structure

Ask where to store this package before writing it, unless a destination is already established. Adapt to the user's existing structure instead of forcing a new root. Use relative links within the package.

## Example
```text
visual-identity/
├── identity.md
├── discovery.md
├── assets/
│   ├── logos/
│   │   ├── symbol.svg
│   │   ├── wordmark.svg
│   │   └── lockup.svg
│   ├── icons/
│   │   ├── favicon.ico
│   │   └── avatar.png
│   └── banners/
│       ├── github.png
│       └── linkedin.png
└── explorations/
```

This is a conditional example, not a mandatory asset inventory. Omit unused directories. A wordmark-only identity needs no symbol; banners exist only when requested. Add social cards, presentation templates or other application assets only when needed. Keep any unapproved candidates under explorations/ or an existing equivalent, never among approved files.

## identity.md
Use as the canonical Markdown reference for:
- Status, version and scope; distinguish draft, selected and approved.
- Fonts: exact families, weights, hierarchy, usage, sources/licences and documented fallbacks.
- Colour palettes: values, roles, combinations and light/dark guidance.
- Logo rules: approved forms, clear space, tested size limits, backgrounds and misuse examples.
- Supporting system: layout, spacing, grids, shapes/patterns and imagery/icon guidance as applicable.
- An asset index with relative file links, intended use, variant, format and pixel dimensions where relevant. For SVG masters record viewBox/aspect ratio and sizing guidance instead of implying fixed output pixels.
- Representative applications, verification performed, outstanding limitations and a link to discovery.md.

## discovery.md
Preserve substantive interview questions and user answers, dates, clarifications, reference feedback and confirmed/unresolved decisions. Label paraphrases and designer interpretations. Mark superseded decisions without erasing the original answer. Link to any existing authoritative interview record instead of duplicating it unnecessarily.

## Actual reusable assets
Store editable vector logo masters and any required raster exports. Name variants explicitly, for example lockup-dark.svg or symbol-white.svg. Export icons and banners at the agreed platform sizes and record those dimensions. Supply editable application sources when available and useful.

Do not claim a font, logo, banner or export is included merely because it is described in identity.md. Verify actual files exist and render correctly where tools permit. Do not present the system as approved until the user approves the relevant version.
