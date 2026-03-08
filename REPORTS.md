# 📊 Polymarket 报告系统

## 概述

自动化生成 Polymarket 每日/每周报告，整合全网数据源和 X 热点。

---

## 📅 更新频率

| 类型 | 频率 | 时间 | 自动推送 |
|------|------|------|---------|
| **日报** | 隔天 | 9:00 AM | ✅ 自动生成并推送 |
| **周报** | 每周 | 周一 9:00 AM | ✅ 自动生成并推送 |
| **知识库** | 每周 | 周日 20:00 | ✅ 批量收集并推送 |
| **健康检查** | 每周 | 周一 9:00 AM | ✅ 仅生成报告 |

---

## 🔧 自动化脚本

### 日报生成
```bash
bash scripts/generate-daily-report.sh
```

**功能**:
- ✅ 抓取 Polymarket 官方 X 账号
- ✅ 抓取 KOL (@mert_mert 等) 动态
- ✅ 搜索 Google News 全网新闻
- ✅ 生成 Markdown 草稿
- ✅ 输出 X 热点预览

**输出**:
- `reports/daily/daily-YYYYMMDD.md` - Markdown 草稿
- `~/x-summaries/` - X 原始数据

---

### 周报生成
```bash
bash scripts/generate-weekly-report.sh
```

**功能**:
- ✅ 抓取多位 KOL 周度动态
- ✅ 汇总周度市场数据
- ✅ 鲸鱼追踪与 PnL 排行
- ✅ 策略复盘与经验教训
- ✅ 下周重大事件预告

**输出**:
- `reports/weekly/weekly-YYYYMMDD.md` - Markdown 草稿

---

## 📝 报告模板

### 日报结构
1. **核心摘要** - 总交易量、活跃市场数
2. **今日热点 TOP 5** - 概率变化、交易量、X 热度
3. **高概率机会 (>80%)** - 稳健套利候选
4. **价值投注 (40-60%)** - Edge 计算与推荐仓位
5. **鲸鱼动向** - 大额交易、聪明钱地址
6. **X/Twitter 热点** - 官方动态 + KOL 观点
7. **全网新闻** - 主流媒体 + Crypto 媒体
8. **风险提示** - 分辨率/流动性/时间风险
9. **明日关注** - 重大事件预告

### 周报结构
1. **本周核心摘要** - 周度数据 + 环比变化
2. **类别表现** - 政治/体育/财经/加密货币
3. **鲸鱼追踪** - 顶级交易者 PnL 排行
4. **KOL 观点汇总** - 核心观点 + 准确率
5. **深度分析** - 套利复盘 + 市场无效性
6. **策略复盘** - 上周推荐表现
7. **下周关注** - 重大事件 + 即将结算

---

## 🛠️ 手动生成流程

### Step 1: 运行脚本
```bash
# 日报
bash scripts/generate-daily-report.sh

# 周报
bash scripts/generate-weekly-report.sh
```

### Step 2: 编辑草稿
```bash
# 编辑 Markdown 草稿
code reports/daily/daily-20260308.md
```

**填充内容**:
- ✅ X 热点数据（脚本已自动抓取）
- ✅ 市场概率和交易量（Polymarket 官网）
- ✅ 鲸鱼地址和 PnL（Polymarket leaderboard）
- ✅ 新闻摘要（脚本已搜索）

### Step 3: 生成 HTML（自动）
脚本已自动完成 HTML 生成和推送，无需手动操作。

**输出位置**:
- `reports/daily/daily-YYYYMMDD.html` - 最终 HTML
- `reports/daily/daily-YYYYMMDD.md` - Markdown 草稿

**自动推送**:
```bash
# 脚本自动执行
git add reports/daily/daily-20260308.html
git commit -m "docs: 发布日报 2026-03-08"
git push origin main
```

Vercel 将自动部署（1-2 分钟）。

---

## 📱 数据源

| 数据源 | 用途 | 认证 |
|--------|------|------|
| **X/Twitter API** | KOL 动态、热点追踪 | ✅ 已配置 Cookie |
| **Google News** | 全网新闻聚合 | ✅ 无需认证 |
| **Polymarket API** | 市场数据、概率 | ✅ 无需认证 |
| **Jina AI** | 网页内容提取 | ✅ 无需认证 |

---

## 🔐 X 认证配置

当前使用 Cookie 认证（无需 API Key）：

```bash
# 查看配置
cat ~/.config/xfetch/session.json

# 更新 Cookie（如过期）
agent-reach configure twitter-cookies "auth_token=xxx; ct0=yyy"
```

---

## 📊 定时任务

```bash
# 查看已配置任务
crontab -l | grep polymarket
```

### 完整配置

```bash
# 日报：隔天 9:00 AM（自动生成并推送）
0 9 */2 * * bash ~/polymarket-reporter/scripts/generate-daily-report.sh

# 周报：周一 9:00 AM（自动生成并推送）
0 9 * * 1 bash ~/polymarket-reporter/scripts/generate-weekly-report.sh

# 知识库周更新：周日 14:00（收集内容，不推送）
0 14 * * 0 bash ~/polymarket-reporter/scripts/weekly-kb-update.sh

# 周日统一推送：周日 20:00（汇总并推送）
0 20 * * 0 bash ~/polymarket-reporter/scripts/weekly-batch-deploy.sh

# 网站周检：周一 9:00 AM
0 9 * * 1 bash ~/polymarket-reporter/scripts/weekly-health-check.sh
```

---

## 📁 文件结构

```
polymarket-reporter/
├── scripts/
│   ├── generate-daily-report.sh    # 日报生成（自动推送）
│   ├── generate-weekly-report.sh   # 周报生成（自动推送）
│   ├── weekly-kb-update.sh         # 知识库周更新（收集）
│   ├── weekly-batch-deploy.sh      # 周日统一推送
│   └── weekly-health-check.sh      # 周检脚本
├── templates/
│   ├── daily-report-template.html  # 日报 HTML 模板
│   └── weekly-report-template.html # 周报 HTML 模板（待创建）
├── reports/
│   ├── daily/
│   │   ├── daily-20260308.md       # Markdown 草稿
│   │   └── daily-20260308.html     # 最终 HTML
│   └── weekly/
│       ├── weekly-20260310.md
│       └── weekly-20260310.html
├── knowledge-base/
│   └── weekly-updates/             # 知识库周更新
│       ├── update-20260310.md
│       └── kol-summary-20260310.md
└── REPORTS.md                       # 本文档
```

---

## 🎯 改进方向

### 已实现
- ✅ X 热点自动抓取
- ✅ 全网新闻搜索
- ✅ Markdown 草稿生成
- ✅ 统一视觉模板

### 待实现
- ⏳ Markdown → HTML 自动转换
- ⏳ Polymarket API 数据自动填充
- ⏳ 鲸鱼 PnL 自动追踪
- ⏳ Telegram 自动推送

---

## 📞 故障排查

### X 抓取失败
```bash
# 检查认证
xreach --auth-token $AUTH_TOKEN --ct0 $CT0 tweets @Polymarket --json -n 1

# 更新 Cookie
agent-reach configure --from-browser chrome
```

### 定时任务未执行
```bash
# 检查 cron 状态
systemctl status cron

# 查看日志
tail ~/polymarket-reports/daily.log
```

---

*文档更新时间：2026-03-08*
