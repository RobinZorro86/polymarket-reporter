#!/usr/bin/env python3
"""
Automated Daily Report Generator
Reads data/polymarket/markets-latest.json and generates HTML report in reports/daily/
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from html import escape

# Configuration - relative paths from workspace root
SCRIPT_DIR = Path(__file__).parent
WORKSPACE_DIR = SCRIPT_DIR.parent
DATA_DIR = WORKSPACE_DIR / "data" / "polymarket"
REPORTS_DIR = WORKSPACE_DIR / "reports" / "daily"
SCHEMA_DIR = WORKSPACE_DIR / "schemas"


def load_data():
    """Load markets data from JSON file."""
    data_file = DATA_DIR / "markets-latest.json"
    if not data_file.exists():
        raise FileNotFoundError(f"Data file not found: {data_file}")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_category_from_tags(tags):
    """Determine category from market tags."""
    if not tags:
        return "Other"
    
    tags_str = ' '.join(tags).lower()
    
    if 'crypto' in tags_str or 'bitcoin' in tags_str or 'ethereum' in tags_str:
        return "Crypto"
    elif 'sports' in tags_str or 'ufc' in tags_str or 'nba' in tags_str or 'nhl' in tags_str:
        return "Sports"
    elif 'politics' in tags_str or 'election' in tags_str:
        return "Politics"
    elif 'weather' in tags_str:
        return "Weather"
    elif 'tech' in tags_str:
        return "Tech"
    else:
        return "Other"


def analyze_markets(data):
    """Analyze markets data and return statistics."""
    markets = data.get('markets', [])
    
    # Top 10 by probability (or volume if available)
    sorted_markets = sorted(
        markets, 
        key=lambda x: x.get('probability', 0.5), 
        reverse=True
    )
    top_10 = sorted_markets[:10]
    
    # Category stats
    categories = {}
    for market in markets:
        cat = get_category_from_tags(market.get('tags', []))
        categories[cat] = categories.get(cat, 0) + 1
    
    return {
        'total_markets': len(markets),
        'top_10': top_10,
        'categories': categories,
        'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
        'timestamp': data.get('timestamp', datetime.now().isoformat())
    }


def generate_html(stats):
    """Generate HTML report."""
    date_str = stats['date']
    date_display = datetime.strptime(date_str, '%Y-%m-%d').strftime('%B %d, %Y')
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Markets Report - {escape(date_display)}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e4e4e7;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 40px;
        }}
        h1 {{ 
            font-size: 2.5rem;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        .subtitle {{ color: #71717a; font-size: 1rem; }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .stat-value {{ font-size: 2rem; font-weight: bold; color: #00d4ff; }}
        .stat-label {{ color: #71717a; font-size: 0.875rem; margin-top: 5px; }}
        h2 {{ 
            font-size: 1.5rem;
            margin-bottom: 20px;
            color: #e4e4e7;
            border-left: 4px solid #00d4ff;
            padding-left: 15px;
        }}
        .market-table {{
            width: 100%;
            border-collapse: collapse;
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 40px;
        }}
        .market-table th {{
            background: rgba(0,212,255,0.1);
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #00d4ff;
        }}
        .market-table td {{
            padding: 15px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        .market-table tr:hover {{ background: rgba(255,255,255,0.03); }}
        .probability {{ 
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
        }}
        .prob-high {{ background: rgba(34,197,94,0.2); color: #22c55e; }}
        .prob-mid {{ background: rgba(234,179,8,0.2); color: #eab308; }}
        .prob-low {{ background: rgba(239,68,68,0.2); color: #ef4444; }}
        .category-tag {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            background: rgba(255,255,255,0.1);
        }}
        .categories {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 40px; }}
        .category {{
            background: rgba(255,255,255,0.05);
            padding: 15px 25px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .category-count {{ font-size: 1.5rem; font-weight: bold; color: #00d4ff; }}
        .category-name {{ color: #71717a; font-size: 0.875rem; }}
        footer {{
            text-align: center;
            padding: 20px;
            color: #52525b;
            font-size: 0.875rem;
            border-top: 1px solid rgba(255,255,255,0.1);
            margin-top: 40px;
        }}
        @media (max-width: 768px) {{
            h1 {{ font-size: 1.75rem; }}
            .stats-grid {{ grid-template-columns: 1fr; }}
            .market-table {{ font-size: 0.875rem; }}
            .market-table th, .market-table td {{ padding: 10px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Daily Markets Report</h1>
            <p class="subtitle">{escape(date_display)} • Generated {datetime.now().strftime('%H:%M %Z')}</p>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{stats['total_markets']}</div>
                <div class="stat-label">Total Markets Tracked</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(stats['top_10'])}</div>
                <div class="stat-label">Top Opportunities</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(stats['categories'])}</div>
                <div class="stat-label">Categories</div>
            </div>
        </div>
        
        <h2>📈 Top 10 Opportunities</h2>
        <table class="market-table">
            <thead>
                <tr>
                    <th>Market</th>
                    <th>Probability</th>
                    <th>Category</th>
                    <th>Resolve</th>
                </tr>
            </thead>
            <tbody>
"""

    for i, market in enumerate(stats['top_10']):
        prob = market.get('probability', 0)
        prob_pct = f"{prob * 100:.1f}%"
        
        # Color coding
        if prob >= 0.7:
            prob_class = "prob-high"
        elif prob >= 0.4:
            prob_class = "prob-mid"
        else:
            prob_class = "prob-low"
        
        category = get_category_from_tags(market.get('tags', []))
        resolve_at = market.get('resolves_at', 'N/A')
        if resolve_at != 'N/A':
            try:
                resolve_date = datetime.fromisoformat(resolve_at.replace('Z', '+00:00'))
                resolve_display = resolve_date.strftime('%m/%d %H:%M')
            except:
                resolve_display = resolve_at[:10]
        else:
            resolve_display = 'N/A'
        
        question = escape(market.get('question', 'Unknown')[:60])
        if len(market.get('question', '')) > 60:
            question += '...'
        
        html += f"""
                <tr>
                    <td>{question}</td>
                    <td><span class="probability {prob_class}">{prob_pct}</span></td>
                    <td><span class="category-tag">{escape(category)}</span></td>
                    <td>{escape(resolve_display)}</td>
                </tr>
"""

    html += f"""
            </tbody>
        </table>
        
        <h2>🏷️ Categories</h2>
        <div class="categories">
"""

    for cat, count in sorted(stats['categories'].items(), key=lambda x: -x[1]):
        html += f"""
            <div class="category">
                <div class="category-count">{count}</div>
                <div class="category-name">{escape(cat)}</div>
            </div>
"""

    html += f"""
        </div>
        
        <footer>
            <p>Data Source: Polymarket API • Generated by Aegis V2</p>
            <p>Report generated at {datetime.now().isoformat()}</p>
        </footer>
    </div>
</body>
</html>
"""
    return html


def main():
    """Main entry point."""
    print(f"[Daily Report] Starting at {datetime.now().isoformat()}")
    
    # Load data
    try:
        data = load_data()
        print(f"[Daily Report] Loaded {len(data.get('markets', []))} markets")
    except Exception as e:
        print(f"[Daily Report] Error loading data: {e}")
        sys.exit(1)
    
    # Analyze
    stats = analyze_markets(data)
    print(f"[Daily Report] Analyzed {stats['total_markets']} markets")
    
    # Generate HTML
    html = generate_html(stats)
    
    # Save report
    date_str = stats['date']
    output_file = REPORTS_DIR / f"daily-{date_str}.html"
    
    # Ensure directory exists
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[Daily Report] Generated: {output_file}")
    print(f"[Daily Report] Complete!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())