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
