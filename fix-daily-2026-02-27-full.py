#!/usr/bin/env python3
"""Fix all Chinese remnants in en/reports/daily/daily-2026-02-27.html"""

FILE = "en/reports/daily/daily-2026-02-27.html"

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open(FILE + ".backup3", 'w', encoding='utf-8') as f:
    f.write(content)

replacements = [
    # Meta tags
    ('<meta name="description" content="Polymarket 预测市场信息聚合 Report，涵盖 Latest News、行业研 Report、Social Media Buzz、Arbitrage Strategies、Risk Warnings 等。">',
     '<meta name="description" content="Polymarket prediction market intelligence report covering latest news, industry research, social media buzz, arbitrage strategies, and risk warnings.">'),
    
    ('<meta name="keywords" content="Polymarket, 预测市场，套利，加密货币，交易策略">',
     '<meta name="keywords" content="Polymarket, prediction market, arbitrage, cryptocurrency, trading strategy">'),
    
    ('<meta property="og:description" content="Polymarket 预测市场信息聚合 Report，涵盖 Latest News、套利策略、Risk Warnings 等。">',
     '<meta property="og:description" content="Polymarket prediction market report covering latest news, arbitrage strategies, and risk warnings.">'),
    
    ('"description": "Polymarket 预测市场信息聚合 Report，涵盖 Latest News、套利策略、Risk Warnings 等"',
     '"description": "Polymarket prediction market report covering latest news, arbitrage strategies, and risk warnings"'),
    
    # Navigation
    ('<a href="/en/reports/">全部 Reports</a>',
     '<a href="/en/reports/">All Reports</a>'),
    
    ('返回 Home',
     '← Back to Home'),
    
    # Content - Latest News
    ('<strong>15 分钟 Ultra short-term 加密市场上线</strong> - 5 分钟涨跌市场已支持 (x.com/Polymarket)',
     '<strong>15-minute ultra short-term crypto markets launch</strong> - 5-minute up/down markets now supported (x.com/Polymarket)'),
    
    ('<strong>US market launch delayed</strong> - 原定 2025-上线计划推迟 (sportico.com)',
     '<strong>US market launch delayed</strong> - Original 2025 launch plan postponed (sportico.com)'),
    
    # Content - Industry Research
    ('<h2>📌 行业研 Report</h2>',
     '<h2>📌 Industry Research</h2>'),
    
    ('<strong>预测市场爆发式增长 2025</strong>',
     '<strong>Prediction market explosive growth in 2025</strong>'),
    
    ('<strong>Kalshi vs Polymarket competition analysis</strong> - Cross-platform arbitrage 机会研究 (cryptonews.com)',
     '<strong>Kalshi vs Polymarket competition analysis</strong> - Cross-platform arbitrage opportunity research (cryptonews.com)'),
    
    # Content - Social Media
    ('<strong>ZachXBT 调查引发 200 万美元押注</strong>',
     '<strong>ZachXBT investigation sparks $2M bets</strong>'),
    
    # Content - Twitter Trending
    ('<strong>@Polymarket</strong>: 29% probability 2026 -通胀超过 3%',
     '<strong>@Polymarket</strong>: 29% probability 2026 inflation exceeds 3%'),
    
    ('<strong>@AFpost</strong>: 美国攻击伊朗 probability 53%，较上周 +13%',
     '<strong>@AFpost</strong>: US attack on Iran probability 53%, +13% from last week'),
    
    ('<strong>@inviteaccess</strong>: 5 分钟 BTC 市场火爆，用户赚取巨额收益',
     '<strong>@inviteaccess</strong>: 5-minute BTC markets hot, users earn massive returns'),
    
    # Content - Arbitrage Strategies
    ('<h2>📌 Arbitrage Strategies</h2>',
     '<h2>📌 Arbitrage Strategies</h2>'),
    
    ('<strong>Bot arbitrage dominates market</strong> - 机器人 - 赚 41 万美元案例 (finance.yahoo.com)',
     '<strong>Bot arbitrage dominates market</strong> - Bot trader earns $410k case study (finance.yahoo.com)'),
    
    ('<strong>4000 万美元套利 profit 池</strong> - 顶级套利者 - 入 20 万美元 + (zhuanlan.zhihu.com)',
     '<strong>$40M arbitrage profit pool</strong> - Top arbitrageur earns $200k+ (zhuanlan.zhihu.com)'),
    
    ('<strong>跨平台/Cross-market arbitrage 策略</strong>',
     '<strong>Cross-platform/Cross-market arbitrage strategy</strong>'),
    
    # Risk Warnings
    ('<strong>加州 DFAL 法规 2026-7-1 生效</strong>',
     '<strong>California DFPL regulations effective 2026-07-01</strong>'),
    
    ('<strong>超 19 个州对预测市场采取执法行动</strong>',
     '<strong>Over 19 states take enforcement action on prediction markets</strong>'),
    
    ('<strong>US 用户需完成 KYC，必须使用授权经纪商</strong>',
     '<strong>US users must complete KYC, use authorized brokers only</strong>'),
    
    # Market Data
    ('<li>Total arbitrage profits：约 4000 万美元</li>',
     '<li>Total arbitrage profits: ~$40 million</li>'),
    
    ('<li>Top arbitrage bots：-profit 超 40 万美元</li>',
     '<li>Top arbitrage bots: >$400k profit</li>'),
    
    # Strategy Key Points
    ('<li><strong>Cross-platform arbitrage</strong>：Polymarket ↔ Kalshi 同一 event 不同价格</li>',
     '<li><strong>Cross-platform arbitrage</strong>: Polymarket ↔ Kalshi same event, different prices</li>'),
    
    ('<li><strong>Cross-market arbitrage</strong>：同一 event 的多、空头寸组合</li>',
     '<li><strong>Cross-market arbitrage</strong>: Long/short position combinations on same event</li>'),
    
    ('<li><strong>15 分钟 Ultra short-term</strong>：High volatility, more opportunities, higher risk</li>',
     '<li><strong>15-minute ultra short-term</strong>: High volatility, more opportunities, higher risk</li>'),
    
    # Footer
    ('<p>🤖 由 Jarvis 自动 Generated | Powered by OpenClaw</p>',
     '<p>🤖 Auto-generated by Jarvis | Powered by OpenClaw</p>'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Fixed {FILE}")
