#!/usr/bin/env python3
"""
Team Weakness Dashboard - 團隊弱點分析儀表板

此腳本彙整所有成員的錯題標籤，生成團隊補坑指南。

功能：
- 彙整個人錯題紀錄（從 progress/individuals/ 目錄）
- 分析團隊整體弱點主題
- 產出 Markdown 格式的統計報表
- 識別需要團隊集中補強的考點

使用範例：
    # 產生團隊儀表板
    python team_weakness_dashboard.py --individuals-dir ./progress/individuals --output team-dashboard.md

    # 輸出到預設位置
    python team_weakness_dashboard.py --individuals-dir ./progress/individuals

個人錯題紀錄格式 (YAML):
    user: "alice"
    wrong_questions:
      - question_id: Q-MOCK01-001
        topics: ["Delta-Lake", "VACUUM"]
        difficulty: L2-Intermediate
        date: "2024-01-15"

      - question_id: Q-STREAM-042
        topics: ["Streaming", "Triggers"]
        difficulty: L3-Advanced
        date: "2024-01-16"
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Set, Optional
from dataclasses import dataclass
from datetime import datetime
from collections import Counter, defaultdict

try:
    import yaml
except ImportError:
    print("Error: PyYAML is not installed. Please run: pip install pyyaml")
    sys.exit(1)


@dataclass
class WrongQuestion:
    """錯題資料結構"""
    question_id: str
    topics: List[str]
    difficulty: str
    date: str
    user: str  # 誰答錯的


@dataclass
class TeamWeakness:
    """團隊弱點資料結構"""
    topic: str
    error_count: int
    affected_members: Set[str]
    difficulty_distribution: Dict[str, int]  # difficulty -> count


class IndividualRecord:
    """個人錯題紀錄"""

    def __init__(self, file_path: Path):
        """
        初始化個人紀錄

        Args:
            file_path: 個人錯題紀錄檔案路徑
        """
        self.file_path = file_path
        self.user_name = ""
        self.wrong_questions: List[WrongQuestion] = []

    def load(self) -> None:
        """
        載入個人錯題紀錄

        Raises:
            yaml.YAMLError: YAML 格式錯誤
            ValueError: 資料格式不符合規範
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"YAML 格式錯誤 ({self.file_path}): {e}")

        if not isinstance(data, dict):
            raise ValueError(f"{self.file_path}: YAML 根節點必須是 dict")

        self.user_name = data.get('user', self.file_path.stem)

        if 'wrong_questions' not in data:
            # 沒有錯題紀錄，返回空列表
            return

        for idx, q in enumerate(data['wrong_questions']):
            try:
                question = WrongQuestion(
                    question_id=q['question_id'],
                    topics=q.get('topics', []),
                    difficulty=q.get('difficulty', 'L2-Intermediate'),
                    date=q.get('date', ''),
                    user=self.user_name
                )
                self.wrong_questions.append(question)
            except KeyError as e:
                raise ValueError(f"{self.file_path}: 錯題 #{idx + 1} 缺少必要欄位: {e}")


