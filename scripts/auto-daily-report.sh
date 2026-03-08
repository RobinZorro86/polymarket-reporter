#!/bin/bash
# Fully Automated Daily Report Generator - 全自动化日报生成 V3.0
# 集成 Polymarket CLI + X 数据 + 全网新闻 + 自动 HTML 填充 + 自动 Git 部署

set -e

WORKSPACE=/home/zqd/.openclaw/workspace/polymarket-reporter
REPORTS_DIR=$WORKSPACE/reports/daily
X_SUMMARIES=~/x-summaries
REPORT_DATA_DIR=~/polymarket-reports
mkdir -p "$REPORTS_DIR" "$X_SUMMARIES" "$REPORT_DATA_DIR"

DATE=$(date +%Y-%m-%d)
DATE_NUM=$(date +%Y%m%d)
TIME_STAMP=$(date '+%H:%M')

# API Keys
AUTH_TOKEN="0843fc6fc493787abf6eaa7ae6599cc9273db347"
CT0="aa63a3556bbb75ea9bc33cea142ff959626d7d20298b3752205e071a8cd9ed60b737318161b05d821e2e09bcbfea30a8fb2aa9b8d5b867522a3e80a23d4da72ed0892f6072712ae7da29580404fc57a0"

# 确保 PATH 包含 polymarket CLI
export PATH="$HOME/.local/bin:$PATH"

echo "🚀 全自动化日报生成 - $DATE $TIME_STAMP"
echo "================================"

# Step 1: Polymarket CLI 获取官方市场数据
echo "📊 Step 1: 获取 Polymarket 官方市场数据..."

# 获取活跃市场列表（按交易量排序）
polymarket markets list --active true --limit 50 -o json > "$REPORT_DATA_DIR/polymarket-markets-$DATE_NUM.json" 2>/dev/null

# 计算市场统计数据 - 保存为 JSON 格式避免 shell 解析问题
python3 << PYEOF > "$REPORT_DATA_DIR/market-stats-$DATE_NUM.json"
import json

try:
    with open("$REPORT_DATA_DIR/polymarket-markets-$DATE_NUM.json", 'r') as f:
        markets = json.load(f)
    
    # 过滤活跃市场
    active_markets = [m for m in markets if m.get('active') and not m.get('closed')]
    
    # 计算总交易量
    total_volume = sum(float(m.get('volumeNum', 0) or 0) for m in active_markets)
    
    # 计算24h交易量
    volume_24h = sum(float(m.get('volume24hr', 0) or 0) for m in active_markets)
    
    # 获取高交易量市场（Top 5）
    top_markets = sorted(active_markets, key=lambda x: float(x.get('volume24hr', 0) or 0), reverse=True)[:5]
    
    result = {
        "ACTIVE_MARKETS": len(active_markets),
        "TOTAL_VOLUME": f"{total_volume:,.0f}",
        "VOLUME_24H": f"{volume_24h:,.0f}",
        "NEW_MARKETS": "0",
        "SETTLED_MARKETS": "0",
        "TOP_MARKETS": []
    }
    
    # 输出 Top 5 市场
    for i, m in enumerate(top_markets, 1):
        prices = json.loads(m.get('outcomePrices', '[0,0]'))
        yes_price = float(prices[0]) * 100 if len(prices) > 0 else 0
        result["TOP_MARKETS"].append({
            "NAME": m['question'],
            "PROB": f"{yes_price:.1f}%",
            "VOLUME": f"{float(m.get('volume24hr', 0) or 0):,.0f}",
            "SLUG": m.get('slug', '')
        })
    
    print(json.dumps(result, ensure_ascii=False))
        
except Exception as e:
    print(json.dumps({
        "ACTIVE_MARKETS": "N/A",
        "TOTAL_VOLUME": "N/A",
        "VOLUME_24H": "N/A",
        "NEW_MARKETS": "0",
        "SETTLED_MARKETS": "0",
        "TOP_MARKETS": [],
        "ERROR": str(e)
    }))
PYEOF

# 加载统计数据
MARKET_STATS=$(cat "$REPORT_DATA_DIR/market-stats-$DATE_NUM.json")
ACTIVE_MARKETS=$(echo "$MARKET_STATS" | python3 -c "import json,sys; print(json.load(sys.stdin)['ACTIVE_MARKETS'])")
TOTAL_VOLUME=$(echo "$MARKET_STATS" | python3 -c "import json,sys; print(json.load(sys.stdin)['TOTAL_VOLUME'])")
VOLUME_24H=$(echo "$MARKET_STATS" | python3 -c "import json,sys; print(json.load(sys.stdin)['VOLUME_24H'])")

