#!/usr/bin/env python3
"""
最簡單的 Skill 範例：文件摘要器
"""

import sys

def summarize_file(filepath):
    """讀取文件並生成簡單摘要"""
    
    # 讀取文件
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # 計算統計資料
    num_lines = len(lines)
    num_words = len(content.split())
    num_chars = len(content)
    
    # 輸出摘要
    print(f"\n📄 File Summary: {filepath}")
    print("=" * 50)
    print(f"Lines:      {num_lines}")
    print(f"Words:      {num_words}")
    print(f"Characters: {num_chars}")
    print("\n📝 First 5 lines:")
    print("-" * 50)
    for i, line in enumerate(lines[:5], 1):
        print(f"{i}: {line[:70]}")
    print("=" * 50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python summarize.py <filename>")
        sys.exit(1)
    
    summarize_file(sys.argv[1])