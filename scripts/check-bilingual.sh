#!/bin/bash
# Bilingual site structure checker for pred101
# Checks: Chinese residue in /en/, English pollution in /zh/, path consistency

BASE="/home/zqd/.openclaw/workspace/polymarket-reporter"

echo "=== pred101 Bilingual Structure Check ==="
echo "Date: $(date -Iseconds)"
echo ""

# 1. Check for Chinese characters in /en/ files
echo "1. Checking for Chinese residue in /en/..."
EN_CHINESE=$(find "$BASE/en" -name "*.html" -exec python3 -c "
import re, sys
with open(sys.argv[1], 'r') as f:
    content = f.read()
    chinese = re.findall(r'[\u4e00-\u9fff]', content)
    if chinese:
        print(sys.argv[1])
" {} \; 2>/dev/null)

if [ -z "$EN_CHINESE" ]; then
    echo "   ✅ No Chinese characters found in /en/ files"
else
    echo "   ⚠️  Chinese found in:"
    echo "$EN_CHINESE" | sed 's/^/      /'
fi
echo ""

# 2. Check /zh/ files have proper lang="zh"
echo "2. Checking /zh/ files have lang=\"zh\"..."
ZH_LANG_ERROR=$(find "$BASE/zh" -name "*.html" -exec grep -L 'lang="zh"' {} \; 2>/dev/null | head -10)
if [ -z "$ZH_LANG_ERROR" ]; then
    echo "   ✅ All /zh/ files have lang=\"zh\""
else
    echo "   ⚠️  Missing lang=\"zh\" in:"
    echo "$ZH_LANG_ERROR" | sed 's/^/      /'
fi
echo ""

# 3. Check /en/ files have proper lang="en"
echo "3. Checking /en/ files have lang=\"en\"..."
EN_LANG_ERROR=$(find "$BASE/en" -name "*.html" -exec grep -L 'lang="en"' {} \; 2>/dev/null | head -10)
if [ -z "$EN_LANG_ERROR" ]; then
    echo "   ✅ All /en/ files have lang=\"en\""
else
    echo "   ⚠️  Missing lang=\"en\" in:"
    echo "$EN_LANG_ERROR" | sed 's/^/      /'
fi
echo ""

# 4. Check for hreflang tags in /en/ files
echo "4. Checking hreflang tags in /en/ files..."
EN_HREFLANG=$(find "$BASE/en" -name "*.html" -exec grep -L 'hreflang=' {} \; 2>/dev/null | head -10)
if [ -z "$EN_HREFLANG" ]; then
    echo "   ✅ All /en/ files have hreflang tags"
else
    echo "   ⚠️  Missing hreflang in:"
    echo "$EN_HREFLANG" | sed 's/^/      /'
fi
echo ""

# 5. Check for hreflang tags in /zh/ files
echo "5. Checking hreflang tags in /zh/ files..."
ZH_HREFLANG=$(find "$BASE/zh" -name "*.html" -exec grep -L 'hreflang=' {} \; 2>/dev/null | head -10)
if [ -z "$ZH_HREFLANG" ]; then
    echo "   ✅ All /zh/ files have hreflang tags"
else
    echo "   ⚠️  Missing hreflang in:"
    echo "$ZH_HREFLANG" | sed 's/^/      /'
fi
echo ""

# 6. Check old paths are empty or have redirects
echo "6. Checking old root paths..."
for dir in knowledge-base reports strategies kol resources learn; do
    COUNT=$(find "$BASE/$dir" -name "*.html" 2>/dev/null | wc -l)
    if [ "$COUNT" -eq 0 ]; then
        echo "   ⚠️  /$dir/ is empty (no redirect page)"
    else
        echo "   ✅ /$dir/ has $COUNT file(s)"
    fi
done
echo ""

# 7. Count files
echo "7. File counts..."
EN_COUNT=$(find "$BASE/en" -name "*.html" | wc -l)
ZH_COUNT=$(find "$BASE/zh" -name "*.html" | wc -l)
echo "   /en/: $EN_COUNT files"
echo "   /zh/: $ZH_COUNT files"
echo ""

echo "=== Check Complete ==="
