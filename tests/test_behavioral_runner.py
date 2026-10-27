"""Exercise evaluation plumbing with a fake agent; no LLM or network is used."""
from __future__ import annotations

import json
import shlex
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_behavioral_evals import review, run, scenarios  # noqa: E402


class SmokeRunnerTests(unittest.TestCase):
    def test_scenarios_contain_discovery_explicit_and_negative(self) -> None:
        items = scenarios()
        self.assertEqual(len(items), 11)
        self.assertTrue(any(x.get("skill") == "ask-career-skills" and x["mode"] == "explicit" for x in items))
        self.assertEqual({x["mode"] for x in items}, {"discovery", "explicit"})
        self.assertTrue(any(x.get("skill") is None for x in items))

    def test_real_command_execution_requires_human_scoring(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "smoke.json"
            python = shlex.quote(sys.executable)
            command = python + ' -c "import sys; sys.stdout.write(sys.stdin.read())"'
            result = run(command, path, {"profile-conflicting-credential"}, 10, "echo-mock")
            self.assertEqual(result, 0)
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["harness"], "echo-mock")
            self.assertEqual(len(data["results"]), 1)
            item = data["results"][0]
            self.assertEqual(item["response"], item["prompt"])
            self.assertEqual(review(path), 2)
            for finding in item["assessments"]:
                finding["status"] = "pass"
                finding["evidence"] = "Verified against mock response and saved trace."
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual(review(path), 0)
            item["assessments"][0]["status"] = "fail"
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual(review(path), 1)

    def test_unknown_selection_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "Unknown smoke IDs"):
                run("python3 -c pass", Path(folder) / "out.json", {"not-a-case"}, 5, "mock")


if __name__ == "__main__":
    unittest.main()
