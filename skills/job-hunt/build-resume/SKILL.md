---
name: build-resume
description: Build, tailor or review a truthful CV or resume using career evidence, job requirements and ATS-readable formatting.
---

# Build a Resume

Produce an evidence-based resume readable by humans and reliably extractable by modern applicant tracking systems. There is no universal ATS score or format guaranteed to pass every system.

## Contract
- **Input:** Supported profile/ facts, selected project evidence, brand/ guidance and an optional research/opportunities/ role.
- **Scope:** Author or tailor a truthful resume; do not alter career facts to match the vacancy or submit an application.
- **Output:** Resume sources/exports in assets/drafts/resumes/; explicitly approved versions in assets/staged/resumes/, with verification and intentional tailoring recorded.

## Steps

1. Read an existing resume, verified career profile or supplied experience. Accept a partial source: do not require a canonical repository. Identify target role, location, language, job description and desired length/format when available. If a configured career source path no longer resolves, use `validate-workspace` when installed for that specific mapping; otherwise continue from available evidence or propose a path correction.
2. Identify the strongest relevant evidence. Build a career narrative with correct role names, organizations, dates, responsibilities and contributions. Treat approximate achievements as approximate; ask or flag when important factual evidence is missing.
3. Write a concise summary and accomplishment-oriented experience bullets. Use language from a supplied job posting naturally only where supported by evidence. Differentiate individual contribution from team outcomes.
4. Structure the resume with conventional headings, single-column reading order, selectable text and usable links. Write `resume.json` in the output folder using only facts supported by the records from steps 1–3. Each field holds one kind of fact; dates go in `dates`, never inside `organization`:

   ```json
   {"name": "Full Name", "headline": "Target role", "contact": ["City, Country", {"text": "site.example", "url": "https://site.example"}],
    "sections": [{"title": "Summary", "text": "..."},
                 {"title": "Experience", "entries": [{"title": "Role", "organization": "Employer", "dates": "Mar 2021 – present", "location": "City", "bullets": ["..."]}]},
                 {"title": "Skills", "lines": [{"label": "Cloud", "items": ["Azure", "Terraform"]}]}]}
   ```

   Then run:

   ```
   python3 <skill-dir>/scripts/build_resume.py <out>/resume.json --out-dir <out> --json
   ```

   `<out>` is `assets/drafts/resumes/<name>/` inside the career workspace root (next to its `README.md`). Fix every entry in `warnings` that is a data mistake; ask the user for a missing name instead of using a placeholder. The script writes `resume.tex` (built from the blocks in `templates/career-resume.sty`), a Markdown copy, and compiles a PDF with the first engine found: `tectonic`, `latexmk`, `xelatex`, `lualatex` or `pdflatex`. If the user wants another layout, edit the generated `.tex` or the copied `.sty` and re-run the engine; keep the blocks.
5. Read the script's JSON status. Exit `0`: a PDF exists and was checked (`pages`, `text_extracted`); look at page 1 as an image when you can (for example `pdftoppm -png -r 80 -f 1 -l 1`). Exit `3`: no TeX engine, so only `.tex` and `.md` exist; say so, give the install hint, and do not claim a PDF. Exit `2`: show the error and fix the `.tex`. Exit `1`: fix `resume.json`. Then validate claim provenance, chronology, spelling, length, relevance, links and reading order, and name the checks you could not run.
6. Report meaningful changes and unresolved evidence gaps. Never silently modify the canonical professional profile as part of tailoring.

## Output

Resume source and requested exports when possible, plus a concise validation summary: relevance choices, verified key claims, format checks and any unresolved assumptions.

When the workspace has a root `README.md` index, add a link to each new record under `Records`.

## Done when

- No fabricated title, skill, certification, metric or business impact appears.
- Target keywords appear only where truthful, without keyword stuffing.
- Resume remains scannable for a human and reasonably parseable by text extraction.
- A PDF is reported only when `build_resume.py` exited `0`; otherwise the `.tex` and `.md` are delivered with the reason no PDF exists.
- Material career evidence is not silently dropped merely to hit a page count.
- Limitations are described instead of asserting an unsupported ATS success percentage.

