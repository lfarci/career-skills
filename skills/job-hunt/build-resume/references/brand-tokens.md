# Brand tokens

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
