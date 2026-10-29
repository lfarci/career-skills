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
4. Structure the resume with conventional headings, single-column reading order where appropriate, selectable text and usable links. Prefer an editable source (Markdown or equivalent); generate PDF/DOCX/HTML only when requested and tools exist.
5. Validate claim provenance, chronology, spelling, length, relevance, links and reading order. When generating a PDF or document, inspect layout and extracted text using available tools. Explain tests not performed if tools are absent.
6. Report meaningful changes and unresolved evidence gaps. Never silently modify the canonical professional profile as part of tailoring.

## Output

Resume source and requested exports when possible, plus a concise validation summary: relevance choices, verified key claims, format checks and any unresolved assumptions.

When the workspace has a root `README.md` index, add a link to each new record under `Records`.

## Done when

- No fabricated title, skill, certification, metric or business impact appears.
- Target keywords appear only where truthful, without keyword stuffing.
- Resume remains scannable for a human and reasonably parseable by text extraction.
- Requested file formats actually exist and have been inspected where tools permit.
- Material career evidence is not silently dropped merely to hit a page count.
- Limitations are described instead of asserting an unsupported ATS success percentage.