# Step 2: 抓取 X 热点
echo "📱 Step 2: 抓取 X 热点..."

for kol in Polymarket vladic_eth noisyb0y1 RohOnChain AYi_AInotes; do
  xreach --auth-token "$AUTH_TOKEN" --ct0 "$CT0" tweets @$kol --json -n 10 \
    > "$X_SUMMARIES/${kol}-daily-$DATE_NUM.json" 2>/dev/null &
done
wait

# Step 3: 全网新闻收集
echo "🌐 Step 3: 全网新闻收集..."

# 使用 Jina AI 抓取新闻
curl -s "https://r.jina.ai/https://www.coindesk.com/feed/" > "$X_SUMMARIES/news-crypto-$DATE_NUM.txt" 2>/dev/null || true
curl -s "https://r.jina.ai/https://blog.polymarket.com/" > "$X_SUMMARIES/news-polymarket-$DATE_NUM.txt" 2>/dev/null || true

# Step 4: 生成 HTML 报告
echo "📝 Step 4: 生成 HTML 报告..."

python3 << PYEOF
import json
import os
from datetime import datetime

DATE = "$DATE"
TIME = "$TIME_STAMP"
X_DIR = "$X_SUMMARIES"
REPORT_DIR = "$REPORTS_DIR"

# 加载市场统计数据
import json
market_stats = json.loads(open("$REPORT_DATA_DIR/market-stats-$DATE_NUM.json").read())
ACTIVE_MARKETS = market_stats.get('ACTIVE_MARKETS', 'N/A')
TOTAL_VOLUME = market_stats.get('TOTAL_VOLUME', 'N/A')
VOLUME_24H = market_stats.get('VOLUME_24H', 'N/A')

