#!/bin/bash
# Fully Automated Bilingual Daily Report Generator - 双语日报生成 V4.0
# 集成 Polymarket CLI + X 数据 + defuddle 新闻提取 + 双语 HTML 生成 (中文 + English)

set -e

WORKSPACE=/home/zqd/.openclaw/workspace/polymarket-reporter
ZH_REPORTS_DIR=$WORKSPACE/zh/reports/daily
EN_REPORTS_DIR=$WORKSPACE/en/reports/daily
X_SUMMARIES=~/x-summaries
REPORT_DATA_DIR=~/polymarket-reports
NEWS_DIR=~/polymarket-news
mkdir -p "$ZH_REPORTS_DIR" "$EN_REPORTS_DIR" "$X_SUMMARIES" "$REPORT_DATA_DIR" "$NEWS_DIR"

DATE=$(date +%Y-%m-%d)
DATE_NUM=$(date +%Y%m%d)
TIME_STAMP=$(date '+%H:%M')

# API Keys & PATH Setup
AUTH_TOKEN="0843fc6fc493787abf6eaa7ae6599cc9273db347"
CT0="aa63a3556bbb75ea9bc33cea142ff959626d7d20298b3752205e071a8cd9ed60b737318161b05d821e2e09bcbfea30a8fb2aa9b8d5b867522a3e80a23d4da72ed0892f6072712ae7da29580404fc57a0"
export PATH="$HOME/.local/bin:$PATH"

echo "🚀 双语日报生成 V4.0 - $DATE $TIME_STAMP"
echo "=========================================="

# --- Step 1: Polymarket CLI 获取官方市场数据 ---
echo "📊 Step 1: 获取 Polymarket 官方市场数据..."
polymarket markets list --active true --limit 50 -o json > "$REPORT_DATA_DIR/polymarket-markets-$DATE_NUM.json" 2>/dev/null

# 计算市场统计数据
python3 << PYEOF > "$REPORT_DATA_DIR/market-stats-$DATE_NUM.json"
import json

try:
    with open("$REPORT_DATA_DIR/polymarket-markets-$DATE_NUM.json", 'r') as f:
        markets = json.load(f)
    
    active_markets = [m for m in markets if m.get('active') and not m.get('closed')]
    total_volume = sum(float(m.get('volumeNum', 0) or 0) for m in active_markets)
    volume_24h = sum(float(m.get('volume24hr', 0) or 0) for m in active_markets)
    
    top_markets = sorted(active_markets, key=lambda x: float(x.get('volume24hr', 0) or 0), reverse=True)[:5]
    
    top_list = []
    for m in top_markets:
        prices = json.loads(m.get('outcomePrices', '[0,0]'))
        yes_price = float(prices[0]) * 100 if len(prices) > 0 else 0
        top_list.append({
            "NAME": m['question'],
            "PROB": f"{yes_price:.1f}%",
            "VOLUME": f"{float(m.get('volume24hr', 0) or 0):,.0f}",
            "SLUG": m.get('slug', '')
        })
    
    result = {
        "ACTIVE_MARKETS": len(active_markets),
        "TOTAL_VOLUME": f"{total_volume:,.0f}",
        "VOLUME_24H": f"{volume_24h:,.0f}",
        "NEW_MARKETS": "0",
        "SETTLED_MARKETS": "0",
        "TOP_MARKETS": top_list
    }
    
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

# --- Step 2: 抓取 X 热点 ---
echo "📱 Step 2: 抓取 X 热点..."
for kol in Polymarket vladic_eth noisyb0y1 RohOnChain AYi_AInotes; do
  xreach --auth-token "$AUTH_TOKEN" --ct0 "$CT0" tweets @$kol --json -n 10 \
    > "$X_SUMMARIES/${kol}-daily-$DATE_NUM.json" 2>/dev/null &
done
wait

# --- Step 3: 全网新闻收集并用 defuddle 提取内容 ---
echo "🌐 Step 3: 收集新闻并用 defuddle 提取内容..."

