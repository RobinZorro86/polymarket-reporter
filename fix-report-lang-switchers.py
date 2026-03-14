#!/usr/bin/env python3
"""Fix language switchers in report pages to point to specific counterpart pages."""
import os
import re
from pathlib import Path

BASE = Path('/home/zqd/.openclaw/workspace/polymarket-reporter')

def fix_en_report(filepath):
    """Fix EN report: change Chinese link from /zh/reports/X/ to /zh/reports/.../specific-file.html"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get the relative path from en/
    rel_path = filepath.relative_to(BASE / 'en')
    zh_path = f'/zh/{rel_path}'
    
    # Find and replace the lang-switch Chinese link
    # Pattern: <a href="/zh/reports/.../">Chinese</a> or <a href="/zh/.../">Chinese</a>
    old_pattern = r'(<div class="lang-switch">.*?<a href="/en/" class="active">EN</a><a href=")(/zh/[^"]*?)(".*?>Chinese</a>)'
    
    def replace_zh_link(match):
        prefix = match.group(1)
        # Keep the /zh/ part but replace the rest with the correct path
        return f'{prefix}{zh_path}{match.group(3)}'
    
    new_content = re.sub(old_pattern, replace_zh_link, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def fix_zh_report(filepath):
    """Fix ZH report: change EN link from /en/ to /en/reports/.../specific-file.html"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get the relative path from zh/
    rel_path = filepath.relative_to(BASE / 'zh')
    en_path = f'/en/{rel_path}'
    
    # Find and replace the lang-switch EN link
    old_pattern = r'(<div class="lang-switch">.*?<a href=")(/en/[^"]*?)(".*?>EN</a>)'
    
    def replace_en_link(match):
        return f'{match.group(1)}{en_path}{match.group(3)}'
    
    new_content = re.sub(old_pattern, replace_en_link, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

# Fix EN reports
print("=== Fixing EN reports ===")
en_fixed = 0
for report_dir in ['reports/daily', 'reports/weekly', 'reports/simmer']:
    dir_path = BASE / 'en' / report_dir
    if dir_path.exists():
        for html_file in dir_path.glob('*.html'):
            if fix_en_report(html_file):
                print(f"  Fixed: {html_file.relative_to(BASE)}")
                en_fixed += 1

# Fix ZH reports
print("\n=== Fixing ZH reports ===")
zh_fixed = 0
for report_dir in ['reports/daily', 'reports/weekly', 'reports/simmer']:
    dir_path = BASE / 'zh' / report_dir
    if dir_path.exists():
        for html_file in dir_path.glob('*.html'):
            if fix_zh_report(html_file):
                print(f"  Fixed: {html_file.relative_to(BASE)}")
                zh_fixed += 1

print(f"\n=== Summary ===")
print(f"EN reports fixed: {en_fixed}")
print(f"ZH reports fixed: {zh_fixed}")
