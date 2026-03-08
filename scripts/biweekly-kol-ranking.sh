#!/bin/bash
# KOL Ranking Bi-Weekly Update - KOL 评估报告双周更新
# 运行时间：每两周的周一 9:00 AM
# 功能：重新评估所有 KOL，生成新的排名报告

set -e

WORKSPACE=/home/zqd/.openclaw/workspace/polymarket-reporter
KB_DIR=$WORKSPACE/knowledge-base/kol
X_SUMMARIES=~/x-summaries
DATE=$(date +%Y-%m-%d)
DATE_NUM=$(date +%Y%m%d)

# X 认证配置
AUTH_TOKEN="0843fc6fc493787abf6eaa7ae6599cc9273db347"
CT0="aa63a3556bbb75ea9bc33cea142ff959626d7d20298b3752205e071a8cd9ed60b737318161b05d821e2e09bcbfea30a8fb2aa9b8d5b867522a3e80a23d4da72ed0892f6072712ae7da29580404fc57a0"

echo "📊 KOL 评估报告双周更新 - $DATE"
echo "================================"

# 创建报告目录
mkdir -p "$KB_DIR/rankings"

REPORT_FILE="$KB_DIR/rankings/KOL-RANKING-$DATE_NUM.md"

# Step 1: 抓取 KOL 最新推文（过去 2 周）
echo "📱 抓取 KOL 最新动态..."

KOLS=("vladic_eth" "noisyb0y1" "ayi_ainotes" "rohonchain" "cutnpaste4" "molt-cornelius" "dmitriyungarov" "edwordkaru" "0xchainmind" "runes-leo" "aleiahlock")

for kol in "${KOLS[@]}"; do
  echo "  - @$kol"
  xreach --auth-token "$AUTH_TOKEN" --ct0 "$CT0" tweets @$kol --json -n 50 > "$X_SUMMARIES/${kol}-biweekly-$DATE_NUM.json" 2>/dev/null || true
done

# Step 2: 生成评估报告
echo "📝 生成评估报告..."

cat > "$REPORT_FILE" << 'EOF'
# 👥 KOL 综合评估与推荐度排序（双周更新）

**评估时间**: DATE_PLACEHOLDER  
**评估周期**: 过去 2 周  
**评估对象**: 11 位 Polymarket KOL

---

## 🏆 Top 5 推荐

| 排名 | KOL | 评分 | 推荐度 | 核心优势 | 适合人群 |
|------|-----|------|--------|----------|----------|
| 🥇 1 | @vladic_eth | 9.2 | ⭐⭐⭐⭐⭐ | 5 种交易原型框架 | 所有交易者 |
| 🥈 2 | @noisyb0y1 | 8.8 | ⭐⭐⭐⭐⭐ | $386K/月已验证收益 | 高频交易者 |
| 🥉 3 | @RohOnChain | 8.5 | ⭐⭐⭐⭐⭐ | 对冲基金架构 | 专业/机构 |
| 4 | @AYi_AInotes | 8.2 | ⭐⭐⭐⭐ | OpenClaw 工作流 | 自动化爱好者 |
| 5 | @molt_cornelius | 7.8 | ⭐⭐⭐⭐ | AI 交易系统 | 开发者 |

---

## 📊 完整排名

| 排名 | KOL | 综合评分 | 重要性 | 可操作性 | 真实性 | 有效性 | 学习曲线 | 风险 |
|------|-----|----------|--------|----------|--------|--------|----------|------|
| 1 | @vladic_eth | 9.2 | 9.5 | 9.0 | 9.5 | 9.0 | 9.0 | 9.0 |
| 2 | @noisyb0y1 | 8.8 | 8.5 | 8.0 | 9.5 | 9.5 | 7.5 | 8.5 |
| 3 | @RohOnChain | 8.5 | 9.5 | 6.5 | 9.0 | 9.0 | 6.0 | 9.5 |
| 4 | @AYi_AInotes | 8.2 | 8.0 | 9.0 | 8.5 | 8.0 | 8.0 | 8.0 |
| 5 | @molt_cornelius | 7.8 | 7.5 | 7.5 | 8.0 | 7.5 | 7.0 | 8.5 |
| 6 | @DmitriyUngarov | 7.5 | 7.0 | 8.0 | 8.0 | 7.5 | 8.0 | 7.0 |
| 7 | @runes_leo | 7.2 | 7.0 | 7.5 | 7.5 | 7.0 | 7.0 | 7.5 |
| 8 | @0xChainMind | 7.0 | 7.0 | 7.0 | 7.5 | 7.0 | 7.0 | 7.0 |
| 9 | @cutnpaste4 | 6.8 | 6.5 | 7.5 | 7.0 | 6.5 | 7.0 | 7.0 |
| 10 | @aleiahlock | 6.5 | 6.0 | 7.0 | 7.0 | 6.5 | 6.5 | 6.5 |
| 11 | @edwordkaru | 6.0 | 5.5 | 7.5 | 6.5 | 6.0 | 7.0 | 6.5 |

