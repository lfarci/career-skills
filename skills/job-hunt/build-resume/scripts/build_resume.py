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

Brand: --brand <workspace>/brand/identity.md reads its ```brand-tokens block (see
references/brand-tokens.md). Approved tokens set colours and fonts; pending or missing tokens
keep the neutral default and add a warning.

Exit codes: 0 PDF built and verified; 1 invalid input; 2 compilation or PDF check failed;
3 no TeX engine found (only .tex and .md written; no PDF exists).
"""
from __future__ import annotations

import argparse
import json
import re
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
    brand: str = "default"
    warnings: list[str] = field(default_factory=list)
    error: str | None = None


HEX = re.compile(r"^#?([0-9A-Fa-f]{6})$")
COLOR_KEYS = {"primary": 3.0, "accent": 3.0, "text": 4.5, "muted": 4.5}  # min contrast on white
FONT_KEYS = ("heading-font", "body-font")
BLOCK = re.compile(r"^```brand-tokens[ \t]*\n(.*?)^```", re.DOTALL | re.MULTILINE)


def contrast_on_white(hex6: str) -> float:
    """WCAG contrast ratio of a colour against white."""
    def channel(value: int) -> float:
        c = value / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex6[i:i + 2], 16) for i in (0, 2, 4))
    luminance = 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)
    return 1.05 / (luminance + 0.05)


def parse_brand_tokens(text: str) -> tuple[dict[str, str], list[str]]:
    """Parse the brand-tokens block; return (valid tokens, warnings). Invalid values are dropped."""
    match = BLOCK.search(text)
    if not match:
        return {}, ["no brand-tokens block found"]
    raw: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip():
            raw[key.strip().lower()] = re.sub(r"\s+#\s.*$", "", value).strip()  # drop "  # comment"
    tokens, warnings = {}, []
    status = raw.get("status", "").split()[0].lower() if raw.get("status") else ""
    if status not in ("approved", "pending"):
        warnings.append(f"status must be approved or pending, got '{raw.get('status', '')}'")
    tokens["status"] = status or "unknown"
    for key, minimum in COLOR_KEYS.items():
        if key not in raw:
            continue
        found = HEX.match(raw[key])
        if not found:
            warnings.append(f"{key}: '{raw[key]}' is not a #RRGGBB hex colour; using the default")
            continue
        hex6 = found.group(1).upper()
        ratio = contrast_on_white(hex6)
        if ratio < minimum:
            warnings.append(f"{key}: #{hex6} has contrast {ratio:.1f}:1 on white (< {minimum}:1); using the default")
            continue
        tokens[key] = hex6
    for key in FONT_KEYS:
        if raw.get(key):
            tokens[key] = raw[key]
    return tokens, warnings


def font_available(name: str) -> bool | str | None:
    """True if fc-list finds a static font file for the family, "variable" if only variable
    font files exist (XeTeX cannot load them), False if absent, None if fc-list is missing."""
    if not shutil.which("fc-list"):
        return None
    out = subprocess.run(["fc-list", ":", "family", "file"], capture_output=True, text=True, check=False).stdout
    files = []
    for line in out.splitlines():
        path, _, families = line.partition(": ")
        if name.lower() in {f.strip().lower() for f in families.split(",")}:
            files.append(path)
    if not files:
        return False
    return True if any("variable" not in Path(f).name.lower() for f in files) else "variable"


def brand_preamble(tokens: dict[str, str], engine: str | None, status: Status) -> str:
    """LaTeX lines that apply approved tokens (colours always; fonts only with fontspec engines)."""
    lines = []
    names = {"text": "ResumeInk", "primary": "ResumeAccent", "muted": "ResumeMuted"}
    for key, colour in names.items():
        if key in tokens:
            lines.append(rf"\definecolor{{{colour}}}{{HTML}}{{{tokens[key]}}}")
    if "primary" in tokens:
        lines.append(r"\colorlet{ResumeSoft}{ResumeAccent!10!white}")
        lines.append(r"\colorlet{ResumeHighlight}{ResumeAccent}")
    if "accent" in tokens:
        lines.append(rf"\definecolor{{ResumeHighlight}}{{HTML}}{{{tokens['accent']}}}")
    fonts = [k for k in FONT_KEYS if k in tokens]
    if fonts and engine not in ("tectonic", "xelatex", "lualatex"):
        status.warnings.append("brand fonts need Tectonic, XeLaTeX or LuaLaTeX; using the default font")
        return "\n".join(lines)
    for key in fonts:
        name = tokens[key]
        available = font_available(name)
        if available is False:
            status.warnings.append(f"{key} '{name}' is not installed; using the default font")
            continue
        if available == "variable":
            status.warnings.append(f"{key} '{name}' is installed only as a variable font, which the TeX engine "
                                   "cannot load; install its static files. Using the default font")
            continue
        if available is None:
            status.warnings.append(f"{key} '{name}' could not be checked (no fc-list); retrying without it if the build fails")
        safe = name.replace("\\", "").replace("{", "").replace("}", "")
        if key == "body-font":
            lines.append(rf"\setmainfont{{{safe}}}")
        else:
            lines.append(rf"\newfontfamily\resumeBrandHeading{{{safe}}}")
            lines.append(r"\renewcommand{\resumeHeadingFont}{\resumeBrandHeading}")
    return "\n".join(lines)


def load_brand(path: Path | None, allow_pending: bool, status: Status) -> dict[str, str]:
    """Read approved tokens, or return {} with a warning explaining the neutral default."""
    if path is None:
        status.warnings.append("no --brand given: neutral default colours and fonts")
        return {}
    try:
        tokens, warnings = parse_brand_tokens(path.read_text(encoding="utf-8"))
    except OSError as exc:
        status.warnings.append(f"cannot read brand file {path}: {exc}; neutral default used")
        return {}
    status.warnings += warnings
    if tokens.get("status") == "approved" or (allow_pending and tokens.get("status") == "pending"):
        status.brand = tokens["status"]
        return tokens
    if tokens.get("status") == "pending":
        status.warnings.append("brand tokens are pending approval: neutral default used; ask the user "
                               "to approve them or re-run with --allow-pending")
    elif tokens:
        status.warnings.append("brand tokens are not approved: neutral default used")
    return {}


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


def is_empty(section: dict) -> bool:
    """True when a section has no text, entries or lines to show."""
    return not (str(section.get("text", "")).strip() or section.get("entries") or section.get("lines"))


def lint(data: dict) -> list[str]:
    """Return warnings about likely data mistakes that still render."""
    warnings = [f"section '{s['title']}' is empty and was left out: fill it from the records or drop it"
                for s in data.get("sections", []) if is_empty(s)]
    if any(mark in str(data.get("name", "")) for mark in "[]<>"):
        warnings.append("name looks like a placeholder: ask the user before sharing")
    for section in data.get("sections", []):
        for entry in section.get("entries", []):
            label = f"{section['title']}: '{entry.get('title', '')}'"
            if re.search(r"\b(19|20)\d\d\b", str(entry.get("organization", ""))):
                warnings.append(f"{label} has a year in 'organization'; put dates in 'dates'")
            elif "experience" in section["title"].lower() and not str(entry.get("dates", "")).strip():
                warnings.append(f"{label} has no dates")
    return warnings


def items_text(items: Any) -> str:
    return ", ".join(map(str, items)) if isinstance(items, list) else str(items)


def render_latex(data: dict, preamble: str = "") -> str:
    """Build the .tex document from resume data using career-resume.sty blocks."""
    contact = r" \textperiodcentered\ ".join(contact_item(c, True) for c in data.get("contact", []))
    out = [r"\documentclass[10pt,a4paper]{article}", r"\usepackage{career-resume}", *([preamble] if preamble else []), r"\begin{document}",
           rf"\resumeHeader{{{escape(data['name'])}}}{{{escape(data.get('headline', ''))}}}{{{contact}}}"]
    for section in (s for s in data.get("sections", []) if not is_empty(s)):
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
    for section in (s for s in data.get("sections", []) if not is_empty(s)):
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
        "tectonic": [engine, tex.name],
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


def retry_without_fonts(data: dict, preamble: str, engine: str, tex: Path,
                        status: Status) -> subprocess.CompletedProcess:
    """Rebuild dropping one brand font at a time, then all, and say which font was dropped."""
    lines = preamble.splitlines()
    body = [l for l in lines if "setmainfont" in l]
    heading = [l for l in lines if "resumeBrandHeading" in l]
    result = None
    for dropped, label in ((heading, "heading-font"), (body, "body-font"), (body + heading, "both brand fonts")):
        if not dropped:
            continue
        kept = "\n".join(l for l in lines if l not in dropped)
        tex.write_text(render_latex(data, kept), encoding="utf-8")
        result = compile_tex(engine, tex)
        if result.returncode == 0:
            status.warnings.append(f"the TeX engine could not load {label} (variable fonts often fail; "
                                   "install a static version): built with the default font instead")
            return result
    return result


def build(source: Path, out_dir: Path, engine_choice: str, brand: Path | None = None,
          allow_pending: bool = False) -> tuple[int, Status]:
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
    engine = find_engine(engine_choice)
    tokens = load_brand(brand, allow_pending, status)
    preamble = brand_preamble(tokens, engine, status)
    tex.write_text(render_latex(data, preamble), encoding="utf-8")
    md.write_text(render_markdown(data), encoding="utf-8")
    shutil.copyfile(STYLE, out_dir / STYLE.name)
    status.tex, status.markdown = tex.as_posix(), md.as_posix()
    if engine is None:
        status.warnings.append("no TeX engine found: install Tectonic (https://tectonic-typesetting.github.io) "
                               "or TeX Live/MiKTeX, then re-run; no PDF was produced")
        return 3, status
    status.engine = engine
    result = compile_tex(engine, tex)
    pdf = out_dir / f"{stem}.pdf"
    if result.returncode != 0 and "font" in preamble.lower():
        result = retry_without_fonts(data, preamble, engine, tex, status)
    if result.returncode != 0:
        status.error = f"{engine} failed: " + (result.stdout + result.stderr)[-800:]
        return 2, status
    if not inspect_pdf(pdf, str(data["name"]), status):
        return 2, status
    status.pdf = pdf.as_posix()
    for suffix in (".log", ".aux", ".out", ".fls", ".fdb_latexmk", ".xdv"):
        (out_dir / f"{stem}{suffix}").unlink(missing_ok=True)  # keep only reviewable sources and the PDF
    if status.pages and status.pages > 2:
        status.warnings.append(f"{status.pages} pages: consider trimming")
    return 0, status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", type=Path, help="resume.json written from career records")
    parser.add_argument("--out-dir", type=Path, required=True, help="output folder, e.g. assets/drafts/resumes/<name>")
    parser.add_argument("--engine", default="auto", choices=("auto", "none", *ENGINES))
    parser.add_argument("--brand", type=Path, help="brand/identity.md with a brand-tokens block")
    parser.add_argument("--allow-pending", action="store_true", help="use pending tokens (user said so)")
    parser.add_argument("--json", action="store_true", help="print a JSON status")
    args = parser.parse_args(argv)
    code, status = build(args.source, args.out_dir, args.engine, args.brand, args.allow_pending)
    if args.json:
        print(json.dumps({"exit_code": code, **asdict(status)}, indent=2))
    else:
        for key, value in asdict(status).items():
            if value not in (None, "", []):
                print(f"{key}: {value}")
    return code


if __name__ == "__main__":
    sys.exit(main())