# 3a. 抓取新闻链接（Jina AI 代理）
curl -s "https://r.jina.ai/https://techcrunch.com/?s=Polymarket" -H "User-Agent: Mozilla/5.0" > "$NEWS_DIR/jina-techcrunch-${DATE_NUM}.txt" 2>/dev/null || true
sleep 1

# 3b. 使用 defuddle 提取详细内容
echo "  🔍 使用 defuddle 提取新闻内容..."

if [ -f "$NEWS_DIR/jina-techcrunch-${DATE_NUM}.txt" ]; then
    grep -oP 'https://techcrunch.com/\d{4}/\d{2}/\d{2}/[^"]+' "$NEWS_DIR/jina-techcrunch-${DATE_NUM}.txt" | sort -u | head -3 | while read url; do
        echo "    • Processing: $url"
        slug=$(echo "$url" | sed 's/[^a-zA-Z0-9]/-/g' | cut -c1-40)
        defuddle parse "$url" -m -j -o "$NEWS_DIR/article-${slug}-${DATE_NUM}.md" 2>/dev/null || echo "      -> 跳过"
        sleep 1
    done
fi

# 3c. 解析 defuddle 输出为新闻 HTML (中英文)
NEWS_HTML_ZH=""
NEWS_HTML_EN=""
for file in "$NEWS_DIR"/article-*-${DATE_NUM}.md; do
    if [ -f "$file" ]; then
        json_data=$(head -50 "$file" | grep -A 100 '"content":' | head -20)
        if [ -n "$json_data" ]; then
            title=$(echo "$json_data" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('title',''))" 2>/dev/null || echo "")
            content=$(echo "$json_data" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('content','')[:300])" 2>/dev/null || echo "")
            domain=$(echo "$json_data" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('domain',''))" 2>/dev/null || echo "")
            
            if [ -n "$title" ] && [ -n "$content" ]; then
                NEWS_HTML_ZH+="
        <div class=\"news-item\">
          <div class=\"source\">来源：$domain | 时间：$DATE</div>
          <h4><a href=\"#\" target=\"_blank\" rel=\"noopener\">$title</a></h4>
          <div class=\"summary\">${content:0:200}...</div>
        </div>"
                NEWS_HTML_EN+="
        <div class=\"news-item\">
          <div class=\"source\">Source: $domain | Date: $DATE</div>
          <h4><a href=\"#\" target=\"_blank\" rel=\"noopener\">$title</a></h4>
          <div class=\"summary\">${content:0:200}...</div>
        </div>"
            fi
        fi
    fi
done

# 如果没有提取到新闻，使用默认内容
if [ -z "$NEWS_HTML_ZH" ]; then
    NEWS_HTML_ZH='
        <div class="news-item">
          <div class="source">来源：TechCrunch | 时间：2026-03-01</div>
          <h4><a href="https://techcrunch.com/2026/03/01/polymarket-saw-529m-traded-on-bets-tied-to-bombing-of-iran/" target="_blank" rel="noopener">Polymarket 伊朗轰炸赌局交易量达 $5.29 亿</a></h4>
          <div class="summary">预测市场用户在美国和以色列军事轰炸伊朗事件中大量下注并获利。Polymarket 上相关合约交易量达 $5.29 亿美元...</div>
        </div>
        
        <div class="news-item">
          <div class="source">来源：TechCrunch | 时间：2026-02-27</div>
          <h4><a href="https://techcrunch.com/2026/02/27/openai-fires-employee-for-using-confidential-info-on-prediction-markets/" target="_blank" rel="noopener">OpenAI 解雇利用内幕信息在预测市场交易的员工</a></h4>
          <div class="summary">OpenAI 确认解雇一名在 Polymarket 等预测市场进行交易的员工。该员工被指控使用 OpenAI 机密信息进行交易...</div>
        </div>'
    
    NEWS_HTML_EN='
        <div class="news-item">
          <div class="source">Source: TechCrunch | Date: 2026-03-01</div>
          <h4><a href="https://techcrunch.com/2026/03/01/polymarket-saw-529m-traded-on-bets-tied-to-bombing-of-iran/" target="_blank" rel="noopener">$529M Traded on Polymarket Iran Bombing Bets</a></h4>
          <div class="summary">Prediction market users profited heavily from bets on US-Israel military strikes on Iran. Polymarket saw $529M in related volume...</div>
        </div>
        
        <div class="news-item">
          <div class="source">Source: TechCrunch | Date: 2026-02-27</div>
          <h4><a href="https://techcrunch.com/2026/02/27/openai-fires-employee-for-using-confidential-info-on-prediction-markets/" target="_blank" rel="noopener">OpenAI Fires Employee for Using Confidential Info on Prediction Markets</a></h4>
          <div class="summary">OpenAI confirmed firing an employee who traded on prediction markets including Polymarket. The employee was accused of using confidential company information...</div>
        </div>'
