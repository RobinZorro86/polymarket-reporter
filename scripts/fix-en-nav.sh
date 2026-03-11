#!/bin/bash
# Fix English pages navigation - replace /zh/ references in logo and About links with /en/

cd /home/zqd/.openclaw/workspace/polymarket-reporter

# Fix divergence strategy page (About link only)
sed -i 's|<a href="/zh/about.html">About</a>|<a href="/en/about.html">About</a>|g' en/knowledge-base/strategies/divergence/index.html

# Fix KOL pages (logo + About link)
for page in en/knowledge-base/kol/runes-leo/index.html \
            en/knowledge-base/kol/edwordkaru/index.html \
            en/knowledge-base/kol/dmitriyungarov/index.html \
            en/knowledge-base/kol/cutnpaste4/index.html \
            en/knowledge-base/kol/aleiahlock/index.html; do
    sed -i 's|<a href="/zh/" class="logo"|<a href="/en/" class="logo"|g' "$page"
    sed -i 's|<a href="/zh/about.html">关于</a>|<a href="/en/about.html">About</a>|g' "$page"
done

# Fix tutorial pages (logo + About link)
for page in en/knowledge-base/tutorials/polymarket-basics/index.html \
            en/knowledge-base/tutorials/wallet-setup/index.html \
            en/knowledge-base/tutorials/simmer-guide/index.html \
            en/knowledge-base/tutorials/openclaw-setup/index.html; do
    sed -i 's|<a href="/zh/" class="logo"|<a href="/en/" class="logo"|g' "$page"
    sed -i 's|<a href="/zh/about.html">关于</a>|<a href="/en/about.html">About</a>|g' "$page"
done

echo "Navigation fixes applied to English pages"
