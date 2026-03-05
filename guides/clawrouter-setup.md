# ClawRouter 配置指南

> ClawRouter 是 OpenClaw 的原生 LLM 路由器，支持 41+ 模型，<1ms 延迟，通过 x402 在 Base 和 Solana 上用 USDC 支付。

## 目录

1. [简介](#1-简介)
2. [安装步骤](#2-安装步骤)
3. [钱包配置](#3-钱包配置)
4. [路由配置](#4-路由配置)
5. [使用示例](#5-使用示例)
6. [常见问题](#6-常见问题)

---

## 1. 简介

ClawRouter 是一个专为 AI Agent 设计的智能 LLM 路由系统：

- **100% 本地路由**：请求经过 15 维度加权评分系统，<1ms 延迟
- **零外部 API 调用**：所有路由决策在本地完成
- **多链支付**：支持 USDC on Base (EVM) 和 Solana
- **x402 支付协议**：非托管，每请求付费

### 核心特性

| 特性 | 说明 |
|------|------|
| 路由策略 | ECO / AUTO / PREMIUM / FREE |
| 模型数量 | 41+ 模型，7 个供应商 |
| 平均成本 | $2.05/M vs $25/M (Claude Opus) = 92% 节省 |
| 免费套餐 | gpt-oss-120b 完全免费 |

---

## 2. 安装步骤

### 2.1 一键安装

```bash
curl -fsSL https://blockrun.ai/ClawRouter-update | bash
openclaw gateway restart
```

安装过程中会自动：
- 生成钱包（Base 和 Solana）
- 配置本地代理（默认端口 8402）
- 启用智能路由

### 2.2 验证安装

```bash
openclaw status
```

确认 Gateway 运行正常。

---

## 3. 钱包配置

### 3.1 查看钱包

```bash
/wallet
```

输出示例：
```
Base 地址: 0x1234...abcd
Solana 地址: ABCD...XYZ
余额: $12.50 USDC
```

### 3.2 充值 USD

**Base (EVM)**：
- 发送 USDC 到你的 EVM 地址

**Solana**：
- 发送 USDC 到你的 Solana 地址

**建议**：$5 足够支持数千次请求。

### 3.3 切换链

```bash
/wallet solana    # 切换到 Solana
/wallet base      # 切换回 Base (EVM)
```

### 3.4 导出钱包（备份）

```bash
/wallet export
```

⚠️ **重要**：妥善保管导出的私钥和助记词！

---

## 4. 路由配置

### 4.1 路由策略

| 命令 | 策略 | 节省 | 适用场景 |
|------|------|------|----------|
| `/model auto` | 均衡（默认） | 74-100% | 通用使用 |
| `/model eco` | 最便宜 | 95-100% | 最大化节省 |
| `/model premium` | 最佳质量 | 0% | 关键任务 |
| `/model free` | 仅免费 | 100% | 零成本 |

### 4.2 路由层级

```
请求 → 15维度加权评分 → Tier 选择 → 最便宜模型 → 响应
```

| Tier | ECO | AUTO | PREMIUM |
|------|-----|------|---------|
| SIMPLE | nvidia/gpt-oss-120b (免费) | kimi-k2.5 | kimi-k2.5 |
| MEDIUM | gemini-2.5-flash-lite | grok-code-fast | gpt-5.2-codex |
| COMPLEX | gemini-2.5-flash-lite | gemini-3.1-pro | claude-opus-4.6 |
| REASONING | grok-4-fast | grok-4-fast | claude-sonnet-4.6 |

### 4.3 快捷命令

```bash
/model grok        # 使用 grok 模型
/model br-sonnet  # 使用 DeepSeek Sonnet
/model gpt5       # 使用 GPT-5
/model o3         # 使用 OpenAI O3
```

### 4.4 图像生成

```bash
/imagegen a dog dancing on the beach
/imagegen --model dall-e-3 a futuristic city at sunset
/imagegen --model banana-pro --size 2048x2048 mountain landscape
```

可用模型：

| 模型 | 价格 | 最大尺寸 |
|------|------|----------|
| nano-banana | $0.05/图 | 1024x1024 |
| banana-pro | $0.10/图 | 4096x4096 |
| dall-e-3 | $0.04/图 | 1792x1024 |
| gpt-image | $0.02/图 | 1536x1024 |
| flux | $0.04/图 | 1024x1024 |

---

## 5. 使用示例

### 5.1 基本使用

```bash
# 与默认模型对话 (AUTO)
openclaw

# 使用免费模型
/model free

# 使用最高质量模型
/model premium
```

### 5.2 代码任务

```bash
# 快速代码任务 (使用 ECO)
/model eco
帮我写一个 Python 脚本
```

### 5.3 复杂推理

```bash
# 复杂推理任务 (使用 PREMIUM)
/model premium
分析这个算法的复杂度...
```

### 5.4 查看统计

```bash
/stats
```

输出示例：
```
本月支出: $3.25
节省: 89%
请求数: 1,234
平均成本: $0.0026/请求
```

---

## 6. 常见问题

### Q1: 钱包余额不足怎么办？

```bash
/wallet
# 查看充值地址
```

向显示的地址充值 USDC。

### Q2: 路由不生效？

```bash
openclaw gateway restart
```

重启 Gateway 使配置生效。

### Q3: 如何诊断问题？

使用 doctor 命令：

```bash
npx @blockrun/clawrouter doctor
```

使用 Opus 进行深度分析：

```bash
npx @blockrun/clawrouter doctor opus
```

### Q4: 支持哪些模型？

41+ 模型，包括：

- **OpenAI**: GPT-4o, GPT-5.2, O1, O3
- **Anthropic**: Claude Opus, Claude Sonnet
- **Google**: Gemini 2.5 Pro, Gemini 3.1 Pro
- **xAI**: Grok 4
- **DeepSeek**: DeepSeek Chat, DeepSeek Reasoner

### Q5: 与 OpenRouter 相比有什么优势？

| 对比项 | OpenRouter | ClawRouter |
|--------|------------|------------|
| 设置 | 需要创建账户 | Agent 自动生成钱包 |
| 认证 | API Key | 钱包签名 |
| 支付 | 预付费（托管） | 每请求付费（非托管） |
| 路由 | 专有/闭源 | 开源，客户端 |
| 成本 | $25/M | $2.05/M |

---

## 配置变量参考

| 变量 | 默认值 | 说明 |
|------|--------|------|
| BLOCKRUN_WALLET_KEY | 自动生成 | 钱包私钥 |
| BLOCKRUN_PROXY_PORT | 8402 | 本地代理端口 |
| CLAWROUTER_DISABLED | false | 禁用智能路由 |
| CLAWROUTER_SOLANA_RPC_URL | https://api.mainnet-beta.solana.com | Solana RPC 端点 |

---

## 相关链接

- [ClawRouter 官方仓库](https://github.com/BlockRunAI/ClawRouter)
- [模型价格列表](https://blockrun.ai/models)
- [完整文档](https://blockrun.ai/docs)
- [Telegram 社区](https://t.me/blockrunAI)
- [X (Twitter)](https://x.com/BlockRunAI)

---

*最后更新：2026-03-05*