#!/usr/bin/env python3
"""
Fix broken canonical tags in Chinese report pages.
The previous script left canonical tags without closing >.
"""

import os
import re
from pathlib import Path

def fix_broken_canonical():
    zh_reports_dir = Path("zh/reports/daily")
    
    fixed = []
    
    for zh_file in zh_reports_dir.glob("*.html"):
        if zh_file.name.endswith(".backup"):
            continue
            
        content = zh_file.read_text(encoding="utf-8")
        
        # Fix pattern: canonical href="..."<newline>  <link rel="alternate"
        # Should be: canonical href="..."><newline>  <link rel="alternate"
        old_pattern = r'(<link rel="canonical" href="[^"]+)"\n(\s+<link rel="alternate" hreflang="en")>\s*>'
        
        def replace_func(match):
            return f'{match.group(1)}>\n{match.group(2)}>'
        
        new_content = re.sub(old_pattern, replace_func, content)
        
        if new_content != content:
            zh_file.write_text(new_content, encoding="utf-8")
            fixed.append(zh_file.name)
    
    print("=== Fixed broken canonical tags ===")
    for f in fixed:
        print(f"  ✅ {f}")
    
    if not fixed:
        print("  No broken tags found")

if __name__ == "__main__":
    os.chdir("/home/zqd/.openclaw/workspace/polymarket-reporter")
    fix_broken_canonical()
