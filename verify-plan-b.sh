#!/bin/bash
echo "============================================================"
echo "Phase-2 Plan B 自动验证 - $(date '+%Y-%m-%d %H:%M JST')"
echo "============================================================"
echo ""

# 1. 检查英文路径中文残留
echo "1. 检查英文路径中文残留..."
EN_CHINESE=$(grep -rl "[\u4e00-\u9fff]" ./en --include="*.html" 2>/dev/null | grep -v "Chinese" | grep -v "zh-CN" | wc -l)
echo "   英文路径中含中文的文件数：$EN_CHINESE"
if [ "$EN_CHINESE" -gt 0 ]; then
    echo "   详情:"
    grep -rl "[\u4e00-\u9fff]" ./en --include="*.html" 2>/dev/null | grep -v "Chinese" | grep -v "zh-CN" | head -10
fi

# 2. 检查中文路径英文污染
echo ""
echo "2. 检查中文路径英文污染..."
ZH_ENGLISH=$(grep -rl "[a-zA-Z]\{5,\}" ./zh --include="*.html" 2>/dev/null | grep -v "href=" | grep -v "class=" | grep -v "id=" | grep -v "OpenClaw" | grep -v "Polymarket" | grep -v "Simmer" | grep -v "USD" | grep -v "API" | wc -l)
echo "   中文路径中可能含英文污染的文件数：$ZH_ENGLISH"

# 3. 检查旧路径跳转配置
echo ""
echo "3. 检查旧路径跳转配置..."
if [ -f "vercel.json" ]; then
    REDIRECTS=$(grep -c "redirects" vercel.json)
    echo "   vercel.json 中 redirects 配置数：$REDIRECTS"
    if [ "$REDIRECTS" -gt 0 ]; then
        echo "   ✅ 旧路径跳转配置存在"
    else
        echo "   ⚠️ 旧路径跳转配置可能缺失"
    fi
else
    echo "   ⚠️ vercel.json 不存在"
fi

# 4. 检查 Canonical / Hreflang
echo ""
echo "4. 检查 Canonical / Hreflang..."
EN_CANONICAL=$(grep -rl "canonical" ./en --include="*.html" | wc -l)
EN_HREFLANG=$(grep -rl "hreflang" ./en --include="*.html" | wc -l)
ZH_CANONICAL=$(grep -rl "canonical" ./zh --include="*.html" | wc -l)
ZH_HREFLANG=$(grep -rl "hreflang" ./zh --include="*.html" | wc -l)
echo "   英文页面 - Canonical: $EN_CANONICAL, Hreflang: $EN_HREFLANG"
echo "   中文页面 - Canonical: $ZH_CANONICAL, Hreflang: $ZH_HREFLANG"

# 5. 检查语言切换器覆盖
echo ""
echo "5. 检查语言切换器覆盖..."
EN_SWITCHER=$(grep -rl "language-switcher\|lang-switch\|切换语言" ./en --include="*.html" | wc -l)
ZH_SWITCHER=$(grep -rl "language-switcher\|lang-switch\|切换语言" ./zh --include="*.html" | wc -l)
echo "   英文页面语言切换器：$EN_SWITCHER"
echo "   中文页面语言切换器：$ZH_SWITCHER"

# 统计
echo ""
echo "============================================================"
echo "统计汇总"
echo "============================================================"
EN_COUNT=$(find ./en -name "*.html" | wc -l)
ZH_COUNT=$(find ./zh -name "*.html" | wc -l)
echo "英文页面数：$EN_COUNT"
echo "中文页面数：$ZH_COUNT"
echo "英文路径中文残留：$EN_CHINESE 页"
echo "中文路径英文污染：$ZH_ENGLISH 页"
echo "============================================================"

if [ "$EN_CHINESE" -eq 0 ] && [ "$ZH_ENGLISH" -lt 5 ]; then
    echo "✅ Phase-2 Plan B 全部验证通过"
else
    echo "⚠️ 发现需要修复的问题"
fi
echo "============================================================"
