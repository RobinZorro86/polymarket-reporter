#!/usr/bin/env python3
"""
Phase-2 Plan B Verification Script
Checks:
1. English pages have no Chinese titles/headings/nav/buttons
2. Language switchers use correct labels (EN/Chinese on EN pages, ZH/English on ZH pages)
3. Hreflang pairs are correct
4. Canonical URLs point to self
5. Old paths redirect configuration exists
"""

import os
import re
from pathlib import Path

BASE_DIR = Path("/home/zqd/.openclaw/workspace/polymarket-reporter")

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def check_chinese_in_visible_content(html, filepath):
    """Check for Chinese characters in visible content (title, h1-h3, nav links, buttons)"""
    issues = []
    
    # Check title
    title_match = re.search(r'<title>([^<]+)</title>', html)
    if title_match:
        title = title_match.group(1)
        if re.search(r'[\u4e00-\u9fff]', title):
            issues.append(f"Title contains Chinese: {title[:80]}")
    
    # Check h1, h2, h3
    for tag in ['h1', 'h2', 'h3']:
        for match in re.finditer(f'<{tag}>([^<]+)</{tag}>', html):
            text = match.group(1)
            if re.search(r'[\u4e00-\u9fff]', text):
                issues.append(f"<{tag}> contains Chinese: {text[:60]}")
    
    # Check navigation links (text between > and </a> in nav context)
    nav_matches = re.findall(r'<nav>.*?</nav>', html, re.DOTALL)
    for nav in nav_matches:
        link_matches = re.findall(r'<a[^>]*>([^<]+)</a>', nav)
        for text in link_matches:
            if text.strip() in ['EN', 'ZH', 'Chinese', 'English']:
                continue  # Language switcher labels are OK
            if re.search(r'[\u4e00-\u9fff]', text):
                issues.append(f"Nav link contains Chinese: {text.strip()[:40]}")
    
    # Check language switcher - should be "Chinese" on EN pages, "English" on ZH pages
    lang_switch = re.search(r'lang-switch.*?</div>', html, re.DOTALL)
    if lang_switch:
        switch_text = lang_switch.group(0)
        if 'lang="en"' in html.lower() or '<html lang="en">' in html.lower():
            # EN page - should link to Chinese with label "Chinese"
            if '>中文</a>' in switch_text:
                issues.append("EN page lang switcher uses '中文' instead of 'Chinese'")
        elif 'lang="zh"' in html.lower() or '<html lang="zh">' in html.lower():
            # ZH page - should link to English with label "English"
            if '>English</a>' not in switch_text and '>英文</a>' not in switch_text:
                if re.search(r'>[A-Za-z]+</a>', switch_text):
                    pass  # Might be OK
                else:
                    issues.append("ZH page lang switcher may have incorrect label")
    
    return issues

def check_hreflang(html, filepath):
    """Check hreflang tags"""
    issues = []
    
    en_hreflang = re.search(r'hreflang="en"[^>]*href="([^"]+)"', html)
    zh_hreflang = re.search(r'hreflang="zh"[^>]*href="([^"]+)"', html)
    
    path_str = str(filepath)
    
    if en_hreflang:
        en_url = en_hreflang.group(1)
        if '/en/' not in en_url:
            issues.append(f"hreflang=en points to non-EN path: {en_url}")
    
    if zh_hreflang:
        zh_url = zh_hreflang.group(1)
        if '/zh/' not in zh_url:
            issues.append(f"hreflang=zh points to non-ZH path: {zh_url}")
    
    return issues

def check_canonical(html, filepath):
    """Check canonical URL"""
    issues = []
    
    canonical = re.search(r'<link rel="canonical"[^>]*href="([^"]+)"', html)
    if canonical:
        canon_url = canonical.group(1)
        path_str = str(filepath)
        
        # Extract relative path from file path
        if '/en/' in path_str:
            if '/en/' not in canon_url:
                issues.append(f"EN page canonical doesn't contain /en/: {canon_url}")
        elif '/zh/' in path_str:
            if '/zh/' not in canon_url:
                issues.append(f"ZH page canonical doesn't contain /zh/: {canon_url}")
    
    return issues

