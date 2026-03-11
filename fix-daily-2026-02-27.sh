#!/bin/bash
# Fix Chinese remnants in en/reports/daily/daily-2026-02-27.html

FILE="en/reports/daily/daily-2026-02-27.html"

cd /home/zqd/.openclaw/workspace/polymarket-reporter

# Backup
cp "$FILE" "$FILE.backup"

# Fix title
sed -i 's|<title>Prediction Market 101Report (2026-2-27) | Prediction Market 101</title>|<title>Polymarket Daily Report · 2026-02-27 | pred101</title>|g' "$FILE"

# Fix meta description (Chinese → English)
sed -i 's|<meta name="description" content="Polymarket 预测市场信息聚合 Report，涵盖 Latest News、行业研 Report、Social Media Buzz、Arbitrage Strategies、Risk Warnings 等。">|<meta name="description" content="Polymarket prediction market intelligence report covering latest news, industry research, social media buzz, arbitrage strategies, and risk warnings.">|g' "$FILE"

# Fix meta keywords
sed -i 's|<meta name="keywords" content="Polymarket, 预测市场，套利，加密货币，交易策略">|<meta name="keywords" content="Polymarket, prediction market, arbitrage, cryptocurrency, trading strategy">|g' "$FILE"

# Fix og:description
sed -i 's|<meta property="og:description" content="Polymarket 预测市场信息聚合 Report，涵盖 Latest News、套利策略、Risk Warnings 等。">|<meta property="og:description" content="Polymarket prediction market report covering latest news, arbitrage strategies, and risk warnings.">|g' "$FILE"

# Fix schema.org description
sed -i 's|"description": "Polymarket 预测市场信息聚合 Report，涵盖 Latest News、套利策略、Risk Warnings 等"|"description": "Polymarket prediction market report covering latest news, arbitrage strategies, and risk warnings"|g' "$FILE"

# Fix Chinese in content - research section
sed -i 's|<strong>预测市场爆发式增长 2025</strong>|<strong>Prediction market explosive growth in 2025</strong>|g' "$FILE"

# Fix Chinese in arbitrage section
sed -i 's|<strong>Bot arbitrage dominates market</strong> - 机器人 - 赚 41 万美元案例|<strong>Bot arbitrage dominates market</strong> - Bot trader earns $410k case study|g' "$FILE"
sed -i 's|<strong>4000 万美元套利 profit 池</strong> - 顶级套利者 - 入 20 万美元 +|<strong>$40M arbitrage profit pool</strong> - Top arbitrageur earns $200k+|g' "$FILE"

echo "✅ Fixed daily-2026-02-27.html"
