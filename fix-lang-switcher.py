#!/usr/bin/env python3
"""
Fix language switcher links in EN knowledge-base and reports pages.
Problem: EN pages link to /zh/strategies/* but ZH pages are at /zh/knowledge-base/strategies/*
"""

import os
import re

BASE_DIR = "/home/zqd/.openclaw/workspace/polymarket-reporter"

# Patterns to fix in EN knowledge-base pages
FIXES = [
    # knowledge-base/strategies/* -> knowledge-base/strategies/*
    (r'href="/zh/strategies/copytrading/"', 'href="/zh/knowledge-base/strategies/copytrading/"'),
    (r'href="/zh/strategies/weather-trader/"', 'href="/zh/knowledge-base/strategies/weather-trader/"'),
    (r'href="/zh/strategies/signal-sniper/"', 'href="/zh/knowledge-base/strategies/signal-sniper/"'),
    (r'href="/zh/strategies/divergence/"', 'href="/zh/knowledge-base/strategies/divergence/"'),
    (r'href="/zh/strategies/fast-loop/"', 'href="/zh/knowledge-base/strategies/fast-loop/"'),
    (r'href="/zh/strategies/mert-sniper/"', 'href="/zh/knowledge-base/strategies/mert-sniper/"'),
    (r'href="/zh/strategies/"', 'href="/zh/knowledge-base/strategies/"'),
    
    # knowledge-base/tutorials/* -> knowledge-base/tutorials/*
    (r'href="/zh/tutorials/openclaw-setup/"', 'href="/zh/knowledge-base/tutorials/openclaw-setup/"'),
    (r'href="/zh/tutorials/polymarket-basics/"', 'href="/zh/knowledge-base/tutorials/polymarket-basics/"'),
    (r'href="/zh/tutorials/simmer-guide/"', 'href="/zh/knowledge-base/tutorials/simmer-guide/"'),
    (r'href="/zh/tutorials/wallet-setup/"', 'href="/zh/knowledge-base/tutorials/wallet-setup/"'),
    (r'href="/zh/tutorials/"', 'href="/zh/knowledge-base/tutorials/"'),
    
    # knowledge-base/resources/* -> knowledge-base/resources/*
    (r'href="/zh/resources/"', 'href="/zh/knowledge-base/resources/"'),
    
    # reports/* -> reports/*
    (r'href="/zh/reports/"', 'href="/zh/reports/"'),
    (r'href="/zh/reports/daily/"', 'href="/zh/reports/daily/"'),
    (r'href="/zh/reports/weekly/"', 'href="/zh/reports/weekly/"'),
    (r'href="/zh/reports/simmer/"', 'href="/zh/reports/simmer/"'),
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
    
    # Fix EN knowledge-base pages
    for root, dirs, files in os.walk(os.path.join(BASE_DIR, 'en', 'knowledge-base')):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if fix_file(filepath):
                    print(f"Fixed: {filepath}")
                    fixed_count += 1
    
    # Fix EN reports pages
    for root, dirs, files in os.walk(os.path.join(BASE_DIR, 'en', 'reports')):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if fix_file(filepath):
                    print(f"Fixed: {filepath}")
                    fixed_count += 1
    
    print(f"\nTotal files fixed: {fixed_count}")

if __name__ == "__main__":
    main()
