#!/usr/bin/env python3
"""
Mistake Tracker for Databricks Exam Helper

錯題本管理系統，追蹤、分析、複習答錯的題目
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from collections import defaultdict


def get_mistakes_db_path() -> Path:
    """取得錯題本資料庫路徑"""
    data_dir = Path.home() / '.claude-exam-helper' / 'user_data'
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / 'mistakes.json'


def load_mistakes_db() -> Dict:
    """載入錯題本資料庫"""
    db_path = get_mistakes_db_path()

    if db_path.exists():
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ 錯題本檔案損壞，建立新的錯題本")
            return create_empty_db()
    else:
        return create_empty_db()


def create_empty_db() -> Dict:
    """建立空的錯題本資料庫"""
    return {
        'version': '1.0',
        'created_date': datetime.now().isoformat(),
        'last_updated': datetime.now().isoformat(),
        'mistakes': [],
        'statistics': {
            'total_mistakes': 0,
            'mastered': 0,
            'not_mastered': 0,
            'topics': {},
            'traps': {}
        }
    }


def save_mistakes_db(db: Dict):
    """保存錯題本資料庫"""
    db['last_updated'] = datetime.now().isoformat()

    # 更新統計資料
    update_statistics(db)

    db_path = get_mistakes_db_path()

    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)


def update_statistics(db: Dict):
    """更新統計資料"""
    mistakes = db['mistakes']

    total = len(mistakes)
    mastered = sum(1 for m in mistakes if m.get('mastered', False))
    not_mastered = total - mastered

    # 主題統計
    topic_stats = defaultdict(int)
    for m in mistakes:
        if not m.get('mastered', False):
            for topic in m.get('topics', []):
                topic_stats[topic] += 1

    # 陷阱統計
    trap_stats = defaultdict(int)
    for m in mistakes:
        if not m.get('mastered', False):
            for trap in m.get('traps', []):
                trap_stats[trap] += 1

    db['statistics'] = {
        'total_mistakes': total,
        'mastered': mastered,
        'not_mastered': not_mastered,
        'topics': dict(topic_stats),
        'traps': dict(trap_stats)
    }


def find_mistake(db: Dict, question_id: str) -> Optional[Dict]:
    """查找錯題記錄"""
    for mistake in db['mistakes']:
        if mistake['question_id'] == question_id:
            return mistake
    return None


def add_mistake(
    question_id: str,
    user_answer: str,
    correct_answer: str,
    topics: List[str] = None,
    traps: List[str] = None,
    level: str = None
):
    """
    添加或更新錯題記錄

    Args:
        question_id: 題目 ID
        user_answer: 使用者答案
        correct_answer: 正確答案
        topics: 主題標籤
        traps: 陷阱標籤
        level: 難度等級
    """
    db = load_mistakes_db()
    mistake = find_mistake(db, question_id)

    is_correct = (user_answer == correct_answer)

    attempt = {
        'date': datetime.now().isoformat(),
        'user_answer': user_answer,
        'correct_answer': correct_answer,
        'correct': is_correct
    }

    if mistake:
        # 更新現有記錄
        mistake['attempts'].append(attempt)

        if is_correct:
            mistake['correct_count'] = mistake.get('correct_count', 0) + 1
            mistake['consecutive_correct'] = mistake.get('consecutive_correct', 0) + 1

            # 連續答對 3 次標記為已精通
            if mistake['consecutive_correct'] >= 3:
                mistake['mastered'] = True
                mistake['mastered_date'] = datetime.now().isoformat()
                print(f"\n🎉 恭喜！{question_id} 已精通！")
        else:
            mistake['wrong_count'] = mistake.get('wrong_count', 0) + 1
            mistake['consecutive_correct'] = 0
    else:
        # 新增記錄
        db['mistakes'].append({
            'question_id': question_id,
            'first_wrong_date': datetime.now().isoformat(),
            'attempts': [attempt],
            'wrong_count': 0 if is_correct else 1,
            'correct_count': 1 if is_correct else 0,
            'consecutive_correct': 1 if is_correct else 0,
            'mastered': False,
            'mastered_date': None,
            'topics': topics or [],
            'traps': traps or [],
            'level': level or '',
            'notes': ''
        })

    save_mistakes_db(db)

    if not is_correct:
        print(f"💾 已將 {question_id} 加入錯題本")


def show_statistics():
    """顯示錯題統計"""
    db = load_mistakes_db()
    stats = db['statistics']

    print("\n" + "="*70)
    print("\n# 📊 您的錯題統計報告\n")
    print(f"**統計時間:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"**總錯題數:** {stats['total_mistakes']} 題")
    print(f"**未精通:** {stats['not_mastered']} 題")
    print(f"**已精通:** {stats['mastered']} 題")

    print("\n" + "-"*70)

    # 主題統計
    if stats['topics']:
        print("\n## 🔴 最常錯的主題\n")
        print("| 主題 | 錯題數 |")
        print("|------|--------|")

        sorted_topics = sorted(
            stats['topics'].items(),
            key=lambda x: x[1],
            reverse=True
        )

        for topic, count in sorted_topics[:5]:
            print(f"| {topic} | {count} 題 |")

    # 陷阱統計
    if stats['traps']:
        print("\n## ⚠️ 最常踩的陷阱\n")
        print("| 陷阱類型 | 出現次數 |")
        print("|---------|---------|")

        sorted_traps = sorted(
            stats['traps'].items(),
            key=lambda x: x[1],
            reverse=True
        )

        for trap, count in sorted_traps[:5]:
            print(f"| `{trap}` | {count} 次 |")

    # 建議
    print("\n" + "-"*70)
    print("\n## 💡 建議\n")

    if stats['not_mastered'] > 0:
        if stats['topics']:
            top_topic = max(stats['topics'].items(), key=lambda x: x[1])[0]
            print(f"1. **優先複習:** {top_topic} 主題（錯題最多）")

        if stats['traps']:
            top_trap = max(stats['traps'].items(), key=lambda x: x[1])[0]
            print(f"2. **注意陷阱:** 特別留意 {top_trap} 類型的題目")

        print(f"3. **複習頻率:** 建議每 2-3 天複習一次錯題")
        print("\n使用以下指令開始錯題複習：")
        print("python .github/skills/practice-exam/scripts/interactive_exam.py --review-mode")
    else:
        print("🎉 太棒了！目前沒有需要複習的錯題")
        print("   繼續保持，可以嘗試更高難度的題目")

    print("\n" + "="*70 + "\n")


def list_mistakes(topic: Optional[str] = None, include_mastered: bool = False):
    """列出錯題清單"""
    db = load_mistakes_db()
    mistakes = db['mistakes']

    # 篩選
    filtered = mistakes
    if not include_mastered:
        filtered = [m for m in filtered if not m.get('mastered', False)]

    if topic:
        filtered = [
            m for m in filtered
            if any(topic.lower() in t.lower() for t in m.get('topics', []))
        ]

    if not filtered:
        print("\n🎉 太棒了！沒有符合條件的錯題")
        return

    # 按主題分組
    grouped = defaultdict(list)
    for mistake in filtered:
        topics = mistake.get('topics', ['其他'])
        primary_topic = topics[0] if topics else '其他'
        grouped[primary_topic].append(mistake)

    # 顯示
    print("\n" + "="*70)
    print("\n# 📝 錯題清單\n")
    print(f"**未精通題目:** {len(filtered)} 題")

    if include_mastered:
        mastered_count = sum(1 for m in mistakes if m.get('mastered', False))
        print(f"**已精通題目:** {mastered_count} 題")

    print("\n" + "-"*70)

    for topic_name, topic_mistakes in sorted(grouped.items()):
        print(f"\n### {topic_name} ({len(topic_mistakes)} 題)\n")
        print("| 題目 ID | 錯誤次數 | 連續答對 | 狀態 |")
        print("|---------|---------|---------|------|")

        # 按錯誤次數排序
        topic_mistakes.sort(key=lambda x: x.get('wrong_count', 0), reverse=True)

        for m in topic_mistakes:
            wrong_count = m.get('wrong_count', 0)
            consecutive = m.get('consecutive_correct', 0)

            # 狀態判定
            if wrong_count >= 3 and consecutive < 2:
                status = "🔴 需加強"
            elif consecutive == 2:
                status = "🟢 接近精通"
            elif consecutive == 1:
                status = "🟡 練習中"
            else:
                status = "⚪ 新錯題"

            print(f"| {m['question_id']} | {wrong_count} 次 | {consecutive} 次 | {status} |")

    print("\n" + "="*70 + "\n")


def mark_as_mastered(question_id: str):
    """手動標記題目為已精通"""
    db = load_mistakes_db()
    mistake = find_mistake(db, question_id)

    if mistake:
        if mistake.get('mastered', False):
            print(f"⚠️ {question_id} 已經是「已精通」狀態")
        else:
            mistake['mastered'] = True
            mistake['mastered_date'] = datetime.now().isoformat()
            save_mistakes_db(db)
            print(f"✅ {question_id} 已標記為「已精通」")
    else:
        print(f"⚠️ 找不到題目: {question_id}")


def clear_mastered():
    """清除已精通的題目"""
    db = load_mistakes_db()

    mastered_count = sum(1 for m in db['mistakes'] if m.get('mastered', False))

    if mastered_count == 0:
        print("⚠️ 沒有已精通的題目可以清除")
        return

    # 確認
    print(f"\n⚠️ 即將清除 {mastered_count} 題已精通的題目")
    confirm = input("確定要繼續嗎？(y/N): ").strip().lower()

    if confirm == 'y':
        db['mistakes'] = [m for m in db['mistakes'] if not m.get('mastered', False)]
        save_mistakes_db(db)
        print(f"✅ 已清除 {mastered_count} 題已精通的題目")
    else:
        print("❌ 已取消")


def export_mistakes(output_file: str):
    """匯出錯題本"""
    db = load_mistakes_db()

    output_path = Path(output_file)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

    print(f"✅ 錯題本已匯出至: {output_path}")


def import_mistakes(input_file: str):
    """匯入錯題本"""
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"❌ 找不到檔案: {input_file}")
        return

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            imported_db = json.load(f)

        # 驗證格式
        if 'mistakes' not in imported_db:
            print("❌ 檔案格式錯誤：缺少 'mistakes' 欄位")
            return

        # 確認
        count = len(imported_db['mistakes'])
        print(f"\n⚠️ 即將匯入 {count} 題錯題記錄")
        print("⚠️ 這將覆蓋現有的錯題本")
        confirm = input("確定要繼續嗎？(y/N): ").strip().lower()

        if confirm == 'y':
            db_path = get_mistakes_db_path()
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(imported_db, f, indent=2, ensure_ascii=False)

            print(f"✅ 已成功匯入 {count} 題錯題記錄")
        else:
            print("❌ 已取消匯入")

    except json.JSONDecodeError:
        print("❌ 檔案格式錯誤：無法解析 JSON")
    except Exception as e:
        print(f"❌ 匯入失敗: {e}")


def get_not_mastered_ids(topic: Optional[str] = None) -> List[str]:
    """
    取得未精通的題目 ID 列表

    Args:
        topic: 主題篩選（可選）

    Returns:
        題目 ID 列表
    """
    db = load_mistakes_db()

    not_mastered = [
        m for m in db['mistakes']
        if not m.get('mastered', False)
    ]

    if topic:
        not_mastered = [
            m for m in not_mastered
            if any(topic.lower() in t.lower() for t in m.get('topics', []))
        ]

    # 按錯誤次數排序（錯誤多的優先）
    not_mastered.sort(key=lambda x: x.get('wrong_count', 0), reverse=True)

    return [m['question_id'] for m in not_mastered]


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='錯題本管理 - Databricks Exam Helper'
    )

    parser.add_argument(
        '--show-stats',
        action='store_true',
        help='顯示錯題統計'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='列出錯題清單'
    )

    parser.add_argument(
        '--topic',
        type=str,
        help='主題篩選'
    )

    parser.add_argument(
        '--include-mastered',
        action='store_true',
        help='包含已精通的題目'
    )

    parser.add_argument(
        '--mark-mastered',
        type=str,
        metavar='QUESTION_ID',
        help='標記題目為已精通'
    )

    parser.add_argument(
        '--clear-mastered',
        action='store_true',
        help='清除已精通的題目'
    )

    parser.add_argument(
        '--export',
        type=str,
        metavar='FILE',
        help='匯出錯題本'
    )

    parser.add_argument(
        '--import',
        type=str,
        dest='import_file',
        metavar='FILE',
        help='匯入錯題本'
    )

    parser.add_argument(
        '--add',
        nargs=3,
        metavar=('QUESTION_ID', 'USER_ANSWER', 'CORRECT_ANSWER'),
        help='添加錯題記錄（測試用）'
    )

    args = parser.parse_args()

    # 處理命令
    try:
        if args.show_stats:
            show_statistics()

        elif args.list:
            list_mistakes(
                topic=args.topic,
                include_mastered=args.include_mastered
            )

        elif args.mark_mastered:
            mark_as_mastered(args.mark_mastered)

        elif args.clear_mastered:
            clear_mastered()

        elif args.export:
            export_mistakes(args.export)

        elif args.import_file:
            import_mistakes(args.import_file)

        elif args.add:
            question_id, user_answer, correct_answer = args.add
            add_mistake(question_id, user_answer, correct_answer)

        else:
            # 預設顯示統計
            show_statistics()

    except KeyboardInterrupt:
        print("\n\n⚠️ 已中斷")
        return 1
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