class TeamDashboard:
    """團隊弱點儀表板"""

    def __init__(self, individuals_dir: Path):
        """
        初始化團隊儀表板

        Args:
            individuals_dir: 個人錯題紀錄目錄
        """
        self.individuals_dir = individuals_dir
        self.records: List[IndividualRecord] = []
        self.team_weaknesses: List[TeamWeakness] = []
        self.total_errors = 0
        self.total_members = 0

    def load_all_records(self) -> None:
        """載入所有個人紀錄"""
        if not self.individuals_dir.exists():
            raise FileNotFoundError(f"個人錯題目錄不存在: {self.individuals_dir}")

        yaml_files = list(self.individuals_dir.glob("*.yaml")) + \
                     list(self.individuals_dir.glob("*.yml"))

        if not yaml_files:
            print(f"⚠️  在 {self.individuals_dir} 中沒有找到任何個人紀錄")
            return

        print(f"📂 找到 {len(yaml_files)} 個個人紀錄")

        for file_path in yaml_files:
            try:
                record = IndividualRecord(file_path)
                record.load()
                self.records.append(record)
                print(f"  ✅ {record.user_name}: {len(record.wrong_questions)} 題錯題")
            except Exception as e:
                print(f"  ⚠️  跳過 {file_path.name}: {e}")

        self.total_members = len(self.records)
        self.total_errors = sum(len(r.wrong_questions) for r in self.records)

    def analyze(self) -> None:
        """分析團隊弱點"""
        # 彙整所有錯題的主題
        topic_errors: Dict[str, List[WrongQuestion]] = defaultdict(list)

        for record in self.records:
            for question in record.wrong_questions:
                for topic in question.topics:
                    topic_errors[topic].append(question)

        # 計算每個主題的統計資料
        weaknesses = []

        for topic, questions in topic_errors.items():
            # 計算影響成員
            affected_members = set(q.user for q in questions)

            # 計算難度分佈
            difficulty_dist = Counter(q.difficulty for q in questions)

            weakness = TeamWeakness(
                topic=topic,
                error_count=len(questions),
                affected_members=affected_members,
                difficulty_distribution=dict(difficulty_dist)
            )
            weaknesses.append(weakness)

        # 按錯誤次數排序
        self.team_weaknesses = sorted(weaknesses, key=lambda w: w.error_count, reverse=True)

    def generate_markdown_report(self) -> str:
        """
        生成 Markdown 格式報告

        Returns:
            str: Markdown 格式報告內容
        """
        lines = []

        # 標題
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines.append("# 團隊弱點分析儀表板\n")
        lines.append(f"**產生時間:** {timestamp}")
        lines.append(f"**團隊人數:** {self.total_members}")
        lines.append(f"**總錯題數:** {self.total_errors}\n")
        lines.append("---\n")

        # 執行摘要
        lines.append("## 📊 執行摘要\n")

        if not self.team_weaknesses:
            lines.append("🎉 **恭喜！團隊目前沒有錯題紀錄。**\n")
        else:
            top_3 = self.team_weaknesses[:3]
            lines.append("### Top 3 團隊弱點\n")

            for rank, weakness in enumerate(top_3, 1):
                impact = len(weakness.affected_members) / self.total_members * 100 if self.total_members > 0 else 0
                lines.append(f"{rank}. **`{weakness.topic}`** - {weakness.error_count} 次錯誤，影響 {len(weakness.affected_members)} 人 ({impact:.0f}%)")

            lines.append("")

        lines.append("---\n")

        # 詳細弱點分析
        if self.team_weaknesses:
            lines.append("## ⚠️ 詳細弱點分析\n")
            lines.append("| 排名 | 主題 | 錯誤次數 | 影響人數 | 影響比例 | 難度分佈 |")
            lines.append("|------|------|----------|----------|----------|----------|")

            for rank, weakness in enumerate(self.team_weaknesses, 1):
                impact_pct = len(weakness.affected_members) / self.total_members * 100 if self.total_members > 0 else 0

                # 難度分佈字串
                diff_parts = []
                for diff in ['L1-Basic', 'L2-Intermediate', 'L3-Advanced']:
                    count = weakness.difficulty_distribution.get(diff, 0)
                    if count > 0:
                        diff_parts.append(f"{diff.replace('-', ' ')}: {count}")

                diff_str = "<br>".join(diff_parts) if diff_parts else "-"

                lines.append(
                    f"| {rank} | `{weakness.topic}` | {weakness.error_count} | "
                    f"{len(weakness.affected_members)} | {impact_pct:.0f}% | {diff_str} |"
                )

            lines.append("")
            lines.append("---\n")

        # 個人表現摘要
        lines.append("## 👥 個人表現摘要\n")
        lines.append("| 成員 | 錯題數 | 主要弱點 (Top 3) |")
        lines.append("|------|--------|------------------|")

        # 按錯題數排序
        sorted_records = sorted(self.records, key=lambda r: len(r.wrong_questions), reverse=True)

        for record in sorted_records:
            # 統計個人弱點
            personal_topics = Counter()
            for question in record.wrong_questions:
                for topic in question.topics:
                    personal_topics[topic] += 1

            top_topics = personal_topics.most_common(3)
            top_topics_str = ", ".join([f"`{t}` ({c})" for t, c in top_topics])

            lines.append(f"| {record.user_name} | {len(record.wrong_questions)} | {top_topics_str or '-'} |")

        lines.append("")
        lines.append("---\n")

        # 補強建議
        lines.append("## 💡 團隊補強建議\n")

        if not self.team_weaknesses:
            lines.append("團隊表現優秀，繼續保持！\n")
        else:
            # 識別需要集中補強的主題（影響超過 50% 成員）
            high_impact = [w for w in self.team_weaknesses
                          if len(w.affected_members) / self.total_members >= 0.5]

            if high_impact:
                lines.append("### 🔥 優先補強主題（影響超過 50% 成員）\n")
                for weakness in high_impact:
                    lines.append(f"- **`{weakness.topic}`**")
                    lines.append(f"  - 影響成員: {', '.join(sorted(weakness.affected_members))}")
                    lines.append(f"  - 建議行動:")
                    lines.append(f"    - 安排團隊共學會議，集中講解此主題")
                    lines.append(f"    - 準備 3-5 題變形題供團隊練習")
                    lines.append(f"    - 建立此主題的 Cheatsheet 至 `docs/core-knowledge/`")
                    lines.append("")

            # 識別個別補強主題（影響少於 50% 但錯誤次數多）
            individual_focus = [w for w in self.team_weaknesses
                               if len(w.affected_members) / self.total_members < 0.5
                               and w.error_count >= 3]

            if individual_focus:
                lines.append("### 📚 個別補強主題（影響少數成員但錯誤頻繁）\n")
                for weakness in individual_focus[:5]:  # 最多列 5 個
                    lines.append(f"- **`{weakness.topic}`**")
                    lines.append(f"  - 建議 {', '.join(sorted(weakness.affected_members))} 加強此主題")
                    lines.append(f"  - 可使用 `solve-question` 技能進行深度解析")
                    lines.append("")

        lines.append("---\n")

        # 資料來源
        lines.append("## 📂 資料來源\n")
        lines.append(f"- 個人錯題目錄: `{self.individuals_dir}`")
        lines.append(f"- 分析成員數: {self.total_members}")
        lines.append(f"- 總錯題數: {self.total_errors}\n")

        lines.append("---\n")
        lines.append(f"*報告生成於 {timestamp}*\n")

        return "\n".join(lines)


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description="團隊弱點分析儀表板 - 彙整所有成員的錯題標籤，生成團隊補坑指南",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 產生團隊儀表板
  python team_weakness_dashboard.py --individuals-dir ./progress/individuals --output team-dashboard.md

  # 輸出到預設位置（progress/team-dashboard.md）
  python team_weakness_dashboard.py --individuals-dir ./progress/individuals
        """
    )

    parser.add_argument(
        '--individuals-dir',
        type=str,
        required=True,
        help='個人錯題紀錄目錄路徑 (必填)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='./progress/team-dashboard.md',
        help='輸出報告檔案路徑 (選填，預設為 ./progress/team-dashboard.md)'
    )

    args = parser.parse_args()

    try:
        individuals_dir = Path(args.individuals_dir)

        print(f"📂 個人錯題目錄: {individuals_dir}")

        # 初始化儀表板
        dashboard = TeamDashboard(individuals_dir)

        # 載入所有紀錄
        dashboard.load_all_records()

        if dashboard.total_members == 0:
            print("⚠️  沒有找到任何有效的個人紀錄")
            sys.exit(0)

        # 分析團隊弱點
        print(f"\n⏳ 分析團隊弱點...")
        dashboard.analyze()
        print(f"✅ 分析完成！")

        # 生成報告
        report = dashboard.generate_markdown_report()

        # 輸出報告
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"💾 報告已儲存至: {output_path}")

        # 顯示摘要
        print(f"\n📊 團隊弱點分析摘要:")
        print(f"  - 團隊人數: {dashboard.total_members}")
        print(f"  - 總錯題數: {dashboard.total_errors}")
        print(f"  - 弱點主題數: {len(dashboard.team_weaknesses)}")

        if dashboard.team_weaknesses:
            print(f"\n🔝 Top 3 弱點:")
            for rank, weakness in enumerate(dashboard.team_weaknesses[:3], 1):
                print(f"  {rank}. {weakness.topic} ({weakness.error_count} 次錯誤)")

    except FileNotFoundError as e:
        print(f"❌ 錯誤: {e}", file=sys.stderr)
        sys.exit(1)

    except yaml.YAMLError as e:
        print(f"❌ YAML 格式錯誤: {e}", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"❌ 資料格式錯誤: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"❌ 未預期的錯誤: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
