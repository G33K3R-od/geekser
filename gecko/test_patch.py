"""Offline smoke tests for the Geekser Firefox source patcher."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).with_name("apply-ui.py")
spec = importlib.util.spec_from_file_location("geekser_patch", MODULE)
patch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch)


class SourcePatchTests(unittest.TestCase):
    def test_marker_removal_and_idempotence(self):
        source = "header\n" + patch.CSS
        cleaned = patch.remove_block(source, patch.START, patch.END)
        self.assertNotIn(patch.START, cleaned)
        self.assertIn("header", cleaned)
        self.assertEqual(patch.remove_block(cleaned, patch.START, patch.END), cleaned)

    def test_incomplete_marker_refused(self):
        with self.assertRaises(ValueError):
            patch.remove_block("header " + patch.START, patch.START, patch.END)

    def test_duplicate_marker_refused(self):
        with self.assertRaises(ValueError):
            patch.remove_block(patch.CSS + patch.CSS, patch.START, patch.END)

    def test_old_m1_patch_migrates(self):
        old = patch.OLD_START + "\nlegacy\n" + patch.OLD_END
        cleaned = patch.remove_block(old, patch.OLD_START, patch.OLD_END)
        self.assertNotIn("legacy", cleaned)


if __name__ == "__main__":
    unittest.main()
