#!/usr/bin/env python3
"""
Phase-2 Plan B 收尾验证脚本 - 检查并修复 zh/knowledge-base/* 深层页面的语言切换器
"""

import os
import re

BASE_DIR = "/home/zqd/.openclaw/workspace/polymarket-reporter"

# 需要检查的中文深层页面目录
ZH_DEEP_DIRS = [
    "zh/knowledge-base/strategies",
    "zh/knowledge-base/kol",
    "zh/knowledge-base/resources",
]

def check_page(filepath):
    """检查页面是否有正确的语言切换器"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否有 hreflang="en"
    has_hreflang_en = 'hreflang="en"' in content
    
    # 检查是否有 English 链接
    has_english_link = 'English' in content or 'href="/en/' in content
    
    # 检查语言切换器
    has_lang_switch = 'lang-switch' in content
    
    return has_hreflang_en, has_english_link, has_lang_switch

def add_lang_switcher(filepath):
    """为中文页面添加语言切换器"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 nav 标签
    nav_pattern = r'(<nav>.*?</nav>)'
    match = re.search(nav_pattern, content, re.DOTALL)
    
    if not match:
        print(f"  ❌ 未找到 nav 标签")
        return False
    
    old_nav = match.group(1)
    
    # 检查是否已有 lang-switch
    if 'lang-switch' in old_nav:
        print(f"  ✅ 已有语言切换器")
        return True
    
    # 构建语言切换器（中文页面）
    lang_switcher = '<div class="lang-switch"><a href="/en/">EN</a><a href="/zh/" class="active">中文</a></div>'
    
    # 插入到 nav 末尾
    new_nav = old_nav.rstrip('</nav>') + lang_switcher + '</nav>'
    content = content.replace(old_nav, new_nav)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print("=" * 60)
    print("Phase-2 Plan B 验证 - zh/knowledge-base/* 深层页面语言切换器")
    print("=" * 60)
    
    total = 0
    fixed = 0
    
    for zh_dir in ZH_DEEP_DIRS:
        zh_path = os.path.join(BASE_DIR, zh_dir)
        if not os.path.exists(zh_path):
            continue
        
        print(f"\n📁 检查 {zh_dir}/")
        
        for root, dirs, files in os.walk(zh_path):
            for file in files:
                if not file.endswith('.html'):
                    continue
                
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, BASE_DIR)
                total += 1
                
                has_hreflang, has_english, has_switch = check_page(filepath)
                
                if has_switch:
                    print(f"  ✅ {rel_path}")
                    fixed += 1
                else:
                    print(f"  🔧 {rel_path} - 添加语言切换器", end="")
                    if add_lang_switcher(filepath):
                        print(" 完成")
                        fixed += 1
                    else:
                        print(" 失败")
    
    print("=" * 60)
    print(f"完成：{fixed}/{total} 页面已检查/修复")
    print("=" * 60)

if __name__ == "__main__":
    main()
