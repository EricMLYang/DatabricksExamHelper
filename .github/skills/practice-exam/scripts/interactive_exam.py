#!/usr/bin/env python3
"""
Interactive Practice Exam for Databricks Exam Helper

互動式練習考試，提供逐題答題、即時反饋、深度解析功能
"""

import sys
import json
import random
import re
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Optional integration with review-mistakes skill.
REVIEW_SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "review-mistakes" / "scripts"
if REVIEW_SCRIPTS_DIR.exists():
    sys.path.insert(0, str(REVIEW_SCRIPTS_DIR))

try:
    from mistake_tracker import add_mistake, get_not_mastered_items
except Exception:
    add_mistake = None
    get_not_mastered_items = None

# Optional integration with profile_manager for study-phase display.
try:
    from profile_manager import display_study_phase_summary
except Exception:
    display_study_phase_summary = None

SOURCE_CHOICES = [
    "by-order_b4",
    "by-order_b3",
    "by-order_b2",
    "by-order_b1",
    "by-order_v1",
    "by-topic",
]

SOURCE_PRIORITY = {name: i for i, name in enumerate(SOURCE_CHOICES)}


def qid_candidates(qid: str) -> List[str]:
    """兼容舊格式題號（例如 Q-01-023 -> Q-023）。"""
    out = [qid]
    m = re.fullmatch(r"Q-\d{2}-(\d{3})", qid)
    if m:
        out.append(f"Q-{m.group(1)}")
    return out


def find_repo_root() -> Path:
    """尋找包含 question-bank 的專案根目錄。"""
    current_dir = Path(__file__).resolve().parent
    for parent in [current_dir] + list(current_dir.parents):
        if (parent / "question-bank").exists():
            return parent
    raise FileNotFoundError("找不到 question-bank 目錄")


def get_all_question_files(repo_root: Path, source: str) -> List[Path]:
    """
    依來源取得所有題目檔案。

    Args:
        repo_root: 專案根目錄
        source: 題庫來源
    """
    base = repo_root / "question-bank"
    source_dir = base / source
    if not source_dir.exists():
        raise FileNotFoundError(f"找不到 question-bank/{source}/ 目錄")

    if source == "by-topic":
        return sorted(source_dir.rglob("Q-*.md"))
    return sorted(source_dir.glob("Q-*.md"))


def get_review_fallback_files(repo_root: Path) -> List[Path]:
    """review-mode 會跨題池查找：新題優先，找不到再回退舊題。"""
    files: List[Path] = []
    for source in ("by-order_b4", "by-order_b3", "by-order_b2", "by-order_b1", "by-order_v1"):
        try:
            files.extend(get_all_question_files(repo_root, source))
        except FileNotFoundError:
            continue
    return files


