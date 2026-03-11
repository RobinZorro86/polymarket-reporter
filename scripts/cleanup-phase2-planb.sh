#!/bin/bash
# Phase-2 Plan B 收尾清理脚本
# 目标：删除 /en/* 下的中文模板源文件，保留 .html 输出

set -e

cd /home/zqd/.openclaw/workspace/polymarket-reporter

echo "=== Phase-2 Plan B 清理脚本 ==="
echo "当前时间：$(date '+%Y-%m-%d %H:%M:%S %Z')"
echo ""

# 计数器
deleted=0
skipped=0

# 1. 删除 en/reports/daily/ 下的中文 .md 模板
echo "📁 检查 en/reports/daily/ ..."
for f in en/reports/daily/*.md; do
  if [ -f "$f" ]; then
    # 检查是否为中文模板（包含中文字符）
    if grep -qP '[\x{4e00}-\x{9fff}]' "$f" 2>/dev/null || grep -q "待填充\|每日报告\|日期" "$f" 2>/dev/null; then
      echo "  🗑️  删除：$f"
      rm "$f"
      ((deleted++))
    else
      echo "  ⏭️  跳过（英文内容）: $f"
      ((skipped++))
    fi
  fi
done

# 2. 删除 en/reports/weekly/ 下的中文 .md 模板
echo "📁 检查 en/reports/weekly/ ..."
for f in en/reports/weekly/*.md; do
  if [ -f "$f" ]; then
    if grep -qP '[\x{4e00}-\x{9fff}]' "$f" 2>/dev/null || grep -q "待填充\|每周报告\|日期" "$f" 2>/dev/null; then
      echo "  🗑️  删除：$f"
      rm "$f"
      ((deleted++))
    else
      echo "  ⏭️  跳过（英文内容）: $f"
      ((skipped++))
    fi
  fi
done

# 3. 删除 en/knowledge-base/ 下可能残留的中文 .md 模板
echo "📁 检查 en/knowledge-base/ ..."
for f in $(find en/knowledge-base/ -name "*.md" -type f 2>/dev/null); do
  if grep -qP '[\x{4e00}-\x{9fff}]' "$f" 2>/dev/null; then
    echo "  🗑️  删除：$f"
    rm "$f"
    ((deleted++))
  else
    echo "  ⏭️  跳过（英文内容）: $f"
    ((skipped++))
  fi
done

echo ""
echo "=== 清理完成 ==="
echo "已删除：$deleted 个中文模板文件"
echo "已跳过：$skipped 个英文文件"
echo ""

# 4. 检查旧根路径跳转配置
echo "🔍 验证 vercel.json 跳转配置..."
if grep -q '"/knowledge-base/:path\*"' vercel.json && grep -q '"/reports/:path\*"' vercel.json; then
  echo "  ✅ vercel.json 跳转规则已配置"
else
  echo "  ⚠️  vercel.json 跳转规则可能缺失"
fi

# 5. 检查 zh/ 完整性
echo ""
echo "🔍 验证 zh/ 路径完整性..."
zh_pages=$(find zh/ -name "*.html" -type f | wc -l)
echo "  zh/ 下 HTML 页面数：$zh_pages"

if [ $zh_pages -gt 20 ]; then
  echo "  ✅ zh/ 路径完整"
else
  echo "  ⚠️  zh/ 页面数偏少，可能需要检查"
fi

echo ""
echo "=== 脚本执行完毕 ==="
