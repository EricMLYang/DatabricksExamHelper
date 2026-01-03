#!/usr/bin/env python3
"""
Tests for tag_and_file.py

測試自動分類功能的正確性。

執行測試：
    pytest tests/test_tag_and_file.py
    pytest tests/test_tag_and_file.py -v  # 顯示詳細資訊
    pytest tests/test_tag_and_file.py -k test_detect_delta_lake  # 執行特定測試
"""

import pytest
import sys
from pathlib import Path
import tempfile
import shutil

# 將 skills/scripted 加入模組搜尋路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "scripted"))

from tag_and_file import QuestionFile, TagAndFileManager, TOPIC_KEYWORDS


class TestQuestionFile:
    """測試 QuestionFile 類別"""

    def test_detect_delta_lake_topic(self, tmp_path):
        """測試 Delta Lake 主題偵測"""
        # 建立測試檔案
        test_file = tmp_path / "test_delta.md"
        test_file.write_text("""
        # 題目
        在 Delta Lake 中，您需要使用 VACUUM 指令清理舊版本資料。
        請問 VACUUM table_name RETAIN 720 HOURS 的作用是什麼？
        """)

        question = QuestionFile(test_file)
        question.read_content()
        question.detect_topics()

        # 驗證
        assert len(question.detected_topics) > 0
        primary_topic = question.get_primary_topic()
        assert primary_topic == "delta-lake"

    def test_detect_streaming_topic(self, tmp_path):
        """測試 Streaming 主題偵測"""
        test_file = tmp_path / "test_streaming.md"
        test_file.write_text("""
        # Structured Streaming 題目
        以下哪個 Trigger 模式會持續處理資料？
        A. Trigger.Once
        B. Trigger.Continuous
        C. Trigger.ProcessingTime('10 seconds')
        """)

        question = QuestionFile(test_file)
        question.read_content()
        question.detect_topics()

        primary_topic = question.get_primary_topic()
        assert primary_topic == "streaming"

    def test_detect_unity_catalog_topic(self, tmp_path):
        """測試 Unity Catalog 主題偵測"""
        test_file = tmp_path / "test_uc.md"
        test_file.write_text("""
        # Unity Catalog 權限管理
        請問如何使用 GRANT 指令授予 SELECT 權限？
        Unity Catalog 的三層架構包含 Metastore, Catalog, Schema。
        """)

        question = QuestionFile(test_file)
        question.read_content()
        question.detect_topics()

        primary_topic = question.get_primary_topic()
        assert primary_topic == "unity-catalog"

    def test_detect_multiple_topics(self, tmp_path):
        """測試多主題偵測（應選優先級最高的）"""
        test_file = tmp_path / "test_multi.md"
        test_file.write_text("""
        # Delta Lake + Streaming 組合題
        如何在 Structured Streaming 中寫入 Delta Table？
        使用 writeStream 配合 .format("delta") 即可。
        """)

        question = QuestionFile(test_file)
        question.read_content()
        question.detect_topics()

        all_topics = question.get_all_topics()
        # 應該同時偵測到 Delta Lake 和 Streaming
        assert "delta-lake" in all_topics
        assert "streaming" in all_topics

        # 主要主題應該是優先級較高的
        primary_topic = question.get_primary_topic()
        assert primary_topic in ["delta-lake", "streaming"]

    def test_detect_no_topic(self, tmp_path):
        """測試無法識別主題的情況"""
        test_file = tmp_path / "test_unknown.md"
        test_file.write_text("""
        # 一般問題
        這是一個沒有特定技術關鍵字的題目。
        """)

        question = QuestionFile(test_file)
        question.read_content()
        question.detect_topics()

        primary_topic = question.get_primary_topic()
        assert primary_topic is None

    def test_case_insensitive_detection(self, tmp_path):
        """測試大小寫不敏感偵測"""
        test_file = tmp_path / "test_case.md"
        test_file.write_text("""
        # 題目
        使用 DELTA LAKE 和 VACUUM 指令。
        DeLtA lake 是很好的技術。
        """)

        question = QuestionFile(test_file)
        question.read_content()
        question.detect_topics()

        primary_topic = question.get_primary_topic()
        assert primary_topic == "delta-lake"


