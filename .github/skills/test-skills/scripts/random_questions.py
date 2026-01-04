#!/usr/bin/env python3
"""
Random Question Selector for Databricks Exam Helper

從 question-bank/by-order_v1/ 隨機挑選指定數量的題目，
並解析題目內容以生成模擬測驗。
"""

import os
import random
import re
from pathlib import Path
from typing import List, Dict, Optional


def find_question_bank_root() -> Path:
    """
    尋找 question-bank/by-order_v1/ 目錄的絕對路徑
    
    Returns:
        Path: question-bank/by-order_v1/ 的絕對路徑
    
    Raises:
        FileNotFoundError: 如果找不到題庫目錄
    """
    # 從當前腳本位置往上找專案根目錄
    current_dir = Path(__file__).resolve().parent
    
    # 往上尋找直到找到 question-bank 目錄
    for parent in [current_dir] + list(current_dir.parents):
        question_bank = parent / "question-bank" / "by-order_v1"
        if question_bank.exists() and question_bank.is_dir():
            return question_bank
    
    raise FileNotFoundError(
        "找不到 question-bank/by-order_v1/ 目錄，"
        "請確認腳本在正確的專案結構中執行"
    )


def get_all_question_files(question_bank_path: Path) -> List[Path]:
    """
    取得題庫目錄中所有的題目檔案
    
    Args:
        question_bank_path: 題庫目錄路徑
    
    Returns:
        List[Path]: 所有 Q-*.md 檔案的路徑列表
    """
    question_files = sorted(question_bank_path.glob("Q-*.md"))
    return question_files


def parse_question_file(file_path: Path) -> Optional[Dict[str, any]]:
    """
    解析單一題目檔案，提取題目內容
    
    Args:
        file_path: 題目檔案路徑
    
    Returns:
        Dict: 包含題目資訊的字典，若解析失敗則返回 None
            {
                'id': 'Q-001',
                'question': '題目內容',
                'options': {'A': '...', 'B': '...', 'C': '...', 'D': '...'},
                'answer': 'B',
                'file_path': Path
            }
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # 提取題目 ID（從檔名）
        question_id = file_path.stem  # Q-001
        
        # 提取題目內容（在 ## 題目 和下一個 ## 之間）
        question_match = re.search(
            r'## 題目\s*\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL
        )
        if not question_match:
            print(f"警告: 無法解析題目內容 - {file_path.name}")
            return None
        
        question_text = question_match.group(1).strip()
        
        # 提取選項（A-D）
        options = {}
        option_pattern = r'^([A-D])[\.、\)]\s*(.+?)$'
        for line in question_text.split('\n'):
            match = re.match(option_pattern, line.strip())
            if match:
                option_letter, option_text = match.groups()
                options[option_letter] = option_text.strip()
        
        # 從題目文本中移除選項部分，保留題幹
        question_lines = []
        for line in question_text.split('\n'):
            if not re.match(option_pattern, line.strip()):
                question_lines.append(line)
        question_stem = '\n'.join(question_lines).strip()
        
        # 提取正確答案（在 ## 正確答案 或 ## 解析 中）
        answer_match = re.search(
            r'(?:## 正確答案|## 解析)\s*\n.*?(?:正確答案|答案)[:：\s]*([A-D])',
            content,
            re.IGNORECASE | re.DOTALL
        )
        answer = answer_match.group(1) if answer_match else None
        
        if not answer:
            print(f"警告: 無法解析答案 - {file_path.name}")
            return None
        
        return {
            'id': question_id,
            'question': question_stem,
            'options': options,
            'answer': answer,
            'file_path': file_path
        }
    
    except Exception as e:
        print(f"錯誤: 解析檔案 {file_path.name} 時發生錯誤 - {e}")
        return None


def select_random_questions(
    question_bank_path: Path,
    count: int = 10,
    seed: Optional[int] = None
) -> List[Dict[str, any]]:
    """
    隨機挑選指定數量的題目
    
    Args:
        question_bank_path: 題庫目錄路徑
        count: 要挑選的題目數量（預設 10）
        seed: 隨機種子（用於可重現的隨機結果）
    
    Returns:
        List[Dict]: 隨機挑選的題目列表
    """
    if seed is not None:
        random.seed(seed)
    
    # 取得所有題目檔案
    all_files = get_all_question_files(question_bank_path)
    
    if not all_files:
        raise ValueError("題庫中沒有找到任何題目檔案")
    
    # 隨機挑選
    selected_count = min(count, len(all_files))
    selected_files = random.sample(all_files, selected_count)
    
    # 解析題目
    questions = []
    for file_path in selected_files:
        parsed = parse_question_file(file_path)
        if parsed:
            questions.append(parsed)
    
    return questions


def format_exam_output(questions: List[Dict[str, any]]) -> str:
    """
    將題目格式化為模擬測驗的輸出格式
    
    Args:
        questions: 題目列表
    
    Returns:
        str: 格式化的測驗內容（Markdown 格式）
    """
    output_lines = []
    
    # 標題
    output_lines.append("# Databricks 模擬測驗")
    output_lines.append("")
    output_lines.append(f"**題數:** {len(questions)} 題")
    output_lines.append(f"**時間建議:** {len(questions) * 2} 分鐘")
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")
    
    # 題目內容
    for idx, q in enumerate(questions, 1):
        output_lines.append(f"## 第 {idx} 題")
        output_lines.append("")
        output_lines.append(q['question'])
        output_lines.append("")
        
        # 選項
        for option_letter in ['A', 'B', 'C', 'D']:
            if option_letter in q['options']:
                output_lines.append(f"{option_letter}. {q['options'][option_letter]}")
        
        output_lines.append("")
        output_lines.append("---")
        output_lines.append("")
    
    # 答案（放在最下方）
    output_lines.append("")
    output_lines.append("## 📝 答案")
    output_lines.append("")
    output_lines.append("<details>")
    output_lines.append("<summary>點擊查看答案</summary>")
    output_lines.append("")
    output_lines.append("| 題號 | 答案 | 題目 ID |")
    output_lines.append("|------|------|---------|")
    
    for idx, q in enumerate(questions, 1):
        output_lines.append(f"| {idx} | **{q['answer']}** | `{q['id']}` |")
    
    output_lines.append("")
    output_lines.append("</details>")
    output_lines.append("")
    
    return '\n'.join(output_lines)


def main():
    """主程式"""
    try:
        # 尋找題庫目錄
        question_bank_path = find_question_bank_root()
        print(f"找到題庫目錄: {question_bank_path}")
        
        # 隨機挑選 10 題
        questions = select_random_questions(question_bank_path, count=10)
        print(f"成功挑選 {len(questions)} 題")
        
        # 格式化輸出
        exam_content = format_exam_output(questions)
        
        # 輸出到標準輸出（可以透過重定向寫入檔案）
        print("\n" + "="*60)
        print(exam_content)
        
    except Exception as e:
        print(f"錯誤: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
