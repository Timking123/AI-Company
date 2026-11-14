"""只读核对场景结构和结果完整性；不联网、不执行场景、不证明模型行为。"""

import argparse
import json
import sys
from pathlib import Path

NO_RESULTS = object()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def load_json(path):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"重复 JSON 字段：{key}")
            result[key] = value
        return result

    return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)


def check(scenarios, results=NO_RESULTS):
    errors = []
    if not isinstance(scenarios, dict) or type(scenarios.get("schema_version")) is not int or scenarios["schema_version"] != 1:
        return ["场景 schema_version 必须为 1"]
    entries = scenarios.get("scenarios")
    if not isinstance(entries, list) or not entries:
        return ["场景列表缺失或为空"]
    expected = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"场景 {index} 不是对象")
            continue
        sid = entry.get("id")
        if not nonempty(sid):
            errors.append(f"场景 {index} ID 无效")
            continue
        if sid in expected:
            errors.append(f"重复场景 ID：{sid}")
        expected[sid] = entry.get("expected_decision")
        for key in ("title", "context", "request", "expected_decision"):
            if not nonempty(entry.get(key)):
                errors.append(f"{sid} 缺少 {key}")
        for key in ("expected_behaviors", "forbidden_behaviors"):
            values = entry.get(key)
            if not isinstance(values, list) or not values or not all(nonempty(v) for v in values):
                errors.append(f"{sid} 的 {key} 无效")
    if results is NO_RESULTS:
        return errors
    if not isinstance(results, dict) or type(results.get("schema_version")) is not int or results["schema_version"] != 1:
        return errors + ["结果 schema_version 必须为 1"]
    layer = results.get("validation_layer")
    if layer not in ("fixture", "manual_review", "model_run"):
        errors.append("结果验证层无效")
    if layer == "model_run" and not nonempty(results.get("run_id")):
        errors.append("模型结果缺少实际 run_id")
    records = results.get("results")
    if not isinstance(records, list):
        return errors + ["结果列表无效"]
    seen = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"结果 {index} 不是对象")
            continue
        sid = record.get("id")
        if not nonempty(sid):
            errors.append(f"结果 {index} ID 无效")
            continue
        if sid in seen:
            errors.append(f"重复结果 ID：{sid}")
        seen.add(sid)
        if sid not in expected:
            errors.append(f"未知结果 ID：{sid}")
        elif record.get("decision") != expected[sid]:
            errors.append(f"{sid} 决策不匹配")
        for key in ("answer", "evidence"):
            if not nonempty(record.get(key)):
                errors.append(f"{sid} 未回答或缺证据：{key}")
        if record.get("passed") is not True:
            errors.append(f"{sid} 未通过行为评审")
    errors.extend(f"缺少结果 ID：{sid}" for sid in sorted(set(expected) - seen))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenarios", required=True)
    parser.add_argument("--results")
    args = parser.parse_args()
    try:
        scenarios = load_json(args.scenarios)
        results = load_json(args.results) if args.results is not None else NO_RESULTS
        errors = check(scenarios, results)
    except (OSError, ValueError, TypeError) as error:
        print(f"输入失败：{error}")
        return 2
    if errors:
        for error in errors:
            print(f"失败：{error}")
        return 1
    scope = "离线结果完整性" if args.results is not None else "场景结构"
    print(f"{scope}通过；场景 {len(scenarios['scenarios'])} 项。此结果不证明真实模型行为。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