class TestTagAndFileManager:
    """測試 TagAndFileManager 類別"""

    def setup_test_files(self, source_dir: Path):
        """建立測試檔案"""
        # Delta Lake 題目
        (source_dir / "delta_001.md").write_text(
            "Delta Lake VACUUM 指令用於清理舊版本。"
        )
        (source_dir / "delta_002.md").write_text(
            "OPTIMIZE table_name ZORDER BY (col) 用於效能優化。"
        )

        # Streaming 題目
        (source_dir / "stream_001.md").write_text(
            "Structured Streaming 使用 Trigger.Continuous 模式。"
        )

        # Unity Catalog 題目
        (source_dir / "uc_001.md").write_text(
            "Unity Catalog 的 GRANT 和 REVOKE 指令用於權限管理。"
        )

        # 無法識別的題目
        (source_dir / "unknown_001.md").write_text(
            "這是一個沒有關鍵字的題目。"
        )

    def test_process_files(self, tmp_path):
        """測試檔案處理"""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        target_dir = tmp_path / "target"

        self.setup_test_files(source_dir)

        manager = TagAndFileManager(source_dir, target_dir, dry_run=True)
        manager.process()

        # 驗證分類結果
        assert "delta-lake" in manager.results
        assert "streaming" in manager.results
        assert "unity-catalog" in manager.results

        # 驗證 Delta Lake 有 2 個檔案
        assert len(manager.results["delta-lake"]) == 2

        # 驗證有未分類檔案
        assert len(manager.unclassified) == 1

    def test_dry_run_mode(self, tmp_path):
        """測試 dry-run 模式不會實際移動檔案"""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        target_dir = tmp_path / "target"

        self.setup_test_files(source_dir)

        original_files = list(source_dir.glob("*.md"))
        original_count = len(original_files)

        manager = TagAndFileManager(source_dir, target_dir, dry_run=True)
        manager.process()
        manager.move_files()

        # 驗證原始檔案數量不變（dry-run 不移動）
        assert len(list(source_dir.glob("*.md"))) == original_count

        # 驗證目標目錄沒有建立
        assert not (target_dir / "delta-lake").exists()

    def test_actual_move(self, tmp_path):
        """測試實際移動檔案"""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        target_dir = tmp_path / "target"

        self.setup_test_files(source_dir)

        manager = TagAndFileManager(source_dir, target_dir, dry_run=False)
        manager.process()
        total_moved = manager.move_files()

        # 驗證檔案已移動
        assert total_moved > 0

        # 驗證目標目錄已建立且包含檔案
        assert (target_dir / "delta-lake").exists()
        assert len(list((target_dir / "delta-lake").glob("*.md"))) == 2

        assert (target_dir / "streaming").exists()
        assert len(list((target_dir / "streaming").glob("*.md"))) == 1

    def test_source_dir_not_exists(self, tmp_path):
        """測試來源目錄不存在的錯誤處理"""
        source_dir = tmp_path / "nonexistent"
        target_dir = tmp_path / "target"

        manager = TagAndFileManager(source_dir, target_dir, dry_run=True)

        with pytest.raises(FileNotFoundError):
            manager.process()

    def test_empty_source_dir(self, tmp_path):
        """測試空來源目錄"""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        target_dir = tmp_path / "target"

        manager = TagAndFileManager(source_dir, target_dir, dry_run=True)
        manager.process()

        # 應該沒有任何分類結果
        assert len(manager.results) == 0
        assert len(manager.unclassified) == 0


class TestTopicKeywords:
    """測試主題關鍵字規則"""

    def test_all_topics_have_folder_name(self):
        """測試所有主題都有資料夾名稱"""
        for topic in TOPIC_KEYWORDS:
            assert topic.folder_name
            assert isinstance(topic.folder_name, str)

    def test_all_topics_have_keywords(self):
        """測試所有主題都有關鍵字"""
        for topic in TOPIC_KEYWORDS:
            assert len(topic.keywords) > 0

    def test_priority_values_are_valid(self):
        """測試優先級數值合理"""
        for topic in TOPIC_KEYWORDS:
            assert topic.priority > 0
            assert topic.priority <= 10


# 執行測試的說明
if __name__ == "__main__":
    print("請使用 pytest 執行測試:")
    print("  pytest tests/test_tag_and_file.py")
    print("  pytest tests/test_tag_and_file.py -v")
