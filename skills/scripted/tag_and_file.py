#!/usr/bin/env python3
"""
Tag and File - 題目自動分類工具

此腳本自動識別題目內容，上標籤並搬移至正確的 by-topic/ 資料夾。

功能：
- 基於關鍵字匹配自動識別題目主題
- 自動建立目標目錄（若不存在）
- 支援 dry-run 模式（僅顯示將執行的動作，不實際移動檔案）
- 產出詳細的分類報告

使用範例：
    # Dry-run 模式（僅顯示分類結果，不實際移動）
    python tag_and_file.py --source ./unsorted --dry-run

    # 實際執行分類與移動
    python tag_and_file.py --source ./unsorted

    # 指定目標目錄
    python tag_and_file.py --source ./unsorted --target ./question-bank/by-topic
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class TopicKeyword:
    """主題關鍵字定義"""
    folder_name: str  # 資料夾名稱 (e.g., "delta-lake")
    keywords: List[str]  # 關鍵字列表
    priority: int  # 優先級 (數字越大優先級越高)


# 主題關鍵字規則
TOPIC_KEYWORDS = [
    # Delta Lake 相關 (高優先級)
    TopicKeyword("delta-lake", [
        "delta lake", "delta", "vacuum", "optimize", "zorder",
        "time travel", "merge into", "cdf", "change data feed",
        "delta table", "delta.*lake"
    ], priority=10),

    # Structured Streaming 相關
    TopicKeyword("streaming", [
        "streaming", "stream", "trigger", "watermark", "checkpoint",
        "foreachbatch", "auto loader", "cloudfiles",
        "readstream", "writestream", "structured streaming"
    ], priority=10),

    # Unity Catalog 相關
    TopicKeyword("unity-catalog", [
        "unity catalog", "metastore", "catalog", "grant", "revoke",
        "external location", "storage credential", "delta sharing",
        "uc\\.\\w+", "unity"
    ], priority=10),

    # Databricks SQL / Warehouse
    TopicKeyword("databricks-sql", [
        "sql warehouse", "databricks sql", "query history",
        "sql endpoint", "serverless sql"
    ], priority=8),

    # Workflows
    TopicKeyword("workflows", [
        "workflows", "job", "task", "orchestration",
        "databricks job", "task dependencies"
    ], priority=8),

    # PySpark / DataFrames
    TopicKeyword("pyspark", [
        "pyspark", "dataframe", "spark\\.sql", "select\\(", "filter\\(",
        "groupby", "agg\\(", "withcolumn", "udf"
    ], priority=7),

    # Cluster Management
    TopicKeyword("cluster", [
        "cluster", "autoscaling", "driver", "worker",
        "cluster mode", "instance type"
    ], priority=7),

    # Performance & Optimization
    TopicKeyword("performance", [
        "performance", "optimization", "cache", "persist",
        "broadcast", "partition", "shuffle", "skew"
    ], priority=6),

    # Security
    TopicKeyword("security", [
        "security", "authentication", "authorization",
        "encryption", "secret", "credential", "access control"
    ], priority=6),
]


class QuestionFile:
    """題目檔案處理類別"""

    def __init__(self, file_path: Path):
        """
        初始化題目檔案

        Args:
            file_path: 題目檔案路徑
        """
        self.file_path = file_path
        self.content = ""
        self.detected_topics: List[Tuple[str, int, int]] = []  # (topic, score, priority)

    def read_content(self) -> None:
        """讀取檔案內容"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
        except UnicodeDecodeError:
            # 嘗試其他編碼
            with open(self.file_path, 'r', encoding='latin-1') as f:
                self.content = f.read()

    def detect_topics(self) -> None:
        """偵測題目主題"""
        content_lower = self.content.lower()

        for topic_def in TOPIC_KEYWORDS:
            score = 0

            for keyword in topic_def.keywords:
                # 使用正則表達式匹配（支援部分正則語法）
                matches = re.findall(keyword.lower(), content_lower)
                score += len(matches)

            if score > 0:
                self.detected_topics.append((
                    topic_def.folder_name,
                    score,
                    topic_def.priority
                ))

        # 按優先級和分數排序
        self.detected_topics.sort(key=lambda x: (x[2], x[1]), reverse=True)

    def get_primary_topic(self) -> Optional[str]:
        """
        取得主要主題

        Returns:
            str: 主要主題資料夾名稱，若無法識別則返回 None
        """
        if self.detected_topics:
            return self.detected_topics[0][0]
        return None

    def get_all_topics(self) -> List[str]:
        """
        取得所有識別出的主題

        Returns:
            List[str]: 主題資料夾名稱列表
        """
        return [topic for topic, _, _ in self.detected_topics]


