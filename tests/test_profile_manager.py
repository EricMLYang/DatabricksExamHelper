#!/usr/bin/env python3
"""
Tests for profile_manager.py

使用者設定檔管理的測試。

執行測試：
    pytest tests/test_profile_manager.py
    pytest tests/test_profile_manager.py -v  # 顯示詳細資訊
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

# 將 practice-exam/scripts 加入模組搜尋路徑
sys.path.insert(
    0,
    str(
        Path(__file__).parent.parent
        / ".github"
        / "skills"
        / "practice-exam"
        / "scripts"
    ),
)

from profile_manager import (
    PROFILE_FILENAME,
    _create_empty_profile,
    get_days_until_exam,
    get_exam_date,
    get_profile_path,
    get_study_mode,
    init_profile,
    load_profile,
    update_exam_date,
    validate_exam_date,
)


class TestValidateExamDate:
    """測試日期驗證功能"""

    def test_valid_date(self):
        """測試有效日期"""
        assert validate_exam_date("2026-06-15") is True

    def test_valid_leap_year_date(self):
        """測試閏年日期"""
        assert validate_exam_date("2028-02-29") is True

    def test_invalid_format_slash(self):
        """測試無效格式（斜線分隔）"""
        assert validate_exam_date("2026/06/15") is False

    def test_invalid_format_no_separator(self):
        """測試無效格式（無分隔符號）"""
        assert validate_exam_date("20260615") is False

    def test_invalid_date_month_13(self):
        """測試無效月份"""
        assert validate_exam_date("2026-13-01") is False

    def test_invalid_date_day_32(self):
        """測試無效日期"""
        assert validate_exam_date("2026-01-32") is False

    def test_invalid_non_leap_year(self):
        """測試非閏年2月29日"""
        assert validate_exam_date("2026-02-29") is False

    def test_empty_string(self):
        """測試空字串"""
        assert validate_exam_date("") is False

    def test_none_input(self):
        """測試 None 輸入"""
        assert validate_exam_date(None) is False

    def test_integer_input(self):
        """測試整數輸入"""
        assert validate_exam_date(20260615) is False

    def test_partial_date(self):
        """測試不完整日期"""
        assert validate_exam_date("2026-06") is False

    def test_iso_datetime_not_accepted(self):
        """測試 ISO datetime 格式不被接受（僅接受日期）"""
        assert validate_exam_date("2026-06-15T10:00:00") is False


class TestCreateEmptyProfile:
    """測試建立空設定檔"""

    def test_has_required_fields(self):
        """測試空設定檔包含必要欄位"""
        profile = _create_empty_profile()
        assert 'exam_date' in profile
        assert 'created_at' in profile
        assert 'last_updated' in profile

    def test_exam_date_is_none(self):
        """測試初始考試日期為 None"""
        profile = _create_empty_profile()
        assert profile['exam_date'] is None

    def test_timestamps_are_iso_format(self):
        """測試時間戳記為 ISO 格式"""
        profile = _create_empty_profile()
        # Should not raise
        datetime.fromisoformat(profile['created_at'])
        datetime.fromisoformat(profile['last_updated'])


class TestInitProfile:
    """測試設定檔初始化"""

    def test_creates_new_profile(self, tmp_path):
        """測試建立新設定檔"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            profile = init_profile()

        assert profile_path.exists()
        assert profile['exam_date'] is None
        assert 'created_at' in profile

    def test_loads_existing_profile(self, tmp_path):
        """測試載入已存在的設定檔"""
        profile_path = tmp_path / PROFILE_FILENAME
        existing = {
            'exam_date': '2026-06-15',
            'created_at': '2026-01-01T00:00:00',
            'last_updated': '2026-01-01T00:00:00',
        }
        profile_path.write_text(json.dumps(existing), encoding='utf-8')

        with patch('profile_manager.get_profile_path', return_value=profile_path):
            profile = init_profile()

        assert profile['exam_date'] == '2026-06-15'

    def test_file_written_with_indent(self, tmp_path):
        """測試設定檔以縮排格式寫入（便於使用者手動閱讀）"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()

        content = profile_path.read_text(encoding='utf-8')
        # indent=4 produces lines with 4-space indentation
        assert '    ' in content


class TestLoadProfile:
    """測試載入設定檔"""

    def test_load_valid_profile(self, tmp_path):
        """測試載入有效設定檔"""
        profile_path = tmp_path / PROFILE_FILENAME
        data = {
            'exam_date': '2026-08-01',
            'created_at': '2026-01-01T00:00:00',
            'last_updated': '2026-02-01T00:00:00',
        }
        profile_path.write_text(
            json.dumps(data, indent=4), encoding='utf-8'
        )

        with patch('profile_manager.get_profile_path', return_value=profile_path):
            profile = load_profile()

        assert profile['exam_date'] == '2026-08-01'

    def test_load_corrupted_file_creates_new(self, tmp_path):
        """測試損壞檔案自動重建"""
        profile_path = tmp_path / PROFILE_FILENAME
        profile_path.write_text('not valid json {{{', encoding='utf-8')

        with patch('profile_manager.get_profile_path', return_value=profile_path):
            profile = load_profile()

        assert profile['exam_date'] is None
        assert 'created_at' in profile

    def test_load_missing_fields_adds_defaults(self, tmp_path):
        """測試缺少欄位時自動補全"""
        profile_path = tmp_path / PROFILE_FILENAME
        data = {'exam_date': '2026-06-15'}
        profile_path.write_text(json.dumps(data), encoding='utf-8')

        with patch('profile_manager.get_profile_path', return_value=profile_path):
            profile = load_profile()

        assert profile['exam_date'] == '2026-06-15'
        assert 'created_at' in profile
        assert 'last_updated' in profile

    def test_load_nonexistent_creates_new(self, tmp_path):
        """測試檔案不存在時自動建立"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            profile = load_profile()

        assert profile_path.exists()
        assert profile['exam_date'] is None


