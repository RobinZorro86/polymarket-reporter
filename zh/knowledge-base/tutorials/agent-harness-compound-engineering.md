---
title: Agent Harness 架构与 Compound Engineering - 完整工作流对比
category: tutorials
type: AI 工程实践
difficulty: 🔴进阶
estimated_time: 40-60分钟
last_updated: 2026-03-29
original_source: https://x.com/xxx111god/status/2038086450013495554
author: Jason Zuo (@xxx111god)
related_links:
  - github.com/EveryInc/compound-engineering-plugin
  - github.com/garrytan/gstack
  - anthropic.com/engineering/effective-harnesses-for-long-running-agents
  - anthropic.com/engineering/harness-design-long-running-apps
---

# Agent Harness 架构与 Compound Engineering

**来源**: Jason Zuo (@xxx111god)  
**原文**: [一个从执行到记忆的完整 Agent Harness](https://x.com/xxx111god/status/2038086450013495554)  
**阅读价值**: ⭐⭐⭐⭐⭐（AI 工程实践深度文章）

---

## 一句话总结

> Agent 工作流的终极问题：每次工作学到的知识去哪了？Compound Engineering (CE) 解决了 Superpowers 没解决的知识积累问题——让 agent 越用越懂你的项目。

---

## Anthropic 的 Harness 架构

Anthropic 提出了让 agent 跨多个 context window 持续工作的核心框架，四个角色：

| 角色 | 功能 |
|------|------|
| **Planner agent** | 把大任务拆成 feature list |
| **Coding agent** | 每次只做一个 feature，做完留结构化笔记 |
| **Evaluator agent** | 独立审查（不让 builder 评价自己的工作）|
| **跨 session 桥接** | 用 progress file 传递上下文 |

**关键洞察**：Generator-evaluator 分离。Agent 评价自己的工作会过度乐观，把「做事」和「评价」分成两个独立 agent，效果显著提升。

**验证结果**：Anthropic 用这套架构让 agent 自主开发了完整的 claude.ai 克隆，200+ 可验证 feature。

---

## 三个工具深度对比

### 1. gstack — Planner + 浏览器 Evaluator

**作者**: @garrytan (YC CEO)

**做对了 harness 里两个角色**：
- `/plan-ceo-review` + `/plan-eng-review` = Planner agent（产品 + 架构视角）
- `/qa` = Evaluator agent（打开浏览器跑 staging URL，像真实用户一样测）

**哲学**：「Boil the Lake」——AI 时代做完整的事，边际成本趋近于零，永远做完整版。

**局限**：主要覆盖决策层和测试层，没有结构化增量执行 workflow，也没有知识积累机制。

---

### 2. Superpowers — 流程有了，深度不够

**Stars**: 120k（Claude Code 事实标配）

**流程**：brainstorm → plan → execute → review

**实现了** generator-evaluator 分离（独立的 spec-reviewer + code-quality-reviewer）

**三个深度差距**：

| 维度 | Superpowers | CE |
|------|-------------|-----|
| **Plan** | 当前 context 直接写 plan | 并行 spawn research agents，读历史 learnings、codebase pattern、git history |
| **Review** | 2 个 reviewer（spec + quality）| 6-15 个专项 reviewer 并行：correctness、security、performance、testing、maintainability、adversarial 等 |
| **知识积累** | **❌ 无** | **✅ /ce:compound** |

**最关键的问题**：做完就完了，下次 session 从零开始。

---

### 3. Compound Engineering (CE) — 完整的 Harness

**作者**: EveryInc  
**地址**: github.com/EveryInc/compound-engineering-plugin

**CE 覆盖所有 harness 角色，且更深**：

| 角色 | CE 对应 | 深度 |
|------|---------|------|
| Planner | `/ce:plan` | spawn research agents，读历史 learnings |
| Coding | `/ce:work` | 按 plan 增量执行 |
| Evaluator | `/ce:review` | 6-15 个专项 reviewer 并行 |
| 跨 session 桥接 | `/ce:compound` | **知识库，不是备忘录** |

---

## 核心：/ce:compound — 把工作变成知识

### 为什么这个命令重要

Anthropic 的 progress file 是**备忘录**：「上一班」交给「下一班」的交接单。

CE 的 docs/solutions/ 是**知识库**：所有 session 都能查的项目记忆。

```
备忘录：线性连续性（相邻 session）
知识库：指数积累性（所有 future session）
```

**这就是 "Compound" 的意思**：每次工作的产出不只是代码，还有下次能复用的知识。用得越久，agent 越懂你的项目。

---

### /ce:compound 的三个并行 Agent

```
Session 结束后跑 /ce:compound，并行 spawn 三个 agent：

Context Analyzer
→ 回溯整个 session 对话，提取问题类型、涉及组件、症状

Solution Extractor
→ 从 debug 过程提取：什么没用、什么管用、root cause、怎么预防

Related Docs Finder
→ 搜已有 docs/solutions/ 查重
  → 高度重复 → 更新旧文档
  → 新问题 → 新建文档
```

三个 agent 跑完后，orchestrator 汇总，写入 `docs/solutions/`。

**文档结构**：
```yaml
---
category: runtime
tags: [bug, edge-case, javascript]
---

# Problem
（一句问题描述）

# What Didn't Work
（排查过程中试了什么没用的）

# Solution
（最终解法和代码）

# Prevention
（以后怎么避免）
```

---

### 实际效果示例

你修了一个 edge runtime 兼容性 bug，compound 记录下来。

三周后做另一个功能碰到类似 runtime 问题：
- plan 阶段 agent 自动翻出那个 learning
- 直接标注：之前踩过的坑 + 解法
- **不再重复踩坑**

---

## /lfg 为什么手动 compound

/lfg（全自动模式：plan 到 PR 一条龙）里没有自动 compound。

**作者的选择是对的**：

不是每个 session 都值得 compound：
- 改个 typo ❌
- 调个 CSS ❌
- 跑个 migration ❌
- 真正 debug 了一个坑 ✅
- 发现了一个 pattern ✅
- 踩了一个雷 ✅

自动 compound 每个 session 会产生噪音，docs/solutions/ 被低价值文档淹没，learnings-researcher 搜索质量下降。

---

## compound janitor 方案（作者计划贡献 PR）

**问题**：人会忘记，应该自动判断哪些 session 值得 compound。

**方案**：
```
每天 end of day，自动扫当天所有 session 的：
- git diff
- conversation

判断哪些值得 compound（高价值 session）
janitor 筛选后，只 compound 有价值的
```

类似记忆管理中的定期 review 和清理机制。

---

## 完整 harness：gstack + CE

| 层级 | 工具 | 命令 |
|------|------|------|
| **决策层** | gstack | `/plan-ceo-review`（砍需求）|
| **决策层** | gstack | `/plan-eng-review`（锁架构）|
| **规划层** | CE | `/ce:plan`（spawn research agents）|
| **执行层** | CE | `/ce:work`（按 plan 增量执行）|
| **审查层** | CE | `/ce:review`（6-15 个专项 reviewer）|
| **审查层** | gstack | `/qa`（浏览器端到端实测）|
| **知识层** | CE | `/ce:compound`（写进可搜索知识库）|

**gstack 负责「做不做」和「真实测」**  
**CE 负责「怎么做」、「做得好不好」和「记住」**  
**没有重叠。**

---

## Superpowers 的优势

- 原生跨工具兼容：Claude Code、Cursor、Codex CLI 都能用
- 120k stars 验证了质量
- 很多人入门的最佳选择

**CE 最近加了 CLI 转换工具**，支持十几种格式——主力 Claude Code 的话，这个差距不重要。

---

## 最重要的问题

> 你的 agent 每天帮你写代码、改 bug、跑测试。做完之后，学到的东西去哪了？

如果答案是「散落在各个 session 里，下次再踩一遍」——

> /ce:compound 可能是你需要的那一行命令。

---

## 对知识库的启发

### AI 工具共享记忆（Runes Leo 方案 vs CE 方案）

| 方案 | 机制 | 特点 |
|------|------|------|
| **Runes Leo** | today.md symlink | 线性，连续两个 session |
| **CE /ce:compound** | docs/solutions/ 知识库 | 指数，所有 future session |

**CE 的方案更优**——知识积累是指数效应，不是线性备忘。

### 迁移价值

如果把 CE 的思路迁移到 Polymarket 研究 agent：
- 每次研究一个市场，记录：判断逻辑、EV 分析、结果复盘
- 知识库积累后，agent 研究新市场时自动翻出相关经验
- 不再重复同样的分析错误

---

## 链接资源

| 资源 | 地址 |
|------|------|
| **CE (Compound Engineering)** | github.com/EveryInc/compound-engineering-plugin |
| **gstack** | github.com/garrytan/gstack |
| **Anthropic Harness 博客 1** | anthropic.com/engineering/effective-harnesses-for-long-running-agents |
| **Anthropic Harness 博客 2** | anthropic.com/engineering/harness-design-long-running-apps |

---

**整理者**: Zorro-Research 🔍  
**用途**: AI 工程实践 / Agent 工作流 / 知识积累  
**版本**: 1.0  
**整理日期**: 2026-03-29
