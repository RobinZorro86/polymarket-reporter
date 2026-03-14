#!/usr/bin/env python3
"""Fix language switchers in ZH pages that link to non-existent EN pages."""
import re
from pathlib import Path

BASE = Path('/home/zqd/.openclaw/workspace/polymarket-reporter')

# Mapping: ZH page path -> current (wrong) EN link -> correct EN fallback
FIXES = [
    ('zh/knowledge-base/daily-reports/', '/en/knowledge-base/daily-reports/', '/en/reports/'),
    ('zh/knowledge-base/kol/runes-leo/', '/en/knowledge-base/kol/runes-leo/', '/en/kol/'),
    ('zh/knowledge-base/kol/edwordkaru/', '/en/knowledge-base/kol/edwordkaru/', '/en/kol/'),
    ('zh/knowledge-base/kol/rohonchain/', '/en/knowledge-base/kol/rohonchain/', '/en/kol/'),
    ('zh/knowledge-base/kol/noisyb0y1/', '/en/knowledge-base/kol/noisyb0y1/', '/en/kol/'),
    ('zh/knowledge-base/kol/dmitriyungarov/', '/en/knowledge-base/kol/dmitriyungarov/', '/en/kol/'),
    ('zh/knowledge-base/kol/vladic_eth/', '/en/knowledge-base/kol/vladic_eth/', '/en/kol/'),
    ('zh/knowledge-base/kol/molt-cornelius/', '/en/knowledge-base/kol/molt-cornelius/', '/en/kol/'),
    ('zh/knowledge-base/kol/rankings/', '/en/knowledge-base/kol/rankings/', '/en/kol/'),
    ('zh/knowledge-base/kol/0xchainmind/', '/en/knowledge-base/kol/0xchainmind/', '/en/kol/'),
    ('zh/knowledge-base/kol/cutnpaste4/', '/en/knowledge-base/kol/cutnpaste4/', '/en/kol/'),
    ('zh/knowledge-base/kol/ayi_ainotes/', '/en/knowledge-base/kol/ayi_ainotes/', '/en/kol/'),
    ('zh/knowledge-base/resources/conviction-score-copytrading/', '/en/knowledge-base/resources/conviction-score-copytrading/', '/en/knowledge-base/resources/'),
    ('zh/knowledge-base/resources/prediction-market-history-sports-betting/', '/en/knowledge-base/resources/prediction-market-history-sports-betting/', '/en/knowledge-base/resources/'),
    ('zh/knowledge-base/resources/tools/', '/en/knowledge-base/resources/tools/', '/en/knowledge-base/resources/'),
]

fixed = 0
for zh_rel_path, old_en_href, en_fallback in FIXES:
    zh_dir = BASE / zh_rel_path
    if zh_dir.exists():
        for html_file in zh_dir.glob('*.html'):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_en_href in content:
                new_content = content.replace(old_en_href, en_fallback, 1)  # Only replace first occurrence (in lang-switch)
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed: {html_file.relative_to(BASE)}")
                print(f"  {old_en_href} -> {en_fallback}")
                fixed += 1

print(f"\nTotal fixed: {fixed}")
