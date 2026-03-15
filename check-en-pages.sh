#!/bin/bash
# Check all EN pages for Chinese content leakage

cd /home/zqd/.openclaw/workspace/polymarket-reporter

echo "=== Checking EN pages for Chinese content ==="
echo ""

# Find all EN HTML files
find ./en -name "*.html" | while read file; do
  # Check for Chinese characters (excluding hreflang and href references to /zh/)
  chinese_content=$(grep -P "[\x{4e00}-\x{9fff}]" "$file" 2>/dev/null | grep -v "hreflang=\"zh\"" | grep -v "href=\"/zh/" | grep -v "Chinese main site" | grep -v "Chinese deep content" | head -3)
  
  if [ -n "$chinese_content" ]; then
    echo "⚠️  CHINESE FOUND: $file"
    echo "$chinese_content" | head -3
    echo "---"
  fi
done

echo ""
echo "=== Checking EN pages for proper canonical/hreflang ==="
echo ""

find ./en -name "*.html" | while read file; do
  has_canonical=$(grep -c 'rel="canonical"' "$file" 2>/dev/null)
  has_hreflang_en=$(grep -c 'hreflang="en"' "$file" 2>/dev/null)
  has_hreflang_zh=$(grep -c 'hreflang="zh"' "$file" 2>/dev/null)
  
  if [ "$has_canonical" -eq 0 ] || [ "$has_hreflang_en" -eq 0 ] || [ "$has_hreflang_zh" -eq 0 ]; then
    echo "⚠️  MISSING TAGS: $file"
    echo "   canonical: $has_canonical | hreflang=en: $has_hreflang_en | hreflang=zh: $has_hreflang_zh"
  fi
done

echo ""
echo "=== Check complete ==="
