#!/usr/bin/env python3
"""
Question quality linter for DatabricksExamHelper.

Checks:
1) File naming and ID format
2) Required sections (ID / Topics / 正解 / 難度)
3) Option and answer consistency
4) Topic/Trap tags against .github/skills/tagging-schema/references/tagging-schema.md
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


QUESTION_POOLS = [
    "question-bank/by-order_v1",
    "question-bank/by-order_b1",
    "question-bank/by-order_b2",
    "question-bank/by-order_b3",
    "question-bank/by-order_b4",
]

LEVEL_TAGS = {"L1-Basic", "L2-Intermediate", "L3-Advanced"}


@dataclass
class LintResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, path: Path, msg: str) -> None:
        self.errors.append(f"{path}: {msg}")

    def add_warning(self, path: Path, msg: str) -> None:
        self.warnings.append(f"{path}: {msg}")


def _extract_table_tags(section_text: str) -> set[str]:
    tags: set[str] = set()
    for line in section_text.splitlines():
        m = re.match(r"^\|\s*`?([A-Za-z][A-Za-z0-9-]+)`?\s*\|", line)
        if not m:
            continue
        token = m.group(1)
        if token in {"標籤", "Tags"}:
            continue
        tags.add(token)
    return tags


def load_valid_tags(schema_path: Path) -> tuple[set[str], set[str]]:
    text = schema_path.read_text(encoding="utf-8")
    topic_start = text.find("## 📚 Topic Tags")
    trap_start = text.find("## ⚠️ Trap Tags")
    level_start = text.find("## 📊 Level Tags")

    if topic_start == -1 or trap_start == -1 or level_start == -1:
        raise RuntimeError("tagging-schema.md section markers not found")

    topic_section = text[topic_start:trap_start]
    trap_section = text[trap_start:level_start]

    return _extract_table_tags(topic_section), _extract_table_tags(trap_section)


def parse_markdown_tags(tag_line: str) -> list[str]:
    tick_tags = re.findall(r"`([^`]+)`", tag_line)
    if tick_tags:
        return [t.strip() for t in tick_tags if t.strip()]
    return [p.strip() for p in tag_line.split(",") if p.strip()]


def detect_pool(path: Path) -> str:
    parts = set(path.parts)
    for pool in ("by-order_v1", "by-order_b1", "by-order_b2", "by-order_b3", "by-order_b4"):
        if pool in parts:
            return pool
    return "unknown"


def _structural_issue(result: LintResult, path: Path, pool: str, msg: str) -> None:
    # by-order_v1 is legacy pool (2024-2025); keep structural issues as warnings.
    if pool == "by-order_v1":
        result.add_warning(path, f"[legacy] {msg}")
    else:
        result.add_error(path, msg)


def check_file(
    path: Path,
    valid_topics: set[str],
    valid_traps: set[str],
    result: LintResult,
    check_tag_schema: bool,
) -> None:
    text = path.read_text(encoding="utf-8")
    pool = detect_pool(path)

    if not re.fullmatch(r"Q-\d{3}\.md", path.name):
        _structural_issue(result, path, pool, f"invalid filename '{path.name}', expected Q-XXX.md")

    id_match = re.search(r"\*\*ID[:：]\*\*\s*`([^`]+)`", text)
    if not id_match:
        _structural_issue(result, path, pool, "missing '**ID:**' field")
        file_id = None
    else:
        file_id = id_match.group(1).strip()
        if pool == "by-order_v1":
            if not (re.fullmatch(r"Q-\d{3}", file_id) or re.fullmatch(r"Q-\d{2}-\d{3}", file_id)):
                _structural_issue(result, path, pool, f"invalid legacy ID format '{file_id}'")
        else:
            if not re.fullmatch(r"Q-\d{3}", file_id):
                result.add_warning(path, f"new pool should prefer Q-XXX format, got '{file_id}'")

        file_num = re.search(r"(\d{3})", path.stem)
        id_num = re.search(r"(\d{3})$", file_id)
        if file_num and id_num and file_num.group(1) != id_num.group(1):
            result.add_warning(path, f"ID/file mismatch: file={path.stem}, id={file_id}")

    options = set(re.findall(r"^\s*-\s*\*\*([A-E])\.\*\*", text, re.MULTILINE))
    if len(options) < 4:
        _structural_issue(result, path, pool, f"expected at least 4 options (A-D), found {sorted(options)}")

    answer_match = re.search(r"\*\*正解[:：]\*\*\s*`?([A-E](?:\s*,\s*[A-E])*)`?", text)
    if not answer_match:
        _structural_issue(result, path, pool, "missing or invalid '**正解:**' field")
    else:
        answers = [x.strip() for x in answer_match.group(1).split(",")]
        for ans in answers:
            if ans not in options:
                _structural_issue(
                    result, path, pool, f"answer '{ans}' not found in options {sorted(options)}"
                )

    topics_match = re.search(r"\*\*Topics[:：]\*\*\s*(.+)", text)
    if not topics_match:
        _structural_issue(result, path, pool, "missing '**Topics:**' field")
        topics: list[str] = []
    else:
        topics = parse_markdown_tags(topics_match.group(1))
        if len(topics) == 0:
            _structural_issue(result, path, pool, "empty Topics")
        if len(topics) > 3:
            result.add_warning(path, f"topics count {len(topics)} exceeds recommended max (3)")
        if check_tag_schema:
            for t in topics:
                if t not in valid_topics:
                    result.add_warning(path, f"unknown Topic tag '{t}'")

    traps_match = re.search(r"\*\*Traps[:：]\*\*\s*(.+)", text)
    if traps_match:
        traps = parse_markdown_tags(traps_match.group(1))
        if len(traps) > 2:
            result.add_warning(path, f"traps count {len(traps)} exceeds recommended max (2)")
        if check_tag_schema:
            for t in traps:
                if t not in valid_traps:
                    result.add_warning(path, f"unknown Trap tag '{t}'")

    level_match = re.search(r"\*\*難度[:：]\*\*\s*`?([^`\n]+)`?", text)
    if not level_match:
        _structural_issue(result, path, pool, "missing '**難度:**' field")
    else:
        level = level_match.group(1).strip()
        if level not in LEVEL_TAGS:
            _structural_issue(result, path, pool, f"invalid level '{level}'")


def iter_question_files(repo_root: Path, include_by_topic: bool) -> Iterable[Path]:
    for rel in QUESTION_POOLS:
        pool = repo_root / rel
        if pool.exists():
            yield from sorted(pool.glob("Q-*.md"))

    if include_by_topic:
        by_topic = repo_root / "question-bank" / "by-topic"
        if by_topic.exists():
            yield from sorted(by_topic.rglob("Q-*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint question markdown files.")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument(
        "--include-by-topic",
        action="store_true",
        help="also lint question-bank/by-topic (off by default)",
    )
    parser.add_argument(
        "--check-tag-schema",
        action="store_true",
        help="validate Topics/Traps against .github/skills/tagging-schema/references/tagging-schema.md",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    schema_path = (
        repo_root / ".github" / "skills" / "tagging-schema" / "references" / "tagging-schema.md"
    )

    valid_topics, valid_traps = load_valid_tags(schema_path)
    result = LintResult()

    files = list(iter_question_files(repo_root, include_by_topic=args.include_by_topic))
    if not files:
        print("No question files found.")
        return 1

    for path in files:
        check_file(path, valid_topics, valid_traps, result, check_tag_schema=args.check_tag_schema)

    for msg in result.errors:
        print(f"ERROR: {msg}")
    for msg in result.warnings:
        print(f"WARN: {msg}")

    print(
        f"\nLint summary: files={len(files)} errors={len(result.errors)} warnings={len(result.warnings)}"
    )

    if result.errors:
        return 1
    if args.strict and result.warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
