"""Exercise evaluation plumbing with a fake agent; no LLM or network is used."""
from __future__ import annotations

import json
import os
import time
import shlex
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_behavioral_evals import review, run, run_with_timeout, scenarios  # noqa: E402


class TimeoutTests(unittest.TestCase):
    def test_timeout_kills_grandchild(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "alive"
            child = ("import subprocess,sys,time;"
                     "subprocess.Popen([sys.executable,'-c',"
                     f"'import time,pathlib;time.sleep(3);pathlib.Path(r\"{marker}\").write_text(\"x\")']);"
                     "time.sleep(30)")
            _, err, code = run_with_timeout([sys.executable, "-c", child], "", 1, cwd=tmp, env=dict(os.environ))
            self.assertEqual(code, 124)
            self.assertIn("process tree killed", err)
            time.sleep(3.5)
            self.assertFalse(marker.exists(), "grandchild survived the timeout")


class FixtureTests(unittest.TestCase):
    def test_case_fixture_is_copied_into_scratch_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "r.json"
            lister = shlex.join([sys.executable, "-c", "import os;print(sorted(os.listdir('career/profile')))"])
            run(lister, out, {"repair-renamed-record-same-fix"}, 30, "test")
            response = json.loads(out.read_text(encoding="utf-8"))["results"][0]["response"]
            self.assertIn("technical-skills.md", response)

    def test_every_fixture_belongs_to_a_smoke_case(self) -> None:
        ids = {case["id"] for case in scenarios()}
        fixtures = Path(__file__).resolve().parent / "fixtures"
        self.assertTrue({p.name for p in fixtures.iterdir()} <= ids)


class SmokeRunnerTests(unittest.TestCase):
    def test_scenarios_contain_discovery_explicit_and_negative(self) -> None:
        items = scenarios()
        ids = {x["id"] for x in items}
        self.assertEqual(len(ids), len(items))
        for core in ("setup-index-holds-no-facts", "setup-resume-facts-in-index-asks-first", "setup-pdf-linkedin-conflicts", "repair-renamed-record-same-fix", "design-banner-concepts-after-logo-approved"):
            self.assertIn(core, ids)
        self.assertTrue(any(x.get("skill") == "ask-career-skills" and x["mode"] == "explicit" for x in items))
        self.assertTrue(any(x.get("skill") == "validate-workspace" and x["mode"] == "discovery" for x in items))
        self.assertTrue(all(any(case["id"] == expected for case in items) for expected in ("profile-no-intent-existing", "profile-no-intent-new")))
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
