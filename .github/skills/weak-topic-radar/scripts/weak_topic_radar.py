#!/usr/bin/env python3
"""
Generate weak-topic radar report from local learning data.

Data sources:
- ~/.claude-exam-helper/user_data/practice_history.json
- ~/.claude-exam-helper/user_data/mistakes.json
- question-bank/by-order_v1 (legacy 2024-2025)
- question-bank/by-order_b1..b4 (new 2025-2026)
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


PREFERRED_POOLS = ["by-order_b4", "by-order_b3", "by-order_b2", "by-order_b1", "by-order_v1"]


@dataclass
class QuestionMeta:
    question_id: str
    pool: str
    era: str  # "old" | "new"
    topics: list[str]
    traps: list[str]
    level: str | None


def normalize_qid(qid: str) -> str:
    qid = qid.strip()
    m = re.fullmatch(r"Q-\d{2}-(\d{3})", qid)
    if m:
        return f"Q-{m.group(1)}"
    return qid


def parse_tags(line: str) -> list[str]:
    tags = []
    for token in line.split("`"):
        token = token.strip()
        if not token or "," in token or token.startswith("**"):
            continue
        if token.startswith("[") or token.startswith("Tag"):
            continue
        tags.append(token)
    if tags:
        return tags
    return [p.strip() for p in line.split(",") if p.strip()]


def parse_question_meta(file_path: Path) -> QuestionMeta | None:
    text = file_path.read_text(encoding="utf-8")
    qid = file_path.stem
    for line in text.splitlines():
        if "**ID:" in line or "**ID：" in line:
            parts = line.split("`")
            if len(parts) >= 2:
                qid = parts[1].strip()
            break
    qid = normalize_qid(qid)

    topics = []
    traps = []
    level = None

    t_match = None
    for line in text.splitlines():
        if "**Topics:" in line or "**Topics：" in line:
            t_match = line
            break
    if t_match:
        topics = [t for t in parse_tags(t_match) if t and not t.startswith("Topics")]

    tr_match = None
    for line in text.splitlines():
        if "**Traps:" in line or "**Traps：" in line:
            tr_match = line
            break
    if tr_match:
        traps = [t for t in parse_tags(tr_match) if t and not t.startswith("Traps")]

    for line in text.splitlines():
        if "**難度:" in line or "**難度：" in line:
            if "`" in line:
                parts = line.split("`")
                if len(parts) >= 2:
                    level = parts[1].strip()
            else:
                level = line.split(":", 1)[-1].strip()
            break

    pool = file_path.parent.name
    era = "old" if pool == "by-order_v1" else "new"
    return QuestionMeta(
        question_id=qid,
        pool=pool,
        era=era,
        topics=topics,
        traps=traps,
        level=level,
    )


def load_question_bank(repo_root: Path) -> tuple[dict[str, QuestionMeta], int]:
    all_items: list[QuestionMeta] = []
    for pool in PREFERRED_POOLS:
        pool_dir = repo_root / "question-bank" / pool
        if not pool_dir.exists():
            continue
        for f in sorted(pool_dir.glob("Q-*.md")):
            meta = parse_question_meta(f)
            if meta:
                all_items.append(meta)

    grouped: dict[str, list[QuestionMeta]] = defaultdict(list)
    for item in all_items:
        grouped[item.question_id].append(item)

    preferred: dict[str, QuestionMeta] = {}
    ambiguous = 0
    for qid, metas in grouped.items():
        if len(metas) > 1:
            ambiguous += 1
        metas.sort(key=lambda m: PREFERRED_POOLS.index(m.pool))
        preferred[qid] = metas[0]

    return preferred, ambiguous


def parse_iso(ts: str) -> datetime | None:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        return None


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def resolve_user_data_dir() -> Path:
    preferred = Path.home() / ".claude-exam-helper" / "user_data"
    fallback = Path("/tmp/.claude-exam-helper/user_data")
    try:
        preferred.mkdir(parents=True, exist_ok=True)
        probe = preferred / ".write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return preferred
    except OSError:
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


def build_report(
    question_map: dict[str, QuestionMeta],
    ambiguous: int,
    history: dict,
    mistakes: dict,
    lookback_days: int,
    min_attempts: int,
) -> str:
    sessions = history.get("sessions", [])
    now = datetime.now()
    window_recent = now - timedelta(days=lookback_days)
    window_prev = now - timedelta(days=lookback_days * 2)

    total_attempts = 0
    total_correct = 0

    topic_attempts = defaultdict(int)
    topic_correct = defaultdict(int)
    trap_attempts = defaultdict(int)
    trap_wrong = defaultdict(int)
    era_attempts = defaultdict(int)
    era_correct = defaultdict(int)

    recent_attempts = recent_correct = 0
    prev_attempts = prev_correct = 0

    unresolved_qids = 0

    for sess in sessions:
        sess_ts = parse_iso(sess.get("timestamp", ""))
        results = sess.get("results", [])
        for r in results:
            qid = str(r.get("question_id", "")).strip()
            if not qid:
                continue
            correct = bool(r.get("correct", False))

            meta = question_map.get(qid)
            topics = r.get("topics") or (meta.topics if meta else [])
            traps = r.get("traps") or (meta.traps if meta else [])
            era = meta.era if meta else "unknown"

            if meta is None:
                unresolved_qids += 1

            total_attempts += 1
            total_correct += 1 if correct else 0
            era_attempts[era] += 1
            era_correct[era] += 1 if correct else 0

            for t in topics:
                topic_attempts[t] += 1
                topic_correct[t] += 1 if correct else 0

            for t in traps:
                trap_attempts[t] += 1
                if not correct:
                    trap_wrong[t] += 1

            if sess_ts:
                if sess_ts >= window_recent:
                    recent_attempts += 1
                    recent_correct += 1 if correct else 0
                elif window_prev <= sess_ts < window_recent:
                    prev_attempts += 1
                    prev_correct += 1 if correct else 0

    topic_rows = []
    for t, a in topic_attempts.items():
        if a < min_attempts:
            continue
        acc = (topic_correct[t] / a) * 100
        topic_rows.append((acc, a, t))
    topic_rows.sort(key=lambda x: (x[0], -x[1], x[2]))

    trap_rows = []
    for t, a in trap_attempts.items():
        if a < min_attempts:
            continue
        wrong_rate = (trap_wrong[t] / a) * 100
        trap_rows.append((wrong_rate, a, t))
    trap_rows.sort(key=lambda x: (-x[0], -x[1], x[2]))

    due_total = 0
    due_by_topic = defaultdict(int)
    for m in mistakes.get("mistakes", []):
        if m.get("mastered", False):
            continue
        due = False
        next_review = m.get("next_review_date")
        if not next_review:
            due = True
        else:
            next_dt = parse_iso(next_review)
            due = next_dt is None or next_dt <= now
        if due:
            due_total += 1
            for t in m.get("topics", []) or ["其他"]:
                due_by_topic[t] += 1

    overall_acc = (total_correct / total_attempts * 100) if total_attempts else 0.0
    recent_acc = (recent_correct / recent_attempts * 100) if recent_attempts else 0.0
    prev_acc = (prev_correct / prev_attempts * 100) if prev_attempts else 0.0
    trend = recent_acc - prev_acc if prev_attempts else 0.0

    lines = []
    lines.append("# Weak Topic Radar")
    lines.append("")
    lines.append(f"- 產生時間: {now.strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"- 歷史 Session 數: {len(sessions)}")
    lines.append(f"- 作答總數: {total_attempts}")
    lines.append(f"- 整體正確率: {overall_acc:.1f}%")
    lines.append(f"- 題庫映射歧義 QID 數: {ambiguous}")
    lines.append(f"- 歷史中未映射題號數: {unresolved_qids}")
    lines.append("")

    lines.append("## 題池表現（舊題/新題）")
    lines.append("")
    lines.append("| 題池 | 作答數 | 正確率 |")
    lines.append("|---|---:|---:|")
    for era in ("new", "old", "unknown"):
        a = era_attempts.get(era, 0)
        if a == 0:
            continue
        acc = era_correct[era] / a * 100
        label = {"new": "2025-2026 新題型 (b1-b4)", "old": "2024-2025 舊題型 (v1)", "unknown": "未知"}[era]
        lines.append(f"| {label} | {a} | {acc:.1f}% |")
    lines.append("")

    lines.append(f"## 弱點主題（至少 {min_attempts} 題）")
    lines.append("")
    lines.append("| Topic | 作答數 | 正確率 |")
    lines.append("|---|---:|---:|")
    if topic_rows:
        for acc, attempts, topic in topic_rows[:12]:
            lines.append(f"| {topic} | {attempts} | {acc:.1f}% |")
    else:
        lines.append("| (資料不足) | 0 | 0.0% |")
    lines.append("")

    lines.append(f"## 陷阱雷達（至少 {min_attempts} 題）")
    lines.append("")
    lines.append("| Trap | 出現數 | 誤選率 |")
    lines.append("|---|---:|---:|")
    if trap_rows:
        for wrong_rate, attempts, trap in trap_rows[:12]:
            lines.append(f"| {trap} | {attempts} | {wrong_rate:.1f}% |")
    else:
        lines.append("| (資料不足) | 0 | 0.0% |")
    lines.append("")

    lines.append("## 間隔複習（Due）")
    lines.append("")
    lines.append(f"- 目前到期題數: **{due_total}**")
    if due_by_topic:
        lines.append("- 到期最多主題:")
        for topic, cnt in sorted(due_by_topic.items(), key=lambda x: x[1], reverse=True)[:5]:
            lines.append(f"  - {topic}: {cnt}")
    lines.append("")

    lines.append(f"## {lookback_days} 天趨勢")
    lines.append("")
    lines.append(f"- 近 {lookback_days} 天正確率: {recent_acc:.1f}% ({recent_attempts} 題)")
    lines.append(f"- 前 {lookback_days} 天正確率: {prev_acc:.1f}% ({prev_attempts} 題)")
    lines.append(f"- 變化: {trend:+.1f} 個百分點")
    lines.append("")

    lines.append("## 建議行動")
    lines.append("")
    if topic_rows:
        weak = topic_rows[0][2]
        lines.append(f"1. 下次練習先跑 `{weak}` 主題：`--topic {weak}`。")
    else:
        lines.append("1. 先累積至少 3 次同主題作答，再啟用弱點聚焦。")
    lines.append("2. 優先清完到期複習題（review-mode + spaced review）。")
    lines.append("3. 每週至少一次用新題池（b1-b4）做 20 題限時模擬。")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate weak-topic radar markdown report.")
    parser.add_argument(
        "--output",
        default="docs/reports/weak-topic-radar.md",
        help="output markdown path",
    )
    parser.add_argument("--lookback-days", type=int, default=7, help="trend window in days")
    parser.add_argument("--min-attempts", type=int, default=3, help="minimum attempts per topic/trap")
    parser.add_argument("--print", dest="print_stdout", action="store_true", help="print report to stdout")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    user_data = resolve_user_data_dir()
    history_path = user_data / "practice_history.json"
    mistakes_path = user_data / "mistakes.json"

    qmap, ambiguous = load_question_bank(repo_root)
    history = load_json(history_path)
    mistakes = load_json(mistakes_path)

    report = build_report(
        qmap,
        ambiguous,
        history,
        mistakes,
        lookback_days=args.lookback_days,
        min_attempts=args.min_attempts,
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report + "\n", encoding="utf-8")

    if args.print_stdout:
        print(report)
    else:
        print(f"Report written to: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