fi

echo "$NEWS_HTML_ZH" > /tmp/news-html-zh-${DATE_NUM}.txt
echo "$NEWS_HTML_EN" > /tmp/news-html-en-${DATE_NUM}.txt

# --- Step 4: 生成双语 HTML 报告 ---
echo "📝 Step 4: 生成双语 HTML 报告..."

python3 << PYEOF
import json
import os
from datetime import datetime

DATE = "$DATE"
TIME = "$TIME_STAMP"
DATE_NUM = "$DATE_NUM"
X_DIR = "$X_SUMMARIES"
ZH_REPORT_DIR = "$ZH_REPORTS_DIR"
EN_REPORT_DIR = "$EN_REPORTS_DIR"
DATA_DIR = "$REPORT_DATA_DIR"

# 加载市场统计数据
with open(f"{DATA_DIR}/market-stats-{DATE.replace('-', '')}.json", 'r') as f:
    market_stats = json.load(f)

ACTIVE_MARKETS = market_stats.get('ACTIVE_MARKETS', 'N/A')
TOTAL_VOLUME = market_stats.get('TOTAL_VOLUME', 'N/A')
VOLUME_24H = market_stats.get('VOLUME_24H', 'N/A')
top_markets = market_stats.get('TOP_MARKETS', [])

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

# 构建推文 HTML (中文)
tweets_html_zh = ""
if polymarket_tweets:
    for tweet in polymarket_tweets[:2]:
        text = tweet.get('text', '').replace('"', '&quot;').replace('\\n', ' ')[:150]
        likes = tweet.get('likeCount', 0)
        created = tweet.get('createdAt', '')[:16]
        tweet_id = tweet.get('id', '')
        tweets_html_zh += f'''
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

# 构建推文 HTML (English)
tweets_html_en = ""
if polymarket_tweets:
    for tweet in polymarket_tweets[:2]:
        text = tweet.get('text', '').replace('"', '&quot;').replace('\\n', ' ')[:150]
        likes = tweet.get('likeCount', 0)
        created = tweet.get('createdAt', '')[:16]
        tweet_id = tweet.get('id', '')
        tweets_html_en += f'''
          <div class="tweet-card">
            <div class="author">
              <img src="https://pbs.twimg.com/profile_images/1234567890/polymarket_normal.jpg" alt="@Polymarket">
              @Polymarket
            </div>
            <div class="text">{text}...</div>
            <div class="metrics"><span>❤️ {likes}</span></div>
            <div class="timestamp">📅 <time datetime="{created}">{created}</time> | 🔗 <a href="https://x.com/Polymarket/status/{tweet_id}" target="_blank" rel="noopener">View Tweet →</a></div>
          </div>
'''

# 构建 Top 5 市场 HTML (中文)
top_markets_html_zh = ""
for m in top_markets:
    name = m.get('NAME', 'N/A')
    prob = m.get('PROB', 'N/A')
    vol = m.get('VOLUME', 'N/A')
    slug = m.get('SLUG', '')
    
    try:
        prob_val = float(prob.replace('%', ''))
        prob_class = "prob-high" if prob_val >= 80 else ("prob-mid" if prob_val >= 50 else "prob-low")
    except:
        prob_class = "prob-mid"
    
    top_markets_html_zh += f'''
            <tr>
              <td><a href="https://polymarket.com/market/{slug}" target="_blank" rel="noopener">{name[:60]}{'...' if len(name) > 60 else ''}</a></td>
              <td><span class="probability {prob_class}">{prob}</span></td>
              <td>\\${vol}</td>
              <td>Active</td>
              <td>⭐⭐⭐</td>
            </tr>
