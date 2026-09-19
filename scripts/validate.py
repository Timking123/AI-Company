"""Validate the public documentation kit without network or model calls."""

from __future__ import annotations

import re
import struct
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = {
    "AGENTS.md", "CLAUDE.md", "GEMINI.md", "WORKFLOW.md", "README.md", "README.zh-CN.md", "LICENSE",
    "docs/ROLES.md", "docs/TEMPLATES.md", "docs/CODEX.md", "docs/EXAMPLES.md",
    "docs/VALIDATION.md", "docs/SOURCES.md", "docs/COMPATIBILITY.md", "docs/PRIVACY.md", "assets/company-hero.png",
    "assets/organization.svg", "assets/parallel.svg", "scripts/validate.py",
    ".gitignore", ".gitattributes", ".github/workflows/docs.yml",
}
EXCLUDED = {".git", ".preview", ".ai-company", "__pycache__", "node_modules"}


def safe_regular(path: Path) -> bool:
    if not path.resolve().is_relative_to(ROOT) or not path.is_file():
        return False
    current = path
    while current != ROOT:
        if current.is_symlink():
            return False
        current = current.parent
    return True


def headings(text: str) -> set[str]:
    """Approximate GitHub heading IDs for this kit's simple headings."""
    result: set[str] = set()
    counts: dict[str, int] = {}
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*$", line)
        if not match:
            continue
        title = re.sub(r"<[^>]+>", "", match.group(1)).lower()
        title = "".join(c for c in title if c in " -_" or unicodedata.category(c)[0] in "LN")
        slug = title.replace(" ", "-")
        count = counts.get(slug, 0)
        result.add(slug if count == 0 else f"{slug}-{count}")
        counts[slug] = count + 1
    result.update(re.findall(r'\bid=["\']([^"\']+)["\']', text))
    return result


def validate() -> list[str]:
    errors: list[str] = []
    for name in sorted(REQUIRED):
        path = ROOT / name
        if not safe_regular(path) or path.stat().st_size == 0:
            errors.append(f"Missing or empty required file: {name}")

    entries = [p for p in ROOT.rglob("*") if not set(p.relative_to(ROOT).parts) & EXCLUDED]
    for path in entries:
        relative = path.relative_to(ROOT).as_posix()
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
            errors.append(f"Unsafe linked path: {relative}")
            continue
        if not path.is_file():
            continue
        if path.suffix not in {".md", ".svg", ".py", ".yml"} and path.name not in {"LICENSE", ".gitignore", ".gitattributes"}:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"Not UTF-8: {relative}")
            continue
        if content.startswith("\ufeff") or "\ufffd" in content:
            errors.append(f"BOM or replacement character: {relative}")
        if any(line != line.rstrip() for line in content.splitlines()):
            errors.append(f"Trailing whitespace: {relative}")
        sensitive = {
            "local user path": r"(?<![A-Za-z0-9._~:/\\-])(?:[A-Za-z]:[\\/](?:Users|home)[\\/]|/(?:Users|home)/)[^\s<>]+",
            "private task UUID": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            "credential-shaped value": r"\b(?:ghp_|github_pat_|sk-proj-)[A-Za-z0-9_]{20,}\b",
        }
        for kind, pattern in sensitive.items():
            if re.search(pattern, content, re.I):
                errors.append(f"Possible {kind}: {relative}")
        if path.suffix == ".md":
            refs = re.findall(r"\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", content)
            refs += re.findall(r'\b(?:src|href)=["\']([^"\']+)["\']', content)
            for ref in refs:
                parsed = urlsplit(ref)
                if parsed.scheme in {"https", "http", "mailto"}:
                    continue
                if parsed.scheme or parsed.netloc:
                    errors.append(f"Unsupported link scheme: {relative}")
                    continue
                target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
                if not target.is_relative_to(ROOT):
                    errors.append(f"Link escapes repository: {relative} -> {ref}")
                elif not target.exists():
                    errors.append(f"Broken local link: {relative} -> {ref}")
                elif parsed.fragment and target.suffix == ".md":
                    if unquote(parsed.fragment) not in headings(target.read_text(encoding="utf-8")):
                        errors.append(f"Broken anchor: {relative} -> {ref}")
        if path.suffix == ".svg":
            try:
                tree = ET.fromstring(content)
                if re.search(r"@import|url\(\s*(?!#)[^)]*\)", content, re.I):
                    errors.append(f"SVG uses external CSS resources: {relative}")
                if "viewBox" not in tree.attrib or not tree.findall("{*}title") or not tree.findall("{*}desc"):
                    errors.append(f"SVG missing accessible title, description, or viewBox: {relative}")
                for element in tree.iter():
                    if element.tag.rsplit("}", 1)[-1] in {"script", "foreignObject", "image"}:
                        errors.append(f"SVG uses active or external content: {relative}")
                    if any(k.lower().startswith("on") or k.rsplit("}", 1)[-1] == "href" for k in element.attrib):
                        errors.append(f"SVG event or external reference: {relative}")
            except ET.ParseError:
                errors.append(f"Malformed SVG: {relative}")

    hero = ROOT / "assets/company-hero.png"
    if safe_regular(hero):
        with hero.open("rb") as stream:
            header = stream.read(24)
        if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
            errors.append("Hero is not a PNG")
        else:
            width, height = struct.unpack(">II", header[16:24])
            if width < 1000 or height < 400 or not 1.8 <= width / height <= 2.2:
                errors.append("Hero dimensions do not match the wide cover format")

    diagram = ROOT / "assets/parallel.svg"
    if safe_regular(diagram):
        try:
            tree = ET.fromstring(diagram.read_text(encoding="utf-8"))
            metadata = tree.find("{*}metadata")
            values = dict(re.findall(r"([a-z_]+)=(\d+)", metadata.text or "")) if metadata is not None else {}
            expected = {"plan": 1, "tasks": 4, "task_duration": 2, "integrate": 1, "serial_slots": 1, "parallel_slots": 4, "serial_elapsed": 10, "parallel_elapsed": 4, "scheduled_work": 10}
            if {key: int(value) for key, value in values.items()} != expected:
                errors.append("Schedule metadata differs from the documented example")
            serial = expected["plan"] + expected["tasks"] * expected["task_duration"] + expected["integrate"]
            parallel = expected["plan"] + expected["task_duration"] + expected["integrate"]
            if serial != expected["scheduled_work"] or parallel != expected["parallel_elapsed"]:
                errors.append("Schedule arithmetic is inconsistent")
        except (ET.ParseError, ValueError):
            errors.append("Schedule metadata cannot be read")
    return errors


if __name__ == "__main__":
    findings = validate()
    if findings:
        for finding in findings:
            print(f"FAIL: {finding}")
        sys.exit(1)
    print(f"PASS: {len(REQUIRED)} required files; links, portable text, artwork structure, and schedule assumptions.")
    print("Structural validation only. No agent runtime, model behavior, or performance benchmark was tested.")
