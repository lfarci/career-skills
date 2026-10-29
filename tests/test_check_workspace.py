"""Tests for the check_workspace.py script shipped with setup and validate-workspace."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "setup-career-skills" / "scripts" / "check_workspace.py"
COPIES = [ROOT / "skills" / "validate-workspace" / "scripts" / "check_workspace.py"]


def load():
    spec = importlib.util.spec_from_file_location("check_workspace", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CheckWorkspaceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cw = load()
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "profile").mkdir()
        (self.root / "profile" / "experience.md").write_text("# Experience\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_index(self, body: str) -> None:
        (self.root / "README.md").write_text(body, encoding="utf-8")

    def test_valid_workspace(self) -> None:
        self.write_index("# W\n## Records\n- [E](profile/experience.md)\n## Setup progress\nStatus: in progress\n")
        report = self.cw.check(self.root)
        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, [])
        self.assertEqual(self.cw.main([str(self.root)]), 0)

    def test_missing_index(self) -> None:
        self.assertIn("README.md: missing workspace index", self.cw.check(self.root).errors)
        self.assertEqual(self.cw.main([str(self.root), "--json"]), 1)

    def test_broken_link_and_unlinked_record(self) -> None:
        self.write_index("## Records\n- [P](projects/x.md)\n- [Site](https://example.invalid)\n")
        report = self.cw.check(self.root)
        self.assertTrue(any("broken link -> projects/x.md" in e for e in report.errors))
        self.assertTrue(any("profile/experience.md: record not linked" in w for w in report.warnings))

    def test_facts_in_index_needs_repair(self) -> None:
        self.write_index("# W\n## Captured facts\n### Education\n- MSc 2020\n## Next decision\nWhat next?\n")
        report = self.cw.check(self.root)
        self.assertTrue(any("Captured facts" in e for e in report.errors))
        self.assertEqual(report.status, "needs repair")

    def test_empty_record_is_error(self) -> None:
        (self.root / "profile" / "skills.md").write_text("", encoding="utf-8")
        self.write_index("## Records\n- [E](profile/experience.md)\n- [S](profile/skills.md)\n")
        self.assertTrue(any("profile/skills.md: empty record" in e for e in self.cw.check(self.root).errors))

    def test_invalid_status(self) -> None:
        self.write_index("## Records\n- [E](profile/experience.md)\n## Setup progress\nStatus: done\n")
        self.assertTrue(self.cw.check(self.root).errors)

    def test_unusable_root(self) -> None:
        self.assertEqual(self.cw.main([str(self.root / "nope")]), 2)

    def test_copies_identical(self) -> None:
        for copy in COPIES:
            self.assertEqual(copy.read_bytes(), SCRIPT.read_bytes(), copy)


if __name__ == "__main__":
    unittest.main()
