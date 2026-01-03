#!/usr/bin/env python3
"""
Mock Exam Grader - 模擬卷批改工具

此腳本讀取模擬卷答案檔（YAML 格式），產出錯題報告與統計分析。

功能：
- 批改模擬卷，計算得分率
- 產出錯題清單與弱點分析
- 支援 Markdown 格式輸出

使用範例：
    python mock_exam_grader.py --input my_answers.yaml --user eric --output result.md
    python mock_exam_grader.py --input exam.yaml --user alice --output ./reports/alice_exam1.md

YAML 輸入格式：
    exam:
      name: "Mock Exam 01"
      total_questions: 40
      passing_score: 70

    answers:
      - question_id: Q-MOCK01-001
        user_answer: A
        correct_answer: B
        topics: ["Delta-Lake", "VACUUM"]
        difficulty: L2-Intermediate

      - question_id: Q-MOCK01-002
        user_answer: C
        correct_answer: C
        topics: ["Streaming", "Triggers"]
        difficulty: L1-Basic
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from collections import Counter

try:
    import yaml
except ImportError:
    print("Error: PyYAML is not installed. Please run: pip install pyyaml")
    sys.exit(1)


@dataclass
class Question:
    """題目資料結構"""
    question_id: str
    user_answer: str
    correct_answer: str
    topics: List[str]
    difficulty: str

    def is_correct(self) -> bool:
        """判斷答案是否正確"""
        return self.user_answer.upper() == self.correct_answer.upper()


@dataclass
class ExamResult:
    """考試結果資料結構"""
    exam_name: str
    user_name: str
    total_questions: int
    correct_count: int
    wrong_count: int
    passing_score: float
    user_score: float
    passed: bool
    wrong_questions: List[Question]
    weak_topics: List[tuple[str, int]]  # (topic, error_count)
    difficulty_stats: Dict[str, Dict[str, int]]  # difficulty: {correct, wrong}
    timestamp: str


class MockExamGrader:
    """模擬卷批改器"""

    def __init__(self, input_file: Path, user_name: str):
        """
        初始化批改器

        Args:
            input_file: YAML 答案檔路徑
            user_name: 使用者名稱
        """
        self.input_file = input_file
        self.user_name = user_name
        self.questions: List[Question] = []
        self.exam_info: Dict[str, Any] = {}

    def load_answers(self) -> None:
        """
        載入 YAML 答案檔

        Raises:
            FileNotFoundError: 檔案不存在
            yaml.YAMLError: YAML 格式錯誤
            ValueError: 資料格式不符合規範
        """
        if not self.input_file.exists():
            raise FileNotFoundError(f"答案檔不存在: {self.input_file}")

        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"YAML 格式錯誤: {e}")

        # 驗證資料結構
        if not isinstance(data, dict):
            raise ValueError("YAML 根節點必須是 dict")

        if 'exam' not in data:
            raise ValueError("缺少必要欄位: exam")

        if 'answers' not in data:
            raise ValueError("缺少必要欄位: answers")

        self.exam_info = data['exam']

        # 驗證 exam 欄位
        required_exam_fields = ['name', 'total_questions', 'passing_score']
        for field in required_exam_fields:
            if field not in self.exam_info:
                raise ValueError(f"exam 缺少必要欄位: {field}")

        # 解析答案
        for idx, answer in enumerate(data['answers']):
            try:
                question = Question(
                    question_id=answer['question_id'],
                    user_answer=answer['user_answer'],
                    correct_answer=answer['correct_answer'],
                    topics=answer.get('topics', []),
                    difficulty=answer.get('difficulty', 'L2-Intermediate')
                )
                self.questions.append(question)
            except KeyError as e:
                raise ValueError(f"答案 #{idx + 1} 缺少必要欄位: {e}")

    def grade(self) -> ExamResult:
        """
        批改考卷

        Returns:
            ExamResult: 考試結果
        """
        correct_count = sum(1 for q in self.questions if q.is_correct())
        wrong_count = len(self.questions) - correct_count

        # 計算得分
        if len(self.questions) > 0:
            user_score = (correct_count / len(self.questions)) * 100
        else:
            user_score = 0

        passing_score = self.exam_info.get('passing_score', 70)
        passed = user_score >= passing_score

        # 統計錯題
        wrong_questions = [q for q in self.questions if not q.is_correct()]

        # 統計弱點主題
        topic_errors = Counter()
        for q in wrong_questions:
            for topic in q.topics:
                topic_errors[topic] += 1

        weak_topics = topic_errors.most_common()

        # 統計難度分佈
        difficulty_stats: Dict[str, Dict[str, int]] = {}
        for q in self.questions:
            if q.difficulty not in difficulty_stats:
                difficulty_stats[q.difficulty] = {'correct': 0, 'wrong': 0}

            if q.is_correct():
                difficulty_stats[q.difficulty]['correct'] += 1
            else:
                difficulty_stats[q.difficulty]['wrong'] += 1

        return ExamResult(
            exam_name=self.exam_info['name'],
            user_name=self.user_name,
            total_questions=len(self.questions),
            correct_count=correct_count,
            wrong_count=wrong_count,
            passing_score=passing_score,
            user_score=user_score,
            passed=passed,
            wrong_questions=wrong_questions,
            weak_topics=weak_topics,
            difficulty_stats=difficulty_stats,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )


class MarkdownReportGenerator:
    """Markdown 報告生成器"""

    @staticmethod
    def generate(result: ExamResult) -> str:
        """
        生成 Markdown 格式報告

        Args:
            result: 考試結果

        Returns:
            str: Markdown 格式報告內容
        """
        lines = []

        # 標題
        lines.append(f"# 模擬卷批改報告\n")
        lines.append(f"**考試名稱:** {result.exam_name}")
        lines.append(f"**考生:** {result.user_name}")
        lines.append(f"**批改時間:** {result.timestamp}\n")
        lines.append("---\n")

        # 總體統計
        lines.append("## 📊 總體統計\n")
        lines.append(f"| 項目 | 數值 |")
        lines.append(f"|------|------|")
        lines.append(f"| 總題數 | {result.total_questions} |")
        lines.append(f"| 答對 | {result.correct_count} ✅ |")
        lines.append(f"| 答錯 | {result.wrong_count} ❌ |")
        lines.append(f"| 正確率 | {result.user_score:.1f}% |")
        lines.append(f"| 及格標準 | {result.passing_score}% |")

        # 結果判定
        if result.passed:
            lines.append(f"| **結果** | **🎉 通過** |")
        else:
            needed = result.passing_score - result.user_score
            lines.append(f"| **結果** | **❌ 未通過** (距離及格還差 {needed:.1f}%) |")

        lines.append("")
        lines.append("---\n")

        # 難度分佈統計
        lines.append("## 📈 各難度表現\n")
        lines.append("| 難度 | 答對 | 答錯 | 正確率 |")
        lines.append("|------|------|------|--------|")

        for difficulty in ['L1-Basic', 'L2-Intermediate', 'L3-Advanced']:
            if difficulty in result.difficulty_stats:
                stats = result.difficulty_stats[difficulty]
                correct = stats['correct']
                wrong = stats['wrong']
                total = correct + wrong
                accuracy = (correct / total * 100) if total > 0 else 0
                lines.append(f"| {difficulty} | {correct} | {wrong} | {accuracy:.1f}% |")

        lines.append("")
        lines.append("---\n")

        # 弱點主題分析
        if result.weak_topics:
            lines.append("## ⚠️ 弱點主題分析\n")
            lines.append("以下是您答錯最多的主題，建議優先複習：\n")
            lines.append("| 排名 | 主題 | 錯誤次數 |")
            lines.append("|------|------|----------|")

            for rank, (topic, count) in enumerate(result.weak_topics[:10], 1):
                lines.append(f"| {rank} | `{topic}` | {count} |")

            lines.append("")
            lines.append("---\n")

        # 錯題清單
        if result.wrong_questions:
            lines.append("## ❌ 錯題清單\n")
            lines.append(f"共 {len(result.wrong_questions)} 題需要複習：\n")

            for idx, q in enumerate(result.wrong_questions, 1):
                lines.append(f"### {idx}. {q.question_id}\n")
                lines.append(f"- **您的答案:** {q.user_answer}")
                lines.append(f"- **正確答案:** {q.correct_answer}")
                lines.append(f"- **考點:** {', '.join([f'`{t}`' for t in q.topics])}")
                lines.append(f"- **難度:** {q.difficulty}")
                lines.append("")
        else:
            lines.append("## 🎉 恭喜！\n")
            lines.append("全部答對，沒有錯題！\n")

        lines.append("---\n")

        # 建議
        lines.append("## 💡 複習建議\n")

        if result.user_score >= 90:
            lines.append("🌟 **優秀！** 您對這些考點掌握得非常好。建議：")
            lines.append("- 複習錯題（若有）")
            lines.append("- 嘗試更高難度的變形題")
            lines.append("- 幫助其他同學理解這些考點")
        elif result.user_score >= result.passing_score:
            lines.append("✅ **通過！** 您已達到及格標準。建議：")
            lines.append("- 重點複習弱點主題")
            lines.append("- 完成錯題的變形題訓練")
            lines.append("- 將錯題解析加入個人筆記")
        else:
            lines.append("📚 **需加強！** 建議：")
            lines.append(f"1. 優先複習弱點主題（見上方「弱點主題分析」）")
            lines.append(f"2. 逐題分析錯題，使用 `explain-why-not` 技能深度拆解")
            lines.append(f"3. 完成錯題的變形題訓練，確保真正理解")
            lines.append(f"4. 7 天後重新做一次這份模擬卷，檢視進步幅度")

        lines.append("")
        lines.append("---\n")
        lines.append(f"*報告生成於 {result.timestamp}*\n")

        return "\n".join(lines)


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description="模擬卷批改工具 - 讀取 YAML 答案檔，產出錯題報告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 批改模擬卷並輸出到檔案
  python mock_exam_grader.py --input my_answers.yaml --user eric --output result.md

  # 批改模擬卷並顯示在螢幕上
  python mock_exam_grader.py --input exam.yaml --user alice

  # 指定輸出目錄
  python mock_exam_grader.py --input exam.yaml --user bob --output ./reports/bob_exam1.md
        """
    )

    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='YAML 答案檔路徑 (必填)'
    )

    parser.add_argument(
        '--user',
        type=str,
        required=True,
        help='使用者名稱 (必填)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='輸出報告檔案路徑 (選填，預設輸出到螢幕)'
    )

    args = parser.parse_args()

    try:
        # 初始化批改器
        input_path = Path(args.input)
        grader = MockExamGrader(input_path, args.user)

        # 載入答案
        print(f"📂 載入答案檔: {input_path}")
        grader.load_answers()
        print(f"✅ 成功載入 {len(grader.questions)} 題")

        # 批改
        print(f"⏳ 批改中...")
        result = grader.grade()
        print(f"✅ 批改完成！")
        print(f"📊 得分: {result.user_score:.1f}% ({result.correct_count}/{result.total_questions})")

        # 生成報告
        report = MarkdownReportGenerator.generate(result)

        # 輸出報告
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)

            print(f"💾 報告已儲存至: {output_path}")
        else:
            print("\n" + "=" * 60)
            print(report)
            print("=" * 60)

    except FileNotFoundError as e:
        print(f"❌ 錯誤: {e}", file=sys.stderr)
        sys.exit(1)

    except yaml.YAMLError as e:
        print(f"❌ YAML 格式錯誤: {e}", file=sys.stderr)
        print("\n請確認 YAML 檔案格式正確。參考格式：", file=sys.stderr)
        print("""
exam:
  name: "Mock Exam 01"
  total_questions: 40
  passing_score: 70

answers:
  - question_id: Q-MOCK01-001
    user_answer: A
    correct_answer: B
    topics: ["Delta-Lake", "VACUUM"]
    difficulty: L2-Intermediate
        """, file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"❌ 資料格式錯誤: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"❌ 未預期的錯誤: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