def parse_question_file(file_path: Path) -> Optional[Dict]:
    """
    解析單一題目檔案

    Returns:
        Dict: 包含題目資訊的字典
            {
                'id': 'Q-001',
                'question': '題目內容',
                'options': {'A': '...', 'B': '...', 'C': '...', 'D': '...'},
                'answer': 'B',
                'topics': ['Delta-Lake', ...],
                'traps': ['Unit-Confusion', ...],
                'level': 'L2-Intermediate',
                'file_path': Path
            }
    """
    try:
        content = file_path.read_text(encoding='utf-8')

        # 提取題目 ID
        question_id = file_path.stem

        # 提取題幹（在 ## 題目內容 或 ### 題幹 之後）
        question_match = re.search(
            r'###? 題幹\s*\n(.*?)(?=\n###?|---|\Z)',
            content,
            re.DOTALL
        )

        if not question_match:
            # 嘗試使用 ## 題目
            question_match = re.search(
                r'## 題目\s*\n(.*?)(?=\n##|\Z)',
                content,
                re.DOTALL
            )

        if not question_match:
            return None

        question_text = question_match.group(1).strip()

        # 提取選項（掃描整份檔案，不只題幹區塊）
        options = {}
        option_pattern = r'[-*]?\s*\*\*([A-E])\.\*\*\s*(.+?)$'

        for line in content.split('\n'):
            match = re.match(option_pattern, line.strip())
            if match:
                option_letter, option_text = match.groups()
                # 移除選項文字中的 markdown 格式
                option_text = re.sub(r'`([^`]+)`', r'\1', option_text)
                options[option_letter] = option_text.strip()

        # 如果沒找到，嘗試其他格式
        if not options:
            option_pattern2 = r'^([A-E])[\.、\)]\s*(.+?)$'
            for line in content.split('\n'):
                match = re.match(option_pattern2, line.strip())
                if match:
                    option_letter, option_text = match.groups()
                    option_text = re.sub(r'`([^`]+)`', r'\1', option_text)
                    options[option_letter] = option_text.strip()

        # 提取題幹（移除選項部分）
        question_lines = []
        for line in question_text.split('\n'):
            if not re.match(r'[-*]?\s*\*\*[A-E]\.\*\*', line.strip()) and \
               not re.match(r'^[A-E][\.、\)]', line.strip()):
                question_lines.append(line)
        question_stem = '\n'.join(question_lines).strip()

        # 提取正確答案
        answer_match = re.search(
            r'\*\*正解[:：]\*\*\s*`?([A-E])`?',
            content,
            re.IGNORECASE
        )
        answer = answer_match.group(1) if answer_match else None

        if not answer:
            return None

        # 提取標籤
        topics = []
        topics_match = re.search(r'\*\*Topics[:：]\*\*\s*(.+)', content)
        if topics_match:
            topics_str = topics_match.group(1)
            topics = [t.strip('`').strip() for t in re.findall(r'`([^`]+)`', topics_str)]

        traps = []
        traps_match = re.search(r'\*\*Traps[:：]\*\*\s*(.+)', content)
        if traps_match:
            traps_str = traps_match.group(1)
            traps = [t.strip('`').strip() for t in re.findall(r'`([^`]+)`', traps_str)]

        level = None
        level_match = re.search(r'\*\*難度[:：]\*\*\s*`?([^`\n]+)`?', content)
        if level_match:
            level = level_match.group(1).strip()

        batch_name = file_path.parent.name
        if batch_name == 'by-order_v1':
            era = 'old'
        elif batch_name.startswith('by-order_b'):
            era = 'new'
        else:
            era = 'mixed'

        return {
            'id': question_id,
            'batch': batch_name,
            'era': era,
            'question': question_stem,
            'options': options,
            'answer': answer,
            'topics': topics,
            'traps': traps,
            'level': level,
            'file_path': file_path
        }

    except Exception as e:
        print(f"⚠️ 解析檔案 {file_path.name} 時發生錯誤: {e}")
        return None


def filter_questions(
    questions: List[Dict],
    topic: Optional[str] = None,
    level: Optional[str] = None,
    era: str = "all",
) -> List[Dict]:
    """
    根據條件篩選題目

    Args:
        questions: 題目列表
        topic: 主題篩選（部分匹配）
        level: 難度篩選（完全匹配）
        era: 題型時代篩選（old/new/all）

    Returns:
        List[Dict]: 符合條件的題目列表
    """
    filtered = questions

    if topic:
        filtered = [
            q for q in filtered
            if any(topic.lower() in t.lower() for t in q.get('topics', []))
        ]

    if level:
        filtered = [
            q for q in filtered
            if q.get('level', '').lower() == level.lower()
        ]

    if era in {"old", "new"}:
        filtered = [q for q in filtered if q.get('era') == era]

    return filtered


