"""合成数据覆盖累计归属、输入损坏与 CLI 隐私边界，不读取真实日志。"""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "usage_report.py"
SPEC = importlib.util.spec_from_file_location("usage_report", SCRIPT)
usage = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = usage
SPEC.loader.exec_module(usage)


def counts(inputs=0, outputs=0, cached=0, reasoning=0):
    return dict(zip(usage.FIELDS, (inputs, cached, outputs, reasoning, inputs + outputs)))


def event(minute, total, last=None):
    return {"timestamp": f"2026-01-01T00:{minute:02d}:00Z", "type": "event_msg",
            "payload": {"type": "token_count", "info": {
                "total_token_usage": total, "last_token_usage": total if last is None else last}}}


def session(minute=0):
    return {"timestamp": f"2026-01-01T00:{minute:02d}:00Z", "type": "session_meta",
            "payload": {"ignored": "不会读取的会话正文"}}


class UsageTests(unittest.TestCase):
    def report(self, records, start=None, end=None):
        report = usage.Usage("worker", usage.parse_time(start) if start else None,
                             usage.parse_time(end) if end else None)
        for record in records:
            report.consume(record)
        return report

    def test_duplicate_counters_and_overlap_do_not_double_count(self):
        a, b = event(1, counts(10, 4)), event(2, counts(30, 8), counts(20, 4))
        report = self.report([session(), a, b, a, b, event(3, counts(30, 8))])
        self.assertEqual(report.totals, (30, 0, 8, 0, 38))
        self.assertEqual(report.duplicates, 3)
        self.assertFalse(report.issues)

    def test_new_session_first_real_request_is_counted(self):
        report = self.report([session(), event(1, counts(10, 5))],
                             "2026-01-01T00:00:00Z", "2026-01-01T00:10:00Z")
        self.assertEqual(report.totals[-1], 15)
        self.assertFalse(report.issues)

    def test_inherited_first_total_is_baseline_and_last_is_visible(self):
        report = self.report([event(1, counts(100, 20), counts(10, 2)),
                              event(2, counts(110, 22), counts(10, 2))])
        self.assertEqual(report.totals[-1], 12)
        self.assertEqual(report.uncertain_last[-1], 12)
        self.assertEqual(report.issues["missing_baseline"], 1)

    def test_half_open_interval_and_timezone(self):
        report = self.report([session(), event(0, counts()), event(1, counts(10)),
                              event(2, counts(20)), event(3, counts(30))],
                             "2026-01-01T08:01:00+08:00", "2026-01-01T00:03:00Z")
        self.assertEqual(report.totals[0], 20)
        self.assertFalse(report.issues)

    def test_first_baseline_before_window_not_counted(self):
        report = self.report([event(0, counts(100)), event(2, counts(110), counts(10))],
                             "2026-01-01T00:01:00Z")
        self.assertEqual(report.totals[0], 10)
        self.assertFalse(report.issues)

    def test_consistent_reset_and_inconsistent_reset(self):
        report = self.report([session(), event(1, counts(100, 20)),
                              event(2, counts(10, 2)),
                              event(3, counts(5, 1), counts(2, 1)),
                              event(4, counts(8, 2), counts(3, 1))])
        self.assertEqual(report.totals[-1], 136)
        self.assertEqual(report.resets, 1)
        self.assertEqual(report.issues["uncertain_reset"], 1)

    def test_cache_and_reasoning_are_subsets(self):
        report = self.report([session(), event(1, counts(100, 30, 60, 10))])
        self.assertEqual(report.totals, (100, 60, 30, 10, 130))
        invalid = counts(110, 31, 100, 11)
        report.consume(event(2, invalid, counts(10, 1)))
        self.assertEqual(report.issues["inconsistent_delta"], 1)
        self.assertEqual(report.totals[-1], 130)

    def test_missing_invalid_fields_and_order_are_explicit(self):
        missing = counts(1)
        del missing["cached_input_tokens"]
        report = self.report([event(1, missing), event(2, counts()), event(1, counts(2))])
        self.assertEqual(report.issues["missing_fields"], 1)
        self.assertEqual(report.issues["out_of_order"], 1)
        for invalid in (counts(-1), counts(1, 0, 2), counts(1, 1, 0, 2),
                        dict(counts(), input_tokens=True), dict(counts(), total_tokens=9)):
            with self.assertRaises(ValueError):
                usage.counters(invalid)
        with self.assertRaises(ValueError):
            usage.parse_time("2026-01-01T00:00:00")

    def test_continuation_files_share_baseline(self):
        with tempfile.TemporaryDirectory() as folder:
            first, second = Path(folder) / "a.jsonl", Path(folder) / "b.jsonl"
            duplicate = event(1, counts(100, 20))
            first.write_text(json.dumps(event(0, counts())) + "\n" + json.dumps(duplicate), encoding="utf-8")
            second.write_text(json.dumps(duplicate) + "\n" + json.dumps(event(2, counts(110, 22), counts(10, 2))), encoding="utf-8")
            report = usage.Usage("worker")
            report.read(first)
            report.read(second)
            self.assertEqual(report.totals[-1], 132)
            self.assertEqual(report.duplicates, 1)
            self.assertFalse(report.issues)

    def test_rate_limit_only_null_info_preserves_usage_baseline(self):
        rate_only = {"timestamp": "2026-01-01T00:02:00Z", "type": "event_msg",
                     "payload": {"type": "token_count", "info": None,
                                 "rate_limits": {"primary": {"used_percent": 12.0}}}}
        report = self.report([session(), event(1, counts(100, 20)), rate_only,
                              event(3, counts(110, 22), counts(10, 2))])
        self.assertEqual(report.totals[-1], 132)
        self.assertEqual(report.samples, 2)
        self.assertFalse(report.issues)

    def test_continuation_recording_metadata_preserves_cumulative_evidence(self):
        for repeat_first in (False, True):
            with self.subTest(repeat_first=repeat_first), tempfile.TemporaryDirectory() as folder:
                first, second = Path(folder) / "a.jsonl", Path(folder) / "b.jsonl"
                earlier = [session(), event(1, counts(100, 20))]
                later = [session(2)]
                if repeat_first:
                    later.append(event(3, counts(100, 20)))
                later.append(event(4, counts(110, 22), counts(10, 2)))
                for path, records in ((first, earlier), (second, later)):
                    path.write_text("\n".join(json.dumps(row) for row in records), encoding="utf-8")
                report = usage.Usage("worker")
                report.read(first)
                report.read(second)
                self.assertEqual(report.totals[-1], 132)
                self.assertFalse(report.issues)
                self.assertEqual(report.segment_changes, 1)
                self.assertEqual(report.duplicates, int(repeat_first))

    def test_segment_metadata_does_not_hide_discontinuity(self):
        report = self.report([session(), event(1, counts(100, 20)), session(2),
                              event(0, counts(80, 16)),
                              event(3, counts(50, 10), counts(5, 1))])
        self.assertEqual(report.issues["out_of_order"], 1)
        self.assertEqual(report.issues["uncertain_reset"], 1)
        self.assertEqual(report.totals[-1], 120)

    def test_outside_window_errors_remain_conservative_incomplete(self):
        malformed = event(0, counts())
        malformed["payload"]["info"] = {}
        report = self.report([malformed, event(1, counts()), event(2, counts(10))],
                             "2026-01-01T00:02:00Z")
        self.assertEqual(report.totals[0], 10)
        self.assertEqual(report.issues["missing_fields"], 1)

    def test_bad_long_lines_and_messages_never_leak(self):
        secret = "SECRET_MARKER_DO_NOT_PRINT"
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "synthetic.jsonl"
            lines = [json.dumps(session()), json.dumps(event(1, counts(4, 2))),
                     json.dumps({"type": "response_item", "payload": {"arguments": secret}}),
                     secret, "x" * 2000 + secret,
                     json.dumps(event(2, counts(8, 4))),
                     json.dumps(event(3, counts(10, 5), counts(2, 1)))]
            path.write_bytes("\n".join(lines).encode("utf-8") + b"\n\xff\xfe\n")
            output = io.StringIO()
            with patch.object(usage, "MAX_LINE_BYTES", 1024), contextlib.redirect_stdout(output):
                result = usage.main(["--label", f"worker={path}"])
            self.assertEqual(result, 1)
            self.assertNotIn(secret, output.getvalue())
            self.assertIn("incomplete / unknown", output.getvalue())
            self.assertIn("超长行", output.getvalue())
            self.assertIn("| 6 | 0 | 6 | 3 | 0 | 9 |", output.getvalue())

    def test_missing_last_keeps_known_delta_but_marks_gap(self):
        broken = event(1, counts(10, 2))
        del broken["payload"]["info"]["last_token_usage"]
        report = self.report([event(0, counts()), broken])
        self.assertEqual(report.totals[-1], 12)
        self.assertEqual(report.issues["missing_fields"], 1)

    def test_no_samples_and_invalid_time_cli(self):
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "empty.jsonl"
            path.write_text("", encoding="utf-8")
            with contextlib.redirect_stdout(output):
                self.assertEqual(usage.main(["--label", f"worker={path}"]), 1)
            self.assertIn("没有可用", output.getvalue())
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            usage.main(["--label", "worker=unused", "--start", "invalid"])
        self.assertEqual(error.exception.code, 2)

    def test_zstd_missing_is_explicit_and_read_errors_redacted(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "synthetic.zst"
            path.write_bytes(b"synthetic")
            report = usage.Usage("worker")
            with patch.dict(sys.modules, {"zstandard": None}):
                report.read(path)
            self.assertEqual(report.issues["zstd_missing"], 1)
            report.previous = (10, 0, 2, 0, 12)
            report.read(Path(folder) / "missing.jsonl")
            self.assertEqual(report.issues["read_error"], 1)
            self.assertIsNone(report.previous)

    def test_zstd_synthetic_success_when_backend_installed(self):
        try:
            import zstandard
        except ImportError:
            self.skipTest("未安装可选 zstandard，缺依赖路径由独立用例验证")
        rows = [session(), event(1, counts(10, 5))]
        data = "\n".join(json.dumps(row) for row in rows).encode("utf-8")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "synthetic.jsonl.zst"
            path.write_bytes(zstandard.ZstdCompressor().compress(data))
            report = usage.Usage("worker")
            report.read(path)
            self.assertEqual(report.totals[-1], 15)
            self.assertFalse(report.issues)
            path.write_bytes(b"corrupt synthetic stream")
            broken = usage.Usage("worker")
            broken.read(path)
            self.assertEqual(broken.issues["read_error"], 1)

    def test_cli_explicit_path_normal_entry_and_bad_arguments(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "synthetic.jsonl"
            path.write_text("\n".join(json.dumps(row) for row in [session(), event(1, counts(10, 5, 4, 2))]), encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", str(SCRIPT), "--label", f"worker={path}"],
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("| 10 | 4 | 6 | 5 | 2 | 15 |", result.stdout)
            self.assertIn("金额：unknown", result.stdout)
            self.assertNotIn(str(path), result.stdout + result.stderr)
            bad = subprocess.run([sys.executable, "-B", str(SCRIPT), "--label", "SECRET_BAD_ARGUMENT"],
                                 capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(bad.returncode, 2)
            self.assertNotIn("SECRET_BAD_ARGUMENT", bad.stdout + bad.stderr)


if __name__ == "__main__":
    unittest.main()