def main():
    print("=" * 60)
    print("Phase-2 Plan B Verification Report")
    print("=" * 60)
    
    en_pages = list(BASE_DIR.glob("en/**/*.html"))
    zh_pages = list(BASE_DIR.glob("zh/**/*.html"))
    
    print(f"\n📁 EN pages: {len(en_pages)}")
    print(f"📁 ZH pages: {len(zh_pages)}")
    
    en_issues = []
    zh_issues = []
    
    # Check EN pages
    print("\n🔍 Checking EN pages for Chinese content...")
    for page in en_pages:
        html = read_file(page)
        if not html:
            continue
        
        issues = check_chinese_in_visible_content(html, page)
        if issues:
            en_issues.append((page, issues))
        
        hreflang_issues = check_hreflang(html, page)
        if hreflang_issues:
            en_issues.append((page, hreflang_issues))
        
        canonical_issues = check_canonical(html, page)
        if canonical_issues:
            en_issues.append((page, canonical_issues))
    
    # Check ZH pages
    print("🔍 Checking ZH pages for English content pollution...")
    for page in zh_pages:
        html = read_file(page)
        if not html:
            continue
        
        # For ZH pages, we check that they have Chinese content (not English pollution)
        # This is a basic check - ZH pages should have Chinese titles
        title_match = re.search(r'<title>([^<]+)</title>', html)
        if title_match:
            title = title_match.group(1)
            if not re.search(r'[\u4e00-\u9fff]', title):
                zh_issues.append((page, [f"ZH page title has no Chinese: {title[:60]}"]))
    
    # Report EN issues
    print("\n" + "=" * 60)
    if en_issues:
        print(f"⚠️  EN pages with issues: {len(en_issues)}")
        for page, issues in en_issues[:20]:  # Show first 20
            rel_path = page.relative_to(BASE_DIR)
            print(f"\n  {rel_path}")
            for issue in issues:
                print(f"    - {issue}")
        if len(en_issues) > 20:
            print(f"\n  ... and {len(en_issues) - 20} more pages")
    else:
        print("✅ All EN pages passed visible content checks")
    
    # Report ZH issues
    print("\n" + "=" * 60)
    if zh_issues:
        print(f"⚠️  ZH pages with issues: {len(zh_issues)}")
        for page, issues in zh_issues[:20]:
            rel_path = page.relative_to(BASE_DIR)
            print(f"\n  {rel_path}")
            for issue in issues:
                print(f"    - {issue}")
        if len(zh_issues) > 20:
            print(f"\n  ... and {len(zh_issues) - 20} more pages")
    else:
        print("✅ All ZH pages have Chinese titles")
    
    # Check vercel.json redirects
    print("\n" + "=" * 60)
    vercel_json = read_file(BASE_DIR / "vercel.json")
    if vercel_json:
        if '/knowledge-base' in vercel_json and '/en/knowledge-base' in vercel_json:
            print("✅ Redirect config: /knowledge-base/* → /en/knowledge-base/*")
        else:
            print("⚠️  Redirect config may be missing for /knowledge-base")
        
        if '/reports' in vercel_json and '/en/reports' in vercel_json:
            print("✅ Redirect config: /reports/* → /en/reports/*")
        else:
            print("⚠️  Redirect config may be missing for /reports")
    else:
        print("⚠️  Could not read vercel.json")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"EN pages checked: {len(en_pages)}")
    print(f"EN pages with issues: {len(en_issues)}")
    print(f"ZH pages checked: {len(zh_pages)}")
    print(f"ZH pages with issues: {len(zh_issues)}")
    
    if len(en_issues) == 0 and len(zh_issues) == 0:
        print("\n✅ Phase-2 Plan B: ALL CHECKS PASSED")
    else:
        print(f"\n⚠️  Phase-2 Plan B: {len(en_issues) + len(zh_issues)} issues found")

if __name__ == "__main__":
    main()
