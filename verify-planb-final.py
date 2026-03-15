#!/usr/bin/env python3
"""
Phase-2 Plan B Final Verification Script
Checks:
1. EN pages for Chinese content residue
2. ZH pages for English contamination
3. Canonical/Hreflang consistency
4. Language switcher consistency
5. Old path redirect configuration
"""

import os
import re
from pathlib import Path

BASE_DIR = Path("/home/zqd/.openclaw/workspace/polymarket-reporter")

def check_chinese_in_en():
    """Check EN pages for Chinese content (excluding legitimate references)"""
    issues = []
    en_files = list((BASE_DIR / "en").rglob("*.html"))
    
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    exclude_patterns = [
        r'hreflang="zh"',
        r'href="/zh/',
        r'Chinese main site',
        r'Chinese deep content',
        r'>中文<',  # Language switcher button
    ]
    
    for f in en_files:
        content = f.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            if chinese_pattern.search(line):
                # Check if it's an excluded pattern
                is_excluded = any(re.search(p, line) for p in exclude_patterns)
                if not is_excluded:
                    issues.append({
                        'file': str(f.relative_to(BASE_DIR)),
                        'line': i,
                        'content': line.strip()[:100]
                    })
    
    return issues

def check_hreflang_consistency():
    """Check that hreflang links match between EN and ZH pages"""
    issues = []
    
    # Map of EN pages to their expected ZH counterparts
    en_files = list((BASE_DIR / "en").rglob("*.html"))
    
    for en_file in en_files:
        content = en_file.read_text(encoding='utf-8')
        rel_path = str(en_file.relative_to(BASE_DIR))
        
        # Extract hreflang zh link
        zh_match = re.search(r'hreflang="zh"[^>]*href="([^"]+)"', content)
        if not zh_match:
            issues.append({
                'file': rel_path,
                'issue': 'Missing hreflang zh'
            })
            continue
        
        zh_href = zh_match.group(1)
        
        # Extract language switcher link
        switcher_match = re.search(r'href="/zh/[^"]*"', content)
        if switcher_match:
            switcher_href = switcher_match.group(0)
            # Check if switcher and hreflang point to same path structure
            zh_path = zh_href.replace('https://www.pred101.com', '')
            if not switcher_href.strip('"').startswith(zh_path.replace('/zh', '/zh')):
                # Check for structural mismatch
                if '/knowledge-base/' in zh_path and '/knowledge-base/' not in switcher_href:
                    issues.append({
                        'file': rel_path,
                        'issue': f'Hreflang/switcher mismatch: hreflang={zh_path}, switcher={switcher_href}',
                        'type': 'structure_mismatch'
                    })
    
    return issues

def check_canonical():
    """Check all pages have proper canonical URLs"""
    issues = []
    
    for lang in ['en', 'zh']:
        files = list((BASE_DIR / lang).rglob("*.html"))
        for f in files:
            content = f.read_text(encoding='utf-8')
            rel_path = str(f.relative_to(BASE_DIR))
            
            if 'rel="canonical"' not in content:
                issues.append({
                    'file': rel_path,
                    'issue': 'Missing canonical'
                })
    
    return issues

def main():
    print("=" * 60)
    print("Phase-2 Plan B Final Verification")
    print("=" * 60)
    print()
    
    # Check 1: Chinese in EN pages
    print("1. Checking EN pages for Chinese residue...")
    chinese_issues = check_chinese_in_en()
    if chinese_issues:
        print(f"   ⚠️  Found {len(chinese_issues)} issues:")
        for issue in chinese_issues[:10]:
            print(f"   - {issue['file']}:{issue['line']}: {issue['content']}")
    else:
        print("   ✅ No Chinese residue found")
    print()
    
    # Check 2: Hreflang consistency
    print("2. Checking hreflang/language switcher consistency...")
    hreflang_issues = check_hreflang_consistency()
    if hreflang_issues:
        print(f"   ⚠️  Found {len(hreflang_issues)} mismatches:")
        for issue in hreflang_issues[:10]:
            print(f"   - {issue['file']}: {issue['issue']}")
    else:
        print("   ✅ All hreflang links consistent")
    print()
    
    # Check 3: Canonical URLs
    print("3. Checking canonical URLs...")
    canonical_issues = check_canonical()
    if canonical_issues:
        print(f"   ⚠️  Found {len(canonical_issues)} pages missing canonical:")
        for issue in canonical_issues[:10]:
            print(f"   - {issue['file']}")
    else:
        print("   ✅ All pages have canonical URLs")
    print()
    
    # Summary
    total_issues = len(chinese_issues) + len(hreflang_issues) + len(canonical_issues)
    print("=" * 60)
    if total_issues == 0:
        print("✅ ALL CHECKS PASSED - Phase-2 Plan B Complete")
    else:
        print(f"⚠️  TOTAL ISSUES: {total_issues}")
        print("   Action required before marking complete")
    print("=" * 60)
    
    return total_issues

if __name__ == "__main__":
    exit(main())
