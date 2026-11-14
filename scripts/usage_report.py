"""只读汇总显式指定的 Codex JSONL；不推测费用或提取消息正文。"""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import sys

MAX_LINE_BYTES = 1024 * 1024
FIELDS = ("input_tokens", "cached_input_tokens", "output_tokens",
          "reasoning_output_tokens", "total_tokens")
ZERO = (0, 0, 0, 0, 0)
ISSUES = {
    "bad_line": "坏行/无法解析的记录",
    "long_line": "超长行已跳过",
    "missing_fields": "计数缺字段或不合法",
    "bad_timestamp": "缺少合法且带时区的时间戳",
    "missing_baseline": "首累计继承历史，缺少前序 baseline",
    "uncertain_reset": "累计下降但 last 不能证明一致 reset",
    "inconsistent_delta": "累计差分违反子集关系",
    "out_of_order": "非重复样本时间倒序",
    "read_error": "文件无法读取或解压",
    "zstd_missing": ".zst 需要已安装的 zstandard；未自动安装",
    "no_data": "区间内没有可用 token_count 样本",
}


def parse_time(value: str) -> datetime:
    """所有比较归一为 UTC；拒绝猜测无时区时间。"""
    if not isinstance(value, str):
        raise ValueError
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError
    return parsed.astimezone(timezone.utc)


def counters(value: object) -> tuple[int, ...]:
    if not isinstance(value, dict):
        raise ValueError
    numbers = tuple(value.get(name) for name in FIELDS)
    if any(type(number) is not int or number < 0 for number in numbers):
        raise ValueError
    if not valid_counts(numbers):
        raise ValueError
    return numbers


def valid_counts(numbers: tuple[int, ...]) -> bool:
    inputs, cached, outputs, reasoning, total = numbers
    return (cached <= inputs and reasoning <= outputs and total == inputs + outputs
            and all(number >= 0 for number in numbers))


@contextmanager
def open_log(path: Path):
    """普通文件仅用标准库；压缩支持是显式可选的已装依赖。"""
    if path.suffix.lower() == ".zst":
        try:
            import zstandard
        except ImportError:
            raise ModuleNotFoundError("zstd_missing") from None
        with path.open("rb") as source:
            with zstandard.ZstdDecompressor().stream_reader(source) as reader:
                with io.BufferedReader(reader) as buffered:
                    yield buffered
    else:
        with path.open("rb") as source:
            yield source


def bounded_lines(source):
    """超长行分块排空，内存不随单行长度增长；不保留原文。"""
    while True:
        line = source.readline(MAX_LINE_BYTES + 1)
        if not line:
            return
        if len(line) > MAX_LINE_BYTES:
            while line and not line.endswith(b"\n"):
                line = source.readline(MAX_LINE_BYTES + 1)
            yield None
        else:
            yield line


