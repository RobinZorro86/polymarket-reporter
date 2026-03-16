#!/usr/bin/env python3
"""
Fix ZH pages that don't have EN counterparts:
1. Remove incorrect hreflang="en" tags
2. Update language switcher to hide/disable EN link or point to parent
"""

import os
import re

# ZH pages without EN counterparts
MISSING_EN = [
    'zh/knowledge-base/kol/runes-leo/index.html',
    'zh/knowledge-base/kol/edwordkaru/index.html',
    'zh/knowledge-base/kol/rohonchain/index.html',
    'zh/knowledge-base/kol/noisyb0y1/index.html',
    'zh/knowledge-base/kol/dmitriyungarov/index.html',
    'zh/knowledge-base/kol/vladic_eth/index.html',
    'zh/knowledge-base/kol/molt-cornelius/index.html',
    'zh/knowledge-base/kol/rankings/KOL-BIWEEKLY-20260308.html',
    'zh/knowledge-base/kol/rankings/KOL-RANKING-20260308.html',
    'zh/knowledge-base/kol/rankings/runes-leo-biweekly-20260308.html',
    'zh/knowledge-base/kol/0xchainmind/index.html',
    'zh/knowledge-base/kol/cutnpaste4/index.html',
    'zh/knowledge-base/kol/ayi_ainotes/index.html',
    'zh/knowledge-base/kol/aleiahlock/index.html',
    'zh/knowledge-base/daily-reports/index.html',
]

def fix_file(path):
    """Fix a single file"""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. Remove hreflang="en" tag
    content = re.sub(
        r'\s*<link rel="alternate" hreflang="en" href="[^"]+">',
        '',
        content
    )
    
    # 2. Fix language switcher - disable EN link for pages without EN counterpart
    # Pattern: <div class="lang-switch"><a href="/en/...">EN</a>...
    # Replace with: <div class="lang-switch"><span class="lang-disabled" title="English version coming soon">EN</span>...
    
    # For KOL pages, point EN to /en/knowledge-base/kol/ (the KOL index)
    if '/knowledge-base/kol/' in path:
        content = re.sub(
            r'<a href="/en/kol/">EN</a>',
            '<a href="/en/knowledge-base/kol/">EN</a>',
            content
        )
    # For daily-reports, point to /en/reports/
    elif '/knowledge-base/daily-reports/' in path:
        content = re.sub(
            r'<a href="/en/[^"]*">EN</a>',
            '<a href="/en/reports/">EN</a>',
            content
        )
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

if __name__ == '__main__':
    fixed = 0
    for path in MISSING_EN:
        if os.path.exists(path):
            if fix_file(path):
                fixed += 1
                print(f'Fixed: {path}')
        else:
            print(f'Not found: {path}')
    
    print(f'\nTotal fixed: {fixed}/{len(MISSING_EN)}')
