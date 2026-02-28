#!/usr/bin/env python3
"""
Tests for exam_date_setup.py

考試日期設定 CLI 的測試。

執行測試：
    pytest tests/test_exam_date_setup.py
    pytest tests/test_exam_date_setup.py -v
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

# Add scripts directory to path
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

from exam_date_setup import _prompt_exam_date, run_set_date, run_show
from profile_manager import PROFILE_FILENAME, init_profile, load_profile


class TestRunSetDate:
    """測試非互動式日期設定"""

    def test_set_valid_future_date(self, tmp_path, capsys):
        """測試設定有效的未來日期"""
        profile_path = tmp_path / PROFILE_FILENAME
        future = (datetime.now().date() + timedelta(days=30)).isoformat()
        with patch(
            'exam_date_setup.init_profile'
        ), patch(
            'profile_manager.get_profile_path', return_value=profile_path
        ):
            init_profile()
            result = run_set_date(future)

        assert result == 0
        captured = capsys.readouterr()
        assert "Exam date saved" in captured.out

    def test_set_today_date(self, tmp_path, capsys):
        """測試設定今天日期（應成功，屬於 Sprint Phase）"""
        profile_path = tmp_path / PROFILE_FILENAME
        today = datetime.now().date().isoformat()
        with patch(
            'exam_date_setup.init_profile'
        ), patch(
            'profile_manager.get_profile_path', return_value=profile_path
        ):
            init_profile()
            result = run_set_date(today)

        assert result == 0

    def test_set_past_date_fails(self, tmp_path, capsys):
        """測試設定過去日期回傳錯誤"""
        profile_path = tmp_path / PROFILE_FILENAME
        past = (datetime.now().date() - timedelta(days=1)).isoformat()
        with patch(
            'exam_date_setup.init_profile'
        ), patch(
            'profile_manager.get_profile_path', return_value=profile_path
        ):
            init_profile()
            result = run_set_date(past)

        assert result == 1
        captured = capsys.readouterr()
        assert "in the past" in captured.out

    def test_set_invalid_format_fails(self, tmp_path, capsys):
        """測試無效格式回傳錯誤"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch(
            'exam_date_setup.init_profile'
        ), patch(
            'profile_manager.get_profile_path', return_value=profile_path
        ):
            init_profile()
            result = run_set_date("not-a-date")

        assert result == 1
        captured = capsys.readouterr()
        assert "not a valid date" in captured.out

    def test_set_date_persists(self, tmp_path):
        """測試設定的日期確實寫入檔案"""
        profile_path = tmp_path / PROFILE_FILENAME
        future = (datetime.now().date() + timedelta(days=60)).isoformat()
        with patch(
            'exam_date_setup.init_profile'
        ), patch(
            'profile_manager.get_profile_path', return_value=profile_path
        ):
            init_profile()
            run_set_date(future)
            profile = load_profile()

        assert profile['exam_date'] == future


class TestRunShow:
    """測試顯示當前狀態"""

    def test_show_without_date(self, tmp_path, capsys):
        """測試未設定日期時的顯示"""
        profile_path = tmp_path / PROFILE_FILENAME
        with patch(
            'exam_date_setup.init_profile'
        ), patch(
            'profile_manager.get_profile_path', return_value=profile_path
        ):
            init_profile()
            result = run_show()

        assert result == 0
        captured = capsys.readouterr()
        assert "Not set" in captured.out

    def test_show_with_date(self, tmp_path, capsys):
        """測試設定日期後的顯示"""
        profile_path = tmp_path / PROFILE_FILENAME
        future = (datetime.now().date() + timedelta(days=45)).isoformat()
        with patch(
            'exam_date_setup.init_profile'
        ), patch(
            'profile_manager.get_profile_path', return_value=profile_path
        ):
            init_profile()
            run_set_date(future)
            result = run_show()

        assert result == 0
        captured = capsys.readouterr()
        assert future in captured.out


class TestPromptExamDate:
    """測試互動式日期輸入提示"""

    def test_valid_input_returns_date(self):
        """測試有效輸入直接回傳"""
        future = (datetime.now().date() + timedelta(days=10)).isoformat()
        with patch('builtins.input', return_value=future):
            result = _prompt_exam_date()
        assert result == future

    def test_today_input_accepted(self):
        """測試今天的日期被接受"""
        today = datetime.now().date().isoformat()
        with patch('builtins.input', return_value=today):
            result = _prompt_exam_date()
        assert result == today

    def test_invalid_then_valid_input(self):
        """測試先輸入無效、再輸入有效日期"""
        future = (datetime.now().date() + timedelta(days=10)).isoformat()
        inputs = iter(["bad-date", future])
        with patch('builtins.input', side_effect=inputs):
            result = _prompt_exam_date()
        assert result == future

    def test_past_then_future_input(self):
        """測試先輸入過去日期、再輸入未來日期"""
        past = (datetime.now().date() - timedelta(days=1)).isoformat()
        future = (datetime.now().date() + timedelta(days=10)).isoformat()
        inputs = iter([past, future])
        with patch('builtins.input', side_effect=inputs):
            result = _prompt_exam_date()
        assert result == future

    def test_empty_then_valid_input(self):
        """測試先輸入空字串、再輸入有效日期"""
        future = (datetime.now().date() + timedelta(days=10)).isoformat()
        inputs = iter(["", future])
        with patch('builtins.input', side_effect=inputs):
            result = _prompt_exam_date()
        assert result == future

    def test_ctrl_c_exits(self):
        """測試 Ctrl-C 導致 SystemExit"""
        with patch('builtins.input', side_effect=KeyboardInterrupt):
            with pytest.raises(SystemExit):
                _prompt_exam_date()

    def test_eof_exits(self):
        """測試 EOF 導致 SystemExit"""
        with patch('builtins.input', side_effect=EOFError):
            with pytest.raises(SystemExit):
                _prompt_exam_date()


# 執行測試的說明
if __name__ == "__main__":
    print("請使用 pytest 執行測試:")
    print("  pytest tests/test_exam_date_setup.py")
    print("  pytest tests/test_exam_date_setup.py -v")
