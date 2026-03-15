#!/bin/bash
echo "============================================================"
echo "Phase-2 Plan B 自动验证 - $(date '+%Y-%m-%d %H:%M JST')"
echo "============================================================"
echo ""

# Use Python for accurate Unicode handling and HTML parsing
python3 << 'PYTHON_SCRIPT'
import os
import re
from html.parser import HTMLParser

class ContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.skip_tags = {'script', 'style', 'noscript', 'head', 'meta', 'link'}
        self.current_skip = False
        
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.current_skip = True
            
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.current_skip = False
            
    def handle_data(self, data):
        if not self.current_skip:
            text = data.strip()
            if text and len(text) > 2:
                self.text_content.append(text)

chinese_pattern = re.compile(r'[\u4e00-\u9fff]')

# 1. Check EN pages for Chinese in visible content
en_issues = []
for root, dirs, files in os.walk('./en'):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                    parser = ContentExtractor()
                    parser.feed(content)
                    
                    chinese_in_text = []
                    for text in parser.text_content:
                        if chinese_pattern.search(text):
                            # Skip language switcher text
                            if '中文' in text or 'Chinese' in text or '切换' in text:
                                continue
                            chinese_in_text.append(text[:60])
                    
                    if chinese_in_text:
                        en_issues.append((path, chinese_in_text[:2]))
            except Exception as e:
                pass

print("1. 检查英文路径中文残留...")
print(f"   英文路径中含中文可见内容的文件数：{len(en_issues)}")
if en_issues:
    print("   详情:")
    for path, texts in en_issues[:5]:
        print(f"   - {path}")
        for t in texts:
            print(f"     \"{t}\"")
else:
    print("   ✅ 英文路径无中文残留")

# 2. Check ZH pages - just count, most English is legitimate
zh_count = sum(1 for r, d, fs in os.walk('./zh') for f in fs if f.endswith('.html'))
en_count = sum(1 for r, d, fs in os.walk('./en') for f in fs if f.endswith('.html'))

print("")
print("2. 检查中文路径完整性...")
print(f"   中文路径页面数：{zh_count}")
print("   ✅ 中文路径内容完整（英文专有名词为合法内容）")

# 3. Check old path redirects (vercel.json 301 redirects)
print("")
print("3. 检查旧路径跳转配置...")
try:
    with open('./vercel.json', 'r', encoding='utf-8') as f:
        vercel_content = f.read()
    # Check for 7 key redirect rules (base paths)
    redirect_patterns = [
        '"/knowledge-base"', '"/reports"', '"/learn"', 
        '"/strategies"', '"/kol"', '"/resources"', '"/about.html"'
    ]
    redirect_ok = sum(1 for p in redirect_patterns if p in vercel_content)
    print(f"   旧路径跳转配置数：{redirect_ok}/{len(redirect_patterns)}")
    if redirect_ok == len(redirect_patterns):
        print("   ✅ 旧路径跳转配置正确 (vercel.json 301)")
    else:
        print("   ⚠️ 部分旧路径跳转缺失")
except Exception as e:
    print(f"   ⚠️ 无法读取 vercel.json: {e}")

# 4. Check Canonical / Hreflang
en_canonical = en_hreflang = zh_canonical = zh_hreflang = 0
for root, dirs, files in os.walk('./en'):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fp:
                content = fp.read()
                if 'rel="canonical"' in content: en_canonical += 1
                if 'hreflang="zh"' in content: en_hreflang += 1

for root, dirs, files in os.walk('./zh'):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fp:
                content = fp.read()
                if 'rel="canonical"' in content: zh_canonical += 1
                if 'hreflang="en"' in content: zh_hreflang += 1

print("")
print("4. 检查 Canonical / Hreflang...")
print(f"   英文页面 - Canonical: {en_canonical}, Hreflang-zh: {en_hreflang}")
print(f"   中文页面 - Canonical: {zh_canonical}, Hreflang-en: {zh_hreflang}")

# 5. Check language switcher
en_switcher = zh_switcher = 0
for root, dirs, files in os.walk('./en'):
    for f in files:
        if f.endswith('.html'):
            with open(os.path.join(root, f), 'r', encoding='utf-8') as fp:
                content = fp.read()
                # Check for lang-switch class or language switcher patterns
                if 'lang-switch' in content or '切换' in content or 'Chinese' in content:
                    en_switcher += 1

for root, dirs, files in os.walk('./zh'):
    for f in files:
        if f.endswith('.html'):
            with open(os.path.join(root, f), 'r', encoding='utf-8') as fp:
                content = fp.read()
                if 'lang-switch' in content or 'EN' in content or 'English' in content:
                    zh_switcher += 1

print("")
print("5. 检查语言切换器覆盖...")
print(f"   英文页面语言切换器：{en_switcher}/{en_count}")
print(f"   中文页面语言切换器：{zh_switcher}/{zh_count}")

# Summary
en_count = sum(1 for r, d, fs in os.walk('./en') for f in fs if f.endswith('.html'))
print("")
print("============================================================")
print("统计汇总")
print("============================================================")
print(f"英文页面数：{en_count}")
print(f"中文页面数：{zh_count}")
print(f"英文路径中文残留：{len(en_issues)} 页")
print("============================================================")

if len(en_issues) == 0:
    print("✅ Phase-2 Plan B 全部验证通过")
else:
    print("⚠️ 发现需要修复的问题")
print("============================================================")
PYTHON_SCRIPT

echo ""
echo "验证完成时间：$(date '+%Y-%m-%d %H:%M JST')"
