#!/bin/bash
# Knowledge Base Completeness Checker

echo "=== Knowledge Base Completeness Check ==="
echo ""

# Check KOL pages
echo "📌 KOL Pages:"
for dir in kol/*/; do
    if [ -f "${dir}index.html" ]; then
        echo "  ✅ $(basename $dir)"
    else
        echo "  ❌ $(basename $dir) - Missing index.html"
    fi
done

echo ""
echo "📌 Strategy Pages:"
for dir in strategies/*/; do
    if [ -f "${dir}index.html" ]; then
        echo "  ✅ $(basename $dir)"
    else
        echo "  ❌ $(basename $dir) - Missing index.html"
    fi
done

echo ""
echo "📌 Tutorial Pages:"
for dir in tutorials/*/; do
    if [ -f "${dir}index.html" ]; then
        echo "  ✅ $(basename $dir)"
    else
        echo "  ❌ $(basename $dir) - Missing index.html"
    fi
done

echo ""
echo "📌 Resource Pages:"
for dir in resources/*/; do
    if [ -f "${dir}index.html" ]; then
        echo "  ✅ $(basename $dir)"
    else
        echo "  ❌ $(basename $dir) - Missing index.html"
    fi
done
