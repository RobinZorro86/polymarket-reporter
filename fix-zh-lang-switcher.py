#!/usr/bin/env python3
"""
Fix language switcher links in ZH knowledge-base pages.
Problem: ZH deep pages link to /en/ but should link to /en/knowledge-base/*
"""

import os
import re
from pathlib import Path

BASE_DIR = Path("/home/zqd/.openclaw/workspace/polymarket-reporter")

def get_relative_path(filepath: Path) -> str:
    """Get the relative path from zh/knowledge-base/"""
    rel = filepath.relative_to(BASE_DIR / "zh" / "knowledge-base")
    return str(rel.parent).replace("\\", "/")

def fix_zh_file(filepath: Path):
    """Fix language switcher in a ZH knowledge-base page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get the relative path
    rel_path = get_relative_path(filepath)
    
    # Build the expected EN path
    if rel_path == ".":
        en_path = "/en/knowledge-base/"
    else:
        en_path = f"/en/knowledge-base/{rel_path}/"
    
    # Pattern to match the lang-switch EN link
    # Looking for: <a href="/en/">EN</a>
    pattern = r'<a href="/en/">EN</a>'
    replacement = f'<a href="{en_path}">EN</a>'
    
    # Use DOTALL to match across lines
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, en_path
    return False, None

def main():
    fixed_count = 0
    total_count = 0
    
    # Find all HTML files in zh/knowledge-base
    zh_kb_dir = BASE_DIR / "zh" / "knowledge-base"
    
    for filepath in zh_kb_dir.rglob("*.html"):
        total_count += 1
        fixed, en_path = fix_zh_file(filepath)
        if fixed:
            print(f"✅ Fixed: {filepath.relative_to(BASE_DIR)}")
            print(f"   → EN link: {en_path}")
            fixed_count += 1
        else:
            print(f"⚪ Skipped: {filepath.relative_to(BASE_DIR)} (already correct or no match)")
    
    print(f"\n{'='*60}")
    print(f"Total files processed: {total_count}")
    print(f"Files fixed: {fixed_count}")
    print(f"Files unchanged: {total_count - fixed_count}")

if __name__ == "__main__":
    main()
