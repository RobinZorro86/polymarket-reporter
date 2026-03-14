#!/usr/bin/env python3
"""
Fix hreflang and language switcher links in EN knowledge-base subdirectory index pages.
Problem: Some EN index pages still point to /zh/strategies/, /zh/tutorials/, /zh/resources/
         but ZH content lives under /zh/knowledge-base/strategies/, etc.
"""

import os
import re

BASE_DIR = "/home/zqd/.openclaw/workspace/polymarket-reporter"

# Files to fix with correct ZH paths
FILES_TO_FIX = {
    "en/knowledge-base/strategies/index.html": "/zh/knowledge-base/strategies/",
    "en/knowledge-base/tutorials/index.html": "/zh/knowledge-base/tutorials/",
    "en/knowledge-base/resources/index.html": "/zh/knowledge-base/resources/",
}

def fix_file(filepath, correct_zh_path):
    """Fix hreflang and language switcher in a single file."""
    full_path = os.path.join(BASE_DIR, filepath)
    
    if not os.path.exists(full_path):
        print(f"⚠️  File not found: {filepath}")
        return False
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix hreflang zh
    # Pattern: hreflang="zh" href="https://www.pred101.com/zh/xxx/"
    # Should be: hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/xxx/"
    content = re.sub(
        r'hreflang="zh" href="https://www\.pred101\.com/zh/(strategies|tutorials|resources)/"',
        r'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/\1/"',
        content
    )
    
    # Fix language switcher link (中文)
    # Pattern: >中文</a> with wrong href
    content = re.sub(
        r'href="/zh/(strategies|tutorials|resources)/">中文</a>',
        r'href="/zh/knowledge-base/\1/">中文</a>',
        content
    )
    
    if content == original:
        print(f"✅ No changes needed: {filepath}")
        return False
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed: {filepath}")
    print(f"   → ZH path now: {correct_zh_path}")
    return True

def main():
    print("=" * 60)
    print("Fix EN knowledge-base index pages: hreflang + lang switcher")
    print("=" * 60)
    
    fixed_count = 0
    for filepath, correct_path in FILES_TO_FIX.items():
        if fix_file(filepath, correct_path):
            fixed_count += 1
    
    print("=" * 60)
    print(f"Total fixed: {fixed_count} files")
    print("=" * 60)

if __name__ == "__main__":
    main()
