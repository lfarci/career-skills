# SVG logo construction and verification

Use an available vector editor or write ordinary SVG directly. Do not introduce a custom geometry format or assume a particular installed tool. Reuse approved source files without redrawing them.

## Construct
- Use a valid SVG namespace and viewBox, simple paths/primitives and consistent geometry. Prefer few deliberate anchors; judge optical balance rather than grid alignment alone.
- Keep logo masters static and self-contained: no scripts, event handlers, external references or embedded raster substitutes. Avoid unnecessary effects.
- Keep editable type sources; for portable final wordmarks, export outlined letters with verified fonts/licences when tools permit. Label live-text/font dependencies.
- Save new option/revision files; never overwrite a competing concept.

## Inspect
- Parse for XML well-formedness with an available tool, then render. XML validity alone proves neither correct geometry nor safety.
- Inspect at presentation size and actual 16/32 px when a favicon is required. Check clipping, joins, negative space, spacing and unintended readings.
- Check required monochrome, reversed and light/dark variants. Verify name readability and requested applications; check text/background palette contrast.
- Render with an available vector editor, browser or established renderer. If CairoSVG is available, for example:
  `cairosvg logo.svg --output-width 512 -o preview.png`
  Do not force both dimensions and distort non-square lockups. Never use the unsafe option.
- Treat imported SVG as untrusted; inspect active/external content before rendering. This guide is not a sanitizer.
- Record actual checks and missing tool/manual steps. If unable to render, keep work unverified; do not declare final assets.

Before adoption, perform bounded similarity research; explain limits without guaranteeing uniqueness or legal clearance. A logo must be judged visually, not certified by code checks.

Technical references: [SVG](https://developer.mozilla.org/en-US/docs/Web/SVG), [CairoSVG](https://cairosvg.org/documentation/).

