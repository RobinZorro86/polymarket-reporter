#!/bin/bash
# Weekly Content Batch Deploy - 周日统一推送部署
# 运行时间：每周日 20:00
# 功能：汇总本周所有更新，一次性推送触发 Vercel 部署

set -e

WORKSPACE=/home/zqd/.openclaw/workspace/polymarket-reporter
KB_DIR=$WORKSPACE/knowledge-base
DATE=$(date +%Y-%m-%d)
DATE_NUM=$(date +%Y%m%d)

echo "🚀 周日统一推送部署 - $DATE"
echo "================================"

cd "$WORKSPACE"

# Step 1: 检查本周更新
echo "📊 检查本周更新内容..."

UPDATE_COUNT=$(git status --porcelain | wc -l)
if [ $UPDATE_COUNT -eq 0 ]; then
  echo "✅ 本周无待推送更新"
  exit 0
fi

echo "发现 $UPDATE_COUNT 个待推送文件"
git status --short

# Step 2: 生成推送摘要
DEPLOY_SUMMARY="$KB_DIR/weekly-updates/deploy-summary-$DATE_NUM.md"

cat > "$DEPLOY_SUMMARY" << 'EOF'
# 🚀 周度推送摘要

**推送时间**: DATE_PLACEHOLDER  
**周数**: WEEK_NUM_PLACEHOLDER

---

## 📝 本次推送内容

### 知识库更新
- KOL 内容更新：待填充
- 策略页面更新：待填充
- 教程更新：待填充
- 资源补充：待填充

### 报告更新
- 日报数量：待填充
- 周报发布：待填充

---

## 📊 统计数据

EOF

WEEK_NUM=$(date +%V)
sed -i "s/DATE_PLACEHOLDER/$DATE/g" "$DEPLOY_SUMMARY"
sed -i "s/WEEK_NUM_PLACEHOLDER/$WEEK_NUM/g" "$DEPLOY_SUMMARY"

# 统计本周文件变化
echo "### 文件变化" >> "$DEPLOY_SUMMARY"
echo "" >> "$DEPLOY_SUMMARY"
git diff --shortstat HEAD >> "$DEPLOY_SUMMARY" 2>/dev/null || echo "无变化统计" >> "$DEPLOY_SUMMARY"
echo "" >> "$DEPLOY_SUMMARY"

# Step 3: 提交并推送
echo ""
echo "📤 推送到 GitHub..."

git add -A
git commit -m "docs: 周度批量更新 W$WEEK_NUM ($DATE)" --allow-empty
git push origin main

echo ""
echo "✅ 推送成功！"
echo ""
echo "🌐 Vercel 部署状态:"
echo "https://vercel.com/robinzorro86s-projects/polymarket-reporter"
echo ""
echo "⏳ 部署预计 1-2 分钟完成，CDN 全球生效 5-10 分钟"
echo ""

# Step 4: 发送通知（可选：Telegram）
echo "📱 发送部署通知..."
# 如需 Telegram 通知，在此添加 message 工具调用

echo "✅ 周度推送完成"