def load_questions(args) -> List[Dict]:
    """
    根據參數載入題目

    Args:
        args: 命令列參數

    Returns:
        List[Dict]: 題目列表
    """
    repo_root = find_repo_root()
    all_files = get_all_question_files(repo_root, args.source)

    all_questions = []
    for file_path in all_files:
        parsed = parse_question_file(file_path)
        if parsed:
            all_questions.append(parsed)

    # 錯題複習模式：先取到期題，再回退未精通題。
    if args.review_mode:
        if get_not_mastered_items is None:
            print("⚠️ 找不到錯題本模組，改用一般題庫模式")
        else:
            review_items = get_not_mastered_items(topic=args.topic, due_only=True)
            if not review_items:
                print("ℹ️ 目前沒有到期題，改抽未精通題目")
                review_items = get_not_mastered_items(topic=args.topic, due_only=False)
            if not review_items:
                print("⚠️ 錯題本中沒有符合條件的未精通題目")
                return []

            # 以「目前 source + 全題池回退」組合索引題目，避免 source 不同導致找不到題。
            fallback_questions = list(all_questions)
            fallback_files = get_review_fallback_files(repo_root)
            for file_path in fallback_files:
                parsed = parse_question_file(file_path)
                if parsed:
                    fallback_questions.append(parsed)

            by_id = {}
            for q in fallback_questions:
                curr = by_id.get(q['id'])
                if curr is None:
                    by_id[q['id']] = q
                    continue
                # 新題池優先（b4 > b3 > b2 > b1 > v1）
                curr_rank = SOURCE_PRIORITY.get(curr.get('batch', ''), 999)
                new_rank = SOURCE_PRIORITY.get(q.get('batch', ''), 999)
                if new_rank < curr_rank:
                    by_id[q['id']] = q

            filtered_review = []
            missing = 0
            for item in review_items:
                q = None
                for candidate in qid_candidates(str(item.get('question_id', '')).strip()):
                    q = by_id.get(candidate)
                    if q:
                        break
                if not q:
                    missing += 1
                    continue
                filtered_review.append(q)
            if missing:
                print(f"⚠️ 有 {missing} 題錯題在題庫中找不到對應檔案")

            if args.level:
                filtered_review = [
                    q for q in filtered_review
                    if q.get('level', '').lower() == args.level.lower()
                ]
            if args.era in {"old", "new"}:
                filtered_review = [q for q in filtered_review if q.get('era') == args.era]

            if not filtered_review:
                print("⚠️ 錯題本有記錄，但經過篩選後沒有可練習題目")
                return []

            if args.seed is not None:
                random.seed(args.seed)
                random.shuffle(filtered_review)

            return filtered_review[:min(args.count, len(filtered_review))]

    # 一般模式：應用主題/難度/時代篩選
    filtered = filter_questions(
        all_questions,
        topic=args.topic,
        level=args.level,
        era=args.era,
    )

    if not filtered:
        print(f"⚠️ 警告: 沒有找到符合條件的題目")
        return []

    # 隨機挑選
    if args.seed is not None:
        random.seed(args.seed)

    count = min(args.count, len(filtered))
    selected = random.sample(filtered, count)

    return selected


def display_question(num: int, total: int, question: Dict):
    """顯示題目"""
    print("\n" + "="*70)
    print(f"\n## 第 {num}/{total} 題\n")
    print(f"**題目 ID:** {question['id']}")
    print(f"**題庫來源:** {question.get('batch', 'unknown')}")
    if question.get('era') in {"old", "new"}:
        label = "舊題 (2024-2025)" if question['era'] == "old" else "新題 (2025-2026)"
        print(f"**題型時代:** {label}")

    if question.get('topics'):
        print(f"**主題:** {', '.join(question['topics'])}")

    if question.get('level'):
        print(f"**難度:** {question['level']}")

    print("\n" + "-"*70)
    print(f"\n{question['question']}\n")

    # 顯示選項
    for letter in sorted(question['options'].keys()):
        print(f"  {letter}. {question['options'][letter]}")

    print()


def get_user_input() -> str:
    """取得使用者輸入的答案"""
    while True:
        answer = input("請輸入您的答案 (A/B/C/D/E): ").strip().upper()
        if answer in ['A', 'B', 'C', 'D', 'E']:
            return answer
        print("⚠️ 請輸入有效的選項 (A/B/C/D/E)")


def show_correct_feedback(question: Dict):
    """顯示答對的反饋"""
    print("\n" + "="*70)
    print("\n✅ **正確！**\n")
    answer_text = question['options'].get(question['answer'], '(選項內容省略)')
    print(f"**正解:** {question['answer']} - {answer_text}")

    # 可以在這裡添加簡短提示
    print("\n" + "-"*70)
    input("\n[按 Enter 繼續下一題...]")


def show_incorrect_feedback(question: Dict, user_answer: str):
    """顯示答錯的反饋與深度解析"""
    print("\n" + "="*70)
    print("\n❌ **答錯了！**\n")
    user_text = question['options'].get(user_answer, '(選項內容省略)')
    answer_text = question['options'].get(question['answer'], '(選項內容省略)')
    print(f"**您的答案:** {user_answer} - {user_text}")
    print(f"**正確答案:** {question['answer']} - {answer_text}")

    # 顯示簡化的錯誤分析
    print("\n" + "-"*70)
    print("\n## 🔍 為什麼答錯了？\n")

    # 顯示陷阱標籤（如果有）
    if question.get('traps'):
        print(f"**陷阱類型:** {', '.join(question['traps'])}")
        print()

    # 提示查看完整解析
    print(f"💡 **提示:** 可查看完整解析了解詳細說明")
    print(f"   檔案位置: {question['file_path']}")

    print("\n" + "-"*70)
    input("\n[按 Enter 繼續下一題...]")


