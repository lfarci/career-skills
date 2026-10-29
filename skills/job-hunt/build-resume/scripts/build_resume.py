#!/usr/bin/env python3
"""Render a resume.json into LaTeX (+ Markdown) and compile it to PDF when a TeX engine exists.

Standard library only; works on Windows, macOS and Linux.

Usage:
    python3 build_resume.py resume.json --out-dir assets/drafts/resumes/<name> [--engine auto] [--json]

resume.json (every value is plain text; the script escapes LaTeX):
    {"name": "...", "headline": "...",
     "contact": ["City, Country", {"text": "site.example", "url": "https://site.example"}],
     "sections": [
       {"title": "Summary", "text": "..."},
       {"title": "Experience", "entries": [{"title": "...", "organization": "...", "dates": "...",
                                            "location": "...", "bullets": ["..."]}]},
       {"title": "Skills", "lines": [{"label": "Cloud", "items": ["Azure", "Terraform"]}]}]}

Exit codes: 0 PDF built and verified; 1 invalid input; 2 compilation or PDF check failed;
3 no TeX engine found (only .tex and .md written; no PDF exists).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
STYLE = SKILL_DIR / "templates" / "career-resume.sty"
ENGINES = ("tectonic", "latexmk", "xelatex", "lualatex", "pdflatex")
LATEX_SPECIALS = {
    "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
    "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}


@dataclass
class Status:
    """Build result reported to the agent."""

    tex: str = ""
    markdown: str = ""
    pdf: str | None = None
    engine: str | None = None
    pages: int | None = None
    text_extracted: bool | None = None
    warnings: list[str] = field(default_factory=list)
    error: str | None = None


def escape(text: Any) -> str:
    """Escape plain text for LaTeX."""
    return "".join(LATEX_SPECIALS.get(ch, ch) for ch in str(text))


def contact_item(item: Any, latex: bool) -> str:
    """Render one contact entry (string or {text, url})."""
    if isinstance(item, dict):
        text, url = str(item.get("text", "")), str(item.get("url", ""))
        if latex:
            return rf"\href{{{url.replace('%', r'\%').replace('#', r'\#')}}}{{{escape(text)}}}" if url else escape(text)
        return f"[{text}]({url})" if url else text
    return escape(item) if latex else str(item)


def validate(data: Any) -> list[str]:
    """Return problems with the resume structure (empty list when valid)."""
    problems = []
    if not isinstance(data, dict):
        return ["top level must be an object"]
    if not str(data.get("name", "")).strip():
        problems.append("name is required")
    for i, section in enumerate(data.get("sections", [])):
        if not isinstance(section, dict) or not section.get("title"):
            problems.append(f"sections[{i}] needs a title")
        elif not any(k in section for k in ("text", "entries", "lines")):
            problems.append(f"sections[{i}] needs text, entries or lines")
    return problems


def lint(data: dict) -> list[str]:
    """Return warnings about likely data mistakes that still render."""
    warnings = []
    if any(mark in str(data.get("name", "")) for mark in "[]<>"):
        warnings.append("name looks like a placeholder: ask the user before sharing")
    for section in data.get("sections", []):
        for entry in section.get("entries", []):
            if not str(entry.get("dates", "")).strip():
                warnings.append(f"{section['title']}: '{entry.get('title', '')}' has no dates field "
                                "(put dates in 'dates', not in 'organization')")
    return warnings


def items_text(items: Any) -> str:
    return ", ".join(map(str, items)) if isinstance(items, list) else str(items)


def render_latex(data: dict) -> str:
    """Build the .tex document from resume data using career-resume.sty blocks."""
    contact = r" \textperiodcentered\ ".join(contact_item(c, True) for c in data.get("contact", []))
    out = [r"\documentclass[10pt,a4paper]{article}", r"\usepackage{career-resume}", r"\begin{document}",
           rf"\resumeHeader{{{escape(data['name'])}}}{{{escape(data.get('headline', ''))}}}{{{contact}}}"]
    for section in data.get("sections", []):
        out.append(rf"\resumeSection{{{escape(section['title'])}}}")
        if "text" in section:
            out.append(rf"\resumeText{{{escape(section['text'])}}}")
        for entry in section.get("entries", []):
            out.append(r"\resumeEntry{%s}{%s}{%s}{%s}" % tuple(
                escape(entry.get(k, "")) for k in ("title", "organization", "dates", "location")))
            bullets = entry.get("bullets", [])
            if bullets:
                out.append(r"\begin{resumeItems}")
                out += [rf"  \item {escape(b)}" for b in bullets]
                out.append(r"\end{resumeItems}")
        for line in section.get("lines", []):
            out.append(rf"\resumeSkillLine{{{escape(line.get('label', ''))}}}{{{escape(items_text(line.get('items', '')))}}}")
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


def render_markdown(data: dict) -> str:
    """Build the Markdown fallback from the same data."""
    out = [f"# {data['name']}", ""]
    if data.get("headline"):
        out += [f"**{data['headline']}**", ""]
    if data.get("contact"):
        out += [" · ".join(contact_item(c, False) for c in data["contact"]), ""]
    for section in data.get("sections", []):
        out += [f"## {section['title']}", ""]
        if "text" in section:
            out += [str(section["text"]), ""]
        for entry in section.get("entries", []):
            org = f", {entry['organization']}" if entry.get("organization") else ""
            dates = f" ({entry['dates']})" if entry.get("dates") else ""
            out += [f"### {entry.get('title', '')}{org}{dates}"]
            if entry.get("location"):
                out.append(str(entry["location"]))
            out += [f"- {b}" for b in entry.get("bullets", [])] + [""]
        for line in section.get("lines", []):
            out.append(f"- **{line.get('label', '')}:** {items_text(line.get('items', ''))}")
        if section.get("lines"):
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def find_engine(choice: str) -> str | None:
    """Return the first available TeX engine (or the requested one when present)."""
    names = ENGINES if choice == "auto" else (choice,)
    for name in names:
        if name != "none" and shutil.which(name):
            return name
    return None


def compile_tex(engine: str, tex: Path) -> subprocess.CompletedProcess:
    """Run the engine in the output directory."""
    commands = {
        "tectonic": [engine, "--keep-logs", tex.name],
        "latexmk": [engine, "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex.name],
    }
    command = commands.get(engine, [engine, "-interaction=nonstopmode", "-halt-on-error", tex.name])
    return subprocess.run(command, cwd=tex.parent, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=300, check=False)


def inspect_pdf(pdf: Path, name: str, status: Status) -> bool:
    """Check the PDF header, page count and extractable text when tools exist."""
    if not pdf.is_file() or not pdf.read_bytes()[:5] == b"%PDF-":
        status.error = "PDF missing or not a PDF file"
        return False
    if shutil.which("pdfinfo"):
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=False)
        for line in info.stdout.splitlines():
            if line.startswith("Pages:"):
                status.pages = int(line.split()[1])
    else:
        status.warnings.append("pdfinfo not found: page count unchecked")
    if shutil.which("pdftotext"):
        text = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=False).stdout
        status.text_extracted = name.split()[0].lower() in text.lower()
        if not status.text_extracted:
            status.warnings.append("name not found in extracted text: check ATS readability")
    else:
        status.warnings.append("pdftotext not found: text extraction unchecked")
    return True


def build(source: Path, out_dir: Path, engine_choice: str) -> tuple[int, Status]:
    """Render, compile and verify; return (exit code, status)."""
    status = Status()
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        status.error = f"cannot read {source}: {exc}"
        return 1, status
    problems = validate(data)
    if problems:
        status.error = "; ".join(problems)
        return 1, status
    status.warnings += lint(data)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = source.stem
    tex, md = out_dir / f"{stem}.tex", out_dir / f"{stem}.md"
    tex.write_text(render_latex(data), encoding="utf-8")
    md.write_text(render_markdown(data), encoding="utf-8")
    shutil.copyfile(STYLE, out_dir / STYLE.name)
    status.tex, status.markdown = tex.as_posix(), md.as_posix()
    engine = find_engine(engine_choice)
    if engine is None:
        status.warnings.append("no TeX engine found: install Tectonic (https://tectonic-typesetting.github.io) "
                               "or TeX Live/MiKTeX, then re-run; no PDF was produced")
        return 3, status
    status.engine = engine
    result = compile_tex(engine, tex)
    pdf = out_dir / f"{stem}.pdf"
    if result.returncode != 0:
        status.error = f"{engine} failed: " + (result.stdout + result.stderr)[-800:]
        return 2, status
    if not inspect_pdf(pdf, str(data["name"]), status):
        return 2, status
    status.pdf = pdf.as_posix()
    if status.pages and status.pages > 2:
        status.warnings.append(f"{status.pages} pages: consider trimming")
    return 0, status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", type=Path, help="resume.json written from career records")
    parser.add_argument("--out-dir", type=Path, required=True, help="output folder, e.g. assets/drafts/resumes/<name>")
    parser.add_argument("--engine", default="auto", choices=("auto", "none", *ENGINES))
    parser.add_argument("--json", action="store_true", help="print a JSON status")
    args = parser.parse_args(argv)
    code, status = build(args.source, args.out_dir, args.engine)
    if args.json:
        print(json.dumps({"exit_code": code, **asdict(status)}, indent=2))
    else:
        for key, value in asdict(status).items():
            if value not in (None, "", []):
                print(f"{key}: {value}")
    return code


if __name__ == "__main__":
    sys.exit(main())
