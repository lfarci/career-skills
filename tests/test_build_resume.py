"""Tests for build-resume's build_resume.py (no TeX engine required)."""
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "skills/job-hunt/build-resume/scripts/build_resume.py"
spec = importlib.util.spec_from_file_location("build_resume", SCRIPT)
br = importlib.util.module_from_spec(spec)
sys.modules["build_resume"] = br
spec.loader.exec_module(br)

SAMPLE = {"name": "Sam Example", "headline": "Engineer & Mentor",
          "contact": ["Ghent", {"text": "site.example", "url": "https://site.example/a#b"}],
          "sections": [{"title": "Summary", "text": "100% remote_ready, C# & $ tips"},
                       {"title": "Experience", "entries": [{"title": "Dev", "organization": "Contoso",
                                                            "dates": "2020 – 2024", "bullets": ["Did {x}"]}]},
                       {"title": "Skills", "lines": [{"label": "Tools", "items": ["Git", "Azure"]}]}]}


class BuildResumeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.src = self.tmp / "resume.json"
        self.src.write_text(json.dumps(SAMPLE), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_escape(self):
        self.assertEqual(br.escape("A&B 50% #1 a_b"), r"A\&B 50\% \#1 a\_b")

    def test_latex_uses_blocks_and_escapes(self):
        tex = br.render_latex(SAMPLE)
        for block in (r"\usepackage{career-resume}", r"\resumeHeader{Sam Example}", r"\resumeSection{Experience}",
                      r"\resumeEntry{Dev}{Contoso}{2020 – 2024}{}", r"\begin{resumeItems}", r"\resumeSkillLine{Tools}{Git, Azure}"):
            self.assertIn(block, tex)
        self.assertIn(r"100\% remote\_ready, C\# \& \$ tips", tex)
        self.assertIn(r"\href{https://site.example/a\#b}", tex)

    def test_no_engine_leaves_tex_and_md_exit_3(self):
        code, status = br.build(self.src, self.tmp / "out", "none")
        self.assertEqual(code, 3)
        self.assertIsNone(status.pdf)
        self.assertTrue((self.tmp / "out/resume.tex").is_file())
        self.assertTrue((self.tmp / "out/career-resume.sty").is_file())
        self.assertIn("## Experience", (self.tmp / "out/resume.md").read_text(encoding="utf-8"))

    def test_lint_flags_missing_dates_and_placeholder(self):
        data = {"name": "[Your Name]", "sections": [{"title": "Experience", "entries": [
            {"title": "Dev", "organization": "Contoso, 2020 - 2024"}]}]}
        warnings = br.lint(data)
        self.assertEqual(len(warnings), 2)

    def test_parse_brand_tokens(self):
        text = "# Identity\n\n```brand-tokens\nstatus: approved  # ok\nprimary: #0f766e  # bars\naccent: B45309\n" \
               "text: #1F2937\nmuted: #DDDDDD\nheading-font: Manrope\n```\n"
        tokens, warnings = br.parse_brand_tokens(text)
        self.assertEqual(tokens["status"], "approved")
        self.assertEqual(tokens["primary"], "0F766E")
        self.assertEqual(tokens["accent"], "B45309")
        self.assertNotIn("muted", tokens)  # low contrast dropped
        self.assertTrue(any("muted" in w and "contrast" in w for w in warnings))
        self.assertEqual(tokens["heading-font"], "Manrope")

    def test_parse_rejects_bad_hex_and_missing_block(self):
        tokens, warnings = br.parse_brand_tokens("```brand-tokens\nstatus: approved\nprimary: teal\n```\n")
        self.assertNotIn("primary", tokens)
        self.assertTrue(any("hex" in w for w in warnings))
        self.assertEqual(br.parse_brand_tokens("no block")[0], {})

    def test_pending_tokens_not_applied(self):
        identity = self.tmp / "identity.md"
        identity.write_text("```brand-tokens\nstatus: pending\nprimary: #0F766E\n```\n", encoding="utf-8")
        status = br.Status()
        self.assertEqual(br.load_brand(identity, False, status), {})
        self.assertTrue(any("pending" in w for w in status.warnings))
        self.assertEqual(br.load_brand(identity, True, br.Status())["primary"], "0F766E")

    def test_preamble_colours_and_font_fallback(self):
        status = br.Status()
        tokens = {"status": "approved", "primary": "0F766E", "body-font": "Surely Not Installed"}
        with mock.patch.object(br, "font_available", return_value=False):
            pre = br.brand_preamble(tokens, "tectonic", status)
        self.assertIn(r"\definecolor{ResumeAccent}{HTML}{0F766E}", pre)
        self.assertNotIn("setmainfont", pre)
        self.assertTrue(any("not installed" in w for w in status.warnings))
        status = br.Status()
        with mock.patch.object(br, "font_available", return_value="variable"):
            self.assertNotIn("setmainfont", br.brand_preamble(tokens, "tectonic", status))
        self.assertTrue(any("variable font" in w for w in status.warnings))
        status = br.Status()
        self.assertNotIn("setmainfont", br.brand_preamble(tokens, "pdflatex", status))
        with mock.patch.object(br, "font_available", return_value=True):
            self.assertIn(r"\setmainfont{Surely Not Installed}", br.brand_preamble(tokens, "xelatex", br.Status()))

    def test_no_brand_says_default(self):
        code, status = br.build(self.src, self.tmp / "out", "none")
        self.assertEqual(status.brand, "default")
        self.assertTrue(any("neutral default" in w for w in status.warnings))

    def test_empty_section_skipped_and_flagged(self):
        data = {"name": "Sam", "sections": [{"title": "Education", "entries": []}]}
        self.assertNotIn("Education", br.render_latex(data))
        self.assertNotIn("Education", br.render_markdown(data))
        self.assertTrue(any("Education" in w for w in br.lint(data)))

    def test_invalid_input_exit_1(self):
        self.src.write_text(json.dumps({"sections": [{"title": "X"}]}), encoding="utf-8")
        code, status = br.build(self.src, self.tmp / "out", "none")
        self.assertEqual(code, 1)
        self.assertIn("name is required", status.error)

    def test_fake_pdf_is_rejected(self):
        def fake_compile(engine, tex):
            (tex.parent / "resume.pdf").write_text("not a pdf", encoding="utf-8")
            return mock.Mock(returncode=0, stdout="", stderr="")
        with mock.patch.object(br, "find_engine", return_value="pdflatex"), \
             mock.patch.object(br, "compile_tex", side_effect=fake_compile):
            code, status = br.build(self.src, self.tmp / "out", "auto")
        self.assertEqual(code, 2)
        self.assertIsNone(status.pdf)

    def test_engine_failure_exit_2(self):
        with mock.patch.object(br, "find_engine", return_value="pdflatex"), \
             mock.patch.object(br, "compile_tex", return_value=mock.Mock(returncode=1, stdout="! Undefined", stderr="")):
            code, status = br.build(self.src, self.tmp / "out", "auto")
        self.assertEqual(code, 2)
        self.assertIn("Undefined", status.error)


if __name__ == "__main__":
    unittest.main()
