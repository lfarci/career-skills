"""Harness selection and missing-binary path; no live agent is started."""
import io
import os
import shlex
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import harness as h  # noqa: E402
from run_behavioral_evals import harness_command  # noqa: E402


class HarnessTest(unittest.TestCase):
    def test_selection_maps_to_adapter_and_resume_flag(self) -> None:
        self.assertEqual(h.DEFAULT_HARNESS, "copilot")
        for name in h.HARNESSES:
            argv = shlex.split(harness_command(name, "m1"))
            self.assertEqual(Path(argv[1]).name, f"{name}_adapter.py")
            self.assertEqual(argv[-2:], ["--model", "m1"])
        self.assertIn("--continue", h.build_command(h.get("copilot"), "copilot", "x", resume=True))
        self.assertEqual(h.build_command(h.get("codex"), "codex", "x", resume=True)[-3:], ["resume", "--last", "x"])
        self.assertIn("-c", h.build_command(h.get("opencode"), "opencode", "x", resume=True))
        with self.assertRaises(ValueError):
            harness_command("claude")

    def test_missing_binary_exits_75_with_harness_error(self) -> None:
        with tempfile.TemporaryDirectory() as empty, \
                mock.patch.dict(os.environ, {"PATH": empty, "HOME": empty, "USERPROFILE": empty}):
            for name in h.HARNESSES:
                out = io.StringIO()
                with mock.patch("sys.stdin", io.StringIO("hi")), redirect_stdout(out):
                    self.assertEqual(h.adapter_main(name, []), 75)
                self.assertIn(f"HARNESS ERROR: {name} not installed/authenticated", out.getvalue())


if __name__ == "__main__":
    unittest.main()
