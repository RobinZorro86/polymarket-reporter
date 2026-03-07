#!/bin/bash
# X Timeline Fetcher - 自动获取指定账号推文并汇总
# Usage: ./fetch-x-timeline.sh @username [count]

set -e

# 认证配置
AUTH_TOKEN="0843fc6fc493787abf6eaa7ae6599cc9273db347"
CT0="aa63a3556bbb75ea9bc33cea142ff959626d7d20298b3752205e071a8cd9ed60b737318161b05d821e2e09bcbfea30a8fb2aa9b8d5b867522a3e80a23d4da72ed0892f6072712ae7da29580404fc57a0"

USERNAME=${1:-@vladic_eth}
COUNT=${2:-20}
OUTPUT_DIR=$HOME/x-summaries
DATE=$(date +%Y%m%d)

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

RAW_FILE="$OUTPUT_DIR/raw-${USERNAME#@}-$DATE.json"
SUMMARY_FILE="$OUTPUT_DIR/summary-${USERNAME#@}-$DATE.txt"

echo "📊 获取 $USERNAME 最近 $COUNT 条推文..."

# 获取推文
xreach --auth-token "$AUTH_TOKEN" --ct0 "$CT0" tweets "$USERNAME" --json -n "$COUNT" > "$RAW_FILE"

echo "✅ 原始数据已保存：$RAW_FILE"
echo ""
echo "📌 最近推文预览："
echo "========================================"

# 用 Python 解析 JSON（替代 jq）
python3 << EOF
import json

with open("$RAW_FILE", 'r') as f:
    data = json.load(f)

for i, tweet in enumerate(data.get('items', [])[:5], 1):
    created = tweet.get('createdAt', 'N/A')[:16]
    text = tweet.get('text', '').replace('\n', ' ')[:150]
    likes = tweet.get('likeCount', 0)
    print(f"{i}. [{created}] {text}... (❤️ {likes})")

print("========================================")
print(f"完整摘要已保存：$SUMMARY_FILE")
EOF

# 生成完整摘要文件
python3 -c "
import json

with open('$RAW_FILE', 'r') as f:
    data = json.load(f)

with open('$SUMMARY_FILE', 'w', encoding='utf-8') as f:
    f.write(f'# $USERNAME 推文摘要\n')
    f.write(f'获取时间：$(date '+%Y-%m-%d %H:%M:%S')\n')
    f.write(f'推文数量：{len(data.get(\"items\", []))}\n\n')
    f.write('=' * 60 + '\n\n')
    
    for tweet in data.get('items', []):
        created = tweet.get('createdAt', 'N/A')
        text = tweet.get('text', '')
        likes = tweet.get('likeCount', 0)
        retweets = tweet.get('retweetCount', 0)
        
        f.write(f'📅 {created}\n')
        f.write(f'📝 {text}\n')
        f.write(f'❤️ {likes} | 🔄 {retweets}\n')
        f.write('-' * 60 + '\n\n')
"

echo "✅ 完成！"