def check_answer(question: Dict, user_answer: str) -> Dict:
    """
    檢查答案正確性

    Returns:
        結果字典
    """
    correct = (user_answer == question['answer'])

    return {
        'correct': correct,
        'user_answer': user_answer,
        'correct_answer': question['answer'],
        'question_id': question['id'],
        'question_batch': question.get('batch'),
        'era': question.get('era'),
        'topics': question.get('topics', []),
        'traps': question.get('traps', [])
    }


def analyze_results(results: List[Dict]) -> Dict:
    """
    分析答題結果

    Returns:
        統計結果
    """
    total = len(results)
    correct_count = sum(1 for r in results if r['correct'])
    accuracy = (correct_count / total * 100) if total > 0 else 0

    # 分析答錯的主題
    wrong_topics = {}
    for r in results:
        if not r['correct']:
            for topic in r['topics']:
                wrong_topics[topic] = wrong_topics.get(topic, 0) + 1

    # 分析常踩的陷阱
    common_traps = {}
    for r in results:
        if not r['correct']:
            for trap in r['traps']:
                common_traps[trap] = common_traps.get(trap, 0) + 1

    return {
        'total': total,
        'correct': correct_count,
        'wrong': total - correct_count,
        'accuracy': accuracy,
        'wrong_topics': dict(sorted(wrong_topics.items(), key=lambda x: x[1], reverse=True)),
        'common_traps': dict(sorted(common_traps.items(), key=lambda x: x[1], reverse=True))
    }


def generate_report(session: Dict) -> str:
    """生成成績報告"""
    stats = analyze_results(session['results'])

    lines = []
    lines.append("\n" + "="*70)
    lines.append("\n# 📊 練習成績報告\n")
    lines.append(f"**完成時間:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**總題數:** {stats['total']} 題")
    lines.append(f"**答對:** {stats['correct']} 題")
    lines.append(f"**答錯:** {stats['wrong']} 題")
    lines.append(f"**準確率:** {stats['accuracy']:.1f}%")
    lines.append("\n" + "-"*70)

    # 詳細結果表格
    lines.append("\n## 詳細結果\n")
    lines.append("| 題號 | 題目 ID | 您的答案 | 正確答案 | 結果 |")
    lines.append("|------|---------|----------|----------|------|")

    for idx, r in enumerate(session['results'], 1):
        result_icon = "✅" if r['correct'] else "❌"
        lines.append(
            f"| {idx} | {r['question_id']} | {r['user_answer']} | "
            f"{r['correct_answer']} | {result_icon} |"
        )

    # 弱點分析
    if stats['wrong_topics']:
        lines.append("\n" + "-"*70)
        lines.append("\n## 🎯 需加強主題\n")
        for topic, count in list(stats['wrong_topics'].items())[:3]:
            lines.append(f"- **{topic}** (答錯 {count} 題)")

    if stats['common_traps']:
        lines.append("\n## ⚠️ 常踩陷阱\n")
        for trap, count in list(stats['common_traps'].items())[:3]:
            lines.append(f"- `{trap}` (出現 {count} 次)")

    # 建議
    lines.append("\n" + "-"*70)
    lines.append("\n## 💡 下一步建議\n")

    if stats['accuracy'] < 70:
        lines.append("1. 使用 `--review-mode` 先清到期錯題")
        lines.append("2. 針對弱點主題進行專項訓練")
        lines.append("3. 閱讀官方文件加強基礎概念")
    elif stats['accuracy'] < 85:
        lines.append("1. 使用 `--review-mode` 複習錯題")
        lines.append("2. 注意常見陷阱類型")
        lines.append("3. 繼續保持練習")
    else:
        lines.append("1. 表現優秀！繼續保持")
        lines.append("2. 可以嘗試更高難度的題目")
        lines.append("3. 使用 `/practice-exam --count 20 --seed 42` 進行模擬考試")

    lines.append("\n" + "="*70 + "\n")

    return '\n'.join(lines)


