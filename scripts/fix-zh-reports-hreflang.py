#!/usr/bin/env python3
"""
Fix missing hreflang="en" in Chinese report pages.
Adds hreflang="en" pointing to corresponding English report.
"""

import os
import re
from pathlib import Path

def fix_zh_reports():
    zh_reports_dir = Path("zh/reports/daily")
    en_reports_dir = Path("en/reports/daily")
    
    fixed = []
    skipped = []
    
    for zh_file in zh_reports_dir.glob("*.html"):
        if zh_file.name.endswith(".backup"):
            continue
            
        content = zh_file.read_text(encoding="utf-8")
        
        # Check if already has hreflang="en"
        if 'hreflang="en"' in content:
            skipped.append(f"{zh_file.name} (already has hreflang)")
            continue
        
        # Find canonical URL
        canonical_match = re.search(r'<link rel="canonical" href="([^"]+)"', content)
        if not canonical_match:
            skipped.append(f"{zh_file.name} (no canonical found)")
            continue
        
        canonical_url = canonical_match.group(1)
        
        # Build English URL by replacing /zh/ with /en/
        en_url = canonical_url.replace("/zh/", "/en/")
        
        # Check if English file exists
        en_file_name = zh_file.name
        en_file_path = en_reports_dir / en_file_name
        
        if not en_file_path.exists():
            # Try alternative naming patterns
            # zh uses daily-2026-03-08.html, en might use daily-20260308.html
            alt_name = en_file_name.replace("-03-", "03").replace("-02-", "02").replace("-01-", "01")
            en_file_path = en_reports_dir / alt_name
            
            if not en_file_path.exists():
                skipped.append(f"{zh_file.name} (no English counterpart)")
                continue
            
            en_url = en_url.replace("/zh/", "/en/").replace(en_file_name, alt_name)
        
        # Insert hreflang after canonical
        hreflang_tag = f'\n  <link rel="alternate" hreflang="en" href="{en_url}">'
        new_content = content.replace(canonical_match.group(0), canonical_match.group(0) + hreflang_tag)
        
        zh_file.write_text(new_content, encoding="utf-8")
        fixed.append(f"{zh_file.name} -> {en_url}")
    
    print("=== Fixed ===")
    for f in fixed:
        print(f"  ✅ {f}")
    
    print("\n=== Skipped ===")
    for s in skipped:
        print(f"  ⚠️  {s}")
    
    print(f"\nTotal: {len(fixed)} fixed, {len(skipped)} skipped")

if __name__ == "__main__":
    os.chdir("/home/zqd/.openclaw/workspace/polymarket-reporter")
    fix_zh_reports()