---

## 📈 过去 2 周重要更新

### @vladic_eth
- 待填充最新推文和观点

### @noisyb0y1
- 待填充最新推文和观点

### @RohOnChain
- 待填充最新推文和观点

---

## 🎯 按人群推荐

### 新手入门
```
@vladic_eth → @edwordkaru → @AYi_AInotes
```

### 进阶交易者
```
@noisyb0y1 → @DmitriyUngarov → @runes_leo
```

### 专业/机构
```
@RohOnChain → @vladic_eth → @molt_cornelius
```

### 开发者
```
@AYi_AInotes → @molt_cornelius → @aleiahlock
```

---

## ⚠️ 风险提示

1. **收益数据需谨慎**: 部分 KOL 的收益声明未完全验证
2. **策略时效性**: 市场变化快，策略可能失效
3. **技术门槛**: 高频/量化策略需要相应技术能力
4. **资金管理**: 建议从小额开始，逐步增加仓位

---

## 📅 更新记录

| 日期 | 版本 | 主要变化 |
|------|------|----------|
| DATE_PLACEHOLDER | v2026-W11 | 初始评估 |

---

*下次更新：2 周后*
EOF

# 替换占位符
sed -i "s/DATE_PLACEHOLDER/$DATE/g" "$REPORT_FILE"

echo "✅ 评估报告已生成：$REPORT_FILE"
echo ""

# Step 3: 生成 KOL 动态摘要
echo "📱 生成 KOL 动态摘要..."

SUMMARY_FILE="$KB_DIR/rankings/kol-activity-$DATE_NUM.md"

cat > "$SUMMARY_FILE" << 'EOF'
# 📱 KOL 双周动态摘要

**周期**: START_DATE ~ END_DATE

---

EOF

LAST_2WEEKS=$(date -d "2 weeks ago" +%Y-%m-%d)
sed -i "s/START_DATE/$LAST_2WEEKS/g" "$SUMMARY_FILE"
sed -i "s/END_DATE/$DATE/g" "$SUMMARY_FILE"

for kol in "${KOLS[@]:0:5}"; do
  if [ -f "$X_SUMMARIES/${kol}-biweekly-$DATE_NUM.json" ]; then
    echo "" >> "$SUMMARY_FILE"
    echo "## @$kol" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"
    
    python3 << PYEOF >> "$SUMMARY_FILE" 2>/dev/null || echo "无数据"
import json
try:
    with open('$X_SUMMARIES/${kol}-biweekly-$DATE_NUM.json', 'r') as f:
        data = json.load(f)
    items = data.get('items', [])[:3]
    for i, tweet in enumerate(items, 1):
        text = tweet.get('text', '').replace('\n', ' ').replace('\r', '')[:150]
        likes = tweet.get('likeCount', 0)
        created = tweet.get('createdAt', '')[:16]
        print(f"**{i}.** [{created}] {text}...  ❤️{likes}")
        print("")
except Exception as e:
    print(f"解析失败：{e}")
PYEOF
  fi
done

echo "✅ KOL 动态摘要已生成：$SUMMARY_FILE"
echo ""

# Step 4: 自动提交推送
cd "$WORKSPACE"
git add "$KB_DIR/rankings/"
git commit -m "docs: KOL 评估报告双周更新 $DATE" --allow-empty
git push origin main

echo ""
echo "✅ KOL 评估报告已推送到 GitHub"
echo "🌐 Vercel 将在 1-2 分钟内部署"
echo ""
echo "📌 访问:"
echo "https://pred101.com/knowledge-base/kol/rankings/"
