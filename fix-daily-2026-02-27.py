#!/usr/bin/env python3
"""Fix Chinese remnants in en/reports/daily/daily-2026-02-27.html"""

import re

FILE = "en/reports/daily/daily-2026-02-27.html"

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open(FILE + ".backup2", 'w', encoding='utf-8') as f:
    f.write(content)

# Fix title
content = content.replace(
    '<title>Prediction Market 101Report (2026-2-27) | Prediction Market 101</title>',
    '<title>Polymarket Daily Report · 2026-02-27 | pred101</title>'
)

# Fix meta description
content = content.replace(
    '<meta name="description" content="Polymarket 预测市场信息聚合 Report，涵盖 Latest News、行业研 Report、Social Media Buzz、Arbitrage Strategies、Risk Warnings 等。">',
    '<meta name="description" content="Polymarket prediction market intelligence report covering latest news, industry research, social media buzz, arbitrage strategies, and risk warnings.">'
)

# Fix meta keywords
content = content.replace(
    '<meta name="keywords" content="Polymarket, 预测市场，套利，加密货币，交易策略">',
    '<meta name="keywords" content="Polymarket, prediction market, arbitrage, cryptocurrency, trading strategy">'
)

# Fix og:description
content = content.replace(
    '<meta property="og:description" content="Polymarket 预测市场信息聚合 Report，涵盖 Latest News、套利策略、Risk Warnings 等。">',
    '<meta property="og:description" content="Polymarket prediction market report covering latest news, arbitrage strategies, and risk warnings.">'
)

# Fix schema.org description (multiple occurrences)
content = content.replace(
    '"description": "Polymarket 预测市场信息聚合 Report，涵盖 Latest News、套利策略、Risk Warnings 等"',
    '"description": "Polymarket prediction market report covering latest news, arbitrage strategies, and risk warnings"'
)

# Fix Chinese in research section
content = content.replace(
    '<strong>预测市场爆发式增长 2025</strong>',
    '<strong>Prediction market explosive growth in 2025</strong>'
)

# Fix Chinese in arbitrage section
content = content.replace(
    '<strong>Bot arbitrage dominates market</strong> - 机器人 - 赚 41 万美元案例 (finance.yahoo.com)',
    '<strong>Bot arbitrage dominates market</strong> - Bot trader earns $410k case study (finance.yahoo.com)'
)
content = content.replace(
    '<strong>4000 万美元套利 profit 池</strong> - 顶级套利者 - 入 20 万美元 + (zhuanlan.zhihu.com)',
    '<strong>$40M arbitrage profit pool</strong> - Top arbitrageur earns $200k+ (zhuanlan.zhihu.com)'
)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Fixed {FILE}")