def save_practice_history(session: Dict):
    """保存答題記錄"""
    try:
        # 確保目錄存在；若家目錄不可寫則回退至 /tmp
        data_dir = Path.home() / '.claude-exam-helper' / 'user_data'
        try:
            data_dir.mkdir(parents=True, exist_ok=True)
            probe = data_dir / '.write_probe'
            probe.write_text('ok', encoding='utf-8')
            probe.unlink(missing_ok=True)
        except OSError:
            data_dir = Path('/tmp/.claude-exam-helper/user_data')
            data_dir.mkdir(parents=True, exist_ok=True)

        history_file = data_dir / 'practice_history.json'

        # 讀取現有記錄
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = {'sessions': []}

        # 添加新記錄
        stats = analyze_results(session['results'])
        history['sessions'].append({
            'timestamp': session['start_time'].isoformat(),
            'mode': session.get('mode', 'general'),
            'filters': session.get('filters', {}),
            'results': session['results'],
            'accuracy': stats['accuracy'],
            'total': stats['total'],
            'correct': stats['correct']
        })

        # 寫回檔案
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

        print(f"\n💾 **答題記錄已保存:** {history_file}")

    except Exception as e:
        print(f"\n⚠️ 保存答題記錄時發生錯誤: {e}")


def start_practice_exam(args):
    """啟動互動式練習考試"""

    # Show study-phase summary when available.
    if display_study_phase_summary is not None:
        try:
            print()
            display_study_phase_summary()
        except Exception:
            pass  # Non-critical; skip silently.

    print("\n" + "="*70)
    print("\n# 📝 Databricks 練習考試\n")
    print(f"**模式:** {'錯題複習' if args.review_mode else '一般練習'}")

    # 載入題目
    print("\n正在載入題目...")
    questions = load_questions(args)

    if not questions:
        print("\n❌ 沒有可用的題目")
        return

    print(f"**題目數量:** {len(questions)} 題")
    print(f"**題庫來源:** {args.source}")
    if args.era in {"old", "new"}:
        era_label = "舊題 (2024-2025)" if args.era == "old" else "新題 (2025-2026)"
        print(f"**題型篩選:** {era_label}")

    if args.topic:
        print(f"**主題篩選:** {args.topic}")
    if args.level:
        print(f"**難度篩選:** {args.level}")

    input("\n[按 Enter 開始答題...]")

    # 初始化答題記錄
    session = {
        'start_time': datetime.now(),
        'mode': 'review' if args.review_mode else 'general',
        'filters': {
            'topic': args.topic,
            'level': args.level,
            'era': args.era,
            'source': args.source,
        },
        'results': []
    }

    # 答題循環
    for i, question in enumerate(questions, 1):
        # 顯示題目
        display_question(i, len(questions), question)

        # 取得答案
        user_answer = get_user_input()

        # 檢查答案
        result = check_answer(question, user_answer)
        session['results'].append(result)

        # 顯示反饋
        if result['correct']:
            show_correct_feedback(question)
        else:
            if add_mistake is not None:
                try:
                    add_mistake(
                        question_id=question['id'],
                        user_answer=user_answer,
                        correct_answer=question['answer'],
                        topics=question.get('topics', []),
                        traps=question.get('traps', []),
                        level=question.get('level'),
                        question_batch=question.get('batch'),
                    )
                except Exception as e:
                    print(f"\n⚠️ 寫入錯題本失敗，將略過記錄：{e}")
            else:
                print("\n⚠️ 無法寫入錯題本（mistake_tracker 不可用）")
            show_incorrect_feedback(question, user_answer)

    # 生成成績報告
    report = generate_report(session)
    print(report)

    # 保存答題記錄
    save_practice_history(session)


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='互動式練習考試 - Databricks Exam Helper'
    )

    parser.add_argument(
        '--count',
        type=int,
        default=10,
        help='題目數量 (預設: 10)'
    )

    parser.add_argument(
        '--topic',
        type=str,
        help='主題篩選 (例如: Delta-Lake)'
    )

    parser.add_argument(
        '--level',
        type=str,
        choices=['L1-Basic', 'L2-Intermediate', 'L3-Advanced'],
        help='難度篩選'
    )

    parser.add_argument(
        '--source',
        type=str,
        default='by-order_b4',
        choices=SOURCE_CHOICES,
        help='題庫來源 (預設: by-order_b4, 建議新題池)'
    )

    parser.add_argument(
        '--era',
        type=str,
        default='all',
        choices=['all', 'new', 'old'],
        help='題型時代篩選：new=2025-2026(b1-b4), old=2024-2025(v1)'
    )

    parser.add_argument(
        '--seed',
        type=int,
        help='隨機種子（用於可重現的結果）'
    )

    parser.add_argument(
        '--review-mode',
        action='store_true',
        help='錯題複習模式（從錯題本載入）'
    )

    args = parser.parse_args()

    try:
        start_practice_exam(args)
    except KeyboardInterrupt:
        print("\n\n⚠️ 練習已中斷")
        return 1
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
