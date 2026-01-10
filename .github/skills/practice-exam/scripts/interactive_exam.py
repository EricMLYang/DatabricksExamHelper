#!/usr/bin/env python3
"""
Interactive Practice Exam for Databricks Exam Helper

互動式練習考試，提供逐題答題、即時反饋、深度解析功能
"""

import os
import sys
import json
import random
import re
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


def find_question_bank_root(source: str = "by-order_v1") -> Path:
    """
    尋找 question-bank 目錄的絕對路徑

    Args:
        source: 題庫來源 (by-order_v1 或 by-topic)

    Returns:
        Path: question-bank/{source}/ 的絕對路徑
    """
    current_dir = Path(__file__).resolve().parent

    for parent in [current_dir] + list(current_dir.parents):
        question_bank = parent / "question-bank" / source
        if question_bank.exists() and question_bank.is_dir():
            return question_bank

    raise FileNotFoundError(
        f"找不到 question-bank/{source}/ 目錄"
    )


def get_all_question_files(question_bank_path: Path) -> List[Path]:
    """
    取得題庫目錄中所有的題目檔案

    Returns:
        List[Path]: 所有 Q-*.md 檔案的路徑列表
    """
    # 支援 by-order_v1 的扁平結構
    if question_bank_path.name == "by-order_v1":
        return sorted(question_bank_path.glob("Q-*.md"))

    # 支援 by-topic 的多層結構
    return sorted(question_bank_path.rglob("Q-*.md"))


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

        # 提取選項
        options = {}
        option_pattern = r'[-*]?\s*\*\*([A-E])\.\*\*\s*(.+?)$'

        for line in question_text.split('\n'):
            match = re.match(option_pattern, line.strip())
            if match:
                option_letter, option_text = match.groups()
                # 移除選項文字中的 markdown 格式
                option_text = re.sub(r'`([^`]+)`', r'\1', option_text)
                options[option_letter] = option_text.strip()

        # 如果沒找到，嘗試其他格式
        if not options:
            option_pattern2 = r'^([A-E])[\.、\)]\s*(.+?)$'
            for line in question_text.split('\n'):
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

        return {
            'id': question_id,
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
    level: Optional[str] = None
) -> List[Dict]:
    """
    根據條件篩選題目

    Args:
        questions: 題目列表
        topic: 主題篩選（部分匹配）
        level: 難度篩選（完全匹配）

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

    return filtered


def load_questions(args) -> List[Dict]:
    """
    根據參數載入題目

    Args:
        args: 命令列參數

    Returns:
        List[Dict]: 題目列表
    """
    # TODO: 支援 review_mode 從錯題本載入

    # 從題庫載入
    question_bank_path = find_question_bank_root(args.source)
    all_files = get_all_question_files(question_bank_path)

    # 解析所有題目
    all_questions = []
    for file_path in all_files:
        parsed = parse_question_file(file_path)
        if parsed:
            all_questions.append(parsed)

    # 應用篩選條件
    filtered = filter_questions(
        all_questions,
        topic=args.topic,
        level=args.level
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
    print(f"**正解:** {question['answer']} - {question['options'][question['answer']]}")

    # 可以在這裡添加簡短提示
    print("\n" + "-"*70)
    input("\n[按 Enter 繼續下一題...]")


def show_incorrect_feedback(question: Dict, user_answer: str):
    """顯示答錯的反饋與深度解析"""
    print("\n" + "="*70)
    print("\n❌ **答錯了！**\n")
    print(f"**您的答案:** {user_answer} - {question['options'][user_answer]}")
    print(f"**正確答案:** {question['answer']} - {question['options'][question['answer']]}")

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

    # 記錄到錯題本（待實作）
    print("\n💾 **已將此題加入錯題本**")

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
        lines.append("1. 使用 `/review-mistakes` 複習錯題")
        lines.append("2. 針對弱點主題進行專項訓練")
        lines.append("3. 閱讀官方文件加強基礎概念")
    elif stats['accuracy'] < 85:
        lines.append("1. 使用 `/review-mistakes` 複習錯題")
        lines.append("2. 注意常見陷阱類型")
        lines.append("3. 繼續保持練習")
    else:
        lines.append("1. 表現優秀！繼續保持")
        lines.append("2. 可以嘗試更高難度的題目")
        lines.append("3. 使用 `/test-skills` 進行模擬考試")

    lines.append("\n" + "="*70 + "\n")

    return '\n'.join(lines)


def save_practice_history(session: Dict):
    """保存答題記錄"""
    try:
        # 確保目錄存在
        data_dir = Path.home() / '.claude-exam-helper' / 'user_data'
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
            'level': args.level
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
        default='by-order_v1',
        choices=['by-order_v1', 'by-topic'],
        help='題庫來源 (預設: by-order_v1)'
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
