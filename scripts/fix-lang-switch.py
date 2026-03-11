#!/usr/bin/env python3
"""
Phase-2 Plan B 收尾脚本：语言切换按钮统一修复
目标：为所有缺少 lang-switch 的 /en/* 深层页面添加语言切换按钮
"""

import os
import re
from pathlib import Path

BASE_DIR = Path("/home/zqd/.openclaw/workspace/polymarket-reporter")

# 需要添加 lang-switch 的页面列表
PAGES_TO_FIX = [
    "en/learn/day1/index.html",
    "en/learn/day2/index.html",
    "en/learn/day3/index.html",
    "en/learn/day4/index.html",
    "en/learn/day5/index.html",
    "en/learn/day6/index.html",
    "en/learn/day7/index.html",
    "en/knowledge-base/resources/index.html",
    "en/knowledge-base/strategies/index.html",
    "en/knowledge-base/tutorials/index.html",
    "en/reports/simmer/index.html",
]

# 语言切换按钮 HTML 片段
LANG_SWITCH_EN = '<div class="lang-switch"><a href="{en_path}" class="active">EN</a><a href="{zh_path}">中文</a></div>'

def get_zh_path(en_path):
    """将英文路径转换为对应的中文路径"""
    return en_path.replace("en/", "zh/", 1)

def add_lang_switch(file_path):
    """在导航栏末尾添加语言切换按钮"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 计算对应的中文路径
    rel_path = str(file_path.relative_to(BASE_DIR))
    zh_path = get_zh_path(rel_path)
    
    # 构建语言切换 HTML
    lang_switch_html = LANG_SWITCH_EN.format(
        en_path=rel_path.rsplit('/index.html', 1)[0] + '/',
        zh_path=zh_path.rsplit('/index.html', 1)[0] + '/'
    )
    
    # 查找导航栏末尾位置（</nav> 之前）
    nav_pattern = r'(<nav[^>]*>.*?)(</nav>)'
    match = re.search(nav_pattern, content, re.DOTALL)
    
    if match:
        nav_content = match.group(1)
        # 检查是否已存在 lang-switch
        if 'lang-switch' in nav_content:
            print(f"⚠️  {rel_path}: 已存在 lang-switch，跳过")
            return False
        
        # 在导航栏末尾添加 lang-switch
        new_nav = nav_content + lang_switch_html
        content = content.replace(match.group(1), new_nav)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {rel_path}: 已添加语言切换按钮 → {zh_path}")
        return True
    else:
        print(f"❌ {rel_path}: 未找到导航栏，跳过")
        return False

def main():
    print("=" * 60)
    print("Phase-2 Plan B 收尾：语言切换按钮统一修复")
    print("=" * 60)
    
    fixed_count = 0
    for page in PAGES_TO_FIX:
        file_path = BASE_DIR / page
        if file_path.exists():
            if add_lang_switch(file_path):
                fixed_count += 1
        else:
            print(f"⚠️  {page}: 文件不存在")
    
    print("=" * 60)
    print(f"完成：{fixed_count}/{len(PAGES_TO_FIX)} 页面已修复")
    print("=" * 60)

if __name__ == "__main__":
    main()
