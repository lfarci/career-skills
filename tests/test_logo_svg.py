import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from xml.etree import ElementTree as ET

SCRIPT = Path(__file__).resolve().parents[1] / "skills/design-identity/scripts/build_logo_svg.py"
spec = importlib.util.spec_from_file_location("svg_builder", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def drawing():
    return {"viewBox": [0, 0, 100, 100], "title": "<study>&", "shapes": [
        {"type": "circle", "cx": 50, "cy": 50, "r": 20, "fill": "#123456"},
        {"type": "path", "d": "M10 10 L20 20 Z", "fill": "none", "stroke": "black"}]}

class BuilderTests(unittest.TestCase):
    def test_static_output_and_escaping(self):
        root = ET.fromstring(module.build(drawing()))
        self.assertEqual(root.find("{http://www.w3.org/2000/svg}title").text, "<study>&")
        self.assertEqual(len(root), 3)

    def test_reject_active_and_external_content(self):
        for shape in [
            {"type": "script"}, {"type": "image", "href": "https://example.com/x"},
            {"type": "circle", "onload": "alert(1)"},
            {"type": "circle", "fill": "url(https://example.com/x)"},
            {"type": "path", "d": "<script/>"},
        ]:
            with self.subTest(shape=shape), self.assertRaises(ValueError):
                module.build({"viewBox": [0, 0, 100, 100], "shapes": [shape]})

    def test_reject_unbounded_or_invalid_geometry(self):
        for change in [
            {"viewBox": [0, 0, float("nan"), 100]},
            {"shapes": [{"type": "circle", "r": -1}]},
            {"shapes": [{"type": "circle", "r": 100001}]},
            {"shapes": [{"type": "polygon", "points": "1 2 3"}]},
            {"shapes": [{"type": "circle"}] * 257},
        ]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                module.build(drawing() | change)

    def test_cli_preserves_existing_file_and_rejects_invalid_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp)/"spec.json", Path(tmp)/"logo.svg"
            source.write_text(json.dumps(drawing()))
            command = [sys.executable, str(SCRIPT), str(source), str(target)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            before = target.read_bytes()
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual(target.read_bytes(), before)
            target.unlink()
            source.write_text('{"viewBox":[0,0,1,1],"shapes":[{"type":"script"}]}')
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertFalse(target.exists())

if __name__ == "__main__":
    unittest.main()
