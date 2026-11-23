"""Tests for the new-tab source patch, using a disposable Firefox-like checkout."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("patch-newtab.py")


class NewTabPatchTests(unittest.TestCase):
    def test_apply_check_reapply_revert(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "mach").write_text("", encoding="utf-8")
            target = root / "browser/base/content/browser.js"
            target.parent.mkdir(parents=True)
            target.write_text("// upstream\n", encoding="utf-8")
            def run(*args):
                return subprocess.run([sys.executable, str(SCRIPT), str(root), *args], capture_output=True, text=True)
            self.assertEqual(run("--check").returncode, 1)
            self.assertEqual(run().returncode, 0)
            applied = target.read_text()
            self.assertIn("AboutNewTab.newTabURL", applied)
            self.assertEqual(run("--check").returncode, 0)
            self.assertEqual(run().returncode, 0)
            self.assertEqual(target.read_text(), applied)
            self.assertEqual(run("--revert").returncode, 0)
            self.assertEqual(target.read_text(), "// upstream\n")
    def test_incomplete_markers_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "mach").write_text("")
            target = root / "browser/base/content/browser.js"
            target.parent.mkdir(parents=True)
            target.write_text("// GEEKSER NEW TAB ROUTING — BEGIN\n")
            p = subprocess.run([sys.executable, str(SCRIPT), str(root)], capture_output=True)
            self.assertEqual(p.returncode, 2)


if __name__ == "__main__":
    unittest.main()
