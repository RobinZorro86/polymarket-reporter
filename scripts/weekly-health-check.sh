#!/bin/bash
# Weekly Website Health Check - 每周网站健康检查
# 检查内容：死链、404、视觉效果统一性、内容更新状态
# 运行时间：每周一 9:00 AM

set -e

WORKSPACE=/home/zqd/.openclaw/workspace/polymarket-reporter
REPORT_DIR=~/website-health-reports
DATE=$(date +%Y%m%d)
REPORT_FILE="$REPORT_DIR/weekly-check-$DATE.md"

# 创建报告目录
mkdir -p "$REPORT_DIR"

echo "# 🧠 Prediction Market 101 网站健康检查报告" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**检查时间**: $(date '+%Y-%m-%d %H:%M:%S')" >> "$REPORT_FILE"
echo "**检查范围**: 首页、知识库、报告、关于页面" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

cd "$WORKSPACE"

echo "## ✅ 1. 基础检查" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 检查网站可访问性
if curl -s --max-time 10 https://pred101.com -o /dev/null; then
  echo "- ✅ 主站可访问：https://pred101.com" >> "$REPORT_FILE"
else
  echo "- ❌ 主站无法访问：https://pred101.com" >> "$REPORT_FILE"
fi

# 检查知识库
if curl -s --max-time 10 https://pred101.com/knowledge-base/ -o /dev/null; then
  echo "- ✅ 知识库可访问" >> "$REPORT_FILE"
else
  echo "- ❌ 知识库无法访问" >> "$REPORT_FILE"
fi

# 检查报告页
if curl -s --max-time 10 https://pred101.com/reports/ -o /dev/null; then
  echo "- ✅ 报告页可访问" >> "$REPORT_FILE"
else
  echo "- ❌ 报告页无法访问" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"
echo "## 🔍 2. 404 链接检查" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 检查知识库链接
BROKEN_LINKS=0
for link in $(grep -o 'href="/knowledge-base/[^"]*"' knowledge-base/index.html 2>/dev/null | cut -d'"' -f2); do
  path="${link#/knowledge-base/}"
  if [ ! -f "$path" ] && [ ! -f "${path}index.html" ]; then
    echo "- ❌ 404: $link" >> "$REPORT_FILE"
    BROKEN_LINKS=$((BROKEN_LINKS + 1))
  fi
done

if [ $BROKEN_LINKS -eq 0 ]; then
  echo "- ✅ 无 404 链接" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"
echo "## 📊 3. 内容统计" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 统计 KOL 数量
KOL_COUNT=$(ls -d knowledge-base/kol/*/ 2>/dev/null | wc -l)
echo "- KOL 页面：$KOL_COUNT" >> "$REPORT_FILE"

# 统计策略数量
STRATEGY_COUNT=$(ls -d knowledge-base/strategies/*/ 2>/dev/null | wc -l)
echo "- 策略页面：$STRATEGY_COUNT" >> "$REPORT_FILE"

# 统计教程数量
TUTORIAL_COUNT=$(ls -d knowledge-base/tutorials/*/ 2>/dev/null | wc -l)
echo "- 教程页面：$TUTORIAL_COUNT" >> "$REPORT_FILE"

# 统计资源数量
RESOURCE_COUNT=$(ls -d knowledge-base/resources/*/ 2>/dev/null | wc -l)
echo "- 资源页面：$RESOURCE_COUNT" >> "$REPORT_FILE"

# 统计日报数量
DAILY_COUNT=$(ls knowledge-base/daily-reports/*.html reports/daily/*.html 2>/dev/null | wc -l)
echo "- 日报数量：$DAILY_COUNT" >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "## 🎨 4. 视觉效果检查" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 检查是否使用 Apple Design System
APPLE_CSS_COUNT=$(grep -r "SF Pro Text" *.html knowledge-base/*.html 2>/dev/null | wc -l)
if [ $APPLE_CSS_COUNT -gt 0 ]; then
  echo "- ✅ 使用 Apple Design System 的页面：$APPLE_CSS_COUNT" >> "$REPORT_FILE"
else
  echo "- ⚠️ 未发现使用 Apple Design System 的页面" >> "$REPORT_FILE"
fi

# 检查深色主题（需要统一）
DARK_THEME_COUNT=$(grep -r "background: linear-gradient" *.html reports/*.html knowledge-base/*.html 2>/dev/null | wc -l)
if [ $DARK_THEME_COUNT -gt 0 ]; then
  echo "- ⚠️ 使用深色主题的页面（需统一）：$DARK_THEME_COUNT" >> "$REPORT_FILE"
else
  echo "- ✅ 无深色主题页面" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"
echo "## 📝 5. Git 状态" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 检查未提交的更改
UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l)
if [ $UNCOMMITTED -gt 0 ]; then
  echo "- ⚠️ 有未提交的更改：$UNCOMMITTED 个文件" >> "$REPORT_FILE"
  git status --porcelain >> "$REPORT_FILE" 2>&1
else
  echo "- ✅ 无未提交的更改" >> "$REPORT_FILE"
fi

# 检查最新提交
LATEST_COMMIT=$(git log -1 --oneline 2>/dev/null)
echo "- 最新提交：$LATEST_COMMIT" >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "## ✅ 6. 建议操作" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

if [ $BROKEN_LINKS -gt 0 ]; then
  echo "1. 修复 $BROKEN_LINKS 个 404 链接" >> "$REPORT_FILE"
fi

if [ $DARK_THEME_COUNT -gt 0 ]; then
  echo "2. 统一 $DARK_THEME_COUNT 个深色主题页面为 Apple Design System" >> "$REPORT_FILE"
fi

if [ $UNCOMMITTED -gt 0 ]; then
  echo "3. 提交 $UNCOMMITTED 个未提交的更改" >> "$REPORT_FILE"
fi

if [ $BROKEN_LINKS -eq 0 ] && [ $DARK_THEME_COUNT -eq 0 ] && [ $UNCOMMITTED -eq 0 ]; then
  echo "✅ 无需操作，网站状态良好" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "*报告生成于 $(date '+%Y-%m-%d %H:%M:%S')*" >> "$REPORT_FILE"

# 输出报告
echo "✅ 周检完成！报告已保存：$REPORT_FILE"
echo ""
cat "$REPORT_FILE"
