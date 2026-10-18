"""Synthetic regression tests; these do not benchmark LLM translation quality."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_report.py"
spec = importlib.util.spec_from_file_location("check_report", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReportChecks(unittest.TestCase):
    def kinds(self, source, target):
        return {item["kind"] for item in module.check(source, target)["issues"]}

    def test_same_data(self):
        result = module.check("Giá 50,000 JPY/tháng [S01].", "料金は月額50,000 JPYである [S01]。")
        self.assertEqual(result["status"], "NO_MECHANICAL_FLAGS")
        self.assertTrue(result["semantic_review_required"])

    def test_changed_number(self):
        self.assertIn("numeric_tokens", self.kinds("50,000 JPY", "500,000 JPY"))

    def test_sign_change(self):
        self.assertIn("numeric_tokens", self.kinds("−2.0%", "+2.0%"))

    def test_empty_target(self):
        self.assertIn("empty_input", self.kinds("Nội dung", " "))

    def test_missing_source(self):
        self.assertIn("empty_input", self.kinds("", "本文"))

    def test_lost_citation(self):
        self.assertIn("citation_markers", self.kinds("Ý [E-12]", "本文"))

    def test_lost_footnote(self):
        self.assertIn("citation_markers", self.kinds("Ý [^source-a]", "本文"))

    def test_duplicate_citation_count(self):
        self.assertIn("citation_markers", self.kinds("[S01] [S01]", "[S01]"))

    def test_changed_url(self):
        self.assertIn("urls", self.kinds("[nguồn](https://example.com/a)", "[出典](https://example.com/b)"))

    def test_translated_link_label(self):
        self.assertNotIn("urls", self.kinds("[nguồn](https://example.com/a)", "[出典](https://example.com/a)"))

    def test_added_tool_credit(self):
        self.assertIn("new_tool_attribution", self.kinds("Báo cáo", "本文\nPowered by natural-japanese"))

    def test_preserve_legitimate_source_name(self):
        self.assertNotIn("new_tool_attribution", self.kinds("Tác giả: coji", "著者: coji"))

    def test_japanese_unit_conversion_requires_review(self):
        self.assertIn("numeric_tokens", self.kinds("50,000 JPY", "5万円"))

    def test_fullwidth_numbers(self):
        self.assertNotIn("numeric_tokens", self.kinds("20%", "２０％"))

    def test_decimal_comma_not_assumed_equivalent(self):
        self.assertIn("numeric_tokens", self.kinds("1,5", "15"))

    def test_limitations_are_explicit(self):
        result = module.check("Có thể thử", "試行できる")
        self.assertNotIn("PASS", result["status"])
        self.assertIn("not translation approval", result["limitations"])

    def test_missing_file_exit(self):
        with tempfile.TemporaryDirectory() as folder:
            missing = Path(folder) / "missing.md"
            result = subprocess.run([sys.executable, str(SCRIPT), str(missing), str(missing)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stderr)["status"], "ERROR")

    def test_cli_does_not_modify_inputs(self):
        with tempfile.TemporaryDirectory() as folder:
            source, target = Path(folder) / "s.md", Path(folder) / "t.md"
            source.write_text("50 JPY [S01]", encoding="utf-8")
            target.write_text("50 JPY [S01]", encoding="utf-8")
            original = source.read_bytes(), target.read_bytes()
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), str(target)], capture_output=True, text=True)
            self.assertEqual((source.read_bytes(), target.read_bytes()), original)
            self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
