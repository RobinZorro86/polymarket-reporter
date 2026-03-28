---
title: 如何构建 Polymarket 体育预测 Bot - 完整教程
category: tutorials
type: 技术教程
difficulty: 🔴进阶
estimated_time: 45-60分钟（深度阅读）
last_updated: 2026-03-29
original_source: https://x.com/Skaly__Bull/status/2037516601331769778
author: Skaly_Bull (@Skaly__Bull)
---

# 如何构建 Polymarket 体育预测 Bot - 完整教程

**来源**: @Skaly__Bull (Skaly_Bull)  
**原文**: [How to Build a Sports Prediction Bot for Polymarket](https://x.com/Skaly__Bull/status/2037516601331769778)  
**阅读价值**: ⭐⭐⭐⭐⭐（技术深度极高的实战教程）

---

## 🎯 这是什么

一个完整的 **Polymarket 体育预测 Bot 构建方案**：
- 6 个体育专项 Agent 并行运行
- AI 新闻分析 + XGBoost 概率预测
- 实时信号 → 执行套利闭环
- 核心公式：`P_agent − P_market = Edge`

**实测结果**：NBA Agent，5 天，23 笔交易，21 胜 / 2 负。

---

## 核心架构：一个体育 = 一个 Agent

**不要做一个通吃的 Bot。** 每个体育有不同数据、时间和信号，专属 Agent 比通用型更快更准。

| Agent | 数据源 | 信号 |
|-------|--------|------|
| **NBA** | basketball-reference.com | Woj + Shams 伤病报告 |
| **UFC** | ufcstats.com | 称重结果、击中数据 |
| **NFL** | pro-football-reference.com | 伤病报告 + 天气 |
| **Soccer** | StatsBomb + API-Football | 阵容泄露、转会 |
| **College Football** | sports-reference.com | 招募排名、主客场 |
| **Tennis** | tennisabstract.com | 场地胜率、疲劳度 |

所有 Agent 共享同一个执行层（Polygon + Polymarket API），但各自有独立数据管道和训练模型。

---

## 的大脑：AI 层

### 两类 AI 组件

**新闻和文本分析**：
```
Claude API (Anthropic) → 结构化 JSON 输出
{ player, team, impact_direction, urgency_score }

GPT-4o → 备选，处理混乱无格式文本
```

**概率预测**：
```
XGBoost / LightGBM → 基于历史数据训练
每个 Agent 有自己的模型——NBA 模型不懂 UFC，这是故意的
```

### 新闻 → 信号 Pipeline

```
原始文本 → Claude API → 影响评分 → 对比 Polymarket 价格
→ 市场尚未反应 → 执行交易
```

---

## 各体育数据源详解

### NBA Agent

**数据源**：basketball-reference.com  
**历史数据**：背靠背赛程、主客场分割、H2H 近 3 赛季、pace、进攻效率

### UFC Agent

**数据源**：ufcstats.com  
**数据项**：风格对决、完成率、臂展和身体数据、称重历史、连胜纪录

### NFL Agent

**数据源**：pro-football-reference.com  
**数据项**：ATS 历史、天气数据、红区效率、失误差异

### Soccer Agent

**数据源**：StatsBomb + API-Football  
**数据项**：xG 历史、阵容轮换模式、UCL vs 国内联赛状态、交手记录

### College Football Agent

**数据源**：sports-reference.com  
**数据项**：招募排名、主场优势（在 NCAAF 中巨大）、联盟记录、赛程强度

### Tennis Agent

**数据源**：tennisabstract.com  
**数据项**：场地-specific 胜率、发球统计、交手记录、赛事疲劳（上次比赛距今天数）

**数据库**：所有数据存入 PostgreSQL——一个数据库，每个体育独立表。

---

## 新闻监控：Alpha 层

### 各体育新闻源

| 体育 | 新闻源 | 关键信号 |
|------|--------|---------|
| **NBA** | Woj + Shams、ESPN RSS、Rotowire | 赛前 1 小时官方伤病报告 |
| **UFC** | 称重结果、媒体日片段、MMA Fighting RSS | 称重失误 = 立即 -15% 胜率 |
| **NFL** | 官方伤病报告（周三/四/五）、天气 API | 风速 > 20mph 压制得分 |
| **Soccer** | 俱乐部 X 阵容泄露、BBC Sport RSS、Fabrizio Romano | 赛前 1 小时阵容 |
| **College Football** | 24/7 Sports、各项目当地记者 | 官方 Athletic 部门账号 |
| **Tennis** | ATP/WTA 抽签、发布会记录、tennisabstract | 疲劳和伤病提及 |

**核心洞察**：官方伤病报告是 NBA 博彩市场中最大的单一 Alpha 来源。

---

## 实时数据：各 Agent 信号

| 体育 | 实时信号 |
|------|---------|
| **NBA** | 球星犯规麻烦、8-0 冲击波、pace 转移、最后 5 分钟投篮热区 |
| **UFC** | 每回合显著击中数、摔倒防御%、伤害累积、回合评分 |
| **NFL** | 红区持球链、时间差、QB 被压率 |
| **Soccer** | xG 累积、施压强度下降、GPS 疲劳信号、战术换人 |
| **College Football** | 失误动量、主场人群噪音影响、4 档决策信号 |
| **Tennis** | 破发转化率、一发% 、每局动量、盘间恢复时间 |

**实时数据源**：Sportradar API——覆盖所有体育、WebSocket 推送、行业标准。

---

## 实测验证：NBA Agent

**结果**：5 天，23 笔交易，**21 胜 / 2 负**

- Agent 扫描 Woj、Shams、ESPN 伤病线
- 在 Polymarket 赔率变动前捕捉 12-20 秒窗口
- 赛前盘、盘中、临关单均有入场

> ⚠️ 过往表现不保证未来结果。

---

## 决策逻辑：所有 Agent 统一公式

```
Agent 获取实时数据 + 新闻信号
        ↓
模型计算 P(win)
        ↓
获取当前 Polymarket 价格
        ↓
Edge = P_agent − P_market
        ↓
Edge > 5% → 执行
Edge < 5% → 跳过
```

每个 Agent 在 live 赛事期间每 2 秒运行一次这个循环。**5% 阈值过滤噪音**——低于此，手续费和方差会吃掉利润。

---

## 执行层：跨 Agent 共享

| 组件 | 工具 |
|------|------|
| Polymarket SDK | `py-clob-client`（官方 Python SDK）|
| 交易签名与广播 | `web3.py` |
| Polygon 节点 | **私有 RPC**（Alchemy 或 QuickNode，比公开节点快 3-5 秒，对延迟套利至关重要）|
| Gas | 始终 overpay（50+ gwei）保证优先区块打包 |

所有 6 个 Agent 共享一个 Polygon 钱包 + USDC。

---

## 风险管理：按 Agent 隔离，非全局

**一个糟糕的 UFC 夜晚不会烧掉 NBA 的资金。**

| 规则 | 参数 |
|------|------|
| 每 Agent 每笔最大仓位 | 分配资金的 **1%** |
| 每 Agent 日损失上限 | **3%** |
| 最低 Edge 阈值 | **5%**（低于跳过）|
| 最小流动性要求 | $5,000+ |
| 连续 3 笔亏损 | **自动暂停**该 Agent |
| 市场关闭前入场限制 | **< 2 分钟**不入场 |

---

## 构建顺序：从 1 个 Agent 开始

### Weeks 1-2：搭建第一个 Agent

**推荐从 NBA 或 UFC 开始**

1. 设置新闻监控
2. 连接 Claude API 做 NLP
3. 爬取历史数据
4. 训练 XGBoost 模型

### Week 3：Paper Trading

1. 通过 `py-clob-client` 连接 Polymarket CLOB API
2. 全流程跑，不投入真钱
3. 记录每条信号和理论交易
4. **验证 Edge 是真实的再入金**

### Week 4：上线

1. 部署在美国 VPS
2. 连接私有 RPC
3. 从最小资金开始
4. 所有交易存入 PostgreSQL

### Month 2

克隆架构，调整数据源，Launch 第二 Agent。

### Month 3+

添加 Soccer、Tennis、NFL、College Football——6 个并行运行在同一执行层。

---

## 核心公式速查

```
Edge = P_agent − P_market

Edge > 5% → 执行
Edge < 5% → 跳过

单笔最大仓位 = 分配资金 × 1%
日损失上限 = 分配资金 × 3%
连续 3 亏 = 暂停

私有 RPC > 公开节点（快 3-5 秒）
```

---

## 对 Polymarket 知识库的意义

### 技术层面

- **体育市场是最适合预测的市场**：数据丰富、新闻源清晰、信号可量化
- **多 Agent 并行架构**：比单一 Bot 更高效、更专注
- **5% Edge 阈值**：实际可行的过滤标准

### 知识库补充

| 已有内容 | 补充方向 |
|---------|---------|
| **lqp2021 套利 6 模型** | 这篇是体育专项版——具体体育数据 + 新闻监控 |
| **runes-leo 25 策略尸检** | 体育 Bot 策略和这套架构可以交叉验证 |
| **Kropanchik/Franky LP 教程** | 体育 Bot ≠ LP，两者互补 |

### 普通人的借鉴

即使不做 Bot，也能借鉴：
- **5% Edge 过滤噪音**的思维
- **按体育分 Agent** 的专业化思路
- **实时信号**对盘口的影响逻辑

---

## 原文信息

- **作者**：Skaly_Bull (@Skaly__Bull)
- **GitHub**：待补充（原文未提供）
- **相关项目**：polymarket-toolkit（runes_leo）、py-clob-client

---

**整理者**: Zorro-Research 🔍  
**用途**: 体育 Bot / 实时信号 / AI 预测架构  
**版本**: 1.0  
**整理日期**: 2026-03-29
