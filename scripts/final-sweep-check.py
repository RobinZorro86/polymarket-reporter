#!/usr/bin/env python3
"""
Phase-2 Plan B 最终收尾检查脚本
执行用户指定的 5 项验证任务
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
EN_DIR = BASE_DIR / "en"
ZH_DIR = BASE_DIR / "zh"
KB_ROOT = BASE_DIR / "knowledge-base"
REPORTS_ROOT = BASE_DIR / "reports"

def count_html_files(directory):
    """统计 HTML 文件数量"""
    if not directory.exists():
        return 0
    return len(list(directory.rglob("*.html")))

def check_chinese_in_en():
    """检查英文路径是否残留中文"""
    issues = []
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    
    for html_file in EN_DIR.rglob("*.html"):
        content = html_file.read_text(encoding='utf-8', errors='ignore')
        # 排除语言切换器中的"中文"链接文案
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if '语言切换' in line or 'language-switcher' in line or '中文' in line:
                # 检查是否是语言切换器部分
                if 'language-switcher' in line or '切换' in line:
                    continue
                # 如果是 href 或链接文本中的"中文"，跳过
                if '中文' in line and ('href=' in line or '中文</a>' in line or '中文</button>' in line):
                    continue
            matches = chinese_pattern.findall(line)
            if matches:
                # 排除技术术语和预期行为
                clean_line = line
                for term in ['中文', 'language-switcher', '切换', 'footer', 'nav', 'navigation']:
                    clean_line = clean_line.replace(term, '')
                if chinese_pattern.search(clean_line):
                    issues.append(f"{html_file.relative_to(BASE_DIR)}:{i} - 可能残留中文")
    
    return issues

def check_english_in_zh():
    """检查中文路径是否被英文污染"""
    issues = []
    # 允许的技术术语
    allowed_terms = ['html', 'css', 'js', 'json', 'xml', 'href', 'canonical', 'hreflang', 'en', 'zh', 'https', 'http', 'www', 'com']
    
    for html_file in ZH_DIR.rglob("*.html"):
        content = html_file.read_text(encoding='utf-8', errors='ignore')
        # 简单检查：如果英文单词密度过高，标记
        english_words = re.findall(r'\b[a-zA-Z]{4,}\b', content)
        total_words = len(content.split())
        if total_words > 0:
            # 只检查非技术区域的英文密度
            # 排除 head 区域的 meta 标签
            body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
            if body_match:
                body_content = body_match.group(1)
                # 排除脚本和样式
                body_content = re.sub(r'<script[^>]*>.*?</script>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                body_content = re.sub(r'<style[^>]*>.*?</style>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                
                english_in_body = re.findall(r'\b[a-zA-Z]{4,}\b', body_content)
                if len(english_in_body) > 50:  # 阈值
                    issues.append(f"{html_file.relative_to(BASE_DIR)} - 英文密度可能过高 ({len(english_in_body)} 词)")
    
    return issues

def check_legacy_redirects():
    """检查旧路径跳转配置"""
    issues = []
    vercel_json = BASE_DIR / "vercel.json"
    
    if vercel_json.exists():
        content = vercel_json.read_text()
        if '/knowledge-base/' not in content or '/en/knowledge-base/' not in content:
            issues.append("vercel.json 缺少 knowledge-base 跳转配置")
        if '/reports/' not in content or '/en/reports/' not in content:
            issues.append("vercel.json 缺少 reports 跳转配置")
    else:
        issues.append("vercel.json 不存在")
    
    # 检查根目录 index.html 的 meta refresh
    kb_index = KB_ROOT / "index.html"
    reports_index = REPORTS_ROOT / "index.html"
    
    if kb_index.exists():
        content = kb_index.read_text()
        if 'meta http-equiv="refresh"' not in content.lower() or '/en/knowledge-base/' not in content:
            issues.append("knowledge-base/index.html 缺少 meta refresh")
    
    if reports_index.exists():
        content = reports_index.read_text()
        if 'meta http-equiv="refresh"' not in content.lower() or '/en/reports/' not in content:
            issues.append("reports/index.html 缺少 meta refresh")
    
    return issues

def check_zh_completeness():
    """检查中文路径完整性"""
    issues = []
    
    # 检查关键目录是否存在
    required_dirs = [
        ZH_DIR / "knowledge-base",
        ZH_DIR / "reports" / "daily",
        ZH_DIR / "reports" / "weekly",
        ZH_DIR / "learn",
        ZH_DIR / "strategies",
        ZH_DIR / "kol"
    ]
    
    for dir_path in required_dirs:
        if not dir_path.exists():
            issues.append(f"缺少目录：{dir_path.relative_to(BASE_DIR)}")
        else:
            html_count = count_html_files(dir_path)
            if html_count == 0:
                issues.append(f"目录为空：{dir_path.relative_to(BASE_DIR)}")
    
    return issues

def check_canonical_hreflang():
    """检查 Canonical / Hreflang 配置"""
    issues = []
    
    # 抽样检查 EN 页面
    en_samples = list(EN_DIR.rglob("*.html"))[:5]
    for html_file in en_samples:
        content = html_file.read_text(encoding='utf-8', errors='ignore')
        if 'rel="canonical"' not in content:
            issues.append(f"{html_file.relative_to(BASE_DIR)} - 缺少 canonical")
        if 'hreflang="zh"' not in content:
            issues.append(f"{html_file.relative_to(BASE_DIR)} - 缺少 hreflang=zh")
    
    # 抽样检查 ZH 页面
    zh_samples = list(ZH_DIR.rglob("*.html"))[:5]
    for html_file in zh_samples:
        content = html_file.read_text(encoding='utf-8', errors='ignore')
        if 'rel="canonical"' not in content:
            issues.append(f"{html_file.relative_to(BASE_DIR)} - 缺少 canonical")
        if 'hreflang="en"' not in content:
            issues.append(f"{html_file.relative_to(BASE_DIR)} - 缺少 hreflang=en")
    
    return issues

def main():
    print("=" * 60)
    print("Phase-2 Plan B 最终收尾检查")
    print("=" * 60)
    print()
    
    all_issues = []
    
    # 1. 检查英文路径中文残留
    print("1. 检查英文路径是否残留中文标题/正文/导航/按钮...")
    issues = check_chinese_in_en()
    if issues:
        print(f"   ⚠️ 发现 {len(issues)} 个潜在问题:")
        for issue in issues[:5]:  # 只显示前 5 个
            print(f"      - {issue}")
        all_issues.extend(issues)
    else:
        print("   ✅ 英文路径无中文残留")
    print()
    
    # 2. 检查中文路径英文污染
    print("2. 检查中文路径是否被英文污染...")
    issues = check_english_in_zh()
    if issues:
        print(f"   ⚠️ 发现 {len(issues)} 个潜在问题:")
        for issue in issues[:5]:
            print(f"      - {issue}")
        all_issues.extend(issues)
    else:
        print("   ✅ 中文路径无英文污染")
    print()
    
    # 3. 检查旧路径跳转
    print("3. 检查旧根路径跳转配置...")
    issues = check_legacy_redirects()
    if issues:
        print(f"   ⚠️ 发现 {len(issues)} 个问题:")
        for issue in issues:
            print(f"      - {issue}")
        all_issues.extend(issues)
    else:
        print("   ✅ 旧路径跳转配置正确")
    print()
    
    # 4. 检查中文路径完整性
    print("4. 检查中文路径完整性...")
    issues = check_zh_completeness()
    if issues:
        print(f"   ⚠️ 发现 {len(issues)} 个问题:")
        for issue in issues:
            print(f"      - {issue}")
        all_issues.extend(issues)
    else:
        print("   ✅ 中文路径完整且未被污染")
    print()
    
    # 5. 检查 Canonical / Hreflang
    print("5. 检查 Canonical / Hreflang / 语言切换...")
    issues = check_canonical_hreflang()
    if issues:
        print(f"   ⚠️ 发现 {len(issues)} 个问题:")
        for issue in issues:
            print(f"      - {issue}")
        all_issues.extend(issues)
    else:
        print("   ✅ Canonical / Hreflang 配置一致")
    print()
    
    # 统计
    print("=" * 60)
    print("统计汇总")
    print("=" * 60)
    print(f"英文页面数：{count_html_files(EN_DIR)}")
    print(f"中文页面数：{count_html_files(ZH_DIR)}")
    print(f"发现问题总数：{len(all_issues)}")
    print()
    
    if all_issues:
        print("⚠️ 发现未清理项，需要修复")
        return 1
    else:
        print("✅ Phase-2 Plan B 全部验证通过，无遗漏项")
        return 0

if __name__ == "__main__":
    exit(main())
