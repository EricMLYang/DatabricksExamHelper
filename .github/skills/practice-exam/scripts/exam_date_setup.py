#!/usr/bin/env python3
"""
Exam Date Setup CLI for Databricks Exam Helper

考試日期設定工具 — 讓使用者透過 CLI 設定目標考試日期，
自動計算倒數天數並顯示目前所處的學習階段。

Usage:
    python exam_date_setup.py                  # Interactive prompt
    python exam_date_setup.py --set-date 2026-06-15   # Set directly
    python exam_date_setup.py --show            # Show current status
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Ensure sibling modules are importable.
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from profile_manager import (  # noqa: E402
    display_study_phase_summary,
    get_exam_date,
    init_profile,
    update_exam_date,
    validate_exam_date,
    validate_exam_date_future,
)


def _prompt_exam_date() -> str:
    """
    互動式提示使用者輸入考試日期。

    反覆提示直到使用者輸入有效且不早於今天的日期或按 Ctrl-C 取消。

    Returns:
        使用者輸入的有效日期字串（YYYY-MM-DD）
    """
    while True:
        try:
            raw = input("Enter your exam date (YYYY-MM-DD): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nCancelled.")
            sys.exit(0)

        if not raw:
            print("  ⚠️  Date cannot be empty. Please try again.\n")
            continue

        if not validate_exam_date(raw):
            print(
                "  ⚠️  Invalid date format or value. "
                "Use YYYY-MM-DD (e.g. 2026-06-15).\n"
            )
            continue

        if not validate_exam_date_future(raw):
            print(
                "  ⚠️  The date must be today or in the future. "
                "Please try again.\n"
            )
            continue

        return raw


def run_interactive() -> int:
    """執行互動式考試日期設定流程。"""
    init_profile()

    current = get_exam_date()

    print()
    print("=" * 50)
    print("  📅  Exam Date Setup")
    print("=" * 50)

    if current:
        print(f"\n  Current exam date: {current}")
        print("  (Enter a new date to update, or Ctrl-C to cancel)\n")
    else:
        print("\n  No exam date set yet.")
        print("  Set your target exam date to see your study timeline.\n")

    date_str = _prompt_exam_date()
    update_exam_date(date_str)

    print(f"\n  ✅  Exam date saved: {date_str}")
    print()
    display_study_phase_summary()

    return 0


def run_set_date(date_str: str) -> int:
    """非互動式設定考試日期。"""
    init_profile()

    if not validate_exam_date(date_str):
        print(
            f"Error: '{date_str}' is not a valid date. "
            "Use YYYY-MM-DD format."
        )
        return 1

    if not validate_exam_date_future(date_str):
        today = datetime.now().date().isoformat()
        print(
            f"Error: '{date_str}' is in the past. "
            f"Today is {today}. Please provide a future date."
        )
        return 1

    update_exam_date(date_str)
    print(f"\n  ✅  Exam date saved: {date_str}\n")
    display_study_phase_summary()
    return 0


def run_show() -> int:
    """顯示目前的考試日期與學習階段。"""
    init_profile()
    display_study_phase_summary()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Set or view your target exam date and study phase."
    )
    parser.add_argument(
        "--set-date",
        type=str,
        metavar="YYYY-MM-DD",
        help="Set the exam date directly (non-interactive).",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display the current exam date and study phase.",
    )

    args = parser.parse_args()

    if args.show:
        return run_show()
    if args.set_date:
        return run_set_date(args.set_date)

    # Default: interactive prompt
    return run_interactive()


if __name__ == "__main__":
    sys.exit(main())