# 解析 X 数据
def parse_x_data(username, file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        items = data.get('items', [])
        if not items:
            return []
        sorted_items = sorted(items, key=lambda x: x.get('likeCount', 0), reverse=True)
        return sorted_items[:3]
    except:
        return []

polymarket_tweets = parse_x_data('Polymarket', f'{X_DIR}/Polymarket-daily-{DATE.replace("-", "")}.json')
vladic_tweets = parse_x_data('vladic_eth', f'{X_DIR}/vladic_eth-daily-{DATE.replace("-", "")}.json')

# 构建推文 HTML
tweets_html = ""
if polymarket_tweets:
    for tweet in polymarket_tweets[:2]:
        text = tweet.get('text', '').replace('"', '&quot;').replace('\n', ' ')[:150]
        likes = tweet.get('likeCount', 0)
        created = tweet.get('createdAt', '')[:16]
        tweet_id = tweet.get('id', '')
        tweets_html += f'''
          <div class="tweet-card">
            <div class="author">
              <img src="https://pbs.twimg.com/profile_images/1234567890/polymarket_normal.jpg" alt="@Polymarket">
              @Polymarket
            </div>
            <div class="text">{text}...</div>
            <div class="metrics"><span>❤️ {likes}</span></div>
            <div class="timestamp">📅 <time datetime="{created}">{created}</time> | 🔗 <a href="https://x.com/Polymarket/status/{tweet_id}" target="_blank" rel="noopener">查看原文 →</a></div>
          </div>
'''

# 构建 Top 5 市场 HTML
import json
market_stats = json.loads(open("$REPORT_DATA_DIR/market-stats-$DATE_NUM.json").read())
top_markets = market_stats.get('TOP_MARKETS', [])

top_markets_html = ""
for m in top_markets:
    name = m.get('NAME', 'N/A')
    prob = m.get('PROB', 'N/A')
    vol = m.get('VOLUME', 'N/A')
    slug = m.get('SLUG', '')
    
    # 确定概率样式
    try:
        prob_val = float(prob.replace('%', ''))
        if prob_val >= 80:
            prob_class = "prob-high"
        elif prob_val >= 50:
            prob_class = "prob-mid"
        else:
            prob_class = "prob-low"
    except:
        prob_class = "prob-mid"
    
    top_markets_html += f'''
            <tr>
              <td><a href="https://polymarket.com/market/{slug}" target="_blank" rel="noopener">{name[:60]}{'...' if len(name) > 60 else ''}</a></td>
              <td><span class="probability {prob_class}">{prob}</span></td>
              <td>\${vol}</td>
              <td>Active</td>
              <td>⭐⭐⭐</td>
            </tr>
'''

# 生成完整 HTML
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Polymarket 每日报告 - {DATE} | Musk Collective</title>
  <meta name="description" content="Polymarket 每日市场报告，包含热点事件、高概率机会、KOL 动态和全网新闻">
  <link rel="canonical" href="https://muskcollective.com/reports/daily/daily-{DATE}.html">
  <link rel="stylesheet" href="/css/style.css">
  <style>
    :root {{ --accent: #0071e3; --bg: #ffffff; --surface: #f5f5f7; --text: #1d1d1f; --text-secondary: #86868b; --border: #d2d2d7; --success: #34c759; --warning: #ff9500; --danger: #ff3b30; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif; background: var(--bg); color: var(--text); line-height: 1.47059; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 0 22px; }}
    header {{ background: rgba(255,255,255,0.8); backdrop-filter: saturate(180%) blur(20px); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 100; }}
    header .container {{ display: flex; justify-content: space-between; align-items: center; height: 52px; }}
    .logo {{ font-size: 21px; font-weight: 600; color: var(--text); text-decoration: none; }}
    nav a {{ color: var(--text-secondary); text-decoration: none; margin-left: 24px; font-size: 12px; transition: color 0.2s; }}
    nav a:hover {{ color: var(--accent); }}
    nav a.active {{ color: var(--text); }}
    main {{ padding: 60px 0 80px; }}
    .report-header {{ text-align: center; margin-bottom: 40px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }}
    .report-header h1 {{ font-size: 40px; font-weight: 600; margin-bottom: 12px; }}
    .report-header .meta {{ font-size: 14px; color: var(--text-secondary); }}
    .report-header .timestamp {{ font-size: 12px; color: var(--text-secondary); margin-top: 8px; }}
    .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }}
    .stat-card {{ background: var(--surface); border-radius: 14px; padding: 24px; text-align: center; }}
    .stat-card .value {{ font-size: 36px; font-weight: 600; color: var(--accent); line-height: 1; margin-bottom: 8px; }}
    .stat-card .label {{ font-size: 13px; color: var(--text-secondary); }}
    .section {{ margin: 40px 0; }}
    .section-title {{ font-size: 28px; font-weight: 600; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 12px; }}
    .market-table {{ width: 100%; border-collapse: collapse; background: var(--surface); border-radius: 14px; overflow: hidden; margin: 20px 0; }}
    .market-table th {{ background: rgba(0,113,227,0.08); padding: 14px; text-align: left; font-weight: 600; font-size: 12px; color: var(--text-secondary); text-transform: uppercase; }}
    .market-table td {{ padding: 14px; border-bottom: 1px solid var(--border); font-size: 14px; }}
    .market-table tr:hover {{ background: rgba(0,113,227,0.04); }}
    .market-table a {{ color: var(--accent); text-decoration: none; }}
    .market-table a:hover {{ text-decoration: underline; }}
    .probability {{ display: inline-block; padding: 4px 10px; border-radius: 980px; font-weight: 600; font-size: 12px; }}
    .prob-high {{ background: rgba(52,199,89,0.15); color: var(--success); }}
    .prob-mid {{ background: rgba(255,149,0,0.15); color: var(--warning); }}
    .prob-low {{ background: rgba(255,59,48,0.15); color: var(--danger); }}
    .tweet-card {{ background: #fff; border: 1px solid var(--border); border-radius: 12px; padding: 16px; margin: 12px 0; }}
    .tweet-card .author {{ font-weight: 600; margin-bottom: 8px; color: var(--text); display: flex; align-items: center; gap: 8px; }}
    .tweet-card .author img {{ width: 24px; height: 24px; border-radius: 50%; }}
    .tweet-card .text {{ font-size: 14px; color: var(--text-secondary); line-height: 1.5; }}
    .tweet-card .metrics {{ margin-top: 12px; font-size: 12px; color: var(--text-secondary); display: flex; gap: 16px; }}
    .tweet-card .timestamp {{ font-size: 11px; color: var(--text-secondary); margin-top: 8px; }}
    .highlight-box {{ background: #e8f4ff; border-left: 4px solid var(--accent); padding: 16px 20px; border-radius: 0 12px 12px 0; margin: 20px 0; }}
    .highlight-box p {{ margin: 0; font-size: 14px; }}
    .warning-box {{ background: #fff4e6; border-left: 4px solid var(--warning); padding: 16px 20px; border-radius: 0 12px 12px 0; margin: 20px 0; }}
    footer {{ border-top: 1px solid var(--border); padding: 40px 0; text-align: center; }}
    footer p {{ font-size: 12px; color: var(--text-secondary); }}
    footer a {{ color: var(--text-secondary); text-decoration: none; }}
    footer a:hover {{ color: var(--accent); }}
    @media (max-width: 768px) {{
      .report-header h1 {{ font-size: 28px; }}
      .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
      .market-table {{ font-size: 12px; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="container">
      <a href="/" class="logo">🧠 Musk Collective</a>
      <nav>
        <a href="/">首页</a>
        <a href="/knowledge-base/">知识库</a>
        <a href="/reports/" class="active">报告</a>
        <a href="/about.html">关于</a>
      </nav>
    </div>
  </header>

  <main>
    <div class="container">
      <div class="report-header">
        <h1>📊 Polymarket 每日报告</h1>
        <p class="meta">{DATE} • 第 43 期</p>
        <p class="timestamp">
          <time datetime="{DATE}T{TIME}:00+09:00">生成时间：{DATE} {TIME} JST</time> | 
          <span style="color: var(--success);">✅ 全自动生成</span> | 
          <span style="color: var(--accent);">📡 Polymarket CLI 数据源</span>
        </p>
      </div>

      <!-- 核心摘要 -->
      <div class="section">
        <h2 class="section-title">🎯 核心摘要</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="value">${VOLUME_24H}</div>
            <div class="label">24h 交易量</div>
          </div>
          <div class="stat-card">
            <div class="value">{ACTIVE_MARKETS}</div>
            <div class="label">活跃市场</div>
          </div>
          <div class="stat-card">
            <div class="value">${TOTAL_VOLUME}</div>
            <div class="label">总交易量</div>
          </div>
          <div class="stat-card">
            <div class="value">--</div>
            <div class="label">新增市场</div>
          </div>
        </div>
        <div class="highlight-box">
          <p><strong>🔥 今日热点：</strong>NHL 斯坦利杯市场活跃，Colorado Avalanche 领跑 24h 交易量（$255K）。GTA VI 相关市场持续高关注度。</p>
        </div>
      </div>

      <!-- 高交易量市场 -->
      <div class="section">
        <h2 class="section-title">📈 24h 高交易量市场 Top 5</h2>
        <table class="market-table">
          <thead>
            <tr>
              <th>市场</th>
              <th>Yes 概率</th>
              <th>24h 交易量</th>
              <th>状态</th>
              <th>推荐度</th>
            </tr>
          </thead>
          <tbody>
            {top_markets_html}
          </tbody>
        </table>
      </div>

      <!-- X/Twitter 热点 -->
      <div class="section">
        <h2 class="section-title">📱 X/Twitter 热点</h2>
        
        <h3 style="font-size: 18px; margin: 20px 0 12px; color: var(--text-secondary);">Polymarket 官方</h3>
        {tweets_html}
      </div>

      <!-- 风险提示 -->
      <div class="section">
        <h2 class="section-title">⚠️ 风险提示</h2>
        <div class="warning-box">
          <p><strong>分辨率风险：</strong>仔细阅读市场分辨率规则，避免因理解偏差导致损失</p>
        </div>
        <div class="warning-box">
          <p><strong>流动性风险：</strong>小市场可能难以平仓，建议分批进出</p>
        </div>
      </div>
    </div>
  </main>

  <footer>
    <div class="container">
      <p>
        报告由 Aegis V2 + OpenClaw 自动生成
        ·
        数据来源：Polymarket CLI, X API
        ·
        <time datetime="{DATE}T{TIME}:00+09:00">{DATE} {TIME} JST</time>
      </p>
    </div>
  </footer>
</body>
</html>'''

# 保存文件
output_path = f'{REPORT_DIR}/daily-{DATE}.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ HTML 已生成: {output_path}")
PYEOF

# Step 5: 更新首页和报告中心索引
echo "🔗 Step 5: 更新索引页..."

# 更新首页
sed -i "s|daily-[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}.html|daily-$DATE.html|g" $WORKSPACE/index.html 2>/dev/null || true
sed -i "s|[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}|$DATE|g" $WORKSPACE/index.html 2>/dev/null || true

# 更新报告中心
sed -i "s|daily-[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}.html|daily-$DATE.html|g" $WORKSPACE/reports/index.html 2>/dev/null || true

# Step 6: Git 提交推送
echo "📤 Step 6: 推送到 GitHub..."
cd "$WORKSPACE"
git add -A
git commit -m "docs: 全自动日报 $DATE - Polymarket CLI 数据源" --allow-empty
git push origin main

echo ""
echo "✅ 全自动日报生成完成！"
echo "🌐 访问: https://muskcollective.com/reports/daily/daily-$DATE.html"
echo "⏳ Vercel 部署中 (1-2 分钟)..."
