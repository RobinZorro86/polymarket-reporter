#!/usr/bin/env python3
"""
Fix hreflang tags in EN knowledge-base pages to match Plan B structure.
Problem: hreflang points to /zh/strategies/* but should point to /zh/knowledge-base/strategies/*
"""

import os
import re

BASE_DIR = "/home/zqd/.openclaw/workspace/polymarket-reporter"

# Patterns to fix hreflang in EN knowledge-base pages
FIXES = [
    # knowledge-base/strategies/*
    (r'hreflang="zh" href="https://www.pred101.com/zh/strategies/copytrading/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/strategies/copytrading/"'),
    (r'hreflang="zh" href="https://www.pred101.com/zh/strategies/weather-trader/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/strategies/weather-trader/"'),
    (r'hreflang="zh" href="https://www.pred101.com/zh/strategies/signal-sniper/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/strategies/signal-sniper/"'),
    (r'hreflang="zh" href="https://www.pred101.com/zh/strategies/divergence/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/strategies/divergence/"'),
    (r'hreflang="zh" href="https://www.pred101.com/zh/strategies/fast-loop/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/strategies/fast-loop/"'),
    (r'hreflang="zh" href="https://www.pred101.com/zh/strategies/mert-sniper/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/strategies/mert-sniper/"'),
    (r'hreflang="zh" href="https://www.pred101.com/zh/strategies/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/strategies/"'),
    
    # knowledge-base/tutorials/*
    (r'hreflang="zh" href="https://www.pred101.com/zh/tutorials/openclaw-setup/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/tutorials/openclaw-setup/"'),
    (r'hreflang="zh" href="https://www.pred101.com/zh/tutorials/polymarket-basics/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/tutorials/polymarket-basics/"'),
    (r'hreflang="zh" href="https://www.pred101.com/zh/tutorials/simmer-guide/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/tutorials/simmer-guide/"'),
    (r'hreflang="zh" href="https://www.pred101.com/zh/tutorials/wallet-setup/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/tutorials/wallet-setup/"'),
    (r'hreflang="zh" href="https://www.pred101.com/zh/tutorials/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/tutorials/"'),
    
    # knowledge-base/resources/*
    (r'hreflang="zh" href="https://www.pred101.com/zh/resources/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/resources/"'),
    (r'hreflang="zh" href="https://www.pred101.com/zh/resources/glossary/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/resources/glossary/"'),
    (r'hreflang="zh" href="https://www.pred101.com/zh/resources/risk-management/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/resources/risk-management/"'),
    
    # knowledge-base/kol/*
    (r'hreflang="zh" href="https://www.pred101.com/zh/kol/"', 
     'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/kol/"'),
]

def fix_file(filepath):
    """Apply fixes to a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for pattern, replacement in FIXES:
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    fixed_count = 0
    scanned_count = 0
    
    # Fix EN knowledge-base pages
    kb_dir = os.path.join(BASE_DIR, 'en', 'knowledge-base')
    for root, dirs, files in os.walk(kb_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                scanned_count += 1
                if fix_file(filepath):
                    print(f"Fixed: {filepath}")
                    fixed_count += 1
    
    print(f"\nScanned: {scanned_count} files")
    print(f"Fixed: {fixed_count} files")

if __name__ == "__main__":
    main()
