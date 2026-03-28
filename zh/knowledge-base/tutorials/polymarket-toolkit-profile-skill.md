---
title: Polymarket Toolkit - AI Agent 开源画像工具
category: tools
type: 工具
difficulty: 🟢新手 / 🟡中级
estimated_time: 15-30分钟
last_updated: 2026-03-28
original_source: https://x.com/runes_leo/status/2037553424540287278
author: Leo (@runes_leo)
tool_url: https://github.com/runesleo/polymarket-toolkit
---

# Polymarket Toolkit - AI Agent 开源画像工具

**来源**: @runes_leo (Leo)  
**工具地址**: [github.com/runesleo/polymarket-toolkit](https://github.com/runesleo/polymarket-toolkit)  
**原文**: [装上这个 Skill，你的 AI 就能扒出 Polymarket 任意玩家的策略](https://x.com/runes_leo/status/2037553424540287278)  
**阅读价值**: ⭐⭐⭐⭐⭐（工具价值极高）

---

## 🎯 这是什么

一个**开源 AI Agent Skill**（只需一个 Markdown 文件），把任意 Polymarket 钱包地址丢进去，几秒钟生成完整的交易画像。

**核心特点**：
- 不要 API Key
- 不要数据库
- 不要服务器配置
- 公开 API + AI Agent 自己跑完整流程
- 支持 Claude Code、OpenClaw、Cursor，或任何能跑 shell 的 AI

---

## 安装方式

### 方式一：告诉 AI 一句话（最简单）

把文章或 GitHub 链接丢给你的 AI，说「帮我装一下这个 Polymarket 画像工具」，它会自动搞定。

### 方式二：手动两步

```bash
git clone https://github.com/runesleo/polymarket-toolkit.git
cp -R polymarket-toolkit/skills/polymarket-profile ~/.claude/skills/
```

### 使用方式

装好后，问你的 AI：

> 「帮我分析这个 Polymarket 地址：0x63ce342161250d705dc0b16df89036c8e5f9ba9a」

---

## 能拿到什么（输出内容）

| 输出项 | 说明 |
|--------|------|
| **盈亏总览** | 总 PnL + 7天/30天趋势 |
| **胜率** | 基于结算数据（不是估算） |
| **当前持仓** | 浮盈浮亏 |
| **交易行为分解** | TRADE / SPLIT / MERGE / REDEEM 各多少 |
| **品类分布** | Crypto、政治、体育、天气…… |
| **最大盈亏 Top 5** | 具体是哪些交易 |
| **策略模式自动识别** | 做市商、SPLIT套利、大户集中、分散投资…… |

---

## 技术架构：4 个公开 API

Skill 编排 4 个 Polymarket 公开 API：

| API | 用途 |
|-----|------|
| **lb-api** | PnL 和排行榜 |
| **data-api** | 持仓 + 完整交易历史（自动翻页）|
| **gamma-api** | 市场元数据 + 品类映射 |
| **CLOB API** | 实时 orderbook 价格 |

---

## 执行流程（7 步）

```
1. 拉取 PnL 快照（总量 + 7天/30天趋势）
2. 拉取当前持仓，计算胜率
3. 翻页拉取完整交易历史（处理 10K+ 条记录）
4. 通过 Gamma API 映射市场品类
5. 分析交易行为，识别策略模式
6. 排序最大盈亏
7. 组装完整画像输出
```

**用户名自动解析**——Agent 会自动搜索排行榜把用户名转换成地址，不需要手动查。

---

## 实战案例：从排行榜数据挖掘真实策略

### 案例 1：Politics #1 — 胜率高但总体亏钱

**地址**：How.Dare.You  
**数据**：92,398 条交易，1181 个市场，4.8 万次买入 + 4.3 万次卖出  
**策略**：广泛覆盖政治类市场，重仓乌克兰停火和 Trump 相关  
**胜率**：81%  
**总 PnL**：-$5.9 万

**结论**：赢得多但亏得狠，风控没跟上——高胜率 ≠ 赚钱。

---

### 案例 2：Culture #1 — SPLIT 套利闷声赚钱

**地址**：cynical.reason  
**自动识别模式**：SPLIT 套利型  
**数据**：$92.9 万 SPLIT + $112 万 MERGE，91 个市场  
**策略**：重仓 Fed 主席提名和伊朗局势——通过 SPLIT 创建 YES+NO 对，卖掉一边，另一边等结算或 MERGE 回来  
**总 PnL**：+$21 万

**结论**：光看交易记录根本看不出来这种策略，画像工具一跑就明白了。

---

### 案例 3：9 大品类本周第一名总览

| 品类 | PnL 冠军 | 特征 |
|------|---------|------|
| Crypto | — | volume 是 PnL 的 170 倍，高频交易 |
| 天气 | — | $4,123 利润 / $58,441 volume，利润薄 |
| 综合 | 与体育相同 | — |
| 政治 | How.Dare.You | 81% 胜率但总亏 |
| Culture | cynical.reason | SPLIT 套利，闷声赚 |

---

## 路线图

### 分析工具（规划中）

| 工具 | 功能 |
|------|------|
| **PnL 计算器** | 持仓级盈亏拆解 |
| **Brier Score 评分** | 地址预测质量打分 |
| **交易风格标签** | 保守 / 激进 / 事件驱动分类 |

### 市场情报（规划中）

| 工具 | 功能 |
|------|------|
| **市场扫描器** | 按品类、成交量、流动性发现市场 |
| **流动性仪表盘** | Spread、深度、做市商集中度分析 |
| **LP 激励扫描** | 发现活跃的流动性激励计划 |

### 追踪 & 预警（规划中）

| 工具 | 功能 |
|------|------|
| **排行榜追踪** | 每日快照、排名变化、连胜检测 |
| **大户异动** | 头部玩家仓位变化提醒 |

### API（规划中）

所有工具的 REST API，供接入自己的应用。

---

## 为什么是 Skill 而不是 App？

传统工具需要：前端 + 服务器 + 数据库

Skill 只需要：一个 Markdown 文件，写清楚指令，AI Agent 读完自己执行。

**优势**：
- 零基建
- 任何能跑 curl 的大模型都能用
- 想改随便改（开源）
- 持续更新（路线图丰富）

---

## 对知识库的意义

### 可直接整合到现有工作流

| 现有内容 | 整合方式 |
|---------|---------|
| **KOL 研究** | 分析 KOL 钱包地址，验证推文里说的策略是否真实 |
| **LP 策略** | 追踪 LP 高手的持仓和策略模式 |
| **套利研究** | 分析套利者的真实 PnL，验证 lqp2021 的 6 模型是否有效 |
| **跟单学习** | 找到真正赚钱的钱包，不是只看排行榜表面数据 |

### 立刻能做的事

1. **验证 KOL 说法**：KOL 说自己赚了 X，用工具验证
2. **找值得跟的钱包**：不只是看 PnL 高，要看策略是否可复制
3. **理解 SPLIT/MERGE 套利**：把抽象策略变成具体数据
4. **补充知识库**：把分析结果沉淀成案例

---

## 快速使用检查表

```
□ 装好 polymarket-profile skill
□ 找一个 Polymarket 地址（排行榜 / KOL 推文 / 朋友推荐）
□ 问 AI：「帮我分析这个地址：0x...」
□ 拿到画像后，记录：
  - PnL 是多少？
  - 胜率是多少？
  - 策略模式是什么？
  - 适合跟单吗？
□ 定期追踪自己关注的钱包变化
```

---

## 原文链接

- **GitHub**: [github.com/runesleo/polymarket-toolkit](https://github.com/runesleo/polymarket-toolkit)
- **推文**: [https://x.com/runes_leo/status/2037553424540287278](https://x.com/runes_leo/status/2037553424540287278)
- **作者**: Leo (@runes_leo) | [leolabs.me](https://leolabs.me/)

---

**整理者**: Zorro-Research 🔍  
**用途**: 钱包分析 / 策略验证 / 跟单学习  
**版本**: 1.0  
**整理日期**: 2026-03-28
