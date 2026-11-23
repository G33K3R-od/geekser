"""Disposable-checkout tests for the Geekser browser command palette patch."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("patch-command.py")


class CommandPatchTests(unittest.TestCase):
    def test_idempotent_and_reversible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "mach").touch()
            path = root / "browser/base/content/browser.js"
            path.parent.mkdir(parents=True)
            path.write_text("// Firefox browser chrome\n")
            def call(*args):
                return subprocess.run([sys.executable, str(SCRIPT), str(root), *args], capture_output=True, text=True)
            self.assertEqual(call("--check").returncode, 1)
            self.assertEqual(call().returncode, 0)
            first = path.read_text()
            self.assertIn("geekser-palette", first)
            self.assertIn("gBrowser.selectedTab", first)
            self.assertEqual(call().returncode, 0)
            self.assertEqual(first, path.read_text())
            self.assertEqual(call("--check").returncode, 0)
            self.assertEqual(call("--revert").returncode, 0)
            self.assertEqual(path.read_text(), "// Firefox browser chrome\n")

    def test_incomplete_marker_is_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "mach").touch()
            path = root / "browser/base/content/browser.js"
            path.parent.mkdir(parents=True)
            path.write_text("// GEEKSER COMMAND PALETTE — BEGIN\n")
            result = subprocess.run([sys.executable, str(SCRIPT), str(root)], capture_output=True)
            self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