@dataclass
class Usage:
    name: str
    start: datetime | None = None
    end: datetime | None = None
    totals: tuple[int, ...] = ZERO
    uncertain_last: tuple[int, ...] = ZERO
    issues: Counter = field(default_factory=Counter)
    previous: tuple[int, ...] | None = None
    latest_time: datetime | None = None
    created: datetime | None = None
    seen: set = field(default_factory=set)
    samples: int = 0
    duplicates: int = 0
    resets: int = 0
    segment_changes: int = 0

    def in_window(self, timestamp: datetime) -> bool:
        return ((self.start is None or timestamp >= self.start)
                and (self.end is None or timestamp < self.end))

    def add(self, delta: tuple[int, ...]) -> None:
        self.totals = tuple(a + b for a, b in zip(self.totals, delta))

    def consume(self, record: object) -> None:
        if not isinstance(record, dict):
            self.issues["bad_line"] += 1
            self.previous = None
            return
        kind = record.get("type")
        payload = record.get("payload")
        if kind == "session_meta":
            try:
                created = parse_time(record.get("timestamp"))
            except (ValueError, TypeError, OverflowError):
                self.issues["bad_timestamp"] += 1
                return
            if self.created is not None and self.created != created:
                # 连续文件可能重新录制元数据；用后续累计验证连续性。
                self.segment_changes += 1
            self.created = created
            return
        if kind != "event_msg" or not isinstance(payload, dict):
            return
        if payload.get("type") != "token_count":
            return
        if "info" in payload and payload["info"] is None:
            # 合法的限额更新不包含用量样本，不改变累计或时间基线。
            return
        try:
            timestamp = parse_time(record.get("timestamp"))
        except (ValueError, TypeError, OverflowError):
            self.issues["bad_timestamp"] += 1
            self.previous = None
            return
        info = payload.get("info")
        try:
            total = counters(info.get("total_token_usage") if isinstance(info, dict) else None)
        except ValueError:
            self.issues["missing_fields"] += 1
            self.previous = None
            return
        try:
            last = counters(info.get("last_token_usage"))
            if any(a > b for a, b in zip(last, total)):
                raise ValueError
        except ValueError:
            self.issues["missing_fields"] += 1
            last = None
        selected = self.in_window(timestamp)
        if selected:
            self.samples += 1
        snapshot = (timestamp, total)
        if snapshot in self.seen:
            self.duplicates += 1
            return
        self.seen.add(snapshot)
        if self.latest_time is not None and timestamp < self.latest_time:
            self.issues["out_of_order"] += 1
            return
        first_snapshot = self.latest_time is None
        self.latest_time = timestamp
        if self.previous is None:
            # 新会话首请求有创建时间和 last 双重证据；继承累计只作基线。
            if selected and total != ZERO:
                if (first_snapshot and self.created is not None and self.in_window(self.created)
                        and self.created <= timestamp and total == last):
                    self.add(total)
                else:
                    self.issues["missing_baseline"] += 1
                    if last is not None:
                        self.uncertain_last = tuple(a + b for a, b in zip(self.uncertain_last, last))
            self.previous = total
            return
        if total == self.previous:
            self.duplicates += 1
            return
        delta = tuple(a - b for a, b in zip(total, self.previous))
        if any(number < 0 for number in delta):
            if total == last:
                self.resets += 1
                if selected:
                    self.add(total)
            else:
                self.issues["uncertain_reset"] += 1
        elif valid_counts(delta):
            if selected:
                self.add(delta)
        else:
            self.issues["inconsistent_delta"] += 1
        # 缺口之后重新建立基线，后续可确认差分仍可报告。
        self.previous = total

    def read(self, path: Path) -> None:
        try:
            if str(path).startswith(("\\\\", "//")) or not path.is_file():
                self.issues["read_error"] += 1
                self.previous = None
                return
            with open_log(path) as source:
                for raw in bounded_lines(source):
                    if raw is None:
                        self.issues["long_line"] += 1
                        self.previous = None
                        continue
                    try:
                        record = json.loads(raw.decode("utf-8"))
                    except (ValueError, UnicodeDecodeError, RecursionError):
                        self.issues["bad_line"] += 1
                        self.previous = None
                        continue
                    self.consume(record)
        except ModuleNotFoundError:
            self.issues["zstd_missing"] += 1
            self.previous = None
        except Exception:
            # 解压异常可能携带原始内容或路径，输出仅使用固定诊断。
            self.issues["read_error"] += 1
            self.previous = None


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(2, "参数错误：请使用 --help 查看显式路径与带时区时间的格式。\n")


def main(argv: list[str] | None = None) -> int:
    parser = SafeParser(description=__doc__)
    parser.add_argument("--label", action="append", required=True, metavar="NAME=PATH",
                        help="显式文件路径；同标签按参数顺序视作连续文件，可重复")
    parser.add_argument("--start", help="含起点的 ISO 时间，必须带时区")
    parser.add_argument("--end", help="不含终点的 ISO 时间，必须带时区")
    args = parser.parse_args(argv)
    try:
        start = parse_time(args.start) if args.start else None
        end = parse_time(args.end) if args.end else None
        if start is not None and end is not None and start >= end:
            raise ValueError
        labels = {}
        for item in args.label:
            name, path = item.split("=", 1)
            if not path or not 1 <= len(name) <= 64 or not all(c.isalnum() or c in "_.-" for c in name):
                raise ValueError
            labels.setdefault(name, []).append(Path(path))
    except (ValueError, TypeError, OverflowError):
        parser.error("")
    reports = []
    for name, paths in labels.items():
        report = Usage(name, start, end)
        for path in paths:
            report.read(path)
        if report.samples == 0:
            report.issues["no_data"] += 1
        reports.append(report)
    print("# Codex Token 用量（只读）\n")
    print("区间按 token_count 时间戳归属，采用 [start, end)。计数是日志已确认部分；金额：unknown。\n")
    print("| 标签 | 状态 | input | 其中 cached | 未缓存 input | output | 其中 reasoning | input+output |")
    print("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for report in reports:
        inputs, cached, outputs, reasoning, total = report.totals
        status = "incomplete / unknown" if report.issues else "complete（日志范围）"
        print(f"| {report.name} | {status} | {inputs} | {cached} | {inputs-cached} | {outputs} | {reasoning} | {total} |")
    for report in reports:
        print(f"\n{report.name}：区间样本 {report.samples}；重复 {report.duplicates}；一致 reset {report.resets}；元数据录制段变化 {report.segment_changes}。")
        for code, count in sorted(report.issues.items()):
            print(f"- {ISSUES[code]}：{count}。")
        if report.uncertain_last != ZERO:
            inputs, cached, outputs, reasoning, total = report.uncertain_last
            print(f"- 首样本 last（区间归属 unknown，未计入合计）：input {inputs}、cached {cached}、output {outputs}、reasoning {reasoning}、total {total}。")
    print("\n缓存属于 input，reasoning 属于 output；不另行相加。Token 不是净新增文字，也不等于金额。")
    if any(report.issues["read_error"] or report.issues["zstd_missing"] for report in reports):
        return 2
    return 1 if any(report.issues for report in reports) else 0


if __name__ == "__main__":
    sys.exit(main())
