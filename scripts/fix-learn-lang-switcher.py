#!/usr/bin/env python3
"""
Phase-2 Plan B 收尾验证脚本 - 学习路径语言切换器修复
检查 zh/learn/day* 页面是否缺少语言切换器，并自动修复
"""

import os
import re

BASE_DIR = "/home/zqd/.openclaw/workspace/polymarket-reporter"

# 需要修复的中文学习路径页面
ZH_LEARN_PAGES = [
    "zh/learn/day1/index.html",
    "zh/learn/day2/index.html",
    "zh/learn/day3/index.html",
    "zh/learn/day4/index.html",
    "zh/learn/day5/index.html",
    "zh/learn/day6/index.html",
    "zh/learn/day7/index.html",
]

# 语言切换器 HTML（中文页面用）
LANG_SWITCHER_ZH = '<div class="lang-switch"><a href="/en/" class="active">EN</a><a href="/zh/" class="active">中文</a></div>'

def fix_lang_switcher(filepath):
    """修复中文页面的语言切换器"""
    full_path = os.path.join(BASE_DIR, filepath)
    
    if not os.path.exists(full_path):
        print(f"❌ 文件不存在：{filepath}")
        return False
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有语言切换器
    if 'lang-switch' in content and 'English' in content:
        print(f"✅ {filepath} - 已有语言切换器")
        return True
    
    # 检查是否有 EN 链接但缺少中文切换器
    if 'lang-switch' in content:
        # 已有 lang-switch 但方向可能不对
        if 'href="/zh/" class="active">中文</a>' not in content:
            # 修复：添加中文链接
            old_switcher = '<div class="lang-switch"><a href="/en/">EN</a><a href="/zh/" class="active">中文</a></div>'
            if old_switcher in content:
                content = content.replace(old_switcher, LANG_SWITCHER_ZH)
                print(f"🔧 {filepath} - 修复语言切换器")
            else:
                print(f"⚠️ {filepath} - 语言切换器格式异常，需手动检查")
                return False
    else:
        # 完全没有语言切换器，需要添加
        # 查找 nav 标签并插入
        nav_pattern = r'(<nav>.*?</nav>)'
        match = re.search(nav_pattern, content, re.DOTALL)
        
        if match:
            old_nav = match.group(1)
            # 在 nav 末尾添加语言切换器
            new_nav = old_nav.rstrip('</nav>') + LANG_SWITCHER_ZH + '</nav>'
            content = content.replace(old_nav, new_nav)
            print(f"🔧 {filepath} - 添加语言切换器")
        else:
            print(f"❌ {filepath} - 未找到 nav 标签")
            return False
    
    # 写回文件
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print("=" * 60)
    print("Phase-2 Plan B 收尾验证 - 学习路径语言切换器修复")
    print("=" * 60)
    
    fixed_count = 0
    for page in ZH_LEARN_PAGES:
        if fix_lang_switcher(page):
            fixed_count += 1
    
    print("=" * 60)
    print(f"完成：{fixed_count}/{len(ZH_LEARN_PAGES)} 页面已修复")
    print("=" * 60)

if __name__ == "__main__":
    main()
