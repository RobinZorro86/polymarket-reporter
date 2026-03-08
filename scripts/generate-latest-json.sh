#!/bin/bash
# Generate latest.json for homepage dynamic content
# Run after daily report generation

set -e

WORKSPACE=/home/zqd/.openclaw/workspace/polymarket-reporter
DATE=$(date +%Y-%m-%d)
DATE_NUM=$(date +%Y%m%d)

echo "🔄 Generating latest.json for homepage..."

# Find latest daily report
LATEST_DAILY=$(ls -t $WORKSPACE/reports/daily/daily-*.html 2>/dev/null | head -1)
LATEST_DAILY_DATE=$(basename $LATEST_DAILY | sed 's/daily-//' | sed 's/.html//')

# Find latest weekly report
LATEST_WEEKLY=$(ls -t $WORKSPACE/reports/weekly/weekly-*.html 2>/dev/null | head -1)
LATEST_WEEKLY_DATE=$(basename $LATEST_WEEKLY | sed 's/weekly-//' | sed 's/.html//')

# Find latest KOL ranking (prefer public ranking file)
LATEST_KOL=$(ls -t $WORKSPACE/knowledge-base/kol/rankings/KOL-RANKING-*.md 2>/dev/null | head -1)
if [ -z "$LATEST_KOL" ]; then
  LATEST_KOL=$(ls -t $WORKSPACE/knowledge-base/kol/rankings/KOL-*.md 2>/dev/null | head -1)
fi
LATEST_KOL_DATE=$(basename "$LATEST_KOL" | sed 's/KOL-RANKING-//' | sed 's/KOL-//' | sed 's/.md//')

# Generate latest.json
cat > $WORKSPACE/data/latest.json << EOF
{
  "generated_at": "$DATE",
  "daily_report": {
    "date": "$LATEST_DAILY_DATE",
    "url": "/reports/daily/daily-$LATEST_DAILY_DATE.html",
    "title": "Polymarket 每日报告 - $LATEST_DAILY_DATE"
  },
  "weekly_report": {
    "date": "$LATEST_WEEKLY_DATE",
    "url": "/reports/weekly/weekly-$LATEST_WEEKLY_DATE.html",
    "title": "Polymarket 周报 - $LATEST_WEEKLY_DATE"
  },
  "kol_ranking": {
    "date": "$LATEST_KOL_DATE",
    "url": "/knowledge-base/kol/rankings/KOL-RANKING-$LATEST_KOL_DATE.md",
    "title": "KOL 综合评估排名 - $LATEST_KOL_DATE"
  },
  "stats": {
    "total_reports": $(ls $WORKSPACE/reports/daily/*.html 2>/dev/null | wc -l),
    "total_kols": 11,
    "total_strategies": 6
  }
}
EOF

echo "✅ latest.json generated: $WORKSPACE/data/latest.json"
