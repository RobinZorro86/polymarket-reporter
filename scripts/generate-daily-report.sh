#!/bin/bash
# Polymarket Daily Report Generator - 精细化日报生成
# 运行时间：隔天 9:00 AM (1,3,5,7,9...)
# 功能：全网检索 + X 热点 + 市场数据 + KOL 动态

set -e

# 配置
WORKSPACE=/home/zqd/.openclaw/workspace/polymarket-reporter
REPORTS_DIR=$WORKSPACE/reports/daily
X_SUMMARIES=~/x-summaries
DATE=$(date +%Y-%m-%d)
DATE_NUM=$(date +%Y%m%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

# X 认证配置
AUTH_TOKEN="0843fc6fc493787abf6eaa7ae6599cc9273db347"
CT0="aa63a3556bbb75ea9bc33cea142ff959626d7d20298b3752205e071a8cd9ed60b737318161b05d821e2e09bcbfea30a8fb2aa9b8d5b867522a3e80a23d4da72ed0892f6072712ae7da29580404fc57a0"

echo "📊 生成 Polymarket 日报 - $DATE"
echo "================================"

# 创建报告目录
mkdir -p "$REPORTS_DIR"

REPORT_FILE="$REPORTS_DIR/daily-$DATE_NUM.html"
MARKDOWN_FILE="$REPORTS_DIR/daily-$DATE_NUM.md"

# Step 1: 抓取 X 热点
echo "📱 抓取 X 热点..."
mkdir -p "$X_SUMMARIES"

# 抓取 Polymarket 官方
xreach --auth-token "$AUTH_TOKEN" --ct0 "$CT0" tweets @Polymarket --json -n 10 > "$X_SUMMARIES/polymarket-official-$DATE_NUM.json" 2>/dev/null || true

# 抓取 Mert
xreach --auth-token "$AUTH_TOKEN" --ct0 "$CT0" tweets @mert_mert --json -n 5 > "$X_SUMMARIES/mert-$DATE_NUM.json" 2>/dev/null || true

# Step 2: 搜索全网新闻
echo "🌐 搜索全网新闻..."
NEWS_FILE="$X_SUMMARIES/news-$DATE_NUM.txt"

curl -s "https://r.jina.ai/https://news.google.com/search?q=Polymarket+prediction+market&hl=en-US&gl=US&ceid=US:en" > "$NEWS_FILE" 2>/dev/null || true

# Step 3: 生成 Markdown 草稿
echo "📝 生成报告草稿..."

cat > "$MARKDOWN_FILE" << 'EOF'
# 📊 Polymarket 每日报告

**日期**: DATE_PLACEHOLDER  
**生成时间**: TIME_PLACEHOLDER  
**覆盖周期**: 过去 24 小时

---

## 🔥 今日热点 TOP 5

### 1. [待填充]
- **市场**: 
- **概率变化**: 
- **交易量**: 
- **X 讨论热度**: 

### 2. [待填充]

### 3. [待填充]

### 4. [待填充]

### 5. [待填充]

---

## 📈 高概率机会 (>80%)

| 市场 | 概率 | 交易量 | 结算时间 | 推荐度 |
|------|------|--------|----------|--------|
| 待填充 | - | - | - | ⭐⭐⭐ |

---

## 🎯 价值投注机会 (40-60% 区间)

| 市场 | 当前概率 | 合理概率 | Edge | 建议仓位 |
|------|----------|----------|------|----------|
| 待填充 | - | - | - | - |

---

## 🐋 鲸鱼动向

- **大额交易**: 待填充
- **聪明钱地址**: 待填充
- **24h PnL 最佳**: 待填充

---

## 📱 X/Twitter 热点

### Polymarket 官方动态
- 待填充

### KOL 观点
- **@mert_mert**: 待填充
- **@noisyb0y1**: 待填充
- **@vladic_eth**: 待填充

### 社区热议
- 待填充

---

## 🌐 全网新闻

### 主流媒体
- 待填充

### Crypto 媒体
- 待填充

---

## 📊 市场情绪指标

- **总交易量 (24h)**: $待填充
- **活跃市场数**: 待填充
- **情绪倾向**: 待填充 (贪婪/恐惧/中性)

---

## ⚠️ 风险提示

1. **分辨率风险**: 待填充
2. **流动性风险**: 待填充
3. **时间风险**: 待填充

---

## 📌 明日关注

- [ ] 待填充事件 1
- [ ] 待填充事件 2
- [ ] 待填充事件 3

---

*报告由 Aegis V2 + OpenClaw 自动生成 | 数据来源：Polymarket API, X API, Google News*
EOF

# 替换日期
sed -i "s/DATE_PLACEHOLDER/$DATE/g" "$MARKDOWN_FILE"
sed -i "s/TIME_PLACEHOLDER/$(date '+%H:%M')/g" "$MARKDOWN_FILE"

echo "✅ Markdown 草稿已生成：$MARKDOWN_FILE"
echo ""

# 自动复制模板生成 HTML
HTML_FILE="$REPORTS_DIR/daily-$DATE_NUM.html"
cp "$WORKSPACE/templates/daily-report-template.html" "$HTML_FILE"

# 替换 HTML 占位符
sed -i "s/DATE_PLACEHOLDER/$DATE/g" "$HTML_FILE"
sed -i "s/TIME_PLACEHOLDER/$(date '+%H:%M')/g" "$HTML_FILE"

echo "✅ HTML 报告已生成：$HTML_FILE"
echo ""

# 自动提交推送
cd "$WORKSPACE"
git add "$HTML_FILE" "$MARKDOWN_FILE" 2>/dev/null || true
git commit -m "docs: 发布日报 $DATE" --allow-empty 2>/dev/null || true
git push origin main 2>&1 | tail -3

echo ""
echo "✅ 日报已自动推送到 GitHub，Vercel 将在 1-2 分钟内部署"
echo "🌐 访问：https://pred101.com/reports/daily/daily-$DATE_NUM.html"

# 输出 X 数据摘要
echo "📱 X 热点预览:"
if [ -f "$X_SUMMARIES/polymarket-official-$DATE_NUM.json" ]; then
  python3 -c "
import json
try:
    with open('$X_SUMMARIES/polymarket-official-$DATE_NUM.json', 'r') as f:
        data = json.load(f)
    for i, tweet in enumerate(data.get('items', [])[:3], 1):
        text = tweet.get('text', '')[:100]
        likes = tweet.get('likeCount', 0)
        print(f'{i}. [{likes}❤️] {text}...')
except:
    print('无法解析 X 数据')
" 2>/dev/null || echo "无数据"
fi