class TagAndFileManager:
    """題目分類管理器"""

    def __init__(self, source_dir: Path, target_dir: Path, dry_run: bool = False):
        """
        初始化分類管理器

        Args:
            source_dir: 來源目錄
            target_dir: 目標目錄（by-topic）
            dry_run: 是否為 dry-run 模式
        """
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.dry_run = dry_run
        self.results: Dict[str, List[Path]] = defaultdict(list)  # topic -> files
        self.unclassified: List[Path] = []

    def process(self) -> None:
        """處理所有題目檔案"""
        if not self.source_dir.exists():
            raise FileNotFoundError(f"來源目錄不存在: {self.source_dir}")

        # 尋找所有 .md 檔案
        md_files = list(self.source_dir.glob("**/*.md"))

        if not md_files:
            print(f"⚠️  在 {self.source_dir} 中沒有找到任何 .md 檔案")
            return

        print(f"📂 找到 {len(md_files)} 個檔案")
        print(f"⏳ 分析中...\n")

        for file_path in md_files:
            question = QuestionFile(file_path)
            question.read_content()
            question.detect_topics()

            primary_topic = question.get_primary_topic()

            if primary_topic:
                self.results[primary_topic].append(file_path)
            else:
                self.unclassified.append(file_path)

    def move_files(self) -> None:
        """移動檔案到目標目錄"""
        total_moved = 0

        for topic, files in self.results.items():
            topic_dir = self.target_dir / topic

            if not self.dry_run:
                topic_dir.mkdir(parents=True, exist_ok=True)

            for file_path in files:
                target_path = topic_dir / file_path.name

                if self.dry_run:
                    print(f"  [DRY-RUN] {file_path.name} → {topic}/{file_path.name}")
                else:
                    # 檢查目標檔案是否已存在
                    if target_path.exists():
                        print(f"  ⚠️  跳過（檔案已存在）: {file_path.name} → {topic}/")
                        continue

                    file_path.rename(target_path)
                    print(f"  ✅ {file_path.name} → {topic}/")
                    total_moved += 1

        return total_moved

    def generate_report(self) -> None:
        """產生分類報告"""
        print("\n" + "=" * 60)
        print("📊 分類報告")
        print("=" * 60 + "\n")

        if self.results:
            print("### 已分類題目\n")
            for topic, files in sorted(self.results.items()):
                print(f"**{topic}/** ({len(files)} 題)")
                for file_path in files[:3]:  # 只顯示前 3 個
                    print(f"  - {file_path.name}")
                if len(files) > 3:
                    print(f"  - ... 及其他 {len(files) - 3} 題")
                print()

        if self.unclassified:
            print(f"### ⚠️  無法分類的題目 ({len(self.unclassified)} 題)\n")
            print("以下題目無法自動識別主題，請手動分類：\n")
            for file_path in self.unclassified:
                print(f"  - {file_path.name}")
            print()

        # 統計
        total_classified = sum(len(files) for files in self.results.values())
        total_files = total_classified + len(self.unclassified)

        print("### 統計摘要\n")
        print(f"- 總檔案數: {total_files}")
        print(f"- 已分類: {total_classified} ({total_classified/total_files*100:.1f}%)" if total_files > 0 else "- 已分類: 0")
        print(f"- 未分類: {len(self.unclassified)}")
        print(f"- 分類主題數: {len(self.results)}")

        if self.dry_run:
            print(f"\n⚠️  **Dry-run 模式** - 未實際移動任何檔案")
        else:
            print(f"\n✅ 分類完成！")

        print("\n" + "=" * 60)


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description="題目自動分類工具 - 基於關鍵字匹配自動分類題目",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # Dry-run 模式（僅顯示分類結果）
  python tag_and_file.py --source ./unsorted --dry-run

  # 實際執行分類
  python tag_and_file.py --source ./unsorted

  # 指定目標目錄
  python tag_and_file.py --source ./unsorted --target ./question-bank/by-topic
        """
    )

    parser.add_argument(
        '--source',
        type=str,
        required=True,
        help='來源目錄路徑 (必填)'
    )

    parser.add_argument(
        '--target',
        type=str,
        default='./question-bank/by-topic',
        help='目標目錄路徑 (選填，預設為 ./question-bank/by-topic)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Dry-run 模式：僅顯示分類結果，不實際移動檔案'
    )

    args = parser.parse_args()

    try:
        source_dir = Path(args.source)
        target_dir = Path(args.target)

        print(f"📁 來源目錄: {source_dir}")
        print(f"🎯 目標目錄: {target_dir}")

        if args.dry_run:
            print(f"⚠️  Dry-run 模式啟用\n")

        # 初始化管理器
        manager = TagAndFileManager(source_dir, target_dir, args.dry_run)

        # 處理檔案
        manager.process()

        # 移動檔案
        if manager.results or manager.unclassified:
            total_moved = manager.move_files()

        # 產生報告
        manager.generate_report()

    except FileNotFoundError as e:
        print(f"❌ 錯誤: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"❌ 未預期的錯誤: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
