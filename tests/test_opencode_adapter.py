import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ADAPTER = Path(__file__).resolve().parents[1] / "scripts" / "opencode_adapter.py"


class FreeLimitTest(unittest.TestCase):
    def test_free_usage_limit_fails_fast_as_harness_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            bindir, cwd = Path(tmp, "bin"), Path(tmp, "case")
            bindir.mkdir(), cwd.mkdir()
            fake = bindir / "opencode"
            # Prints the limit error then hangs, as the real CLI does while retrying.
            fake.write_text("#!/bin/sh\necho 'ERROR stream error error=\"AI_APICallError: Free usage limit reached.\"' >&2\nsleep 60\n")
            fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
            env = {**os.environ, "PATH": f"{bindir}:{os.environ['PATH']}"}
            result = subprocess.run([sys.executable, str(ADAPTER)], input="hi", cwd=cwd, env=env,
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 75)
            self.assertIn("HARNESS ERROR", result.stdout)


if __name__ == "__main__":
    unittest.main()
