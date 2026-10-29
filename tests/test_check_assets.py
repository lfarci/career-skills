"""Tests for visual-identity/scripts/check_assets.py."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "personal-brand" / "visual-identity" / "scripts" / "check_assets.py"


def load():
    spec = importlib.util.spec_from_file_location("check_assets", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CheckAssetsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.ca = load()
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def touch(self, rel: str, text: str = "x") -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_valid_layout(self) -> None:
        self.touch("assets/drafts/logo/a-v1.svg")
        self.touch("assets/drafts/logo/previews/a-v1-32.png")
        self.touch("brand/identity.md", "Status: pending\n- [A/v1](../assets/drafts/logo/a-v1.svg)\n")
        self.assertEqual(self.ca.check(self.root), {"errors": [], "warnings": []})
        self.assertEqual(self.ca.main([str(self.root)]), 0)

    def test_bad_names_scratch_and_missing_identity(self) -> None:
        self.touch("assets/drafts/logo/option-a_pair_v1.svg")
        self.touch("assets/drafts/logo/previews/render-v1-16.html")
        errors = self.ca.check(self.root)["errors"]
        self.assertTrue(any("option-a_pair_v1.svg" in e for e in errors))
        self.assertTrue(any("scratch" in e for e in errors))

    def test_missing_identity(self) -> None:
        self.touch("assets/drafts/logo/a-v1.svg")
        self.assertTrue(any("identity.md" in e for e in self.ca.check(self.root)["errors"]))

    def test_unlinked_master_warns(self) -> None:
        self.touch("assets/drafts/logo/a-v1.svg")
        self.touch("brand/identity.md", "Status: pending\n")
        self.assertTrue(self.ca.check(self.root)["warnings"])

    def test_resume_outputs_are_not_design_assets(self) -> None:
        self.touch("assets/drafts/resumes/general/resume.pdf")
        self.touch("assets/drafts/resumes/general/resume.log")
        self.touch("assets/staged/resumes/general/resume.pdf")
        self.assertEqual(self.ca.check(self.root), {"errors": [], "warnings": []})
        self.touch("assets/drafts/logos/A v1.svg")
        self.assertTrue(self.ca.check(self.root)["errors"])

    def test_missing_root(self) -> None:
        self.assertEqual(self.ca.main([str(self.root / "nope")]), 2)


if __name__ == "__main__":
    unittest.main()
