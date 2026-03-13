#!/bin/bash
# Fix English pages linking to old Chinese /zh/knowledge-base/* paths
# Replace with new /zh/* structure

cd /home/zqd/.openclaw/workspace/polymarket-reporter

# Fix en/strategies/index.html
sed -i 's|/zh/knowledge-base/strategies/signal-sniper/|/zh/strategies/signal-sniper/|g' en/strategies/index.html
sed -i 's|/zh/knowledge-base/strategies/weather-trader/|/zh/strategies/weather-trader/|g' en/strategies/index.html
sed -i 's|/zh/knowledge-base/strategies/fast-loop/|/zh/strategies/fast-loop/|g' en/strategies/index.html
sed -i 's|/zh/knowledge-base/strategies/divergence/|/zh/strategies/divergence/|g' en/strategies/index.html

# Fix en/kol/index.html
sed -i 's|/zh/knowledge-base/kol/rankings/|/zh/kol/rankings/|g' en/kol/index.html
sed -i 's|/zh/knowledge-base/kol/vladic_eth/|/zh/kol/vladic_eth/|g' en/kol/index.html
sed -i 's|/zh/knowledge-base/kol/noisyb0y1/|/zh/kol/noisyb0y1/|g' en/kol/index.html

# Fix en/resources/index.html
sed -i 's|/zh/knowledge-base/resources/|/zh/resources/|g' en/resources/index.html

# Fix en/about.html
sed -i 's|/zh/about.html|/zh/about.html|g' en/about.html  # Already correct

# Fix en/knowledge-base/index.html - multiple references
sed -i 's|/zh/knowledge-base/tutorials/polymarket-basics/|/zh/tutorials/polymarket-basics/|g' en/knowledge-base/index.html
sed -i 's|/zh/knowledge-base/tutorials/wallet-setup/|/zh/tutorials/wallet-setup/|g' en/knowledge-base/index.html
sed -i 's|/zh/knowledge-base/resources/risk-management/|/zh/resources/risk-management/|g' en/knowledge-base/index.html
sed -i 's|/zh/knowledge-base/strategies/|/zh/strategies/|g' en/knowledge-base/index.html
sed -i 's|/zh/knowledge-base/kol/|/zh/kol/|g' en/knowledge-base/index.html
sed -i 's|/zh/knowledge-base/tutorials/|/zh/tutorials/|g' en/knowledge-base/index.html
sed -i 's|/zh/knowledge-base/resources/|/zh/resources/|g' en/knowledge-base/index.html

# Fix en/knowledge-base/strategies/*.html
for f in en/knowledge-base/strategies/*/index.html; do
  sed -i 's|/zh/knowledge-base/strategies/|/zh/strategies/|g' "$f"
  sed -i 's|/zh/knowledge-base/kol/|/zh/kol/|g' "$f"
  sed -i 's|/zh/knowledge-base/resources/|/zh/resources/|g' "$f"
  sed -i 's|/zh/knowledge-base/tutorials/|/zh/tutorials/|g' "$f"
done

# Fix en/knowledge-base/tutorials/*.html
for f in en/knowledge-base/tutorials/*/index.html; do
  sed -i 's|/zh/knowledge-base/tutorials/|/zh/tutorials/|g' "$f"
  sed -i 's|/zh/knowledge-base/resources/|/zh/resources/|g' "$f"
  sed -i 's|/zh/knowledge-base/strategies/|/zh/strategies/|g' "$f"
done

# Fix en/knowledge-base/resources/*.html
for f in en/knowledge-base/resources/*/index.html; do
  sed -i 's|/zh/knowledge-base/resources/|/zh/resources/|g' "$f"
  sed -i 's|/zh/knowledge-base/tutorials/|/zh/tutorials/|g' "$f"
done

# Fix en/reports/*.html
for f in en/reports/**/*.html; do
  sed -i 's|/zh/knowledge-base/|/zh/|g' "$f"
done

echo "Link fix complete"
