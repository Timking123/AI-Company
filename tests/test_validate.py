"""验证版本漂移与场景遗失能够报错，避免结构绿灯掩盖入口分叉。"""

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        names = ("AGENTS.md", "WORKFLOW.md", "README.md", "README.zh-CN.md", "docs/VALIDATION.md", "validation/EXPECTATIONS.md")
        self.documents = {name: (ROOT / name).read_text(encoding="utf-8") for name in names}
        self.scenarios = json.loads((ROOT / "validation/scenarios.json").read_text(encoding="utf-8"))

    def test_current_sources_and_next_release_without_code_pin(self):
        self.assertEqual(validate.validate_protocol(self.version, self.documents, self.scenarios), [])
        next_version = "8.2.1"
        documents = {name: text.replace(self.version, next_version) for name, text in self.documents.items()}
        scenarios = copy.deepcopy(self.scenarios)
        scenarios["workflow_version"] = next_version
        self.assertEqual(validate.validate_protocol(next_version, documents, scenarios), [])

    def test_one_stale_or_missing_current_entry_is_rejected(self):
        for name in ("AGENTS.md", "WORKFLOW.md", "README.md", "README.zh-CN.md", "docs/VALIDATION.md"):
            with self.subTest(name=name):
                documents = dict(self.documents)
                documents[name] = documents[name].replace(self.version, "0.0.0")
                self.assertTrue(validate.validate_protocol(self.version, documents, self.scenarios))
                documents[name] = ""
                self.assertTrue(validate.validate_protocol(self.version, documents, self.scenarios))

    def test_stale_scenarios_or_invalid_release_is_rejected(self):
        scenarios = copy.deepcopy(self.scenarios)
        scenarios["workflow_version"] = "0.0.0"
        self.assertTrue(validate.validate_protocol(self.version, self.documents, scenarios))
        self.assertTrue(validate.validate_protocol("release pending", self.documents, self.scenarios))

    def test_original_id_cannot_be_replaced_even_if_count_and_coverage_hold(self):
        scenarios = copy.deepcopy(self.scenarios)
        scenarios["scenarios"][0]["id"] = "R99"
        documents = dict(self.documents)
        documents["validation/EXPECTATIONS.md"] = documents["validation/EXPECTATIONS.md"].replace("| R01 |", "| R99 |")
        findings = validate.validate_protocol(self.version, documents, scenarios)
        self.assertIn("Original 76 scenario IDs must be retained", findings)

    def test_missing_duplicate_or_unknown_expectation_is_rejected(self):
        for replacement in ("", "| R01 | repeated |\n| R01 | original |", "| R99 | unknown |"):
            with self.subTest(replacement=replacement):
                documents = dict(self.documents)
                lines = documents["validation/EXPECTATIONS.md"].splitlines()
                documents["validation/EXPECTATIONS.md"] = "\n".join(replacement if line.startswith("| R01 |") else line for line in lines)
                self.assertTrue(validate.validate_protocol(self.version, documents, self.scenarios))


if __name__ == "__main__":
    unittest.main()
