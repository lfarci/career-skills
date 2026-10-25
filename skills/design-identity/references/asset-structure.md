# Identity package

Use the user's chosen destination and existing conventions. Create only needed files; link canonical records rather than duplicate them.

```text
visual-identity/
├── discovery.md
├── options/
│   ├── A/
│   │   ├── v1/              # identity.md + assets + comparison preview
│   │   └── v2/
│   ├── B/v1/
│   └── C/v1/
├── identity.md             # current selection/approval and final guide
└── assets/                 # approved deliverables only
    ├── logos/              # editable SVG masters + required exports
    ├── icons/              # favicon/avatar if needed
    └── banners/            # generic editable master + requested sizes
```

## Records
- discovery.md: substantive questions/answers, dates, reference feedback and decisions. Label paraphrases and superseded decisions.
- Each option/revision: a concise identity.md describing its visual idea, font/palette proposals, preview/source links, status and feedback. Use the same comparison format. Keep early options lightweight; no full export kit.
- Root identity.md: selected option/revision, approval status, fonts/weights/hierarchy/licences, palette values/roles, logo spacing/minimum sizes/background rules, supporting layout/graphics rules, representative applications and actual asset links. Record verification and unfinished work.

## Version handling
Preserve existing versions; create a new revision for meaningful changes. Record selections by exact ID, for example B/v2. Copy/export to root assets only after approval, with provenance back to that version. If final files are not approved yet, leave them under their option and mark root identity.md as pending. Before replacing an approved version, retain it in the existing version history or archive it and update the guide explicitly.

## Assets
Omit unused directories: no symbol for a wordmark-only identity, no banners unless needed. Keep banners platform agnostic; optional size/crop exports derive from the generic master. Record relative paths, purpose, variant, format and pixel dimensions (SVG viewBox/aspect ratio for vector masters). Include editable sources where useful; document font fallbacks and source/licence links. Verify saved files exist; descriptions are not substitutes for assets.
