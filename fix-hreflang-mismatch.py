#!/usr/bin/env python3
"""
Fix hreflang/language switcher mismatches in knowledge-base nested structure.
The issue: zh/knowledge-base/* pages have hreflang pointing to /en/* (new flat structure)
but language switcher pointing to /en/knowledge-base/* (old nested structure).

Solution: Make both point to the same structure (old nested for old nested pages).
"""

import re
from pathlib import Path

BASE_DIR = Path("/home/zqd/.openclaw/workspace/polymarket-reporter")

def fix_page(file_path):
    """Fix a single page's hreflang and language switcher to be consistent."""
    content = file_path.read_text(encoding='utf-8')
    original = content
    
    rel_path = str(file_path.relative_to(BASE_DIR))
    
    # Determine the expected counterpart path
    # zh/knowledge-base/X -> en/knowledge-base/X
    # en/knowledge-base/X -> zh/knowledge-base/X
    
    if '/zh/knowledge-base/' in rel_path:
        # This is a ZH nested page
        nested_part = rel_path.replace('zh/knowledge-base/', '')
        expected_en = f'en/knowledge-base/{nested_part}'
        expected_en_url = f'https://www.pred101.com/en/knowledge-base/{nested_part}'
        expected_en_href = f'/en/knowledge-base/{nested_part}'
        
        # Fix hreflang-en
        old_hreflang = r'hreflang="en"[^>]*href="https://www\.pred101\.com/en/[^"]*"'
        new_hreflang = f'hreflang="en" href="{expected_en_url}"'
        content = re.sub(old_hreflang, new_hreflang, content)
        
        # Fix language switcher (English link)
        # Match patterns like: href="/en/kol/" or href="/en/knowledge-base/kol/"
        old_switcher = r'href="/en/[^"]*"[^>]*>English<'
        new_switcher = f'href="{expected_en_href}">English<'
        content = re.sub(old_switcher, new_switcher, content)
        
        # Also fix floating switcher pattern
        old_floating = r'href="/en/[^"]*" style="[^>]*>EN<'
        if expected_en_href.startswith('/en/knowledge-base/'):
            new_floating = f'href="{expected_en_href}" style="padding:4px 10px;border-radius:999px;text-decoration:none;color:#9ba7c4;font-size:.85rem">EN<'
            content = re.sub(old_floating, new_floating, content)
        
        print(f"Fixed ZH page: {rel_path}")
        print(f"  → EN counterpart: {expected_en}")
        
    elif '/en/knowledge-base/' in rel_path:
        # This is an EN nested page
        nested_part = rel_path.replace('en/knowledge-base/', '')
        expected_zh = f'zh/knowledge-base/{nested_part}'
        expected_zh_url = f'https://www.pred101.com/zh/knowledge-base/{nested_part}'
        expected_zh_href = f'/zh/knowledge-base/{nested_part}'
        
        # Fix hreflang-zh
        old_hreflang = r'hreflang="zh"[^>]*href="https://www\.pred101\.com/zh/[^"]*"'
        new_hreflang = f'hreflang="zh" href="{expected_zh_url}"'
        content = re.sub(old_hreflang, new_hreflang, content)
        
        # Fix language switcher (Chinese link)
        old_switcher = r'href="/zh/[^"]*"[^>]*>Chinese<'
        new_switcher = f'href="{expected_zh_href}">Chinese<'
        content = re.sub(old_switcher, new_switcher, content)
        
        # Also fix floating switcher pattern for Chinese
        old_floating_zh = r'href="/zh/[^"]*" style="[^>]*>中文<'
        if expected_zh_href.startswith('/zh/knowledge-base/'):
            new_floating_zh = f'href="{expected_zh_href}" style="padding:4px 10px;border-radius:999px;text-decoration:none;color:#fff;background:#6f7cff;font-size:.85rem">中文<'
            content = re.sub(old_floating_zh, new_floating_zh, content)
        
        print(f"Fixed EN page: {rel_path}")
        print(f"  → ZH counterpart: {expected_zh}")
    
    if content != original:
        file_path.write_text(content, encoding='utf-8')
        return True
    return False

def main():
    print("=" * 60)
    print("Fixing hreflang/switcher mismatches in knowledge-base nested structure")
    print("=" * 60)
    print()
    
    fixed_count = 0
    
    # Fix ZH knowledge-base nested pages
    zh_files = list((BASE_DIR / "zh" / "knowledge-base").rglob("*.html"))
    for f in zh_files:
        if fix_page(f):
            fixed_count += 1
    
    # Fix EN knowledge-base nested pages
    en_files = list((BASE_DIR / "en" / "knowledge-base").rglob("*.html"))
    for f in en_files:
        if fix_page(f):
            fixed_count += 1
    
    print()
    print("=" * 60)
    print(f"Fixed {fixed_count} pages")
    print("=" * 60)

if __name__ == "__main__":
    main()
