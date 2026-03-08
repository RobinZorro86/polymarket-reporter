#!/bin/bash
# Knowledge Base Weekly Batch Update - 知识库每周批量更新
# 运行时间：每周日 20:00 (收集本周内容，周一早上发布)
# 功能：汇总本周 KOL 内容、策略更新、资源补充

set -e

WORKSPACE=/home/zqd/.openclaw/workspace/polymarket-reporter
KB_DIR=$WORKSPACE/knowledge-base
X_SUMMARIES=~/x-summaries
DATE=$(date +%Y-%m-%d)
DATE_NUM=$(date +%Y%m%d)

# X 认证配置
AUTH_TOKEN="0843fc6fc493787abf6eaa7ae6599cc9273db347"
CT0="aa63a3556bbb75ea9bc33cea142ff959626d7d20298b3752205e071a8cd9ed60b737318161b05d821e2e09bcbfea30a8fb2aa9b8d5b867522a3e80a23d4da72ed0892f6072712ae7da29580404fc57a0"

echo "📚 知识库每周批量更新 - $DATE"
echo "================================"

# 创建周报目录
mkdir -p "$KB_DIR/weekly-updates"

UPDATE_LOG="$KB_DIR/weekly-updates/update-$DATE_NUM.md"

# Step 1: 抓取 KOL 本周推文
echo "📱 抓取 KOL 本周动态..."

KOLS=("vladic_eth" "noisyb0y1" "ayi_ainotes" "rohonchain" "cutnpaste4" "molt-cornelius" "dmitriyungarov" "aleiahlock" "0xchainmind" "runes-leo" "edwordkaru")

for kol in "${KOLS[@]}"; do
  echo "  - @$kol"
  xreach --auth-token "$AUTH_TOKEN" --ct0 "$CT0" tweets @$kol --json -n 30 > "$X_SUMMARIES/${kol}-weekly-$DATE_NUM.json" 2>/dev/null || true
done

# Step 2: 生成更新日志
echo "📝 生成更新日志..."

cat > "$UPDATE_LOG" << 'EOF'
# 📚 知识库每周更新日志

**周数**: WEEK_NUM_PLACEHOLDER  
**更新日期**: DATE_PLACEHOLDER  
**覆盖周期**: START_DATE ~ END_DATE

---

## ✅ 本周更新内容

### KOL 策略更新
- [ ] @vladic_eth - 待填充
- [ ] @noisyb0y1 - 待填充
- [ ] @AYi_AInotes - 待填充
- [ ] @RohOnChain - 待填充
- [ ] 其他 KOL - 待填充

### 新增策略
- [ ] 待填充策略名称

### 教程更新
- [ ] 待填充教程名称

### 资源补充
- [ ] 待填充资源名称

---

## 📊 KOL 内容摘要

### @vladic_eth
**推文数量**: 待填充  
**核心观点**:
- 待填充

### @noisyb0y1
**推文数量**: 待填充  
**核心观点**:
- 待填充

### @AYi_AInotes
**推文数量**: 待填充  
**核心观点**:
- 待填充

---

## 🎯 待办事项

### 高优先级
1. [ ] 待填充

### 中优先级
1. [ ] 待填充

### 低优先级
1. [ ] 待填充

---

## 📝 更新记录

| 时间 | 内容 | 状态 | 操作人 |
|------|------|------|--------|
| DATE_PLACEHOLDER | 本周 KOL 内容收集 | ✅ 完成 | Auto |
| DATE_PLACEHOLDER | 更新日志生成 | ✅ 完成 | Auto |

---

*下周继续收集，周日统一推送部署*
EOF

# 替换占位符
WEEK_NUM=$(date +%V)
LAST_MONDAY=$(date -d "last monday" +%Y-%m-%d)
NEXT_SUNDAY=$(date -d "sunday" +%Y-%m-%d)

sed -i "s/WEEK_NUM_PLACEHOLDER/$WEEK_NUM/g" "$UPDATE_LOG"
sed -i "s/DATE_PLACEHOLDER/$DATE/g" "$UPDATE_LOG"
sed -i "s/START_DATE/$LAST_MONDAY/g" "$UPDATE_LOG"
sed -i "s/END_DATE/$NEXT_SUNDAY/g" "$UPDATE_LOG"

echo "✅ 更新日志已生成：$UPDATE_LOG"
echo ""

# Step 3: 生成 KOL 内容摘要
echo "📊 生成 KOL 内容摘要..."

SUMMARY_FILE="$KB_DIR/weekly-updates/kol-summary-$DATE_NUM.md"

cat > "$SUMMARY_FILE" << 'EOF'
# 👥 KOL 周度内容摘要

**周期**: START_DATE ~ END_DATE

---

EOF

sed -i "s/START_DATE/$LAST_MONDAY/g" "$SUMMARY_FILE"
sed -i "s/END_DATE/$NEXT_SUNDAY/g" "$SUMMARY_FILE"

for kol in "${KOLS[@]:0:5}"; do
  if [ -f "$X_SUMMARIES/${kol}-weekly-$DATE_NUM.json" ]; then
    echo "" >> "$SUMMARY_FILE"
    echo "## @$kol" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"
    
    python3 << PYEOF >> "$SUMMARY_FILE" 2>/dev/null || echo "无数据"
import json
try:
    with open('$X_SUMMARIES/${kol}-weekly-$DATE_NUM.json', 'r') as f:
        data = json.load(f)
    items = data.get('items', [])[:5]
    for i, tweet in enumerate(items, 1):
        text = tweet.get('text', '').replace('\n', ' ').replace('\r', '')[:200]
        likes = tweet.get('likeCount', 0)
        retweets = tweet.get('retweetCount', 0)
        created = tweet.get('createdAt', '')[:16]
        print(f"**{i}.** [{created}] {text}...  ❤️{likes} 🔄{retweets}")
        print("")
except Exception as e:
    print(f"解析失败：{e}")
PYEOF
  fi
done

echo "✅ KOL 摘要已生成：$SUMMARY_FILE"
echo ""

# Step 4: 自动提交（不推送，周日统一推送）
cd "$WORKSPACE"
git add "$KB_DIR/weekly-updates/" 2>/dev/null || true
git commit -m "docs: 知识库周度更新 $WEEK_NUM (收集阶段)" --allow-empty 2>/dev/null || true

echo "✅ 本周更新已提交到本地仓库"
echo ""
echo "📌 说明:"
echo "- 本周内容将持续收集到周日"
echo "- 周日晚上统一推送触发 Vercel 部署"
echo "- 查看更新日志：$UPDATE_LOG"
echo ""

# 输出 KOL 数据预览
echo "📱 KOL 数据预览:"
for kol in vladic_eth noisyb0y1; do
  if [ -f "$X_SUMMARIES/${kol}-weekly-$DATE_NUM.json" ]; then
    count=$(python3 -c "import json; print(len(json.load(open('$X_SUMMARIES/${kol}-weekly-$DATE_NUM.json')).get('items', [])))" 2>/dev/null || echo "0")
    echo "  @$kol: $count 条推文"
  fi
done
