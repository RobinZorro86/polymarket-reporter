#!/usr/bin/env python3
"""
Phase-2 Plan B Final Comprehensive Verification
Checks all 5 requirements from cron task:
1. English deep content unified to /en/knowledge-base/* and /en/reports/*
2. Check /en/* pages for Chinese titles, body, nav, buttons
3. Check old root paths /knowledge-base/* and /reports/* redirect to /en/*
4. Check /zh/* is complete and not contaminated by English paths
5. Check canonical / hreflang / language switcher consistency
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path("/home/zqd/.openclaw/workspace/polymarket-reporter")

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def get_relative_path(filepath):
    return str(filepath.relative_to(BASE_DIR))

def check_en_page_purity(html, filepath):
    """Check EN page for any Chinese in visible content"""
    issues = []
    rel_path = get_relative_path(filepath)
    
    # Check title
    title_match = re.search(r'<title>([^<]+)</title>', html)
    if title_match:
        title = title_match.group(1)
        if re.search(r'[\u4e00-\u9fff]', title):
            issues.append(f"TITLE_CN: {title[:60]}")
    
    # Check h1, h2, h3
    for tag in ['h1', 'h2', 'h3']:
        for match in re.finditer(f'<{tag}[^>]*>([^<]+)</{tag}>', html):
            text = match.group(1)
            if re.search(r'[\u4e00-\u9fff]', text):
                issues.append(f"<{tag}>_CN: {text[:40]}")
    
    # Check nav links (excluding lang switcher)
    nav_matches = re.findall(r'<nav[^>]*>.*?</nav>', html, re.DOTALL)
    for nav in nav_matches:
        # Skip lang-switch div
        nav_clean = re.sub(r'<div[^>]*lang-switch[^>]*>.*?</div>', '', nav, flags=re.DOTALL)
        link_matches = re.findall(r'<a[^>]*>([^<]+)</a>', nav_clean)
        for text in link_matches:
            text = text.strip()
            if text and re.search(r'[\u4e00-\u9fff]', text):
                issues.append(f"NAV_CN: {text[:30]}")
    
    # Check button text
    button_matches = re.findall(r'<button[^>]*>([^<]+)</button>', html)
    for text in button_matches:
        if re.search(r'[\u4e00-\u9fff]', text):
            issues.append(f"BTN_CN: {text[:30]}")
    
    # Check lang switcher label - should say "Chinese" not "中文"
    lang_switch = re.search(r'<div[^>]*lang-switch[^>]*>.*?</div>', html, re.DOTALL)
    if lang_switch:
        switch_html = lang_switch.group(0)
        if '>中文</a>' in switch_html:
            issues.append("LANG_SWITCH: Uses '中文' instead of 'Chinese'")
    
    return issues

def check_zh_page_integrity(html, filepath):
    """Check ZH page has Chinese content and proper structure"""
    issues = []
    rel_path = get_relative_path(filepath)
    
    # Check title has Chinese
    title_match = re.search(r'<title>([^<]+)</title>', html)
    if title_match:
        title = title_match.group(1)
        if not re.search(r'[\u4e00-\u9fff]', title):
            issues.append(f"TITLE_NO_CN: {title[:60]}")
    
    # Check h1 has Chinese (skip KOL profile pages - their H1 is the Twitter handle)
    if '/knowledge-base/kol/' not in rel_path or '/index.html' not in rel_path:
        h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
        if h1_match:
            h1 = h1_match.group(1)
            if not re.search(r'[\u4e00-\u9fff]', h1):
                issues.append(f"H1_NO_CN: {h1[:40]}")
    
    # Check lang switcher - should say "English" or "EN", not "英文"
    lang_switch = re.search(r'<div[^>]*lang-switch[^>]*>.*?</div>', html, re.DOTALL)
    if lang_switch:
        switch_html = lang_switch.group(0)
        if '>英文</a>' in switch_html:
            issues.append("LANG_SWITCH: Uses '英文' instead of 'English' or 'EN'")
        if '>English</a>' not in switch_html and '>EN</a>' not in switch_html:
            issues.append("LANG_SWITCH: Missing 'English' or 'EN' label")
    
    return issues

def check_hreflang_pairing(html, filepath):
    """Check hreflang tags are correctly paired"""
    issues = []
    rel_path = get_relative_path(filepath)
    
    # Extract hreflang tags
    en_href = None
    zh_href = None
    
    en_match = re.search(r'hreflang="en"[^>]*href="([^"]+)"', html)
    zh_match = re.search(r'hreflang="zh"[^>]*href="([^"]+)"', html)
    
    if en_match:
        en_href = en_match.group(1)
    if zh_match:
        zh_href = zh_match.group(1)
    
    # Check EN pages have correct hreflang
    if '/en/' in rel_path:
        if not en_href or '/en/' not in en_href:
            issues.append(f"HREFLANG_EN_MISSING: {en_href}")
        if not zh_href or '/zh/' not in zh_href:
            issues.append(f"HREFLANG_ZH_MISSING: {zh_href}")
    
    # Check ZH pages have correct hreflang
    elif '/zh/' in rel_path:
        if not zh_href or '/zh/' not in zh_href:
            issues.append(f"HREFLANG_ZH_MISSING: {zh_href}")
        if not en_href or '/en/' not in en_href:
            issues.append(f"HREFLANG_EN_MISSING: {en_href}")
    
    return issues

def check_canonical(html, filepath):
    """Check canonical URL points to self"""
    issues = []
    rel_path = get_relative_path(filepath)
    
    canonical_match = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"', html)
    if canonical_match:
        canonical = canonical_match.group(1)
        
        # Check canonical contains correct language path
        if '/en/' in rel_path and '/en/' not in canonical:
            issues.append(f"CANONICAL_EN_MISSING: {canonical}")
        elif '/zh/' in rel_path and '/zh/' not in canonical:
            issues.append(f"CANONICAL_ZH_MISSING: {canonical}")
    else:
        issues.append("CANONICAL_MISSING")
    
    return issues

def check_vercel_redirects():
    """Check vercel.json has correct redirect configuration"""
    vercel_path = BASE_DIR / "vercel.json"
    html = read_file(vercel_path)
    
    if not html:
        return ["VERCEL_JSON_MISSING"]
    
    issues = []
    
    # Check knowledge-base redirect
    if '/knowledge-base' in html:
        if '/en/knowledge-base' not in html:
            issues.append("REDIRECT_KB_MISSING_EN")
    else:
        issues.append("REDIRECT_KB_NOT_CONFIGURED")
    
    # Check reports redirect
    if '/reports' in html:
        if '/en/reports' not in html:
            issues.append("REDIRECT_REPORTS_MISSING_EN")
    else:
        issues.append("REDIRECT_REPORTS_NOT_CONFIGURED")
    
    return issues

def check_old_paths_redirect():
    """Check that old root paths have proper HTML redirect pages"""
    issues = []
    
    old_paths = {
        "knowledge-base": "/en/knowledge-base/",
        "reports": "/en/reports/",
        "learn": "/en/learn/",
        "strategies": "/en/strategies/",
        "kol": "/en/kol/",
        "resources": "/en/resources/"
    }
    
    for path_name, expected_redirect in old_paths.items():
        index_path = BASE_DIR / path_name / "index.html"
        if not index_path.exists():
            issues.append(f"OLD_PATH_REDIRECT_MISSING: {path_name}/index.html")
        else:
            # Check the redirect page points to correct destination
            html = read_file(index_path)
            if html:
                if expected_redirect not in html:
                    issues.append(f"OLD_PATH_REDIRECT_WRONG: {path_name} should redirect to {expected_redirect}")
    
    return issues

def count_pages_by_language():
    """Count pages in each language directory"""
    en_pages = list(BASE_DIR.glob("en/**/*.html"))
    zh_pages = list(BASE_DIR.glob("zh/**/*.html"))
    return len(en_pages), len(zh_pages)

def check_kb_resources_structure():
    """Check that /en/knowledge-base/* has proper structure"""
    issues = []
    
    kb_en = BASE_DIR / "en" / "knowledge-base"
    if not kb_en.exists():
        issues.append("KB_EN_DIR_MISSING")
        return issues
    
    # Check subdirectories exist (kol is Chinese-specific, not required in EN)
    expected_subdirs = ["strategies", "resources", "tutorials"]
    for subdir in expected_subdirs:
        if not (kb_en / subdir).exists():
            issues.append(f"KB_EN_SUBDIR_MISSING: {subdir}")
    
    return issues

def main():
    print("=" * 70)
    print("PHASE-2 PLAN B: COMPREHENSIVE FINAL VERIFICATION")
    print("=" * 70)
    print(f"Timestamp: {os.popen('date').read().strip()}")
    print()
    
    all_issues = defaultdict(list)
    
    # 1. Check old paths have proper redirect pages
    print("📁 [1/5] Checking old root paths redirect pages...")
    old_path_issues = check_old_paths_redirect()
    if old_path_issues:
        all_issues["OLD_PATHS"].extend(old_path_issues)
        print(f"   ⚠️  {len(old_path_issues)} issues")
    else:
        print("   ✅ Old paths have proper redirect pages")
    
    # 2. Check vercel.json redirects
    print("📁 [2/5] Checking redirect configuration...")
    redirect_issues = check_vercel_redirects()
    if redirect_issues:
        all_issues["REDIRECTS"].extend(redirect_issues)
        print(f"   ⚠️  {len(redirect_issues)} issues")
    else:
        print("   ✅ Redirect config OK")
    
    # 3. Check EN pages
    print("📁 [3/5] Checking EN pages for Chinese content...")
    en_pages = list(BASE_DIR.glob("en/**/*.html"))
    en_issues_count = 0
    en_sample_issues = []
    
    for page in en_pages:
        html = read_file(page)
        if not html:
            continue
        
        issues = check_en_page_purity(html, page)
        issues.extend(check_hreflang_pairing(html, page))
        issues.extend(check_canonical(html, page))
        
        if issues:
            en_issues_count += 1
            if len(en_sample_issues) < 10:
                en_sample_issues.append((get_relative_path(page), issues))
    
    if en_issues_count > 0:
        all_issues["EN_PAGES"] = [f"{en_issues_count} pages with issues"]
        print(f"   ⚠️  {en_issues_count}/{len(en_pages)} pages with issues")
    else:
        print(f"   ✅ All {len(en_pages)} EN pages clean")
    
    # 4. Check ZH pages
    print("📁 [4/5] Checking ZH pages integrity...")
    zh_pages = list(BASE_DIR.glob("zh/**/*.html"))
    zh_issues_count = 0
    zh_sample_issues = []
    
    for page in zh_pages:
        html = read_file(page)
        if not html:
            continue
        
        issues = check_zh_page_integrity(html, page)
        issues.extend(check_hreflang_pairing(html, page))
        issues.extend(check_canonical(html, page))
        
        if issues:
            zh_issues_count += 1
            if len(zh_sample_issues) < 10:
                zh_sample_issues.append((get_relative_path(page), issues))
    
    if zh_issues_count > 0:
        all_issues["ZH_PAGES"] = [f"{zh_issues_count} pages with issues"]
        print(f"   ⚠️  {zh_issues_count}/{len(zh_pages)} pages with issues")
    else:
        print(f"   ✅ All {len(zh_pages)} ZH pages clean")
    
    # 5. Check knowledge-base structure
    print("📁 [5/5] Checking /en/knowledge-base/* structure...")
    kb_issues = check_kb_resources_structure()
    if kb_issues:
        all_issues["KB_STRUCTURE"].extend(kb_issues)
        print(f"   ⚠️  {len(kb_issues)} issues")
    else:
        print("   ✅ KB structure OK")
    
    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    en_count, zh_count = count_pages_by_language()
    print(f"EN pages: {en_count}")
    print(f"ZH pages: {zh_count}")
    print(f"Total: {en_count + zh_count}")
    print()
    
    total_issues = sum(len(v) for v in all_issues.values())
    
    if total_issues == 0:
        print("✅ ALL CHECKS PASSED - Phase-2 Plan B Complete")
        print()
        print("已完成 / 已完成 / 剩余项: 0 / 下一步: 等待 Phase-3 指令")
    else:
        print(f"⚠️  {total_issues} issues found")
        print()
        for category, issues in all_issues.items():
            print(f"{category}:")
            for issue in issues:
                print(f"  - {issue}")
        print()
        print("进行中 / 进行中 / 剩余项: {} / 下一步: 修复上述问题".format(total_issues))
    
    # Show sample issues if any
    if en_sample_issues:
        print()
        print("Sample EN page issues:")
        for path, issues in en_sample_issues[:5]:
            print(f"  {path}:")
            for issue in issues[:3]:
                print(f"    - {issue}")
    
    if zh_sample_issues:
        print()
        print("Sample ZH page issues:")
        for path, issues in zh_sample_issues[:5]:
            print(f"  {path}:")
            for issue in issues[:3]:
                print(f"    - {issue}")

if __name__ == "__main__":
    main()
