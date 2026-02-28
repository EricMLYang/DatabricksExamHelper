#!/usr/bin/env python3
"""
Profile Manager for Databricks Exam Helper

使用者設定檔管理，儲存考試日期等個人化設定。
此檔案為 Dynamic Mode Selection（策略/引導/衝刺模式）的基礎。

Schema:
    {
        "exam_date": "YYYY-MM-DD",
        "created_at": "ISO-8601-Timestamp",
        "last_updated": "ISO-8601-Timestamp"
    }
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


PROFILE_FILENAME = 'user_profile.json'


def get_user_data_dir() -> Path:
    """取得使用者資料目錄，若家目錄不可寫則回退到 /tmp。"""
    preferred = Path.home() / '.claude-exam-helper' / 'user_data'
    try:
        preferred.mkdir(parents=True, exist_ok=True)
        probe = preferred / '.write_probe'
        probe.write_text('ok', encoding='utf-8')
        probe.unlink(missing_ok=True)
        return preferred
    except OSError:
        fallback = Path('/tmp/.claude-exam-helper/user_data')
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


def get_profile_path() -> Path:
    """取得使用者設定檔路徑。"""
    return get_user_data_dir() / PROFILE_FILENAME


def _create_empty_profile() -> Dict:
    """建立空的使用者設定檔。"""
    now = datetime.now().isoformat()
    return {
        'exam_date': None,
        'created_at': now,
        'last_updated': now,
    }


def validate_exam_date(exam_date: str) -> bool:
    """
    驗證考試日期是否為有效的 YYYY-MM-DD 格式字串。

    Args:
        exam_date: 待驗證的日期字串

    Returns:
        True 若日期格式有效，否則 False
    """
    if not isinstance(exam_date, str):
        return False
    try:
        datetime.strptime(exam_date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_exam_date_future(exam_date: str) -> bool:
    """
    驗證考試日期格式有效且日期 >= 今天。

    Args:
        exam_date: 待驗證的日期字串（YYYY-MM-DD）

    Returns:
        True 若日期格式有效且不早於今天，否則 False
    """
    if not validate_exam_date(exam_date):
        return False
    parsed = datetime.strptime(exam_date, '%Y-%m-%d').date()
    return parsed >= datetime.now().date()


def init_profile() -> Dict:
    """
    初始化使用者設定檔。若檔案不存在則自動建立；若已存在則載入。

    Returns:
        使用者設定檔字典
    """
    profile_path = get_profile_path()

    if profile_path.exists():
        return load_profile()

    profile = _create_empty_profile()
    _save_profile(profile)
    return profile


def load_profile() -> Dict:
    """
    載入使用者設定檔。若檔案不存在或損壞則建立新檔。

    Returns:
        使用者設定檔字典
    """
    profile_path = get_profile_path()

    if profile_path.exists():
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # 確保必要欄位存在
            if 'created_at' not in data:
                data['created_at'] = datetime.now().isoformat()
            if 'last_updated' not in data:
                data['last_updated'] = datetime.now().isoformat()
            if 'exam_date' not in data:
                data['exam_date'] = None
            return data
        except (json.JSONDecodeError, OSError):
            profile = _create_empty_profile()
            _save_profile(profile)
            return profile
    else:
        return init_profile()


def _save_profile(profile: Dict) -> None:
    """
    將設定檔寫入磁碟。

    Args:
        profile: 使用者設定檔字典
    """
    profile_path = get_profile_path()
    with open(profile_path, 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=4, ensure_ascii=False)


def update_exam_date(exam_date: str) -> Dict:
    """
    更新考試日期。寫入前會驗證日期格式。

    Args:
        exam_date: 考試日期字串，格式為 YYYY-MM-DD

    Returns:
        更新後的使用者設定檔字典

    Raises:
        ValueError: 若日期格式無效
    """
    if not validate_exam_date(exam_date):
        raise ValueError(
            f"無效的日期格式: '{exam_date}'。請使用 YYYY-MM-DD 格式。"
        )

    profile = load_profile()
    profile['exam_date'] = exam_date
    profile['last_updated'] = datetime.now().isoformat()
    _save_profile(profile)
    return profile


def get_exam_date() -> Optional[str]:
    """
    取得目前設定的考試日期。

    Returns:
        考試日期字串（YYYY-MM-DD）或 None（若尚未設定）
    """
    profile = load_profile()
    return profile.get('exam_date')


def get_days_until_exam() -> Optional[int]:
    """
    計算距離考試的天數。

    Returns:
        距離考試的天數（可為負數表示已過期），或 None（若尚未設定考試日期）
    """
    exam_date_str = get_exam_date()
    if not exam_date_str:
        return None

    try:
        exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        return (exam_date - today).days
    except ValueError:
        return None


def get_study_mode() -> str:
    """
    根據距離考試的天數決定學習模式。

    Returns:
        'strategy' (> 30 天), 'guided' (7-30 天), 'sprint' (< 7 天),
        或 'default'（若尚未設定考試日期）
    """
    days = get_days_until_exam()
    if days is None:
        return 'default'
    if days > 30:
        return 'strategy'
    if days >= 7:
        return 'guided'
    return 'sprint'


# ---------------------------------------------------------------------------
# Study Phase Summary UI
# ---------------------------------------------------------------------------

# Phase metadata: label, description, icon
_PHASE_INFO = {
    'strategy': {
        'label': 'Strategy Phase',
        'icon': '📐',
        'description': 'Diagnosis and Planning',
        'advice': 'Focus on understanding weak areas and building a study plan.',
    },
    'guided': {
        'label': 'Guided Phase',
        'icon': '📋',
        'description': "Today's Plan — dynamic tasks",
        'advice': 'Follow your daily plan and tackle targeted practice sets.',
    },
    'sprint': {
        'label': 'Sprint Phase',
        'icon': '🔥',
        'description': 'Direct Drill — high-intensity flashcards',
        'advice': 'Drill weak topics and review mistakes at full intensity!',
    },
    'default': {
        'label': 'No Exam Date Set',
        'icon': 'ℹ️',
        'description': 'Set your exam date to unlock your study timeline.',
        'advice': 'Run exam_date_setup.py or use --set-date to get started.',
    },
}


def format_study_phase_summary(
    exam_date_str: Optional[str] = None,
    days: Optional[int] = None,
    mode: Optional[str] = None,
) -> str:
    """
    產生學習階段摘要文字（純文字，不含副作用）。

    可傳入預先計算的值以方便測試，若皆為 None 則自動從 profile 讀取。

    Returns:
        多行純文字摘要字串
    """
    if exam_date_str is None:
        exam_date_str = get_exam_date()
    if days is None:
        days = get_days_until_exam()
    if mode is None:
        mode = get_study_mode()

    info = _PHASE_INFO.get(mode, _PHASE_INFO['default'])
    lines = []
    lines.append("=" * 50)
    lines.append(f"  {info['icon']}  {info['label']}")
    lines.append("-" * 50)

    if exam_date_str and days is not None:
        lines.append(f"  Exam Date  : {exam_date_str}")
        lines.append(f"  Days Left  : {days}")
    else:
        lines.append("  Exam Date  : Not set")

    lines.append(f"  Focus      : {info['description']}")
    lines.append("-" * 50)
    lines.append(f"  💡 {info['advice']}")
    lines.append("=" * 50)
    return "\n".join(lines)


def display_study_phase_summary() -> None:
    """在終端機印出學習階段摘要。"""
    print(format_study_phase_summary())
