#!/usr/bin/env python3
"""
Fix language switcher paths to maintain current page path when switching languages.
"""

import os
import re
from pathlib import Path

def fix_file(file_path):
    """Fix language switcher in a single file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Determine current language
    if '/en/' in file_path:
        current_lang = 'en'
        target_lang = 'zh'
    elif '/zh/' in file_path:
        current_lang = 'zh'
        target_lang = 'en'
    else:
        return False
    
    # Calculate target path
    # e.g., /home/.../polymarket-reporter/en/learn/day1/index.html → /zh/learn/day1/
    base_dir = '/home/zqd/.openclaw/workspace/polymarket-reporter/'
    rel_path = file_path.replace(base_dir, '')
    
    # Get directory path
    if rel_path.endswith('index.html'):
        dir_path = os.path.dirname(rel_path)
    else:
        dir_path = os.path.dirname(rel_path)
    
    # Build target language path
    if dir_path.startswith(f'{current_lang}/'):
        target_path = dir_path.replace(f'{current_lang}/', f'{target_lang}/', 1)
    else:
        return False
    
    # Add trailing slash if needed
    if not target_path.endswith('/'):
        target_path += '/'
    
    original = content
    
    # Fix header lang-switch: <a href="/zh/">中文</a> → <a href="/zh/learn/day1/">中文</a>
    if current_lang == 'en':
        # Replace /zh/ with /zh/learn/day1/ in lang-switch
        content = content.replace('<a href="/zh/">中文</a>', f'<a href="/{target_path}">中文</a>')
    else:
        # Replace /en/ with /en/learn/day1/ in lang-switch  
        content = content.replace('<a href="/en/">English</a>', f'<a href="/{target_path}">English</a>')
    
    # Fix footer language links
    content = content.replace('href="/zh/">语言切换', f'href="/{target_path}">语言切换')
    content = content.replace('href="/en/">Language', f'href="/{target_path}">Language')
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    base_dir = Path('/home/zqd/.openclaw/workspace/polymarket-reporter')
    
    html_files = list(base_dir.glob('en/**/*.html')) + list(base_dir.glob('zh/**/*.html'))
    
    fixed = 0
    skipped = 0
    
    for fp in html_files:
        if fix_file(str(fp)):
            fixed += 1
            print(f"✓ {fp.relative_to(base_dir)}")
        else:
            skipped += 1
    
    print(f"\n=== Summary ===")
    print(f"Fixed: {fixed}")
    print(f"Skipped: {skipped}")
    print(f"Total: {len(html_files)}")

if __name__ == '__main__':
    main()