class TestUpdateExamDate:
    """測試更新考試日期"""

    def test_update_valid_date(self, tmp_path):
        """測試更新有效日期"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            profile = update_exam_date('2026-07-20')

        assert profile['exam_date'] == '2026-07-20'

    def test_update_changes_last_updated(self, tmp_path):
        """測試更新日期時 last_updated 也會更新"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            profile1 = init_profile()
            original_updated = profile1['last_updated']

            profile2 = update_exam_date('2026-07-20')

        assert profile2['last_updated'] >= original_updated

    def test_update_preserves_created_at(self, tmp_path):
        """測試更新日期時 created_at 不變"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            profile1 = init_profile()
            created = profile1['created_at']

            profile2 = update_exam_date('2026-07-20')

        assert profile2['created_at'] == created

    def test_update_invalid_date_raises(self, tmp_path):
        """測試無效日期拋出 ValueError"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            with pytest.raises(ValueError, match="無效的日期格式"):
                update_exam_date('not-a-date')

    def test_update_invalid_date_does_not_persist(self, tmp_path):
        """測試無效日期不會寫入磁碟"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            try:
                update_exam_date('2026-13-01')
            except ValueError:
                pass
            profile = load_profile()

        assert profile['exam_date'] is None

    def test_frequent_updates_supported(self, tmp_path):
        """測試支援頻繁更新（模擬規劃工具使用場景）"""
        profile_path = tmp_path / PROFILE_FILENAME
        dates = ['2026-06-01', '2026-07-15', '2026-08-20', '2026-05-10']

        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            for date in dates:
                profile = update_exam_date(date)

        assert profile['exam_date'] == '2026-05-10'

    def test_persisted_to_disk(self, tmp_path):
        """測試更新後確實寫入磁碟"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            update_exam_date('2026-09-01')

        # Read directly from file
        with open(profile_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert data['exam_date'] == '2026-09-01'


class TestGetExamDate:
    """測試取得考試日期"""

    def test_returns_none_when_not_set(self, tmp_path):
        """測試未設定時回傳 None"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            assert get_exam_date() is None

    def test_returns_date_after_set(self, tmp_path):
        """測試設定後回傳正確日期"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            update_exam_date('2026-12-25')
            assert get_exam_date() == '2026-12-25'


class TestGetDaysUntilExam:
    """測試計算距離考試天數"""

    def test_returns_none_when_not_set(self, tmp_path):
        """測試未設定考試日期時回傳 None"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            assert get_days_until_exam() is None

    def test_future_date_positive_days(self, tmp_path):
        """測試未來日期回傳正數"""
        profile_path = tmp_path / PROFILE_FILENAME
        future = (datetime.now().date() + timedelta(days=60)).isoformat()
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            update_exam_date(future)
            days = get_days_until_exam()
        assert days == 60

    def test_past_date_negative_days(self, tmp_path):
        """測試過去日期回傳負數"""
        profile_path = tmp_path / PROFILE_FILENAME
        past = (datetime.now().date() - timedelta(days=5)).isoformat()
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            update_exam_date(past)
            days = get_days_until_exam()
        assert days == -5

    def test_today_returns_zero(self, tmp_path):
        """測試今天回傳 0"""
        profile_path = tmp_path / PROFILE_FILENAME
        today = datetime.now().date().isoformat()
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            update_exam_date(today)
            days = get_days_until_exam()
        assert days == 0


class TestGetStudyMode:
    """測試學習模式選擇"""

    def test_default_when_no_exam_date(self, tmp_path):
        """測試未設定考試日期時回傳 default"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            assert get_study_mode() == 'default'

    def test_strategy_mode_over_30_days(self, tmp_path):
        """測試超過30天為 strategy 模式"""
        profile_path = tmp_path / PROFILE_FILENAME
        future = (datetime.now().date() + timedelta(days=45)).isoformat()
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            update_exam_date(future)
            assert get_study_mode() == 'strategy'

    def test_guided_mode_between_7_and_30_days(self, tmp_path):
        """測試 7-30 天為 guided 模式"""
        profile_path = tmp_path / PROFILE_FILENAME
        future = (datetime.now().date() + timedelta(days=15)).isoformat()
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            update_exam_date(future)
            assert get_study_mode() == 'guided'

    def test_guided_mode_at_30_days(self, tmp_path):
        """測試剛好30天為 guided 模式"""
        profile_path = tmp_path / PROFILE_FILENAME
        future = (datetime.now().date() + timedelta(days=30)).isoformat()
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            update_exam_date(future)
            assert get_study_mode() == 'guided'

    def test_guided_mode_at_7_days(self, tmp_path):
        """測試剛好7天為 guided 模式"""
        profile_path = tmp_path / PROFILE_FILENAME
        future = (datetime.now().date() + timedelta(days=7)).isoformat()
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            update_exam_date(future)
            assert get_study_mode() == 'guided'

    def test_sprint_mode_under_7_days(self, tmp_path):
        """測試少於7天為 sprint 模式"""
        profile_path = tmp_path / PROFILE_FILENAME
        future = (datetime.now().date() + timedelta(days=3)).isoformat()
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            update_exam_date(future)
            assert get_study_mode() == 'sprint'

    def test_sprint_mode_at_boundary_31_days_is_strategy(self, tmp_path):
        """測試31天為 strategy 模式"""
        profile_path = tmp_path / PROFILE_FILENAME
        future = (datetime.now().date() + timedelta(days=31)).isoformat()
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            update_exam_date(future)
            assert get_study_mode() == 'strategy'

    def test_sprint_mode_at_6_days(self, tmp_path):
        """測試6天為 sprint 模式"""
        profile_path = tmp_path / PROFILE_FILENAME
        future = (datetime.now().date() + timedelta(days=6)).isoformat()
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            update_exam_date(future)
            assert get_study_mode() == 'sprint'

    def test_past_exam_date_is_sprint(self, tmp_path):
        """測試過期考試日期為 sprint 模式"""
        profile_path = tmp_path / PROFILE_FILENAME
        past = (datetime.now().date() - timedelta(days=1)).isoformat()
        with patch('profile_manager.get_profile_path', return_value=profile_path):
            init_profile()
            update_exam_date(past)
            assert get_study_mode() == 'sprint'


class TestGetUserDataDir:
    """測試使用者資料目錄解析"""

    def test_fallback_when_home_not_writable(self):
        """測試家目錄不可寫時回退到 /tmp"""
        from profile_manager import get_user_data_dir

        original_mkdir = Path.mkdir

        def failing_mkdir(self_path, *args, **kwargs):
            if '.claude-exam-helper' in str(self_path) and '/tmp' not in str(self_path):
                raise OSError("Permission denied")
            return original_mkdir(self_path, *args, **kwargs)

        with patch.object(Path, 'mkdir', failing_mkdir):
            data_dir = get_user_data_dir()
            assert str(data_dir).startswith('/tmp/')


class TestProfileFilePath:
    """測試設定檔路徑"""

    def test_profile_filename(self):
        """測試設定檔名稱"""
        path = get_profile_path()
        assert path.name == PROFILE_FILENAME

    def test_profile_in_user_data_dir(self):
        """測試設定檔在 user_data 目錄下"""
        path = get_profile_path()
        assert 'user_data' in str(path)


# 執行測試的說明
if __name__ == "__main__":
    print("請使用 pytest 執行測試:")
    print("  pytest tests/test_profile_manager.py")
    print("  pytest tests/test_profile_manager.py -v")
