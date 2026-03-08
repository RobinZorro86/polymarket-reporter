#!/usr/bin/env python3
"""
Add timestamps and footer to all HTML files in the workspace.
"""

import os
import re
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/zqd/.openclaw/workspace/polymarket-reporter")

# Timestamp for all files (current time)
NOW = datetime.now()
CREATED = "2026-03-02T10:00:00+09:00"  # Original creation
UPDATED = NOW.strftime("%Y-%m-%dT%H:%M+09:00")

# Files with their source URLs and specific creation dates
FILE_METADATA = {
    "index.html": {"source": "https://pred101.com/", "created": "2026-02-27T10:00:00+09:00"},
    "about.html": {"source": "https://pred101.com/about", "created": "2026-02-27T10:00:00+09:00"},
    "search.html": {"source": "https://pred101.com/search", "created": "2026-02-27T10:00:00+09:00"},
    "reports/index.html": {"source": "https://pred101.com/reports", "created": "2026-02-27T10:00:00+09:00"},
    "reports/daily/daily-2026-02-27.html": {"source": "simmer API", "created": "2026-02-27T23:00:00+09:00"},
    "reports/daily/daily-2026-03-01.html": {"source": "simmer API", "created": "2026-03-01T23:00:00+09:00"},
    "reports/daily/daily-2026-03-05.html": {"source": "simmer API", "created": "2026-03-05T13:50:00+09:00"},
    "reports/weekly/weekly-2026-03-02.html": {"source": "weekly summary", "created": "2026-03-02T09:00:00+09:00"},
    "knowledge-base/index.html": {"source": "knowledge base", "created": "2026-02-27T10:00:00+09:00"},
    "knowledge-base/arbitrage-basics.html": {"source": "knowledge base", "created": "2026-02-27T10:00:00+09:00"},
    "knowledge-base/risk-management.html": {"source": "knowledge base", "created": "2026-02-27T10:00:00+09:00"},
    "knowledge-base/tools-resources.html": {"source": "knowledge base", "created": "2026-02-27T10:00:00+09:00"},
    "knowledge-base/kol-strategies.html": {"source": "knowledge base", "created": "2026-02-27T10:00:00+09:00"},
    "knowledge-base/aegis-system/index.html": {"source": "aegis system", "created": "2026-02-27T10:00:00+09:00"},
    "knowledge-base/aegis-system/architecture.html": {"source": "aegis system", "created": "2026-02-27T10:00:00+09:00"},
    "knowledge-base/aegis-system/milestones.html": {"source": "aegis system", "created": "2026-02-27T10:00:00+09:00"},
}

FOOTER_TEMPLATE = """
  <footer class="site-footer">
    <div class="container">
      <p>
        <span class="timestamp">
          <time datetime="{created}">创建: {created_date}</time> | 
          <time datetime="{updated}">更新: {updated_date}</time>
        </span>
        <span class="source">来源: <a href="{source}" target="_blank" rel="noopener">{source}</a></span>
      </p>
    </div>
  </footer>
"""

def process_file(filepath):
    """Add timestamp comment and footer to HTML file."""
    relative_path = str(filepath.relative_to(WORKSPACE))
    
    # Get metadata or use defaults
    meta = FILE_METADATA.get(relative_path, {})
    created = meta.get("created", CREATED)
    updated = UPDATED
    source = meta.get("source", "https://pred101.com/")
    
    created_date = created.split("T")[0]
    updated_date = updated.split("T")[0]
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ❌ Error reading {relative_path}: {e}")
        return False
    
    # Check if already has our timestamp comment
    timestamp_comment = f"<!-- TIMESTAMP: created={created} updated={updated} -->"
    if "<!-- TIMESTAMP:" in content:
        # Already has timestamp, update it
        content = re.sub(
            r'<!-- TIMESTAMP: created=\d{4}-\d{2}-\d{2}T[\d:+]+ updated=\d{4}-\d{2}-\d{2}T[\d:+]+ -->',
            timestamp_comment,
            content
        )
    else:
        # Add timestamp comment after <head>
        content = content.replace("<head>", f"<head>\n  {timestamp_comment}")
    
    # Check if already has our footer
    if '<footer class="site-footer">' not in content:
        # Add footer before </body>
        footer = FOOTER_TEMPLATE.format(
            created=created,
            updated=updated,
            created_date=created_date,
            updated_date=updated_date,
            source=source
        )
        content = content.replace("</body>", f"{footer}\n</body>")
    
    try:
        filepath.write_text(content, encoding='utf-8')
        print(f"  ✅ {relative_path}")
        return True
    except Exception as e:
        print(f"  ❌ Error writing {relative_path}: {e}")
        return False

def main():
    """Main entry point."""
    print(f"[Timestamp] Starting at {datetime.now().isoformat()}")
    
    # Find all HTML files
    html_files = list(WORKSPACE.glob("**/*.html"))
    print(f"[Timestamp] Found {len(html_files)} HTML files")
    
    success = 0
    for filepath in html_files:
        if process_file(filepath):
            success += 1
    
    print(f"[Timestamp] Complete: {success}/{len(html_files)} files processed")
    
    # Generate data.json index
    print("[Timestamp] Generating data.json index...")
    
    articles = []
    for filepath in html_files:
        rel_path = str(filepath.relative_to(WORKSPACE))
        meta = FILE_METADATA.get(rel_path, {})
        articles.append({
            "path": rel_path,
            "title": filepath.stem.replace("-", " ").title(),
            "created": meta.get("created", CREATED),
            "updated": UPDATED,
            "source": meta.get("source", "https://pred101.com/")
        })
    
    import json
    index_data = {
        "articles": articles,
        "lastUpdated": UPDATED,
        "total": len(articles)
    }
    
    index_path = WORKSPACE / "knowledge-base" / "data.json"
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    print(f"[Timestamp] Index generated: {index_path}")
    
    return 0

if __name__ == "__main__":
    exit(main())