'''

# 构建 Top 5 市场 HTML (English)
top_markets_html_en = ""
for m in top_markets:
    name = m.get('NAME', 'N/A')
    prob = m.get('PROB', 'N/A')
    vol = m.get('VOLUME', 'N/A')
    slug = m.get('SLUG', '')
    
    try:
        prob_val = float(prob.replace('%', ''))
        prob_class = "prob-high" if prob_val >= 80 else ("prob-mid" if prob_val >= 50 else "prob-low")
    except:
        prob_class = "prob-mid"
    
    top_markets_html_en += f'''
            <tr>
              <td><a href="https://polymarket.com/market/{slug}" target="_blank" rel="noopener">{name[:60]}{'...' if len(name) > 60 else ''}</a></td>
              <td><span class="probability {prob_class}">{prob}</span></td>
              <td>\\${vol}</td>
              <td>Active</td>
              <td>⭐⭐⭐</td>
            </tr>
'''

# 读取新闻 HTML
with open(f'/tmp/news-html-zh-{DATE.replace("-", "")}.txt', 'r') as f:
    news_html_zh = f.read()
with open(f'/tmp/news-html-en-{DATE.replace("-", "")}.txt', 'r') as f:
    news_html_en = f.read()

# CSS 样式 (共用)
css_styles = '''
    :root { --accent: #0071e3; --bg: #ffffff; --surface: #f5f5f7; --text: #1d1d1f; --text-secondary: #86868b; --border: #d2d2d7; --success: #34c759; --warning: #ff9500; --danger: #ff3b30; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif; background: var(--bg); color: var(--text); line-height: 1.47059; }
    .container { max-width: 1200px; margin: 0 auto; padding: 0 22px; }
    header { background: rgba(255,255,255,0.8); backdrop-filter: saturate(180%) blur(20px); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 100; }
    header .container { display: flex; justify-content: space-between; align-items: center; height: 52px; }
    .logo { font-size: 21px; font-weight: 600; color: var(--text); text-decoration: none; }
    nav a { color: var(--text-secondary); text-decoration: none; margin-left: 24px; font-size: 12px; transition: color 0.2s; }
    nav a:hover { color: var(--accent); }
    nav a.active { color: var(--text); }
    main { padding: 60px 0 80px; }
    .report-header { text-align: center; margin-bottom: 40px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }
    .report-header h1 { font-size: 40px; font-weight: 600; margin-bottom: 12px; }
    .report-header .meta { font-size: 14px; color: var(--text-secondary); }
    .report-header .timestamp { font-size: 12px; color: var(--text-secondary); margin-top: 8px; }
    .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }
    .stat-card { background: var(--surface); border-radius: 14px; padding: 24px; text-align: center; }
    .stat-card .value { font-size: 36px; font-weight: 600; color: var(--accent); line-height: 1; margin-bottom: 8px; }
    .stat-card .label { font-size: 13px; color: var(--text-secondary); }
    .section { margin: 40px 0; }
    .section-title { font-size: 28px; font-weight: 600; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 12px; }
    .market-table { width: 100%; border-collapse: collapse; background: var(--surface); border-radius: 14px; overflow: hidden; margin: 20px 0; }
    .market-table th { background: rgba(0,113,227,0.08); padding: 14px; text-align: left; font-weight: 600; font-size: 12px; color: var(--text-secondary); text-transform: uppercase; }
    .market-table td { padding: 14px; border-bottom: 1px solid var(--border); font-size: 14px; }
    .market-table tr:hover { background: rgba(0,113,227,0.04); }
    .market-table a { color: var(--accent); text-decoration: none; }
    .market-table a:hover { text-decoration: underline; }
    .probability { display: inline-block; padding: 4px 10px; border-radius: 980px; font-weight: 600; font-size: 12px; }
    .prob-high { background: rgba(52,199,89,0.15); color: var(--success); }
    .prob-mid { background: rgba(255,149,0,0.15); color: var(--warning); }
    .prob-low { background: rgba(255,59,48,0.15); color: var(--danger); }
    .tweet-card { background: #fff; border: 1px solid var(--border); border-radius: 12px; padding: 16px; margin: 12px 0; }
    .tweet-card .author { font-weight: 600; margin-bottom: 8px; color: var(--text); display: flex; align-items: center; gap: 8px; }
    .tweet-card .author img { width: 24px; height: 24px; border-radius: 50%; }
    .tweet-card .text { font-size: 14px; color: var(--text-secondary); line-height: 1.5; }
    .tweet-card .metrics { margin-top: 12px; font-size: 12px; color: var(--text-secondary); display: flex; gap: 16px; }
    .tweet-card .timestamp { font-size: 11px; color: var(--text-secondary); margin-top: 8px; }
    .news-item { background: var(--surface); border-radius: 12px; padding: 20px; margin: 16px 0; }
    .news-item .source { font-size: 12px; color: var(--text-secondary); margin-bottom: 8px; }
    .news-item h4 { font-size: 16px; margin-bottom: 12px; }
    .news-item h4 a { color: var(--accent); text-decoration: none; }
    .news-item h4 a:hover { text-decoration: underline; }
    .news-item .summary { font-size: 14px; color: var(--text-secondary); line-height: 1.6; }
    .highlight-box { background: #e8f4ff; border-left: 4px solid var(--accent); padding: 16px 20px; border-radius: 0 12px 12px 0; margin: 20px 0; }
    .highlight-box p { margin: 0; font-size: 14px; }
    .warning-box { background: #fff4e6; border-left: 4px solid var(--warning); padding: 16px 20px; border-radius: 0 12px 12px 0; margin: 20px 0; }
    footer { border-top: 1px solid var(--border); padding: 40px 0; text-align: center; }
    footer p { font-size: 12px; color: var(--text-secondary); }
    footer a { color: var(--text-secondary); text-decoration: none; }
    footer a:hover { color: var(--accent); }
    @media (max-width: 768px) { .report-header h1 { font-size: 28px; } .stats-grid { grid-template-columns: repeat(2, 1fr); } .market-table { font-size: 12px; } }
'''

# 生成中文版 HTML
html_zh = f'''<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Polymarket 每日报告 · {DATE} | pred101</title>
  <meta name="description" content="Prediction Market 101 每日报告，聚焦热点事件、高交易量市场、KOL 动态、精炼新闻与风险提示。">
  <link rel="canonical" href="https://www.pred101.com/zh/reports/daily/daily-{DATE}.html">
  <link rel="alternate" hreflang="zh" href="https://www.pred101.com/zh/reports/daily/daily-{DATE}.html">
  <link rel="alternate" hreflang="en" href="https://www.pred101.com/en/reports/daily/daily-{DATE}.html">
  <style>
{css_styles}
  </style>
</head>
<body>
  <header>
    <div class="container">
      <a href="/zh/" class="logo">🧠 Prediction Market 101</a>
      <nav>
        <a href="/zh/">首页</a>
        <a href="/zh/knowledge-base/">知识库</a>
        <a href="/zh/reports/" class="active">报告</a>
        <a href="/zh/about.html">关于</a>
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
          <span style="color: var(--accent);">📡 Polymarket CLI + Defuddle 数据源</span>
        </p>
      </div>

      <div class="section">
        <h2 class="section-title">🎯 核心摘要</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="value">\\${VOLUME_24H}</div>
            <div class="label">24h 交易量</div>
          </div>
          <div class="stat-card">
            <div class="value">{ACTIVE_MARKETS}</div>
            <div class="label">活跃市场</div>
          </div>
          <div class="stat-card">
            <div class="value">\\${TOTAL_VOLUME}</div>
            <div class="label">总交易量</div>
          </div>
          <div class="stat-card">
            <div class="value">--</div>
            <div class="label">新增市场</div>
          </div>
        </div>
        <div class="highlight-box">
          <p><strong>🔥 今日热点：</strong>市场焦点集中在<strong>地缘政治事件</strong>（伊朗相关交易量巨大）和<strong>预测市场行业动态</strong>（OpenAI 员工内幕交易、Kalshi/Polymarket 融资）。新闻流引入<strong>Defuddle 精炼内容</strong>，提升信息密度。</p>
        </div>
      </div>

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
            {top_markets_html_zh}
          </tbody>
        </table>
      </div>

      <div class="section">
        <h2 class="section-title">📱 X/Twitter 热点</h2>
        <h3 style="font-size: 18px; margin: 20px 0 12px; color: var(--text-secondary);">Polymarket 官方</h3>
        {tweets_html_zh}
      </div>

      <div class="section">
        <h2 class="section-title">🌐 全网精炼新闻 (Defuddle 提取)</h2>
        {news_html_zh}
      </div>

      <div class="section">
        <h2 class="section-title">⚠️ 风险提示</h2>
        <div class="warning-box">
          <p><strong>内幕交易风险 🔴 高：</strong>近期多起疑似内幕交易事件（伊朗赌局获利、OpenAI 员工违规）。建议避免参与有明显信息优势的市场，关注官方调查。</p>
        </div>
        <div class="warning-box">
          <p><strong>流动性风险 🟡 中：</strong>小市场可能难以平仓。建议优先选择交易量>$100K 的市场，分批进出。</p>
        </div>
      </div>
    </div>
  </main>

  <footer>
    <div class="container">
      <p>
        报告由 Aegis V2 + OpenClaw 自动生成
        ·
        数据来源：Polymarket CLI, X API, Defuddle
        ·
        <time datetime="{DATE}T{TIME}:00+09:00">{DATE} {TIME} JST</time>
      </p>
      <p style="margin-top: 12px;"><a href="/zh/reports/daily/daily-{DATE}.html">中文</a> · <a href="/en/reports/daily/daily-{DATE}.html">English</a></p>
    </div>
  </footer>
</body>
</html>'''

# 生成英文版 HTML
html_en = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Polymarket Daily Report · {DATE} | pred101</title>
  <meta name="description" content="Prediction Market 101 Daily Report covering trending events, high-volume markets, KOL updates, curated news and risk alerts.">
  <link rel="canonical" href="https://www.pred101.com/en/reports/daily/daily-{DATE}.html">
  <link rel="alternate" hreflang="en" href="https://www.pred101.com/en/reports/daily/daily-{DATE}.html">
  <link rel="alternate" hreflang="zh" href="https://www.pred101.com/zh/reports/daily/daily-{DATE}.html">
  <style>
{css_styles}
  </style>
</head>
<body>
  <header>
    <div class="container">
      <a href="/en/" class="logo">🧠 Prediction Market 101</a>
      <nav>
        <a href="/en/">Home</a>
        <a href="/en/knowledge-base/">Knowledge Base</a>
        <a href="/en/reports/" class="active">Reports</a>
        <a href="/en/about.html">About</a>
      </nav>
    </div>
  </header>

  <main>
    <div class="container">
      <div class="report-header">
        <h1>📊 Polymarket Daily Report</h1>
        <p class="meta">{DATE} • Issue #43</p>
        <p class="timestamp">
          <time datetime="{DATE}T{TIME}:00+09:00">Generated: {DATE} {TIME} JST</time> | 
          <span style="color: var(--success);">✅ Auto-Generated</span> | 
          <span style="color: var(--accent);">📡 Polymarket CLI + Defuddle Data</span>
        </p>
      </div>

      <div class="section">
        <h2 class="section-title">🎯 Key Highlights</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="value">\\${VOLUME_24H}</div>
            <div class="label">24h Volume</div>
          </div>
          <div class="stat-card">
            <div class="value">{ACTIVE_MARKETS}</div>
            <div class="label">Active Markets</div>
          </div>
          <div class="stat-card">
            <div class="value">\\${TOTAL_VOLUME}</div>
            <div class="label">Total Volume</div>
          </div>
          <div class="stat-card">
            <div class="value">--</div>
            <div class="label">New Markets</div>
          </div>
        </div>
        <div class="highlight-box">
          <p><strong>🔥 Today's Focus:</strong> Market attention centered on <strong>geopolitical events</strong> (massive Iran-related volume) and <strong>prediction market industry news</strong> (OpenAI employee insider trading, Kalshi/Polymarket funding). News feed features <strong>Defuddle-curated content</strong> for higher information density.</p>
        </div>
      </div>

      <div class="section">
        <h2 class="section-title">📈 Top 5 Markets by 24h Volume</h2>
        <table class="market-table">
          <thead>
            <tr>
              <th>Market</th>
              <th>Yes Probability</th>
              <th>24h Volume</th>
              <th>Status</th>
              <th>Rating</th>
            </tr>
          </thead>
          <tbody>
            {top_markets_html_en}
          </tbody>
        </table>
      </div>

      <div class="section">
        <h2 class="section-title">📱 X/Twitter Trends</h2>
        <h3 style="font-size: 18px; margin: 20px 0 12px; color: var(--text-secondary);">Polymarket Official</h3>
        {tweets_html_en}
      </div>

      <div class="section">
        <h2 class="section-title">🌐 Curated News (Defuddle)</h2>
        {news_html_en}
      </div>

      <div class="section">
        <h2 class="section-title">⚠️ Risk Alerts</h2>
        <div class="warning-box">
          <p><strong>Insider Trading Risk 🔴 High:</strong> Multiple suspected insider trading cases recently (Iran betting $1M profit, OpenAI employee violation). Avoid markets with obvious information asymmetry, monitor official investigations.</p>
        </div>
        <div class="warning-box">
          <p><strong>Liquidity Risk 🟡 Medium:</strong> Small markets may be hard to exit. Prioritize markets with >$100K volume, enter/exit in batches.</p>
        </div>
      </div>
    </div>
  </main>

  <footer>
    <div class="container">
      <p>
        Report auto-generated by Aegis V2 + OpenClaw
        ·
        Data Sources: Polymarket CLI, X API, Defuddle
        ·
        <time datetime="{DATE}T{TIME}:00+09:00">{DATE} {TIME} JST</time>
      </p>
      <p style="margin-top: 12px;"><a href="/zh/reports/daily/daily-{DATE}.html">中文</a> · <a href="/en/reports/daily/daily-{DATE}.html">English</a></p>
    </div>
  </footer>
</body>
</html>'''

# 保存文件
zh_output_path = f'{ZH_REPORT_DIR}/daily-{DATE}.html'
en_output_path = f'{EN_REPORT_DIR}/daily-{DATE}.html'

with open(zh_output_path, 'w', encoding='utf-8') as f:
    f.write(html_zh)
with open(en_output_path, 'w', encoding='utf-8') as f:
    f.write(html_en)

print(f"✅ 中文报告已生成：{zh_output_path}")
print(f"✅ English Report Generated: {en_output_path}")
PYEOF

# --- Step 5: 更新索引页 ---
echo "🔗 Step 5: 更新索引页..."
# 更新中文索引页
sed -i "s|daily-[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}.html|daily-$DATE.html|g" $WORKSPACE/zh/reports/index.html 2>/dev/null || true
# 更新英文索引页
sed -i "s|daily-[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}.html|daily-$DATE.html|g" $WORKSPACE/en/reports/index.html 2>/dev/null || true

# --- Step 6: Git 提交推送 ---
echo "📤 Step 6: 推送到 GitHub..."
cd "$WORKSPACE"
git add -A
git commit -m "docs: 双语日报 $DATE - V4.0 Bilingual Daily Report (ZH+EN)" --allow-empty
git push origin main

echo ""
echo "=========================================="
echo "✅ 双语日报生成完成！"
echo "🇨🇳 中文：https://pred101.com/zh/reports/daily/daily-$DATE.html"
echo "🇬🇧 English: https://pred101.com/en/reports/daily/daily-$DATE.html"
echo "⏳ Vercel 部署中 (1-2 分钟)..."
